#!/usr/bin/env python3
"""THE HOUSE OF TRANSLATION — «как будет «кот» по-английски? cat.», «how do you say
"thank you" in french? merci.» in nine languages, each into each.

Born from the eighth band of conversation (BESEDA-8, 06.09): the organism speaks
nine languages and had never been asked to carry a word from one into another.
The words are the letters house's words (tools/letters.py — eight plain words,
declared aligned across the nine languages), the phrases are the dialogue
house's first thanks and first greeting (tools/dialogueforms.py); this house
declares only how each language NAMES the others («по-английски», «in
russian», «auf Englisch», «en anglais») and the two frames. The court reads the
same tables: the answer must be the same word or phrase in the named language.
The world is CLOSED.

    python3 tools/translateforms.py    # self-check with mutants
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import dialogueforms as D  # noqa: E402
import letters as L  # noqa: E402

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")

# how language X names language Y (the adverbial / prepositional phrase of the question)
ИМЕНА = {
    "ru": dict(ru="по-русски", en="по-английски", de="по-немецки", fr="по-французски", es="по-испански", it="по-итальянски",
               pt="по-португальски", nl="по-нидерландски", pl="по-польски"),
    "en": dict(ru="in russian", en="in english", de="in german", fr="in french", es="in spanish", it="in italian",
               pt="in portuguese", nl="in dutch", pl="in polish"),
    "de": dict(ru="auf Russisch", en="auf Englisch", de="auf Deutsch", fr="auf Französisch", es="auf Spanisch", it="auf Italienisch",
               pt="auf Portugiesisch", nl="auf Niederländisch", pl="auf Polnisch"),
    "fr": dict(ru="en russe", en="en anglais", de="en allemand", fr="en français", es="en espagnol", it="en italien",
               pt="en portugais", nl="en néerlandais", pl="en polonais"),
    "es": dict(ru="en ruso", en="en inglés", de="en alemán", fr="en francés", es="en español", it="en italiano",
               pt="en portugués", nl="en neerlandés", pl="en polaco"),
    "it": dict(ru="in russo", en="in inglese", de="in tedesco", fr="in francese", es="in spagnolo", it="in italiano",
               pt="in portoghese", nl="in olandese", pl="in polacco"),
    "pt": dict(ru="em russo", en="em inglês", de="em alemão", fr="em francês", es="em espanhol", it="em italiano",
               pt="em português", nl="em neerlandês", pl="em polaco"),
    "nl": dict(ru="in het Russisch", en="in het Engels", de="in het Duits", fr="in het Frans", es="in het Spaans", it="in het Italiaans",
               pt="in het Portugees", nl="in het Nederlands", pl="in het Pools"),
    "pl": dict(ru="po rosyjsku", en="po angielsku", de="po niemiecku", fr="po francusku", es="po hiszpańsku", it="po włosku",
               pt="po portugalsku", nl="po niderlandzku", pl="po polsku"),
}
# the two frames: a word, and a phrase (what one SAYS); {w} the word in the quotes of
# the asking language, {L} the named language, {t} the answer
РАМКИ = {
    "ru": (("как будет «{w}» {L}?", "{t}."), ("как сказать «{w}» {L}?", "{t}.")),
    "en": (('what is "{w}" {L}?', "{t}."), ('how do you say "{w}" {L}?', "{t}.")),
    "de": (("was heißt „{w}“ {L}?", "{t}."), ("wie sagt man „{w}“ {L}?", "{t}.")),
    "fr": (("comment dit-on « {w} » {L} ?", "{t}."), ("comment dit-on « {w} » {L} ?", "{t}.")),
    "es": (("¿cómo se dice «{w}» {L}?", "{t}."), ("¿cómo se dice «{w}» {L}?", "{t}.")),
    "it": (("come si dice «{w}» {L}?", "{t}."), ("come si dice «{w}» {L}?", "{t}.")),
    "pt": (("como se diz «{w}» {L}?", "{t}."), ("como se diz «{w}» {L}?", "{t}.")),
    "nl": (('wat is "{w}" {L}?', "{t}."), ('hoe zeg je "{w}" {L}?', "{t}.")),
    "pl": (("jak jest „{w}” {L}?", "{t}."), ("jak powiedzieć „{w}” {L}?", "{t}.")),
}


def _слова(язык):
    return L.ЯЗЫКИ[язык]["слова"]


def _фразы(язык):
    я = D.ЯЗЫКИ[язык]["зачины"]
    return (я[D.БЛАГОДАРНОСТЬ][0], я[D.ПРИВЕТ][0], я[D.ПРОЩАНИЕ][0])


for _яз in ЯЗЫКИ:
    assert len(_слова(_яз)) == len(_слова("ru")), (_яз, "слова не выровнены")
assert len(ЯЗЫКИ) == 9


def страница(язык, цель, вид, i):
    """вид 0 — a word (the letters house), 1 — a phrase (the dialogue house)."""
    воп, отв = РАМКИ[язык][вид]
    w = (_слова(язык) if вид == 0 else _фразы(язык))[i]
    t = (_слова(цель) if вид == 0 else _фразы(цель))[i]
    return f"{воп.format(w=w, L=ИМЕНА[язык][цель])} {отв.format(t=t)}"


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for цель in ЯЗЫКИ:
            if цель == язык:
                continue
            for вид, ряд in ((0, _слова(язык)), (1, _фразы(язык))):
                for i in range(len(ряд)):
                    вон[страница(язык, цель, вид, i)] = (язык, "слово" if вид == 0 else "фраза")
    return вон


ПОКАЗЫ = _показы()


def _образцы():
    вон = []
    alt = lambda слова: "(" + "|".join(re.escape(с) for с in sorted(set(слова), key=len, reverse=True)) + ")"
    for язык in ЯЗЫКИ:
        for вид in (0, 1):
            воп, отв = РАМКИ[язык][вид]
            свои = _слова(язык) if вид == 0 else _фразы(язык)
            все = [x for я in ЯЗЫКИ for x in (_слова(я) if вид == 0 else _фразы(я))]
            узор = re.escape(воп + " " + отв)
            узор = узор.replace(re.escape("{w}"), "(?P<w>" + alt(свои)[1:]).replace(re.escape("{L}"), "(?P<L>" + alt(ИМЕНА[язык].values())[1:])
            узор = узор.replace(re.escape("{t}"), "(?P<t>" + alt(все)[1:])
            вон.append((re.compile("^" + узор + "$"), язык, вид))
    return вон


ОБРАЗЦЫ = _образцы()


def судить(строка):
    """(судимо, истинно): the answer is the same word or phrase in the named language."""
    с = строка.strip()
    for образ, язык, вид in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        г = м.groupdict()
        цель = next((я for я, имя in ИМЕНА[язык].items() if имя == г["L"]), None)
        if цель is None or цель == язык:
            return True, False
        свои = _слова(язык) if вид == 0 else _фразы(язык)
        чужие = _слова(цель) if вид == 0 else _фразы(цель)
        return True, г["w"] in свои and г["t"] == чужие[свои.index(г["w"])]
    return False, False


def _самопроверка():
    for показ, (язык, вид) in ПОКАЗЫ.items():
        assert судить(показ) == (True, True), (язык, вид, показ)
    мутанты = 0
    for язык in ЯЗЫКИ:
        цель = "en" if язык != "en" else "ru"
        с = страница(язык, цель, 0, 0)
        # MUTANT: the word of another index; the word of another language
        битая = с[:c_] + _слова(цель)[1] + "." if (c_ := с.rfind(" ") + 1) else с
        assert судить(битая) == (True, False), битая
        мутанты += 1
    for язык in ("ru", "en", "de", "pl"):
        print("  ", страница(язык, "en" if язык != "en" else "ru", 0, 0)); print("  ", страница(язык, "fr", 1, 0))
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, слов {len(_слова('ru'))}, фраз {len(_фразы('ru'))})")


if __name__ == "__main__":
    _самопроверка()
