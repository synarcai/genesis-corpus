"""MASS FROM THE RULE, NOT FROM A TABLE OF PAIRS (М-148, rule 2).

A world that draws its (a, b) from one hand-written table of pairs shows at
most as many distinct pairs as the table has rows — every pass repeats the
same ten shows, and the frame's mass is weight, not knowledge (physics: a
median of 2 distinct shows per frame). Here a pair is composed from two
cycles of FACTORS whose lengths are coprime: the step k walks both cycles
at once, and the pairs repeat only after len(a) × len(b) steps. The nice
numbers stay declared by hand; the mass comes from the rule.
"""


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def пара(k, ряд_a, ряд_b):
    """The k-th pair of two coprime cycles — distinct for len(a) × len(b) steps."""
    assert gcd(len(ряд_a), len(ряд_b)) == 1, "cycle lengths must be coprime"
    return ряд_a[k % len(ряд_a)], ряд_b[k % len(ряд_b)]


def шаг(pass_i, i, ширина):
    """One step counter over passes and shows: pass_i × width + i."""
    assert 0 <= i < ширина, "a show index inside the pass width"
    return pass_i * ширина + i
