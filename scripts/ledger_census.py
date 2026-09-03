#!/usr/bin/env python3
"""[LEDGER CENSUS] — which worlds answer with a ledger of steps, which with a bare value.

holon's first order (03.09, ONE-CARRIER: the ledger is the program is the
proof): a genus with a computed answer must show its ledger in primitive
steps («a × d = ad, b × c = bc, ad − bc = v»), so the market of compositions
buys the executor from the shows and not from code; the genera WITHOUT a
ledger — a value without its explanation — must be named, so that he knows
where the composition cannot be bought in principle.

The census reads every world of shows and sorts its ANSWERED lines (a
question mark followed by an answer) into three kinds:
  · LEDGER — the answer carries a step: an equation «… = …», a comparison
    «≤ / < / >» chain, a verbal step of the pack's verbal mathematics
    («6 times 4 is 24», «плюс … равно»), or a witness clause after a colon
    («97 is prime; its divisors are 1 and 97»);
  · VALUE — the answer is a number (or numbers) and nothing else;
  · WORD — the answer is a word, a verdict, a name, a list (no number).
A world is «without a ledger» when its answered lines are computed (VALUE)
and none carries a ledger; a world of WORD answers is a market of verdicts
or maps, not of computation, and is listed apart.

Print: a TSV per world (answered, ledger, value, word, share of ledger) and
the two lists holon asked for; --out writes the TSV.
"""
import argparse
import collections
import json
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
from genesis import worlds  # noqa: E402

_ВОПРОС = re.compile(r"\?\s*(.*)$", re.S)
ШАГ = re.compile(r"\d\s*[=≤≥<>]\s*[−-]?\d|\d\s*=\s*[−-]?\d|[=≤≥]\s*\d")
ЧИСЛО = re.compile(r"[−-]?\d+(?:[.,]\d+)?")
ТОЛЬКО_ЧИСЛА = re.compile(r"^[\s\d,.;:−\-+×÷/()%$€£\[\]|]*$")


def _словесные_шаги():
    """The verbal steps of every pack's verbal_math («<a> times <b> is <c>»)
    as patterns: the operation words between the holes."""
    вон = []
    for путь in sorted((КОРЕНЬ / "tools" / "langpacks").glob("*.json")):
        try:
            п = json.loads(путь.read_text(encoding="utf-8"))
        except ValueError:
            continue
        for пара in п.get("verbal_math") or ():
            if not (isinstance(пара, list) and пара and isinstance(пара[0], str)):
                continue
            куски = [re.escape(к.strip()) for к in re.split(r"<[^>]*>", пара[0]) if к.strip()]
            if len(куски) >= 2:
                вон.append(r"\d\s+" + r"\s+\d+\s+".join(куски[-2:]).replace(r"\ ", " ") + r"\s+\d")
    return re.compile("|".join(вон)) if вон else None


СЛОВЕСНЫЙ = _словесные_шаги()


def вид_ответа(строка):
    м = _ВОПРОС.search(строка)
    if not м:
        return None
    ответ = м.group(1).strip()
    if not ответ:
        return None
    if ШАГ.search(ответ) or (СЛОВЕСНЫЙ is not None and СЛОВЕСНЫЙ.search(ответ)):
        return "ledger"
    # a ONE-STEP VERBAL EQUATION in the world's own words («сумма 36 и 6 равна
    # 42», «25% of 16 is 4»): the answer restates every number of the question
    # and adds the result — the step is there, written without a sign
    вопрос = строка[:м.start()]
    ч_в, ч_о = ЧИСЛО.findall(вопрос), ЧИСЛО.findall(ответ)
    if ч_в and set(ч_в) <= set(ч_о) and len(ч_о) > len(set(ч_в)):
        return "ledger"
    if not ЧИСЛО.search(ответ):
        return "word"
    # a witness after the value («97 is prime; its divisors are 1 and 97», «yes: 12 = 3 × 4»)
    if ";" in ответ or ":" in ответ:
        return "ledger" if len(ЧИСЛО.findall(ответ)) >= 2 else "value"
    return "value" if ТОЛЬКО_ЧИСЛА.match(ответ) or len(ЧИСЛО.findall(ответ)) == 1 else "value"


def мир_имя(путь):
    return путь.stem[len("genesis_"):] if путь.stem.startswith("genesis_") else путь.stem


def перепись(пути):
    вон = {}
    for путь in пути:
        с = collections.Counter()
        for строка in путь.read_text(encoding="utf-8").splitlines():
            if not строка.strip() or строка.startswith("\x0c"):
                continue
            в = вид_ответа(строка)
            if в:
                с[в] += 1
        вон[мир_имя(путь)] = с
    return вон


def main():
    ап = argparse.ArgumentParser()
    ап.add_argument("--out", type=pathlib.Path)
    а = ап.parse_args()
    п = перепись(worlds(kind="shows"))
    строки = ["мир\tотвеченных\tледжер\tзначение\tслово\tдоля леджера"]
    без = []; словесные = []
    for имя, с in sorted(п.items(), key=lambda kv: -sum(kv[1].values())):
        всего = sum(с.values())
        if not всего:
            continue
        доля = с["ledger"] / (с["ledger"] + с["value"]) if (с["ledger"] + с["value"]) else 0.0
        строки.append(f"{имя}\t{всего}\t{с['ledger']}\t{с['value']}\t{с['word']}\t{доля:.2f}")
        if с["value"] and not с["ledger"]:
            без.append((имя, с["value"]))
        elif not с["value"] and not с["ledger"] and с["word"]:
            словесные.append((имя, с["word"]))
    текст = "\n".join(строки) + "\n"
    if а.out:
        а.out.write_text(текст, encoding="utf-8")
    else:
        sys.stdout.write(текст)
    всего = collections.Counter()
    for с in п.values():
        всего.update(с)
    print(f"ПЕРЕПИСЬ ЛЕДЖЕРОВ: отвеченных {sum(всего.values())}, с леджером {всего['ledger']}, значением {всего['value']}, словом {всего['word']}; "
          f"миров со значением без леджера {len(без)}: {', '.join(f'{и} ({n})' for и, n in без)}; "
          f"миров словесных ответов {len(словесные)}: {', '.join(и for и, n in словесные)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
