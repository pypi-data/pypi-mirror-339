from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta


class Temporis:
    """
    A class for various date and time operations.
    """

    @staticmethod
    def get_current_datetime() -> datetime:
        """Returns the current date and time."""
        return datetime.now()

    @staticmethod
    def get_current_date() -> date:
        """Returns the current date."""
        return Temporis.get_current_datetime().date()

    @staticmethod
    def to_str(dt: datetime | date, format_str: str) -> str:
        """Converts a datetime or date object to a string based on the given format."""
        return dt.strftime(format_str)

    @staticmethod
    def from_str(date_str: str, format_str: str) -> datetime:
        """Parses a string to a datetime object based on the given format."""
        return datetime.strptime(date_str, format_str)

    @staticmethod
    def add_seconds(dt: datetime, seconds: int) -> datetime:
        """Adds a specified number of seconds to a datetime object."""
        return dt + timedelta(seconds=seconds)

    @staticmethod
    def add_minutes(dt: datetime, minutes: int) -> datetime:
        """Adds a specified number of minutes to a datetime object."""
        return dt + timedelta(minutes=minutes)

    @staticmethod
    def add_hours(dt: datetime, hours: int) -> datetime:
        """Adds a specified number of hours to a datetime object."""
        return dt + timedelta(hours=hours)

    @staticmethod
    def add_days(dt: datetime, days: int) -> datetime:
        """Adds a specified number of days to a datetime object."""
        return dt + timedelta(days=days)

    @staticmethod
    def add_months(dt: datetime, months: int) -> datetime:
        """Adds a specified number of months to a datetime object."""
        return dt + relativedelta(months=1)

    @staticmethod
    def next_business_day(dt: datetime, holidays: list[date] = []) -> datetime:
        """
        Returns the next business day, skipping weekends and holidays.

        Parameters:
        -----------
        dt : datetime
            The starting date.
        holidays : list[date], optional
            A list of holiday dates to skip (default is an empty list).
        """
        while True:
            dt = Temporis.add_days(dt, 1)
            if Temporis.is_business_day(dt, holidays):
                return dt

    @staticmethod
    def next_quarter(dt: datetime) -> datetime:
        """Returns the start date of the next quarter."""
        current_quarter = (dt.month - 1) // 3
        return dt.replace(month=current_quarter * 3 + 4)

    @staticmethod
    def next_semester(dt: datetime) -> datetime:
        """Returns the start date of the next semester."""
        current_semester = (dt.month - 1) // 6
        return dt.replace(month=current_semester * 6 + 7)

    @staticmethod
    def next_year(dt: datetime) -> datetime:
        """Returns the start date of the next year."""
        return dt.replace(day=1, month=1, year=dt.year + 1)

    @staticmethod
    def previous_business_day(dt: datetime, holidays: list[date] = []) -> datetime:
        """
        Returns the previous business day, skipping weekends and holidays.

        Parameters:
        -----------
        dt : datetime
            The starting date.
        holidays : list[date], optional
            A list of holiday dates to skip (default is an empty list).
        """
        while True:
            dt = Temporis.add_days(dt, -1)
            if Temporis.is_business_day(dt, holidays):
                return dt

    @staticmethod
    def first_business_day_of_month(
        dt: datetime, holidays: list[date] = []
    ) -> datetime:
        """
        Returns the first business day of the month, skipping holidays.

        Parameters:
        -----------
        dt : datetime
            The starting date.
        holidays : list[date], optional
            A list of holiday dates to skip (default is an empty list).
        """
        dt = Temporis.first_day_of_month(dt)
        if not Temporis.is_business_day(dt, holidays):
            return Temporis.next_business_day(dt, holidays)
        return dt

    @staticmethod
    def last_business_day_of_month(dt: datetime, holidays: list[date] = []) -> datetime:
        """
        Returns the last business day of the month, skipping holidays.

        Parameters:
        -----------
        dt : datetime
            The starting date.
        holidays : list[date], optional
            A list of holiday dates to skip (default is an empty list).
        """
        dt = Temporis.last_day_of_month(dt)
        if not Temporis.is_business_day(dt, holidays):
            return Temporis.previous_business_day(dt, holidays)
        return dt

    @staticmethod
    def is_business_day(dt: datetime, holidays: list[date] = []) -> bool:
        """
        Checks if a date is a business day, excluding weekends and holidays.

        Parameters:
        -----------
        dt : datetime
            The date to check.
        holidays : list[date], optional
            A list of holiday dates to skip (default is an empty list).

        Returns:
        --------
        bool
            True if the date is a business day, False otherwise.
        """
        return not Temporis.is_weekend(dt) and not Temporis.is_holiday(dt, holidays)

    @staticmethod
    def is_weekend(dt: datetime) -> bool:
        """
        Checks if a date falls on a weekend.

        Parameters:
        -----------
        dt : datetime
            The date to check.

        Returns:
        --------
        bool
            True if the date is a weekend, False otherwise.
        """
        return dt.weekday() in [5, 6]

    @staticmethod
    def is_holiday(dt: datetime, holidays: list[date]) -> bool:
        """
        Checks if a date is a holiday.

        Parameters:
        -----------
        dt : datetime
            The date to check.
        holidays : list[date]
            A list of holiday dates.

        Returns:
        --------
        bool
            True if the date is a holiday, False otherwise.
        """
        return dt.date() in holidays

    @staticmethod
    def first_day_of_month(dt: datetime) -> datetime:
        """
        Returns the first day of the month.

        Parameters:
        -----------
        dt : datetime
            The date to modify.

        Returns:
        --------
        datetime
            The first day of the month.
        """
        return dt.replace(day=1)

    @staticmethod
    def last_day_of_month(dt: datetime) -> datetime:
        """
        Returns the last day of the month.

        Parameters:
        -----------
        dt : datetime
            The date to modify.

        Returns:
        --------
        datetime
            The last day of the month.
        """
        return dt.replace(day=1, month=dt.month + 1) - timedelta(days=1)

    @staticmethod
    def count_days_between(start: datetime, end: datetime) -> int:
        """
        Counts the number of days between two dates.

        Parameters:
        -----------
        start : datetime
            The start date.
        end : datetime
            The end date.

        Returns:
        --------
        int
            The number of days between the start and end dates.
        """
        return (end - start).days
