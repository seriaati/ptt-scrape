import time

from dotenv import load_dotenv
from loguru import logger

from src.database import load_posts, save_posts
from src.scraper import AUTHOR_NAME, scrape_posts
from src.utils import line_notify


def main() -> None:
    logger.info("Start scraping")
    load_dotenv()

    posts = scrape_posts()
    logger.info(f"Found {len(posts)} posts from {AUTHOR_NAME} on PTT")

    current_posts = load_posts()
    logger.info(f"Found {len(current_posts)} posts in database")

    saved_posts = save_posts(posts, current_posts)
    logger.info(f"Saved {len(saved_posts)} posts")

    for post in saved_posts:
        line_notify(post.notify_str)

    logger.info("Scraping finished")


if __name__ == "__main__":
    logger.add("log.log", rotation="1 day", retention="7 days", level="INFO")
    start = time.time()
    main()
    logger.info(f"Execution time: {time.time() - start:.2f} seconds")
