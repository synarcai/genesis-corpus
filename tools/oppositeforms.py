#!/usr/bin/env python3
"""ДОМ ПРОТИВОПОЛОЖНОСТЕЙ — отношение, которого во всём своде не было ни одного.

Собеседник знает не только что вещь ЕСТЬ (дом определений) и сколько её (дом
природы), но и чему она ПРОТИВОПОЛОЖНА. Это первое в корпусе отношение
СЛОВА К СЛОВУ, а не слова к вещи, и потому оно ставится особо.

ЗАКОН, КОТОРЫМ ЭТО СУДИТСЯ, — СИММЕТРИЯ. Противоположность есть отношение
взаимное: если большой противоположен маленькому, то маленький противоположен
большому, и обе стороны стоят в показах ОБЕ. Дом проверяет себя этим же
законом: пара, объявленная в одну сторону, обязана дать показ в обе, и суд
ловит подмену второй стороны так же, как подмену первой.

ФОРМА ЦИТАТНАЯ, И ЭТО РЕШЕНИЕ, А НЕ УДОБСТВО. «Что противоположно БОЛЬШОМУ?»
требует дательного падежа, «противоположность большого» — родительного, и
всякий язык потребовал бы двух-трёх форм на слово. Цитатная рамка («что
противоположно слову большой?») берёт слово в словарной форме, и дом обходится
ОДНОЙ формой на слово в каждом языке — то есть объявляет ровно то, что знает,
и не выдумывает падежей, которых не проверял.

    python3 tools/oppositeforms.py    # самопроверка с мутантами
"""

# пары объявлены в словарной форме каждого языка
ПАРЫ = {
    "ru": (("большой", "маленький"), ("длинный", "короткий"), ("высокий", "низкий"),
           ("тёплый", "холодный"), ("быстрый", "медленный"), ("светлый", "тёмный"),
           ("новый", "старый"), ("полный", "пустой"), ("лёгкий", "тяжёлый"),
           ("сухой", "мокрый"), ("громкий", "тихий"), ("сильный", "слабый")),
    "en": (("big", "small"), ("long", "short"), ("high", "low"),
           ("warm", "cold"), ("fast", "slow"), ("light", "dark"),
           ("new", "old"), ("full", "empty"), ("easy", "hard"),
           ("dry", "wet"), ("loud", "quiet"), ("strong", "weak")),
    "de": (("groß", "klein"), ("lang", "kurz"), ("hoch", "niedrig"),
           ("warm", "kalt"), ("schnell", "langsam"), ("hell", "dunkel"),
           ("neu", "alt"), ("voll", "leer"), ("leicht", "schwer"),
           ("trocken", "nass"), ("laut", "leise"), ("stark", "schwach")),
    "fr": (("grand", "petit"), ("long", "court"), ("haut", "bas"),
           ("chaud", "froid"), ("rapide", "lent"), ("clair", "sombre"),
           ("neuf", "vieux"), ("plein", "vide"), ("facile", "difficile"),
           ("sec", "mouillé"), ("fort", "faible"), ("propre", "sale")),
    "es": (("grande", "pequeño"), ("largo", "corto"), ("alto", "bajo"),
           ("caliente", "frío"), ("rápido", "lento"), ("claro", "oscuro"),
           ("nuevo", "viejo"), ("lleno", "vacío"), ("fácil", "difícil"),
           ("seco", "mojado"), ("fuerte", "débil"), ("limpio", "sucio")),
    "it": (("grande", "piccolo"), ("lungo", "corto"), ("alto", "basso"),
           ("caldo", "freddo"), ("veloce", "lento"), ("chiaro", "scuro"),
           ("nuovo", "vecchio"), ("pieno", "vuoto"), ("facile", "difficile"),
           ("asciutto", "bagnato"), ("forte", "debole"), ("pulito", "sporco")),
    "pt": (("grande", "pequeno"), ("longo", "curto"), ("alto", "baixo"),
           ("quente", "frio"), ("rápido", "lento"), ("claro", "escuro"),
           ("novo", "velho"), ("cheio", "vazio"), ("fácil", "difícil"),
           ("seco", "molhado"), ("forte", "fraco"), ("limpo", "sujo")),
    "nl": (("groot", "klein"), ("lang", "kort"), ("hoog", "laag"),
           ("warm", "koud"), ("snel", "langzaam"), ("licht", "donker"),
           ("nieuw", "oud"), ("vol", "leeg"), ("makkelijk", "moeilijk"),
           ("droog", "nat"), ("luid", "stil"), ("sterk", "zwak")),
    "pl": (("duży", "mały"), ("długi", "krótki"), ("wysoki", "niski"),
           ("ciepły", "zimny"), ("szybki", "wolny"), ("jasny", "ciemny"),
           ("nowy", "stary"), ("pełny", "pusty"), ("łatwy", "trudny"),
           ("suchy", "mokry"), ("głośny", "cichy"), ("silny", "słaby")),
}
РАМКИ = {
    "ru": ("{a} и {b} — противоположности.", "что противоположно слову {a}? {b}."),
    "en": ("{a} and {b} are opposites.", "what is the opposite of {a}? {b}."),
    "de": ("{a} und {b} sind Gegensätze.", "was ist das Gegenteil von {a}? {b}."),
    "fr": ("{a} et {b} sont des contraires.", "quel est le contraire de {a} ? {b}."),
    "es": ("{a} y {b} son contrarios.", "¿cuál es el contrario de {a}? {b}."),
    "it": ("{a} e {b} sono contrari.", "qual è il contrario di {a}? {b}."),
    "pt": ("{a} e {b} são contrários.", "qual é o contrário de {a}? {b}."),
    "nl": ("{a} en {b} zijn tegenstellingen.", "wat is het tegenovergestelde van {a}? {b}."),
    "pl": ("{a} i {b} to przeciwieństwa.", "jakie jest przeciwieństwo słowa {a}? {b}."),
}
ЯЗЫКИ = ПАРЫ
ФОРМЫ = ("утв", "утв_воп", "воп", "воп_обратно")

for _яз, _пары in ПАРЫ.items():
    assert _яз in РАМКИ, _яз
    assert len(_пары) == len(ПАРЫ["ru"]), (_яз, len(_пары))
    _слова = [с for п in _пары for с in п]
    assert len(_слова) == len(set(_слова)), (_яз, "слово стоит в двух парах")


def показ(язык, форма, i):
    утв, воп = РАМКИ[язык]
    a, b = ПАРЫ[язык][i % len(ПАРЫ[язык])]
    if форма == "утв":
        return утв.format(a=a, b=b)
    if форма == "утв_воп":
        # УТВЕРЖДЕНИЕ И ЕГО ВОПРОС ОДНОЙ СТРАНИЦЕЙ — тот же ход, каким дом
        # счётных единиц связал парадигму с вопросом о ней: род, чей факт
        # спрошен рядом, не нем, и мера широты вопроса читает его вопросным.
        return f"{утв.format(a=a, b=b)} {воп.format(a=a, b=b)}"
    if форма == "воп":
        return воп.format(a=a, b=b)
    # СИММЕТРИЯ СПРОШЕНА ОБЕИМИ СТОРОНАМИ: отношение взаимно, и корпус,
    # показавший одну сторону, учил бы половине закона.
    return воп.format(a=b, b=a)


def _все_показы():
    вон = {}
    for язык in ПАРЫ:
        for форма in ФОРМЫ:
            for i in range(len(ПАРЫ[язык])):
                вон[показ(язык, форма, i)] = (язык, форма)
    return вон


ПОКАЗЫ = _все_показы()
# РАМКА С ЧУЖИМ СЛОВОМ — ЛОЖЬ, А НЕ МОЛЧАНИЕ: рамка объявлена домом, и пара в
# ней объявлена тоже; строка той же рамки с иной парой отрицает объявленное.
_НАЧАЛА = tuple((язык, воп.split("{a}")[0]) for язык, (_, воп) in РАМКИ.items())


def судить(строка):
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for язык, начало in _НАЧАЛА:
        if начало and с.startswith(начало):
            слова = {w for п in ПАРЫ[язык] for w in п}
            хвост = с[len(начало):]
            if any(хвост.startswith(w) for w in слова):
                return True, False
    return False, False


def _самопроверка():
    мутанты = 0
    for язык in ПАРЫ:
        for форма in ФОРМЫ:
            с = показ(язык, форма, 0)
            assert судить(с) == (True, True), (язык, форма, с)
        # МУТАНТ: пара, сцепленная накрест («что противоположно большому? короткий»)
        _, воп = РАМКИ[язык]
        a = ПАРЫ[язык][0][0]
        чужой = ПАРЫ[язык][1][1]
        битая = воп.format(a=a, b=чужой)
        assert судить(битая) == (True, False), (язык, битая)
        мутанты += 1
    for язык in ("ru", "en", "de", "pl"):
        print("  ", показ(язык, "воп", 0), "|", показ(язык, "воп_обратно", 0))
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ПАРЫ)}, пар {len(ПАРЫ['ru'])}, форм {len(ФОРМЫ)})")


if __name__ == "__main__":
    _самопроверка()
