import requests


def discord_webhook(content: str, *, url: str) -> None:
    requests.post(url, json={"content": content})
