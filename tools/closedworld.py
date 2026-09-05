#!/usr/bin/env python3
"""THE CLOSED WORLD — a line of a world every line of which is a shape of
its court, and which that court does not recognise, is a lie.

The gate demands that every line be judged by SOME court; a corrupted line
of the rates world («th book costs 26 dollars…», «he ha 56 dollars…») was
judged by the count court alone and passed (mutation 04.09). Where the
world's own court covers all of the world's honest lines, silence of that
court on a line of that world is not honest silence but a shape the world
never wrote. A court declares its closed worlds by name; the palata hands
it the layer of the file being judged (the world's name, read from the
manifest — the gate's temporary «<world>.txt.ворота» included).
"""
import json
import pathlib

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
МАНИФЕСТ = КОРЕНЬ / "datasets" / "GENESIS-MANIFEST.json"


class Слой:
    """Протокол палаты: создаётся пустым и впитывает файл мира."""

    def __init__(self):
        self.мир = None

    def впитать(self, путь):
        имя = pathlib.Path(путь).name
        for суффикс in (".ворота",):
            if имя.endswith(суффикс):
                имя = имя[:-len(суффикс)]
        try:
            м = json.loads(МАНИФЕСТ.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        for мир in м.get("worlds", ()):
            if pathlib.Path(мир.get("file", "")).name == имя:
                self.мир = мир.get("name")
                return


def замкнут(слой, миры):
    """Is the file being judged one of the court's closed worlds?"""
    return слой is not None and getattr(слой, "мир", None) in миры


def замкнуть(судить_, миры):
    """The court's judge wrapped by the law: silence on a line of a closed
    world becomes a lie. The palata passes the layer when the court exports
    `Слой` (import it from here beside this call)."""
    миры = frozenset(миры)

    def судить(строка, слой=None):
        вердикт = судить_(строка)
        if вердикт[0] is False and замкнут(слой, миры) and строка.strip() and not строка.startswith("\x0c"):
            return True, False
        return вердикт
    судить.__wrapped__ = судить_
    return судить


# ЦИФРОВОЙ СКЕЛЕТ — ЗАКОН ЗАМКНУТОГО МИРА, ПРОДОЛЖЕННЫЙ НА ЦИФРЫ (05.09, прибор мутантов:
# СЕМЬ судов ОНЕМЕЛИ на порче одного числа). Дом, чьи показы объявлены списком, узнаёт свою
# строку по букве — и порча «в сутках 24 часа» → «в сутках 25 часа» выводит её из
# объявленного. Суд молчит, палата отдаёт молчание соседу, и ложь проходит.
#
# ЗАКОН: строка, отличающаяся от показа ЛИШЬ ЦИФРАМИ, есть строка ЭТОГО дома — и, не будучи
# показом, есть его ЛОЖЬ. Это ровно то, что уже объявлено словами «мир замкнут»: набор
# показов полон, и всё, что имеет форму показа, но показом не является, ложно. Цифра формы
# не меняет.
#
# ГРАНИЦА: закон применим лишь там, где мир ОБЪЯВЛЕН ЗАМКНУТЫМ (его показы суть весь мир).
# Дом, чьи страницы порождаются законом над свободными числами, судит числа своим законом, и
# скелет ему не судья — там повторное вхождение дыры проверяется значением (см. дома ночи).
_ЦИФРЫ = __import__("re").compile(r"\d+")


def скелет(строка):
    """«в сутках 24 часа» → «в сутках # часа»: строка без своих чисел."""
    return _ЦИФРЫ.sub("#", строка.strip())


def скелеты(показы):
    """Множество скелетов объявленных показов — читается домом один раз при сборке."""
    return frozenset(скелет(с) for с in показы)


def ложь_по_цифре(строка, скелеты_, показы):
    """True — строка не показ, но отличается от показа лишь цифрами: ложь дома."""
    с = строка.strip()
    return с not in показы and скелет(с) in скелеты_
