#!/usr/bin/env python3
"""[ОПРЕДЕЛЕНИЯ В HELD-OUT СТРАНИЦАХ] — где полка сама говорит «X есть Y».

holon строит прибор чтения на held-out страницах полки: страница подаётся
утверждениями в одну сессию, потом задаются вопросы, ответы на которые стоят
в самой странице («X is Y.» → «what is X?» ждёт Y). Ему нужен НАБОР страниц
для замера на девяти языках, а не на одном английском, и знание, где факт
спрашивается ТЕКСТОМ САМОЙ СТРАНИЦЫ.

Прибор считает по каждой held-out странице:
  · предложений — всего;
  · СВЯЗОК — утверждений вида «X is Y» на объявленной связке своего языка;
  · ВОПРОСОВ — предложений со знаком вопроса;
  · ПАР — вопрос, за которым СЛЕДУЮЩЕЕ предложение отвечает: делит с ним
    два и более содержательных слова (это оценка сверху, и она названа так
    прямо: прибор не читает смысла, он видит совпадение слов).

СВЯЗКИ ОБЪЯВЛЕНЫ, А НЕ УГАДАНЫ. Для каждого языка полки названы его связки;
язык, чьей связки нет в таблице, считается только предложениями и вопросами —
и это честнее, чем прикладывать английское «is» к финскому тексту.

    python3 scripts/holdout_defs.py [--сколько 25] [--вывод reports/…tsv]
"""
import argparse
import collections
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]

СВЯЗКИ = {
    "en": (r"\bis a\b", r"\bis an\b", r"\bis the\b", r"\bare\b", r"\bis called\b", r"\bmeans\b"),
    "ru": (r" — это ", r"\bесть\b", r"\bявляется\b", r"\bназывается\b", r" — "),
    "de": (r"\bist ein\b", r"\bist eine\b", r"\bist der\b", r"\bist die\b", r"\bist das\b", r"\bheißt\b"),
    "fr": (r"\best un\b", r"\best une\b", r"\best le\b", r"\best la\b", r"\bs'appelle\b"),
    "es": (r"\bes un\b", r"\bes una\b", r"\bes el\b", r"\bes la\b", r"\bse llama\b"),
    "it": (r"\bè un\b", r"\bè una\b", r"\bè il\b", r"\bè la\b", r"\bsi chiama\b"),
    "pt": (r"\bé um\b", r"\bé uma\b", r"\bé o\b", r"\bé a\b", r"\bchama-se\b"),
    "nl": (r"\bis een\b", r"\bis de\b", r"\bis het\b", r"\bheet\b"),
    "pl": (r"\bto jest\b", r"\bjest\b", r"\bnazywa się\b"),
    "la": (r"\best\b", r"\bsunt\b", r"\bappellatur\b", r"\bdicitur\b"),
    "el": (r"\bείναι\b", r"\bλέγεται\b"),
    "fi": (r"\bon\b", r"\bkutsutaan\b"),
    "sv": (r"\bär en\b", r"\bär ett\b", r"\bär den\b", r"\bkallas\b"),
}
КОНЕЦ = re.compile(r"(?<=[.!?])\s+")
СЛОВО = re.compile(r"[^\W\d_]{4,}", re.UNICODE)
ДЛИНА = (25, 400)


def предложения(текст):
    for кусок in КОНЕЦ.split(текст):
        с = " ".join(кусок.split())
        if ДЛИНА[0] <= len(с) <= ДЛИНА[1]:
            yield с


def мера(путь, язык):
    текст = путь.read_text(encoding="utf-8", errors="replace")
    ряд = list(предложения(текст))
    связки = [re.compile(о, re.IGNORECASE | re.UNICODE) for о in СВЯЗКИ.get(язык, ())]
    итог = collections.Counter(предложений=len(ряд))
    предыдущий_вопрос = None
    for с in ряд:
        if any(о.search(с) for о in связки):
            итог["связок"] += 1
        if "?" in с:
            итог["вопросов"] += 1
            предыдущий_вопрос = set(СЛОВО.findall(с.lower()))
            continue
        if предыдущий_вопрос is not None:
            общие = предыдущий_вопрос & set(СЛОВО.findall(с.lower()))
            if len(общие) >= 2:
                итог["пар"] += 1
            предыдущий_вопрос = None
    return итог


def main():
    ап = argparse.ArgumentParser()
    ап.add_argument("--сколько", type=int, default=25)
    ап.add_argument("--вывод", default="reports/HOLDOUT-DEFS-2026-09-03.tsv")
    а = ап.parse_args()
    строки = []
    по_языку = collections.Counter()
    for путь in sorted((КОРЕНЬ / "shelf").rglob("*.holdout.txt")):
        язык = путь.parent.name
        и = мера(путь, язык)
        if not и["предложений"]:
            continue
        плотность = 1000 * и["связок"] // и["предложений"]
        строки.append((язык, str(путь.relative_to(КОРЕНЬ)), и["предложений"],
                       и["связок"], плотность, и["вопросов"], и["пар"]))
        по_языку[язык] += и["связок"]
    строки.sort(key=lambda з: (-з[4], -з[3]))
    вывод = КОРЕНЬ / а.вывод
    with вывод.open("w", encoding="utf-8") as f:
        f.write("# язык\tстраница\tпредложений\tсвязок\tсвязок на 1000\tвопросов\tпар вопрос→ответ\n")
        for р in строки:
            f.write("\t".join(map(str, р)) + "\n")
    print(f"HELD-OUT ОПРЕДЕЛЕНИЯ: страниц {len(строки)}, языков {len(по_языку)}, файл {а.вывод}")
    print(f"  {'язык':4} {'страница':52} {'предл':>7} {'связок':>7} {'/1000':>6} {'вопр':>5} {'пар':>5}")
    for язык, имя, предл, связок, плотн, вопр, пар in строки[:а.сколько]:
        print(f"  {язык:4} {имя[-52:]:52} {предл:7} {связок:7} {плотн:6} {вопр:5} {пар:5}")
    богатые = collections.Counter()
    for язык, _, _, связок, _, _, _ in строки:
        богатые[язык] += связок
    print("  СВЯЗОК ПО ЯЗЫКАМ: " + ", ".join(f"{я} {n}" for я, n in богатые.most_common()))
    с_парами = [р for р in строки if р[6] >= 3]
    print(f"  СТРАНИЦ, ГДЕ ПРОЗА САМА СПРАШИВАЕТ (пар ≥ 3): {len(с_парами)}")
    for р in с_парами[:10]:
        print(f"    {р[0]:4} {р[1][-56:]:56} вопросов {р[5]}, пар {р[6]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
