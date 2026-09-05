#!/usr/bin/env python3
"""[СВОД СПРАШИВАЕТ СЕБЯ] — the canon asks its own questions of the reader forged on it.

THE MEASURE THAT NEEDS NO FOREIGN BAND. Every «question? answer.» line of the
canon whose answer carries a number is a question the reader has SEEN with its
answer; one question per distinct skeleton (numbers → #) is sampled and put to
the reader in --pipe mode; the certified answers are judged BY VALUE against
the canon's own answer. Three outcomes, two of them named debts:
  · RIGHT — certified and the value agrees;
  · LIE   — certified and the value disagrees — the DEFECT (rubric: zero);
  · MUTE  — refused — not a defect but the PLAN: the mute CLASSES (language ×
            head, names masked) by size say what the next point of the canon
            must close (the owner's word, 05.09: «каждая точка закрывает
            крупнейший немой класс форм по языкам»).

THE VALUE IS JUDGED THREE WAYS, AND THE FIRST JUDGE'S TWO BLIND SPOTS ARE
CLOSED (holon, sixth point: an answer with several numbers — «38 рублей 80
копеек» — was judged by its LAST number; a grid answer has no number at all):
  · the reader's answer, normalised, is a piece of the canon's answer (grids,
    words: «grid … shifted down by 2 is ___/___»);
  · every DISTINCT number of the canon's answer stands in the reader's answer
    («45 − 18 = 27. portanto a resposta é 27.» against «45 − 18 = 27»);
  · a canon answer without numbers is compared as text.
A lie under this judge is a lie in VALUE, not in layout.

THE ROSTER READS THE LAST SWEEP, IT DOES NOT FORGE. A sweep needs a reader
state (a forge of the point) and minutes of replies; the suite of courts runs
in seconds. So «judge» writes its verdict to reports/sweep/latest.tsv and the
suite's entry (`sweep_self.py roster`) re-reads that verdict: the point's
sweep is the gate of the point, and its absence is refused aloud, not passed.

WHAT IS NOT MEASURED, NAMED: whether the answer's explanation is sound —
only its value; whether the question is well-posed — the canon's courts judge
that at the world's birth.

usage:
  sweep_self.py gen   CANON N SEED OUTDIR      → OUTDIR/sweep_q.txt, OUTDIR/sweep_key.tsv
  sweep_self.py judge KEY RUN_OUT [--классов K] [--метка ИМЯ] [--в ПУТЬ]
                                               → verdict; writes reports/sweep/latest.tsv
                                                 (or ПУТЬ: a world's sweep must not
                                                 overwrite the point's verdict)
  sweep_self.py roster                         → re-reads the last verdict for the suite
"""
import collections
import json
import pathlib
import random
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))

# РУБЕЖ-ДОЛГА: ЛЖИ_РУБЕЖ = 0
ЛЖИ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: judge no-such-key.tsv no-such-run.out
ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
ВОПРОС = re.compile(r"^([^?\n]{8,160}\?)\s+(.{1,160})$")
ЧИСЛО = re.compile(r"-?\d+(?:[.,]\d+)?")
СЛОВО = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)?")
ПОСЛЕДНИЙ = КОРЕНЬ / "reports" / "sweep" / "latest.tsv"
_ПИСЬМО = (("ru", re.compile(r"[а-яё]")), ("pl", re.compile(r"[ąęłńśźż]")), ("es", re.compile(r"[¿¡ñ]")),
           ("pt", re.compile(r"[ãõç]")), ("de", re.compile(r"[ßü]")))
_МЕТКИ = (("de", re.compile(r"\b(?:wie|ist|hat|hatte|welche[rs]?)\b")),
          ("fr", re.compile(r"\b(?:combien|quel(?:le)?s?|est-ce|il y a|avait|reste)\b")),
          ("it", re.compile(r"\b(?:quant[iea]|qual[ei]|è|aveva|sono)\b")),
          ("pt", re.compile(r"\b(?:quant[oa]s?|tinha|tem|restam|ficam)\b")),
          ("es", re.compile(r"\b(?:cuánt[oa]s?|tiene|tenía|quedan)\b")),
          ("nl", re.compile(r"\b(?:hoeveel|welke|heeft|had|zijn er|is er)\b")),
          ("pl", re.compile(r"\b(?:ile|ilu|ma|miała?|jest)\b")),
          ("en", re.compile(r"\b(?:how|what|which|does|do|is|are|has|had)\b")))


def _пакеты():
    """Declared openers and person names per language — the corpus's own knowledge."""
    зачины, имена = {}, set()
    for я in ЯЗЫКИ:
        п = КОРЕНЬ / "tools" / "langpacks" / f"{я}.json"
        if not п.is_file():
            continue
        пак = json.loads(п.read_text(encoding="utf-8"))
        сл = pак_слова(пак)
        зачины[я] = (frozenset(сл), (пак.get("ask_words") or {}).get("position", "front"))
        for имя in пак.get("person_names") or ():
            имена.add(str(имя).lower())
        for имя, формы in (пак.get("person_forms") or {}).items():
            имена.add(str(имя).lower())
            if isinstance(формы, dict):
                for к, ф in формы.items():
                    if к != "gender" and isinstance(ф, str):
                        имена.add(ф.lower())
    return зачины, frozenset(имена)


def pак_слова(пак):
    return [с.lower() for с in (пак.get("ask_words") or {}).get("words", ()) if с != "¬"]


ЗАЧИНЫ, ИМЕНА = _пакеты()


def язык(вопрос):
    """Script signature first, then the declared openers (front word, then any word), then
    marker words of the first judge; «other» is a named remainder, never a guess."""
    низ = вопрос.lower()
    for я, знак in _ПИСЬМО:
        if знак.search(низ):
            return я
    слова = СЛОВО.findall(низ)
    первое = слова[0] if слова else ""
    спереди = [я for я, (набор, где) in ЗАЧИНЫ.items() if первое in набор]
    if len(спереди) == 1:
        return спереди[0]
    внутри = collections.Counter(я for с in слова for я, (набор, _) in ЗАЧИНЫ.items() if с in набор)
    метки = [я for я, знак in _МЕТКИ if знак.search(низ)]
    кандидаты = спереди or [я for я in ЯЗЫКИ if внутри[я]]
    if len(кандидаты) == 1:
        return кандидаты[0]
    for я in метки:
        if not кандидаты or я in кандидаты:
            return я
    return кандидаты[0] if кандидаты else "other"


def скелет(вопрос):
    return re.sub(r"\d+", "#", вопрос.lower())


def голова(вопрос):
    """The class of a question: its first two words with names masked to X and numbers to #."""
    куски = re.findall(r"[^\W\d_]+(?:['’][^\W\d_]+)?|\d+", вопрос.lower())
    if len(куски) > 1 and куски[0] in ("o", "a") and куски[1] in ИМЕНА:
        куски = куски[1:]          # the Portuguese article before a name is the name's
    вон = []
    for к in куски[:3]:
        вон.append("#" if к.isdigit() else "X" if к in ИМЕНА else к)
        if len(вон) == 2:
            break
    return " ".join(вон)


def gen(канон, n, семя, куда):
    random.seed(семя)
    по_скелету = {}
    with open(канон, encoding="utf-8", errors="replace") as f:
        for л in f:
            м = ВОПРОС.match(л.rstrip("\n"))
            if not м:
                continue
            в, о = м.group(1), м.group(2)
            if not ЧИСЛО.search(о) or not re.search(r"\d", в):
                continue
            по_скелету.setdefault(скелет(в), (в, о))
    ряд = list(по_скелету.items())
    random.shuffle(ряд)
    выборка = ряд[:n]
    куда = pathlib.Path(куда); куда.mkdir(parents=True, exist_ok=True)
    (куда / "sweep_q.txt").write_text("".join(в + "\n" for _, (в, о) in выборка), encoding="utf-8")
    (куда / "sweep_key.tsv").write_text(
        "".join(f"{язык(в)}\t{в}\t{о}\n" for _, (в, о) in выборка), encoding="utf-8")
    по_языку = collections.Counter(язык(в) for _, (в, о) in выборка)
    print(f"СВОД СПРАШИВАЕТ СЕБЯ: скелетов {len(по_скелету)}, выбрано {len(выборка)}; "
          "по языкам: " + " ".join(f"{я} {к}" for я, к in по_языку.most_common()))
    return 0


def _числа(текст):
    return {round(float(ч.replace(",", ".")), 6) for ч in ЧИСЛО.findall(str(текст).replace("−", "-"))}


def _текст(т):
    return re.sub(r"\s+", " ", str(т).replace("−", "-").strip().lower()).rstrip(". ")


def верно(ответ_канона, ответ_читателя):
    канон, чит = _текст(ответ_канона), _текст(ответ_читателя)
    if чит and чит in канон:
        return True
    надо, есть = _числа(ответ_канона), _числа(ответ_читателя)
    if not надо:
        return канон == чит
    return надо <= есть


def _ключ(путь):
    ряд = []
    for л in путь.read_text(encoding="utf-8").splitlines():
        ч = л.rstrip("\n").split("\t")
        if len(ч) != 3:
            continue
        # ключ первого судьи (значение, вопрос, ответ) читается тоже: язык выводится из вопроса
        ряд.append((ч[0], ч[1], ч[2]) if ч[0] in ЯЗЫКИ + ("other",) else (язык(ч[1]), ч[1], ч[2]))
    return ряд


def _ответы(путь):
    вон, json_есть = {}, False
    with open(путь, encoding="utf-8", errors="replace") as f:
        for л in f:
            if not л.startswith("{"):
                continue
            try:
                j = json.loads(л)
            except ValueError:
                continue
            json_есть = True
            c = j.get("compute")
            if isinstance(c, dict) and c.get("verdict") == "certified" and j.get("reply_id") is not None:
                вон[int(j["reply_id"])] = str(c.get("answer", ""))
    return вон, json_есть


def _вердикт(строки, классов, метка):
    верных = лжей = 0; лжи = []; всего = collections.Counter(); ок = collections.Counter()
    немые = collections.Counter()
    for я, в, о, исход, ответ in строки:
        всего[я] += 1
        if исход == "верно":
            верных += 1; ок[я] += 1
        elif исход == "ложь":
            лжей += 1
            if len(лжи) < 20:
                лжи.append(f"{я} {в[:80]} → {ответ[:40]} · надо {о[:40]}")
        else:
            немые[(я, голова(в))] += 1
    немых = sum(1 for с in строки if с[3] == "немо")
    поза = "PASS" if лжей <= ЛЖИ_РУБЕЖ else "FAIL"
    print(f"СВОД СПРАШИВАЕТ СЕБЯ {поза} [{метка}]: сертифицировано {верных + лжей} из {len(строки)}, "
          f"верных {верных}, ЛЖЕЙ {лжей} (рубеж {ЛЖИ_РУБЕЖ}), немых {немых}")
    print("  по языкам (верно/всего): " + " ".join(f"{я} {ок[я]}/{к}" for я, к in всего.most_common()))
    for л in лжи:
        print(f"  ЛОЖЬ {л}")
    print(f"  немые классы (язык · голова · вопросов), крупнейшие {классов}:")
    for (я, г), к in немые.most_common(классов):
        print(f"    {я} · {г} · {к}")
    return 0 if поза == "PASS" else 1


def judge(ключ, прогон, классов=12, метка="sweep", куда=None):
    ключ, прогон = pathlib.Path(ключ), pathlib.Path(прогон)
    if not ключ.is_file() or not прогон.is_file():
        print(f"СВОД СПРАШИВАЕТ СЕБЯ ОТКАЗ: нет ключа или прогона ({ключ.name}, {прогон.name})")
        return 2
    ряд = _ключ(ключ)
    ответы, json_есть = _ответы(прогон)
    if not ряд or not json_есть:
        print("СВОД СПРАШИВАЕТ СЕБЯ ОТКАЗ: прогон без JSON читателя или пустой ключ — пустой обход, не немота")
        return 2
    строки = []
    for i, (я, в, о) in enumerate(ряд, 1):
        if i in ответы:
            строки.append((я, в, о, "верно" if верно(о, ответы[i]) else "ложь", ответы[i]))
        else:
            строки.append((я, в, о, "немо", ""))
    куда = pathlib.Path(куда) if куда else ПОСЛЕДНИЙ
    куда.parent.mkdir(parents=True, exist_ok=True)
    куда.write_text(f"# метка\t{метка}\n" + "".join(
        f"{я}\t{исход}\t{в}\t{о}\t{ответ}\n" for я, в, о, исход, ответ in строки), encoding="utf-8")
    return _вердикт(строки, классов, метка)


def roster(классов=8):
    if not ПОСЛЕДНИЙ.is_file():
        print(f"СВОД СПРАШИВАЕТ СЕБЯ ОТКАЗ: последнего свипа нет ({ПОСЛЕДНИЙ.relative_to(КОРЕНЬ)}) — "
              "точка без свипа не судилась")
        return 2
    метка, строки = "?", []
    for л in ПОСЛЕДНИЙ.read_text(encoding="utf-8").splitlines():
        if л.startswith("# метка\t"):
            метка = л.split("\t", 1)[1]; continue
        ч = л.split("\t")
        if len(ч) == 5:
            строки.append((ч[0], ч[2], ч[3], ч[1], ч[4]))
    if not строки:
        print("СВОД СПРАШИВАЕТ СЕБЯ ОТКАЗ: последний свип пуст")
        return 2
    return _вердикт(строки, классов, метка)


def main(argv):
    if len(argv) >= 5 and argv[0] == "gen":
        return gen(argv[1], int(argv[2]), int(argv[3]), argv[4])
    if len(argv) >= 3 and argv[0] == "judge":
        классов = int(argv[argv.index("--классов") + 1]) if "--классов" in argv else 12
        метка = argv[argv.index("--метка") + 1] if "--метка" in argv else "sweep"
        куда = argv[argv.index("--в") + 1] if "--в" in argv else None
        return judge(argv[1], argv[2], классов, метка, куда)
    if argv and argv[0] == "roster":
        return roster()
    print(__doc__.split("usage:")[1])
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
