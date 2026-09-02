#!/usr/bin/env python3
"""GENESIS layer: FOUNDATIONS OF INFORMATICS — and of control.

Six subjects of informatics and two of cybernetics stood absent from
the whole corpus. They are not advanced topics: they are the ideas
without which a programmer is a typist.

  · ENTROPY is why a message costs bits at all — the bridge between
    counting outcomes and paying for them;
  · THE AUTOMATON is state and transition, the smallest machine that
    REMEMBERS. It is executed here, not described;
  · THE GRAMMAR is a language given by rules rather than by a list —
    the first object that is infinite and finite at once;
  · DECIDABILITY is the discovery that some questions have no general
    algorithm. It cannot be computed, and so it is DECLARED beside the
    computable ones it qualifies (М-103);
  · THE TYPE is the genus of a value: 7 is whole, 7 ÷ 2 is not;
  · THE INVARIANT is what a loop preserves — the only honest way to
    know a loop without running it forever;
  · HOMEOSTASIS is a regulator holding a value inside bounds;
  · THE MODEL is Conant–Ashby: to control a system one must have a
    model of it, and an observer that cannot tell its states apart
    cannot control it.

EVERYTHING IS EXECUTED. The automaton is run, the grammar derived, the
loop unrolled, the clamp applied. Only decidability is declared, and it
is declared as declared.
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rugram  # noqa: E402
from layer import emit_grouped  # noqa: E402


# ИСКОМОЕ ОБЪЯВЛЯЕТ СВОЙ ВОПРОС ОДИН РАЗ, и вопрос берёт ТУ ЖЕ фразу
# предмета, какую берёт ответ. Замер вопросной поверхности назвал этот
# мир немым: 1070 строк, вопросов ноль.
СПРОСИТЬ = {
    "carry": "how many bits do {предмет} carry?",
    "cost": "how much does {предмет} cost?",
    "entropy": "what is the entropy of {предмет}?",
    "несут": "сколько бит несут {предмет}?",
    "стоит": "сколько бит стоит {предмет}?",
    "энтропия": "чему равна энтропия {предмет}?",
}


def спросить(искомое, предмет, ответ):
    """Вопрос о предмете и ответ о нём же — одной строкой."""
    return f"{СПРОСИТЬ[искомое].format(предмет=предмет)} {ответ}"


def степень_двойки(n):
    """Степень ли двойки — отказ считает основание, а не верит."""
    return n >= 2 and not n & (n - 1)


def отказ_алфавита(шаг):
    """Вопрос, чей честный ответ — «целого нет, и вот почему».

    ЗНАК АЛФАВИТА СТОИТ ЦЕЛОЕ ЧИСЛО БИТ ЛИШЬ ТОГДА, КОГДА АЛФАВИТ ЕСТЬ
    СТЕПЕНЬ ДВОЙКИ. Мир пишет цену только на таких алфавитах — таков
    его закон, — и отказ называет основание числом: сам размер и то,
    что он степенью двойки не является.
    """
    вон = []
    for i in range(10):
        n = 3 + (шаг * 3 + i) % 12
        if степень_двойки(n):
            continue
        вон.append(f"how many bits does a sign of an alphabet of {n} "
                   f"signs cost? no whole answer for {n} signs: {n} is "
                   f"not a power of two.")
        # ЧИСЛО СТОИТ ТАМ, ГДЕ СЧЁТНАЯ ФОРМА ПРАВА, — при числе, а не
        # после предлога: «для 3 знака» было бы неверно (предлог требует
        # родительного, а счётная форма даёт «знака»), и мир учил бы
        # неверному управлению с полной судимостью.
        вон.append(f"сколько бит стоит знак алфавита в {n} "
                   f"{rugram.форма('знак', n)}? целого ответа нет: "
                   f"{n} {rugram.форма('знак', n)} — это не степень "
                   f"двойки.")
    return вон


def энтропия(шаг):
    """Число равновозможных исходов и цена сообщения в битах."""
    вон = []
    for k in range(1, 9):
        исходов = 2 ** k
        пред_ru = (f"{исходов} "
                   f"{rugram.форма('равновозможный исход', исходов)}")
        пред_en = f"{исходов} equally likely outcomes"
        утв_ru = f"{пред_ru} несут {k} {rugram.форма('бит', k)}."
        утв_en = (f"{пред_en} carry {k} "
                  f"{'bit' if k == 1 else 'bits'}.")
        вон.append(утв_ru)
        вон.append(утв_en)
        вон.append(спросить("несут", пред_ru, утв_ru))
        вон.append(спросить("carry", пред_en, утв_en))
        длина = 1 + (k % 4)
        алфавит = 2 ** (1 + (k % 3))
        цена = длина * (1 + (k % 3))
        сл_ru = (f"слово из {длина} {rugram.форма('знак', длина)} "
                 f"алфавита в {алфавит} "
                 f"{rugram.форма('знак', алфавит)}")
        сл_en = (f"a word of {длина} signs over an alphabet of "
                 f"{алфавит} signs")
        утв_сл_ru = f"{сл_ru} стоит {цена} {rugram.форма('бит', цена)}."
        утв_сл_en = f"{сл_en} costs {цена} bits."
        вон.append(утв_сл_ru)
        вон.append(утв_сл_en)
        вон.append(спросить("стоит", сл_ru, утв_сл_ru))
        вон.append(спросить("cost", сл_en, утв_сл_en))
        # ПОНЯТИЕ БЕЗ ИМЕНИ НЕ ВЫУЧЕНО: показать счёт битов и не назвать
        # его энтропией значит оставить читателя без слова, которым он
        # найдёт это знание везде.
        # ОБОРОТ ВЫБРАН СЧЁТНЫЙ: «энтропия N исходов» есть родительный
        # по управлению, и суд согласования, не знающий синтаксиса,
        # звал бы его ложью. Приложение оставляет именительный счётный
        # и там, и там.
        утв_э_ru = (f"{пред_ru}: энтропия {k} "
                    f"{rugram.форма('бит', k)}.")
        утв_э_en = (f"{пред_en}: entropy {k} "
                    f"{'bit' if k == 1 else 'bits'}.")
        вон.append(утв_э_ru)
        вон.append(утв_э_en)
        вон.append(спросить("энтропия", пред_ru, утв_э_ru))
        вон.append(спросить("entropy", пред_en, утв_э_en))
    return вон


def автомат(шаг):
    """Автомат чётности: состояние помнит, сколько единиц пришло."""
    вон = []
    входы = ("1 0 1", "1 1", "0 0 1", "1 0 0 1 1", "1", "0",
             "1 1 1", "0 1 0 1")
    for вход in входы:
        единиц = sum(1 for x in вход.split() if x == "1")
        итог = "чётное" if единиц % 2 == 0 else "нечётное"
        итог_en = "even" if единиц % 2 == 0 else "odd"
        вон.append(f"автомат чётности: вход {вход}; "
                   f"состояние после — {итог}.")
        вон.append(f"parity automaton: input {вход}; "
                   f"the state after is {итог_en}.")
    return вон


def грамматика(шаг):
    """Правило S → a S b порождает ровно a^n b^n."""
    вон = []
    for n in range(1, 7):
        слово = "a " * n + "b " * n
        вон.append(f"правило S → a S b, применённое {n} "
                   f"{rugram.форма('раз', n)}, даёт {слово.strip()}.")
        вон.append(f"the rule S → a S b applied {n} "
                   f"{'time' if n == 1 else 'times'} gives "
                   f"{слово.strip()}.")
        вон.append(f"формальная грамматика с правилом S → a S b "
                   f"порождает строку {слово.strip()}.")
        вон.append(f"the formal grammar with rule S → a S b generates "
                   f"the string {слово.strip()}.")
    return вон


def разрешимость(шаг):
    """Что решается алгоритмом и что не решается вовсе."""
    вон = []
    for i in range(6):
        a, b = 12 + i * 3, 3 + (i % 4)
        ответ = "да" if a % b == 0 else "нет"
        ответ_en = "yes" if a % b == 0 else "no"
        вон.append(f"делится ли {a} на {b} — вопрос разрешимый; "
                   f"ответ {ответ}.")
        вон.append(f"is {a} divisible by {b} — a decidable question; "
                   f"the answer is {ответ_en}.")
    вон.append("остановится ли всякая программа на всяком входе — "
               "вопрос неразрешимый: общего алгоритма нет.")
    вон.append("whether every program halts on every input is "
               "undecidable: there is no general algorithm.")
    return вон


def тип(шаг):
    """Род значения: целое или дробь, и деление это меняет."""
    вон = []
    for i in range(12):
        a, b = 6 + i, 2 + (i % 4)
        целое = a % b == 0
        род = "целое" if целое else "дробь"
        род_en = "whole" if целое else "a fraction"
        вон.append(f"тип значения {a} — целое; тип значения "
                   f"{a} ÷ {b} — {род}.")
        вон.append(f"the type of {a} is whole; the type of "
                   f"{a} ÷ {b} is {род_en}.")
    return вон


def инвариант(шаг):
    """Что цикл сохраняет на каждом шаге."""
    вон = []
    for i in range(10):
        шагов = 2 + (i % 5)
        прибавка = 2
        итог = шагов * прибавка
        вон.append(f"цикл: x = 0; повторить {шагов} "
                   f"{rugram.форма('раз', шагов)} x = x + {прибавка}. "
                   f"инвариант: x чётно на каждом шаге. выход x = {итог}.")
        вон.append(f"loop: x = 0; repeat {шагов} times x = x + "
                   f"{прибавка}. invariant: x is even at every step. "
                   f"exit x = {итог}.")
    return вон


def гомеостаз(шаг):
    """Регулятор держит величину в объявленных пределах."""
    вон = []
    for i in range(12):
        низ, верх = 2 + (i % 4), 8 + (i % 5)
        возмущение = низ - 2 - (i % 3) if i % 2 else верх + 1 + (i % 4)
        вернул = min(max(возмущение, низ), верх)
        вон.append(f"регулятор держит значение между {низ} и {верх}: "
                   f"при возмущении {возмущение} он вернул {вернул}.")
        вон.append(f"the regulator holds the value between {низ} and "
                   f"{верх}: given {возмущение} it returned {вернул}.")
        # ЧИСЛО ПЕРЕД СУЩЕСТВИТЕЛЬНЫМ НЕ ВСЕГДА СЧЁТ: «между 3 и 9
        # значение» — девятка есть предел, а «значение» к ней не
        # относится. Оборот переставлен так, что число стоит ПОСЛЕ
        # имени и ловушки нет вовсе.
        вон.append(f"гомеостаз есть удержание величины в пределах "
                   f"от {низ} до {верх}: значение {вернул} допустимо.")
        вон.append(f"homeostasis is holding a value inside bounds "
                   f"from {низ} to {верх}: the value {вернул} "
                   f"is allowed.")
    return вон


def модель(шаг):
    """Управление требует модели: наблюдатель обязан различать состояния."""
    вон = []
    for i in range(10):
        состояний = 2 + (i % 6)
        различает = состояний if i % 2 == 0 else max(1, состояний - 2)
        можно = различает >= состояний
        вон.append(f"модель системы имеет {состояний} "
                   f"{rugram.форма('состояние', состояний)}; наблюдатель "
                   f"различает {различает}: управление "
                   f"{'возможно' if можно else 'невозможно'}.")
        вон.append(f"the model of the system has {состояний} states; "
                   f"the observer tells apart {различает}: control is "
                   f"{'possible' if можно else 'impossible'}.")
    return вон


ГРУППЫ = (отказ_алфавита, энтропия, автомат, грамматика, разрешимость,
          тип, инвариант, гомеостаз, модель)


def pass_groups(pass_i):
    return [сделать(pass_i) for сделать in ГРУППЫ]


def main():
    emit_grouped("datasets/genesis_compsci.txt", pass_groups)


if __name__ == "__main__":
    main()
