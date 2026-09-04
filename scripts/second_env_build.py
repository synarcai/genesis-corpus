#!/usr/bin/env python3
"""[СВОД ДО ВТОРОГО ОКРУЖЕНИЯ] — по N строк на форму, и ни одной сверх.

Закон d5 (04.09): масса одинаковых строк не покупает ничего сверх первого
показа своего рода; покупка родится, когда форма встречена в ДВУХ окружениях.
Прибор массы на форму (`scripts/mass_per_form.py`) назвал цену этого закона:
173 861 строка свода из 324 923 стоят выше рубежа восьми строк на форму.

Число это ВЫКЛАДКА, а не замер, и holon прав, что публиковать его владельцу
рано: закон d5 мерян на десятках показов, а не на десятках тысяч. Замер вместо
выкладки делается так: срезать свод до N строк на форму, сварить на нём и
померить обе полосы. Те же числа — закон перенесён, и «минимальный корпус»
получает ответ замером, а не рассуждением. Хуже — граница повтора на больших
числах работает иначе, и это находка крупнее самой экономии.

СРЕЗ ДЕТЕРМИНИРОВАН: миры идут в порядке манифеста, строки — в порядке файла,
и из каждой формы берутся ПЕРВЫЕ N. Никакой случайности, никакого «лучшего
представителя»: выбор представителя был бы вкусом, а порядок есть закон.

    python3 scripts/second_env_build.py [--сколько 2] [--цель путь]
"""
import argparse
import collections
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
sys.path.insert(0, str(КОРЕНЬ / "scripts"))
import form_census as C  # noqa: E402
import genesis  # noqa: E402


def main():
    ап = argparse.ArgumentParser()
    ап.add_argument("--сколько", type=int, default=2)
    ап.add_argument("--цель", default="")
    а = ап.parse_args()
    цель = pathlib.Path(а.цель) if а.цель else КОРЕНЬ / "datasets" / f"GENESIS-ENV{а.сколько}.txt"
    видано = collections.Counter()
    вон, всего = [], 0
    for путь in genesis.worlds(kind="shows"):
        for с in путь.read_text(encoding="utf-8", errors="replace").splitlines():
            т = с.strip()
            if not т or т.startswith("\x0c"):
                continue
            всего += 1
            ск = C.род(C.скелет(т))
            if видано[ск] >= а.сколько:
                continue
            видано[ск] += 1
            вон.append(т)
    цель.parent.mkdir(parents=True, exist_ok=True)
    цель.write_text("\n".join(вон) + "\n", encoding="utf-8")
    доля = 100 * len(вон) // max(1, всего)
    print(f"written {цель}: {цель.stat().st_size} bytes, {len(вон)} lines, "
          f"форм {len(видано)}, из свода {всего} строк ({доля} %) — по {а.сколько} на форму")
    return 0


if __name__ == "__main__":
    sys.exit(main())
