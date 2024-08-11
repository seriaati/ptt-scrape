# type: ignore[reportOptionalMemberAccess]
from __future__ import annotations

from typing import Final

import requests
from bs4 import BeautifulSoup
from loguru import logger

from .schema import Post

URL: Final[str] = "https://www.ptt.cc/bbs/home-sale/index4999.html"
AUTHOR_NAME: Final[str] = "ceca"


def fetch_content(url: str) -> str:
    logger.info(f"[GET] {url}")
    return requests.get(url).text


def get_post_content(url: str) -> str:
    content = fetch_content(f"https://www.ptt.cc{url}")
    soup = BeautifulSoup(content, "lxml")
    main_content = soup.find("div", id="main-content")
    for meta in main_content.find_all("div", class_="article-metaline"):
        if meta is None:
            continue
        meta.extract()
    meta_right = main_content.find("div", class_="article-metaline-right")
    if meta_right is not None:
        meta_right.extract()
    return main_content.text


def scrape_posts() -> list[Post]:
    content = fetch_content(URL)
    soup = BeautifulSoup(content, "lxml")
    posts: list[Post] = []
    rents = soup.find_all("div", class_="r-ent")

    for rent in rents:
        author = rent.find("div", class_="author").text.strip()
        if author != AUTHOR_NAME:
            continue

        title = rent.find("div", class_="title").text.strip()
        date = rent.find("div", class_="date").text.strip()
        url = rent.find("div", class_="title").a["href"]

        post = Post(url=url, title=title, date=date, content=get_post_content(url))
        posts.append(post)

    return posts
