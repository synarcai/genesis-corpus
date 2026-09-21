#!/usr/bin/env python3
"""КУЗНИЦА МИРА КОШЕЛЬКА.

Перебор живёт в доме (`tools/wallet.py`), кузница берёт у него готовые группы.

ЦЕЛЬ ОБЪЯВЛЯЕТСЯ СТРОКОЙ, А НЕ ВПИСЫВАЕТСЯ В ВЫЗОВ: указатель родов ищет МИР ДОМА по этой
строке и по ввозу кузницы. ИМЯ ПРОХОДА ОБЪЯВЛЕНО ТОЖЕ (`pass_groups`): перепись копий
выводит строчность мира, спрашивая порождающего о проходах.
"""
# ПРОЗВИЩЕ ДОМА В КУЗНЕ — `F` (обычай, читаемый прибором «РОД ДОШЁЛ»).
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import wallet as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_wallet.txt"


def pass_groups(шаг):
    """[[страница]] — по группе на РОД: роды не перемешиваются между собою."""
    вон = []
    for род in F.РОДЫ:
        свои = [с for с, (_я, р) in F.ПОКАЗЫ.items() if р == род]
        вон.append(свои[шаг::len(PASSES)])
    return вон


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
