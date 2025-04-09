from pydantic import BaseModel


class News(BaseModel):
    title: str | None = None
    subtitle: str | None = None
    content: str | None = None
    author: str | None = None

    def __str__(self) -> str:
        return "\n".join(
            [
                f"# {self.title}",
                self.subtitle,
                f"Author: {self.author}",
                "## Content",
                self.content,
            ]
        )
