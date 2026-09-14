#!/usr/bin/env python3
"""THE HOUSE OF REMAINDER PHRASES — division with a remainder in eight languages.

The remainders world says «17 divided by 5 is 3 remainder 2: 5 × 3 = 15,
17 − 15 = 2» and «17 разделить на 5 будет 3, остаток 2: …» in en/ru; this
house says the same in de/fr/es/it/pt/nl/pl/tr, statement and question
answered by the statement (М-153), the ledger of the division unchanged
(holon 03.09, ONE-CARRIER: the answer that is computed shows its steps).
Generator and court read one table through tools/phrases.py (М-159).
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import phrases  # noqa: E402

ЯЗЫКИ = {
    "de": dict(утв="{a} geteilt durch {b} ist {q} Rest {r}: {л}.", воп="was ist {a} geteilt durch {b}?"),
    "fr": dict(утв="{a} divisé par {b} fait {q} reste {r} : {л}.", воп="combien font {a} divisé par {b} ?"),
    "es": dict(утв="{a} dividido entre {b} es {q} con resto {r}: {л}.", воп="¿cuánto es {a} dividido entre {b}?"),
    "it": dict(утв="{a} diviso {b} fa {q} con resto {r}: {л}.", воп="quanto fa {a} diviso {b}?"),
    "pt": dict(утв="{a} dividido por {b} é {q} com resto {r}: {л}.", воп="quanto é {a} dividido por {b}?"),
    "nl": dict(утв="{a} gedeeld door {b} is {q} rest {r}: {л}.", воп="wat is {a} gedeeld door {b}?"),
    "pl": dict(утв="{a} podzielone przez {b} to {q} reszta {r}: {л}.", воп="ile to {a} podzielone przez {b}?"),
    "tr": dict(утв="{a} bölü {b} eşittir {q} kalan {r}: {л}.", воп="{a} bölü {b} kaçtır?"),
}

# ИМЕНА РОДОВ ДЛЯ ПЕРЕПИСИ ДОМОВ (`scripts/houses_census.py`): она печатает их тому, кто ищет
# в своде дыру, — чтобы дом не был построен второй раз. Имена ВЫВОДЯТСЯ ИЗ таблицы `ЯЗЫКИ`, а
# не пишутся рядом с нею: список, живущий отдельно, расходится с делом на первой же правке, а
# этот на новом ключе без имени валит дом ПРЯМО НА ВВОЗЕ.
_ИМЯ_РОДА = {"утв": "утверждение с леджером деления", "воп": "вопрос, отвечаемый тем же утверждением"}
РОДЫ = tuple(_ИМЯ_РОДА[к] for к in next(iter(ЯЗЫКИ.values())))

ДЫРЫ = {"a": r"(\d+)", "b": r"(\d+)", "q": r"(\d+)", "r": r"(\d+)", "л": r"(\d+ × \d+ = \d+, \d+ − \d+ = \d+)"}


def леджер(a, b):
    q, r = divmod(a, b)
    return f"{b} × {q} = {b * q}, {a} − {b * q} = {r}"


def утверждение(язык, a, b):
    q, r = divmod(a, b)
    return ЯЗЫКИ[язык]["утв"].format(a=a, b=b, q=q, r=r, л=леджер(a, b))


def вопрос(язык, a, b):
    return f"{ЯЗЫКИ[язык]['воп'].format(a=a, b=b)} {утверждение(язык, a, b)}"


def образцы(язык):
    я = ЯЗЫКИ[язык]
    утв = phrases.образец(я["утв"], ДЫРЫ)
    return [(re.compile("^" + утв + "$"), False),
            (re.compile("^" + phrases.образец(я["воп"], ДЫРЫ) + " " + утв + "$"), True)]


def судить_группы(язык, спрошено, группы):
    я = ЯЗЫКИ[язык]
    г = list(группы)
    спрош = {}
    if спрошено:
        имена = phrases.порядок(я["воп"])
        спрош = dict(zip(имена, г[:len(имена)])); г = г[len(имена):]
    з = dict(zip(phrases.порядок(я["утв"]), г))
    a, b, q, r = int(з["a"]), int(з["b"]), int(з["q"]), int(з["r"])
    # THE REMAINDER IS NEVER ZERO IN THIS HOUSE (as in the remainders world:
    # a «remainder 0» show would teach that the genus and the quotient coincide)
    if b < 2 or r == 0 or divmod(a, b) != (q, r) or з["л"] != леджер(a, b):
        return False
    return all(int(спрош[имя]) == int(з[имя]) for имя in спрош)


# ------------------------------------------------------------------ СТРАНИЦЫ МИРА
#
# СТРОИТЕЛЬ ПЕРЕЕХАЛ ИЗ КУЗНИЦЫ В ДОМ (13.09) — тем же движением, что стало обычаем.
#
#     ДОМ, ОБЪЯВИВШИЙ РОДЫ И НЕ ОТДАВШИЙ СТРАНИЦ, ОБЕЩАЕТ ИМЕНА, КОТОРЫХ НЕКОМУ ПРИЛОЖИТЬ.

def язык_группа(шаг, язык):
    вон = []
    for i in range(8):
        b = 2 + (шаг * 3 + i * 5) % 8                 # 2..9
        q = 2 + (шаг * 5 + i * 3) % 9                 # 2..10
        r = 1 + (шаг * 7 + i * 11) % (b - 1)          # 1..b−1 — never zero
        a = b * q + r
        вон.append(утверждение(язык, a, b) if i % 2 == 0 else вопрос(язык, a, b))
    return вон

def _меченая(шаг, язык):
    """[(страница, род)] — остаток утверждением и вопросом."""
    утв, воп = РОДЫ
    вон = []
    for i in range(8):
        b = 2 + (шаг * 3 + i * 5) % 8
        q = 2 + (шаг * 5 + i * 3) % 9
        r = 1 + (шаг * 7 + i * 11) % (b - 1)
        a = b * q + r
        вон.append((утверждение(язык, a, b), утв) if i % 2 == 0
                   else (вопрос(язык, a, b), воп))
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
    """Словарь ПОСТРОЧНО: свод построчен, а показ бывает многострочен."""
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
