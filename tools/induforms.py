#!/usr/bin/env python3
"""ДОМ ПОСПЕШНОСТИ — обобщение из случаев и НАЗВАННЫЙ ПРЕДЕЛ этого хода.

Третий из четырёх долгов карты форм рассуждения, и назван он там как самый
опасный: «корпус показывает закон и его случай, но никогда — ход ОТ случаев К
закону вместе с оговоркой о его ненадёжности. Это форма, которой особенно
легко научить неверно.»

Учить ей верно можно ровно одним способом: показать ОБА исхода одного и того
же хода — и когда случаи обманули, и когда не обманули, — и во втором случае
сказать вслух, что доказали не они.

  ПОСПЕШНОСТЬ  0² + 0 + 41 = 41 — простое. 1² + 1 + 41 = 43 — простое.
               2² + 2 + 41 = 47 — простое. 3² + 3 + 41 = 53 — простое.
               значит ли, что n² + n + 41 просто при всяком n?
               нет: при n = 40 выходит 1681, а 1681 = 41 × 41.

  ОСНОВАНИЕ    1 = 1 × 1. 1 + 3 = 2 × 2. 1 + 3 + 5 = 3 × 3. 1 + 3 + 5 + 7 = 4 × 4.
               значит ли, что сумма первых n нечётных чисел равна n × n?
               четыре случая этого не доказывают, но это верно: каждое
               следующее нечётное число достраивает квадрат n × n до квадрата
               (n + 1) × (n + 1).

ВТОРАЯ ФОРМА ВАЖНЕЕ ПЕРВОЙ, и без неё первая учила бы недоверию к любому
обобщению. Первая учит, что случаи не довод; вторая — что довод есть причина,
а не число сошедшихся случаев. Вместе они дают то различение, ради которого
дом и стоит: СВИДЕТЕЛЬСТВО НЕ ЕСТЬ ДОКАЗАТЕЛЬСТВО, а доказательство не есть
множество свидетельств.

ЧИСЛА НЕ ОБЪЯВЛЕНЫ, А ВЫЧИСЛЕНЫ, включая контрпример и его разложение: дом,
объявивший «1681 = 41 × 41» рукой, был бы домом веры. Суд пересчитывает всё —
и случаи, и простоту, и разложение (courts/indu_court.py).

ПЯТЬ ЯЗЫКОВ — названный долг, тот же, что у дома фактов мира: обобщение и его
предел суть предложения, которые надо НАПИСАТЬ верно, а не перевести на глаз.

    python3 tools/induforms.py    # самопроверка с мутантами
"""


def просто(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def _делитель(n):
    d = 2
    while d * d <= n:
        if n % d == 0:
            return d
        d += 1
    return n


def _факториал(n):
    ф = 1
    for i in range(2, n + 1):
        ф *= i
    return ф + 1


def _эйлер(n):
    return n * n + n + 41


def _мерсенн(n):
    return 2 ** n - 1


# РЯДЫ. «вид» говорит, чем читается случай: простотой числа или равенством.
# Значения вычисляются здесь же — ни одно число ряда не написано рукой.
РЯДЫ = (
    dict(имя="эйлер", вид="простое", ключ="n", случаи=(0, 1, 2, 3),
         выражение=lambda n: f"{n}² + {n} + 41", значение=_эйлер, контрпример=40),
    dict(имя="мерсенн", вид="простое", ключ="n", случаи=(2, 3, 5, 7),
         выражение=lambda n: f"2^{n} − 1", значение=_мерсенн, контрпример=11),
    dict(имя="нечётные", вид="равенство", ключ="n", случаи=(1, 2, 3, 4),
         левое=lambda n: " + ".join(str(2 * i - 1) for i in range(1, n + 1)),
         правое=lambda n: f"{n} × {n}", значение=lambda n: n * n, держится=True),
    dict(имя="ряд", вид="равенство", ключ="n", случаи=(1, 2, 3, 4),
         левое=lambda n: " + ".join(str(i) for i in range(1, n + 1)),
         правое=lambda n: f"{n} × {n + 1} ÷ 2", значение=lambda n: n * (n + 1) // 2, держится=True),
    dict(имя="факториал", вид="простое", ключ="n", случаи=(1, 2, 3),
         выражение=lambda n: f"{n}! + 1", значение=_факториал, контрпример=4),
    dict(имя="кубы", вид="равенство", ключ="n", случаи=(1, 2, 3, 4),
         левое=lambda n: " + ".join(str(i ** 3) for i in range(1, n + 1)),
         правое=lambda n: f"{n * (n + 1) // 2} × {n * (n + 1) // 2}",
         значение=lambda n: (n * (n + 1) // 2) ** 2, держится=True),
    # ГОЛОЕ ЧИСЛО — свой вид: «3 — простое.» без «3 = 3», и опровержение без
    # переменной («9 не просто, ибо 9 = 3 × 3»), ибо переменной здесь нет.
    # Пример самый известный и самый наглядный, и ради него объявлены две
    # лишние рамки на язык — дешевле, чем писать его неверно.
    dict(имя="нечётные_простые", вид="голое", случаи=(3, 5, 7),
         значение=lambda n: n, контрпример=9),
)

# УТВЕРЖДЕНИЕ И ПРИЧИНА — по одному на ряд и язык; больше в доме слов нет.
СЛОВА = {
    "ru": dict(простое="{в} = {з} — простое.", равенство="{л} = {п}.",
               голое="{з} — простое.", нет_голое="нет: {з} не просто, ибо {з} = {a} × {b}.",
               вопрос="значит ли, что {у}?", нет="нет: при {к} = {x} выходит {з}, а {з} = {a} × {b}.",
               да="{c} случая этого не доказывают, но это верно: {п}.",
               утверждения=("n² + n + 41 просто при всяком n",
                            "2^n − 1 просто при всяком простом n",
                            "сумма первых n нечётных чисел равна n × n",
                            "сумма первых n чисел равна n × (n + 1) ÷ 2",
                            "n! + 1 просто при всяком n",
                            "сумма первых n кубов равна квадрату суммы первых n чисел",
                            "всякое нечётное число больше 1 просто"),
               причины=("каждое следующее нечётное число достраивает квадрат n × n до квадрата (n + 1) × (n + 1)",
                        "сложив ряд с ним же, записанным наоборот, получим n пар, и в каждой паре n + 1",
                        "прибавление куба n + 1 достраивает квадрат суммы до квадрата следующей суммы")),
    "en": dict(простое="{в} = {з} is prime.", равенство="{л} = {п}.",
               голое="{з} is prime.", нет_голое="no: {з} is not prime, since {з} = {a} × {b}.",
               вопрос="does it follow that {у}?", нет="no: at {к} = {x} it gives {з}, and {з} = {a} × {b}.",
               да="{c} cases do not prove it, but it is true: {п}.",
               утверждения=("n² + n + 41 is prime for every n",
                            "2^n − 1 is prime for every prime n",
                            "the sum of the first n odd numbers is n × n",
                            "the sum of the first n numbers is n × (n + 1) ÷ 2",
                            "n! + 1 is prime for every n",
                            "the sum of the first n cubes is the square of the sum of the first n numbers",
                            "every odd number greater than 1 is prime"),
               причины=("each next odd number completes the square n × n into the square (n + 1) × (n + 1)",
                        "adding the row to itself written backwards gives n pairs, and each pair is n + 1",
                        "adding the cube of n + 1 completes the square of the sum into the square of the next sum")),
    "de": dict(простое="{в} = {з} ist eine Primzahl.", равенство="{л} = {п}.",
               голое="{з} ist eine Primzahl.", нет_голое="nein: {з} ist keine Primzahl, denn {з} = {a} × {b}.",
               вопрос="folgt daraus, dass {у}?", нет="nein: bei {к} = {x} kommt {з} heraus, und {з} = {a} × {b}.",
               да="{c} Fälle beweisen es nicht, aber es stimmt: {п}.",
               утверждения=("n² + n + 41 für jedes n eine Primzahl ist",
                            "2^n − 1 für jede Primzahl n eine Primzahl ist",
                            "die Summe der ersten n ungeraden Zahlen n × n ist",
                            "die Summe der ersten n Zahlen n × (n + 1) ÷ 2 ist",
                            "n! + 1 für jedes n eine Primzahl ist",
                            "die Summe der ersten n Kuben das Quadrat der Summe der ersten n Zahlen ist",
                            "jede ungerade Zahl größer als 1 eine Primzahl ist"),
               причины=("jede nächste ungerade Zahl das Quadrat n × n zum Quadrat (n + 1) × (n + 1) ergänzt",
                        "die Reihe zu sich selbst rückwärts addiert n Paare gibt, und jedes Paar ist n + 1",
                        "das Hinzufügen des Kubus von n + 1 das Quadrat der Summe zum Quadrat der nächsten Summe ergänzt")),
    "fr": dict(простое="{в} = {з} est premier.", равенство="{л} = {п}.",
               голое="{з} est premier.", нет_голое="non : {з} n'est pas premier, car {з} = {a} × {b}.",
               вопрос="en découle-t-il que {у} ?", нет="non : à {к} = {x} on obtient {з}, et {з} = {a} × {b}.",
               да="{c} cas ne le prouvent pas, mais c'est vrai : {п}.",
               утверждения=("n² + n + 41 est premier pour tout n",
                            "2^n − 1 est premier pour tout n premier",
                            "la somme des n premiers nombres impairs vaut n × n",
                            "la somme des n premiers nombres vaut n × (n + 1) ÷ 2",
                            "n! + 1 est premier pour tout n",
                            "la somme des n premiers cubes vaut le carré de la somme des n premiers nombres",
                            "tout nombre impair supérieur à 1 est premier"),
               причины=("chaque nombre impair suivant complète le carré n × n en le carré (n + 1) × (n + 1)",
                        "en ajoutant la suite à elle-même écrite à l'envers on obtient n paires, et chaque paire vaut n + 1",
                        "ajouter le cube de n + 1 complète le carré de la somme en le carré de la somme suivante")),
    "es": dict(простое="{в} = {з} es primo.", равенство="{л} = {п}.",
               голое="{з} es primo.", нет_голое="no: {з} no es primo, pues {з} = {a} × {b}.",
               вопрос="¿se sigue que {у}?", нет="no: en {к} = {x} sale {з}, y {з} = {a} × {b}.",
               да="{c} casos no lo demuestran, pero es cierto: {п}.",
               утверждения=("n² + n + 41 es primo para todo n",
                            "2^n − 1 es primo para todo n primo",
                            "la suma de los primeros n números impares es n × n",
                            "la suma de los primeros n números es n × (n + 1) ÷ 2",
                            "n! + 1 es primo para todo n",
                            "la suma de los primeros n cubos es el cuadrado de la suma de los primeros n números",
                            "todo número impar mayor que 1 es primo"),
               причины=("cada número impar siguiente completa el cuadrado n × n hasta el cuadrado (n + 1) × (n + 1)",
                        "sumando la serie consigo misma escrita al revés se obtienen n pares, y cada par vale n + 1",
                        "añadir el cubo de n + 1 completa el cuadrado de la suma hasta el cuadrado de la suma siguiente")),
}

ЯЗЫКИ = tuple(СЛОВА)
ФОРМЫ = ("случаи", "исход")

# ЧИСЛА ПРОВЕРЯЮТСЯ ПРИ ВВОЗЕ: ряд, объявивший простым составное, не доживает
# до записи мира, а контрпример, оказавшийся простым, не доживает тем более.
for _р in РЯДЫ:
    if _р["вид"] in ("простое", "голое"):
        assert all(просто(_р["значение"](n)) for n in _р["случаи"]), _р["имя"]
        _к = _р["значение"](_р["контрпример"])
        assert not просто(_к), (_р["имя"], _к)
    else:
        assert _р.get("держится"), _р["имя"]
for _яз, _с in СЛОВА.items():
    assert len(_с["утверждения"]) == len(РЯДЫ), _яз
    assert len(_с["причины"]) == sum(1 for _р in РЯДЫ if _р.get("держится")), _яз


def _случаи(язык, ряд):
    с = СЛОВА[язык]
    вон = []
    for n in ряд["случаи"]:
        if ряд["вид"] == "голое":
            вон.append(с["голое"].format(з=ряд["значение"](n)))
        elif ряд["вид"] == "простое":
            вон.append(с["простое"].format(в=ряд["выражение"](n), з=ряд["значение"](n)))
        else:
            вон.append(с["равенство"].format(л=ряд["левое"](n), п=ряд["правое"](n)))
    return " ".join(вон)


def страница(язык, форма, i):
    ряд = РЯДЫ[i % len(РЯДЫ)]
    с = СЛОВА[язык]
    случаи = _случаи(язык, ряд)
    if форма == "случаи":
        return случаи
    вопрос = с["вопрос"].format(у=с["утверждения"][i % len(РЯДЫ)])
    if ряд.get("держится"):
        держащиеся = [р["имя"] for р in РЯДЫ if р.get("держится")]
        причина = с["причины"][держащиеся.index(ряд["имя"])]
        исход = с["да"].format(c=len(ряд["случаи"]), п=причина)
    else:
        x = ряд["контрпример"]
        з = ряд["значение"](x)
        a = _делитель(з)
        исход = (с["нет_голое"].format(з=з, a=a, b=з // a) if ряд["вид"] == "голое"
                 else с["нет"].format(к=ряд["ключ"], x=x, з=з, a=a, b=з // a))
    return f"{случаи} {вопрос} {исход}"


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for форма in ФОРМЫ:
            for i in range(len(РЯДЫ)):
                вон[страница(язык, форма, i)] = (язык, форма)
    return вон


ПОКАЗЫ = _показы()


def main():
    поймано = 0
    for язык in ЯЗЫКИ:
        print(f"  {язык}: {страница(язык, 'исход', 0)[:120]}")
        с = СЛОВА[язык]
        мутант = страница(язык, "исход", 0).replace(" = 41 × 41.", " = 40 × 42.")
        поймано += 0 if мутант in ПОКАЗЫ else 1
    print(f"  мутантов вне показов: {поймано} из {len(ЯЗЫКИ)}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, рядов {len(РЯДЫ)}, форм {len(ФОРМЫ)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
