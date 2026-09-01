#!/usr/bin/env python3
"""GENESIS layer: STORY АS THE THIRD SURFACE (М-1 of
the GSM8K collegium, road step 2).

The cut's seed: a story is one more SURFACE of the
number world — «у маши было 5 яблок» is the same table
triple as «5 − 2 = 3»: (verb, subject, object) = number.
This layer supplies the mass that buys the verb forms,
the glyph pairs that let the number axis marry the
surfaces, and the question shows that teach the
«сколько…? / how many…?» hole.

Verb algebra shown, never told:
  A. had - gave = left      (было − отдал = осталось)
  B. had + got  = became    (было + получил = стало)
  C. k items at p = k·p     (money rate, ties М-4)

Laws: bare shows, explicit RU case forms, deterministic
coprime shuffles, form-feed seams, glyph pair beside
every story block.
"""

from layer import emit


from plural import by_count


# (nominative, genitive «у …», feminine?)
NAMES_RU = [
    ("маша", "маши", True),
    ("петя", "пети", False),
    ("вера", "веры", True),
    ("коля", "коли", False),
    ("аня", "ани", True),
    ("дима", "димы", False),
    ("лена", "лены", True),
    ("юра", "юры", False),
]
NAMES_EN = ["mary", "peter", "vera", "nick",
            "ann", "dima", "lena", "yuri"]


def verb(base, fem):
    return base + ("а" if fem else "")
ITEMS = [
    # ((ru_one, ru_few, ru_many), en_pl)
    (("яблоко", "яблока", "яблок"), "apples"),
    (("шар", "шара", "шаров"), "balls"),
    (("книга", "книги", "книг"), "books"),
    (("монета", "монеты", "монет"), "coins"),
    (("орех", "ореха", "орехов"), "nuts"),
    (("марка", "марки", "марок"), "stamps"),
]


def ru_form(forms, k):
    one, few, many = forms
    if k % 10 == 1 and k % 100 != 11:
        return one
    if k % 10 in (2, 3, 4) and k % 100 not in (
        12, 13, 14,
    ):
        return few
    return many


def story_gave(nrec, ne, it, enp, a, b):
    nr, ng, fem = nrec
    c = a - b
    p = lambda k: ru_form(it, k)
    e = lambda k: by_count(k, enp)
    gave = verb("отдал", fem)
    return [
        f"у {ng} было {a} {p(a)}. {nr} {gave} "
        f"{b} {p(b)}. у {ng} осталось {c} {p(c)}.",
        f"{ne} had {a} {e(a)}. {ne} gave away "
        f"{b} {e(b)}. {ne} has {c} {e(c)} left.",
        f"{a} − {b} = {c}.",
        f"сколько {p(5)} осталось у {ng}? "
        f"осталось {c} {p(c)}.",
        f"how many {enp} does {ne} have left? "
        f"{c} {e(c)} left.",
    ]


def story_got(nrec, ne, it, enp, a, b):
    nr, ng, fem = nrec
    c = a + b
    p = lambda k: ru_form(it, k)
    e = lambda k: by_count(k, enp)
    got = verb("получил", fem)
    return [
        f"у {ng} было {a} {p(a)}. {nr} {got} "
        f"{b} {p(b)}. у {ng} стало {c} {p(c)}.",
        f"{ne} had {a} {e(a)}. {ne} got {b} "
        f"{e(b)} more. now {ne} has {c} {e(c)}.",
        f"{a} + {b} = {c}.",
        f"сколько {p(5)} стало у {ng}? "
        f"стало {c} {p(c)}.",
        f"how many {enp} does {ne} have now? "
        f"now {c} {e(c)}.",
    ]


def story_rate(nrec, ne, it, enp, k, price):
    nr, ng, fem = nrec
    total = k * price
    p = lambda n: ru_form(it, n)
    rub = ("рубль", "рубля", "рублей")
    bought = verb("купил", fem)
    paid = verb("заплатил", fem)
    return [
        f"{nr} {bought} {k} {p(k)} по {price} "
        f"{ru_form(rub, price)}. {nr} {paid} "
        f"{total} {ru_form(rub, total)}.",
        f"{ne} bought {k} {enp} at {price} "
        f"dollars each. {ne} paid {total} "
        f"dollars.",
        f"{k} × {price} = {total}.",
        f"сколько {ru_form(rub, 5)} "
        f"{verb('заплатил', fem)} {nr}? "
        f"{verb('заплатил', fem)} {total} "
        f"{ru_form(rub, total)}.",
        f"how many dollars did {ne} pay? "
        f"{ne} paid {total} dollars.",
    ]


def pass_shows(pi):
    """Shows of one pass — instances shifted, not reordered.

    32's knowledge-trail number: the layer that bought the whole
    vocabulary repeated NOTHING (+9464 at x1) while x22 layers bought
    zero. Passes therefore vary INSTANCES: each regenerates the
    stories with shifted values, so forms take their mass from
    kind-frequency over DIFFERENT shows and twin lines stay near the
    lawful two.
    """
    shows = []
    i = pi * 11
    for (nrec, ne) in zip(NAMES_RU, NAMES_EN):
        for (it, enp) in ITEMS:
            a = (i * 3) % 9 + 6      # 6..14
            b = (i * 2) % 5 + 1      # 1..5
            shows += story_gave(nrec, ne, it, enp, a, b)
            a2 = (i * 5) % 8 + 2     # 2..9
            b2 = (i * 3) % 6 + 1     # 1..6
            shows += story_got(nrec, ne, it, enp, a2, b2)
            k = (i % 4) + 2          # 2..5
            price = (i % 3) + 2      # 2..4
            shows += story_rate(nrec, ne, it, enp, k, price)
            i += 1
    return shows


def main():
    # THE COUNT WAS WRONG AND NOBODY SAW IT: this main printed
    # `len(shows)` — the LAST pass — and called it the layer's shows,
    # understating by five. The shared organ counts every pass.
    emit("datasets/genesis_story.txt", pass_shows)


if __name__ == "__main__":
    main()
