from __future__ import annotations

import uuid
from pathlib import Path
from typing import TYPE_CHECKING

from mkdocs.config import Config, config_options
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.files import File
from nbstore.store import Store

from .converter import convert

if TYPE_CHECKING:
    from typing import Any

    from mkdocs.config.defaults import MkDocsConfig
    from mkdocs.structure.files import Files
    from mkdocs.structure.pages import Page


class NbstoreConfig(Config):
    """Configuration for Nbstore plugin."""

    notebook_dir = config_options.Type(str, default=".")


logger = get_plugin_logger("mkdocs-nbstore")


class NbstorePlugin(BasePlugin[NbstoreConfig]):
    store: Store
    files: Files

    def on_config(self, config: MkDocsConfig, **kwargs: Any) -> MkDocsConfig:
        path = (Path(config.docs_dir) / self.config.notebook_dir).resolve()
        self.store = Store(path)
        config.watch.append(path.as_posix())
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
            elif image.content is not None:
                src = f"{uuid.uuid4()}{image.mime}"
                src_uri = (Path(page.file.src_uri).parent / src).as_posix()
                file = File.generated(config, src_uri, content=image.content)
                self.files.append(file)
                image.src = src
                markdowns.append(str(image))

        return "".join(markdowns)
