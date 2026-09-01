#!/usr/bin/env python3
"""GENESIS layer: THE SURFACES OF AN ACT — one fact, many ways to say it.

The dialogue probe came back mute on «сложение 7 и 6 даёт», «the
addition of 9 and 8 gives» and «сорок два минус пять будет». The corpus
knew the arithmetic — it had said «7 + 6 = 13» and «7 plus 6 is 13»
thousands of times. What it had never said was the act NAMED AS A NOUN.

NOMINALISATION IS NOT DECORATION. It is how a language turns a doing
into a thing that can itself be talked about — the move from «add» to
«addition», from «сложить» to «сложение» — and it is the grammatical
engine of every scientific sentence ever written: «the DECOMPOSITION of
the field», «the CONVERGENCE of the series», «сходимость последовательности».
An organism that has only verbs can execute; an organism that has
nominalisations can REASON ABOUT executions. This is the cheapest
possible purchase of that power, and the corpus had none of it.

FOUR NAMES PER ACT, and they are not synonyms:
    ГЛАГОЛ         — the doing: «умножить на»
    НОМИНАЛИЗАЦИЯ  — the doing as a thing: «умножение»
    ИМЯ РЕЗУЛЬТАТА — the result as a thing: «произведение»
    УПРАВЛЕНИЕ     — which preposition each takes, and it DIFFERS:
                     «сложение A И B», «вычитание B ИЗ A»,
                     «умножение A НА B», «деление A НА B».
Government is the part a table of synonyms cannot carry and a language
model must have: it is where «вычитание 12 из 5» is not a small error
but the opposite claim.

RUSSIAN AGREEMENT COMES FREE AND IS JUDGED. «сумма … равнА» but
«произведение … равнО»: the copula agrees with the GENDER of the result
noun, which the pack declares. The court checks it, so the layer cannot
teach a wrong ending with full judgeability.

NUMBERS SPOKEN, NOT ONLY WRITTEN. «сорок два минус пять будет тридцать
семь» — the numerals come from `tools/numerals.py`, which names a number
by the pack's own declared table and reads it back to prove the name;
a number the language cannot name is not uttered at all.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import numerals  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ДЕЙСТВИЕ ОБЪЯВЛЯЕТ ДВЕ ФРАЗЫ И РОД ИМЕНИ РЕЗУЛЬТАТА — БОЛЬШЕ
# НИЧЕГО. Вопрос НЕ объявляется: он выводится из той же фразы, что и
# ответ. Первая редакция держала вопрос отдельной строкой — и тут же
# солгала управлением: спрашивала «что даёт вычитание 4 И 2?», а
# отвечала «вычитание 2 ИЗ 4». Две записи одного управления расходятся
# в первой же строке; управление объявлено ОДИН раз.
#   (знак, фраза номинализации, фраза имени результата, род имени)
ДЕЙСТВИЯ = {
 "ru": (
   ("+", "сложение {a} и {b}", "сумма {a} и {b}", "ж"),
   ("-", "вычитание {b} из {a}", "разность {a} и {b}", "ж"),
   ("*", "умножение {a} на {b}", "произведение {a} и {b}", "с"),
   ("/", "деление {a} на {b}", "частное {a} и {b}", "с"),
 ),
 "en": (
   ("+", "the addition of {a} and {b}", "the sum of {a} and {b}", "-"),
   ("-", "the subtraction of {b} from {a}",
    "the difference of {a} and {b}", "-"),
   ("*", "the multiplication of {a} by {b}",
    "the product of {a} and {b}", "-"),
   ("/", "the division of {a} by {b}",
    "the quotient of {a} and {b}", "-"),
 ),
}
# ЯЗЫК ОБЪЯВЛЯЕТ, ЧЕМ ФРАЗА СТАНОВИТСЯ УТВЕРЖДЕНИЕМ И ЧЕМ — ВОПРОСОМ.
#   (глагол номинализации, вопрос к ней,
#    {род: связка результата}, {род: вопрос к результату})
РЕЧЬ = {
 "ru": ("даёт", "что даёт {фраза}?",
        {"ж": "равна", "с": "равно"},
        {"ж": "чему равна {фраза}?", "с": "чему равно {фраза}?"}),
 "en": ("gives", "what does {фраза} give?",
        {"-": "is"}, {"-": "what is {фраза}?"}),
}


def _пары(шаг):
    """Пары чисел, на которых действие определено во всех четырёх."""
    вон = []
    for i in range(12):
        b = 2 + (шаг + i) % 9
        a = b * (2 + (шаг * 2 + i) % 8)
        вон.append((a, b))
    return вон


def именование(шаг):
    """Действие, названное именем: номинализация и имя результата."""
    вон = []
    for язык, действия in ДЕЙСТВИЯ.items():
        глагол, вопрос_н, связки, вопросы_р = РЕЧЬ[язык]
        for знак, шаб_н, шаб_р, род in действия:
            for a, b in _пары(шаг):
                c = {"+": a + b, "-": a - b, "*": a * b,
                     "/": a // b}[знак]
                фраза_н = шаб_н.format(a=a, b=b)
                фраза_р = шаб_р.format(a=a, b=b)
                утв_н = f"{фраза_н} {глагол} {c}."
                утв_р = f"{фраза_р} {связки[род]} {c}."
                вон.append(утв_н)
                вон.append(утв_р)
                вон.append(f"{вопрос_н.format(фраза=фраза_н)} {утв_н}")
                вон.append(
                    f"{вопросы_р[род].format(фраза=фраза_р)} {утв_р}")
    return вон


def связкой_будет(шаг):
    """Русская связка «будет» — и числа, СКАЗАННЫЕ СЛОВАМИ.

    «сорок два минус пять будет» немело в пробе, потому что корпус
    писал русскую арифметику цифрами и связкой «равно». Связка «будет»
    есть вторая связка языка, а числительное словами — вторая
    поверхность числа; ни одна из двух не выводится из другой.
    """
    табл = numerals.таблица("ru")
    знаки = (("+", "плюс"), ("-", "минус"))
    вон = []
    for i in range(14):
        a = 21 + (шаг * 5 + i * 3) % 78
        b = 2 + (шаг + i) % 9
        for знак, слово in знаки:
            c = a + b if знак == "+" else a - b
            имена = [numerals.назвать(x, табл) for x in (a, b, c)]
            if any(и is None for и in имена):
                continue
            са, сб, сц = имена
            вон.append(f"{са} {слово} {сб} будет {сц}.")
            вон.append(f"сколько будет {са} {слово} {сб}? "
                       f"{са} {слово} {сб} будет {сц}.")
    return вон


ГРУППЫ = (именование, связкой_будет)


def pass_groups(шаг):
    return [сделать(шаг) for сделать in ГРУППЫ]


def main():
    emit_grouped("datasets/genesis_surfaces.txt", pass_groups)


if __name__ == "__main__":
    main()
