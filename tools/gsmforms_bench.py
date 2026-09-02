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
    raise ValueError(семья)


def пробы():
    вон = []
    семьи = {"сумма": G.п_сумма, "температура": G.п_температура, "процент": G.п_процент,
             "фунты": G.п_фунты, "глубина": G.п_глубина, "вероятность": G.п_вероятность,
             "четверти": G.п_четверти, "дополнение": G.п_дополнение}
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
            for сдвиг in (1, 2, 3, 16, 4, 8):
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
