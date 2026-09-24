#!/usr/bin/env python3
"""[РОСТ] — рост лиц, сравнённый с опорой: ответ пересчитывается из опоры и разности (24.09).

Мир `height` пишет на четырёх языках опору, сравнение, вопрос и ответ со звеном: «Ben is 120 cm tall. Carla
is 8 cm taller than Ben. how tall is Carla? Carla is 128 cm tall: 120 + 8 = 128.» Суд — вторая рука: лица и
русский родительный он берёт у пакетов, а не у дома, и считает сам.

    СЛОВО СРАВНЕНИЯ И ЗНАК ЗВЕНА — ОДНО УТВЕРЖДЕНИЕ, СКАЗАННОЕ ДВАЖДЫ: СУД СВЕРЯЕТ ИХ, А НЕ ВЕРИТ ОБОИМ.

Образец на язык и род, слово сравнения — группа из обоих слов языка («taller|shorter», «выше|ниже»,
«größer|kleiner», «langer|kleiner»): перевёрнутое направление («8 cm shorter … 120 + 8 = 128») — ложь, а не
немота; опора после «than» — то же лицо, что названо первым; спрошенное лицо — то же в вопросе и ответе;
звено повторяет числа фактов.

ГРАНИЦА: строка чужого мира этих образцов суду не подсудна; мир `height` замкнут.

    python3 courts/height_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import json
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402,F401 — палата подаёт имя мира лишь тому, кто ввёз Слой

ИМЯ_СУДА = "height"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"height"})
# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

_ПАКЕТЫ = {я: json.loads((КОРЕНЬ / "tools" / "langpacks" / f"{я}.json").read_text(encoding="utf-8"))
           for я in ("en", "ru", "de", "nl")}
РОДИТЕЛЬНЫЙ = {и: ф["gen"] for и, ф in _ПАКЕТЫ["ru"]["person_forms"].items() if ф.get("gen")}
# (слово «выше», слово «ниже») языка — вторая рука
СЛОВА = {"en": ("taller", "shorter"), "ru": ("выше", "ниже"), "de": ("größer", "kleiner"),
         "nl": ("langer", "kleiner")}


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted(set(слова), key=lambda с: (-len(с), с))) + ")"


def _образцы(язык):
    И = _альт(_ПАКЕТЫ[язык]["person_names"])
    Г = _альт(РОДИТЕЛЬНЫЙ.values())
    С = _альт(СЛОВА[язык])
    ч = r"\d+"
    звено_дано = rf"(?P<vp2>{ч}) (?P<op>[+−]) (?P<r2>{ч}) = (?P<vq2>{ч})\.$"
    звено_разн = rf"(?P<va2>{ч}) (?P<op>[+−]) (?P<vb2>{ч}) = (?P<r2>{ч})\.$"
    if язык == "en":
        дано = (rf"^(?P<p>{И}) is (?P<vp>{ч}) cm tall\. (?P<q>{И}) is (?P<r>{ч}) cm (?P<cmp>{С}) than (?P<p2>{И})\. "
                rf"how tall is (?P<q2>{И})\? (?P<q3>{И}) is (?P<vq>{ч}) cm tall: ")
        разн = (rf"^(?P<a>{И}) is (?P<va>{ч}) cm tall and (?P<b>{И}) is (?P<vb>{ч}) cm tall\. how much (?P<cmp>{С}) "
                rf"is (?P<a2>{И}) than (?P<b2>{И})\? (?P<r>{ч}) cm (?P<cmp2>{С}): ")
    elif язык == "ru":
        дано = (rf"^(?P<p>{И}) ростом (?P<vp>{ч}) см\. (?P<q>{И}) (?P<cmp>{С}) (?P<pg>{Г}) на (?P<r>{ч}) см\. "
                rf"какого роста (?P<q2>{И})\? (?P<q3>{И}) ростом (?P<vq>{ч}) см: ")
        разн = (rf"^(?P<a>{И}) ростом (?P<va>{ч}) см, а (?P<b>{И}) ростом (?P<vb>{ч}) см\. на сколько (?P<a2>{И}) "
                rf"(?P<cmp>{С}) (?P<bg>{Г})\? на (?P<r>{ч}) см: ")
    elif язык == "de":
        дано = (rf"^(?P<p>{И}) ist (?P<vp>{ч}) cm groß\. (?P<q>{И}) ist (?P<r>{ч}) cm (?P<cmp>{С}) als (?P<p2>{И})\. "
                rf"wie groß ist (?P<q2>{И})\? (?P<q3>{И}) ist (?P<vq>{ч}) cm groß: ")
        разн = (rf"^(?P<a>{И}) ist (?P<va>{ч}) cm groß und (?P<b>{И}) ist (?P<vb>{ч}) cm groß\. wie viel "
                rf"(?P<cmp>{С}) ist (?P<a2>{И}) als (?P<b2>{И})\? (?P<r>{ч}) cm (?P<cmp2>{С}): ")
    else:
        дано = (rf"^(?P<p>{И}) is (?P<vp>{ч}) cm lang\. (?P<q>{И}) is (?P<r>{ч}) cm (?P<cmp>{С}) dan (?P<p2>{И})\. "
                rf"hoe lang is (?P<q2>{И})\? (?P<q3>{И}) is (?P<vq>{ч}) cm lang: ")
        разн = (rf"^(?P<a>{И}) is (?P<va>{ч}) cm lang en (?P<b>{И}) is (?P<vb>{ч}) cm lang\. hoeveel (?P<cmp>{С}) "
                rf"is (?P<a2>{И}) dan (?P<b2>{И})\? (?P<r>{ч}) cm (?P<cmp2>{С}): ")
    return re.compile(дано + звено_дано), re.compile(разн + звено_разн)


ОБРАЗЦЫ = {я: _образцы(я) for я in СЛОВА}


def _дано_верно(язык, г):
    """Опора p и спрошенный q — разные лица, названные одинаково в каждом месте; «выше» — q = p + r со
    знаком «+», «ниже» — q = p − r со знаком «−»; звено повторяет числа фактов."""
    вверх, вниз = СЛОВА[язык]
    опора_после = г.get("p2") or next((и for и, род in РОДИТЕЛЬНЫЙ.items() if род == г.get("pg")), None)
    if г["p"] != опора_после or not г["q"] == г["q2"] == г["q3"] or г["p"] == г["q"]:
        return False
    vp, r, vq, vp2, r2, vq2 = (int(г[к]) for к in ("vp", "r", "vq", "vp2", "r2", "vq2"))
    if (vp2, r2, vq2) != (vp, r, vq) or r < 1 or vq < 1:
        return False
    if г["cmp"] == вверх:
        return г["op"] == "+" and vq == vp + r
    return г["cmp"] == вниз and г["op"] == "−" and vq == vp - r


def _разность_верна(язык, г):
    """Разность спрошена словом: «насколько A выше B» — звено «a − b», «ниже» — «b − a»; слово вопроса и
    ответа — одно, лица — те же."""
    вверх, _вниз = СЛОВА[язык]
    b_после = г.get("b2") or next((и for и, род in РОДИТЕЛЬНЫЙ.items() if род == г.get("bg")), None)
    if г["a"] != г["a2"] or г["b"] != b_после or г["a"] == г["b"]:
        return False
    if "cmp2" in г and г["cmp2"] != г["cmp"]:
        return False
    va, vb, r, va2, vb2, r2 = (int(г[к]) for к in ("va", "vb", "r", "va2", "vb2", "r2"))
    больший, меньший = (va, vb) if г["cmp"] == вверх else (vb, va)
    return (г["op"] == "−" and больший - меньший == r >= 1
            and (va2, vb2, r2) == (больший, меньший, r))


def _судить(строка):
    с = строка.strip()
    if not с:
        return False, False
    for язык, (дано, разн) in ОБРАЗЦЫ.items():
        м = дано.match(с)
        if м:
            return True, _дано_верно(язык, м.groupdict())
        м = разн.match(с)
        if м:
            return True, _разность_верна(язык, м.groupdict())
    return False, False


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def _самопроверка():
    """Всякая страница дома истинна; порча итога, слова сравнения, знака звена и лица опоры — ложь."""
    import gen_genesis_height as Д  # noqa: PLC0415 — подсадки от страниц дома, не от литерала сцены
    беды = [с for с in Д.ПОКАЗЫ if _судить(с) != (True, True)]
    порч = 0
    for i, (с, (язык, _род)) in enumerate(sorted(Д.ПОКАЗЫ.items())):
        if i % 5:
            continue
        вверх, вниз = СЛОВА[язык]
        м = re.search(r"= (\d+)\.$", с)
        порчи = [с[:м.start(1)] + f"{int(м.group(1)) + 1}.",
                 re.sub(rf"(?<!\w){вверх}(?!\w)", вниз, с, count=1) if вверх in с
                 else re.sub(rf"(?<!\w){вниз}(?!\w)", вверх, с, count=1),
                 с.replace(" − ", " + ", 1) if " − " in с else с.replace(" + ", " − ", 1)]
        for порча in порчи:
            порч += 1
            if порча == с or _судить(порча) != (True, False):
                беды.append(f"порча прошла: {порча[:100]}")
    return беды, порч, len(Д.ПОКАЗЫ)


def main():
    import genesis
    беды, порч, страниц = _самопроверка()
    for б in беды[:3]:
        print(f"  САМОПРОВЕРКА: {б}")
    судимо = ложных = 0
    примеры = []
    for путь in genesis.worlds(kind="shows"):
        for строка in путь.read_text(encoding="utf-8", errors="replace").split("\n"):
            если, верно = судить(строка)[:2]
            if not если:
                continue
            судимо += 1
            if not верно:
                ложных += 1
                if len(примеры) < 5:
                    примеры.append(f"{путь.stem}: {строка.strip()[:90]}")
    for п in примеры:
        print(f"  {п}")
    поза = "PASS" if ложных <= ЛОЖНЫХ_РУБЕЖ and not беды else "FAIL"
    print(f"РОСТ {поза}: {ложных} ложных из {судимо} судимых (рубеж {ЛОЖНЫХ_РУБЕЖ}); страниц дома {страниц}, "
          f"порч самопроверки {порч}, бед {len(беды)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
