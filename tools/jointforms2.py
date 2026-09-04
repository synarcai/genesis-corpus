#!/usr/bin/env python3
"""ДОМ СОВМЕСТНОГО СЧЁТА — «у меня», «у тебя», «у нас».

Вся арифметика корпуса до сих пор шла О ТРЕТЬИХ ЛИЦАХ: «у Анны 7 шаров, у Вани
4 шара». Замер по своду: «у меня» 141 строка, «у нас» 10, «У ТЕБЯ» — НОЛЬ.
Организм, умеющий считать только чужое, не может сложить своё с тем, что назвал
собеседник, — а это первое, чего требует разговор о деле.

    у меня 7 яблок, у тебя 4 яблока. сколько у нас вместе? 11 яблок: 7 + 4 = 11.
    у меня 7 яблок, у тебя 4 яблока. на сколько у меня больше? на 3: 7 − 4 = 3.
    у меня 6 яблок, у тебя 6 яблок. у кого больше? ни у кого: 6 − 6 = 0, поровну.

ТРЕТЬЯ ФОРМА НЕ УКРАШЕНИЕ. Две первые учат складывать и вычитать названное
двумя лицами; третья учит, что РАЗНИЦЫ МОЖЕТ НЕ БЫТЬ, — и без неё организм,
спрошенный «у кого больше», будет всегда называть кого-то.

ПОРТУГАЛЬСКИЙ ОТВЕТ ПЕРЕСТРОЕН ПО ОТКАЗУ СУДА ФОРМУЛ, и отказ был по делу:
«{d} a mais: {a} − {b} = {d}» есть рамка вида «имя: формула», и суд формул
прочёл «3 a mais» ИМЕНЕМ формулы, а формулу — её телом. Двоеточие после числа
есть чужой знак, и корпус не вправе ставить его там, где сосед читает
объявление. «A diferença é 3: 7 − 4 = 3» той рамки не образует.

ФОРМА ВЕЩИ ПРИ ЧИСЛЕ БЕРЁТСЯ У ДОМА ПРИРОДЫ (`natureforms.вещь`), который для
славянских языков зовёт свои дома счёта, а для прочих — объявленную пару
«один / много». Ни одна форма здесь не угадывается.

    python3 tools/jointforms2.py    # самопроверка с мутантами
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import natureforms as N  # noqa: E402

# (больше, меньше) — пары, где первое строго больше второго; и одна равная
ПАРЫ = ((7, 4), (12, 8), (9, 6), (20, 15), (5, 3), (11, 2))
РАВНЫЕ = (6, 9, 14)

ВЕЩИ = {
    "ru": ("яблоко", "книга", "шар", "монета"),
    "pl": ("jabłko", "książka", "piłka", "moneta"),
    "en": (("apple", "apples"), ("book", "books"), ("ball", "balls"), ("coin", "coins")),
    "de": (("Apfel", "Äpfel"), ("Buch", "Bücher"), ("Ball", "Bälle"), ("Münze", "Münzen")),
    "fr": (("pomme", "pommes"), ("livre", "livres"), ("balle", "balles"), ("pièce", "pièces")),
    "es": (("manzana", "manzanas"), ("libro", "libros"), ("pelota", "pelotas"), ("moneda", "monedas")),
    "it": (("mela", "mele"), ("libro", "libri"), ("palla", "palle"), ("moneta", "monete")),
    "pt": (("maçã", "maçãs"), ("livro", "livros"), ("bola", "bolas"), ("moeda", "moedas")),
    "nl": (("appel", "appels"), ("boek", "boeken"), ("bal", "ballen"), ("munt", "munten")),
}

РАМКИ = {
    "ru": dict(вместе="у меня {a} {ва}, у тебя {b} {вб}. сколько у нас вместе? {c} {вс}: {a} + {b} = {c}.",
               разница="у меня {a} {ва}, у тебя {b} {вб}. на сколько у меня больше? на {d}: {a} − {b} = {d}.",
               поровну="у меня {a} {ва}, у тебя {a} {ва}. у кого больше? ни у кого: {a} − {a} = 0, поровну."),
    "en": dict(вместе="i have {a} {ва}, you have {b} {вб}. how many do we have together? {c} {вс}: {a} + {b} = {c}.",
               разница="i have {a} {ва}, you have {b} {вб}. how many more do i have? {d} more: {a} − {b} = {d}.",
               поровну="i have {a} {ва}, you have {a} {ва}. who has more? neither: {a} − {a} = 0, equally many."),
    "de": dict(вместе="ich habe {a} {ва}, du hast {b} {вб}. wie viele haben wir zusammen? {c} {вс}: {a} + {b} = {c}.",
               разница="ich habe {a} {ва}, du hast {b} {вб}. wie viele habe ich mehr? {d} mehr: {a} − {b} = {d}.",
               поровну="ich habe {a} {ва}, du hast {a} {ва}. wer hat mehr? niemand: {a} − {a} = 0, gleich viele."),
    "fr": dict(вместе="j'ai {a} {ва}, tu as {b} {вб}. combien avons-nous ensemble ? {c} {вс} : {a} + {b} = {c}.",
               разница="j'ai {a} {ва}, tu as {b} {вб}. combien en ai-je de plus ? {d} de plus : {a} − {b} = {d}.",
               поровну="j'ai {a} {ва}, tu as {a} {ва}. qui en a plus ? personne : {a} − {a} = 0, autant l'un que l'autre."),
    "es": dict(вместе="yo tengo {a} {ва}, tú tienes {b} {вб}. ¿cuántas tenemos juntos? {c} {вс}: {a} + {b} = {c}.",
               разница="yo tengo {a} {ва}, tú tienes {b} {вб}. ¿cuántas tengo yo de más? {d} de más: {a} − {b} = {d}.",
               поровну="yo tengo {a} {ва}, tú tienes {a} {ва}. ¿quién tiene más? nadie: {a} − {a} = 0, por igual."),
    "it": dict(вместе="io ho {a} {ва}, tu hai {b} {вб}. quante ne abbiamo insieme? {c} {вс}: {a} + {b} = {c}.",
               разница="io ho {a} {ва}, tu hai {b} {вб}. quante ne ho in più? {d} in più: {a} − {b} = {d}.",
               поровну="io ho {a} {ва}, tu hai {a} {ва}. chi ne ha di più? nessuno: {a} − {a} = 0, in parti uguali."),
    "pt": dict(вместе="eu tenho {a} {ва}, tu tens {b} {вб}. quantas temos juntos? {c} {вс}: {a} + {b} = {c}.",
               разница="eu tenho {a} {ва}, tu tens {b} {вб}. quantas tenho eu a mais? a diferença é {d}: {a} − {b} = {d}.",
               поровну="eu tenho {a} {ва}, tu tens {a} {ва}. quem tem mais? ninguém: {a} − {a} = 0, por igual."),
    "nl": dict(вместе="ik heb {a} {ва}, jij hebt {b} {вб}. hoeveel hebben wij samen? {c} {вс}: {a} + {b} = {c}.",
               разница="ik heb {a} {ва}, jij hebt {b} {вб}. hoeveel heb ik er meer? {d} meer: {a} − {b} = {d}.",
               поровну="ik heb {a} {ва}, jij hebt {a} {ва}. wie heeft er meer? niemand: {a} − {a} = 0, evenveel."),
    "pl": dict(вместе="mam {a} {ва}, ty masz {b} {вб}. ile mamy razem? {c} {вс}: {a} + {b} = {c}.",
               разница="mam {a} {ва}, ty masz {b} {вб}. o ile mam więcej? o {d}: {a} − {b} = {d}.",
               поровну="mam {a} {ва}, ty masz {a} {ва}. kto ma więcej? nikt: {a} − {a} = 0, po równo."),
}


# ВЕЖЛИВЫЙ РЕГИСТР — второе лицо на «вы». Дом говорит собеседнику «у тебя», и
# потому обязан уметь сказать «у вас»: замер по своду нашёл ноль строк с «вы»
# при девяноста двух с «ты», а по-русски, по-немецки, по-французски,
# по-испански, по-итальянски и по-польски это не оттенок, а грубость.
# Английский различия не имеет и пишет одну форму (объявлено списком).
БЕЗ_РАЗЛИЧИЯ_РЕГИСТРА = frozenset({"en"})
# ОБЪЯВЛЕННЫЙ ПРОПУСК — см. tools/linkforms.py
ОБЪЯВЛЕННЫЕ_ПРОПУСКИ = {ф: БЕЗ_РАЗЛИЧИЯ_РЕГИСТРА
                        for ф in ("вместе_вы", "разница_вы", "поровну_вы")}
ВЕЖЛИВЫЕ = {
    "ru": dict(
        вместе="у меня {a} {ва}, у вас {b} {вб}. сколько у нас вместе? {c} {вс}: {a} + {b} = {c}.",
        разница="у меня {a} {ва}, у вас {b} {вб}. на сколько у меня больше? на {d}: {a} − {b} = {d}.",
        поровну="у меня {a} {ва}, у вас {a} {ва}. у кого больше? ни у кого: {a} − {a} = 0, поровну.",
    ),
    "de": dict(
        вместе="ich habe {a} {ва}, Sie haben {b} {вб}. wie viele haben wir zusammen? {c} {вс}: {a} + {b} = {c}.",
        разница="ich habe {a} {ва}, Sie haben {b} {вб}. wie viele habe ich mehr? {d} mehr: {a} − {b} = {d}.",
        поровну="ich habe {a} {ва}, Sie haben {a} {ва}. wer hat mehr? niemand: {a} − {a} = 0, gleich viele.",
    ),
    "fr": dict(
        вместе="j'ai {a} {ва}, vous avez {b} {вб}. combien avons-nous ensemble ? {c} {вс} : {a} + {b} = {c}.",
        разница="j'ai {a} {ва}, vous avez {b} {вб}. combien en ai-je de plus ? {d} de plus : {a} − {b} = {d}.",
        поровну="j'ai {a} {ва}, vous avez {a} {ва}. qui en a plus ? personne : {a} − {a} = 0, autant l'un que l'autre.",
    ),
    "es": dict(
        вместе="yo tengo {a} {ва}, usted tiene {b} {вб}. ¿cuántas tenemos juntos? {c} {вс}: {a} + {b} = {c}.",
        разница="yo tengo {a} {ва}, usted tiene {b} {вб}. ¿cuántas tengo yo de más? {d} de más: {a} − {b} = {d}.",
        поровну="yo tengo {a} {ва}, usted tiene {a} {ва}. ¿quién tiene más? nadie: {a} − {a} = 0, por igual.",
    ),
    "it": dict(
        вместе="io ho {a} {ва}, Lei ha {b} {вб}. quante ne abbiamo insieme? {c} {вс}: {a} + {b} = {c}.",
        разница="io ho {a} {ва}, Lei ha {b} {вб}. quante ne ho in più? {d} in più: {a} − {b} = {d}.",
        поровну="io ho {a} {ва}, Lei ha {a} {ва}. chi ne ha di più? nessuno: {a} − {a} = 0, in parti uguali.",
    ),
    "pt": dict(
        вместе="eu tenho {a} {ва}, você tem {b} {вб}. quantas temos juntos? {c} {вс}: {a} + {b} = {c}.",
        разница="eu tenho {a} {ва}, você tem {b} {вб}. quantas tenho eu a mais? a diferença é {d}: {a} − {b} = {d}.",
        поровну="eu tenho {a} {ва}, você tem {a} {ва}. quem tem mais? ninguém: {a} − {a} = 0, por igual.",
    ),
    "nl": dict(
        вместе="ik heb {a} {ва}, u heeft {b} {вб}. hoeveel hebben wij samen? {c} {вс}: {a} + {b} = {c}.",
        разница="ik heb {a} {ва}, u heeft {b} {вб}. hoeveel heb ik er meer? {d} meer: {a} − {b} = {d}.",
        поровну="ik heb {a} {ва}, u heeft {a} {ва}. wie heeft er meer? niemand: {a} − {a} = 0, evenveel.",
    ),
    "pl": dict(
        вместе="mam {a} {ва}, pan ma {b} {вб}. ile mamy razem? {c} {вс}: {a} + {b} = {c}.",
        разница="mam {a} {ва}, pan ma {b} {вб}. o ile mam więcej? o {d}: {a} − {b} = {d}.",
        поровну="mam {a} {ва}, pan ma {a} {ва}. kto ma więcej? nikt: {a} − {a} = 0, po równo.",
    ),
}

ЯЗЫКИ = tuple(РАМКИ)
ФОРМЫ = ("вместе", "разница", "поровну", "вместе_вы", "разница_вы", "поровну_вы")

for _a, _b in ПАРЫ:
    assert _a > _b > 0, (_a, _b)
for _яз in ЯЗЫКИ:
    assert len(ВЕЩИ[_яз]) == len(ВЕЩИ["ru"]), _яз
    assert (_яз in БЕЗ_РАЗЛИЧИЯ_РЕГИСТРА) != (_яз in ВЕЖЛИВЫЕ), _яз


def страница(язык, форма, i):
    вещи = ВЕЩИ[язык]
    в = вещи[i % len(вещи)]
    рамки = ВЕЖЛИВЫЕ[язык] if форма.endswith("_вы") else РАМКИ[язык]
    ключ = форма[:-3] if форма.endswith("_вы") else форма
    if ключ == "поровну":
        a = РАВНЫЕ[i % len(РАВНЫЕ)]
        return рамки["поровну"].format(a=a, ва=N.вещь(язык, в, a))
    a, b = ПАРЫ[i % len(ПАРЫ)]
    поля = dict(a=a, b=b, ва=N.вещь(язык, в, a), вб=N.вещь(язык, в, b))
    if ключ == "вместе":
        c = a + b
        return рамки["вместе"].format(c=c, вс=N.вещь(язык, в, c), **поля)
    return рамки["разница"].format(d=a - b, **поля)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for форма in ФОРМЫ:
            if форма.endswith("_вы") and язык in БЕЗ_РАЗЛИЧИЯ_РЕГИСТРА:
                continue
            сколько = len(РАВНЫЕ) if форма.startswith("поровну") else len(ПАРЫ)
            for i in range(сколько):
                вон[страница(язык, форма, i)] = (язык, форма)
    return вон


ПОКАЗЫ = _показы()


def main():
    поймано = 0
    for язык in ЯЗЫКИ:
        print(f"  {язык}: {страница(язык, 'вместе', 0)}")
        вещи = ВЕЩИ[язык]
        a, b = ПАРЫ[0]
        в = вещи[0]
        # МУТАНТЫ: неверная сумма, неверная разница, «поровну» при разных числах
        мутанты = (РАМКИ[язык]["вместе"].format(a=a, b=b, c=a + b + 1, ва=N.вещь(язык, в, a),
                                                вб=N.вещь(язык, в, b), вс=N.вещь(язык, в, a + b + 1)),
                   РАМКИ[язык]["разница"].format(a=a, b=b, d=a - b + 1, ва=N.вещь(язык, в, a),
                                                 вб=N.вещь(язык, в, b)),
                   РАМКИ[язык]["вместе"].format(a=a, b=b, c=a - b, ва=N.вещь(язык, в, a),
                                                вб=N.вещь(язык, в, b), вс=N.вещь(язык, в, a - b)))
        for м in мутанты:
            поймано += 0 if м in ПОКАЗЫ else 1
    print(f"  мутантов вне показов: {поймано} из {3 * len(ЯЗЫКИ)}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, пар {len(ПАРЫ)}, "
          f"равных {len(РАВНЫЕ)}, вещей {len(ВЕЩИ['ru'])})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
