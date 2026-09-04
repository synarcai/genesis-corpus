#!/usr/bin/env python3
"""ДОМ ПЕРЕПИСИ — одно число, записанное двумя способами.

d5 назвал шестьдесят два голодающих сбора организма, и среди них `rewrite_facts`
— переписывающие показы. Корпус их не имел вовсе: он показывал, ЧТО равно чему,
и ни разу — что ОДНО И ТО ЖЕ число можно записать иначе.

    чем ещё можно записать 5 + 5? 2 × 5: сложить число с собой значит взять
        его дважды, и то и другое есть 10.
    5 + 5 и 3 × 5 — одно и то же? нет: 5 + 5 = 10, а 3 × 5 = 15.

РАЗНИЦА С РАВЕНСТВОМ ТОНКА И ВАЖНА. «5 + 5 = 10» говорит о ЗНАЧЕНИИ; «5 + 5 и
2 × 5 — одно и то же» говорит о ДВУХ ЗАПИСЯХ одного значения, то есть о самой
возможности переписать. Первое учит считать, второе — что запись есть не сама
вещь, а её имя, и имён у вещи много. Без второго организм считает, но не
преобразует.

ВТОРАЯ ФОРМА НЕОБХОДИМА: без неё дом учил бы, что всякие две записи равны.
Отказ показывает, чем именно две записи различаются, — ПЕРЕСЧЁТОМ обеих.

ПЕРЕПИСЬ БЕЗ ЗАКОНА ЕСТЬ СОВПАДЕНИЕ, А НЕ ПЕРЕПИСЬ, и это исправление, за
которое надо благодарить holon (04.09): он спросил, нет ли в доме пар, чьи
записи сходятся ЛИШЬ НА ЭТИХ ЧИСЛАХ. Были, две из восьми: «12 − 4» и «2 × 4»
дают 8 у этих чисел и ничего общего вообще; «18 ÷ 3» и «3 + 3» — то же.
Показав их, дом учил бы, что всякую запись можно переписать всякой, — то есть
ровно обратному тому, ради чего стоит. Обе заменены, и КАЖДАЯ пара теперь есть
случай ОБЪЯВЛЕННОГО ЗАКОНА, а закон назван в самом показе:

    чем ещё можно записать 9 × 2? 2 × 9: порядок множителей не меняет
        произведения, и то и другое есть 18.

Четыре закона — удвоение, утроение, перестановка множителей, сокращение
частного — и все четыре суть тождества, верные при любых числах, а не при этих.

ГОЛОЙ ПЕРЕПИСИ ДОМ НЕ ПИШЕТ («5 + 5 и 2 × 5 — одно и то же число: 10.»): её
содержание целиком стоит в вопросной форме, а родом без вопросной поверхности
она быть перестаёт (М-268 — третий случай за сутки, когда долг платится
вычитанием).

    python3 tools/rewriteforms.py    # самопроверка с мутантами
"""
# (первая запись, вторая запись, ЛОЖНАЯ третья) — значения вычисляются
ТРОЙКИ = (
    ("5 + 5", "2 × 5", "3 × 5", "удвоение"),
    ("4 + 4 + 4", "3 × 4", "4 × 4", "утроение"),
    ("7 + 7", "2 × 7", "3 × 7", "удвоение"),
    ("6 × 3", "6 + 6 + 6", "6 × 4", "утроение"),
    ("9 × 2", "2 × 9", "9 + 2", "перестановка"),
    ("3 × 8", "8 × 3", "3 + 8", "перестановка"),
    ("20 ÷ 4", "10 ÷ 2", "20 ÷ 2", "сокращение"),
    ("18 ÷ 6", "9 ÷ 3", "18 ÷ 3", "сокращение"),
)

# ЗАКОН, ПО КОТОРОМУ ПЕРЕПИСЬ ЗАКОННА, — по одному на род переписи и язык
ЗАКОНЫ = {
    "ru": {
        "удвоение": "сложить число с собой значит взять его дважды",
        "утроение": "сложить число трижды значит взять его трижды",
        "перестановка": "порядок множителей не меняет произведения",
        "сокращение": "разделить делимое и делитель на одно число значит не изменить частного",
    },
    "en": {
        "удвоение": "adding a number to itself is taking it twice",
        "утроение": "adding a number three times is taking it three times",
        "перестановка": "the order of factors does not change the product",
        "сокращение": "dividing both the dividend and the divisor by one number does not change the quotient",
    },
    "de": {
        "удвоение": "eine Zahl zu sich selbst zu addieren heißt sie zweimal zu nehmen",
        "утроение": "eine Zahl dreimal zu addieren heißt sie dreimal zu nehmen",
        "перестановка": "die Reihenfolge der Faktoren ändert das Produkt nicht",
        "сокращение": "Dividend und Divisor durch dieselbe Zahl zu teilen ändert den Quotienten nicht",
    },
    "fr": {
        "удвоение": "ajouter un nombre à lui-même, c'est le prendre deux fois",
        "утроение": "ajouter un nombre trois fois, c'est le prendre trois fois",
        "перестановка": "l'ordre des facteurs ne change pas le produit",
        "сокращение": "diviser le dividende et le diviseur par un même nombre ne change pas le quotient",
    },
    "es": {
        "удвоение": "sumar un número consigo mismo es tomarlo dos veces",
        "утроение": "sumar un número tres veces es tomarlo tres veces",
        "перестановка": "el orden de los factores no cambia el producto",
        "сокращение": "dividir el dividendo y el divisor por un mismo número no cambia el cociente",
    },
    "it": {
        "удвоение": "sommare un numero a sé stesso significa prenderlo due volte",
        "утроение": "sommare un numero tre volte significa prenderlo tre volte",
        "перестановка": "l'ordine dei fattori non cambia il prodotto",
        "сокращение": "dividere il dividendo e il divisore per uno stesso numero non cambia il quoziente",
    },
    "pt": {
        "удвоение": "somar um número a si mesmo é tomá-lo duas vezes",
        "утроение": "somar um número três vezes é tomá-lo três vezes",
        "перестановка": "a ordem dos fatores não altera o produto",
        "сокращение": "dividir o dividendo e o divisor pelo mesmo número não altera o quociente",
    },
    "nl": {
        "удвоение": "een getal bij zichzelf optellen is het tweemaal nemen",
        "утроение": "een getal driemaal optellen is het driemaal nemen",
        "перестановка": "de volgorde van de factoren verandert het product niet",
        "сокращение": "het deeltal en de deler door hetzelfde getal delen verandert het quotiënt niet",
    },
    "pl": {
        "удвоение": "dodać liczbę do samej siebie znaczy wziąć ją dwa razy",
        "утроение": "dodać liczbę trzy razy znaczy wziąć ją trzy razy",
        "перестановка": "kolejność czynników nie zmienia iloczynu",
        "сокращение": "podzielić dzielną i dzielnik przez tę samą liczbę nie zmienia ilorazu",
    },
}



def значение(запись):
    """Значение записи. Знаки — те, что пишет корпус; ничего, кроме цифр и знаков."""
    т = запись.replace("−", "-").replace("×", "*").replace("÷", "/")
    return int(eval(т, {"__builtins__": {}}, {}))


# ЧИСЛА ПРОВЕРЯЮТСЯ ПРИ ВВОЗЕ: пара, чьи записи не равны, и ложная третья,
# которая случайно равна, не доживают до записи мира.
for _a, _b, _c, _з in ТРОЙКИ:
    assert значение(_a) == значение(_b), (_a, _b)
    assert значение(_c) != значение(_a), (_a, _c)
    for _яз in ЗАКОНЫ:
        assert _з in ЗАКОНЫ[_яз], (_яз, _з)

РАМКИ = {
    "ru": dict(воп="чем ещё можно записать {a}? {b}: {з}, и то и другое есть {v}.",
               нет="{a} и {c} — одно и то же? нет: {a} = {v}, а {c} = {w}."),
    "en": dict(воп="how else can {a} be written? {b}: {з}, and both are {v}.",
               нет="are {a} and {c} the same? no: {a} = {v}, and {c} = {w}."),
    "de": dict(воп="wie kann man {a} noch schreiben? {b}: {з}, und beides ist {v}.",
               нет="sind {a} und {c} dasselbe? nein: {a} = {v}, und {c} = {w}."),
    "fr": dict(воп="comment écrire {a} autrement ? {b} : {з}, et les deux font {v}.",
               нет="{a} et {c} sont-ils la même chose ? non : {a} = {v}, et {c} = {w}."),
    "es": dict(воп="¿cómo se puede escribir {a} de otra manera? {b}: {з}, y ambos son {v}.",
               нет="¿son {a} y {c} lo mismo? no: {a} = {v}, y {c} = {w}."),
    "it": dict(воп="come si può scrivere {a} in un altro modo? {b}: {з}, ed entrambi sono {v}.",
               нет="{a} e {c} sono la stessa cosa? no: {a} = {v}, e {c} = {w}."),
    "pt": dict(воп="como se pode escrever {a} de outra maneira? {b}: {з}, e ambos são {v}.",
               нет="{a} e {c} são a mesma coisa? não: {a} = {v}, e {c} = {w}."),
    "nl": dict(воп="hoe kan {a} nog geschreven worden? {b}: {з}, en beide zijn {v}.",
               нет="zijn {a} en {c} hetzelfde? nee: {a} = {v}, en {c} = {w}."),
    "pl": dict(воп="jak jeszcze można zapisać {a}? {b}: {з}, i oba są {v}.",
               нет="czy {a} i {c} to to samo? nie: {a} = {v}, a {c} = {w}."),
}

ЯЗЫКИ = tuple(РАМКИ)
ФОРМЫ = ("воп", "нет")


def страница(язык, форма, i):
    a, b, c, з = ТРОЙКИ[i % len(ТРОЙКИ)]
    return РАМКИ[язык][форма].format(a=a, b=b, c=c, v=значение(a), w=значение(c),
                                     з=ЗАКОНЫ[язык][з])


def _показы():
    return {страница(язык, форма, i): (язык, форма)
            for язык in ЯЗЫКИ for форма in ФОРМЫ for i in range(len(ТРОЙКИ))}


ПОКАЗЫ = _показы()


def main():
    поймано = 0
    for язык in ЯЗЫКИ:
        print(f"  {язык}: {страница(язык, 'воп', 0)}")
        a, b, c, з = ТРОЙКИ[0]
        # МУТАНТЫ: вторая запись чужая; значение подменено; отказ с равными значениями
        зк = ЗАКОНЫ[язык][з]
        мутанты = (РАМКИ[язык]["воп"].format(a=a, b=c, c=c, v=значение(a), w=значение(c), з=зк),
                   РАМКИ[язык]["воп"].format(a=a, b=b, c=c, v=значение(a) + 1, w=значение(c), з=зк),
                   РАМКИ[язык]["нет"].format(a=a, b=b, c=b, v=значение(a), w=значение(a), з=зк))
        for м in мутанты:
            поймано += 0 if м in ПОКАЗЫ else 1
    print(f"  мутантов вне показов: {поймано} из {3 * len(ЯЗЫКИ)}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, троек {len(ТРОЙКИ)}, форм {len(ФОРМЫ)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
