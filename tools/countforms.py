#!/usr/bin/env python3
"""THE HOUSE OF COUNTED UNITS — not to be confused with tools/unitforms.py,
which names units for CONVERSIONS in eight languages; this one says one unit
with many counts in one frame.

THE HOUSE OF COUNTED UNITS — «1 day, 2 days, 5 days» said in ONE frame.

32's tomograph of the rate (03.09): the market of count forms pairs «day» with
«days» only inside ONE frame carrying at least three different numbers. The
corpus said «worked on 1 day» in one world and «how much in 8 days» in another,
and the pair was never bought — so the rate «cynthia collects 10 eggs every day.
how many eggs in 8 days?» stayed mute while «in 8 day» answered.

This house says the unit with its counts in one show:

    the trip takes 1 day. the trip takes 2 days. the trip takes 3 days.
    the trip takes 5 days. the trip takes 10 days.

Every form is DECLARED, never derived: English and German name two forms, Russian
names three (one, two-to-four, five-and-more), and the frames of each language are
its own. The counts are the same everywhere — one, two, three, five, ten — because
the pair is bought from DIFFERENT numbers in one frame, and five numbers are more
than the three the market asks for.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

СЧЁТЫ = (1, 2, 3, 5, 10)

ЯЗЫКИ = {
    "en": dict(
        рамки=("the trip takes {n} {Е}.", "the meeting lasts {n} {Е}.",
               "the work took {n} {Е}.", "the child waited {n} {Е}."),
        единицы=(("day", "days"), ("hour", "hours"), ("week", "weeks"),
                 ("month", "months"), ("year", "years"), ("minute", "minutes")),
    ),
    "ru": dict(
        рамки=("поездка длится {n} {Е}.", "встреча длится {n} {Е}.",
               "работа заняла {n} {Е}.", "ребёнок ждал {n} {Е}."),
        единицы=(("день", "дня", "дней"), ("час", "часа", "часов"),
                 ("неделя", "недели", "недель"), ("месяц", "месяца", "месяцев"),
                 ("год", "года", "лет"), ("минута", "минуты", "минут")),
    ),
    "de": dict(
        рамки=("die Reise dauert {n} {Е}.", "das Treffen dauert {n} {Е}.",
               "die Arbeit dauerte {n} {Е}.", "das Kind wartete {n} {Е}."),
        единицы=(("Tag", "Tage"), ("Stunde", "Stunden"), ("Woche", "Wochen"),
                 ("Monat", "Monate"), ("Jahr", "Jahre"), ("Minute", "Minuten")),
    ),
}


def форма(язык, единица, n):
    """The declared form of a unit beside its count.

    Russian chooses by the LAST digit under the teenage census — «21 день», but
    «11 дней» — and the choice is the same law the house of things obeys.
    """
    формы = ЯЗЫКИ[язык]["единицы"][единица]
    if len(формы) == 2:
        return формы[0] if n == 1 else формы[1]
    if n % 100 in range(11, 15):
        return формы[2]
    последняя = n % 10
    if последняя == 1:
        return формы[0]
    if последняя in (2, 3, 4):
        return формы[1]
    return формы[2]


def показ(язык, рамка, единица):
    """ONE SHOW: the same frame with every count, so the pair is bought here."""
    ш = ЯЗЫКИ[язык]["рамки"][рамка]
    return "\n".join(ш.format(n=n, Е=форма(язык, единица, n)) for n in СЧЁТЫ)


def _все():
    вон = {}
    for язык, я in ЯЗЫКИ.items():
        for рамка in range(len(я["рамки"])):
            for единица in range(len(я["единицы"])):
                for n in СЧЁТЫ:
                    строка = я["рамки"][рамка].format(n=n, Е=форма(язык, единица, n))
                    вон[строка] = (язык, рамка, единица, n)
    return вон


ВСЕ = _все()


def _образцы():
    вон = []
    for язык, я in ЯЗЫКИ.items():
        формы = sorted({ф for пара in я["единицы"] for ф in пара}, key=len, reverse=True)
        Е = "(?:" + "|".join(map(re.escape, формы)) + ")"
        for ш in я["рамки"]:
            вон.append(re.compile("^" + re.escape(ш).replace(r"\{n\}", r"\d+").replace(r"\{Е\}", Е) + "$"))
    return вон


ОБРАЗЦЫ = _образцы()


def судить(строка):
    """(судимо, истинно): a frame of this house with a form that does not agree
    with its count is a lie — «2 day», «5 дня», «1 Tage»."""
    с = строка.strip()
    if с in ВСЕ:
        return True, True
    for о in ОБРАЗЦЫ:
        if о.match(с):
            return True, False
    return False, False


def _проверка():
    для_показа = показ("ru", 0, 0)
    print(для_показа)
    плохих = [с for с in ВСЕ if судить(с) != (True, True)]
    мутанты = ["the trip takes 2 day.", "поездка длится 5 дня.", "die Reise dauert 1 Tage.",
               "поездка длится 1 дней."]
    поймано = [м for м in мутанты if судить(м) == (True, False)]
    print(f"строк дома: {len(ВСЕ)}, не признано: {len(плохих)}, "
          f"мутантов поймано: {len(поймано)} из {len(мутанты)}")


if __name__ == "__main__":
    _проверка()
