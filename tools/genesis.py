#!/usr/bin/env python3
"""WHAT GENESIS IS — one definition, read by every judge and the conveyor.

The manifest was opened in four places: the language census, the
agreement court, the arithmetic court and the v7 conveyor. Four
readings of one file are four chances to disagree about what the
corpus IS, and they had already begun to: two judges resolved the path
from the REPOSITORY ROOT and one from the CURRENT DIRECTORY, so the
same court answered from the repository and refused from anywhere else.

The refusal is honest (a missing manifest is a refusal, never a
crash, and never an empty walk read as cleanliness), but it belongs to
one place, said once.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "datasets/GENESIS-MANIFEST.json"


class Unreadable(Exception):
    """The manifest could not be read — the caller must REFUSE.

    Carried as an exception rather than an empty list because an empty
    walk read as a clean verdict is the one failure an audit park must
    never produce.
    """


def manifest():
    """The manifest as declared, or Unreadable with the reason named."""
    try:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, ValueError) as why:
        raise Unreadable(f"{MANIFEST.name}: {why}") from why


def worlds(existing=True, kind=None):
    """Paths of the worlds GENESIS is made of.

    `existing` drops a declared world whose file is absent: a judge
    walks what the organism can eat, while a conveyor may want to know
    that a declared world is missing. The choice is the caller's and is
    named, not guessed.

    `kind` selects by the world's declared TEXT KIND. A court
    calibrated on generated shows accuses honest prose falsely — a
    hyphen inside «T-113» reads as minus, a power written «7² − 1»
    reads as «7 − 1», and a falsehood QUOTED in order to be refuted
    reads as a falsehood asserted. Jurisdiction is therefore declared
    by the world and asked for by the judge, never assumed.
    """
    try:
        declared = manifest()["worlds"]
    except KeyError as why:
        raise Unreadable(f"{MANIFEST.name}: no 'worlds'") from why
    if kind is not None:
        declared = [w for w in declared
                    if w.get("text", "shows") == kind]
    paths = [_resolve(w["file"]) for w in declared]
    return [p for p in paths if p.is_file()] if existing else paths


def external_root():
    """Where worlds that do not live in this repository are looked up.

    The prose corpora are built by the architecture repository's own
    pipeline. Copying them here would create a second source of one
    fact — the very drift this module exists to prevent — so the
    manifest DECLARES where they live, and the environment may override
    the declaration for a different layout.
    """
    import os
    названо = os.environ.get("GENESIS_EXTERNAL_ROOT")
    if названо:
        return pathlib.Path(названо)
    try:
        объявлено = manifest().get("external_root")
    except Unreadable:
        объявлено = None
    return (ROOT / объявлено).resolve() if объявлено else ROOT


def _resolve(file):
    """Inside the repository first; outside only if declared."""
    свой = ROOT / file
    if свой.is_file():
        return свой
    чужой = external_root() / file
    return чужой if чужой.is_file() else свой
