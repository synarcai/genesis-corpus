#!/usr/bin/env python3
"""СЛОЙ GENESIS: ЛЕСТНИЦА ДОЗНАНИЯ ПО-ПОЛЬСКИ И ПО-ТУРЕЦКИ.

Третья пара языков, получающая РАССУЖДЕНИЕ, а не только морфологию.
Механизм лестницы не переписан ни строкой: род объявляет четвёрку —
определение, исполнение, контрпример, обобщение, — а обход один на все
роды и на оба языка. Прибавить язык стоит по строке в каждую четвёрку.

ЧЕМ ЭТА ПАРА ДОРОЖЕ ПРЕДЫДУЩЕЙ. Испанский и итальянский ставят вопрос
ЗНАКОМ; польский ставит его СЛОВОМ («czy»), а турецкий — ОТДЕЛЬНОЙ
ЧАСТИЦЕЙ В КОНЦЕ, и частица эта СОГЛАСУЕТСЯ по гармонии гласных с
предыдущим словом. Вопрос перестаёт быть пунктуацией и становится
морфологией, и потому суд этого слоя ВЫВОДИТ частицу из слова, а не
сверяет её со списком.

ТРИ ЯЗЫКОВЫЕ ВЕЩИ, КОТОРЫЕ КОРПУС НЕ СМЕЕТ ВЫУЧИТЬ НЕВЕРНО:

  · ТУРЕЦКАЯ ВОПРОСИТЕЛЬНАЯ ЧАСТИЦА ЕСТЬ ЧЕТЫРЕ СЛОВА, А НЕ ОДНО.
    mı / mi / mu / mü выбираются последней гласной предыдущего слова:
    «sayı» кончается на ı — стало быть «mıdır»; «bölünür» на ü —
    «mü»; «bölünüyor» на o — «mu»; «çift» на i — «midir». Все четыре
    класса стоят в слое ЖИВЫМИ показами, а не примерами в
    комментарии, и суд выводит каждый заново;
  · ЧАСТИЦА ПРИ ИМЕННОМ СКАЗУЕМОМ БЕРЁТ СВЯЗКУ, ПРИ ГЛАГОЛЬНОМ НЕТ.
    «asal sayı mıdır?» (именное) против «bölünür mü?» (глагольное) —
    и связка -dır гармонирует той же гласной: mıdır, midir, mudur,
    müdür. Это два правила, а не одно, и объявлены они порознь;
  · ТУРЕЦКИЙ ПАДЕЖ НА ЦИФРЕ ПИШЕТСЯ ЧЕРЕЗ АПОСТРОФ, и окончание
    выводится из ЧТЕНИЯ числа: «8» читается «sekiz», последняя
    гласная i — переднее «e», согласный на конце — буфера нет, выходит
    «8'e». «6» читается «altı»: гласная ı — заднее «a», основа
    кончается гласной — нужен буфер «y», выходит «6'ya». Правило
    выведено из слова, объявленного пакетом, а не написано таблицей.

ПОЛЬСКИЙ СЧЁТ ПИШЕТСЯ ЦИФРОЙ, И ЭТО ОТКАЗ, А НЕ ЛЕНЬ. «Ile wynosi suma
pierwszych trzech liczb nieparzystych» требует РОДИТЕЛЬНОГО падежа
числительного («trzech», «pięciu», «jedenastu»), а пакет `pl.json`
объявляет только именительный и косвенных форм не несёт вовсе
(`numeral_oblique` пуст). Выдумать склонение за язык нельзя, и потому
по-польски счёт стоит цифрой — запись, которую польский пишет и сам.
Турецкому падежа здесь не нужно, и он говорит словом: «ilk üç tek
sayının», «ilk on bir tek sayının» — причём одиннадцать объявлено
ДВУМЯ СЛОВАМИ, и сегментатор читает объявленное многословное одним
токеном.

ЯДРО ДОСЛОВНЫХ ПОВТОРОВ. Первые три случая КАЖДОГО рода одинаковы во
всех проходах, остальные ходят числами. Рамка «вопрос — ответ»
покупается повторением одного и того же показа ДОСЛОВНО; показ, каждый
раз новый, учит роду, но не учит рамке.

ЧУЖОЙ РОД ПРОВЕРЕН НАРОЧНО. Арифметический суд корпуса знает польские
«razy» (×) и «równa» (=), турецкие «çarpı» (×) и «eder» (=), а турецкое
«on» для него ЧИСЛО ДЕСЯТЬ (и одновременно, из финского пакета, знак
равенства — значения он пробует прежде равенств, и потому здесь
выигрывает верное турецкое чтение). Записи подобраны так, чтобы тот суд
либо судил их ВЕРНО (чистая выкладка «91 = 7 × 13»), либо не судил
вовсе. Ни одна строка слоя не даёт ему (судимо, ложно) — замерено.
"""

import json
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_inquiry_pl_tr.txt"


# ------------------------------------------------------------- ЧИСЛА

def _таблица(язык):
    """Числительные языка — ИЗ ЕГО ПАКЕТА, а не из головы."""
    путь = КОРЕНЬ / "tools" / "langpacks" / f"{язык}.json"
    пакет = json.loads(путь.read_text(encoding="utf-8"))
    return пакет.get("numerals", {})


ЧИСЛА_PL = _таблица("pl")
ЧИСЛА_TR = _таблица("tr")


def по_турецки(n):
    """Число словом, если пакет его объявил; иначе цифрой.

    Одиннадцать объявлено как «on bir» — ДВА СЛОВА, и так оно и
    пишется: сегментатор читает объявленное многословное одним
    токеном, и склеивать его в «onbir» значило бы выдумать за язык
    правило, которого он не знает.
    """
    return ЧИСЛА_TR.get(str(n), str(n))


# ------------------------------------------------- ТУРЕЦКАЯ ГАРМОНИЯ

ЗАДНИЕ = "aıou"
ПЕРЕДНИЕ = "eiöü"
# ЧАСТИЦА ПО ПОСЛЕДНЕЙ ГЛАСНОЙ: четыре класса, а не два. Гармония
# турецкого делит гласные и по РЯДУ (задний/передний), и по
# ОГУБЛЁННОСТИ, и вопросительная частица различает все четыре — это та
# же четвёрка, которой живут окончания настоящего времени.
ПО_ГЛАСНОЙ = {"a": "mı", "ı": "mı", "e": "mi", "i": "mi",
              "o": "mu", "u": "mu", "ö": "mü", "ü": "mü"}
# СВЯЗКА ПРИ ИМЕННОМ СКАЗУЕМОМ ПОВТОРЯЕТ ГЛАСНУЮ ЧАСТИЦЫ.
СО_СВЯЗКОЙ = {"mı": "mıdır", "mi": "midir", "mu": "mudur",
              "mü": "müdür"}


def последняя_гласная(слово):
    """Последняя гласная слова — на ней держится вся гармония."""
    for знак in reversed(слово):
        if знак in ЗАДНИЕ or знак in ПЕРЕДНИЕ:
            return знак
    return None


def частица(слово):
    """mı / mi / mu / mü — вопросительная частица ПОСЛЕ этого слова."""
    return ПО_ГЛАСНОЙ[последняя_гласная(слово)]


def частица_связкой(слово):
    """mıdır / midir / mudur / müdür — частица при ИМЕННОМ сказуемом."""
    return СО_СВЯЗКОЙ[частица(слово)]


def дательный(n):
    """«8'e», «6'ya», «10'a» — падеж на ЦИФРЕ, через апостроф.

    ОКОНЧАНИЕ ВЫВОДИТСЯ ИЗ ЧТЕНИЯ ЧИСЛА, А НЕ ИЗ САМОЙ ЦИФРЫ. Восемь
    читается «sekiz»: последняя гласная i — переднего ряда, стало быть
    окончание «e»; слово кончается согласной, буфер не нужен — «8'e».
    Шесть читается «altı»: гласная ı заднего ряда — окончание «a»;
    слово кончается ГЛАСНОЙ, и между двумя гласными встаёт буферное
    «y» — «6'ya». Оба правила турецкие и оба выведены из слова,
    объявленного пакетом.
    """
    слово = ЧИСЛА_TR[str(n)]
    г = последняя_гласная(слово)
    окончание = "a" if г in ЗАДНИЕ else "e"
    буфер = "y" if слово[-1] in ЗАДНИЕ + ПЕРЕДНИЕ else ""
    return f"{n}'{буфер}{окончание}"


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

    Случай хода, совпавший с ядром, ВЫБРАСЫВАЕТСЯ: перемешивание есть
    перестановка, и двойник в одном проходе стал бы двумя одинаковыми
    строками. Шаг разведён с номером случая нарочно: шрам предыдущего
    слоя, где ход отступал к простым и во всех пяти проходах приходил
    ровно в ядро.
    """
    видано = list(ядро)
    return видано + [с for с in ход if с not in видано]


# ---------------------------------------------------------- ПРОСТОТА

ВОПР_ПРОСТОТА = ["co to jest liczba pierwsza?", "asal sayı nedir?"]
ОПР_ПРОСТОТА = [
    "liczba pierwsza to liczba całkowita większa od 1, która dzieli "
    "się tylko przez 1 i przez samą siebie.",
    "asal sayı, yalnızca 1'e ve kendisine bölünen, 1'den büyük tam "
    "sayıdır.",
]
ЯДРО_ПРОСТОТА = (91, 97, 51)
ЯДРО_КОНТР_ПРОСТОТА = (9, 15, 21)
ЯДРО_ОБЩ_ПРОСТОТА = (84, 90, 100)


def исп_простота(шаг):
    """Вердикт по СЧЁТУ, и основание рядом: делители либо разложение."""
    вон = []
    ход = [40 + шаг * 7 + i * 5 for i in range(5)]
    для_имени = частица_связкой("sayı")
    for n in случаи(ЯДРО_ПРОСТОТА, ход):
        if простое(n):
            вон.append(f"czy {n} jest liczbą pierwszą? tak: dzielniki "
                       f"{n} to 1 i {n}.")
            вон.append(f"{n} asal sayı {для_имени}? evet: {n} "
                       f"sayısının bölenleri yalnızca 1 ve kendisidir.")
        else:
            д = наименьший_делитель(n)
            вон.append(f"czy {n} jest liczbą pierwszą? nie: {n} = {д} "
                       f"× {n // д}.")
            вон.append(f"{n} asal sayı {для_имени}? hayır: {n} = {д} × "
                       f"{n // д}.")
    return вон


def контр_простота(шаг):
    вон = []
    ход = []
    for i in range(3):
        n = 9 + шаг * 6 + i * 4
        while простое(n):
            n += 2
        ход.append(n)
    for n in случаи(ЯДРО_КОНТР_ПРОСТОТА, ход):
        д = наименьший_делитель(n)
        вон.append(f"wszystkie liczby nieparzyste są pierwsze to "
                   f"fałsz: {n} jest nieparzyste i {n} = {д} × "
                   f"{n // д}.")
        вон.append(f"tüm tek sayılar asaldır demek yanlıştır: {n} "
                   f"tektir ve {n} = {д} × {n // д}.")
    return вон


def общ_простота(шаг):
    вон = []
    ход = [84 + шаг * 3 + i for i in range(3)]
    for n in случаи(ЯДРО_ОБЩ_ПРОСТОТА, ход):
        ряд = " × ".join(str(x) for x in разложение(n))
        вон.append(f"każda liczba całkowita większa od 1 jest "
                   f"iloczynem liczb pierwszych: {n} = {ряд}.")
        вон.append(f"1'den büyük her tam sayı asal sayıların "
                   f"çarpımıdır: {n} = {ряд}.")
    return вон


# --------------------------------------------------------- ДЕЛИМОСТЬ

ВОПР_ДЕЛИМОСТЬ = ["co znaczy, że liczba dzieli się przez inną?",
                  "bölünmek ne demektir?"]
ОПР_ДЕЛИМОСТЬ = [
    "liczba dzieli się przez inną, gdy reszta wynosi 0.",
    "kalan 0 olduğunda bir sayı başka bir sayıya bölünür.",
]
ЯДРО_ДЕЛИМОСТЬ = ((128, 8), (100, 3), (91, 7))
ЯДРО_КОНТР_ДЕЛИМОСТЬ = (6, 10, 14)
ЯДРО_ОБЩ_ДЕЛИМОСТЬ = (111, 123, 132)


def исп_делимость(шаг):
    """ДВЕ ТУРЕЦКИЕ ПОВЕРХНОСТИ НА ОДИН ФАКТ, И ЭТО НЕ ИЗЛИШЕСТВО.

    «bölünür mü?» и «bölünüyor mu?» суть один вопрос, заданный
    настоящим-широким и настоящим-длительным, — и частица при них
    РАЗНАЯ, ибо разнятся последние гласные глаголов (ü против o).
    Без второй поверхности класс «mu» не прожил бы в слое ни разу, и
    четвёрка гармонии осталась бы тройкой.
    """
    вон = []
    ход = [(100 + шаг * 11 + i * 9, 3 + (шаг + i) % 8)
           for i in range(5)]
    широкое = частица("bölünür")
    длительное = частица("bölünüyor")
    for a, b in случаи(ЯДРО_ДЕЛИМОСТЬ, ход):
        q, r = divmod(a, b)
        дат = дательный(b)
        if r == 0:
            основание = f"{a} = {b} × {q}, kalan 0"
            вон.append(f"czy {a} dzieli się przez {b}? tak: {a} = {b} "
                       f"× {q}, reszta 0.")
            вон.append(f"{a} sayısı {дат} bölünür {широкое}? evet: "
                       f"{основание}.")
            вон.append(f"{a} sayısı {дат} tam bölünüyor {длительное}? "
                       f"evet: {основание}.")
        else:
            основание = f"{a} = {b} × {q} + {r}, kalan {r}"
            вон.append(f"czy {a} dzieli się przez {b}? nie: {a} = {b} "
                       f"× {q} + {r}, reszta {r}.")
            вон.append(f"{a} sayısı {дат} bölünür {широкое}? hayır: "
                       f"{основание}.")
            вон.append(f"{a} sayısı {дат} tam bölünüyor {длительное}? "
                       f"hayır: {основание}.")
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
        вон.append(f"wszystkie liczby parzyste dzielą się przez 4 to "
                   f"fałsz: {n} jest parzyste i {n} = 4 × {q} + {r}.")
        вон.append(f"tüm çift sayılar {дательный(4)} bölünür demek "
                   f"yanlıştır: {n} çifttir ve {n} = 4 × {q} + {r}.")
    return вон


def общ_делимость(шаг):
    вон = []
    ход = [3 * (37 + шаг * 5 + i) for i in range(3)]
    for n in случаи(ЯДРО_ОБЩ_ДЕЛИМОСТЬ, ход):
        с = сумма_цифр(n)
        вон.append(f"liczba dzieli się przez 3, gdy dzieli się suma "
                   f"jej cyfr: suma cyfr {n} wynosi {с}, a {с} = 3 × "
                   f"{с // 3}.")
        вон.append(f"bir sayı, rakamları toplamı {дательный(3)} "
                   f"bölünüyorsa {дательный(3)} bölünür: {n} sayısında "
                   f"rakamlar toplamı {с} olur ve {с} = 3 × {с // 3}.")
    return вон


# ---------------------------------------------------- СУММА НЕЧЁТНЫХ

ВОПР_НЕЧЁТНЫЕ = ["co to jest liczba nieparzysta?", "tek sayı nedir?"]
ОПР_НЕЧЁТНЫЕ = [
    "liczby nieparzyste zaczynają się 1, 3, 5, 7 i każda następna jest "
    "o 2 większa od poprzedniej.",
    "tek sayılar 1, 3, 5, 7 diye başlar ve her biri bir öncekinden 2 "
    "fazladır.",
]
ЯДРО_НЕЧЁТНЫЕ = (3, 5, 4)
ЯДРО_КОНТР_НЕЧЁТНЫЕ = (3, 5, 7)
ЯДРО_ОБЩ_НЕЧЁТНЫЕ = (4, 6, 9)


def исп_нечётные(шаг):
    """ПОЛЬСКИЙ СЧЁТ ЦИФРОЙ, ТУРЕЦКИЙ — СЛОВОМ, И ПРИЧИНА НАЗВАНА.

    Польскому здесь нужен родительный числительного («pierwszych trzech
    liczb»), а пакет объявляет только именительный; выдумывать
    склонение за язык нельзя, и стоит цифра — запись, которую польский
    пишет и сам. Турецкому падежа не нужно, и он говорит словом.
    """
    вон = []
    ход = [2 + (шаг * 2 + i) % 11 for i in range(5)]
    for k in случаи(ЯДРО_НЕЧЁТНЫЕ, ход):
        ряд = " + ".join(str(2 * j + 1) for j in range(k))
        вон.append(f"ile wynosi suma pierwszych {k} liczb "
                   f"nieparzystych? {ряд} = {k * k}.")
        вон.append(f"ilk {по_турецки(k)} tek sayının toplamı kaçtır? "
                   f"{ряд} = {k * k}.")
    return вон


def контр_нечётные(шаг):
    вон = []
    ход = [3 + (шаг * 2 + i) % 9 for i in range(3)]
    for k in случаи(ЯДРО_КОНТР_НЕЧЁТНЫЕ, ход):
        вон.append(f"suma pierwszych k liczb nieparzystych wynosi "
                   f"2 × k to fałsz: dla k = {k} suma wynosi {k * k}, "
                   f"a 2 × {k} = {2 * k}.")
        вон.append(f"ilk k tek sayının toplamı 2 × k demek yanlıştır: "
                   f"k = {k} için toplam {k * k} ve 2 × {k} = "
                   f"{2 * k}.")
    return вон


def общ_нечётные(шаг):
    вон = []
    ход = [1 + (шаг * 3 + i) % 12 for i in range(3)]
    for k in случаи(ЯДРО_ОБЩ_НЕЧЁТНЫЕ, ход):
        вон.append(f"suma pierwszych k liczb nieparzystych wynosi "
                   f"k × k: dla k = {k} jest to {k} × {k} = {k * k}.")
        вон.append(f"ilk k tek sayının toplamı k × k olur: k = {k} "
                   f"için {k} × {k} = {k * k}.")
    return вон


# --------------------------------------------------- УСЛОВНЫЙ ВЫВОД

ВОПР_УСЛОВНОЕ = ["co to jest zdanie warunkowe?",
                 "koşullu önerme nedir?"]
ОПР_УСЛОВНОЕ = [
    "zdanie warunkowe jest prawdziwe, gdy wniosek zachodzi w każdym "
    "przypadku, w którym zachodzi założenie.",
    "bir koşullu önerme, öncül sağlandığı her durumda sonuç da "
    "sağlanıyorsa doğrudur.",
]
ЯДРО_УСЛОВНОЕ = ((4, 6), (3, 8), (2, 10))
ЯДРО_КОНТР_УСЛОВНОЕ = ((3, 6), (5, 8), (7, 10))
ЯДРО_ОБЩ_УСЛОВНОЕ = ((2, 8), (4, 10), (6, 12))


def исп_условное(шаг):
    вон = []
    ход = [(1 + (шаг * 2 + i) % 9, 4 + ((шаг * 3 + i) % 8) * 2)
           for i in range(5)]
    для_чёта = частица_связкой("çift")
    for m, e in случаи(ЯДРО_УСЛОВНОЕ, ход):
        s = e + m
        да = m % 2 == 0
        вон.append(f"jeśli n jest parzyste, czy n + {m} jest "
                   f"parzyste? {'tak' if да else 'nie'}: {e} jest "
                   f"parzyste i {e} + {m} = {s}, co jest "
                   f"{'parzyste' if s % 2 == 0 else 'nieparzyste'}.")
        вон.append(f"n çift ise n + {m} çift {для_чёта}? "
                   f"{'evet' if да else 'hayır'}: {e} çifttir ve {e} + "
                   f"{m} = {s}, bu da "
                   f"{'çifttir' if s % 2 == 0 else 'tektir'}.")
    return вон


def контр_условное(шаг):
    вон = []
    ход = [(1 + ((шаг * 2 + i) % 5) * 2, 6 + ((шаг * 3 + i) % 7) * 2)
           for i in range(3)]
    for m, e in случаи(ЯДРО_КОНТР_УСЛОВНОЕ, ход):
        s = e + m
        вон.append(f"jeśli n jest parzyste, to n + {m} jest parzyste "
                   f"to fałsz: {e} jest parzyste i {e} + {m} = {s}, co "
                   f"jest nieparzyste.")
        вон.append(f"n çift ise n + {m} çifttir demek yanlıştır: {e} "
                   f"çifttir ve {e} + {m} = {s}, bu da tektir.")
    return вон


def общ_условное(шаг):
    вон = []
    ход = [(2 + ((шаг * 2 + i) % 6) * 2, 8 + ((шаг * 3 + i) % 5) * 2)
           for i in range(3)]
    for m, e in случаи(ЯДРО_ОБЩ_УСЛОВНОЕ, ход):
        s = e + m
        вон.append(f"jeśli n jest parzyste, to n + m jest parzyste "
                   f"dokładnie wtedy, gdy m jest parzyste: {m} jest "
                   f"parzyste i {e} + {m} = {s}, co jest parzyste.")
        вон.append(f"n çift ise n + m çifttir ancak ve ancak m "
                   f"çifttir: {m} çifttir ve {e} + {m} = {s}, bu da "
                   f"çifttir.")
    return вон


# ---------------------------------------------------- ИНЪЕКТИВНОСТЬ

ВОПР_ИНЪЕКЦИЯ = ["co znaczy, że funkcja jest różnowartościowa?",
                 "bir fonksiyonun birebir olması ne demektir?"]
ОПР_ИНЪЕКЦИЯ = [
    "funkcja jest różnowartościowa, gdy różne argumenty dają różne "
    "wartości.",
    "bir fonksiyon, farklı girdiler farklı çıktılar veriyorsa "
    "birebirdir.",
]
ЯДРО_ИНЪЕКЦИЯ = (3, 0, 5)
ЯДРО_КОНТР_ИНЪЕКЦИЯ = ((2, 7), (3, 8), (4, 9))
ЯДРО_ОБЩ_ИНЪЕКЦИЯ = (2, 3, 5)


def исп_инъекция(шаг):
    вон = []
    ход = [(шаг * 2 + i) % 9 for i in range(5)]
    для_имени = частица_связкой("birebir")
    for k in случаи(ЯДРО_ИНЪЕКЦИЯ, ход):
        a, b, c = k, 2 * k, 3 * k
        да = k != 0
        вон.append(f"czy f(x) = x × {k} jest różnowartościowa na "
                   f"1, 2, 3? {'tak' if да else 'nie'}: daje {a}, {b}, "
                   f"{c}, "
                   f"{'wszystkie różne' if да else 'nie wszystkie różne'}.")
        вон.append(f"f(x) = x × {k} birebir {для_имени}? "
                   f"{'evet' if да else 'hayır'}: {a}, {b}, {c} verir, "
                   f"{'hepsi farklıdır' if да else 'hepsi farklı değildir'}.")
    return вон


def контр_инъекция(шаг):
    вон = []
    ход = [(1 + (шаг * 2 + i) % 7, 8 + (шаг * 3 + i) % 7)
           for i in range(3)]
    for a, b in случаи(ЯДРО_КОНТР_ИНЪЕКЦИЯ, ход):
        вон.append(f"wszystkie funkcje są różnowartościowe to fałsz: "
                   f"f(x) = x × 0 prowadzi {a} i {b} do 0.")
        вон.append(f"tüm fonksiyonlar birebirdir demek yanlıştır: "
                   f"f(x) = x × 0 hem {a} hem {b} sayısını 0 yapar.")
    return вон


def общ_инъекция(шаг):
    вон = []
    ход = [1 + (шаг * 2 + i) % 9 for i in range(3)]
    for k in случаи(ЯДРО_ОБЩ_ИНЪЕКЦИЯ, ход):
        вон.append(f"f(x) = x × k jest różnowartościowa dokładnie "
                   f"wtedy, gdy k nie jest 0: dla k = {k} argumenty "
                   f"1 i 2 dają {k} i {2 * k}.")
        вон.append(f"f(x) = x × k birebirdir ancak ve ancak k 0 "
                   f"değildir: k = {k} için 1 ve 2 girdileri {k} ve "
                   f"{2 * k} verir.")
    return вон


# ----------------------------------------------------------- КВАДРАТ

ВОПР_КВАДРАТ = ["co to jest kwadrat liczby?", "bir sayının karesi nedir?"]
ОПР_КВАДРАТ = [
    "kwadrat liczby to ta liczba pomnożona przez samą siebie.",
    "bir sayının karesi, o sayının kendisiyle çarpımıdır.",
]
ЯДРО_КВАДРАТ = (12, 15, 7)
ЯДРО_КОНТР_КВАДРАТ = (7, 9, 11)
ЯДРО_ОБЩ_КВАДРАТ = (6, 7, 10)


def исп_квадрат(шаг):
    вон = []
    ход = [2 + (шаг * 3 + i) % 24 for i in range(5)]
    for n in случаи(ЯДРО_КВАДРАТ, ход):
        вон.append(f"ile wynosi kwadrat liczby {n}? {n} × {n} = "
                   f"{n * n}.")
        вон.append(f"{n} sayısının karesi kaçtır? {n} × {n} = {n * n}.")
    return вон


def контр_квадрат(шаг):
    вон = []
    ход = [3 + ((шаг * 2 + i) % 9) * 2 for i in range(3)]
    for n in случаи(ЯДРО_КОНТР_КВАДРАТ, ход):
        вон.append(f"wszystkie kwadraty są parzyste to fałsz: {n} jest "
                   f"nieparzyste i {n} × {n} = {n * n}, co jest "
                   f"nieparzyste.")
        вон.append(f"tüm kareler çifttir demek yanlıştır: {n} tektir "
                   f"ve {n} × {n} = {n * n}, bu da tektir.")
    return вон


def общ_квадрат(шаг):
    вон = []
    ход = [2 + (шаг * 3 + i) % 15 for i in range(3)]
    for n in случаи(ЯДРО_ОБЩ_КВАДРАТ, ход):
        чёт = n % 2 == 0
        pl_род = "parzystej" if чёт else "nieparzystej"
        pl_сказ = "parzysty" if чёт else "nieparzysty"
        tr = "çift" if чёт else "tek"
        вон.append(f"kwadrat liczby {pl_род} jest {pl_сказ}: {n} × {n} "
                   f"= {n * n}.")
        вон.append(f"{tr} sayının karesi {tr}tir: {n} × {n} = {n * n}.")
    return вон


# -------------------------------------------------------------- РОДЫ

# РОД ОБЪЯВЛЯЕТ ЧЕТВЁРКУ И НИЧЕГО БОЛЬШЕ.
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

    Польский вопрос открывается словом «czy» либо вопросительным
    оборотом («co to jest»), турецкий — вопросительным словом в конце
    («nedir», «ne demektir»). Ни один из двух не есть пунктуация, и
    потому вторая поверхность здесь стоит дороже, чем в языках, где
    вопрос виден одним знаком.
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
