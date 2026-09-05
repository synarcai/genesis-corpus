# GENESIS

A self-verifying foundations corpus: every claim is checked by an
instrument in this repository.

GENESIS is not a general-purpose dataset. It is the material a
[SynarcAI](https://github.com/) organism is grown on, and it is built to
one rule:

> **A corpus may not carry a claim that nobody can verify.**
>
> An unverifiable show teaches the *form* of knowledge without its
> substance, and what the organism buys is the form.

Everything here follows from that rule. The layers are generated, the
generators are in the repository, and the courts that judge the
generated text are in the repository beside them — so the corpus can be
rebuilt from nothing and re-judged by anyone.

## What is inside

| | |
|---|---|
| **167 worlds of shows + 213 of prose** | declared in `datasets/GENESIS-MANIFEST.json`; 71 prose worlds are public-domain books on the shelf (`shelf/`, contract `declarations/SHELF.md`) |
| **29 languages** | one pack each in `tools/langpacks/`, zero engine edits |
| **124 courts + 86 instruments** | every line re-executed by a court; the corpus as a whole measured by judgeability, reproducibility, manifest, shelf, band, library, concept reach, mutation catch |
| **0** | false or blind lines among ~291 000 judged (after the repetition ceiling LAW = 2 per show and world, М-402: ~65 000 copies gone, no show lost) |

The corpus is a **knowledge engine**, not a text dump: worlds are
functions of the manifest, courts re-execute every claim, executor
houses are shared by generator and court, and the whole is closed on
itself by instruments whose verdicts are kept in a ledger — see
`declarations/KNOWLEDGE-ENGINE.md` (in Russian, the working language of
the college) and `python3 scripts/crystal.py`.

The foundations covered: **language** (paradigms shown in frames that
determine the form, never in tables), **mathematics** (arithmetic,
fractions, algebraic identities checked by substitution, logic and
sets), **informatics** (order, number theory, complexity, data
structures, positional notation), **physics** (seven integer laws, whose
*names* are checked against their relations), **cybernetics** (error,
convergence simulated, state machines walked, requisite variety).

## Running the courts

```sh
bash scripts/courts.sh
```

Every court answers in one form — `<NAME> PASS|FAIL: N of M` — and
returns `0` clean, `1` a finding, `2` a refusal to judge. A court that
cannot read its source **refuses**; it never guesses and never reports a
silent zero.

## Rebuilding the corpus

```sh
python3 tools/gen_genesis_algorithms.py     # one layer
python3 scripts/reproducible.py             # every layer, byte for byte
```

`reproducible.py` regenerates each layer into a temporary tree and
compares SHA-256 with what is committed. Its frontier is zero: the
shipped corpus **is** what the generators produce, or the guard falls.

## Adding a language

One file: `tools/langpacks/<lang>.json`. It declares the writing system
and its range, the numerals, the inflection classes with their full
paradigms, the kinds of showing, the agreement rule, and — for a script
that writes without spaces — how words are separated. Nine judged fields
must be green before a single byte is written.

Chinese was the test of that claim: it cost one pack and one general
engine change (declared segmentation), not a branch per language. The
promise held for alphabets and needed one honest amendment for a script
without spaces; that is written down rather than smoothed over.

## Laws this corpus is built on

- **One occurrence is chance; two own the fact.** A word shown once
  costs weight and buys nothing.
- **A lie about the world is not caught by counting.** `peter keeps -1
  coins`, `ida bought 3 friends`, `power = force × distance; 20 × 3 =
  60` — each is grammatically and arithmetically perfect and false about
  what exists. Such knowledge is *declared* beside the list it
  qualifies, never inferred.
- **A show that depends on the neighbouring line is fragile.** Passes
  are shuffled; every show carries what it needs.
- **The question confirms the item.** A word living only after a digit
  is a measure, not a thing.
- **Approximation is a genus of its own.** Nothing here is rounded: a
  corpus stating `3.14` as the value of a circle teaches a rounding as a
  truth.

## Licence

Code (`tools/`, `courts/`, `scripts/`) — Apache-2.0, see `LICENSE`.
Corpus (`datasets/`, `tools/langpacks/`) — CC BY 4.0, see
`LICENSE-DATA`. Derived vocabulary attribution — see `NOTICE`.
