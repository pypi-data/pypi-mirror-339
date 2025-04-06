from __future__ import annotations

from typing import TYPE_CHECKING

from .logger import logger
from .markdown import iter_images

if TYPE_CHECKING:
    from collections.abc import Iterator

    from nbstore.store import Store

    from .image import Image


def convert(markdown: str, store: Store) -> Iterator[str | Image]:
    for image in iter_images(markdown):
        if isinstance(image, str):
            yield image
        else:
            try:
                yield from convert_image(image, store)
            except ValueError:
                logger.warning(f"Could not convert {image.url}#{image.identifier}")
                yield image.markdown


def convert_image(image: Image, store: Store) -> Iterator[str | Image]:
    if image.pop(".source"):
        yield from get_source(image, store)
        return

    if image.pop(".cell"):
        yield from get_source(image, store)

    if mime_content := store.get_mime_content(image.url, image.identifier):
        yield image.convert(*mime_content)


def get_source(image: Image, store: Store) -> Iterator[str]:
    if source := store.get_source(image.url, image.identifier):
        language = store.get_language(image.url)
        yield f"```{{.{language}{image.attr}}}\n{source}\n```\n\n"
