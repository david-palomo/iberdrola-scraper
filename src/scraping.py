import json
import logging
import os
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import Remote, Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep


def create_driver(local=False, remote_url: str = "http://localhost:4444"):
    return Chrome() if local else Remote(remote_url, options=ChromeOptions())


def get_consumption_data(driver, date: str, login_timeout=20) -> dict:
    url = "https://www.i-de.es/consumidores"

    logging.info("Getting the login page...")
    driver.get(f"{url}/web/guest/login")

    try:
        driver.find_element(By.ID, "onetrust-reject-all-handler").click()
    except NoSuchElementException:
        pass

    driver.find_element(By.ID, "mat-input-0").send_keys(os.getenv("USERNAME"))
    driver.find_element(By.ID, "mat-input-1").send_keys(os.getenv("PASSWORD"))
    driver.find_element(By.XPATH, '//div[@class="enter-button"]//button').click()

    logging.info("Form submitted! Waiting for login to complete...")
    try:
        WebDriverWait(driver, login_timeout).until(EC.url_contains("dashboard"))
        sleep(5)
    except TimeoutException:
        raise TimeoutError("Login timeout exceeded!")

    logging.info("Getting consumption data...")
    date = "-".join(reversed(date.split("-")))
    driver.get(f"{url}/rest/consumoNew/obtenerDatosConsumoDH/{date}/{date}/dias/USU/")

    body = driver.find_element(By.TAG_NAME, "body").text
    logging.info(f"Got raw data: {body!r}")

    assert all(s not in body for s in ["error", "WU1"]), f"Error response: {body!r}"

    data = json.loads(body)[0]

    assert isinstance(data, dict) and "total" in data, f"Got invalid data: {data!r}"
    assert data["total"] is not None, f"Data for {date} not available!"

    return data
