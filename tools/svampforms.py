#!/usr/bin/env python3
"""THE HOUSE OF STORY SHAPES — eight constructions that a census of the live public band
named mute (d5, 06.09), each a form with its recomputing court, in nine languages.

The census named what no frame of the corpus held: (1) oblique pronouns as pronouns
(«gave some of them away», «gave him some»); (2) place held by a bare «were» — closed in the
house of action measure; (3) the hidden quantity «some» and the heads of the total («in all»,
«altogether», «in total», «now has N left»); (4) the words of time order («at first … then»);
(5) the hypothetical act in the question («if she gives away k, how many will she have?»);
(6) transfer with a direction («gave k to him» = «gave him k», «took k from her»); (7) the
unit before the number («$ 3») — English only, declared; (8) goods outside the lexicon.
Names and things are the house of action pages' (tools/actionpages.py), pronouns are declared
here by gender; every answer carries its ledger, and the court recomputes it. The world is
CLOSED.

REWRITTEN 23.09 BY THE OWNER'S WORD: a public band is an instrument, never a source. The
scenes of the acts block (`ТОВАРЫ_АКТОВ`, `РАМКИ_АКТОВ`) had been written reading the band's
own stories; now each construction stands in a scene of our own — oaks and birches planted,
ducks on a pond, the cars of a train, stamps collected on two days — with the equation of the
answer in the page. The construction stays, the band's text, build and numbers go; the leak
court (`scripts/bench_leak.py`, three measures) must name none of this house's pages.

    python3 tools/svampforms.py    # self-check with mutants
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import frgram as _fr  # noqa: E402 — французская элизия: один закон, два читателя
import plural as _plural  # noqa: E402 — английский артикль по звуку
import plgram as _PL  # noqa: E402 — закон польской связки: один закон, один читатель
import rugram as _RU  # noqa: E402 — закон русского прошедшего: один закон, один читатель
import romgram  # noqa: E402 — пары романского вопросного слова: один дом закона
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
ТОВАРЫ = {"en": ((("jar of cherry jam", "jars of cherry jam"), ("jar of plum jam", "jars of plum jam"), ("jar of jam", "jars of jam")),
                 (("pack of red cards", "packs of red cards"), ("pack of blue cards", "packs of blue cards"), ("pack of cards", "packs of cards")),
                 (("box of apples", "boxes of apples"), ("box of pears", "boxes of pears"), ("box of fruit", "boxes of fruit"))),
          "ru": ((("банка вишнёвого варенья", "банки вишнёвого варенья", "банок вишнёвого варенья"), ("банка сливового варенья", "банки сливового варенья", "банок сливового варенья"), ("банка варенья", "банки варенья", "банок варенья")),
                 (("пачка красных карт", "пачки красных карт", "пачек красных карт"), ("пачка синих карт", "пачки синих карт", "пачек синих карт"), ("пачка карт", "пачки карт", "пачек карт")),
                 (("коробка яблок", "коробки яблок", "коробок яблок"), ("коробка груш", "коробки груш", "коробок груш"), ("коробка фруктов", "коробки фруктов", "коробок фруктов"))),
          "de": ((("Glas Kirschmarmelade", "Gläser Kirschmarmelade"), ("Glas Pflaumenmarmelade", "Gläser Pflaumenmarmelade"), ("Glas Marmelade", "Gläser Marmelade")),
                 (("Kiste Äpfel", "Kisten Äpfel"), ("Kiste Birnen", "Kisten Birnen"), ("Kiste Obst", "Kisten Obst"))),
          "fr": ((("pot de confiture de cerises", "pots de confiture de cerises"), ("pot de confiture de prunes", "pots de confiture de prunes"), ("pot de confiture", "pots de confiture")),
                 (("caisse de pommes", "caisses de pommes"), ("caisse de poires", "caisses de poires"), ("caisse de fruits", "caisses de fruits"))),
          "es": ((("tarro de mermelada de cereza", "tarros de mermelada de cereza"), ("tarro de mermelada de ciruela", "tarros de mermelada de ciruela"), ("tarro de mermelada", "tarros de mermelada")),
                 (("caja de manzanas", "cajas de manzanas"), ("caja de peras", "cajas de peras"), ("caja de fruta", "cajas de fruta"))),
          "it": ((("vasetto di marmellata di ciliegie", "vasetti di marmellata di ciliegie"), ("vasetto di marmellata di prugne", "vasetti di marmellata di prugne"), ("vasetto di marmellata", "vasetti di marmellata")),
                 (("cassa di mele", "casse di mele"), ("cassa di pere", "casse di pere"), ("cassa di frutta", "casse di frutta"))),
          "pt": ((("frasco de doce de cereja", "frascos de doce de cereja"), ("frasco de doce de ameixa", "frascos de doce de ameixa"), ("frasco de doce", "frascos de doce")),
                 (("caixa de maçãs", "caixas de maçãs"), ("caixa de peras", "caixas de peras"), ("caixa de fruta", "caixas de fruta"))),
          "nl": ((("pot kersenjam", "potten kersenjam"), ("pot pruimenjam", "potten pruimenjam"), ("pot jam", "potten jam")),
                 (("kist appels", "kisten appels"), ("kist peren", "kisten peren"), ("kist fruit", "kisten fruit"))),
          "pl": ((("słoik dżemu wiśniowego", "słoiki dżemu wiśniowego", "słoików dżemu wiśniowego"), ("słoik dżemu śliwkowego", "słoiki dżemu śliwkowego", "słoików dżemu śliwkowego"), ("słoik dżemu", "słoiki dżemu", "słoików dżemu")),
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
        единица="{Т1а} costs $ {n}. how much do {k} {Тмн} cost? $ {v}: {k} × {n} = {v}.",
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
        единица="1 {Т1} стоит {n} ₽. сколько стоят {k} {Тk}? {v} ₽: {k} × {n} = {v}.",
        осталось="у {Xр} было {n} {Тn}. {Он} отдал{а} {k}. сколько у {него} теперь? теперь у {него} осталось {r}: {n} − {k} = {r}.",
        из_них="у {Xр} было {n} {Тn}. {Он} отдал{а} {k} из них {Yд}. сколько {Тмн} у {него} теперь? {r}: {n} − {k} = {r}.",
        ему="у {Xр} было {n} {Тn}. {Y} дал{аY} {ему} ещё {k}. сколько {Тмн} у {него} теперь? {s}: {n} + {k} = {s}.",
        три="{X} собрал{а} {n} {Тn}. {X} купил{а} ещё {k}. {он} потерял{а} {m} из них. сколько {Тмн} у {Xр} осталось? {t}: {n} + {k} − {m} = {t}.",
        три_шаги="{X} собрал{а} {n} {Тn}. {X} купил{а} ещё {k}. {он} потерял{а} {m} из них. сколько {Тмн} у {Xр} осталось? шаг 1: {n} + {k} = {s}. шаг 2: {s} − {m} = {t}. итог: {t}.",
        владеет="у {Xр} есть {n} {Тn}. сколько {Тмн} имеет {X}? {X} имеет {n} {Тn}.",
        владеет_после="у {Xр} есть {n} {Тn}. {Он} отдаёт {k}. сколько {Тмн} имеет {X} теперь? {X} имеет {r} {Тr}: {n} − {k} = {r}.",
        доля="у {Xр} {n} {Тn}. {ДОЛЯ} из них — {ЦП}. сколько из них {ЦП}? {r}: {n} ÷ {q} = {r}.",
        доля_не="у {Xр} {n} {Тn}. {ДОЛЯ} из них — {ЦП}. сколько из них не {ЦП}? шаг 1: {n} ÷ {q} = {r}. шаг 2: {n} − {r} = {d}. итог: {d}.",
        возраст_имя="{X_д} {n} {Гn}. сколько лет будет {X_д} через {k} {Гk}? {X_д} будет {s} {Гs}: {n} + {k} = {s}.",
        его_вещи="у {Xр} {n} {Тn}. у {Рр} {k} {Тk}. сколько {Тмн} у {Xр}? у {Xр} {n} {Тn}.",
        вместе_их="у {Xр} {n} {Тn}. у {Рр} {k} {Тk}. сколько {Тмн} у них вместе? вместе у них {s} {Тs}: {n} + {k} = {s}.",
        дал_ему="у {Xр} было {n} {Тn}. {Y} дал{аY} {ему} {k} {Твk}. сколько {Тмн} у {Xр} теперь? у {Xр} {s} {Тs}: {n} + {k} = {s}.",
        купил_у_него="у {Xр} было {n} {Тn}. у {Yр} тоже были. {Он} купил{а} у {негоY} {k} {Твk}. сколько {Тмн} у {Xр} теперь? у {Xр} {s} {Тs}: {n} + {k} = {s}.",
        оставив_ему="{X} отдал{а} {k} {Твk} {Yд}, и у {него} осталось {r} {Тr}. сколько {Тмн} было у {Xр} сначала? у {Xр} было {n} {Тn}: {k} + {r} = {n}.",
        имя_с_с="у {Рб} {Xде} {k} {Тk}. сколько {Тмн} у {Рб} {Xде}? у {Рб} {Xде} {k} {Тk}.",
        факт="у {Xр} {n} {Тn}. сколько {Тмн} у {Xр}? {n}.",
        без_данных="сколько {Тмн} у {Xр}? не знаю: сколько {Тмн} у {Xр}, не сказано.",
        собрал_у="{X} собрал{а} {n} {Тn}. {Он} потерял{а} {k} из них. сколько {Тмн} у {Xр} осталось? {r}: {n} − {k} = {r}.",
        потерял="у {Xр} было {n} {Тn}. {Он} потерял{а} {k} из них. сколько {Тмн} у {него} осталось? {r}: {n} − {k} = {r}.",
        купил_ещё="у {Xр} было {n} {Тn}. {Он} купил{а} ещё {k}. сколько {Тмн} у {него} теперь? {s}: {n} + {k} = {s}.",
        если="у {Xр} {n} {Тn}. если {он} отдаст {k}, сколько у {него} останется? {r}: {n} − {k} = {r}.",
        если_придут="в коробке {n} {Тn}. если положить ещё {k}, сколько там будет? {s}: {n} + {k} = {s}.",
        время="{В1} у {Xр} было {n} {Тn}. {В2} {он} получил{а} ещё {k}. сколько {Тмн} у {него} теперь? {s}: {n} + {k} = {s}.",
        кому="у {Xр} было {n} {Тn}. {Он} отдал{а} {k} {Твk} {Yд}. сколько {Тмн} у {Xр} теперь? {r}: {n} − {k} = {r}.",
        у_него="у {Xр} было {n} {Тn}. {Y} взял{аY} у {него} {k} {Твk}. сколько {Тмн} у {Xр} теперь? {r}: {n} − {k} = {r}.",
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
# РОД ГОЛОВЫ ТОВАРА — У ХОЗЯИНА ТАБЛИЦЫ ТОВАРОВ (24.09, прибор [ДВУРОДОЕ ИМЯ]). Рамка товара писала
# вопросное слово буквой — «¿cuántas», «quante», «quantas», — и правота её держалась прежним товаром
# женского рода. Перепись 23.09 дала банки варенья («tarros», «vasetti», «frascos» — мужского), и
# страница сказала «¿cuántas tarros»: двадцать семь лжей рода на трёх языках. Ныне слово берётся
# дверью `romgram.по_слову` по роду, объявленному здесь для каждой головы; голова без рода роняет
# ковку, а не пишет ложь.
РОД_ТОВАРА = {
    "es": {"tarros": "m", "cajas": "f"},
    "it": {"vasetti": "m", "casse": "f"},
    "pt": {"frascos": "m", "caixas": "f"},
}
ЦВЕТА_М = {"es": ("rojos", "azules"), "it": ("rossi", "blu"), "pt": ("vermelhos", "azuis")}


def _ряд_по_роду(язык):
    """Указатели вещей языка, разобранные на мужские и женские."""
    м, ж = [], []
    for т_ in range(len(A.ЯЗЫКИ[язык]["вещи"])):
        свой = РОД_ВЕЩЕЙ.get(язык, {}).get(A._вещь(язык, т_, 5), "f")
        (м if свой == "m" else ж).append(т_)
    return м, ж


РЯД_ПО_РОДУ = {язык: _ряд_по_роду(язык) for язык in РОД_ВЕЩЕЙ}

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

# ПАРА ВОПРОСНОГО СЛОВА СВЕРЯЕТСЯ С ДОМОМ ЯЗЫКА (12.09): «кск», «quante», «quantas» суть та же
# пара, какую объявляет `tools/romgram.py` для всех, кто её пишет. Два списка, разойдясь молча,
# дали бы своду два разных «cuántas».
#
#     ДВА ОБЪЯВЛЕНИЯ ОДНОГО ЗАКОНА ЖИВУТ, ПОКА ИХ СВЕРЯЮТ; НЕСВЕРЯЕМЫЕ — РАСХОДЯТСЯ.
for _язык, _пара in romgram.ПАРЫ.items():
    assert _пара in РОДОВЫЕ.get(_язык, {}).values(), (_язык, _пара)
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
        итог_всего="{X} hat {a} {Ц1} {Тмн} und {b} {Ц2} {Тмн}. wie viele {Тмн} hat {X}? insgesamt {s} {Тs}: {a} + {b} = {s}.",
        единица="1 {Т1} kostet {n} €. wie viel kosten {k} {Тk}? {v} €: {k} × {n} = {v}.",
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
        итог_всего="{X} a {a} {Тмн} {Ц1} et {b} {Тмн} {Ц2}. combien de {Тмн} {X} a-t-{он} ? au total {s} {Тs} : {a} + {b} = {s}.",
        единица="1 {Т1} coûte {n} €. combien coûtent {k} {Тk} ? {v} € : {k} × {n} = {v}.",
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
        товар="{X} tiene {a} {Г1a} y {b} {Г2b}. ¿{Г3кск} {Г3мн} tiene en total? {s} {Г3s}: {a} + {b} = {s}.",
        пришло_скрыто="{X} tenía {n} {Тn}. recibió {СК} {Тмн} más. ahora tiene {s} {Тs}. ¿{кск} {Тмн} recibió? {k}: {s} − {n} = {k}.",
        ушло_скрыто="{X} tenía {n} {Тn}. perdió {СК} {Тмн}. ahora tiene {r} {Тr}. ¿{кск} {Тмн} perdió? {k}: {n} − {r} = {k}.",
        часть_из_них="{X} tenía {n} {Тn}. vendió {СКЧ}. ahora tiene {r} {Тr}. ¿{кск} {Тмн} vendió? {k}: {n} − {r} = {k}.",
        взял_скрыто="{X} tenía {n} {Тn}. {Y} {ему} quitó {СК} {Тмн}. ahora tiene {r} {Тr}. ¿{кск} {Тмн} quitó {Y}? {k}: {n} − {r} = {k}.",
        некоторые="{X} tenía {n} {Тn}. dio {algunas}. ahora le quedan {r} {Тr}. ¿{кск} {Тмн} dio? {k}: {n} − {r} = {k}.",
        итог="{X} tiene {a} {Тмн} {Ц1} y {b} {Тмн} {Ц2}. ¿{кск} {Тмн} tiene {X} {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        итог_всего="{X} tiene {a} {Тмн} {Ц1} y {b} {Тмн} {Ц2}. ¿{кск} {Тмн} tiene {X}? en total {s} {Тs}: {a} + {b} = {s}.",
        единица="1 {Т1} cuesta {n} €. ¿cuánto cuestan {k} {Тk}? {v} €: {k} × {n} = {v}.",
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
        товар="{X} ha {a} {Г1a} e {b} {Г2b}. {Г3кск} {Г3мн} ha in tutto? {s} {Г3s}: {a} + {b} = {s}.",
        пришло_скрыто="{X} aveva {n} {Тn}. ha ricevuto {СК} {Тмн} in più. ora ha {s} {Тs}. {quante} {Тмн} ha ricevuto? {k}: {s} − {n} = {k}.",
        ушло_скрыто="{X} aveva {n} {Тn}. ha perso {СК} {Тмн}. ora ha {r} {Тr}. {quante} {Тмн} ha perso? {k}: {n} − {r} = {k}.",
        часть_из_них="{X} aveva {n} {Тn}. ha venduto {СКЧ}. ora ha {r} {Тr}. {quante} {Тмн} ha venduto? {k}: {n} − {r} = {k}.",
        взял_скрыто="{X} aveva {n} {Тn}. {Y} {ему} ha preso {СК} {Тмн}. ora ha {r} {Тr}. {quante} {Тмн} ha preso {Y}? {k}: {n} − {r} = {k}.",
        некоторые="{X} aveva {n} {Тn}. ne ha {date} {alcune}. ora {ему} restano {r} {Тr}. {quante} {Тмн} ha dato? {k}: {n} − {r} = {k}.",
        итог="{X} ha {a} {Тмн} {Ц1} e {b} {Тмн} {Ц2}. {quante} {Тмн} ha {X} {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        итог_всего="{X} ha {a} {Тмн} {Ц1} e {b} {Тмн} {Ц2}. {quante} {Тмн} ha {X}? in tutto {s} {Тs}: {a} + {b} = {s}.",
        единица="1 {Т1} costa {n} €. quanto costano {k} {Тk}? {v} €: {k} × {n} = {v}.",
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
        товар="{X} tem {a} {Г1a} e {b} {Г2b}. {Г3кск} {Г3мн} tem no total? {s} {Г3s}: {a} + {b} = {s}.",
        пришло_скрыто="{X} tinha {n} {Тn}. recebeu mais {СК} {Тмн}. agora tem {s} {Тs}. {quantas} {Тмн} recebeu? {k}: {s} − {n} = {k}.",
        ушло_скрыто="{X} tinha {n} {Тn}. perdeu {СК} {Тмн}. agora tem {r} {Тr}. {quantas} {Тмн} perdeu? {k}: {n} − {r} = {k}.",
        часть_из_них="{X} tinha {n} {Тn}. vendeu {СКЧ}. agora tem {r} {Тr}. {quantas} {Тмн} vendeu? {k}: {n} − {r} = {k}.",
        взял_скрыто="{X} tinha {n} {Тn}. {Y} tirou-{ему} {СК} {Тмн}. agora tem {r} {Тr}. {quantas} {Тмн} tirou {Y}? {k}: {n} − {r} = {k}.",
        некоторые="{X} tinha {n} {Тn}. deu {algumas}. agora tem {r} {Тr}. {quantas} {Тмн} deu? {k}: {n} − {r} = {k}.",
        итог="{X} tem {a} {Тмн} {Ц1} e {b} {Тмн} {Ц2}. {quantas} {Тмн} tem {X} {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        итог_всего="{X} tem {a} {Тмн} {Ц1} e {b} {Тмн} {Ц2}. {quantas} {Тмн} tem {X}? no total {s} {Тs}: {a} + {b} = {s}.",
        единица="1 {Т1} custa {n} €. quanto custam {k} {Тk}? {v} €: {k} × {n} = {v}.",
        из_них="{X} tinha {n} {Тn}. deu {k} {delas} {Yд}. {quantas} {Тмн} tem agora? {r}: {n} − {k} = {r}.",
        три="{X} apanhou {n} {Тn}. {X} comprou mais {k}. {он} perdeu {m}. que quantidade de {Тмн} resta {X_д}? {t}: {n} + {k} − {m} = {t}.",
        три_шаги="{X} apanhou {n} {Тn}. {X} comprou mais {k}. {он} perdeu {m}. que quantidade de {Тмн} resta {X_д}? passo 1: {n} + {k} = {s}. passo 2: {s} − {m} = {t}. total: {t}.",
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
        собрал_у="{X} apanhou {n} {Тn}. perdeu {k}. que quantidade de {Тмн} resta {X_д}? {r}: {n} − {k} = {r}.",
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
        итог_всего="{X} heeft {a} {Ц1} {Тмн} en {b} {Ц2} {Тмн}. hoeveel {Тмн} heeft {X}? in totaal {s} {Тs}: {a} + {b} = {s}.",
        единица="1 {Т1} kost {n} €. hoeveel kosten {k} {Тk}? {v} €: {k} × {n} = {v}.",
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
        итог_всего="{X} ma {a} {Ц1} {Тмн} i {b} {Ц2} {Тмн}. ile {Тмн} ma {X}? łącznie {s} {Тs}: {a} + {b} = {s}.",
        единица="1 {Т1} kosztuje {n} zł. ile kosztują {k} {Тk}? {v} zł: {k} × {n} = {v}.",
        из_них="{X} miał{а} {n} {Тn}. oddał{а} {k} z nich {Yд}. ile {Тмн} ma teraz? {r}: {n} − {k} = {r}.",
        три="{X} zebrał{а} {n} {Тn}. {X} kupił{а} jeszcze {k}. {он} zgubił{а} {m} z nich. ile {Тмн} zostało {X_д}? {t}: {n} + {k} − {m} = {t}.",
        три_шаги="{X} zebrał{а} {n} {Тn}. {X} kupił{а} jeszcze {k}. {он} zgubił{а} {m} z nich. ile {Тмн} zostało {X_д}? krok 1: {n} + {k} = {s}. krok 2: {s} − {m} = {t}. razem: {t}.",
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
        собрал_у="{X} zebrał{а} {n} {Тn}. zgubił{а} {k} z nich. ile {Тмн} zostało {X_д}? {r}: {n} − {k} = {r}.",
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
                       # ПРОПУСК СНЯТ (15.09): русская рамка цены написана, и прибор
                       # щербатости назвал это объявление ЧАСТИЧНЫМ — оно называло одним
                       # русским то, что молчало на восьми языках из девяти.

                       # «possess» — второй английский глагол владения; у других языков один
                       "владеет2": frozenset({"ru", "de", "fr", "es", "it", "pt", "nl", "pl"}),
                       # hold / keep — английские глаголы держания (holon: own/hold/keep становятся
                       # держащими голосом страниц — ответ полным предложением с леджером ±)
                       "держит": frozenset({"ru", "de", "fr", "es", "it", "pt", "nl", "pl"}),
                       "хранит": frozenset({"ru", "de", "fr", "es", "it", "pt", "nl", "pl"})}
# TWO HOLDERS, ONE BEARER ASKED: the answer repeats the FIRST holder's number, not the parent's
ОТВЕТ_ПЕРВОГО = frozenset({"его_вещи"})
# ДЕВЯТАЯ ПАРА ПРИБАВЛЕНА 16.09 РАДИ ЗАКОНА МАССЫ, И ПРИБАВЛЕНА ОДНА НА ВЕСЬ ДОМ. Прибор
# [ОБЕЩАНИЕ ДОМА] назвал род `владеет2` недодавшим: восемь страниц при законе девяти. Род
# этот ОДНОЯЗЫЧЕН по объявлению («possess» — второй английский глагол владения, у прочих
# языков один), и масса его равна ЧИСЛУ ПАР таблицы — восьми.
#
#     РОД, ЧЬЯ МАССА ЕСТЬ ЧИСЛО ПАР ТАБЛИЦЫ, ЛЕЧИТСЯ НЕ ПРИПИСКОЙ ЕМУ СТРАНИЦЫ, А ПАРОЙ:
#     приписка дала бы девятую страницу ОДНОМУ роду, пара даёт её ВСЯКОМУ.
#
# ПАРА ВЗЯТА СВОБОДНОЙ ОТ ТРЁХ ТАБЛИЦ РАЗОМ, И ЭТО НЕ ПЕДАНТСТВО, А ДВЕ ПОЙМАННЫЕ ПОПЫТКИ.
# Сперва взято 36 — и дом сравнения (`cmpframes`) упал: 36 стои́т в его двенадцати парах,
# объявленных ВНЕ таблиц SVAMP. Затем 42 — и он упал снова, по той же причине.
#
#     ЧИСЛО, СВОБОДНОЕ В ОДНОЙ ТАБЛИЦЕ, НЕ СВОБОДНО ВО ВСЕХ. Таблиц, объявивших себя
#     «вне дома SVAMP», в корпусе три — ряд ключа, ряд актов и пары дома сравнения, — и
#     всякая проверяет себя утверждением при ввозе. Потому прибавка пары к дому есть
#     правка ТРЁХ объявлений, и падает она громко, что и хорошо.
#
# Пара (48, 21) свободна от всех трёх.
ЧИСЛА = ((12, 5), (20, 8), (15, 6), (9, 4), (30, 12), (25, 7), (18, 11), (40, 15), (48, 21))
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
    X_д = (_дательный(X[0]) if язык == "ru" else ДАТЕЛЬНЫЙ_PL.get(X[0], X[0]) if язык == "pl"
          else _дательный_pt(X) if язык == "pt" else X[0])
    п = dict(X=X[0], Xр=X[2], Y=Y[0], Yд=Yд, X_д=X_д,
             он=м["он"], Он=м["он"], него=м["него"], ему=м["ему"],
             а=(("a" if X[1] == "f" else "") if язык == "pl" else A._а(язык, X[1])), аY=(("a" if Y[1] == "f" else "") if язык == "pl" else A._а(язык, Y[1])),
             # ЦЕЛАЯ ФОРМА, А НЕ ОСНОВА С СУФФИКСОМ: «нашёл» + «а» даёт «нашёла» — слова,
             # которого в русском нет. Дыра суффикса верна для тринадцати основ дома и лжёт
             # о четырнадцатой, и потому глагол с БЕГЛОЙ ГЛАСНОЙ берётся у дома языка целиком
             # (`rugram.прошедшее`), а не собирается здесь.
             НАШЁЛ=(_RU.прошедшее("нашёл", X[1]) if язык == "ru" else ""),
             n=n, k=k, r=n - k, s=n + k, a=n, b=k, m=(k + 1) // 2, t=n + k - (k + 1) // 2,
             Тn=вещь(n), Тk=вещь(k), Тr=вещь(n - k), Тs=вещь(n + k), Тмн=вещь(5), Т1=вещь(1), Тm=вещь((k + 1) // 2),
             # ДОПОЛНЕНИЕ АКТА — В ВИНИТЕЛЬНОМ ПРИ ЧИСЛЕ (24.09, строка 37 реестра): «отдала 21 монету Пете»
             Твk=(_RU.винительный_при_числе(A.ЯЗЫКИ[язык]["вещи"][Т], k) if язык == "ru" else вещь(k)),
             # АНГЛИЙСКИЙ АРТИКЛЬ ГНЁТСЯ ЗВУКОМ СЛОВА, А НЕ БУКВОЙ РАМКИ: «a apple» ×8
             Т1а=(_plural.with_article(вещь(1)) if язык == "en" else вещь(1)))
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
ПАДЕЖ_НОСИТЕЛЯ = {"он": "X", "Он": "X", "него": "Xр", "ему": "X_д",
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


def _страница_сырая(язык, форма, i, j, Т, n, k, вариант=0, имя=False, середина=False):
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
        # ФОРМА ВЕЩИ ИДЁТ ЗА ЧИСЛОМ, А ЧИСЛО ЗДЕСЬ ПОДМЕНЯЕТСЯ (15.09). Пара цены берётся из
        # своего ряда и кладётся поверх `k`, а `Тk` был сочтён выше по СТАРОМУ числу — и
        # английская рамка того не замечала, ибо берёт `Тмн`, одну на все числа. Славянская
        # рамка замечает сразу: «сколько стоят 4 монет» вместо «4 монеты».
        #
        #     ЧИСЛО, ПОДМЕНЁННОЕ ПОСЛЕ СЧЁТА ФОРМЫ, ОСТАВЛЯЕТ ФОРМУ ОТ ПРЕЖНЕГО ЧИСЛА. Это
        #     видно лишь тому языку, что гнёт вещь счётом, и потому молчало, пока рамка была
        #     одна.
        п.update(n=n_, k=k_, v=n_ * k_, Тмн=A._вещь(язык, Т, 5), Тk=A._вещь(язык, Т, k_))
    if форма == "товар":
        г1, г2, г3 = ТОВАРЫ[язык][вариант % len(ТОВАРЫ[язык])]
        п.update(Г1a=_счёт(г1, n, язык), Г2b=_счёт(г2, k, язык), Г3мн=г3[-1], Г3s=_счёт(г3, n + k, язык))
        if romgram.гнётся(язык):
            п["Г3кск"] = romgram.по_слову(язык, г3[-1].split()[0], РОД_ТОВАРА[язык])
    return р.format(**п)



def страница(язык, форма, i, j, Т, n, k, вариант=0, имя=False, середина=False):
    """Готовая страница с ФРАНЦУЗСКОЙ ЭЛИЗИЕЙ (12.09).

    Рамка подставляет слово в дыру, и «que» + «une» даёт «que une» — по-французски
    ОШИБКУ, а не вариант. Сокращение приходится делать ПОСЛЕ подстановки, и закон
    его живёт в доме языка (`frgram.элизия`), а не переписывается здесь.

        РАМКА, СОБРАННАЯ ИЗ ЦЕЛЫХ СЛОВ, НЕ ЗНАЕТ, ЧТО ДВА ИЗ НИХ СЛИВАЮТСЯ.
    """
    готовая = _страница_сырая(язык, форма, i, j, Т, n, k, вариант, имя, середина)
    # ОБЁРТКА СПРАШИВАЕТ, ЕСТЬ ЛИ ЧТО ОБЁРТЫВАТЬ: рамка иных родов возвращает
    # пустоту, и элизия падала на первом же таком ответе.
    return _fr.элизия(готовая) if язык == "fr" and готовая else готовая

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


# ШОВ РОДА ВЕЩИ (12.09). Вопросное слово трёх языков согласуется с родом вещи («cuántos» —
# «cuántas», «quantos» — «quantas», «quanti» — «quante»), а вещь достаётся числу ОДНИМ
# указателем: `Т = q % вещей` при восьми числах и восьми вещах даёт каждой вещи ровно одну
# страницу рамки. Оттого вопросное слово живёт столько раз, сколько вещей ЕГО рода в таблице, —
# а таблицы перекошены: португальская держит две мужские вещи из восьми, испанская четыре.
# Прибор «ключ без опоры» назвал оба рода поимённо: «quantos tem» 2 страницы, «cuántos tiene» 4
# при законе опоры LAW³ = 8.
#
#     ЧИСЛО, ПОКАЗАННОЕ ОДНОЙ ВЕЩЬЮ, ПОКАЗЫВАЕТСЯ И ВЕЩЬЮ ДРУГОГО РОДА — И ТОГДА СОГЛАСУЕМОЕ
#     СЛОВО ЖИВЁТ РОВНО СТОЛЬКО РАЗ, СКОЛЬКО ЧИСЕЛ В РЯДУ, КАКОВА БЫ НИ БЫЛА ТАБЛИЦА ВЕЩЕЙ.
#
# Это та же ДВУСТОРОННОСТЬ, что объявлена в `declarations/BOTH-SIDES.md`: согласование есть
# ловушка, и ловушка показывается с обеих сторон. Прежняя страница остаётся неизменной — рядом
# с нею встаёт вторая, с вещью другого рода на том же числе; где язык рода не гнёт (русский,
# немецкий, английский), шва нет и ряд идёт как шёл.
_ДЫРА_РАМКИ = re.compile(r"\{([^}]+)\}")


def _согласует_род(язык, форма):
    """True, если рамка языка гнёт хоть одно своё слово по роду вещи."""
    родовые = РОДОВЫЕ.get(язык)
    if not родовые:
        return False
    р = РАМКИ[язык].get(форма)
    тексты = р if isinstance(р, tuple) else (р,)
    return any(д in родовые for текст in тексты if текст for д in _ДЫРА_РАМКИ.findall(текст))


СОГЛАСУЮТ_РОД = {(язык, форма) for язык in РАМКИ for форма in РАМКИ[язык]
                 if _согласует_род(язык, форма)}


def _вещи_шага(язык, форма, q, Т):
    """Вещи, какими рамка показывает q-е число: своя — и, при согласовании, вещь другого рода."""
    if (язык, форма) not in СОГЛАСУЮТ_РОД:
        return (Т,)
    м, ж = РЯД_ПО_РОДУ[язык]
    чужой = ж if Т in м else м
    return (Т, чужой[q % len(чужой)]) if чужой else (Т,)


def _показы():
    вон = {}
    for язык in РАМКИ:
        лиц = len(A.ЛИЦА[язык]); вещей = len(A.ЯЗЫКИ[язык]["вещи"])
        for форма in ФОРМЫ:
            if форма not in РАМКИ[язык]:
                continue
            ряд = ЧИСЛА_ДОЛИ if форма in ("доля", "доля_не") else ЧИСЛА
            for q, (n, k) in enumerate(ряд):
                i = q % лиц; j = (q * 3 + 1) % лиц
                варианты = 3 if форма in ("итог", "время", "товар", "доля", "доля_не") else (4 if форма == "единица" else 1)
                if isinstance(РАМКИ[язык][форма], tuple):
                    варианты = max(варианты, len(РАМКИ[язык][форма]))
                for Т in _вещи_шага(язык, форма, q, q % вещей):
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
        вещи_вин = ([_RU.винительный_при_числе(A.ЯЗЫКИ[язык]["вещи"][Т], c)
                     for Т in range(len(A.ЯЗЫКИ[язык]["вещи"])) for c in (1, 2, 5)]
                    if язык == "ru" else вещи)
        мест = [v for г in МЕСТОИМЕНИЯ[язык].values() for v in г.values()]
        товары = [ф for ряд in ТОВАРЫ.get(язык, ()) for г in ряд for ф in г]
        дыры = {"X": alt(имена), "Y": alt(имена), "Xр": alt(род), "Yд": alt(дат), "X_д": alt(дат), "он": alt(мест), "Он": alt(мест), "него": alt(мест), "ему": alt(мест),
                "а": "(?:а|о|и|a|)", "аY": "(?:а|о|и|a|)", "НАШЁЛ": "(?:нашёл|нашла)", "n": r"(\d+)", "k": r"(\d+)", "r": r"(\d+)", "s": r"(\d+)", "a": r"(\d+)", "b": r"(\d+)", "v": r"(\d+)",
                "m": r"(\d+)", "t": r"(\d+)", "q": r"(\d+)", "d": r"(\d+)",
                "ДОЛЯ": alt(ДОЛИ[язык].values()), "ЦП": alt(ЦВЕТ_ПРЕД[язык]),
                # ДЫРА СКРЫТОГО КОЛИЧЕСТВА ПРИНИМАЕТ ТОЛЬКО ОБЪЯВЛЕННОЕ СЛОВО: строка с числом на
                # этом месте есть строка другого рода, и дом её не признаёт (суд самопроверки).
                "СК": alt(_слова_скрытого(язык, "несколько")), "СКЧ": alt(_слова_скрытого(язык, "часть")),
                "Гn": alt(_годы(язык)), "Гk": alt(_годы(язык)), "Гs": alt(_годы(язык)),
                "Тn": alt(вещи), "Тk": alt(вещи), "Тr": alt(вещи), "Тs": alt(вещи), "Тмн": alt(вещи), "Т1": alt(вещи1), "Тm": alt(вещи),
                "Твk": alt(вещи_вин),
                "Т1а": alt([f"{_plural.article(в)} {в}" for в in вещи1] if язык == "en" else вещи1),
                "ГОЛОВА": alt(ГОЛОВЫ_ИТОГА[язык]), "Ц1": alt(ЦВЕТА[язык] + ЦВЕТА_М.get(язык, ())), "Ц2": alt(ЦВЕТА[язык] + ЦВЕТА_М.get(язык, ())),
                "В1": alt(в for в, _ in ВРЕМЯ[язык]), "В2": alt(в for _, в in ВРЕМЯ[язык]),
                "Г1a": alt(товары), "Г2b": alt(товары), "Г3мн": alt(товары), "Г3s": alt(товары)}
        if язык == "pl":
            дыры["ЕСТЬn"] = alt(_PL.СВЯЗКА["наст"])
        for дыра, пара in РОДОВЫЕ.get(язык, {}).items():
            дыры[дыра] = alt(пара)
        if romgram.гнётся(язык):
            # вопросное слово товара — та же пара двери; какое из двух верно, решает род головы
            # товара, и сверяет его судья, а не образец
            дыры["Г3кск"] = alt(romgram.ПАРЫ[язык])
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
                _эк = _fr.в_образце if язык == "fr" else re.escape
                for кусок in re.split(r"(\{[^}]+\})", рамка):
                    куски.append(дыры[кусок[1:-1]] if кусок.startswith("{") else _эк(кусок))
                вон.append((re.compile("^" + "".join(куски) + "$"), язык, форма))
    return вон


ОБРАЗЦЫ = _образцы()

# ГЛАГОЛЫ-АКТЫ, НАЗВАННЫЕ ПЕРЕПИСЬЮ ЖИВОЙ ПОЛОСЫ (holon, атлас непрочитанных чисел, 06.09): пятая
# точка купила 307 глаголов истории, но не акты, на которых стоят десятки задач полосы: сделал,
# добавил, выбросил, узнал что … пришли, сели / вышли, сыграл, потратил; и конструкции «вместилище
# с N вещей», «всего N часов», «часть целого длиной N», две клаузы с «и», список через запятую того
# же товара, «ones» = тот же товар. Каждому акту — ≥ LAW показов: носитель + глагол + число + товар
# + вопрос. Товары объявлены со счётными формами (en: one/many; ru: one/few/many).
#
# СЦЕНЫ ПЕРЕПИСАНЫ 23.09 (слово владельца: полоса — прибор, а не источник). Прежние сцены были
# писаны чтением задач полосы — их товары, их строй; ныне у каждого акта своя сцена при той же
# конструкции (посадил дубы и берёзы, утки на пруду, места в вагонах поезда, марки за два дня),
# и суд утечки (`scripts/bench_leak.py`) обязан не назвать ни одной страницы дома.
ТОВАРЫ_АКТОВ = {
    "en": {"дубы": ("oak", "oaks"), "берёзы": ("birch", "birches"), "фото": ("photo", "photos"),
           "банки": ("jar", "jars"), "грибы": ("mushroom", "mushrooms"), "груши": ("pear", "pears"),
           "гости": ("guest", "guests"), "утки": ("duck", "ducks"), "марки": ("stamp", "stamps"), "часы": ("hour", "hours"),
           "орехи": ("nut", "nuts"), "места": ("seat", "seats"),
           # КЛАСС НАД ТОВАРАМИ ОБЪЯВЛЕН ТОВАРОМ, И ОТТОГО СЧИТАЕТСЯ ЗАКОНОМ (13.09).
           # Рамка «сделал» спрашивала класс («how many … in all?») и отвечала голой цифрой, и слово
           # класса при числе в своде не стояло НИ РАЗУ ни на одном из девяти языков.
           #     ИМЯ, СПРОШЕННОЕ КЛАССОМ И ОТВЕЧЕННОЕ ГОЛЫМ ЧИСЛОМ, НИ РАЗУ НЕ СТОИ́Т ПРИ
           #     ЧИСЛЕ — и читатель, выучивший вопрос, не выучил ответа.
           # Найдено чужим прибором (holon-f9, рынок классовых слов) и подтверждено своим
           # (`scripts/asked_uncounted.py`).
           "деревья": ("tree", "trees")},
    "ru": {"дубы": ("дуб", "дуба", "дубов"), "берёзы": ("берёза", "берёзы", "берёз"),
           "фото": ("фотография", "фотографии", "фотографий"), "банки": ("банка", "банки", "банок"),
           "грибы": ("гриб", "гриба", "грибов"), "груши": ("груша", "груши", "груш"), "гости": ("гость", "гостя", "гостей"),
           "утки": ("утка", "утки", "уток"), "марки": ("марка", "марки", "марок"), "часы": ("час", "часа", "часов"),
           "орехи": ("орех", "ореха", "орехов"), "места": ("место", "места", "мест"),
           "деревья": ("дерево", "дерева", "деревьев")},
}
РАМКИ_АКТОВ = {
    "en": dict(
        сделал="{X} planted {n} {ОТЖn} and {k} {СКРk}. how many {ОТЖмн} did {X} plant? {n}. how many {УПРмн} in all? {s} {УПРs}: {n} + {k} = {s}.",
        больше_чем="{X} planted {n} {ОТЖn}. {Y} planted {k} more {ОТЖмн} than {X}. how many {ОТЖмн} did {Y} plant? {s}: {n} + {k} = {s}.",
        меньше_чем="{X} planted {n} {ОТЖn}. {Y} planted {k} fewer {ОТЖмн} than {X}. how many {ОТЖмн} did {Y} plant? {r}: {n} − {k} = {r}.",
        вещи3="{X} has {n} {ФИГn}, {k} {МЕЛk} and {m} {ИГРm}. how many things does {X} have in all? {t}: {n} + {k} + {m} = {t}.",
        продал="{X} had {n} {РОЗn}. {Он} sold {k} {РОЗk}. how many {РОЗмн} does {он} have left? {r}: {n} − {k} = {r}.",
        присоединились="there were {n} {ДЕТn} on the lake. {k} more {ДЕТk} joined them. how many {ДЕТмн} are on the lake now? {s}: {n} + {k} = {s}.",
        жили="{n} {ЖИЛn} were living in the hive. {k} {ЖИЛk} flew away. how many {ЖИЛмн} are living in the hive now? {r}: {n} − {k} = {r}.",
        предложил="{X} brought {n} {ФИГn} to the cellar. {Y} took {k} of them away. how many {ФИГмн} are left? {r}: {n} − {k} = {r}.",
        в_школе="on a farm there are {n} {ДЕВn} and {k} {МАЛk}. how many animals are there on the farm? {s}: {n} + {k} = {s}.",
        рецепт="the builders need {n} {ЧАШn} for the wall and {k} {ЧАШk} for the path. how many more {ЧАШмн} do they need for the wall than for the path? {r}: {n} − {k} = {r}.",
        теперь_список="{X} had {n} {ФИГn}. {Он} also got {k} {МЕЛk}. now {он} has {n} {ФИГn} and {k} {МЕЛk}. how many things does {он} have in all? {s}: {n} + {k} = {s}.",
        добавил="{X} had {n} {ПРИЛn} in the album. {Он} added {k} new {ПРИЛмн}. how many {ПРИЛмн} does {он} have now? {s}: {n} + {k} = {s}.",
        добавил_на_полку="{X} had {n} {ФИГn} in the pantry. later {он} put {k} more {ФИГмн} in the pantry. how many {ФИГмн} are in the pantry now? {s}: {n} + {k} = {s}.",
        выбросил="{X} picked {n} {КРЫШn} in the forest and threw away {k} bad ones. how many more {КРЫШмн} did {он} pick than throw away? {r}: {n} − {k} = {r}.",
        выбросил_розы="there were {n} {РОЗn} in the basket. {X} threw away {k} {РОЗмн} from the basket. how many {РОЗмн} are in the basket now? {r}: {n} − {k} = {r}.",
        узнал="{X} counted that {n} {ПОСn} came to the museum on the first day and {k} on the second. how many {ПОСмн} came in all? {s}: {n} + {k} = {s}.",
        сели_вышли="there were {n} {ДЕТn} on the pond. {k} {ДЕТмн} landed on the pond while some flew away. now there are {s} {ДЕТмн} on the pond. how many {ДЕТмн} flew away? {k2}: {n} + {k} − {s} = {k2}.",
        сыграл="{X} collected {n} {ИГРn} on monday and {k} {ИГРмн} on tuesday. how many {ИГРмн} did {X} collect in all? {s}: {n} + {k} = {s}.",
        потратил="{X} spent {n} {ЧАСn} on drawing and {k} {ЧАСмн} on chess. how many {ЧАСмн} did {X} spend in all? a total of {s} {ЧАСмн}: {n} + {k} = {s}.",
        список="every day {X} spends {n} {ЧАСn} on drawing, {k} {ЧАСмн} on chess and {m} {ЧАСмн} on reading. how many {ЧАСмн} does {X} spend in all? {t}: {n} + {k} + {m} = {t}.",
        коробка="{X} got a bag of {n} {МЕЛn} and a bag of {k} {МЕЛмн}. how many {МЕЛмн} does {X} have? {s}: {n} + {k} = {s}.",
        главы="a train has 2 cars. the first car has {n} {СТРn} and the second car has {k} {СТРмн}. how many {СТРмн} does the train have in all? {s}: {n} + {k} = {s}.",
        две_клаузы="{X} had {n} {ИГРn} and {Y} had {k} {ИГРмн}. how many {ИГРмн} did they have together? {s}: {n} + {k} = {s}.",
    ),
    "ru": dict(
        сделал="{X} посадил{а} {n} {ОТЖn} и {k} {СКРk}. сколько {ОТЖмн} посадил{а} {X}? {n}. сколько {УПРмн} всего? {s} {УПРs}: {n} + {k} = {s}.",
        больше_чем="{X} посадил{а} {n} {ОТЖn}. {Y} посадил{аY} на {k} {ОТЖk} больше, чем {X}. сколько {ОТЖмн} посадил{аY} {Y}? {s}: {n} + {k} = {s}.",
        меньше_чем="{X} посадил{а} {n} {ОТЖn}. {Y} посадил{аY} на {k} {ОТЖk} меньше, чем {X}. сколько {ОТЖмн} посадил{аY} {Y}? {r}: {n} − {k} = {r}.",
        вещи3="у {Xр} {n} {ФИГn}, {k} {МЕЛk} и {m} {ИГРm}. сколько всего предметов у {Xр}? {t}: {n} + {k} + {m} = {t}.",
        продал="у {Xр} было {n} {РОЗn}. {Он} продал{а} {k} {РОЗk}. сколько {РОЗмн} у {него} осталось? {r}: {n} − {k} = {r}.",
        присоединились="на озере было {n} {ДЕТn}. к ним присоединилось ещё {k} {ДЕТk}. сколько {ДЕТмн} на озере теперь? {s}: {n} + {k} = {s}.",
        жили="в улье жило {n} {ЖИЛn}. {k} {ЖИЛk} улетели. сколько {ЖИЛмн} живёт в улье теперь? {r}: {n} − {k} = {r}.",
        предложил="{X} поставил{а} в погреб {n} {ФИГn}. {Y} убрал{аY} {k} из них. сколько {ФИГмн} осталось? {r}: {n} − {k} = {r}.",
        в_школе="на ферме {n} {ДЕВn} и {k} {МАЛk}. сколько всего животных на ферме? {s}: {n} + {k} = {s}.",
        рецепт="строителям нужно {n} {ЧАШn} для стены и {k} {ЧАШk} для дорожки. на сколько больше {ЧАШмн} нужно для стены, чем для дорожки? {r}: {n} − {k} = {r}.",
        теперь_список="у {Xр} было {n} {ФИГn}. ещё {он} получил{а} {k} {МЕЛk}. теперь у {него} {n} {ФИГn} и {k} {МЕЛk}. сколько всего предметов у {него}? {s}: {n} + {k} = {s}.",
        добавил="у {Xр} было {n} {ПРИЛn} в альбоме. {Он} добавил{а} {k} {ПРИЛk}. сколько {ПРИЛмн} у {него} теперь? {s}: {n} + {k} = {s}.",
        добавил_на_полку="у {Xр} в кладовке было {n} {ФИГn}. потом {он} поставил{а} в кладовку ещё {k} {ФИГk}. сколько {ФИГмн} в кладовке теперь? {s}: {n} + {k} = {s}.",
        выбросил="{X} собрал{а} в лесу {n} {КРЫШn}, а {k} плохих выбросил{а}. на сколько больше {КРЫШмн} {он} собрал{а}, чем выбросил{а}? {r}: {n} − {k} = {r}.",
        выбросил_розы="в корзине было {n} {РОЗn}. {X} выбросил{а} из корзины {k} {РОЗk}. сколько {РОЗмн} в корзине теперь? {r}: {n} − {k} = {r}.",
        узнал="{X} подсчитал{а}, что в музей в первый день пришли {n} {ПОСn}, а во второй — {k}. сколько {ПОСмн} пришло всего? {s}: {n} + {k} = {s}.",
        сели_вышли="на пруду было {n} {ДЕТn}. {k} {ДЕТk} сели на пруд, а несколько улетели. теперь на пруду {s} {ДЕТs}. сколько {ДЕТмн} улетело? {k2}: {n} + {k} − {s} = {k2}.",
        сыграл="{X} собрал{а} {n} {ИГРn} в понедельник и {k} {ИГРk} во вторник. сколько {ИГРмн} собрал{а} {X} всего? {s}: {n} + {k} = {s}.",
        потратил="{X} потратил{а} {n} {ЧАСn} на рисование и {k} {ЧАСk} на шахматы. сколько {ЧАСмн} потратил{а} {X} всего? всего {s} {ЧАСs}: {n} + {k} = {s}.",
        список="каждый день {X} тратит {n} {ЧАСn} на рисование, {k} {ЧАСk} на шахматы и {m} {ЧАСm} на чтение. сколько {ЧАСмн} тратит {X} всего? {t}: {n} + {k} + {m} = {t}.",
        коробка="{X} получил{а} пакет с {n} {МЕЛпр} и пакет с {k} {МЕЛпр}. сколько {МЕЛмн} у {Xр}? {s}: {n} + {k} = {s}.",
        главы="в поезде 2 вагона. в первом вагоне {n} {СТРn}, во втором — {k} {СТРk}. сколько {СТРмн} в поезде всего? {s}: {n} + {k} = {s}.",
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
    "ru": {"орехи": "орехами"},
    "pl": {"орехи": "orzechami"},
    "de": {"орехи": "Nüssen"},
}
# РОД ТОВАРА АКТОВ ОБЪЯВЛЕН ПОИМЁННО, И ЭТО ТРЕТИЙ СЛУЧАЙ ОДНОГО ЗАКОНА ЗА ДЕНЬ (16.09,
# прибор `scripts/twogender.py`: «quante addominali» 16 страниц при «quanti addominali» 48).
#
# Рамки актов писали вопросное слово ЛИТЕРАЛОМ — «{ОТЖкск} {ОТЖмн}», — и литерал был верен:
# отжимания женского рода на всех трёх языках. Но дом умеет ПОДМЕНЯТЬ товар в дыре
# (`товары={"ОТЖ": "скручивания"}`), и подменённый приносит свой род: «addominali» мужского.
#
#     ЛИТЕРАЛ ВОПРОСНОГО СЛОВА ВЕРЕН, ПОКУДА ТОВАР НЕ ПОДМЕНЁН. Правота, держащаяся тем,
#     что одну дыру всегда заполняет одно слово, есть долг, ещё не предъявленный: подмена
#     объявлена самим домом — и объявлена раньше, чем литерал стал ложью.
#
# Род брался у `вещь(5)` — первого списка вещей, — а в строке стоял товар ВТОРОГО списка.
#
#     РОД БЕРЁТСЯ У СЛОВА, КОТОРОЕ СТОИ́Т В СТРОКЕ, А НЕ У СОСЕДА ПО НОМЕРУ.
#
# Половину этих родов знал соседний дом (`cmpframes.РОД`) — и снова знание языка лежало у
# одного дома из двух. Здесь объявлены ВСЕ семнадцать товаров трёх гнущихся языков, и
# самопроверка ниже не даёт объявлению отстать от таблицы товаров.
РОД_ТОВАРА_АКТОВ = {
    "es": {"robles": "m", "abedules": "m", "árboles": "m", "fotos": "f", "tarros": "m", "setas": "f",
           "peras": "f", "invitados": "m", "patos": "m", "sellos": "m", "horas": "f", "nueces": "f",
           "asientos": "m", "vacas": "f", "cabras": "f", "ladrillos": "m", "abejas": "f"},
    "it": {"querce": "f", "betulle": "f", "alberi": "m", "foto": "f", "barattoli": "m", "funghi": "m",
           "pere": "f", "ospiti": "m", "anatre": "f", "francobolli": "m", "ore": "f", "noci": "f",
           "posti": "m", "mucche": "f", "capre": "f", "mattoni": "m", "api": "f"},
    "pt": {"carvalhos": "m", "bétulas": "f", "árvores": "f", "fotos": "f", "frascos": "m", "cogumelos": "m",
           "peras": "f", "convidados": "m", "patos": "m", "selos": "m", "horas": "f", "nozes": "f",
           "lugares": "m", "vacas": "f", "cabras": "f", "tijolos": "m", "abelhas": "f"},
}

_ТОВАР_ПО_ДЫРЕ = {"УПР": "деревья", "ОТЖ": "дубы", "СКР": "берёзы", "ПРИЛ": "фото", "ФИГ": "банки", "КРЫШ": "грибы", "РОЗ": "груши",
                  "ПОС": "гости", "ДЕТ": "утки", "ИГР": "марки", "ЧАС": "часы", "МЕЛ": "орехи", "СТР": "места"}
ТОВАРЫ_АКТОВ.update({
    "de": {"дубы": ("Eiche", "Eichen"), "берёзы": ("Birke", "Birken"), "фото": ("Foto", "Fotos"), "банки": ("Glas", "Gläser"),
           "грибы": ("Pilz", "Pilze"), "груши": ("Birne", "Birnen"), "гости": ("Gast", "Gäste"), "утки": ("Ente", "Enten"),
           "марки": ("Briefmarke", "Briefmarken"), "часы": ("Stunde", "Stunden"), "орехи": ("Nuss", "Nüsse"),
           "места": ("Platz", "Plätze"), "деревья": ("Baum", "Bäume")},
    "fr": {"дубы": ("chêne", "chênes"), "берёзы": ("bouleau", "bouleaux"), "фото": ("photo", "photos"), "банки": ("bocal", "bocaux"),
           "грибы": ("champignon", "champignons"), "груши": ("poire", "poires"), "гости": ("invité", "invités"),
           "утки": ("canard", "canards"), "марки": ("timbre", "timbres"), "часы": ("heure", "heures"), "орехи": ("noix", "noix"),
           "места": ("place", "places"), "деревья": ("arbre", "arbres")},
    "es": {"дубы": ("roble", "robles"), "берёзы": ("abedul", "abedules"), "фото": ("foto", "fotos"), "банки": ("tarro", "tarros"),
           "грибы": ("seta", "setas"), "груши": ("pera", "peras"), "гости": ("invitado", "invitados"), "утки": ("pato", "patos"),
           "марки": ("sello", "sellos"), "часы": ("hora", "horas"), "орехи": ("nuez", "nueces"), "места": ("asiento", "asientos"),
           "деревья": ("árbol", "árboles")},
    "it": {"дубы": ("quercia", "querce"), "берёзы": ("betulla", "betulle"), "фото": ("foto", "foto"), "банки": ("barattolo", "barattoli"),
           "грибы": ("fungo", "funghi"), "груши": ("pera", "pere"), "гости": ("ospite", "ospiti"), "утки": ("anatra", "anatre"),
           "марки": ("francobollo", "francobolli"), "часы": ("ora", "ore"), "орехи": ("noce", "noci"), "места": ("posto", "posti"),
           "деревья": ("albero", "alberi")},
    "pt": {"дубы": ("carvalho", "carvalhos"), "берёзы": ("bétula", "bétulas"), "фото": ("foto", "fotos"), "банки": ("frasco", "frascos"),
           "грибы": ("cogumelo", "cogumelos"), "груши": ("pera", "peras"), "гости": ("convidado", "convidados"), "утки": ("pato", "patos"),
           "марки": ("selo", "selos"), "часы": ("hora", "horas"), "орехи": ("noz", "nozes"), "места": ("lugar", "lugares"),
           "деревья": ("árvore", "árvores")},
    "nl": {"дубы": ("eik", "eiken"), "берёзы": ("berk", "berken"), "фото": ("foto", "foto's"), "банки": ("pot", "potten"),
           "грибы": ("paddenstoel", "paddenstoelen"), "груши": ("peer", "peren"), "гости": ("gast", "gasten"), "утки": ("eend", "eenden"),
           "марки": ("postzegel", "postzegels"), "часы": ("uur", "uur"), "орехи": ("noot", "noten"), "места": ("zitplaats", "zitplaatsen"),
           "деревья": ("boom", "bomen")},
    "pl": {"дубы": ("dąb", "dęby", "dębów"), "берёзы": ("brzoza", "brzozy", "brzóz"), "фото": ("zdjęcie", "zdjęcia", "zdjęć"),
           "банки": ("słoik", "słoiki", "słoików"), "грибы": ("grzyb", "grzyby", "grzybów"), "груши": ("gruszka", "gruszki", "gruszek"),
           "гости": ("gość", "gości", "gości"), "утки": ("kaczka", "kaczki", "kaczek"), "марки": ("znaczek", "znaczki", "znaczków"),
           "часы": ("godzina", "godziny", "godzin"), "орехи": ("orzech", "orzechy", "orzechów"), "места": ("miejsce", "miejsca", "miejsc"),
           "деревья": ("drzewo", "drzewa", "drzew")},
})
# ТОВАРЫ ВТОРОЙ ПОДАЧИ — коровы и козы на ферме, кирпичи стройки, пчёлы улья — со счётными формами
for _яз, _новые in {
    "en": {"коровы": ("cow", "cows"), "козы": ("goat", "goats"), "кирпичи": ("brick", "bricks"), "пчёлы": ("bee", "bees")},
    "ru": {"коровы": ("корова", "коровы", "коров"), "козы": ("коза", "козы", "коз"), "кирпичи": ("кирпич", "кирпича", "кирпичей"), "пчёлы": ("пчела", "пчелы", "пчёл")},
    "de": {"коровы": ("Kuh", "Kühe"), "козы": ("Ziege", "Ziegen"), "кирпичи": ("Ziegel", "Ziegel"), "пчёлы": ("Biene", "Bienen")},
    "fr": {"коровы": ("vache", "vaches"), "козы": ("chèvre", "chèvres"), "кирпичи": ("brique", "briques"), "пчёлы": ("abeille", "abeilles")},
    "es": {"коровы": ("vaca", "vacas"), "козы": ("cabra", "cabras"), "кирпичи": ("ladrillo", "ladrillos"), "пчёлы": ("abeja", "abejas")},
    "it": {"коровы": ("mucca", "mucche"), "козы": ("capra", "capre"), "кирпичи": ("mattone", "mattoni"), "пчёлы": ("ape", "api")},
    "pt": {"коровы": ("vaca", "vacas"), "козы": ("cabra", "cabras"), "кирпичи": ("tijolo", "tijolos"), "пчёлы": ("abelha", "abelhas")},
    "nl": {"коровы": ("koe", "koeien"), "козы": ("geit", "geiten"), "кирпичи": ("baksteen", "bakstenen"), "пчёлы": ("bij", "bijen")},
    "pl": {"коровы": ("krowa", "krowy", "krów"), "козы": ("koza", "kozy", "kóz"), "кирпичи": ("cegła", "cegły", "cegieł"), "пчёлы": ("pszczoła", "pszczoły", "pszczół")},
}.items():
    ТОВАРЫ_АКТОВ[_яз].update(_новые)
_ТОВАР_ПО_ДЫРЕ.update({"ДЕВ": "коровы", "МАЛ": "козы", "ЧАШ": "кирпичи", "ЖИЛ": "пчёлы"})
РАМКИ_АКТОВ.update({
    "de": dict(
               больше_чем="{X} pflanzte {n} {ОТЖn}. {Y} pflanzte {k} {ОТЖмн} mehr als {X}. wie viele {ОТЖмн} pflanzte {Y}? {s}: {n} + {k} = {s}.",
               меньше_чем="{X} pflanzte {n} {ОТЖn}. {Y} pflanzte {k} {ОТЖмн} weniger als {X}. wie viele {ОТЖмн} pflanzte {Y}? {r}: {n} − {k} = {r}.",
               добавил_на_полку="{X} hatte {n} {ФИГn} in der Speisekammer. später stellte {он} {k} weitere {ФИГмн} in die Speisekammer. wie viele {ФИГмн} stehen jetzt in der Speisekammer? {s}: {n} + {k} = {s}.",
               выбросил="{X} sammelte im Wald {n} {КРЫШn} und warf {k} schlechte weg. wie viele {КРЫШмн} mehr sammelte {он}, als {он} wegwarf? {r}: {n} − {k} = {r}.",
               выбросил_розы="im Korb waren {n} {РОЗn}. {X} warf {k} {РОЗмн} aus dem Korb weg. wie viele {РОЗмн} sind jetzt im Korb? {r}: {n} − {k} = {r}.",
               узнал="{X} zählte, dass am ersten Tag {n} {ПОСn} ins Museum kamen und am zweiten Tag {k}. wie viele {ПОСмн} kamen insgesamt? {s}: {n} + {k} = {s}.",
               сели_вышли="auf dem Teich waren {n} {ДЕТn}. {k} {ДЕТмн} landeten auf dem Teich, während einige wegflogen. jetzt sind {s} {ДЕТмн} auf dem Teich. wie viele {ДЕТмн} flogen weg? {k2}: {n} + {k} − {s} = {k2}.",
               сыграл="{X} sammelte am Montag {n} {ИГРn} und am Dienstag {k} {ИГРмн}. wie viele {ИГРмн} sammelte {X} insgesamt? {s}: {n} + {k} = {s}.",
               потратил="{X} verbrachte {n} {ЧАСn} mit Zeichnen und {k} {ЧАСмн} mit Schach. wie viele {ЧАСмн} verbrachte {X} insgesamt? insgesamt {s} {ЧАСмн}: {n} + {k} = {s}.",
               список="jeden Tag verbringt {X} {n} {ЧАСn} mit Zeichnen, {k} {ЧАСмн} mit Schach und {m} {ЧАСмн} mit Lesen. wie viele {ЧАСмн} verbringt {X} insgesamt? {t}: {n} + {k} + {m} = {t}.",
               коробка="{X} bekam eine Tüte mit {n} {МЕЛпр} und eine Tüte mit {k} {МЕЛпр}. wie viele {МЕЛмн} hat {X}? {s}: {n} + {k} = {s}.",
               главы="ein Zug hat 2 Wagen. der erste Wagen hat {n} {СТРn} und der zweite {k} {СТРмн}. wie viele {СТРмн} hat der Zug insgesamt? {s}: {n} + {k} = {s}.",
               две_клаузы="{X} hatte {n} {ИГРn} und {Y} hatte {k} {ИГРмн}. wie viele {ИГРмн} hatten sie zusammen? {s}: {n} + {k} = {s}.",
               сделал="{X} pflanzte {n} {ОТЖn} und {k} {СКРk}. wie viele {ОТЖмн} pflanzte {X}? {n}. wie viele {УПРмн} insgesamt? {s} {УПРs}: {n} + {k} = {s}.",
               вещи3="{X} hat {n} {ФИГn}, {k} {МЕЛk} und {m} {ИГРm}. wie viele Dinge hat {X} insgesamt? {t}: {n} + {k} + {m} = {t}.",
               продал="{X} hatte {n} {РОЗn}. {Он} verkaufte {k} {РОЗk}. wie viele {РОЗмн} hat {он} noch? {r}: {n} − {k} = {r}.",
               присоединились="auf dem See waren {n} {ДЕТn}. {k} weitere {ДЕТk} kamen dazu. wie viele {ДЕТмн} sind jetzt auf dem See? {s}: {n} + {k} = {s}.",
               жили="{n} {ЖИЛn} lebten im Bienenstock. {k} {ЖИЛk} flogen weg. wie viele {ЖИЛмн} leben jetzt im Bienenstock? {r}: {n} − {k} = {r}.",
               предложил="{X} brachte {n} {ФИГn} in den Keller. {Y} nahm {k} davon weg. wie viele {ФИГмн} bleiben übrig? {r}: {n} − {k} = {r}.",
               в_школе="auf einem Bauernhof gibt es {n} {ДЕВn} und {k} {МАЛk}. wie viele Tiere gibt es auf dem Bauernhof? {s}: {n} + {k} = {s}.",
               рецепт="die Bauarbeiter brauchen {n} {ЧАШn} für die Mauer und {k} {ЧАШk} für den Weg. wie viele {ЧАШмн} mehr brauchen sie für die Mauer als für den Weg? {r}: {n} − {k} = {r}.",
               теперь_список="{X} hatte {n} {ФИГn}. {Он} bekam noch {k} {МЕЛk}. jetzt hat {он} {n} {ФИГn} und {k} {МЕЛk}. wie viele Dinge hat {он} insgesamt? {s}: {n} + {k} = {s}.",
               добавил="{X} hatte {n} {ПРИЛn} im Album. {Он} fügte {k} neue {ПРИЛмн} hinzu. wie viele {ПРИЛмн} hat {он} jetzt? {s}: {n} + {k} = {s}."),
    "fr": dict(
               больше_чем="{X} a planté {n} {ОТЖn}. {Y} a planté {k} {ОТЖмн} de plus que {X}. combien de {ОТЖмн} {Y} a-t-{аY_он} plantés ? {s} : {n} + {k} = {s}.",
               меньше_чем="{X} a planté {n} {ОТЖn}. {Y} a planté {k} {ОТЖмн} de moins que {X}. combien de {ОТЖмн} {Y} a-t-{аY_он} plantés ? {r} : {n} − {k} = {r}.",
               добавил_на_полку="{X} avait {n} {ФИГn} dans le cellier. plus tard {он} a mis {k} {ФИГмн} de plus dans le cellier. combien de {ФИГмн} y a-t-il dans le cellier maintenant ? {s} : {n} + {k} = {s}.",
               выбросил="{X} a cueilli {n} {КРЫШn} dans la forêt et en a jeté {k} mauvais. combien de {КРЫШмн} de plus {X} a-t-{он} cueillis que jetés ? {r} : {n} − {k} = {r}.",
               выбросил_розы="il y avait {n} {РОЗn} dans le panier. {X} a jeté {k} {РОЗмн} du panier. combien de {РОЗмн} y a-t-il dans le panier maintenant ? {r} : {n} − {k} = {r}.",
               узнал="{X} a compté que {n} {ПОСn} sont venus au musée le premier jour et {k} le deuxième. combien de {ПОСмн} sont venus en tout ? {s} : {n} + {k} = {s}.",
               сели_вышли="il y avait {n} {ДЕТn} sur l'étang. {k} {ДЕТмн} se sont posés sur l'étang tandis que quelques-uns se sont envolés. maintenant il y a {s} {ДЕТмн} sur l'étang. combien de {ДЕТмн} se sont envolés ? {k2} : {n} + {k} − {s} = {k2}.",
               сыграл="{X} a collectionné {n} {ИГРn} lundi et {k} {ИГРмн} mardi. combien de {ИГРмн} {X} a-t-{он} collectionnés en tout ? {s} : {n} + {k} = {s}.",
               потратил="{X} a passé {n} {ЧАСn} sur le dessin et {k} {ЧАСмн} sur les échecs. combien d'{ЧАСмн} {X} a-t-{он} passées en tout ? un total de {s} {ЧАСмн} : {n} + {k} = {s}.",
               список="chaque jour {X} passe {n} {ЧАСn} sur le dessin, {k} {ЧАСмн} sur les échecs et {m} {ЧАСмн} sur la lecture. combien d'{ЧАСмн} {X} passe-t-{он} en tout ? {t} : {n} + {k} + {m} = {t}.",
               коробка="{X} a reçu un sachet de {n} {МЕЛn} et un sachet de {k} {МЕЛмн}. combien de {МЕЛмн} {X} a-t-{он} ? {s} : {n} + {k} = {s}.",
               главы="un train a 2 wagons. le premier wagon a {n} {СТРn} et le second {k} {СТРмн}. combien de {СТРмн} le train a-t-il en tout ? {s} : {n} + {k} = {s}.",
               две_клаузы="{X} avait {n} {ИГРn} et {Y} avait {k} {ИГРмн}. combien de {ИГРмн} avaient-ils ensemble ? {s} : {n} + {k} = {s}.",
               сделал="{X} a planté {n} {ОТЖn} et {k} {СКРk}. combien de {ОТЖмн} {X} a-t-{он} plantés ? {n}. combien d'{УПРмн} en tout ? {s} {УПРs} : {n} + {k} = {s}.",
               вещи3="{X} a {n} {ФИГn}, {k} {МЕЛk} et {m} {ИГРm}. combien d'objets a {X} en tout ? {t} : {n} + {k} + {m} = {t}.",
               продал="{X} avait {n} {РОЗn}. {Он} a vendu {k} {РОЗk}. combien de {РОЗмн} lui reste-t-il ? {r} : {n} − {k} = {r}.",
               присоединились="il y avait {n} {ДЕТn} sur le lac. {k} autres {ДЕТk} les ont rejoints. combien de {ДЕТмн} y a-t-il maintenant sur le lac ? {s} : {n} + {k} = {s}.",
               жили="{n} {ЖИЛn} vivaient dans la ruche. {k} {ЖИЛk} se sont envolées. combien de {ЖИЛмн} vivent dans la ruche maintenant ? {r} : {n} − {k} = {r}.",
               предложил="{X} a apporté {n} {ФИГn} à la cave. {Y} en a retiré {k}. combien de {ФИГмн} reste-t-il ? {r} : {n} − {k} = {r}.",
               в_школе="dans une ferme il y a {n} {ДЕВn} et {k} {МАЛk}. combien d'animaux y a-t-il dans la ferme ? {s} : {n} + {k} = {s}.",
               рецепт="les maçons ont besoin de {n} {ЧАШn} pour le mur et de {k} {ЧАШk} pour l'allée. combien de {ЧАШмн} de plus leur faut-il pour le mur que pour l'allée ? {r} : {n} − {k} = {r}.",
               теперь_список="{X} avait {n} {ФИГn}. {Он} a aussi reçu {k} {МЕЛk}. maintenant {он} a {n} {ФИГn} et {k} {МЕЛk}. combien d'objets a-t-{он} en tout ? {s} : {n} + {k} = {s}.",
               добавил="{X} avait {n} {ПРИЛn} dans l'album. {Он} a ajouté {k} nouvelles {ПРИЛмн}. combien de {ПРИЛмн} a-t-{он} maintenant ? {s} : {n} + {k} = {s}."),
    "es": dict(
               больше_чем="{X} plantó {n} {ОТЖn}. {Y} plantó {k} {ОТЖмн} más que {X}. ¿{ОТЖкск} {ОТЖмн} plantó {Y}? {s}: {n} + {k} = {s}.",
               меньше_чем="{X} plantó {n} {ОТЖn}. {Y} plantó {k} {ОТЖмн} menos que {X}. ¿{ОТЖкск} {ОТЖмн} plantó {Y}? {r}: {n} − {k} = {r}.",
               добавил_на_полку="{X} tenía {n} {ФИГn} en la despensa. luego puso {k} {ФИГмн} más en la despensa. ¿{ФИГкск} {ФИГмн} hay ahora en la despensa? {s}: {n} + {k} = {s}.",
               выбросил="{X} recogió {n} {КРЫШn} en el bosque y tiró {k} malas. ¿{КРЫШкск} {КРЫШмн} más recogió de las que tiró? {r}: {n} − {k} = {r}.",
               выбросил_розы="había {n} {РОЗn} en la cesta. {X} tiró {k} {РОЗмн} de la cesta. ¿{РОЗкск} {РОЗмн} hay ahora en la cesta? {r}: {n} − {k} = {r}.",
               узнал="{X} contó que el primer día llegaron {n} {ПОСn} al museo y el segundo día {k}. ¿{ПОСкск} {ПОСмн} llegaron en total? {s}: {n} + {k} = {s}.",
               сели_вышли="había {n} {ДЕТn} en el estanque. {k} {ДЕТмн} se posaron en el estanque mientras algunos se fueron volando. ahora hay {s} {ДЕТмн} en el estanque. ¿{ДЕТкск} {ДЕТмн} se fueron volando? {k2}: {n} + {k} − {s} = {k2}.",
               сыграл="{X} reunió {n} {ИГРn} el lunes y {k} {ИГРмн} el martes. ¿{ИГРкск} {ИГРмн} reunió {X} en total? {s}: {n} + {k} = {s}.",
               потратил="{X} dedicó {n} {ЧАСn} al dibujo y {k} {ЧАСмн} al ajedrez. ¿{ЧАСкск} {ЧАСмн} dedicó {X} en total? un total de {s} {ЧАСмн}: {n} + {k} = {s}.",
               список="cada día {X} dedica {n} {ЧАСn} al dibujo, {k} {ЧАСмн} al ajedrez y {m} {ЧАСмн} a la lectura. ¿{ЧАСкск} {ЧАСмн} dedica {X} en total? {t}: {n} + {k} + {m} = {t}.",
               коробка="{X} recibió una bolsa de {n} {МЕЛn} y una bolsa de {k} {МЕЛмн}. ¿{МЕЛкск} {МЕЛмн} tiene {X}? {s}: {n} + {k} = {s}.",
               главы="un tren tiene 2 vagones. el primer vagón tiene {n} {СТРn} y el segundo {k} {СТРмн}. ¿{СТРкск} {СТРмн} tiene el tren en total? {s}: {n} + {k} = {s}.",
               две_клаузы="{X} tenía {n} {ИГРn} y {Y} tenía {k} {ИГРмн}. ¿{ИГРкск} {ИГРмн} tenían juntos? {s}: {n} + {k} = {s}.",
               сделал="{X} plantó {n} {ОТЖn} y {k} {СКРk}. ¿{ОТЖкск} {ОТЖмн} plantó {X}? {n}. ¿{УПРкск} {УПРмн} en total? {s} {УПРs}: {n} + {k} = {s}.",
               вещи3="{X} tiene {n} {ФИГn}, {k} {МЕЛk} y {m} {ИГРm}. ¿cuántas cosas tiene {X} en total? {t}: {n} + {k} + {m} = {t}.",
               продал="{X} tenía {n} {РОЗn}. vendió {k} {РОЗk}. ¿{РОЗкск} {РОЗмн} le quedan? {r}: {n} − {k} = {r}.",
               присоединились="había {n} {ДЕТn} en el lago. se les unieron {k} {ДЕТk} más. ¿{ДЕТкск} {ДЕТмн} hay ahora en el lago? {s}: {n} + {k} = {s}.",
               жили="{n} {ЖИЛn} vivían en la colmena. {k} {ЖИЛk} se fueron volando. ¿{ЖИЛкск} {ЖИЛмн} viven ahora en la colmena? {r}: {n} − {k} = {r}.",
               предложил="{X} llevó {n} {ФИГn} al sótano. {Y} se llevó {k} de ellos. ¿{ФИГкск} {ФИГмн} quedan? {r}: {n} − {k} = {r}.",
               в_школе="en una granja hay {n} {ДЕВn} y {k} {МАЛk}. ¿cuántos animales hay en la granja? {s}: {n} + {k} = {s}.",
               рецепт="los albañiles necesitan {n} {ЧАШn} para el muro y {k} {ЧАШk} para el camino. ¿{ЧАШкск} {ЧАШмн} más necesitan para el muro que para el camino? {r}: {n} − {k} = {r}.",
               теперь_список="{X} tenía {n} {ФИГn}. también recibió {k} {МЕЛk}. ahora tiene {n} {ФИГn} y {k} {МЕЛk}. ¿cuántas cosas tiene en total? {s}: {n} + {k} = {s}.",
               добавил="{X} tenía {n} {ПРИЛn} en el álbum. añadió {k} {ПРИЛмн} nuevas. ¿{ПРИЛкск} {ПРИЛмн} tiene ahora? {s}: {n} + {k} = {s}."),
    "it": dict(
               больше_чем="{X} ha piantato {n} {ОТЖn}. {Y} ha piantato {k} {ОТЖмн} in più di {X}. {ОТЖкск} {ОТЖмн} ha piantato {Y}? {s}: {n} + {k} = {s}.",
               меньше_чем="{X} ha piantato {n} {ОТЖn}. {Y} ha piantato {k} {ОТЖмн} in meno di {X}. {ОТЖкск} {ОТЖмн} ha piantato {Y}? {r}: {n} − {k} = {r}.",
               добавил_на_полку="{X} aveva {n} {ФИГn} in dispensa. più tardi ha messo altri {k} {ФИГмн} in dispensa. {ФИГкск} {ФИГмн} ci sono ora in dispensa? {s}: {n} + {k} = {s}.",
               выбросил="{X} ha raccolto {n} {КРЫШn} nel bosco e ne ha buttati {k} cattivi. {КРЫШкск} {КРЫШмн} in più ha raccolto rispetto a quelli buttati? {r}: {n} − {k} = {r}.",
               выбросил_розы="nel cesto c'erano {n} {РОЗn}. {X} ha buttato {k} {РОЗмн} dal cesto. {РОЗкск} {РОЗмн} ci sono ora nel cesto? {r}: {n} − {k} = {r}.",
               узнал="{X} ha contato che il primo giorno al museo sono venuti {n} {ПОСn} e il secondo giorno {k}. {ПОСкск} {ПОСмн} sono venuti in tutto? {s}: {n} + {k} = {s}.",
               сели_вышли="sullo stagno c'erano {n} {ДЕТn}. {k} {ДЕТмн} si sono posate sullo stagno mentre alcune sono volate via. ora ci sono {s} {ДЕТмн} sullo stagno. {ДЕТкск} {ДЕТмн} sono volate via? {k2}: {n} + {k} − {s} = {k2}.",
               сыграл="{X} ha raccolto {n} {ИГРn} lunedì e {k} {ИГРмн} martedì. {ИГРкск} {ИГРмн} ha raccolto {X} in tutto? {s}: {n} + {k} = {s}.",
               потратил="{X} ha dedicato {n} {ЧАСn} al disegno e {k} {ЧАСмн} agli scacchi. {ЧАСкск} {ЧАСмн} ha dedicato {X} in tutto? un totale di {s} {ЧАСмн}: {n} + {k} = {s}.",
               список="ogni giorno {X} dedica {n} {ЧАСn} al disegno, {k} {ЧАСмн} agli scacchi e {m} {ЧАСмн} alla lettura. {ЧАСкск} {ЧАСмн} dedica {X} in tutto? {t}: {n} + {k} + {m} = {t}.",
               коробка="{X} ha ricevuto un sacchetto di {n} {МЕЛn} e un sacchetto di {k} {МЕЛмн}. {МЕЛкск} {МЕЛмн} ha {X}? {s}: {n} + {k} = {s}.",
               главы="un treno ha 2 vagoni. il primo vagone ha {n} {СТРn} e il secondo {k} {СТРмн}. {СТРкск} {СТРмн} ha il treno in tutto? {s}: {n} + {k} = {s}.",
               две_клаузы="{X} aveva {n} {ИГРn} e {Y} aveva {k} {ИГРмн}. {ИГРкск} {ИГРмн} avevano insieme? {s}: {n} + {k} = {s}.",
               сделал="{X} ha piantato {n} {ОТЖn} e {k} {СКРk}. {ОТЖкск} {ОТЖмн} ha piantato {X}? {n}. {УПРкск} {УПРмн} in tutto? {s} {УПРs}: {n} + {k} = {s}.",
               вещи3="{X} ha {n} {ФИГn}, {k} {МЕЛk} e {m} {ИГРm}. quante cose ha {X} in tutto? {t}: {n} + {k} + {m} = {t}.",
               продал="{X} aveva {n} {РОЗn}. ha venduto {k} {РОЗk}. {РОЗкск} {РОЗмн} ha ancora? {r}: {n} − {k} = {r}.",
               присоединились="c'erano {n} {ДЕТn} sul lago. si sono unite a loro altre {k} {ДЕТk}. {ДЕТкск} {ДЕТмн} ci sono ora sul lago? {s}: {n} + {k} = {s}.",
               жили="{n} {ЖИЛn} vivevano nell'alveare. {k} {ЖИЛk} sono volate via. {ЖИЛкск} {ЖИЛмн} vivono ora nell'alveare? {r}: {n} − {k} = {r}.",
               предложил="{X} ha portato {n} {ФИГn} in cantina. {Y} ne ha tolti {k}. {ФИГкск} {ФИГмн} restano? {r}: {n} − {k} = {r}.",
               в_школе="in una fattoria ci sono {n} {ДЕВn} e {k} {МАЛk}. quanti animali ci sono nella fattoria? {s}: {n} + {k} = {s}.",
               рецепт="i muratori hanno bisogno di {n} {ЧАШn} per il muro e di {k} {ЧАШk} per il vialetto. {ЧАШкск} {ЧАШмн} in più servono per il muro rispetto al vialetto? {r}: {n} − {k} = {r}.",
               теперь_список="{X} aveva {n} {ФИГn}. ha ricevuto anche {k} {МЕЛk}. ora ha {n} {ФИГn} e {k} {МЕЛk}. quante cose ha in tutto? {s}: {n} + {k} = {s}.",
               добавил="{X} aveva {n} {ПРИЛn} nell'album. ha aggiunto {k} nuove {ПРИЛмн}. {ПРИЛкск} {ПРИЛмн} ha adesso? {s}: {n} + {k} = {s}."),
    "pt": dict(
               больше_чем="{X} plantou {n} {ОТЖn}. {Y} plantou mais {k} {ОТЖмн} do que {X}. {ОТЖкск} {ОТЖмн} plantou {Y}? {s}: {n} + {k} = {s}.",
               меньше_чем="{X} plantou {n} {ОТЖn}. {Y} plantou menos {k} {ОТЖмн} do que {X}. {ОТЖкск} {ОТЖмн} plantou {Y}? {r}: {n} − {k} = {r}.",
               добавил_на_полку="{X} tinha {n} {ФИГn} na despensa. mais tarde pôs mais {k} {ФИГмн} na despensa. {ФИГкск} {ФИГмн} há agora na despensa? {s}: {n} + {k} = {s}.",
               выбросил="{X} apanhou {n} {КРЫШn} na floresta e deitou fora {k} estragados. {КРЫШкск} {КРЫШмн} a mais apanhou do que deitou fora? {r}: {n} − {k} = {r}.",
               выбросил_розы="havia {n} {РОЗn} no cesto. {X} deitou fora {k} {РОЗмн} do cesto. {РОЗкск} {РОЗмн} há agora no cesto? {r}: {n} − {k} = {r}.",
               узнал="{X} contou que no primeiro dia vieram {n} {ПОСn} ao museu e no segundo dia {k}. {ПОСкск} {ПОСмн} vieram no total? {s}: {n} + {k} = {s}.",
               сели_вышли="havia {n} {ДЕТn} na lagoa. {k} {ДЕТмн} pousaram na lagoa enquanto alguns voaram. agora há {s} {ДЕТмн} na lagoa. {ДЕТкск} {ДЕТмн} voaram? {k2}: {n} + {k} − {s} = {k2}.",
               сыграл="{X} juntou {n} {ИГРn} na segunda-feira e {k} {ИГРмн} na terça-feira. {ИГРкск} {ИГРмн} juntou {X} no total? {s}: {n} + {k} = {s}.",
               потратил="{X} gastou {n} {ЧАСn} com desenho e {k} {ЧАСмн} com xadrez. {ЧАСкск} {ЧАСмн} gastou {X} no total? um total de {s} {ЧАСмн}: {n} + {k} = {s}.",
               список="todos os dias {X} gasta {n} {ЧАСn} com desenho, {k} {ЧАСмн} com xadrez e {m} {ЧАСмн} com leitura. {ЧАСкск} {ЧАСмн} gasta {X} no total? {t}: {n} + {k} + {m} = {t}.",
               коробка="{X} recebeu um saco com {n} {МЕЛn} e um saco com {k} {МЕЛмн}. {МЕЛкск} {МЕЛмн} tem {X}? {s}: {n} + {k} = {s}.",
               главы="um comboio tem 2 carruagens. a primeira carruagem tem {n} {СТРn} e a segunda {k} {СТРмн}. {СТРкск} {СТРмн} tem o comboio no total? {s}: {n} + {k} = {s}.",
               две_клаузы="{X} tinha {n} {ИГРn} e {Y} tinha {k} {ИГРмн}. {ИГРкск} {ИГРмн} tinham juntos? {s}: {n} + {k} = {s}.",
               сделал="{X} plantou {n} {ОТЖn} e {k} {СКРk}. {ОТЖкск} {ОТЖмн} plantou {X}? {n}. {УПРкск} {УПРмн} no total? {s} {УПРs}: {n} + {k} = {s}.",
               вещи3="{X} tem {n} {ФИГn}, {k} {МЕЛk} e {m} {ИГРm}. quantas coisas tem {X} ao todo? {t}: {n} + {k} + {m} = {t}.",
               продал="{X} tinha {n} {РОЗn}. vendeu {k} {РОЗk}. {РОЗкск} {РОЗмн} lhe restam? {r}: {n} − {k} = {r}.",
               присоединились="havia {n} {ДЕТn} no lago. juntaram-se a eles mais {k} {ДЕТk}. {ДЕТкск} {ДЕТмн} há agora no lago? {s}: {n} + {k} = {s}.",
               жили="{n} {ЖИЛn} viviam na colmeia. {k} {ЖИЛk} voaram. {ЖИЛкск} {ЖИЛмн} vivem agora na colmeia? {r}: {n} − {k} = {r}.",
               предложил="{X} levou {n} {ФИГn} para a cave. {Y} retirou {k} deles. {ФИГкск} {ФИГмн} restam? {r}: {n} − {k} = {r}.",
               в_школе="numa quinta há {n} {ДЕВn} e {k} {МАЛk}. quantos animais há na quinta? {s}: {n} + {k} = {s}.",
               рецепт="os pedreiros precisam de {n} {ЧАШn} para o muro e de {k} {ЧАШk} para o caminho. {ЧАШкск} {ЧАШмн} a mais precisam para o muro do que para o caminho? {r}: {n} − {k} = {r}.",
               теперь_список="{X} tinha {n} {ФИГn}. também recebeu {k} {МЕЛk}. agora tem {n} {ФИГn} e {k} {МЕЛk}. quantas coisas tem ao todo? {s}: {n} + {k} = {s}.",
               добавил="{X} tinha {n} {ПРИЛn} no álbum. adicionou {k} {ПРИЛмн} novas. {ПРИЛкск} {ПРИЛмн} tem agora? {s}: {n} + {k} = {s}."),
    "nl": dict(
               больше_чем="{X} plantte {n} {ОТЖn}. {Y} plantte {k} {ОТЖмн} meer dan {X}. hoeveel {ОТЖмн} plantte {Y}? {s}: {n} + {k} = {s}.",
               меньше_чем="{X} plantte {n} {ОТЖn}. {Y} plantte {k} {ОТЖмн} minder dan {X}. hoeveel {ОТЖмн} plantte {Y}? {r}: {n} − {k} = {r}.",
               добавил_на_полку="{X} had {n} {ФИГn} in de voorraadkast. later zette {он} er {k} {ФИГмн} bij in de voorraadkast. hoeveel {ФИГмн} staan er nu in de voorraadkast? {s}: {n} + {k} = {s}.",
               выбросил="{X} plukte {n} {КРЫШn} in het bos en gooide er {k} slechte weg. hoeveel {КРЫШмн} meer plukte {он} dan {он} weggooide? {r}: {n} − {k} = {r}.",
               выбросил_розы="er lagen {n} {РОЗn} in de mand. {X} gooide {k} {РОЗмн} uit de mand weg. hoeveel {РОЗмн} liggen er nu in de mand? {r}: {n} − {k} = {r}.",
               узнал="{X} telde dat er op de eerste dag {n} {ПОСn} naar het museum kwamen en op de tweede dag {k}. hoeveel {ПОСмн} kwamen er in totaal? {s}: {n} + {k} = {s}.",
               сели_вышли="er zwommen {n} {ДЕТn} op de vijver. {k} {ДЕТмн} landden op de vijver terwijl er een paar wegvlogen. nu zwemmen er {s} {ДЕТмн} op de vijver. hoeveel {ДЕТмн} vlogen weg? {k2}: {n} + {k} − {s} = {k2}.",
               сыграл="{X} verzamelde {n} {ИГРn} op maandag en {k} {ИГРмн} op dinsdag. hoeveel {ИГРмн} verzamelde {X} in totaal? {s}: {n} + {k} = {s}.",
               потратил="{X} besteedde {n} {ЧАСn} aan tekenen en {k} {ЧАСмн} aan schaken. hoeveel {ЧАСмн} besteedde {X} in totaal? in totaal {s} {ЧАСмн}: {n} + {k} = {s}.",
               список="elke dag besteedt {X} {n} {ЧАСn} aan tekenen, {k} {ЧАСмн} aan schaken en {m} {ЧАСмн} aan lezen. hoeveel {ЧАСмн} besteedt {X} in totaal? {t}: {n} + {k} + {m} = {t}.",
               коробка="{X} kreeg een zakje met {n} {МЕЛn} en een zakje met {k} {МЕЛмн}. hoeveel {МЕЛмн} heeft {X}? {s}: {n} + {k} = {s}.",
               главы="een trein heeft 2 wagons. de eerste wagon heeft {n} {СТРn} en de tweede {k} {СТРмн}. hoeveel {СТРмн} heeft de trein in totaal? {s}: {n} + {k} = {s}.",
               две_клаузы="{X} had {n} {ИГРn} en {Y} had {k} {ИГРмн}. hoeveel {ИГРмн} hadden ze samen? {s}: {n} + {k} = {s}.",
               сделал="{X} plantte {n} {ОТЖn} en {k} {СКРk}. hoeveel {ОТЖмн} plantte {X}? {n}. hoeveel {УПРмн} in totaal? {s} {УПРs}: {n} + {k} = {s}.",
               вещи3="{X} heeft {n} {ФИГn}, {k} {МЕЛk} en {m} {ИГРm}. hoeveel dingen heeft {X} in totaal? {t}: {n} + {k} + {m} = {t}.",
               продал="{X} had {n} {РОЗn}. {он} verkocht {k} {РОЗk}. hoeveel {РОЗмн} heeft {он} nog? {r}: {n} − {k} = {r}.",
               присоединились="er zwommen {n} {ДЕТn} op het meer. er kwamen nog {k} {ДЕТk} bij. hoeveel {ДЕТмн} zijn er nu op het meer? {s}: {n} + {k} = {s}.",
               жили="er woonden {n} {ЖИЛn} in de bijenkorf. {k} {ЖИЛk} vlogen weg. hoeveel {ЖИЛмн} wonen er nu in de bijenkorf? {r}: {n} − {k} = {r}.",
               предложил="{X} bracht {n} {ФИГn} naar de kelder. {Y} haalde er {k} weg. hoeveel {ФИГмн} blijven er over? {r}: {n} − {k} = {r}.",
               в_школе="op een boerderij zijn er {n} {ДЕВn} en {k} {МАЛk}. hoeveel dieren zijn er op de boerderij? {s}: {n} + {k} = {s}.",
               рецепт="de metselaars hebben {n} {ЧАШn} nodig voor de muur en {k} {ЧАШk} voor het pad. hoeveel {ЧАШмн} meer hebben ze nodig voor de muur dan voor het pad? {r}: {n} − {k} = {r}.",
               теперь_список="{X} had {n} {ФИГn}. {он} kreeg ook {k} {МЕЛk}. nu heeft {он} {n} {ФИГn} en {k} {МЕЛk}. hoeveel dingen heeft {он} in totaal? {s}: {n} + {k} = {s}.",
               добавил="{X} had {n} {ПРИЛn} in het album. {он} voegde {k} nieuwe {ПРИЛмн} toe. hoeveel {ПРИЛмн} heeft {он} nu? {s}: {n} + {k} = {s}."),
    "pl": dict(
               больше_чем="{X} posadził{а} {n} {ОТЖn}. {Y} posadził{аY} o {k} {ОТЖk} więcej niż {X}. ile {ОТЖмн} posadził{аY} {Y}? {s}: {n} + {k} = {s}.",
               меньше_чем="{X} posadził{а} {n} {ОТЖn}. {Y} posadził{аY} o {k} {ОТЖk} mniej niż {X}. ile {ОТЖмн} posadził{аY} {Y}? {r}: {n} − {k} = {r}.",
               добавил_на_полку="{X} miał{а} {n} {ФИГn} w spiżarni. potem postawił{а} w spiżarni jeszcze {k} {ФИГk}. ile {ФИГмн} jest teraz w spiżarni? {s}: {n} + {k} = {s}.",
               выбросил="{X} zebrał{а} w lesie {n} {КРЫШn}, a {k} z nich wyrzucił{а}. o ile więcej {КРЫШмн} zebrał{а}, niż wyrzucił{а}? {r}: {n} − {k} = {r}.",
               выбросил_розы="{X} miał{а} w koszyku {n} {РОЗn}. wyrzucił{а} z koszyka {k} {РОЗk}. ile {РОЗмн} jest teraz w koszyku? {r}: {n} − {k} = {r}.",
               узнал="{X} policzył{а}, że pierwszego dnia do muzeum przyszło {n} {ПОСn}, a drugiego {k}. ilu {ПОСмн} przyszło razem? {s}: {n} + {k} = {s}.",
               сели_вышли="{X} naliczył{а} na stawie {n} {ДЕТn}. potem zwabił{а} jeszcze {k} {ДЕТk}, a kilka odleciało. teraz naliczył{а} {s} {ДЕТs}. ile {ДЕТмн} odleciało? {k2}: {n} + {k} − {s} = {k2}.",
               сыграл="{X} zebrał{а} {n} {ИГРn} w poniedziałek i {k} {ИГРk} we wtorek. ile {ИГРмн} zebrał{а} {X} razem? {s}: {n} + {k} = {s}.",
               потратил="{X} spędził{а} {n} {ЧАСn} na rysowaniu i {k} {ЧАСk} na szachach. ile {ЧАСмн} spędził{а} {X} razem? razem {s} {ЧАСs}: {n} + {k} = {s}.",
               список="codziennie {X} spędza {n} {ЧАСn} na rysowaniu, {k} {ЧАСk} na szachach i {m} {ЧАСm} na czytaniu. ile {ЧАСмн} spędza {X} razem? {t}: {n} + {k} + {m} = {t}.",
               коробка="{X} dostał{а} torbę z {n} {МЕЛпр} i torbę z {k} {МЕЛпр}. ile {МЕЛмн} ma {X}? {s}: {n} + {k} = {s}.",
               главы="pociąg ma 2 wagony. pierwszy wagon ma {n} {СТРn}, a drugi {k} {СТРk}. ile {СТРмн} ma pociąg razem? {s}: {n} + {k} = {s}.",
               две_клаузы="{X} miał{а} {n} {ИГРn}, a {Y} miał{аY} {k} {ИГРk}. ile {ИГРмн} mieli razem? {s}: {n} + {k} = {s}.",
               сделал="{X} posadził{а} {n} {ОТЖn} i {k} {СКРk}. ile {ОТЖмн} posadził{а} {X}? {n}. ile {УПРмн} razem? {s} {УПРs}: {n} + {k} = {s}.",
               вещи3="{X} ma {n} {ФИГn}, {k} {МЕЛk} i {m} {ИГРm}. ile rzeczy ma {X} razem? {t}: {n} + {k} + {m} = {t}.",
               продал="{X} miał{а} {n} {РОЗn}. sprzedał{а} {k} {РОЗk}. ile {РОЗмн} ma teraz? {r}: {n} − {k} = {r}.",
               присоединились="{X} naliczył{а} na jeziorze {n} {ДЕТn}. potem zobaczył{а} jeszcze {k} {ДЕТk}. ile {ДЕТмн} jest teraz na jeziorze? {s}: {n} + {k} = {s}.",
               жили="{X} miał{а} w ulu {n} {ЖИЛn}. wypuścił{а} {k} z nich. ile {ЖИЛмн} jest teraz w ulu? {r}: {n} − {k} = {r}.",
               предложил="{X} postawił{а} w piwnicy {n} {ФИГn}. {Y} zabrał{аY} {k} z nich. ile {ФИГмн} zostało? {r}: {n} − {k} = {r}.",
               в_школе="{X} ma w gospodarstwie {n} {ДЕВn} i {k} {МАЛk}. ile zwierząt ma {X} w gospodarstwie? {s}: {n} + {k} = {s}.",
               рецепт="budowlańcy zamówili {n} {ЧАШn} na mur i {k} {ЧАШk} na ścieżkę. o ile więcej {ЧАШмн} zamówili na mur niż na ścieżkę? {r}: {n} − {k} = {r}.",
               теперь_список="{X} miał{а} {n} {ФИГn}. dostał{а} też {k} {МЕЛk}. teraz ma {n} {ФИГn} i {k} {МЕЛk}. ile rzeczy ma razem? {s}: {n} + {k} = {s}.",
               добавил="{X} miał{а} {n} {ПРИЛn} w albumie. dodał{а} {k} {НОВk} {ПРИЛk}. ile {ПРИЛмн} ma teraz? {s}: {n} + {k} = {s}."),
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
    "en": (("on drawing", "on chess"), ("on music", "on history"),
           ("on chemistry", "on geography"), ("on physics", "on biology")),
    "ru": (("на рисование", "на шахматы"), ("на музыку", "на историю"),
           ("на химию", "на географию"), ("на физику", "на биологию")),
    "de": (("mit Zeichnen", "mit Schach"), ("mit Musik", "mit Geschichte"),
           ("mit Chemie", "mit Erdkunde"), ("mit Physik", "mit Biologie")),
    "fr": (("sur le dessin", "sur les échecs"), ("sur la musique", "sur l'histoire"),
           ("sur la chimie", "sur la géographie"), ("sur la physique", "sur la biologie")),
    "es": (("al dibujo", "al ajedrez"), ("a la música", "a la historia"),
           ("a la química", "a la geografía"), ("a la física", "a la biología")),
    "it": (("al disegno", "agli scacchi"), ("alla musica", "alla storia"),
           ("alla chimica", "alla geografia"), ("alla fisica", "alla biologia")),
    "pt": (("com desenho", "com xadrez"), ("com música", "com história"),
           ("com química", "com geografia"), ("com física", "com biologia")),
    "nl": (("aan tekenen", "aan schaken"), ("aan muziek", "aan geschiedenis"),
           ("aan scheikunde", "aan aardrijkskunde"), ("aan natuurkunde", "aan biologie")),
    "pl": (("na rysowaniu", "na szachach"), ("na muzyce", "na historii"),
           ("na chemii", "na geografii"), ("na fizyce", "na biologii")),
}
for _яз, _ряд in ЦЕЛИ_ТРАТЫ.items():
    _рамка = РАМКИ_АКТОВ[_яз]["потратил"]
    _перв_a, _перв_b = _ряд[0]
    assert _перв_a in _рамка and _перв_b in _рамка, (_яз, _рамка)
    РАМКИ_АКТОВ[_яз]["потратил"] = tuple(
        _рамка.replace(_перв_a, _a).replace(_перв_b, _b) for _a, _b in _ряд)


# СОВМЕСТИМЫЕ ТОВАРЫ РАМКИ АКТА — рука, и сказано, что рука (13.09).
#
# ТОВАР В РАМКЕ УЖЕ ПАРАМЕТР: дыры «{ЖИЛn}», «{ЖИЛk}», «{ЖИЛмн}» берут счётные формы законом,
# и подмена товара даёт правильные формы на всех девяти языках сама. Жёстко привязана не проза,
# а ОДНА СТРОКА таблицы `_ТОВАР_ПО_ДЫРЕ`: дыра → один товар навсегда.
#
#     ПАРАМЕТР, ПРИВЯЗАННЫЙ К ОДНОМУ ЗНАЧЕНИЮ, НЕОТЛИЧИМ ОТ КОНСТАНТЫ, ПОКА НЕ ПОПРОБУЕШЬ
#     ВТОРОЕ ЗНАЧЕНИЕ.
#
# ГРАММАТИКА СВОБОДНА, СМЫСЛ — НЕТ. «24 visitors were living in the house» верно, «24 hours
# were living in the house» — вздор, и обе строки грамматически безупречны. Оттого совместимость
# объявляется РУКОЙ и порознь для каждой рамки: она есть знание о мире, а не о языке, и вывести
# её из пакетов нельзя.
#
#     СОВМЕСТИМОСТЬ ТОВАРА С РАМКОЙ ЕСТЬ УТВЕРЖДЕНИЕ О МИРЕ. Дом, выводящий её из таблиц языка,
#     скажет «двадцать четыре часа жили в доме» и будет прав по всякому суду формы.
#
# ДВА ЧЛЕНА РЯДА ОТНЯТЫ ГЛАЗОМ, А НЕ ПРАВИЛОМ (13.09, при первом же чтении страниц). «В
# автобусе было 12 посетителей» и «во дворец пришли 12 жильцов» — обе грамматически чисты и
# обе вздор: ЖИЛЕЦ определён тем, ГДЕ ЖИВЁТ, а ПОСЕТИТЕЛЬ — тем, КУДА ПРИШЁЛ, и потому ни
# один не переносится в чужую сцену. Заменены на девочек и мальчиков, у которых роли нет.
#
#     ТОВАР, ЧЬЁ ИМЯ НЕСЁТ РОЛЬ, НЕ ПЕРЕНОСИТСЯ В СЦЕНУ ДРУГОЙ РОЛИ. Совместимость проверяется
#     ЧТЕНИЕМ страниц, а не таблицей: таблица говорит, что можно построить, глаз — что можно
#     сказать.
#
# ПЕРВЫЙ ТОВАР ВСЯКОГО РЯДА — ПРЕЖНИЙ, и оттого прежние страницы остаются на месте: ряд лишь
# добавляет, а не заменяет. Рамки, у которых товар один, здесь не стоя́т вовсе — им нечего
# добавить, и молчание о них честнее пустого ряда.
СОВМЕСТИМЫЕ = {
    "продал":           {"РОЗ": ("груши", "банки", "орехи")},
    "две_клаузы":       {"ИГР": ("марки", "банки", "орехи")},
    "больше_чем":       {"ОТЖ": ("дубы", "берёзы", "деревья")},
    "меньше_чем":       {"ОТЖ": ("дубы", "берёзы", "деревья")},
}
# НЕ ВАРЬИРУЮТСЯ И ПОЧЕМУ:
#   выбросил_розы  — «в корзине» держит плоды;
#   выбросил       — «собрал в лесу» держит грибы;
#   сыграл         — «собрал по дням» держит марки коллекции;
#   добавил        — «фотографии в альбоме» держат только фотографии;
#   главы          — «вагон на столько-то мест» держит только места;
#   рецепт         — «кирпичи для стены и дорожки» держат только кирпичи;
#   потратил, список — «часы на занятие» держат только часы;
#   присоединились, сели_вышли — «на озере», «на пруду»: у уток и гусей разный род, и
#       причастия романских рамок («se sont posés», «si sono posate») разошлись бы с ним;
#   жили           — «улей» держит только пчёл;
#   вещи3, в_школе, сделал — рамки с ДВУМЯ и ТРЕМЯ товарами разом: подмена там меняет не товар,
#       а состав сцены, и это другая работа.


# СТРАЖ РЯДА СТОИ́Т ПРИ ВВОЗЕ, А НЕ В САМОПРОВЕРКЕ (13.09). Страницы строятся при ввозе дома,
# и товар, не несущий всего, что несёт прежний, роняет ВВОЗ, а не проверку: до самопроверки
# дело не дойдёт. Первая редакция ряда дала рамке «коробка» три товара — а рамка та берёт
# дыру «{МЕЛпр}» (товар при предлоге), и форму эту объявляют лишь мелки и лишь на трёх
# языках. Дом не смог ввезтись вовсе.
#
#     ТОВАР, ПОДМЕНЯЮЩИЙ ДРУГОЙ, ОБЯЗАН НЕСТИ ВСЁ, ЧТО НЕСЁТ ПОДМЕНЯЕМЫЙ, — не только счётные
#     формы, но и всякую особую, какую рамка спросит. Ряд, где это не так, есть обещание
#     страниц, которых не построить.
for _ф, _ряд in СОВМЕСТИМЫЕ.items():
    for _дыра, _товары in _ряд.items():
        _свой = _ТОВАР_ПО_ДЫРЕ[_дыра]
        # ПЕРВЫЙ ЧЛЕН РЯДА — ПРЕЖНИЙ ТОВАР, И ЭТО СТЕРЕЖЁТСЯ, А НЕ ПОДРАЗУМЕВАЕТСЯ. Переставь
        # ряд местами — и прежние страницы дома пропадут, а всякая мера, знавшая их, назовёт
        # это потерей. РЯД, ПРИБАВЛЯЮЩИЙ К ПРЕЖНЕМУ, ОБЯЗАН НАЧИНАТЬСЯ ПРЕЖНИМ.
        assert _товары and _товары[0] == _свой, (_ф, _дыра, _товары[0], _свой)
        assert len(set(_товары)) == len(_товары), (_ф, _дыра, "товар повторён в ряду")
        for _т in _товары:
            for _яз, _таб in ТОВАРЫ_АКТОВ.items():
                assert _т in _таб, (_ф, _т, _яз, "товара нет в таблице языка")
            for _яз, _таб in ПРИ_ПРЕДЛОГЕ.items():
                assert (_свой in _таб) <= (_т in _таб), (_ф, _т, _яз, "нет формы при предлоге")


ФОРМЫ_АКТОВ = tuple(РАМКИ_АКТОВ["en"])
ЧИСЛА_АКТОВ = ((12, 5, 4), (35, 3, 9), (20, 8, 6), (15, 7, 2), (30, 12, 10), (9, 4, 3), (18, 11, 5), (24, 15, 7))
# THE ADJECTIVE BENDS WITH THE COUNT FORM where the language bends it (BESEDA-11, pl: «dodała 5
# nowych aplikacji» — the seven other languages carry «new» as one word inside the frame)
НОВЫЕ = {"pl": ("nowe", "nowe", "nowych")}


def _товар_форма(язык, ключ, c):
    return _счёт(ТОВАРЫ_АКТОВ[язык][ключ], c, язык)


def _поля_акта(язык, i, j, n, k, m, товары=None):
    X, Y = _лицо(язык, i), _лицо(язык, j)
    if Y[0] == X[0]:
        Y = _лицо(язык, j + 1)
    мест = МЕСТОИМЕНИЯ[язык][X[1]]
    мест_Y = МЕСТОИМЕНИЯ[язык][Y[1]]
    п = dict(X=X[0], Xр=X[2], Y=Y[0], Yр=Y[2], он=мест["он"], Он=мест["он"], него=мест["него"], аY_он=мест_Y["он"],
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
    for дыра, свой in _ТОВАР_ПО_ДЫРЕ.items():
        # ПОДМЕНА ТОВАРА — ДЛЯ ОДНОЙ СТРАНИЦЫ И ТОЛЬКО ПО ОБЪЯВЛЕНИЮ РАМКИ. Где подмены нет,
        # берётся прежний товар, и страница выходит той же, что и до сего дня.
        ключ = (товары or {}).get(дыра, свой)
        if ключ not in ТОВАРЫ_АКТОВ[язык]:
            continue
        п[дыра + "n"] = _товар_форма(язык, ключ, n); п[дыра + "k"] = _товар_форма(язык, ключ, k)
        п[дыра + "m"] = _товар_форма(язык, ключ, m); п[дыра + "s"] = _товар_форма(язык, ключ, n + k)
        п[дыра + "мн"] = ТОВАРЫ_АКТОВ[язык][ключ][-1]
        # ВОПРОСНОЕ СЛОВО ПРИ ТОВАРЕ — ДЫРА, А НЕ БУКВА: род берётся у СЛОВА, СТОЯЩЕГО В
        # СТРОКЕ, и потому переживает подмену товара. Языков, гнущих его, три; прочие шесть
        # этой дыры не просят, и лишний ключ формату не мешает.
        пара = РОДОВЫЕ.get(язык, {}).get({"es": "кск", "it": "quante", "pt": "quantas"}.get(язык))
        if пара is not None:
            род_ = РОД_ТОВАРА_АКТОВ[язык][ТОВАРЫ_АКТОВ[язык][ключ][-1]]
            п[дыра + "кск"] = пара[0] if род_ == "m" else пара[1]
        если = ПРИ_ПРЕДЛОГЕ.get(язык, {}).get(ключ)
        if если is not None:
            п[дыра + "пр"] = если
    return п


def страница_акта(язык, форма, i, j, n, k, m=4, имя=False, вариант=0, середина=False,
                  товары=None):
    """Готовая страница акта — С ТОЙ ЖЕ ЭЛИЗИЕЙ, что и прочие (12.09).

    ВТОРОЙ СТРОИТЕЛЬ ДОМА ТРЕБУЕТ ТОГО ЖЕ ЗАКОНА, ЧТО И ПЕРВЫЙ. Обёртка легла на
    `страница`, а страницы актов идут мимо неё — и «de moins que Anne» осталось
    стоять, когда всё прочее стало «qu'Anne».

        ЗАКОН, ПРИМЕНЁННЫЙ К ОДНОМУ СТРОИТЕЛЮ ДОМА, НЕ ПРИМЕНЁН К ДРУГОМУ.
    """
    готовая = _страница_акта_сырая(язык, форма, i, j, n, k, m, имя, вариант, середина,
                                   товары)
    return _fr.элизия(готовая) if язык == "fr" and готовая else готовая


def _страница_акта_сырая(язык, форма, i, j, n, k, m=4, имя=False, вариант=0,
                         середина=False, товары=None):
    р = РАМКИ_АКТОВ[язык][форма]
    if середина:
        р = близнец_середины(язык, р)
        if р is None:
            return None
        п = _поля_акта(язык, i, j, n, k, m, товары)
        if форма == "сели_вышли":
            # ТОВАР БЕРЁТСЯ ИЗ ПОДМЕНЫ, А НЕ ИЗ ИМЕНИ, ВПИСАННОГО РУКОЙ (13.09):
            # «в автобусе было 12 девочек… теперь в автобусе 15 ДЕТЕЙ» — хвост рамки
            # звал прежний товар и менял вещь посреди истории.
            #
            #     ПОДМЕНА, СДЕЛАННАЯ НЕ ВЕЗДЕ, ХУЖЕ НЕСДЕЛАННОЙ: она не оставляет
            #     страницу прежней и не делает её новой, а рвёт её пополам.
            п = dict(п, s=п["s_бус"],
                     ДЕТs=_товар_форма(язык, (товары or {}).get("ДЕТ", _ТОВАР_ПО_ДЫРЕ["ДЕТ"]),
                                       п["s_бус"]))
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
    п = _поля_акта(язык, i, j, n, k, m, товары)
    if форма == "сели_вышли":
        # ТОВАР БЕРЁТСЯ ИЗ ПОДМЕНЫ, А НЕ ИЗ ИМЕНИ, ВПИСАННОГО РУКОЙ (13.09):
        # «в автобусе было 12 девочек… теперь в автобусе 15 ДЕТЕЙ» — хвост рамки
        # звал прежний товар и менял вещь посреди истории.
        #
        #     ПОДМЕНА, СДЕЛАННАЯ НЕ ВЕЗДЕ, ХУЖЕ НЕСДЕЛАННОЙ: она не оставляет
        #     страницу прежней и не делает её новой, а рвёт её пополам.
        п = dict(п, s=п["s_бус"],
                 ДЕТs=_товар_форма(язык, (товары or {}).get("ДЕТ", _ТОВАР_ПО_ДЫРЕ["ДЕТ"]),
                                   п["s_бус"]))
    return р.format(**п)


def подмены(форма):
    """[{дыра: товар}] — ряд подмен для рамки; ПЕРВАЯ ПУСТА, и прежние страницы не двигаются.

        РЯД, У КОТОРОГО ПЕРВЫЙ ЧЛЕН ЕСТЬ ПРЕЖНЕЕ, ПРИБАВЛЯЕТ И НЕ ЗАМЕЩАЕТ. Иначе всякая
        мера, знавшая старую страницу, найдёт её пропавшей и назовёт это потерей.
    """
    ряд = СОВМЕСТИМЫЕ.get(форма)
    if not ряд:
        return [{}]
    (дыра, товары), = ряд.items()
    return [{} if i == 0 else {дыра: т} for i, т in enumerate(товары)]


def _показы_актов():
    вон = {}
    for язык in РАМКИ_АКТОВ:
        лиц = len(A.ЛИЦА[язык])
        for форма in ФОРМЫ_АКТОВ:
            if форма not in РАМКИ_АКТОВ[язык]:
                continue
            р = РАМКИ_АКТОВ[язык][форма]
            вариантов = len(р) if isinstance(р, tuple) else 1
            for товары in подмены(форма):
                for q, (n, k, m) in enumerate(ЧИСЛА_АКТОВ):
                    for вариант in range(вариантов):
                        с = страница_акта(язык, форма, q % лиц, (q * 3 + 1) % лиц, n, k, m,
                                          вариант=вариант, товары=товары)
                        if с:
                            вон[с] = (язык, форма)
                    с = страница_акта(язык, форма, q % лиц, (q * 3 + 1) % лиц, n, k, m,
                                      имя=True, товары=товары)
                    if с:
                        вон[с] = (язык, форма)
                    с = страница_акта(язык, форма, q % лиц, (q * 3 + 1) % лиц, n, k, m,
                                      середина=True, товары=товары)
                    if с:
                        вон[с] = (язык, форма)
    return вон


ПОКАЗЫ.update(_показы_актов())

# ДОМ, ДЕРЖАЩИЙ СТРАНИЦЫ В ДВУХ ТАБЛИЦАХ, ОБЪЯВЛЯЕТ РОДЫ В ОДНОЙ (13.09): указатель
# родов читает `РОДЫ`, и всё, что кует дом, обязано быть в нём названо. Страница,
# кованная под родом вне объявления, живёт БЕЗ ИМЕНИ — она есть в мире и её нет в
# списке, и всякая мера покрытия считает её знаменателем чужого рода.
РОДЫ = ФОРМЫ + ФОРМЫ_АКТОВ            # тридцать девять рамок счёта и двадцать три акта


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
            # ВОПРОСНОЕ СЛОВО ПРИ ТОВАРЕ ЧИТАЕТСЯ ОДНОЙ ФОРМОЙ, А НЕ ОБЕИМИ: ячейка образца
            # принимает ТОЛЬКО тот род, какой объявлен у товара, — и потому подмена рода
            # становится НЕСУДИМОЙ, а ворота записи её не пропустят.
            #
            #     ДЕФЕКТ, СДЕЛАННЫЙ НЕВОЗМОЖНЫМ, ЛУЧШЕ ДЕФЕКТА ОБНАРУЖИМОГО: первый не
            #     доживает до свода, второй живёт до ближайшего прогона прибора.
            пара = РОДОВЫЕ.get(язык, {}).get({"es": "кск", "it": "quante", "pt": "quantas"}.get(язык))
            if пара is not None:
                род_ = РОД_ТОВАРА_АКТОВ[язык][ТОВАРЫ_АКТОВ[язык][ключ][-1]]
                дыры[дыра + "кск"] = alt((пара[0] if род_ == "m" else пара[1],))
            если = ПРИ_ПРЕДЛОГЕ.get(язык, {}).get(ключ)
            if если is not None:
                # НЕ alt(всех форм): падежная ячейка не принимает счётной
                дыры[дыра + "пр"] = alt((если,))
        for форма, рамка in рамки.items():
            поверхности = (list(рамка) if isinstance(рамка, tuple)
                           else [рамка, близнец(рамка), близнец_середины(язык, рамка)])
            # ОБРАЗЕЦ СТРОИТСЯ НА КАЖДУЮ ПОДМЕНУ ТОВАРА, А НЕ НА ОДНУ ПЕРВУЮ (21.09).
            #
            # Рамка акта берёт товар ПАРАМЕТРОМ, и дом пишет ею по ряду совместимых товаров:
            # «фигурки», «игры», «крышки». Образец же строился по таблице `_ТОВАР_ПО_ДЫРЕ`,
            # где дыра привязана к ОДНОМУ товару навсегда, — и 1 752 страницы дома не
            # совпадали ни с одним образцом, а держались выходом по набору.
            #
            #     ПАРАМЕТР, ПРИВЯЗАННЫЙ К ОДНОМУ ЗНАЧЕНИЮ, НЕОТЛИЧИМ ОТ КОНСТАНТЫ, ПОКА НЕ
            #     ПОПРОБУЕШЬ ВТОРОЕ ЗНАЧЕНИЕ. Здесь второе значение пробовало ПИСЬМО и не
            #     пробовало ЧТЕНИЕ — тот же разлад, что у рамки единичной нехватки и у рамок
            #     дома умолчания, найденный в тот же день трижды.
            for подмена in подмены(форма):
                свои = dict(дыры)
                for дыра_, товар_ in подмена.items():
                    формы_ = ТОВАРЫ_АКТОВ.get(язык, {}).get(товар_)
                    if not формы_:
                        continue
                    for суффикс in ("n", "k", "m", "s", "мн"):
                        свои[дыра_ + суффикс] = alt(формы_)
                    пара_ = РОДОВЫЕ.get(язык, {}).get(
                        {"es": "кск", "it": "quante", "pt": "quantas"}.get(язык))
                    if пара_ is not None:
                        род_ = РОД_ТОВАРА_АКТОВ[язык].get(формы_[-1])
                        if род_ is not None:
                            свои[дыра_ + "кск"] = alt((пара_[0] if род_ == "m" else пара_[1],))
                    если_ = ПРИ_ПРЕДЛОГЕ.get(язык, {}).get(товар_)
                    if если_ is not None:
                        свои[дыра_ + "пр"] = alt((если_,))
                _строить(вон, поверхности, свои, язык, форма)
    return вон


def _строить(вон, поверхности, дыры, язык, форма):
    """Собрать образцы всех поверхностей рамки при данном наборе дыр."""
    for р in поверхности:
                if р is None:
                    continue
                # ЭЛИЗИЯ СТОИТ НА СТЫКЕ КУСКА И ДЫРЫ, И ПОТОМУ ЭКРАНИРОВАНИЕ ЗНАЕТ О НЕЙ:
                # рамка говорит «de plus que {Y}», страница — «de plus qu'Anne», и образец,
                # писанный `re.escape`, не совпал бы с собственной страницей дома.
                _эк = _fr.в_образце if язык == "fr" else re.escape
                куски = [дыры[к[1:-1]] if к.startswith("{") else _эк(к) for к in re.split(r"(\{[^}]+\})", р)]
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
        # ШАГ ЦЕПИ КОРМИТСЯ ПРЕЖНИМ РЕЗУЛЬТАТОМ, НО НЕ ОБЯЗАН СТАВИТЬ ЕГО ПЕРВЫМ (21.09).
        # Первая редакция требовала «прежний ⊕ число истории» и тем знала лишь половину
        # цепей: род «доля_не» считает долю, а затем вычитает её ИЗ ИСХОДНОГО — «12 ÷ 2 = 6,
        # 12 − 6 = 6», — и прежний результат стои́т в нём вычитаемым. 444 честные страницы
        # на девяти языках закон звал ложью, а держались они выходом по набору.
        #
        #     ЦЕПЬ ЕСТЬ УТВЕРЖДЕНИЕ О ТОМ, ЧТО КАЖДЫЙ ШАГ КОРМИТСЯ ПРЕЖНИМ, А НЕ О ПОРЯДКЕ
        #     ОПЕРАНДОВ В НЁМ. Требовать первого места значит судить не закон, а привычку
        #     дома писать сложение раньше вычитания.
        #
        # Строгости не убавлено: прежний результат обязан участвовать в шаге, а второй
        # операнд — быть числом истории; шаг, где прежнего нет вовсе, по-прежнему ложь.
        elif not ((a == прежний and b in числа) or (b == прежний and a in числа)):
            return False
        прежний = v
    итог = re.findall(r"\d+", хвост)
    return bool(итог) and int(итог[-1]) == прежний


def _судить_образцом(строка):
    """(судимо, истинно): a page of the house, or a line of its frame whose ledger does not hold."""
    с = строка.strip()
    # ВЫХОД ПО НАБОРУ СНЯТ (21.09) — он укрывал 1 752 страницы, которых образец не знал
    # (товар взят параметром при письме и константой при чтении), и 444 страницы рода
    # «доля_не», которые закон цепи звал ложью. НАБОР ГОВОРИТ, ЧТО ДОМ СТРАНИЦУ
    # НАПИСАЛ, А НЕ ЧТО ОНА ВЕРНА. Замер: закон судит все 10 445 верно и без набора.
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
    # ВОПРОСНОЕ СЛОВО ТОВАРА, ПЕРЕВЁРНУТОЕ В ЧУЖОЙ РОД, ЕСТЬ ЛОЖЬ — на всякой странице товара трёх
    # гнущих языков (24.09); порча выводится из пары двери, а не пишется литералом.
    перевёрнуто = 0
    for показ, (язык, форма) in ПОКАЗЫ.items():
        if форма != "товар" or not romgram.гнётся(язык):
            continue
        м_, ж_ = romgram.ПАРЫ[язык]
        for свой, чужой in ((м_, ж_), (ж_, м_)):
            if f"{свой} " in показ:
                порча = показ.replace(f"{свой} ", f"{чужой} ", 1)
                assert судить(порча)[1] is False, порча
                перевёрнуто += 1
    assert перевёрнуто, "страниц товара с вопросным словом рода нет"
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
    # ПОДМЕНА ДОШЛА ДО ВСЕЙ СТРАНИЦЫ, А НЕ ДО ЕЁ НАЧАЛА. Хвост рамки «сели_вышли» звал товар
    # ИМЕНЕМ, вписанным рукой, и страница говорила «12 девочек … теперь 15 детей».
    #
    #     ПОДМЕНА, СДЕЛАННАЯ НЕ ВЕЗДЕ, ХУЖЕ НЕСДЕЛАННОЙ. Признак прост и не требует знания
    #     языка: подменённой страницы НЕ ДОЛЖНО быть ни одной формы прежнего товара.
    рваных = 0
    for форма, ряд in sorted(СОВМЕСТИМЫЕ.items()):
        for дыра, товары in ряд.items():
            прежний = _ТОВАР_ПО_ДЫРЕ[дыра]
            for товар in товары[1:]:
                for язык in РАМКИ_АКТОВ:
                    с = страница_акта(язык, форма, 0, 1, 12, 5, 4, товары={дыра: товар})
                    if not с:
                        continue
                    следы = [ф for ф in ТОВАРЫ_АКТОВ[язык][прежний]
                             if ф and ф != "" and ф in с
                             and ф not in ТОВАРЫ_АКТОВ[язык][товар]]
                    if следы:
                        print(f"  ПОДМЕНА РВАНА [{язык} {форма} := {товар}]: остался {следы[0]}")
                        рваных += 1
                        беды += 1
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(РАМКИ)}, форм {len(ФОРМЫ)}), "
          f"рамок с рядом товаров {len(СОВМЕСТИМЫЕ)}, рваных подмен {рваных}")




_РОДЫ_ЛИЦ = {л[0]: л[1] for л in A.ЛИЦА.get("ru", ()) if len(л) > 1 and л[1] in ("m", "f")}

import closedworld as _зк  # noqa: E402 — закон замкнутого мира читается после сборки показов
_СКЕЛЕТЫ_ЗНАКА = _зк.скелеты_знака(ПОКАЗЫ)


_ЧУЖОЙ_РОД_ТОВАРА = tuple(f"{romgram.вопросное(я, 'f' if р == 'm' else 'm')} {голова} "
                          for я, головы in РОД_ТОВАРА.items() for голова, р in головы.items())


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
    # ВОПРОСНОЕ СЛОВО ТОВАРА — СЛОВО РОДА ЕГО ГОЛОВЫ (24.09): дыра принимает обе формы пары, и
    # «¿cuántas tarros» проходило образцом. Род головы объявлен в `РОД_ТОВАРА`; страница, где
    # вопросное слово стои́т чужого рода перед головой товара, ложна, что бы ни сказал образец.
    if вердикт[:2] == (True, True) and any(ч in строка for ч in _ЧУЖОЙ_РОД_ТОВАРА):
        return True, False
    return вердикт
if __name__ == "__main__":
    _самопроверка()
