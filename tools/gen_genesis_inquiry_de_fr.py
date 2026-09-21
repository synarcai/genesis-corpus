#!/usr/bin/env python3
"""GENESIS layer: THE LADDER OF INQUIRY IN GERMAN AND FRENCH.

Twenty-nine languages can COUNT and DECLINE. Two can REASON. Every
world that decides a case — inquiry, wagers, everyday, formulas —
speaks English and Russian and nothing else, so twenty-seven packs buy
the organism a vocabulary and no method. That gap is the reason this
layer exists, and it is not a gap of volume: a language that never
shows a DECIDED CASE teaches its words as labels.

THE LADDER IS THE ENGLISH-RUSSIAN ONE, UNCHANGED. Four rungs, and each
rung is a different act:

    ОПРЕДЕЛЕНИЕ  — what the notion IS, said in words and not shown,
                   and said TWICE: as a statement and as the answer to
                   its own question
    ИСПОЛНЕНИЕ   — a particular case DECIDED, with the ground beside
                   the verdict («nein: 91 = 7 × 13»)
    КОНТРПРИМЕР  — a universal claim KILLED by one witness
    ОБОБЩЕНИЕ    — the law the cases were instances of

Six genera declare their four rungs as functions over the pass number;
the machinery is written once. Adding a genus costs a declaration, and
adding a LANGUAGE costs a second string in every declaration — which is
the test that the ladder is a form and not an English habit.

ЯЗЫК ЕСТЬ ЧАСТЬ ФАКТА, А НЕ ЕГО ОДЕЖДА. Три вещи корпус не смеет
выучить неверно, и все три суть правила, а не описки:

  · ФРАНЦУЗСКИЙ СТАВИТ ПРОБЕЛ ПЕРЕД «?» И «:». «91 est-il premier ?»,
    «non : 91 = 7 × 13.» Тонкий неразрывный пробел — типографика
    французского, и написать «premier?» значит написать по-английски
    французскими словами;
  · НЕМЕЦКАЯ РАМКА ДЕРЖИТ ГЛАГОЛ НА КОНЦЕ: «ist 128 durch 8 teilbar?»
    — не «ist 128 teilbar durch 8»; во французском на том же месте
    стоит ИНВЕРСИЯ: «128 est-il divisible par 8 ?»;
  · НЕМЕЦКОЕ ИМЯ ПИШЕТСЯ С ПРОПИСНОЙ. «Primzahl», «Teiler», «Rest»,
    «Quadrat», «Summe» — это орфография, а не оформление: строчное имя
    в немецком есть ошибка, а корпус учит с полной судимостью. Начало
    предложения при этом остаётся строчным, как во всём корпусе:
    заглавная в начале строки НИЧЕГО не значит и потому не пишется.

ЧИСЛА ПИШУТСЯ ЦИФРАМИ, КАК В АНГЛИЙСКОМ И РУССКОМ БЛИЗНЕЦАХ. Ни одного
немецкого или французского числительного здесь не выдумано: там, где
слово было бы естественно, стоит цифра — та же, что у близнецов, и
потому сравнимая с ними. Таблицы `tools/langpacks/de.json` и `fr.json`
прочитаны ради этой проверки, а не ради заимствования.

ЯДРО ДОСЛОВНЫХ ПОВТОРОВ. Первые три случая каждой ступени берут семя
БЕЗ прохода и потому одинаковы во всех пяти проходах слово в слово;
остальные ходят числами. Форма чеканится повторностью — это замер, а не
мнение: слой, у которого каждый показ нов, не даёт дереву формы ни
одной опоры.

EVERY GROUND IS COMPUTED HERE AND RE-COMPUTED BY THE COURT.
`courts/inquiry_de_fr_court.py` factorises again, divides again, sums
the odd series again, and for a counterexample checks the WORK — that
the named witness really satisfies the premise and really breaks the
conclusion. A counterexample that does not refute is the most
convincing lie a corpus can carry, and its form is always correct.
"""

# ПРОЗВИЩЕ ДОМА В КУЗНЕ — `F` (21.09, обычай, читаемый прибором «РОД ДОШЁЛ»):
# ПРОЗВИЩЕ, ОБЪЯВЛЕННОЕ ОДИНАКОВО ВО ВСЕХ КУЗНЯХ, ВИДИТ УСТРОЙСТВО, а признак по
# окончанию имени видит лишь обычай. Кузня, звавшая дом иначе, не проверялась вовсе.
import pathlib  # noqa: E402
import sys  # noqa: E402

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layer import emit_grouped  # noqa: E402

# F ОТДЕЛЁН ОТ КУЗНИЦЫ (13.09): ступени, роды и словарь показов живут в
# `tools/inqdefr.py`, а кузница берёт у него готовые группы.
import inqdefr as F  # noqa: E402

ЦЕЛЬ = "datasets/genesis_inquiry_de_fr.txt"


def pass_groups(шаг):
    """Одна группа на РОД — сборка живёт в доме, кузница её лишь зовёт."""
    return F.группы(шаг)


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
