from loguru import logger
import requests


def discord_webhook(content: str, *, url: str) -> None:
    resp = requests.post(url, json={"content": content})
    logger.info(f"Discord webhook response: {resp.status_code} {resp.text}")
