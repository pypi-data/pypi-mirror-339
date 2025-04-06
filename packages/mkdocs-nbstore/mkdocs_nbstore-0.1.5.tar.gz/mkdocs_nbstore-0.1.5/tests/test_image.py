from mkdocs_nbstore.image import Image


def test_image():
    img = Image("alt", "a.ipynb", "b", " .c .d  k1='v1 v2' k2=v3")
    assert img.markdown == "![alt](a.ipynb){#b .c .d  k1='v1 v2' k2=v3}"
