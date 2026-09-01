#!/usr/bin/env python3
"""СУД ФОРМАТОВ ДАННЫХ: сверяются ЗАПИСИ, а не строки.

Показ утверждает, что одно письмо есть то же, что другое. Суд разбирает
ОБЕ стороны СВОИМИ читателями и требует, чтобы вышла ОДНА И ТА ЖЕ
ЗАПИСЬ. Две записи данных отличаются каждым знаком и значат одно — в
этом весь смысл формата, и потому сверка строк здесь не проверка, а
недоразумение.

ПЕРЕВОД СТРОКИ ВНУТРИ ПОКАЗА ЗАМЕНЁН НА « ; », И ЭТО ОБЪЯВЛЕНО. Корпус
построчен: показ с настоящим переводом строки распался бы на строки, из
которых ни одна не была бы показом. Замена названа здесь и снимается
судом перед чтением — она есть свойство ПОКАЗА, а не формата.

ОРАКУЛ ДОМА ПРОВЕРЯЕТСЯ ПРЕЖДЕ ВСЯКОГО ВЕРДИКТА: дом, потерявший
обратимость письмён, делает бессмысленным весь слой.
"""

import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import dataformat as дф  # noqa: E402
from genesis import Unreadable, worlds  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file

ЧИТАТЕЛИ = {имя: читать for имя, _п, читать in дф.ПИСЬМЕНА}
ПИСЬМА = "|".join(sorted(ЧИТАТЕЛИ))

ЭТО_JSON = re.compile(r"^in json this record is (\{.*\})\.$")
В_ПИСЬМЕ = re.compile(
    rf"^(\{{.*\}}) written in ({ПИСЬМА}) is (.+)\.$")
ИЗ_ПИСЬМА = re.compile(rf"^(.+) written in json is (\{{.*\}})\.$")
В_ПИСЬМЕ_RU = re.compile(
    rf"^(\{{.*\}}) в письме ({ПИСЬМА}) есть (.+)\.$")
В_СЛОВАХ = re.compile(r"^(\{.*\}) in words is (.+)$")
В_СЛОВАХ_RU = re.compile(r"^(\{.*\}) в словах есть (.+)$")
ИЗ_СЛОВ = re.compile(r"^(.+) in json is (\{.*\})\.$")
ИЗ_СЛОВ_RU = re.compile(r"^(.+) в json есть (\{.*\})\.$")
ВОПРОС = re.compile(
    r"^(?:how is \{.*\} said in words\? |как читается \{.*\}\? )(.+)$")


def _вернуть_строки(т):
    """Снять объявленную замену перевода строки."""
    return т.replace(" ; ", "\n")


def _прочесть(текст, чем):
    if чем in ЧИТАТЕЛИ:
        return ЧИТАТЕЛИ[чем](_вернуть_строки(текст))
    if чем.startswith("речь:"):
        return дф.из_речи(текст, чем.split(":")[1])
    return None


def _каким_письмом(текст):
    """Каким письмом читается строка — ровно одним, или None.

    ПИСЬМО ОПОЗНАЁТСЯ ЧТЕНИЕМ, А НЕ ИМЕНЕМ. Если строку читают ДВА
    письма и дают разное, суд молчит: неоднозначность есть свойство
    показа, и вердикт по ней был бы догадкой.
    """
    вышло = {}
    for имя, читать in ЧИТАТЕЛИ.items():
        в = читать(_вернуть_строки(текст))
        if в is not None:
            вышло[имя] = в
    if not вышло:
        return None
    первое = next(iter(вышло.values()))
    return первое if all(в == первое for в in вышло.values()) else None


def судить(строка):
    """(судимо, истинно) для одной строки."""
    с = строка.strip()
    if not с:
        return False, False
    м = ВОПРОС.match(с)
    if м:
        return судить(м.group(1) if м.group(1).endswith(".")
                      else м.group(1) + ".")
    м = ЭТО_JSON.match(с)
    if м:
        return True, дф.из_json(м.group(1)) is not None
    for образец, слева, справа in (
            (В_ПИСЬМЕ, "json", None), (В_ПИСЬМЕ_RU, "json", None)):
        м = образец.match(с)
        if м:
            левый = _прочесть(м.group(1), слева)
            правый = _прочесть(м.group(3), м.group(2))
            if левый is None or правый is None:
                return False, False
            return True, левый == правый
    м = ИЗ_ПИСЬМА.match(с)
    if м:
        левый = _каким_письмом(м.group(1))
        правый = дф.из_json(м.group(2))
        if левый is None or правый is None:
            return False, False
        return True, левый == правый
    for образец, язык in ((В_СЛОВАХ, "en"), (В_СЛОВАХ_RU, "ru")):
        м = образец.match(с)
        if м:
            левый = дф.из_json(м.group(1))
            правый = дф.из_речи(м.group(2), язык)
            if левый is None or правый is None:
                return False, False
            return True, левый == правый
    for образец, язык in ((ИЗ_СЛОВ, "en"), (ИЗ_СЛОВ_RU, "ru")):
        м = образец.match(с)
        if м:
            левый = дф.из_речи(м.group(1) + ".", язык)
            правый = дф.из_json(м.group(2))
            if левый is None or правый is None:
                return False, False
            return True, левый == правый
    return False, False


def обход(явные):
    if явные:
        return [pathlib.Path(п) for п in явные]
    try:
        return worlds(kind="shows")
    except Unreadable as беда:
        print(f"ФОРМАТЫ ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("ФОРМАТЫ ОТКАЗ: обход пуст, судить нечего")
        return 2
    беды = дф.оракул()
    if беды:
        print(f"ФОРМАТЫ FAIL: дом необратим на {len(беды)} записях")
        return 1
    ложных = судимых = 0
    примеры = []
    for путь in пути:
        свои = 0
        with путь.open(encoding="utf-8", errors="replace") as поток:
            for строка in поток:
                судимо, истинно = судить(строка)
                if not судимо:
                    continue
                судимых += 1
                if not истинно:
                    ложных += 1
                    свои += 1
                    if len(примеры) < 4:
                        примеры.append(f"{путь.name}: {строка.strip()[:90]}")
        if свои:
            print(f"  {путь.name:<30} ложных {свои}")
    for п in примеры:
        print(f"    {п}")
    поза = "ЛЕНТА" if явные else (
        "PASS" if ложных <= ЛОЖНЫХ_РУБЕЖ else "FAIL")
    print(f"ФОРМАТЫ {поза}: {ложных} ложных из {судимых} судимых "
          f"({len(пути)} файлов, обратимость дома цела)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
