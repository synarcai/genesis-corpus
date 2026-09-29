#!/usr/bin/env python3
"""МИР ПАМЯТИ дома `toolmemory` — объявление, общее дому, суду и прибору съёмки (29.09, ведущий omega-90: М-2100).

Инструмент — мир: любой сервер Model Context Protocol монтируется мостом ядра `ozar_mcp_world`, его инструменты — роды,
чтения — те, какие сам сервер назвал только читающими (`readOnlyHint`). Первый мир дома — память агента: сервер
memory (граф знаний: сущности с родом и наблюдениями, связи между ними). В корпусе НЕТ МОДЕЛИ ГРАФА: ответы сервера
снимает прибор `toolmemory_capture.py` в семя `tools/seeds/toolmemory_world.json` под отпечатком объявленного графа и
актов; дом печатает ход мира из семени, суд сверяет его с семенем байт в байт. Один источник правды — сервер.

ОБЪЯВЛЕННЫЙ ГРАФ (`ГРАФ`) — как ПРОЕКТ у дома кода: у всякого голоса свои люди, их род и наблюдения — слова голоса,
какими пользователь их сказал бы; граф СТРОИТ САМ СЕРВЕР актами моста (`акты_графа`), файл графа руками не пишется.
Всякий акт страницы снимается на свежем файле графа (`MEMORY_FILE_PATH`): сначала акты объявленного графа, затем акт
страницы; в семя ложатся ответ провода и байты файла графа после акта целиком (строгий судья ключа сверяет файл).

ИМЕНА ЛЮДЕЙ — слова голоса; где голос склоняет имя (ru, pl), дверь `ФОРМЫ_ИМЁН` называет падеж, каким его говорит
страница («о Норе», «zna Pawła»); сервер хранит имя, каким оно названо в именительном.
"""
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import actturn as A  # noqa: E402 — голоса дома
import folderworld as W  # noqa: E402 — ход мира строкой, общий с домом актов

СЕМЯ = pathlib.Path(__file__).resolve().parent / "seeds" / "toolmemory_world.json"
ЯЗЫКИ = A.ЯЗЫКИ

# ======================================================================================================
# ГРАФ ГОЛОСА: люди (имя, род, наблюдения), связи (от кого, к кому, вид связи — слово голоса)
# ======================================================================================================
# ЛЮДИ ПО МЕСТУ: 0 — два наблюдения и связи в обе стороны; 1 — одно наблюдение; 2 — три наблюдения; 3 — без наблюдений
# (контраст плана «записать нечего»); НОВЫЕ — люди, каких граф не знает (запомнить нового: имя, род, наблюдение);
# НЕЗНАКОМЫЙ — имя, какого граф не знает и страница не создаёт («не помню», «забыть нечего»)
ГРАФ = {
    "en": {"люди": (("Nora", "teacher", ("plays the cello", "lives by the sea")),
                    ("Pavel", "baker", ("keeps bees",)),
                    ("Ilse", "doctor", ("grows tomatoes", "speaks Greek", "swims every morning")),
                    ("Tomas", "pilot", ())),
           "связь": "knows", "новые": (("Oskar", "carpenter", "builds boats"), ("Lena", "nurse", "sews dresses")), "незнакомый": "Vera",
           "добавить": ("collects old maps", "sings in a choir", "plays chess")},
    "ru": {"люди": (("Нора", "учительница", ("играет на виолончели", "живёт у моря")),
                    ("Павел", "пекарь", ("держит пчёл",)),
                    ("Ильза", "врач", ("выращивает помидоры", "говорит по-гречески", "плавает каждое утро")),
                    ("Томас", "пилот", ())),
           "связь": "знает", "новые": (("Оскар", "плотник", "строит лодки"), ("Лена", "медсестра", "шьёт платья")), "незнакомый": "Вера",
           "добавить": ("собирает старые карты", "поёт в хоре", "играет в шахматы")},
    "de": {"люди": (("Nora", "Lehrerin", ("spielt Cello", "wohnt am Meer")),
                    ("Pavel", "Bäcker", ("hält Bienen",)),
                    ("Ilse", "Ärztin", ("zieht Tomaten", "spricht Griechisch", "schwimmt jeden Morgen")),
                    ("Tomas", "Pilot", ())),
           "связь": "kennt", "новые": (("Oskar", "Tischler", "baut Boote"), ("Lena", "Pflegerin", "näht Kleider")), "незнакомый": "Vera",
           "добавить": ("sammelt alte Landkarten", "singt im Chor", "spielt Schach")},
    "fr": {"люди": (("Nora", "enseignante", ("joue du violoncelle", "habite au bord de la mer")),
                    ("Pavel", "boulanger", ("élève des abeilles",)),
                    ("Ilse", "médecin", ("cultive des tomates", "parle grec", "nage chaque matin")),
                    ("Tomas", "pilote", ())),
           "связь": "connaît", "новые": (("Oskar", "menuisier", "construit des bateaux"), ("Lena", "infirmière", "coud des robes")), "незнакомый": "Vera",
           "добавить": ("collectionne les vieilles cartes", "chante dans une chorale", "joue aux échecs")},
    "es": {"люди": (("Nora", "profesora", ("toca el violonchelo", "vive junto al mar")),
                    ("Pavel", "panadero", ("cría abejas",)),
                    ("Ilse", "médica", ("cultiva tomates", "habla griego", "nada cada mañana")),
                    ("Tomas", "piloto", ())),
           "связь": "conoce", "новые": (("Oskar", "carpintero", "construye barcos"), ("Lena", "enfermera", "cose vestidos")), "незнакомый": "Vera",
           "добавить": ("colecciona mapas antiguos", "canta en un coro", "juega al ajedrez")},
    "it": {"люди": (("Nora", "insegnante", ("suona il violoncello", "vive al mare")),
                    ("Pavel", "fornaio", ("alleva api",)),
                    ("Ilse", "dottoressa", ("coltiva pomodori", "parla greco", "nuota ogni mattina")),
                    ("Tomas", "pilota", ())),
           "связь": "conosce", "новые": (("Oskar", "falegname", "costruisce barche"), ("Lena", "infermiera", "cuce vestiti")), "незнакомый": "Vera",
           "добавить": ("colleziona vecchie mappe", "canta in un coro", "gioca a scacchi")},
    "pt": {"люди": (("Nora", "professora", ("toca violoncelo", "mora perto do mar")),
                    ("Pavel", "padeiro", ("cria abelhas",)),
                    ("Ilse", "médica", ("cultiva tomates", "fala grego", "nada todas as manhãs")),
                    ("Tomas", "piloto", ())),
           "связь": "conhece", "новые": (("Oskar", "carpinteiro", "constrói barcos"), ("Lena", "enfermeira", "costura vestidos")), "незнакомый": "Vera",
           "добавить": ("coleciona mapas antigos", "canta num coro", "joga xadrez")},
    "nl": {"люди": (("Nora", "lerares", ("speelt cello", "woont aan zee")),
                    ("Pavel", "bakker", ("houdt bijen",)),
                    ("Ilse", "arts", ("kweekt tomaten", "spreekt Grieks", "zwemt elke ochtend")),
                    ("Tomas", "piloot", ())),
           "связь": "kent", "новые": (("Oskar", "timmerman", "bouwt boten"), ("Lena", "verpleegster", "naait jurken")), "незнакомый": "Vera",
           "добавить": ("verzamelt oude kaarten", "zingt in een koor", "speelt schaak")},
    "pl": {"люди": (("Nora", "nauczycielką", ("gra na wiolonczeli", "mieszka nad morzem")),
                    ("Paweł", "piekarzem", ("hoduje pszczoły",)),
                    ("Ilse", "lekarką", ("uprawia pomidory", "mówi po grecku", "pływa każdego ranka")),
                    ("Tomasz", "pilotem", ())),
           "связь": "zna", "новые": (("Oskar", "stolarzem", "buduje łodzie"), ("Lena", "pielęgniarką", "szyje sukienki")), "незнакомый": "Wera",
           "добавить": ("zbiera stare mapy", "śpiewa w chórze", "gra w szachy")},
}
# СВЯЗИ ОБЪЯВЛЕННОГО ГРАФА — местами людей: 0 знает 1, 2 знает 0 (у места 0 связи в обе стороны); НОВЫЕ СВЯЗИ — какие
# страница запоминает: 1 знает 3, 3 знает 2
СВЯЗИ = ((0, 1), (2, 0))
НОВЫЕ_СВЯЗИ = ((1, 3), (3, 2))

# ФОРМЫ ИМЁН — падеж, каким имя стоит на странице там, где голос его склоняет: «пр» — «о ком» (с предлогом, «об
# Ильзе»), «вин» — дополнение связи («Нора знает Павла»), «твор» — «с кем» («связан с Павлом»), «род» — при отрицании
# («nie znam Wery»); у прочих голосов имя стоит как названо
ФОРМЫ_ИМЁН = {
    "ru": {"Нора": {"пр": "о Норе", "вин": "Нору", "твор": "Норой"},
           "Павел": {"пр": "о Павле", "вин": "Павла", "твор": "Павлом"},
           "Ильза": {"пр": "об Ильзе", "вин": "Ильзу", "твор": "Ильзой"},
           "Томас": {"пр": "о Томасе", "вин": "Томаса", "твор": "Томасом"},
           "Оскар": {"пр": "об Оскаре", "вин": "Оскара", "твор": "Оскаром"},
           "Вера": {"пр": "о Вере", "вин": "Веру", "твор": "Верой"},
           "Лена": {"пр": "о Лене", "вин": "Лену", "твор": "Леной"}},
    "pl": {"Nora": {"пр": "o Norze", "вин": "Norę", "твор": "Norą", "род": "Nory"},
           "Paweł": {"пр": "o Pawle", "вин": "Pawła", "твор": "Pawłem", "род": "Pawła"},
           "Ilse": {"пр": "o Ilse", "вин": "Ilse", "твор": "Ilse", "род": "Ilse"},
           "Tomasz": {"пр": "o Tomaszu", "вин": "Tomasza", "твор": "Tomaszem", "род": "Tomasza"},
           "Oskar": {"пр": "o Oskarze", "вин": "Oskara", "твор": "Oskarem", "род": "Oskara"},
           "Wera": {"пр": "o Werze", "вин": "Werę", "твор": "Werą", "род": "Wery"},
           "Lena": {"пр": "o Lenie", "вин": "Lenę", "твор": "Leną", "род": "Leny"}},
}


def люди(язык):
    return ГРАФ[язык]["люди"]


def имя(язык, место):
    return ГРАФ[язык]["люди"][место][0]


def форма(язык, имя_, падеж):
    """Имя в падеже страницы (ru, pl); у прочих голосов — как названо."""
    return ФОРМЫ_ИМЁН.get(язык, {}).get(имя_, {}).get(падеж, имя_)


# ======================================================================================================
# АКТЫ: граф строится актами моста; акты страниц — чтения, правки, отказы
# ======================================================================================================
# ВРЕМЕННОЕ НАБЛЮДЕНИЕ — у человека без наблюдений: сервер создаёт сущность лишь с наблюдением, и граф голоса снимает
# его тем же сервером (delete_observations) — сущность с пустым списком наблюдений есть правда графа, не рука дома
_ВРЕМЕННОЕ = "·"


def акты_графа(язык):
    """Акты моста, какими сервер строит объявленный граф голоса: (род, объект, доводы)."""
    вон = []
    for имя_, род_, наблюдения in люди(язык):
        первое = наблюдения[0] if наблюдения else _ВРЕМЕННОЕ
        вон.append(("create_entities", имя_, (род_, первое)))
        вон += [("add_observations", имя_, (н,)) for н in наблюдения[1:]]
        if not наблюдения:
            вон.append(("delete_observations", имя_, (_ВРЕМЕННОЕ,)))
    вон += [("create_relations", имя(язык, a), (имя(язык, b), ГРАФ[язык]["связь"])) for a, b in СВЯЗИ]
    return вон


def акты_страниц(язык):
    """Акты, какие снимаются на объявленном графе голоса — каждый на свежем файле графа."""
    г = ГРАФ[язык]
    вон = [("read_graph", "", ())]
    вон += [("open_nodes", имя_, ()) for имя_, _р, _н in люди(язык)] + [("open_nodes", г["незнакомый"], ())]
    вон += [("open_nodes", новый, ()) for новый, _р, _н in г["новые"]]
    вон += [("search_nodes", имя_, ()) for имя_, _р, _н in люди(язык)] + [("search_nodes", г["незнакомый"], ())]
    вон += [("create_entities", новый, (род_, наблюдение)) for новый, род_, наблюдение in г["новые"]]
    вон += [("add_observations", имя(язык, м), (н,)) for м, н in zip((0, 1, 3), г["добавить"])]
    вон.append(("add_observations", г["незнакомый"], (г["добавить"][0],)))
    вон += [("create_relations", имя(язык, a), (имя(язык, b), г["связь"])) for a, b in НОВЫЕ_СВЯЗИ]
    вон += [("delete_entities", имя_, ()) for имя_, _р, _н in люди(язык)]
    вон += [("delete_observations", имя_, (н,)) for имя_, _р, наблюдения in люди(язык) for н in наблюдения[:1]]
    вон += [("delete_relations", имя(язык, a), (имя(язык, b), г["связь"])) for a, b in СВЯЗИ]
    return list(dict.fromkeys(вон))


def ключ(род, объект="", доводы=()):
    """Ключ акта в семени — строка провода, как её шлёт прибор (доводы через нуль-байт)."""
    return json.dumps({"act": род, "object": объект, **({"arg": list("\0".join(доводы).encode())} if доводы else {})},
                      ensure_ascii=False)


def отпечаток():
    """Отпечаток объявленных графов и актов страниц: семя верно, пока он тот же, что при съёмке."""
    return hashlib.sha256(json.dumps([[язык, акты_графа(язык), акты_страниц(язык)] for язык in ЯЗЫКИ],
                                     ensure_ascii=False).encode()).hexdigest()[:16]


_СЕМЯ = None


def семя():
    global _СЕМЯ
    if _СЕМЯ is None:
        _СЕМЯ = json.loads(СЕМЯ.read_text(encoding="utf-8")) if СЕМЯ.exists() else {}
    return _СЕМЯ


def объявление():
    """Объявление мира сервером (ответ «declare»): роды, чтения, число мест, поля строк рода."""
    строки = семя()["declare"].splitlines()
    return {"роды": tuple(с[5:] for с in строки if с.startswith("kind ")),
            "чтения": frozenset(с[8:] for с in строки if с.startswith("reading ")),
            "поля": {с.split()[1]: tuple(с.split()[2:]) for с in строки if с.startswith("rows ")}}


def снятое(язык, род, объект="", доводы=()):
    """Снятое акта страницы: {"reply": ответ провода, "graph": байты файла графа после акта}."""
    return семя()["scenes"][язык][ключ(род, объект, доводы)]


# ПОЛЕ ПРИЧИНЫ — у инструмента, сказавшего «провалился» (error 1): его ряды — причина, текстом (контракт М-2100: «без
# схемы — ряд на строку каждого блока ответа, поле text»)
ПОЛЕ_ПРИЧИНЫ = "text"


def ход(язык, род, объект="", доводы=()):
    """Ход мира на акт страницы по семени: наблюдение — меры rows и error и ряды полями рода (у провала — полем
    причины), пустые поля опущены (первая нормальная форма моста: ряд держит одно значение в поле); отказ моста — по
    имени."""
    ответ = снятое(язык, род, объект, доводы)["reply"]
    if ответ["reply"] == "refused":
        return W.Отказ(род, объект or None, tuple(доводы), ответ["why"], ответ["what"])
    меры = tuple((м["ledger"], м["value"]) for м in ответ["measures"])
    поля = (ПОЛЕ_ПРИЧИНЫ,) if dict(меры).get("error") else объявление()["поля"].get(род, ())
    строки = tuple(tuple((п, з) for п, з in zip(поля, ряд) if з != "") for ряд in ответ.get("rows") or ())
    return W.Наблюдение(род, объект or None, tuple(доводы), меры, строки)


def ряды(ход_):
    """Ряды хода словарями {поле: значение} (пустые поля опущены)."""
    return [dict(р) for р in ход_.строки]


if __name__ == "__main__":
    с = семя()
    # головы хода — роды, какие сервер объявил, и знак языка узнаёт провод по ним (`folderworld.ВИДЫ`)
    assert not с or set(объявление()["роды"]) <= set(W.ВИДЫ), sorted(set(объявление()["роды"]) - set(W.ВИДЫ))
    print(f"МИР ПАМЯТИ: голосов {len(ЯЗЫКИ)}, актов графа {sum(len(акты_графа(я)) for я in ЯЗЫКИ)}, актов страниц "
          f"{sum(len(акты_страниц(я)) for я in ЯЗЫКИ)}; отпечаток {отпечаток()}, семя {'есть' if с else 'нет'} "
          f"({с.get('source', '—')})")
