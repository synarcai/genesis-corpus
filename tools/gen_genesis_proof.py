#!/usr/bin/env python3
"""GENESIS layer: THE FORMS OF A PROOF.

    the sum of the first n numbers is n × (n + 1) / 2;
      it holds for n = 1: 1 = 1;
      if it holds for n = 4 then it holds for n = 5: 10 + 5 = 15.
    every whole number is even or odd; 7 is odd; 8 is even.
    all primes are odd is false: 2 is prime and 2 is even.
    if n is even then n squared is even: 4 is even and 16 is even.

A mathematician is not made by theorems but by the SHAPES in which
things are shown to be true. Four shapes are shown here, and each is
shown with an instance that can be checked, because a shape without an
instance is a word:

  · INDUCTION — the base case and the step, both instantiated. The step
    is not asserted («if it holds for n then for n+1») but SHOWN on a
    concrete pair, so the organism meets the move rather than its name.
  · CASES — an exhaustive split with a member of each case, so that
    «even or odd» is met as a partition and not as a slogan.
  · COUNTEREXAMPLE — a universal claim killed by one witness. This is
    the cheapest proof there is and the one most often not taught: a
    corpus that only ever confirms teaches confirmation.
  · DIRECT — a conditional with an instance where the antecedent holds
    and the consequent is checked. A conditional shown only where the
    antecedent FAILS teaches nothing, and this layer never shows one.

WHAT IS ABSENT AND WHY: proof by contradiction is not shown. Its
instances (the irrationality of a root) cannot be checked by counting,
and a shape whose instance cannot be verified is exactly what this
corpus refuses to carry. It waits for a court that can read a
derivation.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import universals  # noqa: E402
from layer import emit  # noqa: E402

ШАГИ = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (2, 3)]
# ЧЁТНОСТЬ ОТЛИЧИМА ОТ ПРОСТОТЫ С ПЕРВОГО ПОКАЗА (holon 03.09, YN-AMBIGUOUS
# prime|parity: все нечётные примеры были простыми, и исполнитель простоты
# делил строки так же, как чётность): нечётные СОСТАВНЫЕ стоят первыми и
# чередуются с простыми и чётными (М-148, разнообразие с первого показа).
ЧИСЛА = [9, 20, 15, 12, 21, 7, 25, 18, 27, 11, 33, 14, 35, 13, 39, 16, 45, 22, 49, 17]
ЧЁТНЫЕ = [4, 6, 8, 10, 12, 14, 16, 20]
ПРОСТЫЕ_ЛОЖЬ = [
    ("all primes are odd", "2 is prime and 2 is even"),
    ("all whole numbers are positive", "0 is whole and 0 is not positive"),
    ("every square is even", "9 is a square and 9 is odd"),
    ("all multiples of 3 are odd", "6 is a multiple of 3 and 6 is even"),
]


def pass_shows(pass_i):
    out = []
    for i in range(8):
        n, m = ШАГИ[(pass_i + i) % len(ШАГИ)]
        x = ЧИСЛА[(pass_i * 3 + i) % len(ЧИСЛА)]
        e = ЧЁТНЫЕ[(pass_i * 5 + i) % len(ЧЁТНЫЕ)]
        ложь, свидетель = ПРОСТЫЕ_ЛОЖЬ[(pass_i + i) % len(ПРОСТЫЕ_ЛОЖЬ)]
        сумма_n = n * (n + 1) // 2
        сумма_m = m * (m + 1) // 2
        # --- индукция: основание и шаг, оба поставленные числами
        out.append("the sum of the first n numbers is n × ( n + 1 ) / 2.")
        out.append(f"it holds for n = 1: 1 = 1.")
        out.append(f"if it holds for n = {n} then it holds for n = {m}: "
                   f"{сумма_n} + {m} = {сумма_m}.")
        out.append(f"если верно для n = {n}, то верно и для n = {m}: "
                   f"{сумма_n} + {m} = {сумма_m}.")
        out.append("основание и шаг вместе дают всё натуральное.")
        # --- разбор случаев: исчерпывающее деление со свидетелем
        out.append(f"every whole number is even or odd; {x} is "
                   f"{'even' if x % 2 == 0 else 'odd'}.")
        out.append(f"всякое целое чётно или нечётно; {x} "
                   f"{'чётно' if x % 2 == 0 else 'нечётно'}.")
        # --- контрпример: одно свидетельство убивает всеобщее
        out.append(f"{ложь} is false: {свидетель}.")
        # A UNIVERSAL IS ASKED BY ITS OWN «IS IT TRUE THAT» (tools/universals.py, М-149).
        out.append(universals.вопрос(f"{ложь} is false: {свидетель}.", ("en", "ru")))
        out.append("one witness kills a universal claim.")
        out.append("одно свидетельство убивает всеобщее утверждение.")
        # --- прямое доказательство: посылка ВЫПОЛНЕНА, следствие проверено
        out.append(f"if n is even then n squared is even: {e} is even and "
                   f"{e * e} is even.")
        out.append(f"если n чётно, то n в квадрате чётно: {e} чётно и "
                   f"{e * e} чётно.")
        # --- ВОПРОСНАЯ ПОВЕРХНОСТЬ: вопрос ПОРОЖДЁН ответом, а не
        # написан рядом. Обе половины строит одна и та же величина, и
        # потому разойтись им негде: закон пары (`tools/asking.py`)
        # требует, чтобы числа вопроса были НАЧАЛЬНЫМ ОТРЕЗКОМ чисел
        # ответа, и ответ судится тем же судом, что и утверждение.
        шаг_en = (f"if it holds for n = {n} then it holds for n = {m}: "
                  f"{сумма_n} + {m} = {сумма_m}.")
        шаг_ru = (f"если верно для n = {n}, то верно и для n = {m}: "
                  f"{сумма_n} + {m} = {сумма_m}.")
        out.append(f"if it holds for n = {n}, does it hold for n = {m}? "
                   f"{шаг_en}")
        out.append(f"если верно для n = {n}, верно ли для n = {m}? "
                   f"{шаг_ru}")
        случай_en = (f"every whole number is even or odd; {x} is "
                     f"{'even' if x % 2 == 0 else 'odd'}.")
        случай_ru = (f"всякое целое чётно или нечётно; {x} "
                     f"{'чётно' if x % 2 == 0 else 'нечётно'}.")
        # THE CHOSEN ALTERNATIVE OPENS THE ANSWER (М-147 for a choice question,
        # holon 03.09: «is # even or odd» read as a value, not a verdict): the
        # word chosen comes first, the witness — the division by two — after.
        чётн = x % 2 == 0
        свид = f"{x} = 2 × {x // 2}" if чётн else f"{x} = 2 × {x // 2} + 1"
        out.append(f"is {x} even or odd? {'even' if чётн else 'odd'}: {свид}.")
        out.append(f"чётно или нечётно {x}? {'чётно' if чётн else 'нечётно'}: {свид}.")
        прямое_en = (f"if n is even then n squared is even: {e} is even "
                     f"and {e * e} is even.")
        прямое_ru = (f"если n чётно, то n в квадрате чётно: {e} чётно и "
                     f"{e * e} чётно.")
        out.append(f"if {e} is even, is {e * e} even? yes: {прямое_en}")
        out.append(f"если {e} чётно, чётно ли {e * e}? да: {прямое_ru}")
        # ВТОРАЯ ПОЛЯРНОСТЬ ТОЙ ЖЕ РАМКОЙ (аудит покупок holon 03.09):
        # одни пары (n, n²) учили «ответ всегда да».
        нечёт = e * e + 1
        out.append(f"if {e} is even, is {нечёт} even? no: {e} is even "
                   f"and {нечёт} is odd.")
        out.append(f"если {e} чётно, чётно ли {нечёт}? нет: {e} чётно, "
                   f"а {нечёт} нечётно.")
        # --- ОТКАЗ ИСЧЕРПАНИЕМ: контрпример наизнанку. Слой умел
        # опровергать одним свидетелем и не умел сказать «свидетеля
        # НЕТ», а это утверждение обо ВСЁМ отрезке и проверяется только
        # проходом. Предел взят из своего же материала — квадрат
        # чётного, уже стоящего в прямом доказательстве.
        out.append(f"there is no even prime between 3 and {e * e}: every "
                   f"even number there has the divisor 2 besides 1 and "
                   f"itself.")
        out.append(f"чётного простого между 3 и {e * e} нет: у всякого "
                   f"чётного там есть делитель 2, кроме 1 и самого себя.")
    out.extend(положительность(pass_i))
    return out


# ПОЛОЖИТЕЛЬНОСТЬ — ВЕРДИКТНАЯ РАМКА ДЛЯ РЫНКА УНИВЕРСАЛИЙ (holon 04.09: «all
# whole numbers are positive is false» ждёт предиката «positive»): обе
# полярности массой — «нет» у нуля и у отрицательных; формы вопроса из пакетов.
# TWO FRAMES OF THE SIGN, EACH WITH BOTH POLARITIES ON DISJOINT ABSOLUTE
# VALUES (holon 04.09, twice): the organism's number reader is unsigned —
# «−3» reads as «3» — so within one frame the absolute values of the «yes»
# numbers and of the «no» numbers never meet, and no reader sees «3 → yes»
# beside «3 → no»; and a «no» shown by zero alone is one number, not a
# polarity (the law of mass wants four distinct), so «is # positive?» carries
# zero AND five negatives whose absolute values are its own. The minus is
# written as the sign U+2212 glued to the digits, as every signed world of
# the corpus writes it (equation_signed, numbers, physics).
ЧИСЛА_ПОЛОЖ = (7, 0, 12, -10, 1, 20, -13, 0, 5, -16, 9, 15, -18, 0, 3, -19)
ЧИСЛА_ЗНАКА = (2, -3, 6, -8, 11, -1, 14, -12, 17, -4)
for _ряд in (ЧИСЛА_ПОЛОЖ, ЧИСЛА_ЗНАКА):
    assert not {abs(n) for n in _ряд if n < 0} & {n for n in _ряд if n > 0}


def _формы(язык, род):
    import json
    пакет = json.loads((pathlib.Path(__file__).resolve().parent / "langpacks" / f"{язык}.json").read_text(encoding="utf-8"))
    return пакет["ask_forms"][род]


def _ответ(n):
    з = str(n).replace("-", "−")
    if n > 0:
        return з, f"yes: {з} > 0.", f"да: {з} > 0."
    if n < 0:
        return з, f"no: {з} < 0.", f"нет: {з} < 0."
    return з, "no: 0 is not above 0.", "нет: 0 не больше 0."


def положительность(pass_i):
    """Form 0 of ask_forms.positive («is {} positive?») and form 1 («is {} above
    zero?») — two frames, each over its own signed numbers."""
    out = []
    формы_en, формы_ru = _формы("en", "positive"), _формы("ru", "positive")
    for i in range(8):
        n = ЧИСЛА_ПОЛОЖ[(pass_i * 5 + i) % len(ЧИСЛА_ПОЛОЖ)]
        з, отв_en, отв_ru = _ответ(n)
        out.append(f"{формы_en[0].format(з)} {отв_en}")
        out.append(f"{формы_ru[0].format(з)} {отв_ru}")
        m = ЧИСЛА_ЗНАКА[(pass_i * 3 + i) % len(ЧИСЛА_ЗНАКА)]
        з, отв_en, отв_ru = _ответ(m)
        out.append(f"{формы_en[1].format(з)} {отв_en}")
        out.append(f"{формы_ru[1].format(з)} {отв_ru}")
    return out


def main():
    emit("datasets/genesis_proof.txt", pass_shows)


if __name__ == "__main__":
    main()
