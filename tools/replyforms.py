#!/usr/bin/env python3
"""ДОМ ОТКЛИКА — совет собеседнику, ОПЁРТЫЙ НА ОБЪЯВЛЕННЫЙ ЗАКОН.

Заказ владельца о «базовых поведенческих и психологических законах» был закрыт
наполовину: дом поведения даёт ЗАКОН («когда человек устал, он ошибается
чаще»), но не даёт его ПРИМЕНЕНИЯ К СОБЕСЕДНИКУ. Человек называет своё
состояние — и ответ обязан быть не сочувствием без опоры, а советом, за
которым стоит проверяемый закон:

    я устал. что мне делать? отдохни: когда человек устал, он ошибается чаще.
    мне страшно. почему? ты не знаешь, что будет: когда человек не знает, что
        будет, он боится.

ЗАКОН НЕ ПИШЕТСЯ ЗДЕСЬ ЗАНОВО, А БЕРЁТСЯ У ДОМА ПОВЕДЕНИЯ. Оттого суд
проверяем сличением с соседом, а не вкусом: закон в отклике обязан совпасть
слово в слово с `behaviorforms.страница(язык, "закон", род)`, и подмена
ловится машинально. Этим же снята опасность двух домов, говорящих о человеке
разное (М-172, прибор согласия домов).

ГОЛОВА ВОПРОСА ВЫБИРАЕТСЯ ПО РОДУ, и это не украшение. Об усталости, голоде и
спешке спрашивают ЧТО ДЕЛАТЬ — состояние поправимо действием; о страхе,
привычке и упущенном внимании спрашивают ПОЧЕМУ — тут поправлять нечего, тут
надо понять. Деление объявлено родами, а не угадано по словам.

СОЧУВСТВЕННАЯ ПАРА ОБЪЯВЛЕНА, НО ПОКАЗОМ НЕ ПИШЕТСЯ, и это названный предел.
holon (04.09) подтвердил, что «мне грустно» → «жаль это слышать» есть законный
род ОБМЕНА: «обмен есть род, в котором ответ законен без основания — ровно как
приветствие», и третья фраза с основанием была бы натяжкой («грусть проходит
быстрее, когда её называют» есть мнение, а не закон, и не проверяемо ни
пересчётом, ни соседом). Но такая строка не несёт ВОПРОСА, а прибор ШИРОТЫ
ВОПРОСА стережёт абсолютное число родов без вопросной поверхности, и расти ему
нельзя. Пара объявлена таблицей `СОЧУВСТВИЕ` — она готова к покупке рынком
обмена напрямую, из объявления, а не из показа. Это первый случай, когда дом
объявляет форму ДЛЯ СОСЕДА, не записывая её себе.

    python3 tools/replyforms.py    # самопроверка с мутантами
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import behaviorforms as B  # noqa: E402

# роды дома поведения: 0 усталость, 1 голод, 2 страх, 3 спешка, 4 привычка, 5 внимание
ДЕЙСТВИЕ = (0, 1, 3)      # спрашивают ЧТО ДЕЛАТЬ — состояние поправимо
ПРИЧИНА = (2, 4, 5)       # спрашивают ПОЧЕМУ — поправлять нечего, надо понять

ЯЗЫКИ_ДОМА = {
    "ru": dict(что="что мне делать?", почему="почему?",
               пары=(("я устал", "отдохни"), ("я голоден", "поешь"),
                     ("мне страшно", "ты не знаешь, что будет"), ("я спешу", "не торопись"),
                     ("я делаю это каждый день", "это привычка"),
                     ("я не заметил знака", "ты смотрел в другую сторону")),
               сочувствие=(("мне грустно", "жаль это слышать"),
                           ("мне тревожно", "расскажи, что случилось"),
                           ("мне хорошо", "рад это слышать"))),
    "en": dict(что="what should i do?", почему="why?",
               пары=(("i am tired", "take a rest"), ("i am hungry", "have something to eat"),
                     ("i am afraid", "you do not know what will happen"), ("i am in a hurry", "do not rush"),
                     ("i do this every day", "that is a habit"),
                     ("i did not notice the sign", "you were looking the other way")),
               сочувствие=(("i am sad", "i am sorry to hear that"),
                           ("i am anxious", "tell me what happened"),
                           ("i feel good", "i am glad to hear that"))),
    "de": dict(что="was soll ich tun?", почему="warum?",
               пары=(("ich bin müde", "ruh dich aus"), ("ich bin hungrig", "iss etwas"),
                     ("ich habe Angst", "du weißt nicht, was kommt"), ("ich bin in Eile", "beeil dich nicht"),
                     ("ich mache das jeden Tag", "das ist eine Gewohnheit"),
                     ("ich habe das Zeichen nicht gesehen", "du hast weggeschaut")),
               сочувствие=(("ich bin traurig", "das tut mir leid"),
                           ("ich bin unruhig", "erzähl mir, was passiert ist"),
                           ("mir geht es gut", "das freut mich"))),
    "fr": dict(что="que dois-je faire ?", почему="pourquoi ?", двоеточие=" : ",
               пары=(("je suis fatigué", "repose-toi"), ("j'ai faim", "mange quelque chose"),
                     ("j'ai peur", "tu ne sais pas ce qui va arriver"), ("je suis pressé", "ne te presse pas"),
                     ("je fais cela chaque jour", "c'est une habitude"),
                     ("je n'ai pas vu le signe", "tu regardais ailleurs")),
               сочувствие=(("je suis triste", "je suis désolé de l'entendre"),
                           ("je suis inquiet", "raconte-moi ce qui s'est passé"),
                           ("je vais bien", "j'en suis content"))),
    "es": dict(что="¿qué debo hacer?", почему="¿por qué?",
               пары=(("estoy cansado", "descansa"), ("tengo hambre", "come algo"),
                     ("tengo miedo", "no sabes qué va a pasar"), ("tengo prisa", "no te apresures"),
                     ("hago esto cada día", "es una costumbre"),
                     ("no vi la señal", "mirabas hacia otro lado")),
               сочувствие=(("estoy triste", "siento oír eso"),
                           ("estoy inquieto", "cuéntame qué ha pasado"),
                           ("estoy bien", "me alegro de oírlo"))),
    "it": dict(что="che cosa devo fare?", почему="perché?",
               пары=(("sono stanco", "riposati"), ("ho fame", "mangia qualcosa"),
                     ("ho paura", "non sai che cosa succederà"), ("ho fretta", "non affrettarti"),
                     ("lo faccio ogni giorno", "è un'abitudine"),
                     ("non ho visto il segnale", "guardavi dall'altra parte")),
               сочувствие=(("sono triste", "mi dispiace sentirlo"),
                           ("sono inquieto", "raccontami che cosa è successo"),
                           ("sto bene", "mi fa piacere sentirlo"))),
    "pt": dict(что="o que devo fazer?", почему="porque é que?",
               пары=(("estou cansado", "descansa"), ("tenho fome", "come alguma coisa"),
                     ("tenho medo", "não sabes o que vai acontecer"), ("tenho pressa", "não te apresses"),
                     ("faço isto todos os dias", "é um hábito"),
                     ("não vi o sinal", "olhavas para o outro lado")),
               сочувствие=(("estou triste", "lamento ouvir isso"),
                           ("estou inquieto", "conta-me o que aconteceu"),
                           ("estou bem", "fico contente por ouvir isso"))),
    "nl": dict(что="wat moet ik doen?", почему="waarom?",
               пары=(("ik ben moe", "rust uit"), ("ik heb honger", "eet iets"),
                     ("ik ben bang", "je weet niet wat er komt"), ("ik heb haast", "haast je niet"),
                     ("ik doe dit elke dag", "dat is een gewoonte"),
                     ("ik heb het teken niet gezien", "je keek de andere kant op")),
               сочувствие=(("ik ben verdrietig", "dat spijt me"),
                           ("ik ben onrustig", "vertel me wat er gebeurd is"),
                           ("het gaat goed met me", "dat doet me genoegen"))),
    "pl": dict(что="co mam robić?", почему="dlaczego?",
               пары=(("jestem zmęczony", "odpocznij"), ("jestem głodny", "zjedz coś"),
                     ("boję się", "nie wiesz, co będzie"), ("spieszę się", "nie spiesz się"),
                     ("robię to codziennie", "to nawyk"),
                     ("nie zauważyłem znaku", "patrzyłeś w inną stronę")),
               сочувствие=(("jestem smutny", "przykro mi to słyszeć"),
                           ("jestem niespokojny", "opowiedz mi, co się stało"),
                           ("czuję się dobrze", "cieszę się, że to słyszę"))),
}

# ОБЪЯВЛЕНО ДЛЯ СОСЕДА, А НЕ ДЛЯ СЕБЯ: рынок обмена holon берёт эти пары из
# объявления; показом дом их не пишет (см. голову файла).
СОЧУВСТВИЕ = {яз: я["сочувствие"] for яз, я in ЯЗЫКИ_ДОМА.items()}

ЯЗЫКИ = tuple(ЯЗЫКИ_ДОМА)
ФОРМЫ = ("отклик",)

for _яз, _я in ЯЗЫКИ_ДОМА.items():
    assert len(_я["пары"]) == len(B.РОДЫ), _яз
    assert _яз in B.ЯЗЫКИ, _яз
    assert len(_я["сочувствие"]) == 3, _яз


def страница(язык, род):
    """«я устал. что мне делать? отдохни: когда человек устал, он ошибается чаще.»"""
    я = ЯЗЫКИ_ДОМА[язык]
    состояние, совет = я["пары"][род]
    голова = я["что"] if род in ДЕЙСТВИЕ else я["почему"]
    закон = B.страница(язык, "закон", род)
    # ДВОЕТОЧИЕ С ПРОБЕЛОМ ВПЕРЕДИ — строй французского, объявленный, а не
    # угаданный: «repose-toi : quand…», но «rust uit: als…»
    двоеточие = ЯЗЫКИ_ДОМА[язык].get("двоеточие", ": ")
    return f"{состояние}. {голова} {совет}{двоеточие}{закон}"


def _показы():
    return {страница(язык, род): (язык, "отклик") for язык in ЯЗЫКИ for род in B.РОДЫ}


ПОКАЗЫ = _показы()


_ЗАЧИНЫ = frozenset(сост for я in ЯЗЫКИ_ДОМА.values() for сост, _ in я["пары"])


def судить(строка):
    """Подсудно лишь то, чей ЗАЧИН есть объявленное состояние (М-180-f2).

    Первая проба брала подсудным ВСЁ («строка непуста → сужу»), и прибор чужой
    рамки, выровненный по корпусу, тут же поймал захват: этот дом звал ложью
    60 показов дома мнения и 58 показов дома поспешности. Ворота того не
    видели, ибо они судят СУДАМИ, а суд отклика был сужен с рождения; но
    функция дома открыта всякому, и открытая функция, судящая всё, есть
    ловушка для следующего, кто её позовёт.
    """
    с = строка.strip()
    if not с:
        return False, False
    голова = с.split(". ")[0]
    if голова not in _ЗАЧИНЫ:
        return False, False
    return True, с in ПОКАЗЫ


def main():
    поймано = 0
    for язык in ЯЗЫКИ:
        print(f"  {язык}: {страница(язык, 0)}")
        я = ЯЗЫКИ_ДОМА[язык]
        # МУТАНТЫ: чужой закон при своём состоянии; чужой совет; закон, снятый вовсе
        состояние, совет = я["пары"][0]
        д = я.get("двоеточие", ": ")
        мутанты = (f"{состояние}. {я['что']} {совет}{д}{B.страница(язык, 'закон', 1)}",
                   f"{состояние}. {я['что']} {я['пары'][1][1]}{д}{B.страница(язык, 'закон', 0)}",
                   f"{состояние}. {я['что']} {совет}.")
        for м in мутанты:
            судимо, истинно = судить(м)
            поймано += 1 if (судимо and not истинно) else 0
    print(f"  мутантов поймано: {поймано} из {3 * len(ЯЗЫКИ)}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, родов {len(B.РОДЫ)}); "
          f"пар сочувствия объявлено для соседа: {sum(len(р) for р in СОЧУВСТВИЕ.values())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
