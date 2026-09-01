#!/usr/bin/env python3
"""THE PASS DISCIPLINE OF A GENESIS LAYER — one law, one place.

Fifteen generators carried this law as fifteen copies, and copies do
not stay equal. `shuffle` had split into FOUR bodies: two guarded the
empty list and two did not, so nine layers died with a bare
StopIteration on a pass that produced nothing — the very «empty walk»
fault the audit park forbids in its own instruments. The pass table
`[(7,5), (11,2), (13,9), (17,4), (19,12)]` stood unnamed in fourteen
files, and the seam, the byte count and the written line were written
out by hand fifteen times.

WHAT THE LAW ACTUALLY SAYS:
  · a layer is emitted in PASSES, and each pass varies its instances,
    so volume buys new facts instead of new weight (the knowledge-trail
    number: an x1 layer bought +9464 owned types where x22 layers
    bought zero);
  · each pass is SHUFFLED by a stride coprime with its length — a
    permutation, never a sample: nothing is dropped and nothing is
    doubled;
  · passes are separated by a FORM FEED, so the reader that cuts a
    corpus into worlds finds an honest seam.
"""

# ПРОХОДЫ: пять пар (шаг, сдвиг). Пары взаимно просты с обычными
# длинами проходов, и потому перестановка — настоящая; пятикратность
# взята из тропы знания, где слой ×1 покупал типы, а ×22 — вес.
PASSES = ((7, 5), (11, 2), (13, 9), (17, 4), (19, 12))
SEAM = "\n\x0c\n"


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def shuffle(items, mult, shift):
    """A PERMUTATION, NOT A SAMPLE — and the empty list is empty.

    Nine of fifteen copies lacked this guard: `next()` over an empty
    range raises StopIteration, so a pass that produced nothing killed
    the generator with a traceback about iterators instead of writing
    nothing. A layer may legitimately produce no shows in a pass.
    """
    n = len(items)
    if n == 0:
        return []
    step = next(k for k in range(mult, mult + n) if gcd(k, n) == 1)
    return [items[(i * step + shift) % n] for i in range(n)]


def emit(path, pass_shows, passes=PASSES):
    """Run the passes, weld them with seams, write, and say the number.

    `pass_shows(i)` returns the shows of pass i. The count printed is
    SHOWS, not lines: a show may span several lines (the fractions
    layer speaks one fact on three surfaces), and reporting lines would
    quietly inflate it.
    """
    blocks, total = [], 0
    for pi, (mult, shift) in enumerate(passes):
        shows = pass_shows(pi)
        total += len(shows)
        blocks.append("\n".join(shuffle(shows, mult, shift)))
    body = SEAM.join(blocks) + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"written {path}: {len(body)} bytes, {total} shows")
    return body


def emit_grouped(path, pass_groups, passes=PASSES):
    """The same law where a pass carries SEVERAL kinds.

    Two layers (structures, units) weld one block per KIND per pass
    rather than one block per pass: their kinds are separate worlds of
    show and must not be interleaved by the shuffle. The stride is the
    pass's own, so a kind is permuted, never sampled — the law is the
    same law, applied one level down.
    """
    blocks, total = [], 0
    for pi, (mult, shift) in enumerate(passes):
        for shows in pass_groups(pi):
            total += len(shows)
            blocks.append("\n".join(shuffle(shows, mult, shift)))
    body = SEAM.join(blocks) + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"written {path}: {len(body)} bytes, {total} shows")
    return body

