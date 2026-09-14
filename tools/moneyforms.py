#!/usr/bin/env python3
"""THE HOUSE OF MONEY WRITINGS — the decimal comma, nine languages.

The svod wrote money as «16.50 dollars» / «$16.50» (en) and «16 рублей 50
копеек» (ru). Europe writes the same price with a COMMA — «16,50 Euro»,
«16,50 euros», «16,50 zł» — and the organism never saw that writing. This
house declares, per language, the big and the small unit with their count
forms, the copula of the bridge, the question of the small unit and the
colon of the ledger; the generator and the court read one table. The cents
stay the axis: every decimal writing stands beside its whole number of
cents with the ledger between them, as the money world does (e9 04.09).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import holes  # noqa: E402
import rugram  # noqa: E402

# per language: big unit forms (one, many), small unit (one, few, many),
# bridge copula, question of the small unit («how many cents is {}»),
# «is» for the way back (the small unit as subject), the ledger colon
ЯЗЫКИ = {
    "de": dict(б=("Euro", "Euro"), м=("Cent", "Cent", "Cent"), есть="sind", вопрос="wie viel {м} sind {б}?", дв=": "),
    "fr": dict(б=("euro", "euros"), м=("centime", "centimes", "centimes"), есть="font", вопрос="combien de {м} font {б} ?", дв=" : "),
    "es": dict(б=("euro", "euros"), м=("céntimo", "céntimos", "céntimos"), есть="son", вопрос="¿cuántos {м} son {б}?", дв=": "),
    "it": dict(б=("euro", "euro"), м=("centesimo", "centesimi", "centesimi"), есть="sono", вопрос="quanti {м} sono {б}?", дв=": "),
    "pt": dict(б=("euro", "euros"), м=("cêntimo", "cêntimos", "cêntimos"), есть="são", вопрос="quantos {м} são {б}?", дв=": "),
    "nl": dict(б=("euro", "euro"), м=("cent", "cent", "cent"), есть="is", вопрос="hoeveel {м} is {б}?", дв=": "),
    "pl": dict(б=("zł", "zł"), м=("grosz", "grosze", "groszy"), есть="to", вопрос="ile {м} to {б}?", дв=": "),
    "tr": dict(б=("lira", "lira"), м=("kuruş", "kuruş", "kuruş"), есть="", вопрос="{б} kaç {м}?", дв=": "),
    "ru": dict(б=("рубля", "рубля"), м=("копейка", "копейки", "копеек"), есть="— это", вопрос="сколько {м} в {б}?", дв=": "),
}

# ИМЕНА РОДОВ ДЛЯ ПЕРЕПИСИ ДОМОВ (`scripts/houses_census.py`): она печатает их тому, кто ищет
# в своде дыру, — чтобы дом не был построен второй раз.
#
# ЗДЕСЬ РОД НЕЛЬЗЯ ВЫВЕСТИ ИЗ ТАБЛИЦЫ, И ЭТО СКАЗАНО, А НЕ ОБОЙДЕНО. Ключ у неё есть лишь у
# ВОПРОСА; рамка утверждения («310 Cent sind 3,10 Euro: 3 × 100 = 300, 310 − 300 = 10») здесь
# не объявлена строкой, а СОБИРАЕТСЯ В КОДЕ из крупной единицы, мелкой, связки и двоеточия
# леджера («б», «м», «есть», «дв»). Потому имена пишутся явно — и `assert` держит при таблице
# то, что в ней есть: изменится её состав, и дом упадёт на ввозе, а не смолчит.
_КЛЮЧИ_ТАБЛИЦЫ = frozenset({"б", "м", "есть", "дв", "вопрос"})
assert _КЛЮЧИ_ТАБЛИЦЫ <= set(next(iter(ЯЗЫКИ.values()))), "состав таблицы ЯЗЫКИ изменился"
# ЧЕТЫРЕ РОДА ДОПИСАНЫ ПО ДЕЛУ СТРОИТЕЛЯ (13.09). Дом объявлял два рода, а кузница строила
# ШЕСТЬ разных дел: сам курс, курс на целом числе, мост, вопрос о мосте, обратный ход и сумму.
# Объявление, беднее дела, есть не скромность, а слепое пятно указателя.
#
#     ДОМ, ОБЪЯВИВШИЙ МЕНЬШЕ РОДОВ, ЧЕМ СТРОИТ ЕГО КУЗНИЦА, ПРЯЧЕТ РАЗНИЦУ ПОД ОБЩИМ ИМЕНЕМ.
РОДЫ = ("мелкая единица, писанная крупной через запятую, с леджером",
        "вопрос о том же размене, отвечаемый тем же утверждением",
        "курс, сказанный предложением",
        "курс на целом числе",
        "обратный ход: из крупной в мелкую",
        "сумма двух размеров")



# THE RATE AS A SENTENCE (holon 04.09: the market of unit conversions buys the
# multiplier from «1 dollar = 100 cents.», and the svod had no such line for
# any other currency): the big unit in its one-form as the language names
# it whole («1 рубль», not the genitive of the decimal writing).
КУРС = {"de": "1 Euro = 100 Cent.", "fr": "1 euro = 100 centimes.", "es": "1 euro = 100 céntimos.", "it": "1 euro = 100 centesimi.",
        "pt": "1 euro = 100 cêntimos.", "nl": "1 euro = 100 cent.", "pl": "1 zł = 100 groszy.", "tr": "1 lira = 100 kuruş.", "ru": "1 рубль = 100 копеек."}


def курс_целый(язык, n):
    """«2 Euro = 200 Cent.», «3 рубля = 300 копеек.», «7 zł = 700 groszy.» —
    the rate at a whole number (holon 03.09: the market of unit conversions
    buys a rate from ≥ 2 DIFFERENT pairs (v1, v2); ten lines of «1 Euro = 100
    Cent.» are one pair)."""
    я = ЯЗЫКИ[язык]
    if язык == "ru":
        б = f"{n} {rugram.форма('рубль', n)}"
    else:
        б = f"{n} {я['б'][0] if n == 1 else я['б'][1]}"
    return f"{б} = {мелкая(язык, n * 100)}."


def запись(d, c):
    """«16,50» — the decimal comma, two digits of cents."""
    return f"{d},{c:02d}"


def большая(язык, d, c):
    """«16,50 Euro» — after a decimal the big unit takes its declared form
    (Russian: the genitive singular «рубля», as the language reads «16,50»)."""
    return f"{запись(d, c)} {ЯЗЫКИ[язык]['б'][1]}"


def мелкая(язык, n):
    """«1650 Cent», «1650 groszy», «1650 копеек» — the small unit by count."""
    формы = ЯЗЫКИ[язык]["м"]
    if язык == "ru":
        return f"{n} {rugram.форма('копейка', n)}"
    if язык == "pl":
        return f"{n} {формы[('one', 'few', 'many').index(holes.форма_счёта('pl', n))]}"
    return f"{n} {формы[0] if n == 1 else формы[2]}"


def мост(язык, d, c):
    я = ЯЗЫКИ[язык]
    всего = d * 100 + c
    леджер = f"{d} × 100 = {d * 100}, {d * 100} + {c} = {всего}"
    если = f" {я['есть']}" if я["есть"] else ""
    if язык == "tr":
        return f"{большая(язык, d, c)} {всего} kuruştur{я['дв']}{леджер}."
    return f"{большая(язык, d, c)}{если} {мелкая(язык, всего)}{я['дв']}{леджер}."


def вопрос(язык, d, c):
    я = ЯЗЫКИ[язык]
    всего = d * 100 + c
    леджер = f"{d} × 100 = {d * 100}, {d * 100} + {c} = {всего}"
    м = я["м"][2] if язык != "ru" else "копеек"
    if язык == "tr":
        q = "{б} kaç kuruştur?".format(б=большая(язык, d, c))
        return f"{q} {леджер} kuruş."
    q = я["вопрос"].format(м=м, б=большая(язык, d, c))
    хвост = мелкая(язык, всего).split(" ", 1)[1]
    return f"{q} {леджер} {хвост}."


def обратно(язык, d, c):
    я = ЯЗЫКИ[язык]
    всего = d * 100 + c
    леджер = f"{d} × 100 = {d * 100}, {всего} − {d * 100} = {c}"
    if язык == "tr":
        return f"{мелкая(язык, всего)} {запись(d, c)} liradır{я['дв']}{леджер}."
    если = f" {я['есть']}" if я["есть"] else ""
    return f"{мелкая(язык, всего)}{если} {большая(язык, d, c)}{я['дв']}{леджер}."


def сумма(язык, a, ac, b, bc):
    я = ЯЗЫКИ[язык]
    A, B = a * 100 + ac, b * 100 + bc
    S = A + B
    s, sc = divmod(S, 100)
    return (f"{большая(язык, a, ac)} + {большая(язык, b, bc)} = {большая(язык, s, sc)}"
            f"{я['дв']}{A} + {B} = {мелкая(язык, S)}.")


# РОД, ЧЬЁ ЧИСЛО СТРАНИЦ ЕСТЬ ФАКТ О ЯЗЫКАХ, А НЕ ВЫБОР ДОМА (13.09).
#
# «Курс, сказанный предложением» есть ОДНО предложение на язык: «1 euro = 100 cents». Языков
# в доме девять — стало быть, и различных страниц девять, и десятой взяться неоткуда. Свод при
# этом показывает каждую ДЕСЯТЬ раз (кузница кладёт её дважды за проход), и это нарочно:
#
#     ЯДРО ДОСЛОВНЫХ ПОВТОРОВ ЕСТЬ ЗАКОН КОРПУСА, А НЕ НЕДОСМОТР: форма покупается
#     повторением. Но мера ровности считает РАЗЛИЧНЫЕ страницы — и род, чьи страницы
#     повторяются нарочно, кажется ей тощим.
#
#     РОД, ЧЬЁ ЧИСЛО СТРАНИЦ ЕСТЬ ФАКТ О ПРЕДМЕТЕ, НЕ ПОДЛЕЖИТ МЕРЕ РОВНОСТИ — НО ОБЯЗАН
#     БЫТЬ ОБЪЯВЛЕН ТАКОВЫМ.
РОДЫ_ПО_ПРЕДМЕТУ = {
    "курс, сказанный предложением": "курс есть ОДНО предложение на язык, а языков девять; "
                                    "свод повторяет каждое десятикратно нарочно, и мера "
                                    "различных страниц видит девять",
}

# ------------------------------------------------------------------ СТРАНИЦЫ МИРА

ШИРИНА = 8

def язык_группа(шаг, язык):
    вон = [КУРС[язык], КУРС[язык]]     # the rate as a sentence, ten times over the passes
    # …and at two whole numbers per pass, ten different ones over the passes
    # (holon 03.09: the market of conversions wants ≥ 2 different pairs)
    for h in range(2):
        вон.append(курс_целый(язык, 2 + (шаг * 2 + h + (шаг >= 3)) % 11))
    for i in range(ШИРИНА):
        d = 3 + (шаг * 7 + i * 5) % 40
        c = 5 * ((шаг * 3 + i * 7) % 18 + 2)          # 10..95, as the money world
        вон.append(мост(язык, d, c) if i % 2 == 0 else вопрос(язык, d, c))
        вон.append(обратно(язык, d, c))
        a, ac = 2 + (шаг * 5 + i * 3) % 30, 5 * ((шаг + i * 3) % 19 + 1)
        b, bc = 1 + (шаг * 3 + i * 7) % 20, 5 * ((шаг * 7 + i) % 19 + 1)
        вон.append(сумма(язык, a, ac, b, bc))
    return вон


def _меченая(шаг, язык):
    """[(страница, род)] — та же группа языка, но каждая страница под своим именем."""
    мост_р, вопрос_р, курс_р, целый_р, обратно_р, сумма_р = РОДЫ
    вон = [(КУРС[язык], курс_р), (КУРС[язык], курс_р)]
    for h in range(2):
        вон.append((курс_целый(язык, 2 + (шаг * 2 + h + (шаг >= 3)) % 11), целый_р))
    for i in range(ШИРИНА):
        d = 3 + (шаг * 7 + i * 5) % 40
        c = 5 * ((шаг * 3 + i * 7) % 18 + 2)
        вон.append((мост(язык, d, c), мост_р) if i % 2 == 0
                   else (вопрос(язык, d, c), вопрос_р))
        вон.append((обратно(язык, d, c), обратно_р))
        a, ac = 2 + (шаг * 5 + i * 3) % 30, 5 * ((шаг + i * 3) % 19 + 1)
        b, bc = 1 + (шаг * 3 + i * 7) % 20, 5 * ((шаг * 7 + i) % 19 + 1)
        вон.append((сумма(язык, a, ac, b, bc), сумма_р))
    return вон


def группы(шаг):
    """[[страница]] — ровно те группы и в том порядке, какими кузница кормит `emit_grouped`."""
    return [язык_группа(шаг, язык) for язык in ЯЗЫКИ]


def перебор_страниц(шаг):
    вон = []
    for язык in ЯЗЫКИ:
        вон.extend(_меченая(шаг, язык))
    return вон


def _показы():
    """{строка свода: род} — ПОСТРОЧНО, ибо свод построчен."""
    from layer import PASSES                              # noqa: PLC0415
    вон = {}
    for шаг in range(len(PASSES)):
        for с, род in перебор_страниц(шаг):
            for строка in с.split("\n"):
                if строка.rstrip():
                    вон.setdefault(строка.rstrip(), род)
    return вон


ПОКАЗЫ = _показы()


def _самопроверка_страниц():
    assert all("\n" not in к for к in ПОКАЗЫ), "словарь показов обязан быть построчным"
    пустые = set(РОДЫ) - set(ПОКАЗЫ.values())
    assert not пустые, f"род объявлен и не кован: {sorted(пустые)}"
    из_перебора = sorted(с for с, _р in перебор_страниц(0))
    из_групп = sorted(с for г in группы(0) for с in г)
    assert из_перебора == из_групп, "пересборка потеряла или выдумала страницы"


_самопроверка_страниц()


def _проверить_предметные():
    """Объявленное «по предмету» сверяется со страницами, а не остаётся прозой."""
    есть = {}
    for _с, род in ПОКАЗЫ.items():
        есть[род] = есть.get(род, 0) + 1
    имя = "курс, сказанный предложением"
    assert есть.get(имя) == len(ЯЗЫКИ), (
        f"род «{имя}» обещан по одной странице на язык ({len(ЯЗЫКИ)}), а дал {есть.get(имя)}")


_проверить_предметные()

