import os
import shutil
import sys
from pathlib import Path

import pytest
from mkdocs.commands.build import build
from mkdocs.config import load_config
from mkdocs.config.defaults import MkDocsConfig

from mkdocs_nbstore.plugin import NbstoreConfig, NbstorePlugin


@pytest.fixture(scope="module")
def config_file():
    return Path(__file__).parent.parent / "mkdocs.yaml"


def test_config_file_exists(config_file: Path):
    assert config_file.exists()


@pytest.fixture(scope="module")
def mkdocs_config(config_file: Path):
    return load_config(str(config_file))


@pytest.fixture(scope="module")
def nbstore_plugin(mkdocs_config: MkDocsConfig):
    return mkdocs_config.plugins["mkdocs-nbstore"]


def test_nbstore_plugin(nbstore_plugin: NbstorePlugin):
    assert isinstance(nbstore_plugin, NbstorePlugin)
    assert isinstance(nbstore_plugin.config, NbstoreConfig)


@pytest.fixture(scope="module")
def nbstore_config(nbstore_plugin: NbstorePlugin):
    return nbstore_plugin.config


def test_nbstore_config(nbstore_config: NbstoreConfig):
    config = nbstore_config
    assert config.notebook_dir == "../notebooks"


@pytest.fixture
def config_plugin(tmp_path):
    dest = Path(tmp_path)
    root = Path(__file__).parent.parent
    config_file = root / "mkdocs.yaml"
    shutil.copy(config_file, dest)
    for src in ["docs", "notebooks", "src", "tests"]:
        src_dir = root / src
        shutil.copytree(src_dir, dest / src)
    curdir = Path(os.curdir).absolute()
    os.chdir(dest)
    sys.path.insert(0, ".")
    config = load_config("mkdocs.yaml")
    plugin = config.plugins["mkdocs-nbstore"]
    assert isinstance(plugin, NbstorePlugin)
    plugin.__init__()

    yield config, plugin

    config.plugins.on_shutdown()
    sys.path.pop(0)
    os.chdir(curdir)


def test_on_config(config_plugin: tuple[MkDocsConfig, NbstorePlugin]):
    config, plugin = config_plugin
    plugin.on_config(config)
    assert plugin.store is not None


@pytest.fixture
def config(config_plugin):
    return config_plugin[0]


def test_build(config: MkDocsConfig):
    config.plugins.on_startup(command="build", dirty=False)
    plugin = config.plugins["mkdocs-nbstore"]
    assert isinstance(plugin, NbstorePlugin)

    build(config, dirty=False)
