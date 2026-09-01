#!/usr/bin/env python3
"""GENESIS layer: THE AVERAGE — a number that stands FOR a row of numbers.

The organism owns no notion of an average at all. The statistics layer
says «the mean of 2 4 6 is 4» and stops there: the number is ASSERTED
and its ground is nowhere. A show that gives the answer without the
work teaches an ORACLE — that averages are things one is told — and an
oracle is exactly what a researcher must not become.

WHAT THIS WORLD SHOWS, AND WHY EACH RUNG EXISTS:

    ОСНОВАНИЕ    the average said TOGETHER with the two quantities it
                 is made of: «their sum is 15 and there are 3 of them».
                 The average is not a primitive — it is a QUOTIENT of
                 two named things, and a corpus that never names them
                 cannot teach the notion, only the word
    ВОПРОС       the same fact asked and answered. A probe on the
                 trained organism went mute on questions whose
                 statements it knew: knowledge with only a declarative
                 surface REPORTS, it does not ANSWER
    СЛАГАЕМЫЕ    the sum and the count said SEPARATELY, each on its own
                 line. The two halves of the quotient must be
                 obtainable apart, or the ground of the average is a
                 phrase and not a computation
    ГРАНИЦЫ      the largest and the smallest — the other two numbers a
                 row gives rise to, and the ones the law needs
    ЗАКОН        the average lies BETWEEN them. This is the first thing
                 about an average that is not its definition, and it is
                 shown on the same row that showed the definition
    КОНТРПРИМЕР  «the average is always one of the numbers» — false,
                 and killed by one witness. The cheapest proof there
                 is, and the one a confirming corpus never teaches

EVERY NUMBER IS COMPUTED HERE AND RE-COMPUTED BY THE COURT. Nothing in
this file is written by hand: the sum is summed, the count counted, the
average divided, the bounds taken. `courts/average_court.py` does all
of it a second time from the row alone, and for the counterexample it
checks the WORK — that the average really is absent from the row —
because a witness that does not refute is the most convincing lie a
corpus can carry.

ЧЕСТНОЕ МОЛЧАНИЕ ВМЕСТО ПРАВДОПОДОБНОЙ ПОВЕРХНОСТИ. A row whose sum
does not divide by its length has no whole average, and this world owns
no notation for halves. Such a row is NOT SHOWN — it is dropped before
any surface is built. Rounding it would teach a rounding as a truth.

ЗАПЯТАЯ ЕСТЬ ЗНАК ЭТОГО МИРА. Neighbouring worlds write a row with
spaces («the mean of 2 4 6», «the sum of 3 5 7»), and their courts are
anchored on that spacing. A row here is written «3, 5, 7» — so the two
worlds cannot mistake each other's shows, and neither court can judge a
genus it does not own. The word is chosen for the same reason:
«average» / «среднее чисел» where the neighbour says «mean» / «среднее».

BOTH TONGUES, ONE ROW. English and Russian say the same fact about the
same numbers and are judged by the same computation, so a defect in one
surface cannot hide behind the other.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import numerals  # noqa: E402
import rugram  # noqa: E402
from layer import emit_grouped  # noqa: E402
from plural import by_count  # noqa: E402

ЦЕЛЬ = "datasets/genesis_average.txt"

# ДЛИНА РЯДА РАЗНАЯ, И ЭТО НЕ УКРАШЕНИЕ: на рядах одной длины счёт
# перестаёт быть величиной и становится частью оборота — организм
# выучил бы «среднее» как «сумма делить на три».
ДЛИНЫ = (2, 3, 4, 5)
РЯДОВ_НА_ДЛИНУ = 12

# Числительное и счётная форма берутся у ДОМА ЯЗЫКА, а не выписываются
# рукой: второй список рядом с таблицей пакета разошёлся бы с нею в
# первый же день. Суд читает имя ОБРАТНО тем же законом разрядов.
ТАБЛИЦА_РУ = numerals.таблица("ru")


def ход(начало, первый, второй, длина):
    """Ряд, собранный ХОДОМ: два шага чередуются.

    ПРОГРЕССИЯ НЕ ГОДИТСЯ В РЯД ЭТОГО МИРА. У арифметической прогрессии
    нечётной длины среднее ЕСТЬ средний член по построению — и показ
    учил бы, что среднее берётся с середины ряда, а не считается. Два
    чередующихся шага ломают это тождество, оставляя ряд простым.
    """
    ряд = [начало]
    for к in range(длина - 1):
        ряд.append(ряд[-1] + (первый if к % 2 == 0 else второй))
    return ряд


def ряды(шаг):
    """Ряды прохода — ТОЛЬКО те, чьё среднее целое.

    ОТСЕВ СТОИТ ДО ВСЯКОЙ ПОВЕРХНОСТИ, а не после. Ряд без целого
    среднего не получает ни одного показа: ни суммы, ни границ, ни
    закона. Иначе мир нёс бы ряды, о среднем которых он молчит, — и
    молчание читалось бы как «среднего нет».
    """
    вон = []
    for длина in ДЛИНЫ:
        for i in range(РЯДОВ_НА_ДЛИНУ):
            ряд = ход(начало=1 + (шаг * 5 + i * 3) % 20,
                      первый=1 + (шаг + i) % 7,
                      второй=1 + (шаг * 2 + i * 3) % 9,
                      длина=длина)
            # РЯД ПОВОРАЧИВАЕТСЯ, ИБО НА ВОЗРАСТАЮЩЕМ РЯДУ
            # «НАИБОЛЬШЕЕ» ЕСТЬ ПОСЛЕДНЕЕ. Показ учил бы месту в
            # записи, а не сравнению величин. Поворот не трогает ни
            # суммы, ни счёта, ни среднего — он трогает только то, чему
            # показ не должен учить.
            поворот = (шаг + i) % длина
            ряд = ряд[поворот:] + ряд[:поворот]
            if sum(ряд) % длина == 0:
                вон.append(ряд)
    return вон


def запись(ряд):
    return ", ".join(str(x) for x in ряд)


def среднее(ряд):
    return sum(ряд) // len(ряд)


# ------------------------------------------------------------- РОДЫ

def показ_среднего(ряд):
    """Среднее, СКАЗАННОЕ ВМЕСТЕ СО СВОИМ ОСНОВАНИЕМ."""
    р, к = запись(ряд), len(ряд)
    return [
        f"the average of {р} is {среднее(ряд)}: their sum is "
        f"{sum(ряд)} and there are {к} of them.",
        f"среднее чисел {р} — это {среднее(ряд)}: их сумма "
        f"{sum(ряд)}, а их количество {к}.",
    ]


def вопросы(ряд):
    return [f"what is the average of {запись(ряд)}?",
            f"чему равно среднее чисел {запись(ряд)}?"]


def показ_вопроса(ряд):
    """ВТОРАЯ ПОВЕРХНОСТЬ ТОГО ЖЕ ФАКТА, и стоит она одной строки.

    Проба показала: организм, знавший «the average of … is …» как
    утверждение, немел на «what is the average of …?». Знание, у
    которого есть лишь повествовательная поверхность, не отвечает — оно
    только сообщает. Ответ здесь не короче утверждения и не беднее его:
    вопрос получает ровно то же основание, иначе он учил бы отвечать
    голым числом.
    """
    return [f"{в} {о}" for в, о in zip(вопросы(ряд), показ_среднего(ряд))]


def показ_суммы(ряд):
    """Сумма отдельно: ПЕРВАЯ из двух названных величин частного.

    СУММА СКАЗАНА СЛОВОМ, А НЕ ЗНАКОМ. Запись «3 + 5 + 7 = 15» есть
    показ АРИФМЕТИКИ и принадлежит суду арифметики; здесь речь о том,
    что у ряда ЕСТЬ сумма и она есть половина основания среднего.
    """
    р = запись(ряд)
    return [f"the sum of {р} is {sum(ряд)}.",
            f"сумма чисел {р} — это {sum(ряд)}."]


def показ_счёта(ряд):
    """Счёт отдельно: ВТОРАЯ названная величина частного.

    ЧИСЛО ПРИ ИМЕНИ ЕСТЬ УТВЕРЖДЕНИЕ О ЯЗЫКЕ, А НЕ О СЧЁТЕ. Русское
    «3 числа» требует падежа при цифре и принадлежит роду согласования,
    у которого свои хозяева; счёт назван потому ЧИСЛИТЕЛЬНЫМ — «три
    числа», — и это не обход суда, а верное место утверждения: имя
    числа строит дом языка, и он же читает его обратно.
    """
    к = len(ряд)
    return [f"there are {к} {by_count(к, 'numbers')} in {запись(ряд)}.",
            f"в ряду {запись(ряд)} {numerals.назвать(к, ТАБЛИЦА_РУ)} "
            f"{rugram.форма('число', к)}."]


def показ_наибольшего(ряд):
    р = запись(ряд)
    return [f"the largest of {р} is {max(ряд)}.",
            f"наибольшее из {р} — это {max(ряд)}."]


def показ_наименьшего(ряд):
    р = запись(ряд)
    return [f"the smallest of {р} is {min(ряд)}.",
            f"наименьшее из {р} — это {min(ряд)}."]


def показ_закона(ряд):
    """ЗАКОН ПОКАЗАН ОТДЕЛЬНО ОТ ОПРЕДЕЛЕНИЯ, и на том же ряду.

    Что среднее лежит между наименьшим и наибольшим — первое, что
    известно о среднем СВЕРХ его определения. Показанный на том же
    ряду, что и определение, закон покупается как ЕЩЁ ОДНО
    утверждение о знакомом, а не как новый предмет.
    """
    р, ср = запись(ряд), среднее(ряд)
    return [f"the average of {р} is {ср}, and {min(ряд)} ≤ {ср} ≤ "
            f"{max(ряд)}.",
            f"среднее чисел {р} — это {ср}, и {min(ряд)} ≤ {ср} ≤ "
            f"{max(ряд)}."]


def показ_контрпримера(ряд):
    """Всеобщее утверждение, УБИТОЕ ОДНИМ СВИДЕТЕЛЕМ, — или молчание.

    СВИДЕТЕЛЬ БЕРЁТСЯ ИЗ ТЕХ ЖЕ РЯДОВ, А НЕ ВЫПИСЫВАЕТСЯ. Ряд, чьё
    среднее лежит среди его чисел, ничего не опровергает — и показа не
    даёт вовсе. Контрпример, который не опровергает, звучит
    убедительнее всего, ибо форма у него правильная.
    """
    ср = среднее(ряд)
    if ср in ряд:
        return []
    р = запись(ряд)
    return [f"the average is always one of the numbers is false: the "
            f"average of {р} is {ср}, and {ср} is not among them.",
            f"среднее всегда есть одно из чисел — ложь: среднее чисел "
            f"{р} — это {ср}, а {ср} среди них нет."]


# РОД ОБЪЯВЛЯЕТ ОДНУ ФУНКЦИЮ НАД РЯДОМ И НИЧЕГО БОЛЬШЕ. Прибавить род
# значит объявить пару, а не написать новый обход: это и есть проба,
# что форма есть форма, а не шаблон.
РОДЫ = (
    ("average", показ_среднего),
    ("question", показ_вопроса),
    ("sum", показ_суммы),
    ("count", показ_счёта),
    ("largest", показ_наибольшего),
    ("smallest", показ_наименьшего),
    ("law", показ_закона),
    ("counterexample", показ_контрпримера),
)


def pass_groups(шаг):
    """Одна группа на РОД: роды не перемешиваются между собой."""
    ряд_прохода = ряды(шаг)
    группы = []
    for _имя, показать in РОДЫ:
        свои = []
        for ряд in ряд_прохода:
            свои += показать(ряд)
        # ПУСТОЙ РОД НЕ ДАЁТ ШВА. Род, промолчавший весь проход (все
        # ряды опровергнуть не смогли), не вправе оставить за собой
        # пустой блок между двумя переводами страницы: читатель
        # корпуса нашёл бы там мир из ноля строк.
        if свои:
            группы.append(свои)
    return группы


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
