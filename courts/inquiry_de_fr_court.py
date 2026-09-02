#!/usr/bin/env python3
"""[ДОЗНАНИЕ DE-FR] — вердикт не читается, а переспрашивается.

Немецкий и французский пласты лестницы дознания говорят четырьмя
ступенями — определение, исполнение, контрпример, обобщение, — и три из
четырёх несут ОСНОВАНИЕ рядом с ответом: «nein: 91 = 7 × 13», «non :
91 = 7 × 13». Суд не верит ни ответу, ни основанию: он раскладывает
число заново, делит заново, складывает ряд заново и сверяет ТРИ вещи
разом — что основание верно, что ответ ему соответствует и что ответ
верен по существу.

ОДИН СЧЁТ НА ДВА ЯЗЫКА, И В ЭТОМ ВЕСЬ СМЫСЛ. Немецкая и французская
поверхности одного факта проверяются ОДНОЙ функцией: образцы разные,
проверка общая. Оттого расхождение языков невозможно скрыть — ложь
пришлось бы солгать дважды и одинаково, а порча шаблона так не
ошибается. Это тот же ход, каким английский и русский близнецы судятся
одним счётом в `courts/inquiry_court.py`.

ОСОБО О КОНТРПРИМЕРЕ. Контрпример есть самое хрупкое место корпуса:
свидетель, который НЕ опровергает, звучит убедительнее всего, ибо форма
у него правильная. Потому здесь проверяется не форма, а РАБОТА — что
названный свидетель ДЕЙСТВИТЕЛЬНО удовлетворяет посылке всеобщего
утверждения и ДЕЙСТВИТЕЛЬНО нарушает его следствие. «9 ist ungerade und
9 = 3 × 3» убивает «alle ungeraden Zahlen sind Primzahlen» лишь если
девять и вправду нечётно, и вправду не просто, и трижды три вправду
девять.

ОБ ОПРЕДЕЛЕНИЯХ. Их суд — сверка с независимо записанным здесь
списком: тот же факт, сказанный второй рукой. Правка определения в
одном доме и не в другом делает строку НЕСУДИМОЙ, а ворота записи
несудимую строку не пропускают — и слой не будет записан вовсе.

ТИПОГРАФИКА ЕСТЬ ЧАСТЬ ОБРАЗЦА, А НЕ ЕГО ОФОРМЛЕНИЕ. Французский пробел
перед «?» и «:» стоит в образцах буквально: строка, написанная по
английскому обычаю («premier?»), сюда НЕ ПОПАДЁТ и останется
несудимой — то есть не пройдёт ворота записи. Так правило языка
охраняется тем же механизмом, что и правильность счёта, а не
доброй волей пишущего.

ЧЕГО СУД НЕ ЧИТАЕТ: чужого рода. Все образцы привязаны к зачину;
неузнанная строка есть (False, False).
"""

import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "scripts"))
sys.path.insert(0, str(КОРЕНЬ / "tools"))
from genesis import Unreadable, worlds  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file

# ВОПРОС И ЕГО ОТВЕТ СВЯЗАНЫ РОДОМ, А НЕ СОСЕДСТВОМ. Пара записана
# здесь ВТОРОЙ РУКОЙ — тот же факт, сказанный отдельно от генератора.
# Ответ на чужой вопрос («was ist eine Primzahl? das Quadrat einer
# Zahl ist…») не пройдёт: суд держит ПАРУ, а не два списка.
РОДЫ = (
    (("was ist eine Primzahl?", "qu'est-ce qu'un nombre premier ?"),
     ("eine Primzahl ist eine ganze Zahl größer als 1, deren einzige "
      "Teiler 1 und sie selbst sind.",
      "un nombre premier est un nombre entier supérieur à 1 dont les "
      "seuls diviseurs sont 1 et lui-même.")),
    (("was bedeutet teilbar?", "que signifie divisible ?"),
     ("eine Zahl ist durch eine andere teilbar, wenn der Rest 0 ist.",
      "un nombre est divisible par un autre quand le reste est 0.")),
    (("was ist eine ungerade Zahl?", "qu'est-ce qu'un nombre impair ?"),
     ("die ungeraden Zahlen beginnen mit 1, 3, 5, 7, und jede ist um "
      "2 größer als die vorige.",
      "les nombres impairs commencent par 1, 3, 5, 7, et chacun "
      "dépasse le précédent de 2.")),
    (("was ist eine bedingte Aussage?",
      "qu'est-ce qu'une proposition conditionnelle ?"),
     ("eine bedingte Aussage gilt, wenn die Folgerung in jedem Fall "
      "gilt, in dem die Voraussetzung gilt.",
      "une proposition conditionnelle est vraie quand la conclusion "
      "vaut dans tous les cas où la prémisse vaut.")),
    (("was heißt es, dass eine Funktion injektiv ist?",
      "que signifie qu'une fonction est injective ?"),
     ("eine Funktion ist injektiv, wenn verschiedene Eingaben "
      "verschiedene Ausgaben liefern.",
      "une fonction est injective quand des entrées différentes "
      "donnent des sorties différentes.")),
    (("was ist das Quadrat einer Zahl?",
      "qu'est-ce que le carré d'un nombre ?"),
     ("das Quadrat einer Zahl ist die Zahl mit sich selbst "
      "multipliziert.",
      "le carré d'un nombre est le nombre multiplié par lui-même.")),
)
ОПРЕДЕЛЕНИЯ = frozenset(о for _в, опр in РОДЫ for о in опр)
ОТВЕТЫ = frozenset(f"{в} {о}" for вопр, опр in РОДЫ
                   for в, о in zip(вопр, опр))

# СЛОВА ВЕРДИКТА И ПРИЗНАКА — ДВА ЯЗЫКА, ОДНО ЗНАЧЕНИЕ. Суд сверяет
# СМЫСЛ ответа с пересчётом, и потому обязан знать, что «ja» и «oui»
# суть одно, а «gerade» и «pair» — одно. Списки объявлены, а не
# выведены отсечением: язык не угадывается.
ДА = frozenset(("ja", "oui"))
ЧЁТНО = frozenset(("gerade", "pair"))
ЧЁТНОЕ_ИМЯ = frozenset(("geraden", "pair"))
ВСЕ_РАЗНЫЕ = frozenset(("alle verschieden", "toutes différentes"))


def делители(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def простое(n):
    return n > 1 and делители(n) == [1, n]


def ч(м, *номера):
    """Целые из НАЗВАННЫХ скобок — не из всей строки.

    Число, стоящее в записи БУКВОЙ ЗАКОНА («= 4 × q + r», «1 und n»),
    не есть величина показа, и суд обязан брать ровно то, что назвал
    образцом.
    """
    return [int(м.group(i)) for i in номера]


# ------------------------------------------------------------ ПРОВЕРКИ

def _простое_да(м):
    n, n2, n3 = ч(м, 1, 2, 3)
    return простое(n) and n2 == n and n3 == n


def _простое_нет(м):
    n, n2, a, b = ч(м, 1, 2, 3, 4)
    return not простое(n) and n2 == n and a * b == n and a > 1 and b > 1


def _контр_простое(м):
    n, n2, a, b = ч(м, 1, 2, 3, 4)
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
    a, b, a2, b2, q = ч(м, 1, 2, 3, 4, 5)
    return a % b == 0 and a2 == a and b2 == b and b * q == a


def _делится_нет(м):
    a, b, a2, b2, q, r, r2 = ч(м, 1, 2, 3, 4, 5, 6, 7)
    return (a % b != 0 and a2 == a and b2 == b and b * q + r == a
            and r == a % b and r2 == r and r > 0)


def _контр_делимость(м):
    n, n2, q, r = ч(м, 1, 2, 3, 4)
    # ЧЕТВЁРКА В ЗАПИСИ ЕСТЬ БУКВА ЗАКОНА, А НЕ ВЕЛИЧИНА РЯДА.
    return (n % 2 == 0 and n % 4 != 0 and n2 == n
            and 4 * q + r == n and r > 0)


def _цифры_на_три(м):
    n, с, с2, q = ч(м, 1, 2, 3, 4)
    return (n % 3 == 0 and sum(int(ц) for ц in str(n)) == с
            and с2 == с and 3 * q == с)


def _сумма_нечётных(м):
    k, итог = ч(м, 1, 3)
    ряд = [int(x) for x in re.findall(r"\d+", м.group(2))]
    return (ряд == [2 * j + 1 for j in range(k)]
            and sum(ряд) == итог == k * k)


def _контр_сумма(м):
    k, сумма, k2, двак = ч(м, 1, 2, 3, 4)
    return (сумма == k * k and k2 == k and двак == 2 * k
            and k * k != 2 * k)


def _общ_сумма(м):
    k, k2, k3, итог = ч(м, 1, 2, 3, 4)
    return k2 == k3 == k and итог == k * k


def _условное_вопрос(м):
    m_, e, e2, m2, s = ч(м, 1, 3, 4, 5, 6)
    да = м.group(2) in ДА
    чётно = м.group(7) in ЧЁТНО
    return (e % 2 == 0 and e2 == e and m2 == m_ and e + m_ == s
            and чётно == (s % 2 == 0) and да == (m_ % 2 == 0))


def _контр_условное(м):
    m_, e, e2, m2, s = ч(м, 1, 2, 3, 4, 5)
    return (m_ % 2 == 1 and e % 2 == 0 and e2 == e and m2 == m_
            and e + m_ == s and s % 2 == 1)


def _общ_условное(м):
    m_, e, m2, s = ч(м, 1, 2, 3, 4)
    return (m_ % 2 == 0 and e % 2 == 0 and m2 == m_
            and e + m_ == s and s % 2 == 0)


def _инъекция_вопрос(м):
    k, a, b, c = ч(м, 1, 3, 4, 5)
    да = м.group(2) in ДА
    разные = м.group(6) in ВСЕ_РАЗНЫЕ
    return (a == k and b == 2 * k and c == 3 * k
            and разные == (len({a, b, c}) == 3)
            and да == (k != 0) and разные == да)


def _контр_инъекция(м):
    a, b = ч(м, 1, 2)
    return a != b


def _общ_инъекция(м):
    k, k2, двак = ч(м, 1, 2, 3)
    return k != 0 and k2 == k and двак == 2 * k


def _квадрат(м):
    n, n2, n3, кв = ч(м, 1, 2, 3, 4)
    return n2 == n3 == n and кв == n * n


def _контр_квадрат(м):
    n, n2, n3, кв = ч(м, 1, 2, 3, 4)
    return n % 2 == 1 and n2 == n3 == n and кв == n * n and кв % 2 == 1


def _общ_квадрат(м):
    n, n2, кв = ч(м, 3, 4, 5)
    чёт = м.group(1) in ЧЁТНОЕ_ИМЯ
    сказ = м.group(2) in ЧЁТНО
    return (n2 == n and кв == n * n and чёт == (n % 2 == 0)
            and сказ == чёт and (кв % 2 == 0) == чёт)


Ч = r"(\d+)"
ОБРАЗЦЫ = (
    (rf"^ist {Ч} eine Primzahl\? ja: die Teiler von {Ч} sind 1 und "
     rf"{Ч}\.$", _простое_да),
    (rf"^{Ч} est-il un nombre premier \? oui : les diviseurs de {Ч} "
     rf"sont 1 et {Ч}\.$", _простое_да),
    (rf"^ist {Ч} eine Primzahl\? nein: {Ч} = {Ч} × {Ч}\.$",
     _простое_нет),
    (rf"^{Ч} est-il un nombre premier \? non : {Ч} = {Ч} × {Ч}\.$",
     _простое_нет),
    (rf"^alle ungeraden Zahlen sind Primzahlen ist falsch: {Ч} ist "
     rf"ungerade und {Ч} = {Ч} × {Ч}\.$", _контр_простое),
    (rf"^tous les nombres impairs sont premiers est faux : {Ч} est "
     rf"impair et {Ч} = {Ч} × {Ч}\.$", _контр_простое),
    (rf"^jede ganze Zahl größer als 1 ist ein Produkt von Primzahlen: "
     rf"{Ч} = " r"([\d ×]+)\.$", _произведение),
    (rf"^tout nombre entier supérieur à 1 est un produit de nombres "
     rf"premiers : {Ч} = " r"([\d ×]+)\.$", _произведение),

    (rf"^ist {Ч} durch {Ч} teilbar\? ja: {Ч} = {Ч} × {Ч}, Rest 0\.$",
     _делится_да),
    (rf"^{Ч} est-il divisible par {Ч} \? oui : {Ч} = {Ч} × {Ч}, "
     rf"reste 0\.$", _делится_да),
    (rf"^ist {Ч} durch {Ч} teilbar\? nein: {Ч} = {Ч} × {Ч} \+ {Ч}, "
     rf"Rest {Ч}\.$", _делится_нет),
    (rf"^{Ч} est-il divisible par {Ч} \? non : {Ч} = {Ч} × {Ч} \+ "
     rf"{Ч}, reste {Ч}\.$", _делится_нет),
    (rf"^jede gerade Zahl ist durch 4 teilbar ist falsch: {Ч} ist "
     rf"gerade und {Ч} = 4 × {Ч} \+ {Ч}\.$", _контр_делимость),
    (rf"^tout nombre pair est divisible par 4 est faux : {Ч} est pair "
     rf"et {Ч} = 4 × {Ч} \+ {Ч}\.$", _контр_делимость),
    (rf"^eine Zahl ist durch 3 teilbar, wenn ihre Quersumme es ist: "
     rf"die Quersumme von {Ч} ist {Ч}, und {Ч} = 3 × {Ч}\.$",
     _цифры_на_три),
    (rf"^un nombre est divisible par 3 quand la somme de ses chiffres "
     rf"l'est : la somme des chiffres de {Ч} est {Ч}, et {Ч} = 3 × "
     rf"{Ч}\.$", _цифры_на_три),

    (rf"^was ist die Summe der ersten {Ч} ungeraden Zahlen\? "
     r"([\d +]+) = " rf"{Ч}\.$", _сумма_нечётных),
    (rf"^quelle est la somme des {Ч} premiers nombres impairs \? "
     r"([\d +]+) = " rf"{Ч}\.$", _сумма_нечётных),
    (rf"^die Summe der ersten k ungeraden Zahlen ist 2 × k ist "
     rf"falsch: bei k = {Ч} ist die Summe {Ч}, und 2 × {Ч} = {Ч}\.$",
     _контр_сумма),
    (rf"^la somme des k premiers nombres impairs est 2 × k est faux : "
     rf"pour k = {Ч} la somme est {Ч}, et 2 × {Ч} = {Ч}\.$",
     _контр_сумма),
    (rf"^die Summe der ersten k ungeraden Zahlen ist k × k: bei "
     rf"k = {Ч} ist es {Ч} × {Ч} = {Ч}\.$", _общ_сумма),
    (rf"^la somme des k premiers nombres impairs est k × k : pour "
     rf"k = {Ч} c'est {Ч} × {Ч} = {Ч}\.$", _общ_сумма),

    (rf"^wenn n gerade ist, ist n \+ {Ч} gerade\? (ja|nein): {Ч} ist "
     rf"gerade, und {Ч} \+ {Ч} = {Ч}, was (gerade|ungerade) ist\.$",
     _условное_вопрос),
    (rf"^si n est pair, n \+ {Ч} est-il pair \? (oui|non) : {Ч} est "
     rf"pair, et {Ч} \+ {Ч} = {Ч}, qui est (pair|impair)\.$",
     _условное_вопрос),
    (rf"^wenn n gerade ist, dann ist n \+ {Ч} gerade ist falsch: {Ч} "
     rf"ist gerade, und {Ч} \+ {Ч} = {Ч}, was ungerade ist\.$",
     _контр_условное),
    (rf"^si n est pair alors n \+ {Ч} est pair est faux : {Ч} est "
     rf"pair, et {Ч} \+ {Ч} = {Ч}, qui est impair\.$",
     _контр_условное),
    (rf"^wenn n gerade ist, dann ist n \+ m genau dann gerade, wenn m "
     rf"gerade ist: {Ч} ist gerade und {Ч} \+ {Ч} = {Ч}, was gerade "
     rf"ist\.$", _общ_условное),
    (rf"^si n est pair alors n \+ m est pair exactement quand m est "
     rf"pair : {Ч} est pair et {Ч} \+ {Ч} = {Ч}, qui est pair\.$",
     _общ_условное),

    (rf"^ist f\(x\) = x × {Ч} auf 1, 2, 3 injektiv\? (ja|nein): sie "
     rf"liefert {Ч}, {Ч}, {Ч}, "
     r"(alle verschieden|nicht alle verschieden)\.$",
     _инъекция_вопрос),
    (rf"^f\(x\) = x × {Ч} est-elle injective sur 1, 2, 3 \? "
     rf"(oui|non) : elle donne {Ч}, {Ч}, {Ч}, "
     r"(toutes différentes|pas toutes différentes)\.$",
     _инъекция_вопрос),
    (rf"^jede Funktion ist injektiv ist falsch: f\(x\) = x × 0 "
     rf"schickt {Ч} und {Ч} beide auf 0\.$", _контр_инъекция),
    (rf"^toute fonction est injective est faux : f\(x\) = x × 0 "
     rf"envoie {Ч} et {Ч} tous deux sur 0\.$", _контр_инъекция),
    (rf"^f\(x\) = x × k ist genau dann injektiv, wenn k nicht 0 ist: "
     rf"bei k = {Ч} liefern die Eingaben 1 und 2 die Werte {Ч} und "
     rf"{Ч}\.$", _общ_инъекция),
    (rf"^f\(x\) = x × k est injective exactement quand k n'est pas "
     rf"0 : pour k = {Ч} les entrées 1 et 2 donnent {Ч} et {Ч}\.$",
     _общ_инъекция),

    (rf"^was ist das Quadrat von {Ч}\? {Ч} × {Ч} = {Ч}\.$", _квадрат),
    (rf"^quel est le carré de {Ч} \? {Ч} × {Ч} = {Ч}\.$", _квадрат),
    (rf"^jedes Quadrat ist gerade ist falsch: {Ч} ist ungerade und "
     rf"{Ч} × {Ч} = {Ч}, was ungerade ist\.$", _контр_квадрат),
    (rf"^tout carré est pair est faux : {Ч} est impair et {Ч} × {Ч} = "
     rf"{Ч}, qui est impair\.$", _контр_квадрат),
    (r"^das Quadrat einer (geraden|ungeraden) Zahl ist "
     r"(gerade|ungerade): " rf"{Ч} × {Ч} = {Ч}\.$", _общ_квадрат),
    (r"^le carré d'un nombre (pair|impair) est (pair|impair) : "
     rf"{Ч} × {Ч} = {Ч}\.$", _общ_квадрат),
)
ПРАВИЛА = tuple((re.compile(о), п) for о, п in ОБРАЗЦЫ)


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
        print(f"ДОЗНАНИЕ-DE-FR ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("ДОЗНАНИЕ-DE-FR ОТКАЗ: обход пуст, судить нечего")
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
    print(f"ДОЗНАНИЕ-DE-FR {поза}: {ложных} ложных из {судимых} "
          f"судимых ({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
