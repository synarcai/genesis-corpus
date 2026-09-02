#!/usr/bin/env python3
"""СЛОЙ GENESIS: ЛЕСТНИЦА ДОЗНАНИЯ ПО-ИСПАНСКИ И ПО-ИТАЛЬЯНСКИ.

РАЗРЫВ, РАДИ КОТОРОГО ЭТО НАПИСАНО. Языков у корпуса двадцать девять, а
РАССУЖДЕНИЕ живёт в двух: дознание, ставки, быт, формулы говорят
по-английски и по-русски. Прочие двадцать семь умеют считать и
склонять — и не умеют РЕШАТЬ. Пакет языка покупает морфологию; он не
покупает поступка «вынести вердикт и положить рядом основание».
Лестница дознания есть именно поступок, и она переносится сюда БЕЗ
ПРАВОК В МЕХАНИЗМЕ: род объявляет четвёрку, лестница одна на все роды.

ЧЕТЫРЕ СТУПЕНИ, ТЕ ЖЕ ШЕСТЬ РОДОВ:

    ОПРЕДЕЛЕНИЕ  — что понятие ЕСТЬ, сказанное словами, и сказанное
                   ВТОРОЙ ПОВЕРХНОСТЬЮ — ответом на прямой вопрос;
    ИСПОЛНЕНИЕ   — частный случай РЕШЁН, и основание стоит рядом с
                   вердиктом («no: 91 = 7 × 13»);
    КОНТРПРИМЕР  — всеобщее утверждение УБИТО одним свидетелем;
    ОБОБЩЕНИЕ    — закон, случаями которого были все решения.

ЯЗЫК ЗДЕСЬ НЕ УКРАШЕНИЕ, И ТРИ ЕГО МЕЛОЧИ СТОЯТ ОТДЕЛЬНОГО СЛОВА:

  · ИСПАНСКИЙ ВОПРОС ОТКРЫВАЕТСЯ ПЕРЕВЁРНУТЫМ ЗНАКОМ. «¿es 91 primo?»
    без «¿» есть не вопрос, а обломок; корпус, выучивший обломок,
    выучит его как норму. Знак стоит в КАЖДОМ вопросе слоя, и суд
    требует его образцом;
  · «SÍ» С УДАРЕНИЕМ ЕСТЬ ДРУГОЕ СЛОВО, ЧЕМ «SI» БЕЗ НЕГО. Первое —
    «да», второе — «если». Оба стоят в одном и том же показе рода
    условного вывода («si n es par, ¿es n + 4 par? sí: …»), и потеря
    ударения превратила бы утверждение в союз. Итальянское «sì» —
    то же самое;
  · ЧИСЛИТЕЛЬНОЕ БЕРЁТСЯ ИЗ ПАКЕТА ЯЗЫКА, А НЕ ВЫДУМЫВАЕТСЯ. Слова
    читаются из `tools/langpacks/es.json` и `it.json`; чего пакет не
    объявил, пишется ЦИФРОЙ. Испанский объявляет связку «y», и
    составное от тридцати одного до девяноста девяти собирается по
    ней («treinta y cinco») — это правило языка, объявленное самим
    языком. Итальянский связки не объявляет, и не по бедности пакета:
    итальянское составное СЛИВАЕТСЯ и притом с выпадением гласной
    («trentuno», «ventotto»), а связкой такого не выразить вовсе.
    Оттого по-итальянски за пределами таблицы стоит цифра — честное
    молчание вместо выдуманного слова.

ЯДРО ДОСЛОВНЫХ ПОВТОРОВ. Первые три случая КАЖДОГО рода одинаковы во
всех проходах, остальные ходят числами. Рамка «вопрос — ответ»
покупается организмом лишь тогда, когда один и тот же показ встречен
многократно ДОСЛОВНО; показ, каждый раз новый, учит роду, но не учит
рамке. Ядро есть плата за рамку, ход — плата за род, и нужны оба.

ЧУЖОЙ РОД ПРОВЕРЕН НАРОЧНО, И ЗДЕСЬ ОН ОПАСНЕЕ ОБЫЧНОГО. Испанский
пакет объявляет арифметическому суду корпуса «es» ЗНАКОМ РАВЕНСТВА, а
«por» — умножением; итальянский объявляет «fa» равенством и «per»
умножением. Но «es» есть связка «есть», а «per» стоит в самом обороте
«divisibile per 8»: слова эти живут в КАЖДОЙ второй строке слоя. Записи
подобраны так, чтобы тот суд либо судил их ВЕРНО (чистая выкладка
«91 = 7 × 13» есть истина и судится истиной), либо не судил вовсе. Ни
одна строка слоя не даёт ему (судимо, ложно) — это замерено, а не
предположено.
"""

import json
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_inquiry_es_it.txt"


# ------------------------------------------------------------- ЧИСЛА

def _таблица(язык):
    """Числительные языка — ИЗ ЕГО ПАКЕТА, а не из головы.

    Пакет есть единственное объявление языка о себе, и второй список
    числительных, набранный рукой здесь, назавтра разошёлся бы с ним
    молча. Читаем то, что язык о себе сказал.
    """
    путь = КОРЕНЬ / "tools" / "langpacks" / f"{язык}.json"
    пакет = json.loads(путь.read_text(encoding="utf-8"))
    связки = пакет.get("numeral_connectors") or []
    return пакет.get("numerals", {}), (связки[0] if связки else None)


ЧИСЛА_ES, СВЯЗКА_ES = _таблица("es")
ЧИСЛА_IT, СВЯЗКА_IT = _таблица("it")


def словом(n, таблица, связка):
    """Число словом, ЕСЛИ язык его объявил; иначе ЦИФРОЙ.

    СОСТАВНОЕ СОБИРАЕТСЯ ТОЛЬКО ТАМ, ГДЕ ЯЗЫК ОБЪЯВИЛ СВЯЗКУ. Испанское
    «treinta y cinco» есть десяток, связка и единица — и все три части
    объявлены пакетом; собрать их значит применить правило языка, а не
    выдумать слово. Итальянское составное сливается с выпадением
    гласной («venti» + «otto» = «ventotto»), и связки для него нет
    ни в пакете, ни в языке — потому за таблицей стоит цифра.

    ГРАНИЦА НАЗВАНА ЧИСЛОМ: собирается только тридцать один — девяносто
    девять и только не кратное десяти. Ниже тридцати испанский пишет
    слитно и неправильно («dieciséis», «veintiuno»), и там годится
    ровно то, что объявлено таблицей.
    """
    слово = таблица.get(str(n))
    if слово:
        return слово
    if связка and 31 <= n <= 99 and n % 10:
        десяток = таблица.get(str(n - n % 10))
        единица = таблица.get(str(n % 10))
        if десяток and единица:
            return f"{десяток} {связка} {единица}"
    return str(n)


def по_испански(n):
    return словом(n, ЧИСЛА_ES, СВЯЗКА_ES)


def по_итальянски(n):
    return словом(n, ЧИСЛА_IT, СВЯЗКА_IT)


# ------------------------------------------------------------- СЧЁТ

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


def случаи(ядро, ход):
    """ЯДРО ДОСЛОВНО ВО ВСЕХ ПРОХОДАХ, ХОД — ЧИСЛАМИ ПО ПРОХОДУ.

    Один закон на все шесть родов и на все четыре ступени. Случай хода,
    совпавший с ядром, ВЫБРАСЫВАЕТСЯ: перемешивание есть перестановка,
    и двойник в одном проходе стал бы двумя одинаковыми строками.
    """
    видано = list(ядро)
    return видано + [с for с in ход if с not in видано]


# ---------------------------------------------------------- ПРОСТОТА

ВОПР_ПРОСТОТА = ["¿qué es un número primo?",
                 "che cos'è un numero primo?"]
ОПР_ПРОСТОТА = [
    "un número primo es un número entero mayor que 1 divisible solo "
    "por 1 y por sí mismo.",
    "un numero primo è un numero intero maggiore di 1 divisibile solo "
    "per 1 e per sé stesso.",
]
ЯДРО_ПРОСТОТА = (91, 97, 51)
ЯДРО_КОНТР_ПРОСТОТА = (9, 15, 21)
ЯДРО_ОБЩ_ПРОСТОТА = (84, 90, 100)


def исп_простота(шаг):
    """Вердикт по СЧЁТУ, и основание рядом: делители либо разложение."""
    вон = []
    ход = [40 + шаг * 7 + i * 5 for i in range(5)]
    for n in случаи(ЯДРО_ПРОСТОТА, ход):
        if простое(n):
            вон.append(f"¿es {n} un número primo? sí: los divisores de "
                       f"{n} son 1 y {n}.")
            вон.append(f"{n} è un numero primo? sì: i divisori di {n} "
                       f"sono 1 e {n}.")
        else:
            д = наименьший_делитель(n)
            вон.append(f"¿es {n} un número primo? no: {n} = {д} × "
                       f"{n // д}.")
            вон.append(f"{n} è un numero primo? no: {n} = {д} × "
                       f"{n // д}.")
    return вон


def контр_простота(шаг):
    """Свидетель назван И СЛОВОМ, И ЦИФРОЙ — две поверхности числа."""
    вон = []
    # ХОД ОБЯЗАН ХОДИТЬ, И ЭТО ЗАМЕРЕНО. Первая редакция брала
    # «9 + (шаг + i) * 2» и, отступая от простых, во ВСЕХ пяти проходах
    # приходила в одни и те же девять, пятнадцать и двадцать один — то
    # есть ровно в ядро. Тридцать показов давали ШЕСТЬ разных: объём
    # покупал вес, а не факты. Шаг разведён с номером случая, и
    # свидетели расходятся до сорока пяти — попутно выводя испанское
    # составное со связкой («treinta y tres»).
    ход = []
    for i in range(3):
        n = 9 + шаг * 6 + i * 4
        while простое(n):
            n += 2
        ход.append(n)
    for n in случаи(ЯДРО_КОНТР_ПРОСТОТА, ход):
        д = наименьший_делитель(n)
        вон.append(f"todos los números impares son primos es falso: "
                   f"{по_испански(n)} es impar y {n} = {д} × "
                   f"{n // д}.")
        вон.append(f"tutti i numeri dispari sono primi è falso: "
                   f"{по_итальянски(n)} è dispari e {n} = {д} × "
                   f"{n // д}.")
    return вон


def общ_простота(шаг):
    вон = []
    ход = [84 + шаг * 3 + i for i in range(3)]
    for n in случаи(ЯДРО_ОБЩ_ПРОСТОТА, ход):
        ряд = " × ".join(str(x) for x in разложение(n))
        вон.append(f"todo número entero mayor que 1 es un producto de "
                   f"primos: {n} = {ряд}.")
        вон.append(f"ogni numero intero maggiore di 1 è un prodotto di "
                   f"primi: {n} = {ряд}.")
    return вон


# --------------------------------------------------------- ДЕЛИМОСТЬ

ВОПР_ДЕЛИМОСТЬ = ["¿qué significa divisible?",
                  "che cosa significa divisibile?"]
ОПР_ДЕЛИМОСТЬ = [
    "un número es divisible por otro cuando el resto es 0.",
    "un numero è divisibile per un altro quando il resto è 0.",
]
ЯДРО_ДЕЛИМОСТЬ = ((128, 8), (100, 3), (91, 7))
ЯДРО_КОНТР_ДЕЛИМОСТЬ = (6, 10, 14)
ЯДРО_ОБЩ_ДЕЛИМОСТЬ = (111, 123, 132)


def исп_делимость(шаг):
    вон = []
    ход = [(100 + шаг * 11 + i * 9, 3 + (шаг + i) % 8)
           for i in range(5)]
    for a, b in случаи(ЯДРО_ДЕЛИМОСТЬ, ход):
        q, r = divmod(a, b)
        if r == 0:
            вон.append(f"¿es {a} divisible por {b}? sí: {a} = {b} × "
                       f"{q}, resto 0.")
            вон.append(f"{a} è divisibile per {b}? sì: {a} = {b} × "
                       f"{q}, resto 0.")
        else:
            вон.append(f"¿es {a} divisible por {b}? no: {a} = {b} × "
                       f"{q} + {r}, resto {r}.")
            вон.append(f"{a} è divisibile per {b}? no: {a} = {b} × "
                       f"{q} + {r}, resto {r}.")
    return вон


def контр_делимость(шаг):
    вон = []
    ход = []
    for i in range(3):
        n = 6 + шаг * 8 + i * 2
        while n % 4 == 0:
            n += 2
        ход.append(n)
    for n in случаи(ЯДРО_КОНТР_ДЕЛИМОСТЬ, ход):
        q, r = divmod(n, 4)
        вон.append(f"todos los números pares son divisibles por 4 es "
                   f"falso: {n} es par y {n} = 4 × {q} + {r}.")
        вон.append(f"tutti i numeri pari sono divisibili per 4 è "
                   f"falso: {n} è pari e {n} = 4 × {q} + {r}.")
    return вон


def общ_делимость(шаг):
    вон = []
    ход = [3 * (37 + шаг * 5 + i) for i in range(3)]
    for n in случаи(ЯДРО_ОБЩ_ДЕЛИМОСТЬ, ход):
        с = сумма_цифр(n)
        вон.append(f"un número es divisible por 3 cuando lo es la suma "
                   f"de sus cifras: la suma de las cifras de {n} es "
                   f"{с}, y {с} = 3 × {с // 3}.")
        вон.append(f"un numero è divisibile per 3 quando lo è la somma "
                   f"delle sue cifre: la somma delle cifre di {n} è "
                   f"{с}, e {с} = 3 × {с // 3}.")
    return вон


# ---------------------------------------------------- СУММА НЕЧЁТНЫХ

ВОПР_НЕЧЁТНЫЕ = ["¿qué es un número impar?",
                 "che cos'è un numero dispari?"]
ОПР_НЕЧЁТНЫЕ = [
    "los números impares empiezan 1, 3, 5, 7 y cada uno supera al "
    "anterior en 2.",
    "i numeri dispari cominciano 1, 3, 5, 7 e ognuno supera il "
    "precedente di 2.",
]
ЯДРО_НЕЧЁТНЫЕ = (3, 5, 4)
ЯДРО_КОНТР_НЕЧЁТНЫЕ = (3, 5, 7)
ЯДРО_ОБЩ_НЕЧЁТНЫЕ = (4, 6, 9)


def исп_нечётные(шаг):
    """ЗДЕСЬ ЧИСЛО ЗВУЧИТ СЛОВОМ: «los primeros tres números impares».

    Счёт первых нечётных не больше двенадцати, и все эти слова оба
    пакета объявляют — выдумывать не пришлось ничего.
    """
    вон = []
    ход = [2 + (шаг * 2 + i) % 11 for i in range(5)]
    for k in случаи(ЯДРО_НЕЧЁТНЫЕ, ход):
        ряд = " + ".join(str(2 * j + 1) for j in range(k))
        вон.append(f"¿cuánto suman los primeros {по_испански(k)} "
                   f"números impares? {ряд} = {k * k}.")
        вон.append(f"quanto fanno i primi {по_итальянски(k)} numeri "
                   f"dispari? {ряд} = {k * k}.")
    return вон


def контр_нечётные(шаг):
    вон = []
    ход = [3 + (шаг * 2 + i) % 9 for i in range(3)]
    for k in случаи(ЯДРО_КОНТР_НЕЧЁТНЫЕ, ход):
        вон.append(f"la suma de los primeros k números impares es "
                   f"2 × k es falso: con k = {k} la suma es {k * k} y "
                   f"2 × {k} = {2 * k}.")
        вон.append(f"la somma dei primi k numeri dispari è 2 × k è "
                   f"falso: con k = {k} la somma è {k * k} e 2 × {k} = "
                   f"{2 * k}.")
    return вон


def общ_нечётные(шаг):
    вон = []
    ход = [1 + (шаг * 3 + i) % 12 for i in range(3)]
    for k in случаи(ЯДРО_ОБЩ_НЕЧЁТНЫЕ, ход):
        вон.append(f"la suma de los primeros k números impares es "
                   f"k × k: con k = {k} es {k} × {k} = {k * k}.")
        вон.append(f"la somma dei primi k numeri dispari è k × k: con "
                   f"k = {k} è {k} × {k} = {k * k}.")
    return вон


# --------------------------------------------------- УСЛОВНЫЙ ВЫВОД

ВОПР_УСЛОВНОЕ = ["¿qué es un enunciado condicional?",
                 "che cos'è un enunciato condizionale?"]
ОПР_УСЛОВНОЕ = [
    "un condicional es verdadero cuando la conclusión se cumple en "
    "todos los casos en que se cumple la premisa.",
    "un condizionale è vero quando la conclusione vale in tutti i casi "
    "in cui vale la premessa.",
]
ЯДРО_УСЛОВНОЕ = ((4, 6), (3, 8), (2, 10))
ЯДРО_КОНТР_УСЛОВНОЕ = ((3, 6), (5, 8), (7, 10))
ЯДРО_ОБЩ_УСЛОВНОЕ = ((2, 8), (4, 10), (6, 12))


def исп_условное(шаг):
    """«SI» И «SÍ» В ОДНОЙ СТРОКЕ: союз без ударения, «да» с ударением.

    Показ этого рода — единственное место корпуса, где оба слова стоят
    рядом, и потому именно здесь потеря ударения была бы всего дороже.
    """
    вон = []
    ход = [(1 + (шаг * 2 + i) % 9, 4 + ((шаг * 3 + i) % 8) * 2)
           for i in range(5)]
    for m, e in случаи(ЯДРО_УСЛОВНОЕ, ход):
        s = e + m
        да = m % 2 == 0
        вон.append(f"si n es par, ¿es n + {m} par? "
                   f"{'sí' if да else 'no'}: {e} es par y {e} + {m} = "
                   f"{s}, que es {'par' if s % 2 == 0 else 'impar'}.")
        вон.append(f"se n è pari, n + {m} è pari? "
                   f"{'sì' if да else 'no'}: {e} è pari e {e} + {m} = "
                   f"{s}, che è "
                   f"{'pari' if s % 2 == 0 else 'dispari'}.")
    return вон


def контр_условное(шаг):
    вон = []
    ход = [(1 + ((шаг * 2 + i) % 5) * 2, 6 + ((шаг * 3 + i) % 7) * 2)
           for i in range(3)]
    for m, e in случаи(ЯДРО_КОНТР_УСЛОВНОЕ, ход):
        s = e + m
        вон.append(f"si n es par entonces n + {m} es par es falso: "
                   f"{e} es par y {e} + {m} = {s}, que es impar.")
        вон.append(f"se n è pari allora n + {m} è pari è falso: {e} è "
                   f"pari e {e} + {m} = {s}, che è dispari.")
    return вон


def общ_условное(шаг):
    вон = []
    ход = [(2 + ((шаг * 2 + i) % 6) * 2, 8 + ((шаг * 3 + i) % 5) * 2)
           for i in range(3)]
    for m, e in случаи(ЯДРО_ОБЩ_УСЛОВНОЕ, ход):
        s = e + m
        вон.append(f"si n es par entonces n + m es par exactamente "
                   f"cuando m es par: {m} es par y {e} + {m} = {s}, "
                   f"que es par.")
        вон.append(f"se n è pari allora n + m è pari esattamente "
                   f"quando m è pari: {m} è pari e {e} + {m} = {s}, "
                   f"che è pari.")
    return вон


# ---------------------------------------------------- ИНЪЕКТИВНОСТЬ

ВОПР_ИНЪЕКЦИЯ = ["¿qué significa que una función sea inyectiva?",
                 "che cosa significa che una funzione è iniettiva?"]
ОПР_ИНЪЕКЦИЯ = [
    "una función es inyectiva cuando entradas distintas dan salidas "
    "distintas.",
    "una funzione è iniettiva quando ingressi diversi danno uscite "
    "diverse.",
]
ЯДРО_ИНЪЕКЦИЯ = (3, 0, 5)
ЯДРО_КОНТР_ИНЪЕКЦИЯ = ((2, 7), (3, 8), (4, 9))
ЯДРО_ОБЩ_ИНЪЕКЦИЯ = (2, 3, 5)


def исп_инъекция(шаг):
    вон = []
    ход = [(шаг * 2 + i) % 9 for i in range(5)]
    for k in случаи(ЯДРО_ИНЪЕКЦИЯ, ход):
        a, b, c = k, 2 * k, 3 * k
        да = k != 0
        вон.append(f"¿es f(x) = x × {k} inyectiva en 1, 2, 3? "
                   f"{'sí' if да else 'no'}: da {a}, {b}, {c}, "
                   f"{'todas distintas' if да else 'no todas distintas'}.")
        вон.append(f"f(x) = x × {k} è iniettiva su 1, 2, 3? "
                   f"{'sì' if да else 'no'}: dà {a}, {b}, {c}, "
                   f"{'tutte diverse' if да else 'non tutte diverse'}.")
    return вон


def контр_инъекция(шаг):
    вон = []
    ход = [(1 + (шаг * 2 + i) % 7, 8 + (шаг * 3 + i) % 7)
           for i in range(3)]
    for a, b in случаи(ЯДРО_КОНТР_ИНЪЕКЦИЯ, ход):
        вон.append(f"todas las funciones son inyectivas es falso: "
                   f"f(x) = x × 0 lleva {a} y {b} a 0.")
        вон.append(f"tutte le funzioni sono iniettive è falso: "
                   f"f(x) = x × 0 porta {a} e {b} a 0.")
    return вон


def общ_инъекция(шаг):
    вон = []
    ход = [1 + (шаг * 2 + i) % 9 for i in range(3)]
    for k in случаи(ЯДРО_ОБЩ_ИНЪЕКЦИЯ, ход):
        вон.append(f"f(x) = x × k es inyectiva exactamente cuando k no "
                   f"es 0: con k = {k} las entradas 1 y 2 dan {k} y "
                   f"{2 * k}.")
        вон.append(f"f(x) = x × k è iniettiva esattamente quando k non "
                   f"è 0: con k = {k} gli ingressi 1 e 2 danno {k} e "
                   f"{2 * k}.")
    return вон


# ----------------------------------------------------------- КВАДРАТ

ВОПР_КВАДРАТ = ["¿qué es el cuadrado de un número?",
                "che cos'è il quadrato di un numero?"]
ОПР_КВАДРАТ = [
    "el cuadrado de un número es ese número multiplicado por sí mismo.",
    "il quadrato di un numero è quel numero moltiplicato per sé stesso.",
]
ЯДРО_КВАДРАТ = (12, 15, 7)
ЯДРО_КОНТР_КВАДРАТ = (7, 9, 11)
ЯДРО_ОБЩ_КВАДРАТ = (6, 7, 10)


def исп_квадрат(шаг):
    вон = []
    ход = [2 + (шаг * 3 + i) % 24 for i in range(5)]
    for n in случаи(ЯДРО_КВАДРАТ, ход):
        вон.append(f"¿cuál es el cuadrado de {n}? {n} × {n} = "
                   f"{n * n}.")
        вон.append(f"qual è il quadrato di {n}? {n} × {n} = {n * n}.")
    return вон


def контр_квадрат(шаг):
    вон = []
    ход = [3 + ((шаг * 2 + i) % 9) * 2 for i in range(3)]
    for n in случаи(ЯДРО_КОНТР_КВАДРАТ, ход):
        вон.append(f"todos los cuadrados son pares es falso: {n} es "
                   f"impar y {n} × {n} = {n * n}, que es impar.")
        вон.append(f"tutti i quadrati sono pari è falso: {n} è dispari "
                   f"e {n} × {n} = {n * n}, che è dispari.")
    return вон


def общ_квадрат(шаг):
    вон = []
    ход = [2 + (шаг * 3 + i) % 15 for i in range(3)]
    for n in случаи(ЯДРО_ОБЩ_КВАДРАТ, ход):
        чёт = n % 2 == 0
        es = "par" if чёт else "impar"
        it = "pari" if чёт else "dispari"
        вон.append(f"el cuadrado de un número {es} es {es}: {n} × {n} "
                   f"= {n * n}.")
        вон.append(f"il quadrato di un numero {it} è {it}: {n} × {n} = "
                   f"{n * n}.")
    return вон


# -------------------------------------------------------------- РОДЫ

# РОД ОБЪЯВЛЯЕТ ЧЕТВЁРКУ И НИЧЕГО БОЛЬШЕ. Механизм лестницы ниже один
# на все роды и на оба языка: прибавить род — значит объявить четвёрку,
# прибавить ЯЗЫК — значит дописать по строке в каждую четвёрку. Ни
# нового обхода, ни нового суда механизм не требует.
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

    Шрам куплен английским слоем дознания и здесь не покупается заново:
    организм, знавший определение повествовательно, немел на прямом
    вопросе. Знание, у которого одна поверхность, не отвечает — оно
    только сообщает. Испанский вопрос при этом открывается «¿», и без
    неё вторая поверхность была бы не вопросом, а обломком.
    """
    return list(опр) + [f"{в} {о}" for в, о in zip(вопр, опр)]


def pass_groups(шаг):
    """Одна группа на РОД: ступени рода не мешаются с чужими."""
    вон = []
    for _имя, вопр, опр, исп, контр, общ in РОДЫ:
        вон.append(ступень_определения(вопр, опр)
                   + исп(шаг) + контр(шаг) + общ(шаг))
    return вон


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
