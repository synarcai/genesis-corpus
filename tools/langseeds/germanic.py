#!/usr/bin/env python3
"""СЕМЕНА ГЕРМАНСКИХ: нидерландский и шведский.

ШВЕДСКИЙ ВЗЯТ РАДИ ИСПЫТАНИЯ, А НЕ РАДИ ЧИСЛА. В нём НЕТ ЛИЧНОГО
СПРЯЖЕНИЯ: «jag talar», «du talar», «vi talar» — одна форма на все
шесть лиц. Всякий движок, требующий РАЗЛИЧНЫХ клеток парадигмы, на нём
упрётся; и если упрётся наш — это находка о движке, а не о шведском.
Язык без личного согласования законен, и архитектура обязана его брать.

ЯРУС ПЕРВЫЙ: строение зелено, формы не проверены носителем.
"""

NL = {
 "lang": "nl", "script": "latin", "script_range": "A-Za-zÉÈËÏÖÜéèëïöü",
 "graphemes": "abcdefghijklmnopqrstuvwxyzéëï",
 "diacritics": "éèëïöü",
 "comment": ("NINTH PACK. Dutch: the verb has three distinct present "
             "cells, not six — singular 1, singular 2/3, and one plural "
             "for all three persons. TIER 1."),
 "numerals": {"0": "nul", "1": "een", "2": "twee", "3": "drie",
              "4": "vier", "5": "vijf", "6": "zes", "7": "zeven",
              "8": "acht", "9": "negen", "10": "tien", "11": "elf",
              "12": "twaalf", "13": "dertien", "14": "veertien",
              "15": "vijftien", "16": "zestien", "17": "zeventien",
              "18": "achttien", "19": "negentien", "20": "twintig",
              "30": "dertig", "40": "veertig", "50": "vijftig",
              "60": "zestig", "70": "zeventig", "80": "tachtig", "90": "negentig", "100": "honderd"},
 "count_agreement": [{"mod": 10, "in": [1], "form": "one"},
                     {"form": "many"}],
 "ops": {"plus": "+", "min": "-", "keer": "*", "gedeeld": "/", "is": "="},
 "w_plus": "plus", "w_minus": "min", "w_times": "keer",
 "w_div": "gedeeld", "w_eq": "is",
 "persons": ["ik", "jij", "hij", "wij", "jullie", "zij"],
 "verbs": {
   "werken": ["werk", "werkt", "werkt", "werken", "werken", "werken"],
   "lezen": ["lees", "leest", "leest", "lezen", "lezen", "lezen"],
   "eten": ["eet", "eet", "eet", "eten", "eten", "eten"],
   "lopen": ["loop", "loopt", "loopt", "lopen", "lopen", "lopen"],
   "kopen": ["koop", "koopt", "koopt", "kopen", "kopen", "kopen"],
   "drinken": ["drink", "drinkt", "drinkt", "drinken", "drinken",
               "drinken"],
   "zingen": ["zing", "zingt", "zingt", "zingen", "zingen", "zingen"],
   "maken": ["maak", "maakt", "maakt", "maken", "maken", "maken"]},
 "nouns": {
   "boek": ["het boek", "de boeken"],
   "huis": ["het huis", "de huizen"],
   "tafel": ["de tafel", "de tafels"],
   "bloem": ["de bloem", "de bloemen"],
   "stad": ["de stad", "de steden"],
   "papier": ["het papier", "de papieren"],
   "kat": ["de kat", "de katten"],
   "kilo": ["de kilo", "de kilos"],
   "examen": ["het examen", "de examens"],
   "taxi": ["de taxi", "de taxis"],
   "trein": ["de trein", "de treinen"],
   "quiz": ["de quiz", "de quizzen"],
   "café": ["het café", "de cafés"],
   "ruïne": ["de ruïne", "de ruïnes"],
   "yoghurt": ["de yoghurt", "de yoghurts"],
   "jas": ["de jas", "de jassen"],
   "wolk": ["de wolk", "de wolken"],
   "zon": ["de zon", "de zonnen"],
   # БУКВА, ОБЪЯВЛЕННАЯ В АЛФАВИТЕ, ОБЯЗАНА ЖИТЬ: «ë» в нидерландском
   # живёт трема́й на стыке гласных, и слово взято РАДИ БУКВЫ.
   "reeks": ["de reeks", "de reeksen"],
   "coëfficiënt": ["de coëfficiënt", "de coëfficiënten"]},
 "words": {
   "count_lexicon": ["hier", "daar"],
   "count_templates": ["hier is {one}.", "hier zijn {many}.",
                       "daar zijn {many}."],
   "def_lexicon": ["ding", "een", "voorwerp"],
   "def_templates": ["{one} is een ding."]},
 "irregulars": ["huizen", "steden", "lees", "eet", "quizzen"],
 "probe": ["de", "het", "een", "ik", "jij", "hij", "wij", "jullie",
           "zij", "hier", "daar", "ding", "voorwerp", "is", "zijn",
           "plus", "min", "keer", "gedeeld", "kat", "boek"],
 "refusals": [
   {"bad": "de boek is klein.", "good": "het boek is klein.",
    "reason": "agreement"},
   {"bad": "de huis zijn groot.", "good": "de huizen zijn groot.",
    "reason": "agreement"},
   {"bad": "ik werkt.", "good": "ik dans.", "reason": "agreement"},
   {"bad": "welke kleur heeft zeven ?", "good": "wat is een voorwerp ?",
    "reason": "unanswerable"},
   {"bad": "boek plus huis is ?",
    "good": "honderd min een is negenennegentig.",
    "reason": "type_mismatch"}],
 "verb_rule": {
   "classes": {
     "en": {"strip": "en",
            "endings": ["", "t", "t", "en", "en", "en"]}},
   "of": {"werken": "en", "lezen": "*", "eten": "*", "lopen": "*",
          "kopen": "*", "drinken": "en", "zingen": "en",
          "maken": "*"}},
}

SV = {
 "lang": "sv", "script": "latin", "script_range": "A-Za-zÅÄÖåäö",
 "graphemes": "abcdefghijklmnopqrstuvwxyzåäö",
 "diacritics": "åäö",
 "comment": ("TENTH PACK, AND THE FIRST WITHOUT PERSON AGREEMENT AT "
             "ALL. Swedish conjugates by TENSE, never by person: «jag "
             "talar», «vi talar» — one form for all six. The paradigm "
             "declared here is therefore TENSE (present, past, "
             "supine), and the six persons take the SAME cell. If the "
             "engine demands distinct person cells, that is a finding "
             "about the engine: a language without person agreement is "
             "lawful, and the architecture must take it. TIER 1."),
 "numerals": {"0": "noll", "1": "ett", "2": "två", "3": "tre",
              "4": "fyra", "5": "fem", "6": "sex", "7": "sju",
              "8": "åtta", "9": "nio", "10": "tio", "11": "elva",
              "12": "tolv", "13": "tretton", "14": "fjorton",
              "15": "femton", "16": "sexton", "17": "sjutton",
              "18": "arton", "19": "nitton", "20": "tjugo",
              "30": "trettio", "40": "fyrtio", "50": "femtio",
              "60": "sextio", "70": "sjuttio", "80": "åttio", "90": "nittio", "100": "hundra"},
 "count_agreement": [{"mod": 10, "in": [1], "form": "one"},
                     {"form": "many"}],
 "ops": {"plus": "+", "minus": "-", "gånger": "*", "delat": "/",
         "blir": "="},
 "w_plus": "plus", "w_minus": "minus", "w_times": "gånger",
 "w_div": "delat", "w_eq": "blir",
 # ЛИЦА ЕСТЬ, СПРЯЖЕНИЯ НЕТ: все шесть берут одну клетку, и это факт
 # языка, а не бедность пакета.
 "persons": ["jag", "du", "han", "vi", "ni", "de"],
 "verbs": {
   "tala": ["talar", "talar", "talar", "talar", "talar", "talar"],
   "läsa": ["läser", "läser", "läser", "läser", "läser", "läser"],
   "äta": ["äter", "äter", "äter", "äter", "äter", "äter"],
   "springa": ["springer", "springer", "springer", "springer",
               "springer", "springer"],
   "köpa": ["köper", "köper", "köper", "köper", "köper", "köper"],
   "dricka": ["dricker", "dricker", "dricker", "dricker", "dricker",
              "dricker"],
   "sjunga": ["sjunger", "sjunger", "sjunger", "sjunger", "sjunger",
              "sjunger"],
   "göra": ["gör", "gör", "gör", "gör", "gör", "gör"]},
 "nouns": {
   "bok": ["en bok", "böcker"],
   "hus": ["ett hus", "hus"],
   "bord": ["ett bord", "bord"],
   "blomma": ["en blomma", "blommor"],
   "stad": ["en stad", "städer"],
   "papper": ["ett papper", "papper"],
   "katt": ["en katt", "katter"],
   "kilo": ["ett kilo", "kilon"],
   "examen": ["en examen", "examina"],
   "taxi": ["en taxi", "taxibilar"],
   "tåg": ["ett tåg", "tåg"],
   "zebra": ["en zebra", "zebror"],
   "quiz": ["ett quiz", "quiz"],
   "väg": ["en väg", "vägar"],
   "yta": ["en yta", "ytor"],
   "jord": ["en jord", "jordar"],
   "ö": ["en ö", "öar"],
   # «w» в шведском живёт лишь в заимствованиях — и это факт языка,
   # а не пробел пакета; слово взято ради буквы.
   "watt": ["ett watt", "watt"],
   "webb": ["en webb", "webbar"]},
 "words": {
   "count_lexicon": ["här", "där"],
   "count_templates": ["här är {one}.", "här är {many}.",
                       "där är {many}."],
   "def_lexicon": ["sak", "ting", "föremål"],
   "def_templates": ["{one} är en sak."]},
 "irregulars": ["böcker", "städer", "gör", "examina", "öar"],
 "probe": ["en", "ett", "jag", "du", "han", "vi", "ni", "de", "här",
           "där", "sak", "ting", "föremål", "är", "plus", "minus",
           "gånger", "delat", "blir", "katt", "bok"],
 "refusals": [
   {"bad": "ett bok är liten.", "good": "en bok är liten.",
    "reason": "agreement"},
   {"bad": "en hus är stora.", "good": "ett hus är stort.",
    "reason": "agreement"},
   {"bad": "jag talarar.", "good": "jag dansar.", "reason": "agreement"},
   {"bad": "vilken färg har sju ?", "good": "vad är ett föremål ?",
    "reason": "unanswerable"},
   {"bad": "bok plus hus blir ?",
    "good": "hundra minus ett blir nittionio.",
    "reason": "type_mismatch"}],
}
