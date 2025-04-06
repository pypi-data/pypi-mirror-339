from __future__ import annotations

import shlex


class Image:
    alt: str
    src: str
    identifier: str
    classes: list[str]
    attributes: dict[str, str]
    markdown: str
    mime: str | None
    content: bytes | str | None

    def __init__(self, alt: str, src: str, attrs: str) -> None:
        self.alt = alt
        self.src = src
        self.identifier = ""
        self.classes = []
        self.attributes = {}
        self.markdown = f"![{alt}]({src}){{{attrs}}}"
        self.mime = None
        self.content = None

        for attr in shlex.split(attrs):
            if attr.startswith("#"):
                self.identifier = attr[1:]
            elif attr.startswith("."):
                self.classes.append(attr[1:])
            elif "=" in attr:
                key, value = attr.split("=", 1)
                self.attributes[key] = value

    def set_mime_content(self, mime: str, content: bytes | str) -> None:
        self.mime = mime
        self.content = content

    def __str__(self) -> str:
        attrs = [f"#{self.identifier}"] if self.identifier else []
        attrs.extend(f".{cls}" for cls in self.classes)
        attrs.extend(f"{k}={shlex.quote(v)}" for k, v in self.attributes.items())
        attr = f"{{{' '.join(attrs)}}}" if attrs else ""
        return f"![{self.alt}]({self.src}){attr}"
