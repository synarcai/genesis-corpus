#!/usr/bin/env python3
"""СТЕНД РАССУЖДЕНИЯ t9 — вопрос, ожидаемый вердикт или величина, и ЗАКОН
подстрокой (holon, 03.09: суд verum с двумя контролями; ложный закон — не в
корпус, а в стенд). Пробы строятся из тех же функций, что показы миров:
дознание (простота, делимость), уравнения (корень), статистика (среднее,
медиана). Поле «law» — общее утверждение рода, которое обязано стоять в
ответе-рассуждении; «not_law» — ложный закон того же рода, которого в
ответе быть не должно (отрицательный контроль)."""
import json
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import gen_genesis_inquiry as I  # noqa: E402
import gen_genesis_equation as E  # noqa: E402
import gen_genesis_statistics as S  # noqa: E402

ВЫХОД = КОРЕНЬ.parent / "omega" / "bench" / "suites" / "t9_reasoning.jsonl"
ЛОЖНЫЕ = {
    "prime": ("a prime number is a whole number whose only divisor is itself.", "простое число — это целое число, у которого один делитель — оно само."),
    "divisible": ("a number is divisible by another when the remainder is 1.", "число делится на другое, когда остаток равен единице."),
    "root": ("a root of an equation is any value of x.", "корень уравнения — это любое значение x."),
    "mean": ("the mean of a list is its largest number.", "среднее набора — это его наибольшее число."),
    "median": ("the median of a list is its first number.", "медиана набора — это его первое число."),
}


def пробы():
    вон = []
    k = 0
    for шаг in range(4):
        for i in range(6):
            n = 40 + шаг * 7 + i * 5
            прост = I.простое(n)
            for яз, ask in (("en", f"is {n} a prime number?"), ("ru", f"является ли {n} простым числом?")):
                вон.append({"id": f"t9.reasoning.prime.{k}", "tier": 9, "ask": ask,
                            "expect": {"kind": "verdict", "v": ("yes" if яз == "en" else "да") if прост else ("no" if яз == "en" else "нет")},
                            "law": I.ОПР_ПРОСТОТА[0 if яз == "en" else 1], "not_law": ЛОЖНЫЕ["prime"][0 if яз == "en" else 1],
                            "tags": ["t9.reasoning", "prime", яз]})
                k += 1
        for i in range(4):
            a, b = 24 + шаг * 5 + i * 7, 2 + (шаг + i) % 8
            да = a % b == 0
            for яз, ask in (("en", f"is {a} divisible by {b}?"), ("ru", f"делится ли {a} на {b}?")):
                вон.append({"id": f"t9.reasoning.divisible.{k}", "tier": 9, "ask": ask,
                            "expect": {"kind": "verdict", "v": ("yes" if яз == "en" else "да") if да else ("no" if яз == "en" else "нет")},
                            "law": I.ОПР_ДЕЛИМОСТЬ[0 if яз == "en" else 1], "not_law": ЛОЖНЫЕ["divisible"][0 if яз == "en" else 1],
                            "tags": ["t9.reasoning", "divisible", яз]})
                k += 1
        E._СО_ЗНАКОМ = False
        for i, (r1, r2) in enumerate(E.пары(шаг)[:3]):
            b, c = E.по_виете(r1, r2)
            ур = E.уравнение(b, c)
            да, нет = E.свидетель_да(r1, r2), E.свидетель_нет(r1, r2, шаг + i)
            for v, есть in ((да, True), (нет, False)):
                for яз, ask in (("en", f"is {v} a root of {ур}?"), ("ru", f"является ли {v} корнем {ур}?")):
                    вон.append({"id": f"t9.reasoning.root.{k}", "tier": 9, "ask": ask,
                                "expect": {"kind": "verdict", "v": ("yes" if яз == "en" else "да") if есть else ("no" if яз == "en" else "нет")},
                                "law": E.ОПР_КОРЕНЬ[0 if яз == "en" else 1], "not_law": ЛОЖНЫЕ["root"][0 if яз == "en" else 1],
                                "tags": ["t9.reasoning", "root", яз]})
                    k += 1
        for i in range(3):
            набор = S.НАБОРЫ[(шаг + i) % len(S.НАБОРЫ)]
            m = sum(набор) // len(набор)
            п = S.spaced(набор)
            for яз, ask in (("en", f"what is the mean of {п}?"), ("ru", f"чему равно среднее {п}?")):
                вон.append({"id": f"t9.reasoning.mean.{k}", "tier": 9, "ask": ask, "expect": {"kind": "value", "n": m, "surfaces": [str(m)]},
                            "law": S.ЗАКОН_СРЕДНЕЕ[яз], "not_law": ЛОЖНЫЕ["mean"][0 if яз == "en" else 1], "tags": ["t9.reasoning", "mean", яз]})
                k += 1
            нечёт = S.НЕЧЁТНЫЕ[(шаг * 3 + i) % len(S.НЕЧЁТНЫЕ)]
            med = sorted(нечёт)[len(нечёт) // 2]
            п = S.spaced(нечёт)
            for яз, ask in (("en", f"what is the median of {п}?"), ("ru", f"чему равна медиана {п}?")):
                вон.append({"id": f"t9.reasoning.median.{k}", "tier": 9, "ask": ask, "expect": {"kind": "value", "n": med, "surfaces": [str(med)]},
                            "law": S.ЗАКОН_МЕДИАНА[яз], "not_law": ЛОЖНЫЕ["median"][0 if яз == "en" else 1], "tags": ["t9.reasoning", "median", яз]})
                k += 1
    return вон


def main():
    строки = пробы()
    ВЫХОД.parent.mkdir(parents=True, exist_ok=True)
    шапка = ("# t9.reasoning — стенд рассуждения (tools/reasoning_bench.py в genesis-corpus): verdict/value + law (общее утверждение рода, "
             "обязанное стоять в ответе подстрокой) + not_law (ложный закон того же рода — отрицательный контроль, в ответе быть не должен)")
    ВЫХОД.write_text(шапка + "\n" + "\n".join(json.dumps(с, ensure_ascii=False) for с in строки) + "\n", encoding="utf-8")
    print(f"стенд: {len(строки)} проб → {ВЫХОД}")


if __name__ == "__main__":
    main()
