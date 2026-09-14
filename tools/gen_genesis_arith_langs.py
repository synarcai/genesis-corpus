#!/usr/bin/env python3
"""GENESIS layer: THE VALUE ASKED IN TEN LANGUAGES.

The owner's word (03.09): every language in surplus. The svod asked the
value of an expression in English and Russian only («what is 3 + 4?»,
«сколько будет 3 + 4?»); in de/fr/es/it/pl/pt/nl/tr the question of value
had no shows at all (34 lines, one Italian world). This world asks it with
the forms the packs declare (ask_forms.value: the question in two forms and
the task form — «was ist {}?», «wie viel ist {}?», «berechne {}.»; Turkish
puts the question word at the end: «{} kaç eder?») over the four operations,
and the answer is the one telling the corpus has for a value: the equation
«3 + 4 = 7.», recomputed by the court of arithmetic; the house of the pair
binds the question to the answer by the form of value (М-156), so a changed
number in the question is caught.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import paraphrase  # noqa: E402
from layer import Сбор, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_arith_langs.txt"
# en and ru too (holon 04.09: the English heads «what's 47 + 38?», «what is the
# result of 47 + 38?», «compute …», «evaluate …» were mute — the paraphrase
# market wants the frame's words shown): every value form of the packs cycles.
ЯЗЫКИ = ("de", "fr", "es", "it", "pl", "pt", "nl", "tr", "en", "ru")
# THE OPERATION IS A WORD OF THE FRAME (holon 04.09: «what's # + #» and
# «what's # − #» are two frames, each wanting LAW ≥ 4 distinct shows — with
# eight English forms over four operations, two shows a frame left the
# market honestly mute): a pass shows eight expressions per form, so every
# (form, operation) frame carries ten shows over the five passes.
ПОКАЗОВ_НА_ФОРМУ = 8


def выражение(шаг, i, оп):
    """(expression, value) of operation оп (0..3), exact division."""
    a = 3 + (шаг * 7 + i * 5) % 40
    b = 2 + (шаг * 3 + i * 11) % 12
    if оп == 0:
        return f"{a} + {b}", a + b
    if оп == 1:
        a, b = max(a, b), min(a, b)
        return f"{a} − {b}", a - b
    if оп == 2:
        return f"{a} × {b}", a * b
    q = 2 + (шаг * 5 + i) % 9
    return f"{b * q} ÷ {b}", q


# ДЕЙСТВИЕ И ЕСТЬ РОД, И ОНО УЖЕ СОСЧИТАНО ПЕРЕМЕННОЙ `оп` (14.09). Язык рассказа и форма
# вопроса — не роды: одно и то же сложение спрашивается всеми объявленными формами на всех
# языках, и в том весь замысел мира («EVERY FORM MEETS EVERY OPERATION»).
РОД_ДЕЙСТВИЯ = ("сложение, спрошенное всеми формами",
                "вычитание, спрошенное всеми формами",
                "умножение, спрошенное всеми формами",
                "деление нацело, спрошенное всеми формами")


def язык_группа(шаг, язык):
    """EVERY FORM MEETS EVERY OPERATION (holon 04.09: with form and operation
    both cycling by шаг + i, «what is the result of …» met only «−» and the
    head was bought for subtraction alone): the show index k walks the
    forms, k ÷ forms walks the operations."""
    формы = paraphrase.формы(язык, "value")
    ширина = ПОКАЗОВ_НА_ФОРМУ * len(формы)
    вон = Сбор()
    for i in range(ширина):
        k = шаг * ширина + i
        форма = формы[k % len(формы)]
        оп = (k // len(формы)) % 4
        в, з = выражение(шаг, i, оп)
        вон.род = РОД_ДЕЙСТВИЯ[оп]
        вон.append(f"{форма.format(в)} {в} = {з}.")
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in ЯЗЫКИ]


# --------------------------------------------------------------- ОБЪЯВЛЕНИЕ ДОМА

РОДЫ = РОД_ДЕЙСТВИЯ

ЗАЧЕМ_РОДА = {
    РОД_ДЕЙСТВИЯ[0]: "a + b на всех объявленных языках и всеми формами вопроса",
    РОД_ДЕЙСТВИЯ[1]: "a − b, где уменьшаемое всегда не меньше вычитаемого",
    РОД_ДЕЙСТВИЯ[2]: "a × b теми же формами",
    РОД_ДЕЙСТВИЯ[3]: "деление, взятое ТОЛЬКО нацело: мир не знает записи для остатка",
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
