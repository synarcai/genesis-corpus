#!/usr/bin/env python3
"""[СТЕНОГРАММЫ] — каждое действие исполняется над состоянием прошлого шага.

Форма объявлена в declarations/STENOGRAM.md. Показ занимает несколько
строк; палата судит ПОСТРОЧНО, и потому суд держит СЛОЙ: заголовок
стенограммы открывает состояние среды, каждый шаг судится исполнением
над состоянием, оставленным предыдущей строкой, конец — сверкой с
последним откликом. Строка стенограммы, встреченная без заголовка,
несудима (чужой род или обрыв).
"""
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import spacegrid as S  # noqa: E402

Г = S.СЕТКА.pattern
ЗАГОЛОВОК = re.compile(rf"^(?:transcript|стенограмма) (\d+) (?:on grid|на сетке) ({Г})$")
ШАГ = re.compile(rf"^(?:step|шаг) (\d+): (?:action|действие) «([^»]+)» → (?:response|отклик): "
                 rf"(?:(?:grid|сетка) ({Г})|(?:refused|отказ): (.+))$")
КОНЕЦ = re.compile(rf"^(?:end|конец): (?:grid|сетка) ({Г})$")
ДЕЙСТВИЕ = re.compile(
    r"^(?:shift|сдвиг) (right|left|down|up|вправо|влево|вниз|вверх) (?:by|на) (\d)$"
    r"|^(?:rotate|поворот на) (90|180|270)° (?:clockwise|по часовой стрелке)$"
    r"|^(?:reflect|отражение) (left-right|top-bottom|слева направо|сверху вниз)$"
    r"|^(?:paint|erase|закрасить|стереть) \((\d),(\d)\)$")
КУДА = {"вправо": "right", "влево": "left", "вниз": "down", "вверх": "up"}
ОСЬ = {"слева направо": "left-right", "сверху вниз": "top-bottom"}


def исполнить(состояние, действие):
    """(новое состояние, None) или (None, причина отказа); None,None — не наше."""
    м = ДЕЙСТВИЕ.match(действие)
    if not м:
        return None, None
    n, m_ = len(состояние), len(состояние[0])
    if м.group(1):
        return S.сдвиг(состояние, КУДА.get(м.group(1), м.group(1)), int(м.group(2))), None
    if м.group(3):
        return S.поворот(состояние, int(м.group(3))), None
    if м.group(4):
        return S.отражение(состояние, ОСЬ.get(м.group(4), м.group(4))), None
    r, c = int(м.group(5)), int(м.group(6))
    if not (1 <= r <= n and 1 <= c <= m_):
        return None, "outside"
    закрасить = действие.startswith(("paint", "закрасить"))
    ряд = list(состояние[r - 1])
    ряд[c - 1] = "#" if закрасить else "."
    вон = list(состояние)
    вон[r - 1] = "".join(ряд)
    return вон, None


class Слой:
    """Состояние среды между строками одной стенограммы."""

    def __init__(self):
        self.состояние = None
        self.шагов = 0
        self.ждём = 0
        self.последний = None
        self.обрыв = False

    def впитать(self, путь):
        pass


def судить(строка, слой=None):
    """(судимо, истинно) для одной строки стенограммы; слой держит среду."""
    с = строка.strip()
    if слой is None:
        слой = Слой()
    м = ЗАГОЛОВОК.match(с)
    if м:
        слой.состояние = S.разобрать(м.group(2))
        слой.шагов, слой.ждём, слой.последний, слой.обрыв = int(м.group(1)), 1, None, False
        return True, слой.состояние is not None and слой.шагов >= 1
    м = ШАГ.match(с)
    if м:
        if слой.состояние is None or слой.обрыв:
            return False, False
        номер, действие, сетка, отказ = int(м.group(1)), м.group(2), м.group(3), м.group(4)
        if номер != слой.ждём:
            слой.обрыв = True
            return True, False
        слой.ждём += 1
        новое, причина = исполнить(слой.состояние, действие)
        if новое is None and причина is None:
            слой.обрыв = True
            return True, False              # действие вне объявленного набора
        if отказ is not None:
            верно = новое is None and причина == "outside" and "outside" in отказ or "вне" in отказ
            return True, bool(новое is None and верно)
        if новое is None:
            return True, False              # среда отказала, а показ дал сетку
        слой.состояние = новое
        слой.последний = S.записать(новое)
        return True, слой.последний == сетка
    м = КОНЕЦ.match(с)
    if м:
        if слой.состояние is None or слой.обрыв:
            return False, False
        верно = (слой.ждём == слой.шагов + 1 and слой.последний == м.group(1))
        слой.состояние = None
        return True, верно
    return False, False


def main():
    import collections
    итог = collections.Counter()
    for путь in [pathlib.Path(п) for п in sys.argv[1:]] or [КОРЕНЬ / "datasets" / "genesis_stenogram.txt"]:
        слой = Слой()
        for с in путь.read_text(encoding="utf-8").splitlines():
            if not с.strip():
                continue
            судимо, истинно = судить(с, слой)
            итог["несудимо" if not судимо else ("истина" if истинно else "ЛОЖЬ")] += 1
            if судимо and not истинно:
                print("  ЛОЖЬ:", с[:120])
    ложь = итог["ЛОЖЬ"]
    print(f"СТЕНОГРАММЫ {'PASS' if not ложь else 'FAIL'}: {ложь} ложных, "
          f"{итог['истина']} истинных, {итог['несудимо']} несудимых")
    return 0 if not ложь else 1


if __name__ == "__main__":
    sys.exit(main())
