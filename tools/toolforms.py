#!/usr/bin/env python3
"""THE HOUSE OF THE TOOL — state before · call · state after (05.09).

The agent's architecture (holon) asks the corpus for the plainest thing a tool-using
organism must read: an ACT changes a count, and the question asks the state AFTER. Three
acts add, one takes away, one moves between two places — and one act CHANGES NOTHING, and
says so in its own words. Idempotence is not a label here but a QUORUM: the same page shows
the act once and twice, and the reader sees that creating twice moves the count twice while
reading twice moves it not at all.

WHAT THE HOUSE DECLARES AND WHAT IT BORROWS. Nine languages; the things of acts (files,
records, messages, lines) are declared HERE with their count forms — they are not the
things of the action-pages house, because a tool's world is files and lines, not coins and
balls; the count cell is the pack's own agreement rule (langpack, through the SVAMP house's
reader), the question word bends by the thing's gender (the SVAMP house's table of gendered
holes), the copula of a place bends by the number where the language bends it. Places are
whole prepositional phrases («в папке», «im Ordner», «na liście») — one declaration, no
guessing at cases; the two folders of a move are named A and B, and every case of their
names stands written in the frame.

THE ACT IS NAMED, NOT ACTED. Nothing here executes: a page says what the act does and what
the count becomes, and the ledger recomputes it. The act that reads says «reading changes
nothing» — a declared sentence of every language, and the judge demands both the unchanged
number and that sentence: an answer that changes the count on a read is a lie, and an
answer that keeps the count without the ground is not a page of this house.

WHAT IS NOT MEASURED, NAMED: whether a real file system would do this. The house shows the
SHAPE of a tool call (before, call, after), not its execution; the effects of a shell are a
neighbouring world and are not written here.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import svampforms as S  # noqa: E402 — the count cell of a pack and the gendered question words

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
ВЕРХ = 30                      # the row of numbers the house walks: 1..30

# ВЕЩИ АКТОВ — объявлены здесь, а не взяты у соседей: мир инструмента есть файлы, строки,
# записи и сообщения. Пара форм у языков с одним множественным, тройка — у ru и pl (ячейку
# счёта даёт правило пакета, а не дом).
ВЕЩИ = {
    "ru": (("файл", "файла", "файлов"), ("запись", "записи", "записей"), ("сообщение", "сообщения", "сообщений")),
    "en": (("file", "files"), ("record", "records"), ("message", "messages")),
    "de": (("Datei", "Dateien"), ("Eintrag", "Einträge"), ("Nachricht", "Nachrichten")),
    "fr": (("fichier", "fichiers"), ("enregistrement", "enregistrements"), ("message", "messages")),
    "es": (("archivo", "archivos"), ("registro", "registros"), ("mensaje", "mensajes")),
    "it": (("file", "file"), ("voce", "voci"), ("messaggio", "messaggi")),
    "pt": (("ficheiro", "ficheiros"), ("registo", "registos"), ("mensagem", "mensagens")),
    "nl": (("bestand", "bestanden"), ("record", "records"), ("bericht", "berichten")),
    "pl": (("plik", "pliki", "plików"), ("wpis", "wpisy", "wpisów"), ("wiadomość", "wiadomości", "wiadomości")),
}
# СТРОКА ЖИВЁТ В ФАЙЛЕ, а не в папке: у формы «дописал» своя вещь и своё место.
СТРОКА = {
    "ru": ("строка", "строки", "строк"), "en": ("line", "lines"), "de": ("Zeile", "Zeilen"),
    "fr": ("ligne", "lignes"), "es": ("línea", "líneas"), "it": ("riga", "righe"),
    "pt": ("linha", "linhas"), "nl": ("regel", "regels"), "pl": ("linia", "linie", "linii"),
}
В_ФАЙЛЕ = {"ru": "в файле", "en": "in the file", "de": "in der Datei", "fr": "dans le fichier",
           "es": "en el archivo", "it": "nel file", "pt": "no ficheiro", "nl": "in het bestand",
           "pl": "w pliku"}
# МЕСТА — целой предложной фразой (падеж не угадывается): папка, ящик, список.
МЕСТА = {
    "ru": ("в папке", "в ящике", "в списке"),
    "en": ("in the folder", "in the box", "in the list"),
    "de": ("im Ordner", "in der Kiste", "in der Liste"),
    "fr": ("dans le dossier", "dans la boîte", "dans la liste"),
    "es": ("en la carpeta", "en la caja", "en la lista"),
    "it": ("nella cartella", "nella scatola", "nell'elenco"),
    "pt": ("na pasta", "na caixa", "na lista"),
    "nl": ("in de map", "in de doos", "in de lijst"),
    "pl": ("w folderze", "w pudełku", "na liście"),
}
# СЛОВО НЕИЗМЕННОСТИ — основание ответа акта, который ничего не меняет.
НЕИЗМЕННОСТЬ = {
    "ru": "чтение ничего не меняет", "en": "reading changes nothing", "de": "Lesen ändert nichts",
    "fr": "la lecture ne change rien", "es": "leer no cambia nada", "it": "leggere non cambia nulla",
    "pt": "ler não muda nada", "nl": "lezen verandert niets", "pl": "czytanie nic nie zmienia",
}
ДВАЖДЫ = {"ru": "дважды", "en": "twice", "de": "zweimal", "fr": "deux fois", "es": "dos veces",
          "it": "due volte", "pt": "duas vezes", "nl": "twee keer", "pl": "dwa razy"}
# СВЯЗКА МЕСТА ГНЁТСЯ ПО ЧИСЛУ там, где язык её гнёт («there is 1 file» / «there are 3 files»,
# «w folderze jest 5 plików» / «są 3 pliki» — польская связка идёт по счётной ЯЧЕЙКЕ).
ЕСТЬ = {"en": ("there is", "there are"), "de": ("ist", "sind"), "it": ("c'è", "ci sono"),
        "nl": ("ligt", "liggen"), "pl": ("jest", "są")}

РАМКИ = {
    "ru": dict(
        создал="{М} {n} {Тn}. акт создаёт {m} {Тm}. сколько {Тмн} {М} после акта? {М} {v} {Тv}: {n} + {m} = {v}.",
        удалил="{М} {n} {Тn}. акт удаляет {m} {Тm}. сколько {Тмн} {М} после акта? {М} {v} {Тv}: {n} − {m} = {v}.",
        дописал="{МФ} {n} {Тn}. акт дописывает {m} {Тm}. сколько {Тмн} {МФ} после акта? {МФ} {v} {Тv}: {n} + {m} = {v}.",
        прочитал="{М} {n} {Тn}. акт только читает. сколько {Тмн} {М} после акта? {М} {n} {Тn}: {НЕИЗМ}.",
        дважды="{М} {n} {Тn}. акт создаёт {m} {Тm} {ДВ}. сколько {Тмн} {М} после акта? {М} {v} {Тv}: {n} + {m} + {m} = {v}.",
        дважды_чтение="{М} {n} {Тn}. акт только читает {ДВ}. сколько {Тмн} {М} после акта? {М} {n} {Тn}: {НЕИЗМ}.",
        переместил="папка A содержит {n} {Тn}, папка B содержит {k} {Тk}. акт переносит {m} {Тm} из папки A в папку B. сколько {Тмн} содержит папка B после акта? папка B содержит {v} {Тv}: {k} + {m} = {v}.",
        переместил_из="папка A содержит {n} {Тn}, папка B содержит {k} {Тk}. акт переносит {m} {Тm} из папки A в папку B. сколько {Тмн} содержит папка A после акта? папка A содержит {v} {Тv}: {n} − {m} = {v}."),
    "en": dict(
        создал="{ЕСТЬn} {n} {Тn} {М}. the act creates {m} {Тm}. how many {Тмн} are {М} after the act? {ЕСТЬv} {v} {Тv} {М}: {n} + {m} = {v}.",
        удалил="{ЕСТЬn} {n} {Тn} {М}. the act deletes {m} {Тm}. how many {Тмн} are {М} after the act? {ЕСТЬv} {v} {Тv} {М}: {n} − {m} = {v}.",
        дописал="{ЕСТЬn} {n} {Тn} {МФ}. the act appends {m} {Тm}. how many {Тмн} are {МФ} after the act? {ЕСТЬv} {v} {Тv} {МФ}: {n} + {m} = {v}.",
        прочитал="{ЕСТЬn} {n} {Тn} {М}. the act only reads. how many {Тмн} are {М} after the act? {ЕСТЬn} {n} {Тn} {М}: {НЕИЗМ}.",
        дважды="{ЕСТЬn} {n} {Тn} {М}. the act creates {m} {Тm} {ДВ}. how many {Тмн} are {М} after the act? {ЕСТЬv} {v} {Тv} {М}: {n} + {m} + {m} = {v}.",
        дважды_чтение="{ЕСТЬn} {n} {Тn} {М}. the act only reads {ДВ}. how many {Тмн} are {М} after the act? {ЕСТЬn} {n} {Тn} {М}: {НЕИЗМ}.",
        переместил="folder A contains {n} {Тn}, folder B contains {k} {Тk}. the act moves {m} {Тm} from folder A to folder B. how many {Тмн} does folder B contain after the act? folder B contains {v} {Тv}: {k} + {m} = {v}.",
        переместил_из="folder A contains {n} {Тn}, folder B contains {k} {Тk}. the act moves {m} {Тm} from folder A to folder B. how many {Тмн} does folder A contain after the act? folder A contains {v} {Тv}: {n} − {m} = {v}."),
    "de": dict(
        создал="{М} {ЕСТЬn} {n} {Тn}. der Akt erstellt {m} {Тm}. wie viele {Тмн} sind nach dem Akt {М}? {М} {ЕСТЬv} {v} {Тv}: {n} + {m} = {v}.",
        удалил="{М} {ЕСТЬn} {n} {Тn}. der Akt löscht {m} {Тm}. wie viele {Тмн} sind nach dem Akt {М}? {М} {ЕСТЬv} {v} {Тv}: {n} − {m} = {v}.",
        дописал="{МФ} {ЕСТЬn} {n} {Тn}. der Akt hängt {m} {Тm} an. wie viele {Тмн} sind nach dem Akt {МФ}? {МФ} {ЕСТЬv} {v} {Тv}: {n} + {m} = {v}.",
        прочитал="{М} {ЕСТЬn} {n} {Тn}. der Akt liest nur. wie viele {Тмн} sind nach dem Akt {М}? {М} {ЕСТЬn} {n} {Тn}: {НЕИЗМ}.",
        дважды="{М} {ЕСТЬn} {n} {Тn}. der Akt erstellt {m} {Тm} {ДВ}. wie viele {Тмн} sind nach dem Akt {М}? {М} {ЕСТЬv} {v} {Тv}: {n} + {m} + {m} = {v}.",
        дважды_чтение="{М} {ЕСТЬn} {n} {Тn}. der Akt liest nur {ДВ}. wie viele {Тмн} sind nach dem Akt {М}? {М} {ЕСТЬn} {n} {Тn}: {НЕИЗМ}.",
        переместил="Ordner A enthält {n} {Тn}, Ordner B enthält {k} {Тk}. der Akt verschiebt {m} {Тm} von Ordner A nach Ordner B. wie viele {Тмн} enthält Ordner B nach dem Akt? Ordner B enthält {v} {Тv}: {k} + {m} = {v}.",
        переместил_из="Ordner A enthält {n} {Тn}, Ordner B enthält {k} {Тk}. der Akt verschiebt {m} {Тm} von Ordner A nach Ordner B. wie viele {Тмн} enthält Ordner A nach dem Akt? Ordner A enthält {v} {Тv}: {n} − {m} = {v}."),
    "fr": dict(
        создал="il y a {n} {Тn} {М}. l'acte crée {m} {Тm}. combien de {Тмн} y a-t-il {М} après l'acte ? il y a {v} {Тv} {М} : {n} + {m} = {v}.",
        удалил="il y a {n} {Тn} {М}. l'acte supprime {m} {Тm}. combien de {Тмн} y a-t-il {М} après l'acte ? il y a {v} {Тv} {М} : {n} − {m} = {v}.",
        дописал="il y a {n} {Тn} {МФ}. l'acte ajoute {m} {Тm}. combien de {Тмн} y a-t-il {МФ} après l'acte ? il y a {v} {Тv} {МФ} : {n} + {m} = {v}.",
        прочитал="il y a {n} {Тn} {М}. l'acte ne fait que lire. combien de {Тмн} y a-t-il {М} après l'acte ? il y a {n} {Тn} {М} : {НЕИЗМ}.",
        дважды="il y a {n} {Тn} {М}. l'acte crée {m} {Тm} {ДВ}. combien de {Тмн} y a-t-il {М} après l'acte ? il y a {v} {Тv} {М} : {n} + {m} + {m} = {v}.",
        дважды_чтение="il y a {n} {Тn} {М}. l'acte ne fait que lire {ДВ}. combien de {Тмн} y a-t-il {М} après l'acte ? il y a {n} {Тn} {М} : {НЕИЗМ}.",
        переместил="le dossier A contient {n} {Тn}, le dossier B contient {k} {Тk}. l'acte déplace {m} {Тm} du dossier A vers le dossier B. combien de {Тмн} le dossier B contient-il après l'acte ? le dossier B contient {v} {Тv} : {k} + {m} = {v}.",
        переместил_из="le dossier A contient {n} {Тn}, le dossier B contient {k} {Тk}. l'acte déplace {m} {Тm} du dossier A vers le dossier B. combien de {Тмн} le dossier A contient-il après l'acte ? le dossier A contient {v} {Тv} : {n} − {m} = {v}."),
    "es": dict(
        создал="hay {n} {Тn} {М}. el acto crea {m} {Тm}. ¿{кск} {Тмн} hay {М} después del acto? hay {v} {Тv} {М}: {n} + {m} = {v}.",
        удалил="hay {n} {Тn} {М}. el acto borra {m} {Тm}. ¿{кск} {Тмн} hay {М} después del acto? hay {v} {Тv} {М}: {n} − {m} = {v}.",
        дописал="hay {n} {Тn} {МФ}. el acto añade {m} {Тm}. ¿{кск} {Тмн} hay {МФ} después del acto? hay {v} {Тv} {МФ}: {n} + {m} = {v}.",
        прочитал="hay {n} {Тn} {М}. el acto solo lee. ¿{кск} {Тмн} hay {М} después del acto? hay {n} {Тn} {М}: {НЕИЗМ}.",
        дважды="hay {n} {Тn} {М}. el acto crea {m} {Тm} {ДВ}. ¿{кск} {Тмн} hay {М} después del acto? hay {v} {Тv} {М}: {n} + {m} + {m} = {v}.",
        дважды_чтение="hay {n} {Тn} {М}. el acto solo lee {ДВ}. ¿{кск} {Тмн} hay {М} después del acto? hay {n} {Тn} {М}: {НЕИЗМ}.",
        переместил="la carpeta A contiene {n} {Тn}, la carpeta B contiene {k} {Тk}. el acto mueve {m} {Тm} de la carpeta A a la carpeta B. ¿{кск} {Тмн} contiene la carpeta B después del acto? la carpeta B contiene {v} {Тv}: {k} + {m} = {v}.",
        переместил_из="la carpeta A contiene {n} {Тn}, la carpeta B contiene {k} {Тk}. el acto mueve {m} {Тm} de la carpeta A a la carpeta B. ¿{кск} {Тмн} contiene la carpeta A después del acto? la carpeta A contiene {v} {Тv}: {n} − {m} = {v}."),
    "it": dict(
        создал="{ЕСТЬn} {n} {Тn} {М}. l'atto crea {m} {Тm}. {quante} {Тмн} ci sono {М} dopo l'atto? {ЕСТЬv} {v} {Тv} {М}: {n} + {m} = {v}.",
        удалил="{ЕСТЬn} {n} {Тn} {М}. l'atto elimina {m} {Тm}. {quante} {Тмн} ci sono {М} dopo l'atto? {ЕСТЬv} {v} {Тv} {М}: {n} − {m} = {v}.",
        дописал="{ЕСТЬn} {n} {Тn} {МФ}. l'atto aggiunge {m} {Тm}. {quante} {Тмн} ci sono {МФ} dopo l'atto? {ЕСТЬv} {v} {Тv} {МФ}: {n} + {m} = {v}.",
        прочитал="{ЕСТЬn} {n} {Тn} {М}. l'atto solo legge. {quante} {Тмн} ci sono {М} dopo l'atto? {ЕСТЬn} {n} {Тn} {М}: {НЕИЗМ}.",
        дважды="{ЕСТЬn} {n} {Тn} {М}. l'atto crea {m} {Тm} {ДВ}. {quante} {Тмн} ci sono {М} dopo l'atto? {ЕСТЬv} {v} {Тv} {М}: {n} + {m} + {m} = {v}.",
        дважды_чтение="{ЕСТЬn} {n} {Тn} {М}. l'atto solo legge {ДВ}. {quante} {Тмн} ci sono {М} dopo l'atto? {ЕСТЬn} {n} {Тn} {М}: {НЕИЗМ}.",
        переместил="la cartella A contiene {n} {Тn}, la cartella B contiene {k} {Тk}. l'atto sposta {m} {Тm} dalla cartella A alla cartella B. {quante} {Тмн} contiene la cartella B dopo l'atto? la cartella B contiene {v} {Тv}: {k} + {m} = {v}.",
        переместил_из="la cartella A contiene {n} {Тn}, la cartella B contiene {k} {Тk}. l'atto sposta {m} {Тm} dalla cartella A alla cartella B. {quante} {Тмн} contiene la cartella A dopo l'atto? la cartella A contiene {v} {Тv}: {n} − {m} = {v}."),
    "pt": dict(
        создал="há {n} {Тn} {М}. o ato cria {m} {Тm}. {quantas} {Тмн} há {М} depois do ato? há {v} {Тv} {М}: {n} + {m} = {v}.",
        удалил="há {n} {Тn} {М}. o ato apaga {m} {Тm}. {quantas} {Тмн} há {М} depois do ato? há {v} {Тv} {М}: {n} − {m} = {v}.",
        дописал="há {n} {Тn} {МФ}. o ato acrescenta {m} {Тm}. {quantas} {Тмн} há {МФ} depois do ato? há {v} {Тv} {МФ}: {n} + {m} = {v}.",
        прочитал="há {n} {Тn} {М}. o ato apenas lê. {quantas} {Тмн} há {М} depois do ato? há {n} {Тn} {М}: {НЕИЗМ}.",
        дважды="há {n} {Тn} {М}. o ato cria {m} {Тm} {ДВ}. {quantas} {Тмн} há {М} depois do ato? há {v} {Тv} {М}: {n} + {m} + {m} = {v}.",
        дважды_чтение="há {n} {Тn} {М}. o ato apenas lê {ДВ}. {quantas} {Тмн} há {М} depois do ato? há {n} {Тn} {М}: {НЕИЗМ}.",
        переместил="a pasta A contém {n} {Тn}, a pasta B contém {k} {Тk}. o ato move {m} {Тm} da pasta A para a pasta B. {quantas} {Тмн} contém a pasta B depois do ato? a pasta B contém {v} {Тv}: {k} + {m} = {v}.",
        переместил_из="a pasta A contém {n} {Тn}, a pasta B contém {k} {Тk}. o ato move {m} {Тm} da pasta A para a pasta B. {quantas} {Тмн} contém a pasta A depois do ato? a pasta A contém {v} {Тv}: {n} − {m} = {v}."),
    "nl": dict(
        создал="er {ЕСТЬn} {n} {Тn} {М}. de handeling maakt {m} {Тm} aan. hoeveel {Тмн} zijn er {М} na de handeling? er {ЕСТЬv} {v} {Тv} {М}: {n} + {m} = {v}.",
        удалил="er {ЕСТЬn} {n} {Тn} {М}. de handeling verwijdert {m} {Тm}. hoeveel {Тмн} zijn er {М} na de handeling? er {ЕСТЬv} {v} {Тv} {М}: {n} − {m} = {v}.",
        дописал="er {ЕСТЬn} {n} {Тn} {МФ}. de handeling voegt {m} {Тm} toe. hoeveel {Тмн} zijn er {МФ} na de handeling? er {ЕСТЬv} {v} {Тv} {МФ}: {n} + {m} = {v}.",
        прочитал="er {ЕСТЬn} {n} {Тn} {М}. de handeling leest alleen. hoeveel {Тмн} zijn er {М} na de handeling? er {ЕСТЬn} {n} {Тn} {М}: {НЕИЗМ}.",
        дважды="er {ЕСТЬn} {n} {Тn} {М}. de handeling maakt {m} {Тm} {ДВ} aan. hoeveel {Тмн} zijn er {М} na de handeling? er {ЕСТЬv} {v} {Тv} {М}: {n} + {m} + {m} = {v}.",
        дважды_чтение="er {ЕСТЬn} {n} {Тn} {М}. de handeling leest {ДВ} alleen. hoeveel {Тмн} zijn er {М} na de handeling? er {ЕСТЬn} {n} {Тn} {М}: {НЕИЗМ}.",
        переместил="map A bevat {n} {Тn}, map B bevat {k} {Тk}. de handeling verplaatst {m} {Тm} van map A naar map B. hoeveel {Тмн} bevat map B na de handeling? map B bevat {v} {Тv}: {k} + {m} = {v}.",
        переместил_из="map A bevat {n} {Тn}, map B bevat {k} {Тk}. de handeling verplaatst {m} {Тm} van map A naar map B. hoeveel {Тмн} bevat map A na de handeling? map A bevat {v} {Тv}: {n} − {m} = {v}."),
    "pl": dict(
        создал="{М} {ЕСТЬn} {n} {Тn}. akt tworzy {m} {Тm}. ile {Тмн} {ЕСТЬv} {М} po akcie? {М} {ЕСТЬv} {v} {Тv}: {n} + {m} = {v}.",
        удалил="{М} {ЕСТЬn} {n} {Тn}. akt usuwa {m} {Тm}. ile {Тмн} {ЕСТЬv} {М} po akcie? {М} {ЕСТЬv} {v} {Тv}: {n} − {m} = {v}.",
        дописал="{МФ} {ЕСТЬn} {n} {Тn}. akt dopisuje {m} {Тm}. ile {Тмн} {ЕСТЬv} {МФ} po akcie? {МФ} {ЕСТЬv} {v} {Тv}: {n} + {m} = {v}.",
        прочитал="{М} {ЕСТЬn} {n} {Тn}. akt tylko czyta. ile {Тмн} {ЕСТЬn} {М} po akcie? {М} {ЕСТЬn} {n} {Тn}: {НЕИЗМ}.",
        дважды="{М} {ЕСТЬn} {n} {Тn}. akt tworzy {m} {Тm} {ДВ}. ile {Тмн} {ЕСТЬv} {М} po akcie? {М} {ЕСТЬv} {v} {Тv}: {n} + {m} + {m} = {v}.",
        дважды_чтение="{М} {ЕСТЬn} {n} {Тn}. akt tylko czyta {ДВ}. ile {Тмн} {ЕСТЬn} {М} po akcie? {М} {ЕСТЬn} {n} {Тn}: {НЕИЗМ}.",
        переместил="folder A zawiera {n} {Тn}, folder B zawiera {k} {Тk}. akt przenosi {m} {Тm} z folderu A do folderu B. ile {Тмн} zawiera folder B po akcie? folder B zawiera {v} {Тv}: {k} + {m} = {v}.",
        переместил_из="folder A zawiera {n} {Тn}, folder B zawiera {k} {Тk}. akt przenosi {m} {Тm} z folderu A do folderu B. ile {Тмн} zawiera folder A po akcie? folder A zawiera {v} {Тv}: {n} − {m} = {v}."),
}
ФОРМЫ = ("создал", "удалил", "дописал", "прочитал", "дважды", "дважды_чтение", "переместил", "переместил_из")
# ФОРМЫ, ЧЕЙ АКТ НИЧЕГО НЕ МЕНЯЕТ: ответ повторяет число истории и несёт объявленное основание.
НЕИЗМЕННЫЕ = frozenset({"прочитал", "дважды_чтение"})
# ЧТО СЧИТАЕТ ЛЕДЖЕР КАЖДОЙ ФОРМЫ (n — счёт до, k — счёт второго места, m — счёт акта).
ЛЕДЖЕР = {"создал": lambda n, k, m: n + m, "удалил": lambda n, k, m: n - m,
          "дописал": lambda n, k, m: n + m, "дважды": lambda n, k, m: n + 2 * m,
          "переместил": lambda n, k, m: k + m, "переместил_из": lambda n, k, m: n - m}
# ФОРМЫ, ЧЬЯ ВЕЩЬ ЕСТЬ СТРОКА, А МЕСТО — ФАЙЛ
СТРОЧНЫЕ = frozenset({"дописал"})
# РОД ВЕЩЕЙ АКТОВ там, где вопросное слово гнётся (es/it/pt): ключ — форма множественного.
РОД = {
    "es": {"archivos": "m", "registros": "m", "mensajes": "m", "líneas": "f"},
    "it": {"file": "m", "voci": "f", "messaggi": "m", "righe": "f"},
    "pt": {"ficheiros": "m", "registos": "m", "mensagens": "f", "linhas": "f"},
}


def _вещь(язык, форма, Т, c):
    """The count form of the act's thing for c — the pack's own agreement rule."""
    ряд = СТРОКА[язык] if форма in СТРОЧНЫЕ else ВЕЩИ[язык][Т % len(ВЕЩИ[язык])]
    return S._счёт(ряд, c, язык)


def _есть(язык, c):
    """The copula of a place for a count of c, where the language bends it."""
    if язык not in ЕСТЬ:
        return None
    if язык == "pl":
        # польская связка идёт по СЧЁТНОЙ ЯЧЕЙКЕ: «są 3 pliki» (few), «jest 5 plików» (many)
        return ЕСТЬ["pl"][1] if S._ячейка("pl", c) == 1 else ЕСТЬ["pl"][0]
    return ЕСТЬ[язык][0 if c == 1 else 1]


def _поля(язык, форма, Т, n, k, m):
    v = ЛЕДЖЕР[форма](n, k, m) if форма in ЛЕДЖЕР else n
    вещь = lambda c: _вещь(язык, форма, Т, c)
    мн = вещь(5)
    п = dict(n=n, k=k, m=m, v=v, Тn=вещь(n), Тk=вещь(k), Тm=вещь(m), Тv=вещь(v), Тмн=мн,
             М=МЕСТА[язык][Т % len(МЕСТА[язык])], МФ=В_ФАЙЛЕ[язык],
             НЕИЗМ=НЕИЗМЕННОСТЬ[язык], ДВ=ДВАЖДЫ[язык])
    род = РОД.get(язык, {}).get(мн, "f")
    for дыра, (м_, ж_) in S.РОДОВЫЕ.get(язык, {}).items():
        п[дыра] = м_ if род == "m" else ж_
    if язык in ЕСТЬ:
        п["ЕСТЬn"] = _есть(язык, n)
        п["ЕСТЬv"] = _есть(язык, v)
    return п


def страница(язык, форма, Т, n, k=0, m=1, М=None):
    п = _поля(язык, форма, Т, n, k, m)
    if М is not None:
        п["М"] = МЕСТА[язык][М % len(МЕСТА[язык])]
    return РАМКИ[язык][форма].format(**п)


def _пара(n):
    """The second folder's count: never the first one's."""
    k = (n * 5 + 2) % ВЕРХ + 1
    return k if k != n else k % ВЕРХ + 1


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        видов = len(ВЕЩИ[язык])
        мест = len(МЕСТА[язык])
        for n in range(1, ВЕРХ + 1):
            for сдвиг in (0, 1):
                Т = (n + сдвиг) % видов
                М = (n + сдвиг) % мест
                m = 1 + (n + сдвиг) % 3
                вон[страница(язык, "создал", Т, n, m=m, М=М)] = (язык, "создал")
                вон[страница(язык, "прочитал", Т, n, m=m, М=М)] = (язык, "прочитал")
                if n - m >= 1:
                    вон[страница(язык, "удалил", Т, n, m=m, М=М)] = (язык, "удалил")
            m = 1 + n % 3
            Т = n % видов
            вон[страница(язык, "дописал", Т, n, m=m)] = (язык, "дописал")
            вон[страница(язык, "дважды", Т, n, m=m, М=n % мест)] = (язык, "дважды")
            вон[страница(язык, "дважды_чтение", Т, n, m=m, М=n % мест)] = (язык, "дважды_чтение")
            k = _пара(n)
            if n - m >= 1:
                вон[страница(язык, "переместил", Т, n, k=k, m=m)] = (язык, "переместил")
                вон[страница(язык, "переместил_из", Т, n, k=k, m=m)] = (язык, "переместил_из")
    return вон


ПОКАЗЫ = _показы()


def _формы_вещей(язык):
    """count form → the kinds of thing wearing it (a form may belong to several rows)."""
    вон = {}
    for Т in range(len(ВЕЩИ[язык])):
        for c in range(0, ВЕРХ * 3 + 2):
            вон.setdefault(S._счёт(ВЕЩИ[язык][Т], c, язык), set()).add(Т)
    for c in range(0, ВЕРХ * 3 + 2):
        вон.setdefault(S._счёт(СТРОКА[язык], c, язык), set()).add("строка")
    return вон


ФОРМЫ_ВЕЩЕЙ = {язык: _формы_вещей(язык) for язык in ЯЗЫКИ}


def _альт(слова):
    """Branches ordered by content, never by the set's own order (закон детерминизма)."""
    return "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, рамка):
    """One pattern over the whole page; the i-th occurrence of a hole is the group «hole__i»."""
    вещи = _альт(ФОРМЫ_ВЕЩЕЙ[язык])
    дыры = {"n": r"\d+", "k": r"\d+", "m": r"\d+", "v": r"\d+",
            "Тn": вещи, "Тk": вещи, "Тm": вещи, "Тv": вещи, "Тмн": вещи,
            "М": _альт(МЕСТА[язык]), "МФ": re.escape(В_ФАЙЛЕ[язык]),
            "НЕИЗМ": _альт(НЕИЗМЕННОСТЬ.values()), "ДВ": re.escape(ДВАЖДЫ[язык])}
    if язык in ЕСТЬ:
        дыры["ЕСТЬn"] = _альт(ЕСТЬ[язык])
        дыры["ЕСТЬv"] = _альт(ЕСТЬ[язык])
    for дыра, пара in S.РОДОВЫЕ.get(язык, {}).items():
        дыры[дыра] = _альт(пара)
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", рамка):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, рамка), язык, форма)
           for язык, рамки in РАМКИ.items() for форма, рамка in рамки.items()]


def _вердикт(язык, форма, м):
    """The ledger recomputes; a repeated hole carries one value; a read changes nothing."""
    значения = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in значения and значения[дыра] != знач:
            return False
        значения[дыра] = знач
    n = int(значения["n"])
    m = int(значения.get("m", 0))
    k = int(значения.get("k", 0))
    if not (1 <= n <= ВЕРХ):
        return False
    # СЧЁТНАЯ ФОРМА ЕСТЬ ФОРМА СВОЕГО ЧИСЛА, И ВСЕ ФОРМЫ СТРАНИЦЫ — ФОРМЫ ОДНОЙ ВЕЩИ
    виды = None
    for дыра, число in (("Тn", n), ("Тk", k), ("Тm", m), ("Тv", int(значения.get("v", n)))):
        if дыра not in значения:
            continue
        свои = {Т for Т in ФОРМЫ_ВЕЩЕЙ[язык].get(значения[дыра], set())
                if S._счёт(СТРОКА[язык] if Т == "строка" else ВЕЩИ[язык][Т], число, язык) == значения[дыра]}
        if not свои:
            return False
        виды = свои if виды is None else виды & свои
        if not виды:
            return False
    if "Тмн" in значения:
        виды = (виды or set()) & ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тмн"], set())
        if not виды:
            return False
    # СТРОКА ЖИВЁТ В ФАЙЛЕ: форма «дописал» пишет строки, прочие формы — вещи актов
    if форма in СТРОЧНЫЕ and виды != {"строка"}:
        return False
    if форма not in СТРОЧНЫЕ and "строка" in (виды or set()):
        return False
    # ЛЕДЖЕР ПЕРЕСЧИТЫВАЕТСЯ; АКТ, КОТОРЫЙ НИЧЕГО НЕ МЕНЯЕТ, ПОВТОРЯЕТ ЧИСЛО ИСТОРИИ
    if форма in НЕИЗМЕННЫЕ:
        if "v" in значения:
            return False
        if значения.get("НЕИЗМ") != НЕИЗМЕННОСТЬ[язык]:
            return False
    else:
        if "v" not in значения:
            return False
        if int(значения["v"]) != ЛЕДЖЕР[форма](n, k, m):
            return False
        if int(значения["v"]) < 0:
            return False
    # СВЯЗКА МЕСТА ПО ЧИСЛУ
    for дыра, число in (("ЕСТЬn", n), ("ЕСТЬv", int(значения.get("v", n)))):
        if дыра in значения and значения[дыра] != _есть(язык, число):
            return False
    # ВОПРОСНОЕ СЛОВО ПО РОДУ ВЕЩИ
    for дыра, пара in S.РОДОВЫЕ.get(язык, {}).items():
        if дыра in значения and "Тмн" in значения:
            род = РОД.get(язык, {}).get(значения["Тмн"], "f")
            if значения[дыра] != (пара[0] if род == "m" else пара[1]):
                return False
    return True


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose ledger holds; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма in ОБРАЗЦЫ:
        м = образ.match(с)
        if м:
            return True, _вердикт(язык, форма, м)
    return False, False


def _хвост(с):
    """The start of the answer (after the last question mark)."""
    м = list(re.finditer(r"[?？] ", с))
    return м[-1].end() if м else 0


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        # (1) АКТ ЧТЕНИЯ ИЗМЕНИЛ СЧЁТ
        ч = страница(язык, "прочитал", 0, 12, m=1, М=0)
        assert судить(ч) == (True, True), ч
        хв = _хвост(ч)
        битая = ч[:хв] + ч[хв:].replace("12", "13", 1)
        assert судить(битая) == (True, False), битая
        # (2) ЛЕДЖЕР НЕ СХОДИТСЯ (число ответа и леджера согласны, но арифметика лжёт)
        с = страница(язык, "создал", 0, 12, m=2, М=0)
        assert судить(с) == (True, True), с
        битая = с[:_хвост(с)] + с[_хвост(с):].replace("14", "15")
        assert судить(битая) == (True, False), битая
        # (3) ОТВЕТ НЕ РАВЕН ИТОГУ ЛЕДЖЕРА (одна из двух копий дыры подменена)
        хвост = с[_хвост(с):]
        битая = с[:_хвост(с)] + хвост.replace("14", "15", 1)
        assert судить(битая) == (True, False), битая
        # (4) «ДВАЖДЫ» ПОСЧИТАНО КАК ОДИН РАЗ
        д = страница(язык, "дважды", 0, 12, m=2, М=0)
        assert судить(д) == (True, True), д
        битая = д[:_хвост(д)] + д[_хвост(д):].replace("16", "14")
        assert судить(битая) == (True, False), битая
        # (5) ПЕРЕНОС ИЗМЕНИЛ НЕ ТУ ПАПКУ (ответ о папке B посчитан убылью папки A)
        п = страница(язык, "переместил", 0, 12, k=20, m=2)
        assert судить(п) == (True, True), п
        битая = п[:_хвост(п)] + п[_хвост(п):].replace("22", "10")
        assert судить(битая) == (True, False), битая
        # (6) ЧТЕНИЕ БЕЗ ОСНОВАНИЯ: слово неизменности заменено чужим языком
        чужое = next(сл for яз, сл in НЕИЗМЕННОСТЬ.items() if яз != язык)
        битая = ч.replace(НЕИЗМЕННОСТЬ[язык], чужое)
        assert судить(битая) == (True, False), битая
        мутанты += 6
    for язык, форма, аргс in (("ru", "создал", (0, 3, 0, 1)), ("en", "создал", (0, 3, 0, 1)),
                              ("ru", "прочитал", (0, 3, 0, 1)), ("de", "дописал", (0, 12, 0, 5)),
                              ("pl", "переместил", (0, 5, 2, 1)), ("es", "дважды", (0, 3, 0, 1)),
                              ("it", "удалил", (1, 9, 0, 2)), ("pt", "дважды_чтение", (2, 7, 0, 1)),
                              ("nl", "переместил_из", (0, 5, 2, 1)), ("fr", "дописал", (0, 12, 0, 5))):
        print("  ", страница(язык, форма, аргс[0], аргс[1], k=аргс[2], m=аргс[3]))
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
