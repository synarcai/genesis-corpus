#!/usr/bin/env python3
"""THE HOUSE OF HOLES — one fact frame, every role of it asked.

holon's Д-1 (REVISION 02.09): in the organism a question is a per-genus
SURFACE bought from that genus' shows, not an OPERATION over a bought fact
frame, so the organism cannot ask what it was never shown asked. This house
holds the frame «{time} {actor} {verb} {number} {things} {place}» and the
operation that turns any one role of it into a hole: the question word
names the hole's TYPE (who → actor, how many → number, what → thing, where
→ place, when → time), the question keeps every other role, and the answer
is exactly the filler the question took out. The generator draws lines from
here; the court parses a fact by the same frame and recomputes every lawful
question with its answer — nothing in the court is looked up from the line.
"""
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rugram  # noqa: E402

ДНИ = {
    "en": ("on monday", "on tuesday", "on wednesday", "on thursday", "on friday", "on saturday", "on sunday"),
    "ru": ("в понедельник", "во вторник", "в среду", "в четверг", "в пятницу", "в субботу", "в воскресенье"),
}
# A frame: the verb (en past, en base, ru masculine, ru feminine), the RU
# question word of its place (куда for putting, где for the rest), its
# places (en, ru in the case the verb governs) and its things (en singular,
# en plural, ru lemma — the count form comes from the house of forms).
РАМКИ = (
    ("put", "put", "положил", "положила", "куда",
     (("on the shelf", "на полку"), ("in the box", "в коробку"), ("on the table", "на стол"), ("in the bag", "в сумку")),
     (("cup", "cups", "чашка"), ("book", "books", "книга"), ("pen", "pens", "ручка"), ("plate", "plates", "тарелка"))),
    ("bought", "buy", "купил", "купила", "где",
     (("at the market", "на рынке"), ("in the shop", "в магазине"), ("at the fair", "на ярмарке")),
     (("apple", "apples", "яблоко"), ("pear", "pears", "груша"), ("pen", "pens", "ручка"), ("book", "books", "книга"))),
    ("found", "find", "нашёл", "нашла", "где",
     (("in the park", "в парке"), ("in the garden", "в саду"), ("on the road", "на дороге"), ("on the beach", "на пляже")),
     (("coin", "coins", "монета"), ("shell", "shells", "ракушка"), ("stone", "stones", "камень"), ("key", "keys", "ключ"))),
    ("ate", "eat", "съел", "съела", "где",
     (("in the kitchen", "на кухне"), ("at school", "в школе"), ("in the garden", "в саду")),
     (("apple", "apples", "яблоко"), ("pear", "pears", "груша"), ("cookie", "cookies", "печенье"), ("plum", "plums", "слива"))),
    ("read", "read", "прочитал", "прочитала", "где",
     (("in the library", "в библиотеке"), ("at school", "в школе"), ("at home", "дома")),
     (("book", "books", "книга"), ("story", "stories", "рассказ"), ("letter", "letters", "письмо"))),
)


def факт(язык, день, имя, род, р, n, вещь, место):
    """The frame with no hole. `род` is the RU gender of the actor."""
    if язык == "en":
        return f"{день} {имя} {р[0]} {n} {вещь[1]} {место[0]}."
    гл = р[3] if род == "f" else р[2]
    return f"{день} {имя} {гл} {n} {rugram.форма(вещь[2], n)} {место[1]}."


def дыры(язык, день, имя, род, р, n, вещь, место):
    """Every role asked in turn: (question, answer) pairs, the answer being
    the filler the question removed; «who» takes the masculine in RU."""
    if язык == "en":
        прош, осн = р[0], р[1]
        return (
            (f"who {прош} {n} {вещь[1]} {место[0]} {день}?", f"{имя}."),
            (f"how many {вещь[1]} did {имя} {осн} {место[0]} {день}?", f"{n}."),
            (f"what did {имя} {осн} {место[0]} {день}?", f"{n} {вещь[1]}."),
            (f"where did {имя} {осн} {n} {вещь[1]} {день}?", f"{место[0]}."),
            (f"when did {имя} {осн} {n} {вещь[1]} {место[0]}?", f"{день}."),
        )
    гл = р[3] if род == "f" else р[2]
    вещи = rugram.форма(вещь[2], n)
    return (
        (f"кто {р[2]} {n} {вещи} {место[1]} {день}?", f"{имя}."),
        (f"сколько {rugram.форма(вещь[2], 5)} {гл} {имя} {место[1]} {день}?", f"{n}."),
        (f"что {гл} {имя} {место[1]} {день}?", f"{n} {вещи}."),
        (f"{р[4]} {гл} {имя} {n} {вещи} {день}?", f"{место[1]}."),
        (f"когда {гл} {имя} {n} {вещи} {место[1]}?", f"{день}."),
    )


def _alt(слова):
    return "|".join(re.escape(с) for с in sorted(set(слова), key=len, reverse=True))


ФАКТ = {
    "en": re.compile(rf"^(?P<день>{_alt(ДНИ['en'])}) (?P<имя>[a-z]+) (?P<гл>{_alt(р[0] for р in РАМКИ)}) (?P<n>\d+) "
                     rf"(?P<вещь>[a-z]+) (?P<место>{_alt(м[0] for р in РАМКИ for м in р[5])})\.$"),
    "ru": re.compile(rf"^(?P<день>{_alt(ДНИ['ru'])}) (?P<имя>[А-ЯЁ][а-яё]+) (?P<гл>{_alt(г for р in РАМКИ for г in р[2:4])}) (?P<n>\d+) "
                     rf"(?P<вещь>[а-яё]+) (?P<место>{_alt(м[1] for р in РАМКИ for м in р[5])})\.$"),
}
СТРОКА = re.compile(r"^(?P<факт>[^.?]+\.)(?: (?P<вопрос>[^?]+)\? (?P<ответ>[^.?]+)\.)?$")


def разобрать(строка):
    """(язык, roles, question, answer) of a line of the hole market, or
    None when the line's fact is not a frame of this house. The roles are
    the generator's arguments, recovered: the verb names the frame, the
    thing and place are looked up in it, the RU count form must agree."""
    м = СТРОКА.match(строка)
    if not м:
        return None
    for язык, образец in ФАКТ.items():
        ф = образец.match(м["факт"])
        if not ф:
            continue
        n = int(ф["n"])
        for р in РАМКИ:
            if язык == "en" and ф["гл"] != р[0]:
                continue
            if язык == "ru" and ф["гл"] not in р[2:4]:
                continue
            места = [м_ for м_ in р[5] if м_[0 if язык == "en" else 1] == ф["место"]]
            if язык == "en":
                вещи = [в for в in р[6] if в[1] == ф["вещь"]]
                род = "m"
            else:
                вещи = [в for в in р[6] if rugram.форма(в[2], n) == ф["вещь"]]
                род = "f" if ф["гл"] == р[3] else "m"
            if not места or not вещи:
                # the frame's own verb, day and place, but a thing this
                # frame does not carry, or a count form that disagrees
                return язык, None, м["вопрос"], м["ответ"]
            роли = (ф["день"], ф["имя"], род, р, n, вещи[0], места[0])
            return язык, роли, м["вопрос"], м["ответ"]
        return None
    return None


def судить(строка):
    """(judged, true): a bare frame is true by its forms; a question is true
    iff it and its answer are one lawful hole of the fact."""
    ч = разобрать(строка)
    if ч is None:
        return (False, False)
    язык, роли, вопрос, ответ = ч
    if роли is None:
        return (True, False)
    if вопрос is None:
        return (True, True)
    return (True, (f"{вопрос}?", f"{ответ}.") in дыры(язык, *роли))
