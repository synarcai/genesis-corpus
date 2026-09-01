#!/usr/bin/env python3
"""СЕМЕНА СЛАВЯНСКИХ: польский и украинский.

ОБА ВЗЯТЫ РАДИ ИСПЫТАНИЯ ПИСЬМА И СЧЁТА. Польский — латиница с
диакритикой, какой нет ни у кого (ą ę ł ń ś ź ż ć ó); украинский —
кириллица с четырьмя буквами, которых нет в русской (ґ є і ї), и
апострофом внутри слова. Правило счёта у обоих то же, что в русском
(1 / 2-4 / 5+), и потому объявляется одинаково — общее живёт общим.

ЯРУС ПЕРВЫЙ: строение зелено, формы не проверены носителем.
"""

СЧЁТ_СЛАВ = [{"mod": 100, "in": [11, 12, 13, 14], "form": "many"},
             {"mod": 10, "in": [1], "form": "one"},
             {"mod": 10, "in": [2, 3, 4], "form": "few"},
             {"form": "many"}]

PL = {
 "lang": "pl", "script": "latin",
 "script_range": "A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż",
 "graphemes": "aąbcćdeęfghijklłmnńoóprsśtuwyzźż",
 "diacritics": "ąćęłńóśźż",
 "comment": ("ELEVENTH PACK. Polish: the Slavic count law (1 / 2-4 / "
             "5+ with the teens exception) on a Latin alphabet, and "
             "nine diacritics no other pack carries. TIER 1."),
 "numerals": {"0": "zero", "1": "jeden", "2": "dwa", "3": "trzy",
              "4": "cztery", "5": "pięć", "6": "sześć", "7": "siedem",
              "8": "osiem", "9": "dziewięć", "10": "dziesięć",
              "11": "jedenaście", "12": "dwanaście",
              "13": "trzynaście", "14": "czternaście",
              "15": "piętnaście", "16": "szesnaście",
              "17": "siedemnaście", "18": "osiemnaście",
              "19": "dziewiętnaście", "20": "dwadzieścia",
              "30": "trzydzieści", "40": "czterdzieści",
              "50": "pięćdziesiąt", "60": "sześćdziesiąt",
              "70": "siedemdziesiąt", "80": "osiemdziesiąt", "90": "dziewięćdziesiąt", "100": "sto"},
 "count_agreement": СЧЁТ_СЛАВ,
 "ops": {"plus": "+", "minus": "-", "razy": "*", "podzielone": "/",
         "równa": "="},
 "w_plus": "plus", "w_minus": "minus", "w_times": "razy",
 "w_div": "podzielone", "w_eq": "równa",
 "persons": ["ja", "ty", "on", "my", "wy", "oni"],
 "verbs": {
   "czytać": ["czytam", "czytasz", "czyta", "czytamy", "czytacie",
              "czytają"],
   "śpiewać": ["śpiewam", "śpiewasz", "śpiewa", "śpiewamy",
               "śpiewacie", "śpiewają"],
   "pytać": ["pytam", "pytasz", "pyta", "pytamy", "pytacie", "pytają"],
   "kochać": ["kocham", "kochasz", "kocha", "kochamy", "kochacie",
              "kochają"],
   "mieszkać": ["mieszkam", "mieszkasz", "mieszka", "mieszkamy",
                "mieszkacie", "mieszkają"],
   "słuchać": ["słucham", "słuchasz", "słucha", "słuchamy",
               "słuchacie", "słuchają"],
   "grać": ["gram", "grasz", "gra", "gramy", "gracie", "grają"],
   "znać": ["znam", "znasz", "zna", "znamy", "znacie", "znają"]},
 "nouns": {
   "książka": ["książka", "książki"], "dom": ["dom", "domy"],
   "stół": ["stół", "stoły"], "kwiat": ["kwiat", "kwiaty"],
   "miasto": ["miasto", "miasta"], "papier": ["papier", "papiery"],
   "kot": ["kot", "koty"], "kilogram": ["kilogram", "kilogramy"],
   "egzamin": ["egzamin", "egzaminy"],
   "taksówka": ["taksówka", "taksówki"],
   "pociąg": ["pociąg", "pociągi"], "gazeta": ["gazeta", "gazety"],
   "źródło": ["źródło", "źródła"], "żaba": ["żaba", "żaby"],
   "ćma": ["ćma", "ćmy"], "łąka": ["łąka", "łąki"],
   "koń": ["koń", "konie"], "ściana": ["ściana", "ściany"],
   "jabłko": ["jabłko", "jabłka"], "ręka": ["ręka", "ręce"],
   "farba": ["farba", "farby"], "fala": ["fala", "fale"]},
 "words": {
   "count_lexicon": ["tutaj", "oto"],
   "count_templates": ["oto {one}.", "oto {many}.", "tutaj {many}."],
   "def_lexicon": ["rzecz", "przedmiot", "jest"],
   "def_templates": ["{one} to rzecz."]},
 "irregulars": ["ręce", "konie", "stoły", "źródła", "jabłka"],
 "probe": ["ja", "ty", "on", "my", "wy", "oni", "oto", "tutaj",
           "rzecz", "przedmiot", "to", "plus", "minus", "razy",
           "podzielone", "równa", "kot", "dom"],
 "refusals": [
   {"bad": "dwa kot.", "good": "dwa koty.", "reason": "agreement"},
   {"bad": "pięć koty.", "good": "pięć kotów.", "reason": "agreement"},
   {"bad": "ja czytasz.", "good": "ja tańczę.", "reason": "agreement"},
   {"bad": "jaki kolor ma siedem ?", "good": "co to jest przedmiot ?",
    "reason": "unanswerable"},
   {"bad": "dom plus kot równa ?",
    "good": "sto minus jeden równa dziewięćdziesiąt dziewięć.",
    "reason": "type_mismatch"}],
 "verb_rule": {
   "classes": {
     "ać": {"strip": "ać",
            "endings": ["am", "asz", "a", "amy", "acie", "ają"]}},
   "of": {"czytać": "ać", "śpiewać": "ać", "pytać": "ać",
          "kochać": "ać", "mieszkać": "ać", "słuchać": "ać",
          "grać": "ać", "znać": "ać"}},
}

UK = {
 "lang": "uk", "script": "cyrillic", "script_range": "А-Яа-яЁёҐґЄєІіЇї",
 "graphemes": "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя",
 "diacritics": "ґєії",
 "comment": ("TWELFTH PACK. Ukrainian: Cyrillic with four letters the "
             "Russian pack does not carry (ґ є і ї) and an apostrophe "
             "INSIDE the word («п'ять») — a sign that is neither letter "
             "nor punctuation there. TIER 1."),
 "numerals": {"0": "нуль", "1": "один", "2": "два", "3": "три",
              "4": "чотири", "5": "п'ять", "6": "шість", "7": "сім",
              "8": "вісім", "9": "дев'ять", "10": "десять",
              "11": "одинадцять", "12": "дванадцять",
              "13": "тринадцять", "14": "чотирнадцять",
              "15": "п'ятнадцять", "16": "шістнадцять",
              "17": "сімнадцять", "18": "вісімнадцять",
              "19": "дев'ятнадцять", "20": "двадцять",
              "30": "тридцять", "40": "сорок", "50": "п'ятдесят",
              "60": "шістдесят", "70": "сімдесят", "80": "вісімдесят", "90": "дев'яносто", "100": "сто"},
 "count_agreement": СЧЁТ_СЛАВ,
 "ops": {"плюс": "+", "мінус": "-", "помножити": "*",
         "поділити": "/", "дорівнює": "="},
 "w_plus": "плюс", "w_minus": "мінус", "w_times": "помножити",
 "w_div": "поділити", "w_eq": "дорівнює",
 "persons": ["я", "ти", "він", "ми", "ви", "вони"],
 "verbs": {
   "читати": ["читаю", "читаєш", "читає", "читаємо", "читаєте",
              "читають"],
   "співати": ["співаю", "співаєш", "співає", "співаємо", "співаєте",
               "співають"],
   "питати": ["питаю", "питаєш", "питає", "питаємо", "питаєте",
              "питають"],
   "гуляти": ["гуляю", "гуляєш", "гуляє", "гуляємо", "гуляєте",
              "гуляють"],
   "знати": ["знаю", "знаєш", "знає", "знаємо", "знаєте", "знають"],
   "думати": ["думаю", "думаєш", "думає", "думаємо", "думаєте",
              "думають"],
   "слухати": ["слухаю", "слухаєш", "слухає", "слухаємо", "слухаєте",
               "слухають"],
   "чекати": ["чекаю", "чекаєш", "чекає", "чекаємо", "чекаєте",
              "чекають"]},
 "nouns": {
   "книга": ["книга", "книги"], "дім": ["дім", "доми"],
   "стіл": ["стіл", "столи"], "квітка": ["квітка", "квітки"],
   "місто": ["місто", "міста"], "папір": ["папір", "папери"],
   "кіт": ["кіт", "коти"], "кілограм": ["кілограм", "кілограми"],
   "іспит": ["іспит", "іспити"], "потяг": ["потяг", "потяги"],
   "газета": ["газета", "газети"], "ґанок": ["ґанок", "ґанки"],
   "щука": ["щука", "щуки"], "яблуко": ["яблуко", "яблука"],
   "їжак": ["їжак", "їжаки"], "єнот": ["єнот", "єноти"],
   "юнак": ["юнак", "юнаки"], "хмара": ["хмара", "хмари"],
   "цибуля": ["цибуля", "цибулі"], "жаба": ["жаба", "жаби"],
   "фарба": ["фарба", "фарби"], "форма": ["форма", "форми"]},
 "words": {
   "count_lexicon": ["ось", "тут"],
   "count_templates": ["ось {one}.", "ось {many}.", "тут {many}."],
   "def_lexicon": ["річ", "предмет", "це"],
   "def_templates": ["{one} — це річ."]},
 "irregulars": ["столи", "доми", "коти", "міста", "яблука"],
 "probe": ["я", "ти", "він", "ми", "ви", "вони", "ось", "тут", "річ",
           "предмет", "це", "плюс", "мінус", "помножити", "поділити",
           "дорівнює", "кіт", "книга"],
 "refusals": [
   {"bad": "два кіт.", "good": "два коти.", "reason": "agreement"},
   {"bad": "п'ять коти.", "good": "п'ять котів.",
    "reason": "agreement"},
   {"bad": "я читаєш.", "good": "я танцюю.", "reason": "agreement"},
   {"bad": "який колір має сім ?", "good": "що таке предмет ?",
    "reason": "unanswerable"},
   {"bad": "дім плюс кіт дорівнює ?",
    "good": "сто мінус один дорівнює дев'яносто дев'ять.",
    "reason": "type_mismatch"}],
 "verb_rule": {
   "classes": {
     "ати": {"strip": "ати",
             "endings": ["аю", "аєш", "ає", "аємо", "аєте", "ають"]},
     "яти": {"strip": "яти",
             "endings": ["яю", "яєш", "яє", "яємо", "яєте", "яють"]}},
   "of": {"читати": "ати", "співати": "ати", "питати": "ати",
          "гуляти": "яти", "знати": "ати", "думати": "ати",
          "слухати": "ати", "чекати": "ати"}},
}
