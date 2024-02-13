import logging
import traceback
import time

from src.config import Config
from src.scraping import get_consumption_data
from src.notify import ntfy


def main():
    args = Config().parse_args()

    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=args.log_level, format=log_format)
    logging.info(f"Getting consumption data for {args.date}...")

    args.warn_args()

    try:
        for i in range(1 + args.retries):
            try:
                data = get_consumption_data(args.date, args.selenium_driver_url)
                logging.info(data)

                total = int(data["total"]) / 1000
                msg = f"{args.date}: {total} kWh"

                if total > args.alert_threshold:
                    resp = ntfy(args.ntfy_url, args.alert_title, msg, 5, args.alert_tag)
                else:
                    resp = ntfy(args.ntfy_url, args.info_title, msg, 3, args.info_tag)

                logging.info(f"NTFY response: {resp.status_code}")
                break

            except Exception as e:
                if i == args.retries:
                    raise

                logging.error(f"{e}. Will retry in {args.retry_delay}s...")
                time.sleep(args.retry_delay)

    except Exception as e:
        logging.error(traceback.format_exc())

        resp = ntfy(args.ntfy_url, args.error_title, f"{e!r}", 3, args.error_tag)
        logging.info(f"Notification sent: {resp.status_code}")


if __name__ == "__main__":
    main()
