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
  · VALUE — the answer is a number COMPUTED from the question's numbers and
    nothing else: the derivation is owed and missing;
  · READ-OFF — the answer is a number READ OFF the question: the question
    carries ONE number and the answer repeats it («the trip takes 3 days.
    how long does the trip take? 3 days.»). Nothing was computed, so no
    ledger is owed and none can honestly be written;
  · UNSUPPORTED — the question carries NO number at all («how many balls
    does mary have left? 6 balls left.»). The line alone shows neither the
    inputs nor the derivation, and the instrument reads lines: it cannot
    tell whether the genus explains itself on another surface. Naming this
    kind apart is the same law as the read-off: an instrument may not call
    a debt what it did not verify — nor deny one;
  · WORD — the answer is a word, a verdict, a name, a list (no number).
A world is «without a ledger» when its answered lines are COMPUTED and none
carries a ledger; a world of WORD answers is a market of verdicts or maps,
not of computation, and is listed apart.

The read-off kind is М-167 applied to this instrument itself (04.09): its
first shape called every bare number a debt and so named 13 376 of them,
counting among them the whole of `holes` (1200) and `unit_counts` (360),
where the answer is the question's own number and there is nothing to
derive. An instrument that names a debt where none exists claims more than
it verified; the debt it prints now is the debt that is real.

The unsupported kind is the same law read backwards, and it was bought by a
mistake of the same hour: the first cure called a numberless question a
read-off, and so quietly ACQUITTED all 1440 lines of `story`, where the
question stands alone («how many balls does mary have left? 6 balls left.»)
and its story lives on another line of the world. An instrument that reads
lines may not pronounce on a page.

Print: a TSV per world (answered, ledger, computed, read-off, unsupported,
word, share of ledger) and the two lists holon asked for; --out writes it.
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
        if len(ЧИСЛО.findall(ответ)) >= 2:
            return "ledger"
    return _вид_значения(ч_в, ч_о)


def _вид_значения(ч_в, ч_о):
    """Computed, read off, or beyond the line's reach — decided by the numbers.

      · the question carries NO number: the line shows nothing to derive FROM,
        and the instrument reads lines — «unsupported», not a debt and not an
        acquittal;
      · the question carries ONE distinct number and every number of the
        answer is that number: there was nothing to combine it WITH, so the
        answer was read off and no ledger is owed;
      · otherwise the answer was computed and its ledger is owed.
    Two distinct numbers in the question always count as computed, even when
    the result coincides with one of them («had 8, gave 4 away, keeps 4»):
    the coincidence is a fact about the values, not about the work done.
    """
    свои = set(ч_в)
    if not свои:
        return "unsupported"
    if len(свои) == 1 and set(ч_о) <= свои:
        return "read-off"
    return "value"


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
    строки = ["мир\tотвеченных\tледжер\tвычислено\tпрочтено\tбез опоры\tслово\tдоля леджера"]
    без = []; словесные = []
    for имя, с in sorted(п.items(), key=lambda kv: -sum(kv[1].values())):
        всего = sum(с.values())
        if not всего:
            continue
        доля = с["ledger"] / (с["ledger"] + с["value"]) if (с["ledger"] + с["value"]) else 0.0
        строки.append(f"{имя}\t{всего}\t{с['ledger']}\t{с['value']}\t{с['read-off']}\t{с['unsupported']}\t{с['word']}\t{доля:.2f}")
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
    print(f"ПЕРЕПИСЬ ЛЕДЖЕРОВ: отвеченных {sum(всего.values())}, с леджером {всего['ledger']}, вычислено без леджера {всего['value']}, "
          f"прочтено с вопроса {всего['read-off']}, без опоры в строке {всего['unsupported']}, словом {всего['word']}; "
          f"миров со значением без леджера {len(без)}: {', '.join(f'{и} ({n})' for и, n in без)}; "
          f"миров словесных ответов {len(словесные)}: {', '.join(и for и, n in словесные)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
