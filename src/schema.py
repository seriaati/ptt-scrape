from pydantic import BaseModel


class Post(BaseModel):
    url: str
    title: str
    date: str
    content: str

    @property
    def notify_str(self) -> str:
        return f"\nhttps://www.ptt.cc{self.url}\n標題: {self.title}\n發布於: {self.date}\n{self.content}"
