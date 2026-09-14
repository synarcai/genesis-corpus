#!/usr/bin/env python3
"""GENESIS layer: SHARES IN EIGHT LANGUAGES — «two thirds of 12».

The owner's word: every language in surplus. The share world says «two
thirds of 12 is 8» with its ledger in en/ru; this world says seven shares
(the half, a third, two thirds, a quarter, three quarters, a fifth, two
fifths) of a number in de/fr/es/it/pt/nl/pl/tr, statement and question
answered by the statement (М-153), the ledger the division and — at a
numerator above one — the multiplication. The house of share names
(tools/shareforms.py) holds the names and copulas; the court reads the
share back from its name and recomputes.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import shareforms as F  # noqa: E402
from layer import Сбор, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_share_langs.txt"


# ЧИСЛИТЕЛЬ И ЕСТЬ РОД, И ДОМ ЕГО УЖЕ СЧИТАЕТ (14.09): у `shareforms` слово доли берётся
# «с[0 if ч == 1 else 1]» — единичная доля зовётся иначе, чем доля из нескольких частей, и
# дело у них разное: первая есть ОДНО деление, вторая — деление И умножение. Язык рассказа и
# лицо речи (утверждение или вопрос) родами не служат.
ЕДИНИЧНАЯ = "единичная доля: одно деление"
СОСТАВНАЯ = "доля из нескольких частей: деление и умножение над ним"


def язык_группа(шаг, язык):
    вон = Сбор()
    for i, (ч, з) in enumerate(F.ДОЛИ):
        вон.род = ЕДИНИЧНАЯ if ч == 1 else СОСТАВНАЯ
        n = з * (2 + (шаг * 5 + i * 3) % 12)
        вон.append(F.утверждение(язык, i, n) if (шаг + i) % 2 == 0 else F.вопрос(язык, i, n))
        n2 = з * (2 + (шаг * 7 + i * 5 + 1) % 12)
        вон.append(F.вопрос(язык, i, n2) if (шаг + i) % 2 == 0 else F.утверждение(язык, i, n2))
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


# --------------------------------------------------------------- ОБЪЯВЛЕНИЕ ДОМА

РОДЫ = (ЕДИНИЧНАЯ, СОСТАВНАЯ)

ЗАЧЕМ_РОДА = {
    ЕДИНИЧНАЯ: "«половина от 8 — это 4»: n ÷ з, один шаг, и своё слово доли",
    СОСТАВНАЯ: "«две пятых от 10 — это 4»: n ÷ з × ч, два шага, и слово доли иное",
}


def группы(шаг):
    return pass_groups(шаг)


def страницы(шаг):
    return [с for г in группы(шаг) for с in г]


def перебор_страниц(шаг):
    return [п for г in группы(шаг) for п in г.парами]


def _показы():
    from layer import PASSES                             # noqa: PLC0415
    вон = {}
    for ш in range(len(PASSES)):
        for с, род in перебор_страниц(ш):
            for строка in с.split("\n"):
                if строка.rstrip():
                    вон.setdefault(строка.rstrip(), род)
    return вон


ПОКАЗЫ = _показы()


def _самопроверка_дома():
    assert set(ЗАЧЕМ_РОДА) == set(РОДЫ), "глосса рода разошлась с объявлением"
    пустые = set(РОДЫ) - set(ПОКАЗЫ.values())
    assert not пустые, f"род объявлен и не кован: {sorted(пустые)}"


_самопроверка_дома()


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
