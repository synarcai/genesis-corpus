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
import mass  # noqa: E402
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
# МАССА ОТ ПРАВИЛА (tools/mass.py, М-148): контур составляется из трёх
# взаимно простых циклов — шаг, число шагов, начало; цель = начало +
# шагов × шаг — различных контуров до 385 (было 10: таблица повторялась
# каждым проходом).
ШАГИ = [2, 3, 4, 5, 6]
ЧИСЛО_ШАГОВ = [3, 2, 5, 4, 6, 1, 7]
НАЧАЛА = [4, 3, 5, 1, 6, 2, 8, 7, 9, 10, 11]
СОСТОЯНИЙ = [2, 4, 8, 16, 3, 5, 6, 10, 32, 12, 7, 9, 11, 13, 14, 15, 17,
             18, 20, 24, 64, 25, 28]
ШИРИНА = 10


def контур(k):
    """(цель, начало, шаг) k-го контура — цель достигается ровно."""
    шаг = ШАГИ[k % len(ШАГИ)]
    m = ЧИСЛО_ШАГОВ[k % len(ЧИСЛО_ШАГОВ)]
    нач = НАЧАЛА[k % len(НАЧАЛА)]
    return нач + m * шаг, нач, шаг
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


# ИСКОМОЕ ОБЪЯВЛЯЕТ СВОЙ ВОПРОС ОДИН РАЗ, и вопрос берёт ТУ ЖЕ фразу
# предмета, какую берёт ответ. Замер вопросной поверхности назвал этот
# мир немым: 700 строк, вопросов ноль.
СПРОСИТЬ = {
    "steps": "how many steps does {предмет} take?",
    "distinguish": "how many disturbances can {предмет} distinguish?",
    "bits": "how many bits does {предмет} need?",
    "шаги": "за сколько шагов {предмет} достигает цели?",
    "различает": "сколько возмущений различает {предмет}?",
    "биты": "сколько бит нужно, чтобы {предмет}?",
    "exact": "does {предмет} land exactly on the target?",
    "точно": "попадает ли {предмет} точно в цель?",
}


def спросить(искомое, предмет, ответ):
    """Вопрос о предмете и ответ о нём же — одной строкой."""
    return f"{СПРОСИТЬ[искомое].format(предмет=предмет)} {ответ}"


import discourse  # noqa: E402
import laws  # noqa: E402


def рассужд_сходимость(pass_i):
    """Счёт шагов рассуждением (дом речи): свидетель — «нач + шагов × шаг =
    цель», вывод — утверждение мира, закон — замкнутый контур."""
    out = []
    зак_en, зак_ru = laws.ЗАКОНЫ["cybernetics"][1][2], laws.ЗАКОНЫ["cybernetics"][1][3]
    for i in range(10):
        цель, нач, шаг = контур(mass.шаг(pass_i, i, ШИРИНА))
        ошибка = цель - нач
        шагов = ошибка // шаг
        св_en = f"{нач} + {шагов} × {шаг} = {цель}"
        св_ru = f"{нач} + {шагов} × {шаг} = {цель}"
        выв_en = f"starting at {нач} with target {цель} and step {шаг} the value reaches {цель} in {шагов} {by_count(шагов, 'steps')}"
        выв_ru = f"начав с {нач} при цели {цель} и шаге {шаг}, значение достигает {цель} за {шагов} {ру('шаг', шагов)}"
        if i % 2 == 0:
            out.append(discourse.рассуждение_величины("en", f"how many steps does starting at {нач} with target {цель} and step {шаг} take", св_en, выв_en, зак_en))
            out.append(discourse.рассуждение_величины("ru", f"за сколько шагов начав с {нач} при цели {цель} и шаге {шаг} достигает цели", св_ru, выв_ru, зак_ru))
        else:
            out.append(discourse.почему("en", f"why does starting at {нач} with target {цель} and step {шаг} take {шагов} {by_count(шагов, 'steps')}", св_en, выв_en, зак_en))
            out.append(discourse.почему("ru", f"почему начав с {нач} при цели {цель} и шаге {шаг}, значение достигает цели за {шагов} {ру('шаг', шагов)}", св_ru, выв_ru, зак_ru))
    return out


def pass_shows(pass_i):
    out = list(laws.ступень("cybernetics")) + рассужд_сходимость(pass_i)
    for i in range(10):
        k = mass.шаг(pass_i, i, ШИРИНА)
        цель, нач, шаг = контур(k)
        n = СОСТОЯНИЙ[k % len(СОСТОЯНИЙ)]
        состояния, переходы, старт, вход, конец = МАШИНЫ[k % len(МАШИНЫ)]
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
        пред_en = (f"starting at {нач} with target {цель} and "
                   f"step {шаг}")
        пред_ru = f"начав с {нач} при цели {цель} и шаге {шаг}"
        утв_en = f"{пред_en} the value reaches {цель} in {шагов} {by_count(шагов, 'steps')}."
        утв_ru = (f"{пред_ru}, значение достигает {цель} за "
                  f"{шагов} {ру('шаг', шагов)}.")
        out.append(утв_en)
        out.append(утв_ru)
        out.append(спросить("steps", пред_en, утв_en))
        out.append(спросить("шаги", пред_ru, утв_ru))
        # ТОЧНОСТЬ — ВОПРОС «ДА/НЕТ» (М-147): вопрос о числе шагов не
        # кончается отказом; попадёт ли контур в цель ровно — свой вопрос,
        # и обе полярности рядом: «да» с числом шагов, «нет» с остатком.
        # Цель названа первой — ответ открывается ею (дом пары, М-145).
        if i % 2 == 0:
            ц, о = цель, ошибка
            отв_en = f"yes: {ц} − {нач} = {о}, {о} ÷ {шаг} = {шагов}."
            отв_ru = f"да: {ц} − {нач} = {о}, {о} ÷ {шаг} = {шагов}."
        else:
            ц, о = цель + 1, ошибка + 1
            отв_en = f"no: {ц} − {нач} = {о}, {о} is not divisible by {шаг}."
            отв_ru = f"нет: {ц} − {нач} = {о}, {о} не делится на {шаг} нацело."
        out.append(спросить("exact", f"a loop with target {ц} starting at {нач} with step {шаг}", отв_en))
        out.append(спросить("точно", f"контур с целью {ц}, начав с {нач} при шаге {шаг}", отв_ru))
        out.append(f"target {цель}: a closed loop stops at {цель} "
                   f"because the error is 0.")
        out.append(f"target {цель}: an open loop takes one step more "
                   f"and reaches {цель + шаг}, overshooting by {шаг}.")
        текст = "; ".join(f"on {в} {a} goes to {b}" for a, в, b in переходы)
        out.append(f"machine {' '.join(состояния)}; {текст}; from {старт} "
                   f"the input {вход} leads to {конец}.")
        out.append(f"machine {' '.join(состояния)}; {текст}; this machine "
                   f"has {len(состояния)} states and {len(переходы)} "
                   f"transitions.")
        # --- закон необходимого разнообразия
        бит = math.ceil(math.log2(n)) if n > 1 else 1
        рег_en = f"a regulator with {n} states"
        рег_ru = f"регулятор с {n} состояниями"
        утв_р_en = f"{рег_en} can distinguish {n} disturbances."
        утв_р_ru = f"{рег_ru} различает {n} {ру('возмущение', n)}."
        out.append(утв_р_en)
        out.append(утв_р_ru)
        out.append(спросить("distinguish", рег_en, утв_р_en))
        out.append(спросить("различает", рег_ru, утв_р_ru))
        бит_en = f"to distinguish {n} disturbances a regulator"
        утв_б_en = (f"{бит_en} needs {бит} "
                    f"{by_count(бит, 'bits')}.")
        out.append(утв_б_en)
        out.append(спросить("bits", бит_en, утв_б_en))
        out.append(f"чтобы различить {n} {ру('возмущение', n)}, регулятору нужно "
                   f"{бит} {ру('бит', бит)}.")
    return out


def main():
    emit("datasets/genesis_cybernetics.txt", pass_shows)


if __name__ == "__main__":
    main()
