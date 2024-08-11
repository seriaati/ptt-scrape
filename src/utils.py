import os

import requests


def line_notify(message: str) -> None:
    token = os.environ.get("LINE_NOTIFY_TOKEN")
    if token is None:
        msg = "LINE_NOTIFY_TOKEN is not set"
        raise ValueError(msg)

    requests.post(
        "https://notify-api.line.me/api/notify",
        headers={"Authorization": f"Bearer {token}"},
        data={"message": message},
    )
