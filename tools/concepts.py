#!/usr/bin/env python3
"""ТАБЛИЦА ПОНЯТИЙ КОРПУСА — одно понятие, девять слов (07.09).

ПОВОД, И ОН ЗАМЕРЕН. Девять языковых пакетов объявляют девять НЕЗАВИСИМЫХ словарей, и
ключом в каждом стои́т слово ЭТОГО ЖЕ языка: `en: book → ['book','books']`, `es: libro →
['el libro','los libros']`, `ru: книга → [...]`. Ни один ключ не говорит, что «book»,
«libro» и «книга» суть ОДНО.

    МЕЖДУ ПАКЕТАМИ НЕТ МОСТА ПОНЯТИЙ. Оттого конструкционный мир на девяти языках нельзя
    построить объявлением — только вписав таблицу руками, и всякий дом впишет свою; а
    четыре своих таблицы суть четыре несогласных словаря.

ЧЕМ ЭТО КОНЧАЕТСЯ, ПОКАЗАНО ДЕЛОМ В ТОТ ЖЕ ДЕНЬ. Дом перевода брал слова у дома букв и
спаривал их ПО НОМЕРУ МЕСТА в списках, проверяя одно — равенство длин; русский список стоял
на одно место иначе, и свод учил, что хлеб есть eau, а солнце есть Brot: 75 ложных строк,
которых не ловил ни один суд. ЭТА таблица есть тот же почин, поднятый с одного дома на весь
корпус.

    ПОНЯТИЕ ЕСТЬ КЛЮЧ, А ЯЗЫК — СТОЛБЕЦ. Английское слово здесь не имя понятия, а один из
    девяти столбцов, и ключ нарочно не равен ни одному из девяти слов: код, взявший ключ за
    слово, сломается сразу, а не через месяц ложью в своде.

ЧТО ЭТА ТАБЛИЦА ЕСТЬ И ЧЕГО В НЕЙ НЕТ:

    ЕСТЬ — слово каждого понятия на девяти языках, В ИМЕНИТЕЛЬНОМ ЕДИНСТВЕННОМ. Это
        СЛОВАРЬ, а не грамматика.
    НЕТ — согласования: рода, падежа, числа, степени, вопросной формы. Они принадлежат
        ПАКЕТУ ЯЗЫКА и остаются там; дом спрашивает форму у пакета, а не у этой таблицы, и
        не выводит её сам. Таблица отвечает только на вопрос «как это зовётся».
    НЕТ — полноты: понятий здесь ровно столько, сколько нужно домам, что её читают.
        Молчание о прочих есть честная граница, а не утверждение, что мир исчерпан.

ПАСПОРТ: дом, читающий эту таблицу, ОБЪЯВЛЯЕТ это в `ЧИТАЮТ`. Правка корня есть правка
всех, кто на него смотрит, — и три шрама одного дня (пакет переписал мир глифов; мир букв
столкнулся с удержанным ключом; дом перевода спаривал по месту) стоили того, чтобы всякий
корень нёс список своих читателей.

    python3 tools/concepts.py     # перепись: понятий, языков, полнота
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")

# ПАСПОРТ КОРНЯ: кто эту таблицу читает. Список объявляется здесь и проверяется переписью
# (прибор ищет `import concepts` по домам и сверяет).
ЧИТАЮТ = ("translateforms", "ninelang")

# ПОНЯТИЯ. Ключ есть ЧИСЛОВОЕ ИМЯ, не слово ни одного языка; человеку понятие читается по
# столбцу `ru`, машине — по ключу. Роды понятий («товар», «вместилище», «существо»,
# «место», «вещество») объявлены при каждом, ибо дом спрашивает не «какое слово вообще», а
# «какое слово ЭТОГО рода».
ПОНЯТИЯ = {
    # ТОВАРЫ — счётные вещи, какие носитель держит, даёт, покупает
    "c01": ("товар", dict(ru="книга", en="book", de="Buch", fr="livre", es="libro", it="libro", pt="livro", nl="boek", pl="książka")),
    "c02": ("товар", dict(ru="карта", en="card", de="Karte", fr="carte", es="carta", it="carta", pt="carta", nl="kaart", pl="karta")),
    "c03": ("товар", dict(ru="монета", en="coin", de="Münze", fr="pièce", es="moneda", it="moneta", pt="moeda", nl="munt", pl="moneta")),
    "c04": ("товар", dict(ru="яблоко", en="apple", de="Apfel", fr="pomme", es="manzana", it="mela", pt="maçã", nl="appel", pl="jabłko")),
    "c05": ("товар", dict(ru="яйцо", en="egg", de="Ei", fr="œuf", es="huevo", it="uovo", pt="ovo", nl="ei", pl="jajko")),
    "c06": ("товар", dict(ru="цветок", en="flower", de="Blume", fr="fleur", es="flor", it="fiore", pt="flor", nl="bloem", pl="kwiat")),
    "c07": ("товар", dict(ru="карандаш", en="pencil", de="Bleistift", fr="crayon", es="lápiz", it="matita", pt="lápis", nl="potlood", pl="ołówek")),
    "c08": ("товар", dict(ru="мяч", en="ball", de="Ball", fr="balle", es="pelota", it="palla", pt="bola", nl="bal", pl="piłka")),
    "c09": ("товар", dict(ru="марка", en="stamp", de="Briefmarke", fr="timbre", es="sello", it="francobollo", pt="selo", nl="postzegel", pl="znaczek")),
    "c10": ("товар", dict(ru="семя", en="seed", de="Samen", fr="graine", es="semilla", it="seme", pt="semente", nl="zaad", pl="nasienie")),
    "c11": ("товар", dict(ru="печенье", en="cookie", de="Keks", fr="biscuit", es="galleta", it="biscotto", pt="biscoito", nl="koekje", pl="ciastko")),
    "c12": ("товар", dict(ru="страница", en="page", de="Seite", fr="page", es="página", it="pagina", pt="página", nl="pagina", pl="strona")),
    # ВМЕСТИЛИЩА — они же меры: слово одно, а чтений два (см. `measureof` и `totalsubj`)
    "c20": ("вместилище", dict(ru="чашка", en="cup", de="Tasse", fr="tasse", es="taza", it="tazza", pt="xícara", nl="kop", pl="filiżanka")),
    "c21": ("вместилище", dict(ru="мешок", en="bag", de="Beutel", fr="sac", es="bolsa", it="sacco", pt="saco", nl="zak", pl="worek")),
    "c22": ("вместилище", dict(ru="бутылка", en="bottle", de="Flasche", fr="bouteille", es="botella", it="bottiglia", pt="garrafa", nl="fles", pl="butelka")),
    "c23": ("вместилище", dict(ru="коробка", en="box", de="Schachtel", fr="boîte", es="caja", it="scatola", pt="caixa", nl="doos", pl="pudełko")),
    "c24": ("вместилище", dict(ru="корзина", en="basket", de="Korb", fr="panier", es="cesta", it="cesto", pt="cesta", nl="mand", pl="kosz")),
    # СУЩЕСТВА — те, кто действует и кого считают подлежащим
    "c30": ("существо", dict(ru="ребёнок", en="child", de="Kind", fr="enfant", es="niño", it="bambino", pt="criança", nl="kind", pl="dziecko")),
    "c31": ("существо", dict(ru="птица", en="bird", de="Vogel", fr="oiseau", es="pájaro", it="uccello", pt="pássaro", nl="vogel", pl="ptak")),
    "c32": ("существо", dict(ru="ученик", en="student", de="Schüler", fr="élève", es="alumno", it="studente", pt="aluno", nl="leerling", pl="uczeń")),
    "c33": ("существо", dict(ru="покупатель", en="customer", de="Kunde", fr="client", es="cliente", it="cliente", pt="cliente", nl="klant", pl="klient")),
    "c34": ("существо", dict(ru="пассажир", en="passenger", de="Passagier", fr="passager", es="pasajero", it="passeggero", pt="passageiro", nl="passagier", pl="pasażer")),
    "c35": ("существо", dict(ru="щенок", en="puppy", de="Welpe", fr="chiot", es="cachorro", it="cucciolo", pt="filhote", nl="puppy", pl="szczeniak")),
    "c36": ("существо", dict(ru="кот", en="cat", de="Katze", fr="chat", es="gato", it="gatto", pt="gato", nl="kat", pl="kot")),
    "c37": ("существо", dict(ru="собака", en="dog", de="Hund", fr="chien", es="perro", it="cane", pt="cão", nl="hond", pl="pies")),
    # МЕСТА — сцены, на которых считают действующих
    "c40": ("место", dict(ru="автобус", en="bus", de="Bus", fr="bus", es="autobús", it="autobus", pt="ônibus", nl="bus", pl="autobus")),
    "c41": ("место", dict(ru="забор", en="fence", de="Zaun", fr="clôture", es="valla", it="recinto", pt="cerca", nl="hek", pl="płot")),
    "c42": ("место", dict(ru="дерево", en="tree", de="Baum", fr="arbre", es="árbol", it="albero", pt="árvore", nl="boom", pl="drzewo")),
    "c43": ("место", dict(ru="лавка", en="shop", de="Laden", fr="magasin", es="tienda", it="negozio", pt="loja", nl="winkel", pl="sklep")),
    "c44": ("место", dict(ru="зал", en="hall", de="Saal", fr="salle", es="sala", it="sala", pt="sala", nl="zaal", pl="sala")),
    "c45": ("место", dict(ru="поезд", en="train", de="Zug", fr="train", es="tren", it="treno", pt="trem", nl="trein", pl="pociąg")),
    "c46": ("место", dict(ru="двор", en="yard", de="Hof", fr="cour", es="patio", it="cortile", pt="pátio", nl="erf", pl="podwórko")),
    "c47": ("место", dict(ru="сад", en="garden", de="Garten", fr="jardin", es="jardín", it="giardino", pt="jardim", nl="tuin", pl="ogród")),
    "c48": ("место", dict(ru="парк", en="park", de="Park", fr="parc", es="parque", it="parco", pt="parque", nl="park", pl="park")),
    "c49": ("место", dict(ru="пруд", en="pond", de="Teich", fr="étang", es="estanque", it="stagno", pt="lago", nl="vijver", pl="staw")),
    "c50": ("место", dict(ru="клетка", en="cage", de="Käfig", fr="cage", es="jaula", it="gabbia", pt="gaiola", nl="kooi", pl="klatka")),
    "c51": ("место", dict(ru="комната", en="room", de="Zimmer", fr="chambre", es="habitación", it="stanza", pt="quarto", nl="kamer", pl="pokój")),
    "c52": ("место", dict(ru="стол", en="table", de="Tisch", fr="table", es="mesa", it="tavolo", pt="mesa", nl="tafel", pl="stół")),
    "c53": ("место", dict(ru="полка", en="shelf", de="Regal", fr="étagère", es="estante", it="scaffale", pt="prateleira", nl="plank", pl="półka")),
    "c54": ("место", dict(ru="дом", en="house", de="Haus", fr="maison", es="casa", it="casa", pt="casa", nl="huis", pl="dom")),
    # ВЕЩЕСТВА — то, что стои́т за предлогом меры и не считается само
    "c60": ("вещество", dict(ru="сахар", en="sugar", de="Zucker", fr="sucre", es="azúcar", it="zucchero", pt="açúcar", nl="suiker", pl="cukier")),
    "c61": ("вещество", dict(ru="мука", en="flour", de="Mehl", fr="farine", es="harina", it="farina", pt="farinha", nl="meel", pl="mąka")),
    "c62": ("вещество", dict(ru="вода", en="water", de="Wasser", fr="eau", es="agua", it="acqua", pt="água", nl="water", pl="woda")),
    "c63": ("вещество", dict(ru="молоко", en="milk", de="Milch", fr="lait", es="leche", it="latte", pt="leite", nl="melk", pl="mleko")),
    "c64": ("вещество", dict(ru="соль", en="salt", de="Salz", fr="sel", es="sal", it="sale", pt="sal", nl="zout", pl="sól")),
    "c65": ("вещество", dict(ru="рис", en="rice", de="Reis", fr="riz", es="arroz", it="riso", pt="arroz", nl="rijst", pl="ryż")),
    "c66": ("вещество", dict(ru="чай", en="tea", de="Tee", fr="thé", es="té", it="tè", pt="chá", nl="thee", pl="herbata")),
    "c67": ("вещество", dict(ru="кофе", en="coffee", de="Kaffee", fr="café", es="café", it="caffè", pt="café", nl="koffie", pl="kawa")),
    "c68": ("вещество", dict(ru="хлеб", en="bread", de="Brot", fr="pain", es="pan", it="pane", pt="pão", nl="brood", pl="chleb")),
    "c69": ("вещество", dict(ru="солнце", en="sun", de="Sonne", fr="soleil", es="sol", it="sole", pt="sol", nl="zon", pl="słońce")),
    "c70": ("часть тела", dict(ru="рука", en="hand", de="Hand", fr="main", es="mano", it="mano", pt="mão", nl="hand", pl="ręka")),
}

# УТВЕРЖДЕНИЯ ПО СУЩЕСТВУ, А НЕ ПО ДЛИНЕ (шрам дома перевода того же дня).
_ВСЕ_СЛОВА = set()
for _к, (_род, _ряд) in ПОНЯТИЯ.items():
    assert set(_ряд) == set(ЯЗЫКИ), (_к, "понятие не полно по языкам")
    assert all(_ряд[_я].strip() for _я in ЯЗЫКИ), (_к, "пустое слово")
    assert _к not in _ряд.values(), (_к, "ключ равен слову — понятие спутано со словом")
    _ВСЕ_СЛОВА |= set(_ряд.values())
assert len({_ряд["ru"] for _к, (_р, _ряд) in ПОНЯТИЯ.items()}) == len(ПОНЯТИЯ), \
    "два понятия зовутся одним русским словом"


def слово(понятие, язык):
    """Слово понятия на языке — именительный единственный. Форму спрашивают у ПАКЕТА."""
    род_и_ряд = ПОНЯТИЯ.get(понятие)
    if род_и_ряд is None:
        raise KeyError("нет такого понятия: " + repr(понятие))
    return род_и_ряд[1][язык]


def рода(род):
    """Ключи понятий объявленного рода — в порядке объявления."""
    return tuple(к for к, (р, _) in ПОНЯТИЯ.items() if р == род)


def ряд(язык, род=None):
    """Слова языка (всех понятий или одного рода) — в порядке объявления."""
    return tuple(ПОНЯТИЯ[к][1][язык] for к in (рода(род) if род else ПОНЯТИЯ))


def main():
    роды = {}
    for _к, (р, _ряд) in ПОНЯТИЯ.items():
        роды[р] = роды.get(р, 0) + 1
    полных = sum(1 for _к, (_р, ряд_) in ПОНЯТИЯ.items() if set(ряд_) == set(ЯЗЫКИ))
    print(f"ТАБЛИЦА ПОНЯТИЙ: понятий {len(ПОНЯТИЯ)}, языков {len(ЯЗЫКИ)}, "
          f"полных по языкам {полных}, слов {len(_ВСЕ_СЛОВА)}; "
          f"роды: {', '.join(f'{р} {n}' for р, n in sorted(роды.items()))}; "
          f"читают: {', '.join(ЧИТАЮТ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
