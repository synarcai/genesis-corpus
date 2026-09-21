#!/usr/bin/env python3
"""СВОЙСТВО, ИЗМЕРЕННОЕ ЧИСЛОМ — «вода глубиной три метра», а не «что глубже».

    СВОД УМЕЛ СРАВНИТЬ СВОЙСТВО И НЕ УМЕЛ ЕГО ИЗМЕРИТЬ. Дом сравнения (`propcompare`, 360
    показов, девять языков) спрашивает «что тяжелее: камень или перо?» — ответ есть ИМЯ, не
    число. Дом перевода единиц (`unitforms`) считает «2 часа суть 120 минут» — число без
    ПРЕДМЕТА, которому оно свойство. Между ними лежал пробел.

ЗАМЕР 21.09 ПО 471 605 СТРОКАМ: форма «X есть N единиц ГЛУБИНОЙ/ДЛИНОЙ/ВЫСОТОЙ» — 86 строк,
и все восемьдесят шесть АНГЛИЙСКИЕ, и все об одном предмете (глубина воды в баке, дом
`gsmforms`). Восемь языков из девяти не имели её ни разу.

    СВОЙСТВО, НАЗВАННОЕ ЧИСЛОМ, ЕСТЬ ТРЕТЬЯ ВЕЩЬ, А НЕ СУММА ДВУХ ПЕРВЫХ: из умения
    сравнить («что глубже») и умения перевести единицы («2 м = 200 см») не следует умение
    ответить «какова глубина» — там спрашивается ИМЯ, тут ЧИСЛО, и число это есть мера
    свойства, а не счёт предметов.

ЕДИНИЦЫ ДЛИНЫ СВОДА РАЗБРОСАНЫ ПО ДВУМ ДОМАМ, И ЭТО НАЗВАННЫЙ ДОЛГ. `actionmeasure`
объявляет их для `ru` и `en`; `unitforms` — для `de`, `fr`, `es`, `it`, `pt`, `nl`, `pl`.
Ни один не покрывает девяти, и дом, которому нужны все, обязан спрашивать ОБОИХ.

    ОДНО ПОНЯТИЕ, ОБЪЯВЛЕННОЕ В ДВУХ ДОМАХ ПОРОЗНЬ, РАЗОЙДЁТСЯ В ТОТ ДЕНЬ, КОГДА ОДИН ИЗ
    НИХ ПОПОЛНЯТ. Здесь оно сведено переходником, и переходник назван — чтобы тот, кто
    станет сводить дома, знал, где искать читателей.

    python3 tools/propmeasure.py    # самопроверка с мутантами
"""
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import actionmeasure as AM   # noqa: E402 — единицы длины ru, en
import unitforms as UF       # noqa: E402 — единицы длины de, fr, es, it, pt, nl, pl

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
РОДЫ = ("мера", "разность")

# РЕЧЬ ДОМА. {n} число, {Е} единица в счётной форме своего числа.
РЕЧЬ = {
    "ru": dict(мера="глубина воды — {n} {Еn}. какова глубина воды? {n} {Еn}.",
               разность="глубина реки — {a} {Еa}, глубина озера — {b} {Еb}. "
                        "на сколько озеро глубже? {r} {Еr}: {b} − {a} = {r}."),
    "en": dict(мера="the water is {n} {Еn} deep. how deep is the water? {n} {Еn}.",
               разность="the river is {a} {Еa} deep, the lake is {b} {Еb} deep. "
                        "how much deeper is the lake? {r} {Еr}: {b} − {a} = {r}."),
    "de": dict(мера="das Wasser ist {n} {Еn} tief. wie tief ist das Wasser? {n} {Еn}.",
               разность="der Fluss ist {a} {Еa} tief, der See ist {b} {Еb} tief. "
                        "wie viel tiefer ist der See? {r} {Еr}: {b} − {a} = {r}."),
    "fr": dict(мера="l'eau a {n} {Еn} de profondeur. "
                    "quelle est la profondeur de l'eau ? {n} {Еn}.",
               разность="la rivière a {a} {Еa} de profondeur, le lac a {b} {Еb} de "
                        "profondeur. de combien le lac est-il plus profond ? "
                        "{r} {Еr} : {b} − {a} = {r}."),
    "es": dict(мера="el agua tiene {n} {Еn} de profundidad. "
                    "¿qué profundidad tiene el agua? {n} {Еn}.",
               разность="el río tiene {a} {Еa} de profundidad, el lago tiene {b} {Еb} de "
                        "profundidad. ¿cuánto más profundo es el lago? "
                        "{r} {Еr}: {b} − {a} = {r}."),
    "it": dict(мера="l'acqua è profonda {n} {Еn}. quanto è profonda l'acqua? {n} {Еn}.",
               разность="il fiume è profondo {a} {Еa}, il lago è profondo {b} {Еb}. "
                        "quanto è più profondo il lago? {r} {Еr}: {b} − {a} = {r}."),
    "pt": dict(мера="a água tem {n} {Еn} de profundidade. "
                    "qual é a profundidade da água? {n} {Еn}.",
               разность="o rio tem {a} {Еa} de profundidade, o lago tem {b} {Еb} de "
                        "profundidade. quanto mais fundo é o lago? "
                        "{r} {Еr}: {b} − {a} = {r}."),
    "nl": dict(мера="het water is {n} {Еn} diep. hoe diep is het water? {n} {Еn}.",
               разность="de rivier is {a} {Еa} diep, het meer is {b} {Еb} diep. "
                        "hoeveel dieper is het meer? {r} {Еr}: {b} − {a} = {r}."),
    "pl": dict(мера="woda ma {n} {Еn} głębokości. jaka jest głębokość wody? {n} {Еn}.",
               разность="rzeka ma {a} {Еa} głębokości, jezioro ma {b} {Еb} głębokości. "
                        "o ile jezioro jest głębsze? {r} {Еr}: {b} − {a} = {r}."),
}

ЧИСЛА = (2, 3, 4, 5, 6, 7, 8, 9, 12, 15)


def единица(язык, n):
    """Метр в счётной форме числа — ПЕРЕХОДНИК К ДВУМ ДОМАМ, где объявлены единицы длины.

    ДОМ, КОТОРОМУ НУЖНЫ ВСЕ ДЕВЯТЬ ЯЗЫКОВ, СПРАШИВАЕТ ОБОИХ ОБЪЯВИТЕЛЕЙ, а не выбирает
    одного и молчит о прочих: `actionmeasure` знает `ru` и `en`, `unitforms` — остальные
    семь. Переходник объявлен здесь, чтобы у разлада двух объявлений был хотя бы один
    названный читатель.
    """
    if язык in AM.ЕДИНИЦЫ:
        return AM.счётная(AM.ЕДИНИЦЫ[язык]["длина"][1], n)
    return UF.форма(язык, "metre", n)


def страница(язык, род, i):
    р = РЕЧЬ[язык]
    if род == "мера":
        n = ЧИСЛА[i % len(ЧИСЛА)]
        return р["мера"].format(n=n, Еn=единица(язык, n))
    a = ЧИСЛА[i % len(ЧИСЛА)]
    b = ЧИСЛА[(i + 3) % len(ЧИСЛА)]
    if b <= a:
        return None                 # ОЗЕРО ОБЯЗАНО БЫТЬ ГЛУБЖЕ: иначе вопрос лжив
    r = b - a
    return р["разность"].format(a=a, Еa=единица(язык, a), b=b, Еb=единица(язык, b),
                                r=r, Еr=единица(язык, r))


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for род in РОДЫ:
            for i in range(len(ЧИСЛА)):
                с = страница(язык, род, i)
                if с:
                    вон[с] = (язык, род)
    return вон


ПОКАЗЫ = _показы()

ЛЕДЖЕР = re.compile(r"(\d+)\s*−\s*(\d+)\s*=\s*(\d+)\.")
ЧИСЛО_ЕДИНИЦА = re.compile(r"(\d+)\s+(\S+?)(?=[\s.,:?!]|$)")


def судить(строка):
    """(судимо, истинно): единица при всяком числе — в счётной форме ЭТОГО числа, а
    разность пересчитывается.

    ЗАКОН ДОМА В ДВУХ ЧАСТЯХ, И ОБЕ ПРОВЕРЯЕМЫ БЕЗ НАБОРА:
      · всякое число страницы несёт при себе единицу, и единица та — счётная форма ЭТОГО
        числа: «3 метра», но «5 метров» и «1 метр»; «3 metry», но «5 metrów»;
      · страница с леджером пересчитывается: разность есть разность, и ответ её носит.
    """
    с = строка.strip()
    судимо = False
    for язык in ЯЗЫКИ:
        свои = {единица(язык, x) for x in (1, 2, 5, 12)}
        пары = ЧИСЛО_ЕДИНИЦА.findall(с)
        если = [(int(ч), е) for ч, е in пары if е in свои]
        if not если:
            continue
        судимо = True
        ладно = all(е == единица(язык, ч) for ч, е in если)
        м = ЛЕДЖЕР.search(с)
        if м:
            a, b, r = int(м.group(1)), int(м.group(2)), int(м.group(3))
            ладно = ладно and a - b == r and r > 0
        if ладно:
            return True, True
    return (True, False) if судимо else (False, False)


def _подсадки():
    """Представленное «НЕТ»: единица не той счётной формы; разность не сходится."""
    вон = []
    for язык in ЯЗЫКИ:
        for род in РОДЫ:
            с = next((п for п, (я, ф) in ПОКАЗЫ.items() if я == язык and ф == род), None)
            if not с:
                continue
            одна, много = единица(язык, 1), единица(язык, 5)
            if одна != много and много in с:
                вон.append(с.replace(много, одна, 1))
            if род == "разность":
                вон.append(ЛЕДЖЕР.sub(
                    lambda м: f"{м.group(1)} − {м.group(2)} = {int(м.group(3)) + 1}.",
                    с, count=1))
    return tuple(вон)


ПОДСАДКИ = _подсадки()


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    пойманы = sum(1 for с in ПОДСАДКИ if судить(с)[:2] == (True, False))
    for язык in ("ru", "en", "pl"):
        for род in РОДЫ:
            с = next((п for п, (я, ф) in ПОКАЗЫ.items() if я == язык and ф == род), None)
            if с:
                print(f"  {язык}/{род}: {с}")
    print(f"  подсадок поймано: {пойманы} из {len(ПОДСАДКИ)}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, родов {len(РОДЫ)}); "
          f"единицы длины взяты у ДВУХ домов — `actionmeasure` (ru, en) и `unitforms` "
          f"(прочие семь), и это названный долг свода")
    assert пойманы == len(ПОДСАДКИ), f"поймано {пойманы} из {len(ПОДСАДКИ)}"


if __name__ == "__main__":
    _самопроверка()
