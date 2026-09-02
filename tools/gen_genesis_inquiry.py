#!/usr/bin/env python3
"""GENESIS layer: THE LADDER OF INQUIRY — how a question is answered.

A dialogue probe on the trained organism came back with twelve mute
mouths, and every one of them was a QUESTION: «is 91 a prime number?»,
«give a counterexample: all odd numbers are prime», «what is the sum of
the first 5 odd numbers?». The corpus already held the facts — primes,
factorisations, counterexamples — and held them as STATEMENTS. Nowhere
did it hold the ACT of deciding a case that had been ASKED.

THE LADDER. A researcher does not know a subject by its facts; a
researcher knows it by four rungs, and each rung is a different act:

    ОПРЕДЕЛЕНИЕ  — what the notion IS, said in words and not shown
    ИСПОЛНЕНИЕ   — a particular case DECIDED, with the ground beside
                   the verdict («no: 91 = 7 × 13»)
    КОНТРПРИМЕР  — a universal claim KILLED by one witness; the cheapest
                   proof there is, and the one a confirming corpus never
                   teaches
    ОБОБЩЕНИЕ    — the law that the cases were instances of

A corpus that shows only the second rung teaches arithmetic. A corpus
that shows all four teaches INQUIRY, and inquiry is what the owner asked
for: «выращиваем универсала-исследователя-математика».

ONE MECHANISM, SIX GENERA. The ladder is not written six times. It is a
form, and each genus DECLARES its four rungs as functions over the pass
number; the layer walks the same ladder for primality, divisibility, the
sum of odd numbers, the conditional, injectivity and the square. Adding
a genus costs a declaration and no machinery — which is the test that
the form is a form and not a template.

EVERY GROUND IS COMPUTED HERE AND RE-COMPUTED BY THE COURT. The verdict
«no: 91 = 7 × 13» is not written; it is factorised, and
`courts/inquiry_court.py` factorises again rather than believing the
line. A counterexample is not trusted either: the court checks that the
witness REALLY refutes the claim, because a counterexample that does not
refute is the most convincing lie a corpus can carry.

BOTH TONGUES, ONE FACT. English and Russian say the same thing and are
judged by the same computation, so a defect in one surface cannot hide
behind the other.
"""

import pathlib
import sys
from math import gcd  # noqa: F401  (родня для будущих родов)

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layer import emit_grouped  # noqa: E402


# ---------------------------------------------------------------- счёт

def делители(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def простое(n):
    return n > 1 and делители(n) == [1, n]


def наименьший_делитель(n):
    for d in range(2, n + 1):
        if n % d == 0:
            return d
    return n


def разложение(n):
    вон, о = [], n
    while о > 1:
        д = наименьший_делитель(о)
        вон.append(д)
        о //= д
    return вон


def сумма_цифр(n):
    return sum(int(ц) for ц in str(n))


# ------------------------------------------------------------ ПРОСТОТА

ВОПР_ПРОСТОТА = ["what is a prime number?", "что такое простое число?"]
ОПР_ПРОСТОТА = [
    "a prime number is a whole number above 1 whose only divisors "
    "are 1 and itself.",
    "простое число — это целое число больше 1, у которого делители "
    "только 1 и оно само.",
]


def исп_простота(шаг):
    вон = []
    for i in range(14):
        n = 40 + шаг * 7 + i * 5
        if простое(n):
            вон.append(f"is {n} a prime number? yes: the divisors of "
                       f"{n} are 1 and {n}.")
            вон.append(f"является ли {n} простым числом? да: делители "
                       f"{n} — 1 и {n}.")
        else:
            д = наименьший_делитель(n)
            вон.append(f"is {n} a prime number? no: {n} = {д} × "
                       f"{n // д}.")
            вон.append(f"является ли {n} простым числом? нет: {n} = "
                       f"{д} × {n // д}.")
    return вон


def контр_простота(шаг):
    вон = []
    for i in range(6):
        n = 9 + (шаг + i) * 2
        while простое(n):
            n += 2
        д = наименьший_делитель(n)
        вон.append(f"all odd numbers are prime is false: {n} is odd "
                   f"and {n} = {д} × {n // д}.")
        вон.append(f"все нечётные числа просты — ложь: {n} нечётно и "
                   f"{n} = {д} × {n // д}.")
    return вон


def общ_простота(шаг):
    вон = []
    for i in range(8):
        n = 84 + шаг * 3 + i
        ряд = " × ".join(str(x) for x in разложение(n))
        вон.append(f"every whole number above 1 is a product of "
                   f"primes: {n} = {ряд}.")
        вон.append(f"всякое целое больше 1 есть произведение простых: "
                   f"{n} = {ряд}.")
    return вон


# ----------------------------------------------------------- ДЕЛИМОСТЬ

ВОПР_ДЕЛИМОСТЬ = ["what does divisible mean?", "что значит «делится»?"]
ОПР_ДЕЛИМОСТЬ = [
    "a number is divisible by another when the remainder is 0.",
    "число делится на другое, когда остаток равен нулю.",
]


def исп_делимость(шаг):
    вон = []
    for i in range(14):
        a = 100 + шаг * 11 + i * 9
        b = 3 + (шаг + i) % 8
        q, r = divmod(a, b)
        if r == 0:
            вон.append(f"is {a} divisible by {b}? yes: {a} = {b} × "
                       f"{q}, remainder 0.")
            вон.append(f"делится ли {a} на {b}? да: {a} = {b} × {q}, "
                       f"остаток 0.")
        else:
            вон.append(f"is {a} divisible by {b}? no: {a} = {b} × "
                       f"{q} + {r}, remainder {r}.")
            вон.append(f"делится ли {a} на {b}? нет: {a} = {b} × {q} "
                       f"+ {r}, остаток {r}.")
    return вон


def контр_делимость(шаг):
    вон = []
    for i in range(6):
        n = 6 + (шаг + i) * 2
        while n % 4 == 0:
            n += 2
        q, r = divmod(n, 4)
        вон.append(f"every even number is divisible by 4 is false: "
                   f"{n} is even and {n} = 4 × {q} + {r}.")
        вон.append(f"всякое чётное делится на 4 — ложь: {n} чётно и "
                   f"{n} = 4 × {q} + {r}.")
    return вон


def общ_делимость(шаг):
    вон = []
    for i in range(8):
        n = 3 * (37 + шаг * 5 + i)
        с = сумма_цифр(n)
        вон.append(f"a number is divisible by 3 when its digit sum "
                   f"is: {n} has digit sum {с}, and {с} = 3 × "
                   f"{с // 3}.")
        вон.append(f"число делится на 3, когда делится сумма его цифр: "
                   f"у {n} сумма цифр {с}, и {с} = 3 × {с // 3}.")
    return вон


# ----------------------------------------------------- СУММА НЕЧЁТНЫХ

ВОПР_НЕЧЁТНЫЕ = ["what is an odd number?", "что такое нечётное число?"]
ОПР_НЕЧЁТНЫЕ = [
    "the odd numbers begin 1, 3, 5, 7 and each is 2 more than the "
    "one before.",
    "нечётные числа начинаются 1, 3, 5, 7, и каждое на 2 больше "
    "предыдущего.",
]


def исп_нечётные(шаг):
    вон = []
    for i in range(10):
        k = 2 + (шаг + i) % 11
        ряд = " + ".join(str(2 * j + 1) for j in range(k))
        вон.append(f"what is the sum of the first {k} odd numbers? "
                   f"{ряд} = {k * k}.")
        вон.append(f"чему равна сумма первых {k} нечётных чисел? "
                   f"{ряд} = {k * k}.")
    return вон


def контр_нечётные(шаг):
    вон = []
    for i in range(6):
        k = 3 + (шаг + i) % 9
        вон.append(f"the sum of the first k odd numbers is 2 × k is "
                   f"false: at k = {k} the sum is {k * k} and 2 × {k} "
                   f"= {2 * k}.")
        вон.append(f"сумма первых k нечётных равна 2 × k — ложь: при "
                   f"k = {k} сумма равна {k * k}, а 2 × {k} = "
                   f"{2 * k}.")
    return вон


def общ_нечётные(шаг):
    вон = []
    for i in range(8):
        k = 1 + (шаг * 2 + i) % 12
        вон.append(f"the sum of the first k odd numbers is k × k: at "
                   f"k = {k} it is {k} × {k} = {k * k}.")
        вон.append(f"сумма первых k нечётных равна k × k: при k = {k} "
                   f"это {k} × {k} = {k * k}.")
    return вон


# ------------------------------------------------------ УСЛОВНЫЙ ВЫВОД

ВОПР_УСЛОВНОЕ = ["what is a conditional?", "что такое условное утверждение?"]
ОПР_УСЛОВНОЕ = [
    "a conditional holds when the conclusion follows in every case "
    "where the premise holds.",
    "условное верно, когда следствие выполняется в каждом случае, где "
    "выполнена посылка.",
]


def исп_условное(шаг):
    вон = []
    for i in range(10):
        m = 1 + (шаг + i) % 9
        e = 4 + ((шаг + i) % 8) * 2
        s = e + m
        да = m % 2 == 0
        вон.append(f"if n is even, is n + {m} even? "
                   f"{'yes' if да else 'no'}: {e} is even and {e} + "
                   f"{m} = {s}, which is "
                   f"{'even' if s % 2 == 0 else 'odd'}.")
        вон.append(f"если n чётно, чётно ли n + {m}? "
                   f"{'да' if да else 'нет'}: {e} чётно, и {e} + {m} "
                   f"= {s}, что "
                   f"{'чётно' if s % 2 == 0 else 'нечётно'}.")
    return вон


def контр_условное(шаг):
    вон = []
    for i in range(6):
        m = 1 + ((шаг + i) % 5) * 2
        e = 6 + ((шаг + i) % 7) * 2
        s = e + m
        вон.append(f"if n is even then n + {m} is even is false: {e} "
                   f"is even and {e} + {m} = {s}, which is odd.")
        вон.append(f"если n чётно, то n + {m} чётно — ложь: {e} чётно, "
                   f"а {e} + {m} = {s}, что нечётно.")
    return вон


def общ_условное(шаг):
    вон = []
    for i in range(6):
        m = 2 + ((шаг + i) % 6) * 2
        e = 8 + ((шаг + i) % 5) * 2
        вон.append(f"if n is even then n + m is even exactly when m is "
                   f"even: {m} is even and {e} + {m} = {e + m}, which "
                   f"is even.")
        вон.append(f"если n чётно, то n + m чётно ровно тогда, когда m "
                   f"чётно: {m} чётно и {e} + {m} = {e + m}, что "
                   f"чётно.")
    return вон


# ------------------------------------------------------ ИНЪЕКТИВНОСТЬ

ВОПР_ИНЪЕКЦИЯ = ["what does it mean for a function to be injective?", "что значит, что функция инъективна?"]
ОПР_ИНЪЕКЦИЯ = [
    "a function is injective when different inputs give different "
    "outputs.",
    "функция инъективна, когда разные входы дают разные выходы.",
]


def исп_инъекция(шаг):
    вон = []
    for i in range(10):
        k = (шаг + i) % 6
        a, b, c = 1 * k, 2 * k, 3 * k
        да = k != 0
        вон.append(f"is f(x) = x × {k} injective on 1, 2, 3? "
                   f"{'yes' if да else 'no'}: it gives {a}, {b}, {c}, "
                   f"{'all different' if да else 'not all different'}.")
        вон.append(f"инъективна ли f(x) = x × {k} на 1, 2, 3? "
                   f"{'да' if да else 'нет'}: она даёт {a}, {b}, {c}, "
                   f"{'все разные' if да else 'не все разные'}.")
    return вон


def контр_инъекция(шаг):
    вон = []
    for i in range(6):
        a, b = 1 + (шаг + i) % 5, 6 + (шаг + i) % 5
        вон.append(f"every function is injective is false: f(x) = x × "
                   f"0 sends {a} and {b} both to 0.")
        вон.append(f"всякая функция инъективна — ложь: f(x) = x × 0 "
                   f"отправляет {a} и {b} в 0.")
    return вон


def общ_инъекция(шаг):
    вон = []
    for i in range(6):
        k = 1 + (шаг + i) % 7
        вон.append(f"f(x) = x × k is injective exactly when k is not "
                   f"0: at k = {k} the inputs 1 and 2 give {k} and "
                   f"{2 * k}.")
        вон.append(f"f(x) = x × k инъективна ровно тогда, когда k не "
                   f"0: при k = {k} входы 1 и 2 дают {k} и {2 * k}.")
    return вон


# ------------------------------------------------------------ КВАДРАТ

ВОПР_КВАДРАТ = ["what is the square of a number?", "что такое квадрат числа?"]
ОПР_КВАДРАТ = [
    "the square of a number is the number multiplied by itself.",
    "квадрат числа — это число, умноженное на само себя.",
]


def исп_квадрат(шаг):
    вон = []
    for i in range(12):
        n = 2 + (шаг * 3 + i) % 24
        вон.append(f"what is the square of {n}? {n} × {n} = {n * n}.")
        вон.append(f"чему равен квадрат {n}? {n} × {n} = {n * n}.")
    return вон


def контр_квадрат(шаг):
    вон = []
    for i in range(6):
        n = 3 + ((шаг + i) % 9) * 2
        вон.append(f"every square is even is false: {n} is odd and "
                   f"{n} × {n} = {n * n}, which is odd.")
        вон.append(f"всякий квадрат чётен — ложь: {n} нечётно и {n} × "
                   f"{n} = {n * n}, что нечётно.")
    return вон


def общ_квадрат(шаг):
    вон = []
    for i in range(8):
        n = 2 + (шаг + i) % 15
        чёт = "even" if n % 2 == 0 else "odd"
        ру = "чётного" if n % 2 == 0 else "нечётного"
        рук = "чётен" if n % 2 == 0 else "нечётен"
        вон.append(f"the square of an {чёт} number is {чёт}: "
                   f"{n} × {n} = {n * n}.")
        вон.append(f"квадрат {ру} числа {рук}: {n} × {n} = {n * n}.")
    return вон



# --------------------------------------------- ПОВЕСТВОВАНИЕ ИСПОЛНЕНИЯ
#
# ОБРАЩЕНИЮ НЕГДЕ КУПИТЬ ПРЕДИКАТ, ЕСЛИ ВЕРДИКТ ЖИВЁТ ТОЛЬКО В ВОПРОСЕ.
#
# Штурм архитектуры замерил организм на вопросах, которых ему не
# показывали. РЕЛЯЦИОННЫЕ роды отвечали («how many minutes are in 2
# hours?» → 120, четыре из пяти): у них есть повествовательные
# утверждения, и дорога берёт роли по словам. РАМОЧНЫЕ роды — простота,
# делимость, инъективность — дали НОЛЬ из пяти: здесь вопрос был
# ЕДИНСТВЕННОЙ поверхностью. Проверено по своду: строк «is not a prime
# number» без знака вопроса — 0 при 1160 вопросных.
#
# Организм никогда не видел, как утверждение о простоте выглядит БЕЗ
# вопроса, — и потому не мог купить предикат «простое» как вещь,
# отдельную от вопросной рамки. Повествование даёт ему эту вещь.
#
# ТРИ УСЛОВИЯ, ВСЕ ОБЯЗАТЕЛЬНЫ. ПАРАЛЛЕЛЬНО вопросу, а не вместо: на
# тех же числах у вердикта две поверхности. ОТРИЦАНИЕ ЯВНЫМ СЛОВОМ —
# «not», «не» — это поверхность ПОЛЯРНОСТИ предиката, по которой рынок
# покупает исполнителя. ОСНОВАНИЕ РЯДОМ, как всегда: суд пересчитывает
# его, а не сверяется с вердиктом.


def повеств_простота(шаг):
    вон = []
    for i in range(14):
        n = 40 + шаг * 7 + i * 5
        if простое(n):
            вон.append(f"{n} is a prime number: the divisors of {n} are "
                       f"1 and {n}.")
            вон.append(f"{n} — простое число: делители {n} — 1 и {n}.")
        else:
            д = наименьший_делитель(n)
            вон.append(f"{n} is not a prime number: {n} = {д} × {n // д}.")
            вон.append(f"{n} — не простое число: {n} = {д} × {n // д}.")
    return вон


def повеств_делимость(шаг):
    вон = []
    for i in range(14):
        a = 100 + шаг * 11 + i * 9
        b = 3 + (шаг + i) % 8
        q, r = divmod(a, b)
        if r == 0:
            вон.append(f"{a} is divisible by {b}: {a} = {b} × {q}, "
                       f"remainder 0.")
            вон.append(f"{a} делится на {b}: {a} = {b} × {q}, остаток 0.")
        else:
            вон.append(f"{a} is not divisible by {b}: {a} = {b} × {q} + "
                       f"{r}, remainder {r}.")
            вон.append(f"{a} не делится на {b}: {a} = {b} × {q} + {r}, "
                       f"остаток {r}.")
    return вон


def повеств_нечётные(шаг):
    вон = []
    for i in range(10):
        k = 2 + (шаг + i) % 11
        ряд = " + ".join(str(2 * j + 1) for j in range(k))
        вон.append(f"the sum of the first {k} odd numbers is {k * k}: "
                   f"{ряд} = {k * k}.")
        вон.append(f"сумма первых {k} нечётных чисел равна {k * k}: "
                   f"{ряд} = {k * k}.")
    return вон


def повеств_условное(шаг):
    вон = []
    for i in range(10):
        m = 1 + (шаг + i) % 9
        e = 4 + ((шаг + i) % 8) * 2
        s = e + m
        да = m % 2 == 0
        вон.append(f"if n is even, n + {m} {'is even' if да else 'is not even'}: "
                   f"{e} is even and {e} + {m} = {s}, which is "
                   f"{'even' if s % 2 == 0 else 'odd'}.")
        вон.append(f"если n чётно, то n + {m} {'чётно' if да else 'не чётно'}: "
                   f"{e} чётно, и {e} + {m} = {s}, что "
                   f"{'чётно' if s % 2 == 0 else 'нечётно'}.")
        # ФОРМА ЗАПЯТОЙ БЕЗ «ТО» — заказ органа обращения (holon, суд-13):
        # рынок покупает полярную пару по одному вставленному слову, а
        # обращение — клаузу после запятой; «то» и «then» учат иному
        # («exactly when») и остаются своей поверхностью.
        вон.append(f"если n чётно, n + {m} {'чётно' if да else 'не чётно'}: "
                   f"{e} чётно и {e} + {m} = {s}.")
    return вон


def повеств_инъекция(шаг):
    вон = []
    for i in range(10):
        k = (шаг + i) % 6
        a, b, c = 1 * k, 2 * k, 3 * k
        да = k != 0
        вон.append(f"f(x) = x × {k} {'is injective' if да else 'is not injective'} "
                   f"on 1, 2, 3: it gives {a}, {b}, {c}, "
                   f"{'all different' if да else 'not all different'}.")
        вон.append(f"f(x) = x × {k} {'инъективна' if да else 'не инъективна'} "
                   f"на 1, 2, 3: она даёт {a}, {b}, {c}, "
                   f"{'все разные' if да else 'не все разные'}.")
    return вон


def повеств_квадрат(шаг):
    вон = []
    for i in range(12):
        n = 2 + (шаг * 3 + i) % 24
        вон.append(f"the square of {n} is {n * n}: {n} × {n} = {n * n}.")
        вон.append(f"квадрат {n} равен {n * n}: {n} × {n} = {n * n}.")
    return вон


# --------------------------------------------------------------- РОДЫ

# РОД ОБЪЯВЛЯЕТ ЧЕТЫРЕ СТУПЕНИ И НИЧЕГО БОЛЬШЕ. Механизм лестницы
# ниже один на все роды: прибавить род — значит объявить четвёрку, а
# не написать новый обход. Это и есть проба, что форма есть форма.
РОДЫ = (
    ("primality", ВОПР_ПРОСТОТА, ОПР_ПРОСТОТА, исп_простота, повеств_простота,
     контр_простота, общ_простота),
    ("divisibility", ВОПР_ДЕЛИМОСТЬ, ОПР_ДЕЛИМОСТЬ, исп_делимость, повеств_делимость,
     контр_делимость, общ_делимость),
    ("odd-sum", ВОПР_НЕЧЁТНЫЕ, ОПР_НЕЧЁТНЫЕ, исп_нечётные, повеств_нечётные,
     контр_нечётные, общ_нечётные),
    ("conditional", ВОПР_УСЛОВНОЕ, ОПР_УСЛОВНОЕ, исп_условное, повеств_условное,
     контр_условное, общ_условное),
    ("injectivity", ВОПР_ИНЪЕКЦИЯ, ОПР_ИНЪЕКЦИЯ, исп_инъекция, повеств_инъекция,
     контр_инъекция, общ_инъекция),
    ("square", ВОПР_КВАДРАТ, ОПР_КВАДРАТ, исп_квадрат, повеств_квадрат, контр_квадрат,
     общ_квадрат),
)


# ОДИН ВОПРОС ЧЕЛОВЕКА ЕСТЬ ДВЕ РАМКИ РЫНКА. Рамка есть точная
# последовательность токенов со слотами, и РОДОВОЕ СЛОВО между вопросом
# и предметом («число», «уравнения», «the number») рвёт её надвое:
# «является ли 91 простым числом?» и «является ли ЧИСЛО 91 простым?» —
# один вопрос для читающего и две разные рамки для покупающего форму.
# Закон дан e9 на уравнениях; здесь он приложен ко всем вопросам мира.
РОДОВЫЕ = (
    ("is ", "is the number ", "a prime number"),
    ("является ли ", "является ли число ", "простым числом"),
    ("is ", "is the number ", "divisible by"),
    ("делится ли ", "делится ли число ", " на "),
    ("what is the square of ", "what is the square of the number ",
     None),
    ("чему равен квадрат ", "чему равен квадрат числа ", None),
)


def с_родовым(показы):
    """Второй вид тех же вопросов — с родовым словом перед предметом."""
    вон = []
    for показ in показы:
        вон.append(показ)
        for голый, полный, признак in РОДОВЫЕ:
            if not показ.startswith(голый):
                continue
            if признак is not None and признак not in показ:
                continue
            вон.append(полный + показ[len(голый):])
            break
    return вон


def ступень_определения(вопр, опр):
    """Определение сказано УТВЕРЖДЕНИЕМ и сказано ОТВЕТОМ НА ВОПРОС.

    Проба показала: организм, знавший «a prime number is …» как
    утверждение, немел на «what is a prime number?». Знание, у которого
    есть лишь повествовательная поверхность, не отвечает — оно только
    сообщает. Вопрос со своим ответом есть ВТОРАЯ ПОВЕРХНОСТЬ того же
    факта, и стоит она одной строки.
    """
    return list(опр) + [f"{в} {о}" for в, о in zip(вопр, опр)]


def pass_groups(шаг):
    """Одна группа на РОД: ступени рода не перемешиваются с чужими."""
    вон = []
    for _имя, вопр, опр, исп, повеств, контр, общ in РОДЫ:
        # ВОПРОС И ПОВЕСТВОВАНИЕ СТОЯТ В ОДНОЙ ГРУППЕ РОДА: у вердикта
        # две поверхности на одних числах, и рынок видит их рядом.
        вон.append(ступень_определения(вопр, опр)
                   + с_родовым(исп(шаг)) + повеств(шаг)
                   + контр(шаг) + общ(шаг))
    return вон


def main():
    emit_grouped("datasets/genesis_inquiry.txt", pass_groups)


if __name__ == "__main__":
    main()
