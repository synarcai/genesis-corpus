#!/usr/bin/env python3
"""[THE NUMBER'S PHRASE COURT] — the number that hangs on a form, not on a digit; CLOSED WORLD.

The measure of the executor (d5, band p156) named the debt exactly: of 423 tacts where the reader
does not read a number, 409 carry PLAIN DIGITS. The trouble is not the shape of the number but the
shape of the PHRASE it hangs on — «the first chapter is 48 pages long», «41 children were riding»,
«36 more but 33 fewer». The court recomputes the whole page in each of the four frames
(tools/numphrase.py):

  обладание  — the measure as what the text HAS («the first chapter has 48 pages»);
  длина      — THE SAME FACT as a PREDICATE OF LENGTH («is 48 pages long»), shown in all nine
               languages beside the first, so the market cannot buy one shape and miss the other.
               In both, the answer must repeat the number IN THE SAME COUNT FORM the language
               gives it («48 stron», never «48 strony»), and each form carries ITS OWN question —
               «how many pages does it have?» is not «how long is it?»;
  прогрессив — the number governs the VERB, and the form is asked of the LANGUAGE PACK, not of the
               last digit: eleven ends in one and takes the plural, twenty-one does not. The verb
               is judged ONLY in a language that moves it (Russian alone of the nine); marking the
               other eight would call an honest English page a lie and would catch a mutant FOR
               FREE, by its number rather than by its damage;
  двойное    — two comparisons of OPPOSITE direction, where the second number must not be dragged
               in the direction of the first, and the answer must be taken from the number that
               was ASKED about.

A page that answers with a different number, drags the second number after the first, or wears a
count form belonging to another number is a lie however plain its digits look.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import numphrase as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"numphrase"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПОДСАДКИ ПИСАНЫ ПОРЧЕЙ ЖИВЫХ СТРАНИЦ (М-483), и каждая ловится СВОЕЙ порчей. ОБЕ ФОРМЫ
    # ДЛИНЫ ПОДСАЖЕНЫ ПОРОЗНЬ: суд, проверенный на одной, не проверен на другой. По порядку:
    # обладание — ответ назвал другое число; длина — ответ назвал другое число; длина —
    # счётная форма страниц от чужого числа; русский глагол в единственном при 35; ЛОВУШКА
    # ПОСЛЕДНЕЙ ЦИФРЫ — одиннадцать в единственном; ответ о детях разошёлся с фразой; второе
    # число потянулось за первым; ответ взят у второго числа, а спрошено о первом; счётная
    # форма товара от чужого числа.
    подсадки = (
        "в первой главе 48 страниц. сколько страниц в первой главе? 96 страниц.",
        "the first chapter is 124 pages long. how long is the first chapter? 96 pages.",
        "pierwszy rozdział ma 48 strony długości. jakiej długości jest pierwszy rozdział? 48 stron.",
        "35 детей катался на карусели. сколько детей каталось на карусели? 35 детей.",
        "11 детей катался на карусели. сколько детей каталось на карусели? 11 детей.",
        "29 Kinder fuhren Karussell. wie viele Kinder fuhren Karussell? 42 Kinder.",
        "ann has 12 books more but 12 pencils fewer. how many more books? 12 books.",
        "у Ани на 8 книг больше, но на 5 карандашей меньше. на сколько книг больше? 5 книг.",
        "anna ma 12 książki więcej, ale 7 ołówków mniej. ile książek więcej? 12 książek.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"ФРАЗА ЧИСЛА FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    # ЧЕСТНАЯ СТРАНИЦА НЕДВИЖУЩЕГО ЯЗЫКА С ЧИСЛОМ ВНЕ ОБЪЯВЛЕННОГО НАБОРА НЕ ЕСТЬ ЛОЖЬ.
    # Рубеж стоит здесь, а не только в доме: суд, ловящий по свободному числу, ловит и правду.
    свободные = []
    for язык in F.ЯЗЫКИ:
        if язык in F.ДВИЖУЩИЕ:
            continue
        for n in (52, 7, 11):
            честная = F.страница(язык, "прогрессив", n)
            сохр = F.ПОКАЗЫ.pop(честная, None)
            вердикт = _судить(честная)
            if сохр is not None:
                F.ПОКАЗЫ[честная] = сохр
            if вердикт != (True, True):
                свободные.append((язык, n, вердикт, честная))
    if свободные:
        for язык, n, вердикт, честная in свободные[:5]:
            print(f"  СВОБОДНОЕ ЧИСЛО {язык} n={n} {вердикт}: {честная[:120]}")
        print(f"ФРАЗА ЧИСЛА FAIL: честных страниц названо ложью {len(свободные)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_numphrase.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_numphrase.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_numphrase.txt по имени")
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
    print(f"ФРАЗА ЧИСЛА {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}, "
          f"свободного числа нет ({len(F.ДВИЖУЩИЕ)} язык двигает глагол из {len(F.ЯЗЫКИ)})")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
