import zoneinfo

import pytz
from temporis.temporis import datetime
from temporis.zones import TemporisZone


class TemporisTz:
    __tz_utc = None

    def __init__(self, tz_info: str = TemporisZone.OTHER.UTC):
        self.tz_info = zoneinfo.ZoneInfo(tz_info)
        self._pytz_info = pytz.timezone(tz_info)

    def now(self):
        return datetime.now(self.tz_info)

    def apply(self, dt: datetime):
        return dt.astimezone(self._pytz_info)

    def replace(self, dt: datetime):
        return self.localize(dt.replace(tzinfo=None))

    def localize(self, dt: datetime):
        return self._pytz_info.localize(dt)

    @classmethod
    def to_UTC(cls, dt):
        return dt.astimezone(zoneinfo.ZoneInfo(TemporisZone.OTHER.UTC))
