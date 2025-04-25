from pydantic import BaseModel


class Post(BaseModel):
    url: str
    title: str
    date: str
    content: str

    @property
    def notify_str(self) -> str:
        return f"\n# {self.title}\n-# 發布於 {self.date}\n<https://www.ptt.cc{self.url}>\n{self.content}"
