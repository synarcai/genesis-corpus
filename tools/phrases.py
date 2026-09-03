#!/usr/bin/env python3
"""ONE HELPER FOR THE HOUSES OF PHRASES — a template with holes becomes a
pattern. A house declares a phrase as «{n} {б} sind {итог} {м}: {л}.»; the
generator fills the holes; the court turns the same phrase into a regex by
escaping the literal parts and putting a group at every hole. Written once
here so that every house of phrases (geometry, units, summary, weekdays,
sequences) reads the same law."""
import re

_ДЫРА = re.compile(r"\{([^{}]+)\}")


def образец(шаблон, дыры):
    """The template as a regex source: literal parts escaped, each hole
    replaced by its group from `дыры` (a dict hole name → regex source)."""
    куски, конец = [], 0
    for м in _ДЫРА.finditer(шаблон):
        куски.append(re.escape(шаблон[конец:м.start()]))
        куски.append(дыры[м.group(1)])
        конец = м.end()
    куски.append(re.escape(шаблон[конец:]))
    return "".join(куски)


def порядок(шаблон):
    """The hole names of the template in order — the order of the groups."""
    return [м.group(1) for м in _ДЫРА.finditer(шаблон)]
