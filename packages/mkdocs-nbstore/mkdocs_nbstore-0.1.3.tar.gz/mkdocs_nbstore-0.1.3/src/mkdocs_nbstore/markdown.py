from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .image import Image

if TYPE_CHECKING:
    from collections.abc import Iterator


def _iter(
    pattern: re.Pattern,
    text: str,
    pos: int = 0,
    endpos: int | None = None,
) -> Iterator[re.Match[str] | tuple[int, int]]:
    r"""Iterate over matches of a regex pattern in the given text.

    Search for all occurrences of the specified regex pattern
    in the provided text. Yield the segments of text between matches
    as well as the matches themselves. This allows for processing
    both the matched content and the surrounding text in a single iteration.

    Args:
        pattern (re.Pattern): The compiled regex pattern to search for in the text.
        text (str): The text to search for matches.
        pos (int): The starting position in the text to search for matches.
        endpos (int | None): The ending position in the text to search for matches.

    Yields:
        re.Match | tuple[int, int]: Segments of text and match objects. The segments
        are the parts of the text that are not matched by the pattern, and the
        matches are the regex match objects.

    Examples:
        >>> import re
        >>> pattern = re.compile(r'\d+')
        >>> text = "There are 2 apples and 3 oranges."
        >>> matches = list(_iter(pattern, text))
        >>> matches[0]
        (0, 10)
        >>> matches[1]
        <re.Match object; span=(10, 11), match='2'>
        >>> matches[2]
        (11, 23)
        >>> matches[3]
        <re.Match object; span=(23, 24), match='3'>
        >>> matches[4]
        (24, 33)

    """
    if endpos is None:
        endpos = len(text)

    cursor = pos

    for match in pattern.finditer(text, pos, endpos=endpos):
        start, end = match.start(), match.end()

        if cursor < start:
            yield cursor, start

        yield match

        cursor = end

    if cursor < endpos:
        yield cursor, endpos


FENCED_CODE = re.compile(r"^(?P<pre> *[~`]{3,}).*?^(?P=pre)", re.MULTILINE | re.DOTALL)


def _iter_fenced_codes(
    text: str,
    pos: int = 0,
    endpos: int | None = None,
) -> Iterator[re.Match[str] | tuple[int, int]]:
    return _iter(FENCED_CODE, text, pos, endpos)


def _iter_matches(
    pattern: re.Pattern,
    text: str,
    pos: int = 0,
    endpos: int | None = None,
) -> Iterator[re.Match[str] | tuple[int, int]]:
    for match in _iter_fenced_codes(text, pos, endpos):
        if isinstance(match, re.Match):
            yield match.start(), match.end()

        else:
            yield from _iter(pattern, text, match[0], match[1])


IMAGE_PATTERN = re.compile(
    r"^!\[(?P<alt>.*?)\]\((?P<src>.*?)\)\{(?P<attr>.*?)\}",
    re.MULTILINE | re.DOTALL,
)


def _iter_images(
    text: str,
    pos: int = 0,
    endpos: int | None = None,
) -> Iterator[re.Match[str] | tuple[int, int]]:
    return _iter_matches(IMAGE_PATTERN, text, pos, endpos)


def iter_images(
    text: str,
    pos: int = 0,
    endpos: int | None = None,
) -> Iterator[Image | str]:
    for match in _iter_images(text, pos, endpos):
        if isinstance(match, re.Match):
            src = match.group("src")
            if not src or src.endswith(".ipynb"):
                yield Image(match.group("alt"), src, match.group("attr"))
            else:
                yield match.group(0)

        else:
            yield text[match[0] : match[1]]
