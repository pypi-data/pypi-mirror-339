from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from mkdocs.config import Config, config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File
from nbstore.store import Store

from .converter import convert
from .logger import logger

if TYPE_CHECKING:
    from typing import Any

    from mkdocs.config.defaults import MkDocsConfig
    from mkdocs.structure.files import Files
    from mkdocs.structure.pages import Page

    from .image import Image


class NbstoreConfig(Config):
    """Configuration for Nbstore plugin."""

    notebook_dir = config_options.Type(str, default=".")


class NbstorePlugin(BasePlugin[NbstoreConfig]):
    store: Store
    files: Files

    def on_config(self, config: MkDocsConfig, **kwargs: Any) -> MkDocsConfig:
        path = (Path(config.docs_dir) / self.config.notebook_dir).resolve()
        self.store = Store(path)
        config.watch.append(path.as_posix())

        _update_extensions(config)

        return config

    def on_files(self, files: Files, config: MkDocsConfig, **kwargs: Any) -> Files:
        self.files = files
        return files

    def on_page_markdown(
        self,
        markdown: str,
        page: Page,
        config: MkDocsConfig,
        **kwargs: Any,
    ) -> str:
        markdowns = []
        for image in convert(markdown, self.store):
            if isinstance(image, str):
                markdowns.append(image)

            elif image.content:
                for file in generate_files(image, page.file.src_uri, config):
                    self.files.append(file)
                markdowns.append(image.markdown)

        return "".join(markdowns)


def generate_files(image: Image, page_uri: str, config: MkDocsConfig) -> list[File]:
    src_uri = (Path(page_uri).parent / image.src).as_posix()

    info = f"{image.url}#{image.identifier} ({image.mime}) -> {src_uri}"
    logger.debug(f"Creating image: {info}")

    file = File.generated(config, src_uri, content=image.content)
    return [file]


def _update_extensions(config: MkDocsConfig) -> None:
    for name in ["attr_list"]:
        if name not in config.markdown_extensions:
            config.markdown_extensions.append(name)
