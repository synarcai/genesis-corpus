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
import doctree as дт  # noqa: E402
from layer import emit_grouped  # noqa: E402


def ссылки(шаг):
    """Ссылка с местом, где она стоит, — и куда она ведёт."""
    вон = []
    n = len(дт.ПУТИ)
    for i in range(n):
        откуда = дт.ПУТИ[(шаг + i) % n]
        for k in (1, 3, 5):
            куда = дт.ПУТИ[(шаг + i + k) % n]
            текст = дт.относительно(откуда, куда)
            заг = дт.УЗЕЛ[куда][0]
            вон.append(f"in {откуда} the link [{заг}]({текст}) leads "
                       f"to {куда}.")
            вон.append(f"в {откуда} ссылка [{заг}]({текст}) ведёт на "
                       f"{куда}.")
            вон.append(f"what does the link [{заг}]({текст}) in "
                       f"{откуда} lead to? in {откуда} the link "
                       f"[{заг}]({текст}) leads to {куда}.")
            вон.append(f"на что ведёт ссылка [{заг}]({текст}) в "
                       f"{откуда}? в {откуда} ссылка [{заг}]({текст}) "
                       f"ведёт на {куда}.")
    return вон


def якоря(шаг):
    """Якорь ведёт в ЧАСТЬ документа, и правило имени объявлено."""
    вон = []
    n = len(дт.ПУТИ)
    for i in range(n):
        откуда = дт.ПУТИ[(шаг + i) % n]
        куда = дт.ПУТИ[(шаг + i + 2) % n]
        for раздел in дт.УЗЕЛ[куда][2]:
            я = дт.якорь(раздел)
            текст = f"{дт.относительно(откуда, куда)}#{я}"
            вон.append(f"in {откуда} the link [{раздел}]({текст}) leads "
                       f"to the section «{раздел}» of {куда}.")
            вон.append(f"в {откуда} ссылка [{раздел}]({текст}) ведёт в "
                       f"раздел «{раздел}» документа {куда}.")
            вон.append(f"the heading «{раздел}» becomes the anchor "
                       f"#{я}.")
            вон.append(f"заголовок «{раздел}» становится якорем #{я}.")
    return вон


def оглавления(шаг):
    """Оглавление есть список ссылок на СВОИ разделы."""
    вон = []
    n = len(дт.ПУТИ)
    for i in range(n):
        путь = дт.ПУТИ[(шаг + i) % n]
        for раздел in дт.УЗЕЛ[путь][2]:
            я = дт.якорь(раздел)
            вон.append(f"in {путь} the table of contents entry "
                       f"- [{раздел}](#{я}) leads to the section "
                       f"«{раздел}» of the same document.")
            вон.append(f"в {путь} строка оглавления - [{раздел}](#{я}) "
                       f"ведёт в раздел «{раздел}» того же документа.")
    return вон


def нигде(шаг):
    """ССЫЛКА, ВЕДУЩАЯ НИКУДА, — и основание отказа названо."""
    вон = []
    n = len(дт.ПУТИ)
    небылицы = ("nowhere.md", "none.md", "absent.md")
    for i in range(n):
        откуда = дт.ПУТИ[(шаг + i) % n]
        небыль = небылицы[(шаг + i) % len(небылицы)]
        вон.append(f"in {откуда} the link [x](./{небыль}) leads "
                   f"nowhere: there is no such document.")
        вон.append(f"в {откуда} ссылка [x](./{небыль}) не ведёт никуда: "
                   f"такого документа нет.")
        куда = дт.ПУТИ[(шаг + i + 4) % n]
        текст = дт.относительно(откуда, куда)
        вон.append(f"in {откуда} the link [x]({текст}#no-such-part) "
                   f"leads nowhere: {куда} has no such section.")
        вон.append(f"в {откуда} ссылка [x]({текст}#no-such-part) не "
                   f"ведёт никуда: в {куда} нет такого раздела.")
    return вон


def порядок(шаг):
    """Порядок объявлен местом в боковике, и «следующий» вычислим."""
    вон = []
    for путь, заг, место, _р in дт.ДЕРЕВО:
        # ID ПО УМОЛЧАНИЮ ЕСТЬ ИМЯ ФАЙЛА БЕЗ РАСШИРЕНИЯ — так делает
        # Docusaurus, и это ВЫВОДИМЫЙ факт, а не второе имя заголовка.
        ид = дт.имя_файла(путь)
        вон.append(f"the document {путь} declares id {ид}, title "
                   f"{заг} and sidebar_position {место}.")
        вон.append(f"документ {путь} объявляет id {ид}, заголовок "
                   f"{заг} и sidebar_position {место}.")
        след = дт.следующий(путь)
        if след:
            вон.append(f"in the folder {дт.папка(путь) or 'root'} the "
                       f"document after {путь} is {след}.")
            вон.append(f"в папке {дт.папка(путь) or 'root'} документ "
                       f"после {путь} — это {след}.")
        else:
            вон.append(f"{путь} is the last document of the folder "
                       f"{дт.папка(путь) or 'root'}.")
            вон.append(f"{путь} — последний документ папки "
                       f"{дт.папка(путь) or 'root'}.")
    return вон


ГРУППЫ = (ссылки, якоря, оглавления, нигде, порядок)


def pass_groups(шаг):
    return [сделать(шаг) for сделать in ГРУППЫ]


def main():
    беды = дт.оракул()
    if беды:
        print(f"ДЕРЕВО ОТКАЗ: {len(беды)} пар разошлись на встречных "
              f"ходах — слой не собран: {беды[:2]}")
        return 2
    emit_grouped("datasets/genesis_doctree.txt", pass_groups)
    return 0


if __name__ == "__main__":
    sys.exit(main())
