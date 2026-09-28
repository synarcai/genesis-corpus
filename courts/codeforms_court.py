#!/usr/bin/env python3
"""[КОД С ПОВЕДЕНИЕМ] — всякий сказанный результат есть результат интерпретатора (25.09).

Мир `codeforms` пишет свои малые программы на Python и Rust и их поведение на девяти языках: вызов и результат,
вопрос и ответ, тест проходит и почему, тест падает — почему и правка, разбор функции, перевод на Rust. Суд —
вторая рука: рамку страницы берёт у СБОРКИ дома (метки вместо кода, вызова, значения), а код ИСПОЛНЯЕТ сам —
Python в пустом пространстве имён и лишь после того, как всякая лексема тела прошла белый список (имена
параметров, целые, арифметика, сравнения, `if … else`, `and/or/not`), Rust — переводом того же подмножества
(`if c { x } else { y }` → условное выражение, `/` → целое деление, `true/false`).

    СТРАНИЦА О КОДЕ ИСТИННА, ЛИШЬ ЕСЛИ КОД ДЕЛАЕТ ТО, ЧТО О НЁМ СКАЗАНО: вызов возвращает сказанное; тест,
    названный проходящим, проходит; названный падающим — падает с тем самым значением, а после правки проходит;
    разбор называет имя, число и имена параметров и тело как они есть; перевод на Rust совпадает с Python на
    пробных входах.

ГРАНИЦА: лексема вне белого списка — не код этого мира, суд о нём молчит; целое деление сверяется на
неотрицательных (Rust к нулю, Python вниз); мир `codeforms` замкнут.

    python3 courts/codeforms_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import itertools
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import closedworld  # noqa: E402
import codeforms as C  # noqa: E402 — сборка страниц дома и объявления речи
from closedworld import Слой  # noqa: E402,F401 — палата подаёт имя мира лишь тому, кто ввёз Слой

ИМЯ_СУДА = "codeforms"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"codeforms"})
# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ======================================================================================================
# ИСПОЛНИТЕЛЬ — свой: разбор определения, белый список лексем, перевод Rust, вычисление без встроенных имён
# ======================================================================================================
_ЛЕКСЕМА = re.compile(r"[A-Za-z_]+|\d+|//|==|!=|<=|>=|&&|\|\||[-+*/%<>()!{}]")
_СЛОВА_PY = frozenset({"if", "else", "and", "or", "not", "True", "False"})
_PY = re.compile(r"^def ([a-z_]+)\(([a-z_]+(?:, [a-z_]+)*)\): return (.+)$")
_RS = re.compile(r"^fn ([a-z_]+)\(([a-z_]+: i32(?:, [a-z_]+: i32)*)\) -> (i32|bool) \{ (.+) \}$")
_ЕСЛИ_RS = re.compile(r"^if (.+?) \{ (.+?) \} else \{ (.+?) \}$")


def _чисто(тело, парам, слова):
    лексемы = _ЛЕКСЕМА.findall(тело)
    if "".join(лексемы) != тело.replace(" ", ""):
        return False
    return all(л.isdigit() or not (л[0].isalpha() or л[0] == "_") or л in парам or л in слова for л in лексемы)


def _из_rust(тело):
    """Тело Rust → выражение Python; None — вне подмножества."""
    м = _ЕСЛИ_RS.match(тело)
    if м:
        ч = [_из_rust(x) for x in м.groups()]
        return None if None in ч else f"(({ч[1]}) if ({ч[0]}) else ({ч[2]}))"
    if "{" in тело or "}" in тело:
        return None
    вон = re.sub(r"(?<![/!=<>])/(?!/)", "//", тело)
    вон = вон.replace("&&", " and ").replace("||", " or ")
    вон = re.sub(r"!(?!=)", " not ", вон)
    return re.sub(r"\btrue\b", "True", re.sub(r"\bfalse\b", "False", вон))


def функция(код):
    """(язык кода, имя, параметры, тело Python) определения — или None, если это не код этого мира."""
    м = _PY.match(код)
    if м:
        имя, парам, тело = м.group(1), tuple(м.group(2).split(", ")), м.group(3)
        return ("python", имя, парам, тело) if _чисто(тело, парам, _СЛОВА_PY) else None
    м = _RS.match(код)
    if м:
        имя = м.group(1)
        парам = tuple(p.split(":")[0] for p in м.group(2).split(", "))
        тело_rs = м.group(4)
        if not _чисто(тело_rs, парам, {"if", "else", "true", "false"}):
            return None
        тело = _из_rust(тело_rs)
        if тело is None or not _чисто(тело, парам, _СЛОВА_PY):
            return None
        return ("rust", имя, парам, тело)
    return None


def вычислить(ф, аргументы):
    _код, имя, парам, тело = ф
    if len(аргументы) != len(парам):
        return None
    try:
        return eval(тело, {"__builtins__": {}}, dict(zip(парам, аргументы)))  # noqa: S307 — белый список выше
    except Exception:  # noqa: BLE001
        return None


def _вызов(текст):
    м = re.fullmatch(r"([a-z_]+)\((\d+(?:, \d+)*)\)", текст)
    return (м.group(1), tuple(int(x) for x in м.group(2).split(", "))) if м else None


def _значение(код, текст):
    таблица = {"python": {"True": True, "False": False}, "rust": {"true": True, "false": False}}[код]
    if текст in таблица:
        return таблица[текст]
    return int(текст) if re.fullmatch(r"-?\d+", текст) else None


# ======================================================================================================
# РАМКИ — у сборки дома, с метками вместо частей
# ======================================================================================================
_ЧАСТИ = ("code", "call", "v", "test", "actual", "expected", "fix", "name", "n", "params", "expr", "rs")


def М(имя):
    return f"\x01{имя}\x01"


def _классы(язык):
    и = re.escape(C.РЕЧЬ[язык]["и"])
    return {"code": r"[^`]+", "call": r"[a-z_]+\(\d+(?:, \d+)*\)", "v": r"-?\d+|True|False|true|false",
            "actual": r"-?\d+|True|False|true|false", "expected": r"-?\d+|True|False|true|false",
            "test": r"[^`]+", "fix": r"[^`]+", "name": r"[a-z_]+", "n": r"\d+ [^\W\d_]+",
            "params": rf"[a-z_]+(?:(?:, | {и} )[a-z_]+)*", "expr": r"[^`]+", "rs": r"[^`]+"}


def _образец(текст, классы):
    куски, счёт = [], {}
    for кусок in re.split(r"(\x01[^\x01]+\x01)", текст):
        if кусок.startswith("\x01"):
            имя = кусок[1:-1]
            счёт[имя] = счёт.get(имя, 0) + 1
            куски.append(f"(?P<{имя}__{счёт[имя]}>{классы[имя]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


def _рамки():
    вон = []
    for язык in C.ЯЗЫКИ:
        кл = _классы(язык)
        метки = {ч: М(ч) for ч in _ЧАСТИ}
        for род in C.РОДЫ:
            вон.append((_образец(C.сборка(язык, род, **метки), кл), язык, род))
    return вон


РАМКИ = _рамки()


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        имя = ключ.rsplit("__", 1)[0]
        if имя in вон and вон[имя] != знач:
            return None
        вон[имя] = знач
    return вон


def _вердикт(язык, род, зн):
    ф = функция(зн["code"])
    if ф is None:
        return False
    код, имя, парам, _тело = ф
    if род == C.РАЗБОР:
        return (зн["name"] == имя and зн["n"] == C.параметров(язык, len(парам))
                and зн["params"] == C.список(язык, парам) and зн["expr"] == зн["code"].split("return ", 1)[-1]
                if код == "python" else
                зн["name"] == имя and зн["n"] == C.параметров(язык, len(парам))
                and зн["params"] == C.список(язык, парам) and зн["expr"] == _RS.match(зн["code"]).group(4))
    if род == C.ПЕРЕВОД:
        ф_rs = функция(зн["rs"])
        if код != "python" or ф_rs is None or ф_rs[0] != "rust" or ф_rs[1:3] != ф[1:3]:
            return False
        пробы = list(itertools.product(range(0, 13, 3), repeat=len(парам)))
        return all(вычислить(ф, п) == вычислить(ф_rs, п) and вычислить(ф, п) is not None for п in пробы)
    выз = _вызов(зн["call"])
    if выз is None or выз[0] != имя:
        return False
    вышло = вычислить(ф, выз[1])
    if вышло is None:
        return False
    if род in (C.ВЫЗОВ, C.ВОПРОС):
        return зн["v"] == C.значение(код, вышло)
    if род == C.ПРОХОДИТ:
        return зн["v"] == C.значение(код, вышло) and зн["test"] == C.тест(код, зн["call"], зн["v"])
    if род == C.ПАДАЕТ:
        ожидаемое = _значение(код, зн["expected"])
        if ожидаемое is None or зн["actual"] != C.значение(код, вышло) or ожидаемое == вышло:
            return False
        if зн["test"] != C.тест(код, зн["call"], зн["expected"]):
            return False
        # ПРАВКА: то же определение с исправленным телом обязано вернуть ожидаемое
        if код == "python":
            м = re.fullmatch(r"return (.+)", зн["fix"])
            исправленное = None if not м else зн["code"].rsplit("return ", 1)[0] + "return " + м.group(1)
        else:
            м = re.fullmatch(r"\{ (.+) \}", зн["fix"])
            голова = _RS.match(зн["code"])
            исправленное = None if not (м and голова) else зн["code"][:голова.start(4) - 2] + "{ " + м.group(1) + " }"
        ф2 = функция(исправленное) if исправленное else None
        return ф2 is not None and вычислить(ф2, выз[1]) == ожидаемое
    return False


def _судить(строка):
    с = строка.strip()
    if not (с.startswith("`def ") or с.startswith("`fn ")):
        return False, False
    совпал = False
    for образ, язык, род in РАМКИ:
        м = образ.match(с)
        if not м:
            continue
        совпал = True
        зн = _значения(м)
        if зн is not None and _вердикт(язык, род, зн):
            return True, True
    return (True, False) if совпал else (False, False)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def _порчи(с):
    """Подсадки от страницы дома, поставленные В ЗНАЧЕНИЕ, а не куда придётся: результат вызова (или то, что
    вернул падающий тест) — другое целое или перевёрнутая истина; число параметров разбора — на единицу больше.
    Число аргумента трогать нельзя: `is_positive(6)` тоже True, и такая «порча» есть правда."""
    вон = []
    for образ, _язык, _род in РАМКИ:
        м = образ.match(с)
        if not м:
            continue
        for ключ in ("v__1", "actual__1", "n__1"):
            if м.groupdict().get(ключ) is None:
                continue
            было = м.group(ключ)
            перевёрнуто = {"True": "False", "False": "True", "true": "false", "false": "true"}
            if было in перевёрнуто:
                стало = перевёрнуто[было]
            else:
                число = re.match(r"-?\d+", было)
                стало = str(int(число.group()) + 1) + было[число.end():]
            вон.append(с[:м.start(ключ)] + стало + с[м.end(ключ):])
        break
    return [в for в in вон if в != с]


def _самопроверка():
    беды = [с for с in C.ПОКАЗЫ if _судить(с) != (True, True)]
    порч = пойманных = 0
    for с in C.ПОКАЗЫ:
        for порча in _порчи(с):
            порч += 1
            вердикт = _судить(порча)
            if вердикт == (True, False):
                пойманных += 1
            elif вердикт == (True, True):
                беды.append(f"порча прошла: {порча[:140]}")
    return беды, порч, пойманных, len(C.ПОКАЗЫ)


def main():
    import genesis
    беды, порч, пойманных, страниц = _самопроверка()
    for б in беды[:3]:
        print(f"  САМОПРОВЕРКА: {б[:160]}")
    судимо = ложных = 0
    примеры = []
    for путь in genesis.worlds(kind="shows"):
        for строка in путь.read_text(encoding="utf-8", errors="replace").split("\n"):
            если, верно = судить(строка)[:2]
            if not если:
                continue
            судимо += 1
            if not верно:
                ложных += 1
                if len(примеры) < 5:
                    примеры.append(f"{путь.stem}: {строка.strip()[:110]}")
    for п in примеры:
        print(f"  {п}")
    поза = "PASS" if ложных <= ЛОЖНЫХ_РУБЕЖ and not беды else "FAIL"
    print(f"КОД С ПОВЕДЕНИЕМ {поза}: {ложных} ложных из {судимо} судимых (рубеж {ЛОЖНЫХ_РУБЕЖ}); страниц дома "
          f"{страниц}, порч самопроверки {порч}, из них поймано рамкой {пойманных}, бед {len(беды)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
