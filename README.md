# Iberdrola i-DE Scraper

A Selenium scraper that logs into the Iberdrola i-DE website, scrapes the energy consumption for a given date-range,
and then sends a NTFY notification with the results.

## Requirements

You will need to have a Selenium Grid server running.
You can use the provided docker-compose.yaml file to start one up locally, by running:

```bash
docker-compose up -d
```

After that, you can either use Docker to build a container and run it,
or use pipenv to install the dependencies and run the script.

## Option A. Run using Docker

Create a .env file following the template of the .env.example file, filling at least the required environment
variables: i-DE `USERNAME`, i-DE `PASSWORD`, and `NTFY_URL` (that is, if you want to receive notifications).
Then, build the Docker image and run it:

```bash
docker build -t iberdrola-scraper .
docker run --network host --env-file .env iberdrola-scraper
```

## Option B. Run using pipenv

If using pipenv, you can configure the script either by:
- Filling in the .env file as described in the previous option (setting at least `USERNAME`, `PASSWORD`, and `NTFY_URL`).
- Passing parameters to the script via command line arguments, when running it (see `pipenv run python -m src --help`).

In any case, you would need to:

```bash
pipenv install
pipenv run python -m src [args]
```

## Possible configuration parameters

You can see this same configuration in the .env.example file, or by running the script with the `--help` flag.
The available parameters that can be configured are:

#### Required

- `USERNAME`: Your email for the Iberdrola i-DE website.
- `PASSWORD`: Your password for the Iberdrola i-DE website.
- `NTFY_URL`: The NTFY server URL with the topic to which notifications will be sent. It can be the public instance (https://ntfy.sh/[topic-name]) or self-hosted (http[s]://[yourdomain]:[port]/[topic-name]).

#### Optional

- `START_DATE`: The start date for the scraping period. Defaults to 'yesterday'.
- `END_DATE`: The end date for the scraping period. Defaults to 'yesterday'.
- `ALERT_THRESHOLD`: The alert threshold as a float. Defaults to 'inf'.
- `DRIVER_URL`: The URL of the Selenium Grid driver. Defaults to 'http://localhost:4444'.
- `RETRIES`: The number of retries in case of failure. Defaults to '3'.
- `RETRY_DELAY`: The delay between retries in seconds. Defaults to '60'.
- `LOG_LEVEL`: The log level. Defaults to 'INFO'.

#### Customization

- `INFO_TITLE`: The title for the information notifications.
- `INFO_TAG`: The tag for the information notifications.
- `ALERT_TITLE`: The title for the alert notifications.
- `ALERT_TAG`: The tag for the alert notifications.
- `ERROR_TITLE`: The title for the error notifications.
- `ERROR_TAG`: The tag for the error notifications.
