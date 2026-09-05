#!/usr/bin/env python3
"""THE HOUSE OF TIME UNITS — «сколько минут в двух часах? 120: 2 × 60 = 120.» in nine languages.

Born from the ninth band of conversation (BESEDA-9, 06.09): «how many minutes
are there in 2 hours?» lived only in the English units world. Four conversions
(hour → minutes, minute → seconds, week → days, day → hours), each asked for two
to five of the larger unit; the count of the larger unit stands in WORDS for
two, three and four (in the case the phrase needs — «в двух часах», «in zwei
Stunden», «w dwóch godzinach») and in digits otherwise; the smaller unit's
count form is the pack's (count_agreement). The court recomputes the product
and both forms. The world is CLOSED.

    python3 tools/timeunits.py    # self-check with mutants
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import langpack  # noqa: E402

_ПАКЕТЫ = pathlib.Path(__file__).resolve().parent / "langpacks"

# the one fact: (larger unit, smaller unit, factor)
ПЕРЕВОДЫ = (("час", "минута", 60), ("минута", "секунда", 60), ("неделя", "день", 7), ("сутки", "час", 24))

# per language: the larger unit in the case after the preposition, by count form
# (one/few/many, the pack's names), the small unit's count forms (genitive plural
# in the question: «сколько минут»), the numerals in words for 2..4 in the case
# the phrase needs, and the frame
ЯЗЫКИ = {
    "ru": dict(большие={"час": dict(few="часах", many="часах"), "минута": dict(few="минутах", many="минутах"),
                        "неделя": dict(few="неделях", many="неделях"), "сутки": dict(few="сутках", many="сутках")},
               малые={"минута": dict(вопрос="минут", one="минута", few="минуты", many="минут"), "секунда": dict(вопрос="секунд", one="секунда", few="секунды", many="секунд"),
                      "день": dict(вопрос="дней", one="день", few="дня", many="дней"), "час": dict(вопрос="часов", one="час", few="часа", many="часов")},
               словом={2: "двух", 3: "трёх", 4: "четырёх"},
               рамка=("сколько {М} в {k} {Б}?", "{v}: {k_} × {f} = {v}.")),
    "en": dict(большие={"час": dict(many="hours"), "минута": dict(many="minutes"), "неделя": dict(many="weeks"), "сутки": dict(many="days")},
               малые={"минута": dict(вопрос="minutes", one="minute", many="minutes"), "секунда": dict(вопрос="seconds", one="second", many="seconds"),
                      "день": dict(вопрос="days", one="day", many="days"), "час": dict(вопрос="hours", one="hour", many="hours")},
               словом={2: "two", 3: "three", 4: "four"},
               рамка=("how many {М} are there in {k} {Б}?", "{v}: {k_} × {f} = {v}.")),
    "de": dict(рамка2=("wie viele {М} haben {k} {Б2}?", "{v}: {k_} × {f} = {v}."),
               большие2={"час": dict(many="Stunden"), "минута": dict(many="Minuten"), "неделя": dict(many="Wochen"), "сутки": dict(many="Tage")},
               большие={"час": dict(many="Stunden"), "минута": dict(many="Minuten"), "неделя": dict(many="Wochen"), "сутки": dict(many="Tagen")},
               малые={"минута": dict(вопрос="Minuten", one="Minute", many="Minuten"), "секунда": dict(вопрос="Sekunden", one="Sekunde", many="Sekunden"),
                      "день": dict(вопрос="Tage", one="Tag", many="Tage"), "час": dict(вопрос="Stunden", one="Stunde", many="Stunden")},
               словом={2: "zwei", 3: "drei", 4: "vier"},
               рамка=("wie viele {М} sind in {k} {Б}?", "{v}: {k_} × {f} = {v}.")),
    "fr": dict(большие={"час": dict(many="heures"), "минута": dict(many="minutes"), "неделя": dict(many="semaines"), "сутки": dict(many="jours")},
               малые={"минута": dict(вопрос="minutes", one="minute", many="minutes"), "секунда": dict(вопрос="secondes", one="seconde", many="secondes"),
                      "день": dict(вопрос="jours", one="jour", many="jours"), "час": dict(вопрос="heures", one="heure", many="heures")},
               словом={2: "deux", 3: "trois", 4: "quatre"},
               рамка=("combien de {М} y a-t-il dans {k} {Б} ?", "{v} : {k_} × {f} = {v}.")),
    "es": dict(рамка2=("¿cuántos {М} tienen {k} {Б2}?", "{v}: {k_} × {f} = {v}."),
               большие2={"час": dict(many="horas"), "минута": dict(many="minutos"), "неделя": dict(many="semanas"), "сутки": dict(many="días")},
               большие={"час": dict(many="horas"), "минута": dict(many="minutos"), "неделя": dict(many="semanas"), "сутки": dict(many="días")},
               малые={"минута": dict(вопрос="minutos", one="minuto", many="minutos"), "секунда": dict(вопрос="segundos", one="segundo", many="segundos"),
                      "день": dict(вопрос="días", one="día", many="días"), "час": dict(вопрос="horas", one="hora", many="horas")},
               словом={2: "dos", 3: "tres", 4: "cuatro"},
               рамка=("¿cuántos {М} hay en {k} {Б}?", "{v}: {k_} × {f} = {v}.")),
    "it": dict(рамка2=("quanti {М} hanno {k} {Б2}?", "{v}: {k_} × {f} = {v}."),
               большие2={"час": dict(many="ore"), "минута": dict(many="minuti"), "неделя": dict(many="settimane"), "сутки": dict(many="giorni")},
               большие={"час": dict(many="ore"), "минута": dict(many="minuti"), "неделя": dict(many="settimane"), "сутки": dict(many="giorni")},
               малые={"минута": dict(вопрос="minuti", one="minuto", many="minuti"), "секунда": dict(вопрос="secondi", one="secondo", many="secondi"),
                      "день": dict(вопрос="giorni", one="giorno", many="giorni"), "час": dict(вопрос="ore", one="ora", many="ore")},
               словом={2: "due", 3: "tre", 4: "quattro"},
               рамка=("quanti {М} ci sono in {k} {Б}?", "{v}: {k_} × {f} = {v}.")),
    "pt": dict(рамка2=("quantos {М} têm {k} {Б2}?", "{v}: {k_} × {f} = {v}."),
               большие2={"час": dict(many="horas"), "минута": dict(many="minutos"), "неделя": dict(many="semanas"), "сутки": dict(many="dias")},
               большие={"час": dict(many="horas"), "минута": dict(many="minutos"), "неделя": dict(many="semanas"), "сутки": dict(many="dias")},
               малые={"минута": dict(вопрос="minutos", one="minuto", many="minutos"), "секунда": dict(вопрос="segundos", one="segundo", many="segundos"),
                      "день": dict(вопрос="dias", one="dia", many="dias"), "час": dict(вопрос="horas", one="hora", many="horas")},
               словом={2: "duas", 3: "três", 4: "quatro"},
               рамка=("quantos {М} há em {k} {Б}?", "{v}: {k_} × {f} = {v}.")),
    "nl": dict(рамка2=("hoeveel {М} hebben {k} {Б2}?", "{v}: {k_} × {f} = {v}."),
               большие2={"час": dict(many="uur"), "минута": dict(many="minuten"), "неделя": dict(many="weken"), "сутки": dict(many="dagen")},
               большие={"час": dict(many="uur"), "минута": dict(many="minuten"), "неделя": dict(many="weken"), "сутки": dict(many="dagen")},
               малые={"минута": dict(вопрос="minuten", one="minuut", many="minuten"), "секунда": dict(вопрос="seconden", one="seconde", many="seconden"),
                      "день": dict(вопрос="dagen", one="dag", many="dagen"), "час": dict(вопрос="uur", one="uur", many="uur")},
               словом={2: "twee", 3: "drie", 4: "vier"},
               рамка=("hoeveel {М} zitten er in {k} {Б}?", "{v}: {k_} × {f} = {v}.")),
    "pl": dict(рамка2=("ile {М} mają {k} {Б2}?", "{v}: {k_} × {f} = {v}."),
               большие2={"час": dict(few="godziny", many="godzin"), "минута": dict(few="minuty", many="minut"), "неделя": dict(few="tygodnie", many="tygodni"), "сутки": dict(few="doby", many="dób")},
               словом2={"час": {2: "dwie", 3: "trzy", 4: "cztery"}, "минута": {2: "dwie", 3: "trzy", 4: "cztery"}, "неделя": {2: "dwa", 3: "trzy", 4: "cztery"}, "сутки": {2: "dwie", 3: "trzy", 4: "cztery"}},
               большие={"час": dict(few="godzinach", many="godzinach"), "минута": dict(few="minutach", many="minutach"),
                        "неделя": dict(few="tygodniach", many="tygodniach"), "сутки": dict(few="dobach", many="dobach")},
               малые={"минута": dict(вопрос="minut", one="minuta", few="minuty", many="minut"), "секунда": dict(вопрос="sekund", one="sekunda", few="sekundy", many="sekund"),
                      "день": dict(вопрос="dni", one="dzień", few="dni", many="dni"), "час": dict(вопрос="godzin", one="godzina", few="godziny", many="godzin")},
               словом={2: "dwóch", 3: "trzech", 4: "czterech"},
               рамка=("ile {М} jest w {k} {Б}?", "{v}: {k_} × {f} = {v}.")),
}
СЧЁТ = (2, 3, 4, 5)
_ПАКЕТ = {}


def _пакет(язык):
    if язык not in _ПАКЕТ:
        _ПАКЕТ[язык] = json.loads((_ПАКЕТЫ / f"{язык}.json").read_text(encoding="utf-8"))
    return _ПАКЕТ[язык]


def форма(язык, таблица, k):
    формы = [ф for ф in ("one", "few", "many") if ф in таблица]
    i = langpack.count_form_index(_пакет(язык), {"forms": формы}, k)
    return таблица[формы[i]]


def _слово(язык, б, k, рамка):
    я = ЯЗЫКИ[язык]
    if рамка == "рамка2" and "словом2" in я:
        return я["словом2"][б].get(k)
    return я["словом"].get(k)


def страница(язык, i, k, словом=True, рамка="рамка"):
    """The k of the larger unit in words (2..4) or in digits; рамка2 — the «have»
    construction with the larger unit in the nominative."""
    я = ЯЗЫКИ[язык]; б, м, f = ПЕРЕВОДЫ[i]
    v = k * f
    сл = _слово(язык, б, k, рамка)
    K = сл if словом and сл else str(k)
    большие = я["большие2"] if рамка == "рамка2" else я["большие"]
    п = dict(М=я["малые"][м]["вопрос"], k=K, Б=форма(язык, я["большие"][б], k), Б2=форма(язык, большие[б], k), v=v, k_=k, f=f)
    воп, отв = я[рамка]
    return f"{воп.format(**п)} {отв.format(**п)}"


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for i in range(len(ПЕРЕВОДЫ)):
            for k in СЧЁТ:
                for рамка in (("рамка", "рамка2") if "рамка2" in ЯЗЫКИ[язык] else ("рамка",)):
                    вон[страница(язык, i, k, True, рамка)] = (язык, "единицы")
                    вон[страница(язык, i, k, False, рамка)] = (язык, "единицы")
    return вон


ПОКАЗЫ = _показы()


def _образцы():
    вон = []
    alt = lambda слова: "(" + "|".join(re.escape(с) for с in sorted(set(слова), key=len, reverse=True)) + ")"
    for язык, я in ЯЗЫКИ.items():
        слова = list(я["словом"].values()) + [с for т in я.get("словом2", {}).values() for с in т.values()]
        дыры = {"М": "(?P<М>" + alt(м["вопрос"] for м in я["малые"].values())[1:],
                "k": r"(?P<k>\d+|" + alt(слова)[1:],
                "Б": "(?P<Б>" + alt(ф for б in я["большие"].values() for ф in б.values())[1:],
                "Б2": "(?P<Б2>" + alt(ф for б in я.get("большие2", {}).values() for ф in б.values())[1:] if "большие2" in я else "",
                "v": r"(?P<v>\d+)", "k_": r"(?P<k_>\d+)", "f": r"(?P<f>\d+)"}
        for рамка in (("рамка", "рамка2") if "рамка2" in я else ("рамка",)):
            видены, куски = set(), []
            for кусок in re.split(r"(\{[^}]+\})", " ".join(я[рамка])):
                if кусок.startswith("{"):
                    имя = кусок[1:-1]
                    куски.append(f"(?P={имя})" if имя in видены else дыры[имя]); видены.add(имя)
                else:
                    куски.append(re.escape(кусок))
            вон.append((re.compile("^" + "".join(куски) + "$"), язык, рамка))
    return вон


ОБРАЗЦЫ = _образцы()


def судить(строка):
    """(судимо, истинно): the units are a declared pair, the count in words is the digit's,
    the larger unit's form is the pack's, and the product holds."""
    с = строка.strip()
    for образ, язык, рамка in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        я = ЯЗЫКИ[язык]; г = м.groupdict()
        k, f, v = int(г["k_"]), int(г["f"]), int(г["v"])
        пара = next(((б, мл, ф) for б, мл, ф in ПЕРЕВОДЫ if я["малые"][мл]["вопрос"] == г["М"] and ф == f), None)
        if пара is None:
            return True, False
        б = пара[0]
        слово_k = _слово(язык, б, k, рамка)
        if not (г["k"] == str(k) or г["k"] == слово_k):
            return True, False
        большие = я["большие2"] if рамка == "рамка2" else я["большие"]
        ключ = "Б2" if рамка == "рамка2" else "Б"
        return True, v == k * f and г[ключ] == форма(язык, большие[б], k)
    return False, False


def _самопроверка():
    for показ, (язык, _) in ПОКАЗЫ.items():
        assert судить(показ) == (True, True), (язык, показ)
    мутанты = 0
    for язык in ЯЗЫКИ:
        с = страница(язык, 0, 2)
        битая = с.replace(" 120", " 130").replace("= 120", "= 130")
        assert судить(битая) == (True, False), битая
        битая = с.replace("× 60", "× 7").replace("120", "14")   # the factor of another pair
        assert судить(битая) == (True, False), битая
        мутанты += 2
    for язык in ("ru", "en", "pl", "de"):
        print("  ", страница(язык, 0, 2)); print("  ", страница(язык, 2, 2)); print("  ", страница(язык, 1, 5))
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, переводов {len(ПЕРЕВОДЫ)})")


if __name__ == "__main__":
    _самопроверка()
