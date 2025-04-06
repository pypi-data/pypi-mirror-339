from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self


@dataclass
class Image:
    alt: str
    """The alternative text for the image."""

    url: str
    """The Notebook URL of the image."""

    identifier: str
    """The identifier of the image."""

    attr: str
    """The attributes of the image."""

    mime: str = ""
    """The MIME type of the image."""

    content: bytes | str = ""
    """The content of the image."""

    src: str = ""
    """The source URI of the image in MkDocs."""

    def __contains__(self, attr: str) -> bool:
        return attr in self.attr.split(" ")

    def pop(self, attr: str, default: str | None = None) -> str | None:
        if attr not in self:
            return default

        self.attr = " ".join(x for x in self.attr.split(" ") if x != attr)
        return attr

    def convert(self, mime: str, content: bytes | str) -> Self | str:
        if mime.startswith("text/") and isinstance(content, str):
            return content

        self.mime = mime
        self.content = content
        self.src = f"{uuid.uuid4()}.{get_suffix(mime)}"
        return self

    @property
    def markdown(self) -> str:
        src = self.src or self.url
        return f"![{self.alt}]({src}){{#{self.identifier}{self.attr}}}"


def get_suffix(mime: str) -> str:
    return mime.split("/")[1].split("+")[0]
