import requests


def ntfy(
    ntfy_url: str, title: str, message: str, priority: int, tags=""
) -> requests.Response:
    return requests.post(
        ntfy_url,
        message,
        headers={
            "Title": title,
            "Priority": str(priority),
            "Tags": tags,
        },
    )
