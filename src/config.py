import argparse
from datetime import datetime, timedelta
import logging
import os
import re


def valid_date(s: str) -> str:
    if not re.match(r"\d{4}-\d{2}-\d{2}", s):
        raise ValueError("Not a valid date: {s!r}")
    return s


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Notifies if consumption for a given date exceeds a threshold.",
        epilog="Requires Selenium Grid or Chrome WebDriver installed.",
    )

    parser.add_argument(
        "-u",
        "--username",
        default=os.getenv("USERNAME"),
        help="User (email) for i-DE. Required!",
    )
    parser.add_argument(
        "-p",
        "--password",
        default=os.getenv("PASSWORD"),
        help="Password for i-DE. Required!",
    )
    parser.add_argument(
        "-d",
        "--date",
        default=os.getenv(
            "DATE", (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        ),
        type=valid_date,
        help="Date in YYYY-MM-DD format",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        default=float(os.getenv("THRESHOLD", "0.0")),
        type=float,
        help="Threshold in kWh",
    )
    parser.add_argument(
        "-n",
        "--ntfy-url",
        default=os.getenv("NTFY_URL"),
        help="NTFY Topic URL (e.g. https://ntfy.sh/mytopic)",
    )
    parser.add_argument(
        "-r",
        "--retries",
        default=int(os.getenv("RETRIES", 2)),
        type=int,
        help="Number of retries in case of timeout. Default: 2",
    )
    parser.add_argument(
        "--local-driver",
        action="store_true",
        help="Use local Chrome WebDriver instead of Selenium Grid",
    )
    parser.add_argument(
        "--remote-driver-url",
        default=os.getenv("REMOTE_DRIVER_URL", "http://localhost:4444"),
        help="Selenium Grid URL. Default: http://localhost:4444",
    )
    parser.add_argument(
        "--log-level",
        default=os.getenv("LOG_LEVEL", "INFO"),
        choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
    )
    parser.add_argument(
        "--log-format",
        default=os.getenv("LOG_FORMAT", "%(asctime)s - %(levelname)s - %(message)s"),
        help="Python logging format",
    )

    args = parser.parse_args()

    if not args.username or not args.password:
        parser.error("Username and password are required.")

    if not args.ntfy_url:
        logging.warning("No NTFY URL provided. Notifications will be disabled.")

    return args
