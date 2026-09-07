# СЛОВА ДОМА ПЛАНА, ОБЪЯВЛЕННЫЕ НА ДЕВЯТИ ЯЗЫКАХ (08.09, форма holon PLAN-GENUS-0907).
#
# Глаголы актов дом НЕ ОБЪЯВЛЯЕТ ЗАНОВО — он берёт их у дома хода (`actturn.ГЛАГОЛЫ`), где
# они уже стоя́т тремя формами: приказ, инфинитив, отчёт. Здесь объявлено лишь то, чего там
# нет: слово следования, форма условия, акт посадки и вопросные зачины.
#
#     УСЛОВИЕ ОБЪЯВЛЕНО ОБРАЗЦОМ ЦЕЛИКОМ, А НЕ СКЛЕЙКОЙ ИЗ «если» И «равно»: у немецкого и
#     нидерландского сказуемое условия стои́т в конце («wenn exit 0 ist», «als exit 0 is»), и
#     склейка по частям дала бы не речь. Порядок слов не выводится — он объявляется.
#
#     ИМЕНА ЛЕДЖЕРОВ НЕ ПЕРЕВОДЯТСЯ. «files», «runs», «exit», «millis» суть имена наблюдения,
#     а не слова языка: кабина возвращает их одинаково, на каком бы языке ни был отдан приказ,
#     и страница, переводящая их, учила бы речи о несуществующем леджере.
СЛОВА = {
    "ru": dict(условие="если exit = {v}, {посади}", отчёт="отчёт", затем="затем", если="если", запятая=",", равно="=",
               запусти="запусти сборку", запуск="запуск сборки",
               посади="посади", посажено="посажено", не_посажено="не посажено",
               сколько_запусков="сколько запусков было?", какой_exit="какой exit у сборки?",
               посажено_ли="посажено ли?", да="да", нет="нет", файл="файл"),
    "en": dict(условие="if exit is {v}, {посади}", отчёт="report", затем="then", если="if", запятая=",", равно="is",
               запусти="run the build", запуск="the run of the build",
               посади="land", посажено="landed", не_посажено="not landed",
               сколько_запусков="how many runs were there?",
               какой_exit="what was the exit of the build?",
               посажено_ли="was it landed?", да="yes", нет="no", файл="the file"),
    "de": dict(условие="wenn exit {v} ist, {посади}", отчёт="bericht", затем="dann", если="wenn", запятая=",", равно="ist",
               запусти="führe den build aus", запуск="der lauf des builds",
               посади="lande", посажено="gelandet", не_посажено="nicht gelandet",
               сколько_запусков="wie viele läufe gab es?",
               какой_exit="welchen exit hatte der build?",
               посажено_ли="wurde gelandet?", да="ja", нет="nein", файл="die datei"),
    "fr": dict(условие="si exit vaut {v}, {посади}", отчёт="rapport", затем="puis", если="si", запятая=",", равно="vaut",
               запусти="lance le build", запуск="le lancement du build",
               посади="atterris", посажено="atterri", не_посажено="non atterri",
               сколько_запусков="combien de lancements y a-t-il eu ?",
               какой_exit="quel était l'exit du build ?",
               посажено_ли="a-t-il atterri ?", да="oui", нет="non", файл="le fichier"),
    "es": dict(условие="si exit es {v}, {посади}", отчёт="informe", затем="luego", если="si", запятая=",", равно="es",
               запусти="ejecuta el build", запуск="la ejecución del build",
               посади="aterriza", посажено="aterrizado", не_посажено="no aterrizado",
               сколько_запусков="¿cuántas ejecuciones hubo?",
               какой_exit="¿cuál fue el exit del build?",
               посажено_ли="¿aterrizó?", да="sí", нет="no", файл="el archivo"),
    "it": dict(условие="se exit è {v}, {посади}", отчёт="rapporto", затем="poi", если="se", запятая=",", равно="è",
               запусти="esegui il build", запуск="l'esecuzione del build",
               посади="atterra", посажено="atterrato", не_посажено="non atterrato",
               сколько_запусков="quante esecuzioni ci sono state?",
               какой_exit="qual era l'exit del build?",
               посажено_ли="è atterrato?", да="sì", нет="no", файл="il file"),
    "pt": dict(условие="se exit é {v}, {посади}", отчёт="relatório", затем="depois", если="se", запятая=",", равно="é",
               запусти="executa o build", запуск="a execução do build",
               посади="aterra", посажено="aterrado", не_посажено="não aterrado",
               сколько_запусков="quantas execuções houve?",
               какой_exit="qual era o exit do build?",
               посажено_ли="aterrou?", да="sim", нет="não", файл="o ficheiro"),
    "nl": dict(условие="als exit {v} is, {посади}", отчёт="rapport", затем="daarna", если="als", запятая=",", равно="is",
               запусти="voer de build uit", запуск="de run van de build",
               посади="land", посажено="geland", не_посажено="niet geland",
               сколько_запусков="hoeveel runs waren er?",
               какой_exit="welke exit had de build?",
               посажено_ли="is er geland?", да="ja", нет="nee", файл="het bestand"),
    "pl": dict(условие="jeśli exit = {v}, {посади}", отчёт="raport", затем="następnie", если="jeśli", запятая=",", равно="=",
               запусти="uruchom build", запуск="uruchomienie builda",
               посади="wyląduj", посажено="wylądowano", не_посажено="nie wylądowano",
               сколько_запусков="ile było uruchomień?",
               какой_exit="jaki był exit builda?",
               посажено_ли="czy wylądowano?", да="tak", нет="nie", файл="plik"),
}
# ЛЕДЖЕРЫ — ИМЕНА НАБЛЮДЕНИЯ, ОДНИ НА ВСЕ ЯЗЫКИ
ЛЕДЖЕРЫ = ("files", "runs", "exit", "millis")
