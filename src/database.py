from __future__ import annotations

import pathlib
import sqlite3
import textwrap

from .scraper import get_post_content
from .schema import Post


def initialize_db(db_path: pathlib.Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                title TEXT,
                date TEXT,
                content TEXT
            )
            """
        )
        conn.commit()


def load_posts(db_path: pathlib.Path) -> list[Post]:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, date, content FROM posts")
        rows = cursor.fetchall()
        return [
            Post(url=row[0], title=row[1], date=row[2], content=row[3]) for row in rows
        ]


def get_post(post_url: str, db_path: pathlib.Path) -> Post | None:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT url, title, date, content FROM posts WHERE url = ?", (post_url,)
        )
        row = cursor.fetchone()
        return (
            Post(url=row[0], title=row[1], date=row[2], content=row[3]) if row else None
        )


def save_posts(posts_to_save: list[Post], db_path: pathlib.Path) -> list[Post]:
    saved_posts = []
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for post in posts_to_save:
            if get_post(post.url, db_path) is None:
                post.content = textwrap.shorten(get_post_content(post.url), 1000)
                cursor.execute(
                    "INSERT INTO posts (url, title, date, content) VALUES (?, ?, ?, ?)",
                    (post.url, post.title, post.date, post.content),
                )
                saved_posts.append(post)
        conn.commit()
    return saved_posts
