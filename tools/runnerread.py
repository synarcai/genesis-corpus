#!/usr/bin/env python3
"""ЧТЕНИЕ ОТЧЁТА БЕГУНА СУДОМ — вторая рука судов рук агента (29.09): числа итога прогона стоят в отчёте бегуна.

Дом называет числа прогона своим чтением отчёта (`toolrepo.строки_итога`); суд читает отчёт СВОИМ чтением: строки
«test result» cargo по порядку или «Ran N tests» и «OK» / «NO TESTS RAN» / «FAILED (failures=K, errors=E)» unittest
(упавшие — провалы и ошибки). Чтение одно на всякий суд, чьи страницы несут прогон мира процесса (`toolrepo_court`,
`toolcode_court`): две копии одной руки разошлись бы молча.
"""
import re

CARGO = re.compile(r"^test result: (?:ok|FAILED)\. (\d+) passed; (\d+) failed;", re.M)
UNITTEST = re.compile(r"^Ran (\d+) tests? in .*\n\n(OK|NO TESTS RAN|FAILED \((.*)\))$", re.M)


def стоят(отчёт, строки_итога):
    """Числа итога [(прошло, упало)] стоят в отчёте бегуна — чтением суда."""
    cargo = [(int(п), int(у)) for п, у in CARGO.findall(отчёт)]
    if cargo:
        return cargo == строки_итога
    м = UNITTEST.search(отчёт)
    if м is None or (м.group(2) == "NO TESTS RAN") != (м.group(1) == "0"):
        return False
    упало = sum(int(x) for x in re.findall(r"\b(?:failures|errors)=(\d+)", м.group(3) or ""))
    return строки_итога == [(int(м.group(1)) - упало, упало)]
