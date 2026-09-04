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
               факт="fakt: to można sprawdzić.",
               мнение="opinia: inny człowiek może mieć inną."),
}

ЯЗЫКИ = tuple(РАМКИ)
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


def страница(язык, форма, i):
    я = РАМКИ[язык]
    return f"{я['вопрос'].format(у=утверждение(язык, форма, i))} {я[форма]}"


def _показы():
    return {страница(язык, форма, i): (язык, форма)
            for язык in ЯЗЫКИ for форма in ФОРМЫ
            for i in range(ФАКТОВ if форма == "факт" else len(МНЕНИЯ[язык]))}


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
            рамка = я["вопрос"].replace("{у}", "\x00") + " " + я[форма]
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
