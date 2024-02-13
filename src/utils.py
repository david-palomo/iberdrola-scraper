from datetime import datetime, timedelta


def get_dates_between(start_date: str, end_date: str) -> list[str]:
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    ndays = (end - start).days + 1

    return [str((start + timedelta(days=i)).date()) for i in range(ndays)]
