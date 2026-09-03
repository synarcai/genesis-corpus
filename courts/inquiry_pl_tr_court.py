#!/usr/bin/env python3
"""СУД ЛЕСТНИЦЫ ДОЗНАНИЯ НА ПОЛЬСКОМ И ТУРЕЦКОМ.

Слой говорит четырьмя ступенями на двух языках, и три ступени из
четырёх несут ОСНОВАНИЕ рядом с ответом. Суд не верит ни ответу, ни
основанию: он раскладывает число заново, делит заново, складывает ряд
заново и сверяет ТРИ вещи разом — что основание верно, что ответ ему
соответствует и что ответ верен по существу.

ЧЕТВЁРТАЯ ВЕЩЬ, КОТОРОЙ ЗДЕСЬ НЕ БЫЛО РАНЬШЕ: ЯЗЫК ВЫВОДИТСЯ, А НЕ
СВЕРЯЕТСЯ СО СПИСКОМ. Испанский вопрос узнавался знаком «¿» — знак
можно было поставить в образец и забыть. Турецкий вопрос есть
МОРФОЛОГИЯ: частица mı / mi / mu / mü выбирается последней гласной
ПРЕДЫДУЩЕГО СЛОВА, и суд эту гласную ищет и частицу ВЫВОДИТ. Показ
«asal sayı midir?» отвергается не потому, что «midir» нет в списке, а
потому, что «sayı» кончается на «ı» и требует «mıdır».

ТРИ ТУРЕЦКИХ ПРАВИЛА, ВЫВОДИМЫЕ ЗДЕСЬ ВТОРОЙ РУКОЙ:

  · ЧАСТИЦА ПО ПОСЛЕДНЕЙ ГЛАСНОЙ — четыре класса, а не два;
  · СВЯЗКА ПРИ ИМЕННОМ СКАЗУЕМОМ повторяет гласную частицы (mıdır,
    midir, mudur, müdür), при глагольном её нет вовсе (mı, mi, mu, mü);
  · ПАДЕЖ НА ЦИФРЕ выводится из ЧТЕНИЯ числа: «8» есть «sekiz» —
    последняя гласная переднего ряда, окончание «e», согласный на
    конце, буфера нет: «8'e». «6» есть «altı» — гласная заднего ряда,
    окончание «a», основа кончается гласной, встаёт буферное «y»:
    «6'ya». Слово берётся из пакета языка, правило написано здесь.

ЧТО ПРО АПОСТРОФ СТОИТ ЗНАТЬ ЧИТАЮЩЕМУ ЭТОТ СУД. Общий сегментатор
корпуса режет «8'e» на «8» и «e» — апостроф ему граница слова, а не
буква (внутрисловным он считает лишь то, что стоит МЕЖДУ ДВУМЯ
БУКВАМИ, а слева здесь цифра). Этому суду это безразлично: он читает
строку образцом целиком и апострофа не рвёт. Но арифметическому суду
корпуса «e» после цифры достаётся как ОБЪЯВЛЕННАЯ СВЯЗКА ЧИСЛИТЕЛЬНЫХ
(её объявил португальский пакет для «noventa E nove»), и турецкий
дательный читается им как «число, связка». Лжи из этого не выходит —
замерено, — но знать об этом надо.

ОСОБО О КОНТРПРИМЕРЕ. Свидетель, который НЕ опровергает, звучит
убедительнее всего, ибо форма у него правильная. Потому проверяется не
форма, а работа: свидетель обязан УДОВЛЕТВОРЯТЬ посылке и НАРУШАТЬ
следствие.

ОБ ОПРЕДЕЛЕНИЯХ. Их суд — сверка с независимо записанным здесь
списком, и держится ПАРА «вопрос — ответ», а не два списка.

СУД НЕ СМЕЕТ ЧИТАТЬ ЧУЖОЙ РОД: образцы узкие и привязаны к зачину,
неузнанная строка есть (False, False) — молчание, а не вердикт.
"""

import json
import pathlib
import re
import sys

# ВТОРАЯ РУКА: буквы переменной объявлены и здесь. Буква подставляется в
# образец целиком, потому она обязана быть ОДНОЙ во всей строке.
БУКВЫ = ("k", "n", "m")


КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "scripts"))
sys.path.insert(0, str(КОРЕНЬ / "tools"))
from genesis import Unreadable, worlds  # noqa: E402
import universals  # noqa: E402
import parity  # noqa: E402
import coprime  # noqa: E402
import paraphrase  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file


def _числа(язык):
    """Числительные языка — ИЗ ЕГО ПАКЕТА.

    Единственное место, где суд не пишет второй рукой, и это нарочно:
    числительные суть объявление ЯЗЫКА о себе, а не утверждение слоя.
    Правила гармонии и падежа написаны здесь отдельно — вот они и есть
    вторая рука.
    """
    путь = КОРЕНЬ / "tools" / "langpacks" / f"{язык}.json"
    try:
        return json.loads(путь.read_text(encoding="utf-8")).get(
            "numerals", {})
    except (OSError, ValueError) as беда:
        print(f"ДОЗНАНИЕ-PL-TR ОТКАЗ: {путь.name}: {беда}")
        sys.exit(2)


ЧИСЛА_TR = _числа("tr")

ЗАДНИЕ = "aıou"
ПЕРЕДНИЕ = "eiöü"
ПО_ГЛАСНОЙ = {"a": "mı", "ı": "mı", "e": "mi", "i": "mi",
              "o": "mu", "u": "mu", "ö": "mü", "ü": "mü"}
СО_СВЯЗКОЙ = {"mı": "mıdır", "mi": "midir", "mu": "mudur",
              "mü": "müdür"}


def последняя_гласная(слово):
    for знак in reversed(слово):
        if знак in ЗАДНИЕ or знак in ПЕРЕДНИЕ:
            return знак
    return None


def частица(слово):
    """mı / mi / mu / mü — ВЫВЕДЕННАЯ, а не выбранная из списка."""
    г = последняя_гласная(слово)
    return ПО_ГЛАСНОЙ[г] if г else None


def частица_связкой(слово):
    """mıdır / midir / mudur / müdür — при ИМЕННОМ сказуемом."""
    ч = частица(слово)
    return СО_СВЯЗКОЙ[ч] if ч else None


def дательный(n):
    """«8'e», «6'ya», «10'a» — или None, если числа пакет не объявил."""
    слово = ЧИСЛА_TR.get(str(n))
    if not слово:
        return None
    г = последняя_гласная(слово)
    окончание = "a" if г in ЗАДНИЕ else "e"
    буфер = "y" if слово[-1] in ЗАДНИЕ + ПЕРЕДНИЕ else ""
    return f"{n}'{буфер}{окончание}"


def по_турецки(слово):
    """Значение написанного турецкого числительного, или None.

    Обратный ход: слой идёт от числа к слову, суд — от слова к числу.
    Одиннадцать объявлено ДВУМЯ СЛОВАМИ («on bir»), и здесь оно
    читается целиком, а не по частям: разобрать его как «десять» плюс
    «один» значило бы выдумать за язык закон сложения, которого пакет
    не объявлял.
    """
    обратно = {з: int(к) for к, з in ЧИСЛА_TR.items()}
    if слово in обратно:
        return обратно[слово]
    return int(слово) if слово.isdigit() else None


# ------------------------------------------------------------- СЧЁТ

def делители(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def простое(n):
    return n > 1 and делители(n) == [1, n]


def сумма_цифр(n):
    return sum(int(ц) for ц in str(n))


# ВОПРОС И ЕГО ОТВЕТ СВЯЗАНЫ РОДОМ, А НЕ СОСЕДСТВОМ. Пары записаны
# здесь ВТОРОЙ РУКОЙ; правка в одном доме и не в другом делает строку
# НЕСУДИМОЙ, а ворота записи несудимую строку не пропускают.
РОДЫ = (
    (("co to jest liczba pierwsza?", "asal sayı nedir?"),
     ("liczba pierwsza to liczba całkowita większa od 1, która dzieli "
      "się tylko przez 1 i przez samą siebie.",
      "asal sayı, yalnızca 1'e ve kendisine bölünen, 1'den büyük tam "
      "sayıdır.")),
    (("co znaczy, że liczba dzieli się przez inną?",
      "bölünmek ne demektir?"),
     ("liczba dzieli się przez inną, gdy reszta wynosi 0.",
      "kalan 0 olduğunda bir sayı başka bir sayıya bölünür.")),
    (("co to jest liczba nieparzysta?", "tek sayı nedir?"),
     ("liczby nieparzyste zaczynają się 1, 3, 5, 7 i każda następna "
      "jest o 2 większa od poprzedniej.",
      "tek sayılar 1, 3, 5, 7 diye başlar ve her biri bir öncekinden "
      "2 fazladır.")),
    (("co to jest zdanie warunkowe?", "koşullu önerme nedir?"),
     ("zdanie warunkowe jest prawdziwe, gdy wniosek zachodzi w każdym "
      "przypadku, w którym zachodzi założenie.",
      "bir koşullu önerme, öncül sağlandığı her durumda sonuç da "
      "sağlanıyorsa doğrudur.")),
    (("co znaczy, że funkcja jest różnowartościowa?",
      "bir fonksiyonun birebir olması ne demektir?"),
     ("funkcja jest różnowartościowa, gdy różne argumenty dają różne "
      "wartości.",
      "bir fonksiyon, farklı girdiler farklı çıktılar veriyorsa "
      "birebirdir.")),
    (("co to jest kwadrat liczby?", "bir sayının karesi nedir?"),
     ("kwadrat liczby to ta liczba pomnożona przez samą siebie.",
      "bir sayının karesi, o sayının kendisiyle çarpımıdır.")),
)
ОПРЕДЕЛЕНИЯ = frozenset(о for _в, опр in РОДЫ for о in опр)
ОТВЕТЫ = frozenset(f"{в} {о}" for вопр, опр in РОДЫ
                   for в, о in zip(вопр, опр))


# ------------------------------------------------------------ ПРОВЕРКИ

def _простое_да(м):
    n, n2, n3 = (int(з) for з in м.groups())
    return простое(n) and n2 == n and n3 == n


def _простое_да_tr(м):
    """Простота — И ЧАСТИЦА, выведенная из слова «sayı»."""
    n, чтц, n2 = int(м.group(1)), м.group(2), int(м.group(3))
    return (простое(n) and n2 == n
            and чтц == частица_связкой("sayı"))


def _простое_нет(м):
    n, n2, a, b = (int(з) for з in м.groups())
    return not простое(n) and n2 == n and a * b == n and a > 1 and b > 1


def _простое_нет_tr(м):
    n, чтц, n2, a, b = (м.group(1), м.group(2), м.group(3), м.group(4),
                        м.group(5))
    n, n2, a, b = int(n), int(n2), int(a), int(b)
    return (not простое(n) and n2 == n and a * b == n and a > 1
            and b > 1 and чтц == частица_связкой("sayı"))


def _контр_простое(м):
    n, n2, a, b = (int(з) for з in м.groups())
    return (n % 2 == 1 and not простое(n) and n2 == n
            and a * b == n and a > 1 and b > 1)


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


def _делится_да_tr(м, глагол):
    """Делимость, ДАТЕЛЬНЫЙ НА ЦИФРЕ и ЧАСТИЦА — три вещи разом."""
    a, b, суф, чтц, a2, b2, q = м.groups()
    a, b, a2, b2, q = int(a), int(b), int(a2), int(b2), int(q)
    return (a % b == 0 and a2 == a and b2 == b and b * q == a
            and дательный(b) == f"{b}'{суф}"
            and чтц == частица(глагол))


def _делится_да_широкое(м):
    return _делится_да_tr(м, "bölünür")


def _делится_да_длительное(м):
    return _делится_да_tr(м, "bölünüyor")


def _делится_нет(м):
    a, b, a2, b2, q, r, r2 = (int(з) for з in м.groups())
    return (a % b != 0 and a2 == a and b2 == b and b * q + r == a
            and r == a % b and r2 == r and r > 0)


def _делится_нет_tr(м, глагол):
    a, b, суф, чтц, a2, b2, q, r, r2 = м.groups()
    a, b, a2, b2, q, r, r2 = (int(a), int(b), int(a2), int(b2), int(q),
                              int(r), int(r2))
    return (a % b != 0 and a2 == a and b2 == b and b * q + r == a
            and r == a % b and r2 == r and r > 0
            and дательный(b) == f"{b}'{суф}"
            and чтц == частица(глагол))


def _делится_нет_широкое(м):
    return _делится_нет_tr(м, "bölünür")


def _делится_нет_длительное(м):
    return _делится_нет_tr(м, "bölünüyor")


def _контр_делимость(м):
    n, n2, q, r = (int(з) for з in м.groups())
    # ЧЕТВЁРКА В ЗАПИСИ ЕСТЬ БУКВА ЗАКОНА, А НЕ ВЕЛИЧИНА РЯДА.
    return (n % 2 == 0 and n % 4 != 0 and n2 == n
            and 4 * q + r == n and r > 0)


def _контр_делимость_tr(м):
    """То же, и вдобавок ДАТЕЛЬНЫЙ на четвёрке выведен верно."""
    четыре, суф, n, n2, q, r = м.groups()
    четыре, n, n2, q, r = (int(четыре), int(n), int(n2), int(q),
                           int(r))
    return (четыре == 4 and дательный(4) == f"4'{суф}"
            and n % 2 == 0 and n % 4 != 0 and n2 == n
            and 4 * q + r == n and r > 0)


def _цифры_на_три(м):
    n, с, с2, q = (int(з) for з in м.groups())
    return (n % 3 == 0 and сумма_цифр(n) == с and с2 == с
            and 3 * q == с)


def _цифры_на_три_tr(м):
    три1, суф1, три2, суф2, n, с, с2, q = м.groups()
    три1, три2, n, с, с2, q = (int(три1), int(три2), int(n), int(с),
                               int(с2), int(q))
    дат = дательный(3)
    return (три1 == три2 == 3 and дат == f"3'{суф1}" == f"3'{суф2}"
            and n % 3 == 0 and сумма_цифр(n) == с and с2 == с
            and 3 * q == с)


def _сумма_нечётных(м):
    k, ряд, итог = int(м.group(1)), м.group(2), int(м.group(3))
    числа = [int(x) for x in re.findall(r"\d+", ряд)]
    return (числа == [2 * j + 1 for j in range(k)]
            and sum(числа) == итог == k * k and len(числа) == k)


def _сумма_нечётных_tr(м):
    """Счёт ВЫВОДИТСЯ ИЗ РЯДА, а слово сверяется с ним.

    Порядок важен: суд, взявший счёт из СЛОВА и проверивший им же ряд,
    проверял бы слово словом.
    """
    слово, ряд, итог = м.group(1), м.group(2), int(м.group(3))
    числа = [int(x) for x in re.findall(r"\d+", ряд)]
    k = len(числа)
    return (числа == [2 * j + 1 for j in range(k)]
            and sum(числа) == итог == k * k
            and по_турецки(слово) == k)


def _контр_сумма(м):
    k, сумма, k2, двак = (int(з) for з in м.groups())
    return (сумма == k * k and k2 == k and двак == 2 * k
            and k * k != 2 * k)


def _общ_сумма(м):
    k, k2, k3, итог = (int(з) for з in м.groups())
    return k2 == k3 == k and итог == k * k


def _условное_pl(м):
    m_, ответ, e, e2, m2, s, чёт = м.groups()
    m_, e, e2, m2, s = int(m_), int(e), int(e2), int(m2), int(s)
    да = ответ == "tak"
    чётно = чёт == "parzyste"
    return (e % 2 == 0 and e2 == e and m2 == m_ and e + m_ == s
            and чётно == (s % 2 == 0) and да == (m_ % 2 == 0))


def _условное_tr(м):
    """Вердикт, счёт — И ЧАСТИЦА, выведенная из слова «çift»."""
    m_, чтц, ответ, e, e2, m2, s, чёт = м.groups()
    m_, e, e2, m2, s = int(m_), int(e), int(e2), int(m2), int(s)
    да = ответ == "evet"
    чётно = чёт == "çifttir"
    return (чтц == частица_связкой("çift")
            and e % 2 == 0 and e2 == e and m2 == m_ and e + m_ == s
            and чётно == (s % 2 == 0) and да == (m_ % 2 == 0))


def _контр_условное(м):
    m_, e, e2, m2, s = (int(з) for з in м.groups())
    return (m_ % 2 == 1 and e % 2 == 0 and e2 == e and m2 == m_
            and e + m_ == s and s % 2 == 1)


def _общ_условное(м):
    m_, e, m2, s = (int(з) for з in м.groups())
    return (m_ % 2 == 0 and e % 2 == 0 and m2 == m_
            and e + m_ == s and s % 2 == 0)


def _инъекция_pl(м):
    k, ответ, a, b, c, разные = м.groups()
    k, a, b, c = int(k), int(a), int(b), int(c)
    да = ответ == "tak"
    все_разные = разные == "wszystkie różne"
    return (a == k and b == 2 * k and c == 3 * k
            and все_разные == (len({a, b, c}) == 3)
            and да == (k != 0) and все_разные == да)


def _инъекция_tr(м):
    k, чтц, ответ, a, b, c, разные = м.groups()
    k, a, b, c = int(k), int(a), int(b), int(c)
    да = ответ == "evet"
    все_разные = разные == "hepsi farklıdır"
    return (чтц == частица_связкой("birebir")
            and a == k and b == 2 * k and c == 3 * k
            and все_разные == (len({a, b, c}) == 3)
            and да == (k != 0) and все_разные == да)


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


def _общ_квадрат_pl(м):
    """Род и сказуемое согласованы между собой и с чётностью числа."""
    род, сказ, n, n2, кв = м.groups()
    n, n2, кв = int(n), int(n2), int(кв)
    чёт = род == "parzystej"
    return (чёт == (сказ == "parzysty") and n2 == n and кв == n * n
            and чёт == (n % 2 == 0) and (кв % 2 == 0) == чёт)


def _общ_квадрат_tr(м):
    имя, сказ, n, n2, кв = м.groups()
    n, n2, кв = int(n), int(n2), int(кв)
    чёт = имя == "çift"
    return (сказ == ("çifttir" if чёт else "tektir")
            and n2 == n and кв == n * n
            and чёт == (n % 2 == 0) and (кв % 2 == 0) == чёт)


# ------------------------------------------------------------- ОБРАЗЦЫ

Ч = r"(\d+)"
С = r"(.+?)"
# ЧАСТИЦА ЛОВИТСЯ ПЕРЕЧНЕМ ВСЕХ ЧЕТЫРЁХ, А ВЫВОДИТСЯ ПРОВЕРКОЙ: образец
# обязан пропустить неверную, чтобы суд назвал её ЛОЖЬЮ. Образец,
# знающий только верную, оставил бы неверную несудимой — и корпус
# получил бы вместо вердикта молчание.
ЧТЦ = r"(mı|mi|mu|mü)"
ЧТЦД = r"(mıdır|midir|mudur|müdür)"
ДАТ = r"(\d+)'(y?[ae])"
ОБРАЗЦЫ = (
    (rf"^czy {Ч} jest liczbą pierwszą\? tak: dzielniki {Ч} to 1 i "
     rf"{Ч}\.$", _простое_да),
    (rf"^{Ч} asal sayı {ЧТЦД}\? evet: {Ч} sayısının bölenleri yalnızca "
     r"1 ve kendisidir\.$", _простое_да_tr),
    (rf"^czy {Ч} jest liczbą pierwszą\? nie: {Ч} = {Ч} × {Ч}\.$",
     _простое_нет),
    (rf"^{Ч} asal sayı {ЧТЦД}\? hayır: {Ч} = {Ч} × {Ч}\.$",
     _простое_нет_tr),
    (rf"^wszystkie liczby nieparzyste są pierwsze to fałsz: {Ч} jest "
     rf"nieparzyste i {Ч} = {Ч} × {Ч}\.$", _контр_простое),
    (rf"^tüm tek sayılar asaldır demek yanlıştır: {Ч} tektir ve {Ч} = "
     rf"{Ч} × {Ч}\.$", _контр_простое),
    (rf"^każda liczba całkowita większa od 1 jest iloczynem liczb "
     rf"pierwszych: {Ч} = " r"([\d ×]+)\.$", _произведение),
    (rf"^1'den büyük her tam sayı asal sayıların çarpımıdır: {Ч} = "
     r"([\d ×]+)\.$", _произведение),
    (rf"^czy {Ч} dzieli się przez {Ч}\? tak: {Ч} = {Ч} × {Ч}, "
     r"reszta 0\.$", _делится_да),
    (rf"^{Ч} sayısı {ДАТ} bölünür {ЧТЦ}\? evet: {Ч} = {Ч} × {Ч}, "
     r"kalan 0\.$", _делится_да_широкое),
    (rf"^{Ч} sayısı {ДАТ} tam bölünüyor {ЧТЦ}\? evet: {Ч} = {Ч} × {Ч}, "
     r"kalan 0\.$", _делится_да_длительное),
    (rf"^czy {Ч} dzieli się przez {Ч}\? nie: {Ч} = {Ч} × {Ч} \+ {Ч}, "
     rf"reszta {Ч}\.$", _делится_нет),
    (rf"^{Ч} sayısı {ДАТ} bölünür {ЧТЦ}\? hayır: {Ч} = {Ч} × {Ч} \+ "
     rf"{Ч}, kalan {Ч}\.$", _делится_нет_широкое),
    (rf"^{Ч} sayısı {ДАТ} tam bölünüyor {ЧТЦ}\? hayır: {Ч} = {Ч} × {Ч} "
     rf"\+ {Ч}, kalan {Ч}\.$", _делится_нет_длительное),
    (rf"^wszystkie liczby parzyste dzielą się przez 4 to fałsz: {Ч} "
     rf"jest parzyste i {Ч} = 4 × {Ч} \+ {Ч}\.$", _контр_делимость),
    (rf"^tüm çift sayılar {ДАТ} bölünür demek yanlıştır: {Ч} çifttir "
     rf"ve {Ч} = 4 × {Ч} \+ {Ч}\.$", _контр_делимость_tr),
    (rf"^liczba dzieli się przez 3, gdy dzieli się suma jej cyfr: suma "
     rf"cyfr {Ч} wynosi {Ч}, a {Ч} = 3 × {Ч}\.$", _цифры_на_три),
    (rf"^bir sayı, rakamları toplamı {ДАТ} bölünüyorsa {ДАТ} bölünür: "
     rf"{Ч} sayısında rakamlar toplamı {Ч} olur ve {Ч} = 3 × {Ч}\.$",
     _цифры_на_три_tr),
    (rf"^ile wynosi suma pierwszych {Ч} liczb nieparzystych\? "
     r"([\d +]+) = " rf"{Ч}\.$", _сумма_нечётных),
    (rf"^ilk {С} tek sayının toplamı kaçtır\? " r"([\d +]+) = "
     rf"{Ч}\.$", _сумма_нечётных_tr),
    *[(rf"^suma pierwszych {б} liczb nieparzystych wynosi 2 × {б} to fałsz: "
     rf"dla {б} = {Ч} suma wynosi {Ч}, a 2 × {Ч} = {Ч}\.$", _контр_сумма) for б in БУКВЫ],
    *[(rf"^ilk {б} tek sayının toplamı 2 × {б} demek yanlıştır: {б} = {Ч} için "
     rf"toplam {Ч} ve 2 × {Ч} = {Ч}\.$", _контр_сумма) for б in БУКВЫ],
    *[(rf"^suma pierwszych {б} liczb nieparzystych wynosi {б} × {б}: dla "
     rf"{б} = {Ч} jest to {Ч} × {Ч} = {Ч}\.$", _общ_сумма) for б in БУКВЫ],
    *[(rf"^ilk {б} tek sayının toplamı {б} × {б} olur: {б} = {Ч} için {Ч} × {Ч} "
     rf"= {Ч}\.$", _общ_сумма) for б in БУКВЫ],
    (rf"^jeśli n jest parzyste, czy n \+ {Ч} jest parzyste\? "
     rf"(tak|nie): {Ч} jest parzyste i {Ч} \+ {Ч} = {Ч}, co jest "
     r"(parzyste|nieparzyste)\.$", _условное_pl),
    (rf"^n çift ise n \+ {Ч} çift {ЧТЦД}\? (evet|hayır): {Ч} çifttir "
     rf"ve {Ч} \+ {Ч} = {Ч}, bu da (çifttir|tektir)\.$", _условное_tr),
    (rf"^jeśli n jest parzyste, to n \+ {Ч} jest parzyste to fałsz: "
     rf"{Ч} jest parzyste i {Ч} \+ {Ч} = {Ч}, co jest nieparzyste\.$",
     _контр_условное),
    (rf"^n çift ise n \+ {Ч} çifttir demek yanlıştır: {Ч} çifttir ve "
     rf"{Ч} \+ {Ч} = {Ч}, bu da tektir\.$", _контр_условное),
    (rf"^jeśli n jest parzyste, to n \+ m jest parzyste dokładnie "
     rf"wtedy, gdy m jest parzyste: {Ч} jest parzyste i {Ч} \+ {Ч} = "
     rf"{Ч}, co jest parzyste\.$", _общ_условное),
    (rf"^n çift ise n \+ m çifttir ancak ve ancak m çifttir: {Ч} "
     rf"çifttir ve {Ч} \+ {Ч} = {Ч}, bu da çifttir\.$", _общ_условное),
    (rf"^czy f\(x\) = x × {Ч} jest różnowartościowa na 1, 2, 3\? "
     rf"(tak|nie): daje {Ч}, {Ч}, {Ч}, "
     r"(wszystkie różne|nie wszystkie różne)\.$", _инъекция_pl),
    (rf"^f\(x\) = x × {Ч} birebir {ЧТЦД}\? (evet|hayır): {Ч}, {Ч}, {Ч} "
     r"verir, (hepsi farklıdır|hepsi farklı değildir)\.$",
     _инъекция_tr),
    (rf"^wszystkie funkcje są różnowartościowe to fałsz: f\(x\) = x × "
     rf"0 prowadzi {Ч} i {Ч} do 0\.$", _контр_инъекция),
    (rf"^tüm fonksiyonlar birebirdir demek yanlıştır: f\(x\) = x × 0 "
     rf"hem {Ч} hem {Ч} sayısını 0 yapar\.$", _контр_инъекция),
    *[(rf"^f\(x\) = x × {б} jest różnowartościowa dokładnie wtedy, gdy {б} "
     rf"nie jest 0: dla {б} = {Ч} argumenty 1 i 2 dają {Ч} i {Ч}\.$",
     _общ_инъекция) for б in БУКВЫ],
    *[(rf"^f\(x\) = x × {б} birebirdir ancak ve ancak {б} 0 değildir: "
     rf"{б} = {Ч} için 1 ve 2 girdileri {Ч} ve {Ч} verir\.$",
     _общ_инъекция) for б in БУКВЫ],
    (rf"^ile wynosi kwadrat liczby {Ч}\? {Ч} × {Ч} = {Ч}\.$", _квадрат),
    (rf"^{Ч} sayısının karesi kaçtır\? {Ч} × {Ч} = {Ч}\.$", _квадрат),
    (rf"^wszystkie kwadraty są parzyste to fałsz: {Ч} jest nieparzyste "
     rf"i {Ч} × {Ч} = {Ч}, co jest nieparzyste\.$", _контр_квадрат),
    (rf"^tüm kareler çifttir demek yanlıştır: {Ч} tektir ve {Ч} × {Ч} "
     rf"= {Ч}, bu da tektir\.$", _контр_квадрат),
    (r"^kwadrat liczby (parzystej|nieparzystej) jest "
     r"(parzysty|nieparzysty): " rf"{Ч} × {Ч} = {Ч}\.$",
     _общ_квадрат_pl),
    (r"^(çift|tek) sayının karesi (çifttir|tektir): "
     rf"{Ч} × {Ч} = {Ч}\.$", _общ_квадрат_tr),
)
# УНИВЕРСАЛИЯ СПРАШИВАЕТСЯ СВОИМ «ВЕРНО ЛИ, ЧТО» (tools/universals.py): образец
# контрпримера или обобщения сварен с выведенным из него вопросом в ОДНО
# семейство (М-146); остальные образцы — как есть.
ЯЗЫКИ_МИРА = ('pl', 'tr')
# ПЕРЕФРАЗА — ФОРМА ПАКЕТА (tools/paraphrase.py, Т-4): образцы других форм
# простоты и делимости выведены из образцов первой формы с теми же судьями.
ПРАВИЛА = universals.правила(list(ОБРАЗЦЫ) + paraphrase.образцы(ОБРАЗЦЫ, ЯЗЫКИ_МИРА, ("prime", "divisible")), ЯЗЫКИ_МИРА) + tuple((re.compile(о), п) for о, п in parity.образцы(ЯЗЫКИ_МИРА) + coprime.образцы(ЯЗЫКИ_МИРА))


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
        print(f"ДОЗНАНИЕ-PL-TR ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("ДОЗНАНИЕ-PL-TR ОТКАЗ: обход пуст, судить нечего")
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
    print(f"ДОЗНАНИЕ-PL-TR {поза}: {ложных} ложных из {судимых} "
          f"судимых ({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
