#!/usr/bin/env python3
"""[PLAN COURT] — a task cut into steps, and every step checked by its number; CLOSED WORLD.

A show of the plan world (tools/planforms.py) is one page: the goal, the numbered steps, a
question about the state after a step, and the verdict on the task. The court reads each line
through the house's frames: a page whose repeated holes carry one value (the number of the
answer is the number of the step, the shortfall is named twice by one number), whose totals
accumulate (what stands after step 2 is the sum of steps 1 and 2), whose count form is the
form of its number, whose verdict follows the numbers («yes» only when the goal is reached,
«no» only when both numbers — needed and gathered — are named), whose order names the FIRST
step of the plan and whose step count is the length of the plan, is true; a line of a frame
that breaks any of these is a lie; a line of no frame is a lie of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import planforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"planforms"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): the sum after step 2 is not the sum of the steps; a plan
    # that falls short is declared done; a plan that reaches its goal is declared undone; the
    # order names the SECOND step; the step count is not the length of the plan; the shortfall
    # is named by two different numbers; the count form is not the form of its number (pl, it);
    # the verdict's number is not the number of the step it repeats.
    подсадки = (
        "план: погрузить 9 ящиков. шаг 1 — собрать 5 ящиков, шаг 2 — собрать ещё 4 ящика, "
        "шаг 3 — погрузить все ящики. сколько ящиков после шага 2? 10 ящиков: 5 + 4 = 10. "
        "выполнена ли задача? да: 9 ящиков погружено.",
        "план: погрузить 9 ящиков. шаг 1 — собрать 5 ящиков, шаг 2 — собрать ещё 4 ящика, "
        "шаг 3 — погрузить все ящики. после шага 2 есть 6 ящиков. выполнена ли задача? "
        "да: нужно 9 ящиков, есть 6 ящиков.",
        "plan: load 9 boxes. step 1 — collect 5 boxes, step 2 — collect 4 more boxes, "
        "step 3 — load all the boxes. how many boxes after step 2? 9 boxes: 5 + 4 = 9. "
        "is the task done? no: 9 boxes loaded.",
        "plan : faire 12 petits pains. étape 1 — acheter 2 paquets, étape 2 — faire 12 petits pains. "
        "que faire d'abord : acheter les paquets ou faire les petits pains ? "
        "d'abord faire les petits pains.",
        "plan: hacer 12 panecillos. paso 1 — comprar 2 paquetes, paso 2 — hacer 12 panecillos. "
        "¿cuántos pasos tiene el plan? 3 pasos.",
        "Plan: 9 Kisten laden. Schritt 1 — 5 Kisten sammeln, Schritt 2 — 4 Kisten mehr sammeln, "
        "Schritt 3 — alle Kisten laden. nach Schritt 2 gibt es 6 Kisten. ist die Aufgabe erledigt? "
        "nein: 9 Kisten nötig, 7 Kisten vorhanden.",
        "plan: upiec 12 bułek. krok 1 — kupić 2 paczki, krok 2 — upiec 12 bułek. "
        "ile paczek po kroku 1? 2 paczki. ile bułek po kroku 2? 12 bułek. "
        "czy zadanie jest wykonane? tak: 12 bułka.",
        "план: испечь 12 булок. шаг 1 — купить 2 пачки, шаг 2 — испечь 12 булок. "
        "сколько пачек после шага 1? 2 пачки. сколько булок после шага 2? 12 булок. "
        "выполнена ли задача? да: 11 булок.",
        "piano: fare 12 panini. passo 1 — comprare 2 pacchi, passo 2 — fare 12 panini. "
        "quanti pacchi dopo il passo 1? 2 pacco. quanti panini dopo il passo 2? 12 panini. "
        "è finito il compito? sì: 12 panini.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"ПЛАН FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_planforms.txt"]
    if not пути:  # the world is not in the manifest yet — the court reads its file by name
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_planforms.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_planforms.txt по имени")
    for путь in пути:
        for стр in путь.read_text(encoding="utf-8").splitlines():
            if not стр.strip() or стр.startswith("\x0c"):
                continue
            судимо, истинно = _судить(стр)  # silence counts as unjudged here; the gate closes it
            итог["судимых" if судимо else "несудимых"] += 1
            if судимо and not истинно:
                итог["ложных"] += 1
                if len(примеры) < 5:
                    примеры.append(стр)
    for п in примеры:
        print(f"  ЛОЖЬ: {п[:120]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"ПЛАН {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
