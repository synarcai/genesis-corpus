#!/usr/bin/env python3
"""ДОМ ФАКТОВ МИРА — «почему» и «что дальше» о вещах, а не о числах.

Полоса БЕСЕДА-92 держала семь немых строк в роду LINKS-OF-A-TALK, и разбор
нашёл у них ОДНУ природу: дом связок говорит только над АРИФМЕТИЧЕСКИМИ
фактами («у Анны 7 шаров. почему? потому что было 7, отдала 2»), а человек
спрашивает те же ходы над фактами МИРА:

    вода кипит при ста градусах. почему?
    дождь идёт. что дальше?
    согласен ли ты, что вода мокрая?

ФОРМА СОГЛАСОВАНА С holon ДО ПОСТРОЙКИ (04.09), и его слово изменило её в
двух местах. Первое: вопрос стоит МЕЖДУ фактом и основанием, а не рядом с
ним. Строка «лёд плавает в воде. лёд легче воды.» есть две короткие фразы без
числа — ровно рамка его обменного рынка, — и рынок купил бы её как реплику и
ответ, если зачин «вода …» станет частым. Вопросительный знак отводит её сам,
без единого нового признака, и — важнее — «основание становится ОТВЕТОМ, а не
соседом: строка без вопроса учит соположению, строка с вопросом учит
переходу».

Второе: факт мира и его ПРИНАДЛЕЖНОСТЬ стоят РАЗНЫМИ строками, ибо это разные
роды знания — факт проверяется наблюдением, принадлежность другим знанием.
Организм holon только что научился покупать класс из прозы («robin» встал в
классе «bird»), и строки «паук — животное» здесь суть корм именно этому
рынку: не заученная строка, а факт рода.

Шесть форм, и каждая проверяема объявленной таблицей:

  (голого факта отдельной строкой дом НЕ ПИШЕТ — см. ниже)
  ОСНОВАНИЕ      «лёд плавает в воде. почему? потому что лёд легче воды.»
  СЛЕДСТВИЕ      «лёд плавает в воде. что дальше? лёд виден на поверхности.»
                 (и второй поверхностью: «… и что потом?» — вопрос о следствии
                 человек задаёт обоими, а следствие у них одно)
  ПРИНАДЛЕЖНОСТЬ «паук — животное.» и её вопрос «чем является паук? паук —
                 животное.» — вопрос ОБЯЗАТЕЛЕН: прибор ШИРОТЫ ВОПРОСА назвал
                 голую принадлежность родом без вопросной поверхности и поднял
                 долг корпуса с 1109 до 1115. Ответом здесь стоит ВЕСЬ показ
                 принадлежности, а не «да», — иначе вопрос засчитался бы новому
                 роду, а старый остался бы должником
  ПРАВДА         «лёд плавает в воде. правда ли это? да, лёд плавает в воде.»
  СОГЛАСЕН       «лёд плавает в воде. согласен ли ты? да, я согласен: лёд плавает в воде.»

ГОЛОГО ФАКТА ОТДЕЛЬНОЙ СТРОКОЙ ДОМ НЕ ПИШЕТ, и снят он не по вкусу. Прибор
ШИРОТЫ ВОПРОСА назвал пять его образцов (по одному на язык) родами БЕЗ
ВОПРОСНОЙ ПОВЕРХНОСТИ и поднял долг корпуса с 1109 до 1115 — а долг этот
стережётся абсолютным числом, и расти ему нельзя. Платить следовало формой, и
форма нашлась вычитанием: голый факт не несёт НИЧЕГО, чего не несут прочие
формы, — он стоит первой фразой и в основании, и в следствии, и в правде, и в
согласии. Строка, чьё содержание целиком повторено соседями, есть не показ, а
долг; сняв её, дом потерял пять родов и ноль знания.

ПЯТЬ ЯЗЫКОВ, И ЭТО НАЗВАННЫЙ ДОЛГ, А НЕ НЕДОСМОТР — тот же закон, по которому
дом бытовых тем держит определения на пяти: всякий факт мира есть предложение,
которое надо НАПИСАТЬ верно, а не перевести на глаз. Четыре языка атаки ждут
своей волны.

РАМКА ПРАВДЫ И СОГЛАСИЯ НЕ ПОДЧИНЯЕТ ПРИДАТОЧНОГО, и это не стиль, а
необходимость: «stimmst du zu, dass Eis im Wasser schwimmt» требует немецкого
порядка с глаголом в конце, то есть ВТОРОЙ формы факта. Рамка «{факт}. правда
ли это?» берёт факт как он есть на всех пяти языках — и потому объявлять
второй раз ничего не нужно.

    python3 tools/worldfacts.py    # самопроверка с мутантами
"""
# (факт, основание с союзом причины, следствие[, тот же факт ЧИСЛОМ-СЛОВОМ])
# ЧЕТВЁРТОЕ ПОЛЕ ЕСТЬ ВТОРАЯ ПОВЕРХНОСТЬ ТОГО ЖЕ ФАКТА, а не второй факт:
# человек говорит «вода кипит при ста градусах», а корпус писал «при 100
# градусах», и полоса беседы звала строку немой при готовом показе. Основание
# и следствие у обеих поверхностей ОДНИ — тем и показано, что поверхность
# числа меняется, а факт нет (тот же довод, что у вопроса о многих).
ФАКТЫ = {
    "ru": (
        ("лёд плавает в воде", "потому что лёд легче воды", "лёд виден на поверхности"),
        ("камень тонет в воде", "потому что камень тяжелее воды", "камень лежит на дне"),
        ("дым поднимается вверх", "потому что дым легче воздуха", "дым уходит в небо"),
        ("ночью темно", "потому что ночью солнце не светит", "ночью нужен свет"),
        ("после дождя земля мокрая", "потому что дождь — это вода, которая падает на землю", "на дороге стоят лужи"),
        ("вода кипит при 100 градусах", "потому что шкала градусов так и построена: сто градусов есть жара кипящей воды", "из воды идёт пар", "вода кипит при ста градусах"),
        ("дождь идёт", "потому что из облаков падает вода", "земля станет мокрой"),
        ("вода мокрая", "потому что вода смачивает всё, к чему прикасается", "после воды рука мокрая"),
        ("огонь горячий", "потому что огонь даёт тепло", "рядом с огнём тепло"),
        ("снег холодный", "потому что снег есть замёрзшая вода", "снег тает в тепле"),
        ("камень твёрдый", "потому что камень не мнётся под рукой", "камнем можно ударить"),
    ),
    "en": (
        ("ice floats in water", "because ice is lighter than water", "the ice is seen on the surface"),
        ("a stone sinks in water", "because a stone is heavier than water", "the stone lies on the bottom"),
        ("smoke rises", "because smoke is lighter than air", "the smoke goes up into the sky"),
        ("it is dark at night", "because the sun does not shine at night", "a light is needed at night"),
        ("after rain the ground is wet", "because rain is water that falls on the ground", "there are puddles on the road"),
        ("water boils at 100 degrees", "because the scale of degrees is built that way: one hundred degrees is the heat of boiling water", "steam comes from the water", "water boils at one hundred degrees"),
        ("it is raining", "because water falls from the clouds", "the ground will become wet"),
        ("water is wet", "because water wets everything it touches", "after the water the hand is wet"),
        ("fire is hot", "because fire gives heat", "near the fire it is warm"),
        ("snow is cold", "because snow is frozen water", "snow melts in the warmth"),
        ("a stone is hard", "because a stone does not yield under the hand", "one can strike with a stone"),
    ),
    "de": (
        ("Eis schwimmt im Wasser", "weil Eis leichter ist als Wasser", "das Eis ist an der Oberfläche zu sehen"),
        ("ein Stein sinkt im Wasser", "weil ein Stein schwerer ist als Wasser", "der Stein liegt auf dem Grund"),
        ("Rauch steigt nach oben", "weil Rauch leichter ist als Luft", "der Rauch zieht in den Himmel"),
        ("nachts ist es dunkel", "weil die Sonne nachts nicht scheint", "nachts braucht man Licht"),
        ("nach dem Regen ist die Erde nass", "weil Regen Wasser ist, das auf die Erde fällt", "auf der Straße stehen Pfützen"),
        ("Wasser kocht bei 100 Grad", "weil die Gradskala so gebaut ist: hundert Grad ist die Hitze kochenden Wassers", "aus dem Wasser kommt Dampf", "Wasser kocht bei hundert Grad"),
        ("es regnet", "weil Wasser aus den Wolken fällt", "die Erde wird nass"),
        ("Wasser ist nass", "weil Wasser alles nass macht, was es berührt", "nach dem Wasser ist die Hand nass"),
        ("Feuer ist heiß", "weil Feuer Wärme gibt", "am Feuer ist es warm"),
        ("Schnee ist kalt", "weil Schnee gefrorenes Wasser ist", "Schnee schmilzt in der Wärme"),
        ("ein Stein ist hart", "weil ein Stein unter der Hand nicht nachgibt", "mit einem Stein kann man schlagen"),
    ),
    "fr": (
        ("la glace flotte sur l'eau", "parce que la glace est plus légère que l'eau", "on voit la glace à la surface"),
        ("une pierre coule dans l'eau", "parce qu'une pierre est plus lourde que l'eau", "la pierre repose au fond"),
        ("la fumée monte", "parce que la fumée est plus légère que l'air", "la fumée s'en va vers le ciel"),
        ("la nuit il fait sombre", "parce que le soleil ne brille pas la nuit", "la nuit il faut de la lumière"),
        ("après la pluie la terre est mouillée", "parce que la pluie est de l'eau qui tombe sur la terre", "il y a des flaques sur la route"),
        ("l'eau bout à 100 degrés", "parce que l'échelle des degrés est faite ainsi : cent degrés, c'est la chaleur de l'eau qui bout", "de la vapeur sort de l'eau", "l'eau bout à cent degrés"),
        ("il pleut", "parce que l'eau tombe des nuages", "la terre va devenir mouillée"),
        ("l'eau est mouillée", "parce que l'eau mouille tout ce qu'elle touche", "après l'eau la main est mouillée"),
        ("le feu est chaud", "parce que le feu donne de la chaleur", "près du feu il fait chaud"),
        ("la neige est froide", "parce que la neige est de l'eau gelée", "la neige fond à la chaleur"),
        ("la pierre est dure", "parce que la pierre ne cède pas sous la main", "on peut frapper avec une pierre"),
    ),
    "es": (
        ("el hielo flota en el agua", "porque el hielo es más ligero que el agua", "el hielo se ve en la superficie"),
        ("una piedra se hunde en el agua", "porque una piedra es más pesada que el agua", "la piedra queda en el fondo"),
        ("el humo sube", "porque el humo es más ligero que el aire", "el humo se va hacia el cielo"),
        ("de noche está oscuro", "porque de noche el sol no brilla", "de noche hace falta luz"),
        ("después de la lluvia la tierra está mojada", "porque la lluvia es agua que cae sobre la tierra", "hay charcos en el camino"),
        ("el agua hierve a 100 grados", "porque la escala de grados está hecha así: cien grados es el calor del agua que hierve", "del agua sale vapor", "el agua hierve a cien grados"),
        ("está lloviendo", "porque cae agua de las nubes", "la tierra se pondrá mojada"),
        ("el agua moja", "porque el agua deja húmedo todo lo que toca", "después del agua la mano está mojada"),
        ("el fuego es caliente", "porque el fuego da calor", "cerca del fuego hace calor"),
        ("la nieve es fría", "porque la nieve es agua congelada", "la nieve se derrite con el calor"),
        ("la piedra es dura", "porque la piedra no cede bajo la mano", "con una piedra se puede golpear"),
    ),
    "it": (
        ("il ghiaccio galleggia sull'acqua", "perché il ghiaccio è più leggero dell'acqua", "si vede il ghiaccio in superficie"),
        ("una pietra affonda nell'acqua", "perché una pietra è più pesante dell'acqua", "la pietra resta sul fondo"),
        ("il fumo sale", "perché il fumo è più leggero dell'aria", "il fumo va verso il cielo"),
        ("di notte è buio", "perché di notte il sole non splende", "di notte serve una luce"),
        ("dopo la pioggia la terra è bagnata", "perché la pioggia è acqua che cade sulla terra", "ci sono pozzanghere sulla strada"),
        ("l'acqua bolle a 100 gradi", "perché la scala dei gradi è fatta così: cento gradi è il calore dell'acqua che bolle", "dall'acqua esce vapore", "l'acqua bolle a cento gradi"),
        ("piove", "perché l'acqua cade dalle nuvole", "la terra diventerà bagnata"),
        ("l'acqua è bagnata", "perché l'acqua bagna tutto ciò che tocca", "dopo l'acqua la mano è bagnata"),
        ("il fuoco è caldo", "perché il fuoco dà calore", "vicino al fuoco fa caldo"),
        ("la neve è fredda", "perché la neve è acqua ghiacciata", "la neve si scioglie al caldo"),
        ("la pietra è dura", "perché la pietra non cede sotto la mano", "con una pietra si può colpire"),
    ),
    "pt": (
        ("o gelo flutua na água", "porque o gelo é mais leve do que a água", "vê-se o gelo à superfície"),
        ("uma pedra afunda na água", "porque uma pedra é mais pesada do que a água", "a pedra fica no fundo"),
        ("o fumo sobe", "porque o fumo é mais leve do que o ar", "o fumo vai para o céu"),
        ("de noite está escuro", "porque de noite o sol não brilha", "de noite é preciso luz"),
        ("depois da chuva a terra está molhada", "porque a chuva é água que cai na terra", "há poças na estrada"),
        ("a água ferve a 100 graus", "porque a escala dos graus é feita assim: cem graus é o calor da água a ferver", "da água sai vapor", "a água ferve a cem graus"),
        ("está a chover", "porque cai água das nuvens", "a terra vai ficar molhada"),
        ("a água molha", "porque a água deixa molhado tudo o que toca", "depois da água a mão está molhada"),
        ("o fogo é quente", "porque o fogo dá calor", "perto do fogo faz calor"),
        ("a neve é fria", "porque a neve é água congelada", "a neve derrete no calor"),
        ("a pedra é dura", "porque a pedra não cede sob a mão", "com uma pedra pode-se bater"),
    ),
    "nl": (
        ("ijs drijft op water", "omdat ijs lichter is dan water", "het ijs is aan de oppervlakte te zien"),
        ("een steen zinkt in water", "omdat een steen zwaarder is dan water", "de steen ligt op de bodem"),
        ("rook stijgt op", "omdat rook lichter is dan lucht", "de rook gaat naar de hemel"),
        ("het is donker in de nacht", "omdat de zon in de nacht niet schijnt", "in de nacht heeft men licht nodig"),
        ("na de regen is de grond nat", "omdat regen water is dat op de grond valt", "er staan plassen op de weg"),
        ("water kookt bij 100 graden", "omdat de gradenschaal zo gemaakt is: honderd graden is de hitte van kokend water", "uit het water komt stoom", "water kookt bij honderd graden"),
        ("het regent", "omdat er water uit de wolken valt", "de grond wordt nat"),
        ("water is nat", "omdat water alles nat maakt wat het aanraakt", "na het water is de hand nat"),
        ("vuur is heet", "omdat vuur warmte geeft", "bij het vuur is het warm"),
        ("sneeuw is koud", "omdat sneeuw bevroren water is", "sneeuw smelt in de warmte"),
        ("een steen is hard", "omdat een steen niet meegeeft onder de hand", "met een steen kan men slaan"),
    ),
    "pl": (
        ("lód pływa po wodzie", "bo lód jest lżejszy od wody", "lód widać na powierzchni"),
        ("kamień tonie w wodzie", "bo kamień jest cięższy od wody", "kamień leży na dnie"),
        ("dym unosi się do góry", "bo dym jest lżejszy od powietrza", "dym idzie ku niebu"),
        ("w nocy jest ciemno", "bo w nocy słońce nie świeci", "w nocy potrzebne jest światło"),
        ("po deszczu ziemia jest mokra", "bo deszcz to woda, która pada na ziemię", "na drodze są kałuże"),
        ("woda wrze przy 100 stopniach", "bo skala stopni tak jest zbudowana: sto stopni to gorąco wrzącej wody", "z wody idzie para", "woda wrze przy stu stopniach"),
        ("pada deszcz", "bo z chmur spada woda", "ziemia zrobi się mokra"),
        ("woda jest mokra", "ponieważ woda moczy wszystko, czego dotknie", "po wodzie ręka jest mokra"),
        ("ogień jest gorący", "ponieważ ogień daje ciepło", "przy ogniu jest ciepło"),
        ("śnieg jest zimny", "ponieważ śnieg to zamarznięta woda", "śnieg topnieje w cieple"),
        ("kamień jest twardy", "ponieważ kamień nie ugina się pod ręką", "kamieniem można uderzyć"),
    ),
}

# ПРИНАДЛЕЖНОСТЬ — отдельной строкой по слову holon: факт проверяется
# наблюдением, принадлежность другим знанием, и в одной строке они образуют
# пару без носителя и без величины, которую всякий рынок тянет к себе.
КЛАССЫ = {
    "ru": (("паук", "животное"), ("дуб", "дерево"), ("акула", "рыба"),
           ("молоко", "жидкость"), ("ласточка", "птица"), ("роза", "цветок"),
           ("сосна", "дерево"),
           ("тюльпан", "цветок"),
           ("карп", "рыба"),
           ("сова", "птица"),
           ("сок", "жидкость"),
           ("муравей", "животное")),
    "en": (("a spider", "an animal"), ("an oak", "a tree"), ("a shark", "a fish"),
           ("milk", "a liquid"), ("a swallow", "a bird"), ("a rose", "a flower"),
           ("a pine", "a tree"),
           ("a tulip", "a flower"),
           ("a carp", "a fish"),
           ("an owl", "a bird"),
           ("juice", "a liquid"),
           ("an ant", "an animal")),
    "de": (("eine Spinne", "ein Tier"), ("eine Eiche", "ein Baum"), ("ein Hai", "ein Fisch"),
           ("Milch", "eine Flüssigkeit"), ("eine Schwalbe", "ein Vogel"), ("eine Rose", "eine Blume"),
           ("eine Kiefer", "ein Baum"),
           ("eine Tulpe", "eine Blume"),
           ("ein Karpfen", "ein Fisch"),
           ("eine Eule", "ein Vogel"),
           ("Saft", "eine Flüssigkeit"),
           ("eine Ameise", "ein Tier")),
    "fr": (("une araignée", "un animal"), ("un chêne", "un arbre"), ("un requin", "un poisson"),
           ("le lait", "un liquide"), ("une hirondelle", "un oiseau"), ("une rose", "une fleur"),
           ("un pin", "un arbre"),
           ("une tulipe", "une fleur"),
           ("une carpe", "un poisson"),
           ("un hibou", "un oiseau"),
           ("le jus", "un liquide"),
           ("une fourmi", "un animal")),
    "es": (("una araña", "un animal"), ("un roble", "un árbol"), ("un tiburón", "un pez"),
           ("la leche", "un líquido"), ("una golondrina", "un pájaro"), ("una rosa", "una flor"),
           ("un pino", "un árbol"),
           ("un tulipán", "una flor"),
           ("una carpa", "un pez"),
           ("un búho", "un pájaro"),
           ("el zumo", "un líquido"),
           ("una hormiga", "un animal")),
    "it": (
           ("un ragno", "un animale"),
           ("una quercia", "un albero"),
           ("uno squalo", "un pesce"),
           ("il latte", "un liquido"),
           ("una rondine", "un uccello"),
           ("una rosa", "un fiore"),
           ("un pino", "un albero"),
           ("un tulipano", "un fiore"),
           ("una carpa", "un pesce"),
           ("un gufo", "un uccello"),
           ("il succo", "un liquido"),
           ("una formica", "un animale")),
    "pt": (
           ("uma aranha", "um animal"),
           ("um carvalho", "uma árvore"),
           ("um tubarão", "um peixe"),
           ("o leite", "um líquido"),
           ("uma andorinha", "uma ave"),
           ("uma rosa", "uma flor"),
           ("um pinheiro", "uma árvore"),
           ("uma tulipa", "uma flor"),
           ("uma carpa", "um peixe"),
           ("uma coruja", "uma ave"),
           ("o sumo", "um líquido"),
           ("uma formiga", "um animal")),
    "nl": (
           ("een spin", "een dier"),
           ("een eik", "een boom"),
           ("een haai", "een vis"),
           ("melk", "een vloeistof"),
           ("een zwaluw", "een vogel"),
           ("een roos", "een bloem"),
           ("een den", "een boom"),
           ("een tulp", "een bloem"),
           ("een karper", "een vis"),
           ("een uil", "een vogel"),
           ("sap", "een vloeistof"),
           ("een mier", "een dier")),
    "pl": (
           ("pająk", "zwierzę"),
           ("dąb", "drzewo"),
           ("rekin", "ryba"),
           ("mleko", "płyn"),
           ("jaskółka", "ptak"),
           ("róża", "kwiat"),
           ("sosna", "drzewo"),
           ("tulipan", "kwiat"),
           ("karp", "ryba"),
           ("sowa", "ptak"),
           ("sok", "płyn"),
           ("mrówka", "zwierzę")),
}


# НАДКЛАССЫ — (класс, класс с квантором, надкласс). Ими живёт СИЛЛОГИЗМ.
# Ступень объявлена после ссоры домов: прибор согласия нашёл, что дом
# определений зовёт дуб РАСТЕНИЕМ, а этот дом ДЕРЕВОМ. Ни один не лжёт —
# это два уровня одной лестницы, и ссора была не ложью, а НЕОБЪЯВЛЕННОЙ
# ступенью между ними. Объявив ступень, дом получил и согласие с соседом,
# и новую форму вывода.
# ЧТО ОБЩЕГО У ДВУХ ЧЛЕНОВ ОДНОГО КЛАССА (пятая полоса беседы, 05.09: «что общего у
# кошки и собаки?» — нем во всех девяти языках). Ответ — класс во МНОЖЕСТВЕННОМ
# числе («кошка и собака — животные»), и множественное объявлено по языкам, не
# выведено; русский вопрос держит члены в родительном («у кошки и собаки») —
# родительный объявлен по членам. Кошка и собака входят в класс животных.
ОБЩЕЕ = {
    "ru": dict(рамка="что общего у {ч1р} и {ч2р}? {ч1} и {ч2} — {км}.",
               мн={"животное": "животные", "дерево": "деревья", "рыба": "рыбы", "жидкость": "жидкости", "птица": "птицы", "цветок": "цветы", 'мебель': 'мебель'},
               род={"паук": "паука", "дуб": "дуба", "акула": "акулы", "молоко": "молока", "ласточка": "ласточки", "роза": "розы",
                    "сосна": "сосны", "тюльпан": "тюльпана", "карп": "карпа", "сова": "совы", "сок": "сока", "муравей": "муравья",
                    "кошка": "кошки", "собака": "собаки", "стол": "стола", "стул": "стула"}),
    "en": dict(рамка="what do {ч1} and {ч2} have in common? {ч1} and {ч2} are {км}.",
               мн={"an animal": "animals", "a tree": "trees", "a fish": "fish", "a liquid": "liquids", "a bird": "birds", "a flower": "flowers", 'furniture': 'furniture'}),
    "de": dict(рамка="was haben {ч1} und {ч2} gemeinsam? {ч1} und {ч2} sind {км}.",
               мн={"ein Tier": "Tiere", "ein Baum": "Bäume", "ein Fisch": "Fische", "eine Flüssigkeit": "Flüssigkeiten", "ein Vogel": "Vögel", "eine Blume": "Blumen", 'ein Möbelstück': 'Möbel'}),
    "fr": dict(рамка="qu'ont en commun {ч1} et {ч2} ? {ч1} et {ч2} sont {км}.",
               мн={"un animal": "des animaux", "un arbre": "des arbres", "un poisson": "des poissons", "un liquide": "des liquides", "un oiseau": "des oiseaux", "une fleur": "des fleurs", 'un meuble': 'des meubles'}),
    "es": dict(рамка="¿qué tienen en común {ч1} y {ч2}? {ч1} y {ч2} son {км}.",
               мн={"un animal": "animales", "un árbol": "árboles", "un pez": "peces", "un líquido": "líquidos", "un pájaro": "pájaros", "una flor": "flores", 'un mueble': 'muebles'}),
    "it": dict(рамка="che cosa hanno in comune {ч1} e {ч2}? {ч1} e {ч2} sono {км}.",
               мн={"un animale": "animali", "un albero": "alberi", "un pesce": "pesci", "un liquido": "liquidi", "un uccello": "uccelli", "un fiore": "fiori", 'un mobile': 'mobili'}),
    "pt": dict(рамка="o que têm em comum {ч1} e {ч2}? {ч1} e {ч2} são {км}.",
               мн={"um animal": "animais", "uma árvore": "árvores", "um peixe": "peixes", "um líquido": "líquidos", "uma ave": "aves", "uma flor": "flores", 'um móvel': 'móveis'}),
    "nl": dict(рамка="wat hebben {ч1} en {ч2} gemeen? {ч1} en {ч2} zijn {км}.",
               мн={"een dier": "dieren", "een boom": "bomen", "een vis": "vissen", "een vloeistof": "vloeistoffen", "een vogel": "vogels", "een bloem": "bloemen", 'een meubel': 'meubels'}),
    "pl": dict(рамка="co mają wspólnego {ч1} i {ч2}? {ч1} i {ч2} to {км}.",
               мн={"zwierzę": "zwierzęta", "drzewo": "drzewa", "ryba": "ryby", "płyn": "płyny", "ptak": "ptaki", "kwiat": "kwiaty", 'mebel': 'meble'}),
}
КОШКА_СОБАКА = {"ru": (("кошка", "животное"), ("собака", "животное")), "en": (("a cat", "an animal"), ("a dog", "an animal")),
                "de": (("eine Katze", "ein Tier"), ("ein Hund", "ein Tier")), "fr": (("un chat", "un animal"), ("un chien", "un animal")),
                "es": (("un gato", "un animal"), ("un perro", "un animal")), "it": (("un gatto", "un animale"), ("un cane", "un animale")),
                "pt": (("um gato", "um animal"), ("um cão", "um animal")), "nl": (("een kat", "een dier"), ("een hond", "een dier")),
                "pl": (("kot", "zwierzę"), ("pies", "zwierzę"))}
МЕБЕЛЬ = {'ru': (('стол', 'мебель'), ('стул', 'мебель')), 'en': (('a table', 'furniture'), ('a chair', 'furniture')), 'de': (('ein Tisch', 'ein Möbelstück'), ('ein Stuhl', 'ein Möbelstück')), 'fr': (('une table', 'un meuble'), ('une chaise', 'un meuble')), 'es': (('una mesa', 'un mueble'), ('una silla', 'un mueble')), 'it': (('un tavolo', 'un mobile'), ('una sedia', 'un mobile')), 'pt': (('uma mesa', 'um móvel'), ('uma cadeira', 'um móvel')), 'nl': (('een tafel', 'een meubel'), ('een stoel', 'een meubel')), 'pl': (('stół', 'mebel'), ('krzesło', 'mebel'))}
for _яз in КЛАССЫ:
    КЛАССЫ[_яз] = tuple(КЛАССЫ[_яз]) + КОШКА_СОБАКА[_яз] + МЕБЕЛЬ[_яз]
    assert set(к for _, к in КЛАССЫ[_яз]) <= set(ОБЩЕЕ[_яз]["мн"]), (_яз, "множественное класса не объявлено")
    if "род" in ОБЩЕЕ[_яз]:
        assert set(ч for ч, _ in КЛАССЫ[_яз]) <= set(ОБЩЕЕ[_яз]["род"]), (_яз, "родительный члена не объявлен")


def _род(язык, ч):
    return ОБЩЕЕ[язык].get("род", {}).get(ч, ч)


def пары_класса(язык):
    """Ordered pairs of distinct members of one class."""
    for ч1, к1 in КЛАССЫ[язык]:
        for ч2, к2 in КЛАССЫ[язык]:
            if ч1 != ч2 and к1 == к2:
                yield ч1, ч2, к1


# ЛИШНЕЕ СРЕДИ ТРЁХ (шестая полоса, 05.09: «что лишнее: кошка, собака, стол?»): два члена
# одного класса и один чужой; ответ — чужой член с основанием обоими классами.
ЛИШНЕЕ = {
    "ru": "что лишнее: {ч1}, {ч2}, {ч3}? {ч3}: {ч1} и {ч2} — {км}, а {ч3} — {к3}.",
    "en": "which is the odd one out: {ч1}, {ч2}, {ч3}? {ч3}: {ч1} and {ч2} are {км}, and {ч3} is {к3}.",
    "de": "was passt nicht dazu: {ч1}, {ч2}, {ч3}? {ч3}: {ч1} und {ч2} sind {км}, und {ч3} ist {к3}.",
    "fr": "lequel est l'intrus : {ч1}, {ч2}, {ч3} ? {ч3} : {ч1} et {ч2} sont {км}, et {ч3} est {к3}.",
    "es": "¿cuál no encaja: {ч1}, {ч2}, {ч3}? {ч3}: {ч1} y {ч2} son {км}, y {ч3} es {к3}.",
    "it": "qual è l'intruso: {ч1}, {ч2}, {ч3}? {ч3}: {ч1} e {ч2} sono {км}, e {ч3} è {к3}.",
    "pt": "qual é o intruso: {ч1}, {ч2}, {ч3}? {ч3}: {ч1} e {ч2} são {км}, e {ч3} é {к3}.",
    "nl": "wat hoort er niet bij: {ч1}, {ч2}, {ч3}? {ч3}: {ч1} en {ч2} zijn {км}, en {ч3} is {к3}.",
    "pl": "co nie pasuje: {ч1}, {ч2}, {ч3}? {ч3}: {ч1} i {ч2} to {км}, a {ч3} to {к3}.",
}


def тройки_лишнего(язык):
    """Two members of one class and a stranger from every other class — one triple
    per unordered pair of the class and per other class."""
    члены = КЛАССЫ[язык]
    классы = list(dict.fromkeys(к for _, к in члены))
    for ч1, ч2, к in пары_класса(язык):
        if ч1 > ч2:
            continue
        # the stranger — the first member of EVERY other class: «кошка, собака, стол»
        # as well as «кошка, собака, дуб»
        for к3 in классы:
            if к3 == к:
                continue
            ч3 = next(ч for ч, кк in члены if кк == к3)
            yield ч1, ч2, ч3, к, к3


ИЕРАРХИЯ = {
    "ru": (
        ("рыба", "всякая рыба", "животное"),
        ("птица", "всякая птица", "животное"),
        ("дерево", "всякое дерево", "растение"),
        ("цветок", "всякий цветок", "растение"),
        ("жидкость", "всякая жидкость", "вещество"),
    ),
    "en": (
        ("a fish", "every fish", "an animal"),
        ("a bird", "every bird", "an animal"),
        ("a tree", "every tree", "a plant"),
        ("a flower", "every flower", "a plant"),
        ("a liquid", "every liquid", "a substance"),
    ),
    "de": (
        ("ein Fisch", "jeder Fisch", "ein Tier"),
        ("ein Vogel", "jeder Vogel", "ein Tier"),
        ("ein Baum", "jeder Baum", "eine Pflanze"),
        ("eine Blume", "jede Blume", "eine Pflanze"),
        ("eine Flüssigkeit", "jede Flüssigkeit", "ein Stoff"),
    ),
    "fr": (
        ("un poisson", "tout poisson", "un animal"),
        ("un oiseau", "tout oiseau", "un animal"),
        ("un arbre", "tout arbre", "une plante"),
        ("une fleur", "toute fleur", "une plante"),
        ("un liquide", "tout liquide", "une substance"),
    ),
    "es": (
        ("un pez", "todo pez", "un animal"),
        ("un pájaro", "todo pájaro", "un animal"),
        ("un árbol", "todo árbol", "una planta"),
        ("una flor", "toda flor", "una planta"),
        ("un líquido", "todo líquido", "una sustancia"),
    ),
    "it": (
        ("un pesce", "ogni pesce", "un animale"),
        ("un uccello", "ogni uccello", "un animale"),
        ("un albero", "ogni albero", "una pianta"),
        ("un fiore", "ogni fiore", "una pianta"),
        ("un liquido", "ogni liquido", "una sostanza"),
    ),
    "pt": (
        ("um peixe", "todo peixe", "um animal"),
        ("uma ave", "toda ave", "um animal"),
        ("uma árvore", "toda árvore", "uma planta"),
        ("uma flor", "toda flor", "uma planta"),
        ("um líquido", "todo líquido", "uma substância"),
    ),
    "nl": (
        ("een vis", "elke vis", "een dier"),
        ("een vogel", "elke vogel", "een dier"),
        ("een boom", "elke boom", "een plant"),
        ("een bloem", "elke bloem", "een plant"),
        ("een vloeistof", "elke vloeistof", "een stof"),
    ),
    "pl": (
        ("ryba", "każda ryba", "zwierzę"),
        ("ptak", "każdy ptak", "zwierzę"),
        ("drzewo", "każde drzewo", "roślina"),
        ("kwiat", "każdy kwiat", "roślina"),
        ("płyn", "każdy płyn", "substancja"),
    ),
}

# ПРЯМОЙ ВОПРОС «ПОЧЕМУ {ФАКТ}?» (четвёртая полоса беседы, 05.09: «почему лёд плавает
# в воде?» был нем во всех девяти языках — дом спрашивал «почему?» лишь ПОСЛЕ
# факта). В русском, польском, испанском, итальянском и португальском вопрос
# есть факт с вопросным словом впереди — рамка. В английском, немецком,
# французском и нидерландском вопрос ПЕРЕСТРАИВАЕТ факт (do-support, инверсия),
# и вопросная форма факта ОБЪЯВЛЯЕТСЯ — по одной на факт, не выводится.
ВОПРОС_ПОЧЕМУ = {
    "en": ("why does ice float in water", "why does a stone sink in water", "why does smoke rise",
           "why is it dark at night", "why is the ground wet after rain", "why does water boil at 100 degrees",
           "why is it raining", "why is water wet", "why is fire hot", "why is snow cold", "why is a stone hard"),
    "de": ("warum schwimmt Eis im Wasser", "warum sinkt ein Stein im Wasser", "warum steigt Rauch nach oben",
           "warum ist es nachts dunkel", "warum ist die Erde nach dem Regen nass", "warum kocht Wasser bei 100 Grad",
           "warum regnet es", "warum ist Wasser nass", "warum ist Feuer heiß", "warum ist Schnee kalt", "warum ist ein Stein hart"),
    "fr": ("pourquoi la glace flotte-t-elle sur l'eau", "pourquoi une pierre coule-t-elle dans l'eau", "pourquoi la fumée monte-t-elle",
           "pourquoi fait-il sombre la nuit", "pourquoi la terre est-elle mouillée après la pluie", "pourquoi l'eau bout-elle à 100 degrés",
           "pourquoi pleut-il", "pourquoi l'eau est-elle mouillée", "pourquoi le feu est-il chaud", "pourquoi la neige est-elle froide",
           "pourquoi la pierre est-elle dure"),
    "nl": ("waarom drijft ijs op water", "waarom zinkt een steen in water", "waarom stijgt rook op",
           "waarom is het donker in de nacht", "waarom is de grond nat na de regen", "waarom kookt water bij 100 graden",
           "waarom regent het", "waarom is water nat", "waarom is vuur heet", "waarom is sneeuw koud", "waarom is een steen hard"),
}
for _яз, _в in ВОПРОС_ПОЧЕМУ.items():
    assert len(_в) == len(ФАКТЫ[_яз]), (_яз, "вопросов не по фактам")

РАМКИ = {
    "ru": dict(почему_прямо="почему {ф}? {о}.",
               основание="{ф}. почему? {о}.", следствие="{ф}. что дальше? {с}.",
               следствие2="{ф}. и что потом? {с}.",
               принадлежность="{ч} — {к}.", правда="{ф}. правда ли это? да, {ф}.",
               силлогизм="что следует из того, что {ч} — {к}, а {кв} — {н}? {ч} — {к}. {кв} — {н}. значит {ч} — {н}.",
               принадлежность_вопрос="чем является {ч}? {ч} — {к}.",
               согласен="{ф}. согласен ли ты? да, я согласен: {ф}.",
               согласен_что="согласен ли ты, что {п}? да, {ф}."),
    "en": dict(почему_прямо="{впф}? {о}.",
               основание="{ф}. why? {о}.", следствие="{ф}. what happens next? {с}.",
               следствие2="{ф}. what next? {с}.",
               принадлежность="{ч} is {к}.", правда="{ф}. is that true? yes, {ф}.",
               силлогизм="what follows from {ч} being {к} and {кв} being {н}? {ч} is {к}. {кв} is {н}. so {ч} is {н}.",
               принадлежность_вопрос="what kind of thing is {ч}? {ч} is {к}.",
               согласен="{ф}. do you agree? yes, i agree: {ф}.",
               согласен_что="do you agree that {п}? yes, {ф}."),
    "de": dict(почему_прямо="{впф}? {о}.",
               основание="{ф}. warum? {о}.", следствие="{ф}. was kommt dann? {с}.",
               следствие2="{ф}. und dann? {с}.",
               принадлежность="{ч} ist {к}.", правда="{ф}. stimmt das? ja, {ф}.",
               силлогизм="was folgt daraus, dass {ч} {к} ist und {кв} {н} ist? {ч} ist {к}. {кв} ist {н}. also ist {ч} {н}.",
               принадлежность_вопрос="was für ein Ding ist {ч}? {ч} ist {к}.",
               согласен="{ф}. stimmst du zu? ja, ich stimme zu: {ф}.",
               согласен_что="stimmst du zu, dass {п}? ja, {ф}."),
    "fr": dict(почему_прямо="{впф} ? {о}.",
               основание="{ф}. pourquoi ? {о}.", следствие="{ф}. et ensuite ? {с}.",
               следствие2="{ф}. et après ? {с}.",
               принадлежность="{ч} est {к}.", правда="{ф}. est-ce vrai ? oui, {ф}.",
               силлогизм="que découle-t-il du fait {чт} est {к} et que {кв} est {н} ? {ч} est {к}. {кв} est {н}. donc {ч} est {н}.",
               гласные_стяжения="aeiouâêîôûàèùéh",
               принадлежность_вопрос="quelle sorte de chose est {ч} ? {ч} est {к}.",
               согласен="{ф}. es-tu d'accord ? oui, je suis d'accord : {ф}.",
               согласен_что="es-tu d'accord que {п} ? oui, {ф}."),
    "es": dict(почему_прямо="¿por qué {ф}? {о}.",
               основание="{ф}. ¿por qué? {о}.", следствие="{ф}. ¿y luego? {с}.",
               следствие2="{ф}. ¿y después? {с}.",
               принадлежность="{ч} es {к}.", правда="{ф}. ¿es verdad? sí, {ф}.",
               силлогизм="¿qué se sigue de que {ч} sea {к} y de que {кв} sea {н}? {ч} es {к}. {кв} es {н}. entonces {ч} es {н}.",
               принадлежность_вопрос="¿qué clase de cosa es {ч}? {ч} es {к}.",
               согласен="{ф}. ¿estás de acuerdo? sí, estoy de acuerdo: {ф}.",
               согласен_что="¿estás de acuerdo en que {п}? sí, {ф}."),
    "it": dict(почему_прямо="perché {ф}? {о}.",
               основание="{ф}. perché? {о}.",
               следствие="{ф}. che cosa succede poi? {с}.",
               следствие2="{ф}. e poi? {с}.",
               принадлежность="{ч} è {к}.",
               принадлежность_вопрос="che tipo di cosa è {ч}? {ч} è {к}.",
               правда="{ф}. è vero? sì, {ф}.",
               согласен="{ф}. sei d'accordo? sì, sono d'accordo: {ф}.",
               согласен_что="sei d'accordo che {п}? sì, {ф}.",
               силлогизм="che cosa segue dal fatto che {ч} è {к} e che {кв} è {н}? {ч} è {к}. {кв} è {н}. quindi {ч} è {н}.",
    ),
    "pt": dict(почему_прямо="porque é que {ф}? {о}.",
               основание="{ф}. porquê? {о}.",
               следствие="{ф}. o que acontece depois? {с}.",
               следствие2="{ф}. e depois? {с}.",
               принадлежность="{ч} é {к}.",
               принадлежность_вопрос="que espécie de coisa é {ч}? {ч} é {к}.",
               правда="{ф}. é verdade? sim, {ф}.",
               согласен="{ф}. concordas? sim, concordo: {ф}.",
               согласен_что="concordas que {п}? sim, {ф}.",
               силлогизм="o que se segue de {ч} ser {к} e de {кв} ser {н}? {ч} é {к}. {кв} é {н}. portanto {ч} é {н}.",
    ),
    "nl": dict(почему_прямо="{впф}? {о}.",
               основание="{ф}. waarom? {о}.",
               следствие="{ф}. wat gebeurt er dan? {с}.",
               следствие2="{ф}. en dan? {с}.",
               принадлежность="{ч} is {к}.",
               принадлежность_вопрос="wat voor ding is {ч}? {ч} is {к}.",
               правда="{ф}. klopt dat? ja, {ф}.",
               согласен="{ф}. ben je het ermee eens? ja, ik ben het ermee eens: {ф}.",
               согласен_что="ben je het ermee eens dat {п}? ja, {ф}.",
               силлогизм="wat volgt eruit dat {ч} {к} is en dat {кв} {н} is? {ч} is {к}. {кв} is {н}. dus is {ч} {н}.",
    ),
    "pl": dict(почему_прямо="dlaczego {ф}? {о}.",
               основание="{ф}. dlaczego? {о}.",
               следствие="{ф}. co będzie dalej? {с}.",
               следствие2="{ф}. a potem? {с}.",
               принадлежность="{ч} to {к}.",
               принадлежность_вопрос="czym jest {ч}? {ч} to {к}.",
               правда="{ф}. czy to prawda? tak, {ф}.",
               согласен="{ф}. zgadzasz się? tak, zgadzam się: {ф}.",
               согласен_что="czy zgadzasz się, że {п}? tak, {ф}.",
               силлогизм="co wynika z tego, że {ч} to {к}, a {кв} to {н}? {ч} to {к}. {кв} to {н}. więc {ч} to {н}.",
    ),
}



# ПРИДАТОЧНОЕ — тот же факт, поставленный под союз «что». Форма согласия
# спрашивает не о строке, а о ПОЛОЖЕНИИ ДЕЛ («согласен ли ты, что лёд плавает
# в воде?»), и это первое в доме подчинение. Четыре языка ставят факт под союз
# БЕЗ ПЕРЕСТРОЙКИ, и это объявлено ЯВНО — списком, а не умолчанием; немецкий
# уводит глагол в конец, и его придаточные написаны по одному.
ПРИДАТОЧНОЕ_РАВНО_ФАКТУ = frozenset({"ru", "en", "fr", "es", "it", "pt", "pl"})
ПРИДАТОЧНОЕ = {
    "nl": (
           "ijs op water drijft",
           "een steen in water zinkt",
           "rook opstijgt",
           "het in de nacht donker is",
           "de grond na de regen nat is",
           "water bij 100 graden kookt",
           "het regent",
           "water nat is", "vuur heet is", "sneeuw koud is", "een steen hard is"),
    "de": ("Eis im Wasser schwimmt", "ein Stein im Wasser sinkt", "Rauch nach oben steigt",
           "es nachts dunkel ist", "die Erde nach dem Regen nass ist",
           "Wasser bei 100 Grad kocht", "es regnet",
           "Wasser nass ist", "Feuer heiß ist", "Schnee kalt ist", "ein Stein hart ist"),
}

# ДВЕНАДЦАТЬ ЧЛЕНОВ, А НЕ ШЕСТЬ, И ЭТО ЧУЖОЕ ЧИСЛО. d5 (04.09) назвал шестьдесят
# два голодающих сбора организма и указал, чего ждут три из них — «def_facts»,
# «def_copulas», «def_rules»: определения через связку с ДОСТАТОЧНЫМ числом
# РАЗНЫХ подлежащих. Шести не хватало ни одному. Добавлены сосна, тюльпан,
# карп, сова, сок и муравей — по два новых члена на каждый объявленный класс,
# чтобы ступень родов тоже стояла не на одном свидетеле.
#
# ЧУЖОЙ ПОКАЗ НЕ ПОВТОРЯЕТСЯ. «iron is a metal.» и «the sun is a star.» уже
# стояли в мире genesis_l4, и первая волна этого дома написала их второй раз —
# прибор ШИРОТЫ ВОПРОСА поймал это с неожиданной стороны: образец дома
# захватил чужие строки и принёс долг НА ЧУЖОМ МИРЕ («НЕТ ВОПРОСА genesis_l4:
# worldfacts.ОБРАЗЦЫ[10]»). Железо и солнце уступили место акуле и ласточке,
# каких свод не знал. Проверка стоит в суде (courts/worldfacts_court.py):
# показ, уже стоящий в чужом мире, есть не знание, а вес.
#
# ЧУЖОЕ ОПРЕДЕЛЁННОЕ СЛОВО НЕ БЕРЁТСЯ В ЧЛЕНЫ (М-172 — дом, не читающий
# объявления соседа, пропускает ложь как незнание). Рамка принадлежности
# «{ч} is {к}.» слово в слово совпадает с рамкой ОПРЕДЕЛЕНИЯ дома бытовых тем,
# и различить их нельзя ничем, кроме СЛОВА: «water is a liquid» замкнутый суд
# тем прочёл своим и назвал ложью, ибо «вода» определена у него иначе. Первая
# волна дома писала «вода — жидкость» и была остановлена воротами на трёх
# языках из пяти — правильно остановлена.
#
# Лекарство не в послаблении суда, а в ЧТЕНИИ соседа: член здесь не вправе
# быть термином, который дом тем определяет. Проверка стоит при ввозе, и
# потому изъян не может вернуться молча.
try:
    import topicforms as _темы
    _ОПРЕДЕЛЕНО = {(_яз, _т) for _яз, _темы_яз in _темы.ОПРЕДЕЛЕНИЯ.items()
                   for _пары in _темы_яз.values() for _т, _ in _пары}
except Exception:      # дом тем недоступен — охраны нет, и это видно
    _ОПРЕДЕЛЕНО = None
if _ОПРЕДЕЛЕНО is not None:
    for _яз, _ряд in КЛАССЫ.items():
        for _ч, _к in _ряд:
            assert (_яз, _ч) not in _ОПРЕДЕЛЕНО, (
                f"{_яз}: «{_ч}» определено домом бытовых тем — принадлежность о нём "
                f"столкнётся с его рамкой определения (М-172)")


# ВЕЖЛИВЫЙ РЕГИСТР СОГЛАСИЯ. Дом спрашивает собеседника «согласен ли ты, что…»
# — единственное место, где он обращается к человеку, — и потому обязан уметь
# спросить на «вы». Английский различия не имеет и пишет одну форму (объявлено
# списком); польский идёт третьим лицом («czy zgadza się pan»).
БЕЗ_РАЗЛИЧИЯ_РЕГИСТРА = frozenset({"en"})
СОГЛАСЕН_ВЫ = {
    "ru": "согласны ли вы, что {п}? да, {ф}.",
    "de": "stimmen Sie zu, dass {п}? ja, {ф}.",
    "fr": "êtes-vous d'accord que {п} ? oui, {ф}.",
    "es": "¿está usted de acuerdo en que {п}? sí, {ф}.",
    "it": "è d'accordo che {п}? sì, {ф}.",
    "pt": "concorda que {п}? sim, {ф}.",
    "nl": "bent u het ermee eens dat {п}? ja, {ф}.",
    "pl": "czy zgadza się pan, że {п}? tak, {ф}.",
}
# ОБЪЯВЛЕННЫЙ ПРОПУСК — см. tools/linkforms.py
ОБЪЯВЛЕННЫЕ_ПРОПУСКИ = {"согласен_что_вы": БЕЗ_РАЗЛИЧИЯ_РЕГИСТРА}

ЯЗЫКИ = tuple(ФАКТЫ)
ФОРМЫ = ("основание", "следствие", "принадлежность", "правда", "согласен", "согласен_что", "согласен_что_вы", "следствие2", "принадлежность_вопрос", "силлогизм", "почему_прямо", "общего", "лишнее")

for _яз in ЯЗЫКИ:
    # «гласные_стяжения» есть ОБЪЯВЛЕНИЕ СТРОЯ, а не форма: язык, где стяжения
    # нет, его не объявляет, и сличение форм ведётся без служебных ключей.
    РАМКИ[_яз]["общего"] = ОБЩЕЕ[_яз]["рамка"]
    РАМКИ[_яз]["лишнее"] = ЛИШНЕЕ[_яз]   # рамка формы «общего» живёт в своей таблице
    assert set(РАМКИ[_яз]) - {"гласные_стяжения"} == set(ФОРМЫ) - {"согласен_что_вы"}, _яз
    assert (_яз in БЕЗ_РАЗЛИЧИЯ_РЕГИСТРА) != (_яз in СОГЛАСЕН_ВЫ), _яз
    assert (_яз in ПРИДАТОЧНОЕ_РАВНО_ФАКТУ) != (_яз in ПРИДАТОЧНОЕ), _яз
    if _яз in ПРИДАТОЧНОЕ:
        assert len(ПРИДАТОЧНОЕ[_яз]) == len(ФАКТЫ[_яз]), _яз
    assert len(КЛАССЫ[_яз]) == len(КЛАССЫ["ru"]), _яз
    assert len(ФАКТЫ[_яз]) == len(ФАКТЫ["ru"]), _яз
    for _пара in ФАКТЫ[_яз]:
        assert len(_пара) in (3, 4), (_яз, _пара)
        assert all(_ч and not _ч.endswith(".") for _ч in _пара), (_яз, _пара)


# обе поверхности числа проходятся одним счётчиком: чётный шаг — как записано,
# нечётный — числом-словом там, где оно объявлено
_ЧИСЛОМ_И_СЛОВОМ = True


def страница(язык, форма, i):
    """Одна страница дома. ФАКТ и ПРИНАДЛЕЖНОСТЬ идут по своим таблицам."""
    р = РАМКИ[язык]
    if форма == "силлогизм":
        # СИЛЛОГИЗМ (Barbara) — единственный ход корпуса от РОДА к НАДРОДУ.
        # Стоит ТОЛЬКО в вопросной обёртке: голый силлогизм был бы родом без
        # вопросной поверхности и поднял бы долг прибора ШИРОТЫ (тот же счёт,
        # по которому снят голый факт). Ответом обёртки стоит ВЕСЬ силлогизм,
        # и рынок покупает его целиком, ничего не теряя.
        к, кв, н = ИЕРАРХИЯ[язык][i % len(ИЕРАРХИЯ[язык])]
        ч = next((ч_ for ч_, кл in КЛАССЫ[язык] if кл == к), None)
        if ч is None:
            return None
        # СТЯЖЕНИЕ СОЮЗА — строй французского, объявленный гласными, а не
        # угаданный: «du fait QU'UN requin» при гласной и «du fait QUE LE lait»
        # при согласной. Языки, где стяжения нет, дыры «чт» и не держат.
        гласные = р.get("гласные_стяжения")
        чт = (("qu'" if ч[:1].lower() in гласные else "que ") + ч) if гласные else None
        return р["силлогизм"].format(ч=ч, к=к, кв=кв, н=н, чт=чт)
    if форма.startswith("принадлежность"):
        ч, к = КЛАССЫ[язык][i % len(КЛАССЫ[язык])]
        return р[форма].format(ч=ч, к=к)
    ряд = ФАКТЫ[язык]
    if форма == "лишнее":
        тройки = list(тройки_лишнего(язык))
        ч1, ч2, ч3, к, к3 = тройки[i % len(тройки)]
        return ЛИШНЕЕ[язык].format(ч1=ч1, ч2=ч2, ч3=ч3, км=ОБЩЕЕ[язык]["мн"][к], к3=к3)
    if форма == "общего":
        пары = list(пары_класса(язык))
        ч1, ч2, к = пары[i % len(пары)]
        return ОБЩЕЕ[язык]["рамка"].format(ч1=ч1, ч2=ч2, ч1р=_род(язык, ч1), ч2р=_род(язык, ч2), км=ОБЩЕЕ[язык]["мн"][к])
    if форма == "почему_прямо":
        к = i % len(ряд)
        ф, о = ряд[к][0], ряд[к][1]
        впф = ВОПРОС_ПОЧЕМУ[язык][к] if язык in ВОПРОС_ПОЧЕМУ else None
        return РАМКИ[язык][форма].format(ф=ф, о=о, впф=впф)
    if форма in ("согласен_что", "согласен_что_вы"):
        # ПОДЧИНЕНИЕ БЕРЁТ ТОЛЬКО ГЛАВНУЮ ПОВЕРХНОСТЬ ФАКТА: вторая (число
        # словом) потребовала бы второго придаточного, а придаточное пишется
        # рукой, не выводится — и дом не станет его угадывать.
        к = i % len(ряд)
        при = ряд[к][0] if язык in ПРИДАТОЧНОЕ_РАВНО_ФАКТУ else ПРИДАТОЧНОЕ[язык][к]
        рамка = (СОГЛАСЕН_ВЫ[язык] if форма == "согласен_что_вы" else р["согласен_что"])
        return рамка.format(п=при, ф=ряд[к][0])
    к, поверхность = divmod(i, 2) if _ЧИСЛОМ_И_СЛОВОМ else (i, 0)
    запись = ряд[к % len(ряд)]
    ф, о, с = запись[0], запись[1], запись[2]
    if поверхность and len(запись) > 3:
        ф = запись[3]
    elif поверхность:
        return None
    return р[форма].format(ф=ф, о=о, с=с)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for форма in ФОРМЫ:
            if форма == "силлогизм":
                for i in range(len(ИЕРАРХИЯ[язык])):
                    с = страница(язык, форма, i)
                    if с:
                        вон[с] = (язык, форма)
                continue
            if форма.startswith("принадлежность"):
                for i in range(len(КЛАССЫ[язык])):
                    вон[страница(язык, форма, i)] = (язык, форма)
                continue
            if форма == "общего":
                for i in range(len(list(пары_класса(язык)))):
                    вон[страница(язык, форма, i)] = (язык, форма)
                continue
            if форма == "лишнее":
                for i in range(len(list(тройки_лишнего(язык)))):
                    вон[страница(язык, форма, i)] = (язык, форма)
                continue
            if форма == "согласен_что_вы" and язык in БЕЗ_РАЗЛИЧИЯ_РЕГИСТРА:
                continue          # язык без различия пишет ОДНУ форму
            шагов = (len(ФАКТЫ[язык]) if форма.startswith("согласен_что") or форма == "почему_прямо"
                     else 2 * len(ФАКТЫ[язык]))
            for i in range(шагов):
                с = страница(язык, форма, i)
                if с:
                    вон[с] = (язык, форма)
    return вон


ПОКАЗЫ = _показы()


# ПОДСУДНОСТЬ ЕСТЬ РАМКА ЦЕЛИКОМ, А НЕ «ВСЯКАЯ СТРОКА» (М-180-f2 — дом шкалы
# судил 128 чужих показов, взяв за подсудность НАЧАЛО рамки). Первая проба
# этого дома брала подсудным ВСЁ, и палата назвала ложью все 1099 показов дома
# бытовых тем: суд, судящий всё, есть не суд, а захват.
#
# Рамка обращается в образец, где всякая дыра связана ОБЪЯВЛЕННЫМ рядом: {ф} —
# факт (обеими поверхностями), {о} — основание, {с} — следствие, {п} —
# придаточное, {ч}/{к} — член и класс. Строка подсудна, лишь если совпала с
# образцом ЦЕЛИКОМ; тогда перестановка объявленных частей («лёд плавает в
# воде. почему? потому что камень тяжелее воды.») подсудна и ложна, а чужой
# показ не подсуден вовсе.
def _образцы():
    import re
    вон = []
    for язык in ЯЗЫКИ:
        ряды = {
            "ф": [з[0] for з in ФАКТЫ[язык]] + [з[3] for з in ФАКТЫ[язык] if len(з) > 3],
            "о": [з[1] for з in ФАКТЫ[язык]],
            "с": [з[2] for з in ФАКТЫ[язык]],
            "ч": [ч for ч, _ in КЛАССЫ[язык]],
            "к": [к for _, к in КЛАССЫ[язык]],
            "п": ([з[0] for з in ФАКТЫ[язык]] if язык in ПРИДАТОЧНОЕ_РАВНО_ФАКТУ
                  else list(ПРИДАТОЧНОЕ[язык])),
            # дыры силлогизма: класс, класс с квантором, надкласс и стянутый
            # союз — БЕЗ НИХ рамка силлогизма не попадала в образцы, а мир
            # ЗАМКНУТ: строка своего мира, не узнанная образцом, есть ложь, и
            # ворота отвергли все 25 силлогизмов разом
            "впф": list(ВОПРОС_ПОЧЕМУ.get(язык, ())),
            "ч1": [ч for ч, _ in КЛАССЫ[язык]], "ч2": [ч for ч, _ in КЛАССЫ[язык]],
            "ч1р": [_род(язык, ч) for ч, _ in КЛАССЫ[язык]], "ч2р": [_род(язык, ч) for ч, _ in КЛАССЫ[язык]],
            "км": list(ОБЩЕЕ[язык]["мн"].values()),
            "ч3": [ч for ч, _ in КЛАССЫ[язык]], "к3": [к for _, к in КЛАССЫ[язык]],
            "кв": [кв for _, кв, _ in ИЕРАРХИЯ[язык]],
            "н": [н for _, _, н in ИЕРАРХИЯ[язык]],
            "чт": ([("qu'" if ч[:1].lower() in (РАМКИ[язык].get("гласные_стяжения") or "")
                     else "que ") + ч for ч, _ in КЛАССЫ[язык]]
                   if РАМКИ[язык].get("гласные_стяжения") else []),
        }
        альт = {к: "(?:" + "|".join(re.escape(з) for з in sorted(set(р), key=len, reverse=True)) + ")"
                for к, р in ряды.items() if р}
        for форма in ФОРМЫ:
            # вежливая рамка живёт в своём словаре; язык без различия её не имеет
            if форма == "согласен_что_вы":
                if язык in БЕЗ_РАЗЛИЧИЯ_РЕГИСТРА:
                    continue
                рамка = СОГЛАСЕН_ВЫ[язык]
            elif форма == "общего":
                рамка = ОБЩЕЕ[язык]["рамка"]
            else:
                рамка = РАМКИ[язык][форма]
            куски, конец, годно = [], 0, True
            for м in re.finditer(r"\{(\w+)\}", рамка):
                куски.append(re.escape(рамка[конец:м.start()]))
                if м.group(1) not in альт:
                    годно = False
                    break
                куски.append(альт[м.group(1)])
                конец = м.end()
            if годно:
                куски.append(re.escape(рамка[конец:]))
                вон.append(re.compile("^" + "".join(куски) + "$"))
    return tuple(вон)


ОБРАЗЦЫ = _образцы()


def судить(строка):
    """(судимо, истинно): показ дома, или ложь. Мир ЗАМКНУТ."""
    с = строка.strip()
    if not с or not any(о.match(с) for о in ОБРАЗЦЫ):
        return False, False
    return True, с in ПОКАЗЫ


def main():
    # МУТАНТЫ — все ТРИ в рамках дома, ибо подсудность есть рамка целиком:
    # чужое основание, чужой класс, чужое следствие. Четвёртый мутант,
    # который просился, — «{факт}. {основание}.» без вопроса — дому НЕ
    # подсуден и подсуден быть не должен: строка без вопроса есть рамка
    # обменного рынка holon, и захватывать её этот дом не вправе.
    поймано = 0
    for язык in ЯЗЫКИ:
        ф0, о0, с0 = ФАКТЫ[язык][0]
        ф1, о1 = ФАКТЫ[язык][1][0], ФАКТЫ[язык][1][1]
        ч0, к0 = КЛАССЫ[язык][0]
        _, к1 = КЛАССЫ[язык][1]
        мутанты = (РАМКИ[язык]["основание"].format(ф=ф0, о=о1, с=с0),
                   РАМКИ[язык]["принадлежность"].format(ч=ч0, к=к1),
                   РАМКИ[язык]["следствие"].format(ф=ф0, о=о0, с=ФАКТЫ[язык][1][2]))
        for м in мутанты:
            судимо, истинно = судить(м)
            поймано += 1 if (судимо and not истинно) else 0
        print(f"  {язык}: {страница(язык, 'основание', 0)[:96]}")
    print(f"  мутантов поймано: {поймано} из {3 * len(ЯЗЫКИ)}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, "
          f"фактов {len(ФАКТЫ['ru'])}, классов {len(КЛАССЫ['ru'])})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
