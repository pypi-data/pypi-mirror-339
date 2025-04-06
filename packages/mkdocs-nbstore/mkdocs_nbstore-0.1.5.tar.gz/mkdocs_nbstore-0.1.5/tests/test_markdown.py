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
    assert m.group("url") == "b.ipynb"
    assert m.group("id") == "c"
    assert m.group("attr") == ""

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
    assert m.url == "b.ipynb"
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
    assert m.url == ""
    assert m.identifier == "b"
    assert m.markdown == "![a](){#b}"


def test_iter_images_other():
    from mkdocs_nbstore.markdown import iter_images

    it = iter_images("![a](b.png){#c}")
    m = next(it)
    assert isinstance(m, str)
    assert m == "![a](b.png){#c}"


def test_iter_images_inline():
    from mkdocs_nbstore.markdown import _iter_images

    text = "`![a](b.ipynb){#c}`"
    it = _iter_images(text)

    m = next(it)
    assert isinstance(m, tuple)
    assert m == (0, len(text))


def test_iter_images_inline_multi():
    from mkdocs_nbstore.markdown import _iter_images

    text = "``![a](b.ipynb){#c}``"
    it = _iter_images(text)

    m = next(it)
    assert isinstance(m, tuple)
    assert m == (0, 1)

    m = next(it)
    assert isinstance(m, tuple)
    assert m == (1, len(text) - 1)

    m = next(it)
    assert isinstance(m, tuple)
    assert m == (len(text) - 1, len(text))
