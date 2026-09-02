#!/usr/bin/env python3
"""GENESIS layer: THE LADDER OF INQUIRY IN PORTUGUESE AND DUTCH.

Twenty-nine languages can COUNT and DECLINE. Six can REASON. A pack
teaches an organism to count and to inflect; a LADDER teaches it to
DECIDE, and those are different things — which is why each of these
layers is not «one more language» but the carrying over of an ABILITY.
A language that never shows a DECIDED CASE teaches its words as labels.

THE LADDER IS THE ENGLISH-RUSSIAN ONE, UNCHANGED. Four rungs, and each
rung is a different act:

    ОПРЕДЕЛЕНИЕ  — what the notion IS, said in words and not shown,
                   and said TWICE: as a statement and as the answer to
                   its own question
    ИСПОЛНЕНИЕ   — a particular case DECIDED, with the ground beside
                   the verdict («não: 91 = 7 × 13»)
    КОНТРПРИМЕР  — a universal claim KILLED by one witness
    ОБОБЩЕНИЕ    — the law the cases were instances of

Six genera declare their four rungs as functions over the pass number;
the machinery is written once. Adding a genus costs a declaration, and
adding a LANGUAGE costs a second string in every declaration.

ЯЗЫК ЕСТЬ ЧАСТЬ ФАКТА, А НЕ ЕГО ОДЕЖДА:

  · ПОРТУГАЛЬСКОЕ «não» НЕСЁТ ТИЛЬДУ. Без неё это другое слово («nao»
    не значит ничего), и корпус, написавший его без знака, выучит
    несуществующее слово с полной судимостью — как выучил бы «пять»
    вместо «пять»;
  · НИДЕРЛАНДСКИЙ ВОПРОС СТАВИТ ГЛАГОЛ ПЕРВЫМ: «is 128 deelbaar door
    8?» — не «128 is deelbaar door 8?». В португальском на том же
    месте порядок слов не меняется вовсе, и вопрос несёт только знак:
    «128 é divisível por 8?». Два языка, две разные рамки одного
    вопроса, и обе показаны на одних числах;
  · СОСТАВНОЕ ЧИСЛИТЕЛЬНОЕ ПОРТУГАЛЬСКОГО ИДЁТ СО СВЯЗКОЙ «e»
    («noventa e nove»), и пакет объявляет её полем `numeral_connectors`.
    Здесь такого случая не возникает: числа этого мира пишутся ЦИФРАМИ
    (см. ниже), и связке негде прозвучать. Правило названо, чтобы оно
    не было нарушено молча, если мир когда-нибудь заговорит словами.

ЧИСЛА ПИШУТСЯ ЦИФРАМИ, КАК ВО ВСЕХ ЧЕТЫРЁХ БЛИЗНЕЦАХ ЭТОЙ ЛЕСТНИЦЫ
(английском, русском, немецком, французском). Ни одного португальского
или нидерландского числительного здесь не выдумано: цифра стоит там,
где слово было бы естественно, и потому показ сравним с близнецами
слово в слово. Таблицы `tools/langpacks/pt.json` и `nl.json` прочитаны
ради проверки, что ни одно числительное не просочилось, а не ради
заимствования.

КОПУЛА ЭТИХ ДВУХ ЯЗЫКОВ ОБЪЯВЛЕНА ЗНАКОМ РАВЕНСТВА, и это надо знать,
берясь за них. `pt.json` объявляет «é» знаком «=», `nl.json` — «is»:
арифметический суд корпуса читает ОБА как равенство, потому что так
сказали сами пакеты. Оттого почти каждая связочная фраза этих языков
приходит к нему с признаком равенства на борту. Спасают её два
объявленных закона суда — «равенство без единой операции не утверждает
арифметики» и «цепь равенств читается только в чистой записи», — и
спасают ПОЛНОСТЬЮ: замер по всему слою даёт ноль ложных. Но закон этот
не наш, а чужого дома, и потому проверен числом, а не доверием.

ЯДРО ДОСЛОВНЫХ ПОВТОРОВ. Первые три случая каждой ступени берут семя
БЕЗ прохода и потому одинаковы во всех пяти проходах слово в слово;
остальные ходят числами. Форма чеканится повторностью — это замер, а не
мнение.

ОБЕ ВЕТВИ ВЕРДИКТА ОБЯЗАНЫ ЗВУЧАТЬ, И ЭТО ПРОВЕРЕНО ЧИСЛОМ. Слой, у
которого «sim» не сказано ни разу, зелен у всякого суда и молчит о
половине рода: он не лжёт, он не показывает. Ряды простоты и делимости
подобраны так, чтобы обе ветви покупались повторностью, и охват ветвей
меряется стендом.

EVERY GROUND IS COMPUTED HERE AND RE-COMPUTED BY THE COURT.
`courts/inquiry_pt_nl_court.py` factorises again, divides again, sums
the odd series again, and for a counterexample checks the WORK — that
the named witness really satisfies the premise and really breaks the
conclusion. A counterexample that does not refute is the most
convincing lie a corpus can carry, and its form is always correct.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layer import emit_grouped  # noqa: E402
import universals  # noqa: E402
import paraphrase  # noqa: E402

ЦЕЛЬ = "datasets/genesis_inquiry_pt_nl.txt"

# ЯДРО ДОСЛОВНЫХ ПОВТОРОВ: столько первых случаев каждой ступени стоят
# во ВСЕХ проходах слово в слово.
ЯДРО = 3
ИСПОЛНЕНИЙ = 12
КОНТРПРИМЕРОВ = 6
ОБОБЩЕНИЙ = 8


def семя(шаг, i):
    """Семя случая. Первые ЯДРО не знают прохода — оттого и дословны."""
    return i if i < ЯДРО else шаг * 13 + i


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

ВОПР_ПРОСТОТА = ["o que é um número primo?", "wat is een priemgetal?"]
ОПР_ПРОСТОТА = [
    "um número primo é um número inteiro maior que 1 cujos únicos "
    "divisores são 1 e ele mesmo.",
    "een priemgetal is een geheel getal groter dan 1 waarvan de enige "
    "delers 1 en het getal zelf zijn.",
]


def исп_простота(шаг):
    """ОБЕ ВЕТВИ ВЕРДИКТА ЗВУЧАТ: шаг взаимно прост с зачином ряда."""
    вон = []
    for i in range(ИСПОЛНЕНИЙ):
        n = 41 + семя(шаг, i) * 3
        if простое(n):
            вон.append(f"{n} é um número primo? sim: os divisores de "
                       f"{n} são 1 e {n}.")
            вон.append(f"is {n} een priemgetal? ja: de delers van {n} "
                       f"zijn 1 en {n}.")
        else:
            д = наименьший_делитель(n)
            вон.append(f"{n} é um número primo? não: {n} = {д} × "
                       f"{n // д}.")
            вон.append(f"is {n} een priemgetal? nee: {n} = {д} × "
                       f"{n // д}.")
    return paraphrase.перефразы(вон, ЯЗЫКИ_МИРА, ("prime", "divisible"))


# A UNIVERSAL IS ASKED BY ITS OWN «IS IT TRUE THAT» (tools/universals.py):
# the question of every counterexample and generalization is derived from
# its statement by the one law of the house, in both languages of the world.
ЯЗЫКИ_МИРА = ('pt', 'nl')


def контр_простота(шаг):
    вон = []
    for i in range(КОНТРПРИМЕРОВ):
        n = 9 + семя(шаг, i) * 2
        while простое(n):
            n += 2
        д = наименьший_делитель(n)
        вон.append(f"todos os números ímpares são primos é falso: {n} "
                   f"é ímpar e {n} = {д} × {n // д}.")
        вон.append(f"alle oneven getallen zijn priemgetallen is "
                   f"onwaar: {n} is oneven en {n} = {д} × {n // д}.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


def общ_простота(шаг):
    вон = []
    for i in range(ОБОБЩЕНИЙ):
        n = 84 + семя(шаг, i)
        ряд = " × ".join(str(x) for x in разложение(n))
        вон.append(f"todo número inteiro maior que 1 é um produto de "
                   f"números primos: {n} = {ряд}.")
        вон.append(f"elk geheel getal groter dan 1 is een product van "
                   f"priemgetallen: {n} = {ряд}.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


# ----------------------------------------------------------- ДЕЛИМОСТЬ

ВОПР_ДЕЛИМОСТЬ = ["o que significa divisível?", "wat betekent deelbaar?"]
ОПР_ДЕЛИМОСТЬ = [
    "um número é divisível por outro quando o resto é 0.",
    "een getal is deelbaar door een ander getal wanneer de rest 0 is.",
]


def исп_делимость(шаг):
    """ДЕЛИМОСТЬ СТРОИТСЯ ОТ ОТВЕТА, А НЕ ВЫПАДАЕТ ПО УДАЧЕ.

    Делитель и частное выбраны первыми, делимое собрано из них — и
    половина случаев делится по построению. Остаток во второй половине
    строго меньше делителя, иначе он не остаток.
    """
    вон = []
    for i in range(ИСПОЛНЕНИЙ):
        с = семя(шаг, i)
        b = 3 + с % 8
        a = b * (7 + с % 13) + (0 if с % 2 == 0 else 1 + с % (b - 1))
        q, r = divmod(a, b)
        if r == 0:
            вон.append(f"{a} é divisível por {b}? sim: {a} = {b} × "
                       f"{q}, resto 0.")
            вон.append(f"is {a} deelbaar door {b}? ja: {a} = {b} × "
                       f"{q}, rest 0.")
            # ПОВЕСТВОВАНИЕ С ПОЛЯРНОСТЬЮ — учитель формы для органа
            # обращения того же языка (holon: пара «вопрос ↔ повествование»
            # одного предиката покупает закон инверсии).
            вон.append(f"{a} é divisível por {b}: {a} = {b} × {q}, resto 0.")
            вон.append(f"{a} is deelbaar door {b}: {a} = {b} × {q}, rest 0.")
        else:
            вон.append(f"{a} é divisível por {b}? não: {a} = {b} × "
                       f"{q} + {r}, resto {r}.")
            вон.append(f"is {a} deelbaar door {b}? nee: {a} = {b} × "
                       f"{q} + {r}, rest {r}.")
            вон.append(f"{a} não é divisível por {b}: {a} = {b} × {q} + {r}, "
                       f"resto {r}.")
            вон.append(f"{a} is niet deelbaar door {b}: {a} = {b} × {q} + "
                       f"{r}, rest {r}.")
    return paraphrase.перефразы(вон, ЯЗЫКИ_МИРА, ("prime", "divisible"))


def контр_делимость(шаг):
    вон = []
    for i in range(КОНТРПРИМЕРОВ):
        n = 6 + семя(шаг, i) * 2
        while n % 4 == 0:
            n += 2
        q, r = divmod(n, 4)
        вон.append(f"todo número par é divisível por 4 é falso: {n} é "
                   f"par e {n} = 4 × {q} + {r}.")
        вон.append(f"elk even getal is deelbaar door 4 is onwaar: {n} "
                   f"is even en {n} = 4 × {q} + {r}.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


def общ_делимость(шаг):
    вон = []
    for i in range(ОБОБЩЕНИЙ):
        n = 3 * (37 + семя(шаг, i))
        с = сумма_цифр(n)
        вон.append(f"um número é divisível por 3 quando a soma dos "
                   f"seus algarismos é divisível por 3: a soma dos "
                   f"algarismos de {n} é {с}, e {с} = 3 × {с // 3}.")
        вон.append(f"een getal is deelbaar door 3 wanneer zijn "
                   f"cijfersom deelbaar is door 3: de cijfersom van "
                   f"{n} is {с}, en {с} = 3 × {с // 3}.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


# ------------------------------------------------------ СУММА НЕЧЁТНЫХ

ВОПР_НЕЧЁТНЫЕ = ["o que é um número ímpar?", "wat is een oneven getal?"]
ОПР_НЕЧЁТНЫЕ = [
    "os números ímpares começam por 1, 3, 5, 7, e cada um é 2 maior "
    "que o anterior.",
    "de oneven getallen beginnen met 1, 3, 5, 7, en elk is 2 groter "
    "dan het vorige.",
]


def исп_нечётные(шаг):
    вон = []
    for i in range(ИСПОЛНЕНИЙ):
        k = 2 + семя(шаг, i) % 11
        ряд = " + ".join(str(2 * j + 1) for j in range(k))
        вон.append(f"qual é a soma dos {k} primeiros números ímpares? "
                   f"{ряд} = {k * k}.")
        вон.append(f"wat is de som van de eerste {k} oneven getallen? "
                   f"{ряд} = {k * k}.")
    return вон


def контр_нечётные(шаг):
    вон = []
    for i in range(КОНТРПРИМЕРОВ):
        k = 3 + семя(шаг, i) % 9
        вон.append(f"a soma dos k primeiros números ímpares é 2 × k é "
                   f"falso: para k = {k} a soma é {k * k}, e 2 × {k} = "
                   f"{2 * k}.")
        вон.append(f"de som van de eerste k oneven getallen is 2 × k "
                   f"is onwaar: bij k = {k} is de som {k * k}, en "
                   f"2 × {k} = {2 * k}.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


def общ_нечётные(шаг):
    вон = []
    for i in range(ОБОБЩЕНИЙ):
        k = 1 + семя(шаг, i) % 12
        вон.append(f"a soma dos k primeiros números ímpares é k × k: "
                   f"para k = {k} isso é {k} × {k} = {k * k}.")
        вон.append(f"de som van de eerste k oneven getallen is k × k: "
                   f"bij k = {k} is het {k} × {k} = {k * k}.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


# ------------------------------------------------------ УСЛОВНЫЙ ВЫВОД

ВОПР_УСЛОВНОЕ = ["o que é uma afirmação condicional?",
                 "wat is een voorwaardelijke bewering?"]
ОПР_УСЛОВНОЕ = [
    "uma afirmação condicional vale quando a conclusão vale em todos "
    "os casos em que a premissa vale.",
    "een voorwaardelijke bewering geldt wanneer de gevolgtrekking "
    "geldt in elk geval waarin de aanname geldt.",
]


def исп_условное(шаг):
    вон = []
    for i in range(ИСПОЛНЕНИЙ):
        с = семя(шаг, i)
        m = 1 + с % 9
        e = 4 + (с % 8) * 2
        s = e + m
        да = m % 2 == 0
        вон.append(f"se n é par, n + {m} é par? "
                   f"{'sim' if да else 'não'}: {e} é par, e {e} + {m} "
                   f"= {s}, que é "
                   f"{'par' if s % 2 == 0 else 'ímpar'}.")
        вон.append(f"als n even is, is n + {m} even? "
                   f"{'ja' if да else 'nee'}: {e} is even, en {e} + "
                   f"{m} = {s}, wat "
                   f"{'even' if s % 2 == 0 else 'oneven'} is.")
    return вон


def контр_условное(шаг):
    вон = []
    for i in range(КОНТРПРИМЕРОВ):
        с = семя(шаг, i)
        m = 1 + (с % 5) * 2
        e = 6 + (с % 7) * 2
        s = e + m
        вон.append(f"se n é par então n + {m} é par é falso: {e} é "
                   f"par, e {e} + {m} = {s}, que é ímpar.")
        вон.append(f"als n even is, dan is n + {m} even is onwaar: "
                   f"{e} is even, en {e} + {m} = {s}, wat oneven is.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


def общ_условное(шаг):
    вон = []
    for i in range(ОБОБЩЕНИЙ):
        с = семя(шаг, i)
        m = 2 + (с % 6) * 2
        e = 8 + (с % 5) * 2
        вон.append(f"se n é par então n + m é par exatamente quando m "
                   f"é par: {m} é par e {e} + {m} = {e + m}, que é "
                   f"par.")
        вон.append(f"als n even is, dan is n + m even precies wanneer "
                   f"m even is: {m} is even en {e} + {m} = {e + m}, "
                   f"wat even is.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


# ------------------------------------------------------- ИНЪЕКТИВНОСТЬ

ВОПР_ИНЪЕКЦИЯ = ["o que significa que uma função é injetiva?",
                 "wat betekent het dat een functie injectief is?"]
ОПР_ИНЪЕКЦИЯ = [
    "uma função é injetiva quando entradas diferentes dão saídas "
    "diferentes.",
    "een functie is injectief wanneer verschillende invoeren "
    "verschillende uitvoeren geven.",
]


def исп_инъекция(шаг):
    вон = []
    for i in range(ИСПОЛНЕНИЙ):
        k = семя(шаг, i) % 6
        a, b, c = 1 * k, 2 * k, 3 * k
        да = k != 0
        разн_pt = "todas diferentes" if да else "nem todas diferentes"
        разн_nl = "alle verschillend" if да else "niet alle verschillend"
        вон.append(f"f(x) = x × {k} é injetiva em 1, 2, 3? "
                   f"{'sim' if да else 'não'}: ela dá {a}, {b}, "
                   f"{c}, {разн_pt}.")
        вон.append(f"is f(x) = x × {k} injectief op 1, 2, 3? "
                   f"{'ja' if да else 'nee'}: zij geeft {a}, {b}, "
                   f"{c}, {разн_nl}.")
    return вон


def контр_инъекция(шаг):
    вон = []
    for i in range(КОНТРПРИМЕРОВ):
        с = семя(шаг, i)
        a, b = 1 + с % 5, 6 + с % 5
        вон.append(f"toda função é injetiva é falso: f(x) = x × 0 "
                   f"leva {a} e {b} ambos a 0.")
        вон.append(f"elke functie is injectief is onwaar: "
                   f"f(x) = x × 0 stuurt {a} en {b} beide naar 0.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


def общ_инъекция(шаг):
    вон = []
    for i in range(ОБОБЩЕНИЙ):
        k = 1 + семя(шаг, i) % 7
        вон.append(f"f(x) = x × k é injetiva exatamente quando k não é "
                   f"0: para k = {k} as entradas 1 e 2 dão {k} e "
                   f"{2 * k}.")
        вон.append(f"f(x) = x × k is injectief precies wanneer k niet "
                   f"0 is: bij k = {k} geven de invoeren 1 en 2 de "
                   f"waarden {k} en {2 * k}.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


# ------------------------------------------------------------- КВАДРАТ

ВОПР_КВАДРАТ = ["o que é o quadrado de um número?",
                "wat is het kwadraat van een getal?"]
ОПР_КВАДРАТ = [
    "o quadrado de um número é o número multiplicado por si mesmo.",
    "het kwadraat van een getal is het getal met zichzelf "
    "vermenigvuldigd.",
]


def исп_квадрат(шаг):
    вон = []
    for i in range(ИСПОЛНЕНИЙ):
        n = 2 + семя(шаг, i) % 24
        вон.append(f"qual é o quadrado de {n}? {n} × {n} = {n * n}.")
        вон.append(f"wat is het kwadraat van {n}? {n} × {n} = "
                   f"{n * n}.")
    return вон


def контр_квадрат(шаг):
    вон = []
    for i in range(КОНТРПРИМЕРОВ):
        n = 3 + (семя(шаг, i) % 9) * 2
        вон.append(f"todo quadrado é par é falso: {n} é ímpar e "
                   f"{n} × {n} = {n * n}, que é ímpar.")
        вон.append(f"elk kwadraat is even is onwaar: {n} is oneven en "
                   f"{n} × {n} = {n * n}, wat oneven is.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


def общ_квадрат(шаг):
    вон = []
    for i in range(ОБОБЩЕНИЙ):
        n = 2 + семя(шаг, i) % 15
        чёт = n % 2 == 0
        порт = "par" if чёт else "ímpar"
        нид = "even" if чёт else "oneven"
        вон.append(f"o quadrado de um número {порт} é {порт}: "
                   f"{n} × {n} = {n * n}.")
        вон.append(f"het kwadraat van een {нид} getal is {нид}: "
                   f"{n} × {n} = {n * n}.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


# ---------------------------------------------------------------- РОДЫ

# РОД ОБЪЯВЛЯЕТ ЧЕТЫРЕ СТУПЕНИ И НИЧЕГО БОЛЬШЕ. Механизм лестницы один
# на все роды и на оба языка: прибавить род — значит объявить четвёрку,
# прибавить ЯЗЫК — значит дописать вторую строку в каждое объявление.
РОДЫ = (
    ("primality", ВОПР_ПРОСТОТА, ОПР_ПРОСТОТА, исп_простота,
     контр_простота, общ_простота),
    ("divisibility", ВОПР_ДЕЛИМОСТЬ, ОПР_ДЕЛИМОСТЬ, исп_делимость,
     контр_делимость, общ_делимость),
    ("odd-sum", ВОПР_НЕЧЁТНЫЕ, ОПР_НЕЧЁТНЫЕ, исп_нечётные,
     контр_нечётные, общ_нечётные),
    ("conditional", ВОПР_УСЛОВНОЕ, ОПР_УСЛОВНОЕ, исп_условное,
     контр_условное, общ_условное),
    ("injectivity", ВОПР_ИНЪЕКЦИЯ, ОПР_ИНЪЕКЦИЯ, исп_инъекция,
     контр_инъекция, общ_инъекция),
    ("square", ВОПР_КВАДРАТ, ОПР_КВАДРАТ, исп_квадрат, контр_квадрат,
     общ_квадрат),
)


def ступень_определения(вопр, опр):
    """Определение сказано УТВЕРЖДЕНИЕМ и сказано ОТВЕТОМ НА ВОПРОС.

    Знание, у которого есть лишь повествовательная поверхность, НЕ
    ОТВЕЧАЕТ — оно только сообщает. Ступень эта прохода не знает вовсе
    и потому дословна во всех пяти: ядро повторов начинается с неё.
    """
    return list(опр) + [f"{в} {о}" for в, о in zip(вопр, опр)]


def pass_groups(шаг):
    """Одна группа на РОД: ступени рода не перемешиваются с чужими."""
    вон = []
    for _имя, вопр, опр, исп, контр, общ in РОДЫ:
        вон.append(ступень_определения(вопр, опр)
                   + исп(шаг) + контр(шаг) + общ(шаг))
    return вон


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
