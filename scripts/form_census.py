#!/usr/bin/env python3
"""[ПЕРЕПИСЬ ФОРМ] — сколько рамок несёт корпус, какова их масса и когда
новые тексты перестают давать новые формы.

Слово владельца (03.09): «исследовать, насколько минимальным должен быть
корпус, чтобы обучение дало исследователя; и когда новые тексты уже не дают
новых форм, которые может изучить архитектура — иметь реальную цифру
покрытия». Организм покупает РАМКИ (формы с дырками) по массе показов;
потому корпус меряется не строками, а рамками и их массой.

СКЕЛЕТ СТРОКИ — её рамка на стороне корпуса: числа → «#», объявленные имена
лиц → «@», нотации пространств (сетка, координата, граф, матрица, глиф) →
одна дыра рода, латинско-цифровые записи ($…$, x^2) — как есть. Скелет
есть ПРИБЛИЖЕНИЕ рамки организма (тот режет по леджеру и словам формы),
но закон один: рамка куплена, когда показов ≥ LAW² = 9.

ТРИ ЧИСЛА:
  · РАМОК ВСЕГО и с массой ≥ 9 — предложение корпуса;
  · МИНИМАЛЬНЫЙ КОРПУС — Σ min(масса, 9) по рамкам: строки сверх девяти
    на рамку — вес, не знание (оценка сверху, ибо разные числа одной рамки
    учат разному — исполнителю нужны разные значения);
  · НАСЫЩЕНИЕ — новых рамок на тысячу строк по мере роста корпуса: в
    порядке манифеста и в случайных порядках (среднее по семенам); мир,
    дающий < 1 новой рамки на тысячу строк, насыщен для этой меры.

Печать: сводка, кривая по десяти долям корпуса, миры по новизне (верх и
низ). Отчёт — reports/FORMS-<дата>.md.
"""
import collections
import datetime
import json
import pathlib
import random
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
from genesis import worlds  # noqa: E402

LAW2 = 9
# «3x» — коэффициент есть число (дыра), буква за ним — не часть числа
ЧИСЛО = re.compile(r"(?<![\w#])[−-]?\d+(?:[.,]\d+)?(?![\d#])")
СЕТКА = re.compile(r"(?<![\w#_])[#_]+(?:/[#_]+)+(?![\w#_])")
СЕТКА_ОДНА = re.compile(r"(?<![\w])[#_]{3,}(?![\w])")
ГРАФ = re.compile(r"\b#-#(?:, #-#)*\b")
МАТРИЦА = re.compile(r"\[[#\- /]+\]")
КООРД = re.compile(r"\(#, #\)")


def имена():
    """Every pack's declared names — the actors of every language (04.09:
    the houses of phrases name actors in ten languages)."""
    вон = set()
    for путь in sorted((КОРЕНЬ / "tools" / "langpacks").glob("*.json")):
        п = json.loads(путь.read_text(encoding="utf-8"))
        if not п.get("person_names"):
            continue
        for и in п.get("person_names", ()):
            вон.add(и); вон.add(и.capitalize())
            for ф in п.get("person_forms", {}).get(и, {}).values():
                if isinstance(ф, str):
                    вон.add(ф); вон.add(ф.capitalize())
    return вон


ИМЕНА = имена()
ИМЯ = re.compile(r"\b(" + "|".join(sorted(map(re.escape, ИМЕНА), key=len, reverse=True)) + r")\b") if ИМЕНА else None


def вещи():
    """Объявленные имена вещей обоих пакетов (формы счёта) — вторая ступень
    скелета: РОД рамки, где вещь есть дыра «※», как число — «#»."""
    вон = set()
    п = json.loads((КОРЕНЬ / "tools" / "langpacks" / "en.json").read_text(encoding="utf-8"))
    for к, ф in п.get("noun_forms", {}).items():
        вон.add(к)
        for x in (ф.values() if isinstance(ф, dict) else (ф if isinstance(ф, list) else [ф])):
            if isinstance(x, str):
                вон.add(x)
    try:
        import rugram
        for ключ, формы in rugram.СЧЁТНЫЕ.items():
            вон.add(ключ); вон.update(формы)
            мн = rugram.именительный_мн(ключ)
            if мн:
                вон.add(мн)
    except Exception:
        pass
    return {в for в in вон if в and " " not in в and len(в) > 1}


def заполнители_домов():
    """THE DECLARED FILLERS OF THE HOUSES OF PHRASES — days, places, things,
    units, share names, multiplier words — are holes of the frame as much as
    a number is (М-159): a house fills them, a court reads them back from
    the table. Without this the census counted «on monday ann put 5 cups on
    the shelf» and «on tuesday ann put 5 pens in the box» as two frames and
    called the hole market unsaturated (holes: 5 939 frames in 6 100 lines)."""
    вон = set()
    def _добавить(x):
        if isinstance(x, str):
            if x and x not in ("m", "f", "n"):
                вон.add(x)
        elif isinstance(x, (list, tuple)):
            for y in x:
                _добавить(y)
        elif isinstance(x, dict):
            for y in x.values():
                _добавить(y)
    try:
        import holes, calforms, cmpforms, unitforms, physforms, shareforms, moneyforms, searchforms, moneystory
    except Exception:
        return вон
    _добавить(searchforms.ЧАСТИ)
    for я in moneystory.ЯЗЫКИ.values():
        _добавить(я["вещи"])
    _добавить(holes.ДНИ)
    for язык, рамки in holes.РАМКИ.items():
        for р in рамки:
            _добавить(р.get("места")); _добавить(р.get("вещи"))
    _добавить(holes.ПРОБЕЛЫ)
    for я in calforms.ЯЗЫКИ.values():
        _добавить(я.get("дни")); _добавить(я.get("косв"))
    _добавить(cmpforms.ВЕЩИ); _добавить(cmpforms.КРАТНО)
    _добавить(unitforms.ЕДИНИЦЫ); _добавить(physforms.ЕДИНИЦЫ); _добавить(shareforms.ИМЕНА)
    for я in moneyforms.ЯЗЫКИ.values():
        _добавить(я.get("б")); _добавить(я.get("м"))
    return {в for в in вон if len(в) > 1}


ВЕЩИ = вещи() | заполнители_домов()
ВЕЩЬ = re.compile(r"(?<![^\W\d_])(" + "|".join(sorted(map(re.escape, ВЕЩИ), key=len, reverse=True)) + r")(?![^\W\d_])") if ВЕЩИ else None


def род(скелет_):
    """Вторая ступень: вещи → «※»."""
    return ВЕЩЬ.sub("※", скелет_) if ВЕЩЬ is not None else скелет_


def скелет(строка):
    с = СЕТКА.sub("⊞", строка)
    с = СЕТКА_ОДНА.sub("⊞", с)
    с = ЧИСЛО.sub("#", с)
    с = МАТРИЦА.sub("[▦]", с)
    с = ГРАФ.sub("⋈", с)
    с = КООРД.sub("(·)", с)
    if ИМЯ is not None:
        с = ИМЯ.sub("@", с)
    return re.sub(r"\s+", " ", с).strip()


def перепись(пути):
    """[(мир, [скелеты строк])]."""
    вон = []
    for п in пути:
        строки = [с for с in п.read_text(encoding="utf-8", errors="replace").splitlines() if с.strip() and not с.startswith("\x0c")]
        вон.append((п.stem.replace("genesis_", ""), [скелет(с) for с in строки]))
    return вон


def кривая(миры, порядок):
    """Новые рамки на тысячу строк по десяти долям корпуса в данном порядке."""
    видано = set(); строк = 0; новых = 0; точки = []
    всего = sum(len(с) for _, с in миры)
    шаг = max(1, всего // 10); рубеж = шаг
    for k in порядок:
        for с in миры[k][1]:
            строк += 1
            if с not in видано:
                видано.add(с); новых += 1
            if строк >= рубеж:
                точки.append((строк, новых)); рубеж += шаг
    if not точки or точки[-1][0] != строк:
        точки.append((строк, новых))
    return точки


def main():
    пути = [п for п in worlds(kind="shows") if п.is_file()]
    миры = перепись(пути)
    масса = collections.Counter()
    for _, с in миры:
        масса.update(с)
    всего = sum(масса.values())
    рамок = len(масса)
    купимых = sum(1 for m in масса.values() if m >= LAW2)
    минимум = sum(min(m, LAW2) for m in масса.values())
    # ВТОРАЯ СТУПЕНЬ — РОДЫ: вещь тоже дыра.
    масса_р = collections.Counter()
    for ск, m in масса.items():
        масса_р[род(ск)] += m
    родов = len(масса_р)
    купимых_р = sum(1 for m in масса_р.values() if m >= LAW2)
    минимум_р = sum(min(m, LAW2) for m in масса_р.values())
    строки = [f"# ПЕРЕПИСЬ ФОРМ {datetime.date.today().isoformat()}",
              f"строк {всего}; РАМОК (числа → #, имена → @) {рамок}; с массой ≥ {LAW2}: {купимых} ({100 * купимых // рамок} %), они несут {sum(m for m in масса.values() if m >= LAW2)} строк ({100 * sum(m for m in масса.values() if m >= LAW2) // всего} %)",
              f"РОДОВ (и вещи → ※) {родов}; с массой ≥ {LAW2}: {купимых_р} ({100 * купимых_р // родов} %), они несут {sum(m for m in масса_р.values() if m >= LAW2)} строк ({100 * sum(m for m in масса_р.values() if m >= LAW2) // всего} %)",
              f"МИНИМАЛЬНЫЙ КОРПУС при массе {LAW2}: по рамкам {минимум} строк ({100 * минимум // всего} %), по родам {минимум_р} строк ({100 * минимум_р // всего} %) — оценки сверху: разные числа одной рамки учат исполнителя разному",
              ""]
    # насыщение: порядок манифеста и три случайных
    точки_м = кривая(миры, range(len(миры)))
    случайные = []
    for семя in (1, 2, 3):
        п = list(range(len(миры))); random.Random(семя).shuffle(п)
        случайные.append(кривая(миры, п))
    строки.append("## Насыщение: новых рамок на тысячу строк по долям корпуса (порядок манифеста | среднее трёх случайных порядков)")
    прош_м = (0, 0); прош_с = [(0, 0)] * 3
    for i, (n, нов) in enumerate(точки_м):
        dм = 1000 * (нов - прош_м[1]) / max(1, n - прош_м[0]); прош_м = (n, нов)
        ds = []
        for j, кр in enumerate(случайные):
            if i < len(кр):
                nn, нн = кр[i]; ds.append(1000 * (нн - прош_с[j][1]) / max(1, nn - прош_с[j][0])); прош_с[j] = (nn, нн)
        строки.append(f"  доля {i + 1:2}: строк {n:7} — новых/1000: {dм:6.1f} | {sum(ds) / max(1, len(ds)):6.1f}")
    # миры по новизне (уникальные рамки мира / строки)
    глоб = collections.Counter()
    по_миру = []
    for имя, с in миры:
        свои = set(с)
        роды = {род(ск) for ск in свои}
        по_миру.append((имя, len(с), len(свои), sum(1 for ск in свои if масса[ск] >= LAW2),
                        len(роды), sum(1 for р in роды if масса_р[р] >= LAW2)))
    по_миру.sort(key=lambda r: -1000 * r[2] / max(1, r[1]))
    строки.append("")
    # ОБЕ СТУПЕНИ: рамка (числа и имена — дыры) и род (и вещи, места, дни,
    # единицы — дыры по домам); мир дыр на десяти языках есть 5 855 рамок и
    # несколько сотен родов — новизна рамок там лексическая, не формальная.
    строки.append("## Миры по новизне форм (рамок на тысячу строк; рамок с массой ≥ 9; родов и родов с массой ≥ 9)")
    for имя, n, р, к, рд, кр in по_миру[:15]:
        строки.append(f"  {имя:24} строк {n:6} рамок {р:6} ({1000 * р / max(1, n):6.1f}/1000) купимых {к:5} | родов {рд:5} купимых {кр:5}")
    строки.append("  …")
    for имя, n, р, к, рд, кр in по_миру[-10:]:
        строки.append(f"  {имя:24} строк {n:6} рамок {р:6} ({1000 * р / max(1, n):6.1f}/1000) купимых {к:5} | родов {рд:5} купимых {кр:5}")
    # ИЗБЫТОК МАССЫ ПО МИРАМ: строки сверх девяти на рамку — кандидаты на
    # сокращение (оценка сверху); мир с большим избытком учит весом, не формой.
    строки.append("")
    строки.append("## Миры по избытку массы (строк сверх 9 на рамку; доля мира)")
    избыток = []
    for имя, с in миры:
        м = collections.Counter(с)
        изб = sum(max(0, v - LAW2) for v in м.values())
        избыток.append((имя, len(с), изб))
    избыток.sort(key=lambda r: -r[2])
    for имя, n, изб in избыток[:15]:
        строки.append(f"  {имя:24} строк {n:6} избыток {изб:6} ({100 * изб // max(1, n):3} %)")
    строки.append(f"  избыток всего: {sum(r[2] for r in избыток)} строк из {всего}")
    текст = "\n".join(строки) + "\n"
    (КОРЕНЬ / "reports").mkdir(exist_ok=True)
    (КОРЕНЬ / "reports" / f"FORMS-{datetime.date.today().isoformat()}.md").write_text(текст, encoding="utf-8")
    print(текст)
    # ПОСЛЕДНЯЯ СТРОКА — ВЕРДИКТ ЛЕДЖЕРА: прибор диагностический, поза ОТЧЁТ.
    хвост = точки_м[-1][1] - точки_м[-2][1] if len(точки_м) > 1 else 0
    хв_строк = точки_м[-1][0] - точки_м[-2][0] if len(точки_м) > 1 else 1
    print(f"ПЕРЕПИСЬ ФОРМ ОТЧЁТ: строк {всего}, рамок {рамок} (масса ≥ {LAW2}: {купимых}), родов {родов} (масса ≥ {LAW2}: {купимых_р}); "
          f"минимальный корпус при массе {LAW2}: {минимум} строк по рамкам ({100 * минимум // всего} %), {минимум_р} по родам ({100 * минимум_р // всего} %); "
          f"насыщение: последняя доля даёт {1000 * хвост / max(1, хв_строк):.0f} новых рамок на тысячу строк")
    return 0


if __name__ == "__main__":
    sys.exit(main())
