#!/usr/bin/env python3
"""ДОМ ВОПРОШАНИЯ (inquiry_pt_nl) — шесть ступеней определения на двух языках.

Мир `inquiry_pt_nl` стоял без объявленного рода: шесть родов лежали в кузнице кортежем
шестёрок, и указатель не мог назвать ни одной его строки.

ТЕЛО ВЗЯТО ОТ ЗАГОЛОВКА, А НЕ ОТ ИМПОРТОВ: таблица БУКВ у этой кузницы стои́т
ВЫШЕ `sys.path.insert`, и граница по импортам оставила бы дом без неё.

    ГРАНИЦА ПЕРЕЕЗДА, ВЗЯТАЯ ПО ОБЫЧАЮ, А НЕ ПО ФАЙЛУ, ОСТАВЛЯЕТ ПОЗАДИ ТО,
    ЧТО ЛЕЖАЛО НЕ ПО ОБЫЧАЮ.
"""

import pathlib
import sys

# БУКВА ПЕРЕМЕННОЙ ЕСТЬ ДЫРА, А НЕ СЛОВО (holon 03.09): универсалия,
# писавшая всегда «k», учила букву как слово рамки; буквы ходят поровну и
# согласованно внутри строки.
БУКВЫ = ("k", "n", "m")


sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layer import emit_grouped  # noqa: E402
import bilang  # noqa: E402 — язык берётся у строителя
import universals  # noqa: E402
import parity  # noqa: E402
import coprime  # noqa: E402
import paraphrase  # noqa: E402


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
    вон = bilang.Двое(ЯЗЫКИ_МИРА)
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
    return paraphrase.перефразы_меченые(вон.парами, ЯЗЫКИ_МИРА, ("prime", "divisible"))


# A UNIVERSAL IS ASKED BY ITS OWN «IS IT TRUE THAT» (tools/universals.py):
# the question of every counterexample and generalization is derived from
# its statement by the one law of the house, in both languages of the world.
ЯЗЫКИ_МИРА = ('pt', 'nl')


def контр_простота(шаг):
    вон = bilang.Двое(ЯЗЫКИ_МИРА)
    for i in range(КОНТРПРИМЕРОВ):
        n = 9 + семя(шаг, i) * 2
        while простое(n):
            n += 2
        д = наименьший_делитель(n)
        вон.append(f"todos os números ímpares são primos é falso: {n} "
                   f"é ímpar e {n} = {д} × {n // д}.")
        вон.append(f"alle oneven getallen zijn priemgetallen is "
                   f"onwaar: {n} is oneven en {n} = {д} × {n // д}.")
    return universals.с_вопросами_меченые(вон.парами, ЯЗЫКИ_МИРА)


def общ_простота(шаг):
    вон = bilang.Двое(ЯЗЫКИ_МИРА)
    for i in range(ОБОБЩЕНИЙ):
        n = 84 + семя(шаг, i)
        ряд = " × ".join(str(x) for x in разложение(n))
        вон.append(f"todo número inteiro maior que 1 é um produto de "
                   f"números primos: {n} = {ряд}.")
        вон.append(f"elk geheel getal groter dan 1 is een product van "
                   f"priemgetallen: {n} = {ряд}.")
    return universals.с_вопросами_меченые(вон.парами, ЯЗЫКИ_МИРА)


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
    вон = bilang.Двое(ЯЗЫКИ_МИРА)
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
    return paraphrase.перефразы_меченые(вон.парами, ЯЗЫКИ_МИРА, ("prime", "divisible"))


def контр_делимость(шаг):
    вон = bilang.Двое(ЯЗЫКИ_МИРА)
    for i in range(КОНТРПРИМЕРОВ):
        n = 6 + семя(шаг, i) * 2
        while n % 4 == 0:
            n += 2
        q, r = divmod(n, 4)
        вон.append(f"todo número par é divisível por 4 é falso: {n} é "
                   f"par e {n} = 4 × {q} + {r}.")
        вон.append(f"elk even getal is deelbaar door 4 is onwaar: {n} "
                   f"is even en {n} = 4 × {q} + {r}.")
    return universals.с_вопросами_меченые(вон.парами, ЯЗЫКИ_МИРА)


def общ_делимость(шаг):
    вон = bilang.Двое(ЯЗЫКИ_МИРА)
    for i in range(ОБОБЩЕНИЙ):
        n = 3 * (37 + семя(шаг, i))
        с = сумма_цифр(n)
        вон.append(f"um número é divisível por 3 quando a soma dos "
                   f"seus algarismos é divisível por 3: a soma dos "
                   f"algarismos de {n} é {с}, e {с} = 3 × {с // 3}.")
        вон.append(f"een getal is deelbaar door 3 wanneer zijn "
                   f"cijfersom deelbaar is door 3: de cijfersom van "
                   f"{n} is {с}, en {с} = 3 × {с // 3}.")
    return universals.с_вопросами_меченые(вон.парами, ЯЗЫКИ_МИРА)


# ------------------------------------------------------ СУММА НЕЧЁТНЫХ

ВОПР_НЕЧЁТНЫЕ = ["o que é um número ímpar?", "wat is een oneven getal?"]
ОПР_НЕЧЁТНЫЕ = [
    "os números ímpares começam por 1, 3, 5, 7, e cada um é 2 maior "
    "que o anterior.",
    "de oneven getallen beginnen met 1, 3, 5, 7, en elk is 2 groter "
    "dan het vorige.",
]


def исп_нечётные(шаг):
    вон = bilang.Двое(ЯЗЫКИ_МИРА)
    for i in range(ИСПОЛНЕНИЙ):
        k = 2 + семя(шаг, i) % 11
        б = БУКВЫ[(шаг + i) % len(БУКВЫ)]
        ряд = " + ".join(str(2 * j + 1) for j in range(k))
        вон.append(f"qual é a soma dos {k} primeiros números ímpares? "
                   f"{ряд} = {k * k}.")
        вон.append(f"wat is de som van de eerste {k} oneven getallen? "
                   f"{ряд} = {k * k}.")
    return вон.парами


def контр_нечётные(шаг):
    вон = bilang.Двое(ЯЗЫКИ_МИРА)
    for i in range(КОНТРПРИМЕРОВ):
        k = 3 + семя(шаг, i) % 9
        б = БУКВЫ[(шаг + i) % len(БУКВЫ)]
        вон.append(f"a soma dos {б} primeiros números ímpares é 2 × {б} é "
                   f"falso: para {б} = {k} a soma é {k * k}, e 2 × {k} = "
                   f"{2 * k}.")
        вон.append(f"de som van de eerste {б} oneven getallen is 2 × {б} "
                   f"is onwaar: bij {б} = {k} is de som {k * k}, en "
                   f"2 × {k} = {2 * k}.")
    return universals.с_вопросами_меченые(вон.парами, ЯЗЫКИ_МИРА)


def общ_нечётные(шаг):
    вон = bilang.Двое(ЯЗЫКИ_МИРА)
    for i in range(ОБОБЩЕНИЙ):
        k = 1 + семя(шаг, i) % 12
        б = БУКВЫ[(шаг + i) % len(БУКВЫ)]
        вон.append(f"a soma dos {б} primeiros números ímpares é {б} × {б}: "
                   f"para {б} = {k} isso é {k} × {k} = {k * k}.")
        вон.append(f"de som van de eerste {б} oneven getallen is {б} × {б}: "
                   f"bij {б} = {k} is het {k} × {k} = {k * k}.")
    return universals.с_вопросами_меченые(вон.парами, ЯЗЫКИ_МИРА)


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
    вон = bilang.Двое(ЯЗЫКИ_МИРА)
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
    return вон.парами


def контр_условное(шаг):
    вон = bilang.Двое(ЯЗЫКИ_МИРА)
    for i in range(КОНТРПРИМЕРОВ):
        с = семя(шаг, i)
        m = 1 + (с % 5) * 2
        e = 6 + (с % 7) * 2
        s = e + m
        вон.append(f"se n é par então n + {m} é par é falso: {e} é "
                   f"par, e {e} + {m} = {s}, que é ímpar.")
        вон.append(f"als n even is, dan is n + {m} even is onwaar: "
                   f"{e} is even, en {e} + {m} = {s}, wat oneven is.")
    return universals.с_вопросами_меченые(вон.парами, ЯЗЫКИ_МИРА)


def общ_условное(шаг):
    вон = bilang.Двое(ЯЗЫКИ_МИРА)
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
    return universals.с_вопросами_меченые(вон.парами, ЯЗЫКИ_МИРА)


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
    вон = bilang.Двое(ЯЗЫКИ_МИРА)
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
    return вон.парами


def контр_инъекция(шаг):
    вон = bilang.Двое(ЯЗЫКИ_МИРА)
    for i in range(КОНТРПРИМЕРОВ):
        с = семя(шаг, i)
        a, b = 1 + с % 5, 6 + с % 5
        вон.append(f"toda função é injetiva é falso: f(x) = x × 0 "
                   f"leva {a} e {b} ambos a 0.")
        вон.append(f"elke functie is injectief is onwaar: "
                   f"f(x) = x × 0 stuurt {a} en {b} beide naar 0.")
    return universals.с_вопросами_меченые(вон.парами, ЯЗЫКИ_МИРА)


def общ_инъекция(шаг):
    вон = bilang.Двое(ЯЗЫКИ_МИРА)
    for i in range(ОБОБЩЕНИЙ):
        k = 1 + семя(шаг, i) % 7
        б = БУКВЫ[(шаг + i) % len(БУКВЫ)]
        вон.append(f"f(x) = x × {б} é injetiva exatamente quando {б} não é "
                   f"0: para {б} = {k} as entradas 1 e 2 dão {k} e "
                   f"{2 * k}.")
        вон.append(f"f(x) = x × {б} is injectief precies wanneer {б} niet "
                   f"0 is: bij {б} = {k} geven de invoeren 1 en 2 de "
                   f"waarden {k} en {2 * k}.")
    return universals.с_вопросами_меченые(вон.парами, ЯЗЫКИ_МИРА)


# ------------------------------------------------------------- КВАДРАТ

ВОПР_КВАДРАТ = ["o que é o quadrado de um número?",
                "wat is het kwadraat van een getal?"]
ОПР_КВАДРАТ = [
    "o quadrado de um número é o número multiplicado por si mesmo.",
    "het kwadraat van een getal is het getal met zichzelf "
    "vermenigvuldigd.",
]


def исп_квадрат(шаг):
    вон = bilang.Двое(ЯЗЫКИ_МИРА)
    for i in range(ИСПОЛНЕНИЙ):
        n = 2 + семя(шаг, i) % 24
        вон.append(f"qual é o quadrado de {n}? {n} × {n} = {n * n}.")
        вон.append(f"wat is het kwadraat van {n}? {n} × {n} = "
                   f"{n * n}.")
    return вон.парами


def контр_квадрат(шаг):
    вон = bilang.Двое(ЯЗЫКИ_МИРА)
    for i in range(КОНТРПРИМЕРОВ):
        n = 3 + (семя(шаг, i) % 9) * 2
        вон.append(f"todo quadrado é par é falso: {n} é ímpar e "
                   f"{n} × {n} = {n * n}, que é ímpar.")
        вон.append(f"elk kwadraat is even is onwaar: {n} is oneven en "
                   f"{n} × {n} = {n * n}, wat oneven is.")
    return universals.с_вопросами_меченые(вон.парами, ЯЗЫКИ_МИРА)


def общ_квадрат(шаг):
    вон = bilang.Двое(ЯЗЫКИ_МИРА)
    for i in range(ОБОБЩЕНИЙ):
        n = 2 + семя(шаг, i) % 15
        чёт = n % 2 == 0
        порт = "par" if чёт else "ímpar"
        нид = "even" if чёт else "oneven"
        вон.append(f"o quadrado de um número {порт} é {порт}: "
                   f"{n} × {n} = {n * n}.")
        вон.append(f"het kwadraat van een {нид} getal is {нид}: "
                   f"{n} × {n} = {n * n}.")
    return universals.с_вопросами_меченые(вон.парами, ЯЗЫКИ_МИРА)


# ---------------------------------------------------------------- РОДЫ

# РОД ОБЪЯВЛЯЕТ ЧЕТЫРЕ СТУПЕНИ И НИЧЕГО БОЛЬШЕ. Механизм лестницы один
# на все роды и на оба языка: прибавить род — значит объявить четвёрку,
# прибавить ЯЗЫК — значит дописать вторую строку в каждое объявление.
# ИМЯ, ЗАНЯТОЕ ДВАЖДЫ, ЕСТЬ ДВА РАЗНЫХ ЗНАНИЯ ПОД ОДНИМ СЛОВОМ (16.09). Кортеж шестёрок
# ниже звался `РОДЫ` и через сорок строк переопределялся рядом имён; первое определение
# умирало молча, и читатель, нашедший его поиском, читал не то, чем дом пользуется.
#
#     ЧИТАТЕЛЬ ИЩЕТ ИМЯ И НАХОДИТ ПЕРВОЕ ЕГО ОПРЕДЕЛЕНИЕ. Если оно мертво, дом соврал ему
#     не строкой, а порядком строк.
#
# Кортеж назван СВОИМ именем сразу — `СОСТАВ`, — и `РОДЫ` остаётся одним рядом имён.
СОСТАВ = (
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
    пары = list(zip(опр, ЯЗЫКИ_МИРА))
    return пары + [(f"{в} {о}", я) for (в, о), я in zip(zip(вопр, опр), ЯЗЫКИ_МИРА)]

# ------------------------------------------------------------------ ОБЪЯВЛЕНИЕ ДОМА
#
# ШЕСТЬ РОДОВ СТОЯЛИ В КУЗНИЦЕ КОРТЕЖЕМ ШЕСТЁРОК С ПЕРВОГО ДНЯ, и дом их лишь ВЫСТАВИЛ наружу
# вместе со словарём показов, которого у мира не было.
#
#     МИР, ЧЬИ СТРАНИЦЫ НЕ НАЗВАНЫ РОДОМ, ЧИТАЕТСЯ ТОЛЬКО ТЕМ, КТО ЧИТАЕТ КУЗНИЦУ.
#
# ДВЕ ПОСЛЕДНИЕ ГРУППЫ ПРИХОДЯТ ИЗ ЧУЖИХ ДОМОВ — чётность (`tools/parity.py`) и взаимная
# простота (`tools/coprime.py`), — и род у них назван по дому, а не выдуман здесь.

РОДЫ = tuple(и for и, *_ in СОСТАВ) + ("чётность", "взаимная простота")

ЗАЧЕМ_РОДА = {
    **{и: "ступень определения: само определение, его вопрос, исполнение, "
          "противоречие и общее правило" for и, *_ in СОСТАВ},
    "чётность": "предикат чётности на языках мира — из дома чётности",
    "взаимная простота": "предикат взаимной простоты — из дома взаимной простоты",
}


def группы_меченые(шаг):
    """[[(страница, язык)]] — те же группы, но каждая страница со своим языком.

    ЯЗЫК ЗДЕСЬ НЕ ВЫВЕДЕН, А ДОНЕСЁН: сборы родов метят строку в месте кладки
    (`bilang.Двое`), помощники вопроса и перефразы несут метку дальше, а чужие дома —
    чётность и взаимная простота — отдают её своим циклом по языкам.
    """
    вон = []
    for _имя, вопр, опр, исп, контр, общ in СОСТАВ:
        вон.append(ступень_определения(вопр, опр) + исп(шаг) + контр(шаг) + общ(шаг))
    вон.append(parity.показы_меченые(ЯЗЫКИ_МИРА, шаг))
    вон.append(coprime.показы_меченые(ЯЗЫКИ_МИРА, шаг))
    return вон


def группы(шаг):
    """[[страница]] — ровно те группы и в том порядке, какими кузница кормит `emit_grouped`."""
    return [[с for с, _я in группа] for группа in группы_меченые(шаг)]


def перебор_страниц(шаг):
    """[(страница, род, язык)] — те же группы, но каждая под своим именем и языком."""
    вон = []
    for имя, группа in zip(РОДЫ, группы_меченые(шаг)):
        for с, язык in группа:
            вон.append((с, имя, язык))
    return вон


def _показы():
    """Словарь ПОСТРОЧНО: свод построчен, а показ бывает многострочен."""
    from layer import PASSES                              # noqa: PLC0415
    вон = {}
    for шаг in range(len(PASSES)):
        for с, род, язык in перебор_страниц(шаг):
            for строка in с.split("\n"):
                if строка.rstrip():
                    вон.setdefault(строка.rstrip(), (язык, род))
    return вон


ПОКАЗЫ = _показы()


РОД_В_ПОКАЗЕ = 1


def _самопроверка_страниц():
    assert set(ЗАЧЕМ_РОДА) == set(РОДЫ), "глосса рода разошлась с объявлением"
    assert all("\n" not in к for к in ПОКАЗЫ), "словарь показов обязан быть построчным"
    пустые = set(РОДЫ) - {р for _я, р in ПОКАЗЫ.values()}
    assert not пустые, f"род объявлен и не кован: {sorted(пустые)}"
    языки = {я for я, _р in ПОКАЗЫ.values()}
    assert языки == set(ЯЗЫКИ_МИРА), f"язык объявлен и не кован: {sorted(set(ЯЗЫКИ_МИРА) - языки)}"
    из_перебора = sorted(с for с, _р, _я in перебор_страниц(0))
    из_групп = sorted(с for г in группы(0) for с in г)
    assert из_перебора == из_групп, "пересборка потеряла или выдумала страницы"
    # МЕТКА ПРОВЕРЯЕТСЯ ПИСЬМОМ ТАМ, ГДЕ ПИСЬМО ЕЁ ЗНАЕТ (15.09). Язык взят у строителя, и
    # взят он верно лишь тогда, когда порядок кладки таков, как объявлено. Утверждения
    # универсалий несут признак своего языка (`universals.язык`), и на них метка СВЕРЯЕТСЯ:
    # дом, положивший три строки подряд на одном языке, будет пойман здесь.
    #
    #     ДОГАДКА ПО ПИСЬМУ ЕСТЬ МЕРА ПОСЛЕДНЕГО СРЕДСТВА: ею проверяют метку, а не ставят.
    сверено = 0
    for с, _род, язык in перебор_страниц(0):
        строка = с.split("\n")[0]
        try:
            по_письму = universals.язык(строка, ЯЗЫКИ_МИРА)
        except ValueError:
            continue                                  # вопрос признаков языка не несёт
        assert по_письму == язык, f"метка {язык}, а письмо {по_письму}: «{строка[:60]}»"
        сверено += 1
    assert сверено > 100, f"сверено с письмом всего {сверено} строк — мало для пробы"


_самопроверка_страниц()
