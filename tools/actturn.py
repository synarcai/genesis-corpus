#!/usr/bin/env python3
"""THE HOUSE OF THE DIALOGUE ACT — the organism's own turn, with confirmation and observation (06.09).

Asked for by holon for the release demo's sixth scene, and it is the one show the corpus never
had: every world of ours SAYS something about the world («в папке 3 файла»), and none shows the
ORGANISM ACTING in it. A turn is four lines and not one: the user's ORDER, the organism's
PROPOSAL with a request to confirm, the user's word, and only then the REPORT — with the folder
counted again. The confirmation is not politeness: it is the seam where a body that may change
the world asks permission, and the corpus that never showed it cannot teach it.

FIVE FRAMES, AND EACH SEALS ITS OWN LAW BY A NUMBER:
  ход       — order, proposal, «да», report, and the folder RECOUNTED («3 + 1 = 4»): an act that
              adds a file adds exactly one;
  отказ     — order, proposal, «нет», and NO act: the folder count is UNCHANGED, and the page
              says so with the same number twice («3 = 3»). A refusal that changed the world
              would be a lie visible in arithmetic, not in tone;
  занято    — the act cannot be done because the file is ALREADY there: no act, count unchanged;
  пусто     — the act cannot be done because the file is NOT there (delete, read, edit): no act,
              count unchanged;
  без_счёта — the act happens and the count does NOT move (read and edit change a file, not the
              folder): «3 = 3» after a DONE act. This is the frame that separates «nothing
              happened» from «something happened that the count cannot see», and a reader that
              conflates them cannot be trusted with a world.

WHAT IS DECLARED HERE: four acts in nine languages, each in three forms (the order, the
infinitive of the proposal, the report), the two role words, the confirmation pair, the folder
sentence with the counting rule of the packs, and the two impossibility phrases. The file names
(a.txt, b.txt) are the same in every language on purpose: the house teaches the ACT, not the
naming of files.

THE RE-ASK CARRIES A QUESTION WORD, AND THAT IS A LAW OF THE CORPUS, NOT A TASTE. The first
draft asked «— подтвердить?» / «— confirm?», and the court of the record refused it: a question
without a declared question word is false BY RECORD (96,6 % of the свод's honest questions carry
one). So the proposal is two sentences — the offer and the question about it («подтверждено ли
это?», «ist das bestätigt?», «czy to potwierdzone?») — and the question word is the pack's own.

ONE WORD GIVEN UP TO A NEIGHBOUR, AND THAT IS A LAW: the folder sentence first said «the folder
HOLDS 1 file», and the court of episodic algebra called nine honest pages false — «holds» is ITS
keyword («A holds N+M X»), and a house that wears a neighbour's keyword is judged by the
neighbour's law. The folder now CONTAINS its files, as it does in the other eight languages.

WHAT IS NOT MEASURED, NAMED: an act over TWO objects (moving a file to another folder), an act
that fails halfway, a confirmation that changes the act («create b.txt instead»), and any world
but a flat folder of files.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import svampforms as S  # noqa: E402 — the count cell of a pack

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
АКТЫ = ("создать", "удалить", "прочитать", "дописать")
# СДВИГ ПАПКИ: создание прибавляет файл, удаление отнимает, чтение и правка не двигают счёта
СДВИГ = {"создать": 1, "удалить": -1, "прочитать": 0, "дописать": 0}
# ЧЕТЫРЕ ИМЕНИ, А НЕ ОДНО (просьба holon к органу мира): дыра ИМЕНИ не рождается
# анти-унификацией, если имя во всех показах одно — рамка покупает дыру объекта из ПОКАЗОВ.
ФАЙЛЫ = ("a.txt", "b.txt", "notes.md", "list.csv")
БАЙТЫ = {"a.txt": 7, "b.txt": 12, "notes.md": 20, "list.csv": 34}
ПРИБАВКА_БАЙТ = 5
# РОД ЛЕДЖЕРА: создание и удаление двигают ПАПКУ, чтение и правка — САМ ФАЙЛ. Без этого
# «прочитал» и «дописал» неразличимы по счёту (оба «N = N»), и род акта не покупается.
РОД_ЛЕДЖЕРА = {"создать": "папка", "удалить": "папка", "прочитать": "байты", "дописать": "байты"}
# СДВИГ БАЙТОВ: чтение не трогает файла, дописывание растит его на объявленную прибавку
СДВИГ_БАЙТ = {"прочитать": 0, "дописать": ПРИБАВКА_БАЙТ}
СОСТОЯНИЯ = (0, 1, 2, 3, 5)
# ГЛАГОЛЫ: (приказ, инфинитив, отчёт) — три формы, которых требуют три роли реплики
ГЛАГОЛЫ = {
    "ru": {"создать": ("создай", "создать", "создал"), "удалить": ("удали", "удалить", "удалил"),
           "прочитать": ("прочитай", "прочитать", "прочитал"),
           "дописать": ("допиши", "дописать", "дописал")},
    "en": {"создать": ("create", "create", "created"), "удалить": ("delete", "delete", "deleted"),
           "прочитать": ("read", "read", "read"), "дописать": ("append to", "append to", "appended to")},
    "de": {"создать": ("erstelle", "erstellen", "erstellt"), "удалить": ("lösche", "löschen", "gelöscht"),
           "прочитать": ("lies", "lesen", "gelesen"), "дописать": ("ergänze", "ergänzen", "ergänzt")},
    "fr": {"создать": ("crée", "créer", "créé"), "удалить": ("supprime", "supprimer", "supprimé"),
           "прочитать": ("lis", "lire", "lu"), "дописать": ("complète", "compléter", "complété")},
    "es": {"создать": ("crea", "crear", "creado"), "удалить": ("elimina", "eliminar", "eliminado"),
           "прочитать": ("lee", "leer", "leído"), "дописать": ("amplía", "ampliar", "ampliado")},
    "it": {"создать": ("crea", "creare", "creato"), "удалить": ("elimina", "eliminare", "eliminato"),
           "прочитать": ("leggi", "leggere", "letto"), "дописать": ("amplia", "ampliare", "ampliato")},
    "pt": {"создать": ("cria", "criar", "criei"), "удалить": ("elimina", "eliminar", "eliminei"),
           "прочитать": ("lê", "ler", "li"), "дописать": ("amplia", "ampliar", "ampliei")},
    "nl": {"создать": ("creëer", "creëren", "gecreëerd"), "удалить": ("verwijder", "verwijderen", "verwijderd"),
           "прочитать": ("lees", "lezen", "gelezen"), "дописать": ("bewerk", "bewerken", "bewerkt")},
    "pl": {"создать": ("utwórz", "utworzyć", "utworzyłem"), "удалить": ("usuń", "usunąć", "usunąłem"),
           "прочитать": ("przeczytaj", "przeczytać", "przeczytałem"),
           "дописать": ("dopisz", "dopisać", "dopisałem")},
}
БАЙТ = {"ru": ("байт", "байта", "байтов"), "en": ("byte", "bytes"), "de": ("Byte", "Byte"),
        "fr": ("octet", "octets"), "es": ("byte", "bytes"), "it": ("byte", "byte"),
        "pt": ("byte", "bytes"), "nl": ("byte", "bytes"), "pl": ("bajt", "bajty", "bajtów")}
ФАЙЛ = {"ru": ("файл", "файла", "файлов"), "en": ("file", "files"), "de": ("Datei", "Dateien"),
        "fr": ("fichier", "fichiers"), "es": ("archivo", "archivos"), "it": ("file", "file"),
        "pt": ("ficheiro", "ficheiros"), "nl": ("bestand", "bestanden"),
        "pl": ("plik", "pliki", "plików")}
РЕЧЬ = {
    "ru": dict(польз="пользователь", орг="организм", файл="файл {f}", нет_файла="файла {f}",
               приказ="{V} {Ф}", предложение="предлагаю {V} {Ф}. подтверждено ли это?",
               отчёт="{V} {Ф}", папка="папка содержит {N}", да="да", нет="нет",
               отказ="подтверждения нет — акт не совершён", есть="{Ф} уже есть — акт не совершён",
               пуст="{НФ} нет — акт не совершён", в_файле="{Ф} содержит {B}", вопрос_счёта="сколько файлов в папке?", двоеточие=": "),
    "en": dict(польз="user", орг="organism", файл="the file {f}", нет_файла="the file {f}",
               приказ="{V} {Ф}", предложение="i propose to {V} {Ф}. is that confirmed?",
               отчёт="{V} {Ф}", папка="the folder contains {N}", да="yes", нет="no",
               отказ="no confirmation — the act is not performed",
               есть="{Ф} is already there — the act is not performed",
               пуст="{НФ} is not there — the act is not performed", в_файле="{Ф} contains {B}", вопрос_счёта="how many files are in the folder?", двоеточие=": "),
    "de": dict(польз="Benutzer", орг="Organismus", файл="die Datei {f}", нет_файла="die Datei {f}",
               приказ="{V} {Ф}", предложение="ich schlage vor, {Ф} zu {V}. ist das bestätigt?",
               отчёт="ich habe {Ф} {V}", папка="der Ordner enthält {N}", да="ja", нет="nein",
               отказ="keine Bestätigung — die Handlung wird nicht ausgeführt",
               есть="{Ф} gibt es schon — die Handlung wird nicht ausgeführt",
               пуст="{НФ} gibt es nicht — die Handlung wird nicht ausgeführt", в_файле="{Ф} enthält {B}", вопрос_счёта="wie viele Dateien sind im Ordner?", двоеточие=": "),
    "fr": dict(польз="utilisateur", орг="organisme", файл="le fichier {f}", нет_файла="le fichier {f}",
               приказ="{V} {Ф}", предложение="je propose de {V} {Ф}. est-ce confirmé ?",
               отчёт="j'ai {V} {Ф}", папка="le dossier contient {N}", да="oui", нет="non",
               отказ="pas de confirmation — l'acte n'est pas exécuté",
               есть="{Ф} existe déjà — l'acte n'est pas exécuté",
               пуст="{НФ} n'existe pas — l'acte n'est pas exécuté", в_файле="{Ф} contient {B}", вопрос_счёта="combien de fichiers y a-t-il dans le dossier ?", двоеточие=" : "),
    "es": dict(польз="usuario", орг="organismo", файл="el archivo {f}", нет_файла="el archivo {f}",
               приказ="{V} {Ф}", предложение="propongo {V} {Ф}. ¿es correcto?",
               отчёт="he {V} {Ф}", папка="la carpeta contiene {N}", да="sí", нет="no",
               отказ="sin confirmación — el acto no se realiza",
               есть="{Ф} ya existe — el acto no se realiza",
               пуст="{НФ} no existe — el acto no se realiza", в_файле="{Ф} contiene {B}", вопрос_счёта="¿cuántos archivos hay en la carpeta?", двоеточие=": "),
    "it": dict(польз="utente", орг="organismo", файл="il file {f}", нет_файла="il file {f}",
               приказ="{V} {Ф}", предложение="propongo di {V} {Ф}. è confermato?",
               отчёт="ho {V} {Ф}", папка="la cartella contiene {N}", да="sì", нет="no",
               отказ="nessuna conferma — l'atto non viene eseguito",
               есть="{Ф} esiste già — l'atto non viene eseguito",
               пуст="{НФ} non esiste — l'atto non viene eseguito", в_файле="{Ф} contiene {B}", вопрос_счёта="quanti file ci sono nella cartella?", двоеточие=": "),
    "pt": dict(польз="utilizador", орг="organismo", файл="o ficheiro {f}", нет_файла="o ficheiro {f}",
               приказ="{V} {Ф}", предложение="proponho {V} {Ф}. é confirmado?",
               отчёт="{V} {Ф}", папка="a pasta contém {N}", да="sim", нет="não",
               отказ="sem confirmação — o ato não é realizado",
               есть="{Ф} já existe — o ato não é realizado",
               пуст="{НФ} não existe — o ato não é realizado", в_файле="{Ф} contém {B}", вопрос_счёта="quantos ficheiros há na pasta?", двоеточие=": "),
    "nl": dict(польз="gebruiker", орг="organisme", файл="het bestand {f}", нет_файла="het bestand {f}",
               приказ="{V} {Ф}", предложение="ik stel voor {Ф} te {V}. is dat bevestigd?",
               отчёт="ik heb {Ф} {V}", папка="de map bevat {N}", да="ja", нет="nee",
               отказ="geen bevestiging — de handeling wordt niet uitgevoerd",
               есть="{Ф} bestaat al — de handeling wordt niet uitgevoerd",
               пуст="{НФ} bestaat niet — de handeling wordt niet uitgevoerd", в_файле="{Ф} bevat {B}", вопрос_счёта="hoeveel bestanden zitten er in de map?", двоеточие=": "),
    "pl": dict(польз="użytkownik", орг="organizm", файл="plik {f}", нет_файла="pliku {f}",
               приказ="{V} {Ф}", предложение="proponuję {V} {Ф}. czy to potwierdzone?",
               отчёт="{V} {Ф}", папка="folder zawiera {N}", да="tak", нет="nie",
               отказ="brak potwierdzenia — akt nie zostaje wykonany",
               есть="{Ф} już istnieje — akt nie zostaje wykonany",
               пуст="{НФ} nie ma — akt nie zostaje wykonany", в_файле="{Ф} zawiera {B}", вопрос_счёта="ile plików jest w folderze?", двоеточие=": "),
}
ФОРМЫ = ("ход", "отказ", "занято", "пусто", "без_счёта", "счёт")


def файлов(язык, n):
    """«3 файла», «1 file», «5 plików» — счётное слово папки берётся у правила пакета."""
    return "%d %s" % (n, S._счёт(ФАЙЛ[язык], n, язык))


def байтов(язык, n):
    """«7 байт», «12 bajtów» — счётное слово размера берётся у правила пакета."""
    return "%d %s" % (n, S._счёт(БАЙТ[язык], n, язык))


def _реплика(язык, кто, что):
    return РЕЧЬ[язык][кто] + РЕЧЬ[язык]["двоеточие"] + что


def леджер(было, сдвиг):
    """Счёт папки до и после акта: прибавление, отнятие или РАВЕНСТВО там, где акт не виден."""
    стало = было + сдвиг
    if сдвиг > 0:
        return f"{было} + {сдвиг} = {стало}", стало
    if сдвиг < 0:
        return f"{было} − {-сдвиг} = {стало}", стало
    return f"{было} = {было}", было


def наблюдение(язык, акт, форма, было, файл):
    """Чем запечатан ход: ПАПКОЙ (создание, удаление, невозможное) или САМИМ ФАЙЛОМ (чтение,
    правка). Род леджера принадлежит акту: без этого «прочитал» и «дописал» неразличимы."""
    р = РЕЧЬ[язык]
    байтовый = РОД_ЛЕДЖЕРА.get(акт) == "байты" and форма in ("без_счёта", "отказ")
    if байтовый:
        б = БАЙТЫ[файл]
        сдвиг = СДВИГ_БАЙТ[акт] if форма == "без_счёта" else 0
        счёт, стало = леджер(б, сдвиг)
        Ф = р["файл"].format(f=файл)
        return р["в_файле"].format(Ф=Ф, B=байтов(язык, стало)) + р["двоеточие"] + счёт + "."
    сдвиг = СДВИГ[акт] if форма in ("ход", "без_счёта") else 0
    счёт, стало = леджер(было, сдвиг)
    return р["папка"].format(N=файлов(язык, стало)) + р["двоеточие"] + счёт + "."


def страница(язык, форма, акт, было, файл=ФАЙЛЫ[0]):
    р = РЕЧЬ[язык]
    приказ_в, инф_в, отчёт_в = ГЛАГОЛЫ[язык][акт]
    Ф = р["файл"].format(f=файл)
    НФ = р["нет_файла"].format(f=файл)
    приказ = _реплика(язык, "польз", р["приказ"].format(V=приказ_в, Ф=Ф) + ".")
    хвост = наблюдение(язык, акт, форма, было, файл)
    if форма == "счёт":
        # НАБЛЮДЕНИЕ БЕЗ АКТА: вопрос о числе файлов и ответ с тем же числом
        return (_реплика(язык, "польз", р["вопрос_счёта"]) + " "
                + _реплика(язык, "орг", р["папка"].format(N=файлов(язык, было))
                           + р["двоеточие"] + f"{было} = {было}."))
    if форма in ("занято", "пусто"):
        # АКТ НЕВОЗМОЖЕН: организм говорит ПОЧЕМУ, а счёт папки СПРАШИВАЕТСЯ пользователем —
        # так неподвижность мира не объявляется, а ПРОВЕРЯЕТСЯ вопросом (храповик вопросной
        # поверхности: рамка без вопроса учит форме и не даёт о ней спросить).
        причина = (р["есть"] if форма == "занято" else р["пуст"]).format(Ф=Ф, НФ=НФ)
        return (приказ + " " + _реплика(язык, "орг", причина + ".") + " "
                + _реплика(язык, "польз", р["вопрос_счёта"]) + " "
                + _реплика(язык, "орг", хвост))
    предложение = _реплика(язык, "орг", р["предложение"].format(V=инф_в, Ф=Ф))
    if форма == "отказ":
        # ОТКАЗ ПРОВЕРЯЕТСЯ ЧИСЛОМ: несовершённый акт не двигает папки
        return (приказ + " " + предложение + " " + _реплика(язык, "польз", р["нет"] + ".")
                + " " + _реплика(язык, "орг", р["отказ"] + ". " + хвост))
    return (приказ + " " + предложение + " " + _реплика(язык, "польз", р["да"] + ".")
            + " " + _реплика(язык, "орг", р["отчёт"].format(V=отчёт_в, Ф=Ф) + ". " + хвост))


def _годно(форма, акт, было):
    """Какие сочетания мир допускает: удалить из пустой папки нельзя, создать поверх — «занято»."""
    if форма == "счёт":
        # НАБЛЮДЕНИЕ БЕЗ АКТА пишется ОДИН раз, а не по разу на каждый род акта
        return акт == АКТЫ[0]
    if форма == "ход":
        return СДВИГ[акт] != 0 and (было > 0 or акт == "создать")
    if форма == "без_счёта":
        return СДВИГ[акт] == 0 and было > 0
    if форма == "занято":
        return акт == "создать" and было > 0
    if форма == "пусто":
        return акт != "создать" and было == 0
    return было > 0 or акт == "создать"


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for i, акт in enumerate(АКТЫ):
            for j, было in enumerate(СОСТОЯНИЯ):
                for k, форма in enumerate(ФОРМЫ):
                    if _годно(форма, акт, было):
                        # ИМЯ ФАЙЛА ХОДИТ ПО СТРАНИЦАМ: дыра имени не рождается там, где имя одно
                        файл = ФАЙЛЫ[(i + j + k) % len(ФАЙЛЫ)]
                        вон[страница(язык, форма, акт, было, файл)] = (язык, форма)
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    сорт = sorted({с for с in слова if с}, key=lambda с: (-len(с), с))
    return "(?:" + "|".join(re.escape(с) for с in сорт) + ")"


def _дыры(язык):
    файлы = _альт(ФАЙЛЫ)
    счёт = r"\d+ " + _альт(ФАЙЛ[язык])
    байты = r"\d+ " + _альт(БАЙТ[язык])
    return {"f": файлы, "f2": файлы, "f3": файлы, "f4": файлы, "f5": файлы,
            "N": счёт, "B": байты,
            "V1": _альт(г[0] for г in ГЛАГОЛЫ[язык].values()),
            "V2": _альт(г[1] for г in ГЛАГОЛЫ[язык].values()),
            "V3": _альт(г[2] for г in ГЛАГОЛЫ[язык].values()),
            "было": r"\d+", "стало": r"\d+", "сдв": r"\d+"}


def рамка(язык, форма, акт, скрещено=None):
    """Рамка хода с дырами; сдвиг счёта — часть рамки, ибо его знак задан РОДОМ акта.

    ДВЕ СКРЕЩЁННЫЕ РАМКИ — ПРОТИВ НЕМОТЫ НА ГЛАВНОЙ ЛЖИ ЭТОГО ДОМА.
      «без_подтверждения» — ход, из которого вынута реплика «да»: приказ, предложение и СРАЗУ
          отчёт. Это первая ложь, которой боится сцена релиза (тело сделало неподтверждённое), и
          суд, молчащий о ней, бесполезен. Строение хода — четыре реплики; вынутая реплика ловится
          не значением, а РАМКОЙ, и потому рамка объявлена отдельно.
      «сдвинутый счёт» — отказ или невозможный акт, в чьём леджере счёт ДВИЖЕТСЯ. Мир, не
          тронутый актом, не может изменить числа; страница, где он изменился, есть ложь, а не
          чужая рамка.
    """
    р = РЕЧЬ[язык]
    Ф1, Ф2, Ф3 = (р["файл"].format(f="{f}"), р["файл"].format(f="{f2}"), р["файл"].format(f="{f3}"))
    НФ = р["нет_файла"].format(f="{f2}")
    приказ = _реплика(язык, "польз", р["приказ"].format(V="{V1}", Ф=Ф1) + ".")
    байтовый = РОД_ЛЕДЖЕРА.get(акт) == "байты" and форма in ("без_счёта", "отказ")
    сдвиг = (СДВИГ_БАЙТ[акт] if форма == "без_счёта" else 0) if байтовый else (
        СДВИГ[акт] if форма in ("ход", "без_счёта") else 0)
    счёт = ("{было} + {сдв} = {стало}" if сдвиг > 0 else
            "{было} − {сдв} = {стало}" if сдвиг < 0 else "{было} = {стало}")
    хвост = ((р["в_файле"].format(Ф=р["файл"].format(f="{f5}"), B="{B}") if байтовый
              else р["папка"].format(N="{N}")) + р["двоеточие"] + счёт + ".")
    if форма == "счёт":
        return (_реплика(язык, "польз", р["вопрос_счёта"]) + " "
                + _реплика(язык, "орг", р["папка"].format(N="{N}") + р["двоеточие"]
                           + "{было} = {стало}."))
    if скрещено == "сдвинутый счёт":
        # НЕ ТРОНУТЫЙ МИР НЕ МЕНЯЕТ ЧИСЛА: любой движущийся леджер здесь — ложь
        счёт = "{было} + {сдв} = {стало}" if СДВИГ[акт] >= 0 else "{было} − {сдв} = {стало}"
        хвост = р["папка"].format(N="{N}") + р["двоеточие"] + счёт + "."
    if форма in ("занято", "пусто"):
        причина = (р["есть"] if форма == "занято" else р["пуст"]).format(Ф=Ф2, НФ=НФ)
        return (приказ + " " + _реплика(язык, "орг", причина + ".") + " "
                + _реплика(язык, "польз", р["вопрос_счёта"]) + " "
                + _реплика(язык, "орг", хвост))
    предложение = _реплика(язык, "орг", р["предложение"].format(V="{V2}", Ф=Ф2))
    if скрещено == "без_подтверждения":
        # ОТЧЁТ БЕЗ СЛОВА ПОЛЬЗОВАТЕЛЯ: тело сделало неподтверждённое
        return (приказ + " " + предложение + " "
                + _реплика(язык, "орг", р["отчёт"].format(V="{V3}", Ф=Ф3) + ". " + хвост))
    if форма == "отказ":
        return (приказ + " " + предложение + " " + _реплика(язык, "польз", р["нет"] + ".")
                + " " + _реплика(язык, "орг", р["отказ"] + ". " + хвост))
    return (приказ + " " + предложение + " " + _реплика(язык, "польз", р["да"] + ".")
            + " " + _реплика(язык, "орг", р["отчёт"].format(V="{V3}", Ф=Ф3) + ". " + хвост))


def _образец(язык, форма, акт, скрещено=None):
    дыры, счёт, куски = _дыры(язык), {}, []
    for кусок in re.split(r"(\{[^}]+\})", рамка(язык, форма, акт, скрещено)):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = ([(_образец(язык, форма, акт), язык, форма, акт, None)
            for язык in ЯЗЫКИ for форма in ФОРМЫ for акт in АКТЫ
            if any(_годно(форма, акт, б) for б in СОСТОЯНИЯ)]
           + [(_образец(язык, "ход", акт, "без_подтверждения"), язык, "ход", акт, "без_подтверждения")
              for язык in ЯЗЫКИ for акт in АКТЫ]
           + [(_образец(язык, форма, акт, "сдвинутый счёт"), язык, форма, акт, "сдвинутый счёт")
              for язык in ЯЗЫКИ for форма in ("отказ", "занято", "пусто") for акт in АКТЫ
              if any(_годно(форма, акт, б) for б in СОСТОЯНИЯ)])


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _акт_по_форме(язык, ступень, слово):
    for акт in АКТЫ:
        if ГЛАГОЛЫ[язык][акт][ступень] == слово:
            return акт
    return None


def _вердикт(язык, форма, акт, зн):
    if форма == "счёт":
        # НАБЛЮДЕНИЕ БЕЗ АКТА: число папки называется дважды и обязано быть одним
        было, стало = int(зн["было"]), int(зн["стало"])
        return было == стало and зн["N"] == файлов(язык, было)
    # ОДИН ХОД — ОДИН АКТ И ОДИН ФАЙЛ: приказ, предложение и отчёт говорят об одном
    файлы = {зн[к] for к in ("f", "f2", "f3", "f5") if к in зн}
    if len(файлы) != 1:
        return False
    ступени = [(0, "V1"), (1, "V2"), (2, "V3")]
    роды = {_акт_по_форме(язык, ст, зн[к]) for ст, к in ступени if к in зн}
    if roды_плохи(роды, акт):
        return False
    было, стало = int(зн["было"]), int(зн["стало"])
    байтовый = РОД_ЛЕДЖЕРА.get(акт) == "байты" and форма in ("без_счёта", "отказ")
    if байтовый:
        # ЛЕДЖЕР ФАЙЛА: «было» есть объявленный размер ЭТОГО файла, и он двигается лишь правкой
        файл = list(файлы)[0]
        сдвиг = СДВИГ_БАЙТ[акт] if форма == "без_счёта" else 0
        _с, ожидаемое = леджер(БАЙТЫ[файл], сдвиг)
        if было != БАЙТЫ[файл] or стало != ожидаемое or зн["B"] != байтов(язык, ожидаемое):
            return False
        return сдвиг == 0 or int(зн["сдв"]) == сдвиг
    сдвиг = СДВИГ[акт] if форма in ("ход", "без_счёта") else 0
    если_счёт, ожидаемое = леджер(было, сдвиг)
    if стало != ожидаемое or зн["N"] != файлов(язык, ожидаемое):
        return False
    if сдвиг != 0 and int(зн["сдв"]) != abs(сдвиг):
        return False
    # МИР ДОПУСКАЕТ НЕ ВСЯКИЙ ХОД: удалить из пустой папки нельзя, создать поверх — «занято»
    return _годно(форма, акт, было)


def roды_плохи(роды, акт):
    return len(роды) != 1 or акт not in роды


def судить(строка):
    """(судимо, истинно): a turn of the house whose folder recounts by the act; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма, акт, скрещено in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        if скрещено:
            return True, False
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(язык, форма, акт, зн)
    return False, False


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        х = страница(язык, "ход", "создать", 3)
        assert судить(х) == (True, True), х
        # (1) ПАПКА НЕ ПЕРЕСЧИТАНА ПОСЛЕ АКТА
        битая = х.replace("3 + 1 = 4", "3 + 1 = 3").replace(файлов(язык, 4), файлов(язык, 3))
        assert судить(битая) == (True, False), битая
        о = страница(язык, "отказ", "создать", 3)
        assert судить(о) == (True, True), о
        # (2) ОТКАЗ СДВИНУЛ МИР: несовершённый акт прибавил файл
        битая = о.replace("3 = 3", "3 + 1 = 4").replace(файлов(язык, 3), файлов(язык, 4))
        assert судить(битая) == (True, False), битая
        # (2б) ОТЧЁТ БЕЗ ПОДТВЕРЖДЕНИЯ: реплика «да» вынута из хода
        да = _реплика(язык, "польз", РЕЧЬ[язык]["да"] + ".") + " "
        битая = х.replace(да, "")
        assert судить(битая) == (True, False), битая
        з = страница(язык, "занято", "создать", 2)
        assert судить(з) == (True, True), з
        # (3) НЕВОЗМОЖНЫЙ АКТ ОБЪЯВЛЕН НАД ПУСТОЙ ПАПКОЙ
        битая = з.replace(файлов(язык, 2), файлов(язык, 0)).replace("2 = 2", "0 = 0")
        assert судить(битая) == (True, False), битая
        б = страница(язык, "без_счёта", "прочитать", 3)
        assert судить(б) == (True, True), б
        # (4) ЧТЕНИЕ СДВИНУЛО СВОЙ ЛЕДЖЕР: файл вырос от того, что его прочли
        битая = б.replace("7 = 7", "7 + 5 = 12").replace(байтов(язык, 7), байтов(язык, 12))
        assert судить(битая) == (True, False), битая
        д = страница(язык, "без_счёта", "дописать", 3)
        assert судить(д) == (True, True), д
        # (4б) ПРАВКА НЕ СДВИНУЛА ЛЕДЖЕРА: дописал, а файл прежнего размера
        битая = д.replace("7 + 5 = 12", "7 = 7").replace(байтов(язык, 12), байтов(язык, 7))
        assert судить(битая) == (True, False), битая
        с2 = страница(язык, "счёт", "создать", 3)
        assert судить(с2) == (True, True), с2
        # (4в) НАБЛЮДЕНИЕ БЕЗ АКТА ЛЖЁТ ЧИСЛОМ: спрошено о папке, названо чужое число
        битая = с2.replace("3 = 3", "3 = 4").replace(файлов(язык, 3), файлов(язык, 4))
        assert судить(битая) == (True, False), битая
        # (5) ДВА РОДА АКТА В ОДНОМ ХОДЕ: приказано создать, отчитано об удалении
        битая = х.replace(ГЛАГОЛЫ[язык]["создать"][2], ГЛАГОЛЫ[язык]["удалить"][2])
        assert судить(битая) == (True, False), битая
        # (6) ДВА ФАЙЛА В ОДНОМ ХОДЕ
        битая = х.replace(ФАЙЛЫ[0], ФАЙЛЫ[1], 1)
        assert судить(битая) == (True, False), битая
        мутанты += 10
        # (9) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        голова = х[:х.index("?") + 1]
        вопрос = голова[голова.rindex(". ") + 2:] if ". " in голова else голова
        assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "ход", "создать", 0))
    for язык in ("ru", "de", "pl"):
        print("  ", страница(язык, "отказ", "удалить", 2))
        print("  ", страница(язык, "пусто", "прочитать", 0))
        print("  ", страница(язык, "без_счёта", "дописать", 3))
    по_форме = {}
    for _, (_я, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, актов {len(АКТЫ)}, "
          f"образцов {len(ОБРАЗЦЫ)}): " + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
