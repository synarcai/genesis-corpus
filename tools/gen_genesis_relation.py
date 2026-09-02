#!/usr/bin/env python3
"""GENESIS layer: RELATION — the metalanguage of structure, at a structure.

A corpus can name numbers, words and formulas and still be unable to say
what CONTAINS what, what CORRESPONDS to what, what is EQUIVALENT to what
and what STANDS at which level. Measured from outside: the tables of
contents of seven prose corpora name «связь» 169 times, «структура» 115,
«hierarchy» 47, «closure» 28, «correspondence»/«соответствие» 24 — and
not one of those words was shown by a single show. Prose is unreadable
without them.

THE LAW OF THIS WORLD: A WORD SHOWN WITHOUT CHECKABLE CONTENT IS A
LABEL. Every relation here stands at a REAL structure which the court
WALKS AND RECOUNTS — a declared tree of eighteen nodes, seven relations
on four numbers, remainder classes on twelve numbers, the divisibility
order on the divisors of twelve, a directed graph of seven nodes. Not a
single answer is written down; every one is walked out. «Transitive» is
either a triple that closes or a triple that does not, and the show says
WHICH triple.

BOTH LANGUAGES CARRY EVERY KIND. «hierarchy», «relation», «transitive»,
«equivalence», «class», «correspondence», «order», «path», «level»,
«closure» are missing from the corpus exactly as their Russian twins
are, and a world that showed structure in one language only would have
taught that structure is a property of English.

WHAT A SHOW OWES BESIDES ITS ANSWER — THE VIOLATOR. Every property is
shown twice: with a case that confirms it and with a case that breaks
it, and the breaking case NAMES ITS WITNESS («1 stands to 2 and 2
stands to 3, but 1 does not stand to 3»). A corpus that only shows
relations that ARE transitive teaches that all relations are; a corpus
that only shows paths that exist teaches that a path always exists.
Refusals here are first-class and carry their ground: no such edge, no
path at all, no greatest element, not one-to-one.

THE ORACLE IS TWO OPPOSITE WALKS, ONE PAIR PER KIND — level counted up
against depth counted down, a witness against set algebra, remainder
buckets against connected pieces, the order rule against reachability
over covers, a walk forward against a walk backward. Nothing is written
here to be compared with itself.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import relation as о  # noqa: E402
import rugram  # noqa: E402
import units  # noqa: E402
from layer import emit_grouped  # noqa: E402
from plural import by_count  # noqa: E402

# ИМЕНА МНОЖЕСТВ ПИШУТСЯ ОДНИМ ЗАКОНОМ, а не двумя строками в двух
# домах: множество, названное в показе иначе, чем его читает суд, есть
# два объявления одного факта.
ЧЕРЕЗ = ", "


def набор(множество):
    return "{" + ЧЕРЕЗ.join(str(э) for э in множество) + "}"


def ру_узел(счёт):
    return units.ру_форма(rugram.СЧЁТНЫЕ["узел"], счёт)


def ру_ребро(счёт):
    return units.ру_форма(rugram.СЧЁТНЫЕ["ребро"], счёт)


def ру_число(счёт):
    return units.ру_форма(rugram.СЧЁТНЫЕ["число"], счёт)


def ру_элемент(счёт):
    return units.ру_форма(rugram.СЧЁТНЫЕ["элемент"], счёт)


def сдвиг(ряд, шаг):
    """Тот же ряд, начатый с другого места: проход меняет случаи."""
    н = len(ряд)
    return [ряд[(шаг + i) % н] for i in range(н)]


# ══════════════ ИЕРАРХИЯ ══════════════════════════════════════════════


def иерархия(шаг):
    """ВЛОЖЕННОСТЬ, УРОВЕНЬ, ПУТЬ ОТ КОРНЯ — всё сосчитано обходом."""
    вон = []
    корень = о.корень()
    узлы = сдвиг(о.ИМЕНА, шаг)
    for узел in узлы:
        вниз = о.потомки(узел)
        вверх = о.предки(узел)
        if вниз:
            # ВЛОЖЕННОСТЬ СКАЗАНА С ОБЕИХ СТОРОН: «A содержит B» и «B
            # лежит в A» суть один факт двумя ходами, и корпус,
            # знающий только первый, не умеет спросить о втором.
            низ = вниз[шаг % len(вниз)]
            вон.append(f"in the tree of kinds the node {узел} contains "
                       f"the node {низ}.")
            вон.append(f"в дереве родов узел {узел} содержит узел {низ}.")
            вон.append(f"the node {узел} contains {len(вниз)} "
                       f"{by_count(len(вниз), 'nodes')}.")
            вон.append(f"узел {узел} содержит {len(вниз)} "
                       f"{ру_узел(len(вниз))}.")
        else:
            вон.append(f"the node {узел} is a leaf of the tree of kinds: "
                       f"it contains no node.")
            вон.append(f"узел {узел} есть лист дерева родов: он не "
                       f"содержит ни одного узла.")
        if вверх:
            верх = вверх[шаг % len(вверх)]
            вон.append(f"in the tree of kinds the node {узел} lies in "
                       f"the node {верх}.")
            вон.append(f"в дереве родов узел {узел} лежит в узле {верх}.")
            вон.append(f"the parent of the node {узел} is the node "
                       f"{вверх[0]}.")
            вон.append(f"родителем узла {узел} является узел {вверх[0]}.")
        else:
            вон.append(f"the node {узел} is the root of the tree of "
                       f"kinds: it lies in no node.")
            вон.append(f"узел {узел} есть корень дерева родов: он не "
                       f"лежит ни в одном узле.")
        к = о.уровень(узел)
        вон.append(f"the level of the node {узел} is {к}.")
        вон.append(f"уровень узла {узел} равен {к}.")
        вон.append(f"the path from the root to the node {узел} has "
                   f"length {к}.")
        вон.append(f"путь от корня до узла {узел} имеет длину {к}.")
        дорога = " / ".join(о.путь_от_корня(узел))
        вон.append(f"the path from the root to the node {узел} is "
                   f"{дорога}.")
        вон.append(f"путь от корня до узла {узел} таков: {дорога}.")
        # ОТКАЗ С ОСНОВАНИЕМ: узел не содержит другого, И СКАЗАНО, В
        # ЧЁМ ТОТ ЛЕЖИТ. Отказ без основания учит отказывать вообще.
        чужие = [и for и in о.ИМЕНА
                 if и != узел and и != корень and not о.содержит(узел, и)
                 and о.УЗЕЛ[и][0] != узел]
        if чужие:
            чужой = чужие[шаг % len(чужие)]
            где = о.УЗЕЛ[чужой][0]
            вон.append(f"in the tree of kinds the node {узел} does not "
                       f"contain the node {чужой}: the node {чужой} lies "
                       f"in the node {где}.")
            вон.append(f"в дереве родов узел {узел} не содержит узел "
                       f"{чужой}: узел {чужой} лежит в узле {где}.")
    n, m = len(о.ИМЕНА), len(о.ИМЕНА) - 1
    вон.append(f"the tree of kinds is a hierarchy of {n} nodes and {m} "
               f"edges: each node except the root lies in exactly one "
               f"node.")
    вон.append(f"дерево родов есть иерархия из {n} {ру_узел(n)} и {m} "
               f"{ру_ребро(m)}: каждый узел, кроме корня, лежит ровно в "
               f"одном узле.")
    у = о.уровней()
    вон.append(f"the tree of kinds is a structure of {у} levels: from "
               f"level 0 to level {у - 1}.")
    вон.append(f"дерево родов есть структура из {у} "
               f"{о.ру('уровень', у)}: от уровня 0 до уровня {у - 1}.")
    return вон


# ══════════════ ОТНОШЕНИЕ И ЕГО СВОЙСТВА ══════════════════════════════


def свойства(шаг):
    """ТРИ СВОЙСТВА, И КАЖДОЕ С ПОДТВЕРЖДЕНИЕМ И С НАРУШИТЕЛЕМ."""
    вон = []
    S = набор(о.МНОЖЕСТВО)
    for имя, ру_имя, _п in сдвиг(о.ОТНОШЕНИЯ, шаг):
        зачин = f"on the set {S} the relation «{имя}»"
        ру_зачин = f"на множестве {S} отношение «{ру_имя}»"
        свид = о.свидетель_рефлексивности(имя)
        if свид is None:
            вон.append(f"{зачин} is reflexive: every element stands in "
                       f"relation to itself.")
            вон.append(f"{ру_зачин} рефлексивно: каждый элемент "
                       f"относится к самому себе.")
        else:
            вон.append(f"{зачин} is not reflexive: {свид} does not stand "
                       f"in relation to itself.")
            вон.append(f"{ру_зачин} не рефлексивно: {свид} не относится "
                       f"к самому себе.")
        свид = о.свидетель_симметричности(имя)
        if свид is None:
            вон.append(f"{зачин} is symmetric: if a stands to b, then b "
                       f"stands to a.")
            вон.append(f"{ру_зачин} симметрично: если a относится к b, "
                       f"то b относится к a.")
        else:
            a, b = свид
            вон.append(f"{зачин} is not symmetric: {a} stands to {b}, "
                       f"but {b} does not stand to {a}.")
            вон.append(f"{ру_зачин} не симметрично: {a} относится к {b}, "
                       f"но {b} не относится к {a}.")
        свид = о.свидетель_транзитивности(имя)
        if свид is None:
            вон.append(f"{зачин} is transitive: if a stands to b and b "
                       f"stands to c, then a stands to c.")
            вон.append(f"{ру_зачин} транзитивно: если a относится к b и "
                       f"b относится к c, то a относится к c.")
        else:
            a, b, c = свид
            вон.append(f"{зачин} is not transitive: {a} stands to {b} "
                       f"and {b} stands to {c}, but {a} does not stand "
                       f"to {c}.")
            вон.append(f"{ру_зачин} не транзитивно: {a} относится к {b} "
                       f"и {b} относится к {c}, но {a} не относится к "
                       f"{c}.")
        все_пары = о.пары(имя)
        сколько, всего = len(все_пары), len(о.МНОЖЕСТВО) ** 2
        вон.append(f"{зачин} holds {сколько} "
                   f"{by_count(сколько, 'pairs')} out of {всего}.")
        вон.append(f"{ру_зачин} содержит {сколько} "
                   f"{о.ру('пара', сколько)} из {всего}.")
        стоящая = все_пары[шаг % len(все_пары)]
        вон.append(f"on the set {S} the pair ({стоящая[0]}, {стоящая[1]}) "
                   f"stands in the relation «{имя}».")
        вон.append(f"на множестве {S} пара ({стоящая[0]}, {стоящая[1]}) "
                   f"стоит в отношении «{ру_имя}».")
        нет = [(a, b) for a in о.МНОЖЕСТВО for b in о.МНОЖЕСТВО
               if not о.стоит(имя, a, b)]
        if нет:
            a, b = нет[шаг % len(нет)]
            вон.append(f"on the set {S} the pair ({a}, {b}) does not "
                       f"stand in the relation «{имя}».")
            вон.append(f"на множестве {S} пара ({a}, {b}) не стоит в "
                       f"отношении «{ру_имя}».")
    return вон


# ══════════════ ЗАМЫКАНИЕ ═════════════════════════════════════════════


def замыкания(шаг):
    """ЗАМЫКАНИЕ ЕСТЬ ТО, ЧЕГО ОТНОШЕНИЮ НЕДОСТАЁТ ДО ТРАНЗИТИВНОСТИ."""
    вон = []
    S = набор(о.МНОЖЕСТВО)
    for имя, ру_имя, _п in сдвиг(о.ОТНОШЕНИЯ, шаг):
        своё = set(о.пары(имя))
        шире = о.замыкание(имя)
        if шире == своё:
            вон.append(f"the transitive closure of the relation «{имя}» "
                       f"on the set {S} is the relation itself: it is "
                       f"already transitive.")
            вон.append(f"транзитивное замыкание отношения «{ру_имя}» на "
                       f"множестве {S} есть само отношение: оно уже "
                       f"транзитивно.")
            continue
        вон.append(f"the transitive closure of the relation «{имя}» on "
                   f"the set {S} holds {len(шире)} "
                   f"{by_count(len(шире), 'pairs')}, the relation itself "
                   f"{len(своё)}.")
        вон.append(f"транзитивное замыкание отношения «{ру_имя}» на "
                   f"множестве {S} содержит {len(шире)} "
                   f"{о.ру('пара', len(шире))}, само отношение — "
                   f"{len(своё)}.")
        новые = sorted(шире - своё)
        a, b = новые[шаг % len(новые)]
        звенья = " - ".join(str(э) for э in о.цепь(имя, a, b))
        вон.append(f"the pair ({a}, {b}) is not in the relation «{имя}», "
                   f"but is in its transitive closure: the chain "
                   f"{звенья}.")
        вон.append(f"пара ({a}, {b}) не стоит в отношении «{ру_имя}», но "
                   f"стоит в его транзитивном замыкании: цепь {звенья}.")
    return вон


# ══════════════ ЭКВИВАЛЕНТНОСТЬ И КЛАСС ═══════════════════════════════


def эквивалентности(шаг):
    """РАЗБИЕНИЕ ПЕРЕСЧИТЫВАЕТСЯ, А НЕ ПЕРЕЧИСЛЯЕТСЯ."""
    вон = []
    предел = о.ПРЕДЕЛ
    for модуль in сдвиг(о.МОДУЛИ, шаг):
        куски = о.классы(модуль)
        вон.append(f"on the numbers from 1 to {предел} the relation «the "
                   f"same remainder modulo {модуль}» is an equivalence: "
                   f"it is reflexive, symmetric and transitive.")
        вон.append(f"на числах от 1 до {предел} отношение «тот же "
                   f"остаток по модулю {модуль}» есть эквивалентность: "
                   f"оно рефлексивно, симметрично и транзитивно.")
        вон.append(f"the numbers from 1 to {предел} fall by remainder "
                   f"modulo {модуль} into {len(куски)} "
                   f"{by_count(len(куски), 'classes')}.")
        вон.append(f"числа от 1 до {предел} разбиваются по остатку по "
                   f"модулю {модуль} на {len(куски)} "
                   f"{о.ру('класс', len(куски))}.")
        вон.append(f"the classes of remainder modulo {модуль} among the "
                   f"numbers from 1 to {предел} do not meet and together "
                   f"give all {предел} numbers.")
        вон.append(f"классы остатка по модулю {модуль} среди чисел от 1 "
                   f"до {предел} не пересекаются и вместе дают все "
                   f"{предел} {ру_число(предел)}.")
        for о_ст, свои in куски.items():
            перечень = ЧЕРЕЗ.join(str(н) for н in свои)
            вон.append(f"the class of remainder {о_ст} modulo {модуль} "
                       f"among the numbers from 1 to {предел} holds "
                       f"{len(свои)} {by_count(len(свои), 'numbers')}: "
                       f"{перечень}.")
            вон.append(f"класс остатка {о_ст} по модулю {модуль} среди "
                       f"чисел от 1 до {предел} содержит {len(свои)} "
                       f"{ру_число(len(свои))}: {перечень}.")
            н = свои[шаг % len(свои)]
            вон.append(f"the number {н} stands in the class of remainder "
                       f"{о_ст} modulo {модуль}.")
            вон.append(f"число {н} стоит в классе остатка {о_ст} по "
                       f"модулю {модуль}.")
            сосед = свои[(шаг + 1) % len(свои)]
            if сосед != н:
                вон.append(f"the numbers {н} and {сосед} stand in one "
                           f"class modulo {модуль}.")
                вон.append(f"числа {н} и {сосед} стоят в одном классе по "
                           f"модулю {модуль}.")
            чужие = [м for м in о.ЧИСЛА
                     if о.остаток(м, модуль) != о_ст]
            чужой = чужие[шаг % len(чужие)]
            вон.append(f"the numbers {н} and {чужой} stand in different "
                       f"classes modulo {модуль}: the remainders are "
                       f"{о_ст} and {о.остаток(чужой, модуль)}.")
            вон.append(f"числа {н} и {чужой} стоят в разных классах по "
                       f"модулю {модуль}: остатки {о_ст} и "
                       f"{о.остаток(чужой, модуль)}.")
    return вон


# ══════════════ СООТВЕТСТВИЕ ══════════════════════════════════════════


def соответствия(шаг):
    """ВЗАИМНАЯ ОДНОЗНАЧНОСТЬ ЕСТЬ ХОД ОБРАТНО, А НЕ СЛОВО ПРИ ПОКАЗЕ."""
    вон = []
    for имя, ру_имя, ан_обл, ру_обл, _п in сдвиг(о.СООТВЕТСТВИЯ, шаг):
        туда = о.отображение(имя)
        ключи = sorted(туда, key=str)
        n = len(туда)
        if о.однозначно(имя):
            вон.append(f"the correspondence «{имя}» on {ан_обл} is "
                       f"one-to-one: {n} {by_count(n, 'elements')} and "
                       f"{n} {by_count(n, 'values')}.")
            вон.append(f"соответствие «{ру_имя}» на {ру_обл} "
                       f"взаимно-однозначно: {n} {ру_элемент(n)} и {n} "
                       f"{о.ру('значение', n)}.")
            э = ключи[шаг % n]
            вон.append(f"in the correspondence «{имя}» the element {э} "
                       f"goes to the value {туда[э]}, and the value "
                       f"{туда[э]} goes back to the element {э}.")
            вон.append(f"в соответствии «{ру_имя}» элемент {э} переходит "
                       f"в значение {туда[э]}, а значение {туда[э]} "
                       f"возвращается в элемент {э}.")
        else:
            a, b, з = о.свидетель_однозначности(имя)
            вон.append(f"the correspondence «{имя}» on {ан_обл} is not "
                       f"one-to-one: the elements {a} and {b} go to one "
                       f"and the same value {з}.")
            вон.append(f"соответствие «{ру_имя}» на {ру_обл} не "
                       f"взаимно-однозначно: элементы {a} и {b} "
                       f"переходят в одно и то же значение {з}.")
            э = ключи[шаг % n]
            вон.append(f"in the correspondence «{имя}» the element {э} "
                       f"goes to the value {туда[э]}.")
            вон.append(f"в соответствии «{ру_имя}» элемент {э} переходит "
                       f"в значение {туда[э]}.")
    return вон


# ══════════════ ПОРЯДОК ═══════════════════════════════════════════════


def порядки(шаг):
    """НЕ ВСЯКИЙ ПОРЯДОК ЛИНЕЕН, И ЭТО ГЛАВНОЕ ЗДЕСЬ."""
    вон = []
    for имя, множество in сдвиг(о.ПОРЯДКИ, шаг):
        ру_имя = о.ИМЯ_ПО_РУССКИ[имя]
        S = набор(множество)
        зачин = f"in the order «{имя}» on the set {S}"
        ру_зачин = f"в порядке «{ру_имя}» на множестве {S}"
        ниже = [(a, b) for a, b in о.пары(имя, множество) if a != b]
        a, b = ниже[шаг % len(ниже)]
        вон.append(f"{зачин} the element {a} stands below the element "
                   f"{b}.")
        вон.append(f"{ру_зачин} элемент {a} стоит ниже элемента {b}.")
        врозь = о.несравнимые(имя, множество)
        if врозь:
            a, b = врозь[шаг % len(врозь)]
            вон.append(f"{зачин} the elements {a} and {b} are "
                       f"incomparable: neither stands below the other.")
            вон.append(f"{ру_зачин} элементы {a} и {b} несравнимы: ни "
                       f"один не стоит ниже другого.")
            вон.append(f"the order «{имя}» on the set {S} is not linear: "
                       f"the elements {a} and {b} are incomparable.")
            вон.append(f"порядок «{ру_имя}» на множестве {S} не линеен: "
                       f"элементы {a} и {b} несравнимы.")
        else:
            вон.append(f"the order «{имя}» on the set {S} is linear: "
                       f"every two elements are comparable.")
            вон.append(f"порядок «{ру_имя}» на множестве {S} линеен: "
                       f"всякие два элемента сравнимы.")
        все_цепи = о.цепи(имя, множество)
        ц = все_цепи[шаг % len(все_цепи)]
        звенья = " - ".join(str(э) for э in ц)
        вон.append(f"{зачин} the chain {звенья} has length {len(ц)}: "
                   f"each element stands below the next.")
        вон.append(f"{ру_зачин} цепь {звенья} имеет длину {len(ц)}: "
                   f"каждый элемент стоит ниже следующего.")
        низ = о.наименьший(имя, множество)
        if низ is not None:
            вон.append(f"{зачин} the least element is {низ}: it stands "
                       f"below every element.")
            вон.append(f"{ру_зачин} наименьший элемент есть {низ}: он "
                       f"стоит ниже каждого элемента.")
        верх = о.наибольший(имя, множество)
        if верх is not None:
            вон.append(f"{зачин} the greatest element is {верх}: every "
                       f"element stands below it.")
            вон.append(f"{ру_зачин} наибольший элемент есть {верх}: "
                       f"каждый элемент стоит ниже него.")
        else:
            # ОТКАЗ С ОСНОВАНИЕМ: наибольшего нет НЕ ПОТОМУ, ЧТО НЕ
            # НАШЛИ, а потому, что два максимальных элемента не
            # сравнимы между собой, и суд эту причину проверяет.
            a, b = о.максимальные(имя, множество)[:2]
            вон.append(f"{зачин} there is no greatest element: {a} and "
                       f"{b} are incomparable.")
            вон.append(f"{ру_зачин} наибольшего элемента нет: {a} и {b} "
                       f"несравнимы.")
        for э in сдвиг(о.максимальные(имя, множество), шаг):
            вон.append(f"{зачин} the element {э} is maximal: no element "
                       f"stands above it.")
            вон.append(f"{ру_зачин} элемент {э} максимален: ни один "
                       f"элемент не стоит выше него.")
    return вон


# ══════════════ СВЯЗЬ И ПУТЬ ══════════════════════════════════════════


def связь(шаг):
    """ПУТЬ ЕСТЬ ОБХОД, А ЕГО ОТСУТСТВИЕ — ТОЖЕ ОБХОД, ДО КОНЦА."""
    вон = []
    узлы = сдвиг(о.УЗЛЫ, шаг)
    for откуда in узлы:
        свои = о.СМЕЖНЫЕ[откуда]
        if свои:
            куда = свои[шаг % len(свои)]
            вон.append(f"in the declared graph there is an edge from "
                       f"{откуда} to {куда}.")
            вон.append(f"в объявленном графе есть ребро из {откуда} в "
                       f"{куда}.")
        нет_ребра = [и for и in о.УЗЛЫ if и != откуда and и not in свои]
        если = нет_ребра[шаг % len(нет_ребра)]
        вон.append(f"in the declared graph there is no edge from "
                   f"{откуда} to {если}.")
        вон.append(f"в объявленном графе нет ребра из {откуда} в {если}.")
        дошли = о.достижимые(откуда)
        вон.append(f"in the declared graph the node {откуда} reaches "
                   f"{len(дошли)} {by_count(len(дошли), 'nodes')}.")
        вон.append(f"в объявленном графе узел {откуда} достигает "
                   f"{len(дошли)} {ру_узел(len(дошли))}.")
        for куда in сдвиг(о.УЗЛЫ, шаг):
            если = о.путь(откуда, куда)
            if если is not None:
                шагов = len(если) - 1
                дорога = " - ".join(если)
                вон.append(f"in the declared graph there is a connection "
                           f"from {откуда} to {куда}: the path {дорога} "
                           f"of length {шагов}.")
                вон.append(f"в объявленном графе есть связь из {откуда} "
                           f"в {куда}: путь {дорога} длины {шагов}.")
                вон.append(f"in the declared graph the shortest path "
                           f"from {откуда} to {куда} has length {шагов}.")
                вон.append(f"в объявленном графе кратчайший путь из "
                           f"{откуда} в {куда} имеет длину {шагов}.")
            elif куда != откуда:
                # ДВЕ РАЗНЫЕ ПРИЧИНЫ ОТСУТСТВИЯ ПУТИ, И ОБЕ НАЗВАНЫ:
                # тупик (из узла не ведёт ни одного ребра) и предел
                # обхода (обход дошёл, докуда дошёл, и цели там нет).
                if not свои:
                    вон.append(f"in the declared graph there is no path "
                               f"from {откуда} to {куда}: from the node "
                               f"{откуда} no edge leads out.")
                    вон.append(f"в объявленном графе нет пути из "
                               f"{откуда} в {куда}: из узла {откуда} не "
                               f"ведёт ни одного ребра.")
                else:
                    вон.append(f"in the declared graph there is no path "
                               f"from {откуда} to {куда}: the walk from "
                               f"{откуда} reaches {len(дошли)} "
                               f"{by_count(len(дошли), 'nodes')}, and "
                               f"{куда} is not among them.")
                    вон.append(f"в объявленном графе нет пути из "
                               f"{откуда} в {куда}: обход из {откуда} "
                               f"достигает {len(дошли)} "
                               f"{ру_узел(len(дошли))}, и {куда} среди "
                               f"них нет.")
    n, m = len(о.УЗЛЫ), len(о.РЁБРА)
    вон.append(f"the declared graph is a structure of {n} nodes and {m} "
               f"edges.")
    вон.append(f"объявленный граф есть структура из {n} {ру_узел(n)} и "
               f"{m} {ру_ребро(m)}.")
    return вон


# ══════════════ ПРОСТРАНСТВО ══════════════════════════════════════════


def пространство(шаг):
    """МНОЖЕСТВО С РАССТОЯНИЕМ ЕСТЬ ПРОСТРАНСТВО, И ЗАКОНЫ ПРОВЕРЯЕМЫ."""
    вон = []
    узлы = сдвиг(о.УЗЛЫ, шаг)
    for i, a in enumerate(узлы):
        b = узлы[(i + 1) % len(узлы)]
        d = о.расстояние(a, b)
        вон.append(f"in the space of the declared graph the distance "
                   f"between {a} and {b} is {d}.")
        вон.append(f"в пространстве объявленного графа расстояние между "
                   f"{a} и {b} равно {d}.")
        вон.append(f"in the space of the declared graph the distance "
                   f"between {a} and {b} equals the distance between "
                   f"{b} and {a}: the distance is symmetric.")
        вон.append(f"в пространстве объявленного графа расстояние между "
                   f"{a} и {b} равно расстоянию между {b} и {a}: "
                   f"расстояние симметрично.")
        # НЕРАВЕНСТВО ТРЕУГОЛЬНИКА ПОКАЗАНО НА ТРЕТЬЕМ УЗЛЕ, ОТЛИЧНОМ
        # ОТ ОБОИХ: при c, равном одному из концов, неравенство
        # обращается в равенство и о законе не говорит ничего.
        c = узлы[(i + 3) % len(узлы)]
        вон.append(f"in the space of the declared graph the distance "
                   f"between {a} and {b} is not greater than the "
                   f"distance through {c}: {d} against "
                   f"{о.расстояние(a, c)} plus {о.расстояние(c, b)}.")
        вон.append(f"в пространстве объявленного графа расстояние между "
                   f"{a} и {b} не больше расстояния через {c}: {d} "
                   f"против {о.расстояние(a, c)} плюс "
                   f"{о.расстояние(c, b)}.")
    вон.append(f"the nodes of the declared graph with this distance "
               f"form a space: the distance is symmetric, vanishes only "
               f"between a node and itself, and never exceeds the sum "
               f"through a third node.")
    вон.append(f"узлы объявленного графа с этим расстоянием образуют "
               f"пространство: расстояние симметрично, обращается в "
               f"ноль только между узлом и им самим и никогда не "
               f"превышает суммы через третий узел.")
    return вон


# ══════════════ ВОПРОСНАЯ ПОВЕРХНОСТЬ ═════════════════════════════════


def вопросы(шаг):
    """ЗНАНИЕ БЕЗ ВОПРОСНОЙ ПОВЕРХНОСТИ НЕ ОТВЕЧАЕТ, ОНО СООБЩАЕТ.

    Вопрос здесь есть ПРИСТАВКА К ОТВЕТУ: ответом стоит показ, уже
    судимый своим родом, и суд требует, чтобы всё названное в вопросе
    стояло в ответе. Оттого вопросов ровно столько, сколько родов, и
    ни один из них не заводит второго вычисления.
    """
    вон = []
    S = набор(о.МНОЖЕСТВО)
    узел = сдвиг(о.ИМЕНА, шаг)[0]
    к = о.уровень(узел)
    вон.append(f"at what level does the node {узел} stand? the level of "
               f"the node {узел} is {к}.")
    вон.append(f"на каком уровне стоит узел {узел}? уровень узла {узел} "
               f"равен {к}.")
    вниз = о.потомки(узел)
    if вниз:
        низ = вниз[шаг % len(вниз)]
        вон.append(f"does the node {узел} contain the node {низ}? in the "
                   f"tree of kinds the node {узел} contains the node "
                   f"{низ}.")
        вон.append(f"содержит ли узел {узел} узел {низ}? в дереве родов "
                   f"узел {узел} содержит узел {низ}.")
    for имя, ру_имя, _п in сдвиг(о.ОТНОШЕНИЯ, шаг)[:3]:
        свид = о.свидетель_транзитивности(имя)
        if свид is None:
            хвост = (f"on the set {S} the relation «{имя}» is "
                     f"transitive: if a stands to b and b stands to c, "
                     f"then a stands to c.")
            ру_хвост = (f"на множестве {S} отношение «{ру_имя}» "
                        f"транзитивно: если a относится к b и b "
                        f"относится к c, то a относится к c.")
        else:
            a, b, c = свид
            хвост = (f"on the set {S} the relation «{имя}» is not "
                     f"transitive: {a} stands to {b} and {b} stands to "
                     f"{c}, but {a} does not stand to {c}.")
            ру_хвост = (f"на множестве {S} отношение «{ру_имя}» не "
                        f"транзитивно: {a} относится к {b} и {b} "
                        f"относится к {c}, но {a} не относится к {c}.")
        вон.append(f"is the relation «{имя}» on the set {S} transitive? "
                   f"{хвост}")
        вон.append(f"транзитивно ли отношение «{ру_имя}» на множестве "
                   f"{S}? {ру_хвост}")
    модуль = сдвиг(о.МОДУЛИ, шаг)[0]
    н = о.ЧИСЛА[шаг % len(о.ЧИСЛА)]
    о_ст = о.остаток(н, модуль)
    вон.append(f"in what class modulo {модуль} does the number {н} "
               f"stand? the number {н} stands in the class of remainder "
               f"{о_ст} modulo {модуль}.")
    вон.append(f"в каком классе по модулю {модуль} стоит число {н}? "
               f"число {н} стоит в классе остатка {о_ст} по модулю "
               f"{модуль}.")
    for имя, ру_имя, ан_обл, ру_обл, _п in сдвиг(о.СООТВЕТСТВИЯ, шаг)[:2]:
        n = len(о.отображение(имя))
        if о.однозначно(имя):
            хвост = (f"the correspondence «{имя}» on {ан_обл} is "
                     f"one-to-one: {n} {by_count(n, 'elements')} and "
                     f"{n} {by_count(n, 'values')}.")
            ру_хвост = (f"соответствие «{ру_имя}» на {ру_обл} "
                        f"взаимно-однозначно: {n} {ру_элемент(n)} и {n} "
                        f"{о.ру('значение', n)}.")
        else:
            a, b, з = о.свидетель_однозначности(имя)
            хвост = (f"the correspondence «{имя}» on {ан_обл} is not "
                     f"one-to-one: the elements {a} and {b} go to one "
                     f"and the same value {з}.")
            ру_хвост = (f"соответствие «{ру_имя}» на {ру_обл} не "
                        f"взаимно-однозначно: элементы {a} и {b} "
                        f"переходят в одно и то же значение {з}.")
        вон.append(f"is the correspondence «{имя}» on {ан_обл} "
                   f"one-to-one? {хвост}")
        вон.append(f"взаимно-однозначно ли соответствие «{ру_имя}» на "
                   f"{ру_обл}? {ру_хвост}")
    имя, множество = сдвиг(о.ПОРЯДКИ, шаг)[0]
    ру_имя = о.ИМЯ_ПО_РУССКИ[имя]
    S2 = набор(множество)
    врозь = о.несравнимые(имя, множество)
    if врозь:
        a, b = врозь[шаг % len(врозь)]
        хвост = (f"in the order «{имя}» on the set {S2} the elements {a} "
                 f"and {b} are incomparable: neither stands below the "
                 f"other.")
        ру_хвост = (f"в порядке «{ру_имя}» на множестве {S2} элементы "
                    f"{a} и {b} несравнимы: ни один не стоит ниже "
                    f"другого.")
    else:
        ниже = [(x, y) for x, y in о.пары(имя, множество) if x != y]
        a, b = ниже[шаг % len(ниже)]
        хвост = (f"in the order «{имя}» on the set {S2} the element {a} "
                 f"stands below the element {b}.")
        ру_хвост = (f"в порядке «{ру_имя}» на множестве {S2} элемент {a} "
                    f"стоит ниже элемента {b}.")
    вон.append(f"are the elements {a} and {b} comparable in the order "
               f"«{имя}»? {хвост}")
    вон.append(f"сравнимы ли элементы {a} и {b} в порядке «{ру_имя}»? "
               f"{ру_хвост}")
    for откуда in сдвиг(о.УЗЛЫ, шаг)[:3]:
        куда = сдвиг(о.УЗЛЫ, шаг + 3)[0]
        если = о.путь(откуда, куда)
        if если is None:
            continue
        шагов = len(если) - 1
        дорога = " - ".join(если)
        вон.append(f"is there a path from {откуда} to {куда} in the "
                   f"declared graph? in the declared graph there is a "
                   f"connection from {откуда} to {куда}: the path "
                   f"{дорога} of length {шагов}.")
        вон.append(f"есть ли путь из {откуда} в {куда} в объявленном "
                   f"графе? в объявленном графе есть связь из {откуда} в "
                   f"{куда}: путь {дорога} длины {шагов}.")
        вон.append(f"how long is the shortest path from {откуда} to "
                   f"{куда} in the declared graph? in the declared graph "
                   f"the shortest path from {откуда} to {куда} has "
                   f"length {шагов}.")
        вон.append(f"какова длина кратчайшего пути из {откуда} в {куда} "
                   f"в объявленном графе? в объявленном графе кратчайший "
                   f"путь из {откуда} в {куда} имеет длину {шагов}.")
    return вон


ГРУППЫ = (иерархия, свойства, замыкания, эквивалентности, соответствия,
          порядки, связь, пространство, вопросы)


def pass_groups(шаг):
    return [сделать(шаг) for сделать in ГРУППЫ]


def main():
    беды = о.оракул()
    if беды:
        print(f"СТРОЕНИЕ ОТКАЗ: {len(беды)} расхождений на встречных "
              f"ходах — слой не собран: {беды[:2]}")
        return 2
    emit_grouped("datasets/genesis_relation.txt", pass_groups)
    return 0


if __name__ == "__main__":
    sys.exit(main())
