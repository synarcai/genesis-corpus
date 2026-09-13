#!/usr/bin/env python3
"""GENESIS layer: DOCUMENT STRUCTURE — a link is an EDGE, and it resolves.

Markdown syntax is judged by a LINE: three hashes are a level-three
heading, and the line alone settles it. STRUCTURE is not judged that way.
«[form](../core/form.md#kinds-of-form)» is true or false only RELATIVE TO
A TREE: is there such a document, counting from where the link stands; is
there such a section in it. That is a verdict about an EDGE OF A GRAPH,
and a corpus that knows the brackets of a link but not its resolution has
learned punctuation and not reference.

A RELATIVE LINK WITHOUT ITS PLACE IS MEANINGLESS, and every show here
says its place: «in core/form.md the link … leads to …». That is not
ceremony — «./matter.md» from core/form.md and from world/water.md are
two different documents, and a corpus showing the link without the place
teaches that they are one.

FOUR THINGS SYNTAX DOES NOT CARRY, and structure is nothing without them:
    RELATIVE PATH  — «./» and «../» counted from the document's own folder
    ANCHOR         — «#kinds-of-form» points into a document, not at it
    SLUGIFICATION  — «Kinds of Form» → «kinds-of-form» by a stated rule
    ORDER          — sidebar_position makes «the next document» computable

AND A FIFTH, WHICH IS THE ONE A CORPUS USUALLY OMITS: A LINK THAT LEADS
NOWHERE. The refusal is shown here with its ground — «there is no such
document», «there is no such section» — because a corpus that only ever
shows links that work teaches that every link works.

THE ORACLE IS TWO OPPOSITE WALKS. The tree home builds the link text from
a pair of documents; it resolves the link text back to a pair. Neither is
derived from the other, and their agreement over every pair and every
anchor is checked before a single show is born.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import doctreeforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ЦЕЛЬ ОБЪЯВЛЯЕТСЯ СТРОКОЙ: её читают и указатель родов, и мера воспроизводимости.
ЦЕЛЬ = "datasets/genesis_doctree.txt"


def main():
    emit_grouped(ЦЕЛЬ, F.группы)


if __name__ == "__main__":
    main()
