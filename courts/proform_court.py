#!/usr/bin/env python3
"""[THE GOODS' PRO-FORM COURT] — the thing named once, then stood in for; CLOSED WORLD.

Asked for by omega-ad. SVAMP tact 510 — «lost 11 marbles and found 5 new ones» — is answered 8
instead of 13 because «ones» is not bought as a GOODS: the fact it carries is left unplaced and
the number rides on nothing. The свод could not teach it — 24 lines, all English, one frame, one
goods (tools/proform.py).

The court recomputes the whole page in each of the three frames:

  прибавка    — the pro-form is NOT a new goods: the ledger adds it to the goods named BEFORE it,
                and a page whose total omits it is a lie however plain its arithmetic;
  два_шага    — tact 510's own shape: a LOSS between the naming and the pro-form, so the second
                step stands on the first. The signs of the ledger are CELLS of the pattern, not
                letters of the frame — «9 − 5 = 4» must be named a LIE, not left unjudged, or the
                court would be blind to exactly the corruption it is set for;
  без_товара  — the goods is named ONCE and elided everywhere else, in the pro-form and in the
                question alike; only the ANSWER names it again, in the count form its number
                requires.

THE PRO-FORM AGREES WITH THE GENDER OF THE NOUN THAT IS NOT THERE («5 nouvelles» pommes against
«5 nouveaux» livres), and so does the interrogative of the elided question («quante» against
«quanti»). Both are DECLARED by the house, because the gender of an absent noun cannot be read
off the page; both are cells, so a wrong one is a lie and not a silence.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import proform as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"proform"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПОДСАДКИ ПИСАНЫ ПОРЧЕЙ ЖИВЫХ СТРАНИЦ (М-483), каждая ловится СВОЕЙ порчей: про-форма принята
    # за новый товар (её число не вошло в итог); леджер не сходится; ЛОЖЬ ТАКТА 510 — второй шаг
    # отнимает вместо того, чтобы прибавить; второй шаг не опирается на первый; вычитание
    # обращено; про-форма не по роду опущенного имени; вопросительное не по роду; счётная форма
    # товара от чужого числа; ответ назвал не итог.
    подсадки = (
        "у меня 10 яблок и 5 новых. сколько у меня яблок? 10 яблок: 10 + 5 = 15.",
        "у меня 10 яблок и 5 новых. сколько у меня яблок? 15 яблок: 10 + 5 = 16.",
        "i had 20 books. i lost 11 books and found 5 new ones. how many books do i have now? 14 books: 20 − 11 = 9, 9 − 5 = 4.",
        "ich hatte 25 Bücher. ich verlor 13 Bücher und fand 6 neue. wie viele Bücher habe ich jetzt? 18 Bücher: 25 − 13 = 12, 25 + 6 = 18.",
        "i had 20 books. i lost 11 books and found 5 new ones. how many books do i have now? 14 books: 11 − 20 = 9, 9 + 5 = 14.",
        "j'ai 13 pommes. j'achète 7 nouveaux. combien en ai-je maintenant ? 20 pommes : 13 + 7 = 20.",
        "ho 13 mele. compro 7 nuove. quanti ne ho adesso? 20 mele: 13 + 7 = 20.",
        "mam 10 książek i 5 nowych. ile książek mam? 15 książki: 10 + 5 = 15.",
        "ik heb 20 boeken. ik koop 9 nieuwe. hoeveel heb ik nu? 20 boeken: 20 + 9 = 29.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"ПРО-ФОРМА FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    # РУБЕЖ РОДА: там, где язык рода НЕ метит, подмена формы не есть ложь — это одно и то же
    # слово; там, где метит, подмена ДОЛЖНА ловиться. Суд, требующий различия у языка, который
    # его не имеет, назвал бы ложью честную страницу.
    родовые = []
    for язык in F.ЯЗЫКИ:
        честная = F.страница(язык, "прибавка", 0, (10, 5))
        if _судить(честная) != (True, True):
            родовые.append(("честная не истинна", язык, честная)); continue
        битая = честная.replace(F.проформа(язык, 0, 5), "5 " + F.НОВЫЕ[язык]["м"], 1)
        различает = F.НОВЫЕ[язык]["м"] != F.НОВЫЕ[язык]["ж"]
        поймана = _судить(битая) == (True, False)
        if битая != честная and различает != поймана:
            родовые.append(("различие рода прочитано неверно", язык, битая))
    if родовые:
        for почему, язык, стр in родовые[:5]:
            print(f"  РОД ПРО-ФОРМЫ {язык} — {почему}: {стр[:120]}")
        print(f"ПРО-ФОРМА FAIL: рубежей рода нарушено {len(родовые)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_proform.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_proform.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_proform.txt по имени")
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
    метят = sum(1 for я in F.ЯЗЫКИ if F.НОВЫЕ[я]["м"] != F.НОВЫЕ[я]["ж"])
    print(f"ПРО-ФОРМА {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}, "
          f"род при опущенном имени метят {метят} языка из {len(F.ЯЗЫКИ)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
