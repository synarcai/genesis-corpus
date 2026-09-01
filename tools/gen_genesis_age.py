#!/usr/bin/env python3
"""GENESIS layer: AGE — a quantity that MOVES ALONG WITH TIME.

Eleven questions of the band die here, and their genus is one: a number
that is not fixed but carried by time. «in 9 years ruby will be twice as
old» asks the organism to hold three things at once — the age now, the
shift, and the fact that the shift is added TO BOTH ALIKE. The last of
the three is the law the corpus never showed: TIME FLOWS FOR EVERYONE.

WHY A CORPUS OF ARITHMETIC DOES NOT ALREADY TEACH THIS. «12 + 3 = 15»
is a fact about numbers; «in 3 years tom will be 15» is a fact about a
number ATTACHED to somebody, and the attachment is what makes the second
person's age move too. A layer that shows only the addition teaches the
step and hides the reason there are two of them.

WHAT IS SHOWN, AND WHY EACH GENUS EXISTS:

    СЕЙЧАС      two ages and the difference between them — the ground
                every later genus stands on
    ВПЕРЁД      the shift added to BOTH, said in one show, so the pair
                of additions is one act and not two
    ЗАКОН       the same shift with its invariant named: the difference
                does not change. This is the one thing about age
                arithmetic that is not arithmetic, and the corpus owes
                it a show of its own
    НАЗАД       the shift subtracted from both — and SILENCE where it
                would take somebody below one year old
    КРАТНОЕ     «three times as old», with «12 = 3 × 4» beside it: the
                relation and its ground in one line
    КРАТНОЕ ВПЕРЁД  the band's hardest genus. It is built BACKWARDS —
                the future ages are chosen first, so the multiple is
                true BY CONSTRUCTION and never by luck
    ВОПРОС      every genus asked as well as told. A probe went mute on
                questions whose statements it knew: knowledge with only
                a declarative surface REPORTS, it does not ANSWER
    ОТКАЗ       «how old is ann's brother? it is not said». Muteness
                needs a PAIR — a refusal WITH ITS GROUND — or the
                organism learns that silence is the answer to what it
                does not know

ЯДРО ДОСЛОВНЫХ ПОВТОРОВ. The first three cases of every genus are the
SAME in every pass, word for word; the rest walk with the pass number.
A form is bought by repetition — that is a measurement, not an opinion —
and a layer whose every line is new gives the form nothing to stand on.

ИМЯ СКЛОНЯЕТСЯ, И ПАДЕЖИ ОБЪЯВЛЕНЫ. «тому 12 лет» is the dative, «том
старше ани» pairs a nominative with a genitive. Russian case cannot be
had by cutting an ending, so the three forms of every name are DECLARED
here and re-declared by the court: an edit in one house and not in the
other makes the line UNJUDGED, and the write gate does not pass an
unjudged line.

СЧЁТНАЯ ФОРМА БЕРЁТСЯ У ДОМА РУССКОГО СЧЁТА (`tools/rugram.py`), not
written out here: «1 год», «3 года», «5 лет» is a law of the language,
and a second list beside the declared one parts from it on the first
day. English does the same through `tools/plural.py`.

EVERY NUMBER IS COMPUTED HERE AND RE-COMPUTED BY THE COURT — including
the law: `courts/age_court.py` adds the shift to both ages itself and
checks that the difference it finds after equals the difference it finds
before. A show that shifted only one of the two dies there.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rugram  # noqa: E402
from layer import emit_grouped  # noqa: E402
from plural import by_count  # noqa: E402

ЦЕЛЬ = "datasets/genesis_age.txt"

# ИМЯ И ЕГО ТРИ ПАДЕЖА: именительный, дательный, родительный. Имена
# взяты на -а/-я и Том — те, чей дательный и родительный коротки и
# ни с чем не спорят. Список МАЛ намеренно: он должен целиком
# повториться в суде второй рукой, а длинный список второй рукой не
# повторяют — его копируют, и копия расходится.
ЛЮДИ = {
    "tom": ("том", "тому", "тома"),
    "ann": ("аня", "ане", "ани"),
    "olya": ("оля", "оле", "оли"),
    "misha": ("миша", "мише", "миши"),
}
ИМЕНА = ("tom", "ann", "olya", "misha")

# КРАТНОСТЬ СКАЗАНА СЛОВОМ, И СЛОВО ОБЪЯВЛЕНО. «вдвое» не выводится
# из двойки ни в одном языке, и «twice» тем более: это лексика, а не
# правило. Отсюда же берётся предел кратностей — мир не скажет того,
# чего не умеет назвать.
КРАТНЫЕ_СЛОВА = {
    2: ("twice", "вдвое"),
    3: ("three times", "втрое"),
    4: ("four times", "вчетверо"),
    5: ("five times", "впятеро"),
}

# ОТНОШЕНИЕ, О КОТОРОМ НЕ СКАЗАНО: (английское, дательный, предложный).
ОТНОШЕНИЯ = (
    ("brother", "брату", "о брате"),
    ("sister", "сестре", "о сестре"),
    ("neighbour", "соседу", "о соседе"),
)

# ЯДРО ДОСЛОВНЫХ ПОВТОРОВ: столько первых случаев каждого рода стоят
# во ВСЕХ проходах слово в слово.
ЯДРО = 3

ЯДРО_ПАР = (
    ("tom", "ann", 12, 7, 3),
    ("olya", "misha", 9, 5, 4),
    ("misha", "tom", 15, 6, 2),
)
ЯДРО_КРАТНЫХ = (
    ("tom", "ann", 4, 3),
    ("olya", "misha", 5, 2),
    ("misha", "tom", 3, 4),
)
ЯДРО_КРАТНЫХ_ВПЕРЁД = (
    ("tom", "ann", 6, 2, 2),
    ("olya", "misha", 4, 3, 3),
    ("misha", "tom", 5, 2, 1),
)
ЯДРО_ОТКАЗОВ = (
    ("ann", 0),
    ("tom", 1),
    ("olya", 2),
)

ПАР_ХОДОМ = 8
КРАТНЫХ_ХОДОМ = 6
ОТКАЗОВ_ХОДОМ = 3


# ----------------------------------------------------------- ИМЕНА

def именительный(кто):
    return ЛЮДИ[кто][0]


def дательный(кто):
    return ЛЮДИ[кто][1]


def родительный(кто):
    return ЛЮДИ[кто][2]


def лет(сколько):
    return rugram.форма("год", сколько)


def years(сколько):
    return by_count(сколько, "years")


def двое(шаг, i):
    """Два РАЗНЫХ имени: второе берётся сдвигом от первого.

    Сдвиг никогда не нулевой, и потому человек не сравнивается сам с
    собою — а такое сравнение и есть первый способ сделать разницу
    нулём, не заметив этого.
    """
    первый = (шаг + i) % len(ИМЕНА)
    второй = (первый + 1 + i % (len(ИМЕНА) - 1)) % len(ИМЕНА)
    return ИМЕНА[первый], ИМЕНА[второй]


# ---------------------------------------------------------- СЕМЬИ

def пары(шаг):
    """(старший, младший, возраст старшего, возраст младшего, сдвиг)."""
    вон = list(ЯДРО_ПАР)
    for i in range(ПАР_ХОДОМ):
        старший, младший = двое(шаг, i)
        мал = 4 + (шаг * 3 + i * 2) % 12
        разница = 1 + (шаг + i * 3) % 9
        сдвиг = 1 + (шаг * 2 + i) % 7
        вон.append((старший, младший, мал + разница, мал, сдвиг))
    return вон


def кратные(шаг):
    """(старший, младший, возраст младшего, кратность)."""
    вон = list(ЯДРО_КРАТНЫХ)
    for i in range(КРАТНЫХ_ХОДОМ):
        старший, младший = двое(шаг, i)
        мал = 2 + (шаг + i * 2) % 8
        к = 2 + (шаг + i) % len(КРАТНЫЕ_СЛОВА)
        вон.append((старший, младший, мал, к))
    return вон


def кратные_вперёд(шаг):
    """(старший, младший, БУДУЩИЙ возраст младшего, кратность, сдвиг).

    СТРОИТСЯ ОТ БУДУЩЕГО НАЗАД, и это не приём, а единственный честный
    путь. Выбери возраста сейчас — и кратность в будущем окажется
    целой лишь по удаче; выбери будущие — и она истинна ПО
    ПОСТРОЕНИЮ, а нынешние получаются вычитанием сдвига. Мир, который
    ищет кратность перебором, показывает то, что нашёл; этот
    показывает то, что построил.
    """
    вон = list(ЯДРО_КРАТНЫХ_ВПЕРЁД)
    for i in range(КРАТНЫХ_ХОДОМ):
        старший, младший = двое(шаг, i)
        потом = 3 + (шаг * 2 + i) % 7
        к = 2 + (шаг + i * 2) % len(КРАТНЫЕ_СЛОВА)
        сдвиг = 1 + (шаг + i) % 5
        вон.append((старший, младший, потом, к, сдвиг))
    return вон


def отказы(шаг):
    """(о ком спрошено, какое отношение)."""
    вон = list(ЯДРО_ОТКАЗОВ)
    for i in range(ОТКАЗОВ_ХОДОМ):
        вон.append((ИМЕНА[(шаг + i) % len(ИМЕНА)],
                    (шаг + i * 2) % len(ОТНОШЕНИЯ)))
    return вон


# ----------------------------------------------------------- РОДЫ

def показ_сейчас(случай):
    """Возраст обоих и РАЗНИЦА между ними — основание всего мира."""
    а, б, ва, вб, _сдвиг = случай
    р = ва - вб
    return [
        f"{а} is {ва} {years(ва)} old and {б} is {вб} {years(вб)} old; "
        f"{а} is {р} {years(р)} older than {б}.",
        f"{дательный(а)} {ва} {лет(ва)}, а {дательный(б)} {вб} "
        f"{лет(вб)}; {именительный(а)} старше {родительный(б)} на {р} "
        f"{лет(р)}.",
    ]


def показ_вперёд(случай):
    """Сдвиг прибавлен ОБОИМ, и сказано это ОДНИМ показом."""
    а, б, ва, вб, с = случай
    return [
        f"{а} is {ва} and {б} is {вб}; in {с} {years(с)} {а} will be "
        f"{ва + с} and {б} will be {вб + с}.",
        f"{дательный(а)} {ва}, а {дательный(б)} {вб}; через {с} "
        f"{лет(с)} {дательный(а)} будет {ва + с}, а {дательный(б)} "
        f"{вб + с}.",
    ]


def показ_закона(случай):
    """ЗАКОН: время течёт для всех, и потому разница не меняется.

    ПОКАЗ НЕСЁТ ОБЕ ПАРЫ ВОЗРАСТОВ, а не одну разницу. Строка «через 3
    года том всё так же старше ани на 5 лет» верна на вид и
    непроверяема на деле: суду не с чем сверить пятёрку. Закон обязан
    приносить с собою то, из чего он считается, — иначе он не закон, а
    заверение.
    """
    а, б, ва, вб, с = случай
    р = ва - вб
    return [
        f"{а} is {ва} and {б} is {вб}; in {с} {years(с)} {а} will be "
        f"{ва + с} and {б} will be {вб + с}, and {а} will still be {р} "
        f"{years(р)} older than {б}: the difference does not change.",
        f"{дательный(а)} {ва}, а {дательный(б)} {вб}; через {с} "
        f"{лет(с)} {дательный(а)} будет {ва + с}, а {дательный(б)} "
        f"{вб + с}, и {именительный(а)} всё так же старше "
        f"{родительный(б)} на {р} {лет(р)}: разница не меняется.",
    ]


def показ_назад(случай):
    """Сдвиг НАЗАД — или молчание, если он уводит младшего за единицу.

    ВОЗРАСТА МЕНЬШЕ ГОДА ЭТОТ МИР НЕ ЗНАЕТ, и отрицательного тем более.
    Показ не выпускается вовсе: округлить до нуля значило бы научить
    нулю как возрасту, а показать «−2 года» — научить бессмыслице с
    полной судимостью.
    """
    а, б, ва, вб, с = случай
    if вб - с < 1:
        return []
    return [
        f"{а} is {ва} and {б} is {вб}; {с} {years(с)} ago {а} was "
        f"{ва - с} and {б} was {вб - с}.",
        f"{дательный(а)} {ва}, а {дательный(б)} {вб}; {с} {лет(с)} "
        f"назад {дательный(а)} было {ва - с}, а {дательный(б)} "
        f"{вб - с}.",
    ]


def показ_кратного(случай):
    """Кратное отношение возрастов, с основанием рядом."""
    а, б, вб, к = случай
    ва = к * вб
    англ, рус = КРАТНЫЕ_СЛОВА[к]
    return [
        f"{а} is {ва} and {б} is {вб}; {а} is {англ} as old as {б}: "
        f"{ва} = {к} × {вб}.",
        f"{дательный(а)} {ва}, а {дательный(б)} {вб}; "
        f"{именительный(а)} {рус} старше {родительный(б)}: {ва} = {к} × "
        f"{вб}.",
    ]


def показ_кратного_вперёд(случай):
    """Кратность, наступающая ЧЕРЕЗ сдвиг, — или молчание.

    Здесь сходятся оба закона мира разом: сдвиг прибавляется обоим, и
    только потому кратность в будущем есть утверждение о ВРЕМЕНИ, а не
    о двух отдельных числах.
    """
    а, б, потом_б, к, с = случай
    if потом_б - с < 1:
        return []
    потом_а = к * потом_б
    ва, вб = потом_а - с, потом_б - с
    англ, рус = КРАТНЫЕ_СЛОВА[к]
    return [
        f"{а} is {ва} and {б} is {вб}; in {с} {years(с)} {а} will be "
        f"{потом_а} and {б} will be {потом_б}, and {потом_а} is {англ} "
        f"{потом_б}.",
        f"{дательный(а)} {ва}, а {дательный(б)} {вб}; через {с} "
        f"{лет(с)} {дательный(а)} будет {потом_а}, а {дательный(б)} "
        f"{потом_б}, и {потом_а} {рус} больше {потом_б}.",
    ]


def показ_вопрос_сейчас(случай):
    """Вопрос об основании. У НЕГО НЕТ ВЫЧИСЛИМОГО ОСНОВАНИЯ — он и
    ЕСТЬ основание: возраст сейчас ниоткуда не выводится, он назван.
    Суду остаётся проверяемое — что отвечено о ТОМ ЖЕ лице и что
    счётная форма при числе своя.
    """
    а, _б, ва, _вб, _с = случай
    return [f"how old is {а} now? {а} is {ва} {years(ва)} old.",
            f"сколько лет {дательный(а)} сейчас? {дательный(а)} {ва} "
            f"{лет(ва)}."]


def показ_вопрос_вперёд(случай):
    """ОТВЕТ НЕСЁТ СВОЁ ОСНОВАНИЕ, иначе он непроверяем.

    «сколько лет будет тому через 3 года? через 3 года тому будет 15»
    верно на вид и не сверяемо ни с чем: возраста сейчас в строке нет,
    и пятнадцать берётся на веру. Ответ называет исходный возраст —
    и становится вычислением, а не заверением.
    """
    а, _б, ва, _вб, с = случай
    return [f"how old will {а} be in {с} {years(с)}? {а} is {ва}, so "
            f"in {с} {years(с)} {а} will be {ва + с}.",
            f"сколько лет будет {дательный(а)} через {с} {лет(с)}? "
            f"{дательный(а)} {ва}, значит через {с} {лет(с)} "
            f"{дательный(а)} будет {ва + с}."]


def показ_вопрос_назад(случай):
    а, _б, ва, _вб, с = случай
    if ва - с < 1:
        return []
    return [f"how old was {а} {с} {years(с)} ago? {а} is {ва}, so {с} "
            f"{years(с)} ago {а} was {ва - с}.",
            f"сколько лет было {дательный(а)} {с} {лет(с)} назад? "
            f"{дательный(а)} {ва}, значит {с} {лет(с)} назад "
            f"{дательный(а)} было {ва - с}."]


def показ_вопрос_разницы(случай):
    а, б, ва, вб, _с = случай
    р = ва - вб
    return [f"how much older is {а} than {б}? {а} is {р} {years(р)} "
            f"older than {б}: {а} is {ва} and {б} is {вб}.",
            f"насколько {именительный(а)} старше {родительный(б)}? "
            f"{именительный(а)} старше {родительный(б)} на {р} {лет(р)}: "
            f"{дательный(а)} {ва}, а {дательный(б)} {вб}."]


def показ_отказа(случай):
    """ОТКАЗ С ОСНОВАНИЕМ — пара немоте.

    Организм, которому нечего ответить, обязан УМЕТЬ СКАЗАТЬ ЭТО и
    сказать ПОЧЕМУ. Корпус, где всякий вопрос имеет число в ответе,
    учит, что число есть всегда, — и тогда незнание выходит наружу
    выдумкой, а не отказом.
    """
    кто, какое = случай
    англ, дат, пред = ОТНОШЕНИЯ[какое]
    return [f"how old is {кто}'s {англ}? it is not said: nothing is "
            f"told about a {англ}.",
            f"сколько лет {дат} {родительный(кто)}? не сказано: {пред} "
            f"ничего не говорится."]


# РОД ОБЪЯВЛЯЕТ СЕМЬЮ СЛУЧАЕВ И ОДНУ ФУНКЦИЮ НАД СЛУЧАЕМ. Прибавить
# род значит объявить тройку, а не написать новый обход; и молчание
# рода есть пустой список, а не особая ветвь.
РОДЫ = (
    ("now", пары, показ_сейчас),
    ("forward", пары, показ_вперёд),
    ("law", пары, показ_закона),
    ("backward", пары, показ_назад),
    ("multiple", кратные, показ_кратного),
    ("multiple-ahead", кратные_вперёд, показ_кратного_вперёд),
    ("ask-now", пары, показ_вопрос_сейчас),
    ("ask-ahead", пары, показ_вопрос_вперёд),
    ("ask-back", пары, показ_вопрос_назад),
    ("ask-difference", пары, показ_вопрос_разницы),
    ("refusal", отказы, показ_отказа),
)


def pass_groups(шаг):
    """Одна группа на РОД: роды не перемешиваются между собой."""
    группы = []
    for _имя, семья, показать in РОДЫ:
        свои = []
        for случай in семья(шаг):
            свои += показать(случай)
        # ПУСТОЙ РОД НЕ ДАЁТ ШВА: род, промолчавший весь проход, не
        # вправе оставить за собою мир из ноля строк.
        if свои:
            группы.append(свои)
    return группы


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
