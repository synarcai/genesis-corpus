#!/usr/bin/env python3
"""GENESIS layer: THE FOUNDATIONS OF PHYSICS.

    a body covering 60 metres in 12 seconds has speed 5 metres per second.
    тело, прошедшее 60 метров за 12 секунд, имеет скорость 5 метров в секунду.
    force = mass × acceleration; 7 kilograms × 3 metres per second squared = 21 newtons.
    speed is measured in metres per second.

PHYSICS ENTERS A CORPUS AS TWO THINGS AT ONCE, and both are checkable:
a RELATION between quantities (v = s / t, F = m × a, U = I × R) and a
DIMENSION — what the quantity is measured in. A corpus giving the
number without the unit teaches arithmetic; one giving the unit without
the relation teaches vocabulary; the organism needs both in one show.

EVERY VALUE IS WHOLE BY CONSTRUCTION. Distances are multiples of their
times, forces are products, kinetic masses are even — nothing is
rounded. A corpus stating «3.33 metres per second» for ten over three
teaches a rounding as a truth. Where a law needs a real constant
(E = m c², gravitation), THE LAW IS NOT SHOWN: constants are a genus of
their own and need their own court before their shows.

SEVEN LAWS as integer relations — speed, force, work, power, density,
Ohm, kinetic energy — plus the PREFIXES (kilo, centi, milli), which are
conversions and are judged as such, and the DIMENSION table, checked
against its own declaration.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rugram
import units
from layer import emit  # noqa: E402
import mass  # noqa: E402
import plural  # noqa: E402

# СЧЁТНАЯ ФОРМА «МЕТР» (21, 51, 81, 91) НЕСЁТ И ЦЕЛУЮ СКОРОСТЬ (аудит
# покупок holon 03.09: под «# метр» оставались одни отказы — морфология
# дробила рамку, и в осколке жила одна полярность).
# МАССА ОТ ПРАВИЛА (tools/mass.py, М-148): каждая величина — цикл
# множителей, пара составляется шагом по двум взаимно простым циклам;
# различных показов на рамку — до 50 при тех же строках (было 10–14:
# таблица пар повторялась каждым проходом). Счётные формы «метр» (21, 51,
# 81, 91 — «# метр») рождаются произведениями 7 × 3, 17 × 3, 9 × 9, 13 × 7.
ВРЕМЯ = [12, 20, 7, 15, 8, 30, 14, 24, 9, 5, 3]
СКОРОСТЬ = [5, 4, 6, 3, 9, 2, 8, 7, 10, 11, 13, 17, 21]
МАССЫ = [7, 5, 12, 9, 6, 11, 4, 15, 8, 10, 3]
УСКОРЕНИЯ = [3, 4, 2, 5, 8, 9, 6, 7]
СИЛЫ = [20, 15, 30, 12, 25, 18, 40, 14, 35, 16, 22, 9, 8]
ПУТИ = [3, 4, 2, 5, 6, 7, 10]
ПЛОТНОСТИ = [8, 5, 9, 10, 11, 12, 7, 6, 13]
ОБЪЁМЫ = [6, 7, 8, 9, 4, 5, 12, 3, 10, 2, 11]
ТОКИ = [3, 5, 2, 7, 4, 6, 9, 8, 10, 12, 11]
СОПРОТИВЛЕНИЯ = [12, 8, 25, 6, 15, 9, 4, 7, 3, 5, 10, 20, 2]
# кинетическая энергия m × v² / 2 цела при чётной массе
МАССЫ_ТЕЛ = [4, 6, 8, 10, 12, 2, 14, 16, 18, 20, 22]
СКОРОСТИ_ТЕЛ = [3, 5, 2, 4, 7, 6, 9]
ШИРИНА = 10
ИЗМЕРЯЕТСЯ = [
    ("speed", "metres per second", "скорость", "метрах в секунду"),
    ("force", "newtons", "сила", "ньютонах"),
    ("work", "joules", "работа", "джоулях"),
    ("power", "watts", "мощность", "ваттах"),
    ("mass", "kilograms", "масса", "килограммах"),
    ("length", "metres", "длина", "метрах"),
    ("time", "seconds", "время", "секундах"),
    ("current", "amperes", "ток", "амперах"),
    ("voltage", "volts", "напряжение", "вольтах"),
    ("resistance", "ohms", "сопротивление", "омах"),
]


# ПРИСТАВКА ЕСТЬ ЗАКОН, А НЕ ПЯТЬ ФАКТОВ. Эти строки стояли написанными
# от руки — и русская сторона миллиметра в них ПРОПАЛА: пять строк там,
# где закон даёт шесть. Пропуск, невидимый глазу в списке, виден сразу,
# как только список стал выводом. Письмо здесь британское, у слоя
# единиц — американское; оба истинны и оба объявлены.
ПИСЬМО = "brit"
ОСНОВА = "metre"

# ИСКОМОЕ ОБЪЯВЛЯЕТ СВОЙ ВОПРОС ОДИН РАЗ, и вопрос берёт ТЕ ЖЕ
# величины, из которых собран ответ. Замер вопросной поверхности назвал
# физику немой: 1150 строк, вопросов ноль — она сообщала, что тело,
# прошедшее 60 метров за 12 секунд, имеет скорость 5, и ни разу не
# спрашивала, какова эта скорость.
СПРОСИТЬ = {
    "speed": "what speed has a body covering {s} {ед_s} in {t} {ед_t}?",
    "скорость": ("какова скорость тела, прошедшего {s} {метры} "
                 "за {t} {секунды}?"),
    "law": "what does {закон} give for {x} and {y}?",
    "закон": "что даёт {закон} при {x} и {y}?",
    "whole_speed": ("is the speed of a body covering {s} {ед_s} in {t} {ед_t} "
                    "a whole number?"),
    "целая_скорость": "целое ли число скорость тела, прошедшего {s} {метры} за {t} {секунды}?",
}

# ФОРМУЛЫ РОДОВ — ЗАКОН ОТВЕТА ОТ ВЕЛИЧИН ВОПРОСА, объявлен при каждом вопросе
# (таблица родов declarations/GENERA.json — эталон суда охвата, holon 03.09).
ФОРМУЛЫ = {
    "speed": "скорость = путь ÷ время",
    "law": "закон: величина = произведение | частное величин",
    "закон": "закон: величина = произведение | частное величин",
    "скорость": "скорость = путь ÷ время",
    "whole_speed": "целость: путь делится на время?",
    "целая_скорость": "целость: путь делится на время?",
}
assert set(ФОРМУЛЫ) == set(СПРОСИТЬ), "формула у каждого вопроса"


def ед(n, мн):
    """Английская единица при числе — ЗАКОНОМ ПАКЕТА, а не литералом (07.09, вечер).

    Дом писал русскую сторону законом (`rugram.форма`), а английскую — литералом во
    множественном: «{m * a} newtons». Правоту такой строки держит не закон, а ЖРЕБИЙ:
    множители дома таковы, что произведение ни разу не вышло единицей. В день, когда
    выйдет, свод напишет «1 newtons» и станет учить лжи.

        ДОМ, ЗНАЮЩИЙ ЗАКОН СОГЛАСОВАНИЯ НА ОДНОМ ЯЗЫКЕ И ПИШУЩИЙ ЛИТЕРАЛОМ НА ДРУГОМ, НЕ
        ЗАБЫЛ ЗАКОН — ОН ОБЪЯВИЛ ОДИН ЯЗЫК ВТОРОСОРТНЫМ.

    Правка НЕ МЕНЯЕТ НИ БАЙТА нынешнего мира (сличено): при всяком нынешнем числе закон
    даёт ровно тот литерал, что стоял. Она меняет то, что БУДЕТ написано, когда число
    станет единицей, — и потому есть страховка, а не показ.

    Многословная единица склоняет ГОЛОВУ, а не хвост: «1 metre per second», «1 kilogram
    per cubic metre», «1 metre per second squared».
    """
    голова, разрыв, хвост = мн.partition(" per ")
    return plural.by_count(n, голова) + разрыв + хвост


def спросить(искомое, ответ, **части):
    """Вопрос и ответ одной строкой; величины у них одни и те же."""
    return f"{СПРОСИТЬ[искомое].format(**части)} {ответ}"


def приставочные():
    """«1 X = N Y» для каждой приставки, обоими языками."""
    пары = []
    for пр, пр_ru, множитель in units.ПРИСТАВКИ:
        имя = пр + ОСНОВА
        большая, меньшая = ((имя, ОСНОВА) if множитель >= 1
                            else (ОСНОВА, имя))
        сколько = int(units.отношение(большая, меньшая))
        пары.append((f"1 {units.англ(большая, False, ПИСЬМО)} = "
                     f"{сколько} {units.англ(меньшая, True, ПИСЬМО)}.",
                     f"1 {units.рус(большая, 1)} = "
                     f"{сколько} {units.рус(меньшая, сколько)}."))
    # СОСЕДНИЕ ПРИСТАВКИ ТОЖЕ СТОЯ́Т В ОТНОШЕНИИ (07.09, вечер). Ряд ходил только от
    # ОСНОВЫ: «1 metre = 100 centimetres», «1 metre = 1000 millimetres», «1 kilometre =
    # 1000 metres». Оттого САНТИМЕТР ни разу не стоял единицей — мера праздного слова
    # назвала «centimetre» объявленным и не встречающимся в своде при 292 «centimetres».
    #
    #     ЕДИНИЦА, ВСЕГДА СТОЯЩАЯ МЕНЬШЕЙ СТОРОНОЙ ОТНОШЕНИЯ, НИКОГДА НЕ ПОКАЗАНА ОДНА.
    #
    # Отношение сантиметра к миллиметру дом мер знает (десять); строка того же рода, тот
    # же вопрос, новых родов не заводится.
    for большая, меньшая in (("centimetre", "millimetre"),):
        сколько = int(units.отношение(большая, меньшая))
        пары.append((f"1 {units.англ(большая, False, ПИСЬМО)} = "
                     f"{сколько} {units.англ(меньшая, True, ПИСЬМО)}.",
                     f"1 {units.рус(большая, 1)} = "
                     f"{сколько} {units.рус(меньшая, сколько)}."))
    return [en for en, _ in пары] + [ru for _, ru in пары]


def единичные():
    """Страницы, где ВЕЛИЧИНА РАВНА ЕДИНИЦЕ СВОЕЙ МЕРЫ (07.09, вечер).

    Мера `scripts/one_singular.py` назвала долг поимённо: из ста сорока восьми английских
    имён, показанных своду при числе, двадцать четыре показаны ТОЛЬКО во множественном.
    Шесть из них — единицы этого дома: «5 newtons» шестьсот одиннадцать раз, «1 newton» —
    ни разу; так же ampere, ohm, volt, watt, joule.

        ФОРМА, НЕ ПОКАЗАННАЯ ПРИ ЕДИНИЦЕ, НЕ КУПЛЕНА. Читателю неоткуда взять, что при
        единице имя стои́т иначе, — сколько бы строк о множественном он ни прочёл.

    Жребий дома единицы не даёт: множители подобраны так, что произведение не выходит
    единицей ни разу. Потому единица показывается ПРЯМО — но ТЕМИ ЖЕ РОДАМИ, что и всякое
    другое число, и с теми же вопросами. Новый род без вопроса стоил бы долга ширины
    (738 при рубеже 738 — запаса нет ни на один род), а показ, взятый чужим родом, не
    купил бы ничего.

    ЕДИНИЦА ДЕРЖИТСЯ НА ОДНОМ МЕСТЕ, ВТОРОЕ ХОДИТ. Один показ на форму дал бы кворум
    ниже LAW² = 4; потому каждый закон разворачивается по ВТОРОМУ множителю (1, 2, 3, 5) —
    четыре разные страницы одного рода, и во всех четырёх единица стои́т на своём месте.
    Там, где арифметика единицы не допускает (произведение равно единице лишь при обоих
    единицах — «1 ampere × 1 ohm = 1 volt»), страница ОДНА, и это сказано, а не скрыто.
    """
    РЯД = (1, 2, 3, 5)
    вон = []

    def оба(en, ru, ключ=None, ru_ключ=None, ru_закон=None, **части):
        """Страница обоими языками; вопрос — если род его имеет.

        РУССКИЙ ВОПРОС НАЗЫВАЕТ РУССКИЙ ЗАКОН. Первая правка передала обеим сторонам одно
        имя закона, и по-русски вышло «что даёт work = force × distance при 1 и 1?» —
        вопрос на одном языке о законе, названном на другом.
        """
        вон.append(en)
        if ключ:
            вон.append(спросить(ключ, en, **части))
        вон.append(ru)
        if ru_ключ:
            ру_части = {k: v for k, v in части.items() if not k.startswith("ед_")}
            if ru_закон:
                ру_части["закон"] = ru_закон
            вон.append(спросить(ru_ключ, ru, **ру_части))

    for n in РЯД:
        # СКОРОСТЬ: путь ходит, время держит единицу
        оба(f"a body covering {n} {ед(n, 'metres')} in 1 {ед(1, 'seconds')} has speed "
            f"{n} {ед(n, 'metres per second')}.",
            f"тело, прошедшее {n} {rugram.форма('метр', n)} за 1 "
            f"{rugram.форма('секунда', 1)}, имеет скорость "
            f"{n} {rugram.форма('метр', n)} в секунду.",
            "speed", None, s=n, t=1, ед_s=ед(n, "metres"), ед_t=ед(1, "seconds"))
        # СИЛА: ускорение ходит, масса держит единицу — и наоборот
        оба(f"force = mass × acceleration; 1 {ед(1, 'kilograms')} × "
            f"{n} {ед(n, 'metres per second squared')} = {n} {ед(n, 'newtons')}.",
            f"сила = масса × ускорение; 1 {rugram.форма('килограмм', 1)} × "
            f"{n} {rugram.форма('метр', n)} на секунду в квадрате = "
            f"{n} {rugram.форма('ньютон', n)}.",
            "law", None, закон="force = mass × acceleration", x=1, y=n)
        оба(f"force = mass × acceleration; {n} {ед(n, 'kilograms')} × "
            f"1 {ед(1, 'metres per second squared')} = {n} {ед(n, 'newtons')}.",
            f"сила = масса × ускорение; {n} {rugram.форма('килограмм', n)} × "
            f"1 {rugram.форма('метр', 1)} на секунду в квадрате = "
            f"{n} {rugram.форма('ньютон', n)}.",
            "law", None, закон="force = mass × acceleration", x=n, y=1)
        # РАБОТА: путь ходит, сила держит единицу — и наоборот
        оба(f"work = force × distance; 1 {ед(1, 'newtons')} × "
            f"{n} {ед(n, 'metres')} = {n} {ед(n, 'joules')}.",
            f"работа = сила × путь; 1 {rugram.форма('ньютон', 1)} × "
            f"{n} {rugram.форма('метр', n)} = {n} {rugram.форма('джоуль', n)}.",
            "law", "закон", ru_закон="работа = сила × путь",
            закон="work = force × distance", x=1, y=n)
        оба(f"work = force × distance; {n} {ед(n, 'newtons')} × "
            f"1 {ед(1, 'metres')} = {n} {ед(n, 'joules')}.",
            f"работа = сила × путь; {n} {rugram.форма('ньютон', n)} × "
            f"1 {rugram.форма('метр', 1)} = {n} {rugram.форма('джоуль', n)}.",
            "law", "закон", ru_закон="работа = сила × путь",
            закон="work = force × distance", x=n, y=1)
        # МОЩНОСТЬ: равное частное — единица ватта на четырёх разных страницах
        оба(f"power = work / time; {n} {ед(n, 'joules')} / {n} {ед(n, 'seconds')} = "
            f"1 {ед(1, 'watts')}.",
            f"мощность = работа / время; {n} {rugram.форма('джоуль', n)} / "
            f"{n} {rugram.форма('секунда', n)} = 1 {rugram.форма('ватт', 1)}.")
        # НАПРЯЖЕНИЕ: сопротивление ходит, ток держит единицу — и наоборот
        оба(f"voltage = current × resistance; 1 {ед(1, 'amperes')} × "
            f"{n} {ед(n, 'ohms')} = {n} {ед(n, 'volts')}.",
            f"напряжение = ток × сопротивление; 1 {rugram.форма('ампер', 1)} × "
            f"{n} {rugram.форма('ом', n)} = {n} {rugram.форма('вольт', n)}.",
            "law", None, закон="voltage = current × resistance", x=1, y=n)
        оба(f"voltage = current × resistance; {n} {ед(n, 'amperes')} × "
            f"1 {ед(1, 'ohms')} = {n} {ед(n, 'volts')}.",
            f"напряжение = ток × сопротивление; {n} {rugram.форма('ампер', n)} × "
            f"1 {rugram.форма('ом', 1)} = {n} {rugram.форма('вольт', n)}.",
            "law", None, закон="voltage = current × resistance", x=n, y=1)
        # ПЛОТНОСТЬ: равное частное — единица плотности на четырёх страницах
        оба(f"density = mass / volume; {n} {ед(n, 'kilograms')} / "
            f"{n} {ед(n, 'cubic metres')} = 1 {ед(1, 'kilograms per cubic metre')}.",
            f"плотность = масса / объём; {n} {rugram.форма('килограмм', n)} / "
            f"{n} {rugram.форма('кубометр', n)} = "
            f"1 {rugram.форма('килограмм', 1)} на кубометр.")
    return вон


ЕДИНИЧНЫЕ = единичные()

ПРИСТАВОЧНЫЕ = приставочные()


def pass_shows(pass_i):
    out = []
    for i in range(ШИРИНА):
        k = mass.шаг(pass_i, i, ШИРИНА)
        v0, t = mass.пара(k, СКОРОСТЬ, ВРЕМЯ)
        s = v0 * t
        m, a = mass.пара(k, МАССЫ, УСКОРЕНИЯ)
        f, d = mass.пара(k, СИЛЫ, ПУТИ)
        ρ, v = mass.пара(k, ПЛОТНОСТИ, ОБЪЁМЫ)
        mm = ρ * v
        cur, r = mass.пара(k, ТОКИ, СОПРОТИВЛЕНИЯ)
        km, kv = mass.пара(k, МАССЫ_ТЕЛ, СКОРОСТИ_ТЕЛ)
        ск_en = (f"a body covering {s} {ед(s, 'metres')} in {t} {ед(t, 'seconds')} "
                 f"has speed {s // t} {ед(s // t, 'metres per second')}.")
        ск_ru = (f"тело, прошедшее {s} {rugram.форма('метр', s)} за "
                 f"{t} {rugram.форма('секунда', t)}, имеет скорость "
                 f"{s // t} {rugram.форма('метр', s // t)} в секунду.")
        out.append(ск_en)
        out.append(ск_ru)
        out.append(спросить("speed", ск_en, s=s, t=t,
                            ед_s=ед(s, "metres"), ед_t=ед(t, "seconds")))
        out.append(спросить("скорость", ск_ru, s=s, t=t,
                            метры=rugram.форма("метр", s),
                            секунды=rugram.форма("секунда", t)))
        закон_ск = f"speed = distance / time; {s} / {t} = {s // t}."
        out.append(закон_ск)
        out.append(спросить("law", закон_ск, закон="speed = distance / time",
                            x=s, y=t))
        сил_en = (f"force = mass × acceleration; {m} {ед(m, 'kilograms')} × {a} "
                  f"{ед(a, 'metres per second squared')} = "
                  f"{m * a} {ед(m * a, 'newtons')}.")
        out.append(сил_en)
        out.append(спросить("law", сил_en,
                            закон="force = mass × acceleration", x=m, y=a))
        out.append(f"сила = масса × ускорение; "
                   f"{m} {rugram.форма('килограмм', m)} × "
                   f"{a} {rugram.форма('метр', a)} на секунду в квадрате = "
                   f"{m * a} {rugram.форма('ньютон', m * a)}.")
        раб_en = (f"work = force × distance; {f} {ед(f, 'newtons')} × "
                  f"{d} {ед(d, 'metres')} = {f * d} {ед(f * d, 'joules')}.")
        out.append(раб_en)
        out.append(спросить("law", раб_en, закон="work = force × distance",
                            x=f, y=d))
        раб_ru = (f"работа = сила × путь; "
                  f"{f} {rugram.форма('ньютон', f)} × "
                  f"{d} {rugram.форма('метр', d)} = "
                  f"{f * d} {rugram.форма('джоуль', f * d)}.")
        out.append(раб_ru)
        out.append(спросить("закон", раб_ru, закон="работа = сила × путь",
                            x=f, y=d))
        out.append(f"power = work / time; {f * d} {ед(f * d, 'joules')} / "
                   f"{d} {ед(d, 'seconds')} = {f} {ед(f, 'watts')}.")
        out.append(f"мощность = работа / время; {f * d} "
                   f"{rugram.форма('джоуль', f * d)} / {d} "
                   f"{rugram.форма('секунда', d)} = {f} "
                   f"{rugram.форма('ватт', f)}.")
        out.append(f"density = mass / volume; {mm} {ед(mm, 'kilograms')} / "
                   f"{v} {ед(v, 'cubic metres')} = "
                   f"{mm // v} {ед(mm // v, 'kilograms per cubic metre')}.")
        out.append(f"плотность = масса / объём; "
                   f"{mm} {rugram.форма('килограмм', mm)} / "
                   f"{v} {rugram.форма('кубометр', v)} = "
                   f"{mm // v} {rugram.форма('килограмм', mm // v)} "
                   f"на кубометр.")
        напр_en = (f"voltage = current × resistance; {cur} {ед(cur, 'amperes')} × "
                   f"{r} {ед(r, 'ohms')} = {cur * r} {ед(cur * r, 'volts')}.")
        out.append(напр_en)
        out.append(спросить("law", напр_en,
                            закон="voltage = current × resistance",
                            x=cur, y=r))
        out.append(f"напряжение = ток × сопротивление; {cur} "
                   f"{rugram.форма('ампер', cur)} × {r} {rugram.форма('ом', r)} = "
                   f"{cur * r} {rugram.форма('вольт', cur * r)}.")
        out.append(f"kinetic energy = mass × speed squared / 2; {km} × "
                   f"{kv} × {kv} / 2 = "
                   f"{km * kv * kv // 2} {ед(km * kv * kv // 2, 'joules')}.")
        out.append(f"кинетическая энергия = масса × квадрат скорости / 2; "
                   f"{km} × {kv} × {kv} / 2 = {km * kv * kv // 2} "
                   f"{rugram.форма('джоуль', km * kv * kv // 2)}.")
        out.extend(ПРИСТАВОЧНЫЕ)
        out.extend(ЕДИНИЧНЫЕ)
        en_имя, en_ед, ru_имя, ru_ед = ИЗМЕРЯЕТСЯ[
            (pass_i * 3 + i) % len(ИЗМЕРЯЕТСЯ)]
        out.append(f"{en_имя} is measured in {en_ед}.")
        out.append(f"{ru_имя} измеряется в {ru_ед}.")
        # WHOLENESS IS A YES/NO QUESTION (holon 03.09, value-not-verdict: a
        # question for a VALUE answered by a refusal looked like a verdict
        # frame with one polarity). The value question keeps its value
        # answers; wholeness is asked as its own question, and both answers
        # lie side by side — «yes» with the whole value, «no» with the reason.
        путь, срок = (s + t if i % 2 == 0 else s + 1), t
        м, сек = rugram.форма("метр", путь), rugram.форма("секунда", срок)
        # СКАЗУЕМОЕ ИДЁТ ЗА ЧИСЛОМ, А НЕ ЗА СЛОВОМ «МЕТРЫ»: «61 метр не
        # даёт», но «73 метра не дают»; единственность выводится из того
        # же дома форм — если форма при этом числе совпала с формой при
        # единице, число ведёт себя как один.
        один = (rugram.форма("метр", путь) == rugram.форма("метр", 1))
        if путь % срок == 0:
            v = путь // срок
            out.append(спросить("whole_speed",
                                f"yes: {путь} ÷ {срок} = {v} {ед(v, 'metres per second')}.",
                                ед_s=ед(путь, "metres"), ед_t=ед(срок, "seconds"),
                                s=путь, t=срок))
            out.append(спросить("целая_скорость", f"да: {путь} ÷ {срок} = {v} {rugram.форма('метр', v)} в секунду.",
                                s=путь, t=срок, метры=м, секунды=сек))
        else:
            дают = "не даёт" if один else "не дают"
            # АНГЛИЙСКОЕ СКАЗУЕМОЕ СОГЛАСУЕТСЯ ПО СВОЕМУ ЗАКОНУ, А НЕ ПО ЧУЖОМУ ПРИЗНАКУ.
            # Первая правка взяла русский признак `один` — «форма метра при N та же, что
            # при единице», — и написала «61 metres does not give»: по-русски «61 метр»
            # ведёт себя как один, по-английски «61 metres» — как многие.
            #
            #     ВЗЯТЬ ЧУЖОЙ ПРИЗНАК СОГЛАСОВАНИЯ ЕСТЬ ТОТ ЖЕ ГРЕХ, ЧТО НАПИСАТЬ ЛИТЕРАЛ:
            #     ОБА РАЗА ЯЗЫК СУДИТСЯ НЕ СВОИМ ЗАКОНОМ.
            out.append(спросить("whole_speed",
                                f"no: {путь} {ед(путь, 'metres')} in {срок} {ед(срок, 'seconds')} "
                                f"{'does' if путь == 1 else 'do'} not give a whole speed, "
                                f"{путь} is not divisible by {срок}.",
                                ед_s=ед(путь, "metres"), ед_t=ед(срок, "seconds"),
                                s=путь, t=срок))
            out.append(спросить("целая_скорость", f"нет: {путь} {м} за {срок} {сек} {дают} целой "
                                f"скорости, {путь} не делится на {срок} нацело.",
                                s=путь, t=срок, метры=м, секунды=сек))
    return out


def main():
    emit("datasets/genesis_physics.txt", pass_shows)


if __name__ == "__main__":
    main()
