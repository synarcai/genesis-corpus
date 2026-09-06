#!/usr/bin/env python3
"""THE HOUSE OF THE TEMPERATURE SCALE — one quantity, two scales, and a formula with an INVERSE (06.09).

The census found ZERO lines carrying «по Цельсию», «Celsius» or «Fahrenheit» in the whole свод.
The corpus converts units by multiplication (kilometres to metres, hours to minutes) — every one
of those conversions is a single factor, and a factor is the easy half of conversion. The two
temperature scales are the other half: they differ by a FACTOR AND AN OFFSET, and that is the
first conversion in this corpus that cannot be done by one multiplication. Whoever has learned
only factors will multiply twenty by nine fifths and call it Fahrenheit.

WHAT THE HOUSE SHOWS:
  в_фаренгейт — the forward road, in two steps that are both written out: the factor first
                («20 × 9 ÷ 5 = 36»), then the offset («36 + 32 = 68»);
  в_цельсий   — the road back, in the OPPOSITE ORDER: the offset first («68 − 32 = 36»), then the
                factor inverted («36 × 5 ÷ 9 = 20»). A reader that undoes the steps in the same
                order they were done gets a wrong number, and this pair of frames is where that is
                learned;
  опора       — the two anchors of the pair, tied to the facts the corpus already holds: water
                freezes at zero Celsius (thirty-two Fahrenheit) and boils at a hundred (two
                hundred and twelve). The offset is not an arbitrary constant — it is the distance
                between the two zeros, and the page says which fact stands at each anchor.

THE NUMBERS ARE CHOSEN SO THAT BOTH ROADS ARE WHOLE: every Celsius value is a multiple of five,
and the house shows the negative ones too (−10, −5), because the offset is where a sign is easiest
to lose.

TWO STEPS, TWO SENTENCES — AND THAT IS A SCAR, NOT A STYLE. Written with a comma between them
(«… = −18, (−18) + 32 = 14»), the second step MERGES with the first for the court of arithmetic:
a negative number after a comma is read as a continuation of the previous expression, and the
court called thirty-six honest pages false. The parenthesis around the negative summand was not
enough; only the full stop separates the steps. The same scar is written in the corpus's laws for
a ledger opening with a negative number.

WHAT IS BORROWED: the count forms of «degree» through the pack rule (the house of the pair), and
the two water facts from the house of nature. Declared here: the degree word in nine languages and
the names of the two scales.

WHAT IS NOT MEASURED, NAMED: Kelvin (a third scale with a third zero), a temperature that is not
a whole number on both scales, and the DIFFERENCE of two temperatures (where the offset cancels
and the factor does not — a trap worth its own house).
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import natureforms as NF  # noqa: E402 — the two water facts live there and are not rewritten here
import svampforms as S  # noqa: E402 — the count cell of a pack

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
# ГРАДУС СО СЧЁТНЫМИ ФОРМАМИ: дом природы объявляет его для СВОИХ рамок одним словом,
# а здесь число стоит при нём в трёх видах (1, 2, 5), и правило пакета требует форм.
ГРАДУС = {"ru": ("градус", "градуса", "градусов"), "en": ("degree", "degrees"),
          "de": ("Grad", "Grad"), "fr": ("degré", "degrés"), "es": ("grado", "grados"),
          "it": ("grado", "gradi"), "pt": ("grau", "graus"), "nl": ("graad", "graden"),
          "pl": ("stopień", "stopnie", "stopni")}
ШКАЛЫ = {"ru": ("по Цельсию", "по Фаренгейту"), "en": ("Celsius", "Fahrenheit"),
         "de": ("Celsius", "Fahrenheit"), "fr": ("Celsius", "Fahrenheit"),
         "es": ("Celsius", "Fahrenheit"), "it": ("Celsius", "Fahrenheit"),
         "pt": ("Celsius", "Fahrenheit"), "nl": ("Celsius", "Fahrenheit"),
         "pl": ("Celsjusza", "Fahrenheita")}
# ЦЕЛЬСИИ, КРАТНЫЕ ПЯТИ: обе дороги целые, и два из них ОТРИЦАТЕЛЬНЫ — знак теряется на сдвиге
ЦЕЛЬСИИ = (-10, -5, 5, 10, 15, 20, 25, 30, 35, 40)
ОПОРЫ = ((0, "замерзает"), (100, "кипит"))
ФОРМЫ = ("в_фаренгейт", "в_цельсий", "опора")
РЕЧЬ = {
    "ru": dict(вопрос_ф="{C} {Ш1} — сколько это {Ш2}?", вопрос_ц="{F} {Ш2} — сколько это {Ш1}?",
               опора="{C} {Ш1} — это {F} {Ш2}: при этой температуре вода {что}",
               вопрос_опоры="при скольких градусах {Ш1} вода {что}?", двоеточие=": "),
    "en": dict(вопрос_ф="{C} {Ш1} — how much is that in {Ш2}?",
               вопрос_ц="{F} {Ш2} — how much is that in {Ш1}?",
               опора="{C} {Ш1} is {F} {Ш2}: at this temperature water {что}", вопрос_опоры="at how many degrees {Ш1} does water {что}?", двоеточие=": "),
    "de": dict(вопрос_ф="{C} {Ш1} — wie viel ist das in {Ш2}?",
               вопрос_ц="{F} {Ш2} — wie viel ist das in {Ш1}?",
               опора="{C} {Ш1} sind {F} {Ш2}: bei dieser Temperatur {что} Wasser", вопрос_опоры="bei wie viel Grad {Ш1} {что} Wasser?", двоеточие=": "),
    "fr": dict(вопрос_ф="{C} {Ш1} — combien cela fait-il en {Ш2} ?",
               вопрос_ц="{F} {Ш2} — combien cela fait-il en {Ш1} ?",
               опора="{C} {Ш1} font {F} {Ш2} : à cette température l'eau {что}", вопрос_опоры="à combien de degrés {Ш1} l'eau {что} ?", двоеточие=" : "),
    "es": dict(вопрос_ф="{C} {Ш1} — ¿cuánto es eso en {Ш2}?",
               вопрос_ц="{F} {Ш2} — ¿cuánto es eso en {Ш1}?",
               опора="{C} {Ш1} son {F} {Ш2}: a esta temperatura el agua {что}", вопрос_опоры="¿a cuántos grados {Ш1} el agua {что}?", двоеточие=": "),
    "it": dict(вопрос_ф="{C} {Ш1} — quanto fa in {Ш2}?", вопрос_ц="{F} {Ш2} — quanto fa in {Ш1}?",
               опора="{C} {Ш1} sono {F} {Ш2}: a questa temperatura l'acqua {что}", вопрос_опоры="a quanti gradi {Ш1} l'acqua {что}?", двоеточие=": "),
    "pt": dict(вопрос_ф="{C} {Ш1} — quanto é isso em {Ш2}?",
               вопрос_ц="{F} {Ш2} — quanto é isso em {Ш1}?",
               опора="{C} {Ш1} são {F} {Ш2}: a esta temperatura a água {что}", вопрос_опоры="a quantos graus {Ш1} a água {что}?", двоеточие=": "),
    "nl": dict(вопрос_ф="{C} {Ш1} — hoeveel is dat in {Ш2}?",
               вопрос_ц="{F} {Ш2} — hoeveel is dat in {Ш1}?",
               опора="{C} {Ш1} is {F} {Ш2}: bij deze temperatuur {что} water", вопрос_опоры="bij hoeveel graden {Ш1} {что} water?", двоеточие=": "),
    "pl": dict(вопрос_ф="{C} {Ш1} — ile to jest {Ш2}?", вопрос_ц="{F} {Ш2} — ile to jest {Ш1}?",
               опора="{C} {Ш1} to {F} {Ш2}: w tej temperaturze woda {что}", вопрос_опоры="przy ilu stopniach {Ш1} woda {что}?", двоеточие=": "),
}


# ФОРМА ГЛАГОЛА В ВОПРОСЕ — ОБЪЯВЛЕНА, А НЕ ВЗЯТА У УТВЕРЖДЕНИЯ.
#
# Ворота записи поймали это ДО того, как оно легло в свод (06.09): вопрос, собранный из глагола
# утверждения, дал «at how many degrees Celsius does water FREEZES?» и «l'eau BOUT-T-ELLE ?».
# Английский после «does» требует ГОЛОЙ формы; французская инверсия вставляет эвфоническое «-t-»
# лишь тогда, когда глагол кончается ГЛАСНОЙ («gèle-t-elle» против «bout-elle»). Семь прочих
# языков ставят в вопросе ту же форму, что в утверждении, и это объявлено, а не умолчано.
ВОПРОСНАЯ_ФОРМА = {
    "en": {"freezes": "freeze", "boils": "boil"},
    "fr": {"gèle": "gèle-t-elle", "bout": "bout-elle"},
}


def _вода_в_вопросе(язык, что):
    глагол = _вода(язык, что)
    return ВОПРОСНАЯ_ФОРМА.get(язык, {}).get(глагол, глагол)


def _вода(язык, что):
    """The verb of the water fact is the house of nature's own — taken, not written again."""
    for _вещь, глагол, градусов in NF.ЯЗЫКИ[язык]["температуры"]:
        if (градусов == 100) == (что == "кипит"):
            return глагол
    return что


def знак(n):
    """МИНУС КОРПУСА ЕСТЬ «−» (U+2212), А НЕ ДЕФИС: подписанный мир пишет его так во всех
    1 296 своих строках, и суд знаков читает именно его."""
    return f"−{-n}" if n < 0 else str(n)


def в_леджере(n):
    """Отрицательное ПЕРВОЕ слагаемое шага стоит в скобках: «(−18) × 5 ÷ 9 = −10» — иначе минус
    между двумя числами читается знаком действия (шрам подписанного мира)."""
    return f"({знак(n)})" if n < 0 else знак(n)


def градусы(язык, n):
    """«20 градусов», «41 stopień» — счётная форма при числе берётся у правила пакета."""
    return "%s %s" % (знак(n), S._счёт(ГРАДУС[язык], abs(n), язык))


def фаренгейт(c):
    return c * 9 // 5 + 32


def страница(язык, форма, c):
    р, (Ш1, Ш2) = РЕЧЬ[язык], ШКАЛЫ[язык]
    f, шаг = фаренгейт(c), c * 9 // 5
    C, F = градусы(язык, c) + " " + Ш1, градусы(язык, f) + " " + Ш2
    if форма == "в_фаренгейт":
        # ВПЕРЁД: сперва множитель, потом сдвиг
        return (р["вопрос_ф"].format(C=градусы(язык, c), Ш1=Ш1, Ш2=Ш2) + " " + градусы(язык, f)
                + " " + Ш2 + р["двоеточие"]
                + f"{в_леджере(c)} × 9 ÷ 5 = {знак(шаг)}. {в_леджере(шаг)} + 32 = {знак(f)}.")
    if форма == "в_цельсий":
        # НАЗАД: сперва сдвиг, потом множитель — порядок ОБРАТНЫЙ, и в этом весь урок
        return (р["вопрос_ц"].format(F=градусы(язык, f), Ш1=Ш1, Ш2=Ш2) + " " + градусы(язык, c)
                + " " + Ш1 + р["двоеточие"]
                + f"{в_леджере(f)} − 32 = {знак(шаг)}. {в_леджере(шаг)} × 5 ÷ 9 = {знак(c)}.")
    # ОПОРА СПРОШЕНА, А НЕ ОБЪЯВЛЕНА: вопрос о температуре факта, ответ — обе шкалы
    что = "кипит" if c == 100 else "замерзает"
    вопрос = р["вопрос_опоры"].format(Ш1=Ш1, что=_вода_в_вопросе(язык, что))
    return (вопрос + " " + р["опора"].format(C=градусы(язык, c), F=градусы(язык, f),
                                             Ш1=Ш1, Ш2=Ш2, что=_вода(язык, что)) + ".")


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for c in ЦЕЛЬСИИ:
            for форма in ("в_фаренгейт", "в_цельсий"):
                вон[страница(язык, форма, c)] = (язык, форма)
        for c, _что in ОПОРЫ:
            вон[страница(язык, "опора", c)] = (язык, "опора")
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    сорт = sorted({с for с in слова if с}, key=lambda с: (-len(с), с))
    return "(?:" + "|".join(re.escape(с) for с in сорт) + ")"


def _дыры(язык):
    гр = r"−?\d+ " + _альт(ГРАДУС[язык])
    # КОНСТАНТЫ ЗАКОНА (9, 5, 32) СТОЯТ ДЫРАМИ, А НЕ БУКВОЙ: подменённый множитель обязан
    # быть ЛОЖЬЮ, а не немотой — суд, чей образец держит закон буквой, слепнет ровно на той
    # порче, ради которой поставлен (тот же шрам, что у дома цены с обратной ссылкой).
    return {"C": гр, "F": гр, "c": r"\(?−?\d+\)?", "f": r"\(?−?\d+\)?",
            "ш": r"−?\d+", "шл": r"\(?−?\d+\)?",
            "a": r"\d+", "b": r"\d+", "o": r"\d+", "Ш1": _альт([ШКАЛЫ[язык][0]]),
            "Ш2": _альт([ШКАЛЫ[язык][1]]), "что": _альт(г for _в, г, _n in NF.ЯЗЫКИ[язык]["температуры"]),
            # ЯЧЕЙКА ВОПРОСНОЙ ФОРМЫ ОТДЕЛЬНА ОТ ЯЧЕЙКИ УТВЕРЖДЕНИЯ: иначе «does water freezes»
            # прошла бы образцом как «что», и суд, поставленный ловить порчу глагола, слеп бы
            # ровно на ней
            "чтоВ": _альт(ВОПРОСНАЯ_ФОРМА.get(язык, {}).get(г, г)
                          for _в, г, _n in NF.ЯЗЫКИ[язык]["температуры"])}


# ПЕРЕВЁРНУТЫЙ ПОРЯДОК ШАГОВ — не чужой леджер, а СВОЙ, сделанный не в том порядке:
# вперёд сперва прибавляют, потом множат; назад сперва множат, потом отнимают.
ЛЕДЖЕР_ВПЕРЁД_НАВЫВОРОТ = "{c} + {o} = {ш}. {шл} × {a} ÷ {b} = {f}."
ЛЕДЖЕР_НАЗАД_НАВЫВОРОТ = "{f} × {b} ÷ {a} = {ш}. {шл} − {o} = {c}."


def рамка(язык, форма, скрещено=False):
    """Рамка дороги; СКРЕЩЁННАЯ — вопрос одной дороги с леджером другой.

    ПОРЯДОК ШАГОВ ЕСТЬ ЗАКОН ЭТОГО ДОМА, И СУД, МОЛЧАЩИЙ О ПЕРЕВЁРНУТОМ ПОРЯДКЕ, СЛЕП РОВНО
    НА ТОЙ ЛЖИ, РАДИ КОТОРОЙ ПОСТАВЛЕН. Страница «68 − 32 = 36, 36 × 5 ÷ 9 = 20» истинна, а
    «68 × 5 ÷ 9 = 36, 36 − 32 = 20» — ложь ТОГО ЖЕ дома: числа те же, порядок обратный. Без
    скрещённой рамки она не совпадала ни с одним образцом и получала молчание, а немота хуже
    лжи (палата, услышав молчание, берёт вердикт у соседа).
    """
    р = РЕЧЬ[язык]
    if скрещено:
        вопрос = (р["вопрос_ф"].format(C="{C}", Ш1="{Ш1}", Ш2="{Ш2}") + " {F} {Ш2}"
                  if форма == "в_фаренгейт" else
                  р["вопрос_ц"].format(F="{F}", Ш1="{Ш1}", Ш2="{Ш2}") + " {C} {Ш1}")
        навыворот = (ЛЕДЖЕР_ВПЕРЁД_НАВЫВОРОТ if форма == "в_фаренгейт"
                     else ЛЕДЖЕР_НАЗАД_НАВЫВОРОТ)
        return вопрос + р["двоеточие"] + навыворот
    if форма == "в_фаренгейт":
        return (р["вопрос_ф"].format(C="{C}", Ш1="{Ш1}", Ш2="{Ш2}") + " {F} {Ш2}"
                + р["двоеточие"] + "{c} × {a} ÷ {b} = {ш}. {шл} + {o} = {f}.")
    if форма == "в_цельсий":
        return (р["вопрос_ц"].format(F="{F}", Ш1="{Ш1}", Ш2="{Ш2}") + " {C} {Ш1}"
                + р["двоеточие"] + "{f} − {o} = {ш}. {шл} × {b} ÷ {a} = {c}.")
    return (р["вопрос_опоры"].format(Ш1="{Ш1}", что="{чтоВ}") + " "
            + р["опора"].format(C="{C}", F="{F}", Ш1="{Ш1}", Ш2="{Ш2}", что="{что}") + ".")


def _образец(язык, форма, скрещено=False):
    дыры, счёт, куски = _дыры(язык), {}, []
    for кусок in re.split(r"(\{[^}]+\})", рамка(язык, форма, скрещено)):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = ([(_образец(язык, форма), язык, форма, False) for язык in ЯЗЫКИ for форма in ФОРМЫ]
           + [(_образец(язык, форма, True), язык, форма, True)
              for язык in ЯЗЫКИ for форма in ("в_фаренгейт", "в_цельсий")])


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _число(кусок):
    """Число страницы: минус корпуса и скобки леджера снимаются перед счётом."""
    голое = кусок.split(" ", 1)[0].strip("()").replace("−", "-")
    return int(голое)


def _вердикт(язык, форма, зн):
    c, f = _число(зн["C"]), _число(зн["F"])
    if зн["C"] != градусы(язык, c) or зн["F"] != градусы(язык, f):
        return False
    if фаренгейт(c) != f:
        return False
    if форма == "опора":
        # ОПОРА ЕСТЬ ФАКТ МИРА: нуль замерзания и сто кипения, и глагол при них — свой
        что = "кипит" if c == 100 else "замерзает"
        return c in (0, 100) and зн["что"] == _вода(язык, что)
    ш = c * 9 // 5
    # ЗАКОН ЖИВЁТ В ЧИСЛАХ СТРАНИЦЫ: девять пятых и тридцать два судятся, а не подразумеваются;
    # и СКОБКА ПРИ ОТРИЦАТЕЛЬНОМ ПЕРВОМ СЛАГАЕМОМ есть часть записи, а не украшение
    # ЧИСЛО ШАГА ПИШЕТСЯ ДВАЖДЫ И ПО-РАЗНОМУ: голым после равенства и В СКОБКАХ, когда оно
    # отрицательно и стоит ПЕРВЫМ слагаемым следующего шага. Обе записи судятся, и скобка есть
    # часть записи мира, а не украшение.
    if зн["ш"] != знак(ш) or зн["шл"] != в_леджере(ш):
        return False
    return (_число(зн["c"]) == c and _число(зн["f"]) == f and _число(зн["ш"]) == ш
            and (int(зн["a"]), int(зн["b"]), int(зн["o"])) == (9, 5, 32))


def _судить_образцом(строка):
    """(судимо, истинно): a page of the two scales whose both steps recompute; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма, скрещено in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        if скрещено:
            # ВОПРОС ОДНОЙ ДОРОГИ С ЛЕДЖЕРОМ ДРУГОЙ: числа могут сойтись, порядок — нет
            return True, False
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(язык, форма, зн)
    return False, False


def _самопроверка():
    assert фаренгейт(0) == 32 and фаренгейт(100) == 212 and фаренгейт(-10) == 14
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        ф = страница(язык, "в_фаренгейт", 20)
        # (1) СДВИГ ЗАБЫТ: множитель есть, тридцати двух нет
        битая = ф.replace("36 + 32 = 68", "36 + 32 = 36").replace(градусы(язык, 68), градусы(язык, 36))
        assert судить(битая) == (True, False), битая
        # (2) МНОЖИТЕЛЬ ПЕРЕВЁРНУТ: пять девятых вместо девяти пятых
        битая = ф.replace("20 × 9 ÷ 5 = 36", "20 × 5 ÷ 9 = 11")
        assert судить(битая) == (True, False), битая
        ц = страница(язык, "в_цельсий", 20)
        assert судить(ц) == (True, True), ц
        # (3) ДОРОГА НАЗАД ИДЁТ В ТОМ ЖЕ ПОРЯДКЕ: сперва множитель, потом сдвиг
        битая = ц.replace("68 − 32 = 36. 36 × 5 ÷ 9 = 20", "68 × 5 ÷ 9 = 36. 36 − 32 = 20")
        assert судить(битая) == (True, False), битая
        # (3б) СКОБКА ПРИ ОТРИЦАТЕЛЬНОМ ПЕРВОМ СЛАГАЕМОМ СНЯТА — запись мира нарушена
        мм = страница(язык, "в_цельсий", -10)
        битая = мм.replace("(−18) × 5", "−18 × 5")
        assert судить(битая) in ((True, False), (False, False)), битая
        # (4) ЗНАК ПОТЕРЯН НА СДВИГЕ
        м = страница(язык, "в_фаренгейт", -10)
        assert судить(м) == (True, True), м
        битая = м.replace("(−18) + 32 = 14", "18 + 32 = 50").replace(градусы(язык, 14), градусы(язык, 50))
        assert судить(битая) in ((True, False), (False, False)), битая
        о = страница(язык, "опора", 0)
        assert судить(о) == (True, True), о
        # (5) ОПОРА НАЗВАЛА ЧУЖОЙ ФАКТ: при нуле вода не кипит. ВОПРОСНАЯ ФОРМА ПОДМЕНЯЕТСЯ
        # СВОЕЙ ЖЕ, а не общей заменой строки: «gèle-t-elle» → «bout-t-elle» дало бы форму,
        # которой во французском нет вовсе, и порча стала бы НЕМОТОЙ вместо лжи
        битая = о.replace(_вода_в_вопросе(язык, "замерзает"), _вода_в_вопросе(язык, "кипит"), 1)
        битая = битая.replace(_вода(язык, "замерзает"), _вода(язык, "кипит"))
        assert судить(битая) == (True, False), битая
        мутанты += 5
        # (6) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        вопрос = ф[:ф.index("?") + 1]
        assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "в_фаренгейт", 20))
    for язык in ("ru", "de", "pl"):
        print("  ", страница(язык, "в_цельсий", -10))
        print("  ", страница(язык, "опора", 100))
    по_форме = {}
    for _, (_я, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, цельсиев {len(ЦЕЛЬСИИ)}, "
          f"образцов {len(ОБРАЗЦЫ)}): " + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))




import closedworld as _зк  # noqa: E402 — закон замкнутого мира читается после сборки показов
_СКЕЛЕТЫ_ЗНАКА = _зк.скелеты_знака(ПОКАЗЫ)


def судить(строка):
    """(судимо, истинно) — с ЗАКОНОМ ЗНАКА поверх образца.

    ЗНАК ДЕЙСТВИЯ СУДИТСЯ ЗАКОНОМ ЗАМКНУТОГО МИРА, А НЕ ДЫРОЙ В КАЖДОЙ РАМКЕ: строка,
    становящаяся ИСТИННОЙ при замене одного знака, есть строка ЭТОГО дома с испорченным
    знаком (М-489). Прежде такая строка получала НЕМОТУ, и палата брала истину у суда
    арифметики — у соседа (М-131).
    """
    вердикт = _судить_образцом(строка)
    if вердикт[0] is False and _зк.ложь_по_знаку(
            строка, _СКЕЛЕТЫ_ЗНАКА, ПОКАЗЫ, _судить_образцом):
        return True, False
    return вердикт
if __name__ == "__main__":
    _самопроверка()
