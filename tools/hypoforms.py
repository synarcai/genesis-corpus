#!/usr/bin/env python3
"""ДОМ ПРОВЕРКИ ГИПОТЕЗЫ — и ГЛАВНАЯ АСИММЕТРИЯ знания.

Дом поспешности показал, что случаи не доказывают. Дом строгого вывода показал
верные и неверные ходы. Ни один не показал САМОГО ДЕЙСТВИЯ: выдвинуть догадку,
выбрать проверку, провести её и назвать итог — и назвать его ПО-РАЗНОМУ в двух
исходах, ибо исходы эти НЕ РАВНОСИЛЬНЫ.

    я думаю, что всякое число, делящееся на 6, делится на 3. как это проверить?
        проверю на 18:
        18 делится на 6 и делится на 3. пока сходится — но одна проверка не
        доказывает.

    я думаю, что всякое число, делящееся на 3, делится на 6. как это проверить?
        проверю на 9:
        9 делится на 3, но не делится на 6. значит нет — одной проверки
        довольно, чтобы отвергнуть.

ЭТО И ЕСТЬ ВЕСЬ ДОМ. Сошедшаяся проверка даёт «ПОКА СХОДИТСЯ», и никогда «значит
да»; несошедшаяся даёт «ЗНАЧИТ НЕТ» сразу. Асимметрия названа в самом показе, а
не оставлена читателю: организм, выучивший её, не объявит правилом то, что
сошлось трижды, и не станет искать четвёртой проверки тому, что уже отвергнуто.

ГИПОТЕЗЫ ВЗЯТЫ ПАРАМИ И ВЗАИМНО ОБРАЩЁННЫМИ: «делится на 6 → делится на 3»
держится, «делится на 3 → делится на 6» падает. Так один и тот же вид догадки
даёт оба исхода, и разница между ними не в форме слов, а в ДЕЛЕ.

ВОПРОС «КАК ЭТО ПРОВЕРИТЬ?» СТОИТ МЕЖДУ ДОГАДКОЙ И ПРОВЕРКОЙ, и он не украшение:
без него показ был бы родом БЕЗ ВОПРОСНОЙ ПОВЕРХНОСТИ (прибор ШИРОТЫ поднял долг
1109 → 1128 на первой волне), а полярное «верно ли, что…?» потребовало бы «да» или
«нет» первым словом — то есть ровно того ответа, какого проверка ещё не дала.
Невопросительно-полярная голова спрашивает о СПОСОБЕ, и ответом ей стоит весь ход
проверки. Тот же ход, что у дома строгого вывода, и куплен он теми же двумя
отказами судов.

Свидетель выбирается наименьшим годным и вычисляется, а не объявляется.

    python3 tools/hypoforms.py    # самопроверка с мутантами
"""
# пары делителей: (больший, меньший) — «делится на больший ⇒ делится на меньший»
# держится всегда; обращение падает, и свидетель обращения вычисляется
ПАРЫ = ((6, 3), (4, 2), (10, 5), (9, 3), (8, 4), (15, 5), (12, 6), (14, 7))


def свидетель_держится(a, b):
    """Наименьшее число, делящееся на больший делитель (и потому на меньший)."""
    n = a
    while n % a or n % b:
        n += a
    return n


def свидетель_падает(a, b):
    """Наименьшее число, делящееся на МЕНЬШИЙ и не делящееся на больший."""
    n = b
    while n % b or n % a == 0:
        n += b
    return n


for _a, _b in ПАРЫ:
    assert _a % _b == 0 and _a != _b, (_a, _b)
    _д = свидетель_держится(_a, _b)
    assert _д % _a == 0 and _д % _b == 0, (_a, _b, _д)
    _п = свидетель_падает(_a, _b)
    assert _п % _b == 0 and _п % _a != 0, (_a, _b, _п)

РАМКИ = {
    "ru": dict(держится="я думаю, что всякое число, делящееся на {a}, делится на {b}. как это проверить? проверю на {n}: "
                        "{n} делится на {a} и делится на {b}. пока сходится — но одна проверка не доказывает.",
               падает="я думаю, что всякое число, делящееся на {b}, делится на {a}. как это проверить? проверю на {m}: "
                      "{m} делится на {b}, но не делится на {a}. значит нет — одной проверки довольно, чтобы отвергнуть."),
    "en": dict(держится="i think every number divisible by {a} is divisible by {b}. how can that be tested? i will test {n}: "
                        "{n} is divisible by {a} and divisible by {b}. it holds so far — but one test does not prove it.",
               падает="i think every number divisible by {b} is divisible by {a}. how can that be tested? i will test {m}: "
                      "{m} is divisible by {b} but not divisible by {a}. so no — one test is enough to reject it."),
    "de": dict(держится="ich denke, jede durch {a} teilbare Zahl ist durch {b} teilbar. wie lässt sich das prüfen? ich prüfe {n}: "
                        "{n} ist durch {a} teilbar und durch {b} teilbar. es hält bisher — aber eine Prüfung beweist es nicht.",
               падает="ich denke, jede durch {b} teilbare Zahl ist durch {a} teilbar. wie lässt sich das prüfen? ich prüfe {m}: "
                      "{m} ist durch {b} teilbar, aber nicht durch {a} teilbar. also nein — eine Prüfung genügt zur Ablehnung."),
    "fr": dict(держится="je pense que tout nombre divisible par {a} est divisible par {b}. comment le vérifier ? je teste {n} : "
                        "{n} est divisible par {a} et divisible par {b}. cela tient pour l'instant — mais un test ne le prouve pas.",
               падает="je pense que tout nombre divisible par {b} est divisible par {a}. comment le vérifier ? je teste {m} : "
                      "{m} est divisible par {b} mais pas divisible par {a}. donc non — un seul test suffit pour rejeter."),
    "es": dict(держится="creo que todo número divisible por {a} es divisible por {b}. ¿cómo se puede comprobar? voy a probar {n}: "
                        "{n} es divisible por {a} y divisible por {b}. se sostiene por ahora, pero una prueba no lo demuestra.",
               падает="creo que todo número divisible por {b} es divisible por {a}. ¿cómo se puede comprobar? voy a probar {m}: "
                      "{m} es divisible por {b} pero no divisible por {a}. entonces no: una sola prueba basta para rechazarlo."),
    "it": dict(держится="penso che ogni numero divisibile per {a} sia divisibile per {b}. come si può verificarlo? provo {n}: "
                        "{n} è divisibile per {a} ed è divisibile per {b}. per ora regge, ma una prova non lo dimostra.",
               падает="penso che ogni numero divisibile per {b} sia divisibile per {a}. come si può verificarlo? provo {m}: "
                      "{m} è divisibile per {b} ma non è divisibile per {a}. quindi no: una sola prova basta per respingerlo."),
    "pt": dict(держится="penso que todo número divisível por {a} é divisível por {b}. como se pode verificar? vou testar {n}: "
                        "{n} é divisível por {a} e é divisível por {b}. por agora aguenta, mas um teste não o prova.",
               падает="penso que todo número divisível por {b} é divisível por {a}. como se pode verificar? vou testar {m}: "
                      "{m} é divisível por {b} mas não é divisível por {a}. então não: um só teste basta para o rejeitar."),
    "nl": dict(держится="ik denk dat elk getal deelbaar door {a} deelbaar is door {b}. hoe kan dat getest worden? ik test {n}: "
                        "{n} is deelbaar door {a} en deelbaar door {b}. het houdt voorlopig — maar één test bewijst het niet.",
               падает="ik denk dat elk getal deelbaar door {b} deelbaar is door {a}. hoe kan dat getest worden? ik test {m}: "
                      "{m} is deelbaar door {b} maar niet deelbaar door {a}. dus nee — één test is genoeg om het te verwerpen."),
    "pl": dict(держится="myślę, że każda liczba dzieląca się przez {a} dzieli się przez {b}. jak to sprawdzić? sprawdzę {n}: "
                        "{n} dzieli się przez {a} i dzieli się przez {b}. na razie się trzyma, ale jedna próba tego nie dowodzi.",
               падает="myślę, że każda liczba dzieląca się przez {b} dzieli się przez {a}. jak to sprawdzić? sprawdzę {m}: "
                      "{m} dzieli się przez {b}, ale nie dzieli się przez {a}. więc nie: jedna próba wystarczy, by to odrzucić."),
}

ЯЗЫКИ = tuple(РАМКИ)
ФОРМЫ = ("держится", "падает")


def страница(язык, форма, i):
    a, b = ПАРЫ[i % len(ПАРЫ)]
    if форма == "держится":
        return РАМКИ[язык]["держится"].format(a=a, b=b, n=свидетель_держится(a, b))
    return РАМКИ[язык]["падает"].format(a=a, b=b, m=свидетель_падает(a, b))


def _показы():
    return {страница(язык, форма, i): (язык, форма)
            for язык in ЯЗЫКИ for форма in ФОРМЫ for i in range(len(ПАРЫ))}


ПОКАЗЫ = _показы()


def main():
    поймано = 0
    for язык in ЯЗЫКИ:
        print(f"  {язык}: {страница(язык, 'падает', 0)}")
        a, b = ПАРЫ[0]
        # МУТАНТЫ: свидетель, не делящийся на больший; свидетель падения,
        # делящийся на больший (то есть отвергающий верное); обращённая пара
        мутанты = (РАМКИ[язык]["держится"].format(a=a, b=b, n=свидетель_падает(a, b)),
                   РАМКИ[язык]["падает"].format(a=a, b=b, m=свидетель_держится(a, b)),
                   РАМКИ[язык]["держится"].format(a=b, b=a, n=свидетель_держится(a, b)))
        for м in мутанты:
            поймано += 0 if м in ПОКАЗЫ else 1
    print(f"  мутантов вне показов: {поймано} из {3 * len(ЯЗЫКИ)}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, пар {len(ПАРЫ)}, форм {len(ФОРМЫ)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
