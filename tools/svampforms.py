#!/usr/bin/env python3
"""THE HOUSE OF SVAMP SHAPES — the eight mute shapes of the live SVAMP band (d5, 06.09),
each a form with its recomputing court, in English and Russian.

d5 read the live band (726 tacts) and named what no frame of the corpus holds:
(1) oblique pronouns as pronouns («gave 5 of them», «gave him 20»); (2) place held
by a bare «were» — closed in the house of action measure; (3) the hidden quantity
«some» and the heads of the total («in all», «altogether», «in total», «a total
of», «now has N left»); (4) the words of time order («at first … then»); (5) the
hypothetical act in the question («if she gives away 64, how many will she
have?»); (6) transfer with a direction («gave 20 to him» = «gave him 20», «took
5 from her»); (7) the unit before the number («$ 3») — English only, declared;
(8) goods outside the lexicon («2 pages of reading homework and 4 pages of math
homework»). Names and things are the house of action pages' (tools/actionpages.py),
pronouns are declared here by gender; every answer carries its ledger, and the
court recomputes it. The world is CLOSED.

    python3 tools/svampforms.py    # self-check with mutants
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import plgram as _PL  # noqa: E402 — закон польской связки: один закон, один читатель
import rugram as _RU  # noqa: E402 — закон русского прошедшего: один закон, один читатель
_RUG = _RU
import actionpages as A  # noqa: E402

_ПАКЕТЫ = pathlib.Path(__file__).resolve().parent / "langpacks"

# pronouns by gender: nominative, genitive-with-у (ru) / object (en), dative (ru) / object (en)
МЕСТОИМЕНИЯ = {"en": {"m": dict(он="he", него="him", ему="him"), "f": dict(он="she", него="her", ему="her")},
               "ru": {"m": dict(он="он", него="него", ему="ему"), "f": dict(он="она", него="неё", ему="ей")},
               "de": {"m": dict(он="er", него="ihm", ему="ihm"), "f": dict(он="sie", него="ihr", ему="ihr")},
               "fr": {"m": dict(он="il", него="lui", ему="lui"), "f": dict(он="elle", него="elle", ему="lui")},
               "es": {"m": dict(он="él", него="él", ему="le"), "f": dict(он="ella", него="ella", ему="le")},
               "it": {"m": dict(он="lui", него="lui", ему="gli"), "f": dict(он="lei", него="lei", ему="le")},
               "pt": {"m": dict(он="ele", него="ele", ему="lhe"), "f": dict(он="ela", него="ela", ему="lhe")},
               "nl": {"m": dict(он="hij", него="hem", ему="hem"), "f": dict(он="ze", него="haar", ему="haar")},
               "pl": {"m": dict(он="on", него="niego", ему="mu"), "f": dict(он="ona", него="niej", ему="jej")}}
ГОЛОВЫ_ИТОГА = {"en": ("in all", "altogether", "in total"), "ru": ("всего", "в сумме", "итого"), "de": ("insgesamt", "zusammen", "im Ganzen"),
                "fr": ("en tout", "au total", "en tout et pour tout"), "es": ("en total", "en conjunto", "en suma"), "it": ("in tutto", "in totale", "complessivamente"),
                "pt": ("no total", "ao todo", "em conjunto"), "nl": ("in totaal", "bij elkaar", "alles bij elkaar"), "pl": ("razem", "łącznie", "w sumie")}
ВРЕМЯ = {"en": (("at first", "then"), ("initially", "later"), ("originally", "finally"), ("at the start", "then")),
         "ru": (("сначала", "потом"), ("вначале", "затем"), ("изначально", "позже")),
         "de": (("zuerst", "dann"), ("anfangs", "später"), ("am Anfang", "danach")), "fr": (("d'abord", "puis"), ("au début", "ensuite"), ("à l'origine", "plus tard")),
         "es": (("al principio", "luego"), ("primero", "después"), ("inicialmente", "más tarde")), "it": (("all'inizio", "poi"), ("prima", "dopo"), ("inizialmente", "più tardi")),
         "pt": (("no início", "depois"), ("primeiro", "a seguir"), ("inicialmente", "mais tarde")), "nl": (("eerst", "daarna"), ("aanvankelijk", "later"), ("in het begin", "toen")),
         "pl": (("najpierw", "potem"), ("na początku", "później"), ("początkowo", "następnie"))}
ЦВЕТА = {"en": ("red", "blue"), "ru": ("красных", "синих"), "de": ("rote", "blaue"), "fr": ("rouges", "bleues"), "es": ("rojas", "azules"),
         "it": ("rosse", "blu"), "pt": ("vermelhas", "azuis"), "nl": ("rode", "blauwe"), "pl": ("czerwonych", "niebieskich")}
# A FRACTION OF THE THINGS (sweep of the sixth point, 05.09: stories with shares — 41 mute in en, the
# largest reasoning class after holdings): the share is a DECLARED WORD, its denominator is the
# ledger's divisor («a third of them are red: 12 ÷ 3 = 4»); the colour is a predicate that does not
# bend with the thing's gender (fr rouges/jaunes, es verdes/azules, it verdi/blu, pt verdes/azuis)
ДОЛИ = {"en": {2: "half", 3: "a third", 4: "a quarter"}, "ru": {2: "половина", 3: "треть", 4: "четверть"},
        "de": {2: "die Hälfte", 3: "ein Drittel", 4: "ein Viertel"}, "fr": {2: "la moitié", 3: "un tiers", 4: "un quart"},
        "es": {2: "la mitad", 3: "un tercio", 4: "un cuarto"}, "it": {2: "la metà", 3: "un terzo", 4: "un quarto"},
        "pt": {2: "metade", 3: "um terço", 4: "um quarto"}, "nl": {2: "de helft", 3: "een derde", 4: "een kwart"},
        "pl": {2: "połowa", 3: "jedna trzecia", 4: "jedna czwarta"}}
ЦВЕТ_ПРЕД = {"en": ("red", "blue"), "ru": ("красные", "синие"), "de": ("rot", "blau"), "fr": ("rouges", "jaunes"),
             "es": ("verdes", "azules"), "it": ("verdi", "blu"), "pt": ("verdes", "azuis"), "nl": ("rood", "blauw"),
             "pl": ("czerwone", "niebieskie")}
# Polish dative of the names (the pack declares gender only)
ДАТЕЛЬНЫЙ_PL = {"Anna": "Annie", "Jan": "Janowi", "Maria": "Marii", "Piotr": "Piotrowi", "Zofia": "Zofii", "Paweł": "Pawłowi", "Ewa": "Ewie", "Marek": "Markowi"}
# THE PARENT AND THE PAIR BEND BY THE BEARER'S GENDER (d5, live band p156, 05.09: nine of twelve
# lies of the grove stand on unbought pronouns — «his strawberries», «together their strawberries»,
# «gave HIM 20», «bought 140 cakes FROM HIM», «leaving HIM with 27»): the possessive parent (his
# father / her mother — the bearer's gender picks both words), its Russian genitive after «у», the
# bare parent of the name's possessive («Marco's father», «у отца Марко», «le père de Louis»), and
# the pair's word where the language bends it (fr ils/elles, es/pt juntos/juntas)
РОДНЯ = {
    "en": {"m": dict(Р="his father", Рб="father", они="they"), "f": dict(Р="her mother", Рб="mother", они="they")},
    "ru": {"m": dict(Р="его отец", Рр="его отца", Рб="отца"), "f": dict(Р="её мать", Рр="её матери", Рб="матери")},
    "de": {"m": dict(Р="sein Vater", Рб="der Vater", они="sie"), "f": dict(Р="ihre Mutter", Рб="die Mutter", они="sie")},
    "fr": {"m": dict(Р="son père", Рб="le père", они="ils"), "f": dict(Р="sa mère", Рб="la mère", они="elles")},
    "es": {"m": dict(Р="su padre", Рб="el padre", вместе="juntos"), "f": dict(Р="su madre", Рб="la madre", вместе="juntas")},
    "it": {"m": dict(Р="suo padre", Рб="il padre"), "f": dict(Р="sua madre", Рб="la madre")},
    "pt": {"m": dict(Р="o pai dele", Рб="o pai", вместе="juntos"), "f": dict(Р="a mãe dela", Рб="a mãe", вместе="juntas")},
    "nl": {"m": dict(Р="zijn vader", Рб="de vader", они="ze"), "f": dict(Р="haar moeder", Рб="de moeder", они="ze")},
    "pl": {"m": dict(Р="jego tata", Рб="tata"), "f": dict(Р="jej mama", Рб="mama")},
}
# Polish genitive of the names (the pack declares gender only): «tata Marka», «mama Anny»
РОДИТЕЛЬНЫЙ_PL = {"Anna": "Anny", "Jan": "Jana", "Maria": "Marii", "Piotr": "Piotra", "Zofia": "Zofii", "Paweł": "Pawła", "Ewa": "Ewy", "Marek": "Marka"}
# goods outside the lexicon: (two kinds, the union), count forms one/many (ru: one/few/many)
ТОВАРЫ = {"en": ((("page of reading homework", "pages of reading homework"), ("page of math homework", "pages of math homework"), ("page of homework", "pages of homework")),
                 (("pack of red cards", "packs of red cards"), ("pack of blue cards", "packs of blue cards"), ("pack of cards", "packs of cards")),
                 (("box of apples", "boxes of apples"), ("box of pears", "boxes of pears"), ("box of fruit", "boxes of fruit"))),
          "ru": ((("страница чтения", "страницы чтения", "страниц чтения"), ("страница математики", "страницы математики", "страниц математики"), ("страница", "страницы", "страниц")),
                 (("пачка красных карт", "пачки красных карт", "пачек красных карт"), ("пачка синих карт", "пачки синих карт", "пачек синих карт"), ("пачка карт", "пачки карт", "пачек карт")),
                 (("коробка яблок", "коробки яблок", "коробок яблок"), ("коробка груш", "коробки груш", "коробок груш"), ("коробка фруктов", "коробки фруктов", "коробок фруктов"))),
          "de": ((("Seite Lesehausaufgaben", "Seiten Lesehausaufgaben"), ("Seite Mathehausaufgaben", "Seiten Mathehausaufgaben"), ("Seite Hausaufgaben", "Seiten Hausaufgaben")),
                 (("Kiste Äpfel", "Kisten Äpfel"), ("Kiste Birnen", "Kisten Birnen"), ("Kiste Obst", "Kisten Obst"))),
          "fr": ((("page de lecture", "pages de lecture"), ("page de maths", "pages de maths"), ("page de devoirs", "pages de devoirs")),
                 (("caisse de pommes", "caisses de pommes"), ("caisse de poires", "caisses de poires"), ("caisse de fruits", "caisses de fruits"))),
          "es": ((("página de lectura", "páginas de lectura"), ("página de matemáticas", "páginas de matemáticas"), ("página de deberes", "páginas de deberes")),
                 (("caja de manzanas", "cajas de manzanas"), ("caja de peras", "cajas de peras"), ("caja de fruta", "cajas de fruta"))),
          "it": ((("pagina di lettura", "pagine di lettura"), ("pagina di matematica", "pagine di matematica"), ("pagina di compiti", "pagine di compiti")),
                 (("cassa di mele", "casse di mele"), ("cassa di pere", "casse di pere"), ("cassa di frutta", "casse di frutta"))),
          "pt": ((("página de leitura", "páginas de leitura"), ("página de matemática", "páginas de matemática"), ("página de trabalhos", "páginas de trabalhos")),
                 (("caixa de maçãs", "caixas de maçãs"), ("caixa de peras", "caixas de peras"), ("caixa de fruta", "caixas de fruta"))),
          "nl": ((("pagina leeshuiswerk", "pagina's leeshuiswerk"), ("pagina rekenhuiswerk", "pagina's rekenhuiswerk"), ("pagina huiswerk", "pagina's huiswerk")),
                 (("kist appels", "kisten appels"), ("kist peren", "kisten peren"), ("kist fruit", "kisten fruit"))),
          "pl": ((("strona czytania", "strony czytania", "stron czytania"), ("strona matematyki", "strony matematyki", "stron matematyki"), ("strona", "strony", "stron")),
                 (("skrzynka jabłek", "skrzynki jabłek", "skrzynek jabłek"), ("skrzynka gruszek", "skrzynki gruszek", "skrzynek gruszek"), ("skrzynka owoców", "skrzynki owoców", "skrzynek owoców")))}

РАМКИ = {
    "en": dict(
        пришло_скрыто="{X} had {n} {Тn}. {Он} got {СК} more {Тмн}. now {он} has {s} {Тs}. how many {Тмн} did {он} get? {k}: {s} − {n} = {k}.",
        ушло_скрыто="{X} had {n} {Тn}. {Он} lost {СК} {Тмн}. now {он} has {r} {Тr}. how many {Тмн} did {он} lose? {k}: {n} − {r} = {k}.",
        часть_из_них="{X} had {n} {Тn}. {Он} sold {СКЧ}. now {он} has {r} {Тr}. how many {Тмн} did {он} sell? {k}: {n} − {r} = {k}.",
        взял_скрыто="{X} had {n} {Тn}. {Y} took {СК} {Тмн} from {него}. now {он} has {r} {Тr}. how many {Тмн} did {Y} take? {k}: {n} − {r} = {k}.",
        некоторые="{X} had {n} {Тn}. {Он} gave some of them away. now {он} has {r} {Тr} left. how many {Тмн} did {он} give away? {k}: {n} − {r} = {k}.",
        итог="{X} has {a} {Ц1} {Тмн} and {b} {Ц2} {Тмн}. how many {Тмн} does {X} have {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        итог_всего="{X} has {a} {Ц1} {Тмн} and {b} {Ц2} {Тмн}. how many {Тмн} does {X} have? a total of {s} {Тs}: {a} + {b} = {s}.",
        осталось="{X} had {n} {Тn}. {Он} gave away {k}. how many does {он} have now? {он} now has {r} left: {n} − {k} = {r}.",
        из_них="{X} had {n} {Тn}. {Он} gave {k} of them to {Y}. how many {Тмн} does {он} have now? {r}: {n} − {k} = {r}.",
        ему="{X} had {n} {Тn}. {Y} gave {ему} {k} more. how many {Тмн} does {он} have now? {s}: {n} + {k} = {s}.",
        три="{X} collected {n} {Тn}. {X} bought {k} more. {он} lost {m} of them. how many {Тмн} does {X} have left? {t}: {n} + {k} − {m} = {t}.",
        три_шаги="{X} collected {n} {Тn}. {X} bought {k} more. {он} lost {m} of them. how many {Тмн} does {X} have left? step 1: {n} + {k} = {s}. step 2: {s} − {m} = {t}. total: {t}.",
        владеет="{X} has {n} {Тn}. how many {Тмн} does {X} own? {X} owns {n} {Тn}.",
        владеет2="{X} has {n} {Тn}. how many {Тмн} does {X} possess? {X} possesses {n} {Тn}.",
        держит="{X} has {n} {Тn}. {Он} finds {k} more. how many {Тмн} does {X} hold now? {X} holds {s} {Тs}: {n} + {k} = {s}.",
        хранит="{X} has {n} {Тn}. {Он} gives away {k}. how many {Тмн} does {X} keep? {X} keeps {r} {Тr}: {n} − {k} = {r}.",
        владеет_после="{X} has {n} {Тn}. {Он} gives away {k}. how many {Тмн} does {X} own now? {X} owns {r} {Тr}: {n} − {k} = {r}.",
        доля="{X} has {n} {Тn}. {ДОЛЯ} of them are {ЦП}. how many {Тмн} are {ЦП}? {r}: {n} ÷ {q} = {r}.",
        доля_не="{X} has {n} {Тn}. {ДОЛЯ} of them are {ЦП}. how many {Тмн} are not {ЦП}? step 1: {n} ÷ {q} = {r}. step 2: {n} − {r} = {d}. total: {d}.",
        возраст_имя="{X} is {n} {Гn} old. how old will {X} be in {k} {Гk}? {X} will be {s} {Гs} old: {n} + {k} = {s}.",
        его_вещи="{X} has {n} {Тn}. {Р} has {k} {Тk}. how many {Тмн} does {X} have? {X} has {n} {Тn}.",
        вместе_их="{X} has {n} {Тn}. {Р} has {k} {Тk}. how many {Тмн} do {они} have together? together {они} have {s} {Тs}: {n} + {k} = {s}.",
        дал_ему="{X} had {n} {Тn}. {Y} gave {ему} {k} {Тk}. how many {Тмн} does {X} have now? {X} has {s} {Тs}: {n} + {k} = {s}.",
        купил_у_него="{X} had {n} {Тn}. {Y} had some too. {Он} bought {k} {Тk} from {негоY}. how many {Тмн} does {X} have now? {X} has {s} {Тs}: {n} + {k} = {s}.",
        оставив_ему="{X} gave {k} {Тk} to {Y}, leaving {него} with {r} {Тr}. how many {Тмн} did {X} have at first? {X} had {n} {Тn}: {k} + {r} = {n}.",
        имя_с_с="{Xде} {Рб} has {k} {Тk}. how many {Тмн} does {Xде} {Рб} have? {Xде} {Рб} has {k} {Тk}.",
        факт="{X} has {n} {Тn}. how many {Тмн} does {X} have? {n}.",
        без_данных="how many {Тмн} does {X} have? I do not know: how many {Тмн} {X} has is not said.",
        собрал_у="{X} collected {n} {Тn}. {Он} lost {k} of them. how many {Тмн} does {X} have left? {r}: {n} − {k} = {r}.",
        потерял="{X} had {n} {Тn}. {Он} lost {k} of them. how many {Тмн} does {он} have left? {r}: {n} − {k} = {r}.",
        купил_ещё="{X} had {n} {Тn}. {Он} bought {k} more. how many {Тмн} does {он} have now? {s}: {n} + {k} = {s}.",
        если="{X} has {n} {Тn}. if {он} gives away {k}, how many will {он} have? {r}: {n} − {k} = {r}.",
        если_придут="there are {n} {Тn} in the box. if {k} more are put in, how many will there be? {s}: {n} + {k} = {s}.",
        время="{В1} {X} had {n} {Тn}. {В2} {он} got {k} more. how many {Тмн} does {он} have now? {s}: {n} + {k} = {s}.",
        кому="{X} had {n} {Тn}. {Он} gave {k} {Тk} to {Y}. how many {Тмн} does {X} have now? {r}: {n} − {k} = {r}.",
        у_него="{X} had {n} {Тn}. {Y} took {k} {Тk} from {него}. how many {Тмн} does {X} have now? {r}: {n} − {k} = {r}.",
        единица="a {Т1} costs $ {n}. how much do {k} {Тмн} cost? $ {v}: {k} × {n} = {v}.",
        товар="{X} has {a} {Г1a} and {b} {Г2b}. how many {Г3мн} does {он} have in all? {s} {Г3s}: {a} + {b} = {s}.",
    ),
    "ru": dict(
        пришло_скрыто="у {Xр} было {n} {Тn}. {Он} получил{а} ещё {СК} {Тмн}. теперь у {него} {s} {Тs}. сколько {Тмн} {он} получил{а}? {k}: {s} − {n} = {k}.",
        ушло_скрыто="у {Xр} было {n} {Тn}. {Он} потерял{а} {СК} {Тмн}. теперь у {него} {r} {Тr}. сколько {Тмн} {он} потерял{а}? {k}: {n} − {r} = {k}.",
        часть_из_них="у {Xр} было {n} {Тn}. {Он} продал{а} {СКЧ}. теперь у {него} {r} {Тr}. сколько {Тмн} {он} продал{а}? {k}: {n} − {r} = {k}.",
        взял_скрыто="у {Xр} было {n} {Тn}. {Y} взял{аY} у {него} {СК} {Тмн}. теперь у {него} {r} {Тr}. сколько {Тмн} взял{аY} {Y}? {k}: {n} − {r} = {k}.",
        некоторые="у {Xр} было {n} {Тn}. {Он} отдал{а} несколько. теперь у {него} осталось {r} {Тr}. сколько {Тмн} {он} отдал{а}? {k}: {n} − {r} = {k}.",
        итог="у {Xр} {a} {Ц1} {Тмн} и {b} {Ц2} {Тмн}. сколько {Тмн} у {Xр} {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        итог_всего="у {Xр} {a} {Ц1} {Тмн} и {b} {Ц2} {Тмн}. сколько {Тмн} у {Xр}? всего {s} {Тs}: {a} + {b} = {s}.",
        осталось="у {Xр} было {n} {Тn}. {Он} отдал{а} {k}. сколько у {него} теперь? теперь у {него} осталось {r}: {n} − {k} = {r}.",
        из_них="у {Xр} было {n} {Тn}. {Он} отдал{а} {k} из них {Yд}. сколько {Тмн} у {него} теперь? {r}: {n} − {k} = {r}.",
        ему="у {Xр} было {n} {Тn}. {Y} дал{аY} {ему} ещё {k}. сколько {Тмн} у {него} теперь? {s}: {n} + {k} = {s}.",
        три="{X} собрал{а} {n} {Тn}. {X} купил{а} ещё {k}. {он} потерял{а} {m} из них. сколько {Тмн} у {Xр} осталось? {t}: {n} + {k} − {m} = {t}.",
        три_шаги="{X} собрал{а} {n} {Тn}. {X} купил{а} ещё {k}. {он} потерял{а} {m} из них. сколько {Тмн} у {Xр} осталось? шаг 1: {n} + {k} = {s}. шаг 2: {s} − {m} = {t}. итог: {t}.",
        владеет="у {Xр} есть {n} {Тn}. сколько {Тмн} имеет {X}? {X} имеет {n} {Тn}.",
        владеет_после="у {Xр} есть {n} {Тn}. {Он} отдаёт {k}. сколько {Тмн} имеет {X} теперь? {X} имеет {r} {Тr}: {n} − {k} = {r}.",
        доля="у {Xр} {n} {Тn}. {ДОЛЯ} из них — {ЦП}. сколько из них {ЦП}? {r}: {n} ÷ {q} = {r}.",
        доля_не="у {Xр} {n} {Тn}. {ДОЛЯ} из них — {ЦП}. сколько из них не {ЦП}? шаг 1: {n} ÷ {q} = {r}. шаг 2: {n} − {r} = {d}. итог: {d}.",
        возраст_имя="{Xд} {n} {Гn}. сколько лет будет {Xд} через {k} {Гk}? {Xд} будет {s} {Гs}: {n} + {k} = {s}.",
        его_вещи="у {Xр} {n} {Тn}. у {Рр} {k} {Тk}. сколько {Тмн} у {Xр}? у {Xр} {n} {Тn}.",
        вместе_их="у {Xр} {n} {Тn}. у {Рр} {k} {Тk}. сколько {Тмн} у них вместе? вместе у них {s} {Тs}: {n} + {k} = {s}.",
        дал_ему="у {Xр} было {n} {Тn}. {Y} дал{аY} {ему} {k} {Тk}. сколько {Тмн} у {Xр} теперь? у {Xр} {s} {Тs}: {n} + {k} = {s}.",
        купил_у_него="у {Xр} было {n} {Тn}. у {Yр} тоже были. {Он} купил{а} у {негоY} {k} {Тk}. сколько {Тмн} у {Xр} теперь? у {Xр} {s} {Тs}: {n} + {k} = {s}.",
        оставив_ему="{X} отдал{а} {k} {Тk} {Yд}, и у {него} осталось {r} {Тr}. сколько {Тмн} было у {Xр} сначала? у {Xр} было {n} {Тn}: {k} + {r} = {n}.",
        имя_с_с="у {Рб} {Xде} {k} {Тk}. сколько {Тмн} у {Рб} {Xде}? у {Рб} {Xде} {k} {Тk}.",
        факт="у {Xр} {n} {Тn}. сколько {Тмн} у {Xр}? {n}.",
        без_данных="сколько {Тмн} у {Xр}? не знаю: сколько {Тмн} у {Xр}, не сказано.",
        собрал_у="{X} собрал{а} {n} {Тn}. {Он} потерял{а} {k} из них. сколько {Тмн} у {Xр} осталось? {r}: {n} − {k} = {r}.",
        потерял="у {Xр} было {n} {Тn}. {Он} потерял{а} {k} из них. сколько {Тмн} у {него} осталось? {r}: {n} − {k} = {r}.",
        купил_ещё="у {Xр} было {n} {Тn}. {Он} купил{а} ещё {k}. сколько {Тмн} у {него} теперь? {s}: {n} + {k} = {s}.",
        если="у {Xр} {n} {Тn}. если {он} отдаст {k}, сколько у {него} останется? {r}: {n} − {k} = {r}.",
        если_придут="в коробке {n} {Тn}. если положить ещё {k}, сколько там будет? {s}: {n} + {k} = {s}.",
        время="{В1} у {Xр} было {n} {Тn}. {В2} {он} получил{а} ещё {k}. сколько {Тмн} у {него} теперь? {s}: {n} + {k} = {s}.",
        кому="у {Xр} было {n} {Тn}. {Он} отдал{а} {k} {Тk} {Yд}. сколько {Тмн} у {Xр} теперь? {r}: {n} − {k} = {r}.",
        у_него="у {Xр} было {n} {Тn}. {Y} взял{аY} у {него} {k} {Тk}. сколько {Тмн} у {Xр} теперь? {r}: {n} − {k} = {r}.",
        товар="у {Xр} {a} {Г1a} и {b} {Г2b}. сколько {Г3мн} у {него} всего? {s} {Г3s}: {a} + {b} = {s}.",
    ),
}
# THE GENDER OF THE THING BENDS THE QUESTION WORD, THE PARTICIPLE, THE PRONOUN AND THE COLOUR
# (05.09): the things of es/it/pt are of mixed gender, and one form «¿cuántas» wrote «¿cuántas
# balones». Keyed by the plural the frame shows; a thing not named here is feminine, the majority.
РОД_ВЕЩЕЙ = {
    "es": {"balones": "m", "libros": "m", "huevos": "m", "bolígrafos": "m"},
    "it": {"palloni": "m", "libri": "m", "fiori": "m"},
    "pt": {"livros": "m", "ovos": "m"},
}
ЦВЕТА_М = {"es": ("rojos", "azules"), "it": ("rossi", "blu"), "pt": ("vermelhos", "azuis")}
# СКРЫТОЕ КОЛИЧЕСТВО — ЭТО НЕ ЧИСЛО, А ЕГО ОТСУТСТВИЕ (05.09, d5: рынок читателя hidden_words
# покупает «несколько / some / einige» как ДЫРУ ЧИСЛА, и на старых ковках он инертен, потому что
# корпус показывал скрытое лишь одной английской формой). Слово скрытого количества объявлено
# здесь таблицей: оно стоит там, где стояло бы число, и восстанавливается ЛЕДЖЕРОМ из двух
# названных чисел истории — иначе строка учила бы догадке, а не счёту. Где язык гнёт слово по
# роду вещи, объявлена пара (мужской, женский) и выбирается тем же родом, что и вопросное слово.
СКРЫТОЕ = {
    "ru": {"несколько": "несколько", "часть": "часть из них"},
    "en": {"несколько": "some", "часть": "some of them"},
    "de": {"несколько": "einige", "часть": "einen Teil davon"},
    "fr": {"несколько": "plusieurs", "часть": "une partie"},
    "es": {"несколько": ("algunos", "algunas"), "часть": "una parte"},
    "it": {"несколько": ("alcuni", "alcune"), "часть": "una parte"},
    "pt": {"несколько": ("alguns", "algumas"), "часть": "uma parte"},
    "nl": {"несколько": "enkele", "часть": "een deel ervan"},
    "pl": {"несколько": "kilka", "часть": "część z nich"},
}
РОДОВЫЕ = {  # hole → (masculine, feminine)
    "es": {"кск": ("cuántos", "cuántas"), "ellas": ("ellos", "ellas"), "algunas": ("algunos", "algunas")},
    "it": {"quante": ("quanti", "quante"), "date": ("dati", "date"), "altre": ("altri", "altre"),
           "alcune": ("alcuni", "alcune"), "ricevute": ("ricevuti", "ricevute")},
    "pt": {"quantas": ("quantos", "quantas"), "delas": ("deles", "delas"), "algumas": ("alguns", "algumas")},
}
РАМКИ.update({
    "de": dict(
        осталось=("{X} hatte {n} {Тn}. {Он} gab {k} weg. wie viele hat {он} jetzt? {он} hat jetzt noch {r}: {n} − {k} = {r}.",
                  "{X} hatte {n} {Тn}. {Он} gab {k} weg. wie viele bleiben übrig? es bleiben {r} übrig: {n} − {k} = {r}."),
        ему="{X} hatte {n} {Тn}. {Y} gab {ему} {k} mehr. wie viele {Тмн} hat {он} jetzt? {s}: {n} + {k} = {s}.",
        если_придут="in der Kiste sind {n} {Тn}. wenn {k} mehr hineingelegt werden, wie viele werden es sein? {s}: {n} + {k} = {s}.",
        у_него="{X} hatte {n} {Тn}. {Y} nahm {ему} {k} {Тk} weg. wie viele {Тмн} hat {X} jetzt? {r}: {n} − {k} = {r}.",
        товар="{X} hat {a} {Г1a} und {b} {Г2b}. wie viele {Г3мн} hat {он} insgesamt? {s} {Г3s}: {a} + {b} = {s}.",
        пришло_скрыто="{X} hatte {n} {Тn}. {Он} bekam noch {СК} {Тмн}. jetzt hat {он} {s} {Тs}. wie viele {Тмн} bekam {он}? {k}: {s} − {n} = {k}.",
        ушло_скрыто="{X} hatte {n} {Тn}. {Он} verlor {СК} {Тмн}. jetzt hat {он} {r} {Тr}. wie viele {Тмн} verlor {он}? {k}: {n} − {r} = {k}.",
        часть_из_них="{X} hatte {n} {Тn}. {Он} verkaufte {СКЧ}. jetzt hat {он} {r} {Тr}. wie viele {Тмн} verkaufte {он}? {k}: {n} − {r} = {k}.",
        взял_скрыто="{X} hatte {n} {Тn}. {Y} nahm {ему} {СК} {Тмн} weg. jetzt hat {он} {r} {Тr}. wie viele {Тмн} nahm {Y} weg? {k}: {n} − {r} = {k}.",
        некоторые="{X} hatte {n} {Тn}. {Он} gab einige weg. jetzt hat {он} noch {r} {Тr}. wie viele {Тмн} gab {он} weg? {k}: {n} − {r} = {k}.",
        итог="{X} hat {a} {Ц1} {Тмн} und {b} {Ц2} {Тмн}. wie viele {Тмн} hat {X} {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        из_них="{X} hatte {n} {Тn}. {Он} gab {k} davon an {Y}. wie viele {Тмн} hat {он} jetzt? {r}: {n} − {k} = {r}.",
        три="{X} sammelte {n} {Тn}. {X} kaufte noch {k}. {он} verlor {m} davon. wie viele {Тмн} hat {X} noch? {t}: {n} + {k} − {m} = {t}.",
        три_шаги="{X} sammelte {n} {Тn}. {X} kaufte noch {k}. {он} verlor {m} davon. wie viele {Тмн} hat {X} noch? Schritt 1: {n} + {k} = {s}. Schritt 2: {s} − {m} = {t}. Ergebnis: {t}.",
        владеет="{X} hat {n} {Тn}. wie viele {Тмн} besitzt {X}? {X} besitzt {n} {Тn}.",
        владеет_после="{X} hat {n} {Тn}. {Он} gibt {k} weg. wie viele {Тмн} besitzt {X} jetzt? {X} besitzt {r} {Тr}: {n} − {k} = {r}.",
        доля="{X} hat {n} {Тn}. {ДОЛЯ} davon ist {ЦП}. wie viele davon sind {ЦП}? {r}: {n} ÷ {q} = {r}.",
        доля_не="{X} hat {n} {Тn}. {ДОЛЯ} davon ist {ЦП}. wie viele davon sind nicht {ЦП}? Schritt 1: {n} ÷ {q} = {r}. Schritt 2: {n} − {r} = {d}. Ergebnis: {d}.",
        возраст_имя="{X} ist {n} {Гn} alt. wie alt wird {X} in {k} {Гk} sein? {X} wird {s} {Гs} alt sein: {n} + {k} = {s}.",
        его_вещи="{X} hat {n} {Тn}. {Р} hat {k} {Тk}. wie viele {Тмн} hat {X}? {X} hat {n} {Тn}.",
        вместе_их="{X} hat {n} {Тn}. {Р} hat {k} {Тk}. wie viele {Тмн} haben {они} zusammen? zusammen haben {они} {s} {Тs}: {n} + {k} = {s}.",
        дал_ему="{X} hatte {n} {Тn}. {Y} gab {ему} {k} {Тk}. wie viele {Тмн} hat {X} jetzt? {X} hat {s} {Тs}: {n} + {k} = {s}.",
        купил_у_него="{X} hatte {n} {Тn}. {Y} hatte auch welche. {Он} kaufte {k} {Тk} von {негоY}. wie viele {Тмн} hat {X} jetzt? {X} hat {s} {Тs}: {n} + {k} = {s}.",
        оставив_ему="{X} gab {Y} {k} {Тk}, womit {ему} {r} {Тr} blieben. wie viele {Тмн} hatte {X} zuerst? {X} hatte {n} {Тn}: {k} + {r} = {n}.",
        имя_с_с="{Рб} {Xде} hat {k} {Тk}. wie viele {Тмн} hat {Рб} {Xде}? {Рб} {Xде} hat {k} {Тk}.",
        факт="{X} hat {n} {Тn}. wie viele {Тмн} hat {X}? {n}.",
        без_данных="wie viele {Тмн} hat {X}? ich weiß es nicht: wie viele {Тмн} {X} hat, ist nicht gesagt.",
        собрал_у="{X} sammelte {n} {Тn}. {Он} verlor {k} davon. wie viele {Тмн} hat {X} noch? {r}: {n} − {k} = {r}.",
        потерял="{X} hatte {n} {Тn}. {Он} verlor {k} davon. wie viele {Тмн} hat {он} noch? {r}: {n} − {k} = {r}.",
        купил_ещё="{X} hatte {n} {Тn}. {Он} kaufte noch {k}. wie viele {Тмн} hat {он} jetzt? {s}: {n} + {k} = {s}.",
        если="{X} hat {n} {Тn}. wenn {он} {k} weggibt, wie viele wird {он} haben? {r}: {n} − {k} = {r}.",
        время="{В1} hatte {X} {n} {Тn}. {В2} bekam {он} {k} mehr. wie viele {Тмн} hat {он} jetzt? {s}: {n} + {k} = {s}.",
        кому="{X} hatte {n} {Тn}. {Он} gab {Y} {k} {Тk}. wie viele {Тмн} hat {X} jetzt? {r}: {n} − {k} = {r}."),
    "fr": dict(
        осталось="{X} avait {n} {Тn}. {Он} en a donné {k}. combien en a-t-{он} maintenant ? il {ему} en reste {r} : {n} − {k} = {r}.",
        ему="{X} avait {n} {Тn}. {Y} {ему} en a donné {k} de plus. combien de {Тмн} a-t-{он} maintenant ? {s} : {n} + {k} = {s}.",
        если_придут="il y a {n} {Тn} dans la boîte. si on en ajoute {k}, combien y en aura-t-il ? {s} : {n} + {k} = {s}.",
        у_него="{X} avait {n} {Тn}. {Y} {ему} a pris {k} {Тk}. combien de {Тмн} {X} a-t-{он} maintenant ? {r} : {n} − {k} = {r}.",
        товар="{X} a {a} {Г1a} et {b} {Г2b}. combien de {Г3мн} a-t-{он} en tout ? {s} {Г3s} : {a} + {b} = {s}.",
        пришло_скрыто="{X} avait {n} {Тn}. {Он} en a reçu {СК} de plus. maintenant {он} a {s} {Тs}. combien en a-t-{он} reçu de plus ? {k} : {s} − {n} = {k}.",
        ушло_скрыто="{X} avait {n} {Тn}. {Он} en a perdu {СК}. maintenant {он} a {r} {Тr}. combien en a-t-{он} perdu ? {k} : {n} − {r} = {k}.",
        часть_из_них="{X} avait {n} {Тn}. {Он} en a vendu {СКЧ}. maintenant {он} a {r} {Тr}. combien en a-t-{он} vendu ? {k} : {n} − {r} = {k}.",
        взял_скрыто="{X} avait {n} {Тn}. {Y} {ему} en a pris {СК}. maintenant {он} a {r} {Тr}. combien {Y} en a-t-{онY} pris ? {k} : {n} − {r} = {k}.",
        некоторые="{X} avait {n} {Тn}. {Он} en a donné quelques-unes. maintenant il {ему} en reste {r}. combien de {Тмн} a-t-{он} données ? {k} : {n} − {r} = {k}.",
        итог="{X} a {a} {Тмн} {Ц1} et {b} {Тмн} {Ц2}. combien de {Тмн} {X} a-t-{он} {ГОЛОВА} ? {s} {Тs} : {a} + {b} = {s}.",
        из_них="{X} avait {n} {Тn}. {Он} en a donné {k} à {Y}. combien de {Тмн} a-t-{он} maintenant ? {r} : {n} − {k} = {r}.",
        три="{X} a ramassé {n} {Тn}. {X} en a acheté {k} de plus. {он} en a perdu {m}. combien de {Тмн} reste-t-il à {X} ? {t} : {n} + {k} − {m} = {t}.",
        три_шаги="{X} a ramassé {n} {Тn}. {X} en a acheté {k} de plus. {он} en a perdu {m}. combien de {Тмн} reste-t-il à {X} ? étape 1 : {n} + {k} = {s}. étape 2 : {s} − {m} = {t}. total : {t}.",
        владеет="{X} a {n} {Тn}. combien de {Тмн} possède {X} ? {X} possède {n} {Тn}.",
        владеет_после="{X} a {n} {Тn}. {Он} en donne {k}. combien de {Тмн} possède {X} maintenant ? {X} possède {r} {Тr} : {n} − {k} = {r}.",
        доля="{X} a {n} {Тn}. {ДОЛЯ} sont {ЦП}. combien sont {ЦП} ? {r} : {n} ÷ {q} = {r}.",
        доля_не="{X} a {n} {Тn}. {ДОЛЯ} sont {ЦП}. combien ne sont pas {ЦП} ? étape 1 : {n} ÷ {q} = {r}. étape 2 : {n} − {r} = {d}. total : {d}.",
        возраст_имя="{X} a {n} {Гn}. quel âge aura {X} dans {k} {Гk} ? {X} aura {s} {Гs} : {n} + {k} = {s}.",
        его_вещи="{X} a {n} {Тn}. {Р} a {k} {Тk}. combien de {Тмн} a {X} ? {X} a {n} {Тn}.",
        вместе_их="{X} a {n} {Тn}. {Р} a {k} {Тk}. combien de {Тмн} ont-{они} ensemble ? ensemble {они} ont {s} {Тs} : {n} + {k} = {s}.",
        дал_ему="{X} avait {n} {Тn}. {Y} {ему} a donné {k} {Тk}. combien de {Тмн} a {X} maintenant ? {X} a {s} {Тs} : {n} + {k} = {s}.",
        купил_у_него="{X} avait {n} {Тn}. {Y} en avait aussi. {Он} {емуY} a acheté {k} {Тk}. combien de {Тмн} a {X} maintenant ? {X} a {s} {Тs} : {n} + {k} = {s}.",
        оставив_ему="{X} a donné {k} {Тk} à {Y}, ce qui {ему} laisse {r} {Тr}. combien de {Тмн} avait {X} au début ? {X} avait {n} {Тn} : {k} + {r} = {n}.",
        имя_с_с="{Рб} {Xде} a {k} {Тk}. combien de {Тмн} a {Рб} {Xде} ? {Рб} {Xде} a {k} {Тk}.",
        факт="{X} a {n} {Тn}. combien de {Тмн} a {X} ? {n}.",
        без_данных="combien de {Тмн} a {X} ? je ne sais pas : combien de {Тмн} a {X} n'est pas dit.",
        собрал_у="{X} a ramassé {n} {Тn}. {Он} en a perdu {k}. combien de {Тмн} reste-t-il à {X} ? {r} : {n} − {k} = {r}.",
        потерял="{X} avait {n} {Тn}. {Он} en a perdu {k}. combien de {Тмн} lui reste-t-il ? {r} : {n} − {k} = {r}.",
        купил_ещё="{X} avait {n} {Тn}. {Он} en a acheté {k} de plus. combien de {Тмн} a-t-{он} maintenant ? {s} : {n} + {k} = {s}.",
        если="{X} a {n} {Тn}. si {он} en donne {k}, combien lui en restera-t-il ? {r} : {n} − {k} = {r}.",
        время="{В1} {X} avait {n} {Тn}. {В2} {он} en a reçu {k} de plus. combien de {Тмн} a-t-{он} maintenant ? {s} : {n} + {k} = {s}.",
        кому="{X} avait {n} {Тn}. {Он} a donné {k} {Тk} à {Y}. combien de {Тмн} {X} a-t-{он} maintenant ? {r} : {n} − {k} = {r}."),
    "es": dict(
        # ОДНО ГНЕЗДО, ДВА ЗАПОЛНИТЕЛЯ: имя и ударное местоимение стоя́т после «a» на одном
        # месте, и рынок носителя читает его дырой.
        гнездо_датива=(
            "a {X} le quedan {n} {Тn}. {Y} le da {k} más. "
            "¿{кск} le quedan ahora? {s}: {n} + {k} = {s}.",
            "a {он} le quedan {n} {Тn}. {Y} le da {k} más. "
            "¿{кск} le quedan ahora? {s}: {n} + {k} = {s}.",
        ),
        осталось="{X} tenía {n} {Тn}. dio {k}. ¿{кск} tiene ahora? ahora le quedan {r}: {n} − {k} = {r}.",
        ему="{X} tenía {n} {Тn}. {Y} {ему} dio {k} más. ¿{кск} {Тмн} tiene ahora? {s}: {n} + {k} = {s}.",
        если_придут="hay {n} {Тn} en la caja. si se ponen {k} más, ¿{кск} habrá? {s}: {n} + {k} = {s}.",
        у_него="{X} tenía {n} {Тn}. {Y} {ему} quitó {k} {Тk}. ¿{кск} {Тмн} tiene {X} ahora? {r}: {n} − {k} = {r}.",
        товар="{X} tiene {a} {Г1a} y {b} {Г2b}. ¿cuántas {Г3мн} tiene en total? {s} {Г3s}: {a} + {b} = {s}.",
        пришло_скрыто="{X} tenía {n} {Тn}. recibió {СК} {Тмн} más. ahora tiene {s} {Тs}. ¿{кск} {Тмн} recibió? {k}: {s} − {n} = {k}.",
        ушло_скрыто="{X} tenía {n} {Тn}. perdió {СК} {Тмн}. ahora tiene {r} {Тr}. ¿{кск} {Тмн} perdió? {k}: {n} − {r} = {k}.",
        часть_из_них="{X} tenía {n} {Тn}. vendió {СКЧ}. ahora tiene {r} {Тr}. ¿{кск} {Тмн} vendió? {k}: {n} − {r} = {k}.",
        взял_скрыто="{X} tenía {n} {Тn}. {Y} {ему} quitó {СК} {Тмн}. ahora tiene {r} {Тr}. ¿{кск} {Тмн} quitó {Y}? {k}: {n} − {r} = {k}.",
        некоторые="{X} tenía {n} {Тn}. dio {algunas}. ahora le quedan {r} {Тr}. ¿{кск} {Тмн} dio? {k}: {n} − {r} = {k}.",
        итог="{X} tiene {a} {Тмн} {Ц1} y {b} {Тмн} {Ц2}. ¿{кск} {Тмн} tiene {X} {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        из_них="{X} tenía {n} {Тn}. dio {k} de {ellas} a {Y}. ¿{кск} {Тмн} tiene ahora? {r}: {n} − {k} = {r}.",
        три="{X} recogió {n} {Тn}. {X} compró {k} más. {он} perdió {m}. ¿qué cantidad de {Тмн} le queda a {X}? {t}: {n} + {k} − {m} = {t}.",
        три_шаги="{X} recogió {n} {Тn}. {X} compró {k} más. {он} perdió {m}. ¿qué cantidad de {Тмн} le queda a {X}? paso 1: {n} + {k} = {s}. paso 2: {s} − {m} = {t}. total: {t}.",
        владеет="{X} tiene {n} {Тn}. ¿{кск} {Тмн} posee {X}? {X} posee {n} {Тn}.",
        владеет_после="{X} tiene {n} {Тn}. da {k}. ¿{кск} {Тмн} posee {X} ahora? {X} posee {r} {Тr}: {n} − {k} = {r}.",
        доля="{X} tiene {n} {Тn}. {ДОЛЯ} de {ellas} son {ЦП}. ¿{кск} son {ЦП}? {r}: {n} ÷ {q} = {r}.",
        доля_не="{X} tiene {n} {Тn}. {ДОЛЯ} de {ellas} son {ЦП}. ¿{кск} no son {ЦП}? paso 1: {n} ÷ {q} = {r}. paso 2: {n} − {r} = {d}. total: {d}.",
        возраст_имя="{X} tiene {n} {Гn}. ¿cuántos años tendrá {X} dentro de {k} {Гk}? {X} tendrá {s} {Гs}: {n} + {k} = {s}.",
        его_вещи="{X} tiene {n} {Тn}. {Р} tiene {k} {Тk}. ¿{кск} {Тмн} tiene {X}? {X} tiene {n} {Тn}.",
        вместе_их="{X} tiene {n} {Тn}. {Р} tiene {k} {Тk}. ¿{кск} {Тмн} tienen {вместе}? {вместе} tienen {s} {Тs}: {n} + {k} = {s}.",
        дал_ему="{X} tenía {n} {Тn}. {Y} {ему} dio {k} {Тk}. ¿{кск} {Тмн} tiene {X} ahora? {X} tiene {s} {Тs}: {n} + {k} = {s}.",
        купил_у_него="{X} tenía {n} {Тn}. {Y} también tenía. {Он} {емуY} compró {k} {Тk}. ¿{кск} {Тмн} tiene {X} ahora? {X} tiene {s} {Тs}: {n} + {k} = {s}.",
        оставив_ему="{X} dio {k} {Тk} a {Y}, lo que {ему} deja {r} {Тr}. ¿{кск} {Тмн} tenía {X} al principio? {X} tenía {n} {Тn}: {k} + {r} = {n}.",
        имя_с_с="{Рб} {Xде} tiene {k} {Тk}. ¿{кск} {Тмн} tiene {Рб} {Xде}? {Рб} {Xде} tiene {k} {Тk}.",
        факт="{X} tiene {n} {Тn}. ¿{кск} {Тмн} tiene {X}? {n}.",
        без_данных="¿{кск} {Тмн} tiene {X}? no lo sé: no se dice {кск} {Тмн} tiene {X}.",
        собрал_у="{X} recogió {n} {Тn}. perdió {k}. ¿qué cantidad de {Тмн} le queda a {X}? {r}: {n} − {k} = {r}.",
        потерял="{X} tenía {n} {Тn}. perdió {k}. ¿qué cantidad de {Тмн} le queda? {r}: {n} − {k} = {r}.",
        купил_ещё="{X} tenía {n} {Тn}. compró {k} más. ¿qué cantidad de {Тмн} tiene ahora? {s}: {n} + {k} = {s}.",
        если="{X} tiene {n} {Тn}. si da {k}, ¿{кск} le quedarán? {r}: {n} − {k} = {r}.",
        время="{В1} {X} tenía {n} {Тn}. {В2} recibió {k} más. ¿{кск} {Тмн} tiene ahora? {s}: {n} + {k} = {s}.",
        кому="{X} tenía {n} {Тn}. dio {k} {Тk} a {Y}. ¿{кск} {Тмн} tiene {X} ahora? {r}: {n} − {k} = {r}."),
    "it": dict(
        осталось="{X} aveva {n} {Тn}. ne ha {date} {k}. {quante} ne ha adesso? {ему} ne restano {r}: {n} − {k} = {r}.",
        ему="{X} aveva {n} {Тn}. {Y} {ему} ne ha {date} {altre} {k}. {quante} {Тмн} ha adesso? {s}: {n} + {k} = {s}.",
        если_придут="ci sono {n} {Тn} nella scatola. se se ne mettono {altre} {k}, {quante} ce ne saranno? {s}: {n} + {k} = {s}.",
        у_него="{X} aveva {n} {Тn}. {Y} {ему} ha preso {k} {Тk}. {quante} {Тмн} ha {X} adesso? {r}: {n} − {k} = {r}.",
        товар="{X} ha {a} {Г1a} e {b} {Г2b}. quante {Г3мн} ha in tutto? {s} {Г3s}: {a} + {b} = {s}.",
        пришло_скрыто="{X} aveva {n} {Тn}. ha ricevuto {СК} {Тмн} in più. ora ha {s} {Тs}. {quante} {Тмн} ha ricevuto? {k}: {s} − {n} = {k}.",
        ушло_скрыто="{X} aveva {n} {Тn}. ha perso {СК} {Тмн}. ora ha {r} {Тr}. {quante} {Тмн} ha perso? {k}: {n} − {r} = {k}.",
        часть_из_них="{X} aveva {n} {Тn}. ha venduto {СКЧ}. ora ha {r} {Тr}. {quante} {Тмн} ha venduto? {k}: {n} − {r} = {k}.",
        взял_скрыто="{X} aveva {n} {Тn}. {Y} {ему} ha preso {СК} {Тмн}. ora ha {r} {Тr}. {quante} {Тмн} ha preso {Y}? {k}: {n} − {r} = {k}.",
        некоторые="{X} aveva {n} {Тn}. ne ha {date} {alcune}. ora {ему} restano {r} {Тr}. {quante} {Тмн} ha dato? {k}: {n} − {r} = {k}.",
        итог="{X} ha {a} {Тмн} {Ц1} e {b} {Тмн} {Ц2}. {quante} {Тмн} ha {X} {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        из_них="{X} aveva {n} {Тn}. ne ha {date} {k} a {Y}. {quante} {Тмн} ha adesso? {r}: {n} − {k} = {r}.",
        три="{X} ha raccolto {n} {Тn}. {X} ha comprato {altre} {k} {Тk}. {он} ha perso {m} {Тm}. che quantità di {Тмн} resta a {X}? {t}: {n} + {k} − {m} = {t}.",
        три_шаги="{X} ha raccolto {n} {Тn}. {X} ha comprato {altre} {k} {Тk}. {он} ha perso {m} {Тm}. che quantità di {Тмн} resta a {X}? passo 1: {n} + {k} = {s}. passo 2: {s} − {m} = {t}. totale: {t}.",
        владеет="{X} ha {n} {Тn}. {quante} {Тмн} possiede {X}? {X} possiede {n} {Тn}.",
        владеет_после="{X} ha {n} {Тn}. ne dà {k}. {quante} {Тмн} possiede {X} adesso? {X} possiede {r} {Тr}: {n} − {k} = {r}.",
        доля="{X} ha {n} {Тn}. {ДОЛЯ} sono {ЦП}. {quante} sono {ЦП}? {r}: {n} ÷ {q} = {r}.",
        доля_не="{X} ha {n} {Тn}. {ДОЛЯ} sono {ЦП}. {quante} non sono {ЦП}? passo 1: {n} ÷ {q} = {r}. passo 2: {n} − {r} = {d}. totale: {d}.",
        возраст_имя="{X} ha {n} {Гn}. quanti anni avrà {X} tra {k} {Гk}? {X} avrà {s} {Гs}: {n} + {k} = {s}.",
        его_вещи="{X} ha {n} {Тn}. {Р} ha {k} {Тk}. {quante} {Тмн} ha {X}? {X} ha {n} {Тn}.",
        вместе_их="{X} ha {n} {Тn}. {Р} ha {k} {Тk}. {quante} {Тмн} hanno insieme? insieme hanno {s} {Тs}: {n} + {k} = {s}.",
        дал_ему="{X} aveva {n} {Тn}. {Y} {ему} ha dato {k} {Тk}. {quante} {Тмн} ha {X} adesso? {X} ha {s} {Тs}: {n} + {k} = {s}.",
        купил_у_него="{X} aveva {n} {Тn}. anche {Y} ne aveva. {Он} {емуY} ha comprato {k} {Тk}. {quante} {Тмн} ha {X} adesso? {X} ha {s} {Тs}: {n} + {k} = {s}.",
        оставив_ему="{X} ha dato {k} {Тk} a {Y}, il che {ему} lascia {r} {Тr}. {quante} {Тмн} aveva {X} all'inizio? {X} aveva {n} {Тn}: {k} + {r} = {n}.",
        имя_с_с="{Рб} {Xде} ha {k} {Тk}. {quante} {Тмн} ha {Рб} {Xде}? {Рб} {Xде} ha {k} {Тk}.",
        факт="{X} ha {n} {Тn}. {quante} {Тмн} ha {X}? {n}.",
        без_данных="{quante} {Тмн} ha {X}? non lo so: non è detto {quante} {Тмн} ha {X}.",
        собрал_у="{X} ha raccolto {n} {Тn}. ha perso {k} {Тk}. che quantità di {Тмн} resta a {X}? {r}: {n} − {k} = {r}.",
        потерял="{X} aveva {n} {Тn}. ha perso {k} {Тk}. che quantità di {Тмн} ha ancora? {r}: {n} − {k} = {r}.",
        купил_ещё="{X} aveva {n} {Тn}. ha comprato altre {k} {Тk}. che quantità di {Тмн} ha adesso? {s}: {n} + {k} = {s}.",
        если="{X} ha {n} {Тn}. se ne dà {k}, {quante} ne avrà? {r}: {n} − {k} = {r}.",
        время="{В1} {X} aveva {n} {Тn}. {В2} ne ha {ricevute} {altre} {k}. {quante} {Тмн} ha adesso? {s}: {n} + {k} = {s}.",
        кому="{X} aveva {n} {Тn}. ha dato {k} {Тk} a {Y}. {quante} {Тмн} ha {X} adesso? {r}: {n} − {k} = {r}."),
    "pt": dict(
        осталось="{X} tinha {n} {Тn}. deu {k}. {quantas} tem agora? agora tem {r}: {n} − {k} = {r}.",
        ему="{X} tinha {n} {Тn}. {Y} deu-{ему} mais {k}. {quantas} {Тмн} tem agora? {s}: {n} + {k} = {s}.",
        если_придут="há {n} {Тn} na caixa. se puserem mais {k}, {quantas} haverá? {s}: {n} + {k} = {s}.",
        у_него="{X} tinha {n} {Тn}. {Y} tirou-{ему} {k} {Тk}. {quantas} {Тмн} tem {X} agora? {r}: {n} − {k} = {r}.",
        товар="{X} tem {a} {Г1a} e {b} {Г2b}. quantas {Г3мн} tem no total? {s} {Г3s}: {a} + {b} = {s}.",
        пришло_скрыто="{X} tinha {n} {Тn}. recebeu mais {СК} {Тмн}. agora tem {s} {Тs}. {quantas} {Тмн} recebeu? {k}: {s} − {n} = {k}.",
        ушло_скрыто="{X} tinha {n} {Тn}. perdeu {СК} {Тмн}. agora tem {r} {Тr}. {quantas} {Тмн} perdeu? {k}: {n} − {r} = {k}.",
        часть_из_них="{X} tinha {n} {Тn}. vendeu {СКЧ}. agora tem {r} {Тr}. {quantas} {Тмн} vendeu? {k}: {n} − {r} = {k}.",
        взял_скрыто="{X} tinha {n} {Тn}. {Y} tirou-{ему} {СК} {Тмн}. agora tem {r} {Тr}. {quantas} {Тмн} tirou {Y}? {k}: {n} − {r} = {k}.",
        некоторые="{X} tinha {n} {Тn}. deu {algumas}. agora tem {r} {Тr}. {quantas} {Тмн} deu? {k}: {n} − {r} = {k}.",
        итог="{X} tem {a} {Тмн} {Ц1} e {b} {Тмн} {Ц2}. {quantas} {Тмн} tem {X} {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        из_них="{X} tinha {n} {Тn}. deu {k} {delas} {Yд}. {quantas} {Тмн} tem agora? {r}: {n} − {k} = {r}.",
        три="{X} apanhou {n} {Тn}. {X} comprou mais {k}. {он} perdeu {m}. que quantidade de {Тмн} resta {Xд}? {t}: {n} + {k} − {m} = {t}.",
        три_шаги="{X} apanhou {n} {Тn}. {X} comprou mais {k}. {он} perdeu {m}. que quantidade de {Тмн} resta {Xд}? passo 1: {n} + {k} = {s}. passo 2: {s} − {m} = {t}. total: {t}.",
        владеет="{X} tem {n} {Тn}. {quantas} {Тмн} possui {X}? {X} possui {n} {Тn}.",
        владеет_после="{X} tem {n} {Тn}. dá {k}. {quantas} {Тмн} possui {X} agora? {X} possui {r} {Тr}: {n} − {k} = {r}.",
        доля="{X} tem {n} {Тn}. {ДОЛЯ} são {ЦП}. {quantas} são {ЦП}? {r}: {n} ÷ {q} = {r}.",
        доля_не="{X} tem {n} {Тn}. {ДОЛЯ} são {ЦП}. {quantas} não são {ЦП}? passo 1: {n} ÷ {q} = {r}. passo 2: {n} − {r} = {d}. total: {d}.",
        возраст_имя="{X} tem {n} {Гn}. quantos anos terá {X} daqui a {k} {Гk}? {X} terá {s} {Гs}: {n} + {k} = {s}.",
        его_вещи="{X} tem {n} {Тn}. {Р} tem {k} {Тk}. {quantas} {Тмн} tem {X}? {X} tem {n} {Тn}.",
        вместе_их="{X} tem {n} {Тn}. {Р} tem {k} {Тk}. {quantas} {Тмн} têm {вместе}? {вместе} têm {s} {Тs}: {n} + {k} = {s}.",
        дал_ему="{X} tinha {n} {Тn}. {Y} deu-{ему} {k} {Тk}. {quantas} {Тмн} tem {X} agora? {X} tem {s} {Тs}: {n} + {k} = {s}.",
        купил_у_него="{X} tinha {n} {Тn}. {Y} também tinha. {Он} comprou-{емуY} {k} {Тk}. {quantas} {Тмн} tem {X} agora? {X} tem {s} {Тs}: {n} + {k} = {s}.",
        оставив_ему="{X} deu {k} {Тk} {Yд}, o que {ему} deixa {r} {Тr}. {quantas} {Тмн} tinha {X} no início? {X} tinha {n} {Тn}: {k} + {r} = {n}.",
        имя_с_с="{Рб} {Xде} tem {k} {Тk}. {quantas} {Тмн} tem {Рб} {Xде}? {Рб} {Xде} tem {k} {Тk}.",
        факт="{X} tem {n} {Тn}. {quantas} {Тмн} tem {X}? {n}.",
        без_данных="{quantas} {Тмн} tem {X}? não sei: não é dito {quantas} {Тмн} tem {X}.",
        собрал_у="{X} apanhou {n} {Тn}. perdeu {k}. que quantidade de {Тмн} resta {Xд}? {r}: {n} − {k} = {r}.",
        потерял="{X} tinha {n} {Тn}. perdeu {k}. que quantidade de {Тмн} lhe resta? {r}: {n} − {k} = {r}.",
        купил_ещё="{X} tinha {n} {Тn}. comprou mais {k}. que quantidade de {Тмн} tem agora? {s}: {n} + {k} = {s}.",
        если=("{X} tem {n} {Тn}. se der {k}, com {quantas} ficará? {r}: {n} − {k} = {r}.",
              "{X} tem {n} {Тn}. se der {k}, {quantas} lhe restarão? {r}: {n} − {k} = {r}."),
        время="{В1} {X} tinha {n} {Тn}. {В2} recebeu mais {k}. {quantas} {Тмн} tem agora? {s}: {n} + {k} = {s}.",
        кому="{X} tinha {n} {Тn}. deu {k} {Тk} {Yд}. {quantas} {Тмн} tem {X} agora? {r}: {n} − {k} = {r}."),
    "nl": dict(
        осталось="{X} had {n} {Тn}. {он} gaf er {k} weg. hoeveel heeft {он} nu? {он} heeft er nu nog {r}: {n} − {k} = {r}.",
        ему="{X} had {n} {Тn}. {Y} gaf {ему} er {k} bij. hoeveel {Тмн} heeft {он} nu? {s}: {n} + {k} = {s}.",
        если_придут="er zitten {n} {Тn} in de doos. als er {k} bij worden gedaan, hoeveel zijn het er dan? {s}: {n} + {k} = {s}.",
        у_него="{X} had {n} {Тn}. {Y} nam {k} {Тk} van {него} af. hoeveel {Тмн} heeft {X} nu? {r}: {n} − {k} = {r}.",
        товар="{X} heeft {a} {Г1a} en {b} {Г2b}. hoeveel {Г3мн} heeft {он} in totaal? {s} {Г3s}: {a} + {b} = {s}.",
        пришло_скрыто="{X} had {n} {Тn}. {он} kreeg er {СК} bij. nu heeft {он} {s} {Тs}. hoeveel {Тмн} kreeg {он} erbij? {k}: {s} − {n} = {k}.",
        ушло_скрыто="{X} had {n} {Тn}. {он} verloor er {СК}. nu heeft {он} {r} {Тr}. hoeveel {Тмн} verloor {он}? {k}: {n} − {r} = {k}.",
        часть_из_них="{X} had {n} {Тn}. {он} verkocht {СКЧ}. nu heeft {он} {r} {Тr}. hoeveel {Тмн} verkocht {он}? {k}: {n} − {r} = {k}.",
        взял_скрыто="{X} had {n} {Тn}. {Y} nam er {СК} van {него}. nu heeft {он} {r} {Тr}. hoeveel {Тмн} nam {Y}? {k}: {n} − {r} = {k}.",
        некоторые="{X} had {n} {Тn}. {он} gaf er een paar weg. nu heeft {он} er nog {r}. hoeveel {Тмн} gaf {он} weg? {k}: {n} − {r} = {k}.",
        итог="{X} heeft {a} {Ц1} {Тмн} en {b} {Ц2} {Тмн}. hoeveel {Тмн} heeft {X} {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        из_них="{X} had {n} {Тn}. {он} gaf er {k} aan {Y}. hoeveel {Тмн} heeft {он} nu? {r}: {n} − {k} = {r}.",
        три="{X} verzamelde {n} {Тn}. {X} kocht er nog {k} bij. {он} verloor er {m}. hoeveel {Тмн} heeft {X} nog? {t}: {n} + {k} − {m} = {t}.",
        три_шаги="{X} verzamelde {n} {Тn}. {X} kocht er nog {k} bij. {он} verloor er {m}. hoeveel {Тмн} heeft {X} nog? stap 1: {n} + {k} = {s}. stap 2: {s} − {m} = {t}. totaal: {t}.",
        владеет="{X} heeft {n} {Тn}. hoeveel {Тмн} bezit {X}? {X} bezit {n} {Тn}.",
        владеет_после="{X} heeft {n} {Тn}. {он} geeft er {k} weg. hoeveel {Тмн} bezit {X} nu? {X} bezit {r} {Тr}: {n} − {k} = {r}.",
        доля="{X} heeft {n} {Тn}. {ДОЛЯ} daarvan is {ЦП}. hoeveel daarvan zijn {ЦП}? {r}: {n} ÷ {q} = {r}.",
        доля_не="{X} heeft {n} {Тn}. {ДОЛЯ} daarvan is {ЦП}. hoeveel daarvan zijn niet {ЦП}? stap 1: {n} ÷ {q} = {r}. stap 2: {n} − {r} = {d}. totaal: {d}.",
        возраст_имя="{X} is {n} {Гn} oud. hoe oud is {X} over {k} {Гk}? {X} is dan {s} {Гs} oud: {n} + {k} = {s}.",
        его_вещи="{X} heeft {n} {Тn}. {Р} heeft {k} {Тk}. hoeveel {Тмн} heeft {X}? {X} heeft {n} {Тn}.",
        вместе_их="{X} heeft {n} {Тn}. {Р} heeft {k} {Тk}. hoeveel {Тмн} hebben {они} samen? samen hebben {они} {s} {Тs}: {n} + {k} = {s}.",
        дал_ему="{X} had {n} {Тn}. {Y} gaf {ему} {k} {Тk}. hoeveel {Тмн} heeft {X} nu? {X} heeft {s} {Тs}: {n} + {k} = {s}.",
        купил_у_него="{X} had {n} {Тn}. {Y} had er ook. {Он} kocht {k} {Тk} van {негоY}. hoeveel {Тмн} heeft {X} nu? {X} heeft {s} {Тs}: {n} + {k} = {s}.",
        оставив_ему="{X} gaf {k} {Тk} aan {Y}, waardoor {ему} {r} {Тr} overbleven. hoeveel {Тмн} had {X} eerst? {X} had {n} {Тn}: {k} + {r} = {n}.",
        имя_с_с="{Рб} {Xде} heeft {k} {Тk}. hoeveel {Тмн} heeft {Рб} {Xде}? {Рб} {Xде} heeft {k} {Тk}.",
        факт="{X} heeft {n} {Тn}. hoeveel {Тмн} heeft {X}? {n}.",
        без_данных="hoeveel {Тмн} heeft {X}? ik weet het niet: hoeveel {Тмн} {X} heeft, is niet gezegd.",
        собрал_у="{X} verzamelde {n} {Тn}. {он} verloor er {k}. hoeveel {Тмн} heeft {X} nog? {r}: {n} − {k} = {r}.",
        потерял="{X} had {n} {Тn}. {он} verloor er {k}. hoeveel {Тмн} heeft {он} nog? {r}: {n} − {k} = {r}.",
        купил_ещё="{X} had {n} {Тn}. {он} kocht er nog {k} bij. hoeveel {Тмн} heeft {он} nu? {s}: {n} + {k} = {s}.",
        если="{X} heeft {n} {Тn}. als {он} er {k} weggeeft, hoeveel heeft {он} dan? {r}: {n} − {k} = {r}.",
        время="{В1} had {X} {n} {Тn}. {В2} kreeg {он} er {k} bij. hoeveel {Тмн} heeft {он} nu? {s}: {n} + {k} = {s}.",
        кому="{X} had {n} {Тn}. {он} gaf {k} {Тk} aan {Y}. hoeveel {Тмн} heeft {X} nu? {r}: {n} − {k} = {r}."),
    "pl": dict(
        осталось="{X} miał{а} {n} {Тn}. oddał{а} {k}. ile ma teraz? teraz zostało {ему} {r}: {n} − {k} = {r}.",
        ему="{X} miał{а} {n} {Тn}. {Y} dał{аY} {ему} jeszcze {k}. ile {Тмн} ma teraz? {s}: {n} + {k} = {s}.",
        если_придут="w pudełku {ЕСТЬn} {n} {Тn}. jeśli włożyć jeszcze {k}, ile będzie? {s}: {n} + {k} = {s}.",
        у_него="{X} miał{а} {n} {Тn}. {Y} zabrał{аY} {ему} {k} {Тk}. ile {Тмн} ma {X} teraz? {r}: {n} − {k} = {r}.",
        товар="{X} ma {a} {Г1a} i {b} {Г2b}. ile {Г3мн} ma razem? {s} {Г3s}: {a} + {b} = {s}.",
        пришло_скрыто="{X} miał{а} {n} {Тn}. dostał{а} jeszcze {СК} {Тмн}. teraz ma {s} {Тs}. ile {Тмн} dostał{а}? {k}: {s} − {n} = {k}.",
        ушло_скрыто="{X} miał{а} {n} {Тn}. zgubił{а} {СК} {Тмн}. teraz ma {r} {Тr}. ile {Тмн} zgubił{а}? {k}: {n} − {r} = {k}.",
        часть_из_них="{X} miał{а} {n} {Тn}. sprzedał{а} {СКЧ}. teraz ma {r} {Тr}. ile {Тмн} sprzedał{а}? {k}: {n} − {r} = {k}.",
        взял_скрыто="{X} miał{а} {n} {Тn}. {Y} zabrał{аY} {ему} {СК} {Тмн}. teraz ma {r} {Тr}. ile {Тмн} zabrał{аY} {Y}? {k}: {n} − {r} = {k}.",
        некоторые="{X} miał{а} {n} {Тn}. oddał{а} kilka. teraz ma {r} {Тr}. ile {Тмн} oddał{а}? {k}: {n} − {r} = {k}.",
        итог="{X} ma {a} {Ц1} {Тмн} i {b} {Ц2} {Тмн}. ile {Тмн} ma {X} {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        из_них="{X} miał{а} {n} {Тn}. oddał{а} {k} z nich {Yд}. ile {Тмн} ma teraz? {r}: {n} − {k} = {r}.",
        три="{X} zebrał{а} {n} {Тn}. {X} kupił{а} jeszcze {k}. {он} zgubił{а} {m} z nich. ile {Тмн} zostało {Xд}? {t}: {n} + {k} − {m} = {t}.",
        три_шаги="{X} zebrał{а} {n} {Тn}. {X} kupił{а} jeszcze {k}. {он} zgubił{а} {m} z nich. ile {Тмн} zostało {Xд}? krok 1: {n} + {k} = {s}. krok 2: {s} − {m} = {t}. razem: {t}.",
        владеет="{X} ma {n} {Тn}. ile {Тмн} posiada {X}? {X} posiada {n} {Тn}.",
        владеет_после="{X} ma {n} {Тn}. oddaje {k}. ile {Тмн} posiada {X} teraz? {X} posiada {r} {Тr}: {n} − {k} = {r}.",
        доля="{X} ma {n} {Тn}. {ДОЛЯ} z nich to {ЦП}. ile z nich to {ЦП}? {r}: {n} ÷ {q} = {r}.",
        доля_не="{X} ma {n} {Тn}. {ДОЛЯ} z nich to {ЦП}. ile z nich to nie {ЦП}? krok 1: {n} ÷ {q} = {r}. krok 2: {n} − {r} = {d}. razem: {d}.",
        возраст_имя="{X} ma {n} {Гn}. ile lat będzie mieć {X} za {k} {Гk}? {X} będzie mieć {s} {Гs}: {n} + {k} = {s}.",
        его_вещи="{X} ma {n} {Тn}. {Р} ma {k} {Тk}. ile {Тмн} ma {X}? {X} ma {n} {Тn}.",
        вместе_их="{X} ma {n} {Тn}. {Р} ma {k} {Тk}. ile {Тмн} mają razem? razem mają {s} {Тs}: {n} + {k} = {s}.",
        дал_ему="{X} miał{а} {n} {Тn}. {Y} dał{аY} {ему} {k} {Тk}. ile {Тмн} ma {X} teraz? {X} ma {s} {Тs}: {n} + {k} = {s}.",
        купил_у_него="{X} miał{а} {n} {Тn}. {Y} też miał{аY}. {Он} kupił{а} od {негоY} {k} {Тk}. ile {Тмн} ma {X} teraz? {X} ma {s} {Тs}: {n} + {k} = {s}.",
        оставив_ему="{X} dał{а} {Yд} {k} {Тk}, co zostawiło {ему} {r} {Тr}. ile {Тмн} miał{а} {X} na początku? {X} miał{а} {n} {Тn}: {k} + {r} = {n}.",
        имя_с_с="{Рб} {Xде} ma {k} {Тk}. ile {Тмн} ma {Рб} {Xде}? {Рб} {Xде} ma {k} {Тk}.",
        факт="{X} ma {n} {Тn}. ile {Тмн} ma {X}? {n}.",
        без_данных="ile {Тмн} ma {X}? nie wiem: nie powiedziano, ile {Тмн} ma {X}.",
        собрал_у="{X} zebrał{а} {n} {Тn}. zgubił{а} {k} z nich. ile {Тмн} zostało {Xд}? {r}: {n} − {k} = {r}.",
        потерял="{X} miał{а} {n} {Тn}. zgubił{а} {k} z nich. ile {Тмн} {ему} zostało? {r}: {n} − {k} = {r}.",
        купил_ещё="{X} miał{а} {n} {Тn}. kupił{а} jeszcze {k}. ile {Тмн} ma teraz? {s}: {n} + {k} = {s}.",
        если="{X} ma {n} {Тn}. jeśli odda {k}, ile {ему} zostanie? {r}: {n} − {k} = {r}.",
        время="{В1} {X} miał{а} {n} {Тn}. {В2} dostał{а} jeszcze {k}. ile {Тмн} ma teraz? {s}: {n} + {k} = {s}.",
        кому="{X} miał{а} {n} {Тn}. oddał{а} {k} {Тk} {Yд}. ile {Тмн} ma {X} teraz? {r}: {n} − {k} = {r}."),
})
ФОРМЫ = ("гнездо_датива", "некоторые", "итог", "итог_всего", "осталось", "из_них", "ему", "если", "если_придут", "время", "кому", "у_него", "единица", "товар", "потерял", "купил_ещё", "собрал_у", "три", "три_шаги", "факт", "без_данных", "пришло_скрыто", "ушло_скрыто", "часть_из_них", "взял_скрыто", "владеет", "владеет2", "владеет_после", "держит", "хранит", "доля", "доля_не", "возраст_имя", "его_вещи", "вместе_их", "дал_ему", "купил_у_него", "оставив_ему", "имя_с_с")
# the unit before the number is an English shape of the band; Russian writes «3 ₽» after — declared gap
ОБЪЯВЛЕННЫЕ_ПРОПУСКИ = {
                       # ГНЕЗДО ДАТИВА — ИСПАНСКОЕ, И ЭТО НЕ ЛЕНЬ, А ГРАММАТИКА (08.09).
                       #
                       # Рынок носителя покупает дыру там, где на одном месте стоя́т и имя, и
                       # местоимение. По-испански такое место есть: «a Ana le quedan 5» рядом
                       # с «a ella le quedan 5» — после предлога «a» стои́т либо имя, либо
                       # УДАРНОЕ местоимение, клитика «le» остаётся при обоих.
                       #
                       #     УДВОЕНИЕ КЛИТИКИ НЕ ДАЁТ ОБЩЕГО МЕСТА: там имя ДОБАВЛЯЕТСЯ к
                       #     клитике, а не встаёт на её место. Общее место даёт УДАРНОЕ
                       #     местоимение, и потому дом берёт его, а не клитику.
                       #
                       # Итальянское то же без клитики («a lei restano 5» / «a Marta restano
                       # 5») — форма верна, но её партитив («gliene dà») стои́т проверки живым
                       # глазом, и я не пишу того, чего не проверил. Португальское отложено с
                       # названной причиной: с именами там «à Marta» в европейской норме и «a
                       # Marta» в бразильской, а pt-свод писан европейским.
                       "гнездо_датива": frozenset({"ru", "en", "de", "fr", "it", "pt",
                                                   "nl", "pl"}),
                       "единица": frozenset({"ru"}),
                       # «possess» — второй английский глагол владения; у других языков один
                       "владеет2": frozenset({"ru", "de", "fr", "es", "it", "pt", "nl", "pl"}),
                       # hold / keep — английские глаголы держания (holon: own/hold/keep становятся
                       # держащими голосом страниц — ответ полным предложением с леджером ±)
                       "держит": frozenset({"ru", "de", "fr", "es", "it", "pt", "nl", "pl"}),
                       "хранит": frozenset({"ru", "de", "fr", "es", "it", "pt", "nl", "pl"})}
# TWO HOLDERS, ONE BEARER ASKED: the answer repeats the FIRST holder's number, not the parent's
ОТВЕТ_ПЕРВОГО = frozenset({"его_вещи"})
ЧИСЛА = ((12, 5), (20, 8), (15, 6), (9, 4), (30, 12), (25, 7), (18, 11), (40, 15))
# СВОЙ РЯД ЧИСЕЛ У РОДА ДОЛИ (08.09). Прибор «ключ без опоры» назвал четырнадцать родов вопросов,
# держащихся менее чем на LAW³ = 8 страницах, и одиннадцать из них — вопросы ДОЛИ на романских
# языках: «cuántos son», «quanti sono», «quantos são». Причина в числах: доля показывается лишь
# там, где она ДЕЛИТ, и из восьми пар общего ряда делятся немногие — тринадцать страниц доли на
# язык, а их надо разделить ещё надвое по роду вещи и надвое по полярности.
#
#     РОД, ЧЬЯ СТРАНИЦА РОЖДАЕТСЯ НЕ ОТ ВСЯКОГО ЧИСЛА, ДОЛЖЕН ИМЕТЬ СВОЙ РЯД ЧИСЕЛ. Общий ряд
#     писан для сложения и разности, где делится всё; доле он даёт остатки, а не страницы.
#
# Ряд доли собран из чисел, делящихся на два, три и четыре разом или порознь, — и оттого каждая
# пара даёт страницу, а не отбрасывается.
# РЯД ДОЛИ ДОВЕДЁН ДО ПОЛНОГО ОБОРОТА ВЕЩЕЙ (08.09, вечер). Двенадцать пар при восьми вещах
# давали неполный оборот: первые четыре вещи выходили дважды, остальные по разу, — и роды
# вопросов, чьё слово зависит от РОДА вещи («quantos» при мужском, «quantas» при женском),
# делились неровно. Шестнадцать пар суть ровно два оборота: всякая вещь выходит дважды.
ЧИСЛА_ДОЛИ = ((12, 5), (24, 7), (36, 9), (48, 11), (60, 13), (16, 6),
              (18, 8), (20, 9), (28, 5), (30, 7), (32, 11), (40, 13),
              (44, 6), (52, 8), (54, 10), (56, 12))
ЦЕНЫ = ((3, 4), (2, 5), (6, 3), (5, 5))
_ДАТ = None


def _дательный(имя):
    global _ДАТ
    if _ДАТ is None:
        п = json.loads((_ПАКЕТЫ / "ru.json").read_text(encoding="utf-8"))
        _ДАТ = {и: ф.get("dat") for и, ф in (п.get("person_forms") or {}).items()}
    return _ДАТ.get(имя)


def _лицо(язык, i):
    л = A.ЛИЦА[язык][i % len(A.ЛИЦА[язык])]
    if язык == "pt":
        # EUROPEAN PORTUGUESE puts the article before a name: «a Ana», «o Luís»; the dative
        # contracts it: «à Ana», «ao Luís» — the article is the gender's, declared here
        арт = "a " if л[1] == "f" else "o "
        return (арт + л[0], л[1], л[2])
    return л


def _дательный_pt(лицо):
    return ("à " if лицо[1] == "f" else "ao ") + лицо[0].split(" ", 1)[1]


def _имя_чьё(язык, X):
    """THE NAME'S POSSESSIVE — one surface per language: en «Ann's», ru the genitive, de/nl «von/van»,
    es «de», it «di», fr «de» with the elision before a vowel («d'Anne», «d'Hugo»), pt the article
    contracted («do João», «da Ana»), pl the genitive declared by the house."""
    имя = X[0]
    if язык == "en": return имя + "'s"
    if язык == "ru": return X[2]
    if язык == "de": return "von " + имя
    if язык == "nl": return "van " + имя
    if язык == "es": return "de " + имя
    if язык == "it": return "di " + имя
    if язык == "fr": return ("d'" if имя[0] in "AEIOUHÉÈaeiouhéè" else "de ") + имя
    if язык == "pt": return "d" + имя
    return РОДИТЕЛЬНЫЙ_PL.get(имя, имя)


def _поля(язык, i, j, Т, n, k, форма):
    X, Y = _лицо(язык, i), _лицо(язык, j)
    if Y[0] == X[0]:
        Y = _лицо(язык, j + 1)
    м = МЕСТОИМЕНИЯ[язык][X[1]]
    вещь = lambda c: A._вещь(язык, Т, c)
    Yд = (_дательный(Y[0]) if язык == "ru" else ДАТЕЛЬНЫЙ_PL.get(Y[0], Y[0]) if язык == "pl"
          else _дательный_pt(Y) if язык == "pt" else Y[0])
    Xд = (_дательный(X[0]) if язык == "ru" else ДАТЕЛЬНЫЙ_PL.get(X[0], X[0]) if язык == "pl"
          else _дательный_pt(X) if язык == "pt" else X[0])
    п = dict(X=X[0], Xр=X[2], Y=Y[0], Yд=Yд, Xд=Xд,
             он=м["он"], Он=м["он"], него=м["него"], ему=м["ему"],
             а=(("a" if X[1] == "f" else "") if язык == "pl" else A._а(язык, X[1])), аY=(("a" if Y[1] == "f" else "") if язык == "pl" else A._а(язык, Y[1])),
             # ЦЕЛАЯ ФОРМА, А НЕ ОСНОВА С СУФФИКСОМ: «нашёл» + «а» даёт «нашёла» — слова,
             # которого в русском нет. Дыра суффикса верна для тринадцати основ дома и лжёт
             # о четырнадцатой, и потому глагол с БЕГЛОЙ ГЛАСНОЙ берётся у дома языка целиком
             # (`rugram.прошедшее`), а не собирается здесь.
             НАШЁЛ=(_RU.прошедшее("нашёл", X[1]) if язык == "ru" else ""),
             n=n, k=k, r=n - k, s=n + k, a=n, b=k, m=(k + 1) // 2, t=n + k - (k + 1) // 2,
             Тn=вещь(n), Тk=вещь(k), Тr=вещь(n - k), Тs=вещь(n + k), Тмн=вещь(5), Т1=вещь(1), Тm=вещь((k + 1) // 2))
    # THE YEAR BENDS BY THE COUNT — the numberline house declares its forms (one table, two houses);
    # after the preposition the oblique form where the language bends it («in 5 Jahren»)
    import numberline as _NL
    п.update(Гn=_NL.год(язык, n), Гk=_NL.год(язык, k, после=True), Гs=_NL.год(язык, n + k))
    # СВЯЗКА ГНЁТСЯ ПОЛОСОЙ СЧЁТА, А НЕ СТОИТ БУКВОЙ (08.09). Рамка коробки писала «w pudełku
    # jest {n}» при всяком числе, и правота её держалась ЖРЕБИЕМ: восемь чисел этой формы —
    # 9, 12, 15, 18, 20, 25, 30, 40 — все легли в родительный множественный, где «jest» верно.
    # Первое же число от двух до четырёх дало бы ложь: по-польски там стои́т «są».
    #
    #     ПРАВОТА, ДЕРЖАЩАЯСЯ ВЫБОРОМ ЧИСЕЛ, А НЕ ЗАКОНОМ, ЕСТЬ ДОЛГ, ЕЩЁ НЕ ПРЕДЪЯВЛЕННЫЙ.
    if язык == "pl":
        п["ЕСТЬn"] = _PL.связка("наст", n)
    род = РОД_ВЕЩЕЙ.get(язык, {}).get(вещь(5), "f")
    for дыра, (м_, ж_) in РОДОВЫЕ.get(язык, {}).items():
        п[дыра] = м_ if род == "m" else ж_
    п["_род"] = род
    # СЛОВО СКРЫТОГО КОЛИЧЕСТВА СТОИТ ТАМ, ГДЕ СТОЯЛО БЫ ЧИСЛО, и гнётся родом вещи там, где язык
    # его гнёт (es/it/pt): пара (мужской, женский) выбирается тем же родом, что и вопросное слово.
    ск = СКРЫТОЕ[язык]
    п["СК"] = ск["несколько"][0 if род == "m" else 1] if isinstance(ск["несколько"], tuple) else ск["несколько"]
    п["СКЧ"] = ск["часть"][0 if род == "m" else 1] if isinstance(ск["часть"], tuple) else ск["часть"]
    # THE OTHER PERSON'S PRONOUNS (Y), the parent and the pair by X's gender, the name's possessive
    мY = МЕСТОИМЕНИЯ[язык][Y[1]]
    п.update(Yр=Y[2], онY=мY["он"], негоY=мY["него"], емуY=мY["ему"], Xде=_имя_чьё(язык, X))
    п.update(РОДНЯ[язык][X[1]])
    return п


_МЕСТОИМЕНИЕ_В_НАЧАЛЕ = re.compile(r"(?<=\. )\{[Оо]н\}")


def близнец(рамка):
    """THE NAME IN THE PRONOUN'S PLACE (holon, sweep of the sixth point: the substitution
    market buys «she/he/they» and no other language's pronoun — because the canon shows the
    pronoun without the same frame worn by the name). A frame whose second sentence opens with
    the pronoun gets a twin whose second sentence opens with the name; None if there is none."""
    двойник = _МЕСТОИМЕНИЕ_В_НАЧАЛЕ.sub("{X}", рамка)
    return двойник if двойник != рамка else None


# КАРТА ПАДЕЖЕЙ ДЫРЫ НОСИТЕЛЯ (07.09, вечер; заказ holon, волна X, М-734).
#
# Рынок местоимений покупает слово, стоящее в ДЫРЕ НОСИТЕЛЯ купленной рамки, а дыра
# образуется лишь там, где на одном месте предложения на разных страницах стоя́т и имя, и
# местоимение. Перепись мест по девяти языкам дала:
#
#     ru 6 общих мест · en 5 · de 4 · nl 3 · fr 2 · pl 1 · es 0 · it 0 · pt 0
#     при 5–24 местах, где местоимение стои́т ВСЕГДА ОДНО
#
#     ГДЕ МЕСТОИМЕНИЕ СТОИ́Т ВСЕГДА ОДНО, ТАМ НЕТ ДЫРЫ, А ЕСТЬ ЗАСТЫВШАЯ ФРАЗА. Читатель
#     выучит её целиком и не узнает, что на её месте может стоять имя.
#
# `близнец` ставит имя на место местоимения лишь В НАЧАЛЕ предложения; все прочие гнёзда —
# середина («у {него}», «ещё {он}»), и их он не видит.
#
# ЗАМЕНЯТЬ НАДО ОДНО ГНЕЗДО, А НЕ ВСЕ. Первый замысел менял все местоимения разом — и убивал
# ровно то, ради чего делается: страницу, где имя стои́т в начале, а местоимение в середине,
# то есть единственное нынешнее общее место. Потому близнец середины СОХРАНЯЕТ местоимение
# начала и даёт имя только срединным гнёздам; вместе три поверхности покрывают каждое гнездо
# обоими заполнителями.
#
# Падеж имени не выводится из падежа местоимения — он ОБЪЯВЛЕН здесь.
ПАДЕЖ_НОСИТЕЛЯ = {"он": "X", "Он": "X", "него": "Xр", "ему": "Xд",
                  "онY": "Y", "негоY": "Yр", "емуY": "Yд"}
_ДЫРА = re.compile(r"\{([^}]+)\}")

# НЕ ВСЯКОЕ МЕСТОИМЕНИЕ ЗАМЕНИМО ИМЕНЕМ, И ЭТО КУПЛЕНО ГЛАЗОМ, А НЕ ПРИБОРОМ (07.09, вечер).
#
# Первая правка ставила имя в срединные гнёзда ВСЕХ девяти языков. Прибор бы её пропустил:
# суды дома читают счёт и леджер, а не синтаксис клитики. Глаз, прочитавший образцы, нашёл
# четыре языка, где подстановка даёт НЕ РЕЧЬ:
#
#     es «{Y} le dio {k} más»   → «{Y} Ana dio»       — клитика не заменяется именем;
#                                  правильно «Marta le dio … a Ana» (удвоение клитики)
#     pt «deu-lhe mais {k}»     → «deu-Ana mais»      — энклитика тем более
#     it «{Y} gli ha dato»      → «{Y} Ana ha dato»   — то же
#     fr «combien en a-t-il ?»  → «combien en a-t-Marie ?» — инверсия требует местоимения;
#                                  правильно «combien Marie en a-t-elle ?»
#
#     КЛИТИКА И ИНВЕРТИРОВАННОЕ ПОДЛЕЖАЩЕЕ — НЕ ДЫРЫ НОСИТЕЛЯ, А ЧАСТИ СКАЗУЕМОГО. Имя в
#     них не стои́т ни на одной странице ни одного языка — не оттого, что дом поленился, а
#     оттого, что язык так устроен.
#
# Языки названы поимённо; романский рынок (удвоение клитики «a Marta le quedan») есть рынок
# ИНОЙ формы и ставится отдельно, а не подстановкой.
БЛИЗНЕЦ_СЕРЕДИНЫ_ЯЗЫКИ = frozenset({"ru", "de", "en", "nl", "pl"})


def близнец_середины(язык, рамка):
    """Имя в СРЕДИННЫХ гнёздах носителя; местоимение начала предложения сохранено.

    None, если срединных гнёзд нет или язык не объявлен пригодным.
    """
    if язык not in БЛИЗНЕЦ_СЕРЕДИНЫ_ЯЗЫКИ or isinstance(рамка, tuple):
        return None
    начала = {м.start() for м in _МЕСТОИМЕНИЕ_В_НАЧАЛЕ.finditer(рамка)}
    места = [м for м in _ДЫРА.finditer(рамка)
             if м.group(1) in ПАДЕЖ_НОСИТЕЛЯ and м.start() not in начала]
    if not места:
        return None
    куски, было = [], 0
    for м in места:
        куски.append(рамка[было:м.start()] + "{" + ПАДЕЖ_НОСИТЕЛЯ[м.group(1)] + "}")
        было = м.end()
    куски.append(рамка[было:])
    двойник = "".join(куски)
    return двойник if двойник != рамка else None


def страница(язык, форма, i, j, Т, n, k, вариант=0, имя=False, середина=False):
    if язык in ОБЪЯВЛЕННЫЕ_ПРОПУСКИ.get(форма, ()):
        return None
    р = РАМКИ[язык][форма]
    if имя:
        р = близнец(р) if not isinstance(р, tuple) else None
        if р is None:
            return None
    elif середина:
        р = близнец_середины(язык, р)
        if р is None:
            return None
    if isinstance(р, tuple):
        # A FORM MAY WEAR SEVERAL SURFACES IN ONE LANGUAGE (BESEDA-11, pt «если»: «com quantas
        # ficará?» and «quantas lhe restarão?» are one question); the variant picks the surface
        р = р[вариант % len(р)]
    п = _поля(язык, i, j, Т, n, k, форма)
    if форма == "итог":
        п.update(ГОЛОВА=ГОЛОВЫ_ИТОГА[язык][вариант % len(ГОЛОВЫ_ИТОГА[язык])])
    if форма in ("итог", "итог_всего"):
        цвета = ЦВЕТА_М[язык] if п.get("_род") == "m" and язык in ЦВЕТА_М else ЦВЕТА[язык]
        п.update(Ц1=цвета[0], Ц2=цвета[1])
    if форма in ("доля", "доля_не"):
        q = (2, 3, 4)[вариант % 3]
        if n % q:
            return None            # a share is shown only where it divides — no fractions of things
        п.update(q=q, r=n // q, d=n - n // q, ДОЛЯ=ДОЛИ[язык][q], ЦП=ЦВЕТ_ПРЕД[язык][Т % 2])
    if форма == "время":
        в1, в2 = ВРЕМЯ[язык][вариант % len(ВРЕМЯ[язык])]
        п.update(В1=в1, В2=в2)
    if форма == "единица":
        n_, k_ = ЦЕНЫ[вариант % len(ЦЕНЫ)]
        п.update(n=n_, k=k_, v=n_ * k_, Тмн=A._вещь(язык, Т, 5))
    if форма == "товар":
        г1, г2, г3 = ТОВАРЫ[язык][вариант % len(ТОВАРЫ[язык])]
        п.update(Г1a=_счёт(г1, n, язык), Г2b=_счёт(г2, k, язык), Г3мн=г3[-1], Г3s=_счёт(г3, n + k, язык))
    return р.format(**п)


def _счёт(ф, c, язык="ru"):
    """Count form of a declared goods phrase: (one, many) for en, (one, few, many) for ru and pl.

    THE RULE IS THE PACK'S, NOT RUSSIAN (05.09, the agreement court: «21 kwiat», «31 moneta» —
    Polish gives 21, 31, 101 the genitive plural, only exactly 1 the singular; Russian gives 21
    the singular). The cell is read from the language pack's declared count_agreement."""
    if len(ф) == 2:
        return ф[0] if c == 1 else ф[1]
    return ф[_ячейка(язык, c)]


_ПАКЕТЫ_СЧЁТА = {}


def _ячейка(язык, c):
    import langpack
    if язык not in _ПАКЕТЫ_СЧЁТА:
        _ПАКЕТЫ_СЧЁТА[язык] = json.loads((_ПАКЕТЫ / f"{язык}.json").read_text(encoding="utf-8"))
    return langpack.count_form_index(_ПАКЕТЫ_СЧЁТА[язык], {"forms": ["one", "few", "many"]}, c)


def _показы():
    вон = {}
    for язык in РАМКИ:
        лиц = len(A.ЛИЦА[язык]); вещей = len(A.ЯЗЫКИ[язык]["вещи"])
        for форма in ФОРМЫ:
            if форма not in РАМКИ[язык]:
                continue
            ряд = ЧИСЛА_ДОЛИ if форма in ("доля", "доля_не") else ЧИСЛА
            for q, (n, k) in enumerate(ряд):
                i = q % лиц; j = (q * 3 + 1) % лиц; Т = q % вещей
                варианты = 3 if форма in ("итог", "время", "товар", "доля", "доля_не") else (4 if форма == "единица" else 1)
                if isinstance(РАМКИ[язык][форма], tuple):
                    варианты = max(варианты, len(РАМКИ[язык][форма]))
                for вариант in range(варианты):
                    с = страница(язык, форма, i, j, Т, n, k, вариант)
                    if с:
                        вон[с] = (язык, форма)
                с = страница(язык, форма, i, j, Т, n, k, 0, имя=True)
                if с:
                    вон[с] = (язык, форма)
                с = страница(язык, форма, i, j, Т, n, k, 0, середина=True)
                if с:
                    вон[с] = (язык, форма)
    return вон


ПОКАЗЫ = _показы()


def _годы(язык):
    import numberline as _NL
    return list(_NL.ГОД[язык].values()) + list(_NL.ГОД_ПОСЛЕ.get(язык, {}).values())


def _слова_скрытого(язык, ключ):
    з = СКРЫТОЕ[язык][ключ]
    return list(з) if isinstance(з, tuple) else [з]


def _образцы():
    """A regex per frame: names, things, pronouns, time words and goods are declared
    alternations; numbers are holes; the ledger is read by the judge."""
    вон = []
    alt = lambda слова: "(?:" + "|".join(re.escape(с) for с in sorted(set(с for с in слова if с), key=lambda с: (-len(с), с))) + ")"
    for язык, рамки in РАМКИ.items():
        имена = [л[0] for л in A.ЛИЦА[язык]]; род = [л[2] for л in A.ЛИЦА[язык]]
        имена = [_лицо(язык, i)[0] for i in range(len(A.ЛИЦА[язык]))]
        дат = ([_дательный(л[0]) for л in A.ЛИЦА[язык]] if язык == "ru" else
               [ДАТЕЛЬНЫЙ_PL.get(л[0], л[0]) for л in A.ЛИЦА[язык]] if язык == "pl" else
               [_дательный_pt(_лицо(язык, i)) for i in range(len(A.ЛИЦА[язык]))] if язык == "pt" else имена)
        вещи = [A._вещь(язык, Т, c) for Т in range(len(A.ЯЗЫКИ[язык]["вещи"])) for c in (1, 2, 5)]
        вещи1 = [A._вещь(язык, Т, 1) for Т in range(len(A.ЯЗЫКИ[язык]["вещи"]))]
        мест = [v for г in МЕСТОИМЕНИЯ[язык].values() for v in г.values()]
        товары = [ф for ряд in ТОВАРЫ.get(язык, ()) for г in ряд for ф in г]
        дыры = {"X": alt(имена), "Y": alt(имена), "Xр": alt(род), "Yд": alt(дат), "Xд": alt(дат), "он": alt(мест), "Он": alt(мест), "него": alt(мест), "ему": alt(мест),
                "а": "(?:а|о|и|a|)", "аY": "(?:а|о|и|a|)", "НАШЁЛ": "(?:нашёл|нашла)", "n": r"(\d+)", "k": r"(\d+)", "r": r"(\d+)", "s": r"(\d+)", "a": r"(\d+)", "b": r"(\d+)", "v": r"(\d+)",
                "m": r"(\d+)", "t": r"(\d+)", "q": r"(\d+)", "d": r"(\d+)",
                "ДОЛЯ": alt(ДОЛИ[язык].values()), "ЦП": alt(ЦВЕТ_ПРЕД[язык]),
                # ДЫРА СКРЫТОГО КОЛИЧЕСТВА ПРИНИМАЕТ ТОЛЬКО ОБЪЯВЛЕННОЕ СЛОВО: строка с числом на
                # этом месте есть строка другого рода, и дом её не признаёт (суд самопроверки).
                "СК": alt(_слова_скрытого(язык, "несколько")), "СКЧ": alt(_слова_скрытого(язык, "часть")),
                "Гn": alt(_годы(язык)), "Гk": alt(_годы(язык)), "Гs": alt(_годы(язык)),
                "Тn": alt(вещи), "Тk": alt(вещи), "Тr": alt(вещи), "Тs": alt(вещи), "Тмн": alt(вещи), "Т1": alt(вещи1), "Тm": alt(вещи),
                "ГОЛОВА": alt(ГОЛОВЫ_ИТОГА[язык]), "Ц1": alt(ЦВЕТА[язык] + ЦВЕТА_М.get(язык, ())), "Ц2": alt(ЦВЕТА[язык] + ЦВЕТА_М.get(язык, ())),
                "В1": alt(в for в, _ in ВРЕМЯ[язык]), "В2": alt(в for _, в in ВРЕМЯ[язык]),
                "Г1a": alt(товары), "Г2b": alt(товары), "Г3мн": alt(товары), "Г3s": alt(товары)}
        if язык == "pl":
            дыры["ЕСТЬn"] = alt(_PL.СВЯЗКА["наст"])
        for дыра, пара in РОДОВЫЕ.get(язык, {}).items():
            дыры[дыра] = alt(пара)
        дыры.update({"Yр": alt(род), "онY": alt(мест), "негоY": alt(мест), "емуY": alt(мест),
                     "Xде": alt(_имя_чьё(язык, _лицо(язык, i)) for i in range(len(A.ЛИЦА[язык])))})
        for ключ in {к for г in РОДНЯ[язык].values() for к in г}:
            дыры[ключ] = alt(г.get(ключ) for г in РОДНЯ[язык].values())
        for форма, рамки_формы in рамки.items():
            поверхности = list(рамки_формы if isinstance(рамки_формы, tuple) else (рамки_формы,))
            if not isinstance(рамки_формы, tuple):
                for двойник in (близнец(рамки_формы), близнец_середины(язык, рамки_формы)):
                    if двойник:
                        поверхности.append(двойник)
            for рамка in поверхности:
                куски = []
                for кусок in re.split(r"(\{[^}]+\})", рамка):
                    куски.append(дыры[кусок[1:-1]] if кусок.startswith("{") else re.escape(кусок))
                вон.append((re.compile("^" + "".join(куски) + "$"), язык, форма))
    return вон


ОБРАЗЦЫ = _образцы()

# ГЛАГОЛЫ-АКТЫ ЖИВОЙ ПОЛОСЫ (holon, атлас непрочитанных чисел, 06.09): пятая точка купила 307
# глаголов истории, но среди них нет тех, на которых стоят десятки задач SVAMP — did, added, threw
# away, learned that … came, got on / got off, played, spent; и формы «a box of N crayons»,
# «a total of N hours», «the first chapter is N pages long», две клаузы с «and», список через
# запятую того же товара, «ones» = тот же товар. Каждому глаголу — ≥ LAW показов как АКТ: носитель +
# глагол + число + товар + вопрос. Товары объявлены со счётными формами (en: one/many; ru: one/few/many).
ТОВАРЫ_АКТОВ = {
    "en": {"отжимания": ("push-up", "push-ups"), "скручивания": ("crunch", "crunches"), "приложения": ("app", "apps"),
           "фигурки": ("action figure", "action figures"), "крышки": ("bottle cap", "bottle caps"), "розы": ("rose", "roses"),
           "посетители": ("visitor", "visitors"), "дети": ("child", "children"), "игры": ("game", "games"), "часы": ("hour", "hours"),
           "мелки": ("crayon", "crayons"), "страницы": ("page", "pages")},
    "ru": {"отжимания": ("отжимание", "отжимания", "отжиманий"), "скручивания": ("скручивание", "скручивания", "скручиваний"),
           "приложения": ("приложение", "приложения", "приложений"), "фигурки": ("фигурка", "фигурки", "фигурок"),
           "крышки": ("крышка", "крышки", "крышек"), "розы": ("роза", "розы", "роз"), "посетители": ("посетитель", "посетителя", "посетителей"),
           "дети": ("ребёнок", "ребёнка", "детей"), "игры": ("игра", "игры", "игр"), "часы": ("час", "часа", "часов"),
           "мелки": ("мелок", "мелка", "мелков"), "страницы": ("страница", "страницы", "страниц")},
}
РАМКИ_АКТОВ = {
    "en": dict(
        сделал="{X} did {n} {ОТЖn} and {k} {СКРk}. how many {ОТЖмн} did {X} do? {n}. how many exercises in all? {s}: {n} + {k} = {s}.",
        больше_чем="{X} did {n} {ОТЖn}. {Y} did {k} more {ОТЖмн} than {X}. how many {ОТЖмн} did {Y} do? {s}: {n} + {k} = {s}.",
        меньше_чем="{X} did {n} {ОТЖn}. {Y} did {k} {ОТЖмн} less than {X}. how many {ОТЖмн} did {Y} do? {r}: {n} − {k} = {r}.",
        # THE p156 FEED (d5, 05.09): sold; joined them; were living / moved out; suggested / removed … of them;
        # a decoration before «there are N girls and M boys»; the recipe calls for; «now he has N … and M …»
        вещи3="{X} has {n} {ФИГn}, {k} {МЕЛk} and {m} {ИГРm}. how many things does {X} have in all? {t}: {n} + {k} + {m} = {t}.",
        продал="{X} had {n} {РОЗn}. {Он} sold {k} {РОЗk}. how many {РОЗмн} does {он} have left? {r}: {n} − {k} = {r}.",
        присоединились="there were {n} {ДЕТn} on the playground. {k} more {ДЕТk} joined them. how many {ДЕТмн} are on the playground now? {s}: {n} + {k} = {s}.",
        жили="{n} {ЖИЛn} were living in the house. {k} {ЖИЛk} moved out. how many {ЖИЛмн} are living in the house now? {r}: {n} − {k} = {r}.",
        предложил="{X} suggested {n} {ФИГn} for the shelf. {Y} removed {k} of them. how many {ФИГмн} are left? {r}: {n} − {k} = {r}.",
        в_школе="in a school there are {n} {ДЕВn} and {k} {МАЛk}. how many pupils are there in the school? {s}: {n} + {k} = {s}.",
        рецепт="the recipe calls for {n} {ЧАШn} of flour and {k} {ЧАШk} of sugar. how many more cups of flour than sugar does it call for? {r}: {n} − {k} = {r}.",
        теперь_список="{X} had {n} {ФИГn}. {Он} also got {k} {МЕЛk}. now {он} has {n} {ФИГn} and {k} {МЕЛk}. how many things does {он} have in all? {s}: {n} + {k} = {s}.",
        добавил="{X} had {n} {ПРИЛn} on the phone. {Он} added {k} new {ПРИЛмн}. how many {ПРИЛмн} does {он} have now? {s}: {n} + {k} = {s}.",
        добавил_на_полку="{X} had {n} {ФИГn} on the shelf. later {он} added {k} more {ФИГмн} to the shelf. how many {ФИГмн} are on the shelf now? {s}: {n} + {k} = {s}.",
        выбросил="{X} found {n} {КРЫШn} at the park while {он} threw away {k} old ones. how many more {КРЫШмн} did {он} find than throw away? {r}: {n} − {k} = {r}.",
        выбросил_розы="there were {n} {РОЗn} in the vase. {X} threw away {k} {РОЗмн} from the vase. how many {РОЗмн} are in the vase now? {r}: {n} − {k} = {r}.",
        узнал="{X} learned that {n} {ПОСn} came to the palace that day and {k} the next day. how many {ПОСмн} came in all? {s}: {n} + {k} = {s}.",
        сели_вышли="there were {n} {ДЕТn} on the bus. at the bus stop {k} {ДЕТмн} got on the bus while some got off. now there are {s} {ДЕТмн} on the bus. how many {ДЕТмн} got off? {k2}: {n} + {k} − {s} = {k2}.",
        сыграл="{X} played {n} {ИГРn} on monday and {k} {ИГРмн} on tuesday. how many {ИГРмн} did {X} play in all? {s}: {n} + {k} = {s}.",
        потратил="{X} spent {n} {ЧАСn} on english and {k} {ЧАСмн} on chinese. how many {ЧАСмн} did {X} spend in all? a total of {s} {ЧАСмн}: {n} + {k} = {s}.",
        список="every day {X} spends {n} {ЧАСn} on english, {k} {ЧАСмн} on chinese and {m} {ЧАСмн} on spanish. how many {ЧАСмн} does {X} spend in all? {t}: {n} + {k} + {m} = {t}.",
        коробка="{X} got a box of {n} {МЕЛn} and a box of {k} {МЕЛмн}. how many {МЕЛмн} does {X} have? {s}: {n} + {k} = {s}.",
        главы="a book has 2 chapters. the first chapter is {n} {СТРn} long and the second chapter is {k} {СТРмн} long. how many {СТРмн} does the book have in all? {s}: {n} + {k} = {s}.",
        две_клаузы="{X} had {n} {ИГРn} and {Y} had {k} {ИГРмн}. how many {ИГРмн} did they have together? {s}: {n} + {k} = {s}.",
    ),
    "ru": dict(
        сделал="{X} сделал{а} {n} {ОТЖn} и {k} {СКРk}. сколько {ОТЖмн} сделал{а} {X}? {n}. сколько упражнений всего? {s}: {n} + {k} = {s}.",
        больше_чем="{X} сделал{а} {n} {ОТЖn}. {Y} сделал{аY} на {k} {ОТЖk} больше, чем {X}. сколько {ОТЖмн} сделал{аY} {Y}? {s}: {n} + {k} = {s}.",
        меньше_чем="{X} сделал{а} {n} {ОТЖn}. {Y} сделал{аY} на {k} {ОТЖk} меньше, чем {X}. сколько {ОТЖмн} сделал{аY} {Y}? {r}: {n} − {k} = {r}.",
        вещи3="у {Xр} {n} {ФИГn}, {k} {МЕЛk} и {m} {ИГРm}. сколько всего предметов у {Xр}? {t}: {n} + {k} + {m} = {t}.",
        продал="у {Xр} было {n} {РОЗn}. {Он} продал{а} {k} {РОЗk}. сколько {РОЗмн} у {него} осталось? {r}: {n} − {k} = {r}.",
        присоединились="на площадке было {n} {ДЕТn}. к ним присоединилось ещё {k} {ДЕТk}. сколько {ДЕТмн} на площадке теперь? {s}: {n} + {k} = {s}.",
        жили="в доме жило {n} {ЖИЛn}. {k} {ЖИЛk} съехали. сколько {ЖИЛмн} живёт в доме теперь? {r}: {n} − {k} = {r}.",
        предложил="{X} предложил{а} для полки {n} {ФИГn}. {Y} убрал{аY} {k} из них. сколько {ФИГмн} осталось? {r}: {n} − {k} = {r}.",
        в_школе="в школе {n} {ДЕВn} и {k} {МАЛk}. сколько всего учеников в школе? {s}: {n} + {k} = {s}.",
        рецепт="по рецепту нужно {n} {ЧАШn} муки и {k} {ЧАШk} сахара. на сколько {ЧАШмн} муки больше, чем сахара? {r}: {n} − {k} = {r}.",
        теперь_список="у {Xр} было {n} {ФИГn}. ещё {он} получил{а} {k} {МЕЛk}. теперь у {него} {n} {ФИГn} и {k} {МЕЛk}. сколько всего предметов у {него}? {s}: {n} + {k} = {s}.",
        добавил="у {Xр} было {n} {ПРИЛn} в телефоне. {Он} добавил{а} {k} {ПРИЛk}. сколько {ПРИЛмн} у {него} теперь? {s}: {n} + {k} = {s}.",
        добавил_на_полку="у {Xр} на полке было {n} {ФИГn}. потом {он} добавил{а} на полку ещё {k} {ФИГk}. сколько {ФИГмн} на полке теперь? {s}: {n} + {k} = {s}.",
        выбросил="{X} {НАШЁЛ} в парке {n} {КРЫШn}, а {k} старых выбросил{а}. на сколько больше {КРЫШмн} {он} {НАШЁЛ}, чем выбросил{а}? {r}: {n} − {k} = {r}.",
        выбросил_розы="в вазе было {n} {РОЗn}. {X} выбросил{а} из вазы {k} {РОЗk}. сколько {РОЗмн} в вазе теперь? {r}: {n} − {k} = {r}.",
        узнал="{X} узнал{а}, что во дворец в тот день пришли {n} {ПОСn}, а на следующий — {k}. сколько {ПОСмн} пришло всего? {s}: {n} + {k} = {s}.",
        сели_вышли="в автобусе было {n} {ДЕТn}. на остановке {k} {ДЕТk} сели, а несколько вышли. теперь в автобусе {s} {ДЕТs}. сколько {ДЕТмн} вышло? {k2}: {n} + {k} − {s} = {k2}.",
        сыграл="{X} сыграл{а} {n} {ИГРn} в понедельник и {k} {ИГРk} во вторник. сколько {ИГРмн} сыграл{а} {X} всего? {s}: {n} + {k} = {s}.",
        потратил="{X} потратил{а} {n} {ЧАСn} на английский и {k} {ЧАСk} на китайский. сколько {ЧАСмн} потратил{а} {X} всего? всего {s} {ЧАСs}: {n} + {k} = {s}.",
        список="каждый день {X} тратит {n} {ЧАСn} на английский, {k} {ЧАСk} на китайский и {m} {ЧАСm} на испанский. сколько {ЧАСмн} тратит {X} всего? {t}: {n} + {k} + {m} = {t}.",
        коробка="{X} получил{а} коробку с {n} {МЕЛпр} и коробку с {k} {МЕЛпр}. сколько {МЕЛмн} у {Xр}? {s}: {n} + {k} = {s}.",
        главы="в книге 2 главы. в первой главе {n} {СТРn}, во второй — {k} {СТРk}. сколько {СТРмн} в книге всего? {s}: {n} + {k} = {s}.",
        две_клаузы="у {Xр} было {n} {ИГРn}, а у {Yр} — {k} {ИГРk}. сколько {ИГРмн} было у них вместе? {s}: {n} + {k} = {s}.",
    ),
}
# ФОРМА ТОВАРА ПОСЛЕ ПРЕДЛОГА, ПРАВЯЩЕГО ПАДЕЖОМ, — ОБЪЯВЛЕНА, А НЕ ВЫВЕДЕНА.
#
# Свод три дня нёс «коробку с 12 мелков», «pudełko z 12 kredek», «eine Schachtel mit 12
# Buntstifte» — 24 строки, ложные о языке, и НИ ОДИН СУД ИХ НЕ ЧИТАЛ. Причина не в небрежности,
# а в том, что СЧЁТНАЯ ФОРМА НЕ ЕСТЬ ПАДЕЖНАЯ: «мелков» — верная счётная форма при двенадцати,
# и суд согласования, сверяющий счёт, видел верное. Но «с» правит творительным, «z» правит
# творительным, «mit» правит дательным, и правление предлога числом не выводится: при двенадцати
# и при пяти форма ОДНА И ТА ЖЕ («с 12 мелками», «с 5 мелками»), тогда как счётная — разная.
#
# Форма объявлена только для трёх языков, что её метят; прочие шесть падежа здесь не имеют, и
# рамка их не трогает. Ячейка образца принимает ТОЛЬКО объявленную форму, а не любую из форм
# товара, — потому строка со счётной формой становится НЕСУДИМОЙ, и ворота записи слоя её не
# пропустят: дефект сделан невозможным, а не обнаружимым.
ПРИ_ПРЕДЛОГЕ = {
    "ru": {"мелки": "мелками"},
    "pl": {"мелки": "kredkami"},
    "de": {"мелки": "Buntstiften"},
}
_ТОВАР_ПО_ДЫРЕ = {"ОТЖ": "отжимания", "СКР": "скручивания", "ПРИЛ": "приложения", "ФИГ": "фигурки", "КРЫШ": "крышки", "РОЗ": "розы",
                  "ПОС": "посетители", "ДЕТ": "дети", "ИГР": "игры", "ЧАС": "часы", "МЕЛ": "мелки", "СТР": "страницы"}
ТОВАРЫ_АКТОВ.update({
    "de": {"отжимания": ("Liegestütz", "Liegestütze"), "скручивания": ("Sit-up", "Sit-ups"), "приложения": ("App", "Apps"), "фигурки": ("Actionfigur", "Actionfiguren"), "крышки": ("Kronkorken", "Kronkorken"), "розы": ("Rose", "Rosen"), "посетители": ("Besucher", "Besucher"), "дети": ("Kind", "Kinder"), "игры": ("Spiel", "Spiele"), "часы": ("Stunde", "Stunden"), "мелки": ("Buntstift", "Buntstifte"), "страницы": ("Seite", "Seiten")},
    "fr": {"отжимания": ("pompe", "pompes"), "скручивания": ("abdo", "abdos"), "приложения": ("application", "applications"), "фигурки": ("figurine", "figurines"), "крышки": ("capsule", "capsules"), "розы": ("rose", "roses"), "посетители": ("visiteur", "visiteurs"), "дети": ("enfant", "enfants"), "игры": ("partie", "parties"), "часы": ("heure", "heures"), "мелки": ("crayon", "crayons"), "страницы": ("page", "pages")},
    "es": {"отжимания": ("flexión", "flexiones"), "скручивания": ("abdominal", "abdominales"), "приложения": ("aplicación", "aplicaciones"), "фигурки": ("figura", "figuras"), "крышки": ("chapa", "chapas"), "розы": ("rosa", "rosas"), "посетители": ("visitante", "visitantes"), "дети": ("niño", "niños"), "игры": ("partida", "partidas"), "часы": ("hora", "horas"), "мелки": ("lápiz de color", "lápices de colores"), "страницы": ("página", "páginas")},
    "it": {"отжимания": ("flessione", "flessioni"), "скручивания": ("addominale", "addominali"), "приложения": ("app", "app"), "фигурки": ("statuina", "statuine"), "крышки": ("tappo", "tappi"), "розы": ("rosa", "rose"), "посетители": ("visitatore", "visitatori"), "дети": ("bambino", "bambini"), "игры": ("partita", "partite"), "часы": ("ora", "ore"), "мелки": ("pastello", "pastelli"), "страницы": ("pagina", "pagine")},
    "pt": {"отжимания": ("flexão", "flexões"), "скручивания": ("abdominal", "abdominais"), "приложения": ("aplicação", "aplicações"), "фигурки": ("boneco", "bonecos"), "крышки": ("tampa", "tampas"), "розы": ("rosa", "rosas"), "посетители": ("visitante", "visitantes"), "дети": ("criança", "crianças"), "игры": ("jogo", "jogos"), "часы": ("hora", "horas"), "мелки": ("lápis de cor", "lápis de cor"), "страницы": ("página", "páginas")},
    "nl": {"отжимания": ("push-up", "push-ups"), "скручивания": ("sit-up", "sit-ups"), "приложения": ("app", "apps"), "фигурки": ("actiefiguur", "actiefiguren"), "крышки": ("dop", "doppen"), "розы": ("roos", "rozen"), "посетители": ("bezoeker", "bezoekers"), "дети": ("kind", "kinderen"), "игры": ("spel", "spellen"), "часы": ("uur", "uur"), "мелки": ("kleurpotlood", "kleurpotloden"), "страницы": ("pagina", "pagina's")},
    "pl": {"отжимания": ("pompka", "pompki", "pompek"), "скручивания": ("brzuszek", "brzuszki", "brzuszków"), "приложения": ("aplikacja", "aplikacje", "aplikacji"), "фигурки": ("figurka", "figurki", "figurek"), "крышки": ("kapsel", "kapsle", "kapsli"), "розы": ("róża", "róże", "róż"), "посетители": ("gość", "goście", "gości"), "дети": ("dziecko", "dzieci", "dzieci"), "игры": ("gra", "gry", "gier"), "часы": ("godzina", "godziny", "godzin"), "мелки": ("kredka", "kredki", "kredek"), "страницы": ("strona", "strony", "stron")},
})
# GOODS OF THE p156 FEED (d5, reader traces, 05.09): girls / boys, cups, tenants — with count forms
for _яз, _новые in {
    "en": {"девочки": ("girl", "girls"), "мальчики": ("boy", "boys"), "чашки": ("cup", "cups"), "жильцы": ("tenant", "tenants")},
    "ru": {"девочки": ("девочка", "девочки", "девочек"), "мальчики": ("мальчик", "мальчика", "мальчиков"), "чашки": ("чашка", "чашки", "чашек"), "жильцы": ("жилец", "жильца", "жильцов")},
    "de": {"девочки": ("Mädchen", "Mädchen"), "мальчики": ("Junge", "Jungen"), "чашки": ("Tasse", "Tassen"), "жильцы": ("Mieter", "Mieter")},
    "fr": {"девочки": ("fille", "filles"), "мальчики": ("garçon", "garçons"), "чашки": ("tasse", "tasses"), "жильцы": ("locataire", "locataires")},
    "es": {"девочки": ("niña", "niñas"), "мальчики": ("niño", "niños"), "чашки": ("taza", "tazas"), "жильцы": ("inquilino", "inquilinos")},
    "it": {"девочки": ("bambina", "bambine"), "мальчики": ("bambino", "bambini"), "чашки": ("tazza", "tazze"), "жильцы": ("inquilino", "inquilini")},
    "pt": {"девочки": ("menina", "meninas"), "мальчики": ("menino", "meninos"), "чашки": ("chávena", "chávenas"), "жильцы": ("inquilino", "inquilinos")},
    "nl": {"девочки": ("meisje", "meisjes"), "мальчики": ("jongen", "jongens"), "чашки": ("kopje", "kopjes"), "жильцы": ("huurder", "huurders")},
    "pl": {"девочки": ("dziewczynka", "dziewczynki", "dziewczynek"), "мальчики": ("chłopiec", "chłopcy", "chłopców"), "чашки": ("filiżanka", "filiżanki", "filiżanek"), "жильцы": ("lokator", "lokatorzy", "lokatorów")},
}.items():
    ТОВАРЫ_АКТОВ[_яз].update(_новые)
_ТОВАР_ПО_ДЫРЕ.update({"ДЕВ": "девочки", "МАЛ": "мальчики", "ЧАШ": "чашки", "ЖИЛ": "жильцы"})
РАМКИ_АКТОВ.update({
    "de": dict(
               больше_чем="{X} machte {n} {ОТЖn}. {Y} machte {k} {ОТЖмн} mehr als {X}. wie viele {ОТЖмн} machte {Y}? {s}: {n} + {k} = {s}.",
               меньше_чем="{X} machte {n} {ОТЖn}. {Y} machte {k} {ОТЖмн} weniger als {X}. wie viele {ОТЖмн} machte {Y}? {r}: {n} − {k} = {r}.",
               добавил_на_полку="{X} hatte {n} {ФИГn} im Regal. später stellte {он} {k} weitere {ФИГмн} ins Regal. wie viele {ФИГмн} stehen jetzt im Regal? {s}: {n} + {k} = {s}.",
               выбросил="{X} fand im Park {n} {КРЫШn} und warf {k} alte weg. wie viele {КРЫШмн} mehr fand {он}, als {он} wegwarf? {r}: {n} − {k} = {r}.",
               выбросил_розы="in der Vase waren {n} {РОЗn}. {X} warf {k} {РОЗмн} aus der Vase weg. wie viele {РОЗмн} sind jetzt in der Vase? {r}: {n} − {k} = {r}.",
               узнал="{X} erfuhr, dass an dem Tag {n} {ПОСn} in den Palast kamen und am nächsten Tag {k}. wie viele {ПОСмн} kamen insgesamt? {s}: {n} + {k} = {s}.",
               сели_вышли="im Bus waren {n} {ДЕТn}. an der Haltestelle stiegen {k} {ДЕТмн} ein, während einige ausstiegen. jetzt sind {s} {ДЕТмн} im Bus. wie viele {ДЕТмн} stiegen aus? {k2}: {n} + {k} − {s} = {k2}.",
               сыграл="{X} spielte am Montag {n} {ИГРn} und am Dienstag {k} {ИГРмн}. wie viele {ИГРмн} spielte {X} insgesamt? {s}: {n} + {k} = {s}.",
               потратил="{X} verbrachte {n} {ЧАСn} mit Englisch und {k} {ЧАСмн} mit Chinesisch. wie viele {ЧАСмн} verbrachte {X} insgesamt? insgesamt {s} {ЧАСмн}: {n} + {k} = {s}.",
               список="jeden Tag verbringt {X} {n} {ЧАСn} mit Englisch, {k} {ЧАСмн} mit Chinesisch und {m} {ЧАСмн} mit Spanisch. wie viele {ЧАСмн} verbringt {X} insgesamt? {t}: {n} + {k} + {m} = {t}.",
               коробка="{X} bekam eine Schachtel mit {n} {МЕЛпр} und eine Schachtel mit {k} {МЕЛпр}. wie viele {МЕЛмн} hat {X}? {s}: {n} + {k} = {s}.",
               главы="ein Buch hat 2 Kapitel. das erste Kapitel ist {n} {СТРn} lang und das zweite {k} {СТРмн}. wie viele {СТРмн} hat das Buch insgesamt? {s}: {n} + {k} = {s}.",
               две_клаузы="{X} hatte {n} {ИГРn} und {Y} hatte {k} {ИГРмн}. wie viele {ИГРмн} hatten sie zusammen? {s}: {n} + {k} = {s}.",
               сделал="{X} machte {n} {ОТЖn} und {k} {СКРk}. wie viele {ОТЖмн} machte {X}? {n}. wie viele Übungen insgesamt? {s}: {n} + {k} = {s}.",
               вещи3="{X} hat {n} {ФИГn}, {k} {МЕЛk} und {m} {ИГРm}. wie viele Dinge hat {X} insgesamt? {t}: {n} + {k} + {m} = {t}.",
               продал="{X} hatte {n} {РОЗn}. {Он} verkaufte {k} {РОЗk}. wie viele {РОЗмн} hat {он} noch? {r}: {n} − {k} = {r}.",
               присоединились="auf dem Spielplatz waren {n} {ДЕТn}. {k} weitere {ДЕТk} kamen dazu. wie viele {ДЕТмн} sind jetzt auf dem Spielplatz? {s}: {n} + {k} = {s}.",
               жили="{n} {ЖИЛn} wohnten im Haus. {k} {ЖИЛk} zogen aus. wie viele {ЖИЛмн} wohnen jetzt im Haus? {r}: {n} − {k} = {r}.",
               предложил="{X} schlug {n} {ФИГn} für das Regal vor. {Y} nahm {k} davon weg. wie viele {ФИГмн} bleiben übrig? {r}: {n} − {k} = {r}.",
               в_школе="in einer Schule gibt es {n} {ДЕВn} und {k} {МАЛk}. wie viele Schüler gibt es in der Schule? {s}: {n} + {k} = {s}.",
               рецепт="das Rezept verlangt {n} {ЧАШn} Mehl und {k} {ЧАШk} Zucker. wie viele Tassen Mehl mehr als Zucker verlangt es? {r}: {n} − {k} = {r}.",
               теперь_список="{X} hatte {n} {ФИГn}. {Он} bekam noch {k} {МЕЛk}. jetzt hat {он} {n} {ФИГn} und {k} {МЕЛk}. wie viele Dinge hat {он} insgesamt? {s}: {n} + {k} = {s}.",
               добавил="{X} hatte {n} {ПРИЛn} auf dem Handy. {Он} fügte {k} neue {ПРИЛмн} hinzu. wie viele {ПРИЛмн} hat {он} jetzt? {s}: {n} + {k} = {s}."),
    "fr": dict(
               больше_чем="{X} a fait {n} {ОТЖn}. {Y} a fait {k} {ОТЖмн} de plus que {X}. combien de {ОТЖмн} {Y} a-t-{аY_он} faites ? {s} : {n} + {k} = {s}.",
               меньше_чем="{X} a fait {n} {ОТЖn}. {Y} a fait {k} {ОТЖмн} de moins que {X}. combien de {ОТЖмн} {Y} a-t-{аY_он} faites ? {r} : {n} − {k} = {r}.",
               добавил_на_полку="{X} avait {n} {ФИГn} sur l'étagère. plus tard {он} a ajouté {k} {ФИГмн} de plus sur l'étagère. combien de {ФИГмн} y a-t-il sur l'étagère maintenant ? {s} : {n} + {k} = {s}.",
               выбросил="{X} a trouvé {n} {КРЫШn} au parc et en a jeté {k} vieilles. combien de {КРЫШмн} de plus {X} a-t-{он} trouvées que jetées ? {r} : {n} − {k} = {r}.",
               выбросил_розы="il y avait {n} {РОЗn} dans le vase. {X} a jeté {k} {РОЗмн} du vase. combien de {РОЗмн} y a-t-il dans le vase maintenant ? {r} : {n} − {k} = {r}.",
               узнал="{X} a appris que {n} {ПОСn} sont venus au palais ce jour-là et {k} le lendemain. combien de {ПОСмн} sont venus en tout ? {s} : {n} + {k} = {s}.",
               сели_вышли="il y avait {n} {ДЕТn} dans le bus. à l'arrêt {k} {ДЕТмн} sont montés tandis que quelques-uns sont descendus. maintenant il y a {s} {ДЕТмн} dans le bus. combien d'{ДЕТмн} sont descendus ? {k2} : {n} + {k} − {s} = {k2}.",
               сыграл="{X} a joué {n} {ИГРn} lundi et {k} {ИГРмн} mardi. combien de {ИГРмн} {X} a-t-{он} jouées en tout ? {s} : {n} + {k} = {s}.",
               потратил="{X} a passé {n} {ЧАСn} sur l'anglais et {k} {ЧАСмн} sur le chinois. combien d'{ЧАСмн} {X} a-t-{он} passées en tout ? un total de {s} {ЧАСмн} : {n} + {k} = {s}.",
               список="chaque jour {X} passe {n} {ЧАСn} sur l'anglais, {k} {ЧАСмн} sur le chinois et {m} {ЧАСмн} sur l'espagnol. combien d'{ЧАСмн} {X} passe-t-{он} en tout ? {t} : {n} + {k} + {m} = {t}.",
               коробка="{X} a reçu une boîte de {n} {МЕЛn} et une boîte de {k} {МЕЛмн}. combien de {МЕЛмн} {X} a-t-{он} ? {s} : {n} + {k} = {s}.",
               главы="un livre a 2 chapitres. le premier chapitre fait {n} {СТРn} et le second {k} {СТРмн}. combien de {СТРмн} le livre a-t-il en tout ? {s} : {n} + {k} = {s}.",
               две_клаузы="{X} avait {n} {ИГРn} et {Y} avait {k} {ИГРмн}. combien de {ИГРмн} avaient-ils ensemble ? {s} : {n} + {k} = {s}.",
               сделал="{X} a fait {n} {ОТЖn} et {k} {СКРk}. combien de {ОТЖмн} {X} a-t-{он} faites ? {n}. combien d'exercices en tout ? {s} : {n} + {k} = {s}.",
               вещи3="{X} a {n} {ФИГn}, {k} {МЕЛk} et {m} {ИГРm}. combien d'objets a {X} en tout ? {t} : {n} + {k} + {m} = {t}.",
               продал="{X} avait {n} {РОЗn}. {Он} a vendu {k} {РОЗk}. combien de {РОЗмн} lui reste-t-il ? {r} : {n} − {k} = {r}.",
               присоединились="il y avait {n} {ДЕТn} sur le terrain de jeu. {k} autres {ДЕТk} les ont rejoints. combien d'{ДЕТмн} y a-t-il maintenant sur le terrain de jeu ? {s} : {n} + {k} = {s}.",
               жили="{n} {ЖИЛn} habitaient la maison. {k} {ЖИЛk} ont déménagé. combien de {ЖИЛмн} habitent la maison maintenant ? {r} : {n} − {k} = {r}.",
               предложил="{X} a proposé {n} {ФИГn} pour l'étagère. {Y} en a retiré {k}. combien de {ФИГмн} reste-t-il ? {r} : {n} − {k} = {r}.",
               в_школе="dans une école il y a {n} {ДЕВn} et {k} {МАЛk}. combien d'élèves y a-t-il dans l'école ? {s} : {n} + {k} = {s}.",
               рецепт="la recette demande {n} {ЧАШn} de farine et {k} {ЧАШk} de sucre. combien de tasses de farine de plus que de sucre demande-t-elle ? {r} : {n} − {k} = {r}.",
               теперь_список="{X} avait {n} {ФИГn}. {Он} a aussi reçu {k} {МЕЛk}. maintenant {он} a {n} {ФИГn} et {k} {МЕЛk}. combien d'objets a-t-{он} en tout ? {s} : {n} + {k} = {s}.",
               добавил="{X} avait {n} {ПРИЛn} sur le téléphone. {Он} a ajouté {k} nouvelles {ПРИЛмн}. combien d'{ПРИЛмн} a-t-{он} maintenant ? {s} : {n} + {k} = {s}."),
    "es": dict(
               больше_чем="{X} hizo {n} {ОТЖn}. {Y} hizo {k} {ОТЖмн} más que {X}. ¿cuántas {ОТЖмн} hizo {Y}? {s}: {n} + {k} = {s}.",
               меньше_чем="{X} hizo {n} {ОТЖn}. {Y} hizo {k} {ОТЖмн} menos que {X}. ¿cuántas {ОТЖмн} hizo {Y}? {r}: {n} − {k} = {r}.",
               добавил_на_полку="{X} tenía {n} {ФИГn} en la estantería. luego añadió {k} {ФИГмн} más a la estantería. ¿cuántas {ФИГмн} hay ahora en la estantería? {s}: {n} + {k} = {s}.",
               выбросил="{X} encontró {n} {КРЫШn} en el parque y tiró {k} viejas. ¿cuántas {КРЫШмн} más encontró de las que tiró? {r}: {n} − {k} = {r}.",
               выбросил_розы="había {n} {РОЗn} en el jarrón. {X} tiró {k} {РОЗмн} del jarrón. ¿cuántas {РОЗмн} hay ahora en el jarrón? {r}: {n} − {k} = {r}.",
               узнал="{X} se enteró de que ese día llegaron {n} {ПОСn} al palacio y al día siguiente {k}. ¿cuántos {ПОСмн} llegaron en total? {s}: {n} + {k} = {s}.",
               сели_вышли="había {n} {ДЕТn} en el autobús. en la parada subieron {k} {ДЕТмн} mientras algunos bajaron. ahora hay {s} {ДЕТмн} en el autobús. ¿cuántos {ДЕТмн} bajaron? {k2}: {n} + {k} − {s} = {k2}.",
               сыграл="{X} jugó {n} {ИГРn} el lunes y {k} {ИГРмн} el martes. ¿cuántas {ИГРмн} jugó {X} en total? {s}: {n} + {k} = {s}.",
               потратил="{X} dedicó {n} {ЧАСn} al inglés y {k} {ЧАСмн} al chino. ¿cuántas {ЧАСмн} dedicó {X} en total? un total de {s} {ЧАСмн}: {n} + {k} = {s}.",
               список="cada día {X} dedica {n} {ЧАСn} al inglés, {k} {ЧАСмн} al chino y {m} {ЧАСмн} al español. ¿cuántas {ЧАСмн} dedica {X} en total? {t}: {n} + {k} + {m} = {t}.",
               коробка="{X} recibió una caja de {n} {МЕЛn} y una caja de {k} {МЕЛмн}. ¿cuántos {МЕЛмн} tiene {X}? {s}: {n} + {k} = {s}.",
               главы="un libro tiene 2 capítulos. el primer capítulo tiene {n} {СТРn} y el segundo {k} {СТРмн}. ¿cuántas {СТРмн} tiene el libro en total? {s}: {n} + {k} = {s}.",
               две_клаузы="{X} tenía {n} {ИГРn} y {Y} tenía {k} {ИГРмн}. ¿cuántas {ИГРмн} tenían juntos? {s}: {n} + {k} = {s}.",
               сделал="{X} hizo {n} {ОТЖn} y {k} {СКРk}. ¿cuántas {ОТЖмн} hizo {X}? {n}. ¿cuántos ejercicios en total? {s}: {n} + {k} = {s}.",
               вещи3="{X} tiene {n} {ФИГn}, {k} {МЕЛk} y {m} {ИГРm}. ¿cuántas cosas tiene {X} en total? {t}: {n} + {k} + {m} = {t}.",
               продал="{X} tenía {n} {РОЗn}. vendió {k} {РОЗk}. ¿cuántas {РОЗмн} le quedan? {r}: {n} − {k} = {r}.",
               присоединились="había {n} {ДЕТn} en el patio. se les unieron {k} {ДЕТk} más. ¿cuántos {ДЕТмн} hay ahora en el patio? {s}: {n} + {k} = {s}.",
               жили="{n} {ЖИЛn} vivían en la casa. {k} {ЖИЛk} se mudaron. ¿cuántos {ЖИЛмн} viven ahora en la casa? {r}: {n} − {k} = {r}.",
               предложил="{X} propuso {n} {ФИГn} para la estantería. {Y} quitó {k} de ellas. ¿cuántas {ФИГмн} quedan? {r}: {n} − {k} = {r}.",
               в_школе="en una escuela hay {n} {ДЕВn} y {k} {МАЛk}. ¿cuántos alumnos hay en la escuela? {s}: {n} + {k} = {s}.",
               рецепт="la receta requiere {n} {ЧАШn} de harina y {k} {ЧАШk} de azúcar. ¿cuántas tazas de harina más que de azúcar requiere? {r}: {n} − {k} = {r}.",
               теперь_список="{X} tenía {n} {ФИГn}. también recibió {k} {МЕЛk}. ahora tiene {n} {ФИГn} y {k} {МЕЛk}. ¿cuántas cosas tiene en total? {s}: {n} + {k} = {s}.",
               добавил="{X} tenía {n} {ПРИЛn} en el teléfono. añadió {k} {ПРИЛмн} nuevas. ¿cuántas {ПРИЛмн} tiene ahora? {s}: {n} + {k} = {s}."),
    "it": dict(
               больше_чем="{X} ha fatto {n} {ОТЖn}. {Y} ha fatto {k} {ОТЖмн} in più di {X}. quante {ОТЖмн} ha fatto {Y}? {s}: {n} + {k} = {s}.",
               меньше_чем="{X} ha fatto {n} {ОТЖn}. {Y} ha fatto {k} {ОТЖмн} in meno di {X}. quante {ОТЖмн} ha fatto {Y}? {r}: {n} − {k} = {r}.",
               добавил_на_полку="{X} aveva {n} {ФИГn} sullo scaffale. più tardi ha aggiunto altre {k} {ФИГмн} allo scaffale. quante {ФИГмн} ci sono ora sullo scaffale? {s}: {n} + {k} = {s}.",
               выбросил="{X} ha trovato {n} {КРЫШn} al parco e ne ha buttati {k} vecchi. quanti {КРЫШмн} in più ha trovato rispetto a quelli buttati? {r}: {n} − {k} = {r}.",
               выбросил_розы="nel vaso c'erano {n} {РОЗn}. {X} ha buttato {k} {РОЗмн} dal vaso. quante {РОЗмн} ci sono ora nel vaso? {r}: {n} − {k} = {r}.",
               узнал="{X} ha saputo che quel giorno al palazzo sono venuti {n} {ПОСn} e il giorno dopo {k}. quanti {ПОСмн} sono venuti in tutto? {s}: {n} + {k} = {s}.",
               сели_вышли="sull'autobus c'erano {n} {ДЕТn}. alla fermata sono saliti {k} {ДЕТмн} mentre alcuni sono scesi. ora ci sono {s} {ДЕТмн} sull'autobus. quanti {ДЕТмн} sono scesi? {k2}: {n} + {k} − {s} = {k2}.",
               сыграл="{X} ha giocato {n} {ИГРn} lunedì e {k} {ИГРмн} martedì. quante {ИГРмн} ha giocato {X} in tutto? {s}: {n} + {k} = {s}.",
               потратил="{X} ha dedicato {n} {ЧАСn} all'inglese e {k} {ЧАСмн} al cinese. quante {ЧАСмн} ha dedicato {X} in tutto? un totale di {s} {ЧАСмн}: {n} + {k} = {s}.",
               список="ogni giorno {X} dedica {n} {ЧАСn} all'inglese, {k} {ЧАСмн} al cinese e {m} {ЧАСмн} allo spagnolo. quante {ЧАСмн} dedica {X} in tutto? {t}: {n} + {k} + {m} = {t}.",
               коробка="{X} ha ricevuto una scatola di {n} {МЕЛn} e una scatola di {k} {МЕЛмн}. quanti {МЕЛмн} ha {X}? {s}: {n} + {k} = {s}.",
               главы="un libro ha 2 capitoli. il primo capitolo è di {n} {СТРn} e il secondo di {k} {СТРмн}. quante {СТРмн} ha il libro in tutto? {s}: {n} + {k} = {s}.",
               две_клаузы="{X} aveva {n} {ИГРn} e {Y} aveva {k} {ИГРмн}. quante {ИГРмн} avevano insieme? {s}: {n} + {k} = {s}.",
               сделал="{X} ha fatto {n} {ОТЖn} e {k} {СКРk}. quante {ОТЖмн} ha fatto {X}? {n}. quanti esercizi in tutto? {s}: {n} + {k} = {s}.",
               вещи3="{X} ha {n} {ФИГn}, {k} {МЕЛk} e {m} {ИГРm}. quante cose ha {X} in tutto? {t}: {n} + {k} + {m} = {t}.",
               продал="{X} aveva {n} {РОЗn}. ha venduto {k} {РОЗk}. quante {РОЗмн} ha ancora? {r}: {n} − {k} = {r}.",
               присоединились="c'erano {n} {ДЕТn} nel cortile. si sono uniti a loro altri {k} {ДЕТk}. quanti {ДЕТмн} ci sono ora nel cortile? {s}: {n} + {k} = {s}.",
               жили="{n} {ЖИЛn} abitavano nella casa. {k} {ЖИЛk} si sono trasferiti. quanti {ЖИЛмн} abitano ora nella casa? {r}: {n} − {k} = {r}.",
               предложил="{X} ha proposto {n} {ФИГn} per lo scaffale. {Y} ne ha tolte {k}. quante {ФИГмн} restano? {r}: {n} − {k} = {r}.",
               в_школе="in una scuola ci sono {n} {ДЕВn} e {k} {МАЛk}. quanti alunni ci sono nella scuola? {s}: {n} + {k} = {s}.",
               рецепт="la ricetta richiede {n} {ЧАШn} di farina e {k} {ЧАШk} di zucchero. quante tazze di farina in più rispetto allo zucchero richiede? {r}: {n} − {k} = {r}.",
               теперь_список="{X} aveva {n} {ФИГn}. ha ricevuto anche {k} {МЕЛk}. ora ha {n} {ФИГn} e {k} {МЕЛk}. quante cose ha in tutto? {s}: {n} + {k} = {s}.",
               добавил="{X} aveva {n} {ПРИЛn} sul telefono. ha aggiunto {k} nuove {ПРИЛмн}. quante {ПРИЛмн} ha adesso? {s}: {n} + {k} = {s}."),
    "pt": dict(
               больше_чем="{X} fez {n} {ОТЖn}. {Y} fez mais {k} {ОТЖмн} do que {X}. quantas {ОТЖмн} fez {Y}? {s}: {n} + {k} = {s}.",
               меньше_чем="{X} fez {n} {ОТЖn}. {Y} fez menos {k} {ОТЖмн} do que {X}. quantas {ОТЖмн} fez {Y}? {r}: {n} − {k} = {r}.",
               добавил_на_полку="{X} tinha {n} {ФИГn} na prateleira. mais tarde acrescentou mais {k} {ФИГмн} à prateleira. quantos {ФИГмн} há agora na prateleira? {s}: {n} + {k} = {s}.",
               выбросил="{X} encontrou {n} {КРЫШn} no parque e deitou fora {k} velhas. quantas {КРЫШмн} a mais encontrou do que deitou fora? {r}: {n} − {k} = {r}.",
               выбросил_розы="havia {n} {РОЗn} na jarra. {X} deitou fora {k} {РОЗмн} da jarra. quantas {РОЗмн} há agora na jarra? {r}: {n} − {k} = {r}.",
               узнал="{X} soube que nesse dia vieram {n} {ПОСn} ao palácio e no dia seguinte {k}. quantos {ПОСмн} vieram no total? {s}: {n} + {k} = {s}.",
               сели_вышли="havia {n} {ДЕТn} no autocarro. na paragem entraram {k} {ДЕТмн} enquanto algumas saíram. agora há {s} {ДЕТмн} no autocarro. quantas {ДЕТмн} saíram? {k2}: {n} + {k} − {s} = {k2}.",
               сыграл="{X} jogou {n} {ИГРn} na segunda-feira e {k} {ИГРмн} na terça-feira. quantos {ИГРмн} jogou {X} no total? {s}: {n} + {k} = {s}.",
               потратил="{X} gastou {n} {ЧАСn} com inglês e {k} {ЧАСмн} com chinês. quantas {ЧАСмн} gastou {X} no total? um total de {s} {ЧАСмн}: {n} + {k} = {s}.",
               список="todos os dias {X} gasta {n} {ЧАСn} com inglês, {k} {ЧАСмн} com chinês e {m} {ЧАСмн} com espanhol. quantas {ЧАСмн} gasta {X} no total? {t}: {n} + {k} + {m} = {t}.",
               коробка="{X} recebeu uma caixa com {n} {МЕЛn} e uma caixa com {k} {МЕЛмн}. quantos {МЕЛмн} tem {X}? {s}: {n} + {k} = {s}.",
               главы="um livro tem 2 capítulos. o primeiro capítulo tem {n} {СТРn} e o segundo {k} {СТРмн}. quantas {СТРмн} tem o livro no total? {s}: {n} + {k} = {s}.",
               две_клаузы="{X} tinha {n} {ИГРn} e {Y} tinha {k} {ИГРмн}. quantos {ИГРмн} tinham juntos? {s}: {n} + {k} = {s}.",
               сделал="{X} fez {n} {ОТЖn} e {k} {СКРk}. quantas {ОТЖмн} fez {X}? {n}. quantos exercícios no total? {s}: {n} + {k} = {s}.",
               вещи3="{X} tem {n} {ФИГn}, {k} {МЕЛk} e {m} {ИГРm}. quantas coisas tem {X} ao todo? {t}: {n} + {k} + {m} = {t}.",
               продал="{X} tinha {n} {РОЗn}. vendeu {k} {РОЗk}. quantas {РОЗмн} lhe restam? {r}: {n} − {k} = {r}.",
               присоединились="havia {n} {ДЕТn} no recreio. juntaram-se a elas mais {k} {ДЕТk}. quantas {ДЕТмн} há agora no recreio? {s}: {n} + {k} = {s}.",
               жили="{n} {ЖИЛn} moravam na casa. {k} {ЖИЛk} mudaram-se. quantos {ЖИЛмн} moram agora na casa? {r}: {n} − {k} = {r}.",
               предложил="{X} propôs {n} {ФИГn} para a prateleira. {Y} retirou {k} deles. quantos {ФИГмн} restam? {r}: {n} − {k} = {r}.",
               в_школе="numa escola há {n} {ДЕВn} e {k} {МАЛk}. quantos alunos há na escola? {s}: {n} + {k} = {s}.",
               рецепт="a receita pede {n} {ЧАШn} de farinha e {k} {ЧАШk} de açúcar. quantas chávenas de farinha a mais do que de açúcar pede? {r}: {n} − {k} = {r}.",
               теперь_список="{X} tinha {n} {ФИГn}. também recebeu {k} {МЕЛk}. agora tem {n} {ФИГn} e {k} {МЕЛk}. quantas coisas tem ao todo? {s}: {n} + {k} = {s}.",
               добавил="{X} tinha {n} {ПРИЛn} no telemóvel. adicionou {k} {ПРИЛмн} novas. quantas {ПРИЛмн} tem agora? {s}: {n} + {k} = {s}."),
    "nl": dict(
               больше_чем="{X} deed {n} {ОТЖn}. {Y} deed {k} {ОТЖмн} meer dan {X}. hoeveel {ОТЖмн} deed {Y}? {s}: {n} + {k} = {s}.",
               меньше_чем="{X} deed {n} {ОТЖn}. {Y} deed {k} {ОТЖмн} minder dan {X}. hoeveel {ОТЖмн} deed {Y}? {r}: {n} − {k} = {r}.",
               добавил_на_полку="{X} had {n} {ФИГn} op de plank. later zette {он} er {k} {ФИГмн} bij op de plank. hoeveel {ФИГмн} staan er nu op de plank? {s}: {n} + {k} = {s}.",
               выбросил="{X} vond {n} {КРЫШn} in het park en gooide er {k} oude weg. hoeveel {КРЫШмн} meer vond {он} dan {он} weggooide? {r}: {n} − {k} = {r}.",
               выбросил_розы="er stonden {n} {РОЗn} in de vaas. {X} gooide {k} {РОЗмн} uit de vaas weg. hoeveel {РОЗмн} staan er nu in de vaas? {r}: {n} − {k} = {r}.",
               узнал="{X} hoorde dat er die dag {n} {ПОСn} naar het paleis kwamen en de dag erna {k}. hoeveel {ПОСмн} kwamen er in totaal? {s}: {n} + {k} = {s}.",
               сели_вышли="er zaten {n} {ДЕТn} in de bus. bij de halte stapten {k} {ДЕТмн} in terwijl er een paar uitstapten. nu zitten er {s} {ДЕТмн} in de bus. hoeveel {ДЕТмн} stapten uit? {k2}: {n} + {k} − {s} = {k2}.",
               сыграл="{X} speelde {n} {ИГРn} op maandag en {k} {ИГРмн} op dinsdag. hoeveel {ИГРмн} speelde {X} in totaal? {s}: {n} + {k} = {s}.",
               потратил="{X} besteedde {n} {ЧАСn} aan Engels en {k} {ЧАСмн} aan Chinees. hoeveel {ЧАСмн} besteedde {X} in totaal? in totaal {s} {ЧАСмн}: {n} + {k} = {s}.",
               список="elke dag besteedt {X} {n} {ЧАСn} aan Engels, {k} {ЧАСмн} aan Chinees en {m} {ЧАСмн} aan Spaans. hoeveel {ЧАСмн} besteedt {X} in totaal? {t}: {n} + {k} + {m} = {t}.",
               коробка="{X} kreeg een doos met {n} {МЕЛn} en een doos met {k} {МЕЛмн}. hoeveel {МЕЛмн} heeft {X}? {s}: {n} + {k} = {s}.",
               главы="een boek heeft 2 hoofdstukken. het eerste hoofdstuk is {n} {СТРn} lang en het tweede {k} {СТРмн}. hoeveel {СТРмн} heeft het boek in totaal? {s}: {n} + {k} = {s}.",
               две_клаузы="{X} had {n} {ИГРn} en {Y} had {k} {ИГРмн}. hoeveel {ИГРмн} hadden ze samen? {s}: {n} + {k} = {s}.",
               сделал="{X} deed {n} {ОТЖn} en {k} {СКРk}. hoeveel {ОТЖмн} deed {X}? {n}. hoeveel oefeningen in totaal? {s}: {n} + {k} = {s}.",
               вещи3="{X} heeft {n} {ФИГn}, {k} {МЕЛk} en {m} {ИГРm}. hoeveel dingen heeft {X} in totaal? {t}: {n} + {k} + {m} = {t}.",
               продал="{X} had {n} {РОЗn}. {он} verkocht {k} {РОЗk}. hoeveel {РОЗмн} heeft {он} nog? {r}: {n} − {k} = {r}.",
               присоединились="er waren {n} {ДЕТn} op de speelplaats. er kwamen nog {k} {ДЕТk} bij. hoeveel {ДЕТмн} zijn er nu op de speelplaats? {s}: {n} + {k} = {s}.",
               жили="er woonden {n} {ЖИЛn} in het huis. {k} {ЖИЛk} verhuisden. hoeveel {ЖИЛмн} wonen er nu in het huis? {r}: {n} − {k} = {r}.",
               предложил="{X} stelde {n} {ФИГn} voor de plank voor. {Y} haalde er {k} weg. hoeveel {ФИГмн} blijven er over? {r}: {n} − {k} = {r}.",
               в_школе="op een school zijn er {n} {ДЕВn} en {k} {МАЛk}. hoeveel leerlingen zijn er op de school? {s}: {n} + {k} = {s}.",
               рецепт="het recept vraagt om {n} {ЧАШn} bloem en {k} {ЧАШk} suiker. hoeveel kopjes bloem meer dan suiker vraagt het? {r}: {n} − {k} = {r}.",
               теперь_список="{X} had {n} {ФИГn}. {он} kreeg ook {k} {МЕЛk}. nu heeft {он} {n} {ФИГn} en {k} {МЕЛk}. hoeveel dingen heeft {он} in totaal? {s}: {n} + {k} = {s}.",
               добавил="{X} had {n} {ПРИЛn} op de telefoon. {он} voegde {k} nieuwe {ПРИЛмн} toe. hoeveel {ПРИЛмн} heeft {он} nu? {s}: {n} + {k} = {s}."),
    "pl": dict(
               больше_чем="{X} zrobił{а} {n} {ОТЖn}. {Y} zrobił{аY} o {k} {ОТЖk} więcej niż {X}. ile {ОТЖмн} zrobił{аY} {Y}? {s}: {n} + {k} = {s}.",
               меньше_чем="{X} zrobił{а} {n} {ОТЖn}. {Y} zrobił{аY} o {k} {ОТЖk} mniej niż {X}. ile {ОТЖмн} zrobił{аY} {Y}? {r}: {n} − {k} = {r}.",
               добавил_на_полку="{X} miał{а} {n} {ФИГn} na półce. potem dodał{а} na półkę jeszcze {k} {ФИГk}. ile {ФИГмн} jest teraz na półce? {s}: {n} + {k} = {s}.",
               выбросил="{X} znalazł{а} w parku {n} {КРЫШn}, a {k} starych wyrzucił{а}. o ile więcej {КРЫШмн} znalazł{а}, niż wyrzucił{а}? {r}: {n} − {k} = {r}.",
               выбросил_розы="w wazonie było {n} {РОЗn}. {X} wyrzucił{а} z wazonu {k} {РОЗk}. ile {РОЗмн} jest teraz w wazonie? {r}: {n} − {k} = {r}.",
               узнал="{X} dowiedział{а} się, że tego dnia do pałacu przyszło {n} {ПОСn}, a następnego {k}. ilu {ПОСмн} przyszło razem? {s}: {n} + {k} = {s}.",
               сели_вышли="w autobusie było {n} {ДЕТn}. na przystanku wsiadło {k} {ДЕТk}, a kilkoro wysiadło. teraz w autobusie jest {s} {ДЕТs}. ile {ДЕТмн} wysiadło? {k2}: {n} + {k} − {s} = {k2}.",
               сыграл="{X} zagrał{а} {n} {ИГРn} w poniedziałek i {k} {ИГРk} we wtorek. ile {ИГРмн} zagrał{а} {X} razem? {s}: {n} + {k} = {s}.",
               потратил="{X} spędził{а} {n} {ЧАСn} na angielskim i {k} {ЧАСk} na chińskim. ile {ЧАСмн} spędził{а} {X} razem? razem {s} {ЧАСs}: {n} + {k} = {s}.",
               список="codziennie {X} spędza {n} {ЧАСn} na angielskim, {k} {ЧАСk} na chińskim i {m} {ЧАСm} na hiszpańskim. ile {ЧАСмн} spędza {X} razem? {t}: {n} + {k} + {m} = {t}.",
               коробка="{X} dostał{а} pudełko z {n} {МЕЛпр} i pudełko z {k} {МЕЛпр}. ile {МЕЛмн} ma {X}? {s}: {n} + {k} = {s}.",
               главы="książka ma 2 rozdziały. pierwszy rozdział ma {n} {СТРn}, a drugi {k} {СТРk}. ile {СТРмн} ma książka razem? {s}: {n} + {k} = {s}.",
               две_клаузы="{X} miał{а} {n} {ИГРn}, a {Y} miał{аY} {k} {ИГРk}. ile {ИГРмн} mieli razem? {s}: {n} + {k} = {s}.",
               сделал="{X} zrobił{а} {n} {ОТЖn} i {k} {СКРk}. ile {ОТЖмн} zrobił{а} {X}? {n}. ile ćwiczeń razem? {s}: {n} + {k} = {s}.",
               вещи3="{X} ma {n} {ФИГn}, {k} {МЕЛk} i {m} {ИГРm}. ile rzeczy ma {X} razem? {t}: {n} + {k} + {m} = {t}.",
               продал="{X} miał{а} {n} {РОЗn}. sprzedał{а} {k} {РОЗk}. ile {РОЗмн} ma teraz? {r}: {n} − {k} = {r}.",
               присоединились="na placu zabaw było {n} {ДЕТn}. dołączyło do nich jeszcze {k} {ДЕТk}. ile {ДЕТмн} jest teraz na placu zabaw? {s}: {n} + {k} = {s}.",
               жили="w domu mieszkało {n} {ЖИЛn}. {k} z nich się wyprowadziło. ile {ЖИЛмн} mieszka teraz w domu? {r}: {n} − {k} = {r}.",
               предложил="{X} zaproponował{а} na półkę {n} {ФИГn}. {Y} odrzucił{аY} {k} z nich. ile {ФИГмн} zostało? {r}: {n} − {k} = {r}.",
               в_школе="w szkole jest {n} {МАЛn} i {k} {ДЕВk}. ilu uczniów jest w szkole? {s}: {n} + {k} = {s}.",
               рецепт="przepis podaje {n} {ЧАШn} mąki i {k} {ЧАШk} cukru. o ile {ЧАШмн} mąki więcej niż cukru podaje przepis? {r}: {n} − {k} = {r}.",
               теперь_список="{X} miał{а} {n} {ФИГn}. dostał{а} też {k} {МЕЛk}. teraz ma {n} {ФИГn} i {k} {МЕЛk}. ile rzeczy ma razem? {s}: {n} + {k} = {s}.",
               добавил="{X} miał{а} {n} {ПРИЛn} w telefonie. dodał{а} {k} {НОВk} {ПРИЛk}. ile {ПРИЛмн} ma teraz? {s}: {n} + {k} = {s}."),
})
# ЦЕЛЬ ТРАТЫ — ОБЪЯВЛЕННЫЙ РЯД, А НЕ ЛИТЕРАЛ (07.09, вечер; заказ holon, купленный ключом).
#
# Ядро, кованное на тринадцатой точке, ответило «14» на вопрос «Ваня потратил 14 часов на
# английский и 9 часов на китайский. сколько часов потратил Ваня всего?». Первая догадка —
# «свод не показывает координации» — ложна: координированных держаний с вопросом об итоге в
# своде 410 русских и 250 английских, и дом `action_pages` их пишет.
#
# Перепись по РОДУ назвала настоящую беду: род «потратил {n} единиц на A и {k} единиц на B»
# имел ВОСЕМЬ страниц, и все восемь — об одной и той же паре целей.
#
#     РОД, СТОЯЩИЙ РОВНО НА ПОЛУ КВОРУМА (LAW³ = 8), ОБЪЯВЛЕН, НО НЕ КУПЛЕН.
#     РОД, У КОТОРОГО МЕНЯЮТСЯ ЧИСЛА И ИМЕНА, НО НИКОГДА ЦЕЛИ, УЧИТ ИДИОМЕ, А НЕ ЗАКОНУ.
#
# Цели объявлены С УПРАВЛЕНИЕМ ПРЕДЛОГА, а не одними именами: «на математику» (винительный),
# «na matematyce» (местный), «alla matematica», «a la música», «sur l'histoire» с артиклем и
# элизией. Это тот же закон, что уже стои́т в этом доме для товара после предлога, — ПАДЕЖ И
# АРТИКЛЬ ИЗ ЧИСЛА НЕ ВЫВОДЯТСЯ и потому объявляются.
ЦЕЛИ_ТРАТЫ = {
    "en": (("on english", "on chinese"), ("on music", "on history"),
           ("on chemistry", "on geography"), ("on physics", "on biology")),
    "ru": (("на английский", "на китайский"), ("на музыку", "на историю"),
           ("на химию", "на географию"), ("на физику", "на биологию")),
    "de": (("mit Englisch", "mit Chinesisch"), ("mit Musik", "mit Geschichte"),
           ("mit Chemie", "mit Erdkunde"), ("mit Physik", "mit Biologie")),
    "fr": (("sur l'anglais", "sur le chinois"), ("sur la musique", "sur l'histoire"),
           ("sur la chimie", "sur la géographie"), ("sur la physique", "sur la biologie")),
    "es": (("al inglés", "al chino"), ("a la música", "a la historia"),
           ("a la química", "a la geografía"), ("a la física", "a la biología")),
    "it": (("all'inglese", "al cinese"), ("alla musica", "alla storia"),
           ("alla chimica", "alla geografia"), ("alla fisica", "alla biologia")),
    "pt": (("com inglês", "com chinês"), ("com música", "com história"),
           ("com química", "com geografia"), ("com física", "com biologia")),
    "nl": (("aan Engels", "aan Chinees"), ("aan muziek", "aan geschiedenis"),
           ("aan scheikunde", "aan aardrijkskunde"), ("aan natuurkunde", "aan biologie")),
    "pl": (("na angielskim", "na chińskim"), ("na muzyce", "na historii"),
           ("na chemii", "na geografii"), ("na fizyce", "na biologii")),
}
for _яз, _ряд in ЦЕЛИ_ТРАТЫ.items():
    _рамка = РАМКИ_АКТОВ[_яз]["потратил"]
    _перв_a, _перв_b = _ряд[0]
    assert _перв_a in _рамка and _перв_b in _рамка, (_яз, _рамка)
    РАМКИ_АКТОВ[_яз]["потратил"] = tuple(
        _рамка.replace(_перв_a, _a).replace(_перв_b, _b) for _a, _b in _ряд)


ФОРМЫ_АКТОВ = tuple(РАМКИ_АКТОВ["en"])
ЧИСЛА_АКТОВ = ((12, 5, 4), (35, 3, 9), (20, 8, 6), (15, 7, 2), (30, 12, 10), (9, 4, 3), (18, 11, 5), (24, 15, 7))
# THE ADJECTIVE BENDS WITH THE COUNT FORM where the language bends it (BESEDA-11, pl: «dodała 5
# nowych aplikacji» — the seven other languages carry «new» as one word inside the frame)
НОВЫЕ = {"pl": ("nową", "nowe", "nowych")}


def _товар_форма(язык, ключ, c):
    return _счёт(ТОВАРЫ_АКТОВ[язык][ключ], c, язык)


def _поля_акта(язык, i, j, n, k, m):
    X, Y = _лицо(язык, i), _лицо(язык, j)
    if Y[0] == X[0]:
        Y = _лицо(язык, j + 1)
    мест = МЕСТОИМЕНИЯ[язык][X[1]]
    местY = МЕСТОИМЕНИЯ[язык][Y[1]]
    п = dict(X=X[0], Xр=X[2], Y=Y[0], Yр=Y[2], он=мест["он"], Он=мест["он"], него=мест["него"], аY_он=местY["он"],
             а=(("a" if X[1] == "f" else "") if язык == "pl" else A._а(язык, X[1])), аY=(("a" if Y[1] == "f" else "") if язык == "pl" else A._а(язык, Y[1])),
             # ЦЕЛАЯ ФОРМА, А НЕ ОСНОВА С СУФФИКСОМ: «нашёл» + «а» даёт «нашёла» — слова,
             # которого в русском нет. Дыра суффикса верна для тринадцати основ дома и лжёт
             # о четырнадцатой, и потому глагол с БЕГЛОЙ ГЛАСНОЙ берётся у дома языка целиком
             # (`rugram.прошедшее`), а не собирается здесь.
             НАШЁЛ=(_RU.прошедшее("нашёл", X[1]) if язык == "ru" else ""),
             n=n, k=k, m=m, r=n - k, s=n + k, t=n + k + m, k2=k - (n + k - (n + k - k)) if False else k)
    # «сели_вышли»: сели k, вышли k2, теперь s = n + k − k2 — вышло меньше, чем село
    п["k2"] = max(1, k // 2); п["s_бус"] = n + k - п["k2"]
    if язык in НОВЫЕ:
        п["НОВk"] = _счёт(НОВЫЕ[язык], k, язык)
    for дыра, ключ in _ТОВАР_ПО_ДЫРЕ.items():
        if ключ not in ТОВАРЫ_АКТОВ[язык]:
            continue
        п[дыра + "n"] = _товар_форма(язык, ключ, n); п[дыра + "k"] = _товар_форма(язык, ключ, k)
        п[дыра + "m"] = _товар_форма(язык, ключ, m); п[дыра + "s"] = _товар_форма(язык, ключ, n + k)
        п[дыра + "мн"] = ТОВАРЫ_АКТОВ[язык][ключ][-1]
        если = ПРИ_ПРЕДЛОГЕ.get(язык, {}).get(ключ)
        if если is not None:
            п[дыра + "пр"] = если
    return п


def страница_акта(язык, форма, i, j, n, k, m=4, имя=False, вариант=0, середина=False):
    р = РАМКИ_АКТОВ[язык][форма]
    if середина:
        р = близнец_середины(язык, р)
        if р is None:
            return None
        п = _поля_акта(язык, i, j, n, k, m)
        if форма == "сели_вышли":
            п = dict(п, s=п["s_бус"], ДЕТs=_товар_форма(язык, "дети", п["s_бус"]))
        return р.format(**п)
    if isinstance(р, tuple):
        # РАМКА-РЯД: несколько поверхностей одного рода (цели траты). Близнеца ряду не
        # берём — тот же закон, что у базовых рамок выше.
        if имя:
            return None
        р = р[вариант % len(р)]
    elif вариант:
        return None
    if имя:
        р = близнец(р)
        if р is None:
            return None
    п = _поля_акта(язык, i, j, n, k, m)
    if форма == "сели_вышли":
        п = dict(п, s=п["s_бус"], ДЕТs=_товар_форма(язык, "дети", п["s_бус"]))
    return р.format(**п)


def _показы_актов():
    вон = {}
    for язык in РАМКИ_АКТОВ:
        лиц = len(A.ЛИЦА[язык])
        for форма in ФОРМЫ_АКТОВ:
            if форма not in РАМКИ_АКТОВ[язык]:
                continue
            р = РАМКИ_АКТОВ[язык][форма]
            вариантов = len(р) if isinstance(р, tuple) else 1
            for q, (n, k, m) in enumerate(ЧИСЛА_АКТОВ):
                for вариант in range(вариантов):
                    с = страница_акта(язык, форма, q % лиц, (q * 3 + 1) % лиц, n, k, m,
                                      вариант=вариант)
                    if с:
                        вон[с] = (язык, форма)
                с = страница_акта(язык, форма, q % лиц, (q * 3 + 1) % лиц, n, k, m, имя=True)
                if с:
                    вон[с] = (язык, форма)
                с = страница_акта(язык, форма, q % лиц, (q * 3 + 1) % лиц, n, k, m,
                                  середина=True)
                if с:
                    вон[с] = (язык, форма)
    return вон


ПОКАЗЫ.update(_показы_актов())


def _образцы_актов():
    вон = []
    alt = lambda слова: "(?:" + "|".join(re.escape(с) for с in sorted(set(с for с in слова if с), key=lambda с: (-len(с), с))) + ")"
    for язык, рамки in РАМКИ_АКТОВ.items():
        имена = [_лицо(язык, i)[0] for i in range(len(A.ЛИЦА[язык]))]; род = [л[2] for л in A.ЛИЦА[язык]]
        мест = [v for г in МЕСТОИМЕНИЯ[язык].values() for v in г.values()]
        дыры = {"X": alt(имена), "Y": alt(имена), "Xр": alt(род), "Yр": alt(род), "он": alt(мест), "Он": alt(мест), "него": alt(мест), "аY_он": alt(мест),
                "а": "(?:а|о|и|a|)", "аY": "(?:а|о|и|a|)", "НАШЁЛ": "(?:нашёл|нашла)", "n": r"(\d+)", "k": r"(\d+)", "m": r"(\d+)", "r": r"(\d+)", "s": r"(\d+)", "t": r"(\d+)", "k2": r"(\d+)"}
        if язык in НОВЫЕ:
            дыры["НОВk"] = alt(НОВЫЕ[язык])
        for дыра, ключ in _ТОВАР_ПО_ДЫРЕ.items():
            if ключ not in ТОВАРЫ_АКТОВ[язык]:
                continue
            формы = alt(ТОВАРЫ_АКТОВ[язык][ключ])
            for суффикс in ("n", "k", "m", "s", "мн"):
                дыры[дыра + суффикс] = формы
            если = ПРИ_ПРЕДЛОГЕ.get(язык, {}).get(ключ)
            if если is not None:
                # НЕ alt(всех форм): падежная ячейка не принимает счётной
                дыры[дыра + "пр"] = alt((если,))
        for форма, рамка in рамки.items():
            поверхности = (list(рамка) if isinstance(рамка, tuple)
                           else [рамка, близнец(рамка), близнец_середины(язык, рамка)])
            for р in поверхности:
                if р is None:
                    continue
                куски = [дыры[к[1:-1]] if к.startswith("{") else re.escape(к) for к in re.split(r"(\{[^}]+\})", р)]
                вон.append((re.compile("^" + "".join(куски) + "$"), язык, форма))
    return вон


ОБРАЗЦЫ.extend(_образцы_актов())
ЛЕДЖЕР3 = re.compile(r"(\d+) \+ (\d+) ([+−]) (\d+) = (\d+)\.$")
ЛЕДЖЕР = re.compile(r"(\d+) ([+−×÷]) (\d+) = (\d+)\.$")
ШАГ = re.compile(r"(\d+) ([+−×÷]) (\d+) = (\d+)")


def _значение(a, з, b):
    if з == "+": return a + b
    if з == "−": return a - b
    if з == "×": return a * b
    return a // b if b and a % b == 0 else None       # ÷ only where it divides


def _знаменатели(язык, текст):
    """The denominators of the declared share words in the story: «a third» lends the 3."""
    return {q for q, слово in ДОЛИ.get(язык, {}).items() if слово in текст}
ВОПРОС_КОНЕЦ = re.compile(r"[?？] ")


def _имена_в(язык, текст):
    формы = set()
    for i in range(len(A.ЛИЦА[язык])):
        л = _лицо(язык, i)
        формы |= {л[0], л[2], л[0].split(" ", 1)[-1]}
        if язык == "ru":
            формы.add(_дательный(л[0]) or "")
        elif язык == "pl":
            формы.add(ДАТЕЛЬНЫЙ_PL.get(л[0], л[0]))
        elif язык == "pt":
            формы.add(_дательный_pt(л).split(" ", 1)[-1])
    return {с for с in re.findall(r"[^\W\d_]+", текст) if с in формы}


def _шаги(с, язык=None):
    """A CHAIN OF STEPS (the long surface of one genus, 05.09): every step recomputed, every
    next step fed by the previous result, the total the last result, the first inputs the
    story's numbers. None — the line is not a chain (fewer than two steps)."""
    шаги = ШАГ.findall(с)
    if len(шаги) < 2:
        return None
    хвост = с[ШАГ.search(с).start():]
    голова = с[:ШАГ.search(с).start()]
    числа = {int(x) for x in re.findall(r"\d+", голова)} | _знаменатели(язык, голова)
    прежний = None
    for a, з, b, v in шаги:
        a, b, v = int(a), int(b), int(v)
        if v != _значение(a, з, b):
            return False
        if прежний is None:
            if a not in числа or b not in числа:
                return False
        elif a != прежний or b not in числа:
            return False
        прежний = v
    итог = re.findall(r"\d+", хвост)
    return bool(итог) and int(итог[-1]) == прежний


def _судить_образцом(строка):
    """(судимо, истинно): a page of the house, or a line of its frame whose ledger does not hold."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма in ОБРАЗЦЫ:
        if образ.match(с):
            цепь = _шаги(с, язык)
            if цепь is not None:
                return True, цепь
            if not ЛЕДЖЕР.search(с):
                # ANSWER WITHOUT A LEDGER: the fact's own number, or the holding «I do not
                # know» when the question carries no number — the numbers of the answer must
                # be the story's, and a story without numbers allows none in the answer
                м = list(ВОПРОС_КОНЕЦ.finditer(с))
                if not м:
                    return True, False
                история, ответ = с[:м[-1].start()], с[м[-1].end():]
                в_истории = {int(x) for x in re.findall(r"\d+", история)}
                в_ответе = [int(x) for x in re.findall(r"\d+", ответ)]
                if not в_истории:
                    # the holding names the same bearer as the question — a refusal about
                    # another person is a lie, not a holding
                    return True, (not в_ответе) and _имена_в(язык, история) == _имена_в(язык, ответ)
                if форма in ОТВЕТ_ПЕРВОГО:
                    return True, в_ответе == [int(x) for x in re.findall(r"\d+", история)][:1]
                return True, bool(в_ответе) and all(x in в_истории for x in в_ответе)
            м3 = ЛЕДЖЕР3.search(с)
            if м3:
                a, b, з, c_, v = int(м3.group(1)), int(м3.group(2)), м3.group(3), int(м3.group(4)), int(м3.group(5))
                верно = v == (a + b + c_ if з == "+" else a + b - c_)
                числа = [int(x) for x in re.findall(r"\d+", с[:м3.start()])]
                return True, верно and a in числа and b in числа and c_ in числа
            м = ЛЕДЖЕР.search(с)
            if not м:
                return True, False
            a, з, b, v = int(м.group(1)), м.group(2), int(м.group(3)), int(м.group(4))
            верно = v == _значение(a, з, b)
            # the numbers of the STORY (before the question mark) must be the numbers of the
            # ledger — a declared share word lends its denominator («a third» → 3), and a share's
            # divisor must be that denominator; the ANSWER (between the question mark and the
            # ledger) states the ledger's result — «6: 12 − 5 = 7» is a lie of the answer, not of
            # the equation (05.09: the first judge read the answer's number as a story number)
            вопросы = list(ВОПРОС_КОНЕЦ.finditer(с[:м.start()]))
            история = с[:вопросы[-1].start()] if вопросы else с[:м.start()]
            ответ = с[вопросы[-1].end():м.start()] if вопросы else ""
            знаменатели = _знаменатели(язык, история)
            числа = [int(x) for x in re.findall(r"\d+", история)] + list(знаменатели)
            заявлено = [int(x) for x in re.findall(r"\d+", ответ)]
            if заявлено and заявлено[-1] != v:
                return True, False
            if з == "÷" and знаменатели and b not in знаменатели:
                return True, False
            return True, верно and a in числа and b in числа
    return False, False


def _самопроверка():
    for показ, (язык, форма) in ПОКАЗЫ.items():
        assert судить(показ) == (True, True), (язык, форма, показ)
    мутанты = 0
    for язык in РАМКИ:
        for форма in ФОРМЫ:
            if форма not in РАМКИ[язык] or язык in ОБЪЯВЛЕННЫЕ_ПРОПУСКИ.get(форма, ()):
                continue
            р = РАМКИ[язык][форма]
            # ТРЕТЬЯ ПОВЕРХНОСТЬ ПРОВЕРЯЕТСЯ ТАК ЖЕ, КАК ПЕРВЫЕ ДВЕ: близнец середины есть
            # страница дома, а не украшение, и мутант её леджера обязан быть пойман.
            с = страница(язык, форма, 0, 1, 0, 12, 5, середина=True)
            if с and re.search(r"= (\d+)\.$", с):
                assert судить(с) == (True, True), с
                битая = re.sub(r"= (\d+)\.$", lambda м: f"= {int(м.group(1)) + 1}.", с)
                assert судить(битая) == (True, False), битая
                мутанты += 1
            for вариант in range(len(р) if isinstance(р, tuple) else 1):
                с = страница(язык, форма, 0, 1, 0, 12, 5, вариант)
                if not re.search(r"= (\d+)\.$", с):
                    continue          # без леджера в конце — свой мутант ниже (шаги, факт, удержание)
                битая = re.sub(r"= (\d+)\.$", lambda м: f"= {int(м.group(1)) + 1}.", с)
                assert судить(битая) == (True, False), битая
                мутанты += 1
    for язык in РАМКИ_АКТОВ:
        for форма in ФОРМЫ_АКТОВ:
            if форма not in РАМКИ_АКТОВ[язык]:
                continue
            р = РАМКИ_АКТОВ[язык][форма]
            пробы = ([(False, в) for в in range(len(р))] if isinstance(р, tuple)
                     else [(False, 0), (True, 0)])
            for имя, вариант in пробы:
                с = страница_акта(язык, форма, 0, 1, 12, 5, имя=имя, вариант=вариант)
                if с is None:
                    continue
                битая = re.sub(r"= (\d+)\.$", lambda м: f"= {int(м.group(1)) + 1}.", с)
                assert судить(битая) == (True, False), битая
                мутанты += 1
            с = страница_акта(язык, форма, 0, 1, 12, 5, середина=True)
            if с and re.search(r"= (\d+)\.$", с):
                assert судить(с) == (True, True), с
                битая = re.sub(r"= (\d+)\.$", lambda м: f"= {int(м.group(1)) + 1}.", с)
                assert судить(битая) == (True, False), битая
                мутанты += 1
    # МУТАНТЫ СКРЫТОГО КОЛИЧЕСТВА (три рода): леджер не сходится — общим ножом выше; ответ не равен
    # итогу леджера; СЛОВО СКРЫТОГО КОЛИЧЕСТВА, ЗАМЕНЁННОЕ ЧИСЛОМ, делает строку строкой другого
    # рода — дом её не признаёт вовсе (дыра принимает лишь объявленное слово, и это не придирка
    # к письму: названное число не есть скрытое, и учить по нему счёту нечему).
    for язык in РАМКИ:
        for форма in ("пришло_скрыто", "ушло_скрыто", "часть_из_них", "взял_скрыто"):
            с = страница(язык, форма, 0, 1, 0, 12, 5)
            assert судить(с) == (True, True), с
            заявлен = re.sub(r"([?？]\s*)(\d+)(\s*:)", lambda м: f"{м.group(1)}{int(м.group(2)) + 1}{м.group(3)}", с, 1)
            assert судить(заявлен) == (True, False), заявлен
            for ключ, дыра in (("несколько", "СК"), ("часть", "СКЧ")):
                слово = _слова_скрытого(язык, ключ)
                если = next((w for w in слово if w in с), None)
                if если is None:
                    continue
                числом = с.replace(если, "4", 1)
                assert судить(числом) == (False, False), числом
                мутанты += 1
            мутанты += 1
    # мутанты двух длин и удержания: шаг с неверным итогом, разорванная связь шагов, число в удержании,
    # чужое число в факте
    for язык in РАМКИ:
        for цепная in ("три_шаги", "доля_не"):
            ш = страница(язык, цепная, 0, 1, 0, 12, 5)
            assert судить(ш) == (True, True), ш
            assert судить(re.sub(r"= (\d+)\. (\S+ 2)", lambda м: f"= {int(м.group(1)) + 1}. {м.group(2)}", ш, 1)) == (True, False), ш
            мутанты += 1
        ф = страница(язык, "факт", 0, 1, 0, 12, 5)
        assert судить(ф) == (True, True), ф
        assert судить(ф[:-3] + "13.") == (True, False), ф
        б0, б1 = страница(язык, "без_данных", 0, 1, 0, 12, 5), страница(язык, "без_данных", 1, 2, 0, 12, 5)
        assert судить(б0) == (True, True), б0
        подмена = б0[:б0.index("? ") + 2] + б1[б1.index("? ") + 2:]     # удержание о другом носителе
        assert судить(подмена) == (True, False), подмена
        мутанты += 4
    # мутанты поссессивов: ответ числом родителя, чужое число у родителя имени
    for язык in РАМКИ:
        е = страница(язык, "его_вещи", 0, 1, 0, 12, 5)
        assert судить(е) == (True, True), е
        голова, ответ = е.rsplit("? ", 1)
        assert судить(голова + "? " + ответ.replace("12", "5")) == (True, False), е
        и = страница(язык, "имя_с_с", 0, 1, 0, 12, 5)
        assert судить(и) == (True, True), и
        голова, ответ = и.rsplit("? ", 1)
        assert судить(голова + "? " + ответ.replace("5", "6")) == (True, False), и
        мутанты += 2
    for форма in ("некоторые", "итог", "из_них", "если", "время", "кому", "единица", "товар", "три_шаги", "факт", "без_данных", "вместе_их", "купил_у_него", "оставив_ему", "имя_с_с"):
        print("  ", страница("en", форма, 0, 1, 0, 12, 5))
    for форма in ("некоторые", "из_них", "кому", "товар"):
        print("  ", страница("ru", форма, 2, 3, 1, 12, 5))
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(РАМКИ)}, форм {len(ФОРМЫ)})")




_РОДЫ_ЛИЦ = {л[0]: л[1] for л in A.ЛИЦА.get("ru", ()) if len(л) > 1 and л[1] in ("m", "f")}

import closedworld as _зк  # noqa: E402 — закон замкнутого мира читается после сборки показов
_СКЕЛЕТЫ_ЗНАКА = _зк.скелеты_знака(ПОКАЗЫ)


def судить(строка):
    """(судимо, истинно) — с ЗАКОНОМ ЗНАКА поверх образца.

    ЗНАК ДЕЙСТВИЯ СУДИТСЯ ЗАКОНОМ ЗАМКНУТОГО МИРА, А НЕ ДЫРОЙ В КАЖДОЙ РАМКЕ: строка,
    становящаяся ИСТИННОЙ при замене одного знака, есть строка ЭТОГО дома с испорченным
    знаком (М-489). Прежде такая строка получала НЕМОТУ, и палата брала истину у суда
    арифметики — у соседа (М-131).
    """
    вердикт = _судить_образцом(строка)
    if вердикт[0] is False and _зк.ложь_по_знаку(
            строка, _СКЕЛЕТЫ_ЗНАКА, ПОКАЗЫ, _судить_образцом):
        return True, False
    # РОД ПРОШЕДШЕГО ЕСТЬ РОД ЛИЦА, А НЕ БУКВА ДЫРЫ: окончание глагола стои́т в образце дырой
    # «(?:а|о|и|a|)», принимающей любую букву, и вердикт о нём не спрашивал — «Анна отдал»
    # проходило образцом и звалось ИСТИНОЙ. Закон берётся у дома языка, лица — у себя.
    if вердикт[:2] == (True, True) and _RUG.не_по_роду(строка, _РОДЫ_ЛИЦ):
        return True, False
    # СВЯЗКА ЕСТЬ ЗНАК СТРОКИ: подмена «jest»↔«są» делает страницу ЛОЖНОЙ, а не чужой.
    #
    # ДВА ПУТИ, И ОБА НУЖНЫ. Дыра рамки принимает обе формы (иначе образец не покрыл бы всех
    # чисел), а дыры этого дома НЕ ИМЕНОВАНЫ — вердикт читает группы по счёту, и вставить
    # проверку внутрь него значило бы сдвинуть их все. Оттого связка судится ПОСЛЕ вердикта,
    # чтением строки у дома языка: страница, чья связка не по полосе, ложна, что бы ни сказал
    # о ней образец. Закон замкнутого мира ловит второй случай — когда образец не совпал вовсе.
    if вердикт[:2] == (True, True) and _PL.не_по_полосе(строка):
        return True, False
    if вердикт[0] is False and _зк.ложь_по_связке(строка, ПОКАЗЫ, _PL.ГРУППЫ_СВЯЗКИ):
        return True, False
    return вердикт
if __name__ == "__main__":
    _самопроверка()
