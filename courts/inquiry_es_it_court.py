#!/usr/bin/env python3
"""СУД ЛЕСТНИЦЫ ДОЗНАНИЯ НА ИСПАНСКОМ И ИТАЛЬЯНСКОМ.

Слой говорит четырьмя ступенями на двух языках, и три ступени из
четырёх несут ОСНОВАНИЕ рядом с ответом: «no: 91 = 7 × 13», «è falso:
nove è dispari e 9 = 3 × 3». Суд не верит ни ответу, ни основанию: он
раскладывает число заново, делит заново, складывает ряд заново и
сверяет ТРИ вещи разом — что основание верно, что ответ ему
соответствует и что ответ верен по существу.

ЯЗЫК СУДИТСЯ НАРАВНЕ СО СЧЁТОМ, И ЭТО ЗДЕСЬ ГЛАВНОЕ НОВОЕ. Английский
суд дознания проверял только числа: у английского нет ни перевёрнутого
знака, ни ударения, различающего два слова. Здесь три языковые вещи
входят в вердикт наравне с арифметикой:

  · ПЕРЕВЁРНУТЫЙ ЗНАК стоит в образце. Испанский вопрос без «¿» не
    узнаётся вовсе и остаётся НЕСУДИМЫМ, а ворота записи несудимую
    строку не пропускают. Корпус не может родиться с обломком вопроса;
  · «SÍ» И «SI» РАЗЛИЧАЮТСЯ ОБРАЗЦОМ. Вердикт читается только из
    «sí»/«no» (испанский) и «sì»/«no» (итальянский); «si» без ударения
    в этой клетке образцу не подходит, и показ становится несудимым.
    То же для итальянского «sì»;
  · ЧИСЛИТЕЛЬНОЕ СЛОВОМ ПЕРЕСЧИТЫВАЕТСЯ ПО ПАКЕТУ ЯЗЫКА. «treinta y
    cinco» верно не потому, что так написал генератор, а потому, что
    таблица `es.json` объявляет «treinta» и «cinco», а сам пакет
    объявляет связку «y». Правило сборки написано здесь ВТОРОЙ РУКОЙ;
    таблица одна и та же нарочно — двух списков числительных у одного
    языка быть не должно, иначе корпус разойдётся с пакетом молча.

ОСОБО О КОНТРПРИМЕРЕ. Свидетель, который НЕ опровергает, звучит
убедительнее всего, ибо форма у него правильная. Потому проверяется не
форма, а работа: названный свидетель обязан УДОВЛЕТВОРЯТЬ посылке
всеобщего утверждения и НАРУШАТЬ его следствие. «nove è dispari e
9 = 3 × 3» убивает «все нечётные просты» лишь если девять и вправду
нечётно, и вправду не просто, и трижды три вправду девять.

ОБ ОПРЕДЕЛЕНИЯХ. Их суд — сверка с независимо записанным здесь
списком, и держится ПАРА «вопрос — ответ», а не два списка: ответ на
чужой вопрос («¿qué es un número primo? un condicional es verdadero…»)
состоит из двух объявленных кусков и обязан быть отвергнут.

СУД НЕ СМЕЕТ ЧИТАТЬ ЧУЖОЙ РОД. Образцы узкие и привязаны к зачину;
неузнанная строка есть (False, False) — молчание, а не вердикт.
"""

import json
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "scripts"))
sys.path.insert(0, str(КОРЕНЬ / "tools"))
from genesis import Unreadable, worlds  # noqa: E402
import universals  # noqa: E402
import paraphrase  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file


def _пакет(язык):
    """Числительные и связка языка — ИЗ ЕГО ПАКЕТА.

    Единственное место, где суд НЕ пишет второй рукой, и это нарочно:
    числительные суть объявление ЯЗЫКА о себе, а не утверждение слоя.
    Второй список, набранный здесь, разошёлся бы с пакетом молча — и
    суд стал бы судить корпус по своей памяти вместо языка. Правило
    СБОРКИ составного написано здесь отдельно, и вот оно-то и есть
    вторая рука.
    """
    путь = КОРЕНЬ / "tools" / "langpacks" / f"{язык}.json"
    try:
        пакет = json.loads(путь.read_text(encoding="utf-8"))
    except (OSError, ValueError) as беда:
        print(f"ДОЗНАНИЕ-ES-IT ОТКАЗ: {путь.name}: {беда}")
        sys.exit(2)
    связки = пакет.get("numeral_connectors") or []
    return пакет.get("numerals", {}), (связки[0] if связки else None)


ЧИСЛА_ES, СВЯЗКА_ES = _пакет("es")
ЧИСЛА_IT, СВЯЗКА_IT = _пакет("it")


def числом(слово, таблица, связка):
    """Значение написанного числительного, или None — слово не читается.

    ОБРАТНЫЙ ХОД, А НЕ ПОВТОР ПРЯМОГО. Слой идёт от числа к слову; суд
    идёт от СЛОВА к числу и лишь потом сверяет. Составное разбирается
    по объявленной связке: «treinta y cinco» есть десяток плюс единица,
    и обе части обязаны стоять в таблице языка. Языку без объявленной
    связки составное не читается вовсе — и не должно: итальянское
    составное сливается с выпадением гласной, и разбирать его связкой
    значило бы выдумать за язык правило, которого у него нет.
    """
    обратно = {з: int(к) for к, з in таблица.items()}
    if слово in обратно:
        return обратно[слово]
    if слово.isdigit():
        return int(слово)
    if связка:
        куски = слово.split(f" {связка} ")
        if len(куски) == 2:
            д, е = обратно.get(куски[0]), обратно.get(куски[1])
            if (д is not None and е is not None
                    and 30 <= д <= 90 and д % 10 == 0 and 1 <= е <= 9):
                return д + е
    return None


def по_испански(слово):
    return числом(слово, ЧИСЛА_ES, СВЯЗКА_ES)


def по_итальянски(слово):
    """Итальянское числительное — ТОЛЬКО объявленное либо цифрой.

    Связки итальянский пакет не объявляет, и суд её не выдумывает:
    «21» здесь есть законная запись, а «ventuno» — слово, которого
    пакет не сказал, и потому суд его не признаёт. Граница честная:
    слой такого слова и не пишет.
    """
    return числом(слово, ЧИСЛА_IT, None)


# ------------------------------------------------------------- СЧЁТ

def делители(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def простое(n):
    return n > 1 and делители(n) == [1, n]


def сумма_цифр(n):
    return sum(int(ц) for ц in str(n))


# ВОПРОС И ЕГО ОТВЕТ СВЯЗАНЫ РОДОМ, А НЕ СОСЕДСТВОМ. Пары записаны
# здесь ВТОРОЙ РУКОЙ — тот же факт, сказанный отдельно от генератора;
# правка в одном доме и не в другом делает строку НЕСУДИМОЙ, а ворота
# записи несудимую строку не пропускают. Держится именно ПАРА.
РОДЫ = (
    (("¿qué es un número primo?", "che cos'è un numero primo?"),
     ("un número primo es un número entero mayor que 1 divisible solo "
      "por 1 y por sí mismo.",
      "un numero primo è un numero intero maggiore di 1 divisibile "
      "solo per 1 e per sé stesso.")),
    (("¿qué significa divisible?", "che cosa significa divisibile?"),
     ("un número es divisible por otro cuando el resto es 0.",
      "un numero è divisibile per un altro quando il resto è 0.")),
    (("¿qué es un número impar?", "che cos'è un numero dispari?"),
     ("los números impares empiezan 1, 3, 5, 7 y cada uno supera al "
      "anterior en 2.",
      "i numeri dispari cominciano 1, 3, 5, 7 e ognuno supera il "
      "precedente di 2.")),
    (("¿qué es un enunciado condicional?",
      "che cos'è un enunciato condizionale?"),
     ("un condicional es verdadero cuando la conclusión se cumple en "
      "todos los casos en que se cumple la premisa.",
      "un condizionale è vero quando la conclusione vale in tutti i "
      "casi in cui vale la premessa.")),
    (("¿qué significa que una función sea inyectiva?",
      "che cosa significa che una funzione è iniettiva?"),
     ("una función es inyectiva cuando entradas distintas dan salidas "
      "distintas.",
      "una funzione è iniettiva quando ingressi diversi danno uscite "
      "diverse.")),
    (("¿qué es el cuadrado de un número?",
      "che cos'è il quadrato di un numero?"),
     ("el cuadrado de un número es ese número multiplicado por sí "
      "mismo.",
      "il quadrato di un numero è quel numero moltiplicato per sé "
      "stesso.")),
)
ОПРЕДЕЛЕНИЯ = frozenset(о for _в, опр in РОДЫ for о in опр)
ОТВЕТЫ = frozenset(f"{в} {о}" for вопр, опр in РОДЫ
                   for в, о in zip(вопр, опр))


# ------------------------------------------------------------ ПРОВЕРКИ

def _простое_да(м):
    n, n2, n3 = (int(з) for з in м.groups())
    return простое(n) and n2 == n and n3 == n


def _простое_нет(м):
    n, n2, a, b = (int(з) for з in м.groups())
    return not простое(n) and n2 == n and a * b == n and a > 1 and b > 1


def _контр_простое(м, читать):
    """Свидетель обязан быть нечётным, составным — и НАЗВАННЫМ ВЕРНО.

    Три утверждения в одной строке, и все три проверяются: число
    нечётно (посылка всеобщего), число не просто (следствие нарушено),
    произведение сходится — и вдобавок ЧЕТВЁРТОЕ, языковое: слово,
    которым свидетель назван, читается пакетом языка в то же самое
    число. «treinta y seis es impar y 35 = 5 × 7» есть ложь по языку
    при верной арифметике.
    """
    слово, n, a, b = м.group(1), *(int(з) for з in м.groups()[1:])
    сказано = читать(слово)
    return (сказано == n and n % 2 == 1 and not простое(n)
            and a * b == n and a > 1 and b > 1)


def _контр_простое_es(м):
    return _контр_простое(м, по_испански)


def _контр_простое_it(м):
    return _контр_простое(м, по_итальянски)


def _произведение(м):
    n = int(м.group(1))
    множители = [int(x) for x in re.findall(r"\d+", м.group(2))]
    ц = 1
    for x in множители:
        ц *= x
    return n > 1 and ц == n and all(простое(x) for x in множители)


def _делится_да(м):
    a, b, a2, b2, q = (int(з) for з in м.groups())
    return a % b == 0 and a2 == a and b2 == b and b * q == a


def _делится_нет(м):
    a, b, a2, b2, q, r, r2 = (int(з) for з in м.groups())
    return (a % b != 0 and a2 == a and b2 == b and b * q + r == a
            and r == a % b and r2 == r and r > 0)


def _контр_делимость(м):
    n, n2, q, r = (int(з) for з in м.groups())
    # ЧЕТВЁРКА В ЗАПИСИ ЕСТЬ БУКВА ЗАКОНА, А НЕ ВЕЛИЧИНА РЯДА, и потому
    # в образце она стоит литералом, а не скобкой.
    return (n % 2 == 0 and n % 4 != 0 and n2 == n
            and 4 * q + r == n and r > 0)


def _цифры_на_три(м):
    n, с, с2, q = (int(з) for з in м.groups())
    return (n % 3 == 0 and сумма_цифр(n) == с and с2 == с
            and 3 * q == с)


def _сумма_нечётных(м, читать):
    """Счёт слагаемых ВЫВОДИТСЯ ИЗ РЯДА, а слово сверяется с ним.

    Порядок важен: суд, взявший счёт из СЛОВА и проверивший им же ряд,
    проверял бы слово словом. Здесь счёт есть длина ряда, ряд обязан
    быть первыми нечётными, сумма обязана сойтись — и лишь потом слово
    обязано называть эту длину.
    """
    слово, ряд, итог = м.group(1), м.group(2), int(м.group(3))
    числа = [int(x) for x in re.findall(r"\d+", ряд)]
    k = len(числа)
    return (числа == [2 * j + 1 for j in range(k)]
            and sum(числа) == итог == k * k and читать(слово) == k)


def _сумма_es(м):
    return _сумма_нечётных(м, по_испански)


def _сумма_it(м):
    return _сумма_нечётных(м, по_итальянски)


def _контр_сумма(м):
    k, сумма, k2, двак = (int(з) for з in м.groups())
    return (сумма == k * k and k2 == k and двак == 2 * k
            and k * k != 2 * k)


def _общ_сумма(м):
    k, k2, k3, итог = (int(з) for з in м.groups())
    return k2 == k3 == k and итог == k * k


def _условное(м, да_слово, чёт_слово):
    """Вердикт по ЧЁТНОСТИ ПРИБАВКИ, а основание — по счёту.

    «Si n es par» есть посылка, «¿es n + m par?» — следствие, и ответ
    зависит только от чётности m. Свидетель обязан быть чётным (иначе
    посылка не выполнена), сумма обязана сойтись, а названная чётность
    суммы — соответствовать ей.
    """
    m_, ответ, e, e2, m2, s, чёт = м.groups()
    m_, e, e2, m2, s = int(m_), int(e), int(e2), int(m2), int(s)
    да = ответ == да_слово
    чётно = чёт == чёт_слово
    return (e % 2 == 0 and e2 == e and m2 == m_ and e + m_ == s
            and чётно == (s % 2 == 0) and да == (m_ % 2 == 0))


def _условное_es(м):
    return _условное(м, "sí", "par")


def _условное_it(м):
    return _условное(м, "sì", "pari")


def _контр_условное(м):
    m_, e, e2, m2, s = (int(з) for з in м.groups())
    return (m_ % 2 == 1 and e % 2 == 0 and e2 == e and m2 == m_
            and e + m_ == s and s % 2 == 1)


def _общ_условное(м):
    m_, e, m2, s = (int(з) for з in м.groups())
    return (m_ % 2 == 0 and e % 2 == 0 and m2 == m_
            and e + m_ == s and s % 2 == 0)


def _инъекция(м, да_слово, разные_слово):
    k, ответ, a, b, c, разные = м.groups()
    k, a, b, c = int(k), int(a), int(b), int(c)
    да = ответ == да_слово
    все_разные = разные == разные_слово
    return (a == k and b == 2 * k and c == 3 * k
            and все_разные == (len({a, b, c}) == 3)
            and да == (k != 0) and все_разные == да)


def _инъекция_es(м):
    return _инъекция(м, "sí", "todas distintas")


def _инъекция_it(м):
    return _инъекция(м, "sì", "tutte diverse")


def _контр_инъекция(м):
    a, b = (int(з) for з in м.groups())
    return a != b


def _общ_инъекция(м):
    k, k2, двак = (int(з) for з in м.groups())
    return k != 0 and k2 == k and двак == 2 * k


def _квадрат(м):
    n, n2, n3, кв = (int(з) for з in м.groups())
    return n2 == n3 == n and кв == n * n


def _контр_квадрат(м):
    n, n2, n3, кв = (int(з) for з in м.groups())
    return n % 2 == 1 and n2 == n3 == n and кв == n * n and кв % 2 == 1


def _общ_квадрат(м, чёт_слово):
    """Прилагательное сказано ДВАЖДЫ и обязано совпасть с собою и с n.

    Испанский и итальянский не меняют здесь формы между подлежащим и
    сказуемым («un número par es par»), и потому оба слова обязаны быть
    одним и тем же — а оно обязано отвечать чётности числа и чётности
    квадрата.
    """
    чёт, сказ, n, n2, кв = м.groups()
    n, n2, кв = int(n), int(n2), int(кв)
    это_чёт = чёт == чёт_слово
    return (чёт == сказ and n2 == n and кв == n * n
            and это_чёт == (n % 2 == 0)
            and (кв % 2 == 0) == это_чёт)


def _общ_квадрат_es(м):
    return _общ_квадрат(м, "par")


def _общ_квадрат_it(м):
    return _общ_квадрат(м, "pari")


# ------------------------------------------------------------- ОБРАЗЦЫ

Ч = r"(\d+)"
С = r"(.+?)"
ОБРАЗЦЫ = (
    (rf"^¿es {Ч} un número primo\? sí: los divisores de {Ч} son 1 y "
     rf"{Ч}\.$", _простое_да),
    (rf"^{Ч} è un numero primo\? sì: i divisori di {Ч} sono 1 e {Ч}\.$",
     _простое_да),
    (rf"^¿es {Ч} un número primo\? no: {Ч} = {Ч} × {Ч}\.$",
     _простое_нет),
    (rf"^{Ч} è un numero primo\? no: {Ч} = {Ч} × {Ч}\.$", _простое_нет),
    (rf"^todos los números impares son primos es falso: {С} es impar y "
     rf"{Ч} = {Ч} × {Ч}\.$", _контр_простое_es),
    (rf"^tutti i numeri dispari sono primi è falso: {С} è dispari e "
     rf"{Ч} = {Ч} × {Ч}\.$", _контр_простое_it),
    (rf"^todo número entero mayor que 1 es un producto de primos: {Ч} "
     r"= ([\d ×]+)\.$", _произведение),
    (rf"^ogni numero intero maggiore di 1 è un prodotto di primi: {Ч} "
     r"= ([\d ×]+)\.$", _произведение),
    (rf"^¿es {Ч} divisible por {Ч}\? sí: {Ч} = {Ч} × {Ч}, resto 0\.$",
     _делится_да),
    (rf"^{Ч} è divisibile per {Ч}\? sì: {Ч} = {Ч} × {Ч}, resto 0\.$",
     _делится_да),
    (rf"^¿es {Ч} divisible por {Ч}\? no: {Ч} = {Ч} × {Ч} \+ {Ч}, resto "
     rf"{Ч}\.$", _делится_нет),
    (rf"^{Ч} è divisibile per {Ч}\? no: {Ч} = {Ч} × {Ч} \+ {Ч}, resto "
     rf"{Ч}\.$", _делится_нет),
    (rf"^todos los números pares son divisibles por 4 es falso: {Ч} es "
     rf"par y {Ч} = 4 × {Ч} \+ {Ч}\.$", _контр_делимость),
    (rf"^tutti i numeri pari sono divisibili per 4 è falso: {Ч} è pari "
     rf"e {Ч} = 4 × {Ч} \+ {Ч}\.$", _контр_делимость),
    (rf"^un número es divisible por 3 cuando lo es la suma de sus "
     rf"cifras: la suma de las cifras de {Ч} es {Ч}, y {Ч} = 3 × "
     rf"{Ч}\.$", _цифры_на_три),
    (rf"^un numero è divisibile per 3 quando lo è la somma delle sue "
     rf"cifre: la somma delle cifre di {Ч} è {Ч}, e {Ч} = 3 × {Ч}\.$",
     _цифры_на_три),
    (rf"^¿cuánto suman los primeros {С} números impares\? ([\d +]+) = "
     rf"{Ч}\.$", _сумма_es),
    (rf"^quanto fanno i primi {С} numeri dispari\? ([\d +]+) = {Ч}\.$",
     _сумма_it),
    (rf"^la suma de los primeros k números impares es 2 × k es falso: "
     rf"con k = {Ч} la suma es {Ч} y 2 × {Ч} = {Ч}\.$", _контр_сумма),
    (rf"^la somma dei primi k numeri dispari è 2 × k è falso: con "
     rf"k = {Ч} la somma è {Ч} e 2 × {Ч} = {Ч}\.$", _контр_сумма),
    (rf"^la suma de los primeros k números impares es k × k: con "
     rf"k = {Ч} es {Ч} × {Ч} = {Ч}\.$", _общ_сумма),
    (rf"^la somma dei primi k numeri dispari è k × k: con k = {Ч} è "
     rf"{Ч} × {Ч} = {Ч}\.$", _общ_сумма),
    (rf"^si n es par, ¿es n \+ {Ч} par\? (sí|no): {Ч} es par y {Ч} \+ "
     rf"{Ч} = {Ч}, que es (par|impar)\.$", _условное_es),
    (rf"^se n è pari, n \+ {Ч} è pari\? (sì|no): {Ч} è pari e {Ч} \+ "
     rf"{Ч} = {Ч}, che è (pari|dispari)\.$", _условное_it),
    (rf"^si n es par entonces n \+ {Ч} es par es falso: {Ч} es par y "
     rf"{Ч} \+ {Ч} = {Ч}, que es impar\.$", _контр_условное),
    (rf"^se n è pari allora n \+ {Ч} è pari è falso: {Ч} è pari e {Ч} "
     rf"\+ {Ч} = {Ч}, che è dispari\.$", _контр_условное),
    (rf"^si n es par entonces n \+ m es par exactamente cuando m es "
     rf"par: {Ч} es par y {Ч} \+ {Ч} = {Ч}, que es par\.$",
     _общ_условное),
    (rf"^se n è pari allora n \+ m è pari esattamente quando m è pari: "
     rf"{Ч} è pari e {Ч} \+ {Ч} = {Ч}, che è pari\.$", _общ_условное),
    (rf"^¿es f\(x\) = x × {Ч} inyectiva en 1, 2, 3\? (sí|no): da {Ч}, "
     rf"{Ч}, {Ч}, (todas distintas|no todas distintas)\.$",
     _инъекция_es),
    (rf"^f\(x\) = x × {Ч} è iniettiva su 1, 2, 3\? (sì|no): dà {Ч}, "
     rf"{Ч}, {Ч}, (tutte diverse|non tutte diverse)\.$", _инъекция_it),
    (rf"^todas las funciones son inyectivas es falso: f\(x\) = x × 0 "
     rf"lleva {Ч} y {Ч} a 0\.$", _контр_инъекция),
    (rf"^tutte le funzioni sono iniettive è falso: f\(x\) = x × 0 "
     rf"porta {Ч} e {Ч} a 0\.$", _контр_инъекция),
    (rf"^f\(x\) = x × k es inyectiva exactamente cuando k no es 0: con "
     rf"k = {Ч} las entradas 1 y 2 dan {Ч} y {Ч}\.$", _общ_инъекция),
    (rf"^f\(x\) = x × k è iniettiva esattamente quando k non è 0: con "
     rf"k = {Ч} gli ingressi 1 e 2 danno {Ч} e {Ч}\.$", _общ_инъекция),
    (rf"^¿cuál es el cuadrado de {Ч}\? {Ч} × {Ч} = {Ч}\.$", _квадрат),
    (rf"^qual è il quadrato di {Ч}\? {Ч} × {Ч} = {Ч}\.$", _квадрат),
    (rf"^todos los cuadrados son pares es falso: {Ч} es impar y {Ч} × "
     rf"{Ч} = {Ч}, que es impar\.$", _контр_квадрат),
    (rf"^tutti i quadrati sono pari è falso: {Ч} è dispari e {Ч} × {Ч} "
     rf"= {Ч}, che è dispari\.$", _контр_квадрат),
    (r"^el cuadrado de un número (par|impar) es (par|impar): "
     rf"{Ч} × {Ч} = {Ч}\.$", _общ_квадрат_es),
    (r"^il quadrato di un numero (pari|dispari) è (pari|dispari): "
     rf"{Ч} × {Ч} = {Ч}\.$", _общ_квадрат_it),
)
# УНИВЕРСАЛИЯ СПРАШИВАЕТСЯ СВОИМ «ВЕРНО ЛИ, ЧТО» (tools/universals.py): образец
# контрпримера или обобщения сварен с выведенным из него вопросом в ОДНО
# семейство (М-146); остальные образцы — как есть.
ЯЗЫКИ_МИРА = ('es', 'it')
# ПЕРЕФРАЗА — ФОРМА ПАКЕТА (tools/paraphrase.py, Т-4): образцы других форм
# простоты и делимости выведены из образцов первой формы с теми же судьями.
ПРАВИЛА = universals.правила(list(ОБРАЗЦЫ) + paraphrase.образцы(ОБРАЗЦЫ, ЯЗЫКИ_МИРА, ("prime", "divisible")), ЯЗЫКИ_МИРА)


def судить(строка):
    """(судимо, истинно) для одной строки."""
    с = строка.strip()
    if not с:
        return False, False
    if с in ОПРЕДЕЛЕНИЯ or с in ОТВЕТЫ:
        return True, True
    for образец, проверить in ПРАВИЛА:
        м = образец.match(с)
        if м:
            return True, bool(проверить(м))
    return False, False


def обход(явные):
    if явные:
        return [pathlib.Path(п) for п in явные]
    try:
        return worlds(kind="shows")
    except Unreadable as беда:
        print(f"ДОЗНАНИЕ-ES-IT ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("ДОЗНАНИЕ-ES-IT ОТКАЗ: обход пуст, судить нечего")
        return 2
    ложных = судимых = 0
    примеры = []
    for путь in пути:
        свои = 0
        with путь.open(encoding="utf-8", errors="replace") as поток:
            for строка in поток:
                судимо, истинно = судить(строка)
                if not судимо:
                    continue
                судимых += 1
                if not истинно:
                    ложных += 1
                    свои += 1
                    if len(примеры) < 4:
                        примеры.append(f"{путь.name}: {строка.strip()[:80]}")
        if свои:
            print(f"  {путь.name:<30} ложных {свои}")
    for п in примеры:
        print(f"    {п}")
    поза = "ЛЕНТА" if явные else (
        "PASS" if ложных <= ЛОЖНЫХ_РУБЕЖ else "FAIL")
    print(f"ДОЗНАНИЕ-ES-IT {поза}: {ложных} ложных из {судимых} судимых "
          f"({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
