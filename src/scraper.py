from __future__ import annotations
import os
import textwrap

import requests
from bs4 import BeautifulSoup
from loguru import logger
from dotenv import load_dotenv
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from urllib3.exceptions import ProxyError
from http.client import RemoteDisconnected
from requests.exceptions import ConnectionError

from .schema import Post

load_dotenv()
PROXY = os.getenv("PROXY")

proxies = {"http": PROXY, "https": PROXY}


@retry(
    retry=retry_if_exception_type((ProxyError, RemoteDisconnected, ConnectionError)),
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    reraise=True,
)
def fetch_content(url: str) -> str:
    logger.info(f"[GET] {url}")
    return requests.get(
        url, headers={"User-Agent": "Mozilla/5.0"}, proxies=proxies
    ).text


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


def scrape_posts(url: str) -> list[Post]:
    content = fetch_content(url)
    soup = BeautifulSoup(content, "lxml")
    posts: list[Post] = []
    rents = soup.find_all("div", class_="r-ent")

    for rent in rents:
        title = rent.find("div", class_="title").text.strip()
        date = rent.find("div", class_="date").text.strip()
        url = rent.find("div", class_="title").a["href"]

        post = Post(url=url, title=title, date=date, content="")
        posts.append(post)

    return posts
