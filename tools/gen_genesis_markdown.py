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

ВОПРОС = {"en": "what does «{запись}» mean?",
          "ru": "что значит «{запись}»?"}
# У МНОГОСТРОЧНОЙ КОНСТРУКЦИИ ВОПРОС КЛЮЧИТСЯ НА ЗАЧИН, А НЕ НА ВЕСЬ
# БЛОК. Корпус построчен, и вопрос, вобравший перевод строки, распался
# бы на несколько строк, из которых ни одна не была бы показом.
# Зачин при этом и есть то, что различает конструкции глазом: «:::note»,
# «---», «```mermaid» узнаются по первой строке.
ВОПРОС_БЛОКА = {"en": "what does a block opening with «{зачин}» mean?",
                "ru": "что значит блок, начатый с «{зачин}»?"}


def _ключ(запись, ответ):
    """Чем вопрос называет предмет: цитатой из ОТВЕТА, иначе записью."""
    if "\n" in запись:
        return {"зачин": запись.split("\n")[0]}
    м = re.search(r"«(.+?)»", ответ)
    return {"запись": м.group(1) if м else запись}


def поверхности(семья, шаг):
    """[(запись, [поверхности])] — показы семьи с их ЗАПИСЬЮ рядом.

    Запись отдаётся вместе с поверхностями нарочно: суду нужно знать, О
    ЧЁМ говорит предложение, чтобы сосчитать притязание САМОМУ. Не всякое
    предложение цитирует свою запись («текст, подчёркнутый знаками
    равенства, …» её не несёт), и суд, вынимавший запись из кавычек,
    оставался без предмета счёта.
    """
    вон = []
    for имя, своя, _обр, собрать, смысл_en, смысл_ru, случаи in md.все():
        if своя != семья:
            continue
        for поля in случаи(шаг):
            запись = собрать(поля)
            ен, ру = смысл_en(поля), смысл_ru(поля)
            # ВОПРОС ЦИТИРУЕТ ТУ ЖЕ ЗАПИСЬ, ЧТО И ЕГО ОТВЕТ. Русский
            # ответ о стиле цитирует РУССКУЮ запись («*вода*»), и
            # вопрос, спрашивавший английскую, разошёлся бы с ним в
            # первой же строке — тот же шрам, что «что даёт вычитание 4
            # и 2?» при ответе «вычитание 2 из 4». Запись берётся ИЗ
            # ОТВЕТА, а не из полей.
            шаблон = (ВОПРОС_БЛОКА if "\n" in запись else ВОПРОС)
            # СОДЕРЖИМОЕ ОГРАДЫ ОБЪЯВЛЯЕТСЯ — тем же оборотом, каким
            # его объявляет старый слой разметки. Код, которого никто
            # не объявлял, есть дрейф той же природы, что заголовок без
            # уровня; закон не мой, и второго оборота ему не нужно.
            # У СТИЛЯ ЕСТЬ И РУССКАЯ ЗАПИСЬ. Разметка обнимает слово
            # любого языка, и русское предложение цитирует русскую
            # запись; она обязана быть в слое МАТЕРИАЛОМ, а не только
            # внутри предложения о ней.
            близнец = []
            поле = поля.get("текст") or поля.get("код")
            if имя in ("emphasis", "strong", "strikethrough",
                       "code_span") and поле:
                близнец = [собрать({**поля,
                                    ("код" if имя == "code_span"
                                     else "текст"): md.ру(поле)})]
            блок = []
            if запись.startswith("```") and запись.count("\n") == 2:
                тело = запись.split("\n")[1]
                блок = [f"a code block of one line: {тело}",
                        f"код-блок из одной строки: {тело}"]
            вон.append((запись, блок + близнец + [
                запись, ен, ру,
                f"{шаблон['en'].format(**_ключ(запись, ен))} {ен}",
                f"{шаблон['ru'].format(**_ключ(запись, ру))} {ру}"]))
    return вон


def показы_семьи(семья, шаг):
    """Только поверхности, без записи рядом."""
    return [с for _з, стр in поверхности(семья, шаг) for с in стр]


def pass_groups(шаг):
    # СЕМЬЯ — СВОЯ ГРУППА: ядро, расширения и MDX не перемешиваются,
    # ибо это три разных договора, а не три части одного.
    return [показы_семьи(с, шаг) for с in ("commonmark", "gfm", "mdx")]


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
