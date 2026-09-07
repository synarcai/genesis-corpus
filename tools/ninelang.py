#!/usr/bin/env python3
"""ДОМ ТРЁХ ФОРМ НА ДЕВЯТИ ЯЗЫКАХ — одно место, девять разных слов (07.09).

ЗАЧЕМ. Обзор 07.09 (Р-2) требует: роль принадлежит МЕСТУ, а не слову. Свидетельства этого
у корпуса не было ни одного: четыре конструкционных дома, писанные в этот день, ОДНОЯЗЫЧНЫ,
а покуда конструкция стои́т на одном языке, «место сцены» и «слово bus» для рынка
неразличимы — они всегда вместе.

    РОЛЬ ОТДЕЛЯЕТСЯ ОТ СЛОВА ТОЛЬКО ТАМ, ГДЕ ОДНО МЕСТО ЗАНЯТО РАЗНЫМИ СЛОВАМИ. Девять
    языков дают девять разных слов в ОДНОМ месте — и место становится видимым как место.

ТРИ ФОРМЫ ЗАКАЗАНЫ holon-f9 ПОИМЁННО, под законы М-709 (сцена-место), М-716 (рамка —
клауза) и М-710 (стык списка), и каждая стои́т на девяти языках:

    ЧИСЛО-ПЕРВОЕ С ДЕРЖАНИЕМ СЦЕНЫ и два контраста к нему — опенер-первое («there are N X
        on the table») и зачин без роли («if N X are on the table…»). Три соседних начала,
        из которых число стои́т на нулевом месте лишь в первом.
    ДВЕ КЛАУЗЫ В ОДНОМ ПРЕДЛОЖЕНИИ — с ОДНИМ носителем и с РАЗНЫМИ, и вопрос то на сумму,
        то на ОДНУ клаузу: рамка есть клауза, и читатель, берущий предложение целиком,
        на третьей странице лжёт.
    СПИСОК ДВУХ ЧИСЛОВЫХ ФРАЗ без деятеля между ними («5 книг и 3 цветка») с вопросом «в
        сумме» — свидетель слова списка.

ОТКУДА СЛОВА И ОТКУДА ФОРМЫ (условие holon-f9, и оно же — закон корней):

    СЛОВО — у таблицы понятий (`tools/concepts.py`): она отвечает лишь на вопрос «как это
        зовётся», и ключ там есть понятие, а не английское слово.
    ФОРМА СЧЁТА — у ПАКЕТА ЯЗЫКА, через `langpack.count_form_index`: пакет знает, что при
        пяти русский берёт «книг», а польский «książek». Дом не выводит форм сам.
    РАМКА — здесь. Предлог сцены, вопросное слово, «и», «всего» суть части рамки, а не
        свойства слова, и живут в доме, который эту рамку пишет.

Четыре понятия: кот (существо), стол (сцена), книга и цветок (товары) — те, чьи формы
объявлены на всех девяти языках. Счётный класс семи языков починен в тот же день: прежде
он объявлял формы С АРТИКЛЕМ и «5 les livres» вышло бы из него само.

ЗАКОН ЧИСЛА: не менее LAW² = 4 страниц каждой формы на КАЖДОМ языке.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from layer import emit                                            # noqa: E402
import concepts as C                                              # noqa: E402
import langpack                                                   # noqa: E402

ЯЗЫКИ = C.ЯЗЫКИ
_ПАК = {я: json.loads((pathlib.Path(__file__).resolve().parent / "langpacks" / f"{я}.json")
                      .read_text(encoding="utf-8")) for я in ЯЗЫКИ}

СУЩЕСТВО, СЦЕНА, ТОВАР_A, ТОВАР_B = "c36", "c52", "c01", "c06"


def ячейка(язык, понятие, n):
    """Имя ячейки счёта («one» / «few» / «many»), какую пакет требует при этом числе."""
    низ = C.слово(понятие, язык).lower()
    пак = _ПАК[язык]
    for _имя, кл in (пак.get("morph_classes") or {}).items():
        формы = кл.get("forms") or []
        лек = {k.lower(): v for k, v in (кл.get("lexemes") or {}).items()}
        if низ in лек and (set(формы) & {"one", "many"}):
            return формы[langpack.count_form_index(пак, кл, n)]
    return "one" if n == 1 else "many"


def счёт(язык, понятие, n):
    """«N слово» в форме, какую требует ПАКЕТ при этом числе."""
    слово = C.слово(понятие, язык)
    низ = слово.lower()
    пак = _ПАК[язык]
    for _имя, кл in (пак.get("morph_classes") or {}).items():
        формы = кл.get("forms") or []
        лек = {k.lower(): v for k, v in (кл.get("lexemes") or {}).items()}
        if низ in лек and (set(формы) & {"one", "many"}):
            i = langpack.count_form_index(пак, кл, n)
            счётная = f"count_{формы[i]}"
            j = формы.index(счётная) if счётная in формы else i
            return f"{n} {лек[низ][j]}"
    nf = пак.get("noun_forms") or {}
    if низ in nf:
        return f"{n} {слово if n == 1 else nf[низ]}"
    raise KeyError(f"{язык}: нет счётных форм для «{слово}»")


# РАМКИ ДОМА. Каждая — строка с местами {a} {b} {c} {t} для чисел-со-словом и {и1} {и2} для
# имён. Объявлены на девяти языках поимённо: предлог сцены, вопросное слово, «и», «всего»
# суть части рамки.
Р = {
 "ru": dict(имена=("Аня", "Ваня", "Вера", "Глеб"),
     число_первое="{a} сидели на столе. {b} пришли. сколько котов на столе теперь? {t}: {na} + {nb} = {nt}.",
     опенер="на столе лежат {a}. на стол кладут ещё {b}. сколько книг на столе теперь? {t}: {na} + {nb} = {nt}.",
     если="если на столе {a}, а на стол кладут ещё {b}, сколько книг на столе? {t}: {na} + {nb} = {nt}.",
     клаузы_один="{и1} купил {a} и {и1} купил {c}. сколько вещей купил {и1}? {t}: {na} + {nc} = {nt}.",
     клаузы_два="{и1} купил {a}, а {и2} купил {c}. сколько вещей они купили? {t}: {na} + {nc} = {nt}.",
     клауза_одна="{и1} купил {a} и {и1} купил {c}. сколько книг купил {и1}? {a}.",
     список="на столе {a} и {c}. сколько вещей на столе? {t}: {na} + {nc} = {nt}."),
 "en": dict(имена=("Ann", "Ben", "Carla", "Dan"),
     число_первое="{a} were sitting on the table. {b} came. how many cats are on the table now? {t}: {na} + {nb} = {nt}.",
     опенер="there are {a} on the table. {b} more are put on the table. how many books are on the table now? {t}: {na} + {nb} = {nt}.",
     если="if {a} are on the table and {b} more are put there, how many books are on the table? {t}: {na} + {nb} = {nt}.",
     клаузы_один="{и1} bought {a} and {и1} bought {c}. how many things did {и1} buy? {t}: {na} + {nc} = {nt}.",
     клаузы_два="{и1} bought {a} and {и2} bought {c}. how many things did they buy? {t}: {na} + {nc} = {nt}.",
     клауза_одна="{и1} bought {a} and {и1} bought {c}. how many books did {и1} buy? {a}.",
     список="{a} and {c} are on the table. how many things are on the table? {t}: {na} + {nc} = {nt}."),
 "de": dict(имена=("Anna", "Felix", "Jonas", "Laura"),
     число_первое="{a} saßen auf dem Tisch. {b} kamen dazu. wie viele Katzen sind jetzt auf dem Tisch? {t}: {na} + {nb} = {nt}.",
     опенер="auf dem Tisch liegen {a}. {b} werden dazugelegt. wie viele Bücher liegen jetzt auf dem Tisch? {t}: {na} + {nb} = {nt}.",
     если="wenn {a} auf dem Tisch liegen und {b} dazugelegt werden, wie viele Bücher liegen auf dem Tisch? {t}: {na} + {nb} = {nt}.",
     клаузы_один="{и1} kaufte {a} und {и1} kaufte {c}. wie viele Dinge kaufte {и1}? {t}: {na} + {nc} = {nt}.",
     клаузы_два="{и1} kaufte {a} und {и2} kaufte {c}. wie viele Dinge kauften sie? {t}: {na} + {nc} = {nt}.",
     клауза_одна="{и1} kaufte {a} und {и1} kaufte {c}. wie viele Bücher kaufte {и1}? {a}.",
     список="{a} und {c} liegen auf dem Tisch. wie viele Dinge liegen auf dem Tisch? {t}: {na} + {nc} = {nt}."),
 "fr": dict(имена=("Anne", "Hugo", "Jules", "Claire"),
     число_первое="{a} étaient assis sur la table. {b} sont arrivés. combien de chats y a-t-il sur la table maintenant ? {t} : {na} + {nb} = {nt}.",
     опенер="il y a {a} sur la table. on pose {b} de plus sur la table. combien de livres y a-t-il sur la table maintenant ? {t} : {na} + {nb} = {nt}.",
     если="si {a} sont sur la table et qu'on pose {b} de plus, combien de livres y a-t-il sur la table ? {t} : {na} + {nb} = {nt}.",
     клаузы_один="{и1} a acheté {a} et {и1} a acheté {c}. combien de choses {и1} a-t-il achetées ? {t} : {na} + {nc} = {nt}.",
     клаузы_два="{и1} a acheté {a} et {и2} a acheté {c}. combien de choses ont-ils achetées ? {t} : {na} + {nc} = {nt}.",
     клауза_одна="{и1} a acheté {a} et {и1} a acheté {c}. combien de livres {и1} a-t-il achetés ? {a}.",
     список="{a} et {c} sont sur la table. combien de choses y a-t-il sur la table ? {t} : {na} + {nc} = {nt}."),
 "es": dict(имена=("Ana", "Carlos", "Diego", "Elena"),
     число_первое="{a} estaban sentados en la mesa. {b} llegaron. ¿cuántos gatos hay en la mesa ahora? {t}: {na} + {nb} = {nt}.",
     опенер="hay {a} en la mesa. se ponen {b} más en la mesa. ¿cuántos libros hay en la mesa ahora? {t}: {na} + {nb} = {nt}.",
     если="si {a} están en la mesa y se ponen {b} más, ¿cuántos libros hay en la mesa? {t}: {na} + {nb} = {nt}.",
     клаузы_один="{и1} compró {a} y {и1} compró {c}. ¿cuántas cosas compró {и1}? {t}: {na} + {nc} = {nt}.",
     клаузы_два="{и1} compró {a} y {и2} compró {c}. ¿cuántas cosas compraron? {t}: {na} + {nc} = {nt}.",
     клауза_одна="{и1} compró {a} y {и1} compró {c}. ¿cuántos libros compró {и1}? {a}.",
     список="{a} y {c} están en la mesa. ¿cuántas cosas hay en la mesa? {t}: {na} + {nc} = {nt}."),
 "it": dict(имена=("Anna", "Luca", "Marco", "Giulia"),
     число_первое="{a} erano seduti sul tavolo. {b} sono arrivati. quanti gatti ci sono sul tavolo adesso? {t}: {na} + {nb} = {nt}.",
     опенер="ci sono {a} sul tavolo. si mettono {b} in più sul tavolo. quanti libri ci sono sul tavolo adesso? {t}: {na} + {nb} = {nt}.",
     если="se {a} sono sul tavolo e se ne mettono {b} in più, quanti libri ci sono sul tavolo? {t}: {na} + {nb} = {nt}.",
     клаузы_один="{и1} ha comprato {a} e {и1} ha comprato {c}. quante cose ha comprato {и1}? {t}: {na} + {nc} = {nt}.",
     клаузы_два="{и1} ha comprato {a} e {и2} ha comprato {c}. quante cose hanno comprato? {t}: {na} + {nc} = {nt}.",
     клауза_одна="{и1} ha comprato {a} e {и1} ha comprato {c}. quanti libri ha comprato {и1}? {a}.",
     список="{a} e {c} sono sul tavolo. quante cose ci sono sul tavolo? {t}: {na} + {nc} = {nt}."),
 "pt": dict(имена=("Ana", "João", "Maria", "Beatriz"),
     число_первое="{a} estavam sentados na mesa. {b} chegaram. quantos gatos há na mesa agora? {t}: {na} + {nb} = {nt}.",
     опенер="há {a} na mesa. põem-se {b} a mais na mesa. quantos livros há na mesa agora? {t}: {na} + {nb} = {nt}.",
     если="se {a} estão na mesa e se põem {b} a mais, quantos livros há na mesa? {t}: {na} + {nb} = {nt}.",
     клаузы_один="{и1} comprou {a} e {и1} comprou {c}. quantas coisas {и1} comprou? {t}: {na} + {nc} = {nt}.",
     клаузы_два="{и1} comprou {a} e {и2} comprou {c}. quantas coisas eles compraram? {t}: {na} + {nc} = {nt}.",
     клауза_одна="{и1} comprou {a} e {и1} comprou {c}. quantos livros {и1} comprou? {a}.",
     список="{a} e {c} estão na mesa. quantas coisas há na mesa? {t}: {na} + {nc} = {nt}."),
 "nl": dict(имена=("Anna", "Bram", "Daan", "Emma"),
     число_первое="{a} zaten op de tafel. {b} kwamen erbij. hoeveel katten zitten er nu op de tafel? {t}: {na} + {nb} = {nt}.",
     опенер="er liggen {a} op de tafel. er worden {b} bij gelegd. hoeveel boeken liggen er nu op de tafel? {t}: {na} + {nb} = {nt}.",
     если="als {a} op de tafel liggen en er {b} bij worden gelegd, hoeveel boeken liggen er op de tafel? {t}: {na} + {nb} = {nt}.",
     клаузы_один="{и1} kocht {a} en {и1} kocht {c}. hoeveel dingen kocht {и1}? {t}: {na} + {nc} = {nt}.",
     клаузы_два="{и1} kocht {a} en {и2} kocht {c}. hoeveel dingen kochten zij? {t}: {na} + {nc} = {nt}.",
     клауза_одна="{и1} kocht {a} en {и1} kocht {c}. hoeveel boeken kocht {и1}? {a}.",
     список="{a} en {c} liggen op de tafel. hoeveel dingen liggen op de tafel? {t}: {na} + {nc} = {nt}."),
 "pl": dict(имена=("Anna", "Jan", "Marek", "Ewa"),
     # ГЛАГОЛ СОГЛАСУЕТСЯ С ЧИСЛОМ ТАК ЖЕ, КАК ИМЯ (07.09, первая проба дома): польский при
     # пяти и более берёт средний род единственного — «18 kotów SIEDZIAŁO», а не
     # «siedziały». Это та же ячейка счёта, что у имени, и потому берётся тем же путём —
     # у пакета, а не догадкой. Первая проба написала «18 kotów siedziały», и это была бы
     # ложь о языке при верной арифметике.
     глагол_сидели={"one": "siedział", "few": "siedziały", "many": "siedziało"},
     глагол_пришли={"one": "przyszedł", "few": "przyszły", "many": "przyszło"},
     число_первое="{a} {гл_с} na stole. {b} {гл_п}. ile kotów jest teraz na stole? {t}: {na} + {nb} = {nt}.",
     опенер="na stole leży {a}. kładzie się jeszcze {b}. ile książek leży teraz na stole? {t}: {na} + {nb} = {nt}.",
     если="jeśli na stole leży {a}, a kładzie się jeszcze {b}, ile książek leży na stole? {t}: {na} + {nb} = {nt}.",
     клаузы_один="{и1} kupił {a} i {и1} kupił {c}. ile rzeczy kupił {и1}? {t}: {na} + {nc} = {nt}.",
     клаузы_два="{и1} kupił {a}, a {и2} kupił {c}. ile rzeczy kupili? {t}: {na} + {nc} = {nt}.",
     клауза_одна="{и1} kupił {a} i {и1} kupił {c}. ile książek kupił {и1}? {a}.",
     список="na stole {a} i {c}. ile rzeczy jest na stole? {t}: {na} + {nc} = {nt}."),
}
ФОРМЫ = ("число_первое", "опенер", "если", "клаузы_один", "клаузы_два", "клауза_одна", "список")
for _я in ЯЗЫКИ:
    assert set(ФОРМЫ) <= set(Р[_я]), (_я, "рамка не объявлена")
    assert len(Р[_я]["имена"]) >= 2, (_я, "носителей меньше LAW")
    assert set(Р[_я]["имена"]) <= set(_ПАК[_я]["person_names"]), (_я, "имя не объявлено пакетом")


def показы(pi):
    основа = pi * 47
    вон = []
    for i in range(len(ЯЗЫКИ) * len(ФОРМЫ) * 4):
        язык = ЯЗЫКИ[(основа + i) % len(ЯЗЫКИ)]
        форма = ФОРМЫ[((основа + i) // len(ЯЗЫКИ)) % len(ФОРМЫ)]
        рамка = Р[язык]
        na = (основа + i * 7) % 40 + 2
        nb = (основа + i * 11) % 30 + 2
        и1 = рамка["имена"][(основа + i) % len(рамка["имена"])]
        и2 = рамка["имена"][(основа + i + 1) % len(рамка["имена"])]
        # ЧИСЛО-ПЕРВОЕ — о СУЩЕСТВЕ на сцене; прочие формы — о ТОВАРАХ
        пон_a = СУЩЕСТВО if форма == "число_первое" else ТОВАР_A
        a = счёт(язык, пон_a, na)
        b = счёт(язык, пон_a, nb)
        c = счёт(язык, ТОВАР_B, nb)
        t = счёт(язык, пон_a if форма in ("число_первое", "опенер", "если") else ТОВАР_A, na + nb)
        поля = dict(a=a, b=b, c=c, t=t, na=na, nb=nb, nc=nb, nt=na + nb)
        поля["и1"], поля["и2"] = и1, и2
        # ГЛАГОЛ ПО ТОЙ ЖЕ ЯЧЕЙКЕ, ЧТО И ИМЯ — там, где язык его двигает
        if "глагол_сидели" in рамка:
            поля["гл_с"] = рамка["глагол_сидели"][ячейка(язык, пон_a, na)]
            поля["гл_п"] = рамка["глагол_пришли"][ячейка(язык, пон_a, nb)]
        вон.append(рамка[форма].format(**поля))
    return вон


def main():
    emit("datasets/genesis_ninelang.txt", показы)


if __name__ == "__main__":
    main()
