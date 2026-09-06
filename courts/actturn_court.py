#!/usr/bin/env python3
"""[DIALOGUE ACT COURT] — the organism's own turn, sealed by the folder's number; CLOSED WORLD.

A show of the act world (tools/actturn.py) is a whole turn: the user's order, the organism's
proposal with a request to confirm, the user's word, and the report — with the folder counted
again. The court recomputes the count from the ACT: creation adds exactly one, deletion takes
one, reading and editing move nothing, and a REFUSAL moves nothing either. That last is the
seam the demo stands on: a refusal that changed the world would be a lie visible in arithmetic.
The court also demands ONE act and ONE file per turn — the order, the proposal and the report
must speak of the same thing — and refuses a turn the world does not allow (deleting from an
empty folder, creating over an existing file).

Written for the release demo's sixth scene at holon's ask: the corpus said what the world is and
never showed the organism acting in it.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import actturn as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"actturn"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): отчёт БЕЗ подтверждения; папка не пересчитана после
    # создания; ОТКАЗ СДВИНУЛ МИР; чужой файл в отчёте; два рода акта в одном ходе; чтение
    # прибавило файл; невозможный акт объявлен над пустой папкой; удаление из пустой папки.
    подсадки = (
        "пользователь: создай файл b.txt. организм: предлагаю создать файл b.txt. подтверждено ли это? организм: создал файл b.txt. папка содержит 4 файла: 3 + 1 = 4.",
        "user: create the file a.txt. organism: i propose to create the file a.txt. is that confirmed? user: yes. organism: created the file a.txt. the folder contains 3 files: 3 + 1 = 3.",
        "Benutzer: erstelle die Datei a.txt. Organismus: ich schlage vor, die Datei a.txt zu erstellen. ist das bestätigt? Benutzer: nein. Organismus: keine Bestätigung — die Handlung wird nicht ausgeführt. der Ordner enthält 3 Dateien: 2 + 1 = 3.",
        "użytkownik: utwórz plik a.txt. organizm: proponuję utworzyć plik a.txt. czy to potwierdzone? użytkownik: tak. organizm: utworzyłem plik b.txt. folder zawiera 2 pliki: 1 + 1 = 2.",
        "utilisateur : supprime le fichier a.txt. organisme : je propose de supprimer le fichier a.txt. est-ce confirmé ? utilisateur : oui. organisme : j'ai créé le fichier a.txt. le dossier contient 1 fichier : 2 − 1 = 1.",
        "utente: leggi il file a.txt. organismo: propongo di leggere il file a.txt. è confermato? utente: sì. organismo: ho letto il file a.txt. il file a.txt contiene 12 byte: 7 + 5 = 12.",
        "usuario: amplía el archivo a.txt. organismo: propongo ampliar el archivo a.txt. ¿es correcto? usuario: sí. organismo: he ampliado el archivo a.txt. el archivo a.txt contiene 7 bytes: 7 = 7.",
        "gebruiker: hoeveel bestanden zitten er in de map? organisme: de map bevat 4 bestanden: 3 = 4.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"АКТ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_actturn.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_actturn.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_actturn.txt по имени")
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
        print(f"  ЛОЖЬ: {п[:150]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"АКТ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
