#!/usr/bin/env python3
"""THE HOUSE OF THE EPISODE — a TAPE of acts over one state (05.09).

The house of the tool (tools/toolforms.py) shows ONE act: state before · call · state
after. An agent does not live by one act: it runs a TAPE, and the state it must answer
about is the state after the WHOLE tape — and, when asked, after any single step of it.
This house shows exactly that, and nothing more: a place holds n things, three acts follow
one another, and the question asks the count after all of them, or after the second, or
which act moved the count most, or how many acts moved it at all, or what the count was
before against what it is now.

WHAT THE HOUSE BORROWS AND WHAT IT DECLARES. Nine languages; the things of acts, their
places, the copula bent by number, the ground of a read («reading changes nothing») and the
gendered question words are BORROWED from the house of the tool by import — one
declaration, several readers, and a tape speaks of the same files and folders as a single
call. Declared here: the acts in their ordinal («the first act creates …»), the ordinal in
its after-phrase («after the second act»), the phrase of the whole tape («after all the
acts»), the words that count acts («two acts»), the words of what an act did («it added 3
files»), and the words of comparison («before 9, after 6: less»).

THE FRAME IS CONCRETE, THE JUDGE VERIFIES IT AGAINST THE NUMBERS. A page names its winner
(«the third act»), its count of changing acts («two acts») and its verdict of comparison
(«less») in the FRAME, not in a hole — so a page that names the wrong step matches the
frame of THAT step and is judged by its rule: the judge recomputes the changes and demands
that the named step be the greatest one, that the named count be the count of acts whose
change is not nought, and that the named verdict agree with the numbers. A lie therefore
cannot hide in a different reading of the same line.

THE LEDGER IS THE TAPE ITSELF. The full answer carries «n + a − b + c = v», and the answer
about the second step carries its PREFIX «n + a − b = v₂»: the state after a step is not a
new fact but a piece of the same sum, and the judge recomputes both. An act that only reads
stands in the tape without standing in the ledger — and the page that counts changing acts
says why: «reading changes nothing».

WHAT IS NOT MEASURED, NAMED: whether the acts could run in another order, and whether a real
tool would do this. The house shows the SHAPE of a tape (state, steps, state), not its
execution, and never asks what the tape MEANT — that is the neighbouring house of the plan.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import svampforms as S  # noqa: E402 — the count cell of a pack and the gendered question words
import toolforms as T  # noqa: E402 — things of acts, places, the copula, the ground of a read

ЯЗЫКИ = T.ЯЗЫКИ
НАЧАЛА = tuple(range(5, 21))     # the state a tape starts from: 5..20
ШАГИ_ЧИСЕЛ = (1, 2, 3, 4, 5, 6, 7, 8, 9)   # what one act moves

# ФИГУРЫ ЛЕНТЫ — знаки трёх актов. «0» есть акт, который только читает: он стоит в ленте,
# но не стоит в леджере.
ФИГУРЫ_ПОЛНЫЕ = (("+", "−", "+"), ("+", "+", "−"), ("−", "+", "+"))
ФИГУРЫ_С_ЧТЕНИЕМ = (("+", "0", "+"), ("0", "+", "−"), ("+", "−", "0"))
ФИГУРЫ_СРАВНЕНИЯ = (("−", "+", "−"), ("+", "−", "−"), ("+", "+", "−"))

# ПОРЯДОК АКТА В ИМЕНИТЕЛЬНОМ — подлежащее шага и имя победителя.
ПОРЯДОК = {
    "ru": ("первый акт", "второй акт", "третий акт"),
    "en": ("the first act", "the second act", "the third act"),
    "de": ("der erste Akt", "der zweite Akt", "der dritte Akt"),
    "fr": ("le premier acte", "le deuxième acte", "le troisième acte"),
    "es": ("el primer acto", "el segundo acto", "el tercer acto"),
    "it": ("il primo atto", "il secondo atto", "il terzo atto"),
    "pt": ("o primeiro ato", "o segundo ato", "o terceiro ato"),
    "nl": ("de eerste handeling", "de tweede handeling", "de derde handeling"),
    "pl": ("pierwszy akt", "drugi akt", "trzeci akt"),
}
# ПОРЯДОК АКТА В ПРЕДЛОЖНОЙ ФРАЗЕ — падеж не угадывается, он написан.
ПОСЛЕ_ШАГА = {
    "ru": ("после первого акта", "после второго акта", "после третьего акта"),
    "en": ("after the first act", "after the second act", "after the third act"),
    "de": ("nach dem ersten Akt", "nach dem zweiten Akt", "nach dem dritten Akt"),
    "fr": ("après le premier acte", "après le deuxième acte", "après le troisième acte"),
    "es": ("después del primer acto", "después del segundo acto", "después del tercer acto"),
    "it": ("dopo il primo atto", "dopo il secondo atto", "dopo il terzo atto"),
    "pt": ("depois do primeiro ato", "depois do segundo ato", "depois do terceiro ato"),
    "nl": ("na de eerste handeling", "na de tweede handeling", "na de derde handeling"),
    "pl": ("po pierwszym akcie", "po drugim akcie", "po trzecim akcie"),
}
ПОСЛЕ_ВСЕХ = {
    "ru": "после всех актов", "en": "after all the acts", "de": "nach allen Akten",
    "fr": "après tous les actes", "es": "después de todos los actos", "it": "dopo tutti gli atti",
    "pt": "depois de todos os atos", "nl": "na alle handelingen", "pl": "po wszystkich aktach",
}
# СЧЁТ АКТОВ СЛОВОМ — ответ о том, сколько актов двинули счёт.
АКТОВ = {
    "ru": {1: "один акт", 2: "два акта", 3: "три акта"},
    "en": {1: "one act", 2: "two acts", 3: "three acts"},
    "de": {1: "ein Akt", 2: "zwei Akte", 3: "drei Akte"},
    "fr": {1: "un acte", 2: "deux actes", 3: "trois actes"},
    "es": {1: "un acto", 2: "dos actos", 3: "tres actos"},
    "it": {1: "un atto", 2: "due atti", 3: "tre atti"},
    "pt": {1: "um ato", 2: "dois atos", 3: "três atos"},
    "nl": {1: "één handeling", 2: "twee handelingen", 3: "drie handelingen"},
    "pl": {1: "jeden akt", 2: "dwa akty", 3: "trzy akty"},
}
# СЛОВА СРАВНЕНИЯ — вердикт «стало больше / стало меньше».
СРАВНЕНИЕ = {
    "ru": {"+": "больше", "−": "меньше"}, "en": {"+": "more", "−": "less"},
    "de": {"+": "mehr", "−": "weniger"}, "fr": {"+": "plus", "−": "moins"},
    "es": {"+": "más", "−": "menos"}, "it": {"+": "di più", "−": "di meno"},
    "pt": {"+": "mais", "−": "menos"}, "nl": {"+": "meer", "−": "minder"},
    "pl": {"+": "więcej", "−": "mniej"},
}
# РЕЧЬ ДОМА — по одной строке на каждый кусок страницы; всё, чего нет у соседей.
РЕЧЬ = {
    "ru": dict(
        начало="{М} {n} {Тn}.",
        состояние="{М} {v} {Тv}",
        шаг_плюс="{П} создаёт {m} {Тm}.",
        шаг_минус="{П} удаляет {m} {Тm}.",
        шаг_чтение="{П} только читает.",
        вопрос_лента="сколько {Тмн} {М} {ВСЕ}?",
        вопрос_шаг="сколько {Тмн} {М} {ШАГ}?",
        ответ_шаг="{ШАГ} {М} {v} {Тv}",
        вопрос_какой="какой акт изменил счёт больше всех?",
        ответ_ничья="{ПA} и {ПB} поровну: по {mp} {Тmp}.",
        дело_плюс="он добавил {mp} {Тmp}",
        дело_минус="он убрал {mp} {Тmp}",
        вопрос_сколько="сколько актов изменили счёт?",
        вопрос_сравнение="сколько было и сколько стало?",
        ответ_сравнение="было {n}, стало {v}: {СРАВ}."),
    "en": dict(
        начало="{ЕСТЬn} {n} {Тn} {М}.",
        состояние="{ЕСТЬv} {v} {Тv} {М}",
        шаг_плюс="{П} creates {m} {Тm}.",
        шаг_минус="{П} deletes {m} {Тm}.",
        шаг_чтение="{П} only reads.",
        вопрос_лента="how many {Тмн} are {М} {ВСЕ}?",
        вопрос_шаг="how many {Тмн} are {М} {ШАГ}?",
        ответ_шаг="{ШАГ} {ЕСТЬv} {v} {Тv} {М}",
        вопрос_какой="which act changed the count most?",
        ответ_ничья="{ПA} and {ПB} equally: {mp} {Тmp} each.",
        дело_плюс="it added {mp} {Тmp}",
        дело_минус="it deleted {mp} {Тmp}",
        вопрос_сколько="how many acts changed the count?",
        вопрос_сравнение="how many were there before and after?",
        ответ_сравнение="before {n}, after {v}: {СРАВ}."),
    "de": dict(
        начало="{М} {ЕСТЬn} {n} {Тn}.",
        состояние="{М} {ЕСТЬv} {v} {Тv}",
        шаг_плюс="{П} erstellt {m} {Тm}.",
        шаг_минус="{П} löscht {m} {Тm}.",
        шаг_чтение="{П} liest nur.",
        вопрос_лента="wie viele {Тмн} sind {М} {ВСЕ}?",
        вопрос_шаг="wie viele {Тмн} sind {М} {ШАГ}?",
        ответ_шаг="{ШАГ} {М} {ЕСТЬv} {v} {Тv}",
        вопрос_какой="welcher Akt hat die Zahl am meisten geändert?",
        ответ_ничья="{ПA} und {ПB} gleich: je {mp} {Тmp}.",
        дело_плюс="er hat {mp} {Тmp} hinzugefügt",
        дело_минус="er hat {mp} {Тmp} entfernt",
        вопрос_сколько="wie viele Akte haben die Zahl geändert?",
        # НЕМЕЦКИЙ ВОПРОС БЕЗ «es»: «waren es / gab es» есть заявка о величине, за
        # которой обязано стоять число — вопрос его не несёт, и арифметика слепла на нём.
        вопрос_сравнение="wie viele {Тмн} sind {М} vorher und nachher?",
        ответ_сравнение="vorher {n}, nachher {v}: {СРАВ}."),
    "fr": dict(
        начало="il y a {n} {Тn} {М}.",
        состояние="il y a {v} {Тv} {М}",
        шаг_плюс="{П} crée {m} {Тm}.",
        шаг_минус="{П} supprime {m} {Тm}.",
        шаг_чтение="{П} ne fait que lire.",
        вопрос_лента="combien de {Тмн} y a-t-il {М} {ВСЕ} ?",
        вопрос_шаг="combien de {Тмн} y a-t-il {М} {ШАГ} ?",
        ответ_шаг="{ШАГ} il y a {v} {Тv} {М}",
        вопрос_какой="quel acte a le plus changé le compte ?",
        ответ_ничья="{ПA} et {ПB} à égalité : {mp} {Тmp} chacun.",
        дело_плюс="il a ajouté {mp} {Тmp}",
        дело_минус="il a supprimé {mp} {Тmp}",
        вопрос_сколько="combien d'actes ont changé le compte ?",
        вопрос_сравнение="combien y en avait-il avant et après ?",
        ответ_сравнение="avant {n}, après {v} : {СРАВ}."),
    "es": dict(
        начало="hay {n} {Тn} {М}.",
        состояние="hay {v} {Тv} {М}",
        шаг_плюс="{П} crea {m} {Тm}.",
        шаг_минус="{П} borra {m} {Тm}.",
        шаг_чтение="{П} solo lee.",
        вопрос_лента="¿{кск} {Тмн} hay {М} {ВСЕ}?",
        вопрос_шаг="¿{кск} {Тмн} hay {М} {ШАГ}?",
        ответ_шаг="{ШАГ} hay {v} {Тv} {М}",
        вопрос_какой="¿qué acto cambió más la cuenta?",
        ответ_ничья="{ПA} y {ПB} por igual: {mp} {Тmp} cada uno.",
        дело_плюс="añadió {mp} {Тmp}",
        дело_минус="borró {mp} {Тmp}",
        вопрос_сколько="¿cuántos actos cambiaron la cuenta?",
        вопрос_сравнение="¿{кск} había antes y después?",
        ответ_сравнение="antes {n}, después {v}: {СРАВ}."),
    "it": dict(
        начало="{ЕСТЬn} {n} {Тn} {М}.",
        состояние="{ЕСТЬv} {v} {Тv} {М}",
        шаг_плюс="{П} crea {m} {Тm}.",
        шаг_минус="{П} elimina {m} {Тm}.",
        шаг_чтение="{П} solo legge.",
        вопрос_лента="{quante} {Тмн} ci sono {М} {ВСЕ}?",
        вопрос_шаг="{quante} {Тмн} ci sono {М} {ШАГ}?",
        ответ_шаг="{ШАГ} {ЕСТЬv} {v} {Тv} {М}",
        вопрос_какой="quale atto ha cambiato di più il conto?",
        ответ_ничья="{ПA} e {ПB} allo stesso modo: {mp} {Тmp} ciascuno.",
        дело_плюс="ha aggiunto {mp} {Тmp}",
        дело_минус="ha eliminato {mp} {Тmp}",
        вопрос_сколько="quanti atti hanno cambiato il conto?",
        вопрос_сравнение="{quante} ce n'erano prima e dopo?",
        ответ_сравнение="prima {n}, dopo {v}: {СРАВ}."),
    "pt": dict(
        начало="há {n} {Тn} {М}.",
        состояние="há {v} {Тv} {М}",
        шаг_плюс="{П} cria {m} {Тm}.",
        шаг_минус="{П} apaga {m} {Тm}.",
        шаг_чтение="{П} apenas lê.",
        вопрос_лента="{quantas} {Тмн} há {М} {ВСЕ}?",
        вопрос_шаг="{quantas} {Тмн} há {М} {ШАГ}?",
        ответ_шаг="{ШАГ} há {v} {Тv} {М}",
        вопрос_какой="que ato mudou mais a contagem?",
        ответ_ничья="{ПA} e {ПB} por igual: {mp} {Тmp} cada um.",
        дело_плюс="acrescentou {mp} {Тmp}",
        дело_минус="apagou {mp} {Тmp}",
        вопрос_сколько="quantos atos mudaram a contagem?",
        вопрос_сравнение="{quantas} havia antes e depois?",
        ответ_сравнение="antes {n}, depois {v}: {СРАВ}."),
    "nl": dict(
        начало="er {ЕСТЬn} {n} {Тn} {М}.",
        состояние="er {ЕСТЬv} {v} {Тv} {М}",
        шаг_плюс="{П} maakt {m} {Тm} aan.",
        шаг_минус="{П} verwijdert {m} {Тm}.",
        шаг_чтение="{П} leest alleen.",
        вопрос_лента="hoeveel {Тмн} zijn er {М} {ВСЕ}?",
        вопрос_шаг="hoeveel {Тмн} zijn er {М} {ШАГ}?",
        ответ_шаг="{ШАГ} {ЕСТЬv} er {v} {Тv} {М}",
        вопрос_какой="welke handeling heeft het aantal het meest veranderd?",
        ответ_ничья="{ПA} en {ПB} even veel: {mp} {Тmp} elk.",
        дело_плюс="het heeft {mp} {Тmp} toegevoegd",
        дело_минус="het heeft {mp} {Тmp} verwijderd",
        вопрос_сколько="hoeveel handelingen hebben het aantal veranderd?",
        вопрос_сравнение="hoeveel waren er eerst en daarna?",
        ответ_сравнение="eerst {n}, daarna {v}: {СРАВ}."),
    "pl": dict(
        начало="{М} {ЕСТЬn} {n} {Тn}.",
        состояние="{М} {ЕСТЬv} {v} {Тv}",
        шаг_плюс="{П} tworzy {m} {Тm}.",
        шаг_минус="{П} usuwa {m} {Тm}.",
        шаг_чтение="{П} tylko czyta.",
        # ВОПРОС ПОЛЬСКОГО ДЕРЖИТ «jest» ВСЕГДА: «ile plików jest w folderze» — связка
        # вопроса не гнётся по числу ответа, гнётся связка УТВЕРЖДЕНИЯ.
        вопрос_лента="ile {Тмн} jest {М} {ВСЕ}?",
        вопрос_шаг="ile {Тмн} jest {М} {ШАГ}?",
        ответ_шаг="{ШАГ} {М} {ЕСТЬv} {v} {Тv}",
        вопрос_какой="jaki akt najbardziej zmienił liczbę?",
        ответ_ничья="{ПA} i {ПB} po równo: po {mp} {Тmp}.",
        дело_плюс="dodał {mp} {Тmp}",
        дело_минус="usunął {mp} {Тmp}",
        вопрос_сколько="ile aktów zmieniło liczbę?",
        вопрос_сравнение="ile było przedtem i potem?",
        ответ_сравнение="przedtem {n}, potem {v}: {СРАВ}."),
}
ФОРМЫ = ("лента_три", "после_шага", "какой_шаг", "какой_шаг_ничья", "лента_без_изменения",
         "итог_сравнение")
ПАРЫ_НИЧЬИ = ((0, 1), (0, 2), (1, 2))   # какие два акта могут сойтись поровну


def _вещь(язык, Т, c):
    """The count form of the act's thing — the tool house's things, the pack's own rule."""
    return S._счёт(T.ВЕЩИ[язык][Т % len(T.ВЕЩИ[язык])], c, язык)


def _род_поля(язык, мн):
    """The gendered question words of a thing whose plural is «мн» (es/it/pt)."""
    род = T.РОД.get(язык, {}).get(мн, "f")
    return {дыра: (м_ if род == "m" else ж_) for дыра, (м_, ж_) in S.РОДОВЫЕ.get(язык, {}).items()}


def _леджер(фигура, шаги, до, конец):
    """«n + a − b + c = v» — the tape's own sum; a reading act stands outside it."""
    куски = ["{n}"]
    for i in range(конец):
        if фигура[i] == "0":
            continue
        куски.append("+" if фигура[i] == "+" else "−")
        куски.append("{m%d}" % (i + 1))
    return " ".join(куски) + " = {%s}" % ("v" if конец == 3 else "v2")


def _счёты(n, фигура, шаги):
    """The running counts of a tape: (after step 1, after step 2, after step 3)."""
    вон, теперь = [], n
    for знак, m in zip(фигура, шаги):
        if знак == "+":
            теперь += m
        elif знак == "−":
            теперь -= m
        вон.append(теперь)
    return вон


def _перемены(фигура, шаги):
    """What each act moved: a signed change; a reading act moves nought."""
    return [0 if з == "0" else (m if з == "+" else -m) for з, m in zip(фигура, шаги)]


def рамка(язык, форма, фигура, победитель=None, актов=None, знак_итога=None, ничья=None):
    """The page's template: the frame is CONCRETE (it names its winner, its count of
    changing acts and its verdict), and the judge verifies that naming against the numbers."""
    р = РЕЧЬ[язык]
    шаги = []
    for i, знак in enumerate(фигура):
        клеть = {"+": р["шаг_плюс"], "−": р["шаг_минус"], "0": р["шаг_чтение"]}[знак]
        клеть = клеть.replace("{П}", ПОРЯДОК[язык][i])
        клеть = клеть.replace("{m}", "{m%d}" % (i + 1)).replace("{Тm}", "{Тm%d}" % (i + 1))
        шаги.append(клеть)
    начало = " ".join([р["начало"]] + шаги)
    if форма == "лента_три":
        вопрос = р["вопрос_лента"].replace("{ВСЕ}", ПОСЛЕ_ВСЕХ[язык])
        ответ = р["состояние"] + ": " + _леджер(фигура, шаги, 0, 3) + "."
    elif форма == "после_шага":
        вопрос = р["вопрос_шаг"].replace("{ШАГ}", ПОСЛЕ_ШАГА[язык][1])
        ответ = (р["ответ_шаг"].replace("{ШАГ}", ПОСЛЕ_ШАГА[язык][1]).replace("{v}", "{v2}").replace("{Тv}", "{Тv2}")
                 + ": " + _леджер(фигура, шаги, 0, 2) + ".")
    elif форма == "какой_шаг":
        вопрос = р["вопрос_какой"]
        дело = р["дело_плюс"] if фигура[победитель] == "+" else р["дело_минус"]
        дело = дело.replace("{mp}", "{m%d}" % (победитель + 1)).replace("{Тmp}", "{Тm%d}" % (победитель + 1))
        ответ = ПОРЯДОК[язык][победитель] + ": " + дело + "."
    elif форма == "какой_шаг_ничья":
        # НИЧЬЯ ЕСТЬ ОТВЕТ, А НЕ ОТСУТСТВИЕ ОТВЕТА: два акта двинули счёт поровну, и
        # страница называет ОБА — иначе читатель купил бы «наибольший всегда один».
        А, Б = ничья
        вопрос = р["вопрос_какой"]
        ответ = (р["ответ_ничья"].replace("{ПA}", ПОРЯДОК[язык][А]).replace("{ПB}", ПОРЯДОК[язык][Б])
                 .replace("{mp}", "{m%d}" % (А + 1)).replace("{Тmp}", "{Тm%d}" % (А + 1)))
    elif форма == "лента_без_изменения":
        вопрос = р["вопрос_сколько"]
        ответ = АКТОВ[язык][актов] + ": " + T.НЕИЗМЕННОСТЬ[язык] + "."
    else:                                  # итог_сравнение
        вопрос = р["вопрос_сравнение"]
        ответ = р["ответ_сравнение"].replace("{СРАВ}", СРАВНЕНИЕ[язык][знак_итога])
    return начало + " " + вопрос + " " + ответ


def страница(язык, форма, Т, n, фигура, шаги, победитель=None, актов=None, знак_итога=None, ничья=None):
    счёты = _счёты(n, фигура, шаги)
    мн = _вещь(язык, Т, 5)
    п = dict(n=n, v=счёты[2], v2=счёты[1], Тn=_вещь(язык, Т, n), Тv=_вещь(язык, Т, счёты[2]),
             Тv2=_вещь(язык, Т, счёты[1]), Тмн=мн, М=T.МЕСТА[язык][Т % len(T.МЕСТА[язык])])
    for i, m in enumerate(шаги):
        п["m%d" % (i + 1)] = m
        п["Тm%d" % (i + 1)] = _вещь(язык, Т, m)
    if язык in T.ЕСТЬ:
        п["ЕСТЬn"] = T._есть(язык, n)
        п["ЕСТЬv"] = T._есть(язык, счёты[2] if форма != "после_шага" else счёты[1])
    п.update(_род_поля(язык, мн))
    return рамка(язык, форма, фигура, победитель, актов, знак_итога, ничья).format(**п)


def _тройки():
    """The number tuples of a tape: three steps whose partial sums never fall below one.

    Two tapes per starting state, drawn by a stride over the step numbers — the market sees
    the same start move by different amounts, and no tuple repeats."""
    вон = []
    for i, n in enumerate(НАЧАЛА):
        for сдвиг in (0, 4):
            a = ШАГИ_ЧИСЕЛ[(i + сдвиг) % len(ШАГИ_ЧИСЕЛ)]
            b = ШАГИ_ЧИСЕЛ[(i * 3 + 1 + сдвиг) % len(ШАГИ_ЧИСЕЛ)]
            c = ШАГИ_ЧИСЕЛ[(i * 5 + 2 + сдвиг) % len(ШАГИ_ЧИСЕЛ)]
            вон.append((n, (a, b, c)))
    return вон


ТРОЙКИ = _тройки()


def _тройки_ничьи():
    """Tapes where TWO acts move the count by the same amount and the third moves less."""
    вон = []
    for i, n in enumerate(НАЧАЛА):
        велик = 3 + i % 6          # то, что двинули оба
        мал = 1 + i % 2            # то, что двинул третий; всегда меньше
        for А, Б in ПАРЫ_НИЧЬИ:
            шаги = [мал, мал, мал]
            шаги[А] = шаги[Б] = велик
            вон.append((n, tuple(шаги), (А, Б)))
    return вон


ТРОЙКИ_НИЧЬИ = _тройки_ничьи()


def _годна(n, фигура, шаги, единственный_максимум=False, знак_итога=None):
    счёты = _счёты(n, фигура, шаги)
    if min(счёты) < 1:
        return False
    перемены = [abs(x) for x in _перемены(фигура, шаги)]
    if единственный_максимум and перемены.count(max(перемены)) != 1:
        return False
    if знак_итога is not None:
        if знак_итога == "+" and счёты[2] <= n:
            return False
        if знак_итога == "−" and счёты[2] >= n:
            return False
    return True


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        видов = len(T.ВЕЩИ[язык])
        for i, (n, шаги) in enumerate(ТРОЙКИ):
            Т = (i + n) % видов
            for ф, фигура in enumerate(ФИГУРЫ_ПОЛНЫЕ):
                if not _годна(n, фигура, шаги):
                    continue
                вон[страница(язык, "лента_три", Т, n, фигура, шаги)] = (язык, "лента_три")
                вон[страница(язык, "после_шага", Т, n, фигура, шаги)] = (язык, "после_шага")
                if _годна(n, фигура, шаги, единственный_максимум=True):
                    перемены = [abs(x) for x in _перемены(фигура, шаги)]
                    победитель = перемены.index(max(перемены))
                    вон[страница(язык, "какой_шаг", Т, n, фигура, шаги, победитель=победитель)] = (язык, "какой_шаг")
            for фигура in ФИГУРЫ_С_ЧТЕНИЕМ:
                if not _годна(n, фигура, шаги):
                    continue
                актов = sum(1 for з in фигура if з != "0")
                вон[страница(язык, "лента_без_изменения", Т, n, фигура, шаги, актов=актов)] = (язык, "лента_без_изменения")
            for фигура in ФИГУРЫ_СРАВНЕНИЯ:
                for знак in ("+", "−"):
                    if not _годна(n, фигура, шаги, знак_итога=знак):
                        continue
                    вон[страница(язык, "итог_сравнение", Т, n, фигура, шаги, знак_итога=знак)] = (язык, "итог_сравнение")
        for i, (n, шаги, (А, Б)) in enumerate(ТРОЙКИ_НИЧЬИ):
            Т = (i + n) % видов
            for фигура in ФИГУРЫ_ПОЛНЫЕ:
                if not _годна(n, фигура, шаги):
                    continue
                перемены = [abs(x) for x in _перемены(фигура, шаги)]
                if {j for j, x in enumerate(перемены) if x == max(перемены)} != {А, Б}:
                    continue
                вон[страница(язык, "какой_шаг_ничья", Т, n, фигура, шаги, ничья=(А, Б))] = (язык, "какой_шаг_ничья")
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    """Branches ordered by content, never by the set's own order (закон детерминизма)."""
    return "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, шаблон):
    """One pattern over the whole page; the i-th occurrence of a hole is «h_<hole>__i»."""
    вещи = _альт(T.ФОРМЫ_ВЕЩЕЙ[язык])
    дыры = {"n": r"\d+", "v": r"\d+", "v2": r"\d+", "Тn": вещи, "Тv": вещи, "Тv2": вещи,
            "Тмн": вещи, "М": _альт(T.МЕСТА[язык])}
    for i in (1, 2, 3):
        дыры["m%d" % i] = r"\d+"
        дыры["Тm%d" % i] = вещи
    if язык in T.ЕСТЬ:
        дыры["ЕСТЬn"] = _альт(T.ЕСТЬ[язык])
        дыры["ЕСТЬv"] = _альт(T.ЕСТЬ[язык])
    for дыра, пара in S.РОДОВЫЕ.get(язык, {}).items():
        дыры[дыра] = _альт(пара)
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", шаблон):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


def _все_рамки():
    """Every concrete frame of the house: (pattern, language, form, shape, extras)."""
    вон = []
    for язык in ЯЗЫКИ:
        for фигура in ФИГУРЫ_ПОЛНЫЕ:
            вон.append((_образец(язык, рамка(язык, "лента_три", фигура)), язык, "лента_три", фигура, {}))
            вон.append((_образец(язык, рамка(язык, "после_шага", фигура)), язык, "после_шага", фигура, {}))
            for победитель in (0, 1, 2):
                вон.append((_образец(язык, рамка(язык, "какой_шаг", фигура, победитель=победитель)),
                            язык, "какой_шаг", фигура, {"победитель": победитель}))
            for пара in ПАРЫ_НИЧЬИ:
                вон.append((_образец(язык, рамка(язык, "какой_шаг_ничья", фигура, ничья=пара)),
                            язык, "какой_шаг_ничья", фигура, {"ничья": пара}))
        for фигура in ФИГУРЫ_С_ЧТЕНИЕМ:
            for актов in (1, 2, 3):
                вон.append((_образец(язык, рамка(язык, "лента_без_изменения", фигура, актов=актов)),
                            язык, "лента_без_изменения", фигура, {"актов": актов}))
        for фигура in ФИГУРЫ_СРАВНЕНИЯ:
            for знак in ("+", "−"):
                вон.append((_образец(язык, рамка(язык, "итог_сравнение", фигура, знак_итога=знак)),
                            язык, "итог_сравнение", фигура, {"знак_итога": знак}))
    return вон


ОБРАЗЦЫ = _все_рамки()


def _значения(м):
    """The holes of a match; a hole repeated in the frame must carry ONE value."""
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _вердикт(язык, форма, фигура, добавка, зн):
    n = int(зн["n"])
    шаги = [int(зн["m%d" % i]) for i in (1, 2, 3) if "m%d" % i in зн]
    if len(шаги) != 3:
        # шаг чтения не несёт числа: его место в ленте занято, а в счёте — нет
        шаги = [int(зн.get("m%d" % i, 0)) for i in (1, 2, 3)]
        for i, з in enumerate(фигура):
            if з != "0" and "m%d" % (i + 1) not in зн:
                return False
    if n not in НАЧАЛА:
        return False
    счёты = _счёты(n, фигура, шаги)
    if min(счёты) < 1:
        return False
    # СЧЁТНАЯ ФОРМА ЕСТЬ ФОРМА СВОЕГО ЧИСЛА, И ВСЕ ФОРМЫ СТРАНИЦЫ — ФОРМЫ ОДНОЙ ВЕЩИ
    виды = None
    пары = [("Тn", n)]
    for i in (1, 2, 3):
        if "Тm%d" % i in зн:
            пары.append(("Тm%d" % i, шаги[i - 1]))
    if "Тv" in зн:
        пары.append(("Тv", счёты[2]))
    if "Тv2" in зн:
        пары.append(("Тv2", счёты[1]))
    for дыра, число in пары:
        свои = {Т for Т in T.ФОРМЫ_ВЕЩЕЙ[язык].get(зн[дыра], set())
                if Т != "строка" and S._счёт(T.ВЕЩИ[язык][Т], число, язык) == зн[дыра]}
        if not свои:
            return False
        виды = свои if виды is None else виды & свои
        if not виды:
            return False
    if "Тмн" in зн:
        виды = (виды or set()) & {Т for Т in T.ФОРМЫ_ВЕЩЕЙ[язык].get(зн["Тмн"], set()) if Т != "строка"}
        if not виды:
            return False
    # ЛЕДЖЕР ЛЕНТЫ И ЕГО ПРЕФИКС ПЕРЕСЧИТЫВАЮТСЯ
    if "v" in зн and int(зн["v"]) != счёты[2]:
        return False
    if "v2" in зн and int(зн["v2"]) != счёты[1]:
        return False
    # СВЯЗКА МЕСТА ГНЁТСЯ ПО ЧИСЛУ
    if "ЕСТЬn" in зн and зн["ЕСТЬn"] != T._есть(язык, n):
        return False
    if "ЕСТЬv" in зн:
        своё = счёты[1] if форма == "после_шага" else счёты[2]
        if зн["ЕСТЬv"] != T._есть(язык, своё):
            return False
    # ВОПРОСНОЕ СЛОВО ПО РОДУ ВЕЩИ
    if "Тмн" in зн:
        свои = _род_поля(язык, зн["Тмн"])
        for дыра, слово in свои.items():
            if дыра in зн and зн[дыра] != слово:
                return False
    перемены = [abs(x) for x in _перемены(фигура, шаги)]
    if форма == "какой_шаг":
        # НАЗВАННЫЙ ШАГ ОБЯЗАН БЫТЬ НАИБОЛЬШИМ, И НАИБОЛЬШИЙ ОБЯЗАН БЫТЬ ОДИН
        if перемены.count(max(перемены)) != 1:
            return False
        if перемены.index(max(перемены)) != добавка["победитель"]:
            return False
    if форма == "какой_шаг_ничья":
        # НАЗВАННАЯ ПАРА ОБЯЗАНА БЫТЬ РОВНО МНОЖЕСТВОМ НАИБОЛЬШИХ ПЕРЕМЕН
        наибольшие = {i for i, x in enumerate(перемены) if x == max(перемены)}
        if наибольшие != set(добавка["ничья"]):
            return False
        if перемены[добавка["ничья"][0]] != перемены[добавка["ничья"][1]]:
            return False
    if форма == "лента_без_изменения":
        # НАЗВАННОЕ ЧИСЛО АКТОВ ОБЯЗАНО БЫТЬ ЧИСЛОМ АКТОВ, ДВИНУВШИХ СЧЁТ
        if добавка["актов"] != sum(1 for x in перемены if x != 0):
            return False
    if форма == "итог_сравнение":
        # НАЗВАННЫЙ ВЕРДИКТ ОБЯЗАН СОГЛАСОВАТЬСЯ С ЧИСЛАМИ
        если_больше = счёты[2] > n
        if (добавка["знак_итога"] == "+") != если_больше:
            return False
        if счёты[2] == n:
            return False
    return True


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose tape recomputes; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма, фигура, добавка in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(язык, форма, фигура, добавка, зн)
    return False, False


def _хвост(с):
    """The start of the answer (after the last question mark)."""
    м = list(re.finditer(r"[?？] ", с))
    return м[-1].end() if м else 0


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        Т, n, шаги = 0, 10, (2, 1, 3)
        # (1) ИТОГ ЛЕНТЫ НЕ СХОДИТСЯ
        л = страница(язык, "лента_три", Т, n, ("+", "−", "+"), шаги)
        assert судить(л) == (True, True), л
        битая = л[:_хвост(л)] + л[_хвост(л):].replace("14", "15")
        assert судить(битая) == (True, False), битая
        # (2) ПРЕФИКС ШАГА НЕ СХОДИТСЯ
        ш = страница(язык, "после_шага", Т, n, ("+", "−", "+"), шаги)
        assert судить(ш) == (True, True), ш
        битая = ш[:_хвост(ш)] + ш[_хвост(ш):].replace("11", "12")
        assert судить(битая) == (True, False), битая
        # (3) НАЗВАН НЕ ТОТ ШАГ
        к = страница(язык, "какой_шаг", Т, n, ("+", "−", "+"), шаги, победитель=2)
        assert судить(к) == (True, True), к
        # (страница той же ленты, но названа первым актом: рамка есть, число — нет)
        битая = страница(язык, "какой_шаг", Т, n, ("+", "−", "+"), шаги, победитель=0)
        assert судить(битая) == (True, False), битая
        # (4) ЧТЕНИЕ СОЧТЕНО ИЗМЕНЯЮЩИМ
        б = страница(язык, "лента_без_изменения", Т, n, ("+", "0", "+"), шаги, актов=2)
        assert судить(б) == (True, True), б
        битая = б.replace(АКТОВ[язык][2] + ":", АКТОВ[язык][3] + ":")
        assert судить(битая) == (True, False), битая
        # (5) «БОЛЬШЕ» ПРИ УБЫЛИ
        с = страница(язык, "итог_сравнение", Т, n, ("+", "−", "−"), шаги, знак_итога="−")
        assert судить(с) == (True, True), с
        битая = с.replace(": " + СРАВНЕНИЕ[язык]["−"] + ".", ": " + СРАВНЕНИЕ[язык]["+"] + ".")
        assert судить(битая) == (True, False), битая
        мутанты += 5
        # (6) СЧЁТНАЯ ФОРМА ИТОГА — ФОРМА ЧУЖОГО ЧИСЛА
        итог = _счёты(n, ("+", "−", "+"), шаги)[2]
        своя, чужая = _вещь(язык, Т, итог), _вещь(язык, Т, 1)
        if своя != чужая:
            хв = _хвост(л)
            битая = л[:хв] + л[хв:].replace(своя, чужая, 1)
            assert судить(битая) == (True, False), битая
            мутанты += 1
        # (7) СВЯЗКА МЕСТА НЕ ПО ЧИСЛУ
        if язык in T.ЕСТЬ and T._есть(язык, итог) != T._есть(язык, 1):
            хв = _хвост(л)
            битая = л[:хв] + л[хв:].replace(T._есть(язык, итог), T._есть(язык, 1), 1)
            assert судить(битая) == (True, False), битая
            мутанты += 1
        # (8) ПРИ НИЧЬЕЙ НАЗВАН ОДИН ШАГ
        ничьи_шаги = (3, 1, 3)
        н = страница(язык, "какой_шаг_ничья", Т, n, ("+", "−", "+"), ничьи_шаги, ничья=(0, 2))
        assert судить(н) == (True, True), н
        битая = страница(язык, "какой_шаг", Т, n, ("+", "−", "+"), ничьи_шаги, победитель=0)
        assert судить(битая) == (True, False), битая
        # (9) НИЧЬЯ ОБЪЯВЛЕНА ТАМ, ГДЕ НАИБОЛЬШИЙ ОДИН
        битая = страница(язык, "какой_шаг_ничья", Т, n, ("+", "−", "+"), (2, 1, 3), ничья=(0, 2))
        assert судить(битая) == (True, False), битая
        мутанты += 2
        # (10) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ — иначе ворота съедят страницу целиком
        for стр in (л, ш, к, б, с, н):
            вопрос = стр[:стр.index("?") + 1].split(". ")[-1]
            assert asking.зачин_объявлен(вопрос) is not False, вопрос
    for язык, форма, фигура, добавка in (("ru", "лента_три", ("+", "−", "+"), {}),
                                         ("en", "лента_три", ("+", "−", "+"), {}),
                                         ("ru", "после_шага", ("+", "−", "+"), {}),
                                         ("de", "какой_шаг", ("+", "−", "+"), {"победитель": 2}),
                                         ("pl", "лента_без_изменения", ("+", "0", "+"), {"актов": 2}),
                                         ("fr", "итог_сравнение", ("+", "−", "−"), {"знак_итога": "−"}),
                                         ("es", "лента_три", ("−", "+", "+"), {}),
                                         ("it", "после_шага", ("+", "+", "−"), {}),
                                         ("pt", "какой_шаг", ("+", "+", "−"), {"победитель": 2}),
                                         ("nl", "итог_сравнение", ("−", "+", "−"), {"знак_итога": "−"})):
        print("  ", страница(язык, форма, 0, 10, фигура, (2, 1, 3), **добавка))
    for язык in ("ru", "en", "pl"):
        print("  ", страница(язык, "какой_шаг_ничья", 0, 10, ("+", "−", "+"), (3, 1, 3), ничья=(0, 2)))
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
