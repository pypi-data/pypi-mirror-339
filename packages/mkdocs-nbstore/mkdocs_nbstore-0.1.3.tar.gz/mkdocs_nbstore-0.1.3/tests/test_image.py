import pytest

from mkdocs_nbstore.image import Image


def test_image():
    img = Image("alt", "a.ipynb", "#b  .c .d  k1='v1 v2' k2=v3")
    assert img.markdown == "![alt](a.ipynb){#b  .c .d  k1='v1 v2' k2=v3}"
    assert img.src == "a.ipynb"
    assert img.identifier == "b"
    assert img.classes == ["c", "d"]
    assert img.attributes == {"k1": "v1 v2", "k2": "v3"}


@pytest.mark.parametrize(
    ("attr", "expected"),
    [
        ("", ""),
        ("#id", "{#id}"),
        (".cls", "{.cls}"),
        ("#id .cls", "{#id .cls}"),
        ("k1=v1 k2='a b'", "{k1=v1 k2='a b'}"),
    ],
)
def test_str(attr, expected):
    img = Image("alt", "url", attr)
    assert str(img) == f"![alt](url){expected}"
