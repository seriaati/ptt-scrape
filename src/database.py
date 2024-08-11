from __future__ import annotations

import json
from typing import TYPE_CHECKING

from .schema import Post

if TYPE_CHECKING:
    import pathlib


def load_posts(file_path: pathlib.Path) -> list[Post]:
    if not file_path.exists():
        return []
    with open(file_path, encoding="utf-8") as f:
        return [Post(**post) for post in json.load(f)]


def get_post(posts: list[Post], post_url: str) -> Post | None:
    for post in posts:
        if post.url == post_url:
            return post
    return None


def save_posts(
    posts_to_save: list[Post], current_posts: list[Post], file_path: pathlib.Path
) -> list[Post]:
    posts_to_save = [post for post in posts_to_save if get_post(current_posts, post.url) is None]
    current_posts.extend(posts_to_save)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump([post.model_dump() for post in current_posts], f, ensure_ascii=False, indent=2)

    return posts_to_save
