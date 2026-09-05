#!/usr/bin/env python3
"""A PERSISTENT CACHE OF COMPILED REGULAR EXPRESSIONS — the fixed price of the palata (05.09).

The mandate of diagnostics (50/50): the loop defect → law → stand runs in minutes, not hours.
The palata is 125 courts; building it compiles ≈ 6 800 patterns (≈ 7 M opcodes), and Python's
regex compiler is pure Python: parsing and coding those patterns is ≈ 80 % of the 22 s a cold
palata costs — and the parallel gate pays that price in EVERY worker process, so it is the
ceiling of the gate's speed-up (SVAMP 56 → 23 s and no further).

A compiled pattern is a pure function of (pattern text, flags, interpreter): the same text
compiles to the same code every time. The derived is not stored in the repo (the .gitignore
law: what is reproducible is not history), but a reproducible cache lives beside the
interpreter's own caches — ~/.cache/genesis-corpus/ — keyed by the interpreter version and the
regex engine's MAGIC, and consulted at the ONE function below re's own in-process cache,
re._compiler.compile. A miss compiles exactly as before and remembers the code; a hit hands the
remembered code to the same engine. The verdicts cannot change: the engine receives the same
arguments either way (checked elementwise on three worlds, all four fields).

What is trusted and what is not: every entry is keyed by the FULL pattern text and flags, so a
foreign or stale entry can never answer for another pattern; a file that does not load is
ignored, not repaired; the file is rewritten atomically. A process that built the palata
rewrites the file with exactly the patterns it used — the cache stays the live set, not a
graveyard of every pattern the houses ever had. GENESIS_RECACHE=0 turns the cache off;
GENESIS_RECACHE_DIR names another directory.
"""
import atexit
import marshal
from array import array
import os
import pathlib
import sys
import tempfile

import _sre
import re
import re._compiler as _compiler
import re._parser as _parser

# The interpreter's compile() is copied below verbatim for the miss path; it must stay the
# same shape as the one shipped with the interpreter this was written against.
ВЕРСИИ = ((3, 11), (3, 12), (3, 13))
# EVERY PROCESS MERGES; ONLY A FULL FILE IS PRUNED, AND PRUNED TO A LIVE SET. A rule that let
# any process of a thousand patterns REWRITE the file looked frugal and was not: a single heavy
# court (doznanie uses over a thousand) evicted the palata's other 4 000, and the next gate paid
# the misses again. Merging never evicts; the ceiling bounds the file, and when it is reached the
# file is rewritten with exactly the patterns the current process used — a live set, not a
# graveyard. The palata's own build uses ≈ 5 200 entries, so the ceiling is set well above it.
ПОТОЛОК_ЗАПИСЕЙ = 20000

_ПАМЯТЬ = None      # {(pattern, flags): (flags_out, code bytes, groups, groupindex, indexgroup)}
# The engine's code word is a 32-bit unsigned int; the code is kept as the bytes of an array of
# them (the compiler's own list holds named int constants, which marshal refuses).
КОД = "I"
_ИСПОЛЬЗОВАНО = {}  # entries this process used (hits and misses)
_НОВЫХ = 0
_ИСХОДНЫЙ = None    # re._compiler.compile before installation


def каталог():
    свой = os.environ.get("GENESIS_RECACHE_DIR")
    return pathlib.Path(свой).expanduser() if свой else pathlib.Path("~/.cache/genesis-corpus").expanduser()


def файл():
    в = sys.version_info
    return каталог() / f"recache-{в[0]}.{в[1]}.{в[2]}-{_sre.MAGIC}.marshal"


def _загрузить():
    global _ПАМЯТЬ
    if _ПАМЯТЬ is not None:
        return _ПАМЯТЬ
    _ПАМЯТЬ = {}
    try:
        with open(файл(), "rb") as f:
            данные = marshal.load(f)
        if isinstance(данные, dict):
            _ПАМЯТЬ = данные
    except (OSError, EOFError, ValueError, TypeError):
        _ПАМЯТЬ = {}
    return _ПАМЯТЬ


def _собрать(pattern, flags):
    """The interpreter's re._compiler.compile, split so the code can be remembered."""
    p = _parser.parse(pattern, flags)
    code = _compiler._code(p, flags)
    groupindex = p.state.groupdict
    indexgroup = [None] * p.state.groups
    for k, i in groupindex.items():
        indexgroup[i] = k
    return (flags | p.state.flags, array(КОД, [int(x) for x in code]).tobytes(),
            p.state.groups - 1, dict(groupindex), tuple(indexgroup))


def _код(байты):
    а = array(КОД)
    а.frombytes(байты)
    return list(а)


def _компилировать(p, flags=0):
    global _НОВЫХ
    if not isinstance(p, str) or flags & _compiler.SRE_FLAG_DEBUG:
        return _ИСХОДНЫЙ(p, flags)
    flags = int(flags)  # a RegexFlag is an int subclass — marshal takes only the plain int
    ключ = (p, flags)
    память = _загрузить()
    запись = память.get(ключ)
    if запись is None:
        запись = _собрать(p, flags)
        память[ключ] = запись
        _НОВЫХ += 1
    _ИСПОЛЬЗОВАНО[ключ] = запись
    flags_out, code, groups, groupindex, indexgroup = запись
    return _sre.compile(p, flags_out, _код(code), groups, dict(groupindex), tuple(indexgroup))


def _сохранить():
    """Write the cache; the error, if any, is returned (atexit cannot raise), never raised."""
    if not _НОВЫХ:
        return None
    try:
        global _ПАМЯТЬ
        _ПАМЯТЬ = None  # re-read: a neighbour process may have written since this one loaded
        данные = dict(_загрузить())
        данные.update(_ИСПОЛЬЗОВАНО)
        if len(данные) > ПОТОЛОК_ЗАПИСЕЙ:
            данные = dict(_ИСПОЛЬЗОВАНО)
        путь = файл()
        путь.parent.mkdir(parents=True, exist_ok=True)
        fd, врем = tempfile.mkstemp(dir=путь.parent, prefix=путь.name + ".", suffix=".tmp")
        try:
            with os.fdopen(fd, "wb") as f:
                marshal.dump(данные, f)
            os.replace(врем, путь)
        except (OSError, ValueError, TypeError):
            try:
                os.unlink(врем)
            except OSError:
                pass
            raise
    except (OSError, ValueError, TypeError) as e:
        return e
    return None


def установить():
    """Install the cache below re's own; idempotent; a no-op on an untested interpreter."""
    global _ИСХОДНЫЙ
    if _ИСХОДНЫЙ is not None or os.environ.get("GENESIS_RECACHE", "1") == "0":
        return False
    if sys.version_info[:2] not in ВЕРСИИ or _compiler.compile.__module__ != "re._compiler":
        return False
    if _sre.CODESIZE != array(КОД).itemsize:
        return False
    _ИСХОДНЫЙ = _compiler.compile
    _compiler.compile = _компилировать
    atexit.register(_сохранить)
    return True


def состояние():
    """(entries in memory, used by this process, new in this process) — for the report."""
    return (len(_загрузить()), len(_ИСПОЛЬЗОВАНО), _НОВЫХ)


def _самопроверка():
    """The cached pattern is the compiled pattern: same text, flags, groups, and the same
    behaviour on strings — checked on a few patterns of every shape the houses use."""
    import time
    установить()
    образцы = [(r"^(?P<т>кот|дом) — это (?:зверь|жильё)\. (?P=т)\.", 0),
               (r"\b(?:quant[oa]s?|tinha|tem)\b", re.I),
               (r"^glyph ([#_]{5}(?:/[#_]{5}){6}) is (not )?(a|b)$", re.M | re.S),
               ("[^\\W\\d_]+(?:'[^\\W\\d_]+)?", re.U)]
    for текст, флаги in образцы:
        своё = _ИСХОДНЫЙ(текст, флаги)
        t = time.perf_counter(); первый = _компилировать(текст, флаги); t1 = time.perf_counter() - t
        t = time.perf_counter(); второй = _компилировать(текст, флаги); t2 = time.perf_counter() - t
        for п in (первый, второй):
            assert (п.pattern, п.flags, п.groups, dict(п.groupindex)) == (своё.pattern, своё.flags, своё.groups, dict(своё.groupindex))
        for с in ("кот — это зверь. кот.", "кот — это зверь. дом.", "quantas", "tinha ", "glyph ##___/#####/#####/#####/#####/#####/##### is not a"):
            assert (своё.fullmatch(с) is None) == (второй.fullmatch(с) is None), (текст, с)
            assert [m.span() for m in своё.finditer(с)] == [m.span() for m in второй.finditer(с)]
        print(f"  {текст[:40]!r}: промах {t1 * 1e3:.2f} мс, попадание {t2 * 1e3:.3f} мс")
    ошибка = _сохранить()
    assert ошибка is None, ошибка
    print(f"  кэш: {файл()}; записей в памяти {состояние()[0]}, записан: {файл().stat().st_size} байт")


if __name__ == "__main__":
    _самопроверка()
