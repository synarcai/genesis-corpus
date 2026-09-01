#!/usr/bin/env python3
"""GENESIS layer: THE FOUNDATIONS OF CYBERNETICS.

    target 10, value 4, error 6.
    after a step of 3 the value is 7 and the error is 3.
    starting at 4 with target 10 and step 2 the value reaches 10 in 3 steps.
    machine A B C; on 1 A goes to B; on 1 B goes to C; from A the input 1 1 leads to C.
    to distinguish 8 disturbances a regulator needs 3 bits.

CYBERNETICS IS THE SCIENCE OF CONTROL, and control is exactly the place
where a corpus can lie most comfortably: «feedback corrects the system»
is a sentence no instrument can check. So the layer says nothing it
cannot show as a NUMBER or a WALK:
  · the ERROR is a subtraction, and every step of it is arithmetic;
  · CONVERGENCE is a count of steps, and the count is simulated;
  · a MACHINE is a set of transitions, and «this input leads to that
    state» is a walk, not an opinion;
  · REQUISITE VARIETY is a relation between the number of states a
    regulator has and the number of disturbances it can tell apart —
    Ashby's law as an inequality, checkable on both sides;
  · the BITS needed for n distinctions are ceil(log2 n), the same fact
    the algorithms layer teaches as binary search — one fact, two
    faces, and the organism should meet both.

OPEN AND CLOSED LOOP are shown as what they DO, not as what they are
called: an open loop repeats its step regardless of the error and
overshoots; a closed loop stops when the error is zero. The difference
is visible in the numbers, which is the only way it can be taught.
"""

import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import json  # noqa: E402

from langpack import count_form_index  # noqa: E402
from layer import emit  # noqa: E402
from plural import by_count  # noqa: E402

RU_PACK = json.loads(
    (pathlib.Path(__file__).resolve().parent
     / "langpacks/ru.json").read_text(encoding="utf-8"))
RU_RULE = {"forms": ["one", "few", "many"],
           "count_agreement": RU_PACK["count_agreement"]}
# РУССКОЕ СОГЛАСОВАНИЕ НЕ ПЕРЕПИСАНО, А ПРОЧИТАНО: правило 1 / 2–4 / 5+
# живёт данными в пакете языка, и вторая копия разошлась бы с первой.
ФОРМЫ = {
    "шаг": ("шаг", "шага", "шагов"),
    "бит": ("бит", "бита", "бит"),
    "возмущение": ("возмущение", "возмущения", "возмущений"),
    "состояние": ("состояние", "состояния", "состояний"),
}


def ру(слово, k):
    return ФОРМЫ[слово][count_form_index(RU_PACK, RU_RULE, k)]

# (цель, начальное, шаг) — цель достижима шагом ровно
КОНТУРЫ = [(10, 4, 2), (12, 3, 3), (20, 5, 5), (9, 1, 2), (16, 4, 4),
           (15, 3, 6), (18, 6, 4), (14, 2, 3), (24, 4, 5), (11, 5, 2)]
СОСТОЯНИЙ = [2, 4, 8, 16, 3, 5, 6, 10, 32, 12]
МАШИНЫ = [
    (("A", "B", "C"), (("A", "1", "B"), ("B", "1", "C")), "A", "1 1", "C"),
    (("A", "B", "C"), (("A", "1", "B"), ("B", "0", "A")), "A", "1 0", "A"),
    (("A", "B", "C", "D"),
     (("A", "1", "B"), ("B", "1", "C"), ("C", "1", "D")), "A", "1 1 1", "D"),
    (("A", "B"), (("A", "1", "B"), ("B", "1", "A")), "A", "1 1", "A"),
    (("A", "B", "C"),
     (("A", "0", "C"), ("C", "1", "B")), "A", "0 1", "B"),
    (("A", "B", "C", "D"),
     (("A", "1", "B"), ("B", "0", "C"), ("C", "1", "D")), "A", "1 0 1", "D"),
]


def pass_shows(pass_i):
    out = []
    for i in range(10):
        цель, нач, шаг = КОНТУРЫ[(pass_i + i) % len(КОНТУРЫ)]
        n = СОСТОЯНИЙ[(pass_i * 3 + i) % len(СОСТОЯНИЙ)]
        состояния, переходы, старт, вход, конец = МАШИНЫ[
            (pass_i * 5 + i) % len(МАШИНЫ)]
        ошибка = цель - нач
        # --- ошибка и один шаг
        out.append(f"target {цель}, value {нач}, error {ошибка}.")
        out.append(f"цель {цель}, значение {нач}, ошибка {ошибка}.")
        # ПОКАЗ САМОДОСТАТОЧЕН: перестановка проходов разводит соседние
        # строки, и «после шага 4 значение равно 8» без своей цели не
        # значит ничего и не судится ничем.
        out.append(f"target {цель}, value {нач}: after a step of {шаг} the "
                   f"value is {нач + шаг} and the error is {ошибка - шаг}.")
        out.append(f"цель {цель}, значение {нач}: после шага {шаг} значение "
                   f"равно {нач + шаг}, а ошибка равна {ошибка - шаг}.")
        # --- сходимость: счёт шагов
        шагов = ошибка // шаг
        if ошибка % шаг == 0:
            out.append(f"starting at {нач} with target {цель} and step "
                       f"{шаг} the value reaches {цель} in {шагов} steps.")
            out.append(f"начав с {нач} при цели {цель} и шаге {шаг}, "
                       f"значение достигает {цель} за {шагов} {ру('шаг', шагов)}.")
            out.append(f"target {цель}: a closed loop stops at {цель} "
                       f"because the error is 0.")
            out.append(f"target {цель}: an open loop takes one step more "
                       f"and reaches {цель + шаг}, overshooting by {шаг}.")
        # --- машина: переходы и обход
        текст = "; ".join(f"on {в} {a} goes to {b}" for a, в, b in переходы)
        out.append(f"machine {' '.join(состояния)}; {текст}; from {старт} "
                   f"the input {вход} leads to {конец}.")
        out.append(f"machine {' '.join(состояния)}; {текст}; this machine "
                   f"has {len(состояния)} states and {len(переходы)} "
                   f"transitions.")
        # --- закон необходимого разнообразия
        бит = math.ceil(math.log2(n)) if n > 1 else 1
        out.append(f"a regulator with {n} states can distinguish {n} "
                   f"disturbances.")
        out.append(f"регулятор с {n} состояниями различает {n} "
                   f"{ру('возмущение', n)}.")
        out.append(f"to distinguish {n} disturbances a regulator needs "
                   f"{бит} {by_count(бит, 'bits')}.")
        out.append(f"чтобы различить {n} {ру('возмущение', n)}, регулятору нужно "
                   f"{бит} {ру('бит', бит)}.")
    return out


def main():
    emit("datasets/genesis_cybernetics.txt", pass_shows)


if __name__ == "__main__":
    main()
