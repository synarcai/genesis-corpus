#!/usr/bin/env python3
"""[ЯЗЫКОВОЙ ПЛАСТ] — всякое слово показа обязано быть ОБЪЯВЛЕНО в пакете.

Языковой пласт не проверяется счётом: «我学» и «ich lese» ничего не
вычисляют. Но у него есть своя истина, и она строже арифметической:
пласт порождён ПАКЕТОМ, и всякое слово в нём обязано быть формой,
которую пакет объявил.

Слово, которого в пакете нет, есть одно из двух — опечатка генератора
или форма, придуманная на ходу. Оба случая учат языку, которого никто
не описывал, и оба невидимы всякому иному прибору: строка при этом
грамматична, а числа в ней сходятся.

СЛОВАРЬ ПАКЕТА СОБИРАЕТСЯ ИЗ ВСЕГО, ЧТО ОБЪЯВЛЕНО: числительные, слова
операций, словари родов показа, все формы всех классов, имена знаков,
служебные слова, пары отказов, удержанные вопросы. Ничего не берётся из
головы прибора.

ПЛАСТ УЗНАЁТСЯ ПО ИМЕНИ МИРА (`lang_XX`), а не по содержимому: судить
чужой слой словарём одного языка значило бы объявлять ложью всё
иноязычное в нём.
"""
import json
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
ПАКЕТЫ = КОРЕНЬ / "tools/langpacks"
sys.path.insert(0, str(КОРЕНЬ / "tools"))
from genesis import Unreadable, manifest  # noqa: E402
from segment import tokens, word_re  # noqa: E402

# РУБЕЖ-ДОЛГА: ЧУЖИХ_РУБЕЖ = 0
ЧУЖИХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file

# СЛОВО РЕЖЕТСЯ ПО ПИСЬМУ ПАКЕТА, А НЕ ПО ЛАТИНСКОЙ ПРИВЫЧКЕ. Этот
# образец — лишь запасной, для пакета, чьи слова ещё не прочтены;
# рабочий выводится из объявленного словаря (`segment.word_re`), ибо
# знак, живущий между двумя буквами объявленного слова, тем самым
# объявлен буквой по должности. Украинское «п'ятнадцять» резалось
# надвое, и «ятнадцять» звалось необъявленным.
СЛОВО = word_re()


def словарь_пакета(язык):
    """Всё, что пакет объявил, — и ничего сверх того."""
    ф = ПАКЕТЫ / f"{язык}.json"
    try:
        п = json.loads(ф.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None, False
    слова = {str(v).lower() for v in (п.get("numerals") or {}).values()}
    for род in (п.get("show_kinds") or {}).values():
        слова |= {str(w).lower() for w in (род.get("ops") or {})}
        слова |= {str(w).lower() for w in род.get("lexicon", [])}
        for пара in род.get("pairs", []):
            for сторона in ("bad", "good"):
                слова |= {w.lower() for w in СЛОВО.findall(пара.get(сторона, ""))}
        for шаблон in род.get("templates", []):
            # слова САМОГО шаблона — рамка, в которой живёт форма
            голый = re.sub(r"\{[^}]*\}", " ", шаблон)
            слова |= {w.lower() for w in СЛОВО.findall(голый)}
    for кл in (п.get("morph_classes") or {}).values():
        for формы in кл.get("lexemes", {}).values():
            for ф_ in формы:
                слова |= {w.lower() for w in СЛОВО.findall(str(ф_))}
    for имена in (п.get("sign_names") or {}).values():
        имена = [имена] if isinstance(имена, str) else имена
        for имя in имена:
            слова |= {w.lower() for w in СЛОВО.findall(str(имя))}
    слова |= {w.lower() for w in п.get("function_words", [])}
    for вопрос in п.get("reserved", []):
        слова |= {w.lower() for w in СЛОВО.findall(вопрос)}
    for пара in (п.get("noun_forms") or {}).items():
        слова |= {str(x).lower() for x in пара}
    без_пробела = п.get("segmentation") == "longest-match"
    return слова, без_пробела


def чужие(строка, слова, без_пробела):
    """Слова показа, которых пакет не объявлял."""
    образец = word_re(слова)
    if без_пробела:
        куски = tokens(строка.lower(), слова, spaced=False)
    else:
        куски = образец.findall(строка.lower())
    return [w for w in куски if образец.fullmatch(w) and w not in слова]


def пласты(явные):
    if явные:
        вон = []
        for п in явные:
            путь = pathlib.Path(п)
            язык = путь.stem.rsplit("_", 1)[-1]
            вон.append((язык, путь))
        return вон
    try:
        миры = manifest()["worlds"]
    except Unreadable as беда:
        print(f"ПЛАСТ ОТКАЗ: {беда}")
        sys.exit(2)
    вон = []
    for м in миры:
        if not м["name"].startswith("lang_"):
            continue
        путь = КОРЕНЬ / м["file"]
        if путь.is_file():
            вон.append((м["name"][5:], путь))
    return вон


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    работа = пласты(явные)
    if not работа:
        print("ПЛАСТ ОТКАЗ: обход пуст, судить нечего")
        return 2
    всего_чужих = проверено = 0
    примеры = []
    for язык, путь in работа:
        слова, без_пробела = словарь_пакета(язык)
        if слова is None:
            print(f"ПЛАСТ ОТКАЗ: пакет {язык} не читается")
            return 2
        свои = set()
        with путь.open(encoding="utf-8", errors="replace") as поток:
            for строка in поток:
                if not строка.strip():
                    continue
                проверено += 1
                свои.update(чужие(строка, слова, без_пробела))
        всего_чужих += len(свои)
        if свои:
            print(f"  {путь.name:<28} необъявленных слов {len(свои)}: "
                  f"{sorted(свои)[:6]}")
        if свои and len(примеры) < 3:
            примеры.append(f"{язык}: {sorted(свои)[:4]}")
    поза = "ЛЕНТА" if явные else (
        "PASS" if всего_чужих <= ЧУЖИХ_РУБЕЖ else "FAIL")
    print(f"ПЛАСТ {поза}: {всего_чужих} необъявленных слов "
          f"({проверено} строк, {len(работа)} пластов)")
    if явные:
        return 0
    return 0 if всего_чужих <= ЧУЖИХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
