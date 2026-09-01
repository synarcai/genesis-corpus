#!/usr/bin/env python3
"""СЕМЯ ТУРЕЦКОГО — три беды в одном пакете, и все три нарочно.

ПЕРВАЯ: СЧЁТ БЕЗ СОГЛАСОВАНИЯ. После числительного турецкое имя стоит
в ЕДИНСТВЕННОМ числе — «beş kedi», пять кот. Множественное у языка
есть, но счёт его не требует. Русский движок знает три формы, английский
две; здесь форма ОДНА на все счета. Всякий прибор, требующий РАЗЛИЧИЯ
между формами счёта, на этом упрётся.

ВТОРАЯ: ЧИСЛИТЕЛЬНОЕ ИЗ ДВУХ СЛОВ. Одиннадцать есть «on bir» — десять
один. Это ровно то составное числительное, о которое сегодня разбилась
арифметика на украинском «дев'яносто дев'ять»; здесь оно объявлено
ЧЕСТНО — таблицей, — и потому должно быть прочтено как один токен по
закону «объявленный токен главнее разбиения по глифам».

ТРЕТЬЯ: ГАРМОНИЯ ГЛАСНЫХ. Окончание не одно, а четыре, и выбор его
решает ПОСЛЕДНЯЯ ГЛАСНАЯ ОСНОВЫ: yaz-ıyor, gel-iyor, gör-üyor. Правило
пакета делит глаголы на четыре класса не по виду окончания, а по звуку
основы — и встроенный оракул проверит все четыре, выведя формы из
правила и сверив с таблицей.

ЯРУС ПЕРВЫЙ: строение зелено, формы не проверены носителем.
"""

TR = {
 "lang": "tr", "script": "latin",
 "script_range": "A-Za-zÇĞİIÖŞÜçğıiöşü",
 "graphemes": "abcçdefgğhıijklmnoöprsştuüvyz",
 "diacritics": "çğıöşü",
 "comment": ("THIRTEENTH PACK. Turkish: agglutination, vowel harmony in "
             "four classes, teens written as two words, and NO count "
             "agreement at all — after a numeral the noun stays "
             "singular. Three architectural probes in one pack. TIER 1."),
 "numerals": {"0": "sıfır", "1": "bir", "2": "iki", "3": "üç",
              "4": "dört", "5": "beş", "6": "altı", "7": "yedi",
              "8": "sekiz", "9": "dokuz", "10": "on",
              "11": "on bir", "12": "on iki", "13": "on üç",
              "14": "on dört", "15": "on beş", "16": "on altı",
              "17": "on yedi", "18": "on sekiz", "19": "on dokuz",
              "20": "yirmi", "30": "otuz", "40": "kırk", "50": "elli",
              "60": "altmış", "70": "yetmiş", "80": "seksen",
              "90": "doksan", "100": "yüz"},
 # ФОРМА ОДНА НА ВСЕ СЧЕТА: числительное не требует множественного.
 "count_agreement": [{"form": "one"}],
 "ops": {"artı": "+", "eksi": "-", "çarpı": "*", "bölü": "/",
         "eder": "="},
 "w_plus": "artı", "w_minus": "eksi", "w_times": "çarpı",
 "w_div": "bölü", "w_eq": "eder",
 "persons": ["ben", "sen", "o", "biz", "siz", "onlar"],
 "verbs": {
   "yazmak": ["yazıyorum", "yazıyorsun", "yazıyor", "yazıyoruz",
              "yazıyorsunuz", "yazıyorlar"],
   "bakmak": ["bakıyorum", "bakıyorsun", "bakıyor", "bakıyoruz",
              "bakıyorsunuz", "bakıyorlar"],
   "almak": ["alıyorum", "alıyorsun", "alıyor", "alıyoruz",
             "alıyorsunuz", "alıyorlar"],
   "gelmek": ["geliyorum", "geliyorsun", "geliyor", "geliyoruz",
              "geliyorsunuz", "geliyorlar"],
   "sevmek": ["seviyorum", "seviyorsun", "seviyor", "seviyoruz",
              "seviyorsunuz", "seviyorlar"],
   "bilmek": ["biliyorum", "biliyorsun", "biliyor", "biliyoruz",
              "biliyorsunuz", "biliyorlar"],
   "görmek": ["görüyorum", "görüyorsun", "görüyor", "görüyoruz",
              "görüyorsunuz", "görüyorlar"],
   "gülmek": ["gülüyorum", "gülüyorsun", "gülüyor", "gülüyoruz",
              "gülüyorsunuz", "gülüyorlar"],
   "gitmek": ["gidiyorum", "gidiyorsun", "gidiyor", "gidiyoruz",
              "gidiyorsunuz", "gidiyorlar"]},
 "nouns": {
   "kitap": ["kitap", "kitaplar"], "ev": ["ev", "evler"],
   "masa": ["masa", "masalar"], "çiçek": ["çiçek", "çiçekler"],
   "şehir": ["şehir", "şehirler"], "kağıt": ["kağıt", "kağıtlar"],
   "kedi": ["kedi", "kediler"], "kilo": ["kilo", "kilolar"],
   "sınav": ["sınav", "sınavlar"], "tren": ["tren", "trenler"],
   "gazete": ["gazete", "gazeteler"], "göz": ["göz", "gözler"],
   "yol": ["yol", "yollar"], "öğrenci": ["öğrenci", "öğrenciler"],
   "ağaç": ["ağaç", "ağaçlar"], "su": ["su", "sular"],
   "güneş": ["güneş", "güneşler"], "ışık": ["ışık", "ışıklar"],
   "dağ": ["dağ", "dağlar"], "jeton": ["jeton", "jetonlar"],
   "cam": ["cam", "camlar"], "fil": ["fil", "filler"],
   "vapur": ["vapur", "vapurlar"], "para": ["para", "paralar"],
   "uçak": ["uçak", "uçaklar"], "lale": ["lale", "laleler"],
   "jüri": ["jüri", "jüriler"], "hava": ["hava", "havalar"],
   "fikir": ["fikir", "fikirler"], "resim": ["resim", "resimler"],
   "cevap": ["cevap", "cevaplar"]},
 "words": {
   "count_lexicon": ["işte", "burada"],
   "count_templates": ["işte {one}.", "işte {many}.",
                       "burada {many}."],
   "def_lexicon": ["nesne", "şey", "nedir"],
   "def_templates": ["{one} bir nesnedir."]},
 "irregulars": ["gidiyorum", "gidiyor", "filler", "yollar"],
 "probe": ["ben", "sen", "o", "biz", "siz", "onlar", "işte", "burada",
           "nesne", "şey", "bir", "artı", "eksi", "çarpı", "bölü",
           "eder", "kedi", "kitap"],
 "refusals": [
   {"bad": "beş kediler.", "good": "beş kedi.", "reason": "agreement"},
   {"bad": "ben okuyorsun.", "good": "ben koşuyorum.",
    "reason": "agreement"},
   {"bad": "iki eviniz.", "good": "iki ev.", "reason": "agreement"},
   {"bad": "yedi ne renktedir ?", "good": "nesne nedir ?",
    "reason": "unanswerable"},
   {"bad": "ev artı kedi eder ?", "good": "on eksi bir dokuz eder.",
    "reason": "type_mismatch"}],
 # ГАРМОНИЯ ГЛАСНЫХ ЕСТЬ ПРАВИЛО, А НЕ СПИСОК: класс глагола назван
 # по звуку, в который переходит последняя гласная основы, и оракул
 # выводит все шесть форм из одного окончания класса. gitmek стоит
 # «*» — у него меняется СОГЛАСНАЯ основы (t → d), чего гармония
 # гласных не объясняет: честный отказ правила, а не подгон.
 "verb_rule": {
   "classes": {
     "ı": {"strip": "mak",
           "endings": ["ıyorum", "ıyorsun", "ıyor", "ıyoruz",
                       "ıyorsunuz", "ıyorlar"]},
     "i": {"strip": "mek",
           "endings": ["iyorum", "iyorsun", "iyor", "iyoruz",
                       "iyorsunuz", "iyorlar"]},
     "ü": {"strip": "mek",
           "endings": ["üyorum", "üyorsun", "üyor", "üyoruz",
                       "üyorsunuz", "üyorlar"]}},
   "of": {"yazmak": "ı", "bakmak": "ı", "almak": "ı", "gelmek": "i",
          "sevmek": "i", "bilmek": "i", "görmek": "ü", "gülmek": "ü",
          "gitmek": "*"}},
}
