#!/usr/bin/env python3
"""ДОМ ФАКТА И МНЕНИЯ — что можно проверить и что проверить нельзя.

Корпус научился отказывать честно (граница знания: «я не знаю: погода меняется
каждый день, а я её не вижу») и научился отвечать с основанием. Одного он не
умел вовсе: РАЗЛИЧАТЬ ДВА РОДА УТВЕРЖДЕНИЙ. «Лёд плавает в воде» и «эта книга
интересная» стоят в речи одинаково, а проверяются по-разному — первое
наблюдением, второе никак, — и организм, не знающий этой разницы, будет спорить
о вкусах и соглашаться с ложью с равной уверенностью.

    лёд плавает в воде — это факт или мнение? факт: это можно проверить.
    эта книга интересная — это факт или мнение? мнение: у другого человека
        оно может быть другим.

ФАКТ ЗДЕСЬ НЕ ПИШЕТСЯ ЗАНОВО, А ЦИТИРУЕТСЯ У ДОМА ФАКТОВ МИРА — тем же ходом,
каким дом отклика цитирует закон дома поведения. Суд сличает процитированное со
списком соседа слово в слово, и подмена ловится машинально: строка, объявившая
ФАКТОМ то, чего сосед фактом не объявлял, ложна, даже если звучит верно.
Так корпус не может завести себе «фактов» тайком от собственного объявления.

МНЕНИЯ ОБЪЯВЛЕНЫ СВОИМ СПИСКОМ, и список этот нарочно безобиден: вкус к книге,
цвету, супу. Мнение о ЧЕЛОВЕКЕ («он ленивый») сюда не берётся ни одно — корпус,
показывающий такие мнения, учит их высказывать, а различению рода они не нужны:
для него довольно вкуса к супу.

ДЕВЯТЬ ЯЗЫКОВ: названный долг пяти уплачен вслед за домом фактов мира, и
раньше него он уплачен быть не мог — дом мнения ЦИТИРУЕТ его факты, и цитировать
было нечего, пока сосед молчал на четырёх языках. Порядок уплаты был назван
вместе с долгом и соблюдён.

ОБЕ ФОРМЫ ВОПРОСНЫЕ, голых утверждений дом не пишет (М-268).

    python3 tools/opinionforms.py    # самопроверка с мутантами
"""
import re
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import worldfacts as W  # noqa: E402

# ФАКТЫ БЕРУТСЯ У СОСЕДА, и берутся ПЕРВЫЕ ШЕСТЬ: седьмой («дождь идёт») есть
# наблюдение мгновения, а не устойчивый факт мира — назвать его фактом наравне
# со «лёд плавает в воде» значило бы стереть разницу, ради которой дом и стоит.
ФАКТОВ = 6

МНЕНИЯ = {
    "ru": ("эта книга интересная", "этот цвет красивый", "этот суп вкусный",
           "эта музыка хорошая", "здесь уютно", "эта дорога длинная"),
    "en": ("this book is interesting", "this colour is beautiful", "this soup is tasty",
           "this music is good", "it is cosy here", "this road is long"),
    "de": ("dieses Buch ist interessant", "diese Farbe ist schön", "diese Suppe ist lecker",
           "diese Musik ist gut", "hier ist es gemütlich", "dieser Weg ist lang"),
    "fr": ("ce livre est intéressant", "cette couleur est belle", "cette soupe est bonne",
           "cette musique est bonne", "il fait bon ici", "cette route est longue"),
    "es": ("este libro es interesante", "este color es bonito", "esta sopa está rica",
           "esta música es buena", "aquí se está bien", "este camino es largo"),
    "it": (
           "questo libro è interessante",
           "questo colore è bello",
           "questa zuppa è buona",
           "questa musica è bella",
           "qui si sta bene",
           "questa strada è lunga"),
    "pt": (
           "este livro é interessante",
           "esta cor é bonita",
           "esta sopa é boa",
           "esta música é boa",
           "aqui está-se bem",
           "esta estrada é longa"),
    "nl": (
           "dit boek is interessant",
           "deze kleur is mooi",
           "deze soep is lekker",
           "deze muziek is goed",
           "het is hier gezellig",
           "deze weg is lang"),
    "pl": (
           "ta książka jest ciekawa",
           "ten kolor jest ładny",
           "ta zupa jest smaczna",
           "ta muzyka jest dobra",
           "tu jest przytulnie",
           "ta droga jest długa"),
}

РАМКИ = {
    "ru": dict(вопрос="{у} — это факт или мнение?",
               факт="факт: это можно проверить.",
               мнение="мнение: у другого человека оно может быть другим."),
    "en": dict(вопрос="{у} — is that a fact or an opinion?",
               факт="a fact: it can be checked.",
               мнение="an opinion: another person may have a different one."),
    "de": dict(вопрос="{у} — ist das eine Tatsache oder eine Meinung?",
               факт="eine Tatsache: das lässt sich prüfen.",
               мнение="eine Meinung: ein anderer Mensch kann eine andere haben."),
    "fr": dict(вопрос="{у} — est-ce un fait ou une opinion ?",
               факт="un fait : cela peut être vérifié.",
               мнение="une opinion : une autre personne peut en avoir une autre."),
    "es": dict(вопрос="{у} — ¿es un hecho o una opinión?",
               факт="un hecho: eso se puede comprobar.",
               мнение="una opinión: otra persona puede tener otra."),
    "it": dict(вопрос="{у} — è un fatto o un'opinione?",
               факт="un fatto: si può verificare.",
               мнение="un'opinione: un'altra persona può averne un'altra."),
    "pt": dict(вопрос="{у} — é um facto ou uma opinião?",
               факт="um facto: isso pode ser verificado.",
               мнение="uma opinião: outra pessoa pode ter outra."),
    "nl": dict(вопрос="{у} — is dat een feit of een mening?",
               факт="een feit: dat kan gecontroleerd worden.",
               мнение="een mening: een ander mens kan een andere hebben."),
    "pl": dict(вопрос="{у} — czy to fakt, czy opinia?",
               вопрос2="{у} — to fakt czy opinia?",   # вторая поверхность (полоса BESEDA-2)
               факт="fakt: to można sprawdzić.",
               мнение="opinia: inny człowiek może mieć inną."),
}

ЯЗЫКИ = tuple(РАМКИ)

# ТРЕТЬЯ ФОРМА: ФАКТ И МНЕНИЕ РЯДОМ, В ОДНОЙ СТРОКЕ (09.09).
#
#     РАЗЛИЧИЕ ПОКУПАЕТСЯ ПАРОЙ, А НЕ ДВУМЯ СТРАНИЦАМИ ПОРОЗНЬ. Дом учит отличать факт от
#     мнения — и показывал их врозь, каждое своей страницей. Пара ставит их рядом при одном
#     вопросе, и различие видно НЕ ИЗ ОТВЕТА, А ИЗ САМОГО ПОЛОЖЕНИЯ.
#
# ПОВОД ИЗМЕРЕН: прибор [СЛОВО ОДНАЖДЫ] держал двадцать восемь слов этого дома — сами оценочные
# слова (belle, bello, buena, gemütlich, gezellig, interesting), каждое показанное РОВНО РАЗ,
# ибо мнение стои́т одной страницей на язык. Вторая поверхность гасит их все.
#
# ВОПРОС ПРИ ПАРЕ ОБЯЗАТЕЛЕН, И ЭТО НЕ УКРАШЕНИЕ: род без вопросной поверхности есть долг
# прибора [ШИРОТА ВОПРОСА], и форма, закрывшая один долг ценою другого, ничего не закрыла.
ПАРА = {
    "ru": ("что тут факт, а что мнение?", "{ф} — это факт, а {м} — мнение."),
    "en": ("which is a fact and which is an opinion?", "{ф} — that is a fact, and {м} — that is an opinion."),
    "de": ("was ist hier eine Tatsache und was eine Meinung?", "{ф} — das ist eine Tatsache, und {м} — das ist eine Meinung."),
    "fr": ("qu'est-ce qui est un fait et qu'est-ce qui est une opinion ?", "{ф} — c'est un fait, et {м} — c'est une opinion."),
    "es": ("¿qué es un hecho y qué es una opinión?", "{ф} — eso es un hecho, y {м} — eso es una opinión."),
    "it": ("che cosa è un fatto e che cosa è un'opinione?", "{ф} — questo è un fatto, e {м} — questa è un'opinione."),
    "pt": ("o que é um facto e o que é uma opinião?", "{ф} — isso é um facto, e {м} — isso é uma opinião."),
    "nl": ("wat is een feit en wat is een mening?", "{ф} — dat is een feit, en {м} — dat is een mening."),
    "pl": ("co jest faktem, a co opinią?", "{ф} — to jest fakt, a {м} — to jest opinia."),
}

ФОРМЫ = ("факт", "мнение")

for _яз in ЯЗЫКИ:
    assert _яз in W.ЯЗЫКИ, _яз
    assert len(МНЕНИЯ[_яз]) == len(МНЕНИЯ["ru"]), _яз
    assert len(W.ФАКТЫ[_яз]) >= ФАКТОВ, _яз


def утверждение(язык, форма, i):
    """Само утверждение: факт — у соседа, мнение — своё."""
    if форма == "факт":
        return W.ФАКТЫ[язык][i % ФАКТОВ][0]
    return МНЕНИЯ[язык][i % len(МНЕНИЯ[язык])]


def страница(язык, форма, i, поверхность="вопрос"):
    я = РАМКИ[язык]
    return f"{я[поверхность].format(у=утверждение(язык, форма, i))} {я[форма]}"


def страница_пары(язык, i):
    """Факт и мнение рядом при одном вопросе."""
    воп, отв = ПАРА[язык]
    ф = утверждение(язык, "факт", i)
    м = утверждение(язык, "мнение", i)
    return f"{воп} {отв.format(ф=ф, м=м)}"


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for форма in ФОРМЫ:
            for i in range(ФАКТОВ if форма == "факт" else len(МНЕНИЯ[язык])):
                for поверхность in ("вопрос", "вопрос2"):
                    if поверхность in РАМКИ[язык]:
                        вон[страница(язык, форма, i, поверхность)] = (язык, форма)
        for i in range(min(ФАКТОВ, len(МНЕНИЯ[язык]))):
            вон[страница_пары(язык, i)] = (язык, "пара")
    return вон


ПОКАЗЫ = _показы()


def _хвосты():
    """Полный образец рамки: дыра утверждения — ОДНА клауза, а не «что угодно».

    Проба «начинается головой и кончается хвостом» пропускала удвоенный показ:
    голова на месте, хвост на месте, а между ними две страницы. Прибор ЛОВУШКИ
    НАЧАЛА поймал это на всех сорока пробах. Дыра «[^.?!]+» держит дом в его
    собственной строке: подмена утверждения ловится по-прежнему, речь соседа
    после точки — не его дело (М-172).
    """
    вон = []
    for яз, я in РАМКИ.items():
        for форма in ФОРМЫ:
            for поверхность in ("вопрос", "вопрос2"):
                if поверхность not in я:
                    continue
                рамка = я[поверхность].replace("{у}", "\x00") + " " + я[форма]
                вон.append(re.compile(re.escape(рамка).replace("\x00", "[^.?!]+")))
    return tuple(вон)


_РАМКИ_ЦЕЛИКОМ = _хвосты()


def судить(строка):
    """Подсудно лишь то, что совпало с рамкой ЦЕЛИКОМ (М-180-f2).

    Первая проба брала подсудным всё, и прибор чужой рамки поймал захват: этот
    дом звал ложью 54 показа дома отклика и 58 показов дома поспешности. Суд
    мира был сужен с рождения, а функция дома — нет; открытая функция, судящая
    всё, есть ловушка для следующего, кто её позовёт.
    """
    с = строка.strip()
    if not с:
        return False, False
    if not any(о.fullmatch(с) for о in _РАМКИ_ЦЕЛИКОМ):
        return False, False
    return True, с in ПОКАЗЫ


def main():
    поймано = 0
    for язык in ЯЗЫКИ:
        print(f"  {язык}: {страница(язык, 'факт', 0)}")
        print(f"      {страница(язык, 'мнение', 0)}")
        я = РАМКИ[язык]
        # МУТАНТЫ: мнение, названное фактом; факт, названный мнением; чужое
        # утверждение, объявленное фактом (соседу оно фактом не объявлено)
        мутанты = (f"{я['вопрос'].format(у=МНЕНИЯ[язык][0])} {я['факт']}",
                   f"{я['вопрос'].format(у=W.ФАКТЫ[язык][0][0])} {я['мнение']}",
                   f"{я['вопрос'].format(у=W.ФАКТЫ[язык][6][0])} {я['факт']}")
        for м in мутанты:
            судимо, истинно = судить(м)
            поймано += 1 if (судимо and not истинно) else 0
    print(f"  мутантов поймано: {поймано} из {3 * len(ЯЗЫКИ)}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, фактов {ФАКТОВ}, "
          f"мнений {len(МНЕНИЯ['ru'])})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
