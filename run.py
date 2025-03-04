import argparse
import pathlib
import time

from loguru import logger

from src.database import load_posts, save_posts
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
    "--url",
    type=str,
    required=True,
    help="PTT board url",
)
parser.add_argument(
    "--author",
    type=str,
    required=True,
    help="Author to scrape",
)
args = parser.parse_args()


def main() -> None:
    logger.info("Start scraping")
    file_path = pathlib.Path(f"{args.author}_{args.url.split('/')[-2]}.json")

    posts = scrape_posts(args.url, author_name=args.author)
    logger.info(f"Found {len(posts)} posts from {args.author} on PTT")

    current_posts = load_posts(file_path)
    logger.info(f"Found {len(current_posts)} posts in database")

    saved_posts = save_posts(posts, current_posts, file_path)
    logger.info(f"Saved {len(saved_posts)} posts")

    for post in saved_posts:
        discord_webhook(post.notify_str, url=args.webhook)

    logger.info("Scraping finished")


if __name__ == "__main__":
    logger.add("log.log", rotation="1 day", retention="7 days", level="INFO")
    start = time.time()
    main()
    logger.info(f"Execution time: {time.time() - start:.2f} seconds")
