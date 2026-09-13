#!/usr/bin/env python3
"""GENESIS layer: CONNECTED SPEECH — the joints of reasoning.

THE OWNER NAMED THE DEFECT: after training on GENESIS the speech is
poor. The diagnosis is self-accusing — poverty of speech is the DIRECT
CONSEQUENCE of what bought us total judgeability. The whole corpus is
SHOWS: self-sufficient atoms. The law «a show carries everything it
needs» was applied twice today to fix generators whose line leaned on a
neighbour. That law gave 100% coverage and it forbade the corpus to
JOIN. The organism learned atoms and never learned connection.

MEASURED, NOT GUESSED (omega-e9, 3000 bytes of generated stream):
92 sentences → 64 forms, 30% repeats; ONE frame («how many cookies»)
is 24% of the whole stream; 55% are question frames; NOT ONE coherent
chain fact→question→answer; and the decisive fact — outside bought
genera the organism is COMPLETELY MUTE (60 of 65). It does not produce
forms it was never judged on.

THE LAW IS NOT BROKEN BUT RAISED A FLOOR (holon-e2): the atom becomes a
GROUP, self-sufficient AT THE LEVEL OF THE GROUP. Here a group is ONE
LINE holding two to four sentences — judgeability is preserved (the
court judges the whole line), and connection appears exactly inside it.

FORM AND SUBJECT ARE TOLD APART BY EXECUTION (holon-e2): a SUBJECT has
its own table of facts; a FORM takes as its operand the VERDICT OF A
SUB-COURT. Anaphora, quantifier, connective, modality are FORMS.

EVERY FORM IS BOUGHT BY A COURT THAT EXECUTES IT — and, by verum-6c's
law, a form is bought only when the court executes it AND REJECTS ITS
COUNTERFEIT. A court that never said «no» measured nothing.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import speechforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ЦЕЛЬ ОБЪЯВЛЯЕТСЯ СТРОКОЙ: её читают и указатель родов, и мера воспроизводимости.
ЦЕЛЬ = "datasets/genesis_speech.txt"


def main():
    emit_grouped(ЦЕЛЬ, F.группы)


if __name__ == "__main__":
    main()
