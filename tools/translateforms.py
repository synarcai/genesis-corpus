#!/usr/bin/env python3
"""THE HOUSE OF TRANSLATION — «как будет «кот» по-английски? cat.», «how do you say
"thank you" in french? merci.» in nine languages, each into each.

Born from the eighth band of conversation (BESEDA-8, 06.09): the organism speaks
nine languages and had never been asked to carry a word from one into another.
The words are THIS HOUSE'S OWN table, declared by CONCEPT and not by place (07.09:
the words were taken from the letters house by INDEX, and the Russian list stood one
place apart — 75 false translations shipped in the свод), the phrases are the dialogue
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
import concepts as C  # noqa: E402

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


# СЛОВАРЬ ПЕРЕВОДА ОБЪЯВЛЕН ПОНЯТИЯМИ, А НЕ МЕСТАМИ (07.09) — и это починка лжи, которая
# лежала в своде и которую не ловил никто.
#
# Дом брал слова у ДОМА БУКВ и спаривал их ПО НОМЕРУ МЕСТА, проверяя при этом одно:
#
#     assert len(_слова(_яз)) == len(_слова("ru")), (_яз, "слова не выровнены")
#
#     УТВЕРЖДЕНИЕ О ДЛИНЕ СПИСКА НЕ ЕСТЬ УТВЕРЖДЕНИЕ О ЕГО ПОРЯДКЕ. Утверждение стояло,
#     звалось «слова не выровнены» и считало ДЛИНУ. Так объявление лгало вдвойне — и
#     делом, и именем.
#
# Восемь языков были согласны между собой (cat, dog, house, water, bread, sun, hand,
# table), а русский стоял иначе — «кот, дом, вода, хлеб, солнце, окно, рука, стол»: в нём
# нет собаки и есть окно, отчего места 1…5 сдвинулись на одно. ЗАМЕР по лежащему миру
# (792 строки): верных по смыслу 437, ЛОЖНЫХ 75 — «как будет «хлеб» по-французски? eau»,
# «как будет «солнце» по-немецки? Brot», «как будет «вода» по-испански? casa». Ни один суд
# этого не ловил: перевод не пересчитывается из строки, и палата молчала по существу.
#
# ДВА ДОМА, ЧИТАЮЩИЕ ОДИН СПИСОК, ТРЕБУЮТ ОТ НЕГО РАЗНОГО. Дому букв нужны РАЗНЫЕ ДЛИНЫ
# слов (иначе счёт букв отвечается угадыванием), дому перевода — ВЫРАВНИВАНИЕ ПО СМЫСЛУ.
# Одному списку обоих не дать, и попытка дать кончается ложью в том доме, который спросили
# позже. Потому список здесь СВОЙ, объявленный понятиями.
# СЛОВА БЕРУТСЯ У ОБЩЕЙ ТАБЛИЦЫ ПОНЯТИЙ (07.09, `tools/concepts.py`). Своя таблица дома
# прожила час: она чинила ложь, но была ЧЕТВЁРТЫМ словарём корпуса — у пакетов девять своих,
# у домов свои, и ни один ключ не говорил, что «book», «libro» и «книга» суть одно.
#
#     СЛОВАРЬ, ЖИВУЩИЙ В ДОМЕ, ЕСТЬ СЛОВАРЬ ЭТОГО ДОМА. Четыре дома напишут четыре
#     несогласных словаря, и разойдутся они молча — как разошлись списки букв и перевода.
#
# Понятия, какие берёт этот дом, названы ПО КЛЮЧУ, а не по английскому слову: ключ есть имя
# понятия, английское — один из девяти столбцов.
ПОНЯТИЯ_ДОМА = ("c36", "c37", "c54", "c62", "c68", "c69", "c70", "c52")
СЛОВАРЬ = tuple((к, C.ПОНЯТИЯ[к][1]) for к in ПОНЯТИЯ_ДОМА)
# УТВЕРЖДЕНИЕ ПО СУЩЕСТВУ: у всякого понятия есть слово на КАЖДОМ из девяти языков, и
# каждое понятие названо. Это и есть выравнивание — не длина, а полнота по понятию.
for _пон, _ряд in СЛОВАРЬ:
    assert set(_ряд) == set(ЯЗЫКИ), (_пон, "понятие не полно по языкам")
assert len({п for п, _ in СЛОВАРЬ}) == len(СЛОВАРЬ), "понятие названо дважды"


def _слова(язык):
    return tuple(ряд[язык] for _пон, ряд in СЛОВАРЬ)


def _фразы(язык):
    я = D.ЯЗЫКИ[язык]["зачины"]
    return (я[D.БЛАГОДАРНОСТЬ][0], я[D.ПРИВЕТ][0], я[D.ПРОЩАНИЕ][0])


# (утверждение о ДЛИНЕ списков снято: оно звалось «слова не выровнены» и выравнивания не
# проверяло; ныне выравнивание утверждается выше — по полноте каждого ПОНЯТИЯ.)
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
    alt = lambda слова: "(" + "|".join(re.escape(с) for с in sorted(set(слова), key=lambda с: (-len(с), с))) + ")"
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
