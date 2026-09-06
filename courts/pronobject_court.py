#!/usr/bin/env python3
"""[PRONOUN-OBJECT TRANSFER COURT] — the receiver named once, then only pointed at; CLOSED WORLD.

Asked for by holon on the measure of omega-ad. SVAMP tact 458 — «Jack gave HIM 20 marbles. Josh
had 22 before…» — is answered 22 instead of 42 because «him/her/them» are not bought as pronouns:
the market votes with the word in the ACTOR'S place, and the object's place never votes. The свод
could not teach it: «him» 12 lines, «gave her» 10 on the whole FULL (tools/pronobject.py).

The court recomputes the whole page:

  · two bearers are NAMED with their counts, and they must be TWO — the giver first, the receiver
    second, the giver of the OTHER gender, so the pronoun cannot be resolved by «the only person
    there is»;
  · the object pronoun must be the receiver's OWN, and only where the language marks it: French
    and Spanish collapse «to him» and «to her» into one word, and a court demanding a distinction
    they do not have would call their honest pages lies;
  · THE QUESTION DECIDES WHICH LEDGER IS MEANT. Asked about the giver, the ledger SUBTRACTS
    (n − m); asked about the receiver, it ADDS (k + m). The commonest lie is the giver's ledger
    written under the receiver's question — that is tact 458, and it is the first intrusion here;
  · the verbs agree: the giver's own verb with the GIVER'S gender where the language moves it
    («Marek dał» / «Maria dała»), and BOTH the having-verb and the question's verb with the
    NUMBER of the receiver — seven of the nine languages move it («hatten», «avaient», «tenían»,
    «avevano», «tinham», «hadden», «miały», and English «do» against «does»);
  · the interrogative agrees with the GOODS' GENDER where the language bends it («quanti libri»
    against «quante matite»), and it is a CELL of the pattern, not a letter of the frame, so a
    wrong one is named a LIE rather than left unjudged.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import pronobject as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"pronobject"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПОДСАДКИ ПИСАНЫ ПОРЧЕЙ ЖИВЫХ СТРАНИЦ (М-483), каждая ловится СВОЕЙ порчей: леджер отдающего
    # подставлен получателю (такт 458); леджер не сходится; вычитание обращено; местоимение чужого
    # лица; глагол отдающего не по его роду; двое получателей поставлены в единственном; вопрос об
    # одном, а ответ о другом; счётная форма товара от чужого числа; вопросительное не по роду вещи.
    подсадки = (
        "у Вани было 20 книг, а у Ани было 5 книг. Ваня дал ей 8 книг. сколько книг у Ани теперь? 12 книг: 20 − 8 = 12.",
        "у Вани было 20 книг, а у Ани было 5 книг. Ваня дал ей 8 книг. сколько книг у Вани теперь? 12 книг: 20 − 8 = 13.",
        "у Вани было 20 книг, а у Ани было 5 книг. Ваня дал ей 8 книг. сколько книг у Вани теперь? 12 книг: 8 − 20 = 12.",
        "Ben hatte 20 Bücher und Anna hatte 5 Bücher. Ben gab ihm 8 Bücher. wie viele Bücher hat Ben jetzt? 12 Bücher: 20 − 8 = 12.",
        "Marek miał 20 książek, a Maria miała 5 książek. Marek dała jej 8 książek. ile książek ma Marek teraz? 12 książek: 20 − 8 = 12.",
        "Hugo avait 20 livres et Léa et Zoé avait 5 livres. Hugo leur a donné 8 livres. combien de livres ont Léa et Zoé maintenant ? 13 livres : 5 + 8 = 13.",
        "Tom had 14 books and Ann had 3 books. Tom gave her 6 books. how many books does Kate have now? 9 books: 3 + 6 = 9.",
        "у Вани было 20 карандашей, а у Ани и Оли было 5 карандашей. Ваня дал им 8 карандашей. сколько карандашей у Ани и Оли теперь? 13 карандаша: 5 + 8 = 13.",
        "Matteo aveva 20 matite e Giulia aveva 5 matite. Matteo le ha dato 8 matite. quanti matite ha Matteo adesso? 12 matite: 20 − 8 = 12.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"МЕСТОИМЕНИЕ-ОБЪЕКТ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    # РУБЕЖ СЛИЯНИЯ РОДА: там, где язык НЕ различает «ему» и «ей», подмена одного другим
    # НЕ ЕСТЬ ЛОЖЬ — это одно и то же слово, и суд, требующий различия, назвал бы ложью
    # честную французскую и испанскую страницу. Там, где различает, подмена ДОЛЖНА ловиться.
    слияние = []
    for язык in F.ЯЗЫКИ:
        мест = F.РЕЧЬ[язык]["мест"]
        честная = F.страница(язык, "отдающий", 1, "она", 0)
        if _судить(честная) != (True, True):
            слияние.append(("честная не истинна", язык, честная)); continue
        битая = честная.replace(мест["она"], мест["он"], 1)
        поймана = _судить(битая) == (True, False)
        различает = мест["она"] != мест["он"]
        if различает != поймана and битая != честная:
            слияние.append(("различие рода прочитано неверно", язык, битая))
    if слияние:
        for почему, язык, стр in слияние[:5]:
            print(f"  СЛИЯНИЕ РОДА {язык} — {почему}: {стр[:120]}")
        print(f"МЕСТОИМЕНИЕ-ОБЪЕКТ FAIL: рубежей слияния нарушено {len(слияние)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_pronobject.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_pronobject.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_pronobject.txt по имени")
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
    различают = sum(1 for я in F.ЯЗЫКИ if F.РЕЧЬ[я]["мест"]["она"] != F.РЕЧЬ[я]["мест"]["он"])
    print(f"МЕСТОИМЕНИЕ-ОБЪЕКТ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}, "
          f"род местоимения различают {различают} языка из {len(F.ЯЗЫКИ)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
