import argparse
import pathlib
import time

from loguru import logger

from src.database import initialize_db, load_posts, save_posts
from src.scraper import scrape_posts
from src.utils import discord_webhook

parser = argparse.ArgumentParser()
parser.add_argument(
    "--webhook-url",
    type=str,
    required=True,
    help="Discord Webhook URL",
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
webhook_url, board_name, author = (args.webhook_url, args.board_name, args.author)

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

    for post in saved_posts:
        discord_webhook(post.notify_str, url=webhook_url)

    logger.info("Scraping finished")


if __name__ == "__main__":
    start = time.time()
    try:
        main()
    except Exception as e:
        logger.exception(e)
        discord_webhook(f"錯誤: {e}", url=args.webhook_url)
    logger.info(f"Execution time: {time.time() - start:.2f} seconds")
