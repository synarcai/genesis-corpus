#!/usr/bin/env python3
"""[ДОЗНАНИЕ PT-NL] — вердикт не читается, а переспрашивается.

Португальский и нидерландский пласты лестницы дознания говорят четырьмя
ступенями — определение, исполнение, контрпример, обобщение, — и три из
четырёх несут ОСНОВАНИЕ рядом с ответом: «não: 91 = 7 × 13», «nee:
91 = 7 × 13». Суд не верит ни ответу, ни основанию: он раскладывает
число заново, делит заново, складывает ряд заново и сверяет ТРИ вещи
разом — что основание верно, что ответ ему соответствует и что ответ
верен по существу.

ОДИН СЧЁТ НА ДВА ЯЗЫКА, И В ЭТОМ ВЕСЬ СМЫСЛ. Португальская и
нидерландская поверхности одного факта проверяются ОДНОЙ функцией:
образцы разные, проверка общая. Расхождение языков потому и невозможно
скрыть, что ложь пришлось бы солгать дважды и одинаково, а порча
шаблона так не ошибается. Тот же ход держат близнецы в
`courts/inquiry_court.py` и `courts/inquiry_de_fr_court.py`.

СЛОВА ВЕРДИКТА ОБЪЯВЛЕНЫ, А НЕ ВЫВЕДЕНЫ. Суд сверяет СМЫСЛ ответа с
пересчётом и потому обязан знать, что «sim» и «ja» суть одно, а «par» и
«even» — одно. Здесь эти списки записаны; язык не угадывается ни по
окончанию, ни по соседству.

ПРИЗНАК В ЭТИХ ДВУХ ЯЗЫКАХ ПОВТОРЯЕТСЯ, А В НЕМЕЦКОМ МЕНЯЛСЯ. Немецкое
обобщение квадрата говорит «einer geraden Zahl ist gerade» — имя и
сказуемое разными формами, и суд держал для них два списка. Здесь оба
языка ставят одно слово дважды («de um número par é par», «een even
getal is even»), и список нужен один. Разница объявлена, а не сглажена:
она есть факт о языках, а не удобство прибора.

ОСОБО О КОНТРПРИМЕРЕ. Свидетель, который НЕ опровергает, звучит
убедительнее всего, ибо форма у него правильная. Потому здесь
проверяется не форма, а РАБОТА — что названный свидетель
ДЕЙСТВИТЕЛЬНО удовлетворяет посылке всеобщего утверждения и
ДЕЙСТВИТЕЛЬНО нарушает его следствие.

ОБ ОПРЕДЕЛЕНИЯХ. Их суд — сверка с независимо записанным здесь
списком: тот же факт, сказанный второй рукой. Правка определения в
одном доме и не в другом делает строку НЕСУДИМОЙ, а ворота записи
несудимую строку не пропускают — и слой не будет записан вовсе.

ТИЛЬДА ЕСТЬ ЧАСТЬ ОБРАЗЦА. Португальское «não» стоит в образцах со
своим знаком: строка, написанная как «nao», сюда НЕ ПОПАДЁТ и останется
несудимой, то есть не пройдёт ворота записи. Так правило письма
охраняется тем же механизмом, что и правильность счёта, а не доброй
волей пишущего.

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
import universals  # noqa: E402
import parity  # noqa: E402
import coprime  # noqa: E402
import paraphrase  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file

# ВОПРОС И ЕГО ОТВЕТ СВЯЗАНЫ РОДОМ, А НЕ СОСЕДСТВОМ. Пара записана
# здесь ВТОРОЙ РУКОЙ — тот же факт, сказанный отдельно от генератора.
# Ответ на чужой вопрос («wat is een priemgetal? het kwadraat van een
# getal is…») не пройдёт: суд держит ПАРУ, а не два списка.
РОДЫ = (
    (("o que é um número primo?", "wat is een priemgetal?"),
     ("um número primo é um número inteiro maior que 1 cujos únicos "
      "divisores são 1 e ele mesmo.",
      "een priemgetal is een geheel getal groter dan 1 waarvan de "
      "enige delers 1 en het getal zelf zijn.")),
    (("o que significa divisível?", "wat betekent deelbaar?"),
     ("um número é divisível por outro quando o resto é 0.",
      "een getal is deelbaar door een ander getal wanneer de rest 0 "
      "is.")),
    (("o que é um número ímpar?", "wat is een oneven getal?"),
     ("os números ímpares começam por 1, 3, 5, 7, e cada um é 2 maior "
      "que o anterior.",
      "de oneven getallen beginnen met 1, 3, 5, 7, en elk is 2 groter "
      "dan het vorige.")),
    (("o que é uma afirmação condicional?",
      "wat is een voorwaardelijke bewering?"),
     ("uma afirmação condicional vale quando a conclusão vale em "
      "todos os casos em que a premissa vale.",
      "een voorwaardelijke bewering geldt wanneer de gevolgtrekking "
      "geldt in elk geval waarin de aanname geldt.")),
    (("o que significa que uma função é injetiva?",
      "wat betekent het dat een functie injectief is?"),
     ("uma função é injetiva quando entradas diferentes dão saídas "
      "diferentes.",
      "een functie is injectief wanneer verschillende invoeren "
      "verschillende uitvoeren geven.")),
    (("o que é o quadrado de um número?",
      "wat is het kwadraat van een getal?"),
     ("o quadrado de um número é o número multiplicado por si mesmo.",
      "het kwadraat van een getal is het getal met zichzelf "
      "vermenigvuldigd.")),
)
ОПРЕДЕЛЕНИЯ = frozenset(о for _в, опр in РОДЫ for о in опр)
ОТВЕТЫ = frozenset(f"{в} {о}" for вопр, опр in РОДЫ
                   for в, о in zip(вопр, опр))

ДА = frozenset(("sim", "ja"))
# ОДИН СПИСОК НА ОБА МЕСТА: и португальский, и нидерландский ставят в
# обобщении квадрата ОДНО слово дважды («número par é par», «even
# getal is even»), в отличие от немецкого, где имя и сказуемое стоят
# разными формами (geraden / gerade).
ЧЁТНО = frozenset(("par", "even"))
ВСЕ_РАЗНЫЕ = frozenset(("todas diferentes", "alle verschillend"))


def делители(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def простое(n):
    return n > 1 and делители(n) == [1, n]


def ч(м, *номера):
    """Целые из НАЗВАННЫХ скобок — не из всей строки.

    Число, стоящее в записи БУКВОЙ ЗАКОНА («= 4 × q + r», «1 e n»), не
    есть величина показа, и суд обязан брать ровно то, что назвал
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


def _делится_повеств(м):
    """Повествование делимости: полярность слова судится остатком, не
    совпадением с образцом — снятое «не» есть ложь по счёту."""
    a, не, b, a2, b2, q, r, rest = м.groups()
    a, b, a2, b2, q = int(a), int(b), int(a2), int(b2), int(q)
    r = int(r) if r is not None else 0
    rest = int(rest)
    return (a == a2 and b == b2 and a == b * q + r and 0 <= r < b
            and rest == r and (не is None) == (r == 0))


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
    чёт = м.group(1) in ЧЁТНО
    сказ = м.group(2) in ЧЁТНО
    return (n2 == n and кв == n * n and чёт == (n % 2 == 0)
            and сказ == чёт and (кв % 2 == 0) == чёт)


Ч = r"(\d+)"
ОБРАЗЦЫ = (
    (rf"^{Ч} é um número primo\? sim: os divisores de {Ч} são 1 e "
     rf"{Ч}\.$", _простое_да),
    (rf"^is {Ч} een priemgetal\? ja: de delers van {Ч} zijn 1 en "
     rf"{Ч}\.$", _простое_да),
    (rf"^{Ч} é um número primo\? não: {Ч} = {Ч} × {Ч}\.$",
     _простое_нет),
    (rf"^is {Ч} een priemgetal\? nee: {Ч} = {Ч} × {Ч}\.$",
     _простое_нет),
    (rf"^todos os números ímpares são primos é falso: {Ч} é ímpar e "
     rf"{Ч} = {Ч} × {Ч}\.$", _контр_простое),
    (rf"^alle oneven getallen zijn priemgetallen is onwaar: {Ч} is "
     rf"oneven en {Ч} = {Ч} × {Ч}\.$", _контр_простое),
    (rf"^todo número inteiro maior que 1 é um produto de números "
     rf"primos: {Ч} = " r"([\d ×]+)\.$", _произведение),
    (rf"^elk geheel getal groter dan 1 is een product van "
     rf"priemgetallen: {Ч} = " r"([\d ×]+)\.$", _произведение),

    (rf"^{Ч} (não )?é divisível por {Ч}: {Ч} = {Ч} × {Ч}(?: \+ {Ч})?, "
     rf"resto {Ч}\.$", _делится_повеств),
    (rf"^{Ч} is (niet )?deelbaar door {Ч}: {Ч} = {Ч} × {Ч}(?: \+ {Ч})?, "
     rf"rest {Ч}\.$", _делится_повеств),
    (rf"^{Ч} é divisível por {Ч}\? sim: {Ч} = {Ч} × {Ч}, resto 0\.$",
     _делится_да),
    (rf"^is {Ч} deelbaar door {Ч}\? ja: {Ч} = {Ч} × {Ч}, rest 0\.$",
     _делится_да),
    (rf"^{Ч} é divisível por {Ч}\? não: {Ч} = {Ч} × {Ч} \+ {Ч}, "
     rf"resto {Ч}\.$", _делится_нет),
    (rf"^is {Ч} deelbaar door {Ч}\? nee: {Ч} = {Ч} × {Ч} \+ {Ч}, "
     rf"rest {Ч}\.$", _делится_нет),
    (rf"^todo número par é divisível por 4 é falso: {Ч} é par e {Ч} = "
     rf"4 × {Ч} \+ {Ч}\.$", _контр_делимость),
    (rf"^elk even getal is deelbaar door 4 is onwaar: {Ч} is even en "
     rf"{Ч} = 4 × {Ч} \+ {Ч}\.$", _контр_делимость),
    (rf"^um número é divisível por 3 quando a soma dos seus "
     rf"algarismos é divisível por 3: a soma dos algarismos de {Ч} é "
     rf"{Ч}, e {Ч} = 3 × {Ч}\.$", _цифры_на_три),
    (rf"^een getal is deelbaar door 3 wanneer zijn cijfersom deelbaar "
     rf"is door 3: de cijfersom van {Ч} is {Ч}, en {Ч} = 3 × {Ч}\.$",
     _цифры_на_три),

    (rf"^qual é a soma dos {Ч} primeiros números ímpares\? "
     r"([\d +]+) = " rf"{Ч}\.$", _сумма_нечётных),
    (rf"^wat is de som van de eerste {Ч} oneven getallen\? "
     r"([\d +]+) = " rf"{Ч}\.$", _сумма_нечётных),
    (rf"^a soma dos k primeiros números ímpares é 2 × k é falso: para "
     rf"k = {Ч} a soma é {Ч}, e 2 × {Ч} = {Ч}\.$", _контр_сумма),
    (rf"^de som van de eerste k oneven getallen is 2 × k is onwaar: "
     rf"bij k = {Ч} is de som {Ч}, en 2 × {Ч} = {Ч}\.$", _контр_сумма),
    (rf"^a soma dos k primeiros números ímpares é k × k: para k = {Ч} "
     rf"isso é {Ч} × {Ч} = {Ч}\.$", _общ_сумма),
    (rf"^de som van de eerste k oneven getallen is k × k: bij k = {Ч} "
     rf"is het {Ч} × {Ч} = {Ч}\.$", _общ_сумма),

    (rf"^se n é par, n \+ {Ч} é par\? (sim|não): {Ч} é par, e {Ч} \+ "
     rf"{Ч} = {Ч}, que é (par|ímpar)\.$", _условное_вопрос),
    (rf"^als n even is, is n \+ {Ч} even\? (ja|nee): {Ч} is even, en "
     rf"{Ч} \+ {Ч} = {Ч}, wat (even|oneven) is\.$", _условное_вопрос),
    (rf"^se n é par então n \+ {Ч} é par é falso: {Ч} é par, e {Ч} \+ "
     rf"{Ч} = {Ч}, que é ímpar\.$", _контр_условное),
    (rf"^als n even is, dan is n \+ {Ч} even is onwaar: {Ч} is even, "
     rf"en {Ч} \+ {Ч} = {Ч}, wat oneven is\.$", _контр_условное),
    (rf"^se n é par então n \+ m é par exatamente quando m é par: {Ч} "
     rf"é par e {Ч} \+ {Ч} = {Ч}, que é par\.$", _общ_условное),
    (rf"^als n even is, dan is n \+ m even precies wanneer m even is: "
     rf"{Ч} is even en {Ч} \+ {Ч} = {Ч}, wat even is\.$",
     _общ_условное),

    (rf"^f\(x\) = x × {Ч} é injetiva em 1, 2, 3\? (sim|não): ela dá "
     rf"{Ч}, {Ч}, {Ч}, "
     r"(todas diferentes|nem todas diferentes)\.$", _инъекция_вопрос),
    (rf"^is f\(x\) = x × {Ч} injectief op 1, 2, 3\? (ja|nee): zij "
     rf"geeft {Ч}, {Ч}, {Ч}, "
     r"(alle verschillend|niet alle verschillend)\.$",
     _инъекция_вопрос),
    (rf"^toda função é injetiva é falso: f\(x\) = x × 0 leva {Ч} e "
     rf"{Ч} ambos a 0\.$", _контр_инъекция),
    (rf"^elke functie is injectief is onwaar: f\(x\) = x × 0 stuurt "
     rf"{Ч} en {Ч} beide naar 0\.$", _контр_инъекция),
    (rf"^f\(x\) = x × k é injetiva exatamente quando k não é 0: para "
     rf"k = {Ч} as entradas 1 e 2 dão {Ч} e {Ч}\.$", _общ_инъекция),
    (rf"^f\(x\) = x × k is injectief precies wanneer k niet 0 is: bij "
     rf"k = {Ч} geven de invoeren 1 en 2 de waarden {Ч} en {Ч}\.$",
     _общ_инъекция),

    (rf"^qual é o quadrado de {Ч}\? {Ч} × {Ч} = {Ч}\.$", _квадрат),
    (rf"^wat is het kwadraat van {Ч}\? {Ч} × {Ч} = {Ч}\.$", _квадрат),
    (rf"^todo quadrado é par é falso: {Ч} é ímpar e {Ч} × {Ч} = {Ч}, "
     rf"que é ímpar\.$", _контр_квадрат),
    (rf"^elk kwadraat is even is onwaar: {Ч} is oneven en {Ч} × {Ч} = "
     rf"{Ч}, wat oneven is\.$", _контр_квадрат),
    (r"^o quadrado de um número (par|ímpar) é (par|ímpar): "
     rf"{Ч} × {Ч} = {Ч}\.$", _общ_квадрат),
    (r"^het kwadraat van een (even|oneven) getal is (even|oneven): "
     rf"{Ч} × {Ч} = {Ч}\.$", _общ_квадрат),
)
# УНИВЕРСАЛИЯ СПРАШИВАЕТСЯ СВОИМ «ВЕРНО ЛИ, ЧТО» (tools/universals.py): образец
# контрпримера или обобщения сварен с выведенным из него вопросом в ОДНО
# семейство (М-146); остальные образцы — как есть.
ЯЗЫКИ_МИРА = ('pt', 'nl')
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
        print(f"ДОЗНАНИЕ-PT-NL ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("ДОЗНАНИЕ-PT-NL ОТКАЗ: обход пуст, судить нечего")
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
    print(f"ДОЗНАНИЕ-PT-NL {поза}: {ложных} ложных из {судимых} "
          f"судимых ({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
