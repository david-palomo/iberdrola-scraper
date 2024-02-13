import logging
import os
from datetime import datetime, timedelta
from tap import Tap


class Config(Tap):
    "Get daily consumption data from i-DE and send a notification."

    username: str = os.getenv("USERNAME", "")  # i-DE username (email)
    password: str = os.getenv("PASSWORD", "")  # i-DE password
    ntfy_url: str = os.getenv("NTFY_URL", "")  # e.g. https://ntfy.sh/mytopic

    _default_date = str(datetime.now().date() - timedelta(days=1))

    start_date: str = os.getenv("START_DATE", _default_date)
    end_date: str = os.getenv("END_DATE", _default_date)
    alert_threshold: float = float(os.getenv("ALERT_THRESHOLD", "inf"))  # kWh
    driver_url: str = os.getenv("DRIVER_URL", "http://localhost:4444")  # Selenium URL
    retries: int = int(os.getenv("RETRIES", 3))
    retry_delay: int = int(os.getenv("RETRY_DELAY", 60))  # seconds
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    info_title: str = os.getenv("INFO_TITLE", "i-DE: Consumption info")
    info_tag: str = os.getenv("INFO_TAG", "green_circle")
    alert_title: str = os.getenv("ALERT_TITLE", "i-DE: Consumption alert!")
    alert_tag: str = os.getenv("ALERT_TAG", "red_circle")
    error_title: str = os.getenv("ERROR_TITLE", "i-DE: Error running script!")
    error_tag: str = os.getenv("ERROR_TAG", "warning")

    def process_args(self):
        if not self.username or not self.password:
            exit("Username and password are required.")

        try:
            datetime.strptime(self.start_date, "%Y-%m-%d")
            datetime.strptime(self.end_date, "%Y-%m-%d")
        except ValueError:
            exit("Incorrect date format, should be YYYY-MM-DD.")

    def warn_args(self):
        if not self.ntfy_url:
            logging.warn("No NTFY URL provided. Notifications will be disabled.")

        if self.alert_threshold == float("inf"):
            logging.info("No alert threshold provided. All notifications will be INFO.")
