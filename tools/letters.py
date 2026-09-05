#!/usr/bin/env python3
"""THE HOUSE OF LETTERS — «how many letters are there in the word "cat"? 3: c, a, t.»
in nine languages.

Born from the fourth band of conversation (BESEDA-4, 05.09): «сколько букв в
слове «кот»?» was mute in all nine languages — the corpus counted goods,
sides and legs, but never the letters of a word. Every answer here is
RECOMPUTED by the court from the word itself: the count is the length, the
first and the last letter are the word's own; the ground of the count is
the word spelled out letter by letter. The word stands in the quotes of its
language («», "", „“, « »). Generator and court read one table; the world is
CLOSED — a line of it that no frame reads is a lie.

    python3 tools/letters.py    # self-check with mutants
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

# per language: eight plain words, and the three frames — the count with its
# spelling, the first letter, the last letter; {w} the word, {n} the count,
# {L} the letters «к, о, т», {l} one letter
ЯЗЫКИ = {
    "ru": dict(слова=("кот", "дом", "вода", "хлеб", "солнце", "окно", "рука", "стол"),
               букв=("сколько букв в слове «{w}»?", "{n}: {L}."),
               первая=("какая первая буква в слове «{w}»?", "«{l}»."),
               последняя=("какая последняя буква в слове «{w}»?", "«{l}»."),
               наоборот=("скажи слово «{w}» наоборот.", "«{r}».")),
    "en": dict(слова=("cat", "dog", "house", "water", "bread", "sun", "hand", "table"),
               букв=('how many letters are there in the word "{w}"?', "{n}: {L}."),
               первая=('what is the first letter of the word "{w}"?', '"{l}".'),
               последняя=('what is the last letter of the word "{w}"?', '"{l}".'),
               наоборот=('say the word "{w}" backwards.', '"{r}".')),
    "de": dict(слова=("Katze", "Hund", "Haus", "Wasser", "Brot", "Sonne", "Hand", "Tisch"),
               букв=("wie viele Buchstaben hat das Wort „{w}“?", "{n}: {L}."),
               первая=("was ist der erste Buchstabe des Wortes „{w}“?", "„{l}“."),
               последняя=("was ist der letzte Buchstabe des Wortes „{w}“?", "„{l}“."),
               наоборот=("sag das Wort „{w}“ rückwärts.", "„{r}“.")),
    "fr": dict(слова=("chat", "chien", "maison", "eau", "pain", "soleil", "main", "table"),
               букв=("combien de lettres y a-t-il dans le mot « {w} » ?", "{n} : {L}."),
               первая=("quelle est la première lettre du mot « {w} » ?", "« {l} »."),
               последняя=("quelle est la dernière lettre du mot « {w} » ?", "« {l} »."),
               наоборот=("dis le mot « {w} » à l'envers.", "« {r} ».")),
    "es": dict(слова=("gato", "perro", "casa", "agua", "pan", "sol", "mano", "mesa"),
               букв=("¿cuántas letras tiene la palabra «{w}»?", "{n}: {L}."),
               первая=("¿cuál es la primera letra de la palabra «{w}»?", "«{l}»."),
               последняя=("¿cuál es la última letra de la palabra «{w}»?", "«{l}»."),
               наоборот=("di la palabra «{w}» al revés.", "«{r}».")),
    "it": dict(слова=("gatto", "cane", "casa", "acqua", "pane", "sole", "mano", "tavolo"),
               букв=("quante lettere ha la parola «{w}»?", "{n}: {L}."),
               первая=("qual è la prima lettera della parola «{w}»?", "«{l}»."),
               последняя=("qual è l'ultima lettera della parola «{w}»?", "«{l}»."),
               наоборот=("di' la parola «{w}» al contrario.", "«{r}».")),
    "pt": dict(слова=("gato", "cão", "casa", "água", "pão", "sol", "mão", "mesa"),
               букв=("quantas letras tem a palavra «{w}»?", "{n}: {L}."),
               первая=("qual é a primeira letra da palavra «{w}»?", "«{l}»."),
               последняя=("qual é a última letra da palavra «{w}»?", "«{l}»."),
               наоборот=("diz a palavra «{w}» ao contrário.", "«{r}».")),
    "nl": dict(слова=("kat", "hond", "huis", "water", "brood", "zon", "hand", "tafel"),
               букв=('hoeveel letters heeft het woord "{w}"?', "{n}: {L}."),
               первая=('wat is de eerste letter van het woord "{w}"?', '"{l}".'),
               последняя=('wat is de laatste letter van het woord "{w}"?', '"{l}".'),
               наоборот=('zeg het woord "{w}" achterstevoren.', '"{r}".')),
    "pl": dict(слова=("kot", "pies", "dom", "woda", "chleb", "słońce", "ręka", "stół"),
               букв=("ile liter ma słowo „{w}”?", "{n}: {L}."),
               первая=("jaka jest pierwsza litera słowa „{w}”?", "„{l}”."),
               последняя=("jaka jest ostatnia litera słowa „{w}”?", "„{l}”."),
               наоборот=("powiedz słowo „{w}” od tyłu.", "„{r}”.")),
}
ФОРМЫ = ("букв", "первая", "последняя", "наоборот")

# THE WORD BACKWARDS (sixth band, 05.09) is a TASK, not a question — and a genus
# without a question surface is a debt of the width of asking; the question after
# the task is the one declared by the house of tasks, read here, not redeclared.
import taskforms as _T
ВОПРОС_ПОСЛЕ = _T.ВОПРОСЫ

for _яз, _я in ЯЗЫКИ.items():
    assert len(_я["слова"]) == len(set(_я["слова"])) == 8, _яз
    for _w in _я["слова"]:
        assert _w.isalpha(), (_яз, _w)


def _поля(w):
    return dict(w=w, n=len(w), L=", ".join(w), l=w[0], r=w[::-1])


def страница(язык, форма, w, вопросом=False):
    воп, отв = ЯЗЫКИ[язык][форма]
    п = _поля(w)
    if форма == "последняя":
        п["l"] = w[-1]
    между = f" {ВОПРОС_ПОСЛЕ[язык]}" if вопросом else ""
    return f"{воп.format(**п)}{между} {отв.format(**п)}"


def _показы():
    вон = {страница(язык, форма, w): (язык, форма)
           for язык, я in ЯЗЫКИ.items() for форма in ФОРМЫ for w in я["слова"]}
    for язык, я in ЯЗЫКИ.items():
        for w in я["слова"]:
            вон[страница(язык, "наоборот", w, вопросом=True)] = (язык, "наоборот")
    return вон


ПОКАЗЫ = _показы()

ДЫРЫ = {"w": r"(?P<w>[^\W\d_]+)", "n": r"(?P<n>\d+)", "L": r"(?P<L>[^\W\d_](?:, [^\W\d_])*)", "l": r"(?P<l>[^\W\d_])",
        "r": r"(?P<r>[^\W\d_]+)"}


def _образец(шаблон):
    куски = []
    for кусок in re.split(r"(\{[^}]+\})", шаблон):
        куски.append(ДЫРЫ[кусок[1:-1]] if кусок.startswith("{") else re.escape(кусок))
    return "".join(куски)


ОБРАЗЦЫ = [(re.compile("^" + _образец(я[форма][0]) + ("(?: " + re.escape(ВОПРОС_ПОСЛЕ[язык]) + ")?" if форма == "наоборот" else "")
                       + " " + _образец(я[форма][1]) + "$"), язык, форма)
           for язык, я in ЯЗЫКИ.items() for форма in ФОРМЫ]


def судить(строка):
    """(судимо, истинно): a page of a frame whose count, spelling and letter are the word's own."""
    с = строка.strip()
    for образ, язык, форма in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        г = м.groupdict(); w = г["w"]
        if w not in ЯЗЫКИ[язык]["слова"]:
            return True, False        # a word the house never declared
        if форма == "букв":
            return True, int(г["n"]) == len(w) and г["L"] == ", ".join(w)
        if форма == "наоборот":
            return True, г["r"] == w[::-1]
        return True, г["l"] == (w[0] if форма == "первая" else w[-1])
    return False, False


def _самопроверка():
    for показ, (язык, форма) in ПОКАЗЫ.items():
        assert судить(показ) == (True, True), (язык, форма, показ)
    мутанты = 0
    for язык, я in ЯЗЫКИ.items():
        w = я["слова"][0]
        # MUTANT: the count off by one (the number after the question mark)
        битая = re.sub(r"(\? )(\d+)", lambda м: м.group(1) + str(int(м.group(2)) + 1), страница(язык, "букв", w), 1)
        assert судить(битая) == (True, False), битая
        # MUTANT: the last letter given as the first (the letter inside the answer's quotes)
        w2 = next(с for с in я["слова"] if с[0] != с[-1])
        с = страница(язык, "первая", w2)
        вопрос, ответ = с.rsplit("? ", 1)
        битая = вопрос + "? " + ответ.replace(w2[0], w2[-1], 1)
        assert судить(битая) == (True, False), битая
        мутанты += 2
    for язык in ("ru", "en", "de", "pl"):
        print("  ", страница(язык, "букв", ЯЗЫКИ[язык]["слова"][0])); print("  ", страница(язык, "первая", ЯЗЫКИ[язык]["слова"][0]))
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, слов {sum(len(я['слова']) for я in ЯЗЫКИ.values())})")


if __name__ == "__main__":
    _самопроверка()
