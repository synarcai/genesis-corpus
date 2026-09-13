#!/usr/bin/env python3
"""GENESIS layer: AGE — a quantity that MOVES ALONG WITH TIME.

Eleven questions of the band die here, and their genus is one: a number
that is not fixed but carried by time. «in 9 years ruby will be twice as
old» asks the organism to hold three things at once — the age now, the
shift, and the fact that the shift is added TO BOTH ALIKE. The last of
the three is the law the corpus never showed: TIME FLOWS FOR EVERYONE.

WHY A CORPUS OF ARITHMETIC DOES NOT ALREADY TEACH THIS. «12 + 3 = 15»
is a fact about numbers; «in 3 years tom will be 15» is a fact about a
number ATTACHED to somebody, and the attachment is what makes the second
person's age move too. A layer that shows only the addition teaches the
step and hides the reason there are two of them.

WHAT IS SHOWN, AND WHY EACH GENUS EXISTS:

    СЕЙЧАС      two ages and the difference between them — the ground
                every later genus stands on
    ВПЕРЁД      the shift added to BOTH, said in one show, so the pair
                of additions is one act and not two
    ЗАКОН       the same shift with its invariant named: the difference
                does not change. This is the one thing about age
                arithmetic that is not arithmetic, and the corpus owes
                it a show of its own
    НАЗАД       the shift subtracted from both — and SILENCE where it
                would take somebody below one year old
    КРАТНОЕ     «three times as old», with «12 = 3 × 4» beside it: the
                relation and its ground in one line
    КРАТНОЕ ВПЕРЁД  the band's hardest genus. It is built BACKWARDS —
                the future ages are chosen first, so the multiple is
                true BY CONSTRUCTION and never by luck
    ВОПРОС      every genus asked as well as told. A probe went mute on
                questions whose statements it knew: knowledge with only
                a declarative surface REPORTS, it does not ANSWER
    ОТКАЗ       «how old is ann's brother? it is not said». Muteness
                needs a PAIR — a refusal WITH ITS GROUND — or the
                organism learns that silence is the answer to what it
                does not know

ЯДРО ДОСЛОВНЫХ ПОВТОРОВ. The first three cases of every genus are the
SAME in every pass, word for word; the rest walk with the pass number.
A form is bought by repetition — that is a measurement, not an opinion —
and a layer whose every line is new gives the form nothing to stand on.

ИМЯ СКЛОНЯЕТСЯ, И ПАДЕЖИ ОБЪЯВЛЕНЫ. «тому 12 лет» is the dative, «том
старше ани» pairs a nominative with a genitive. Russian case cannot be
had by cutting an ending, so the three forms of every name are DECLARED
here and re-declared by the court: an edit in one house and not in the
other makes the line UNJUDGED, and the write gate does not pass an
unjudged line.

СЧЁТНАЯ ФОРМА БЕРЁТСЯ У ДОМА РУССКОГО СЧЁТА (`tools/rugram.py`), not
written out here: «1 год», «3 года», «5 лет» is a law of the language,
and a second list beside the declared one parts from it on the first
day. English does the same through `tools/plural.py`.

EVERY NUMBER IS COMPUTED HERE AND RE-COMPUTED BY THE COURT — including
the law: `courts/age_court.py` adds the shift to both ages itself and
checks that the difference it finds after equals the difference it finds
before. A show that shifted only one of the two dies there.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ageforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_age.txt"


def main():
    emit_grouped(ЦЕЛЬ, F.группы)


if __name__ == "__main__":
    main()
