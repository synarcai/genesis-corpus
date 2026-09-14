#!/usr/bin/env python3
"""THE HOUSE OF PROGRESSION PHRASES — the k-th term in eight languages.

The sequences world says «term number 5 of the progression from 9 with
step 4 is 25: 5 − 1 = 4, 4 × 4 = 16, 9 + 16 = 25» in en/ru; this house says
the same in de/fr/es/it/pt/nl/pl/tr, statement and question answered by
the statement (М-153), the ledger unchanged. Generator and court read one
table through tools/phrases.py.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import phrases  # noqa: E402

ЯЗЫКИ = {
    "de": dict(утв="das Glied Nummer {k} der Folge ab {a} mit Schritt {d} ist {v}: {л}.", воп="was ist das Glied Nummer {k} der Folge ab {a} mit Schritt {d}?"),
    "fr": dict(утв="le terme numéro {k} de la progression partant de {a} avec le pas {d} est {v} : {л}.", воп="quel est le terme numéro {k} de la progression partant de {a} avec le pas {d} ?"),
    "es": dict(утв="el término número {k} de la progresión desde {a} con paso {d} es {v}: {л}.", воп="¿cuál es el término número {k} de la progresión desde {a} con paso {d}?"),
    "it": dict(утв="il termine numero {k} della progressione da {a} con passo {d} è {v}: {л}.", воп="qual è il termine numero {k} della progressione da {a} con passo {d}?"),
    "pt": dict(утв="o termo número {k} da progressão desde {a} com passo {d} é {v}: {л}.", воп="qual é o termo número {k} da progressão desde {a} com passo {d}?"),
    "nl": dict(утв="term nummer {k} van de rij vanaf {a} met stap {d} is {v}: {л}.", воп="wat is term nummer {k} van de rij vanaf {a} met stap {d}?"),
    "pl": dict(утв="wyraz numer {k} ciągu od {a} o kroku {d} to {v}: {л}.", воп="ile wynosi wyraz numer {k} ciągu od {a} o kroku {d}?"),
    "tr": dict(утв="{a} ile başlayan ve adımı {d} olan dizinin {k} numaralı terimi: {л}.", воп="{a} ile başlayan ve adımı {d} olan dizinin {k} numaralı terimi kaçtır?"),
}

# ИМЕНА РОДОВ ДЛЯ ПЕРЕПИСИ ДОМОВ (`scripts/houses_census.py`): она печатает их тому, кто ищет
# в своде дыру, — чтобы дом не был построен второй раз. Имена ВЫВОДЯТСЯ ИЗ таблицы `ЯЗЫКИ`, а
# не пишутся рядом с нею: список, живущий отдельно, расходится с делом на первой же правке, а
# этот на новом ключе без имени валит дом ПРЯМО НА ВВОЗЕ.
_ИМЯ_РОДА = {"утв": "утверждение с леджером прогрессии", "воп": "вопрос, отвечаемый тем же утверждением"}
РОДЫ = tuple(_ИМЯ_РОДА[к] for к in next(iter(ЯЗЫКИ.values())))

ДЫРЫ = {"k": r"(\d+)", "a": r"(\d+)", "d": r"(\d+)", "v": r"(\d+)", "л": r"(\d+ − 1 = \d+, \d+ × \d+ = \d+, \d+ \+ \d+ = \d+)"}


def леджер(k, a, d):
    return f"{k} − 1 = {k - 1}, {k - 1} × {d} = {(k - 1) * d}, {a} + {(k - 1) * d} = {a + (k - 1) * d}"


def утверждение(язык, k, a, d):
    return ЯЗЫКИ[язык]["утв"].format(k=k, a=a, d=d, v=a + (k - 1) * d, л=леджер(k, a, d))


def вопрос(язык, k, a, d):
    return f"{ЯЗЫКИ[язык]['воп'].format(k=k, a=a, d=d)} {утверждение(язык, k, a, d)}"


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
    k, a, d = int(з["k"]), int(з["a"]), int(з["d"])
    if k < 2 or з["л"] != леджер(k, a, d):
        return False
    if "v" in з and int(з["v"]) != a + (k - 1) * d:
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
        k = 2 + (шаг * 3 + i) % 7
        a = 2 + (шаг * 5 + i * 3) % 20
        d = 1 + (шаг * 2 + i * 5) % 9
        вон.append(утверждение(язык, k, a, d) if i % 2 == 0 else вопрос(язык, k, a, d))
    return вон

def _меченая(шаг, язык):
    """[(страница, род)] — прогрессия утверждением и вопросом."""
    утв, воп = РОДЫ
    вон = []
    for i in range(8):
        k = 2 + (шаг * 3 + i) % 7
        a = 2 + (шаг * 5 + i * 3) % 20
        d = 1 + (шаг * 2 + i * 5) % 9
        вон.append((утверждение(язык, k, a, d), утв) if i % 2 == 0
                   else (вопрос(язык, k, a, d), воп))
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
