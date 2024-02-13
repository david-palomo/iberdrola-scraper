import json
import logging
import os
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def start_remote_driver(driver_url) -> Remote:
    logging.info("Starting Remote WebDriver...")
    try:
        return Remote(driver_url, options=ChromeOptions())
    except Exception as e:
        raise ConnectionError(f"Can't connect to Selenium at {driver_url}: {e!r}")


def get_consumption(
    start_date: str, end_date: str, driver_url="http://localhost:4444"
) -> dict:
    url = "https://www.i-de.es/consumidores"
    driver = start_remote_driver(driver_url)

    try:
        logging.info("Getting the login page...")
        driver.get(f"{url}/web/guest/login")

        try:
            driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        except NoSuchElementException:
            logging.info("No cookies banner found, continuing...")

        driver.find_element(By.ID, "mat-input-0").send_keys(os.getenv("USERNAME"))
        driver.find_element(By.ID, "mat-input-1").send_keys(os.getenv("PASSWORD"))
        driver.find_element(By.XPATH, '//div[@class="enter-button"]//button').click()

        logging.info("Form submitted! Waiting for login to complete...")
        try:
            WebDriverWait(driver, 25).until(EC.url_contains("dashboard"))
            time.sleep(5)
        except TimeoutException:
            raise TimeoutError("Login timeout exceeded!")

        logging.info("Getting consumption data...")
        sd = "-".join(reversed(start_date.split("-")))
        ed = "-".join(reversed(end_date.split("-")))
        driver.get(f"{url}/rest/consumoNew/obtenerDatosConsumoDH/{sd}/{ed}/dias/USU/")

        body = driver.find_element(By.TAG_NAME, "body").text
        logging.info(f"Got raw data: {body!r}")

        assert all(s not in body for s in ["error", "WU1"]), f"Error response: {body!r}"

        data = json.loads(body)[0]

        assert isinstance(data, dict) and "total" in data, f"Got invalid data: {data!r}"
        assert data["total"] is not None, f"Got no data for {start_date} - {end_date}"

        return data

    finally:
        driver.quit()
