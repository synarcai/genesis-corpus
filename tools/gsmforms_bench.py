#!/usr/bin/env python3
"""СТЕНД М-143 ДЛЯ ШКОЛЬНЫХ ФОРМ — данные суда, не свода.

Заказ verum/holon (03.09): для многошаговых школьных миров — три вида
проб на каждую задачу, и все три выводятся из ОДНОЙ функции параметров
семейства (tools/gen_genesis_gsmforms.п_*), той же, что пишет показы:
  · value   — вопрос как в мире, ключ = ответ;
  · refuse  — тот же вопрос с УДАЛЁННЫМ фактом, без которого ответ не
              выводится; ключ — отказ с названной недостающей величиной
              (expect {"kind": "refuse", "need": "…"}): единственный прямой
              контроль того, что организм отказывает, а не считает наугад;
  · perturb — те же слова с ВОЗМУЩЁННЫМ числом и ПЕРЕСЧИТАННЫМ ключом:
              генератор знает программу решения и считает сам.
Пишется в omega/bench/suites/t7_gsmforms.jsonl тем же форматом, что
t7_svamp_all.jsonl (id, tier, ask, expect, tags). Полоса организма читает
`need` через bandlib (holon): ok, если организм отказал И его стекло
называет величину.
"""
import json
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import gen_genesis_gsmforms as G  # noqa: E402

ВЫХОД = КОРЕНЬ.parent / "omega" / "bench" / "suites" / "t7_gsmforms.jsonl"
СЕМЯН = 6


def ч(n):
    return str(n).replace("-", "−")


def факты_и_вопрос(семья, п):
    """(факты как список (имя, текст EN), вопрос EN, ключ, программа).
    Программа — функция от словаря фактов к ответу; удаление факта делает
    ответ невыводимым, возмущение числа пересчитывается ею же."""
    if семья == "сумма":
        f = [("x", f"{п['a']} has {п['x']} {G.by_count(п['x'], п['en'])}"),
             ("y", f"{п['b']} has {п['y']} {G.by_count(п['y'], п['en'])}")]
        return f, f"what's the total number of {п['en']}?", lambda d: d["x"] + d["y"], {"x": п["x"], "y": п["y"]}, {"x": f"how many {п['en']} {п['a']} has", "y": f"how many {п['en']} {п['b']} has"}
    if семья == "температура":
        f = [("t0", f"the temperature was {ч(п['t0'])} {G.by_count(abs(п['t0']), 'degrees')}"),
             ("d", f"it {'fell' if п['падение'] else 'rose'} by {п['d']} {G.by_count(п['d'], 'degrees')}")]
        return f, "what is the temperature in degrees now?", (lambda d: d["t0"] - d["d"]) if п["падение"] else (lambda d: d["t0"] + d["d"]), {"t0": п["t0"], "d": п["d"]}, {"t0": "the starting temperature", "d": "by how many degrees it changed"}
    if семья == "процент":
        f = [("всего", f"the class has {п['всего']} pupils"), ("часть", f"{п['часть']} of them are girls")]
        return f, "what percentage of the class are girls?", lambda d: d["часть"] * 100 // d["всего"] if d["часть"] * 100 % d["всего"] == 0 else None, {"всего": п["всего"], "часть": п["часть"]}, {"всего": "how many pupils the class has", "часть": "how many of them are girls"}
    if семья == "фунты":
        f = [("унц", f"the parcel weighs {п['унц']} ounces"), ("правило", "a pound is 16 ounces")]
        return f, "what is the weight in pounds?", lambda d: d["унц"] // 16 if d["унц"] % 16 == 0 else None, {"унц": п["унц"]}, {"унц": "the weight in ounces", "правило": "how many ounces make a pound"}
    if семья == "глубина":
        f = [("w", f"the tank is {п['w']} feet wide"), ("l", f"it is {п['l']} feet long"), ("v", f"it holds {п['v']} cubic feet of water")]
        return f, "what is the tank's water depth in feet?", lambda d: d["v"] // (d["w"] * d["l"]) if d["v"] % (d["w"] * d["l"]) == 0 else None, {"w": п["w"], "l": п["l"], "v": п["v"]}, {"w": "the width of the tank", "l": "the length of the tank", "v": "how much water the tank holds"}
    if семья == "вероятность":
        f = [("r", f"a bag holds {п['r']} red {G.by_count(п['r'], 'marbles')}"), ("b", f"it holds {п['b']} blue {G.by_count(п['b'], 'marbles')}")]
        return f, "what is the probability of drawing a red marble, expressed as a fraction?", lambda d: f"{d['r']}/{d['r'] + d['b']}", {"r": п["r"], "b": п["b"]}, {"r": "how many red marbles the bag holds", "b": "how many blue marbles the bag holds"}
    if семья == "четверти":
        f = [("часть", f"{п['часть']} pupils are {п['слово']} of the class")]
        return f, "how many pupils does the class have?", lambda d: d["часть"] * 4 // п["k"] if d["часть"] * 4 % п["k"] == 0 else None, {"часть": п["часть"]}, {"часть": f"how many pupils are {п['слово']} of the class"}
    if семья == "дополнение":
        род = п["род"]
        if род == 0:
            f = [("было", f"there were originally {п['было']} cars in the lot"), ("ушло", f"{п['ушло']} drove away")]
            return f, "how many cars remain?", lambda d: d["было"] - d["ушло"], {"было": п["было"], "ушло": п["ушло"]}, {"было": "how many cars there were originally", "ушло": "how many cars drove away"}
        if род == 1:
            f = [("было", f"the set has {п['было']} pieces"), ("осталось", f"{п['было'] - п['ушло']} pieces are in the box")]
            return f, "how many pieces are missing?", lambda d: d["было"] - d["осталось"], {"было": п["было"], "осталось": п["было"] - п["ушло"]}, {"было": "how many pieces the set has", "осталось": "how many pieces are in the box"}
        f = [("было", f"there were {п['было']} people on the bus"), ("ушло", f"{п['ушло']} got off")]
        return f, "how many people are on the bus now?", lambda d: d["было"] - d["ушло"], {"было": п["было"], "ушло": п["ушло"]}, {"было": "how many people were on the bus", "ушло": "how many got off"}
    # ---- ВТОРОЙ СЛОЙ (03.09): семейства 9–17 и роды SVAMP; словесные
    # величины (доля, кратность) не входят в данные — их факт не
    # удаляется и не возмущается, программа замыкает их число.
    if семья == "население":
        доля = п["доля"]
        f = [("всего", f"the town has {п['всего']} people"), ("доля", f"{п['слово']} of the whole population lives in the centre")]
        return f, "how many people live in the centre?", lambda d: d["всего"] // доля if d["всего"] % доля == 0 else None, {"всего": п["всего"]}, {"всего": "how many people the town has", "доля": "what part of the population lives in the centre"}
    if семья == "команда":
        f = [("м", f"the number of boys on the team is {п['м']}"), ("д", f"the number of girls is {п['д']}")]
        return f, "how many players does the team have?", lambda d: d["м"] + d["д"], {"м": п["м"], "д": п["д"]}, {"м": "how many boys are on the team", "д": "how many girls are on the team"}
    if семья == "кратно":
        k = п["k"]
        f = [("цена", f"the car cost {п['цена']} dollars"), ("k", f"the house cost {п['слово']} as much as the car")]
        return f, "how much did the house cost in dollars?", lambda d: d["цена"] * k, {"цена": п["цена"]}, {"цена": "how much the car cost", "k": "how many times as much the house cost"}
    if семья == "проект":
        k = п["k"]
        f = [("старт", f"the design started with {п['старт']} panels"), ("k", f"it was {'doubled' if k == 2 else 'tripled'}"), ("минус", f"then it was reduced by {п['минус']}")]
        return f, "how many panels does the final design have?", lambda d: d["старт"] * k - d["минус"] if d["старт"] * k > d["минус"] else None, {"старт": п["старт"], "минус": п["минус"]}, {"старт": "how many panels the design started with", "k": "how many times the design grew", "минус": "by how many panels the design was reduced"}
    if семья == "окружность":
        f = [("длина", f"the circumference of the earth is taken as {п['длина']} miles"), ("скорость", f"the plane flies {п['скорость']} miles per hour")]
        return f, "how many hours does the flight around the earth take?", lambda d: d["длина"] // d["скорость"] if d["длина"] % d["скорость"] == 0 else None, {"длина": п["длина"], "скорость": п["скорость"]}, {"длина": "the circumference of the earth", "скорость": "how fast the plane flies"}
    if семья == "верёвки":
        f = [("всего", f"the total length of the ropes is {п['всего']} meters"), ("n", f"there are {п['n']} ropes")]
        return f, "how long is the average rope in meters?", lambda d: d["всего"] // d["n"] if d["всего"] % d["n"] == 0 else None, {"всего": п["всего"], "n": п["n"]}, {"всего": "the total length of the ropes", "n": "how many ropes there are"}
    if семья == "трое":
        k = п["k"]
        x, y, z = G.ИМЕНА_EN[п["a"] % len(G.ИМЕНА_EN)], G.ИМЕНА_EN[(п["a"] + 1) % len(G.ИМЕНА_EN)], G.ИМЕНА_EN[(п["a"] + 2) % len(G.ИМЕНА_EN)]
        f = [("a", f"{x} has {п['a']} books"), ("больше", f"{y} has {п['больше']} more books than {x}"), ("k", f"{z} has {'twice' if k == 2 else 'three times'} as many books as {x}")]
        return f, "how many books do they have together?", lambda d: d["a"] + (d["a"] + d["больше"]) + k * d["a"], {"a": п["a"], "больше": п["больше"]}, {"a": f"how many books {x} has", "больше": f"how many more books {y} has than {x}", "k": f"how many times as many books {z} has as {x}"}
    if семья == "ставка":
        x = G.ИМЕНА_EN[п["часы"] % len(G.ИМЕНА_EN)]
        f = [("в_час", f"{x} makes {п['в_час']} candles an hour"), ("часы", f"{x} works {п['часы']} hours")]
        return f, f"how many candles does {x} make?", lambda d: d["в_час"] * d["часы"], {"в_час": п["в_час"], "часы": п["часы"]}, {"в_час": f"how many candles {x} makes an hour", "часы": f"how many hours {x} works"}
    if семья == "листки":
        x = G.ИМЕНА_EN[п["раз"] % len(G.ИМЕНА_EN)]
        f = [("было", f"{x} had {п['было']} post-it notes"), ("раз", f"{x} used {п['раз']} on the fridge"), ("два", f"{x} used {п['два']} on the door")]
        return f, f"how many post-it notes does {x} have left?", lambda d: d["было"] - d["раз"] - d["два"] if d["было"] >= d["раз"] + d["два"] else None, {"было": п["было"], "раз": п["раз"], "два": п["два"]}, {"было": f"how many post-it notes {x} had", "раз": "how many went on the fridge", "два": "how many went on the door"}
    if семья == "разница":
        x = G.ИМЕНА_EN[п["x"] % len(G.ИМЕНА_EN)]
        f = [("x", f"{x} planted {п['x']} trees in the morning"), ("y", f"{x} planted {п['y']} trees in the afternoon")]
        return f, f"how many more trees did {x} plant in the morning than in the afternoon?", lambda d: d["x"] - d["y"] if d["x"] > d["y"] else None, {"x": п["x"], "y": п["y"]}, {"x": "how many trees were planted in the morning", "y": "how many trees were planted in the afternoon"}
    if семья == "скидка":
        f = [("цена", f"each pack costs {п['цена']} dollars"), ("скидка", f"there is a discount of {п['скидка']} dollars on each pack")]
        return f, "how much do you have to pay for each pack in dollars?", lambda d: d["цена"] - d["скидка"] if d["цена"] > d["скидка"] else None, {"цена": п["цена"], "скидка": п["скидка"]}, {"цена": "how much each pack costs", "скидка": "how big the discount is"}
    if семья == "всего":
        x = G.ИМЕНА_EN[п["x"] % len(G.ИМЕНА_EN)]
        en = G.ВЕЩИ[п["y"] % len(G.ВЕЩИ)][0]
        if п["род"] == 2:
            y = min(п["y"], п["x"] - 1)
            f = [("x", f"{x} had {п['x']} {G.by_count(п['x'], en)}"), ("y", f"{x} gave away {y}")]
            return f, f"how many {en} are left?", lambda d: d["x"] - d["y"] if d["x"] >= d["y"] else None, {"x": п["x"], "y": y}, {"x": f"how many {en} {x} had", "y": f"how many {en} {x} gave away"}
        слово = "in all" if п["род"] == 0 else "altogether"
        f = [("x", f"{x} has {п['x']} {G.by_count(п['x'], en)} in one box"), ("y", f"{x} has {п['y']} {G.by_count(п['y'], en)} in another box")]
        return f, f"how many {en} does {x} have {слово}?", lambda d: d["x"] + d["y"], {"x": п["x"], "y": п["y"]}, {"x": f"how many {en} are in the first box", "y": f"how many {en} are in the second box"}
    if семья == "группы":
        f = [("всего", f"there are {п['всего']} pupils"), ("n", f"they stand in groups of {п['n']}")]
        return f, "how many groups are there?", lambda d: d["всего"] // d["n"] if d["всего"] % d["n"] == 0 else None, {"всего": п["всего"], "n": п["n"]}, {"всего": "how many pupils there are", "n": "how big each group is"}
    # ---- ТРЕТИЙ СЛОЙ (03.09): роды SVAMP по массе e9 и остаток g1
    if семья == "полосы":
        д1, д2, г, г0, в = п["д1"], п["д2"], п["г"], п["г0"], п["в"]
        f = [("x", f"{д1} {г} {п['x']} {в}"), ("y", f"{д2} {г} {п['y']} {в}")]
        return (f, f"how many more {в} did {д1} {г0} than {д2}?",
                lambda d: d["x"] - d["y"] if d["x"] > d["y"] else None, {"x": п["x"], "y": п["y"]},
                {"x": f"how many {в} {д1} {г}", "y": f"how many {в} {д2} {г}"})
    if семья == "больше":
        оч, сл = п["очертание"], п["слова"]
        имя = G.ИМЕНА_EN[п["x"] % len(G.ИМЕНА_EN)]
        if оч == 0:
            г, г0, в = сл[0], сл[1], сл[2]
            к1, к2 = G.КОГДА[п["x"] % len(G.КОГДА)][:2]
            f = [("x", f"{имя} {г} {п['x']} {в} {к1}"), ("y", f"{имя} {г} {п['y']} {в} {к2}")]
            вопрос = f"how many more {в} did {имя} {г0} {к1} than {к2}?"
        elif оч == 1:
            г, г0, в1, в2 = сл[0], сл[1], сл[2], сл[3]
            f = [("x", f"{имя} {г} {п['x']} {в1}"), ("y", f"{имя} {г} {п['y']} {в2}")]
            вопрос = f"how many more {в1} than {в2} did {имя} {г0}?"
        elif оч == 2:
            a, b, где = сл[0], сл[1], сл[2]
            f = [("x", f"there were {п['x']} {a} {где}"), ("y", f"there were {п['y']} {b} {где}")]
            вопрос = f"how many more {a} than {b} were there?"
        else:
            на1, на2 = сл[0], сл[1]
            f = [("x", f"{имя} spent {п['x']} dollars {на1}"), ("y", f"{имя} spent {п['y']} dollars {на2}")]
            вопрос = f"how much more money did {имя} spend {на1} than {на2}?"
        нужды = {"x": f[0][1].replace(str(п["x"]), "how many", 1) if оч != 3 else f"how much money {имя} spent {сл[0]}",
                 "y": f[1][1].replace(str(п["y"]), "how many", 1) if оч != 3 else f"how much money {имя} spent {сл[1]}"}
        return f, вопрос, lambda d: d["x"] - d["y"] if d["x"] > d["y"] else None, {"x": п["x"], "y": п["y"]}, нужды
    if семья == "отбор":
        г, г0, в = п["слова"][0], п["слова"][1], п["слова"][2]
        имя = G.ИМЕНА_EN[п["a"] % len(G.ИМЕНА_EN)]
        когда = G.СРОКИ[п["срок"]]
        f = [("a", f"{имя} {г} {п['a']} {в} in the morning"), ("b", f"{имя} {г} {п['b']} {в} in the afternoon"), ("c", f"{имя} {г} {п['c']} {в} in the evening")]
        ключ = ("a", "b", "c")[п["срок"]]
        return f, f"how many {в} did {имя} {г0} {когда}?", lambda d: d[ключ], {"a": п["a"], "b": п["b"], "c": п["c"]}, {"a": f"how many {в} {имя} {г} in the morning", "b": f"how many {в} {имя} {г} in the afternoon", "c": f"how many {в} {имя} {г} in the evening"}
    if семья == "остаток":
        что = "cakes" if п["свои"] else "pastries"
        f = [("n", f"the baker made {п['n']} cakes"), ("m", f"the baker made {п['m']} pastries"), ("k", f"the baker sold {п['k']} {что}")]
        return f, "how many cakes would the baker still have?", (lambda d: d["n"] - d["k"] if d["n"] >= d["k"] else None) if п["свои"] else (lambda d: d["n"]), {"n": п["n"], "m": п["m"], "k": п["k"]}, {"n": "how many cakes the baker made", "m": "how many pastries the baker made", "k": f"how many {что} the baker sold"}
    if семья == "класс":
        if п["род"] == 0:
            f = [("g", f"there are {п['g']} girls in the class"), ("b", f"there are {п['b']} boys in the class")]
            return f, "how many pupils are there in the class?", lambda d: d["g"] + d["b"], {"g": п["g"], "b": п["b"]}, {"g": "how many girls are in the class", "b": "how many boys are in the class"}
        f = [("s", f"there are {п['s']} pupils in the class"), ("g", f"{п['g']} of them are girls")]
        return f, "how many boys are there in the class?", lambda d: d["s"] - d["g"] if d["s"] > d["g"] else None, {"s": п["s"], "g": п["g"]}, {"s": "how many pupils are in the class", "g": "how many of them are girls"}
    if семья == "деньги":
        имя = G.ИМЕНА_EN[п["n"] % len(G.ИМЕНА_EN)]
        en = G.ВЕЩИ[п["p"] % len(G.ВЕЩИ)][0]
        if п["род"] == 0:
            f = [("n", f"{имя} bought {п['n']} {en}"), ("p", f"each of the {en} cost {п['p']} dollars")]
            return f, f"how much money did {имя} spend?", lambda d: d["n"] * d["p"], {"n": п["n"], "p": п["p"]}, {"n": f"how many {en} {имя} bought", "p": f"how much each of the {en} cost"}
        f = [("a", f"{имя} had {п['a']} dollars"), ("b", f"{имя} spent {п['b']} dollars")]
        return f, "how much money is left?", lambda d: d["a"] - d["b"] if d["a"] > d["b"] else None, {"a": п["a"], "b": п["b"]}, {"a": f"how much money {имя} had", "b": f"how much money {имя} spent"}
    if семья == "сдача":
        имя = G.ИМЕНА_EN[п["p"] % len(G.ИМЕНА_EN)]
        f = [("n", f"{имя} gave the craftsman {п['n']} bills"), ("b", f"each bill is {п['b']} dollars"), ("p", f"the hat is worth {п['p']} dollars")]
        return f, f"how much change did {имя} get?", lambda d: d["n"] * d["b"] - d["p"] if d["n"] * d["b"] > d["p"] else None, {"n": п["n"], "b": п["b"], "p": п["p"]}, {"n": f"how many bills {имя} gave", "b": "how many dollars each bill is", "p": "how much the hat is worth"}
    if семья == "прибыль":
        имя = G.ИМЕНА_EN[п["p"] % len(G.ИМЕНА_EN)]
        a, b = п["a"], п["b"]
        f = [("p", f"{имя} bought the magazines at {п['p']} dollars"), ("дробь", f"{имя} sells them at {a}/{b} of the price")]
        return f, "what is the profit in dollars?", lambda d: d["p"] * a // b - d["p"] if d["p"] % b == 0 else None, {"p": п["p"]}, {"p": "how much the magazines were bought at", "дробь": "at what part of the price they are sold"}
    if семья == "завышение":
        имя = G.ИМЕНА_EN[п["n"] % len(G.ИМЕНА_EN)]
        f = [("n", f"{имя} reported {п['n']} people at the concert"), ("q", f"the number was overstated by {п['q']} percent")]
        return f, "how many people really attended?", lambda d: d["n"] * 100 // (100 + d["q"]) if d["n"] * 100 % (100 + d["q"]) == 0 else None, {"n": п["n"], "q": п["q"]}, {"n": "how many people were reported", "q": "by how many percent the number was overstated"}
    if семья == "половина":
        k, делить = п["k"], п["делить"]
        f = [("n", f"there were {п['n']} ants in the garden"), ("k", f"there were {п['слово']} bugs as ants")]
        return f, "how many insects were there in all?", lambda d: d["n"] + (d["n"] // k if делить else d["n"] * k) if (not делить or d["n"] % k == 0) else None, {"n": п["n"]}, {"n": "how many ants there were", "k": "how many bugs there were compared to ants"}
    raise ValueError(семья)


def пробы():
    вон = []
    семьи = {"сумма": G.п_сумма, "температура": G.п_температура, "процент": G.п_процент,
             "фунты": G.п_фунты, "глубина": G.п_глубина, "вероятность": G.п_вероятность,
             "четверти": G.п_четверти, "дополнение": G.п_дополнение,
             "население": G.п_население, "команда": G.п_команда, "кратно": G.п_кратно,
             "проект": G.п_проект, "окружность": G.п_окружность, "верёвки": G.п_верёвки,
             "трое": G.п_трое, "ставка": G.п_ставка, "листки": G.п_листки,
             "разница": G.п_разница, "скидка": G.п_скидка, "всего": G.п_всего, "группы": G.п_группы,
             "больше": G.п_больше, "отбор": G.п_отбор, "остаток": G.п_остаток, "класс": G.п_класс,
             "деньги": G.п_деньги, "сдача": G.п_сдача, "прибыль": G.п_прибыль, "завышение": G.п_завышение,
             "половина": G.п_половина, "полосы": G.п_полосы}
    for имя, п_ in семьи.items():
        for k in range(СЕМЯН):
            шаг, i = k % 5, 7 * k + 3
            п = п_(шаг, i)
            факты, вопрос, программа, данные, нужды = факты_и_вопрос(имя, п)
            текст = ". ".join(т for _, т in факты) + ". " + вопрос
            ключ = программа(данные)
            if ключ is None:
                continue
            бирка = f"t7.gsmforms.{имя}.{k}"
            def ожидание(з):
                return ({"kind": "value", "n": з, "surfaces": [ч(з)]} if isinstance(з, int)
                        else {"kind": "value", "surfaces": [з]})
            вон.append({"id": бирка, "tier": 7, "ask": текст, "expect": ожидание(ключ),
                        "tags": ["t7.gsmforms", имя, "value"]})
            # ОТКАЗ: удалён факт, без которого ответ не выводится (первый числовой)
            имя_факта = next(n for n, _ in факты if n in данные)
            без = ". ".join(т for n, т in факты if n != имя_факта) + ". " + вопрос
            вон.append({"id": бирка + ".refuse", "tier": 7, "ask": без,
                        "expect": {"kind": "refuse", "need": нужды[имя_факта]},
                        "tags": ["t7.gsmforms", имя, "refuse", "m143"]})
            # ВОЗМУЩЕНИЕ: одно число сдвинуто, ключ пересчитан программой
            возм = dict(данные)
            for сдвиг in (1, 2, 3, 16, 4, 8, 5, 10, 20):
                возм[имя_факта] = данные[имя_факта] + сдвиг
                ключ2 = программа(возм)
                if ключ2 is not None and ключ2 != ключ:
                    break
            else:
                continue
            старое = str(данные[имя_факта]).replace("-", "−")
            новое = str(возм[имя_факта]).replace("-", "−")
            факты2 = [(n, т.replace(старое, новое, 1) if n == имя_факта else т) for n, т in факты]
            текст2 = ". ".join(т for _, т in факты2) + ". " + вопрос
            вон.append({"id": бирка + ".perturb", "tier": 7, "ask": текст2, "expect": ожидание(ключ2),
                        "tags": ["t7.gsmforms", имя, "perturb", "m143"]})
    return вон


def main():
    строки = пробы()
    ВЫХОД.parent.mkdir(parents=True, exist_ok=True)
    шапка = ("# t7.gsmforms — стенд М-143 школьных форм g1 (tools/gsmforms_bench.py в genesis-corpus): "
             "value / refuse (удалён факт, expect.need — недостающая величина) / perturb (возмущённое число, ключ пересчитан)")
    ВЫХОД.write_text(шапка + "\n" + "\n".join(json.dumps(с, ensure_ascii=False) for с in строки) + "\n", encoding="utf-8")
    виды = {}
    for с in строки:
        виды[с["tags"][2]] = виды.get(с["tags"][2], 0) + 1
    print(f"стенд: {len(строки)} проб — {виды} → {ВЫХОД}")


if __name__ == "__main__":
    main()
