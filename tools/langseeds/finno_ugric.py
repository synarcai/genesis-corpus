#!/usr/bin/env python3
"""СЕМЕНА ФИНСКОГО И ВЕНГЕРСКОГО — три пробы, и одна из них радостная.

ПРОБА ПЕРВАЯ: ПЯТНАДЦАТЬ ПАДЕЖЕЙ. Финское «в доме» есть talossa, «из
дома» — talosta, «в дом» — taloon: не предлог, а ОКОНЧАНИЕ, и таких
окончаний полтора десятка. Число клеток движок берёт БЕЗ ЖАЛОБЫ —
парадигма объявляется списком, и двенадцать клеток ему ровно так же
хороши, как две. Упирается он в другое, и об этом ниже.

ПРОБА ВТОРАЯ: ЧЕРЕДОВАНИЕ СТУПЕНЕЙ. kukka → kukan, katu → kadun,
kauppa → kaupan: меняется НЕ окончание, а согласная ОСНОВЫ. Правило
пакета устроено как «отсечь хвост, прирастить окончание», и потому
чередование им, казалось бы, невыразимо. ОКАЗАЛОСЬ ВЫРАЗИМО, и это
главная радостная находка семени: класс называется не по окончанию, а
по ЧЕРЕДОВАНИЮ, и отсекается вся чередующаяся часть — «lukea» с
отсечением «kea» даёт основу «lu», а окончания несут обе ступени
(«en» слабую, «kee» сильную). Оракул правил вывёл так все пятнадцать
финских глаголов и сошёлся с таблицей. Чего НЕ вышло — приложить то же
правило к ИМЕНАМ: `verb_rule` вешается кузней только на `verb_pres`, и
падежная парадигма осталась перечнем форм.

ПРОБА ТРЕТЬЯ: ОПРЕДЕЛЁННОЕ СПРЯЖЕНИЕ. Венгерский глагол меняется по
ОПРЕДЕЛЁННОСТИ ДОПОЛНЕНИЯ: látok valamit («вижу нечто») против látom
azt («вижу его»). Такого нет ни в одном нашем языке, и поля для этого
нет: клеток у глагола ровно шесть, и имена им кузня даёт по лицам
(s1..p3). Венгерская парадигма настоящего времени — ДВЕНАДЦАТЬ клеток,
и объявить её одним классом нельзя: список имён клеток в кузне обрезан
шестёркой, и класс с двенадцатью формами упал бы на «cells 6/12».
Второе спряжение поехало в слот прилагательного с честно названными
клетками; имя класса лжёт, клетки — нет.

ЧТО ЕЩЁ ВСКРЫЛОСЬ, И ЭТО ЗАКОН, А НЕ СЛУЧАЙ: ЗНАК ДЕЙСТВИЯ, УПРАВЛЯЮЩИЙ
ПАДЕЖОМ, ОБЪЯВИТЬ НЕЛЬЗЯ. Кузня пишет «{число} {знак} {число}», и
второе число приходит в словарной форме. Финское деление говорит
«kuusi jaettuna kolmella» — с адессивом на делителе; венгерское
умножение «kettő szorozva hárommal» — с инструменталем. Ни то, ни
другое в голый именительный не встаёт. Тот же самый закон уже был
куплен корейским равенством («삼 더하기 이는 오» приклеивает частицу к
предыдущему числу): ТРИ СЕМЬИ ЯЗЫКОВ, НЕ РОДНЫЕ ДРУГ ДРУГУ, УПЁРЛИСЬ В
ОДНУ И ТУ ЖЕ СТЕНУ. Где нашлось слово, берущее именительный, оно взято
(финское «kertaa», венгерское «meg», «mínusz», «egyenlő»); где не
нашлось — взят ВСЕОБЩИЙ ЗНАК («×», «÷»), какой обе письменности и
употребляют, а выдумывать неграмотную фразу не стали.

И ЧЕТВЁРТОЕ, САМОЕ ДОРОГОЕ, ЗАМЕРЕННОЕ ЗДЕСЬ ЖЕ: СЛОВАРЬ ОПЕРАЦИЙ У
СУДА АРИФМЕТИКИ ОДИН НА ВСЕ ЯЗЫКИ, И РАСХОЖДЕНИЕ ОН ГЛОТАЕТ МОЛЧА.
Венгерское и финское «per» значит ДЕЛЕНИЕ, итальянское «per» —
УМНОЖЕНИЕ («due per tre»); суд берёт последний пакет по имени файла, и
семьдесят четыре истинных венгерских деления были объявлены ЛОЖЬЮ.
Числительным тот же суд расхождения не прощает — он выходит с отказом
и называет оба значения; операциям прощает без единого слова. Оттого
«per» здесь снято, а находка осталась.

И ПЯТОЕ, ТОГО ЖЕ РОДА: финское «on» («есть») объявлено ТУРЕЦКИМ пакетом
ЧИСЛИТЕЛЬНЫМ (on = десять), а разбор пробует значения ПРЕЖДЕ равенств —
и вся финская словесная арифметика для суда корпуса НЕВИДИМА. Не ложна,
а нема: восемьдесят пять глифовых равенств он читает, четыреста
словесных не видит вовсе. Слово оставлено — «kaksi plus kolme on viisi»
есть верный финский.

И ВТОРОЙ ЗАКОН, ТОЖЕ ПОВТОРНЫЙ: СЛОВО РАВЕНСТВА ЕСТЬ САМОЕ ЧАСТОЕ
СЛОВО ЯЗЫКА. Финское «on» — связка «есть», и объявив её знаком «=», мы
заставляем судью арифметики видеть недоразобранное уравнение в каждом
обычном предложении. Ровно это уже случилось с японским «は». У
венгерского «egyenlő» такой беды нет — и разница видна числом:
`unparsed` у финского велик, у венгерского нуль.

ЧИСЛИТЕЛЬНЫЕ ОБЪЯВЛЕНЫ ДО СТА БЕЗ ДЫР — все единицы, все подростки,
все десятки и сотня, — и сверх того все произведения, какие сеет
кузня. Дыра в таблице заставила бы форж написать ЦИФРУ посреди речи, и
ни одно из девяти полей этого не увидело бы. Составные писаны ОДНИМ
объявлением, а не склейкой: финское kaksikymmentäyksi и венгерское
huszonegy суть одно слово каждое, и склеивать их из частей значило бы
выдумывать закон, которого пакет не знает.

ЯРУС ПЕРВЫЙ ОБОИМ: строение зелено, формы не проверены носителем.
"""

import re


def _знаки(*строки):
    """Буквенные знаки всего сказанного — ИНВЕНТАРЬ ВЫВОДИТСЯ, НЕ ПИШЕТСЯ.

    `graphemes` есть утверждение «каждый из этих знаков прожит в пласте
    не реже двух раз», и писать его рукой значит писать список, который
    завтра разойдётся со словарём. Дыра шаблона («{lex:adj_forms:…}»)
    выбрасывается: она написана латиницей служебного языка и в пласт не
    попадает ни разу — этот шрам куплен восточным семенем, где суд
    графем поймал девятнадцать таких мнимых знаков первым же прогоном.
    """
    вон = set()
    for строка in строки:
        for знак in re.sub(r"\{[^}]*\}", "", str(строка)):
            if знак.isalpha():
                вон.add(знак)
    return "".join(sorted(вон))


def _всё(семя):
    """Все строки семени, из которых собирается инвентарь знаков."""
    куски = list(семя["numerals"].values()) + list(семя["ops"])
    куски += семя["persons"]
    for таблица in ("verbs", "nouns", "adjs"):
        for формы in семя.get(таблица, {}).values():
            куски += формы
    сл = семя["words"]
    куски += сл["count_lexicon"] + сл["count_templates"]
    куски += сл["def_lexicon"] + сл["def_templates"]
    куски += семя.get("adj_lexicon", []) + семя.get("adj_templates", [])
    for пара in семя["refusals"]:
        куски += [пара["bad"], пара["good"]]
    return куски


# ======================================================= ФИНСКИЙ (fi)

# ЧИСЛИТЕЛЬНЫЕ ДО СТА БЕЗ ДЫР, И СВЕРХ ТОГО ВСЕ ПРОИЗВЕДЕНИЯ ПОСЕВА.
# Кузня сеет слагаемые от одного до девяти и множители от одного до
# пяти; произведения доходят до сорока пяти и берутся не подряд.
# Пропусти одно — и форж напишет цифру посреди финской речи, чего не
# увидит ни одно поле.
FI_ЧИСЛА = {
    "0": "nolla", "1": "yksi", "2": "kaksi", "3": "kolme", "4": "neljä",
    "5": "viisi", "6": "kuusi", "7": "seitsemän", "8": "kahdeksan",
    "9": "yhdeksän", "10": "kymmenen", "11": "yksitoista",
    "12": "kaksitoista", "13": "kolmetoista", "14": "neljätoista",
    "15": "viisitoista", "16": "kuusitoista", "17": "seitsemäntoista",
    "18": "kahdeksantoista", "19": "yhdeksäntoista",
    "20": "kaksikymmentä", "21": "kaksikymmentäyksi",
    "24": "kaksikymmentäneljä", "25": "kaksikymmentäviisi",
    "27": "kaksikymmentäseitsemän", "28": "kaksikymmentäkahdeksan",
    "30": "kolmekymmentä", "32": "kolmekymmentäkaksi",
    "35": "kolmekymmentäviisi", "36": "kolmekymmentäkuusi",
    "40": "neljäkymmentä", "45": "neljäkymmentäviisi",
    "50": "viisikymmentä", "60": "kuusikymmentä",
    "70": "seitsemänkymmentä", "80": "kahdeksankymmentä",
    "90": "yhdeksänkymmentä", "100": "sata",
}

# ДВЕНАДЦАТЬ ПАДЕЖЕЙ, А НЕ ПЯТНАДЦАТЬ, И ЭТО МОЙ ОТКАЗ, А НЕ ДВИЖКА.
# Финский счёт падежей ведут до пятнадцати; здесь объявлены те
# двенадцать, за формы которых я ручаюсь. Инструктив (taloin) и
# комитатив (taloineen) — множественные по числу, редкие в живой речи и
# требующие притяжательного суффикса; писать их наугад значило бы учить
# неверному как верному. Движку разницы нет: клеток он берёт столько,
# сколько объявлено.
#
# ЧЕРЕДОВАНИЕ СТУПЕНЕЙ ВИДНО ЗДЕСЬ ГЛАЗОМ: у kukka сильная ступень
# стоит в именительном, партитиве, иллативе и эссиве (kukka, kukkaa,
# kukkaan, kukkana), слабая — во всех прочих (kukan, kukassa, kukalla).
# То же у katu/kadun, kauppa/kaupan, pöytä/pöydän.
FI_ПАДЕЖИ = {
    "talo": ["talo", "talon", "taloa", "talossa", "talosta", "taloon",
             "talolla", "talolta", "talolle", "talona", "taloksi",
             "talotta"],
    "auto": ["auto", "auton", "autoa", "autossa", "autosta", "autoon",
             "autolla", "autolta", "autolle", "autona", "autoksi",
             "autotta"],
    "koulu": ["koulu", "koulun", "koulua", "koulussa", "koulusta",
              "kouluun", "koululla", "koululta", "koululle", "kouluna",
              "kouluksi", "koulutta"],
    "kirja": ["kirja", "kirjan", "kirjaa", "kirjassa", "kirjasta",
              "kirjaan", "kirjalla", "kirjalta", "kirjalle", "kirjana",
              "kirjaksi", "kirjatta"],
    "kukka": ["kukka", "kukan", "kukkaa", "kukassa", "kukasta",
              "kukkaan", "kukalla", "kukalta", "kukalle", "kukkana",
              "kukaksi", "kukatta"],
    "katu": ["katu", "kadun", "katua", "kadussa", "kadusta", "katuun",
             "kadulla", "kadulta", "kadulle", "katuna", "kaduksi",
             "kadutta"],
    "kauppa": ["kauppa", "kaupan", "kauppaa", "kaupassa", "kaupasta",
               "kauppaan", "kaupalla", "kaupalta", "kaupalle",
               "kauppana", "kaupaksi", "kaupatta"],
    "pöytä": ["pöytä", "pöydän", "pöytää", "pöydässä", "pöydästä",
              "pöytään", "pöydällä", "pöydältä", "pöydälle", "pöytänä",
              "pöydäksi", "pöydättä"],
}
FI_ПАДЕЖИ_ИМЕНА = ["nominative", "genitive", "partitive", "inessive",
                   "elative", "illative", "adessive", "ablative",
                   "allative", "essive", "translative", "abessive"]

# ЧИСЛО: именительный единственного против именительного множественного.
# Чередование правит и здесь: katu → kadut, kauppa → kaupat.
FI_ЧИСЛО = {ключ: [формы[0], множ] for ключ, формы, множ in (
    ("talo", FI_ПАДЕЖИ["talo"], "talot"),
    ("auto", FI_ПАДЕЖИ["auto"], "autot"),
    ("koulu", FI_ПАДЕЖИ["koulu"], "koulut"),
    ("kirja", FI_ПАДЕЖИ["kirja"], "kirjat"),
    ("kukka", FI_ПАДЕЖИ["kukka"], "kukat"),
    ("katu", FI_ПАДЕЖИ["katu"], "kadut"),
    ("kauppa", FI_ПАДЕЖИ["kauppa"], "kaupat"),
    ("pöytä", FI_ПАДЕЖИ["pöytä"], "pöydät"),
)}

FI_ГЛАГОЛЫ = {
    "puhua": ["puhun", "puhut", "puhuu", "puhumme", "puhutte",
              "puhuvat"],
    "asua": ["asun", "asut", "asuu", "asumme", "asutte", "asuvat"],
    "sanoa": ["sanon", "sanot", "sanoo", "sanomme", "sanotte",
              "sanovat"],
    "katsoa": ["katson", "katsot", "katsoo", "katsomme", "katsotte",
               "katsovat"],
    "ostaa": ["ostan", "ostat", "ostaa", "ostamme", "ostatte",
              "ostavat"],
    "lukea": ["luen", "luet", "lukee", "luemme", "luette", "lukevat"],
    "kirjoittaa": ["kirjoitan", "kirjoitat", "kirjoittaa",
                   "kirjoitamme", "kirjoitatte", "kirjoittavat"],
    "antaa": ["annan", "annat", "antaa", "annamme", "annatte",
              "antavat"],
    "tietää": ["tiedän", "tiedät", "tietää", "tiedämme", "tiedätte",
               "tietävät"],
    "oppia": ["opin", "opit", "oppii", "opimme", "opitte", "oppivat"],
    "syödä": ["syön", "syöt", "syö", "syömme", "syötte", "syövät"],
    "juoda": ["juon", "juot", "juo", "juomme", "juotte", "juovat"],
    "tulla": ["tulen", "tulet", "tulee", "tulemme", "tulette",
              "tulevat"],
    "mennä": ["menen", "menet", "menee", "menemme", "menette",
              "menevät"],
    "nähdä": ["näen", "näet", "näkee", "näemme", "näette", "näkevät"],
    "olla": ["olen", "olet", "on", "olemme", "olette", "ovat"],
}

FI = {
    "lang": "fi",
    "script": "latin",
    "script_range": "A-Za-zÄÖÅäöå",
    "diacritics": "äöå",
    "comment": (
        "TWENTIETH PACK. Finnish: FIFTEEN CASES (twelve declared — the "
        "three I would not guess are left out), all suffixed, none "
        "prepositional; CONSONANT GRADATION (kukka/kukan, katu/kadun, "
        "kauppa/kaupan) which changes the STEM, not the ending — and "
        "which the rule oracle CAN express once the class is keyed on "
        "the alternation and the whole alternating chunk is stripped; "
        "a numeral takes the PARTITIVE SINGULAR, never the plural. The "
        "equality word is the copula «on», the commonest word in the "
        "language, and the arithmetic judge goes half-blind on ordinary "
        "sentences because of it. TIER 1."),
    "numerals": FI_ЧИСЛА,
    # ПОСЛЕ ЧИСЛИТЕЛЬНОГО МНОЖЕСТВЕННОЕ НЕ СТАВИТСЯ НИКОГДА — «kaksi
    # taloa», а не «kaksi talot». Это правда, и она объявлена. Но вся
    # правда сюда не влезает: нужная форма есть ПАРТИТИВ ЕДИНСТВЕННОГО,
    # то есть клетка ДРУГОГО класса, а правило умеет указывать лишь на
    # клетки своего. Счётные показы берут партитив прямо из падежной
    # парадигмы; это поле честно говорит только половину — «не
    # множественное».
    "count_agreement": [{"form": "one"}],
    # «kertaa» берёт именительный и потому годится и взято. ДЕЛЕНИЕ
    # СЛОВОМ НАПИСАТЬ НЕЛЬЗЯ: финское «jaettuna» требует адессива на
    # делителе («kuusi jaettuna kolmella»), а шаблон кузни подаёт
    # голый именительный. Стояло обиходное «per» — и снято замером:
    # ИТАЛЬЯНСКИЙ ПАКЕТ ОБЪЯВЛЯЕТ «per» УМНОЖЕНИЕМ («due per tre»), а
    # суд арифметики строит ОДИН словарь операций на все языки и при
    # расхождении молча берёт последний по имени файла. Числительным
    # он расхождения не прощает и выходит с отказом; операциям —
    # прощает молча. Взят всеобщий знак «÷», объявления не требующий.
    "ops": {"plus": "+", "miinus": "-", "kertaa": "*", "÷": "/",
            "on": "="},
    "w_plus": "plus", "w_minus": "miinus", "w_times": "kertaa",
    "w_div": "÷", "w_eq": "on",
    "persons": ["minä", "sinä", "hän", "me", "te", "he"],
    "verbs": FI_ГЛАГОЛЫ,
    "nouns": FI_ЧИСЛО,
    "adjs": FI_ПАДЕЖИ,
    "adj_cells": FI_ПАДЕЖИ_ИМЕНА,
    "adj_lexicon": ["Tämä", "Minä", "Se", "hyvä"],
    # ЗАМЕЧАНИЕ О СЛОВЕ РАВЕНСТВА, ЗАМЕРЕННОЕ И НЕ ИСПРАВЛЕННОЕ:
    # финское «on» есть связка «есть», и оно же объявлено турецким
    # пакетом ЧИСЛИТЕЛЬНЫМ (on = десять). Разбор суда арифметики
    # пробует значения ПРЕЖДЕ равенств, и потому вся финская
    # словесная арифметика для него НЕВИДИМА — не ложна, а нема.
    # Слово оставлено: «kaksi plus kolme on viisi» есть верный
    # финский, и подменять его ради чужого прибора значило бы
    # подгонять язык под движок.
    # ДВЕНАДЦАТЬ ПОКАЗОВ НА ДВЕНАДЦАТЬ ПАДЕЖЕЙ: клетка, не прожитая
    # показом, объявлена и не показана, а это худший род объявления.
    # Пары «menen taloon» / «menen talolle» и «olen talossa» / «olen
    # talotta» стоят нарочно: падеж виден различием, а не именем.
    "adj_templates": [
        "{lex:adj_forms:nominative} on tässä.",
        "Tämä on {lex:adj_forms:genitive} väri.",
        "Minä katson {lex:adj_forms:partitive}.",
        "Minä olen {lex:adj_forms:inessive}.",
        "Minä tulen {lex:adj_forms:elative}.",
        "Minä menen {lex:adj_forms:illative}.",
        "Se on {lex:adj_forms:adessive}.",
        "Minä otan sen {lex:adj_forms:ablative}.",
        "Minä menen {lex:adj_forms:allative}.",
        "Se on hyvä {lex:adj_forms:essive}.",
        "Se muuttui {lex:adj_forms:translative}.",
        "Minä olen {lex:adj_forms:abessive}.",
    ],
    "words": {
        "count_lexicon": ["Tässä", "yksi", "kaksi"],
        # ПАРТИТИВ БЕРЁТСЯ ИЗ ЧУЖОГО КЛАССА, И БЕРЁТСЯ ВЕРНО: обе
        # парадигмы объявлены на ОДНИХ И ТЕХ ЖЕ восьми именах, и выбор
        # лексемы у кузни зависит только от посева и номера шаблона —
        # стало быть, «{one}» и «{lex:adj_forms:partitive}» в одном
        # показе суть одно и то же имя. Сумма всегда не меньше двух, и
        # потому партитив тут уместен всегда; произведение бывает
        # единицей, и с ним этот шаблон был бы неграмотен.
        "count_templates": ["Tässä on yksi {one}.",
                            "Tässä ovat {many}.",
                            "Tässä on kaksi {lex:adj_forms:partitive}.",
                            "Tässä on {num:sum} "
                            "{lex:adj_forms:partitive}."],
        "def_lexicon": ["suomen", "sana", "sanoja"],
        "def_templates": ["{one} on suomen sana.",
                          "{many} ovat suomen sanoja."],
    },
    "irregulars": ["olen", "olet", "on", "olemme", "ovat"],
    "probe": ["minä", "sinä", "hän", "me", "te", "he", "on", "yksi",
              "kaksi", "plus", "miinus", "kertaa", "per", "talo",
              "kirja", "Tässä", "Tämä", "sana"],
    "refusals": [
        {"bad": "Minä näen kaksi talo.",
         "good": "Minä näen kaksi taloa.", "reason": "agreement"},
        {"bad": "minä puhut suomea.", "good": "minä puhun suomea.",
         "reason": "agreement"},
        {"bad": "hän on kirjastoon.", "good": "hän on kirjastossa.",
         "reason": "agreement"},
        {"bad": "mikä on seitsemän väri?", "good": "mikä on talo?",
         "reason": "unanswerable"},
        # ДВАДЦАТЬ ОДИН ЖИВЁТ ТОЛЬКО ЗДЕСЬ: из посева кузни это число
        # выходит РОВНО ОДИН раз, а закон повтора требует двух. Отказ
        # повторяется каждым проходом, и слово оживает законно —
        # вычитание истинно.
        {"bad": "kirja plus kukka on ?",
         "good": "kaksikymmentäyksi miinus yksi on kaksikymmentä.",
         "reason": "type_mismatch"},
    ],
    # ЧЕРЕДОВАНИЕ СТУПЕНЕЙ, ВЫРАЖЕННОЕ ПРАВИЛОМ. Класс назван не по
    # окончанию, а по ЧЕРЕДУЮЩЕЙСЯ ЧАСТИ, и отсекается она целиком:
    # «lukea» минус «kea» есть «lu», и окончания несут обе ступени —
    # «en» слабую, «kee» сильную. Так же «kirjoittaa» минус «ttaa»,
    # «antaa» минус «ntaa», «tietää» минус «tää», «oppia» минус
    # «ppia», «nähdä» минус «hdä». Правило и таблица суть два
    # независимых высказывания об одном факте, и оракул их сверяет.
    # «olla» стоит под «*»: у неё третье лицо «on» и «ovat» не выводимы
    # ниоткуда — честный отказ правила, а не подгон.
    "verb_rule": {
        "classes": {
            "ua": {"strip": "ua",
                   "endings": ["un", "ut", "uu", "umme", "utte",
                               "uvat"]},
            "oa": {"strip": "oa",
                   "endings": ["on", "ot", "oo", "omme", "otte",
                               "ovat"]},
            "aa": {"strip": "aa",
                   "endings": ["an", "at", "aa", "amme", "atte",
                               "avat"]},
            "kea": {"strip": "kea",
                    "endings": ["en", "et", "kee", "emme", "ette",
                                "kevat"]},
            "ttaa": {"strip": "ttaa",
                     "endings": ["tan", "tat", "ttaa", "tamme",
                                 "tatte", "ttavat"]},
            "ntaa": {"strip": "ntaa",
                     "endings": ["nnan", "nnat", "ntaa", "nnamme",
                                 "nnatte", "ntavat"]},
            "tää": {"strip": "tää",
                    "endings": ["dän", "dät", "tää", "dämme", "dätte",
                                "tävät"]},
            "ppia": {"strip": "ppia",
                     "endings": ["pin", "pit", "ppii", "pimme",
                                 "pitte", "ppivat"]},
            "dä": {"strip": "dä",
                   "endings": ["n", "t", "", "mme", "tte", "vät"]},
            "da": {"strip": "da",
                   "endings": ["n", "t", "", "mme", "tte", "vat"]},
            "lla": {"strip": "lla",
                    "endings": ["len", "let", "lee", "lemme", "lette",
                                "levat"]},
            "nnä": {"strip": "nnä",
                    "endings": ["nen", "net", "nee", "nemme", "nette",
                                "nevät"]},
            "hdä": {"strip": "hdä",
                    "endings": ["en", "et", "kee", "emme", "ette",
                                "kevät"]},
        },
        "of": {"puhua": "ua", "asua": "ua", "sanoa": "oa",
               "katsoa": "oa", "ostaa": "aa", "lukea": "kea",
               "kirjoittaa": "ttaa", "antaa": "ntaa", "tietää": "tää",
               "oppia": "ppia", "syödä": "dä", "juoda": "da",
               "tulla": "lla", "mennä": "nnä", "nähdä": "hdä",
               "olla": "*"},
    },
}
FI["graphemes"] = _знаки(*_всё(FI))


# ==================================================== ВЕНГЕРСКИЙ (hu)

HU_ЧИСЛА = {
    "0": "nulla", "1": "egy", "2": "kettő", "3": "három", "4": "négy",
    "5": "öt", "6": "hat", "7": "hét", "8": "nyolc", "9": "kilenc",
    "10": "tíz", "11": "tizenegy", "12": "tizenkettő",
    "13": "tizenhárom", "14": "tizennégy", "15": "tizenöt",
    "16": "tizenhat", "17": "tizenhét", "18": "tizennyolc",
    "19": "tizenkilenc", "20": "húsz", "21": "huszonegy",
    "24": "huszonnégy", "25": "huszonöt", "27": "huszonhét",
    "28": "huszonnyolc", "30": "harminc", "32": "harminckettő",
    "35": "harmincöt", "36": "harminchat", "40": "negyven",
    "45": "negyvenöt", "50": "ötven", "60": "hatvan", "70": "hetven",
    "80": "nyolcvan", "90": "kilencven", "100": "száz",
}

# НЕОПРЕДЕЛЁННОЕ СПРЯЖЕНИЕ — то, что кузня зовёт лицами.
HU_ГЛАГОЛЫ = {
    "lát": ["látok", "látsz", "lát", "látunk", "láttok", "látnak"],
    "ír": ["írok", "írsz", "ír", "írunk", "írtok", "írnak"],
    "tanul": ["tanulok", "tanulsz", "tanul", "tanulunk", "tanultok",
              "tanulnak"],
    "olvas": ["olvasok", "olvasol", "olvas", "olvasunk", "olvastok",
              "olvasnak"],
    "kér": ["kérek", "kérsz", "kér", "kérünk", "kértek", "kérnek"],
    "néz": ["nézek", "nézel", "néz", "nézünk", "néztek", "néznek"],
    "köszön": ["köszönök", "köszönsz", "köszön", "köszönünk",
               "köszöntök", "köszönnek"],
    "főz": ["főzök", "főzöl", "főz", "főzünk", "főztök", "főznek"],
}

# ОПРЕДЕЛЁННОЕ СПРЯЖЕНИЕ — ТЕ ЖЕ ВОСЕМЬ ГЛАГОЛОВ, ДРУГИЕ ШЕСТЬ КЛЕТОК.
# Лексемы намеренно те же и в том же числе: кузня выбирает лексему по
# посеву и номеру шаблона, и при одинаковых списках оба класса
# выбирают ОДНУ И ТУ ЖЕ — оттого «látok valamit, és látom azt» стоит в
# одном показе про один глагол, а не про два разных.
HU_ОПРЕДЕЛЁННОЕ = {
    "lát": ["látom", "látod", "látja", "látjuk", "látjátok", "látják"],
    "ír": ["írom", "írod", "írja", "írjuk", "írjátok", "írják"],
    "tanul": ["tanulom", "tanulod", "tanulja", "tanuljuk",
              "tanuljátok", "tanulják"],
    "olvas": ["olvasom", "olvasod", "olvassa", "olvassuk",
              "olvassátok", "olvassák"],
    "kér": ["kérem", "kéred", "kéri", "kérjük", "kéritek", "kérik"],
    "néz": ["nézem", "nézed", "nézi", "nézzük", "nézitek", "nézik"],
    "köszön": ["köszönöm", "köszönöd", "köszöni", "köszönjük",
               "köszönitek", "köszönik"],
    "főz": ["főzöm", "főzöd", "főzi", "főzzük", "főzitek", "főzik"],
}

# ГАРМОНИЯ ГЛАСНЫХ ВИДНА В МНОЖЕСТВЕННОМ: задний ряд берёт -ok, передний
# неогублённый -ek, передний огублённый -ök. Три набора, а не турецкие
# четыре, и делятся они по ИНОМУ признаку — по огублённости, а не по
# ряду одному.
HU_ИМЕНА = {
    "ház": ["ház", "házak"], "ablak": ["ablak", "ablakok"],
    "asztal": ["asztal", "asztalok"], "virág": ["virág", "virágok"],
    "város": ["város", "városok"], "kert": ["kert", "kertek"],
    "könyv": ["könyv", "könyvek"], "gyerek": ["gyerek", "gyerekek"],
    "szék": ["szék", "székek"], "kép": ["kép", "képek"],
    "kutya": ["kutya", "kutyák"], "alma": ["alma", "almák"],
}

HU = {
    "lang": "hu",
    "script": "latin",
    "script_range": "A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű",
    "diacritics": "áéíóöőúüű",
    "comment": (
        "TWENTY-FIRST PACK. Hungarian: DEFINITE AND INDEFINITE "
        "CONJUGATION — the verb inflects for the DEFINITENESS OF ITS "
        "OBJECT (látok valamit / látom azt), a category no other pack "
        "carries and no field holds: the present tense has TWELVE "
        "cells and the engine's cell names stop at six, so the second "
        "conjugation rides in the adjective slot with honestly named "
        "cells; THREE-WAY VOWEL HARMONY (-ok / -ek / -ök) split by "
        "roundedness, shown as six rule classes with a sibilant "
        "sub-rule (olvasol, főzöl); POSSESSIVE SUFFIXES instead of "
        "pronouns (házam = my house) with no fourth class slot to hold "
        "their paradigm, so they are shown as constants only. "
        "Multiplication governs the instrumental and could not be "
        "written. TIER 1."),
    "numerals": HU_ЧИСЛА,
    # ПОСЛЕ ЧИСЛИТЕЛЬНОГО ИМЯ ОСТАЁТСЯ В ЕДИНСТВЕННОМ: «két ház», а не
    # «két házak». Здесь поле говорит ВСЮ правду — в отличие от
    # финского, где нужная форма лежит в чужом классе.
    "count_agreement": [{"form": "one"}],
    # «meg», «mínusz» и «egyenlő» берут именительный и потому годятся.
    # УМНОЖЕНИЕ И ДЕЛЕНИЕ СЛОВОМ НАПИСАТЬ НЕЛЬЗЯ: венгерское «kettő
    # szorozva hárommal» и «hat osztva kettővel» требуют ИНСТРУМЕНТАЛЯ
    # на втором числе, а шаблон кузни подаёт голый именительный. Стояло
    # «per» (обиходное венгерское деление) — и снято замером: суд
    # арифметики корпуса объявил СЕМЬДЕСЯТ ЧЕТЫРЕ истинных венгерских
    # деления ЛОЖЬЮ, ибо итальянский пакет объявил то же «per»
    # УМНОЖЕНИЕМ, а словарь операций у суда один на все языки и
    # расхождение он глотает молча. Взяты всеобщие знаки «×» и «÷»:
    # венгерская запись их знает, а объявления они не требуют.
    "ops": {"meg": "+", "mínusz": "-", "×": "*", "÷": "/",
            "egyenlő": "="},
    "w_plus": "meg", "w_minus": "mínusz", "w_times": "×",
    "w_div": "÷", "w_eq": "egyenlő",
    "persons": ["én", "te", "ő", "mi", "ti", "ők"],
    "verbs": HU_ГЛАГОЛЫ,
    "nouns": HU_ИМЕНА,
    "adjs": HU_ОПРЕДЕЛЁННОЕ,
    # КЛЕТКИ НАЗВАНЫ ПО СУЩЕСТВУ, ХОТЯ КЛАСС КУЗНЯ ЗОВЁТ «adj_forms»:
    # третьего имени класса у неё нет, и второе спряжение едет в слоте
    # прилагательного. Имя класса лжёт, имена клеток — нет.
    "adj_cells": ["def_s1", "def_s2", "def_s3", "def_p1", "def_p2",
                  "def_p3"],
    "adj_lexicon": ["valamit", "azt", "és"],
    # ОБА СПРЯЖЕНИЯ В ОДНОМ ПОКАЗЕ И НА ОДНОМ ГЛАГОЛЕ: различие видно
    # различием, а не объявлением. «valamit» (нечто) требует
    # неопределённого, «azt» (то) — определённого, и переставить их
    # нельзя.
    "adj_templates": [
        "{lex:verb_pres:s1} valamit, és {lex:adj_forms:def_s1} azt.",
        "{lex:verb_pres:s2} valamit, és {lex:adj_forms:def_s2} azt.",
        "{lex:verb_pres:s3} valamit, és {lex:adj_forms:def_s3} azt.",
        "{lex:verb_pres:p1} valamit, és {lex:adj_forms:def_p1} azt.",
        "{lex:verb_pres:p2} valamit, és {lex:adj_forms:def_p2} azt.",
        "{lex:verb_pres:p3} valamit, és {lex:adj_forms:def_p3} azt.",
    ],
    "words": {
        "count_lexicon": ["Itt", "Ott", "van"],
        "count_templates": ["Itt van egy {one}.",
                            "Itt vannak a {many}.",
                            "Ott van egy {one}."],
        "def_lexicon": ["Ez", "Az", "egy"],
        # ПРИТЯЖАТЕЛЬНЫЙ СУФФИКС ПОКАЗАН ПОСТОЯННЫМИ, А НЕ ПАРАДИГМОЙ,
        # И ЭТО ГРАНИЦА ДВИЖКА, А НЕ ВЫБОР. Классов у кузни ровно три,
        # и все три заняты: неопределённое спряжение, число имени,
        # определённое спряжение. Четвёртому — притяжательному —
        # места нет, и он живёт шестью постоянными показами: суффикс
        # виден (házam, kertem, könyvem, székem, ablakom, almám, и
        # гармония в нём та же тройная), но по именам не ходит.
        "def_templates": ["Ez egy {one}.", "Az egy {one}.",
                          "Ez a házam.", "Ez a kertem.",
                          "Ez a könyvem.", "Ez a székem.",
                          "Ez az ablakom.", "Ez az almám."],
    },
    "irregulars": ["házam", "kertem", "könyvem", "székem", "almám"],
    "probe": ["én", "te", "ő", "mi", "ti", "ők", "Ez", "Az", "egy",
              "Itt", "van", "meg", "mínusz", "per", "egyenlő", "ház",
              "könyv", "valamit", "azt"],
    "refusals": [
        # ОПРЕДЕЛЁННОСТЬ ДОПОЛНЕНИЯ — ровно та пара, ради которой язык
        # и взят: половины различаются ОДНИМ окончанием глагола.
        {"bad": "én látom valamit.", "good": "én látok valamit.",
         "reason": "agreement"},
        {"bad": "én látok azt.", "good": "én látom azt.",
         "reason": "agreement"},
        {"bad": "két házak vannak itt.", "good": "két ház van itt.",
         "reason": "agreement"},
        {"bad": "a házek szépek.", "good": "a házak szépek.",
         "reason": "agreement"},
        {"bad": "mi a hét színe?", "good": "mi ez?",
         "reason": "unanswerable"},
        {"bad": "könyv meg kutya egyenlő?",
         "good": "huszonegy mínusz egy egyenlő húsz.",
         "reason": "type_mismatch"},
    ],
    # ГАРМОНИЯ ГЛАСНЫХ ТРЕМЯ РЯДАМИ, И ЧЕТВЁРТЫЙ ПРИЗНАК СВЕРХ НЕЁ.
    # Задний ряд берёт -ok/-unk/-tok, передний неогублённый
    # -ek/-ünk/-tek, передний огублённый -ök/-ünk/-tök. Сверх ряда
    # правит СВИСТЯЩАЯ ОСНОВА: после s, sz, z второе лицо берёт -ol/
    # -el/-öl вместо -sz (olvasol, nézel, főzöl), и это отдельный
    # признак, а не гармония. Шесть классов — три ряда на два вида
    # основы.
    "verb_rule": {
        "classes": {
            "back": {"strip": "",
                     "endings": ["ok", "sz", "", "unk", "tok", "nak"]},
            "back-sibilant": {
                "strip": "",
                "endings": ["ok", "ol", "", "unk", "tok", "nak"]},
            "front": {"strip": "",
                      "endings": ["ek", "sz", "", "ünk", "tek",
                                  "nek"]},
            "front-sibilant": {
                "strip": "",
                "endings": ["ek", "el", "", "ünk", "tek", "nek"]},
            "front-round": {
                "strip": "",
                "endings": ["ök", "sz", "", "ünk", "tök", "nek"]},
            "front-round-sibilant": {
                "strip": "",
                "endings": ["ök", "öl", "", "ünk", "tök", "nek"]},
        },
        "of": {"lát": "back", "ír": "back", "tanul": "back",
               "olvas": "back-sibilant", "kér": "front",
               "néz": "front-sibilant", "köszön": "front-round",
               "főz": "front-round-sibilant"},
    },
}
HU["graphemes"] = _знаки(*_всё(HU))
