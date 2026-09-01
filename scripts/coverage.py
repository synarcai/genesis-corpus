#!/usr/bin/env python3
"""[СУДИМОСТЬ КОРПУСА] — доля строк, которую хоть один суд ЧИТАЕТ.

Всякий суд отвечает на вопрос «нет ли лжи среди того, что я понимаю».
Ни один не отвечает на вопрос «а много ли я понимаю» — и корпус может
стоять зелёным, будучи проверенным наполовину. Это тот же род беды, что
молчащий прибор: ноль находок при нулевом обходе.

ПРИБОР МЕРИТ ОХВАТ, А НЕ ИСТИНУ. Строка считается судимой, если ХОТЬ
ОДИН суд взялся её судить — безразлично, признал он её истинной или
ложной. Ложь считают суды; здесь считают ВИДИМОСТЬ.

СТРОКА ЯЗЫКОВОГО ПЛАСТА СУДИМА ВСЕГДА: суд пластов проверяет каждое её
слово на объявленность, и это проверка не слабее счётной.

РУБЕЖ МОЖЕТ ТОЛЬКО РАСТИ. Владелец потребовал ста процентов, и путь
туда лежит через объявления: форма, которую не судит никто, обязана
либо получить судью, либо исчезнуть из слоя.
"""
import importlib
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "courts"))
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import genesis  # noqa: E402
import arith_court as A  # noqa: E402
import logic_court as L  # noqa: E402
import markup_court as MK  # noqa: E402
import langlayer_court as LL  # noqa: E402
import episode_court as EP  # noqa: E402

# РУБЕЖ-ОХВАТА: доля судимых строк корпуса, %
СУДИМОСТЬ_РУБЕЖ = 86

# ПУСТОЙ-ОБХОД: no-such-manifest

ПРОЧИЕ = ["algo", "formula", "physics", "cyber", "notation", "program",
          "statistics", "proof", "machine", "episode", "copula"]


def main():
    словарь = A.словари()
    знаки = L.имена_знаков()
    суды = {и: importlib.import_module(f"{и}_court") for и in ПРОЧИЕ}
    try:
        миры = genesis.manifest()["worlds"]
    except genesis.Unreadable as беда:
        print(f"СУДИМОСТЬ ОТКАЗ: {беда}")
        return 2
    всего = взято = 0
    по_мирам = []
    for мир in миры:
        if мир.get("text") == "prose":
            continue
        путь = genesis._resolve(мир["file"])
        if not путь.is_file():
            continue
        слой = MK.Слой()
        слой.впитать(путь)
        EP.впитать_ставки(путь)
        EP.впитать_итоги(путь)
        пласт = мир["name"].startswith("lang_")
        слова = LL.словарь_пакета(мир["name"][5:])[0] if пласт else None
        свои = взяты = 0
        with путь.open(encoding="utf-8", errors="replace") as поток:
            for строка in поток:
                if not строка.strip():
                    continue
                свои += 1
                видно = (
                    any(A.судить(ч, словарь)[0]
                        for ч in A.предложения(строка))
                    or L.судить(строка, знаки)[0]
                    or MK.судить(строка, слой)[0]
                    or any(с.судить(строка)[0] for с in суды.values())
                )
                if not видно and слова is not None:
                    видно = True
                взяты += видно
        всего += свои
        взято += взяты
        по_мирам.append((взяты / свои if свои else 1.0,
                         мир["name"], свои, взяты))
    if not всего:
        print("СУДИМОСТЬ ОТКАЗ: обход пуст, мерить нечего")
        return 2
    доля = 100 * взято // всего
    по_мирам.sort()
    for д, имя, свои, взяты in по_мирам[:5]:
        if д < 1.0:
            print(f"  {имя:<22}{свои:>7}{взяты:>8}{int(д * 100):>6}%")
    итог = "PASS" if доля >= СУДИМОСТЬ_РУБЕЖ else "FAIL"
    print(f"СУДИМОСТЬ {итог}: {взято} из {всего} строк судимы "
          f"({доля}% при рубеже {СУДИМОСТЬ_РУБЕЖ}%)")
    return 0 if доля >= СУДИМОСТЬ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
