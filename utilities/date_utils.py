# =========================================================
# Date Utilities - Date Formatting and Manipulation
# =========================================================
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DateUtils:

    @staticmethod
    def get_current_date(format="%Y-%m-%d"):

        date = datetime.now().strftime(format)

        logger.info(f"Current date: {date}")

        return date

    @staticmethod
    def get_current_datetime(
        format="%Y-%m-%d %H:%M:%S"
    ):

        dt = datetime.now().strftime(format)

        logger.info(f"Current datetime: {dt}")

        return dt

    @staticmethod
    def get_current_timestamp():

        return datetime.now().strftime(
            "%Y%m%d%H%M%S"
        )

    @staticmethod
    def get_future_date(
        days=30,
        format="%Y-%m-%d"
    ):

        future = (
            datetime.now()
            + timedelta(days=days)
        ).strftime(format)

        logger.info(
            f"Future date ({days} days): {future}"
        )

        return future

    @staticmethod
    def get_past_date(
        days=30,
        format="%Y-%m-%d"
    ):

        past = (
            datetime.now()
            - timedelta(days=days)
        ).strftime(format)

        logger.info(
            f"Past date ({days} days): {past}"
        )

        return past

    @staticmethod
    def get_current_month():

        return datetime.now().month

    @staticmethod
    def get_current_year():

        return datetime.now().year

    @staticmethod
    def format_date(
        date_string,
        from_format,
        to_format
    ):

        dt = datetime.strptime(
            date_string,
            from_format
        )

        return dt.strftime(to_format)