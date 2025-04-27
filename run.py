import argparse
import pathlib
import time

from loguru import logger
from urllib3.exceptions import ProxyError
from requests.exceptions import ConnectionError
from http.client import RemoteDisconnected

from src.database import initialize_db, load_posts, save_posts
from src.scraper import scrape_posts
from src.utils import discord_webhook

parser = argparse.ArgumentParser()
parser.add_argument(
    "--webhook-url",
    type=str,
    required=False,
    help="Discord Webhook URL",
    default=None,
)
parser.add_argument(
    "--board-name",
    type=str,
    required=True,
    help="PTT board name",
)
parser.add_argument(
    "--author",
    type=str,
    required=True,
    help="Author to scrape",
)

args = parser.parse_args()
webhook_url: str | None = args.webhook_url
if webhook_url is None:
    logger.info("No webhook URL provided, will skip Discord notification")

board_name, author = (args.board_name, args.author)

file_path = pathlib.Path(f"databases/{author}_{board_name}_posts.db")
log_path = pathlib.Path(f"logs/{author}_{board_name}.log")
logger.add(log_path, rotation="1 day", retention="14 days", level="INFO")


def main() -> None:
    logger.info("Start scraping")
    initialize_db(file_path)

    posts = scrape_posts(
        f"https://www.ptt.cc/bbs/{board_name}/search?q=author%3A{author}"
    )
    logger.info(f"Found {len(posts)} posts from {author} on PTT")

    current_posts = load_posts(file_path)
    logger.info(f"Found {len(current_posts)} posts in database")

    saved_posts = save_posts(posts, file_path)
    logger.info(f"Saved {len(saved_posts)} posts")

    if webhook_url is not None:
        for post in saved_posts:
            discord_webhook(post.notify_str, url=webhook_url)

    logger.info("Scraping finished")


if __name__ == "__main__":
    start = time.time()
    try:
        main()
    except (ProxyError, ConnectionError, RemoteDisconnected):
        pass
    except Exception as e:
        logger.exception(e)
        discord_webhook(f"錯誤: {type(e)} {e}", url=args.webhook_url)
    logger.info(f"Execution time: {time.time() - start:.2f} seconds")
