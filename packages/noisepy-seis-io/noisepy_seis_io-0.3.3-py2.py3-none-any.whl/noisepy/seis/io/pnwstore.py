import io
import logging
import os
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from typing import Callable, List, Tuple

import obspy
from datetimerange import DateTimeRange

from .channelcatalog import ChannelCatalog
from .datatypes import Channel, ChannelData, ChannelType, Station
from .stores import RawDataStore
from .utils import fs_join, get_filesystem

logger = logging.getLogger(__name__)


class PNWDataStore(RawDataStore):
    """
    A data store implementation to read from a SQLite DB of metadata and a directory of data files
    """

    def __init__(
        self,
        path: str,
        db_file: str,
        chan_catalog: ChannelCatalog,
        chan_filter: Callable[[Channel], bool] = None,
        date_range: DateTimeRange = None,
    ):
        """
        Parameters:
            path: path to look for ms files. Can be a local file directory or an s3://... url path
            db_file: path to the sqlite DB file
            chan_catalog: ChannelCatalog to retrieve inventory information for the channels
            chan_filter: Optional function to decide whether a channel should be used or not,
                            if None, all channels are used
            date_range: Optional date range to filter the data
        """
        super().__init__()
        self.fs = get_filesystem(path)
        self.chan_catalog = chan_catalog
        self.path = path
        self.db_file = db_file
        self.paths = {}
        # to store a dict of {timerange: list of channels}
        self.channels = {}
        if chan_filter is None:
            chan_filter = lambda s: True  # noqa: E731

        if date_range is None:
            self._load_channels(self.path, chan_filter)
        else:
            dt = date_range.end_datetime - date_range.start_datetime
            for d in range(0, dt.days):
                date = date_range.start_datetime + timedelta(days=d)
                date_path = str(date.year) + "/" + str(date.timetuple().tm_yday).zfill(3) + "/"
                full_path = fs_join(self.path, date_path)
                self._load_channels(full_path, chan_filter)

    def _load_channels(self, full_path: str, chan_filter: Callable[[Channel], bool]):
        # The path should look like: .../UW/2020/125/
        parts = full_path.split(os.path.sep)
        assert len(parts) >= 4
        net, year, doy = parts[-4:-1]
        cmd = (
            f"SELECT DISTINCT network, station, channel, location, filename "
            f"FROM tsindex WHERE filename LIKE '%%/{net}/{year}/{doy}/%%' "
            "AND (channel LIKE '_H_' OR channel LIKE '_N_') "
        )

        # if network is speficied, query will be faster
        if net != "__":
            cmd += f" AND network = '{net}'"
        else:
            logging.warning("Data path contains wildcards. Channel query might be slow.")
        rst = self._dbquery(cmd)
        for i in rst:
            timespan = PNWDataStore._parse_timespan(os.path.basename(i[4]))
            self.paths[timespan.start_datetime] = full_path
            channel = PNWDataStore._parse_channel(i)
            if not chan_filter(channel):
                continue
            key = str(timespan)
            if key not in self.channels:
                self.channels[key] = [channel]
            else:
                self.channels[key].append(channel)

    def get_channels(self, date_range: DateTimeRange) -> List[Channel]:
        tmp_channels = self.channels.get(str(date_range), [])
        executor = ThreadPoolExecutor()
        stations = set(map(lambda c: c.station, tmp_channels))
        _ = list(executor.map(lambda s: self.chan_catalog.get_inventory(date_range, s), stations))
        logger.info(f"Getting {len(tmp_channels)} channels for {date_range}")
        return list(executor.map(lambda c: self.chan_catalog.get_full_channel(date_range, c), tmp_channels))

    def get_timespans(self) -> List[DateTimeRange]:
        return list([DateTimeRange.from_range_text(d) for d in sorted(self.channels.keys())])

    def read_data(self, timespan: DateTimeRange, chan: Channel) -> ChannelData:
        assert (
            timespan.start_datetime.year == timespan.end_datetime.year
        ), "Did not expect timespans to cross years"
        year = timespan.start_datetime.year
        doy = str(timespan.start_datetime.timetuple().tm_yday).zfill(3)

        rst = self._dbquery(
            f"SELECT byteoffset, bytes "
            f"FROM tsindex WHERE network='{chan.station.network}' AND station='{chan.station.name}' "
            f"AND channel='{chan.type.name}' and location='{chan.station.location}' "
            f"AND filename LIKE '%%/{chan.station.network}/{year}/{doy}/%%'"
            "ORDER BY byteoffset ASC"
        )

        if len(rst) == 0:
            logger.warning(f"Could not find file {timespan}/{chan} in the database")
            return ChannelData.empty()
        elif len(rst) > 10:
            # skip if stream has more than 10 gaps
            logger.warning(f"Too many gaps (>10) from {timespan}/{chan}")
            return ChannelData.empty()

        # reconstruct the file name from the channel parameters
        chan_str = f"{chan.station.name}.{chan.station.network}.{timespan.start_datetime.strftime('%Y.%j')}"
        filename = fs_join(
            self.paths[timespan.start_datetime].replace("__", chan.station.network), f"{chan_str}"
        )
        if not self.fs.exists(filename):
            logger.warning(f"Could not find file {filename}")
            return ChannelData.empty()

        stream = obspy.Stream()
        with self.fs.open(filename, "rb") as f:
            for byteoffset, bytes in rst:
                f.seek(byteoffset)
                buff = io.BytesIO(f.read(bytes))
                stream += obspy.read(buff)
        return ChannelData(stream)

    def get_inventory(self, timespan: DateTimeRange, station: Station) -> obspy.Inventory:
        return self.chan_catalog.get_inventory(timespan, station)

    def _parse_timespan(filename: str) -> DateTimeRange:
        # The PNWStore repository stores files in the form: STA.NET.YYYY.DOY
        # YA2.UW.2020.366
        year = int(filename.split(".")[2])
        day = int(filename.split(".")[3])
        jan1 = datetime(year, 1, 1, tzinfo=timezone.utc)
        return DateTimeRange(jan1 + timedelta(days=day - 1), jan1 + timedelta(days=day))

    def _parse_channel(record: tuple) -> Channel:
        # e.g.
        # YA2.UW.2020.366
        network = record[0]
        station = record[1]
        channel = record[2]
        location = record[3]
        c = Channel(
            ChannelType(channel, location),
            # lat/lon/elev will be populated later
            Station(network, station, location=location),
        )
        return c

    def _dbquery(self, query: str) -> List[Tuple]:
        db = sqlite3.connect(self.db_file)
        cursor = db.cursor()
        rst = cursor.execute(query)
        all = rst.fetchall()
        db.close()
        return all
