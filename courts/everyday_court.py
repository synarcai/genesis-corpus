#!/usr/bin/env python3
"""СУД БЫТА: слово прожито честно или не прожито вовсе.

Мир быта заведён ради СЛОВ, и потому соблазн его — насыпать бытовых
предложений и объявить словарь покрытым. Этот суд стоит ровно против
такого соблазна: он не спрашивает, красиво ли сказано, он ПЕРЕСЧИТЫВАЕТ
основание каждой строки — и строка, основания не имеющая, остаётся
несудимой, а ворота записи несудимую не пропускают.

ЧТО ИМЕННО ПЕРЕСЧИТЫВАЕТСЯ, РОД ЗА РОДОМ:

    СЧЁТ        — сумма покупки, разность траты, произведение доли,
                  частное дележа: числа складываются заново;
    ВМЕСТИЛИЩЕ  — ДОСТИЖИМОСТЬ ПРОХОДИТСЯ ПО ДЕРЕВУ (`путь_вверх`), а
                  не сверяется со списком выводов; и ОТКАЗ проверяется
                  тем же ходом: место, названное недостижимым, обязано
                  не лежать на пути;
    ВРЕМЯ       — «before» и «after» сверяются с ОБЪЯВЛЕННЫМ рядом, и
                  «next» требует именно соседа, а не любого, кто позже;
    ФОРМЫ       — прошедшее правильного глагола ВЫВОДИТСЯ правилом
                  заново, и совпадение с показом есть вердикт; список
                  неправильных читается как список исключений, а не
                  как ответ на всякий вопрос;
    КВАНТОР И ЧАСТОТА — «all / some / no / both», «never / once /
                  often / always» ВЫЧИСЛЯЮТСЯ из пары чисел: слой,
                  сказавший «some» там, где все, лжёт, и эта ложь не
                  видна ни одному счётному прибору;
    АНГЛИЙСКИЕ МЕЛОЧИ — артикль по ЗВУКУ («an hour», не «a hour»),
                  число по счёту («1 apple», не «1 apples»), связка по
                  числу («there is 1 book», «there are 3 books»).
                  Мелочь, выученная неверно, выучивается навсегда;
    РУССКОЕ СОГЛАСОВАНИЕ — форма при счёте берётся из `tools/rugram.py`
                  и сверяется оттуда же: суд не знает русского языка,
                  он знает объявленные тройки.

СУД ЧИТАЕТ СВОЙ РОД И ТОЛЬКО СВОЙ. Образцы привязаны к зачину и
закрыты с обоих концов; имя, не объявленное в доме этого мира,
отнимает подсудность, а не даёт обвинение. Суд, обвиняющий слишком
охотно, опаснее молчащего: его вердикт выглядит работой.

ОБЪЯВЛЕНИЕ ОДНО НА ДВОИХ, ВЫВОД — У КАЖДОГО СВОЙ. Дерево мест, ряды
времени и таблицы глаголов живут в генераторе; суд читает их оттуда
(как суд разметки читает свой генератор) и ВЫВОДИТ по ним заново.
Второе объявление здесь было бы двойником, и разошлось бы с первым в
тот же день, что и всякий двойник.
"""

import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import gen_genesis_everyday as дом  # noqa: E402
import rugram  # noqa: E402
from genesis import Unreadable, worlds  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file


# ─── ДОМ ИМЁН: ОБРАТНЫЙ ХОД ОТ ФОРМЫ К СЛОВУ ───────────────────────
#
# Слой пишет «3 apples», а суд читает «apples» и обязан узнать, что это
# «apple». Обратный ход строится из ТОГО ЖЕ правила, каким слой писал:
# суд, заведший свой список множественных, судил бы собственную копию.
_ИМЕНА = ({en for en, _ru in дом.ВЕЩИ}
          | {роль for тройка in дом.РОЛИ for роль in тройка[:3]}
          | set(дом.МЕСТА)
          | {"student", "friend", "day", "thing", "coin", "hour",
             "cup", "loaf"})
_ПО_МН = {дом.множественное(с): с for с in _ИМЕНА}


def _ед(слово):
    """Единственное число по любой форме имени, или None."""
    if слово in _ИМЕНА:
        return слово
    return _ПО_МН.get(слово)


def _форма_верна(n, слово):
    """Английская форма имени при числе: 1 — единственное, прочее — мн."""
    имя = _ед(слово)
    return имя is not None and слово == дом.по_счёту(n, имя)


def _ру_ключ(форма):
    """Счётный ключ русского дома по любой его форме, или None."""
    return rugram.ПО_ФОРМЕ.get(форма)


def _ру_верна(n, форма):
    """Русская форма при счёте — по объявленной тройке дома форм."""
    ключ = _ру_ключ(форма)
    return ключ is not None and форма == rugram.форма(ключ, n)


def _ру_пара(n, форма, ключ):
    """Та же проверка, когда ключ уже известен по соседней форме."""
    return ключ is not None and форма == rugram.форма(ключ, n)


def _место_по_русски(предлог, местный):
    """Английское имя места по русскому предлогу и местному падежу.

    Русский показ не называет английского имени, и суд обязан найти
    его сам — иначе он проверял бы русскую строку по русской строке.
    """
    for имя, (_п, п_ru, _им, _род, м_ru) in дом.МЕСТА.items():
        if п_ru == предлог and м_ru == местный:
            return имя
    return None


def _место_по_имени_ru(имя_ru):
    for имя, (_п, _п_ru, им, _род, _м) in дом.МЕСТА.items():
        if им == имя_ru:
            return имя
    return None


# ─── ГЛАГОЛЫ: ОТ ПОКАЗАННОЙ ФОРМЫ К ОСНОВЕ ─────────────────────────
_ГЛАГОЛ_ЕД = {(дом.третье_лицо(г), один): г
              for г, один, _много in дом.ГЛАГОЛЫ}
_ГЛАГОЛ_МН = {(г, много): г for г, _один, много in дом.ГЛАГОЛЫ}
_ОСНОВЫ = {г for г, _о, _м in дом.ГЛАГОЛЫ}
_ГЛАГОЛ_RU = {(наст, доп): (инф, прош)
              for инф, наст, прош, доп in дом.ГЛАГОЛЫ_RU}
_ГЛАГОЛ_RU_ИНФ = {инф: прош for инф, _н, прош, _д in дом.ГЛАГОЛЫ_RU}

# ─── РЯДЫ ВРЕМЕНИ: МЕСТО В РЯДУ, А НЕ ПАМЯТЬ О ПАРЕ ────────────────
_МЕСТО_В_СУТКАХ = {имя: i for i, имя in enumerate(дом.СУТКИ)}
_МЕСТО_В_ДНЯХ = {имя: i for i, имя in enumerate(дом.ДНИ)}
_СУТКИ_ПО_ИМ = {формы[0]: имя for имя, формы in дом.СУТКИ_RU.items()}
_СУТКИ_ПО_РОД = {формы[1]: имя for имя, формы in дом.СУТКИ_RU.items()}
_СУТКИ_ПО_ТВОР = {формы[2]: имя for имя, формы in дом.СУТКИ_RU.items()}
_ДНИ_ПО_RU = {ru: en for en, ru in дом.ДНИ_RU.items()}

# ─── РОЛИ: ОБЪЯВЛЕННАЯ ТРОЙКА ──────────────────────────────────────
_РОЛИ_EN = {(ч1, ч2): целое for ч1, ч2, целое, _r1, _r2, _rц in дом.РОЛИ}
_РОЛИ_RU = {(ру1, ру2): ру_целое
            for _ч1, _ч2, _ц, ру1, ру2, ру_целое in дом.РОЛИ}

# ─── ЛЮДИ: ИМЯ, РОДИТЕЛЬНЫЙ И РОД ПРОШЕДШЕГО ───────────────────────
_ИМЕНА_RU = {ru: (род, суф) for _en, ru, род, ж in дом.ЛЮДИ
             for суф in (дом.суффикс_рода(ж),)}
_РОД_ПО_ИМЕНИ = {род: (ru, дом.суффикс_рода(ж))
                 for _en, ru, род, ж in дом.ЛЮДИ}


def _суффикс_верен(имя_ru, суф):
    """Русское прошедшее метит род деятеля, и суд метит его снова."""
    свой = _ИМЕНА_RU.get(имя_ru)
    return свой is not None and свой[1] == суф


# ═══ ОБРАЗЦЫ ═══════════════════════════════════════════════════════
#
# Всякий образец закрыт с обоих концов и привязан к зачину: суд не
# смеет узнать в чужой строке свою.

ПОКУПКА = re.compile(
    r"^([a-z]+) bought (\d+) ([a-z]+) and (\d+) ([a-z]+) at the "
    r"([a-z ]+); \1 bought (\d+) things in all: (\d+) \+ (\d+) = (\d+)\.$")
ПОКУПКА_ВОПРОС = re.compile(
    r"^([a-z]+) bought (\d+) ([a-z]+) and (\d+) ([a-z]+) at the "
    r"([a-z ]+)\. how many things did \1 buy\? \1 bought (\d+) "
    r"things in all: (\d+) \+ (\d+) = (\d+)\.$")
ПОКУПКА_RU = re.compile(
    r"^(\S+) купил(а?) (\d+) (\S+) и (\d+) (\S+) (в|на) (\S+); всего "
    r"\1 купил\2 (\d+) (\S+): (\d+) \+ (\d+) = (\d+)\.$")
ПОКУПКА_RU_ВОПРОС = re.compile(
    r"^(\S+) купил(а?) (\d+) (\S+) и (\d+) (\S+) (в|на) (\S+)\. "
    r"сколько предметов купил\2 \1\? всего \1 купил\2 (\d+) (\S+): (\d+) \+ (\d+) = (\d+)\.$")

МЕСТО = re.compile(r"^the ([a-z ]+) is (on|in|at) the ([a-z ]+)\.$")
МЕСТО_ЧЕРЕЗ = re.compile(
    r"^the ([a-z ]+) is (on|in|at) the ([a-z ]+), and the ([a-z ]+) "
    r"is (on|in|at) the ([a-z ]+); so the ([a-z ]+) is (on|in|at) "
    r"the ([a-z ]+)\.$")
МЕСТО_ВОПРОС = re.compile(
    r"^the ([a-z ]+) is (on|in|at) the ([a-z ]+), and the ([a-z ]+) "
    r"is (on|in|at) the ([a-z ]+)\. where is the ([a-z ]+)\? the "
    r"([a-z ]+) is (on|in|at) the ([a-z ]+)\.$")
МЕСТО_ОТКАЗ = re.compile(
    r"^the ([a-z ]+) is not (on|in|at) the ([a-z ]+): the ([a-z ]+) "
    r"is not on the path from the ([a-z ]+) to the ([a-z ]+)\.$")
МЕСТО_RU = re.compile(r"^(\S+) (в|на) (\S+)\.$")
МЕСТО_RU_ЧЕРЕЗ = re.compile(
    r"^(\S+) (в|на) (\S+), а (\S+) (в|на) (\S+); значит (\S+) (в|на) "
    r"(\S+)\.$")
МЕСТО_RU_ВОПРОС = re.compile(
    r"^(\S+) (в|на) (\S+), а (\S+) (в|на) (\S+)\. где (\S+)\? (\S+) "
    r"(в|на) (\S+)\.$")
МЕСТО_RU_ОТКАЗ = re.compile(
    r"^(\S+) не (в|на) (\S+): (\S+) не на пути от (\S+) до (\S+)\.$")

ВРЕМЯ_ДО = re.compile(r"^the ([a-z]+) comes before the ([a-z]+)\.$")
ВРЕМЯ_ПОСЛЕ = re.compile(r"^the ([a-z]+) comes after the ([a-z]+)\.$")
ВРЕМЯ_СЛЕД = re.compile(
    r"^the ([a-z]+) comes next after the ([a-z]+)\.$")
ВРЕМЯ_ВОПРОС = re.compile(
    r"^what comes before the ([a-z]+)\? the ([a-z]+) comes before "
    r"the \1\.$")
ВРЕМЯ_КРАЙ = re.compile(
    r"^the ([a-z]+) comes first and the ([a-z]+) comes last\.$")
ВРЕМЯ_РАНО = re.compile(
    r"^the ([a-z]+) comes early and the ([a-z]+) comes late\.$")
ВРЕМЯ_РАБОТА = re.compile(
    r"^([a-z]+) worked (in|during) the ([a-z]+) and rested "
    r"(in|during) the ([a-z]+); \1 worked before \1 rested\.$")
ВРЕМЯ_ПОКА = re.compile(
    r"^([a-z]+) worked in the ([a-z]+) and ([a-z]+) rested in the "
    r"([a-z]+); \1 worked while \3 rested\.$")
ВРЕМЯ_СЕЙЧАС = re.compile(
    r"^([a-z]+) works now and rests later; \1 works before \1 "
    r"rests\.$")
ВРЕМЯ_ДОМ = re.compile(
    r"^([a-z]+) left home in the ([a-z]+) and arrived at the "
    r"([a-z ]+) in the ([a-z]+); \1 left home before \1 arrived at "
    r"the ([a-z ]+)\.$")
ДЕНЬ_ДО = re.compile(r"^([a-z]+) comes before ([a-z]+)\.$")
ДЕНЬ_ПОСЛЕ = re.compile(r"^([a-z]+) comes after ([a-z]+)\.$")
НЕДЕЛЯ = re.compile(
    r"^the ([a-z]+) has (\d+) days and the ([a-z]+) has (\d+) days; "
    r"the \1 has (\d+) days more than the \3\.$")
ВРЕМЯ_RU_ДО = re.compile(r"^(\S+) раньше (\S+)\.$")
ВРЕМЯ_RU_ПОСЛЕ = re.compile(r"^(\S+) позже (\S+)\.$")
ВРЕМЯ_RU_ВОПРОС = re.compile(
    r"^что раньше (\S+)\? (\S+) раньше \1\.$")
ВРЕМЯ_RU_РАБОТА = re.compile(
    r"^(\S+) работал(а?) (\S+), а отдыхал\2 (\S+); значит \1 "
    r"работал\2 раньше, чем отдыхал\2\.$")
ВРЕМЯ_RU_ВМЕСТЕ = re.compile(
    r"^(\S+) работал(а?) (\S+), а (\S+) отдыхал(а?) (\S+); они "
    r"делали это в одно время\.$")
ВРЕМЯ_RU_ДОМ = re.compile(
    r"^(\S+) (ушёл|ушла) из дома (\S+), а (пришёл|пришла) (в|на) "
    r"(\S+) (\S+); значит \1 \2 раньше, чем \4\.$")
ДЕНЬ_RU = re.compile(r"^(\S+) раньше, чем (\S+)\.$")
НЕДЕЛЯ_RU = re.compile(
    r"^в неделе (\d+) (\S+), а в выходных (\d+) (\S+); в неделе на "
    r"(\d+) (\S+) больше\.$")

ГЛАГОЛ_ДВОЕ = re.compile(
    r"^today ([a-z]+) and ([a-z]+) ([a-z]+) (.+); yesterday \1 and "
    r"\2 ([a-z]+) \4\.$")
ГЛАГОЛ_ОДИН = re.compile(
    r"^today ([a-z]+) ([a-z]+) (.+); yesterday \1 ([a-z]+) \3\.$")
ГЛАГОЛ_ПРОШ = re.compile(r"^the past of ([a-z]+) is ([a-z]+)\.$")
ГЛАГОЛ_ВОПРОС = re.compile(
    r"^today ([a-z]+) ([a-z]+) (.+)\. what is the past of ([a-z]+)\? "
    r"the past of \4 is ([a-z]+)\.$")
ГЛАГОЛ_RU = re.compile(
    r"^сегодня (\S+) (\S+) (.+); вчера \1 (\S+) \3\.$")
ГЛАГОЛ_RU_ИМЯ = re.compile(
    r"^глагол «(\S+)» в прошедшем даёт «(\S+)»\.$")

БОЛЬШЕ = re.compile(
    r"^([a-z]+) has (\d+) ([a-z]+), and ([a-z]+) has (\d+) ([a-z]+); "
    r"\1 has (\d+) more ([a-z]+) than \4\.$")
МЕНЬШЕ = re.compile(
    r"^([a-z]+) has (\d+) ([a-z]+), and ([a-z]+) has (\d+) ([a-z]+); "
    r"\1 has (\d+) fewer ([a-z]+) than \4\.$")
СТОЛЬКО_ЖЕ = re.compile(
    r"^([a-z]+) has (\d+) ([a-z]+), and ([a-z]+) has (\d+) ([a-z]+); "
    r"\1 has the same number of ([a-z]+) as \4\.$")
БОЛЬШЕ_ВОПРОС = re.compile(
    r"^([a-z]+) has (\d+) ([a-z]+), and ([a-z]+) has (\d+) "
    r"([a-z]+)\. how many more ([a-z]+) does \1 have than \4\? \1 "
    r"has (\d+) more ([a-z]+) than \4\.$")
КРАЙНИЕ = re.compile(
    r"^([a-z]+) has (\d+) ([a-z]+), ([a-z]+) has (\d+) ([a-z]+) and "
    r"([a-z]+) has 1 ([a-z]+); \1 has the most ([a-z]+) and \7 has "
    r"the least ([a-z]+)\.$")
ВДВОЕ = re.compile(
    r"^([a-z]+) has (\d+) ([a-z]+), and ([a-z]+) has (\d+) ([a-z]+); "
    r"\1 has twice as many ([a-z]+) as \4\.$")
КРАТНО = re.compile(
    r"^([a-z]+) has (\d+) ([a-z]+), and ([a-z]+) has (\d+) ([a-z]+); "
    r"\1 has (double|triple) the ([a-z]+) of \4\.$")
ПОЛОВИНА = re.compile(
    r"^([a-z]+) has (\d+) ([a-z]+), and ([a-z]+) has (\d+) ([a-z]+); "
    r"\4 has half the ([a-z]+) of \1\.$")
РАВНЫ = re.compile(
    r"^([a-z]+) has (\d+) ([a-z]+), and ([a-z]+) has (\d+) ([a-z]+); "
    r"the two counts are (equal|different)\.$")
ВМЕСТЕ_ВРОЗЬ = re.compile(
    r"^([a-z]+) has (\d+) ([a-z]+), and ([a-z]+) has (\d+) ([a-z]+); "
    r"together they have (\d+) ([a-z]+), and apart they have (\d+) "
    r"([a-z]+) and (\d+) ([a-z]+)\.$")
ИТОГО = re.compile(
    r"^([a-z]+) has (\d+) ([a-z]+), and ([a-z]+) has (\d+) ([a-z]+); "
    r"the total comes to (\d+) ([a-z]+) altogether\.$")
ТОЛЬКО = re.compile(
    r"^([a-z]+) bought (\d+) ([a-z]+), but ([a-z]+) bought just "
    r"(\d+) ([a-z]+); (\d+) ([a-z]+) are fewer than (\d+) ([a-z]+), "
    r"and \4 bought less than \1\.$")
ДРУГ_ДРУГУ = re.compile(
    r"^([a-z]+) and ([a-z]+) gave (\d+) ([a-z]+) to each other; \1 "
    r"gave (\d+) ([a-z]+) to \2, and \2 gave (\d+) ([a-z]+) to \1\.$")
МЕНЬШЕ_МАССЫ = re.compile(
    r"^([a-z]+) bought (\d+) ([a-z]+) of ([a-z]+), and ([a-z]+) "
    r"bought (\d+) ([a-z]+) of \4; \5 bought less \4 than \1\.$")
БОЛЬШЕ_RU = re.compile(
    r"^у (\S+) (\d+) (\S+), а у (\S+) (\d+) (\S+); у \1 на (\d+) "
    r"(\S+) больше, чем у \4\.$")
МЕНЬШЕ_RU = re.compile(
    r"^у (\S+) (\d+) (\S+), а у (\S+) (\d+) (\S+); у \1 на (\d+) "
    r"(\S+) меньше, чем у \4\.$")
ПОРОВНУ_RU = re.compile(
    r"^у (\S+) (\d+) (\S+), и у (\S+) (\d+) (\S+); у них поровну "
    r"(\S+)\.$")
ВМЕСТЕ_RU = re.compile(
    r"^у (\S+) (\d+) (\S+), а у (\S+) (\d+) (\S+); вместе у них "
    r"(\d+) (\S+)\.$")
БОЛЬШЕ_ВОПРОС_RU = re.compile(
    r"^у (\S+) (\d+) (\S+), а у (\S+) (\d+) (\S+)\. на сколько (\S+) "
    r"больше у \1\? у \1 на (\d+) (\S+) больше, чем у \4\.$")
ВДВОЕ_RU = re.compile(
    r"^у (\S+) (\d+) (\S+), а у (\S+) (\d+) (\S+); у \1 вдвое "
    r"больше, чем у \4\.$")
МАССА_RU = re.compile(
    r"^(\S+) купил(а?) (\d+) (\S+) (\S+), а (\S+) купил(а?) (\d+) "
    r"(\S+) \5; у (\S+) \5 меньше, чем у (\S+)\.$")

ОСТАТОК = re.compile(
    r"^([a-z]+) had (\d+) ([a-z]+) and used (\d+) ([a-z]+); (\d+) "
    r"([a-z]+) remain\.$")
ОСТАТОК_ПРОЧЕЕ = re.compile(
    r"^([a-z]+) had (\d+) ([a-z]+) and used (\d+) ([a-z]+); the rest "
    r"are (\d+) ([a-z]+)\.$")
ОСТАТОК_СВЕРХ = re.compile(
    r"^([a-z]+) had (\d+) ([a-z]+) and used (\d+) ([a-z]+); (\d+) "
    r"([a-z]+) are left over\.$")
ОСТАТОК_ХРАНИТ = re.compile(
    r"^([a-z]+) had (\d+) ([a-z]+) and used (\d+) ([a-z]+); \1 keeps "
    r"the remaining (\d+) ([a-z]+)\.$")
ОСТАТОК_ВОПРОС = re.compile(
    r"^([a-z]+) had (\d+) ([a-z]+) and used (\d+) ([a-z]+)\. how "
    r"many ([a-z]+) remain\? (\d+) ([a-z]+) remain\.$")
ОСТАТОК_RU = re.compile(
    r"^у (\S+) было (\d+) (\S+), (\S+) израсходовал(а?) (\d+) (\S+); "
    r"осталось (\d+) (\S+)\.$")
ОСТАТОК_RU_ВОПРОС = re.compile(
    r"^у (\S+) было (\d+) (\S+), (\S+) израсходовал(а?) (\d+) "
    r"(\S+)\. сколько (\S+) осталось\? осталось (\d+) (\S+)\.$")

ВМЕЩАЕТ = re.compile(
    r"^the ([a-z ]+) holds (\d+) ([a-z]+); ([a-z]+) filled the \1 "
    r"with (\d+) ([a-z]+); the \1 needs (\d+) ([a-z]+) more\.$")
ВМЕЩАЕТ_НЫНЕ = re.compile(
    r"^the ([a-z ]+) holds (\d+) ([a-z]+); ([a-z]+) fills the \1 "
    r"with (\d+) ([a-z]+) and needs (\d+) ([a-z]+) more\.$")
ВМЕЩАЕТ_ВОПРОС = re.compile(
    r"^the ([a-z ]+) holds (\d+) ([a-z]+) and ([a-z]+) filled the \1 "
    r"with (\d+) ([a-z]+)\. how many ([a-z]+) does the \1 need\? the "
    r"\1 needs (\d+) ([a-z]+) more\.$")
ОПУСТОШЕНО = re.compile(
    r"^([a-z]+) (emptied|empties) the ([a-z ]+) of (\d+) ([a-z]+); "
    r"the \3 keeps 0 ([a-z]+) (now|then)\.$")
ВМЕЩАЕТ_RU = re.compile(
    r"^(\S+) вмещает (\d+) (\S+); (\S+) положил(а?) туда (\d+) "
    r"(\S+); не хватает ещё (\d+) (\S+)\.$")
ОПУСТОШЕНО_RU = re.compile(
    r"^(\S+) освободил(а?) (\S+): было (\d+) (\S+), теперь там 0 "
    r"(\S+)\.$")

ДЕЛЁЖ = re.compile(
    r"^([a-z]+) shared (\d+) ([a-z]+) among (\d+) friends; each "
    r"friend got (\d+) ([a-z]+)\.$")
ДЕЛЁЖ_НЫНЕ = re.compile(
    r"^([a-z]+) shares (\d+) ([a-z]+) among (\d+) friends; every "
    r"friend gets (\d+) ([a-z]+)\.$")
ДЕЛЁЖ_ВОПРОС = re.compile(
    r"^([a-z]+) shared (\d+) ([a-z]+) among (\d+) friends\. how many "
    r"([a-z]+) did each friend get\? each friend got (\d+) "
    r"([a-z]+)\.$")
ДЕЛЁЖ_RU = re.compile(
    r"^(\S+) разделил(а?) (\d+) (\S+) между (\d+) друзьями; каждому "
    r"досталось по (\d+) (\S+)\.$")

ДЕНЬГИ = re.compile(
    r"^([a-z]+) (earned|earns) (\d+) coins and (paid|pays) (\d+) "
    r"(coins?) for a ticket; \1 (saved|saves) (\d+) coins\.$")
ДЕНЬГИ_ВОПРОС = re.compile(
    r"^([a-z]+) earned (\d+) coins and paid (\d+) (coins?) for a "
    r"ticket\. how many coins did \1 save\? \1 saved (\d+) coins\.$")
ДЕНЬГИ_RU = re.compile(
    r"^(\S+) заработал(а?) (\d+) (\S+) и заплатил\2 (\d+) (\S+) за "
    r"билет; \1 отложил\2 (\d+) (\S+)\.$")

КВАНТОР = re.compile(
    r"^(\d+) students are in the class, and (\d+) (students?) "
    r"(have|has) a key; ([a-z ]+) students have a key\.$")
КВАНТОР_ЛИЦО = re.compile(
    r"^(\d+) students are in the class, and (\d+) (students?) "
    r"(have|has) a key; ([a-z ]+) in the class has a key\.$")
КАЖДЫЙ = re.compile(
    r"^(\d+) students are in the class, and (each|every) student has "
    r"(\d+) ([a-z]+); the class has (\d+) books\.$")
КАЖДЫЙ_ВОПРОС = re.compile(
    r"^(\d+) students are in the class, and each student has (\d+) "
    r"([a-z]+)\. how many books does the class have\? the class has "
    r"(\d+) books\.$")
ИНОЙ = re.compile(
    r"^([a-z]+) has 2 ([a-z]+); \1 read 1 ([a-z]+) and keeps the "
    r"other ([a-z]+)\.$")
ЕЩЁ_ОДИН = re.compile(
    r"^([a-z]+) has 1 ([a-z]+) and bought another ([a-z]+); \1 has 2 "
    r"([a-z]+)\.$")
КВАНТОР_RU = re.compile(
    r"^у (\S+) (\d+) (\S+), и (\d+) (\S+) прочитаны; (.+)\.$")
КАЖДЫЙ_RU = re.compile(
    r"^у (\S+) (\d+) (\S+), и в каждой коробке (\d+) (\S+); всего "
    r"(\d+) (\S+)\.$")

ЕСТЬ_СУТЬ = re.compile(
    r"^there is 1 ([a-z]+) (on|in|at) the ([a-z ]+), and there are "
    r"(\d+) ([a-z]+) \2 the \3\.$")
АРТИКЛЬ = re.compile(
    r"^([a-z]+) took 1 ([a-z]+) and 1 ([a-z]+); \1 took (a|an) \2 "
    r"and (a|an) \3\.$")
СУММА_ЕДИНИЦЫ = re.compile(
    r"^1 ([a-z]+) and (\d+) ([a-z]+) make (\d+) ([a-z]+) in all\.$")
ЖДАЛ = re.compile(
    r"^([a-z]+) waited (a|an) ([a-z]+) and counted 1 ([a-z]+)\.$")
СУММА_ЕДИНИЦЫ_RU = re.compile(
    r"^1 (\S+) и (\d+) (\S+) дают всего (\d+) (\S+)\.$")

РОЛИ_ПРИШЛИ = re.compile(
    r"^(\d+) ([a-z]+) and (\d+) ([a-z]+) came to the ([a-z ]+); "
    r"(\d+) ([a-z]+) came to the \5 in all\.$")
РОЛИ_ВОПРОС = re.compile(
    r"^(\d+) ([a-z]+) and (\d+) ([a-z]+) came to the ([a-z ]+)\. how "
    r"many ([a-z]+) came to the \5\? (\d+) ([a-z]+) came to the \5 "
    r"in all\.$")
РОЛИ_RU_ОБРАЗЕЦ = re.compile(
    r"^(\S+) и (\S+) вместе зовутся (\S+)\.$")
РОЛИ_RU_ВОПРОС = re.compile(
    r"^кто такие (\S+)\? (\S+) и (\S+) вместе зовутся \1\.$")
# КЛАСС СПИСКОМ: «люди: мужчина, женщина, …» / «people: man, woman, …» —
# перечень обязан совпасть с объявленными членами класса (дом.РОЛИ) как
# множество, без повторов.
КЛАСС_СПИСКОМ = re.compile(r"^([a-zа-яё]+): ([a-zа-яё]+(?:, [a-zа-яё]+)+)\.$")
_КЛАСС_EN = {}
_КЛАСС_RU = {}
for _ч1, _ч2, _ц, _р1, _р2, _рц in дом.РОЛИ:
    _КЛАСС_EN.setdefault(дом.множественное(_ц), set()).update((_ч1, _ч2))
    _КЛАСС_RU.setdefault(_рц, set()).update((_р1, _р2))
СЕМЬЯ = re.compile(
    r"^the family has a ([a-z]+), a ([a-z]+) and a ([a-z]+); the "
    r"family has (\d+) people\.$")
СЕМЬЯ_RU = re.compile(
    r"^в семье ([а-яё]+), ([а-яё]+) и ([а-яё]+); в семье (\d+) "
    r"человека\.$")

ЧАСТОТА = re.compile(
    r"^([a-z]+) worked on (\d+) (days?) of (\d+) days; \1 "
    r"([a-z ]+)\.$")
ЧАСТОТА_RU = re.compile(
    r"^(\S+) работал(а?) (\d+) (\S+) из (\d+); \1 (.+)\.$")
СНОВА = re.compile(
    r"^([a-z]+) counted the ([a-z]+) once and counted the \2 again; "
    r"\1 counted the \2 ([a-z ]+) in all\.$")
СНОВА_RU = re.compile(
    r"^(\S+) считал(а?) (\S+) один раз и потом ещё раз; всего \1 "
    r"считал\2 (.+)\.$")

ОКОЛО = re.compile(
    r"^([a-z]+) counted (\d+) ([a-z]+); (\d+) ([a-z]+) are "
    r"(nearly|about) (\d+) ([a-z]+)\.$")
ОКОЛО_RU = re.compile(
    r"^(\S+) насчитал(а?) (\d+) (\S+); это (почти|примерно) (\d+) "
    r"(\S+)\.$")

ПОЧЕМУ = re.compile(
    r"^why does ([a-z]+) have (\d+) ([a-z]+)\? because \1 bought "
    r"(\d+) ([a-z]+) and then (\d+) ([a-z]+) more\.$")
ПОЧЕМУ_RU = re.compile(
    r"^почему у (\S+) (\d+) (\S+)\? потому что (\S+) купил(а?) (\d+) "
    r"(\S+), а потом ещё (\d+) (\S+)\.$")
ПЕРЕЧЕНЬ = re.compile(
    r"^([a-z]+) bought ([a-z]+), ([a-z]+) and ([a-z]+) at the "
    r"([a-z ]+); \1 bought (\d+) things in all\.$")
ПЕРЕЧЕНЬ_RU = re.compile(
    r"^(в|на) (\S+) лежат (\S+), (\S+) и (\S+); \1 \2 лежат (\d+) "
    r"(\S+)\.$")


def _сумма_покупки(а, имя1, б, имя2, всего):
    """Сумма покупки со всеми английскими согласованиями разом."""
    return (int(а) + int(б) == int(всего)
            and _форма_верна(int(а), имя1)
            and _форма_верна(int(б), имя2))


def _сумма_покупки_ru(а, ф1, б, ф2, всего, фп):
    """То же по-русски: и сумма, и три формы при своих числах."""
    а, б, всего = int(а), int(б), int(всего)
    return (а + б == всего and _ру_верна(а, ф1) and _ру_верна(б, ф2)
            and _ру_верна(всего, фп)
            and _ру_ключ(фп) == "предмет")


def _разность(а, б, ф_а, ф_б, разн, ф_разн, знак):
    """Разность двух счётов одного имени: и число, и три формы."""
    а, б, разн = int(а), int(б), int(разн)
    имя = _ед(ф_а)
    if имя is None or _ед(ф_б) != имя or _ед(ф_разн) != имя:
        return False
    return (знак * (а - б) == разн and разн > 0
            and _форма_верна(а, ф_а) and _форма_верна(б, ф_б)
            and _форма_верна(разн, ф_разн))


def _путь(что):
    try:
        return дом.путь_вверх(что)
    except (KeyError, ValueError):
        return None


def _вместилище(что, предлог, где):
    """Прямая связь: объявленное родительство и предлог самого места."""
    if что not in дом.МЕСТА or где not in дом.МЕСТА:
        return None
    if что not in дом.ДЕРЕВО:
        return None
    return дом.ДЕРЕВО[что] == где and дом.предлог(где) == предлог


def _вместилище_ru(им, предлог, местный):
    """Та же связь, названная по-русски: имена переводятся в дом мест."""
    что = _место_по_имени_ru(им)
    где = _место_по_русски(предлог, местный)
    if что is None or где is None or что not in дом.ДЕРЕВО:
        return None
    return дом.ДЕРЕВО[что] == где


def _через(что, п1, где, что2, п2, дед, что3, п3, дед2):
    """Переходность: посылки объявлены, вывод ПРОЙДЕН по дереву."""
    прямо = _вместилище(что, п1, где)
    второе = _вместилище(где, п2, дед)
    if прямо is None or второе is None:
        return None
    цепь = _путь(что)
    if цепь is None:
        return None
    return (прямо and второе and что2 == где and что3 == что
            and дед2 == дед and п3 == дом.предлог(дед)
            and дед in цепь)


def _через_ru(им1, п1, м1, им2, п2, м2, им3, п3, м3):
    первое = _вместилище_ru(им1, п1, м1)
    второе = _вместилище_ru(им2, п2, м2)
    что = _место_по_имени_ru(им1)
    где = _место_по_имени_ru(им2)
    дед = _место_по_русски(п2, м2)
    if первое is None or второе is None or что is None or дед is None:
        return None
    цепь = _путь(что)
    return (первое and второе and где == дом.ДЕРЕВО.get(что)
            and им3 == им1 and п3 == п2 and м3 == м2
            and цепь is not None and дед in цепь)


def _ряд_суток(а, б):
    """Места двух имён в объявленном ряду суток, или None."""
    if а not in _МЕСТО_В_СУТКАХ or б not in _МЕСТО_В_СУТКАХ:
        return None
    return _МЕСТО_В_СУТКАХ[а], _МЕСТО_В_СУТКАХ[б]


def судить(строка):
    """(судимо, истинно) для одной строки мира быта."""
    с = строка.strip()
    if not с:
        return False, False

    # ── СЧЁТ ПРЕДМЕТОВ ────────────────────────────────────────────
    # ЗВЕНО ПОКУПКИ (compose, e9): «а + б = всего» сверяется с числами условия.
    m = ПОКУПКА.match(с) or ПОКУПКА_ВОПРОС.match(с)
    if m:
        _к, а, и1, б, и2, место, всего, з1, з2, з3 = m.groups()
        if место not in дом.МЕСТА:
            return False, False
        return True, (_сумма_покупки(а, и1, б, и2, всего)
                      and (int(з1), int(з2), int(з3)) == (int(а), int(б), int(всего)))
    m = ПОКУПКА_RU.match(с) or ПОКУПКА_RU_ВОПРОС.match(с)
    if m:
        кто, суф, а, ф1, б, ф2, п, местн, всего, фп, з1, з2, з3 = m.groups()
        if _место_по_русски(п, местн) is None:
            return False, False
        return True, (_суффикс_верен(кто, суф)
                      and _сумма_покупки_ru(а, ф1, б, ф2, всего, фп)
                      and (int(з1), int(з2), int(з3)) == (int(а), int(б), int(всего)))

    # ── ВМЕСТИЛИЩЕ ────────────────────────────────────────────────
    m = МЕСТО_ЧЕРЕЗ.match(с)
    if m:
        итог = _через(*m.groups())
        return (False, False) if итог is None else (True, итог)
    m = МЕСТО_ВОПРОС.match(с)
    if m:
        (что, п1, где, что2, п2, дед, что3, что4, п3, дед2) = m.groups()
        if что3 != что or что4 != что:
            return True, False
        итог = _через(что, п1, где, что2, п2, дед, что4, п3, дед2)
        return (False, False) if итог is None else (True, итог)
    m = МЕСТО_ОТКАЗ.match(с)
    if m:
        что, п, чужое, чужое2, что2, корень = m.groups()
        if что not in дом.МЕСТА or чужое not in дом.МЕСТА:
            return False, False
        цепь = _путь(что)
        if not цепь:
            return False, False
        return True, (чужое2 == чужое and что2 == что
                      and чужое not in цепь and чужое != что
                      and корень == цепь[-1]
                      and п == дом.предлог(чужое))
    m = МЕСТО.match(с)
    if m:
        итог = _вместилище(*m.groups())
        return (False, False) if итог is None else (True, итог)
    m = МЕСТО_RU_ЧЕРЕЗ.match(с)
    if m:
        итог = _через_ru(*m.groups())
        return (False, False) if итог is None else (True, итог)
    m = МЕСТО_RU_ВОПРОС.match(с)
    if m:
        (им1, п1, м1, им2, п2, м2, им3, им4, п3, м3) = m.groups()
        if им3 != им1 or им4 != им1:
            return True, False
        итог = _через_ru(им1, п1, м1, им2, п2, м2, им4, п3, м3)
        return (False, False) if итог is None else (True, итог)
    m = МЕСТО_RU_ОТКАЗ.match(с)
    if m:
        им, п, местн, им_ч, род_что, род_корень = m.groups()
        что = _место_по_имени_ru(им)
        чужое = _место_по_русски(п, местн)
        if что is None or чужое is None:
            return False, False
        цепь = _путь(что)
        if not цепь:
            return False, False
        return True, (им_ч == дом.имя_ru(чужое) and чужое not in цепь
                      and род_что == дом.род_ru(что)
                      and род_корень == дом.род_ru(цепь[-1]))
    m = МЕСТО_RU.match(с)
    if m:
        итог = _вместилище_ru(*m.groups())
        return (False, False) if итог is None else (True, итог)

    # ── ПОРЯДОК ВРЕМЕНИ ───────────────────────────────────────────
    m = ВРЕМЯ_ДО.match(с)
    if m:
        пара = _ряд_суток(*m.groups())
        return (False, False) if пара is None else (True, пара[0] < пара[1])
    m = ВРЕМЯ_ПОСЛЕ.match(с)
    if m:
        пара = _ряд_суток(*m.groups())
        return (False, False) if пара is None else (True, пара[0] > пара[1])
    m = ВРЕМЯ_СЛЕД.match(с)
    if m:
        пара = _ряд_суток(*m.groups())
        return ((False, False) if пара is None
                else (True, пара[0] == пара[1] + 1))
    m = ВРЕМЯ_ВОПРОС.match(с)
    if m:
        б, а = m.groups()
        пара = _ряд_суток(а, б)
        return ((False, False) if пара is None
                else (True, пара[0] + 1 == пара[1]))
    m = ВРЕМЯ_КРАЙ.match(с)
    if m:
        а, б = m.groups()
        if а not in _МЕСТО_В_СУТКАХ or б not in _МЕСТО_В_СУТКАХ:
            return False, False
        return True, (а == дом.СУТКИ[0] and б == дом.СУТКИ[-1])
    m = ВРЕМЯ_РАНО.match(с)
    if m:
        пара = _ряд_суток(*m.groups())
        if пара is None:
            return False, False
        рано, поздно = пара
        половина = len(дом.СУТКИ) / 2
        return True, (рано < половина <= поздно)
    m = ВРЕМЯ_РАБОТА.match(с)
    if m:
        _к, п1, а, п2, б = m.groups()
        пара = _ряд_суток(а, б)
        if пара is None:
            return False, False
        return True, (пара[0] < пара[1] and п1 == п2
                      and п1 in дом.ВРЕМЕННЫЕ_ПРЕДЛОГИ)
    m = ВРЕМЯ_ПОКА.match(с)
    if m:
        _к1, а, _к2, б = m.groups()
        пара = _ряд_суток(а, б)
        return (False, False) if пара is None else (True, пара[0] == пара[1])
    m = ВРЕМЯ_СЕЙЧАС.match(с)
    if m:
        if not {"now", "later"} <= set(дом.СРОКИ):
            return False, False
        return True, (дом.СРОКИ.index("now")
                      < дом.СРОКИ.index("later"))
    m = ВРЕМЯ_ДОМ.match(с)
    if m:
        _к, а, место, б, место2 = m.groups()
        пара = _ряд_суток(а, б)
        if пара is None or место not in дом.МЕСТА:
            return False, False
        return True, (пара[0] < пара[1] and место == место2)
    m = НЕДЕЛЯ.match(с)
    if m:
        широкое, много, узкое, мало, разн = m.groups()
        объявлено = dict(дом.ДЛИТЕЛЬНОСТИ)
        if широкое not in объявлено or узкое not in объявлено:
            return False, False
        return True, (объявлено[широкое] == int(много)
                      and объявлено[узкое] == int(мало)
                      and int(много) - int(мало) == int(разн))
    m = ДЕНЬ_ДО.match(с)
    if m:
        а, б = m.groups()
        if а not in _МЕСТО_В_ДНЯХ or б not in _МЕСТО_В_ДНЯХ:
            return False, False
        return True, _МЕСТО_В_ДНЯХ[а] < _МЕСТО_В_ДНЯХ[б]
    m = ДЕНЬ_ПОСЛЕ.match(с)
    if m:
        а, б = m.groups()
        if а not in _МЕСТО_В_ДНЯХ or б not in _МЕСТО_В_ДНЯХ:
            return False, False
        return True, _МЕСТО_В_ДНЯХ[а] > _МЕСТО_В_ДНЯХ[б]
    m = ДЕНЬ_RU.match(с)
    if m:
        а, б = m.groups()
        if а not in _ДНИ_ПО_RU or б not in _ДНИ_ПО_RU:
            return False, False
        return True, (_МЕСТО_В_ДНЯХ[_ДНИ_ПО_RU[а]]
                      < _МЕСТО_В_ДНЯХ[_ДНИ_ПО_RU[б]])
    m = ВРЕМЯ_RU_ДО.match(с)
    if m:
        им, род = m.groups()
        if им not in _СУТКИ_ПО_ИМ or род not in _СУТКИ_ПО_РОД:
            return False, False
        return True, (_МЕСТО_В_СУТКАХ[_СУТКИ_ПО_ИМ[им]]
                      < _МЕСТО_В_СУТКАХ[_СУТКИ_ПО_РОД[род]])
    m = ВРЕМЯ_RU_ПОСЛЕ.match(с)
    if m:
        им, род = m.groups()
        if им not in _СУТКИ_ПО_ИМ or род not in _СУТКИ_ПО_РОД:
            return False, False
        return True, (_МЕСТО_В_СУТКАХ[_СУТКИ_ПО_ИМ[им]]
                      > _МЕСТО_В_СУТКАХ[_СУТКИ_ПО_РОД[род]])
    m = ВРЕМЯ_RU_ВОПРОС.match(с)
    if m:
        род, им = m.groups()
        if им not in _СУТКИ_ПО_ИМ or род not in _СУТКИ_ПО_РОД:
            return False, False
        return True, (_МЕСТО_В_СУТКАХ[_СУТКИ_ПО_ИМ[им]] + 1
                      == _МЕСТО_В_СУТКАХ[_СУТКИ_ПО_РОД[род]])
    m = ВРЕМЯ_RU_РАБОТА.match(с)
    if m:
        кто, суф, твор1, твор2 = m.groups()
        if твор1 not in _СУТКИ_ПО_ТВОР or твор2 not in _СУТКИ_ПО_ТВОР:
            return False, False
        return True, (_суффикс_верен(кто, суф)
                      and (_МЕСТО_В_СУТКАХ[_СУТКИ_ПО_ТВОР[твор1]]
                           < _МЕСТО_В_СУТКАХ[_СУТКИ_ПО_ТВОР[твор2]]))
    m = ВРЕМЯ_RU_ВМЕСТЕ.match(с)
    if m:
        кто1, суф1, твор1, кто2, суф2, твор2 = m.groups()
        if твор1 not in _СУТКИ_ПО_ТВОР or твор2 not in _СУТКИ_ПО_ТВОР:
            return False, False
        return True, (твор1 == твор2 and кто1 != кто2
                      and _суффикс_верен(кто1, суф1)
                      and _суффикс_верен(кто2, суф2))
    m = ВРЕМЯ_RU_ДОМ.match(с)
    if m:
        кто, ушёл, твор1, пришёл, п, местн, твор2 = m.groups()
        если = _ИМЕНА_RU.get(кто)
        место = _место_по_русски(п, местн)
        if (если is None or место is None
                or твор1 not in _СУТКИ_ПО_ТВОР
                or твор2 not in _СУТКИ_ПО_ТВОР):
            return False, False
        женский = если[1] == "а"
        return True, (ушёл == дом.ДВИЖЕНИЕ_RU["leave"][женский]
                      and пришёл == дом.ДВИЖЕНИЕ_RU["arrive"][женский]
                      and (_МЕСТО_В_СУТКАХ[_СУТКИ_ПО_ТВОР[твор1]]
                           < _МЕСТО_В_СУТКАХ[_СУТКИ_ПО_ТВОР[твор2]]))
    m = НЕДЕЛЯ_RU.match(с)
    if m:
        много, ф1, мало, ф2, разн, ф3 = m.groups()
        много, мало, разн = int(много), int(мало), int(разн)
        объявлено = dict(дом.ДЛИТЕЛЬНОСТИ)
        return True, (объявлено.get("week") == много
                      and объявлено.get("weekend") == мало
                      and много - мало == разн
                      and _ру_пара(много, ф1, "день")
                      and _ру_пара(мало, ф2, "день")
                      and _ру_пара(разн, ф3, "день"))

    # ── ФОРМЫ ДЕЙСТВИЯ ────────────────────────────────────────────
    m = ГЛАГОЛ_ДВОЕ.match(с)
    if m:
        _к1, _к2, база, много, прош = m.groups()
        if (база, много) not in _ГЛАГОЛ_МН:
            return False, False
        return True, прош == дом.прошедшее(база)
    m = ГЛАГОЛ_ВОПРОС.match(с)
    if m:
        _к, третье, один, база, прош = m.groups()
        if (третье, один) not in _ГЛАГОЛ_ЕД:
            return False, False
        своя = _ГЛАГОЛ_ЕД[(третье, один)]
        return True, (база == своя and прош == дом.прошедшее(своя)
                      and третье == дом.третье_лицо(своя))
    m = ГЛАГОЛ_ОДИН.match(с)
    if m:
        _к, третье, один, прош = m.groups()
        if (третье, один) not in _ГЛАГОЛ_ЕД:
            return False, False
        своя = _ГЛАГОЛ_ЕД[(третье, один)]
        return True, (прош == дом.прошедшее(своя)
                      and третье == дом.третье_лицо(своя))
    m = ГЛАГОЛ_ПРОШ.match(с)
    if m:
        база, прош = m.groups()
        if база not in _ОСНОВЫ:
            return False, False
        return True, прош == дом.прошедшее(база)
    m = ГЛАГОЛ_RU.match(с)
    if m:
        кто, наст, доп, прош = m.groups()
        если = _ИМЕНА_RU.get(кто)
        свой = _ГЛАГОЛ_RU.get((наст, доп))
        if если is None or свой is None:
            return False, False
        return True, прош == свой[1] + если[1]
    m = ГЛАГОЛ_RU_ИМЯ.match(с)
    if m:
        инф, прош = m.groups()
        if инф not in _ГЛАГОЛ_RU_ИНФ:
            return False, False
        return True, прош == _ГЛАГОЛ_RU_ИНФ[инф]

    # ── СРАВНЕНИЕ ─────────────────────────────────────────────────
    m = БОЛЬШЕ.match(с)
    if m:
        _к1, а, ф1, _к2, б, ф2, разн, ф3 = m.groups()
        if _ед(ф1) is None:
            return False, False
        return True, _разность(а, б, ф1, ф2, разн, ф3, 1)
    m = МЕНЬШЕ.match(с)
    if m:
        _к1, а, ф1, _к2, б, ф2, разн, ф3 = m.groups()
        if _ед(ф1) is None:
            return False, False
        return True, _разность(а, б, ф1, ф2, разн, ф3, -1)
    m = БОЛЬШЕ_ВОПРОС.match(с)
    if m:
        _к1, а, ф1, _к2, б, ф2, ф_в, разн, ф3 = m.groups()
        if _ед(ф1) is None:
            return False, False
        return True, (ф_в == ф1 and _разность(а, б, ф1, ф2, разн, ф3, 1))
    m = СТОЛЬКО_ЖЕ.match(с)
    if m:
        _к1, а, ф1, _к2, б, ф2, ф3 = m.groups()
        if _ед(ф1) is None:
            return False, False
        return True, (int(а) == int(б) and ф1 == ф2 == ф3
                      and _форма_верна(int(а), ф1))
    m = КРАЙНИЕ.match(с)
    if m:
        _к1, а, ф1, _к2, б, ф2, _к3, ф3, ф4, ф5 = m.groups()
        а, б = int(а), int(б)
        if _ед(ф1) is None:
            return False, False
        return True, (а > б > 1 and ф1 == ф2 and _ед(ф3) == _ед(ф1)
                      and ф4 == ф5 == ф1
                      and _форма_верна(а, ф1) and _форма_верна(б, ф2)
                      and _форма_верна(1, ф3))
    m = ВДВОЕ.match(с)
    if m:
        _к1, а, ф1, _к2, б, ф2, ф3 = m.groups()
        if _ед(ф1) is None:
            return False, False
        return True, (int(а) == 2 * int(б) and ф1 == ф2 == ф3
                      and _форма_верна(int(а), ф1))
    m = КРАТНО.match(с)
    if m:
        _к1, а, ф1, _к2, б, ф2, слово, ф3 = m.groups()
        кратность = {"double": 2, "triple": 3}[слово]
        if _ед(ф1) is None:
            return False, False
        return True, (int(а) == кратность * int(б) and ф1 == ф2 == ф3
                      and _форма_верна(int(а), ф1))
    m = ПОЛОВИНА.match(с)
    if m:
        _к1, а, ф1, _к2, б, ф2, ф3 = m.groups()
        if _ед(ф1) is None:
            return False, False
        return True, (int(а) == 2 * int(б) and ф1 == ф2 == ф3
                      and _форма_верна(int(б), ф2))
    m = РАВНЫ.match(с)
    if m:
        _к1, а, ф1, _к2, б, ф2, слово = m.groups()
        if _ед(ф1) is None:
            return False, False
        равны = int(а) == int(б)
        return True, (ф1 == ф2 and равны == (слово == "equal")
                      and _форма_верна(int(а), ф1))
    m = ВМЕСТЕ_ВРОЗЬ.match(с)
    if m:
        (_к1, а, ф1, _к2, б, ф2, всего, ф3, а2, ф4, б2, ф5) = m.groups()
        а, б, всего = int(а), int(б), int(всего)
        if _ед(ф1) is None:
            return False, False
        return True, (а + б == всего and int(а2) == а and int(б2) == б
                      and ф1 == ф2 and _ед(ф3) == _ед(ф1)
                      and _форма_верна(всего, ф3)
                      and _форма_верна(а, ф4) and _форма_верна(б, ф5))
    m = ИТОГО.match(с)
    if m:
        _к1, а, ф1, _к2, б, ф2, всего, ф3 = m.groups()
        if _ед(ф1) is None:
            return False, False
        return True, (int(а) + int(б) == int(всего) and ф1 == ф2
                      and _форма_верна(int(всего), ф3)
                      and _ед(ф3) == _ед(ф1))
    m = ТОЛЬКО.match(с)
    if m:
        (_к1, а, ф1, _к2, б, ф2, б2, ф3, а2, ф4) = m.groups()
        а, б = int(а), int(б)
        if _ед(ф1) is None:
            return False, False
        return True, (б < а and int(б2) == б and int(а2) == а
                      and ф1 == ф2 == ф3 == ф4
                      and _форма_верна(а, ф1))
    m = ДРУГ_ДРУГУ.match(с)
    if m:
        (к1, к2, а, ф1, а2, ф2, а3, ф3) = m.groups()
        if _ед(ф1) is None:
            return False, False
        return True, (к1 != к2 and int(а) == int(а2) == int(а3)
                      and ф1 == ф2 == ф3
                      and _форма_верна(int(а), ф1))
    m = МЕНЬШЕ_МАССЫ.match(с)
    if m:
        _к1, а, мера1, масса, _к2, б, мера2, = m.groups()
        объявлено = {м: мера for м, мера, _ру, _ключ in дом.НЕСЧЁТНОЕ}
        if масса not in объявлено:
            return False, False
        мера = объявлено[масса]
        return True, (int(б) < int(а)
                      and _форма_верна(int(а), мера1)
                      and _форма_верна(int(б), мера2)
                      and _ед(мера1) == мера and _ед(мера2) == мера)
    m = БОЛЬШЕ_RU.match(с)
    if m:
        _р1, а, ф1, _р2, б, ф2, разн, ф3 = m.groups()
        ключ = _ру_ключ(ф1)
        а, б, разн = int(а), int(б), int(разн)
        if ключ is None:
            return False, False
        return True, (а - б == разн and разн > 0
                      and _ру_пара(а, ф1, ключ)
                      and _ру_пара(б, ф2, ключ)
                      and _ру_пара(разн, ф3, ключ))
    m = МЕНЬШЕ_RU.match(с)
    if m:
        _р1, а, ф1, _р2, б, ф2, разн, ф3 = m.groups()
        ключ = _ру_ключ(ф1)
        а, б, разн = int(а), int(б), int(разн)
        if ключ is None:
            return False, False
        return True, (б - а == разн and разн > 0
                      and _ру_пара(а, ф1, ключ)
                      and _ру_пара(б, ф2, ключ)
                      and _ру_пара(разн, ф3, ключ))
    m = ПОРОВНУ_RU.match(с)
    if m:
        _р1, а, ф1, _р2, б, ф2, ф5 = m.groups()
        ключ = _ру_ключ(ф1)
        if ключ is None:
            return False, False
        return True, (int(а) == int(б) and ф1 == ф2
                      and _ру_пара(int(а), ф1, ключ)
                      and _ру_пара(5, ф5, ключ))
    m = ВМЕСТЕ_RU.match(с)
    if m:
        _р1, а, ф1, _р2, б, ф2, всего, ф3 = m.groups()
        ключ = _ру_ключ(ф1)
        а, б, всего = int(а), int(б), int(всего)
        if ключ is None:
            return False, False
        return True, (а + б == всего and _ру_пара(а, ф1, ключ)
                      and _ру_пара(б, ф2, ключ)
                      and _ру_пара(всего, ф3, ключ))
    m = БОЛЬШЕ_ВОПРОС_RU.match(с)
    if m:
        _р1, а, ф1, _р2, б, ф2, ф5, разн, ф3 = m.groups()
        ключ = _ру_ключ(ф1)
        а, б, разн = int(а), int(б), int(разн)
        if ключ is None:
            return False, False
        return True, (а - б == разн and разн > 0
                      and _ру_пара(5, ф5, ключ)
                      and _ру_пара(а, ф1, ключ)
                      and _ру_пара(б, ф2, ключ)
                      and _ру_пара(разн, ф3, ключ))
    m = ВДВОЕ_RU.match(с)
    if m:
        _р1, а, ф1, _р2, б, ф2 = m.groups()
        ключ = _ру_ключ(ф1)
        if ключ is None:
            return False, False
        return True, (int(а) == 2 * int(б)
                      and _ру_пара(int(а), ф1, ключ)
                      and _ру_пара(int(б), ф2, ключ))
    m = МАССА_RU.match(с)
    if m:
        (кто1, суф1, а, ф1, масса, кто2, суф2, б, ф2,
         род_меньше, род_больше) = m.groups()
        объявлено = {ру: ключ for _м, _мера, ру, ключ in дом.НЕСЧЁТНОЕ}
        if масса not in объявлено:
            return False, False
        ключ = объявлено[масса]
        свой1 = _РОД_ПО_ИМЕНИ.get(род_больше)
        свой2 = _РОД_ПО_ИМЕНИ.get(род_меньше)
        if свой1 is None or свой2 is None:
            return False, False
        return True, (int(б) < int(а)
                      and _ру_пара(int(а), ф1, ключ)
                      and _ру_пара(int(б), ф2, ключ)
                      and свой1[0] == кто1 and свой2[0] == кто2
                      and _суффикс_верен(кто1, суф1)
                      and _суффикс_верен(кто2, суф2))

    # ── ТРАТА И ОСТАТОК ───────────────────────────────────────────
    for образец in (ОСТАТОК, ОСТАТОК_ПРОЧЕЕ, ОСТАТОК_СВЕРХ,
                    ОСТАТОК_ХРАНИТ):
        m = образец.match(с)
        if m:
            _к, было, ф1, ушло, ф2, цел, ф3 = m.groups()
            было, ушло, цел = int(было), int(ушло), int(цел)
            if _ед(ф1) is None:
                return False, False
            return True, (было - ушло == цел and ушло > 0
                          and _ед(ф2) == _ед(ф1) and _ед(ф3) == _ед(ф1)
                          and _форма_верна(было, ф1)
                          and _форма_верна(ушло, ф2)
                          and _форма_верна(цел, ф3))
    m = ОСТАТОК_ВОПРОС.match(с)
    if m:
        _к, было, ф1, ушло, ф2, ф_в, цел, ф3 = m.groups()
        было, ушло, цел = int(было), int(ушло), int(цел)
        if _ед(ф1) is None:
            return False, False
        return True, (было - ушло == цел and ушло > 0 and ф_в == ф1
                      and _ед(ф2) == _ед(ф1) and _ед(ф3) == _ед(ф1)
                      and _форма_верна(было, ф1)
                      and _форма_верна(ушло, ф2)
                      and _форма_верна(цел, ф3))
    m = ОСТАТОК_RU.match(с)
    if m:
        _род, было, ф1, кто, суф, ушло, ф2, цел, ф3 = m.groups()
        было, ушло, цел = int(было), int(ушло), int(цел)
        ключ = _ру_ключ(ф1)
        if ключ is None:
            return False, False
        return True, (было - ушло == цел and ушло > 0
                      and _суффикс_верен(кто, суф)
                      and _ру_пара(было, ф1, ключ)
                      and _ру_пара(ушло, ф2, ключ)
                      and _ру_пара(цел, ф3, ключ))
    m = ОСТАТОК_RU_ВОПРОС.match(с)
    if m:
        _род, было, ф1, кто, суф, ушло, ф2, ф5, цел, ф3 = m.groups()
        было, ушло, цел = int(было), int(ушло), int(цел)
        ключ = _ру_ключ(ф1)
        if ключ is None:
            return False, False
        return True, (было - ушло == цел and ушло > 0
                      and _суффикс_верен(кто, суф)
                      and _ру_пара(5, ф5, ключ)
                      and _ру_пара(было, ф1, ключ)
                      and _ру_пара(ушло, ф2, ключ)
                      and _ру_пара(цел, ф3, ключ))

    # ── ВМЕСТИМОСТЬ ───────────────────────────────────────────────
    for образец in (ВМЕЩАЕТ, ВМЕЩАЕТ_НЫНЕ):
        m = образец.match(с)
        if m:
            сосуд, всё, ф1, _к, внутри, ф2, нужно, ф3 = m.groups()
            всё, внутри, нужно = int(всё), int(внутри), int(нужно)
            if сосуд not in дом.МЕСТА or _ед(ф1) is None:
                return False, False
            return True, (всё - внутри == нужно and внутри > 0
                          and _ед(ф2) == _ед(ф1) and _ед(ф3) == _ед(ф1)
                          and _форма_верна(всё, ф1)
                          and _форма_верна(внутри, ф2)
                          and _форма_верна(нужно, ф3))
    m = ВМЕЩАЕТ_ВОПРОС.match(с)
    if m:
        сосуд, всё, ф1, _к, внутри, ф2, ф_в, нужно, ф3 = m.groups()
        всё, внутри, нужно = int(всё), int(внутри), int(нужно)
        if сосуд not in дом.МЕСТА or _ед(ф1) is None:
            return False, False
        return True, (всё - внутри == нужно and внутри > 0
                      and ф_в == ф1 and _ед(ф3) == _ед(ф1)
                      and _форма_верна(всё, ф1)
                      and _форма_верна(внутри, ф2)
                      and _форма_верна(нужно, ф3))
    m = ОПУСТОШЕНО.match(с)
    if m:
        _к, глагол, сосуд, внутри, ф1, ф2, когда = m.groups()
        if сосуд not in дом.МЕСТА or _ед(ф1) is None:
            return False, False
        верное = {"emptied": "now", "empties": "then"}[глагол]
        return True, (когда == верное and int(внутри) > 0
                      and _форма_верна(int(внутри), ф1)
                      and _форма_верна(0, ф2)
                      and _ед(ф2) == _ед(ф1))
    m = ВМЕЩАЕТ_RU.match(с)
    if m:
        сосуд, всё, ф1, кто, суф, внутри, ф2, нужно, ф3 = m.groups()
        всё, внутри, нужно = int(всё), int(внутри), int(нужно)
        ключ = _ру_ключ(ф1)
        if ключ is None or _место_по_имени_ru(сосуд) is None:
            return False, False
        return True, (всё - внутри == нужно and внутри > 0
                      and _суффикс_верен(кто, суф)
                      and _ру_пара(всё, ф1, ключ)
                      and _ру_пара(внутри, ф2, ключ)
                      and _ру_пара(нужно, ф3, ключ))
    m = ОПУСТОШЕНО_RU.match(с)
    if m:
        кто, суф, сосуд, внутри, ф1, ф2 = m.groups()
        ключ = _ру_ключ(ф1)
        if ключ is None or _место_по_имени_ru(сосуд) is None:
            return False, False
        return True, (int(внутри) > 0 and _суффикс_верен(кто, суф)
                      and _ру_пара(int(внутри), ф1, ключ)
                      and _ру_пара(0, ф2, ключ))

    # ── ДЕЛЁЖ ─────────────────────────────────────────────────────
    for образец in (ДЕЛЁЖ, ДЕЛЁЖ_НЫНЕ):
        m = образец.match(с)
        if m:
            _к, всего, ф1, друзей, каждому, ф2 = m.groups()
            всего, друзей, каждому = (int(всего), int(друзей),
                                      int(каждому))
            if _ед(ф1) is None:
                return False, False
            return True, (друзей > 0 and всего == друзей * каждому
                          and _ед(ф2) == _ед(ф1)
                          and _форма_верна(всего, ф1)
                          and _форма_верна(каждому, ф2))
    m = ДЕЛЁЖ_ВОПРОС.match(с)
    if m:
        _к, всего, ф1, друзей, ф_в, каждому, ф2 = m.groups()
        всего, друзей, каждому = int(всего), int(друзей), int(каждому)
        if _ед(ф1) is None:
            return False, False
        return True, (друзей > 0 and всего == друзей * каждому
                      and ф_в == ф1 and _ед(ф2) == _ед(ф1)
                      and _форма_верна(всего, ф1)
                      and _форма_верна(каждому, ф2))
    m = ДЕЛЁЖ_RU.match(с)
    if m:
        кто, суф, всего, ф1, друзей, каждому, ф2 = m.groups()
        всего, друзей, каждому = int(всего), int(друзей), int(каждому)
        ключ = _ру_ключ(ф1)
        if ключ is None:
            return False, False
        return True, (друзей > 0 and всего == друзей * каждому
                      and _суффикс_верен(кто, суф)
                      and _ру_пара(всего, ф1, ключ)
                      and _ру_пара(каждому, ф2, ключ))

    # ── ДЕНЬГИ БЫТА ───────────────────────────────────────────────
    m = ДЕНЬГИ.match(с)
    if m:
        _к, зар, плата, пл, билет, ф1, сбер, осталось = m.groups()
        времена = {("earned", "paid", "saved"),
                   ("earns", "pays", "saves")}
        return True, ((зар, пл, сбер) in времена
                      and int(плата) - int(билет) == int(осталось)
                      and int(билет) > 0
                      and _форма_верна(int(билет), ф1))
    m = ДЕНЬГИ_ВОПРОС.match(с)
    if m:
        _к, плата, билет, ф1, осталось = m.groups()
        return True, (int(плата) - int(билет) == int(осталось)
                      and int(билет) > 0
                      and _форма_верна(int(билет), ф1))
    m = ДЕНЬГИ_RU.match(с)
    if m:
        кто, суф, плата, ф1, билет, ф2, осталось, ф3 = m.groups()
        плата, билет, осталось = int(плата), int(билет), int(осталось)
        return True, (плата - билет == осталось and билет > 0
                      and _суффикс_верен(кто, суф)
                      and _ру_пара(плата, ф1, "рубль")
                      and _ру_пара(билет, ф2, "рубль")
                      and _ру_пара(осталось, ф3, "рубль"))

    # ── КВАНТОРЫ ──────────────────────────────────────────────────
    m = КВАНТОР.match(с)
    if m:
        всех, сколько, ф1, связка, слово = m.groups()
        всех, сколько = int(всех), int(сколько)
        return True, (сколько <= всех
                      and _форма_верна(сколько, ф1)
                      and связка == дом.иметь(сколько)
                      and слово == дом.квантор(сколько, всех))
    m = КВАНТОР_ЛИЦО.match(с)
    if m:
        всех, сколько, ф1, связка, слово = m.groups()
        всех, сколько = int(всех), int(сколько)
        return True, (сколько <= всех
                      and _форма_верна(сколько, ф1)
                      and связка == дом.иметь(сколько)
                      and слово == дом.квантор_лица(сколько, всех))
    m = КАЖДЫЙ.match(с)
    if m:
        всех, _слово, по, ф1, итог = m.groups()
        всех, по, итог = int(всех), int(по), int(итог)
        return True, (всех * по == итог and _форма_верна(по, ф1)
                      and _ед(ф1) == "book")
    m = КАЖДЫЙ_ВОПРОС.match(с)
    if m:
        всех, по, ф1, итог = m.groups()
        всех, по, итог = int(всех), int(по), int(итог)
        return True, (всех * по == итог and _форма_верна(по, ф1)
                      and _ед(ф1) == "book")
    m = ИНОЙ.match(с)
    if m:
        _к, мн, ед1, ед2 = m.groups()
        if _ед(мн) is None:
            return False, False
        return True, (ед1 == ед2 == _ед(мн)
                      and _форма_верна(2, мн))
    m = ЕЩЁ_ОДИН.match(с)
    if m:
        _к, ед1, ед2, мн = m.groups()
        if _ед(мн) is None:
            return False, False
        return True, (ед1 == ед2 == _ед(мн) and _форма_верна(2, мн))
    m = КВАНТОР_RU.match(с)
    if m:
        _род, всех, ф1, сколько, ф2, фраза = m.groups()
        всех, сколько = int(всех), int(сколько)
        return True, (сколько <= всех
                      and _ру_пара(всех, ф1, "книга")
                      and _ру_пара(сколько, ф2, "книга")
                      and фраза == дом.квантор_ru(сколько, всех))
    m = КАЖДЫЙ_RU.match(с)
    if m:
        _род, коробок, ф1, по, ф2, итог, ф3 = m.groups()
        коробок, по, итог = int(коробок), int(по), int(итог)
        ключ = _ру_ключ(ф2)
        if ключ is None:
            return False, False
        return True, (коробок * по == итог
                      and _ру_пара(коробок, ф1, "коробка")
                      and _ру_пара(по, ф2, ключ)
                      and _ру_пара(итог, ф3, ключ))

    # ── ЧИСЛО И АРТИКЛЬ ───────────────────────────────────────────
    m = ЕСТЬ_СУТЬ.match(с)
    if m:
        ед, п, место, сколько, мн = m.groups()
        if _ед(ед) != ед or место not in дом.МЕСТА:
            return False, False
        return True, (int(сколько) > 1 and _форма_верна(1, ед)
                      and _форма_верна(int(сколько), мн)
                      and _ед(мн) == ед
                      and п == дом.предлог(место))
    m = АРТИКЛЬ.match(с)
    if m:
        _к, ед1, ед2, а1, а2 = m.groups()
        if _ед(ед1) != ед1 or _ед(ед2) != ед2:
            return False, False
        return True, (а1 == дом.артикль(ед1) and а2 == дом.артикль(ед2))
    m = ЖДАЛ.match(с)
    if m:
        _к, арт, слово, слово2 = m.groups()
        if _ед(слово) != слово:
            return False, False
        return True, (слово == слово2 and арт == дом.артикль(слово))
    m = СУММА_ЕДИНИЦЫ.match(с)
    if m:
        ед, сколько, мн1, итог, мн2 = m.groups()
        if _ед(ед) != ед:
            return False, False
        return True, (1 + int(сколько) == int(итог) and мн1 == мн2
                      and _форма_верна(int(сколько), мн1)
                      and _форма_верна(int(итог), мн2)
                      and _ед(мн1) == ед)
    m = СУММА_ЕДИНИЦЫ_RU.match(с)
    if m:
        ф1, сколько, ф2, итог, ф3 = m.groups()
        ключ = _ру_ключ(ф1)
        if ключ is None:
            return False, False
        return True, (1 + int(сколько) == int(итог)
                      and _ру_пара(1, ф1, ключ)
                      and _ру_пара(int(сколько), ф2, ключ)
                      and _ру_пара(int(итог), ф3, ключ))

    # ── ЛЮДИ ──────────────────────────────────────────────────────
    m = СЕМЬЯ.match(с)
    if m:
        члены, сколько = m.groups()[:3], int(m.group(4))
        объявлено = {en for en, _ru in дом.СЕМЬЯ}
        if not set(члены) <= объявлено:
            return False, False
        return True, len(set(члены)) == сколько
    m = СЕМЬЯ_RU.match(с)
    if m:
        члены, сколько = m.groups()[:3], int(m.group(4))
        объявлено = {ru for _en, ru in дом.СЕМЬЯ}
        if not set(члены) <= объявлено:
            return False, False
        return True, len(set(члены)) == сколько
    m = РОЛИ_ПРИШЛИ.match(с)
    if m:
        а, ф1, б, ф2, место, всего, ф3 = m.groups()
        ч1, ч2, целое = _ед(ф1), _ед(ф2), _ед(ф3)
        if None in (ч1, ч2, целое) or место not in дом.МЕСТА:
            return False, False
        return True, (_РОЛИ_EN.get((ч1, ч2)) == целое
                      and int(а) + int(б) == int(всего)
                      and _форма_верна(int(а), ф1)
                      and _форма_верна(int(б), ф2)
                      and _форма_верна(int(всего), ф3))
    m = РОЛИ_ВОПРОС.match(с)
    if m:
        а, ф1, б, ф2, место, ф_в, всего, ф3 = m.groups()
        ч1, ч2, целое = _ед(ф1), _ед(ф2), _ед(ф3)
        if None in (ч1, ч2, целое) or место not in дом.МЕСТА:
            return False, False
        return True, (_РОЛИ_EN.get((ч1, ч2)) == целое and ф_в == ф3
                      and int(а) + int(б) == int(всего)
                      and _форма_верна(int(а), ф1)
                      and _форма_верна(int(б), ф2)
                      and _форма_верна(int(всего), ф3))
    m = РОЛИ_RU_ВОПРОС.match(с)
    if m:
        целое, ру1, ру2 = m.groups()
        if (ру1, ру2) not in _РОЛИ_RU:
            return False, False
        return True, _РОЛИ_RU[(ру1, ру2)] == целое
    m = КЛАСС_СПИСКОМ.match(с)
    if m:
        имя, члены = m.group(1), m.group(2).split(", ")
        объявлено = _КЛАСС_EN.get(имя) or _КЛАСС_RU.get(имя)
        if объявлено is None:
            return False, False
        return True, len(члены) == len(set(члены)) and set(члены) == объявлено
    m = РОЛИ_RU_ОБРАЗЕЦ.match(с)
    if m:
        ру1, ру2, целое = m.groups()
        if (ру1, ру2) not in _РОЛИ_RU:
            return False, False
        return True, _РОЛИ_RU[(ру1, ру2)] == целое

    # ── ЧАСТОТА ───────────────────────────────────────────────────
    m = ЧАСТОТА.match(с)
    if m:
        _к, сколько, ф1, всех, слово = m.groups()
        сколько, всех = int(сколько), int(всех)
        return True, (сколько <= всех and _форма_верна(сколько, ф1)
                      and _ед(ф1) == "day"
                      and слово == дом.частота(сколько, всех))
    m = ЧАСТОТА_RU.match(с)
    if m:
        кто, суф, сколько, ф1, всех, слово = m.groups()
        сколько, всех = int(сколько), int(всех)
        if not _суффикс_верен(кто, суф):
            return True, False
        return True, (сколько <= всех
                      and _ру_пара(сколько, ф1, "день")
                      and слово == дом.частота_ru(сколько, всех, суф))
    m = СНОВА.match(с)
    if m:
        _к, мн, слово = m.groups()
        if _ед(мн) is None or слово not in дом.КРАТНОСТИ:
            return False, False
        # ДВА РАЗА ЕСТЬ ОДИН ДА ЕЩЁ ОДИН, И СУД СКЛАДЫВАЕТ ИХ САМ.
        return True, (дом.КРАТНОСТИ[слово]
                      == 2 * дом.КРАТНОСТИ["once"])
    m = СНОВА_RU.match(с)
    if m:
        кто, суф, ф5, слово = m.groups()
        if _ру_ключ(ф5) is None:
            return False, False
        сколько = {ч: с2 for с2, ч in дом.КРАТНОСТИ_RU.items()}
        return True, (_суффикс_верен(кто, суф) and _ру_верна(5, ф5)
                      and сколько.get(слово)
                      == 2 * дом.КРАТНОСТИ["once"])

    # ── ОКОЛО ─────────────────────────────────────────────────────
    m = ОКОЛО.match(с)
    if m:
        _к, n, ф1, n2, ф2, слово, круг, ф3 = m.groups()
        n, n2, круг = int(n), int(n2), int(круг)
        if _ед(ф1) is None:
            return False, False
        близко = (abs(n - круг) <= дом.ДОПУСК
                  and круг == дом.круглое(n))
        если = близко and (n < круг if слово == "nearly" else True)
        return True, (n == n2 and ф1 == ф2 and _ед(ф3) == _ед(ф1)
                      and если and _форма_верна(n, ф1)
                      and _форма_верна(круг, ф3))
    m = ОКОЛО_RU.match(с)
    if m:
        кто, суф, n, ф1, слово, круг, ф2 = m.groups()
        n, круг = int(n), int(круг)
        ключ = _ру_ключ(ф1)
        if ключ is None:
            return False, False
        близко = (abs(n - круг) <= дом.ДОПУСК
                  and круг == дом.круглое(n))
        если = близко and (n < круг if слово == "почти" else True)
        return True, (если and _суффикс_верен(кто, суф)
                      and _ру_пара(n, ф1, ключ)
                      and _ру_пара(круг, ф2, ключ))

    # ── ПОЧЕМУ И ПЕРЕЧЕНЬ ─────────────────────────────────────────
    m = ПОЧЕМУ.match(с)
    if m:
        _к, всего, ф1, а, ф2, б, ф3 = m.groups()
        if _ед(ф1) is None:
            return False, False
        return True, (int(а) + int(б) == int(всего)
                      and _ед(ф2) == _ед(ф1) and _ед(ф3) == _ед(ф1)
                      and _форма_верна(int(всего), ф1)
                      and _форма_верна(int(а), ф2)
                      and _форма_верна(int(б), ф3))
    m = ПОЧЕМУ_RU.match(с)
    if m:
        _род, всего, ф1, кто, суф, а, ф2, б, ф3 = m.groups()
        ключ = _ру_ключ(ф1)
        if ключ is None:
            return False, False
        return True, (int(а) + int(б) == int(всего)
                      and _суффикс_верен(кто, суф)
                      and _ру_пара(int(всего), ф1, ключ)
                      and _ру_пара(int(а), ф2, ключ)
                      and _ру_пара(int(б), ф3, ключ))
    m = ПЕРЕЧЕНЬ.match(с)
    if m:
        _к, и1, и2, и3, место, всего = m.groups()
        объявлено = {м for м, _мера, _ру, _ключ in дом.НЕСЧЁТНОЕ}
        объявлено |= {en for en, _ru in дом.ВЕЩИ}
        if место not in дом.МЕСТА:
            return False, False
        if not {и1, и2, и3} <= объявлено:
            return False, False
        return True, len({и1, и2, и3}) == int(всего)
    m = ПЕРЕЧЕНЬ_RU.match(с)
    if m:
        п, местн, и1, и2, и3, всего, фп = m.groups()
        if _место_по_русски(п, местн) is None:
            return False, False
        if not {и1, и2, и3} <= set(rugram.СЧЁТНЫЕ):
            return False, False
        всего = int(всего)
        return True, (len({и1, и2, и3}) == всего
                      and _ру_пара(всего, фп, "предмет"))

    return False, False


def обход(явные):
    if явные:
        return [pathlib.Path(п) for п in явные]
    try:
        return worlds(kind="shows")
    except Unreadable as беда:
        print(f"БЫТ ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("БЫТ ОТКАЗ: обход пуст, судить нечего")
        return 2
    ложных = судимых = 0
    примеры = []
    for путь in пути:
        свои = 0
        with путь.open(encoding="utf-8", errors="replace") as поток:
            for строка in поток:
                судимо, истинно = судить(строка)
                if not судимо:
                    continue
                судимых += 1
                if not истинно:
                    ложных += 1
                    свои += 1
                    if len(примеры) < 4:
                        примеры.append(
                            f"{путь.name}: {строка.strip()[:80]}")
        if свои:
            print(f"  {путь.name:<30} ложных {свои}")
    for п in примеры:
        print(f"    {п}")
    поза = "ЛЕНТА" if явные else (
        "PASS" if ложных <= ЛОЖНЫХ_РУБЕЖ else "FAIL")
    print(f"БЫТ {поза}: {ложных} ложных из {судимых} судимых "
          f"({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
