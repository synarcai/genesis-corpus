#!/usr/bin/env python3
"""[SELF-MODEL COURT] — the answer comes from the ledger, never from the prediction; CLOSED WORLD.

A show of the self-model world (tools/selfmodelforms.py) is one turn of the φ-cycle named in
Д-2: a PREDICTION about one's own answer, the answer itself, and the verdict on the prediction
— «the prediction came true», «the prediction did not come true: i thought 9, and the answer is
8», «by how much was i wrong? by 1: 9 − 8 = 1» — and the page that predicts its own silence
and gets it right.

The court reads each line back through the house's frames. A page is true when the tape's
ledger recomputes AND THE ANSWER EQUALS THE LEDGER — a page whose answer follows its own
prediction is a lie, and that is Campbell's shield written as a court: a self-estimate may be
measured and may be wrong, but it never enters the court of truth. Further: a «came true»
stands only over a prediction equal to the answer, a «did not come true» only over one that
differs, the size of an error recomputes by subtraction and is not nought, each count form is
the form of ITS number, and the copula of a place bends with the number it stands at. A line
of a frame that breaks any of these is a lie; a line of no frame is a lie of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import selfmodelforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"selfmodelforms"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): ответ пошёл за предсказанием, а не за леджером (главная
    # ложь этого дома и ровно то, что запрещает щит Кэмпбелла); «сбылось» над разошедшимся
    # предсказанием; «не сбылось» над совпавшим; размер ошибки не сходится; ошибка объявлена
    # нулём; счётная форма чужого числа.
    подсадки = (
        "there are 5 files in the folder. the first act creates 3 files. i thought 9, and the answer is 8. what is true? there are 9 files in the folder: 5 + 3 = 9. my thought does not change the fact.",
        "there are 5 files in the folder. the first act creates 3 files. i think i will answer 9. how many files are in the folder? there are 9 files in the folder: 5 + 3 = 9. the prediction came true.",
        "there are 5 files in the folder. the first act creates 3 files. i think i will answer 8. how many files are in the folder? there are 8 files in the folder: 5 + 3 = 8. the prediction did not come true: i thought 8, and the answer is 8.",
        "there are 5 files in the folder. the first act creates 3 files. i think i will answer 10. how many files are in the folder? there are 8 files in the folder: 5 + 3 = 8. by how much was i wrong? by 3: 10 − 8 = 3.",
        "в папке 5 файлов. первый акт создаёт 3 файла. я думаю, что отвечу 9. сколько файлов в папке? в папке 9 файлов: 5 + 3 = 9. предсказание сбылось.",
        "в папке 5 файлов. первый акт создаёт 3 файла. я думал 9, а ответ 8. что верно? в папке 9 файлов: 5 + 3 = 9. моя мысль факта не меняет.",
        "w folderze jest 5 plików. pierwszy akt tworzy 3 pliki. myślę, że odpowiem 9. ile plików jest w folderze? w folderze jest 8 plików: 5 + 3 = 9. przewidywanie się nie sprawdziło: myślałem 9, a odpowiedź to 8.",
        "im Ordner sind 5 Dateien. der erste Akt erstellt 3 Dateien. ich denke, ich werde 10 antworten. wie viele Dateien sind im Ordner? im Ordner sind 8 Dateien: 5 + 3 = 8. wie viel war mein Fehler? 1: 10 − 8 = 1.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:170]}")
        print(f"САМОМОДЕЛЬ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_selfmodelforms.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_selfmodelforms.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_selfmodelforms.txt по имени")
    for путь in пути:
        for стр in путь.read_text(encoding="utf-8").splitlines():
            if not стр.strip() or стр.startswith("\x0c"):
                continue
            судимо, истинно = _судить(стр)
            итог["судимых" if судимо else "несудимых"] += 1
            if судимо and not истинно:
                итог["ложных"] += 1
                if len(примеры) < 5:
                    примеры.append(стр)
    for п in примеры:
        print(f"  ЛОЖЬ: {п[:170]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"САМОМОДЕЛЬ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
