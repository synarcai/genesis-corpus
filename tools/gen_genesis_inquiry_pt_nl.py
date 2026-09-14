#!/usr/bin/env python3
"""GENESIS layer: THE LADDER OF INQUIRY IN PORTUGUESE AND DUTCH.

Twenty-nine languages can COUNT and DECLINE. Six can REASON. A pack
teaches an organism to count and to inflect; a LADDER teaches it to
DECIDE, and those are different things — which is why each of these
layers is not «one more language» but the carrying over of an ABILITY.
A language that never shows a DECIDED CASE teaches its words as labels.

THE LADDER IS THE ENGLISH-RUSSIAN ONE, UNCHANGED. Four rungs, and each
rung is a different act:

    ОПРЕДЕЛЕНИЕ  — what the notion IS, said in words and not shown,
                   and said TWICE: as a statement and as the answer to
                   its own question
    ИСПОЛНЕНИЕ   — a particular case DECIDED, with the ground beside
                   the verdict («não: 91 = 7 × 13»)
    КОНТРПРИМЕР  — a universal claim KILLED by one witness
    ОБОБЩЕНИЕ    — the law the cases were instances of

Six genera declare their four rungs as functions over the pass number;
the machinery is written once. Adding a genus costs a declaration, and
adding a LANGUAGE costs a second string in every declaration.

ЯЗЫК ЕСТЬ ЧАСТЬ ФАКТА, А НЕ ЕГО ОДЕЖДА:

  · ПОРТУГАЛЬСКОЕ «não» НЕСЁТ ТИЛЬДУ. Без неё это другое слово («nao»
    не значит ничего), и корпус, написавший его без знака, выучит
    несуществующее слово с полной судимостью — как выучил бы «пять»
    вместо «пять»;
  · НИДЕРЛАНДСКИЙ ВОПРОС СТАВИТ ГЛАГОЛ ПЕРВЫМ: «is 128 deelbaar door
    8?» — не «128 is deelbaar door 8?». В португальском на том же
    месте порядок слов не меняется вовсе, и вопрос несёт только знак:
    «128 é divisível por 8?». Два языка, две разные рамки одного
    вопроса, и обе показаны на одних числах;
  · СОСТАВНОЕ ЧИСЛИТЕЛЬНОЕ ПОРТУГАЛЬСКОГО ИДЁТ СО СВЯЗКОЙ «e»
    («noventa e nove»), и пакет объявляет её полем `numeral_connectors`.
    Здесь такого случая не возникает: числа этого мира пишутся ЦИФРАМИ
    (см. ниже), и связке негде прозвучать. Правило названо, чтобы оно
    не было нарушено молча, если мир когда-нибудь заговорит словами.

ЧИСЛА ПИШУТСЯ ЦИФРАМИ, КАК ВО ВСЕХ ЧЕТЫРЁХ БЛИЗНЕЦАХ ЭТОЙ ЛЕСТНИЦЫ
(английском, русском, немецком, французском). Ни одного португальского
или нидерландского числительного здесь не выдумано: цифра стоит там,
где слово было бы естественно, и потому показ сравним с близнецами
слово в слово. Таблицы `tools/langpacks/pt.json` и `nl.json` прочитаны
ради проверки, что ни одно числительное не просочилось, а не ради
заимствования.

КОПУЛА ЭТИХ ДВУХ ЯЗЫКОВ ОБЪЯВЛЕНА ЗНАКОМ РАВЕНСТВА, и это надо знать,
берясь за них. `pt.json` объявляет «é» знаком «=», `nl.json` — «is»:
арифметический суд корпуса читает ОБА как равенство, потому что так
сказали сами пакеты. Оттого почти каждая связочная фраза этих языков
приходит к нему с признаком равенства на борту. Спасают её два
объявленных закона суда — «равенство без единой операции не утверждает
арифметики» и «цепь равенств читается только в чистой записи», — и
спасают ПОЛНОСТЬЮ: замер по всему слою даёт ноль ложных. Но закон этот
не наш, а чужого дома, и потому проверен числом, а не доверием.

ЯДРО ДОСЛОВНЫХ ПОВТОРОВ. Первые три случая каждой ступени берут семя
БЕЗ прохода и потому одинаковы во всех пяти проходах слово в слово;
остальные ходят числами. Форма чеканится повторностью — это замер, а не
мнение.

ОБЕ ВЕТВИ ВЕРДИКТА ОБЯЗАНЫ ЗВУЧАТЬ, И ЭТО ПРОВЕРЕНО ЧИСЛОМ. Слой, у
которого «sim» не сказано ни разу, зелен у всякого суда и молчит о
половине рода: он не лжёт, он не показывает. Ряды простоты и делимости
подобраны так, чтобы обе ветви покупались повторностью, и охват ветвей
меряется стендом.

EVERY GROUND IS COMPUTED HERE AND RE-COMPUTED BY THE COURT.
`courts/inquiry_pt_nl_court.py` factorises again, divides again, sums
the odd series again, and for a counterexample checks the WORK — that
the named witness really satisfies the premise and really breaks the
conclusion. A counterexample that does not refute is the most
convincing lie a corpus can carry, and its form is always correct.
"""

import pathlib  # noqa: E402
import sys  # noqa: E402

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layer import emit_grouped  # noqa: E402

# ДОМ ОТДЕЛЁН ОТ КУЗНИЦЫ (13.09): ступени, роды и словарь показов живут в
# `tools/inqptnl.py`, а кузница берёт у него готовые группы.
import inqptnl as ДОМ  # noqa: E402

ЦЕЛЬ = "datasets/genesis_inquiry_pt_nl.txt"


def pass_groups(шаг):
    """Одна группа на РОД — сборка живёт в доме, кузница её лишь зовёт."""
    return ДОМ.группы(шаг)


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
