import re

SOURCE = """\
![a](b.ipynb){#c}

```
![d](e.ipynb){#f}
```
"""


def test_iter_images_internal():
    from mkdocs_nbstore.markdown import _iter_images

    it = _iter_images(SOURCE)

    m = next(it)
    assert isinstance(m, re.Match)
    assert m.group("src") == "b.ipynb"
    assert m.group("attr") == "#c"

    m = next(it)
    assert m == (17, 19)
    assert SOURCE[m[0] : m[1]] == "\n\n"

    m = next(it)
    assert m == (19, 44)
    assert SOURCE[m[0] : m[1]] == "```\n![d](e.ipynb){#f}\n```"

    m = next(it)
    assert m == (44, 45)
    assert SOURCE[m[0] : m[1]] == "\n"


def test_iter_images():
    from mkdocs_nbstore.image import Image
    from mkdocs_nbstore.markdown import iter_images

    it = iter_images(SOURCE)

    m = next(it)
    assert isinstance(m, Image)
    assert m.alt == "a"
    assert m.src == "b.ipynb"
    assert m.identifier == "c"
    assert m.markdown == "![a](b.ipynb){#c}"

    m = next(it)
    assert isinstance(m, str)
    assert m == "\n\n"

    m = next(it)
    assert isinstance(m, str)
    assert m == "```\n![d](e.ipynb){#f}\n```"

    m = next(it)
    assert isinstance(m, str)
    assert m == "\n"


def test_iter_images_empty():
    from mkdocs_nbstore.image import Image
    from mkdocs_nbstore.markdown import iter_images

    it = iter_images("![a](){#b}")
    m = next(it)
    assert isinstance(m, Image)
    assert m.alt == "a"
    assert m.src == ""
    assert m.identifier == "b"
    assert m.markdown == "![a](){#b}"


def test_iter_images_other():
    from mkdocs_nbstore.markdown import iter_images

    it = iter_images("![a](b.png){#c}")
    m = next(it)
    assert isinstance(m, str)
    assert m == "![a](b.png){#c}"
