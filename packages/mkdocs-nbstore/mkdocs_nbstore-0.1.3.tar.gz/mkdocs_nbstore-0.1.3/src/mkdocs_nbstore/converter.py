from __future__ import annotations

from typing import TYPE_CHECKING

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
            yield from convert_image(image, store)


def convert_image(image: Image, store: Store) -> Iterator[str | Image]:
    if "source" in image.classes:
        image.classes.remove("source")
        yield from get_source(image, store)

    try:
        mime_content = store.get_mime_content(image.src, image.identifier)
    except Exception:  # noqa: BLE001
        yield image.markdown
    else:
        if mime_content:
            image.set_mime_content(*mime_content)
            yield image


def get_source(image: Image, store: Store) -> Iterator[str]:
    if source := store.get_source(image.src, image.identifier):
        language = store.get_language(image.src)
        yield f"```{language}\n{source}\n```\n\n"
