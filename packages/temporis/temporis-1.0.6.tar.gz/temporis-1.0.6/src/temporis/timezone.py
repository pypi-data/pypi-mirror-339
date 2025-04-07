import zoneinfo
from datetime import datetime

import pytz

from src.temporis.zones import TemporisZone


class TemporisTz:
    """
    A class to handle timezone-related operations.
    """

    __tz_utc = None

    def __init__(self, tz_info: str = TemporisZone.OTHER.UTC):
        """
        Initializes the TemporisTz class with the given timezone information.

        Parameters:
        -----------
        tz_info : str
            The timezone information to use (default is TemporisZone.OTHER.UTC).
        """
        self.tz_info = zoneinfo.ZoneInfo(tz_info)
        self._pytz_info = pytz.timezone(tz_info)

    def now(self):
        """
        Returns the current date and time in the specified timezone.

        Returns:
        --------
        datetime
            The current date and time in the specified timezone.
        """
        return datetime.now(self.tz_info)

    def apply(self, dt: datetime):
        """
        Converts the given datetime object to the specified timezone.

        Parameters:
        -----------
        dt : datetime
            The datetime object to convert.

        Returns:
        --------
        datetime
            The converted datetime object in the specified timezone.
        """
        return dt.astimezone(self._pytz_info)

    def replace(self, dt: datetime):
        """
        Replaces the timezone information of the given datetime object with the specified timezone.

        Parameters:
        -----------
        dt : datetime
            The datetime object to modify.

        Returns:
        --------
        datetime
            The datetime object with the replaced timezone information.
        """
        return self.localize(dt.replace(tzinfo=None))

    def localize(self, dt: datetime):
        """
        Localizes the given naive datetime object to the specified timezone.

        Parameters:
        -----------
        dt : datetime
            The naive datetime object to localize.

        Returns:
        --------
        datetime
            The localized datetime object in the specified timezone.
        """
        return self._pytz_info.localize(dt)

    @classmethod
    def to_UTC(cls, dt):
        """
        Converts the given datetime object to UTC timezone.

        Parameters:
        -----------
        dt : datetime
            The datetime object to convert.

        Returns:
        --------
        datetime
            The converted datetime object in UTC timezone.
        """
        return dt.astimezone(zoneinfo.ZoneInfo(TemporisZone.OTHER.UTC))
