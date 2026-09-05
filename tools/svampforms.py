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
# Polish dative of the names (the pack declares gender only)
ДАТЕЛЬНЫЙ_PL = {"Anna": "Annie", "Jan": "Janowi", "Maria": "Marii", "Piotr": "Piotrowi", "Zofia": "Zofii", "Paweł": "Pawłowi", "Ewa": "Ewie", "Marek": "Markowi"}
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
        некоторые="{X} had {n} {Тn}. {Он} gave some of them away. now {он} has {r} {Тr} left. how many {Тмн} did {он} give away? {k}: {n} − {r} = {k}.",
        итог="{X} has {a} {Ц1} {Тмн} and {b} {Ц2} {Тмн}. how many {Тмн} does {X} have {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        итог_всего="{X} has {a} {Ц1} {Тмн} and {b} {Ц2} {Тмн}. how many {Тмн} does {X} have? a total of {s} {Тs}: {a} + {b} = {s}.",
        осталось="{X} had {n} {Тn}. {Он} gave away {k}. how many does {он} have now? {он} now has {r} left: {n} − {k} = {r}.",
        из_них="{X} had {n} {Тn}. {Он} gave {k} of them to {Y}. how many {Тмн} does {он} have now? {r}: {n} − {k} = {r}.",
        ему="{X} had {n} {Тn}. {Y} gave {ему} {k} more. how many {Тмн} does {он} have now? {s}: {n} + {k} = {s}.",
        если="{X} has {n} {Тn}. if {он} gives away {k}, how many will {он} have? {r}: {n} − {k} = {r}.",
        если_придут="there are {n} {Тn} in the box. if {k} more are put in, how many will there be? {s}: {n} + {k} = {s}.",
        время="{В1} {X} had {n} {Тn}. {В2} {он} got {k} more. how many {Тмн} does {он} have now? {s}: {n} + {k} = {s}.",
        кому="{X} had {n} {Тn}. {Он} gave {k} {Тk} to {Y}. how many {Тмн} does {X} have now? {r}: {n} − {k} = {r}.",
        у_него="{X} had {n} {Тn}. {Y} took {k} {Тk} from {него}. how many {Тмн} does {X} have now? {r}: {n} − {k} = {r}.",
        единица="a {Т1} costs $ {n}. how much do {k} {Тмн} cost? $ {v}: {k} × {n} = {v}.",
        товар="{X} has {a} {Г1a} and {b} {Г2b}. how many {Г3мн} does {он} have in all? {s} {Г3s}: {a} + {b} = {s}.",
    ),
    "ru": dict(
        некоторые="у {Xр} было {n} {Тn}. {Он} отдал{а} несколько. теперь у {него} осталось {r} {Тr}. сколько {Тмн} {он} отдал{а}? {k}: {n} − {r} = {k}.",
        итог="у {Xр} {a} {Ц1} {Тмн} и {b} {Ц2} {Тмн}. сколько {Тмн} у {Xр} {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        итог_всего="у {Xр} {a} {Ц1} {Тмн} и {b} {Ц2} {Тмн}. сколько {Тмн} у {Xр}? всего {s} {Тs}: {a} + {b} = {s}.",
        осталось="у {Xр} было {n} {Тn}. {Он} отдал{а} {k}. сколько у {него} теперь? теперь у {него} осталось {r}: {n} − {k} = {r}.",
        из_них="у {Xр} было {n} {Тn}. {Он} отдал{а} {k} из них {Yд}. сколько {Тмн} у {него} теперь? {r}: {n} − {k} = {r}.",
        ему="у {Xр} было {n} {Тn}. {Y} дал{аY} {ему} ещё {k}. сколько {Тмн} у {него} теперь? {s}: {n} + {k} = {s}.",
        если="у {Xр} {n} {Тn}. если {он} отдаст {k}, сколько у {него} останется? {r}: {n} − {k} = {r}.",
        если_придут="в коробке {n} {Тn}. если положить ещё {k}, сколько там будет? {s}: {n} + {k} = {s}.",
        время="{В1} у {Xр} было {n} {Тn}. {В2} {он} получил{а} ещё {k}. сколько {Тмн} у {него} теперь? {s}: {n} + {k} = {s}.",
        кому="у {Xр} было {n} {Тn}. {Он} отдал{а} {k} {Тk} {Yд}. сколько {Тмн} у {Xр} теперь? {r}: {n} − {k} = {r}.",
        у_него="у {Xр} было {n} {Тn}. {Y} взял{аY} у {него} {k} {Тk}. сколько {Тмн} у {Xр} теперь? {r}: {n} − {k} = {r}.",
        товар="у {Xр} {a} {Г1a} и {b} {Г2b}. сколько {Г3мн} у {него} всего? {s} {Г3s}: {a} + {b} = {s}.",
    ),
}
РАМКИ.update({
    "de": dict(
        осталось="{X} hatte {n} {Тn}. {Он} gab {k} weg. wie viele hat {он} jetzt? {он} hat jetzt noch {r}: {n} − {k} = {r}.",
        ему="{X} hatte {n} {Тn}. {Y} gab {ему} {k} mehr. wie viele {Тмн} hat {он} jetzt? {s}: {n} + {k} = {s}.",
        если_придут="in der Kiste sind {n} {Тn}. wenn {k} mehr hineingelegt werden, wie viele werden es sein? {s}: {n} + {k} = {s}.",
        у_него="{X} hatte {n} {Тn}. {Y} nahm {ему} {k} {Тk} weg. wie viele {Тмн} hat {X} jetzt? {r}: {n} − {k} = {r}.",
        товар="{X} hat {a} {Г1a} und {b} {Г2b}. wie viele {Г3мн} hat {он} insgesamt? {s} {Г3s}: {a} + {b} = {s}.",
        некоторые="{X} hatte {n} {Тn}. {Он} gab einige weg. jetzt hat {он} noch {r} {Тr}. wie viele {Тмн} gab {он} weg? {k}: {n} − {r} = {k}.",
        итог="{X} hat {a} {Ц1} {Тмн} und {b} {Ц2} {Тмн}. wie viele {Тмн} hat {X} {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        из_них="{X} hatte {n} {Тn}. {Он} gab {k} davon an {Y}. wie viele {Тмн} hat {он} jetzt? {r}: {n} − {k} = {r}.",
        если="{X} hat {n} {Тn}. wenn {он} {k} weggibt, wie viele wird {он} haben? {r}: {n} − {k} = {r}.",
        время="{В1} hatte {X} {n} {Тn}. {В2} bekam {он} {k} mehr. wie viele {Тмн} hat {он} jetzt? {s}: {n} + {k} = {s}.",
        кому="{X} hatte {n} {Тn}. {Он} gab {Y} {k} {Тk}. wie viele {Тмн} hat {X} jetzt? {r}: {n} − {k} = {r}."),
    "fr": dict(
        осталось="{X} avait {n} {Тn}. {Он} en a donné {k}. combien en a-t-{он} maintenant ? il {ему} en reste {r} : {n} − {k} = {r}.",
        ему="{X} avait {n} {Тn}. {Y} {ему} en a donné {k} de plus. combien de {Тмн} a-t-{он} maintenant ? {s} : {n} + {k} = {s}.",
        если_придут="il y a {n} {Тn} dans la boîte. si on en ajoute {k}, combien y en aura-t-il ? {s} : {n} + {k} = {s}.",
        у_него="{X} avait {n} {Тn}. {Y} {ему} a pris {k} {Тk}. combien de {Тмн} {X} a-t-{он} maintenant ? {r} : {n} − {k} = {r}.",
        товар="{X} a {a} {Г1a} et {b} {Г2b}. combien de {Г3мн} a-t-{он} en tout ? {s} {Г3s} : {a} + {b} = {s}.",
        некоторые="{X} avait {n} {Тn}. {Он} en a donné quelques-unes. maintenant il {ему} en reste {r}. combien de {Тмн} a-t-{он} données ? {k} : {n} − {r} = {k}.",
        итог="{X} a {a} {Тмн} {Ц1} et {b} {Тмн} {Ц2}. combien de {Тмн} {X} a-t-{он} {ГОЛОВА} ? {s} {Тs} : {a} + {b} = {s}.",
        из_них="{X} avait {n} {Тn}. {Он} en a donné {k} à {Y}. combien de {Тмн} a-t-{он} maintenant ? {r} : {n} − {k} = {r}.",
        если="{X} a {n} {Тn}. si {он} en donne {k}, combien lui en restera-t-il ? {r} : {n} − {k} = {r}.",
        время="{В1} {X} avait {n} {Тn}. {В2} {он} en a reçu {k} de plus. combien de {Тмн} a-t-{он} maintenant ? {s} : {n} + {k} = {s}.",
        кому="{X} avait {n} {Тn}. {Он} a donné {k} {Тk} à {Y}. combien de {Тмн} {X} a-t-{он} maintenant ? {r} : {n} − {k} = {r}."),
    "es": dict(
        осталось="{X} tenía {n} {Тn}. dio {k}. ¿cuántas tiene ahora? ahora le quedan {r}: {n} − {k} = {r}.",
        ему="{X} tenía {n} {Тn}. {Y} {ему} dio {k} más. ¿cuántas {Тмн} tiene ahora? {s}: {n} + {k} = {s}.",
        если_придут="hay {n} {Тn} en la caja. si se ponen {k} más, ¿cuántas habrá? {s}: {n} + {k} = {s}.",
        у_него="{X} tenía {n} {Тn}. {Y} {ему} quitó {k} {Тk}. ¿cuántas {Тмн} tiene {X} ahora? {r}: {n} − {k} = {r}.",
        товар="{X} tiene {a} {Г1a} y {b} {Г2b}. ¿cuántas {Г3мн} tiene en total? {s} {Г3s}: {a} + {b} = {s}.",
        некоторые="{X} tenía {n} {Тn}. dio algunas. ahora le quedan {r} {Тr}. ¿cuántas {Тмн} dio? {k}: {n} − {r} = {k}.",
        итог="{X} tiene {a} {Тмн} {Ц1} y {b} {Тмн} {Ц2}. ¿cuántas {Тмн} tiene {X} {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        из_них="{X} tenía {n} {Тn}. dio {k} de ellas a {Y}. ¿cuántas {Тмн} tiene ahora? {r}: {n} − {k} = {r}.",
        если="{X} tiene {n} {Тn}. si da {k}, ¿cuántas le quedarán? {r}: {n} − {k} = {r}.",
        время="{В1} {X} tenía {n} {Тn}. {В2} recibió {k} más. ¿cuántas {Тмн} tiene ahora? {s}: {n} + {k} = {s}.",
        кому="{X} tenía {n} {Тn}. dio {k} {Тk} a {Y}. ¿cuántas {Тмн} tiene {X} ahora? {r}: {n} − {k} = {r}."),
    "it": dict(
        осталось="{X} aveva {n} {Тn}. ne ha date {k}. quante ne ha adesso? {ему} ne restano {r}: {n} − {k} = {r}.",
        ему="{X} aveva {n} {Тn}. {Y} {ему} ne ha date altre {k}. quante {Тмн} ha adesso? {s}: {n} + {k} = {s}.",
        если_придут="ci sono {n} {Тn} nella scatola. se se ne mettono altre {k}, quante ce ne saranno? {s}: {n} + {k} = {s}.",
        у_него="{X} aveva {n} {Тn}. {Y} {ему} ha preso {k} {Тk}. quante {Тмн} ha {X} adesso? {r}: {n} − {k} = {r}.",
        товар="{X} ha {a} {Г1a} e {b} {Г2b}. quante {Г3мн} ha in tutto? {s} {Г3s}: {a} + {b} = {s}.",
        некоторые="{X} aveva {n} {Тn}. ne ha date alcune. ora {ему} restano {r} {Тr}. quante {Тмн} ha dato? {k}: {n} − {r} = {k}.",
        итог="{X} ha {a} {Тмн} {Ц1} e {b} {Тмн} {Ц2}. quante {Тмн} ha {X} {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        из_них="{X} aveva {n} {Тn}. ne ha date {k} a {Y}. quante {Тмн} ha adesso? {r}: {n} − {k} = {r}.",
        если="{X} ha {n} {Тn}. se ne dà {k}, quante ne avrà? {r}: {n} − {k} = {r}.",
        время="{В1} {X} aveva {n} {Тn}. {В2} ne ha ricevute altre {k}. quante {Тмн} ha adesso? {s}: {n} + {k} = {s}.",
        кому="{X} aveva {n} {Тn}. ha dato {k} {Тk} a {Y}. quante {Тмн} ha {X} adesso? {r}: {n} − {k} = {r}."),
    "pt": dict(
        осталось="{X} tinha {n} {Тn}. deu {k}. quantas tem agora? agora tem {r}: {n} − {k} = {r}.",
        ему="{X} tinha {n} {Тn}. {Y} deu-{ему} mais {k}. quantas {Тмн} tem agora? {s}: {n} + {k} = {s}.",
        если_придут="há {n} {Тn} na caixa. se puserem mais {k}, quantas haverá? {s}: {n} + {k} = {s}.",
        у_него="{X} tinha {n} {Тn}. {Y} tirou-{ему} {k} {Тk}. quantas {Тмн} tem {X} agora? {r}: {n} − {k} = {r}.",
        товар="{X} tem {a} {Г1a} e {b} {Г2b}. quantas {Г3мн} tem no total? {s} {Г3s}: {a} + {b} = {s}.",
        некоторые="{X} tinha {n} {Тn}. deu algumas. agora tem {r} {Тr}. quantas {Тмн} deu? {k}: {n} − {r} = {k}.",
        итог="{X} tem {a} {Тмн} {Ц1} e {b} {Тмн} {Ц2}. quantas {Тмн} tem {X} {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        из_них="{X} tinha {n} {Тn}. deu {k} delas {Yд}. quantas {Тмн} tem agora? {r}: {n} − {k} = {r}.",
        если="{X} tem {n} {Тn}. se der {k}, com quantas ficará? {r}: {n} − {k} = {r}.",
        время="{В1} {X} tinha {n} {Тn}. {В2} recebeu mais {k}. quantas {Тмн} tem agora? {s}: {n} + {k} = {s}.",
        кому="{X} tinha {n} {Тn}. deu {k} {Тk} {Yд}. quantas {Тмн} tem {X} agora? {r}: {n} − {k} = {r}."),
    "nl": dict(
        осталось="{X} had {n} {Тn}. {он} gaf er {k} weg. hoeveel heeft {он} nu? {он} heeft er nu nog {r}: {n} − {k} = {r}.",
        ему="{X} had {n} {Тn}. {Y} gaf {ему} er {k} bij. hoeveel {Тмн} heeft {он} nu? {s}: {n} + {k} = {s}.",
        если_придут="er zitten {n} {Тn} in de doos. als er {k} bij worden gedaan, hoeveel zijn het er dan? {s}: {n} + {k} = {s}.",
        у_него="{X} had {n} {Тn}. {Y} nam {k} {Тk} van {него} af. hoeveel {Тмн} heeft {X} nu? {r}: {n} − {k} = {r}.",
        товар="{X} heeft {a} {Г1a} en {b} {Г2b}. hoeveel {Г3мн} heeft {он} in totaal? {s} {Г3s}: {a} + {b} = {s}.",
        некоторые="{X} had {n} {Тn}. {он} gaf er een paar weg. nu heeft {он} er nog {r}. hoeveel {Тмн} gaf {он} weg? {k}: {n} − {r} = {k}.",
        итог="{X} heeft {a} {Ц1} {Тмн} en {b} {Ц2} {Тмн}. hoeveel {Тмн} heeft {X} {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        из_них="{X} had {n} {Тn}. {он} gaf er {k} aan {Y}. hoeveel {Тмн} heeft {он} nu? {r}: {n} − {k} = {r}.",
        если="{X} heeft {n} {Тn}. als {он} er {k} weggeeft, hoeveel heeft {он} dan? {r}: {n} − {k} = {r}.",
        время="{В1} had {X} {n} {Тn}. {В2} kreeg {он} er {k} bij. hoeveel {Тмн} heeft {он} nu? {s}: {n} + {k} = {s}.",
        кому="{X} had {n} {Тn}. {он} gaf {k} {Тk} aan {Y}. hoeveel {Тмн} heeft {X} nu? {r}: {n} − {k} = {r}."),
    "pl": dict(
        осталось="{X} miał{а} {n} {Тn}. oddał{а} {k}. ile ma teraz? teraz zostało {ему} {r}: {n} − {k} = {r}.",
        ему="{X} miał{а} {n} {Тn}. {Y} dał{аY} {ему} jeszcze {k}. ile {Тмн} ma teraz? {s}: {n} + {k} = {s}.",
        если_придут="w pudełku jest {n} {Тn}. jeśli włożyć jeszcze {k}, ile będzie? {s}: {n} + {k} = {s}.",
        у_него="{X} miał{а} {n} {Тn}. {Y} zabrał{аY} {ему} {k} {Тk}. ile {Тмн} ma {X} teraz? {r}: {n} − {k} = {r}.",
        товар="{X} ma {a} {Г1a} i {b} {Г2b}. ile {Г3мн} ma razem? {s} {Г3s}: {a} + {b} = {s}.",
        некоторые="{X} miał{а} {n} {Тn}. oddał{а} kilka. teraz ma {r} {Тr}. ile {Тмн} oddał{а}? {k}: {n} − {r} = {k}.",
        итог="{X} ma {a} {Ц1} {Тмн} i {b} {Ц2} {Тмн}. ile {Тмн} ma {X} {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        из_них="{X} miał{а} {n} {Тn}. oddał{а} {k} z nich {Yд}. ile {Тмн} ma teraz? {r}: {n} − {k} = {r}.",
        если="{X} ma {n} {Тn}. jeśli odda {k}, ile {ему} zostanie? {r}: {n} − {k} = {r}.",
        время="{В1} {X} miał{а} {n} {Тn}. {В2} dostał{а} jeszcze {k}. ile {Тмн} ma teraz? {s}: {n} + {k} = {s}.",
        кому="{X} miał{а} {n} {Тn}. oddał{а} {k} {Тk} {Yд}. ile {Тмн} ma {X} teraz? {r}: {n} − {k} = {r}."),
})
ФОРМЫ = ("некоторые", "итог", "итог_всего", "осталось", "из_них", "ему", "если", "если_придут", "время", "кому", "у_него", "единица", "товар")
# the unit before the number is an English shape of the band; Russian writes «3 ₽» after — declared gap
ОБЪЯВЛЕННЫЕ_ПРОПУСКИ = {"единица": frozenset({"ru"})}
ЧИСЛА = ((12, 5), (20, 8), (15, 6), (9, 4), (30, 12), (25, 7), (18, 11), (40, 15))
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


def _поля(язык, i, j, Т, n, k, форма):
    X, Y = _лицо(язык, i), _лицо(язык, j)
    if Y[0] == X[0]:
        Y = _лицо(язык, j + 1)
    м = МЕСТОИМЕНИЯ[язык][X[1]]
    вещь = lambda c: A._вещь(язык, Т, c)
    Yд = (_дательный(Y[0]) if язык == "ru" else ДАТЕЛЬНЫЙ_PL.get(Y[0], Y[0]) if язык == "pl"
          else _дательный_pt(Y) if язык == "pt" else Y[0])
    п = dict(X=X[0], Xр=X[2], Y=Y[0], Yд=Yд,
             он=м["он"], Он=м["он"], него=м["него"], ему=м["ему"],
             а=(("a" if X[1] == "f" else "") if язык == "pl" else A._а(язык, X[1])), аY=(("a" if Y[1] == "f" else "") if язык == "pl" else A._а(язык, Y[1])),
             n=n, k=k, r=n - k, s=n + k, a=n, b=k,
             Тn=вещь(n), Тk=вещь(k), Тr=вещь(n - k), Тs=вещь(n + k), Тмн=вещь(5), Т1=вещь(1))
    return п


def страница(язык, форма, i, j, Т, n, k, вариант=0):
    if язык in ОБЪЯВЛЕННЫЕ_ПРОПУСКИ.get(форма, ()):
        return None
    р = РАМКИ[язык][форма]
    п = _поля(язык, i, j, Т, n, k, форма)
    if форма == "итог":
        п.update(ГОЛОВА=ГОЛОВЫ_ИТОГА[язык][вариант % len(ГОЛОВЫ_ИТОГА[язык])])
    if форма in ("итог", "итог_всего"):
        п.update(Ц1=ЦВЕТА[язык][0], Ц2=ЦВЕТА[язык][1])
    if форма == "время":
        в1, в2 = ВРЕМЯ[язык][вариант % len(ВРЕМЯ[язык])]
        п.update(В1=в1, В2=в2)
    if форма == "единица":
        n_, k_ = ЦЕНЫ[вариант % len(ЦЕНЫ)]
        п.update(n=n_, k=k_, v=n_ * k_, Тмн=A._вещь(язык, Т, 5))
    if форма == "товар":
        г1, г2, г3 = ТОВАРЫ[язык][вариант % len(ТОВАРЫ[язык])]
        п.update(Г1a=_счёт(г1, n), Г2b=_счёт(г2, k), Г3мн=г3[-1], Г3s=_счёт(г3, n + k))
    return р.format(**п)


def _счёт(ф, c):
    """Count form of a declared goods phrase: (one, many) for en, (one, few, many) for ru."""
    if len(ф) == 2:
        return ф[0] if c == 1 else ф[1]
    if c % 100 in range(11, 15):
        return ф[2]
    п = c % 10
    return ф[0] if п == 1 else ф[1] if п in (2, 3, 4) else ф[2]


def _показы():
    вон = {}
    for язык in РАМКИ:
        лиц = len(A.ЛИЦА[язык]); вещей = len(A.ЯЗЫКИ[язык]["вещи"])
        for форма in ФОРМЫ:
            if форма not in РАМКИ[язык]:
                continue
            for q, (n, k) in enumerate(ЧИСЛА):
                i = q % лиц; j = (q * 3 + 1) % лиц; Т = q % вещей
                for вариант in range(3 if форма in ("итог", "время", "товар") else (4 if форма == "единица" else 1)):
                    с = страница(язык, форма, i, j, Т, n, k, вариант)
                    if с:
                        вон[с] = (язык, форма)
    return вон


ПОКАЗЫ = _показы()


def _образцы():
    """A regex per frame: names, things, pronouns, time words and goods are declared
    alternations; numbers are holes; the ledger is read by the judge."""
    вон = []
    alt = lambda слова: "(?:" + "|".join(re.escape(с) for с in sorted(set(с for с in слова if с), key=len, reverse=True)) + ")"
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
        дыры = {"X": alt(имена), "Y": alt(имена), "Xр": alt(род), "Yд": alt(дат), "он": alt(мест), "Он": alt(мест), "него": alt(мест), "ему": alt(мест),
                "а": "(?:а|о|и|a|)", "аY": "(?:а|о|и|a|)", "n": r"(\d+)", "k": r"(\d+)", "r": r"(\d+)", "s": r"(\d+)", "a": r"(\d+)", "b": r"(\d+)", "v": r"(\d+)",
                "Тn": alt(вещи), "Тk": alt(вещи), "Тr": alt(вещи), "Тs": alt(вещи), "Тмн": alt(вещи), "Т1": alt(вещи1),
                "ГОЛОВА": alt(ГОЛОВЫ_ИТОГА[язык]), "Ц1": alt(ЦВЕТА[язык]), "Ц2": alt(ЦВЕТА[язык]),
                "В1": alt(в for в, _ in ВРЕМЯ[язык]), "В2": alt(в for _, в in ВРЕМЯ[язык]),
                "Г1a": alt(товары), "Г2b": alt(товары), "Г3мн": alt(товары), "Г3s": alt(товары)}
        for форма, рамка in рамки.items():
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
        добавил="у {Xр} было {n} {ПРИЛn} в телефоне. {Он} добавил{а} {k} {ПРИЛk}. сколько {ПРИЛмн} у {него} теперь? {s}: {n} + {k} = {s}.",
        добавил_на_полку="у {Xр} на полке было {n} {ФИГn}. потом {он} добавил{а} на полку ещё {k} {ФИГk}. сколько {ФИГмн} на полке теперь? {s}: {n} + {k} = {s}.",
        выбросил="{X} нашёл{а} в парке {n} {КРЫШn}, а {k} старых выбросил{а}. на сколько больше {КРЫШмн} {он} нашёл{а}, чем выбросил{а}? {r}: {n} − {k} = {r}.",
        выбросил_розы="в вазе было {n} {РОЗn}. {X} выбросил{а} из вазы {k} {РОЗk}. сколько {РОЗмн} в вазе теперь? {r}: {n} − {k} = {r}.",
        узнал="{X} узнал{а}, что во дворец в тот день пришли {n} {ПОСn}, а на следующий — {k}. сколько {ПОСмн} пришло всего? {s}: {n} + {k} = {s}.",
        сели_вышли="в автобусе было {n} {ДЕТn}. на остановке {k} {ДЕТk} сели, а несколько вышли. теперь в автобусе {s} {ДЕТs}. сколько {ДЕТмн} вышло? {k2}: {n} + {k} − {s} = {k2}.",
        сыграл="{X} сыграл{а} {n} {ИГРn} в понедельник и {k} {ИГРk} во вторник. сколько {ИГРмн} сыграл{а} {X} всего? {s}: {n} + {k} = {s}.",
        потратил="{X} потратил{а} {n} {ЧАСn} на английский и {k} {ЧАСk} на китайский. сколько {ЧАСмн} потратил{а} {X} всего? всего {s} {ЧАСs}: {n} + {k} = {s}.",
        список="каждый день {X} тратит {n} {ЧАСn} на английский, {k} {ЧАСk} на китайский и {m} {ЧАСm} на испанский. сколько {ЧАСмн} тратит {X} всего? {t}: {n} + {k} + {m} = {t}.",
        коробка="{X} получил{а} коробку с {n} {МЕЛn} и коробку с {k} {МЕЛk}. сколько {МЕЛмн} у {Xр}? {s}: {n} + {k} = {s}.",
        главы="в книге 2 главы. в первой главе {n} {СТРn}, во второй — {k} {СТРk}. сколько {СТРмн} в книге всего? {s}: {n} + {k} = {s}.",
        две_клаузы="у {Xр} было {n} {ИГРn}, а у {Yр} — {k} {ИГРk}. сколько {ИГРмн} было у них вместе? {s}: {n} + {k} = {s}.",
    ),
}
_ТОВАР_ПО_ДЫРЕ = {"ОТЖ": "отжимания", "СКР": "скручивания", "ПРИЛ": "приложения", "ФИГ": "фигурки", "КРЫШ": "крышки", "РОЗ": "розы",
                  "ПОС": "посетители", "ДЕТ": "дети", "ИГР": "игры", "ЧАС": "часы", "МЕЛ": "мелки", "СТР": "страницы"}
ТОВАРЫ_АКТОВ.update({
    "de": {"отжимания": ("Liegestütz", "Liegestütze"), "скручивания": ("Sit-up", "Sit-ups"), "приложения": ("App", "Apps")},
    "fr": {"отжимания": ("pompe", "pompes"), "скручивания": ("abdo", "abdos"), "приложения": ("application", "applications")},
    "es": {"отжимания": ("flexión", "flexiones"), "скручивания": ("abdominal", "abdominales"), "приложения": ("aplicación", "aplicaciones")},
    "it": {"отжимания": ("flessione", "flessioni"), "скручивания": ("addominale", "addominali"), "приложения": ("app", "app")},
    "pt": {"отжимания": ("flexão", "flexões"), "скручивания": ("abdominal", "abdominais"), "приложения": ("aplicação", "aplicações")},
    "nl": {"отжимания": ("push-up", "push-ups"), "скручивания": ("sit-up", "sit-ups"), "приложения": ("app", "apps")},
    "pl": {"отжимания": ("pompka", "pompki", "pompek"), "скручивания": ("brzuszek", "brzuszki", "brzuszków"), "приложения": ("aplikacja", "aplikacje", "aplikacji")},
})
РАМКИ_АКТОВ.update({
    "de": dict(сделал="{X} machte {n} {ОТЖn} und {k} {СКРk}. wie viele {ОТЖмн} machte {X}? {n}. wie viele Übungen insgesamt? {s}: {n} + {k} = {s}.",
               добавил="{X} hatte {n} {ПРИЛn} auf dem Handy. {Он} fügte {k} neue {ПРИЛмн} hinzu. wie viele {ПРИЛмн} hat {он} jetzt? {s}: {n} + {k} = {s}."),
    "fr": dict(сделал="{X} a fait {n} {ОТЖn} et {k} {СКРk}. combien de {ОТЖмн} {X} a-t-{он} faites ? {n}. combien d'exercices en tout ? {s} : {n} + {k} = {s}.",
               добавил="{X} avait {n} {ПРИЛn} sur le téléphone. {Он} a ajouté {k} nouvelles {ПРИЛмн}. combien d'{ПРИЛмн} a-t-{он} maintenant ? {s} : {n} + {k} = {s}."),
    "es": dict(сделал="{X} hizo {n} {ОТЖn} y {k} {СКРk}. ¿cuántas {ОТЖмн} hizo {X}? {n}. ¿cuántos ejercicios en total? {s}: {n} + {k} = {s}.",
               добавил="{X} tenía {n} {ПРИЛn} en el teléfono. añadió {k} {ПРИЛмн} nuevas. ¿cuántas {ПРИЛмн} tiene ahora? {s}: {n} + {k} = {s}."),
    "it": dict(сделал="{X} ha fatto {n} {ОТЖn} e {k} {СКРk}. quante {ОТЖмн} ha fatto {X}? {n}. quanti esercizi in tutto? {s}: {n} + {k} = {s}.",
               добавил="{X} aveva {n} {ПРИЛn} sul telefono. ha aggiunto {k} nuove {ПРИЛмн}. quante {ПРИЛмн} ha adesso? {s}: {n} + {k} = {s}."),
    "pt": dict(сделал="{X} fez {n} {ОТЖn} e {k} {СКРk}. quantas {ОТЖмн} fez {X}? {n}. quantos exercícios no total? {s}: {n} + {k} = {s}.",
               добавил="{X} tinha {n} {ПРИЛn} no telemóvel. adicionou {k} {ПРИЛмн} novas. quantas {ПРИЛмн} tem agora? {s}: {n} + {k} = {s}."),
    "nl": dict(сделал="{X} deed {n} {ОТЖn} en {k} {СКРk}. hoeveel {ОТЖмн} deed {X}? {n}. hoeveel oefeningen in totaal? {s}: {n} + {k} = {s}.",
               добавил="{X} had {n} {ПРИЛn} op de telefoon. {он} voegde {k} nieuwe {ПРИЛмн} toe. hoeveel {ПРИЛмн} heeft {он} nu? {s}: {n} + {k} = {s}."),
    "pl": dict(сделал="{X} zrobił{а} {n} {ОТЖn} i {k} {СКРk}. ile {ОТЖмн} zrobił{а} {X}? {n}. ile ćwiczeń razem? {s}: {n} + {k} = {s}.",
               добавил="{X} miał{а} {n} {ПРИЛn} w telefonie. dodał{а} {k} {ПРИЛk}. ile {ПРИЛмн} ma teraz? {s}: {n} + {k} = {s}."),
})
ФОРМЫ_АКТОВ = tuple(РАМКИ_АКТОВ["en"])
ЧИСЛА_АКТОВ = ((12, 5, 4), (35, 3, 9), (20, 8, 6), (15, 7, 2), (30, 12, 10), (9, 4, 3), (18, 11, 5), (24, 15, 7))


def _товар_форма(язык, ключ, c):
    return _счёт(ТОВАРЫ_АКТОВ[язык][ключ], c)


def _поля_акта(язык, i, j, n, k, m):
    X, Y = _лицо(язык, i), _лицо(язык, j)
    if Y[0] == X[0]:
        Y = _лицо(язык, j + 1)
    мест = МЕСТОИМЕНИЯ[язык][X[1]]
    п = dict(X=X[0], Xр=X[2], Y=Y[0], Yр=Y[2], он=мест["он"], Он=мест["он"], него=мест["него"],
             а=(("a" if X[1] == "f" else "") if язык == "pl" else A._а(язык, X[1])), аY=(("a" if Y[1] == "f" else "") if язык == "pl" else A._а(язык, Y[1])),
             n=n, k=k, m=m, r=n - k, s=n + k, t=n + k + m, k2=k - (n + k - (n + k - k)) if False else k)
    # «сели_вышли»: сели k, вышли k2, теперь s = n + k − k2 — вышло меньше, чем село
    п["k2"] = max(1, k // 2); п["s_бус"] = n + k - п["k2"]
    for дыра, ключ in _ТОВАР_ПО_ДЫРЕ.items():
        if ключ not in ТОВАРЫ_АКТОВ[язык]:
            continue
        п[дыра + "n"] = _товар_форма(язык, ключ, n); п[дыра + "k"] = _товар_форма(язык, ключ, k)
        п[дыра + "m"] = _товар_форма(язык, ключ, m); п[дыра + "s"] = _товар_форма(язык, ключ, n + k)
        п[дыра + "мн"] = ТОВАРЫ_АКТОВ[язык][ключ][-1]
    return п


def страница_акта(язык, форма, i, j, n, k, m=4):
    р = РАМКИ_АКТОВ[язык][форма]
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
            for q, (n, k, m) in enumerate(ЧИСЛА_АКТОВ):
                вон[страница_акта(язык, форма, q % лиц, (q * 3 + 1) % лиц, n, k, m)] = (язык, форма)
    return вон


ПОКАЗЫ.update(_показы_актов())


def _образцы_актов():
    вон = []
    alt = lambda слова: "(?:" + "|".join(re.escape(с) for с in sorted(set(с for с in слова if с), key=len, reverse=True)) + ")"
    for язык, рамки in РАМКИ_АКТОВ.items():
        имена = [_лицо(язык, i)[0] for i in range(len(A.ЛИЦА[язык]))]; род = [л[2] for л in A.ЛИЦА[язык]]
        мест = [v for г in МЕСТОИМЕНИЯ[язык].values() for v in г.values()]
        дыры = {"X": alt(имена), "Y": alt(имена), "Xр": alt(род), "Yр": alt(род), "он": alt(мест), "Он": alt(мест), "него": alt(мест),
                "а": "(?:а|о|и|a|)", "аY": "(?:а|о|и|a|)", "n": r"(\d+)", "k": r"(\d+)", "m": r"(\d+)", "r": r"(\d+)", "s": r"(\d+)", "t": r"(\d+)", "k2": r"(\d+)"}
        for дыра, ключ in _ТОВАР_ПО_ДЫРЕ.items():
            if ключ not in ТОВАРЫ_АКТОВ[язык]:
                continue
            формы = alt(ТОВАРЫ_АКТОВ[язык][ключ])
            for суффикс in ("n", "k", "m", "s", "мн"):
                дыры[дыра + суффикс] = формы
        for форма, рамка in рамки.items():
            куски = [дыры[к[1:-1]] if к.startswith("{") else re.escape(к) for к in re.split(r"(\{[^}]+\})", рамка)]
            вон.append((re.compile("^" + "".join(куски) + "$"), язык, форма))
    return вон


ОБРАЗЦЫ.extend(_образцы_актов())
ЛЕДЖЕР3 = re.compile(r"(\d+) \+ (\d+) ([+−]) (\d+) = (\d+)\.$")
ЛЕДЖЕР = re.compile(r"(\d+) ([+−×]) (\d+) = (\d+)\.$")


def судить(строка):
    """(судимо, истинно): a page of the house, or a line of its frame whose ledger does not hold."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма in ОБРАЗЦЫ:
        if образ.match(с):
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
            верно = v == (a + b if з == "+" else a - b if з == "−" else a * b)
            # the numbers of the story (BEFORE the ledger) must be the numbers of the ledger
            числа = [int(x) for x in re.findall(r"\d+", с[:м.start()])]
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
            с = страница(язык, форма, 0, 1, 0, 12, 5)
            битая = re.sub(r"= (\d+)\.$", lambda м: f"= {int(м.group(1)) + 1}.", с)
            assert судить(битая) == (True, False), битая
            мутанты += 1
    for язык in РАМКИ_АКТОВ:
        for форма in ФОРМЫ_АКТОВ:
            if форма not in РАМКИ_АКТОВ[язык]:
                continue
            с = страница_акта(язык, форма, 0, 1, 12, 5)
            битая = re.sub(r"= (\d+)\.$", lambda м: f"= {int(м.group(1)) + 1}.", с)
            assert судить(битая) == (True, False), битая
            мутанты += 1
    for форма in ("некоторые", "итог", "из_них", "если", "время", "кому", "единица", "товар"):
        print("  ", страница("en", форма, 0, 1, 0, 12, 5))
    for форма in ("некоторые", "из_них", "кому", "товар"):
        print("  ", страница("ru", форма, 2, 3, 1, 12, 5))
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(РАМКИ)}, форм {len(ФОРМЫ)})")


if __name__ == "__main__":
    _самопроверка()
