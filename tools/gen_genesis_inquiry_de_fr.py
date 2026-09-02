#!/usr/bin/env python3
"""GENESIS layer: THE LADDER OF INQUIRY IN GERMAN AND FRENCH.

Twenty-nine languages can COUNT and DECLINE. Two can REASON. Every
world that decides a case — inquiry, wagers, everyday, formulas —
speaks English and Russian and nothing else, so twenty-seven packs buy
the organism a vocabulary and no method. That gap is the reason this
layer exists, and it is not a gap of volume: a language that never
shows a DECIDED CASE teaches its words as labels.

THE LADDER IS THE ENGLISH-RUSSIAN ONE, UNCHANGED. Four rungs, and each
rung is a different act:

    ОПРЕДЕЛЕНИЕ  — what the notion IS, said in words and not shown,
                   and said TWICE: as a statement and as the answer to
                   its own question
    ИСПОЛНЕНИЕ   — a particular case DECIDED, with the ground beside
                   the verdict («nein: 91 = 7 × 13»)
    КОНТРПРИМЕР  — a universal claim KILLED by one witness
    ОБОБЩЕНИЕ    — the law the cases were instances of

Six genera declare their four rungs as functions over the pass number;
the machinery is written once. Adding a genus costs a declaration, and
adding a LANGUAGE costs a second string in every declaration — which is
the test that the ladder is a form and not an English habit.

ЯЗЫК ЕСТЬ ЧАСТЬ ФАКТА, А НЕ ЕГО ОДЕЖДА. Три вещи корпус не смеет
выучить неверно, и все три суть правила, а не описки:

  · ФРАНЦУЗСКИЙ СТАВИТ ПРОБЕЛ ПЕРЕД «?» И «:». «91 est-il premier ?»,
    «non : 91 = 7 × 13.» Тонкий неразрывный пробел — типографика
    французского, и написать «premier?» значит написать по-английски
    французскими словами;
  · НЕМЕЦКАЯ РАМКА ДЕРЖИТ ГЛАГОЛ НА КОНЦЕ: «ist 128 durch 8 teilbar?»
    — не «ist 128 teilbar durch 8»; во французском на том же месте
    стоит ИНВЕРСИЯ: «128 est-il divisible par 8 ?»;
  · НЕМЕЦКОЕ ИМЯ ПИШЕТСЯ С ПРОПИСНОЙ. «Primzahl», «Teiler», «Rest»,
    «Quadrat», «Summe» — это орфография, а не оформление: строчное имя
    в немецком есть ошибка, а корпус учит с полной судимостью. Начало
    предложения при этом остаётся строчным, как во всём корпусе:
    заглавная в начале строки НИЧЕГО не значит и потому не пишется.

ЧИСЛА ПИШУТСЯ ЦИФРАМИ, КАК В АНГЛИЙСКОМ И РУССКОМ БЛИЗНЕЦАХ. Ни одного
немецкого или французского числительного здесь не выдумано: там, где
слово было бы естественно, стоит цифра — та же, что у близнецов, и
потому сравнимая с ними. Таблицы `tools/langpacks/de.json` и `fr.json`
прочитаны ради этой проверки, а не ради заимствования.

ЯДРО ДОСЛОВНЫХ ПОВТОРОВ. Первые три случая каждой ступени берут семя
БЕЗ прохода и потому одинаковы во всех пяти проходах слово в слово;
остальные ходят числами. Форма чеканится повторностью — это замер, а не
мнение: слой, у которого каждый показ нов, не даёт дереву формы ни
одной опоры.

EVERY GROUND IS COMPUTED HERE AND RE-COMPUTED BY THE COURT.
`courts/inquiry_de_fr_court.py` factorises again, divides again, sums
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
import parity  # noqa: E402
import paraphrase  # noqa: E402

ЦЕЛЬ = "datasets/genesis_inquiry_de_fr.txt"

# ЯДРО ДОСЛОВНЫХ ПОВТОРОВ: столько первых случаев каждой ступени стоят
# во ВСЕХ проходах слово в слово.
ЯДРО = 3
ИСПОЛНЕНИЙ = 12
КОНТРПРИМЕРОВ = 6
ОБОБЩЕНИЙ = 8


def семя(шаг, i):
    """Семя случая. Первые ЯДРО не знают прохода — оттого и дословны.

    ХОД ПРОХОДА ВЗЯТ КРАТНЫМ ТРИНАДЦАТИ, чтобы хвост одного прохода не
    сел на хвост другого: при шаге 1 семя хвоста начинается за пределом
    ядра и дальше расходится, а не повторяет соседа со сдвигом на один.
    """
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

ВОПР_ПРОСТОТА = ["was ist eine Primzahl?",
                 "qu'est-ce qu'un nombre premier ?"]
ОПР_ПРОСТОТА = [
    "eine Primzahl ist eine ganze Zahl größer als 1, deren einzige "
    "Teiler 1 und sie selbst sind.",
    "un nombre premier est un nombre entier supérieur à 1 dont les "
    "seuls diviseurs sont 1 et lui-même.",
]


def исп_простота(шаг):
    """ОБЕ ВЕТВИ ВЕРДИКТА ОБЯЗАНЫ ЗВУЧАТЬ, И ЭТО ПРОВЕРЕНО ЧИСЛОМ.

    Первая редакция брала n = 40 + семя × 5 — и всякое n делилось на
    пять: ноль простых на шестьдесят случаев, и ответ «ja» не звучал
    НИ РАЗУ. Слой при этом был бы зелен у всякого суда: он не лгал, он
    молчал о половине рода. Шаг, взаимно простой с сорока одним,
    даёт двадцать пять простых из шестидесяти.
    """
    вон = []
    for i in range(ИСПОЛНЕНИЙ):
        n = 41 + семя(шаг, i) * 3
        if простое(n):
            вон.append(f"ist {n} eine Primzahl? ja: die Teiler von {n} "
                       f"sind 1 und {n}.")
            вон.append(f"{n} est-il un nombre premier ? oui : les "
                       f"diviseurs de {n} sont 1 et {n}.")
        else:
            д = наименьший_делитель(n)
            вон.append(f"ist {n} eine Primzahl? nein: {n} = {д} × "
                       f"{n // д}.")
            вон.append(f"{n} est-il un nombre premier ? non : {n} = "
                       f"{д} × {n // д}.")
    return paraphrase.перефразы(вон, ЯЗЫКИ_МИРА, ("prime", "divisible"))


# A UNIVERSAL IS ASKED BY ITS OWN «IS IT TRUE THAT» (tools/universals.py):
# the question of every counterexample and generalization is derived from
# its statement by the one law of the house, in both languages of the world.
ЯЗЫКИ_МИРА = ('de', 'fr')


def контр_простота(шаг):
    вон = []
    for i in range(КОНТРПРИМЕРОВ):
        n = 9 + семя(шаг, i) * 2
        while простое(n):
            n += 2
        д = наименьший_делитель(n)
        вон.append(f"alle ungeraden Zahlen sind Primzahlen ist falsch: "
                   f"{n} ist ungerade und {n} = {д} × {n // д}.")
        вон.append(f"tous les nombres impairs sont premiers est faux : "
                   f"{n} est impair et {n} = {д} × {n // д}.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


def общ_простота(шаг):
    вон = []
    for i in range(ОБОБЩЕНИЙ):
        n = 84 + семя(шаг, i)
        ряд = " × ".join(str(x) for x in разложение(n))
        вон.append(f"jede ganze Zahl größer als 1 ist ein Produkt von "
                   f"Primzahlen: {n} = {ряд}.")
        вон.append(f"tout nombre entier supérieur à 1 est un produit "
                   f"de nombres premiers : {n} = {ряд}.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


# ----------------------------------------------------------- ДЕЛИМОСТЬ

ВОПР_ДЕЛИМОСТЬ = ["was bedeutet teilbar?", "que signifie divisible ?"]
ОПР_ДЕЛИМОСТЬ = [
    "eine Zahl ist durch eine andere teilbar, wenn der Rest 0 ist.",
    "un nombre est divisible par un autre quand le reste est 0.",
]


def исп_делимость(шаг):
    """ДЕЛИМОСТЬ СТРОИТСЯ ОТ ОТВЕТА, А НЕ ВЫПАДАЕТ ПО УДАЧЕ.

    Ряд, взятый наугад (a = 100 + семя × 9), давал деление без остатка
    ТРИ раза на шестьдесят: ветвь «ja» покупалась бы тремя показами на
    пять проходов, и форма утвердительного ответа не сложилась бы. Здесь
    делитель и частное выбраны первыми, а делимое собрано из них — и
    половина случаев делится по построению. Остаток во второй половине
    берётся строго меньше делителя, иначе он не остаток.
    """
    вон = []
    for i in range(ИСПОЛНЕНИЙ):
        с = семя(шаг, i)
        b = 3 + с % 8
        a = b * (7 + с % 13) + (0 if с % 2 == 0 else 1 + с % (b - 1))
        q, r = divmod(a, b)
        if r == 0:
            вон.append(f"ist {a} durch {b} teilbar? ja: {a} = {b} × "
                       f"{q}, Rest 0.")
            вон.append(f"{a} est-il divisible par {b} ? oui : {a} = "
                       f"{b} × {q}, reste 0.")
            вон.append(f"{a} ist durch {b} teilbar: {a} = {b} × {q}, Rest 0.")
            вон.append(f"{a} est divisible par {b} : {a} = {b} × {q}, "
                       f"reste 0.")
        else:
            вон.append(f"ist {a} durch {b} teilbar? nein: {a} = {b} × "
                       f"{q} + {r}, Rest {r}.")
            вон.append(f"{a} est-il divisible par {b} ? non : {a} = "
                       f"{b} × {q} + {r}, reste {r}.")
        if r:
            вон.append(f"{a} ist nicht durch {b} teilbar: {a} = {b} × {q} + "
                       f"{r}, Rest {r}.")
            вон.append(f"{a} n'est pas divisible par {b} : {a} = {b} × {q} "
                       f"+ {r}, reste {r}.")
    return paraphrase.перефразы(вон, ЯЗЫКИ_МИРА, ("prime", "divisible"))


def контр_делимость(шаг):
    вон = []
    for i in range(КОНТРПРИМЕРОВ):
        n = 6 + семя(шаг, i) * 2
        while n % 4 == 0:
            n += 2
        q, r = divmod(n, 4)
        вон.append(f"jede gerade Zahl ist durch 4 teilbar ist falsch: "
                   f"{n} ist gerade und {n} = 4 × {q} + {r}.")
        вон.append(f"tout nombre pair est divisible par 4 est faux : "
                   f"{n} est pair et {n} = 4 × {q} + {r}.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


def общ_делимость(шаг):
    вон = []
    for i in range(ОБОБЩЕНИЙ):
        n = 3 * (37 + семя(шаг, i))
        с = сумма_цифр(n)
        вон.append(f"eine Zahl ist durch 3 teilbar, wenn ihre "
                   f"Quersumme es ist: die Quersumme von {n} ist {с}, "
                   f"und {с} = 3 × {с // 3}.")
        вон.append(f"un nombre est divisible par 3 quand la somme de "
                   f"ses chiffres l'est : la somme des chiffres de {n} "
                   f"est {с}, et {с} = 3 × {с // 3}.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


# ------------------------------------------------------ СУММА НЕЧЁТНЫХ

ВОПР_НЕЧЁТНЫЕ = ["was ist eine ungerade Zahl?",
                 "qu'est-ce qu'un nombre impair ?"]
ОПР_НЕЧЁТНЫЕ = [
    "die ungeraden Zahlen beginnen mit 1, 3, 5, 7, und jede ist um 2 "
    "größer als die vorige.",
    "les nombres impairs commencent par 1, 3, 5, 7, et chacun dépasse "
    "le précédent de 2.",
]


def исп_нечётные(шаг):
    вон = []
    for i in range(ИСПОЛНЕНИЙ):
        k = 2 + семя(шаг, i) % 11
        ряд = " + ".join(str(2 * j + 1) for j in range(k))
        вон.append(f"was ist die Summe der ersten {k} ungeraden "
                   f"Zahlen? {ряд} = {k * k}.")
        вон.append(f"quelle est la somme des {k} premiers nombres "
                   f"impairs ? {ряд} = {k * k}.")
    return вон


def контр_нечётные(шаг):
    вон = []
    for i in range(КОНТРПРИМЕРОВ):
        k = 3 + семя(шаг, i) % 9
        вон.append(f"die Summe der ersten k ungeraden Zahlen ist "
                   f"2 × k ist falsch: bei k = {k} ist die Summe "
                   f"{k * k}, und 2 × {k} = {2 * k}.")
        вон.append(f"la somme des k premiers nombres impairs est "
                   f"2 × k est faux : pour k = {k} la somme est "
                   f"{k * k}, et 2 × {k} = {2 * k}.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


def общ_нечётные(шаг):
    вон = []
    for i in range(ОБОБЩЕНИЙ):
        k = 1 + семя(шаг, i) % 12
        вон.append(f"die Summe der ersten k ungeraden Zahlen ist "
                   f"k × k: bei k = {k} ist es {k} × {k} = {k * k}.")
        вон.append(f"la somme des k premiers nombres impairs est "
                   f"k × k : pour k = {k} c'est {k} × {k} = {k * k}.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


# ------------------------------------------------------ УСЛОВНЫЙ ВЫВОД

ВОПР_УСЛОВНОЕ = ["was ist eine bedingte Aussage?",
                 "qu'est-ce qu'une proposition conditionnelle ?"]
ОПР_УСЛОВНОЕ = [
    "eine bedingte Aussage gilt, wenn die Folgerung in jedem Fall "
    "gilt, in dem die Voraussetzung gilt.",
    "une proposition conditionnelle est vraie quand la conclusion "
    "vaut dans tous les cas où la prémisse vaut.",
]


def исп_условное(шаг):
    вон = []
    for i in range(ИСПОЛНЕНИЙ):
        с = семя(шаг, i)
        m = 1 + с % 9
        e = 4 + (с % 8) * 2
        s = e + m
        да = m % 2 == 0
        вон.append(f"wenn n gerade ist, ist n + {m} gerade? "
                   f"{'ja' if да else 'nein'}: {e} ist gerade, und "
                   f"{e} + {m} = {s}, was "
                   f"{'gerade' if s % 2 == 0 else 'ungerade'} ist.")
        вон.append(f"si n est pair, n + {m} est-il pair ? "
                   f"{'oui' if да else 'non'} : {e} est pair, et "
                   f"{e} + {m} = {s}, qui est "
                   f"{'pair' if s % 2 == 0 else 'impair'}.")
    return вон


def контр_условное(шаг):
    вон = []
    for i in range(КОНТРПРИМЕРОВ):
        с = семя(шаг, i)
        m = 1 + (с % 5) * 2
        e = 6 + (с % 7) * 2
        s = e + m
        вон.append(f"wenn n gerade ist, dann ist n + {m} gerade ist "
                   f"falsch: {e} ist gerade, und {e} + {m} = {s}, was "
                   f"ungerade ist.")
        вон.append(f"si n est pair alors n + {m} est pair est faux : "
                   f"{e} est pair, et {e} + {m} = {s}, qui est impair.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


def общ_условное(шаг):
    вон = []
    for i in range(ОБОБЩЕНИЙ):
        с = семя(шаг, i)
        m = 2 + (с % 6) * 2
        e = 8 + (с % 5) * 2
        вон.append(f"wenn n gerade ist, dann ist n + m genau dann "
                   f"gerade, wenn m gerade ist: {m} ist gerade und "
                   f"{e} + {m} = {e + m}, was gerade ist.")
        вон.append(f"si n est pair alors n + m est pair exactement "
                   f"quand m est pair : {m} est pair et {e} + {m} = "
                   f"{e + m}, qui est pair.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


# ------------------------------------------------------- ИНЪЕКТИВНОСТЬ

ВОПР_ИНЪЕКЦИЯ = ["was heißt es, dass eine Funktion injektiv ist?",
                 "que signifie qu'une fonction est injective ?"]
ОПР_ИНЪЕКЦИЯ = [
    "eine Funktion ist injektiv, wenn verschiedene Eingaben "
    "verschiedene Ausgaben liefern.",
    "une fonction est injective quand des entrées différentes donnent "
    "des sorties différentes.",
]


def исп_инъекция(шаг):
    вон = []
    for i in range(ИСПОЛНЕНИЙ):
        k = семя(шаг, i) % 6
        a, b, c = 1 * k, 2 * k, 3 * k
        да = k != 0
        разн_de = "alle verschieden" if да else "nicht alle verschieden"
        разн_fr = "toutes différentes" if да else "pas toutes différentes"
        вон.append(f"ist f(x) = x × {k} auf 1, 2, 3 injektiv? "
                   f"{'ja' if да else 'nein'}: sie liefert {a}, {b}, "
                   f"{c}, {разн_de}.")
        вон.append(f"f(x) = x × {k} est-elle injective sur 1, 2, 3 ? "
                   f"{'oui' if да else 'non'} : elle donne {a}, {b}, "
                   f"{c}, {разн_fr}.")
    return вон


def контр_инъекция(шаг):
    вон = []
    for i in range(КОНТРПРИМЕРОВ):
        с = семя(шаг, i)
        a, b = 1 + с % 5, 6 + с % 5
        вон.append(f"jede Funktion ist injektiv ist falsch: "
                   f"f(x) = x × 0 schickt {a} und {b} beide auf 0.")
        вон.append(f"toute fonction est injective est faux : "
                   f"f(x) = x × 0 envoie {a} et {b} tous deux sur 0.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


def общ_инъекция(шаг):
    вон = []
    for i in range(ОБОБЩЕНИЙ):
        k = 1 + семя(шаг, i) % 7
        вон.append(f"f(x) = x × k ist genau dann injektiv, wenn k "
                   f"nicht 0 ist: bei k = {k} liefern die Eingaben 1 "
                   f"und 2 die Werte {k} und {2 * k}.")
        вон.append(f"f(x) = x × k est injective exactement quand k "
                   f"n'est pas 0 : pour k = {k} les entrées 1 et 2 "
                   f"donnent {k} et {2 * k}.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


# ------------------------------------------------------------- КВАДРАТ

ВОПР_КВАДРАТ = ["was ist das Quadrat einer Zahl?",
                "qu'est-ce que le carré d'un nombre ?"]
ОПР_КВАДРАТ = [
    "das Quadrat einer Zahl ist die Zahl mit sich selbst "
    "multipliziert.",
    "le carré d'un nombre est le nombre multiplié par lui-même.",
]


def исп_квадрат(шаг):
    вон = []
    for i in range(ИСПОЛНЕНИЙ):
        n = 2 + семя(шаг, i) % 24
        вон.append(f"was ist das Quadrat von {n}? {n} × {n} = "
                   f"{n * n}.")
        вон.append(f"quel est le carré de {n} ? {n} × {n} = {n * n}.")
    return вон


def контр_квадрат(шаг):
    вон = []
    for i in range(КОНТРПРИМЕРОВ):
        n = 3 + (семя(шаг, i) % 9) * 2
        вон.append(f"jedes Quadrat ist gerade ist falsch: {n} ist "
                   f"ungerade und {n} × {n} = {n * n}, was ungerade "
                   f"ist.")
        вон.append(f"tout carré est pair est faux : {n} est impair et "
                   f"{n} × {n} = {n * n}, qui est impair.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


def общ_квадрат(шаг):
    вон = []
    for i in range(ОБОБЩЕНИЙ):
        n = 2 + семя(шаг, i) % 15
        чёт = n % 2 == 0
        нем = "geraden" if чёт else "ungeraden"
        немс = "gerade" if чёт else "ungerade"
        фр = "pair" if чёт else "impair"
        вон.append(f"das Quadrat einer {нем} Zahl ist {немс}: "
                   f"{n} × {n} = {n * n}.")
        вон.append(f"le carré d'un nombre {фр} est {фр} : "
                   f"{n} × {n} = {n * n}.")
    return universals.с_вопросами(вон, ЯЗЫКИ_МИРА)


# ---------------------------------------------------------------- РОДЫ

# РОД ОБЪЯВЛЯЕТ ЧЕТЫРЕ СТУПЕНИ И НИЧЕГО БОЛЬШЕ. Механизм лестницы один
# на все роды и на оба языка: прибавить род — значит объявить четвёрку,
# прибавить ЯЗЫК — значит дописать вторую строку в каждое объявление.
# Ни то, ни другое не стоит нового обхода, и это есть проба, что форма
# есть форма.
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

    Проба на обученном организме показала: знание, у которого есть лишь
    повествовательная поверхность, НЕ ОТВЕЧАЕТ — оно только сообщает.
    Вопрос со своим ответом есть вторая поверхность того же факта, и
    стоит она одной строки. Ступень эта прохода не знает вовсе и потому
    дословна во всех пяти — ядро повторов начинается с неё.
    """
    return list(опр) + [f"{в} {о}" for в, о in zip(вопр, опр)]


def pass_groups(шаг):
    """Одна группа на РОД: ступени рода не перемешиваются с чужими."""
    вон = []
    for _имя, вопр, опр, исп, контр, общ in РОДЫ:
        вон.append(ступень_определения(вопр, опр)
                   + исп(шаг) + контр(шаг) + общ(шаг))
    # ЧЁТНОСТЬ КАК ВОПРОС ВЫБОРА (tools/parity.py, holon 03.09): предикат
    # «чётно/нечётно» рынку универсалий на языках мира.
    вон.append(parity.показы(ЯЗЫКИ_МИРА, шаг))
    return вон


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
