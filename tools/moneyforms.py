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


# THE RATE AS A SENTENCE (holon 04.09: the market of unit conversions buys the
# multiplier from «1 dollar = 100 cents.», and the svod had no such line for
# any other currency): the big unit in its one-form as the language names
# it whole («1 рубль», not the genitive of the decimal writing).
КУРС = {"de": "1 Euro = 100 Cent.", "fr": "1 euro = 100 centimes.", "es": "1 euro = 100 céntimos.", "it": "1 euro = 100 centesimi.",
        "pt": "1 euro = 100 cêntimos.", "nl": "1 euro = 100 cent.", "pl": "1 zł = 100 groszy.", "tr": "1 lira = 100 kuruş.", "ru": "1 рубль = 100 копеек."}


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
