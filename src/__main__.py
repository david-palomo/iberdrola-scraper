import logging
import requests
import time
import traceback

from src.config import parse_args
from src.scraping import create_driver, get_consumption_data


def notify(ntfy_url, title, message, tags="") -> requests.Response:
    requests.post(ntfy_url, message, headers={"Title": title, "Tags": tags})


def main():
    args = parse_args()
    logging.basicConfig(level=args.log_level, format=args.log_format)

    logging.info("Starting Selenium WebDriver...")
    driver = create_driver(args.local_driver, args.remote_driver_url)
    try:
        logging.info(f"Getting consumption data for {args.date}...")

        for _ in range(1 + args.retries):
            try:
                data = get_consumption_data(driver, args.date)
                break
            except Exception as e:
                time.sleep(60)
                logging.warning(f"{e}. Retrying...")

        logging.info(data)
        total = int(data["total"])

        if total > args.threshold:
            message = f"Total for {args.date}: {total} kWh"
            notify(args.ntfy_url, "i-DE Consumption Alert", message, "warning")

    except Exception as e:
        logging.error(traceback.format_exc())
        notify(args.ntfy_url, "i-DE Script Failed", f"{e!r}", "rotating_light")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
