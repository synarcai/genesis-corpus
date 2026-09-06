#!/usr/bin/env python3
"""[THE ACTING RELATIVE COURT] — a bearer that is not a name, and that ACTS; CLOSED WORLD.

The census that bought the house (tools/kinbearer.py): the relative stands in the свод as a
HOLDER — «her mother has 5 coins», «у её матери 5 монет», 64 lines — and NEVER acts. Zero lines
in all nine languages carry «her dad gave», «её мама дала», «sa mère a donné», «ihr Vater gab»,
«jej tata dał». A bearer met only in one role is not a bearer.

The court recomputes the whole page in each of the four frames:

  дар        — the relative gives; the ledger ADDS and the answer is its total, in the count form
               the language gives that number;
  даритель   — the same page, and the question asks WHO. The answer must be the bearer THAT
               ACTED — not the other relative, and not a word the house never declared;
  отдача     — the girl gives TO the relative: the bearer wears the RECIPIENT'S case («своей
               маме», «ihrem Vater», «swojemu tacie»), the ledger SUBTRACTS, and giving more than
               one has is refused;
  двое       — both relatives give in one page, and they must be TWO: a page naming the same
               relative twice is a lie about who acted. The ledger has two steps and the second
               stands on the first.

THE VERB IS AGREED WITH THE RELATIVE'S GENDER where the language moves it (Russian «её мама дала»
against «её папа дал», Polish «dała» against «dał»); the verb of the girl's own giving is HERS
and never the relative's. The bearer's cell of the pattern admits only a DECLARED relative, so a
page whose bearer is some other word is not judged true by accident.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import kinbearer as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"kinbearer"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПОДСАДКИ ПИСАНЫ ПОРЧЕЙ ЖИВЫХ СТРАНИЦ (М-483), каждая ловится СВОЕЙ порчей: леджер не
    # сходится; ответ не есть итог леджера; ответ о дарителе назвал другого носителя; глагол не
    # согласован с родом родственника; вычитание обращено; счётная форма товара от чужого числа;
    # второй шаг не опирается на первый; два носителя слились в одного; ответ о дарителе не тот.
    подсадки = (
        "у Ани было 5 книг. её папа дал ей ещё 4 книги. сколько книг у Ани теперь? 9 книг: 5 + 4 = 10.",
        "Ann had 12 books. her mom gave her 7 books. how many books does Ann have now? 18 books: 12 + 7 = 19.",
        "Anna hatte 5 Bücher. ihr Vater gab ihr noch 4 Bücher. wer gab Anna die Bücher? ihre Mutter.",
        "у Ани было 5 книг. её мама дал ей ещё 4 книги. сколько книг у Ани теперь? 9 книг: 5 + 4 = 9.",
        "Maria miała 9 ołówków. ona dała swojemu tacie 3 ołówki. ile ołówków ma Maria teraz? 6 ołówków: 3 − 9 = 6.",
        "у Ани было 9 книг. она дала своей маме 3 книги. сколько книг у Ани теперь? 6 книги: 9 − 3 = 6.",
        "Giulia aveva 2 libri. sua madre le ha dato 3 libri e suo padre le ha dato 4 libri. quanti libri ha Giulia adesso? 9 libri: 2 + 3 = 5, 2 + 4 = 9.",
        "Lotte had 6 boeken. haar moeder gaf haar 5 boeken en haar moeder gaf haar 7 boeken. hoeveel boeken heeft Lotte nu? 18 boeken: 6 + 5 = 11, 11 + 7 = 18.",
        "Ana tenía 20 lápices. su madre le dio 15 lápices más. ¿quién le dio los lápices a Ana? su padre.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"РОДСТВЕННИК FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    # НОСИТЕЛЬ НЕ СВОБОДЕН: ячейка родителя принимает только ОБЪЯВЛЕННОЕ слово.
    # Рубеж стоит здесь, а не только в доме: суд, принимающий любое слово на месте носителя,
    # назвал бы истиной страницу, где действует кто угодно, — и «носитель» стал бы украшением.
    свободные = []
    for язык in F.ЯЗЫКИ:
        честная = F.страница(язык, "дар", 1, "отец", (5, 4))
        if _судить(честная) != (True, True):
            свободные.append(("честная не истинна", язык, честная)); continue
        for чужое in ("её сосед", "her neighbour", "der Mann", "quelqu'un"):
            битая = честная.replace(F.РЕЧЬ[язык]["родитель"]["отец"], чужое, 1)
            if битая != честная and _судить(битая)[1]:
                свободные.append(("чужое слово принято носителем", язык, битая))
    if свободные:
        for почему, язык, стр in свободные[:5]:
            print(f"  НОСИТЕЛЬ {язык} — {почему}: {стр[:120]}")
        print(f"РОДСТВЕННИК FAIL: рубежей носителя нарушено {len(свободные)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_kinbearer.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_kinbearer.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_kinbearer.txt по имени")
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
    print(f"РОДСТВЕННИК {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}, "
          f"носитель не свободен ({len(F.ЯЗЫКИ)} языков × 4 чужих слова)")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
