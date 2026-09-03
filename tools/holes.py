#!/usr/bin/env python3
"""THE HOUSE OF HOLES — one fact frame, every role of it asked, in six languages.

holon's Д-1 (REVISION 02.09): in the organism a question is a per-genus
SURFACE bought from that genus' shows, not an OPERATION over a bought fact
frame, so the organism cannot ask what it was never shown asked. This house
holds the frame «{time} {actor} {verb} {number} {things} {place}» and the
operation that turns any one role of it into a hole: the question word
names the hole's TYPE (who → actor, how many → number, what → thing, where
→ place, when → time), the question keeps every other role, and the answer
is exactly the filler the question took out. The generator draws lines from
here; the court parses a fact by the same frame and recomputes every lawful
question with its answer — nothing in the court is looked up from the line.

Six languages (the owner's word: every language in surplus): en, ru, de,
es, it, fr. What differs is declared per language — the word order of the
fact (German verb-second, the Romance languages subject-first), the count
forms (Russian by the house of forms), the gender agreement of the
question word (Spanish cuántos/cuántas, Italian quanti/quante), the French
past participle agreeing with the fronted object («combien de tasses
Anne a-t-elle mises»), the case-bearing place («на полку» vs «на полке»,
«auf das Regal» vs «auf dem Markt») and the «whither» word where the
language has one (куда, wohin). Names and their gender come from the packs.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rugram  # noqa: E402

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
ЯЗЫКИ = ("en", "ru", "de", "es", "it", "fr", "pt", "nl", "pl", "tr")

ДНИ = {
    "en": ("on monday", "on tuesday", "on wednesday", "on thursday", "on friday", "on saturday", "on sunday"),
    "ru": ("в понедельник", "во вторник", "в среду", "в четверг", "в пятницу", "в субботу", "в воскресенье"),
    "de": ("am Montag", "am Dienstag", "am Mittwoch", "am Donnerstag", "am Freitag", "am Samstag", "am Sonntag"),
    "es": ("el lunes", "el martes", "el miércoles", "el jueves", "el viernes", "el sábado", "el domingo"),
    "it": ("lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"),
    "fr": ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"),
    "pt": ("na segunda-feira", "na terça-feira", "na quarta-feira", "na quinta-feira", "na sexta-feira", "no sábado", "no domingo"),
    "nl": ("op maandag", "op dinsdag", "op woensdag", "op donderdag", "op vrijdag", "op zaterdag", "op zondag"),
    "pl": ("w poniedziałek", "we wtorek", "w środę", "w czwartek", "w piątek", "w sobotę", "w niedzielę"),
    "tr": ("pazartesi", "salı", "çarşamba", "perşembe", "cuma", "cumartesi", "pazar"),
}

# FRAMES BY INDEX — 0 put, 1 bought, 2 found, 3 ate, 4 read. Per language: the
# verb forms, the «whither» word where the language has one, the places in
# the case the verb governs, the things (en: singular and plural; ru: the
# lemma, the count form comes from the house of forms; de: the plural,
# capitalised as German writes nouns; es/it/fr: the plural and its gender).
РАМКИ = {
    "en": (
        dict(прош="put", осн="put", места=("on the shelf", "in the box", "on the table", "in the bag"),
             вещи=(("cup", "cups"), ("book", "books"), ("pen", "pens"), ("plate", "plates"))),
        dict(прош="bought", осн="buy", места=("at the market", "in the shop", "at the fair"),
             вещи=(("apple", "apples"), ("pear", "pears"), ("pen", "pens"), ("book", "books"))),
        dict(прош="found", осн="find", места=("in the park", "in the garden", "on the road", "on the beach"),
             вещи=(("coin", "coins"), ("shell", "shells"), ("stone", "stones"), ("key", "keys"))),
        dict(прош="ate", осн="eat", места=("in the kitchen", "at school", "in the garden"),
             вещи=(("apple", "apples"), ("pear", "pears"), ("cookie", "cookies"), ("plum", "plums"))),
        dict(прош="read", осн="read", места=("in the library", "at school", "at home"),
             вещи=(("book", "books"), ("story", "stories"), ("letter", "letters"))),
    ),
    "ru": (
        dict(м="положил", ж="положила", куда="куда", места=("на полку", "в коробку", "на стол", "в сумку"),
             вещи=("чашка", "книга", "ручка", "тарелка")),
        dict(м="купил", ж="купила", куда="где", места=("на рынке", "в магазине", "на ярмарке"),
             вещи=("яблоко", "груша", "ручка", "книга")),
        dict(м="нашёл", ж="нашла", куда="где", места=("в парке", "в саду", "на дороге", "на пляже"),
             вещи=("монета", "ракушка", "камень", "ключ")),
        dict(м="съел", ж="съела", куда="где", места=("на кухне", "в школе", "в саду"),
             вещи=("яблоко", "груша", "печенье", "слива")),
        dict(м="прочитал", ж="прочитала", куда="где", места=("в библиотеке", "в школе", "дома"),
             вещи=("книга", "рассказ", "письмо")),
    ),
    "de": (
        dict(гл="legte", куда="wohin", места=("auf das Regal", "in die Kiste", "auf den Tisch", "in die Tasche"),
             вещи=("Tassen", "Bücher", "Stifte", "Teller")),
        dict(гл="kaufte", куда="wo", места=("auf dem Markt", "im Laden", "auf dem Jahrmarkt"),
             вещи=("Äpfel", "Birnen", "Stifte", "Bücher")),
        dict(гл="fand", куда="wo", места=("im Park", "im Garten", "auf der Straße", "am Strand"),
             вещи=("Münzen", "Muscheln", "Steine", "Schlüssel")),
        dict(гл="aß", куда="wo", места=("in der Küche", "in der Schule", "im Garten"),
             вещи=("Äpfel", "Birnen", "Kekse", "Pflaumen")),
        dict(гл="las", куда="wo", места=("in der Bibliothek", "in der Schule", "zu Hause"),
             вещи=("Bücher", "Geschichten", "Briefe")),
    ),
    "es": (
        dict(гл="puso", места=("en el estante", "en la caja", "en la mesa", "en la bolsa"),
             вещи=(("tazas", "f"), ("libros", "m"), ("bolígrafos", "m"), ("platos", "m"))),
        dict(гл="compró", места=("en el mercado", "en la tienda", "en la feria"),
             вещи=(("manzanas", "f"), ("peras", "f"), ("bolígrafos", "m"), ("libros", "m"))),
        dict(гл="encontró", места=("en el parque", "en el jardín", "en el camino", "en la playa"),
             вещи=(("monedas", "f"), ("conchas", "f"), ("piedras", "f"), ("llaves", "f"))),
        dict(гл="comió", места=("en la cocina", "en la escuela", "en el jardín"),
             вещи=(("manzanas", "f"), ("peras", "f"), ("galletas", "f"), ("ciruelas", "f"))),
        dict(гл="leyó", места=("en la biblioteca", "en la escuela", "en casa"),
             вещи=(("libros", "m"), ("cuentos", "m"), ("cartas", "f"))),
    ),
    "it": (
        dict(гл="ha messo", места=("sullo scaffale", "nella scatola", "sul tavolo", "nella borsa"),
             вещи=(("tazze", "f"), ("libri", "m"), ("penne", "f"), ("piatti", "m"))),
        dict(гл="ha comprato", места=("al mercato", "nel negozio", "alla fiera"),
             вещи=(("mele", "f"), ("pere", "f"), ("penne", "f"), ("libri", "m"))),
        dict(гл="ha trovato", места=("nel parco", "nel giardino", "sulla strada", "sulla spiaggia"),
             вещи=(("monete", "f"), ("conchiglie", "f"), ("pietre", "f"), ("chiavi", "f"))),
        dict(гл="ha mangiato", места=("in cucina", "a scuola", "nel giardino"),
             вещи=(("mele", "f"), ("pere", "f"), ("biscotti", "m"), ("prugne", "f"))),
        dict(гл="ha letto", места=("in biblioteca", "a scuola", "a casa"),
             вещи=(("libri", "m"), ("racconti", "m"), ("lettere", "f"))),
    ),
    "fr": (  # прич: the participle agreed with a fronted plural object (m, f)
        dict(гл="a mis", прич=("mis", "mises"), места=("sur l'étagère", "dans la boîte", "sur la table", "dans le sac"),
             вещи=(("tasses", "f"), ("livres", "m"), ("stylos", "m"), ("assiettes", "f"))),
        dict(гл="a acheté", прич=("achetés", "achetées"), места=("au marché", "au magasin", "à la foire"),
             вещи=(("pommes", "f"), ("poires", "f"), ("stylos", "m"), ("livres", "m"))),
        dict(гл="a trouvé", прич=("trouvés", "trouvées"), места=("dans le parc", "dans le jardin", "sur la route", "sur la plage"),
             вещи=(("pièces", "f"), ("coquillages", "m"), ("pierres", "f"), ("clés", "f"))),
        dict(гл="a mangé", прич=("mangés", "mangées"), места=("dans la cuisine", "à l'école", "dans le jardin"),
             вещи=(("pommes", "f"), ("poires", "f"), ("biscuits", "m"), ("prunes", "f"))),
        dict(гл="a lu", прич=("lus", "lues"), места=("à la bibliothèque", "à l'école", "à la maison"),
             вещи=(("livres", "m"), ("histoires", "f"), ("lettres", "f"))),
    ),
    "pt": (
        dict(гл="pôs", места=("na estante", "na caixa", "na mesa", "na bolsa"),
             вещи=(("xícaras", "f"), ("livros", "m"), ("canetas", "f"), ("pratos", "m"))),
        dict(гл="comprou", места=("no mercado", "na loja", "na feira"),
             вещи=(("maçãs", "f"), ("peras", "f"), ("canetas", "f"), ("livros", "m"))),
        dict(гл="encontrou", места=("no parque", "no jardim", "na estrada", "na praia"),
             вещи=(("moedas", "f"), ("conchas", "f"), ("pedras", "f"), ("chaves", "f"))),
        dict(гл="comeu", места=("na cozinha", "na escola", "no jardim"),
             вещи=(("maçãs", "f"), ("peras", "f"), ("biscoitos", "m"), ("ameixas", "f"))),
        dict(гл="leu", места=("na biblioteca", "na escola", "em casa"),
             вещи=(("livros", "m"), ("contos", "m"), ("cartas", "f"))),
    ),
    "nl": (  # Dutch: verb-second fact like German, nouns lowercase, «waar» for every place
        dict(гл="legde", места=("op de plank", "in de doos", "op de tafel", "in de tas"),
             вещи=("kopjes", "boeken", "pennen", "borden")),
        dict(гл="kocht", места=("op de markt", "in de winkel", "op de kermis"),
             вещи=("appels", "peren", "pennen", "boeken")),
        dict(гл="vond", места=("in het park", "in de tuin", "op de weg", "op het strand"),
             вещи=("munten", "schelpen", "stenen", "sleutels")),
        dict(гл="at", места=("in de keuken", "op school", "in de tuin"),
             вещи=("appels", "peren", "koekjes", "pruimen")),
        dict(гл="las", места=("in de bibliotheek", "op school", "thuis"),
             вещи=("boeken", "verhalen", "brieven")),
    ),
    "pl": (  # Polish: past by gender, things as (few, many) — the count form by the pack's count_agreement
        dict(м="położył", ж="położyła", места=("na półkę", "do pudełka", "na stół", "do torby"),
             вещи=(("filiżanki", "filiżanek"), ("książki", "książek"), ("długopisy", "długopisów"), ("talerze", "talerzy"))),
        dict(м="kupił", ж="kupiła", места=("na targu", "w sklepie", "na jarmarku"),
             вещи=(("jabłka", "jabłek"), ("gruszki", "gruszek"), ("długopisy", "długopisów"), ("książki", "książek"))),
        dict(м="znalazł", ж="znalazła", места=("w parku", "w ogrodzie", "na drodze", "na plaży"),
             вещи=(("monety", "monet"), ("muszle", "muszli"), ("kamienie", "kamieni"), ("klucze", "kluczy"))),
        dict(м="zjadł", ж="zjadła", места=("w kuchni", "w szkole", "w ogrodzie"),
             вещи=(("jabłka", "jabłek"), ("gruszki", "gruszek"), ("ciastka", "ciastek"), ("śliwki", "śliwek"))),
        dict(м="przeczytał", ж="przeczytała", места=("w bibliotece", "w szkole", "w domu"),
             вещи=(("książki", "książek"), ("opowiadania", "opowiadań"), ("listy", "listów"))),
    ),
    "tr": (  # Turkish: SOV fact «Ayşe pazartesi rafa 5 fincan koydu.», no plural after a numeral,
             # places in the dative (whither) or locative, things as (bare, accusative) for the
             # definite object of a question («5 fincanı kim koydu?»), «nereye» for putting
        dict(гл="koydu", куда="nereye", места=("rafa", "kutuya", "masaya", "çantaya"),
             вещи=(("fincan", "fincanı"), ("kitap", "kitabı"), ("kalem", "kalemi"), ("tabak", "tabağı"))),
        dict(гл="aldı", куда="nerede", места=("pazarda", "dükkânda", "panayırda"),
             вещи=(("elma", "elmayı"), ("armut", "armudu"), ("kalem", "kalemi"), ("kitap", "kitabı"))),
        dict(гл="buldu", куда="nerede", места=("parkta", "bahçede", "yolda", "plajda"),
             вещи=(("taş", "taşı"), ("anahtar", "anahtarı"), ("top", "topu"), ("boncuk", "boncuğu"))),
        dict(гл="yedi", куда="nerede", места=("mutfakta", "okulda", "bahçede"),
             вещи=(("elma", "elmayı"), ("armut", "armudu"), ("kurabiye", "kurabiyeyi"), ("erik", "eriği"))),
        dict(гл="okudu", куда="nerede", места=("kütüphanede", "okulda", "evde"),
             вещи=(("kitap", "kitabı"), ("hikâye", "hikâyeyi"), ("mektup", "mektubu"))),
    ),
}


def форма_счёта(язык, n):
    """one / few / many by the pack's count_agreement — the first rule that
    fits; the declared law of the language, not a guess of this house."""
    правила = json.loads((КОРЕНЬ / "tools" / "langpacks" / f"{язык}.json").read_text(encoding="utf-8"))["count_agreement"]
    for п in правила:
        if "mod" not in п or (n % п["mod"]) in п["in"]:
            return п["form"]
    return "many"


# THE OPEN ROLE — the organism asks about its own open hole (Д-1, second
# half: «lets the organism ASK about its own open holes»). A fact whose one
# role is unfilled is written with the language's placeholder for that role
# (someone / some / something / somewhere / at some time), and what follows
# is the question of that role — the same question the hole market answers,
# now produced, not answered. The «whither» placeholder pairs with the
# «whither» frame (put), the «where» one with the rest; the count
# placeholder agrees in gender where the language asks it (algunos/algunas).
ПРОБЕЛЫ = {
    "en": dict(кто="someone", сколько="some", что="something", куда=("somewhere", "somewhere"), когда="at some time"),
    "ru": dict(кто="кто-то", сколько="несколько", что="что-то", куда=("куда-то", "где-то"), когда="когда-то"),
    "de": dict(кто="jemand", сколько="einige", что="etwas", куда=("irgendwohin", "irgendwo"), когда="irgendwann"),
    "es": dict(кто="alguien", сколько=("algunos", "algunas"), что="algo", куда=("en algún lugar", "en algún lugar"), когда="en algún momento"),
    "it": dict(кто="qualcuno", сколько=("alcuni", "alcune"), что="qualcosa", куда=("da qualche parte", "da qualche parte"), когда="a un certo punto"),
    "fr": dict(кто="quelqu'un", сколько="quelques", что="quelque chose", куда=("quelque part", "quelque part"), когда="un jour"),
    "pt": dict(кто="alguém", сколько=("alguns", "algumas"), что="algo", куда=("em algum lugar", "em algum lugar"), когда="em algum momento"),
    "nl": dict(кто="iemand", сколько="enkele", что="iets", куда=("ergens", "ergens"), когда="ooit"),
    "pl": dict(кто="ktoś", сколько="kilka", что="coś", куда=("gdzieś", "gdzieś"), когда="kiedyś"),
    "tr": dict(кто="biri", сколько="birkaç", что="bir şey", куда=("bir yere", "bir yerde"), когда="bir gün"),
}
РОЛИ = ("кто", "сколько", "что", "куда", "когда")


def _к_месту(язык, р):
    """True for the frame whose place is a goal (put): куда / wohin / nereye."""
    return р.get("куда") in ("куда", "wohin", "nereye") or (язык not in ("ru", "de", "tr") and р is РАМКИ[язык][0])


def _много(язык, вещь):
    """The thing beside a count placeholder — the plural / many form."""
    if язык == "en":
        return вещь[1]
    if язык == "ru":
        return rugram.форма(вещь, 5)
    if язык in ("de", "nl"):
        return вещь
    if язык == "pl":
        return вещь[1]
    return вещь[0]


def _глагол(язык, р, род):
    if язык == "en":
        return р["прош"]
    if язык in ("ru", "pl"):
        return р["ж"] if род == "f" else р["м"]
    return р["гл"]


def _сборка(язык, день, имя, гл, слот, место):
    """The word order of the fact per language."""
    if язык in ("de", "nl"):
        return f"{день} {гл} {имя} {слот} {место}."
    if язык == "tr":
        return f"{имя} {день} {место} {слот} {гл}."
    return f"{день} {имя} {гл} {слот} {место}."


def открытый_факт(язык, роль, день, имя, род, k, n, вещь, место):
    """The fact with the role `роль` (0..4) unfilled — its placeholder in place."""
    р, пр = РАМКИ[язык][k], ПРОБЕЛЫ[язык]
    if роль == 0:
        имя, род = пр["кто"], "m"
    if роль == 4:
        день = пр["когда"]
    if роль == 3:
        место = пр["куда"][0 if _к_месту(язык, р) else 1]
    if роль == 1:
        ск = пр["сколько"]
        if isinstance(ск, tuple):
            ск = ск[1 if вещь[1] == "f" else 0]
        слот = f"{ск} {_много(язык, вещь)}"
    elif роль == 2:
        слот = пр["что"]
    else:
        слот = f"{n} {_вещь(язык, вещь, n)}"
    return _сборка(язык, день, имя, _глагол(язык, р, род), слот, место)


def запросы(язык, день, имя, род, k, n, вещь, место):
    """(open fact, its question) for every role — the question is the one
    the hole market would answer, and it never names the open filler."""
    вопросы = дыры(язык, день, имя, род, k, n, вещь, место)
    return tuple((открытый_факт(язык, роль, день, имя, род, k, n, вещь, место), вопросы[роль][0])
                 for роль in range(5))


def _имена():
    """(name, gender) per language from the packs — the actors of the frame.
    English names are written lowercase as the English worlds write them."""
    вон = {}
    for язык in ЯЗЫКИ:
        п = json.loads((КОРЕНЬ / "tools" / "langpacks" / f"{язык}.json").read_text(encoding="utf-8"))
        формы = п.get("person_forms") or {}
        if язык == "en":
            вон[язык] = tuple((n, "m") for n in п["person_names"][:16])
        else:
            вон[язык] = tuple((n if язык != "ru" else n.capitalize(), ф["gender"]) for n, ф in list(формы.items())[:16])
    return вон


ИМЕНА = _имена()
РОД = {язык: dict(ИМЕНА[язык]) for язык in ЯЗЫКИ}


def _вещь(язык, вещь, n):
    """The thing as the frame writes it beside the number n."""
    if язык == "en":
        return вещь[1]
    if язык == "ru":
        return rugram.форма(вещь, n)
    if язык in ("de", "nl"):
        return вещь
    if язык == "pl":
        return вещь[0] if форма_счёта("pl", n) == "few" else вещь[1]
    return вещь[0]


def факт(язык, день, имя, род, k, n, вещь, место):
    """The frame with no hole; `род` is the actor's gender (ru, pl, fr)."""
    р = РАМКИ[язык][k]
    return _сборка(язык, день, имя, _глагол(язык, р, род), f"{n} {_вещь(язык, вещь, n)}", место)


def дыры(язык, день, имя, род, k, n, вещь, место):
    """Every role asked in turn: (question, answer) pairs, the answer being
    the filler the question removed. The question word names the role."""
    р = РАМКИ[язык][k]
    в = _вещь(язык, вещь, n)
    if язык == "en":
        прош, осн = р["прош"], р["осн"]
        return (
            (f"who {прош} {n} {в} {место} {день}?", f"{имя}."),
            (f"how many {в} did {имя} {осн} {место} {день}?", f"{n}."),
            (f"what did {имя} {осн} {место} {день}?", f"{n} {в}."),
            (f"where did {имя} {осн} {n} {в} {день}?", f"{место}."),
            (f"when did {имя} {осн} {n} {в} {место}?", f"{день}."),
        )
    if язык == "ru":
        гл = р["ж"] if род == "f" else р["м"]
        return (
            (f"кто {р['м']} {n} {в} {место} {день}?", f"{имя}."),
            (f"сколько {rugram.форма(вещь, 5)} {гл} {имя} {место} {день}?", f"{n}."),
            (f"что {гл} {имя} {место} {день}?", f"{n} {в}."),
            (f"{р['куда']} {гл} {имя} {n} {в} {день}?", f"{место}."),
            (f"когда {гл} {имя} {n} {в} {место}?", f"{день}."),
        )
    if язык == "de":
        гл = р["гл"]
        return (
            (f"wer {гл} {день} {n} {в} {место}?", f"{имя}."),
            (f"wie viele {в} {гл} {имя} {день} {место}?", f"{n}."),
            (f"was {гл} {имя} {день} {место}?", f"{n} {в}."),
            (f"{р['куда']} {гл} {имя} {день} {n} {в}?", f"{место}."),
            (f"wann {гл} {имя} {n} {в} {место}?", f"{день}."),
        )
    if язык == "es":
        гл = р["гл"]
        ск = "cuántas" if вещь[1] == "f" else "cuántos"
        return (
            (f"¿quién {гл} {n} {в} {место} {день}?", f"{имя}."),
            (f"¿{ск} {в} {гл} {имя} {место} {день}?", f"{n}."),
            (f"¿qué {гл} {имя} {место} {день}?", f"{n} {в}."),
            (f"¿dónde {гл} {имя} {n} {в} {день}?", f"{место}."),
            (f"¿cuándo {гл} {имя} {n} {в} {место}?", f"{день}."),
        )
    if язык == "it":
        гл = р["гл"]
        ск = "quante" if вещь[1] == "f" else "quanti"
        return (
            (f"chi {гл} {n} {в} {место} {день}?", f"{имя}."),
            (f"{ск} {в} {гл} {имя} {место} {день}?", f"{n}."),
            (f"che cosa {гл} {имя} {место} {день}?", f"{n} {в}."),
            (f"dove {гл} {имя} {n} {в} {день}?", f"{место}."),
            (f"quando {гл} {имя} {n} {в} {место}?", f"{день}."),
        )
    if язык == "tr":
        гл, вин = р["гл"], вещь[1]
        return (
            (f"{день} {место} {n} {вин} kim {гл}?", f"{имя}."),
            (f"{имя} {день} {место} kaç {в} {гл}?", f"{n}."),
            (f"{имя} {день} {место} ne {гл}?", f"{n} {в}."),
            (f"{имя} {день} {n} {вин} {р['куда']} {гл}?", f"{место}."),
            (f"{имя} {n} {вин} ne zaman {место} {гл}?", f"{день}."),
        )
    if язык == "pl":
        гл = р["ж"] if род == "f" else р["м"]
        return (
            (f"kto {р['м']} {n} {в} {место} {день}?", f"{имя}."),
            (f"ile {вещь[1]} {гл} {имя} {место} {день}?", f"{n}."),
            (f"co {гл} {имя} {место} {день}?", f"{n} {в}."),
            (f"gdzie {гл} {имя} {n} {в} {день}?", f"{место}."),
            (f"kiedy {гл} {имя} {n} {в} {место}?", f"{день}."),
        )
    if язык == "pt":
        гл = р["гл"]
        ск = "quantas" if вещь[1] == "f" else "quantos"
        return (
            (f"quem {гл} {n} {в} {место} {день}?", f"{имя}."),
            (f"{ск} {в} {имя} {гл} {место} {день}?", f"{n}."),
            (f"o que {имя} {гл} {место} {день}?", f"{n} {в}."),
            (f"onde {имя} {гл} {n} {в} {день}?", f"{место}."),
            (f"quando {имя} {гл} {n} {в} {место}?", f"{день}."),
        )
    if язык == "nl":
        гл = р["гл"]
        return (
            (f"wie {гл} {день} {n} {в} {место}?", f"{имя}."),
            (f"hoeveel {в} {гл} {имя} {день} {место}?", f"{n}."),
            (f"wat {гл} {имя} {день} {место}?", f"{n} {в}."),
            (f"waar {гл} {имя} {день} {n} {в}?", f"{место}."),
            (f"wanneer {гл} {имя} {n} {в} {место}?", f"{день}."),
        )
    гл = р["гл"]
    осн = гл.split(" ", 1)[1]                       # the participle unagreed
    прич = р["прич"][1 if вещь[1] == "f" else 0]    # agreed with the fronted object
    он = "elle" if род == "f" else "il"
    что = "qu'est-ce qu'" if имя[0].lower() in "aeiouhéè" else "qu'est-ce que "
    return (
        (f"qui {гл} {n} {в} {место} {день} ?", f"{имя}."),
        (f"combien de {в} {имя} a-t-{он} {прич} {место} {день} ?", f"{n}."),
        (f"{что}{имя} {гл} {место} {день} ?", f"{n} {в}."),
        (f"où {имя} a-t-{он} {осн} {n} {в} {день} ?", f"{место}."),
        (f"quand {имя} a-t-{он} {осн} {n} {в} {место} ?", f"{день}."),
    )


def _alt(слова):
    return "|".join(re.escape(с) for с in sorted(set(слова), key=len, reverse=True))


def _глаголы(язык):
    if язык == "en":
        return [р["прош"] for р in РАМКИ[язык]]
    if язык in ("ru", "pl"):
        return [г for р in РАМКИ[язык] for г in (р["м"], р["ж"])]
    return [р["гл"] for р in РАМКИ[язык]]


_ЛАТ = "[A-ZÀ-ŻİĞÖŞÜÇ][^\\W\\d_]+"      # a capitalised word of any Latin alphabet
_ЛАТ_СЛОВО = "[^\\W\\d_]+"
ФАКТ = {
    "en": re.compile(rf"^(?P<день>{_alt(ДНИ['en'])}) (?P<имя>[a-z]+) (?P<гл>{_alt(_глаголы('en'))}) (?P<n>\d+) "
                     rf"(?P<вещь>[a-z]+) (?P<место>{_alt(м for р in РАМКИ['en'] for м in р['места'])})\.$"),
    "ru": re.compile(rf"^(?P<день>{_alt(ДНИ['ru'])}) (?P<имя>[А-ЯЁ][а-яё]+) (?P<гл>{_alt(_глаголы('ru'))}) (?P<n>\d+) "
                     rf"(?P<вещь>[а-яё]+) (?P<место>{_alt(м for р in РАМКИ['ru'] for м in р['места'])})\.$"),
    "de": re.compile(rf"^(?P<день>{_alt(ДНИ['de'])}) (?P<гл>{_alt(_глаголы('de'))}) (?P<имя>{_ЛАТ}) (?P<n>\d+) "
                     rf"(?P<вещь>{_ЛАТ}) (?P<место>{_alt(м for р in РАМКИ['de'] for м in р['места'])})\.$"),
}
ФАКТ["nl"] = re.compile(rf"^(?P<день>{_alt(ДНИ['nl'])}) (?P<гл>{_alt(_глаголы('nl'))}) (?P<имя>{_ЛАТ}) (?P<n>\d+) "
                        rf"(?P<вещь>{_ЛАТ_СЛОВО}) (?P<место>{_alt(м for р in РАМКИ['nl'] for м in р['места'])})\.$")
ФАКТ["tr"] = re.compile(rf"^(?P<имя>{_ЛАТ}) (?P<день>{_alt(ДНИ['tr'])}) (?P<место>{_alt(м for р in РАМКИ['tr'] for м in р['места'])}) (?P<n>\d+) "
                        rf"(?P<вещь>{_ЛАТ_СЛОВО}) (?P<гл>{_alt(_глаголы('tr'))})\.$")
for _я in ("es", "it", "fr", "pt", "pl"):
    ФАКТ[_я] = re.compile(rf"^(?P<день>{_alt(ДНИ[_я])}) (?P<имя>{_ЛАТ}) (?P<гл>{_alt(_глаголы(_я))}) (?P<n>\d+) "
                          rf"(?P<вещь>{_ЛАТ_СЛОВО}) (?P<место>{_alt(м for р in РАМКИ[_я] for м in р['места'])})\.$")
СТРОКА = re.compile(r"^(?P<факт>[^.?]+\.)(?: (?P<вопрос>[^?]+?) ?\? (?P<ответ>[^.?]+)\.)?$")


def _открытый_образец(язык):
    """One regex per language: the fact with ANY one role replaced by its
    placeholder — the open role is read off which alternative matched."""
    пр = ПРОБЕЛЫ[язык]
    дни = _alt(ДНИ[язык]) + "|" + re.escape(пр["когда"])
    места = _alt(м for р in РАМКИ[язык] for м in р["места"]) + "|" + _alt(пр["куда"])
    глаголы = _alt(_глаголы(язык))
    ск = _alt(пр["сколько"] if isinstance(пр["сколько"], tuple) else (пр["сколько"],))
    if язык == "en":
        имя, слово = "[a-z]+", "[a-z]+"
    elif язык == "ru":
        имя, слово = "[А-ЯЁ][а-яё]+", "[а-яё]+"
    elif язык == "de":
        имя, слово = _ЛАТ, _ЛАТ
    else:
        имя, слово = _ЛАТ, _ЛАТ_СЛОВО
    имя = f"{имя}|{re.escape(пр['кто'])}"
    слот = rf"(?:(?P<n>\d+) (?P<вещь>{слово})|(?P<ск>{ск}) (?P<вещьм>{слово})|{re.escape(пр['что'])})"
    if язык in ("de", "nl"):
        return re.compile(rf"^(?P<день>{дни}) (?P<гл>{глаголы}) (?P<имя>{имя}) {слот} (?P<место>{места})\.$")
    if язык == "tr":
        return re.compile(rf"^(?P<имя>{имя}) (?P<день>{дни}) (?P<место>{места}) {слот} (?P<гл>{глаголы})\.$")
    return re.compile(rf"^(?P<день>{дни}) (?P<имя>{имя}) (?P<гл>{глаголы}) {слот} (?P<место>{места})\.$")


ОТКРЫТЫЙ = {язык: _открытый_образец(язык) for язык in ЯЗЫКИ}
ЗАПРОС = re.compile(r"^(?P<факт>[^.?]+\.) (?P<вопрос>[^?]+?) ?\?$")


def разобрать_запрос(строка):
    """(язык, roles, open role, question) of a line «open fact. question?»,
    None when it is not one; roles None when a filler is not the frame's."""
    м = ЗАПРОС.match(строка)
    if not м:
        return None
    for язык, образец in ОТКРЫТЫЙ.items():
        ф = образец.match(м["факт"])
        if not ф:
            continue
        пр = ПРОБЕЛЫ[язык]
        k, р = _рамка(язык, ф["гл"])
        if р is None:
            return None
        открытые = []
        if ф["имя"] == пр["кто"]:
            открытые.append(0)
        if ф["день"] == пр["когда"]:
            открытые.append(4)
        if ф["место"] in пр["куда"]:
            открытые.append(3)
        if ф["n"] is None:
            открытые.append(1 if ф["вещьм"] else 2)
        if len(открытые) != 1:
            return язык, None, None, м["вопрос"]
        роль = открытые[0]
        # the known fillers must be the frame's own
        n = int(ф["n"]) if ф["n"] else 5
        if ф["n"]:
            вещь = _та_вещь(язык, р, ф["вещь"], n)
        elif ф["вещьм"]:
            вещь = next((в for в in р["вещи"] if _много(язык, в) == ф["вещьм"]), None)
            ск = пр["сколько"]
            if вещь is not None and isinstance(ск, tuple) and ф["ск"] != ск[1 if вещь[1] == "f" else 0]:
                вещь = None
        else:
            вещь = р["вещи"][0]
        if роль == 3:
            место = р["места"][0]
            if ф["место"] != пр["куда"][0 if _к_месту(язык, р) else 1]:
                место = None
        else:
            место = ф["место"] if ф["место"] in р["места"] else None
        if роль == 0:
            имя, род = ИМЕНА[язык][0][0], "m"
            if язык in ("ru", "pl") and ф["гл"] != р["м"]:
                имя = None
        else:
            имя = ф["имя"]
            род = РОД[язык].get(имя)
            if род is None or (язык in ("ru", "pl") and ф["гл"] != (р["ж"] if род == "f" else р["м"])):
                имя = None
        день = ф["день"] if роль != 4 else ДНИ[язык][0]
        if вещь is None or место is None or имя is None:
            return язык, None, роль, м["вопрос"]
        return язык, (день, имя, род, k, n, вещь, место), роль, м["вопрос"]
    return None


def _рамка(язык, глагол):
    for k, р in enumerate(РАМКИ[язык]):
        формы = (р["прош"],) if язык == "en" else (р["м"], р["ж"]) if язык in ("ru", "pl") else (р["гл"],)
        if глагол in формы:
            return k, р
    return None, None


def _та_вещь(язык, р, слово, n):
    for в in р["вещи"]:
        if _вещь(язык, в, n) == слово:
            return в
    return None


def разобрать(строка):
    """(язык, roles, question, answer) of a line of the hole market, or None
    when the line's fact is not a frame of this house. roles is None when the
    frame's own verb, day and place stand beside a thing the frame does not
    carry, a count form that disagrees, or an undeclared name (fr, ru)."""
    м = СТРОКА.match(строка)
    if not м:
        return None
    for язык, образец in ФАКТ.items():
        ф = образец.match(м["факт"])
        if not ф:
            continue
        n = int(ф["n"])
        k, р = _рамка(язык, ф["гл"])
        if р is None:
            return None
        вещь = _та_вещь(язык, р, ф["вещь"], n)
        место = ф["место"] if ф["место"] in р["места"] else None
        # THE ACTOR IS A NAME OF THE PACK, and where the verb carries gender
        # the two agree («Анна положил» is no frame of this house).
        род = РОД[язык].get(ф["имя"])
        if язык in ("ru", "pl") and род is not None and ф["гл"] != (р["ж"] if род == "f" else р["м"]):
            род = None
        if вещь is None or место is None or род is None:
            return язык, None, м["вопрос"], м["ответ"]
        return язык, (ф["день"], ф["имя"], род, k, n, вещь, место), м["вопрос"], м["ответ"]
    return None


def судить(строка):
    """(judged, true): a bare frame is true by its forms; a question is true
    iff it and its answer are one lawful hole of the fact."""
    з = разобрать_запрос(строка)
    if з is not None:
        язык, роли, роль, вопрос = з
        if роли is None:
            return (True, False)
        return (True, вопрос.rstrip(" ?") == запросы(язык, *роли)[роль][1].rstrip(" ?"))
    ч = разобрать(строка)
    if ч is None:
        return (False, False)
    язык, роли, вопрос, ответ = ч
    if роли is None:
        return (True, False)
    if вопрос is None:
        return (True, True)
    пары = {(в.rstrip(" ?"), о) for в, о in дыры(язык, *роли)}
    return (True, (вопрос.rstrip(" ?"), f"{ответ}.") in пары)
