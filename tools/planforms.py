#!/usr/bin/env python3
"""THE HOUSE OF THE PLAN — a task cut into steps, each step checked by a number (05.09).

The agent architecture (omega/ozar/OZAR-AGENT-ARCH-0905.md) asks the corpus for the level it
calls SUBTASK: a goal, its steps, and a verifiable end. A reader that answers «how many after
step 2?» and «is the task done?» has read a PLAN, not a story: the page carries the plan whole,
and every question of it is answered from the plan's own numbers.

WHAT THE HOUSE SHOWS. Five frames on nine languages, each a page «show · question? · answer.»:
  · a two-step plan whose steps count DIFFERENT things (buy 2 packs, bake 12 buns) — the
    question after each step, then the verdict of the task;
  · a three-step plan whose first two steps count the SAME thing (collect 5 boxes, collect 4
    more) — the number after step 2 is their sum and carries its ledger, and the third step
    acts on all of them;
  · the same plan UNDONE: after step 2 there are fewer things than the goal, and the verdict
    is «no» WITH ITS GROUND — both numbers named (needed, present);
  · the order of steps — the answer is a step, not a number;
  · the length of the plan — «how many steps?» answered by the count form of «step».

WHAT THE HOUSE DECLARES AND WHAT IT BORROWS. The units of counting (buns, packs, boxes,
buckets, beds, books) with their count forms and gender are declared HERE, because the house
writes them and nobody else does; the count form of a number is taken by the pack's agreement
rule (the SVAMP house's reader of that rule), and the words of polarity are read from the pack
— «да», «yes», «tak» are the language's, not the house's.

THE JUDGE IS THE PLAN ITSELF. A page is a frame whose holes are filled by the plan; every hole
repeated in the frame carries one value (the goal's number is the answer's number, the unit of
the question is the unit of the answer); the count form is the form of its number; the sum
after step 2 is the sum of steps 1 and 2; the verdict «yes» stands only when the number reaches
the goal, «no» only when it falls short and names both numbers; the order names the first step;
the length is the length of the plan. The world is CLOSED.

WHAT IS NOT MEASURED, NAMED: whether the plan is a GOOD plan — the house shows plans that work
and plans that fall short, and asks only whether the reader can read the plan and check it.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import svampforms as S  # noqa: E402 — the reader of the pack's count-agreement rule

_ПАКЕТЫ = pathlib.Path(__file__).resolve().parent / "langpacks"
ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")

# ЕДИНИЦЫ СЧЁТА ОБЪЯВЛЕНЫ ЗДЕСЬ: их пишет этот дом, и ничей чужой список их не знает. Три формы
# у русского и польского, две у прочих — счётную ячейку выбирает правило пакета (S._счёт); род
# нужен там, где вопросное слово гнётся («¿cuántos paquetes?» против «¿cuántas cajas?»).
ЕДИНИЦЫ = {
    "ru": {"булки": (("булка", "булки", "булок"), "f"), "пачки": (("пачка", "пачки", "пачек"), "f"),
           "ящики": (("ящик", "ящика", "ящиков"), "m"), "вёдра": (("ведро", "ведра", "вёдер"), "n"),
           "грядки": (("грядка", "грядки", "грядок"), "f"), "книги": (("книга", "книги", "книг"), "f")},
    "en": {"булки": (("bun", "buns"), "m"), "пачки": (("pack", "packs"), "m"),
           "ящики": (("box", "boxes"), "m"), "вёдра": (("bucket", "buckets"), "m"),
           "грядки": (("bed", "beds"), "m"), "книги": (("book", "books"), "m")},
    "de": {"булки": (("Brötchen", "Brötchen"), "n"), "пачки": (("Packung", "Packungen"), "f"),
           "ящики": (("Kiste", "Kisten"), "f"), "вёдра": (("Eimer", "Eimer"), "m"),
           "грядки": (("Beet", "Beete"), "n"), "книги": (("Buch", "Bücher"), "n")},
    "fr": {"булки": (("petit pain", "petits pains"), "m"), "пачки": (("paquet", "paquets"), "m"),
           "ящики": (("caisse", "caisses"), "f"), "вёдра": (("seau", "seaux"), "m"),
           "грядки": (("planche", "planches"), "f"), "книги": (("livre", "livres"), "m")},
    "es": {"булки": (("panecillo", "panecillos"), "m"), "пачки": (("paquete", "paquetes"), "m"),
           "ящики": (("caja", "cajas"), "f"), "вёдра": (("cubo", "cubos"), "m"),
           "грядки": (("bancal", "bancales"), "m"), "книги": (("libro", "libros"), "m")},
    "it": {"булки": (("panino", "panini"), "m"), "пачки": (("pacco", "pacchi"), "m"),
           "ящики": (("cassa", "casse"), "f"), "вёдра": (("secchio", "secchi"), "m"),
           "грядки": (("aiuola", "aiuole"), "f"), "книги": (("libro", "libri"), "m")},
    "pt": {"булки": (("pãozinho", "pãezinhos"), "m"), "пачки": (("pacote", "pacotes"), "m"),
           "ящики": (("caixa", "caixas"), "f"), "вёдра": (("balde", "baldes"), "m"),
           "грядки": (("canteiro", "canteiros"), "m"), "книги": (("livro", "livros"), "m")},
    "nl": {"булки": (("broodje", "broodjes"), "m"), "пачки": (("pak", "pakken"), "m"),
           "ящики": (("kist", "kisten"), "m"), "вёдра": (("emmer", "emmers"), "m"),
           "грядки": (("bed", "bedden"), "m"), "книги": (("boek", "boeken"), "m")},
    "pl": {"булки": (("bułka", "bułki", "bułek"), "f"), "пачки": (("paczka", "paczki", "paczek"), "f"),
           "ящики": (("skrzynka", "skrzynki", "skrzynek"), "f"), "вёдра": (("wiadro", "wiadra", "wiader"), "n"),
           "грядки": (("grządka", "grządki", "grządek"), "f"), "книги": (("książka", "książki", "książek"), "f")},
}
# «ШАГ» СЧИТАЕТСЯ ТАК ЖЕ, КАК ВЕЩЬ: «2 шага», «3 kroki», «3 steps» — форма по правилу пакета
ШАГ_СЛОВО = {"ru": ("шаг", "шага", "шагов"), "en": ("step", "steps"), "de": ("Schritt", "Schritte"),
             "fr": ("étape", "étapes"), "es": ("paso", "pasos"), "it": ("passo", "passi"),
             "pt": ("passo", "passos"), "nl": ("stap", "stappen"), "pl": ("krok", "kroki", "kroków")}
# ВОПРОСНОЕ СЛОВО ГНЁТСЯ РОДОМ ЕДИНИЦЫ там, где язык его гнёт; прочие пишут одно слово в рамке
КСК = {"es": ("cuántos", "cuántas"), "it": ("quanti", "quante"), "pt": ("quantos", "quantas")}


# СЛОВАРНОЕ МНОЖЕСТВЕННОЕ — форма для КРАТКОЙ фразы шага («собрать ящики», «kupić paczki») и для
# «все {вещи}»: у русского и польского это не та форма, что после «сколько» (там родительный),
# и потому объявлена отдельно; у прочих языков она совпадает с формой множества.
СЛОВАРНОЕ_МН = {'ru': {'булки': 'булки', 'пачки': 'пачки', 'ящики': 'ящики', 'вёдра': 'вёдра', 'грядки': 'грядки', 'книги': 'книги'}, 'pl': {'булки': 'bułki', 'пачки': 'paczki', 'ящики': 'skrzynki', 'вёдра': 'wiadra', 'грядки': 'grządki', 'книги': 'książki'}}
for _я in ЯЗЫКИ:
    СЛОВАРНОЕ_МН.setdefault(_я, {к: ф[0][-1] for к, ф in ЕДИНИЦЫ[_я].items()})


def _пакет(язык):
    return json.loads((_ПАКЕТЫ / f"{язык}.json").read_text(encoding="utf-8"))


# ДА И НЕТ ЧИТАЮТСЯ У ПАКЕТА (полярность объявлена языком, а не этим домом)
ДА = {я: (_пакет(я).get("polarity") or {}).get("yes", ["yes"])[0] for я in ЯЗЫКИ}
НЕТ = {я: (_пакет(я).get("polarity") or {}).get("no", ["no"])[0] for я in ЯЗЫКИ}
for _я in ЯЗЫКИ:
    assert ДА[_я] and НЕТ[_я], (_я, "the pack declares no polarity")

# СЛОВА ПЛАНА: заголовок плана, слово шага, «раньше», «нужно», «есть» — объявлены домом
СЛОВА = {
    "ru": dict(план="план", шаг="шаг", раньше="раньше", нужно="нужно", есть="есть",
               сколько_шагов="сколько шагов в плане?", вопрос_готово="выполнена ли задача?",
               что_раньше="что делать раньше", после="после шага"),
    "en": dict(план="plan", шаг="step", раньше="first", нужно="needed", есть="there are",
               сколько_шагов="how many steps are in the plan?", вопрос_готово="is the task done?",
               что_раньше="what to do first", после="after step"),
    "de": dict(план="Plan", шаг="Schritt", раньше="zuerst", нужно="nötig", есть="es gibt",
               сколько_шагов="wie viele Schritte hat der Plan?", вопрос_готово="ist die Aufgabe erledigt?",
               что_раньше="was ist zuerst zu tun", после="nach Schritt"),
    "fr": dict(план="plan", шаг="étape", раньше="d'abord", нужно="il faut", есть="il y a",
               сколько_шагов="combien d'étapes a le plan ?", вопрос_готово="est-ce que la tâche est finie ?",
               что_раньше="que faire d'abord", после="après l'étape"),
    "es": dict(план="plan", шаг="paso", раньше="primero", нужно="hacen falta", есть="hay",
               сколько_шагов="¿cuántos pasos tiene el plan?", вопрос_готово="¿está hecha la tarea?",
               что_раньше="¿qué hacer primero", после="después del paso"),
    "it": dict(план="piano", шаг="passo", раньше="prima", нужно="servono", есть="ci sono",
               сколько_шагов="quanti passi ha il piano?", вопрос_готово="è finito il compito?",
               что_раньше="che cosa fare prima", после="dopo il passo"),
    "pt": dict(план="plano", шаг="passo", раньше="primeiro", нужно="são precisos", есть="há",
               сколько_шагов="quantos passos tem o plano?", вопрос_готово="a tarefa está feita?",
               что_раньше="o que fazer primeiro", после="depois do passo"),
    "nl": dict(план="plan", шаг="stap", раньше="eerst", нужно="nodig", есть="er zijn",
               сколько_шагов="hoeveel stappen heeft het plan?", вопрос_готово="is de taak klaar?",
               что_раньше="wat eerst te doen", после="na stap"),
    "pl": dict(план="plan", шаг="krok", раньше="najpierw", нужно="potrzeba", есть="jest",
               сколько_шагов="ile kroków ma plan?", вопрос_готово="czy zadanie jest wykonane?",
               что_раньше="co zrobić najpierw", после="po kroku"),
}

# ЗАДАЧИ ДОМА: цель, шаги и краткие имена шагов. Две задачи о двух шагах, считающих РАЗНОЕ
# (купить пачки → испечь булки), и две о трёх шагах, где первые два считают ОДНО и потому
# складываются. Числа стоят дырами: одна задача даёт столько страниц, сколько наборов чисел.
ЗАДАЧИ = {
    "ru": (
        dict(имя="булки", ед="булки", ед1="пачки", цель="испечь {b} {Ub}",
             шаги=("купить {a} {U1a}", "испечь {b} {Ub}"), к=("купить {U1сл}", "испечь {Uсл}")),
        dict(имя="грядки", ед="грядки", ед1="вёдра", цель="полить {b} {Ub}",
             шаги=("налить {a} {U1a}", "полить {b} {Ub}"), к=("налить {U1сл}", "полить {Uсл}")),
        dict(имя="ящики", ед="ящики", цель="погрузить {s} {Us}", готово="погружено",
             шаги=("собрать {a} {Ua}", "собрать ещё {c} {Uc}", "погрузить все {Uсл}"),
             к=("собрать {Uсл}", "погрузить {Uсл}")),
        dict(имя="книги", ед="книги", цель="уложить {s} {Us}", готово="уложено",
             шаги=("положить {a} {Ua}", "положить ещё {c} {Uc}", "закрыть рюкзак"),
             к=("положить {Uсл}", "закрыть рюкзак")),
    ),
    "en": (
        dict(имя="булки", ед="булки", ед1="пачки", цель="bake {b} {Ub}",
             шаги=("buy {a} {U1a}", "bake {b} {Ub}"), к=("buy the {U1сл}", "bake the {Uсл}")),
        dict(имя="грядки", ед="грядки", ед1="вёдра", цель="water {b} {Ub}",
             шаги=("fill {a} {U1a}", "water {b} {Ub}"), к=("fill the {U1сл}", "water the {Uсл}")),
        dict(имя="ящики", ед="ящики", цель="load {s} {Us}", готово="loaded",
             шаги=("collect {a} {Ua}", "collect {c} more {Uc}", "load all the {Uсл}"),
             к=("collect the {Uсл}", "load the {Uсл}")),
        dict(имя="книги", ед="книги", цель="pack {s} {Us}", готово="packed",
             шаги=("put in {a} {Ua}", "put in {c} more {Uc}", "close the bag"),
             к=("put in the {Uсл}", "close the bag")),
    ),
    "de": (
        dict(имя="булки", ед="булки", ед1="пачки", цель="{b} {Ub} backen",
             шаги=("{a} {U1a} kaufen", "{b} {Ub} backen"), к=("{U1сл} kaufen", "{Uсл} backen")),
        dict(имя="грядки", ед="грядки", ед1="вёдра", цель="{b} {Ub} gießen",
             шаги=("{a} {U1a} füllen", "{b} {Ub} gießen"), к=("{U1сл} füllen", "{Uсл} gießen")),
        dict(имя="ящики", ед="ящики", цель="{s} {Us} laden", готово="geladen",
             шаги=("{a} {Ua} sammeln", "{c} {Uc} mehr sammeln", "alle {Uсл} laden"),
             к=("{Uсл} sammeln", "{Uсл} laden")),
        dict(имя="книги", ед="книги", цель="{s} {Us} packen", готово="gepackt",
             шаги=("{a} {Ua} einlegen", "{c} {Uc} mehr einlegen", "die Tasche schließen"),
             к=("{Uсл} einlegen", "die Tasche schließen")),
    ),
    "fr": (
        dict(имя="булки", ед="булки", ед1="пачки", цель="faire {b} {Ub}",
             шаги=("acheter {a} {U1a}", "faire {b} {Ub}"), к=("acheter les {U1сл}", "faire les {Uсл}")),
        dict(имя="грядки", ед="грядки", ед1="вёдра", цель="arroser {b} {Ub}",
             шаги=("remplir {a} {U1a}", "arroser {b} {Ub}"), к=("remplir les {U1сл}", "arroser les {Uсл}")),
        dict(имя="ящики", ед="ящики", цель="charger {s} {Us}", готово="chargées",
             шаги=("ramasser {a} {Ua}", "ramasser {c} {Uc} de plus", "charger toutes les {Uсл}"),
             к=("ramasser les {Uсл}", "charger les {Uсл}")),
        dict(имя="книги", ед="книги", цель="ranger {s} {Us}", готово="rangés",
             шаги=("mettre {a} {Ua}", "mettre {c} {Uc} de plus", "fermer le sac"),
             к=("mettre les {Uсл}", "fermer le sac")),
    ),
    "es": (
        dict(имя="булки", ед="булки", ед1="пачки", цель="hacer {b} {Ub}",
             шаги=("comprar {a} {U1a}", "hacer {b} {Ub}"), к=("comprar los {U1сл}", "hacer los {Uсл}")),
        dict(имя="грядки", ед="грядки", ед1="вёдра", цель="regar {b} {Ub}",
             шаги=("llenar {a} {U1a}", "regar {b} {Ub}"), к=("llenar los {U1сл}", "regar los {Uсл}")),
        dict(имя="ящики", ед="ящики", цель="cargar {s} {Us}", готово="cargadas",
             шаги=("juntar {a} {Ua}", "juntar {c} {Uc} más", "cargar todas las {Uсл}"),
             к=("juntar las {Uсл}", "cargar las {Uсл}")),
        dict(имя="книги", ед="книги", цель="guardar {s} {Us}", готово="guardados",
             шаги=("meter {a} {Ua}", "meter {c} {Uc} más", "cerrar la mochila"),
             к=("meter los {Uсл}", "cerrar la mochila")),
    ),
    "it": (
        dict(имя="булки", ед="булки", ед1="пачки", цель="fare {b} {Ub}",
             шаги=("comprare {a} {U1a}", "fare {b} {Ub}"), к=("comprare i {U1сл}", "fare i {Uсл}")),
        dict(имя="грядки", ед="грядки", ед1="вёдра", цель="innaffiare {b} {Ub}",
             шаги=("riempire {a} {U1a}", "innaffiare {b} {Ub}"), к=("riempire i {U1сл}", "innaffiare le {Uсл}")),
        dict(имя="ящики", ед="ящики", цель="caricare {s} {Us}", готово="caricate",
             шаги=("raccogliere {a} {Ua}", "raccogliere {c} {Uc} in più", "caricare tutte le {Uсл}"),
             к=("raccogliere le {Uсл}", "caricare le {Uсл}")),
        dict(имя="книги", ед="книги", цель="mettere via {s} {Us}", готово="messi via",
             шаги=("mettere {a} {Ua}", "mettere {c} {Uc} in più", "chiudere la borsa"),
             к=("mettere i {Uсл}", "chiudere la borsa")),
    ),
    "pt": (
        dict(имя="булки", ед="булки", ед1="пачки", цель="fazer {b} {Ub}",
             шаги=("comprar {a} {U1a}", "fazer {b} {Ub}"), к=("comprar os {U1сл}", "fazer os {Uсл}")),
        dict(имя="грядки", ед="грядки", ед1="вёдра", цель="regar {b} {Ub}",
             шаги=("encher {a} {U1a}", "regar {b} {Ub}"), к=("encher os {U1сл}", "regar os {Uсл}")),
        dict(имя="ящики", ед="ящики", цель="carregar {s} {Us}", готово="carregadas",
             шаги=("juntar {a} {Ua}", "juntar mais {c} {Uc}", "carregar todas as {Uсл}"),
             к=("juntar as {Uсл}", "carregar as {Uсл}")),
        dict(имя="книги", ед="книги", цель="arrumar {s} {Us}", готово="arrumados",
             шаги=("pôr {a} {Ua}", "pôr mais {c} {Uc}", "fechar a mochila"),
             к=("pôr os {Uсл}", "fechar a mochila")),
    ),
    "nl": (
        dict(имя="булки", ед="булки", ед1="пачки", цель="{b} {Ub} bakken",
             шаги=("{a} {U1a} kopen", "{b} {Ub} bakken"), к=("de {U1сл} kopen", "de {Uсл} bakken")),
        dict(имя="грядки", ед="грядки", ед1="вёдра", цель="{b} {Ub} begieten",
             шаги=("{a} {U1a} vullen", "{b} {Ub} begieten"), к=("de {U1сл} vullen", "de {Uсл} begieten")),
        dict(имя="ящики", ед="ящики", цель="{s} {Us} laden", готово="geladen",
             шаги=("{a} {Ua} verzamelen", "nog {c} {Uc} verzamelen", "alle {Uсл} laden"),
             к=("de {Uсл} verzamelen", "de {Uсл} laden")),
        dict(имя="книги", ед="книги", цель="{s} {Us} inpakken", готово="ingepakt",
             шаги=("{a} {Ua} inleggen", "nog {c} {Uc} inleggen", "de tas sluiten"),
             к=("de {Uсл} inleggen", "de tas sluiten")),
    ),
    "pl": (
        dict(имя="булки", ед="булки", ед1="пачки", цель="upiec {b} {Ub}",
             шаги=("kupić {a} {U1a}", "upiec {b} {Ub}"), к=("kupić {U1сл}", "upiec {Uсл}")),
        dict(имя="грядки", ед="грядки", ед1="вёдра", цель="podlać {b} {Ub}",
             шаги=("napełnić {a} {U1a}", "podlać {b} {Ub}"), к=("napełnić {U1сл}", "podlać {Uсл}")),
        dict(имя="ящики", ед="ящики", цель="załadować {s} {Us}", готово="załadowane",
             шаги=("zebrać {a} {Ua}", "zebrać jeszcze {c} {Uc}", "załadować wszystkie {Uсл}"),
             к=("zebrać {Uсл}", "załadować {Uсл}")),
        dict(имя="книги", ед="книги", цель="spakować {s} {Us}", готово="spakowane",
             шаги=("włożyć {a} {Ua}", "włożyć jeszcze {c} {Uc}", "zamknąć plecak"),
             к=("włożyć {Uсл}", "zamknąć plecak")),
    ),
}
for _я, _зз in ЗАДАЧИ.items():
    assert len(_зз) == 4, _я
    for _з in _зз:
        assert _з["ед"] in ЕДИНИЦЫ[_я], (_я, _з["имя"])
        assert (len(_з["шаги"]) == 2) == ("ед1" in _з), (_я, _з["имя"], "two steps need a second unit")
        assert (len(_з["шаги"]) == 3) == ("готово" in _з), (_я, _з["имя"], "three steps need a participle")


# «СКОЛЬКО» — одно слово там, где язык его не гнёт, и слово по роду единицы там, где гнёт
СК_СЛОВО = {"ru": "сколько", "en": "how many", "de": "wie viele", "fr": "combien de",
            "nl": "hoeveel", "pl": "ile"}
ИЛИ = {"ru": "или", "en": "or", "de": "oder", "fr": "ou", "es": "o", "it": "o", "pt": "ou",
       "nl": "of", "pl": "czy"}
# ФРАНЦУЗСКАЯ ТИПОГРАФИКА СТАВИТ ПРОБЕЛ ПЕРЕД ВОПРОСОМ, испанский — знак в начале; и то и другое
# есть дело языка, а не дома, и потому объявлено, а не вписано в каждую рамку.
ЗВ = {я: (" ?" if я == "fr" else "?") for я in ЯЗЫКИ}
# и двоеточие: французский отбивает его пробелом
ДВ = {я: (" :" if я == "fr" else ":") for я in ЯЗЫКИ}
ВОПР_НАЧАЛО = {я: ("¿" if я == "es" else "") for я in ЯЗЫКИ}
# СОСТОЯНИЕ ПОСЛЕ ШАГА И НЕДОСТАЧА — целыми фразами языка: порядок слов немецкого («gibt es»,
# «nötig») и предлоги романских не выводятся склейкой, и дом их не угадывает.
СОСТОЯНИЕ = {
    "ru": "после шага 2 есть {f} {Uf}.", "en": "after step 2 there are {f} {Uf}.",
    "de": "nach Schritt 2 gibt es {f} {Uf}.", "fr": "après l'étape 2 il y a {f} {Uf}.",
    "es": "después del paso 2 hay {f} {Uf}.", "it": "dopo il passo 2 ci sono {f} {Uf}.",
    "pt": "depois do passo 2 há {f} {Uf}.", "nl": "na stap 2 zijn er {f} {Uf}.",
    "pl": "po kroku 2 jest {f} {Uf}.",
}
НЕДОСТАЧА = {
    "ru": "{В}: нужно {s} {Us}, есть {f} {Uf}.", "en": "{В}: {s} {Us} needed, {f} {Uf} present.",
    "de": "{В}: {s} {Us} nötig, {f} {Uf} vorhanden.", "fr": "{В} : il faut {s} {Us}, il y a {f} {Uf}.",
    "es": "{В}: hacen falta {s} {Us}, hay {f} {Uf}.", "it": "{В}: servono {s} {Us}, ci sono {f} {Uf}.",
    "pt": "{В}: são precisos {s} {Us}, há {f} {Uf}.", "nl": "{В}: {s} {Us} nodig, er zijn {f} {Uf}.",
    "pl": "{В}: potrzeba {s} {Us}, jest {f} {Uf}.",
}

# РАМКИ ФОРМ: план целиком стоит в показе, вопрос спрашивает о шаге или об итоге, ответ —
# полным предложением; там, где есть счёт, ответ несёт леджер.
РАМКИ = {}
for _я in ЯЗЫКИ:
    _с, _зв, _вн, _дв = СЛОВА[_я], ЗВ[_я], ВОПР_НАЧАЛО[_я], ДВ[_я]
    РАМКИ[_я] = {
        "план_два_шага": ("{ПЛ}" + _дв + " {Ц}. {ПЛАН}. " + _вн + "{СК1} {U1мн} " + _с["после"] + " 1" + _зв
                          + " {a} {U1a}. " + _вн + "{СК} {Uмн} " + _с["после"] + " 2" + _зв
                          + " {b} {Ub}. " + _с["вопрос_готово"] + " {В}" + _дв + " {b} {Ub}."),
        "план_три_шага": ("{ПЛ}" + _дв + " {Ц}. {ПЛАН}. " + _вн + "{СК} {Uмн} " + _с["после"] + " 2" + _зв
                          + " {s} {Us}" + _дв + " {a} + {c} = {s}. " + _с["вопрос_готово"] + " {В}"
                          + _дв + " {s} {Us} {ГОТОВО}."),
        "шаг_не_выполнен": "{ПЛ}" + _дв + " {Ц}. {ПЛАН}. " + СОСТОЯНИЕ[_я] + " " + _с["вопрос_готово"] + " " + НЕДОСТАЧА[_я],
        "порядок_шагов": ("{ПЛ}" + _дв + " {Ц}. {ПЛАН}. " + _с["что_раньше"] + _дв + " {К1} " + ИЛИ[_я] + " {К2}" + _зв
                          + " " + _с["раньше"] + " {КОТВ}."),
        "сколько_шагов": "{ПЛ}" + _дв + " {Ц}. {ПЛАН}. " + _с["сколько_шагов"] + " {N} {ШАГN}.",
    }
ФОРМЫ = ("план_два_шага", "план_три_шага", "шаг_не_выполнен", "порядок_шагов", "сколько_шагов")
ДВУХШАГОВЫЕ = ("план_два_шага",)
ТРЁХШАГОВЫЕ = ("план_три_шага", "шаг_не_выполнен")

# НАБОРЫ ЧИСЕЛ: (a, b) для двух шагов — второй шаг считает СВОЁ; (a, c) для трёх — первые два
# считают ОДНО и складываются, s = a + c, а недостача f выведена правилом, не выбрана рукой.
ДВА = ((2, 12), (3, 18), (4, 24), (5, 15), (6, 30), (2, 14), (3, 21), (4, 16), (5, 25), (6, 18),
       (7, 28), (3, 27), (2, 16), (4, 20), (5, 35), (6, 24), (7, 14), (8, 32), (3, 12), (4, 28))
ТРИ = ((5, 4), (7, 6), (9, 3), (11, 8), (6, 5), (12, 7), (8, 9), (13, 4), (10, 6), (14, 5),
       (15, 8), (9, 7), (16, 3), (11, 6), (17, 4), (12, 9), (18, 5), (13, 8), (19, 6), (14, 7))


def _счёт(язык, ключ, c):
    return S._счёт(ЕДИНИЦЫ[язык][ключ][0], c, язык)


def _сколько(язык, ключ):
    """The question word: one word, or the word bent by the unit's gender."""
    if язык in КСК:
        return КСК[язык][0 if ЕДИНИЦЫ[язык][ключ][1] == "m" else 1]
    return СК_СЛОВО[язык]


def _недостача(s, a):
    """The shortfall is DERIVED, not chosen: fewer than the goal, and never nought."""
    return max(1, s - (a % 3 + 1))


def _короткие(язык, задача):
    """The two steps as short phrases, with their units in the dictionary plural."""
    поля = {"Uсл": СЛОВАРНОЕ_МН[язык][задача["ед"]]}
    if "ед1" in задача:
        поля["U1сл"] = СЛОВАРНОЕ_МН[язык][задача["ед1"]]
    return tuple(ф.format(**поля) for ф in задача["к"])


def _полная_рамка(язык, форма, задача):
    """The frame with the plan written into it — the holes of the numbers stay holes."""
    план = ", ".join(f"{СЛОВА[язык]['шаг']} {i + 1} — {ш}" for i, ш in enumerate(задача["шаги"]))
    рамка = РАМКИ[язык][форма].replace("{Ц}", задача["цель"]).replace("{ПЛАН}", план)
    рамка = рамка.replace("{К1}", задача["к"][0]).replace("{К2}", задача["к"][1])
    if "готово" in задача:
        рамка = рамка.replace("{ГОТОВО}", задача["готово"])
    return рамка


def _поля(язык, задача, числа):
    ед, ед1 = задача["ед"], задача.get("ед1")
    п = dict(ПЛ=СЛОВА[язык]["план"], СК=_сколько(язык, ед), Uсл=СЛОВАРНОЕ_МН[язык][ед],
             Uмн=_счёт(язык, ед, 5),
             N=len(задача["шаги"]), ШАГN=S._счёт(ШАГ_СЛОВО[язык], len(задача["шаги"]), язык), В=ДА[язык])
    п["КОТВ"] = _короткие(язык, задача)[0]
    if len(задача["шаги"]) == 2:
        a, b = числа
        п.update(a=a, b=b, U1a=_счёт(язык, ед1, a), Ub=_счёт(язык, ед, b),
                 СК1=_сколько(язык, ед1), U1сл=СЛОВАРНОЕ_МН[язык][ед1], U1мн=_счёт(язык, ед1, 5))
    else:
        a, c = числа
        s = a + c
        п.update(a=a, c=c, s=s, f=_недостача(s, a), Ua=_счёт(язык, ед, a), Uc=_счёт(язык, ед, c),
                 Us=_счёт(язык, ед, s), Uf=_счёт(язык, ед, _недостача(s, a)))
    return п


def страница(язык, форма, зi, чi, вердикт=None):
    задача = ЗАДАЧИ[язык][зi % len(ЗАДАЧИ[язык])]
    двух = len(задача["шаги"]) == 2
    if (форма in ДВУХШАГОВЫЕ) != двух and форма in ДВУХШАГОВЫЕ:
        return None
    if форма in ТРЁХШАГОВЫЕ and двух:
        return None
    числа = (ДВА if двух else ТРИ)[чi % len(ДВА)]
    п = _поля(язык, задача, числа)
    if форма == "шаг_не_выполнен":
        п["В"] = НЕТ[язык]
    if вердикт is not None:
        п["В"] = вердикт
    return _полная_рамка(язык, форма, задача).format(**п)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for зi in range(len(ЗАДАЧИ[язык])):
            for чi in range(len(ДВА)):
                for форма in ФОРМЫ:
                    с = страница(язык, форма, зi, чi)
                    if с:
                        вон[с] = (язык, форма)
    return вон


ПОКАЗЫ = _показы()


def _формы_единицы(язык, ключ):
    """Every form the unit wears: the count forms of the pack's rule and the dictionary plural."""
    формы = {_счёт(язык, ключ, c) for c in range(0, 60)}
    формы.add(СЛОВАРНОЕ_МН[язык][ключ])
    return формы


_ДЫРА = re.compile(r"\{([^}]+)\}")


def _образец(язык, форма, задача):
    """One pattern over the whole page; the i-th occurrence of a hole is the group «h_hole__i»."""
    alt = lambda слова: "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"
    ед, ед1 = задача["ед"], задача.get("ед1")
    свои = alt(_формы_единицы(язык, ед))
    дыры = {"ПЛ": re.escape(СЛОВА[язык]["план"]), "СК": alt(КСК.get(язык, (СК_СЛОВО.get(язык, ""),))),
            "В": alt((ДА[язык], НЕТ[язык])), "ШАГN": alt({S._счёт(ШАГ_СЛОВО[язык], c, язык) for c in (1, 2, 3, 4, 5)}),
            "КОТВ": alt(_короткие(язык, задача)), "a": r"\d+", "b": r"\d+", "c": r"\d+", "s": r"\d+", "f": r"\d+", "N": r"\d+",
            "Uмн": свои, "Uсл": свои, "Ua": свои, "Ub": свои, "Uc": свои, "Us": свои, "Uf": свои}
    if ед1:
        свои1 = alt(_формы_единицы(язык, ед1))
        дыры.update({"СК1": alt(КСК.get(язык, (СК_СЛОВО.get(язык, ""),))), "U1мн": свои1, "U1сл": свои1, "U1a": свои1})
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", _полная_рамка(язык, форма, задача)):
        if кусок.startswith("{"):
            д = кусок[1:-1]
            счёт[д] = счёт.get(д, 0) + 1
            куски.append(f"(?P<h_{д}__{счёт[д]}>{дыры[д]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, форма, задача), язык, форма, зi)
           for язык in ЯЗЫКИ for зi, задача in enumerate(ЗАДАЧИ[язык]) for форма in ФОРМЫ
           if страница(язык, форма, зi, 0) is not None]


def _вердикт(язык, форма, зi, м):
    """The plan checks itself: repeated holes agree, forms are the forms of their numbers, the
    sum after step 2 is the sum of the steps, and the verdict follows the numbers."""
    задача = ЗАДАЧИ[язык][зi]
    ед, ед1 = задача["ед"], задача.get("ед1")
    значения = {}
    for ключ, v in м.groupdict().items():
        д = ключ[2:].rsplit("__", 1)[0]
        if д in значения and значения[д] != v:
            return False
        значения[д] = v
    число = lambda д: int(значения[д]) if д in значения else None
    a, b, c, s, f, N = (число(д) for д in ("a", "b", "c", "s", "f", "N"))
    # формы единиц суть формы своих чисел; множественное вопроса и словарное — свои
    for дыра, ключ, n in (("Ua", ед, a), ("Ub", ед, b), ("Uc", ед, c), ("Us", ед, s), ("Uf", ед, f), ("U1a", ед1, a)):
        if дыра in значения and ключ is not None and n is not None and значения[дыра] != _счёт(язык, ключ, n):
            return False
    for дыра, ключ in (("Uмн", ед), ("U1мн", ед1)):
        if дыра in значения and ключ is not None and значения[дыра] != _счёт(язык, ключ, 5):
            return False
    for дыра, ключ in (("Uсл", ед), ("U1сл", ед1)):
        if дыра in значения and ключ is not None and значения[дыра] != СЛОВАРНОЕ_МН[язык][ключ]:
            return False
    if s is not None and a is not None and c is not None and s != a + c:
        return False                      # the number after step 2 is the sum of steps 1 and 2
    if форма == "шаг_не_выполнен":
        if f is None or s is None or not (1 <= f < s):
            return False                  # the shortfall falls short — and is named
        if значения.get("В") != НЕТ[язык]:
            return False                  # a task that falls short is NOT done
    elif "В" in значения and значения["В"] != ДА[язык]:
        return False                      # a plan that reaches its goal IS done
    if "КОТВ" in значения and значения["КОТВ"] != _короткие(язык, задача)[0]:
        return False                      # what to do first is the FIRST step of the plan
    if форма == "сколько_шагов":
        if N != len(задача["шаги"]):
            return False                  # the length of the plan is the length of the plan
        if значения.get("ШАГN") != S._счёт(ШАГ_СЛОВО[язык], N, язык):
            return False
    if форма == "план_два_шага" and (a is None or b is None):
        return False
    return True


def судить(строка):
    """(судимо, истинно): a page of a plan of the house, and its numbers hold; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма, зi in ОБРАЗЦЫ:
        м = образ.match(с)
        if м:
            return True, _вердикт(язык, форма, зi, м)
    return False, False


def _хвост(с):
    """The start of the answer — after the last question mark."""
    м = list(re.finditer(r"[?？] ", с))
    return м[-1].end() if м else 0


def _иной_вердикт(с, было, стало):
    """The verdict swapped WHERE IT STANDS — after the last question mark; «да» also lives inside
    «задача» and «no» inside a dozen Spanish words, and a blind replace would break the frame."""
    хв = _хвост(с)
    assert с[хв:].startswith(было), (с, было)
    return с[:хв] + стало + с[хв + len(было):]


def _иное_число_шагов(язык, хвост):
    """The answer «2 steps» made «3 steps» — number and count form move together, the stop stays."""
    м = re.search(r"(\d+)(\s+)(\S+?)(\W*)$", хвост)
    n = int(м.group(1)) + 1
    return хвост[:м.start()] + f"{n}{м.group(2)}{S._счёт(ШАГ_СЛОВО[язык], n, язык)}{м.group(4)}"


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        # (1) ИТОГ ШАГА НЕ СХОДИТСЯ: сумма после шага 2 подменена
        три = страница(язык, "план_три_шага", 2, 0)
        битая = re.sub(r"= (\d+)\.", lambda м: f"= {int(м.group(1)) + 1}.", три, 1)
        assert судить(битая) == (True, False), битая
        # (2) «ДА» ПРИ НЕДОСТАЧЕ: невыполненный план объявлен выполненным
        нев = страница(язык, "шаг_не_выполнен", 2, 0)
        assert судить(нев) == (True, True), нев
        assert судить(_иной_вердикт(нев, НЕТ[язык], ДА[язык])) == (True, False), нев
        # (3) «НЕТ» ПРИ ДОСТАТКЕ: выполненный план объявлен невыполненным
        assert судить(_иной_вердикт(три, ДА[язык], НЕТ[язык])) == (True, False), три
        # (4) ПОРЯДОК ШАГОВ ПЕРЕСТАВЛЕН: ответ называет второй шаг
        пор = страница(язык, "порядок_шагов", 0, 0)
        к1, к2 = _короткие(язык, ЗАДАЧИ[язык][0])
        хв = _хвост(пор)
        assert судить(пор[:хв] + пор[хв:].replace(к1, к2, 1)) == (True, False), пор
        # (5) ЧИСЛО ШАГОВ НЕ ПО ПЛАНУ
        скш = страница(язык, "сколько_шагов", 0, 0)
        хв = _хвост(скш)
        assert судить(скш[:хв] + _иное_число_шагов(язык, скш[хв:])) == (True, False), скш
        # (6) СЧЁТНАЯ ФОРМА НЕ ПО ЧИСЛУ (там, где язык её гнёт)
        дв = страница(язык, "план_два_шага", 0, 0)
        своя, иная = _счёт(язык, "булки", 12), _счёт(язык, "булки", 1)
        if своя != иная:
            хв = _хвост(дв)
            assert судить(дв[:хв] + дв[хв:].replace(своя, иная, 1)) == (True, False), дв
            мутанты += 1
        мутанты += 5
    for я, ф in (("ru", "план_два_шага"), ("ru", "план_три_шага"), ("en", "план_три_шага"),
                 ("de", "шаг_не_выполнен"), ("fr", "порядок_шагов"), ("es", "сколько_шагов"),
                 ("it", "план_два_шага"), ("pl", "шаг_не_выполнен"), ("nl", "план_три_шага"),
                 ("pt", "порядок_шагов")):
        print("  ", next(с for с, м in ПОКАЗЫ.items() if м == (я, ф))[:170])
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, задач {len(ЗАДАЧИ['ru'])}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
