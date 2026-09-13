#!/usr/bin/env python3
"""GENESIS layer: MARKDOWN IN FULL — the notation the organism will speak in.

A census over the whole corpus found NINE markdown constructs taught out
of thirty-nine that markdown has: headings, a bare fence, code spans,
italic, bold, two kinds of list, an inline link and a table. Nothing of
blockquotes, images, reference links, escapes, entities, task lists,
footnotes, table alignment. NOTHING of Docusaurus — no front matter, no
admonitions, no tabs, no MDX imports. And nothing at all of DOCUMENT
STRUCTURE — no relative links, no anchors, no table of contents.

This matters more than a gap in a subject. Markdown is not a subject; it
is the PROTOCOL — the notation in which everything else will be asked and
answered. An organism fluent in number theory and mute in front matter
cannot read the corpus it was taught from.

FOUR SURFACES PER CONSTRUCT, and each is a different act:
    ЗАПИСЬ   — the construct itself, as material: «**light**»
    СМЫСЛ    — what it means, in English and in Russian
    ВОПРОС   — the same meaning asked for, because knowledge with no
               question surface only reports (the law of the day before)

THE ORACLE IS REVERSIBILITY, NOT REVIEW. Every construct declares how to
WRITE it and how to READ it, and neither is derived from the other
(tools/markdown.py). A construct whose reading does not return what was
written never reaches the corpus: a grammar error becomes IMPOSSIBLE
rather than detectable. The layer refuses to build if the oracle is not
empty — the same discipline as the write gate, one level lower.
"""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import markdown as md  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ДОМ ОТДЕЛЁН ОТ КУЗНИЦЫ (13.09): поверхности, семьи и словарь показов живут в
# `tools/markdownforms.py`, а кузница берёт у него готовые группы. Мир был вторым по величине
# бездомным миром свода — 3 428 строк без объявленного рода.
#
#     МИР, ЧЬИ СТРАНИЦЫ НЕ НАЗВАНЫ РОДОМ, ЧИТАЕТСЯ ТОЛЬКО ТЕМ, КТО ЧИТАЕТ КУЗНИЦУ.
import markdownforms as F  # noqa: E402


def pass_groups(шаг):
    # СЕМЬЯ — СВОЯ ГРУППА: ядро, расширения и MDX не перемешиваются,
    # ибо это три разных договора, а не три части одного.
    return F.группы(шаг)


def main():
    беды = md.оракул()
    if беды:
        print(f"РАЗМЕТКА ОТКАЗ: {len(беды)} конструкций необратимы — "
              f"слой не собран: {беды[:3]}")
        return 2
    emit_grouped("datasets/genesis_markdown.txt", pass_groups)
    return 0


if __name__ == "__main__":
    sys.exit(main())
