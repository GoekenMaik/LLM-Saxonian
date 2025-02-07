import re
import json

def format_data(text):
    """
    Reformats the input text into a list of dictionaries, 
    where each dictionary contains a question and its corresponding answer.
    """
    data = []
    
    # Split the text into question and answer blocks
    blocks = re.split(r"(Fragen:|Antwoorten:)", text, flags=re.IGNORECASE)

    # Remove empty strings and whitespace from the blocks
    blocks = [block.strip() for block in blocks if block.strip()]

    # Iterate through the blocks, pairing questions with answers
    for i in range(0, len(blocks), 2):
        if i + 1 < len(blocks) and blocks[i].lower() == "fragen:" and blocks[i+1].lower() == "antwoorten:":
            continue
        if i + 1 < len(blocks) and blocks[i].lower() == "fragen:" and blocks[i+1].lower() != "antwoorten:":
            questions_block = blocks[i+1]
            
            if i + 2 < len(blocks) and blocks[i+2].lower() == "antwoorten:":
              answers_block = blocks[i+3]
            else:
              answers_block = blocks[i+2]
        
            
            # Split the question and answer blocks into individual questions and answers
            questions = re.findall(r"\d+\.\s*(.+)", questions_block)
            answers = re.findall(r"\d+\.\s*(.+)", answers_block)
            
            # Create dictionaries for each question-answer pair
            for j in range(min(len(questions), len(answers))):
                data.append({
                    "question": questions[j].strip(),
                    "answer": answers[j].strip()
                })

    return data

text = """Fragen:
1. Woneem is Helmut Schön boren un woneem hett he leevt?
2. Welke Mannschap hett Helmut Schön in' Oktober 1965 gegen Schweden speelt un wat weer dat Resultat vun dat Speel?
3. Welche Weltmeesterschap hett Helmut Schön mit de düütsch Natschonalmannschap wunnen?
4. Woneem is Helmut Schön 1978 doodbleven?
5. Welke Ehrenbezeichnung hett Helmut Schön in' September 2015 kregen?

Antwoorten:
1. Helmut Schön is in Bremen boren un hett in Wiesbaden leevt.
2. De düütsch Natschonalmannschap hett gegen Schweden mit 3:0 Doren wunnen.
3. Helmut Schön hett mit de düütsch Natschonalmannschap an' 17. Juni 1974 in Belgrad den Titel vun de Weltmeesterschap wunnen.
4. Helmut Schön is doodbleven in Wiesbaden.
5. Helmut Schön hett den Breefmark "100 Jahre Helmut Schön" kregen.

Fragen:
1. Wo hett dat mit de Schenen to doon? 
2. Wie warrt de Töög in de Iesenbahn billt? Gifft dat en Lokomotiv, dat de Wogens treckt?
3. Wo hett dat mit den Damplokomotiven to doon?
4. Wie warrt de Iesenbahn in't 19. Johrhunnert utbaut? Gifft dat den Opdrag för de Linie Liverpool-Manchester?
5. Wo is de langste Iesenbahn up de Eer?

Antwoorten:
1. De Schenen sünd ut Stahl un heurn de Iesenbahn.
2. Dat gifft en Lokomotiv, dat de Wogens treckt. Achter de Lokomotiv hangt de Wogens.
3. De Damplokomotiven sünd ut hitten Damp andreven ward. Un an dat Enn vun dat 19. Johrhunnert güng dat denn ok mit de Elektroloks los.
4. Dat duer nich lang, denn wurrn de Damplokomotiven jümmers gauer. Un an dat Enn vun dat 19. Johrhunnert güng dat denn ok mit de Elektroloks los. De gröttste Erfinner weer woll de George Stephenson.
5. De Transsibirische Iesenbahn in Russland is de langste Iesenbahn up de Eer.

Fragen:
1. Wat is Fiktschoon in de Vertelltheorie? Wo hett dat mit de Würklikheed to doon?
2. Wie warrt Fiktschoon in de Literaturwetenschop ünnersöcht? Gifft dat ene Theorie vun de Fiktionalität?
3. Welke Soorten vun Fiktschoon gifft dat? Realistsche oder unrealistsche Fiktschoon?
4. Wie warrt Fiktschoon in de Kognitschoonspsychologie ünnersöcht? Gifft dat ene Theorie över den psychologischen Effekt vun Fiktionalität?
5. Wo finnt een Fiktschoonstheorie, un wat is dorbi to doon?

Antwoorten:
1. Fiktschoon is in de Vertelltheorie een Vertellen, de sik to’n groten Deel in de Fantasie vun Schriever un Leser afspeelt.
2. In de Literaturwetenschop warrt Fiktschoon ünnersöcht, wat dat mit den Begriff Fiktionalität hett. Dor gifft dat ene Theorie vun de Fiktionalität, de sik op de Würklikheed stütt.
3. Realistsche Fiktschoon vertellt uutdachte Scheenisse, de in de Würklikheed scheen könnt. Unrealistsche Fiktschoon beschrivt Scheenisse, de unmööglik in’n echten Leven sind, vanwegen dat se övernatüürlich sünd.
4. In de Kognitschoonspsychologie warrt Fiktionalität ünnersöcht, wat dat mit den psychologischen Effekt vun Fiktionalität hett. Gifft dat ene Theorie över den psychologischen Effekt vun Fiktionalität, de sik op den Leser richten deit.
5. Dat gifft een Fiktschoonstheorie, de sik op den Begriff Fiktionalität utdrücken deit un wat dat mit den Würklikheed to doon hett. Dor is ok ene Theorie över den psychologischen Effekt vun Fiktionalität to finnen.

Fragen:
1. Wo warrt dat Woort "Antike" in Düütschland bruukt un wat bedüden dat?
2. Wie warrt de Tied vun de Antike bestimmt? Wann is dat Enn vun de Antike?
3. Wat gifft dat to'n Begreep vun de Antike, wenn man den Islam in't Bild bringt?
4. Wo hett de antike Kultur anfangen un wat hefft de Greken un Römers dorbi maakt?
5. Wie warrt de Tied vun de Antike ünnerscheedlich? Wann is dat Anfang vun de Statenwelt in Grekenland?

Antwoorten:
1. Dat Woort "Antike" warrt in Düütschland bruukt för de Ole Tied in de Länner rund um de Middellannsche See to. Op Nedderlandsch warrt vun de Klassieke oudheid snackt, op Engelsch heet de Antike Classical antiquity.
2. De Tied vun de Antike is bit an dat Johr 476 oder ok bit to’n Dood vun den ooströömschen Kaiser Justinian I. in dat Johr 565. Vun de Arbeit vun den belgischen Historiker Henri Pirenne af an warrt ok dat Johr 632 as Enn vun de Antike vörslahn.
3. Mit den Begreep vun de „Antike“ warrt an un for sik de Geschicht vun dat Ole Grekenland, vun’n Anfang bit hen to de klassische Tied, dorto de Historie vun den Hellenismus un vun dat Röömsche Riek betekent. Vun dat 1. Johrhunnert n. Chr. af an hett Rom ja de Gemarken um de Middellannsche See hen in siene Grenzen tohopenfaat’. Annere Völker un Kulturen hefft denn blot noch en Rull speelt, wenn se mit Greken un Römers wat to kriegen harrn.
4. De antike Kultur anfangen is up de Tied, wo Homer siene Epen tostanne kamen sund un wo dat losgung mit de Greeksche Kolonisatschoon rund um de Middellannsche See rüm. Dat weer in dat 8. Johrhunnert v. Chr.. De Greken hefft ehre Kultur in de Johrhunnerte dornah denn utbreedt in all Gemarken um de Middellannsche See to un ok an de Küsten vun de Seen, de dor vun afgüngen.
5. De Tied vun de Antike is ünnerscheedlich. Dat gifft dat för den Anfang vun de Statenwelt in Grekenland bit hen to dat Enn vun dat Weströömsche Riek in dat Johr 476 oder ok bit to’n Dood vun den ooströömschen Kaiser Justinian I. in dat Johr 565. Ok de Kultur vun Minos un vun Mykene vun um un bi 1900 bit 1100 v. Chr. un de so nömmten „Düüstern Johrhunnerte“ 1200 v. Chr. bit 750 v. Chr. warrt to de Antike mit reken.

Fragen:
1. Wo hett dat mit de plattdüütsche Schrieveree in Düütschland to doon?
2. Wie warrt de plattdüütsche Schrieveree in de Nedderlannen utbillt un föödert?
3. Wo hett dat mit den Schrievers in Drenthe to doon? Gifft dat ene wichtig Schrievers in Drenthe, as Jan Glas?
4. Wie warrt de plattdüütsche Schrieveree in Grunneng utbillt un föödert?
5. Wo hett dat mit den Schrievers op Plautdietsch to doon? Gifft dat ene wichtig Schrievers op Plautdietsch, as Arnolt Ditj?

Antwoorten:
1. De plattdüütsche Schrieveree is nich mehr so wichtig, as dat in’t 19. Johrhunnert weer.
2. Dat gifft ok in de Nedderlannen ene wichtig Schrievers op Platt, as Jan Boer un Sien Jensema ut Grunneng.
3. Ja, dat gifft ene wichtig Schrievers in Drenthe, as Jan Glas, de Freudenthal-Pries 2006 kregen hett.
4. Dat gifft ok in Grunneng ene wichtig Schrievers op Platt, as Jan Boer un Sien Jensema.
5. Ja, dat gifft ene wichtig Schrievers op Plautdietsch, as Arnolt Ditj un Ruben Ap.

Fragen:
1. Wat is Wetenschop? Wo hett dat mit Wetenschop to doon?
2. Wie warrt Wetenschop utbüxt? Welke Schritt föhrt een dör, wenn een wetenschoplich Arbeet maken will?
3. Woneem warrt Wetenschop in de Tiet opdeelt? Wo hett dat mit den Indelen na de söven Künst to doon?
4. Wie warrt Wetenschop geiht faaken na düsse Schritt för sick? Welke Kriterien mutt een sik anholen, wenn een wetenschoplich Arbeet maken will?
5. Wo hett dat mit den Bewies in de Wetenschop to doon? Wat is en Bewies oder vun de Theorien oder Nawies, dat se falsch sünd?

Antwoorten:
1. Wetenschop is all dat, wat de Minschen rutkreegen hebbt över Minsch un Natur as ok dat Ünnersöken vun Tosamenhäng un Saken, de opstunns noch nich verstahn warrt.
2. De modernen wetenschopliche Methoden gaht trüch op Francis Bacon. Een kann sik an sünnere Kriterien hollen: Objektivität, Reliabilität, Validität un Wetenschop geiht faaken na düsse Schritt för sick.
3. In de olle Tiet weer de Indelen na de söven Künst (lat. Artes). Dor weer ok de Astronomie bi, de fröher ok de Astrologie as Deel harr. Hüüt warrn de Wetenschoppen faaken so indeelt: Natuurwetenschoppen, Geisteswetenschoppen un Sellschopswetenschoppen.
4. Bi wetenschoplich Arbeet is dat wichtig, sik an Kriterien as Objektivität (dat Weten schall nich vun persönliche Ansichten afhangen), Reliabilität (de Resultaten müssen bi Wedderhalen to'n sülven Resultat föhren) un Validität (dat meeten warrt, wat meeten warrn schall) to hollen.
5. Dat heet, dat se verifizeert oder falsifizeert warrn kann. Een mutt ok so opschreven, wat een rutkregen hett, un in Tiedschriften un Beukers openbar moken.

Fragen:
1. Wo hett dat mit den Artikel in't Plattdüütsche to doon?
2. Wie warrt de Konjugatschoon von Verben in't Plattdüütsche billt? De Verben warrt konjugeert, wat dat meent?
3. Wo hett dat mit den Tied bi Verben to doon? Gifft dat Präsens, Präteritum, Perfekt un Plusquamperfekt, oder gifft dat noch annere Tieden?
4. Wie warrt de Hülpsverben in't Plattdüütsche bruukt? 
5. Wo hett dat mit den Mehrtall to doon in't Plattdüütsche?

Antwoorten:
1. De Artikel in't Plattdüütsche sünd 'de', 'dat' un 'een'. In'n Gegensatz to'n Hoochdüütsche gifft dat weniger Fällen, un de Genitiv is meist verswunnen.
2. Dat heet, dat se sik ännert. Wenn ik wat do heet dat anners ans wenn du dat deist oder se dat doot oder gor wenn ik wat doon harr. Dat heet, dat kümmt dorop an, welk Person dat is, wat dat Eentall oder Mehrtall is un vör allens, wat för en Tiet dat is.
3. Ja, dat gifft dat. De Präsens is för dat, wat nu is. Dat Präteritum is för dat, wat weer (verleden Tiet). Dat Perfekt is för dat, wat jüst vörbi is un dat Plusquamperfekt is för dat, wat all lang vörbi is.
4. De Hülpsverben sünd: sien/wesen, hebben, wullen, schallen (sallen), doon, warrn, könen, mögen, möten, dörven. De Hülpsverben hebbt t.B. mit de Tied to doon.
5. In't Plattdüütsche gifft dat verscheden Aarten, den Mehrtall to billen: -en (t.B. Dag - Dagen), -s (t.B. Jung - Jungs), oder ok keen Enn (t.B. Mann - Mannlüüd). Dat is nich jümmers licht, de richtige Form to finnen.

Fragen:
1. Wat is Historie in de plattdüütsche Spraak? Wo kummt dat Woort her un wat bedüden kann dat?
2. Wie warrt de Tied bi Verben in't Plattdüütsche billt? Gifft dat Präsens, Präteritum, Perfekt un Plusquamperfekt?
3. Wat is en Hülpsverb in't Plattdüütsche? Wie warrt dat bruukt un wat bedüden kann dat?
4. Wie warrt de Mehrtall in't Plattdüütsche billt? Gifft dat mehr oder minner een Schema?
5. Wat is Historie in de plattdüütsche Spraak? Wo kummt dat Woord her un wat bedüden kann dat?

Antwoorten:
1. Historie is de Leer vun verleden Tieden, Zivilisatschonen un Sellschoppen.
2. De Tied warrt in't Plattdüütsche billt as Präsens för dat, wat nu is, Präteritum för dat, wat weer (verleden Tiet), Perfekt för dat, wat jüst vörbi is un dat Plusquamperfekt för dat, wat all lang vörbi is.
3. En Hülpsverb is en lütte Verb, de tosamen mit een anner Verb staht un denn wat an de Bedüden ännert. De köönt ok alleen stahn. Hülpsverben sünd: sien/wesen, hebben, wullen, schallen (sallen), doon, warrn, könen, mögen, möten, dörven.
4. De Mehrtall köönt de plattdüütschen Wöör op verschedene Wies billen, un faken is de Mehrtall denn anners as in dat Hoochdüütsche. Bi de Mehrtaal gifft dat mehr or minner een Schema.
5. Historie is de Leer vun verleden Tieden, Zivilisatschonen un Sellschoppen. Dat Woord „Historie“ kummt van’t ooldgreeksche ἱστορία historía för „Kunn“, „Weten“ oder „Unnersöök“, wieldess dat Woord „Geschichte“ med den Verb „scheen“ tohopehängt un dat betekent wat scheen is.

Fragen:
1. Wo kummt dat Woort "Kunst" her un wat bedüden de Begriff Kunst?
2. Wat is de Bedüden vun den Begriff Kunst, wenn een sik dat vun sülvst versteiht?
3. Wie warrt en künstlerische Utsaag utbillt? Gifft dat ene bestimmte Lehr oder kann een ok op annere Weise utbillen warrn?
4. Wat is de Bedüden vun den Begriff Kreativität in't Kontext vun de Kunst?
5. Wie kummt de Kreativität bi enen groten Künstler her? Kann se ok utbaut warrn oder is dat faken so, as dat is?

Antwoorten:
1. Dat Woort "Kunst" kummt von "könen oder künnen" un bedüden allns, wat de Minsch mit utermaten Könen tostannbringt.
2. Dat heet, dat se will blots wat darstellen, wiesen oder utseggen un darmit de Tolüsterers oder Tokiekers to'n Nadenken anrögen.
3. De jungen Künstler gingen fröher bi enen Meister in de Lehr un keken sik de Kunstgrepen af. Hüüt besöökt se ene Kunstakademie oder ene Hoochschool un studeert all dat, wat neven dat Handwarkliche noch an Theorie nödig is.
4. De Kreativität is faken so, as dat is, un kann nich utbaut warrn. Se kummt bi enen groten Künstler vun binnen herut.
5. Bi enen groden Künstler kummt de Kreativität vun binnen herut un is darum faken dat, wat de echte Kunst utmaakt.

Fragen:
1. Wat is en Book un wat gifft dat för Böker?
2. Wo hett dat mit de Bibel to doon? Is se ok in't Plattdüütsche översett?
3. Wie warrt een Book bunnen? Wann is dat nötig, een Book bunnen to laten?
4. Wat gifft dat för Böker, wat nich bi de Kinner sünd? T.B. de Romaan
5. Wo hett dat mit den Druck vun en Book to doon? Wie warrt dat Book druckt?

Antwoorten:
1. Dat is Papeer, wat bunnen is un wo wat binnen steiht.
2. Ja, se is ok in't Plattdüütsche översett. De Bibel is de Hillige Schrift.
3. Wenn een Book veele Sieden hett, warrt dat bunnen. Dat mookt de Bookbinner. Wenn dat bannig veele Sieden sünd, dat mookt de Bookbinner mehr Bände.
4. Alle Böker, egal wat dor insteiht, hebbt mindest enen Schriever hatt. De Romaan is een grötteret Vertellen un gifft dat för Kinner, Leevesromaan, Tokumstromaan, Krimsche, Billerbook.
5. Um de Sieden to moken, bruukt een’n Papeer. Üm dat wat op to schrieven, ohn dat een dat veel mol kopeern mutt, warrt dat Book druckt. De Technik dorför heet Bookdruckeree. Ok de Billers warrt so in dat Book druckt.

Fragen:
1. Woher kümmt dat Woort „Minsch“ un wat bedüden doot?
2. Wie is de Naam „Homo sapiens“ utkamen un wat he bedüden doot?
3. Wann is de moderne Minsch opkamen un wo hett he vörher leevt?
4. Wo hett de Homo sapiens sien Tahl vun Lüde anstegen? Un warrt dat noch so gau gahn?
5. Wie is de Naam „Homo sapiens“ utkamen un wat he bedüden doot?

Antwoorten:
1. Dat Woort „Minsch“ (Hoochdüütsch Mensch, Sweedsch människa, Däänsch menneske) is en Variant vun „Mann“, (as up Düütsch, Engelsch: man). Amenne geiht düt Woort torüch op den indogermaanschen Stamm *„man-“: „denken“ oder *„ma-“: „meten“. Düsse Stamm is ok to finnen in latiensch „mens, mentis“: „Geist, Verstand“, „memoria“: „Gedächtnis, Erinnerung“, Greeksch „menos“: „Geist“, „mnèmè“: „Gedächtnis“, Sanskrit „man-“: „Denken, Geist“, Russisch „mnit“: „menen, denken“. In dat ooldindische gifft dat „Manu“: „(Oor-)minsch“, in dat moderne Hindi „manusha“: „Minsch, Mann“.
2. De wetenschoppliche Naam vun den modernen Minschen is Homo sapiens. He kümmt ut de Latiensche Sprake. Dat Woort „homo, hominis“ is villicht verwandt mit „humus“: „Eer, Land“.
3. Vör um un bi 40.000 Johren is de moderne Minsch in Europa as Cro-Magnon-Minsch henkamen. In Afrika harr he avers al veel länger leevt. Düsse „Afrikaners“ sünd as Vörlöpers vun den Cro-Magnon-Minschen ankeken wurrn.
4. De Homo sapiens is in de Tiet vun 107,5 Milliarden Minschen boren wurrn. Dat gifft nich bloß en Tahl vun Lüde, man ok en Tahl vun Generatschonen un Aartengeschichten. Un wenn dat noch so gau gahn deit, denn is dat noch nich rutkamen.
5. De Naam „Homo sapiens“ is utkamen ut de Latiensche Sprake. Dat Woort „homo, hominis“ is villicht verwandt mit „humus“: „Eer, Land“.

Fragen:
1. Wo hett dat mit de Kriterien to doon? Welke Religionen warrt denn as Weltreligion ansehn un wat sünd de wichtigsten Kriterien?
2. Wie warrt de Tall vun Liddmaten in de Religion bestimmt? Un welke Religionen hebbt en grote Tall vun Liddmaten?
3. Wo hett dat mit den Missionaarschen Ansprook to doon? Welche Religionen hett'n missionaarschen Ansprook un welche Religionen maakt dat nich?
4. Wie warrt de Religion in groten Delen vun de Welt finnt? Un welke Religionen finnt sik in groten Delen vun de Welt?
5. Wo hett dat mit den Jödendom to doon? Is dat ok en egen Weltreligion oder is dat en Wörtel vun Christendom un Islam?

Antwoorten:
1. De wichtigsten Kriterien sünd: de Religion hett en grote Tall vun Liddmaten, de Religion finnt sik in groten Delen vun de Welt un de Religion hett’n missionaarschen Ansprook.
2. De Tall vun Liddmaten warrt bestimmt, wenn een jümmer mehr as een Mio. Anhängers hebbt. Dat gifft denn noch vele Religionen mit weniger Liddmaten, man se sünd nich in disse List toföhrt.
3. De Religionen, de den missionaarschen Ansprook hett, sünd dat Christendom un de Islam. De Buddhismus un de Hinduismus maakt dat nich. Juud oder Hindu warrt een tomehrst dör de Geboort.
4. De Religionen, de sik in groten Delen vun de Welt finnt, sünd dat Christendom, de Islam, de Buddhismus un de Hinduismus.
5. Dat Jödendom is nich ok en egen Weltreligion, man een Wörtel vun Christendom un Islam. Dat gifft keen aktive jüüdsche Mission.

Fragen:
1. Wo is Sassen anlegen? Woneem grenzt dat Land an?
2. Wie hett Sassen 1918 ut wat billt un worüm?
3. In welke Bezirke keem dat Freestaat Sassen in den Naam vun de DDR 1990 wieder?
4. Wo is de Hööftstadt vun Sassen? Welk is de gröttste Stadt?
5. Woneem leevt up 18.451,51 km² 4.254.000 Inwahners (30. September 2006) in Sassen?

Antwoorten:
1. Sassen grenzt an Polen un Tschechien. Todem grenzt Sassen an de Bundslänner Bayern, Döringen, Sassen-Anholt un Brannenborg.
2. De Freestaat Sassen hett sik 1918 ut dat Königriek Sassen billt. Düütschland weer nu Republiek un de König afsett.
3. In den Naam vun de DDR 1990 weer dat Freestaat Sassen in siene Grenzen vun 1952 wedder tostannen kamen. Dat keem an de Bezirke Leipzig, Dresden un Chemnitz.
4. De Hööftstadt is Dresden, de gröttste Stadt is Leipzig.
5. Up 18.451,51 km² leevt 4.254.000 Inwahners (30. September 2006) in Sassen.

Fragen:
1. Wat heet Prosa un wat is de Differenz twuschen Prosa un Verse?
2. Wie hett dat mit den Begreep Prosa in de Literatur utsehn? Wann is Prosa först in de Neetied as ene Form vun Literatuur ankeken wurrn?
3. Wat gifft dat, wat as Prosagenres tosamenfaat warrt un wat sünd se denn?
4. Wie kann Prosa ok upbaut weern? Gifft dat faste Regels för den Textkompitschoon vun Prosatexten oder nich?
5. Woneem is de Begreep Prosa in den Text utdrückt, un warrt he bloot in de Eentaal bruukt?

Antwoorten:
1. De Begreep Prosa bedütt unbunnen Sprake, anders as bunnen Spraakformen as Verse, Riemels oder rhythmische Sprake.
2. Dat Woord givt’t bloot in de Eentaal un een Schriever oder ene Schrieversche, de alleen oder to’n groten Deel Prosa affaat, is een Prosaist.
3. Prosagenres sünd to’n Bispeel Romane, Novellen, Vertellens, Kortgeschichten, Essays, Feuilletons, Memoirenliteratuur, Biografien, Breve, allerhand Slag Saaktexte un heel de wetenschoplike Literatuur.
4. Prosatexten kann ok opbaut weern mit rhythmische Elemente oder rhetoorsche Figuren, wat den Inhoold düüdliker to’n Uutdruck bröcht.
5. De Begreep Prosa is in den Text utdrückt un warrt bloot in de Eentaal bruukt.

Fragen:
1. Wo hett dat mit den Ball to doon in Football? 
2. Wie warrt een Football-Speel utbillt? Gifft dat een Speelfeld, een Mannschop un en Halftied?
3. Wo hett dat mit de Hööchstklass in Düütschland to doon? Gifft dat een Profi-Football-Liga oder gifft dat noch annere klassen?
4. Wie warrt Football utbillt för Fruunslüü? Gifft dat ene Speel, wo de Fruunslüü mit elkanner uttreten sünd?
5. Wo hett dat mit den düütschen Mannslü in Football to doon?

Antwoorten:
1. De Ball warrt mit de Füten un ok mit den Kopp speelt. Dat geiht dorüm, den Ball in dat Door vun de anner Mannschop to spelen.
2. Een Speelfeld is een Reecheck mit Doren an de korten Sieden un een Speel geiht 90 Minuten. Na een Dreeveertelstünn is Halftied un denn ward Foffteihn maakt. Na de Halftied warrt de Sieden wesselt.
3. In Düütschland gifft dat de hööchste Speelklass, de Eerste Football-Bundsliga. Dor sünd 18 Verenen in togange un in’n Momang löppt de Saison 2023/2024.
4. De düütsche Fruunslüü hebbt nu in 't Weltmeesterschop 2023 spöölt, aver sünd in 't Vörrund utschkeden. In Düütschland gifft dat Football vun de Mannslü un vun de Fruunslü.
5. De düütsche Mannslü wassen 2014 de Weltmeesters un hebbt danaach nich eenmal de Vörrund överstaan (2018 in Russland un 2022 in Kataar).

Fragen:
1. Wat is Künstlike Intelligenz (K.I.) un wat kann dat doon?
2. Wie warrt Künstlike Intelligenz utbillt? Kann dat leren?
3. Wo hett dat mit den Bruuk vun Künstlike Intelligenz to doon? Gifft dat to’n Bispeel virtuelle Assistenten oder Söökmaschinen, de sülvenst wat lernen könnt?
4. Wie warrt Maschinenleren in Künstlike Intelligenz bruukt? Gifft dat to’n Bispeel Gesichtserkennunge oder automaatsche Spraaköversetters?
5. Wo kann een mehr över Künstlike Intelligenz lesen? Gifft dat en Book, dat den Inholt vun dissen Text so goot as mööglich afdeckt?

Antwoorten:
1. Künstlike Intelligenz is een Systeem, dat Daten van buten richtig düden un uutleggen kann, uut düssen Daten leren kann, un wat dat Systeem uut düssen Daten leert het up niege Upgaven anpassen un överdregen kann oder de glieke Upgave effitscheter lösen kann.
2. Künstlike Intelligenz un Maschinenleren bruukt to’n Bispeel: Söökmaschinen, virtuelle Assistenten, Faartüge, de sülvenst faart, automaatsche Spraaköversetters, Gesichtserkennunge oder Onlinereklame, de up den Bruker sienen Internetverloop tosneden is.
3. Ja, dat gifft to’n Bispeel virtuelle Assistenten oder Söökmaschinen, de sülvenst wat lernen könnt. Ok Gesichtserkennunge un automaatsche Spraaköversetters warrt in Künstlike Intelligenz bruukt.
4. Maschinenleren is in Künstlike Intelligenz bruukt, um dat Systeem to helpen, wat dat lernen kann. Dat gifft to’n Bispeel Gesichtserkennunge oder automaatsche Spraaköversetters, de sülvenst wat leren könnt.
5. Een kann mehr över Künstlike Intelligenz lesen in den Book "Artificial Intelligence: A Modern Approach" vun Stuart J. Russell un Peter Norvig. Ok dat Book "Artificial Intelligence" vun Elaine Rich, Kevin Knight un Shivashankar B. Nair is en good Book för de Lüüd, de mehr över Künstlike Intelligenz lehren wullen.

Fragen:
1. Wo is Indien un wat gifft dat dor för Inwahners?
2. Wie warrt Indien politisch regert? 
3. Welke Spraken sünd in ganz Indien Amtsspraken?
4. Wo sünd de gröttsten Städer vun Indien?
5. Woneem is de Hööftstadt van Indien un wat is dor de Baas vun de Regeerung?

Antwoorten:
1. Indien is en Land in Asien, dat dor 1.293.057.000 Inwahners leevt op 3.287.590 km².
2. Indien is en Bundsrepublik un dor is de Präsidentsche as Hööft vun den Staat anstellt, de Baas vun de Regeerung is Manmohan Singh.
3. Amtsspraken in ganz Indien sünd Engelsch un Hindi. Spraken, de in bestimmte Delen vun Indien as Amtsspraken gellen doot, sünd Asamiya, Bengaalsch, Bodo, Dogri, Gujarati, Kannada, Kashmiri, Konkani, Maithili, Malayalam, Marathi, Meitei, Nepali, Oriya, Punjabi, Santali, Sanskrit, Sindhi, Tamilsch un Telugu.
4. De gröttsten Städer vun Indien sünd Mumbai (fröher: Bombay), Delhi, Bangalore, Kalkutta un Chennai.
5. Nee-Delhi is de Hööftstadt van Indien un Manmohan Singh is dor de Baas vun de Regeerung.

Fragen:
1. Wo hett dat mit den Utwickeln vun Theoter to doon? Wann is dat anfungen, Theoter to spelen?
2. Wie warrt en Theaterstück in't Plattdüütsche speelt? Gifft dat Snacktheoter oder Tragödien?
3. Wo hett dat mit den Oorten vun Stücken to doon? Gifft dat Drama, Komödie, Lustspeel un Oper?
4. Wie warrt en Operette un en Musical in't Plattdüütsche speelt? Gifft dat ok Musiktheoter?
5. Wo hett dat mit den Oosterspeel to doon? Wann is dat anfungen, Theoter to spelen?

Antwoorten:
1. Wi weet nich, wannehr dat anfungen hett, Theoter to spelen. De olen Greken hebbt dat to richtige Theoters bröcht un ut de Tied (so wat bi 500 vör Christus) sünd ok de eersten opschreven Theoterstücken.
2. Dat gifft Snacktheoter, wo tomeist snackt warrt un blots af un an wat sungen warrt. Tragödien sünd to’n Bispill Hans Brüggemann vun Hans Ehrke.
3. Dat gifft ’n Slag ünnerscheedliche Oorten vun Stücken, as Drama, Komödie, Lustspeel un Oper. Ok Musiktheoter gifft dat, wo dat mehr üm de Musik geiht un nich so üm dat Snacken.
4. Operetten un Musicals sünd lieksterwelt as en Operett, bloots mit modernere Slagers. Dat gifft ok Musiktheoter, wo dat mehr üm de Musik geiht un nich so üm dat Snacken.
5. De Oosterspeel is een ole Kultursaak un en Vergneugen togliek. Dat Speel heet Theoter un dat Huus, wo Theoter speelt warrt, ok. Gifft ok de Utdrück Speeldeel, Speelkoppel un Theatergrupp för Lüüd, de Theaterstücken spelen doot. De Oosterspeel is vandaag noch in Hamborg to sehn.

Fragen:
1. Wat is en Reekner un wat hett he to doon?
2. Wie warrt en Computer utbillt? Welke Bestanddeelen gifft dat in'n Inbott vun en Computer?
3. Wo hett dat mit de Grött vun de Reekners to doon? Gifft dat grote Reekners un lütte Reekners?
4. Wie warrt en Computer mit annere Computern verbunnen? Gifft dat Nettwarken oder Internet?
5. Wat is KDE un wat hett dat mit Linux to doon?

Antwoorten:
1. En Reekner is en elektroonsch Rekenmaschien, de för dat Reken dor un ok för Texten schrieven, teken un speelen bruukt warrt.
2. De Hardware vun en Computer besteiht ut een Perzesser, den Slag Elektronik in'n Spieker (RAM) un de Fastplaat (Plattenspieker). Na de Grött ünnerscheed wi Personalcomputers, Desktops, Laptops, Mini-Computers, Mainframes.
3. Ja, dat gifft grote Reekners un lütte Reekners. De eersten Reekner weern bannig groot, so as en Kamer. Un können graad so'n beten wat vun dat, wat vundaag een lütten Taschenreekner kann.
4. Ja, dat gifft Nettwarken oder Internet. De meesten Reekners sünd Personalcomputers, de mitmanner to en Nettwark knütt sien köönt. Lütte Nettwarken heet LAN, grote as dat Internet WAN.
5. KDE is en grafisch Böversiet för dat Bedriefssystem Linux. Dat gifft dat nu ok op platt.

Fragen:
1. Wo liggt Neddersassen un wat is dat Bundsland?
2. Wie groot is Neddersassen un welke Länner grenzt dor an?
3. Welche Spraken warrt in Neddersassen snackt? Gifft dat ok annere Dialekten?
4. Woneem is de Hööftstadt vun Neddersassen un wat liggt dor an de Waterkant vun?
5. Wie hett Neddersassen sien Naam kregen un wat bedüden dat?

Antwoorten:
1. Neddersassen liggt in de Noorden un is een Bundsland, dat to de Bundsrepubliek Düütschland tohöört.
2. Neddersassen grenzt an Sleswig-Holsteen, Hamborg, Mekelborg-Vörpommern, Brannenborg, Schaumburg-Lippe, Hessen, Noordrhien-Westfalen un de Nedderlannen. An de Waterkant vun de Noordsee liggt dat Königriek vun de Nedderlannen.
3. In heel Neddersassen warrt traditschonell Plattdüütsch snackt, aver ok Hoogdüütsch is begäng. Ok Saterfreesch gifft dat noch in’t Saterland, man dat is lüttje un överall in Neddersassen is Hoogdüütsch begäng.
4. De Hööftstadt vun Neddersassen is Hannober un dat liggt an de Waterkant vun de Noordsee.
5. Neddersassen hett sien Naam kregen, as dat Volk vun de Sassen leev deed. Dat Volk vun de Sassen wöör in de Historie to’n Bundsland Sassen tohören un för dat fröhere Sassen wöör de Naam Neddersassen präägt.


Fragen:
1. Wo hett Tolstoi sien Leben anfangen?
2. Wat hett Tolstoi in den Krieg in’n Kaukasus maakt?
3. Wo hett Tolstoi sien Roman „Krieg un Freden“ schreven? Un wat is dor vun to seggen?
4. Wat hett Tolstoi mit de Religion to doon?
5. Wo hett Tolstoi sien Leven afslaten?

Antwoorten:
1. Tolstoi weer en Weetkind un hett mit negen Johre anfungen, un studeer orientaalsche Spraken an de Universität Kasan.
2. Tolstoi hett in den Krieg in’n Kaukasus as Fähnrich bi ene Brigade vun de Artillerie mitmaakt.
3. Tolstoi hett sien Roman „Krieg un Freden“ in Russland schreven. Dat is een Roman över den Krieg un de Freden, den he in’n Kaukasus maakt hett.
4. Tolstoi weer en Anarchisten, den siene Wuddeln in de Religion ehrn Grund harrn. He meen, datt geev an sik keene Wunner un sunnerlich konn he dor nix mit anfangen, datt in dat Avendmahl dat Brood in dat Fleesch vun Christus verwannelt weern scholl.
5. Tolstoi is an’n 20. November 1910 in Astapowo sturven un is dor ok inkuhlt wurrn.

Fragen:
1. Wo hett dat mit den Kohlenstoffdioxid in de Atmosphäär to doon?
2. Wie warrt Kohlenstoffdioxid in de Atmosphäär freestellt?
3. Wo hett dat mit den pH-Weert in’t Blood to doon? 
4. Wie warrt Kohlenstoffdioxid in Binnenrüüm freestellt?
5. Wo hett dat mit den Kohlenstoffdioxid in de Atmosphäär to’n Dood vun Minschen to doon? 

Antwoorten:
1. De Kohlenstoffdioxid-Konzentratschoon is jümmer ünner 280 ppm, man siet tomindest 650.000 Johren leeg se ok ünner 280 ppm.
2. Dat gifft dat bi’t Verbrennen vun fossile Brennstoffen un ok bi’t Nütten vun’t Land, man blots en lütten Deel vun’t Kohlenstoffdioxid is dorbi utnahmen.
3. Kohlenstoffdioxid kann de pH-Weert rünnersetten un dat Blood warrt cheemsch surer, wenn mehr Kohlenstoffdioxid in de Luft oder in’t Frischwater is.
4. De Kohlenstoffdioxid-Konzentratschoon kann överschreden warrn, wenn sik mehrere Lüüd över en längere Tiet in en lütten, slaten un goot isoleerten Ruum ophollen doot.
5. De Kohlenstoffdioxid-Konzentratschoon kann bi 8 % oder mehr to’n Dood vun Minschen föhren, wenn sik nich noog Suerstoff in’t Blood inföhrt warrt.

Fragen:
1. Wo hett Leonardo da Vinci leevt?
2. Wat weer sien Berop un wat hett he maakt?
3. Wie is Leonardo da Vinci mit Michelangelo inverstahn?
4. Was weer Leonardo da Vincis Eten? 
5. Wo hett Leonardo da Vinci doodbleven?

Antwoorten:
1. He leev in Florenz, Rom, Mailand un annere Städer.
2. He weer en Maler, Bildhauer, Architekt, Musiker, Mechaniker, Ingenieur un Naturphilosoph. Welke vun de Rebeden vun sien Arbeid weern Mechanik un Hydraulik.
3. Mit Michelangelo verstund he sik nich so goot. Dat is nich utdrückt in den Text, man dat kann ut den Satz "Mit Michelangelo verstund he sik nich so goot" afleiden warrn.
4. He weer Vegetarier un schreev in Spegelschrift.
5. Op’t Slott Clos Lucé, Amboise.

Fragen:
1. Wat is de Bedüden vun de Vereenten Natschonen?
2. Wie hett dat mit de Grünning vun de Vereenten Natschonen to doon? Wann is dat denn passert?
3. Wie veel Staten sünd hüüt Maten vun de Vereenten Natschonen?
4. Wat is den Freedensnobelpries för un woneem is he utdeelt?
5. Wie heet de aktuelle Generalsekretär vun de Vereenten Natschonen?

Antwoorten:
1. De Vereenten Natschonen sünd en Statenbund, de sik to Opgaav geven hett, internatschonaal Freden un Recht, de Gliekheit vun de Minschen un den weertschoplichen Uttuusch to fördern.
2. De Vereenten Natschonen hebbt sik 1945 na’n Tweten Weltkrieg as Opfolger vun den Völkerbund grünnt, nadem 51 Staten de Charta vun de Vereenten Natschonen ünnertekent harrn.
3. Hüüt sünd 193 Staten Maten vun de Vereenten Natschonen, wat meist all Staten op de Eer sünd.
4. De Institutschoon kreeg den Freedensnobelpries in’n Johr 2001.
5. De aktuelle Generalsekretär vun de Vereenten Natschonen is António Guterres.

Fragen:
1. Wo kümmt dat Woort "Religion" her un wat heet dat?
2. Gifft dat mehrere Arten von Religionen? Wenn ja, wo hett dat denn mit to doon?
3. Wie warrt den Gott in de Religionen dör den Gottsdeenst utdrückt? Woneem gifft dat den Gottdeenst?
4. Wo kümmt dat mit den Dood un wat gifft dat'n Leven na den Dood in de Religionen to doon?
5. Gifft dat mehrere Arten von Religionen, wo dat keen Gott gifft oder wenn een keen Gott hett? Wenn ja, woneem gifft dat denn so?

Antwoorten:
1. Dat Woort "Religion" kümmt ut dat Latinsche (religio) un heet Gloven.
2. Ja, dat gifft mehrere Arten von Religionen. Bi de Christen is dat in de Kark, bi de Juden tohuus un in de Synagogen, aver eerst siet de Tied, wo dat keen Tempel mehr gifft. Den harrn ja de Römers tweislaan. Bi de Muselmanen is dat de Moschee.
3. Meisttieds geiht dat in'n Gloven ok dorüm, wo de Minsch vun herkümmt un wo dat mit den Dood is un wat dat'n Leven na den Dood gifft. De olen Germanen harrn keen Tempel, man so'n hillig Holt.
4. Dat gifft mehrere Arten von Religionen, wo dat keen Gott gifft oder wenn een keen Gott hett. Gifft aver ok Religionen, wo dat keen Gott gifft, blots Spöken un Dämonen (Animismus). Un denn noch den Atheismus, wat meent, dat een keen Gott hett. Un denn noch den Agnostizismus, wat meent, dat een nich weet: Gifft dat een Gott? Gifft dat keen?
5. Bi de Muselmanen is dat de Moschee. Tempels geev dat ok bi de olen Ägypter, de Greken un de Römer. De olen Germanen harrn keen Tempel, man so'n hillig Holt. Weer ok so bi de olen Kelten.

Fragen:
1. Wo hett Katharina de Grote leevt un wat is se in Russland wesen?
2. Wie hett Katharina den Staat vun Russland reepen?
3. Welke Lüüt weern in't russ'sche Riek vun Katharina de Grote un wat hebbt se mit ehr maakt?
4. Wat sünd de Reformen, de Katharina de Grote maakt harr? Wo hett se dat för den Staat vun Russland maakt?
5. Welke Kriegen weern in't russ'sche Riek vun Katharina de Grote un wat weer de Insel Krim?

Antwoorten:
1. Katharina de Grote is 1729 in Stettin boren un is 1796 doodbleven. Se weer Zarin vun Russland.
2. Katharina hett den Staat vun Russland reepen, as se Zarin weern. Se hett na düütschen Vorbild reformeert.
3. Welche Lüüt weern in't russ'sche Riek vun Katharina de Grote, warrt nich in'n Text nöömt. De Hoor vun disse Lüüt sünd de Favoriten, to't Bispeel Münnich, un se weern ut Düütschland.
4. Katharina hett Reformen na düütschen Vorbild maakt. To'n Bispeel weer dat so dat de Staat, sünners de Hoff, bannig veel vun de Innahmen vun de Lüüt kreegen. De Reformen weern dorbi ok för den Staat vun Russland wichtig.
5. Katharina hett Upnahmen vun bannig wichtige törksche un poolsche Rebeden in't russ'sche Riek dor Kriegen. En Bispeel weer de Insel Krim.

Fragen:
1. Wo hett dat mit den Naam Jan in't Plattdüütsche to doon?
2. Woher kummt de Naam Jan?
3. Wie warrt den Naam Jan in annere Spraken un anner Formen utdrückt? 
4. Woneem is de Naam Jan in de Bibel vörkamen? 
5. Wat bedüden de beiden Jüngers Johannes, de in de Bibel vörkamen doot?

Antwoorten:
1. De Naam Jan is ut den greekschen Naam Ioannes kamen un heet dorbi „De Herr (JHWH) is gnädig“ oder ok „De Herr hett (sien) Gnaad sehn laten“.
2. Dat kummt wedder ut de hebreesche Spraak, wo dat Naam Yochanan heet. Dat bedüden: Düt Kind, dat so heten deit, is vunwegen Gott sien Gnaad op de Welt kamen.
3. Den Naam Jan gifft dat nich bloß in de plattdüütsche Spraak. Ok in dat Poolsche un in dat Tschechisch is dat een Vörnaam, de faken bruukt warrt. Ok nich veel anners heet dat in Italieensch (Gian) un in Franzöösch (Jean)
4. De beiden Jüngers Johannes sünd ut de Bibel bekannt. Dorüm is sien Naam mank de Christen in all Tieden ganz begäng.
5. Dat gifft nich veel annere Informationen över den Naam Jan in de Bibel, aver dat he in de Bibel vörkamen doot as een vun de Jüngers, de Jesus leevst hett.

Fragen:
1. Wo warrt Hindi snackt? Gifft dat ok in annere Länner?
2. Wie is Hindi mit Urdu verwandt? Sünd se Susterspraken oder gifft dat noch annere Verwandtschop?
3. Woneem is Hindi an de Siet vun Engelsch Amtsspraak wurrn? Gifft dat ok in annere Länner, wo Engelsch Amtsspraak is?
4. Woher kümmt Urdu? Is se ok en Susterspraak von Hindi oder gifft dat noch annere Verwandtschop?
5. Woneem gifft dat Lehn- un Frömdwöör ut Hindi in de düütsche un plattdüütsche Spraak? Gifft dat ok annere Länner, wo so veel Lehnwöör vun Hindi to finnen sünd?

Antwoorten:
1. Hindi warrt in de meisten Länner vun Noord- un Zentralindien snackt. Ok op Mauritius un Fidschi warrt dat snackt.
2. Hindi is en Susterspraak von Urdu. De beiden stimmt so wiet övereen, dat se tohopen faken as een Spraak ankeken weert.
3. Hindi is an de Siet vun Engelsch Amtsspraak in Indien an den 26. Januar 1965 wurrn. Man nich bloß in Indien warrt dat snackt, man ok op Mauritius un Fidschi.
4. Urdu is en Spraak, de ut de Wuddel rutwussen is, as Hindi. Se kiekt de beiden Spraken ok as Soziolekten an, vunwegen dat dat verscheden Gruppen ween sünd, de jem snackt hefft.
5. In de düütsche un plattdüütsche Spraak gifft dat allerhand Lehn- un Frömdwöör ut Hindi: Bhagwan, Chutney, Guru, Kuli, Punsch, Shampoo, Kummerbund, Dschungel, Kajal, Monsun. Dat sünd Wöör, de vun Hindi övernahmen warrt.

Fragen:
1. Wo is de Islam utkamen?
2. Is de Islam mit dat Christendom un dat Judendom verwandt?

Antwoorten:
1. De Islam is en monotheistische Religion, de sik op den Koran grünnt, so as Mohammed em kunddoon hett.
2. De Islam is mit Christendom un Judendom verwandt (Abrahamitsche Religionen). Moses un Jesus Christus warrt beid as Propheten ansehn, ok wenn Mohammed de gröttste ünner de Propheten is.

Fragen:
1. Wie hett de Zoroastrismus anfangen? Woneem is he gründt wurrn?
2. Wat glöövt de Zoroastriers över den Gott Ahura Mazda?
3. Wo sünd de Religionsgruppen Manichäers un Paulikianers mit'n Zoroastrismus in Verbindung stahn?
4. Wie hett sik de Zoroastrismus in de Tiet utwannert? Woneem is he noch vör to finnen?
5. Wo gifft dat noch ene Grupp mit christlichen Elementen, de an den Zoroastrismus denkt?

Antwoorten:
1. De Zoroastrismus is vun Zarathustra gründ't wurrn.
2. De Zoroastriers glöövt, dat de Welt böös is un vun ene böse Macht mookt wurrn is.
3. Bi't Turkvolk vun de Uiguren in't Rebeet vun Tibet un Noberlannschapen weer de Manichäismus Staatsreligion. Ünner Influss vun'n Zoroastrismus stunnen ok de Bogomilen, ene Grupp mit christlichen Elementen ahn an de Eenheid vun Gott un Jesus Christus to glöven.
4. De meisten Anhängers hett düsse Religion hüdigendags woll in Indien. De Lüüd, vun de vele in Bombay leevt, heten Parsen. Se sünd Marathen, man snackt Gujarati.
5. Ene anner Grupp mit christlichen Elementen ünner den Influss vun'n Zoroastrismus weern de Katharer in Okzitanien un annere Delen vun Europa in't Medeloller. De ehre Nahkamen sünd sunenrlich Bulgaren un de Muslims vun Bosnien-Herzegwonia sünd.

Fragen:
1. Wo hett dat mit den Börgerkrieg in de USA to doon?
2. Wie warrt de Verfaten vun de USA billt?
3. Wo hett dat mit den Tweeten Weltkrieg to doon in de USA?
4. Wie warrt de Butenpolitik vun de USA billt?
5. Wo hett dat mit den Vietnamkrieg to doon in de USA?

Antwoorten:
1. De Börgerkrieg weer en Krieg, de 1860-1865 in de USA losgüng. He weer een Krieg twuschen Noord un Süüd vun de USA över de Slaven.
2. De Verfaten is de oolste demokraatsche Verfaten, de hüüt noch bruukt warrt. Se ward 1787 afleggt un is denn ok de Grundlage för de Politik in de USA.
3. De USA hefft 1941 den Krieg an Japan angrepen un 1945 den Krieg an Düütschland un Italien angrepen. Dat weer een groten Krieg, de de USA mit bi harrn.
4. De Butenpolitik is de Politik, de de USA in’e Welt utöövt. Se ward vun’n Präsidenten maakt un is denn ok de Grundlage för de Beziehungen to annere Länner.
5. De USA hefft 1964-1973 in’n Vietnamkrieg gegen de Kommunisten angrepen. Dat weer een groten Krieg, de de USA mit bi harrn.

Fragen:
1. Wo hett Johann Wolfgang von Goethe leevt un wat hett he dor för Tieten verbröcht?
2. Wie is dat mit den Dichterstil vun Goethe? He weer en Sturm- un Drang-Dichter oder hett he sik laterhen anners utdrücken laten?
3. Wo hett Goethe siene Dichtungen schreven? In Italien, in Weimar oder in Darmstadt?
4. Wie is dat mit den Naturwetenschoppen vun Goethe? 
5. Wo hett Goethe siene Süster Cornelia anstifft, un wat weer dorup för den Dichterstil vun Goethe?
6. Wie is dat mit den Weimarer Theater? He weer Leiter dor un hett dort ok ene junge Frau heiraat.
7. Wo hett Goethe siene Verlobte Lili Schönemann sett, un wat weer dorup för den Dichterstil vun Goethe?
8. Wie is dat mit den ölleren Deel von "Faust"? He weer al in Italien schreven oder hett he sik laterhen anners utdrücken laten?

Antwoorten:
1. Johann Wolfgang von Goethe weer 1749 in Frankfort an’n Main boren un is 1832 doodbleven.
2. He weer en Sturm- un Drang-Dichter, man laterhen hett he sik ok anners utdrücken laten.
3. He hett siene Dichtungen in Italien schreven, as he dor för de Romane "De Wahlverwandtschaften" un "Wilhelm Meisters Lehrjahren" reist hett.
4. He hett sik mit de Farvenlehre un de Morphologie besöcht, wat he in siene Öller tostann brocht hett.
5. Se hett em anstifft, as he noch jung weer.
6. He weer Leiter vun dat Weimarer Theater un hett dort ok ene junge Frau heiraat.
7. Se hett em 1794 sett, as he ut Italien trüchkamen weer.
8. De öllere Deel von "Faust" is al in Italien schreven worrn.

Fragen:
1. Wat hett den Anslag vun’n 20. Juli 1944 mit den Natschonalsozialismus un gegen Adolf Hitler to doon?
2. Wie warrt de Lüde, de an'n Anslag beteelt weern, in't Textbook beschreven? Woneem steken se ut?
3. Wo hett dat mit den Kreisauer Kreis üm Helmuth James Graf von Moltke to doon? Weert he ok in den Textbook vunwegen düssen Upstand nöömt?
4. Wie warrt de Anslag op Hitler beschreven? Woneem is dat upschreven un wat hett dat mit de Bomb to doon?
5. Wat weer de Grundlaag för den Greep na de Macht, wenn ok de Anslag nich an’e Siet bröcht harr?

Antwoorten:
1. De Anslag vun’n 20. Juli 1944 un de Greep na den Staat wiest an’n düütlichsten, dat dat in de Tiet vun den Natschonalsozialismus in Düütschland en Wedderstand gegen den Natschonalsozialismus un gegen de Regeern vun Adolf Hitler geven hett.
2. Achter düssen Anslag steken Lüde ut ganz verscheden Krinken vun dat düütsche Volk, veel vun jem harrn wat mit den Kreisauer Kreis üm Helmuth James Graf von Moltke ümto to kriegen.
3. Wo hett dat mit den Kreisauer Kreis üm Helmuth James Graf von Moltke to doon? Weert he ok in den Textbook vunwegen düssen Upstand nöömt? Ja, de Textbook nöömt den Kreisauer Kreis un Helmuth James Graf von Moltke.
4. Wie warrt de Anslag op Hitler beschreven? Woneem is dat upschreven un wat hett dat mit de Bomb to doon? De Anslag op Hitler weer Grundlaag för den Greep na de Macht, man de Bomb hett em nich an’e Siet bröcht. Dorüm, un ok vunwegen dat dat mit den Anfang vun de „Operatschoon Walküre“ to lange duert hett, is dat nix wurrn mit den Greep na den Staat.
5. Wat weer de Grundlaag för den Greep na de Macht, wenn ok de Anslag nich an’e Siet bröcht harr? De Grundlaag weer, dat de Anslag up Hitler sien Leven slumpen dö. Man de Bomb, de Claus Schenk Graf von Stauffenberg an den Diktater sien Siet afstellt hett, hett em nich an’e Siet bröcht.

Fragen:
1. Wo hett Carl von Linné sien Dagbook över de Reis na Lappland schreven? Dat is dat „Iter Lapponicum“.
2. Wie hett he sik denn mit den Botaniker Jan Frederik Gronovius uttoftaten?
3. Wat weer de Grundlaag vun de Klassifikatschoon, de Linné entwickelt hett?
4. Wo hett he dat Systema Naturae schreven? Dat is in Leiden.

Antwoorten:
1. Carl von Linné hett sien Dagbook över de Reis na Lappland schreven, dat „Iter Lapponicum“, as Student.
2. Dat is nich bekannt, wat he mit den Botaniker Jan Frederik Gronovius uttoftaten is. He hett aver ok en fröheren Botaniker, Johann Rothman, drapen un wies em en fröhen Entwurf vun siene Arbeit över Taxonomie.
3. De Grundlaag vun de Klassifikatschoon, de Linné entwickelt hett, weer dat Blötenkennteken as Grundlaag för dat Indelen vun ’t Plantenriek to bruken.
4. Dat Systema Naturae is in Leiden schreven worrn.

Fragen:
1. Wo hett dat mit dat ARPANET to doon? Wat weer dat för en Projekt un warrn dorbi de Universitäten anboeten?
2. Wie is dat Internet denn billt worrn? Woneem is dat för de elektronsche Kommunikatschoon vörsehn worrn un wat gifft dat denn noch över den Reekners?
3. Wo hett dat mit dat Domain Name System (DNS) to doon? Wat is dat för en System un warrn dorbi de Domains ansluten?
4. Wie is dat World Wide Web denn billt worrn? Woneem is dat för een Hypertext-Projekt vörsehn worrn un wat gifft dat denn noch över den Reekners?
5. Wo hett dat mit de Internet Corporation for Assigned Names and Numbers (ICANN) to doon? Wat is dat för en Organisation un warrn dorbi de Domains ansluten?

Antwoorten:
1. Dat ARPANET weer een Projekt vun de Advanced Research Project Agency (ARPA), för dat Militäär opbaut weern. Dat schull seker ook vör een Atomslag ween, un dorüm harrn se sik överleggt, dat dat dezentral sien schull. Denn kemen de Universitäten an.
2. Dat Internet is för de elektronsche Kommunikatschoon billt worrn. Dat heet, een kann Nettbreven rutschicken un kreegen, Datens schüffeln, Sieden vun dat World Wide Web ankieken, wat daalladen, telefoneern un anners. De Reekner snackt över wisse Protokollen mitnanner, sünnerlich dat TCP/IP-Protokoll.
3. Dat Domain Name System (DNS) is een System, dat de Domains ansluten deit. Dat gifft ok noch ene Form vun den DNS, de as Ümluut un Sünnerteken bruukt weern kann, so as ä, ö, ü.
4. Dat World Wide Web ward in dat Europäisch Kernforschungslabor CERN insett. Tim Berners-Lee hett dat Konzept för een Hypertext-Projekt för de heele Welt schreven. Dat gifft ok noch annere Webserver un Webbrowser, as de eerste düütschen Reekners ansluten weern.
5. De Internet Corporation for Assigned Names and Numbers (ICANN) is een Organisation, de de Domains ansluten deit. Dat gifft ok noch ene Form vun ICANN, de as Registrar för .de-Domains opmookt is. Nu gifft dat ok mol foffteihn Webservers un 3 Millionen Computers, de ansluten sünd.

Fragen:
1. Wo hett Frankriek sien Naam kregen un wat heet dat?
2. Wie warrt de Spraak in Frankriek utdrückt un is se Amtsspraak?
3. Wann is Frankriek Republik un wie kummt dat denn dorhen?
4. Wo hett Frankriek sien Överseegebeden un wat gifft dor noch mehr to seggen?
5. Wie warrt Frankriek in de Tiedsche Geschicht utdrückt un wat heet dat?

Antwoorten:
1. De Naam Frankriek kummt vun den germaanschen Franken, de een Riek in den tovöör gallischen Deel van den daalgaan Röömschen Riek grünnen. „Franken“ kümt weder uut oorgermaansche *frankon, wat Piek oder Speer heet oder na een anner Versöök dat Woord to verklören „friege Männer“ heet.
2. De Amtsspraak is Franzöösch un ok de Spraak, de meest alle in’n Land spreekt. Se is sied 1992 offitschell „la langue la République“ (plattdüütsch Sprake van de Republik). Frankriek is dat franschsprakige Land med den tweedmeesten Sprekers, up den eersten Platz liggt de Demokraatsche Republik Kongo.  In de  Organisation internationale la francophonie (Frankphonie) wakrt Frankriek med franschsprakigen Länner tohope un versöcht datFranzöösche weltwied wedder mehr Belang to geven.
3. Frankriek is Republik un siet 1958 hett Präsident van Frankriek böberste exekutive Gewalt. Wiels de Städen in de Tied daalgüngen breed sik dat Christendoomup·n Lanne uut un Klöster worden gründ. De Merowingers, de Dynastie van Chlodwig I., konn sik bet 751 an de Macht hoolden, as Pepin de Korte Frankenkönig worre un de Karolingers begünnre.
4. Frankriek hett sien Överseegebede up verschedene Kontinente un Ozeane verdeelt. Bet op Franzöösch-Guyana un dat Antarktisgebeed sind alle heel verscheden topgraafsche Kennteken. Bet op den Fastland sett sik uut velen verscheden Landschoppen tohoop, med Plattland för de Buerie oder Woold, Bargkeden, Middelbargen, Küsten un Däler. De Överseegebede wiest ene grote Aardenveefoold, besunners de Woold van Franzöösch Guyana oder de Eilanden van Neekaledonien up de vele endeemsche Aarden leevt.
5. Frankriek is dat wooldriekst Land in Westeuropa; 31 % van den franzööschen Modderland bedeckt Woold. De Woold sett sik to uu 67 % de Loovwoold, 21 % uut Nadelwoold un to 12 % uut Mischwoold tohoop. Fuchtgebede, de maal een Veerdel van dat Land bedecken, sind sied den 19. Jahrhunderd stark torüchgaan.

Fragen:
1. Wo hett Chopin leven? Un wo is he doodbleven?
2. Wie hett Chopin sien Leven anfangen? Woneem hett he anfungen to komponeren un wat hett he denn studert?
3. Wo hett Chopin sik denn na wesen? Wat weer dat för en Tiet, as he sik in Paris opsett hett?
4. Wie is Chopins Musik bekannt worrn? Was he een vun de Grünners vun de klassischen Pianistik un wat hett he mit Franz Liszt to doon?
5. Wo liggt Chopins Hart begraven un wo is he denn gräven worrn?

Antwoorten:
1. Chopin weer in Polen boren, man sien Vader weer franzööschen. He is doodbleven in Paris.
2. Al mit 7 Johren füng he an to komponeren un hett sik denn na’t Konservatorium in Warschau üm Piano to studeren. Later hett he sik toeerst in Wien, later in Paris opsett.
3. He is denn na Paris kamen, woneem he as Komponist un Pianist vun vör all sien egen Arbeid worrn is. He speel veel in Salons. Vun 1838 bet 1839 weer he op Mallorca.
4. Chopin wurr bekannt dör sien virtuose Klavierspeel un sien Salonkonzerte. He un Franz Liszt weern wichtige Figuren in de Entwicklung vun de klassische Pianistik, un Liszt hett Chopins Talent bewunnert.
5. Seine Hart is in Polen begraven worrn, man sien Leven liggt gräven in Paris.

Fragen:
1. Wo hett dat mit den Hinduismus to doon?
2. Wie warrt de Hinduisten nöömt?
3. Wat gifft dat in den Hinduismus för Göddern? Un wie veel gifft dat?
4. Wo hett dat mit den Hinduismus to doon?
5. Wie warrt de Gödder in den Hinduismus utsehn? Un welke Gödder gifft dat denn?

Antwoorten:
1. De Hinduismus is een vun de groten Weltreligionen un de öllste, de an dat Dharma glöövt.
2. Anhängers vun den Hinduismus warrt tomehrst Hindus nöömt.
3. Dat gifft en groot Tall vun Gödder in den Hinduismus. De wichtigsten sünd Brahma, Vishnu un Shiva, de as de Trimurti bekannt sünd.
4. De Hööftgödder in den Hinduismus sünn Schiwa, Wischnu un Brahma.
5. Dat gifft ok keen zentraal Bekenntnis vun den hinduistischen Gloven un keen Grünner vun den Hinduismus (so as t.B. Jesus Christus bi dat Christendom oder Buddha bin den Buddhismus).

Fragen:
1. Wo hett dat mit den Naam "Hillig Röömsch Riek" to doon?
3. Woher kümmt de Naam "Hillig Röömsche Riek"?
4. Wie hett dat Riek sik an’n 6. August 1806 afsetten laten?
5. Wo warrt de Naam "Hillig Röömsche Riek" noch bruukt?

Antwoorten:
1. Dat is nich so as in annere Staaten. De Naam "Hillig Röömsch Riek" is dorüm ok "Olet Riek" nömmt wurrn, dormit en dat nich dör’nanner bringt mit dat Düütsche Riek vun 1871.
3. De Naam maak kloor, dat dat Riek wiedergahn mit de olen Traditschonen vun dat Röömsche Riek ut de Antike weer.
4. Dat Riek is vun den Kaiser Franz II. utgahn. Dor weer de Geschicht vun dat „Hillig Röömsche Riek vun Düütsche Natschoon“ mit to Enn.
5. De Naam "Hillig Röömsche Riek" is noch bruukt, wenn een sik mit de Historie akraat nehmen will. Dat Riek warrt ok as "Olet Riek" nömmt wurrn, dormit en dat nich dör’nanner bringt mit dat Düütsche Riek vun 1871.

Fragen:
1. Wo liggt de Stadt Stralsund in Düütschland?
2. Wie warrt de Stadt Stralsund wichtig för den Verkehr in Mekelnborg-Vörpommern?
3. Wie groot is de Stadt Stralsund un wat is dat Landkreis, in den se tohöört?
4. Wo kann een na Rostock fohren, wenn man ut Stralsund utföhrt?
5. Welche Attrakschonen gifft dat in de Stadt Wismer un Stralsund?

Antwoorten:
1. De Stadt Stralsund liggt in’n Noordoosten vun Düütschland.
2. De Stadt Stralsund is wichtig för den Verkehr in Mekelnborg-Vörpommern, man ok för den Verkehr in den Noorden vun Mekelnborg-Vörpommern.
3. De Stadt Stralsund streckt sik ut öber 38,97 km² un tohöört to’n Landkreis Vörpommern-Rügen.
4. Een kann na Rostock fohrn, wenn man ut Stralsund utföhrt.
5. Dat Zentrum vun Wismer un Stralsund hett de UNESCO 2002 in de „List vun dat Weltarv“ nahmen. De Binnenstadt bargt eenige feine Museen, as to’n Bispeel dat Ozeaneum.

Fragen:
1. Wo hett dat mit de Reformatschoon to doon? De Reformatschoon weer en Bewegung, de toerst de kathoolsche Kark reformeren wull.
2. Wie hebbt sik de wichtigsten Reformaters in de Reformatschoon ümsett? Welke Lüde hebbt an de Reformatschoon mitmaakt?
3. Wo hett Martin Luther den Anfang vun de Reformatschoon maakt? He weer nich de eerste un ok nich de letzte Reformator.
4. Wie hett Ulrich Zwingli de Reformatschoon in de Swiez inföhrt? Was he mit sien Ideen ut de Bibel?
5. Wo hett Johannes Calvin den Anfang vun de Reformatschoon maakt? He weer een Franzoos un is denn laterhen so wat as de Baas vun de Reformeerte Karken in Europa worrn.

Antwoorten:
1. De Reformatschoon weer en Bewegung, de toerst de kathoolsche Kark reformeren wull.
2. Bi de Reformatschoon hett ’n Barg vun Reformaters mitmaakt, to’n Bispeel: Martin Luther, Ulrich Zwingli, Johannes Calvin un Harmen Tast.
3. Martin Luther hett den Anfang vun de Reformatschoon in Düütschland maakt.
4. Ulrich Zwingli hett de Reformatschoon in de Swiez inföhrt. Sien Ideen hebbt he sülben ut de Bibel rutfunnen, man dat weer liek den Ideen vun Luther, de sien Ideen ok ut de Bibel harr.
5. Johannes Calvin hett den Anfang vun de Reformatschoon na Schottland bracht. He weer een Franzoos un is denn laterhen so wat as de Baas vun de Reformeerte Karken in Europa worrn.

Fragen:
1. Wo liggt Australien in’n Eerddeel?
2. Wie groot is dat Land Australien?
3. Welke Städer sünd de gröttsten un bekanntesten in Australien?
4. Wat is Amtsspraak in Australien?
5. Wann is Natschonalfierdag in Australien?

Antwoorten:
1. Australien liggt op den Eerddeel, de ok den Naam Australien hett.
2. De Fläck vun’t Land is 7,686,850 km².
3. De gröttsten un bekanntesten Städer sünd Sydney (4 Mio. Inwahners), Melbourne (3,4 Mio. Inwahners), Brisbane (1,4 Mio. Inwahners), Perth (1,2 Mio. Inwahners) un Adelaide (1,1 Mio. Inwahners).
4. De Amtsspraak is Engelsch.
5. Natschonalfierdag is de 26. Januar.


Fragen:
1. Wo is Ioonsch utkamen?
2. Woneem warrt dat Ioonsche snackt wurrn?
3. Wie is dat Ioonsche mit annere ooltgreeksche Dialekten in Verbindung stahn?
4. Welke Schriever weern in den ioonschen Dialekt bekannt?
5. Wo hett Homer sien Kunstspraak mit dat Ioonsche tohopenleggt?

Antwoorten:
1. Ioonsch is vun den Stamm vun de Ioniers snackt wurrn.
2. De Kuntreien, wo düsse Dialekt in snackt wurrn is, weern de Westküst vun Lüttasien, de Inseln in de Ägäis, Euböa un de ioonschen Kolonien an de Swarte See un in Süüditalien.
3. Dat Ioonsche steiht dicht bi dat Attisch. Binnen de ooltgreekschen Dialekten is dat Ioonsche dorbi nich so wiet weg vun as annere Dialekten, as dat ut den Äoolschen Dialekt.
4. De wichtigsten Schriever in den ioonschen Dialekt weern Herodot un Hippokrates.
5. Homer hett sien Kunstspraak mit dat Ioonsche tohopenleggt. Dat is nich ganz klarr, woans he dat daan hett, man dat gifft en öllerhaftige Form vun dat Ioonsche in sien Kunstspraak.

Fragen:
1. Wat sünd de Natuurwetenschoppen?
2. Wie is de Grunnlag för de Natuurwetenschoppen?
3. Welke Wetenschoppen sünd to'n Deel vun de Eerdwetenschoppen?
4. Woneem warrt dat Experiment un dat Nakieken in de Natuurwetenschoppen bruukt?
5. Wat mutt nakeken warrn, wenn een en nee Chemikalie isoleert oder maakt hett?

Antwoorten:
1. Een Natuurwetenschop is een Wetenschop vun de Natuur.
2. De Grunnlag för de Natuurwetenschoppen is dat Experiment un dat Nakieken.
3. De Eerdwetenschoppen sünd to'n Deel vun de Natuurwetenschoppen, wat to'n Deel de annern Wetenschoppen verbinnt un een Överbegreep is för een ganze Reeg von iengelt Rebeeten.
4. Dat Experiment un dat Nakieken warrt in de Natuurwetenschoppen bruukt, um de Egenschoppen vun en nee Chemikalie to rutfinnen.
5. Wenn een en nee Chemikalie isoleert oder maakt hett, denn mutt nakeken warrn, wat för Egenschoppen de hett, as Smeltpunkt, Kaakpunkt, elektrisch Strom leed un anners.

Fragen:
1. Wo is Apoll in de greeksche Mythologie upkamen un wat hett he denn tostännig wesen?
2. Wie hett Apollo den Python doot maakt un wat weer dat för en Fiend, den he bi den Barg Parnass doodslahn hett?
3. Wat is mit Apoll in sien Leven passert, as he bi den Barg Parnass den Python doot maakt? Wo is he denn nahm un worüm?
4. Wie hett Apollo dat dor up ankamen laten un is opsternaatsch wurrn gegen sienen egen Vadder Zeus? Wat hett he denn torüch betahlen müssen?
5. Welke Froonslüde, mit de Apoll wat harrt hett un Kinner hett he ok tüügt?

Antwoorten:
1. Apoll is in de greeksche Mythologie as Söhn vun den Göddervadder Zeus un Leto opkamen un he weer een vun de twolf Olympiers.
2. Apollo hett den Python doot maakt, as he bi den Barg Parnass doodslahn hett. Dat weer een Fiend vun sien Mudder Leto.
3. As Apoll den Python so swaar tosett hett, is he utneiht nah dat Orakel vun de Mudder Eer in Delphi un möss sik dor in een besunnere Prozedur rein maken vun dat, wat he daan harr.
4. Apollo hett dat torüch betahlen müssen, as he bi den Barg Parnass den Python doot maakt hett. He hett denn nah Tarrha up de Insel Kreta un möss sik dor in een besunnere Prozedur rein maken vun dat, wat he daan harr.
5. Mit Froonslüde un Mannslüde hett Apoll wat harrt un Kinner hett he ok tüügt: Akantha, Amphissos, Anios, Aristaios, Arsinoe, Asklepios, Chione, Daphne, Dryope, Hekuba, Hyakinthos, Kalliope, Kassandra, Kinyras, Koronis, Kyknos, Kyparissos, Leukothea, Linos, Manto, Mopsos, Orpheus, Phemonoe, Philammon, Polyxena, Psamathe, Rhoeo un Terpsichore.

Fragen:
1. Wo hett dat mit den Artikel in't Sünnsystem to doon?
2. Wie warrt de Sünn mit de Planeten in Verbindung bracht?
3. Wo hett dat mit den Asteroiden to doon?
4. Wie warrt en Kometen utbillt?
5. Wo hett dat mit den Kuipergördel to doon?

Antwoorten:
1. De Sünn is in de Mitt vun dat Sünnsystem un treckt vunwegen de Gravitatschoonknööv (oder ok Swoorkraft naamt ward), de Planeten an, de sik üm ehr dreit.
2. De Sünn is de meste Masse un treckt de Planeten an, de sik üm ehr dreit.
3. De Asteroiden sünd lüttere Maanden vun de Planeten un finnt sik twüschen den Mars un den Jupiter.
4. Wenn en Kometen dicht an de Sünn rankaamt, smült dat Ies un verdampt, so dat en Kometen denn een Steert utbült.
5. De Wetenschoppers glövt, dat een Deel vun de Asteroiden dorher kummt, wenn een von de Planeten dicht bi kummt un mit sien Gravitatschoonknööv trekkt. Man hett al welke grote Kuiper-Gürtel-Asteroiden funnen.

Fragen:
1. Wat is de Begreep "Eerdwetenschoppen" un wat hett he mit de Wetenschoppen to doon?
2. Welke Rebeden höört to de Eerdwetenschoppen, wenn een dat nich so genau weet?
3. Wo hett de Begreep "Eerdwetenschoppen" anfangen? Kannst du seggen, wannehr he utkamen is?
4. Wat sünd de Opgaven vun de Eerdwetenschoppen? Gifft dat mehr as een Saken?
5. Woans hett de Eer mit allns Leven dorop entstahn un sik entwickelt hett, wat warrt dor to'n Bispeel ünnersökt?

Antwoorten:
1. De Eerdwetenschoppen vereent all Wetenschoppen, de sik mit den Opbo, Tohopensetten, Gestalt und de Aflööp op un binnen de Eer mitsams ehr Atmosphäär befaten doot.
2. Welche Rebeden höört to de Eerdwetenschoppen, wenn een dat nich so genau weet? Dat sünd ünner annern de Geologie, Geographie, Eerdphysik, Mineralogie, Glaziologie, Meteorologie, Petrographie, Paläontologie, Geodäsie un vele annere.
3. Wo hett de Begreep "Eerdwetenschoppen" anfangen? Kannst du seggen, wannehr he utkamen is? De Eerdwetenschoppen sünd en junge Wetenschop.
4. Wat sünd de Opgaven vun de Eerdwetenschoppen? Gifft dat mehr as een Saken? Ja, dat gifft ok. Dat Söken von Rohstoffen, dat Begriepen von Gefohren (t.B. Eerdbeven, Storm, Överflooten, Vulkanen), dat Ünnersöken von flachen Ünnergrund op Bofastigkeit, Ümweltgefohren (t.B. wenn Grundwater dör Schuttkuhlen verdreckt warrt oder Klimaännern) un eenfach de Grundlagen von dat Tosamenhangen und dat Funkschoneren von de enkelten Aflööp to sammeln un to verstahn, so as de Platentektonik oder woneem dat Eerdmagnetfeld herkummt.
5. Woans hett de Eer mit allns Leven dorop entstahn un sik entwickelt hett, wat warrt dor to'n Bispeel ünnersökt? Dat warrt torüchtoverfolgen un Sporen to söken, woans de Eer mit allns Leven dorop entstahn is un sik entwickelt hett.

Fragen:
1. Wat is de Begreep "Eerdphysik" un wat bedüden dat?
2. Wo warrt Eerdphysik ünnerdeelt? Gifft dat ok annere Rebeeten, as Marine Eerdphysik oder Planetologie?
3. Wie warrt de Eer in Eerdphysik ünnersocht? Gifft dat ok Methoden, de op'n Schipp maken deit?
4. Wat is de Differenz twuschen Anwendte Eerdphysik un Allgemeene Eerdphysik?
5. Wo warrt de Eer ünnersocht, wenn een sik mit Seismologie afrieten deit? Gifft dat ok Methoden, de op'n Schipp maken deit?

Antwoorten:
1. De Begreep "Eerdphysik" bedüden, wat wi över physikalsche Tosamenhäng un Modellen von de Eer weten mutt.
2. Ja, dat gifft ok annere Rebeeten, as Marine Eerdphysik oder Planetologie. Eerdmagnetik, Magnetotellurik, Eerdelektrik, Eerdradar un Seismologie sünd ok ünnerdeelt Wies vun de Eerdphysik.
3. Ja, dat gifft Methoden, de op'n Schipp maken deit. So warrt Gravimetrie ünnersocht, wat de Swoorkraft oder ok Gravitatschoon is.
4. De Differenz twuschen Anwendte Eerdphysik un Allgemeene Eerdphysik is, dat Anwendte Eerdphysik sik mit ganz bestimmte Probleme afrieten deit un disse denn ünnersöken doot, während Allgemeene Eerdphysik sik mit allens tosamenlöpt, wat wi över de Eer weten kann.
5. Wenn een sik mit Seismologie afrieten deit, warrt de Eer ünnersocht, wenn een sik mit Seismologie afrieten deit. Dormit warrt dat lieke, aber nütt natürlich Bülgenborns, de Eerdbeven, un künnt dormit veel deeper in de Eer kieken.

Fragen:
1. Wo is Python utklemmert worrn?

Antwoorten:
1. En Besünnerheid vun Python is, dat de Programmstruktur dör dat Inrücken vun de Regen billt warrt.

Fragen:
1. Wo hett dat mit de Eer to doon?
2. Wie warrt de Eer kiekt? 
3. Wo hett dat mit den Maand to doon?
4. Wie warrt de Eer dreven?
5. Wo hett dat mit den Globus to doon?

Antwoorten:
1. De Eer is de Planet, op den wi all leven un de drütte in uns Sünnsystem is.
2. Dat heet, dat de Wetenschoppers na de Steen kiekt und wo dick de Eerdkrust is un woneem de Eer in ehrn Innern opboot is.
3. Wi hebbt bloot den enen Maand, de jümmers üm de Eer lööpt.
4. De Eer dreiht sik ok sülven un duert slankweg een Johr.
5. Dat is denn en Modell vun de Eer, op den wi kieken köpen un kieken woneem de Länner un de See sünd un wo se heten.

Fragen:
1. Wat is de Quantenmechanik un wat bedüden se?
2. Wo hett dat mit de Interpretatschoon vun de Quantenmechanik to doon? Gifft dat ene, de allgemeene Interpretatschoon oder gifft dat mehrere?
3. Wie warrt de Quantenmechanik bruukt un in welke Fäll is se wichtig?
4. Wo hett dat mit den Begriff "Realismus" to doon? Gifft dat ene, de allgemeene Interpretatschoon vun Realismus oder gifft dat mehrere?
5. Wie warrt de Quantenmechanik in't Leven un in de Technik anwennt?

Antwoorten:
1. De Quantenmechanik is ene physikaalsche Theorie, de Egenschopen un Gesette för de Tostänne un Vörgänge van Materie beschrivt.
2. Dat gifft mehrere Interpretatschonen vun de Quantenmechanik, as de Realistische Interpretatschoon, de Kopenhagener Interpretatschoon, de Many-Worlds-Interpretatschoon usw.
3. De Quantenmechanik warrt bruukt in de Atomphysik, Faststoffphysik, Kärn- un Elementaardeelkenphysik un ok in de Quanteninformatik.
4. Realismus is ene Interpretatschoon vun de Quantenmechanik, de besagt, dat de Quantenmechanik en realen, physikaalschen Prozess beschreven deit un nich bloß een Modell för de Wirklichkeit is.
5. De Quantenmechanik warrt in't Leven un in de Technik anwennt in de Form vun Transistoren, Diodes usw., de in de Elektronik bruukt warrt.

Fragen:
1. Wo hett Isaac Newton de Gravitatschoon opfunnen?
2. Wat sorgt de Gravitatschoon för, wenn se nich in'n Satz steiht? Kanns se dorüm ok Swoorkraft naamen?
3. Wie hangt de Gravitatschoon von de Materie af?
4. Wo kummt dat, dat de Eer sik üm de Sünn dreiht un de Maand üm de Eer?
5. Wat is de Grund för de Tiden (Ebb un Floot)?

Antwoorten:
1. De Gravitatschoon weer Isaac Newton opfunnen.
2. Se sorgt dorför, dat Saken swoor sünd. Kanns se dorüm ok Swoorkraft naamen.
3. De Gravitatschoon is en Egenschap vun de Materie un hangt direkt vun de Masse af.
4. So kummt ok de Tiden (Ebb un Floot) dör de Swoorkraft tostann.
5. Dat sorgt aver ok dorför, dat di en Appel vun baben op den Kopp fallt un nich vun ünnen.

Fragen:
1. Wo hett Monty Python anfangen?
2. Wie veel Folgen vun de Serie Monty Python’s Flying Circus hebbt se för de BBC maakt?
3. Woneem is de eerste Kinofilm vun Monty Python utreken?
4. Wo hett de Grupp noch mehr Filmen drehen?
5. Woneem is de Book/Biografie vun Monty Python utreken?

Antwoorten:
1. De Grupp weer in Oxford un Cambridge studeert un weren al vörher as Komiker aktiv.
2. Se möken för de BBC 45 Folgen (3 Staffeln to 13, ene Staffel to söss Folgen) vun de Serie Monty Python’s Flying Circus.
3. De eerste Kinofilm vun Monty Python is in Schottland dreht worrn un hett den tweten Kinofilm Monty Python and the Holy Grail geven.
4. Se möken noch en poor mehr Filmen, Life of Brian is för sienen typischen britischen Monty-Python-Humor beröhmt.
5. De Book/Biografie vun Monty Python is in 2003 utreken worrn.

Fragen:
1. Wat is Energie in't Plattdüütsche? Wo hett dat mit Energie to doon?
2. Wie warrt Energie in den Appel an den Boom utbillt un wat gifft dorbi Kinnekinetische Energie?
3. Woneem gifft dat verschedene Oorten vun Energie, as potentschelle Energie, kinetisch Energie, elektrisch Energie, Wärmeenergie? Wo kanns een vun de Energieoorten ümwanneln?
4. Wie warrt in den Dampmaschin Energie utbillt un wat gifft dorbi Kinnekinetische Energie?
5. Wat hett Albert Einstein rutfunnen, dat Masse un Energie tosomenhangt? Wo is de Formel för dat?

Antwoorten:
1. De Energie is dat wat wat bewerkt. Un wenn een Appel an den Boom fallt, denn ward de Energie frie.
2. De Appel hett kinetisch Energie, wenn he di op den Kopp fallt. Dor gifft dat verschedene Oorten vun Energie: potentschelle Energie (de Appel hett dorbi veel Energie), kinetische Energie (de Appel hett kinetisch Energie, wenn he di op den Kopp fallt) un elektrisch Energie (wenn de Appel in een Dynamo andriffs).
3. Dat gifft verschedene Oorten vun Energie: potentschelle Energie, kinetische Energie, elektrisch Energie, Wärmeenergie.
4. In den Dampmaschin ward Water hitt mookt un denn to Damp. Mit bannig veel Druck. Un de Damp kümmt denn in den Zylinder. Dor kann he sick utbreiden. Denn ward de Kolben wegdreewen. Nu hess kinetische Energie.
5. Dat Masse un Energie tosomenhangt, wat dat meent? De Formel is: E = M · c2.

Fragen:
1. Wat is Nedderslag in de Meteorologie? Wo kummt dat vun?
2. Wie warrt Nedderslag tostanne kamen?
3. Welke Aarden vun Nedderslag gifft dat? Gifft dat natten un drögen Nedderslag?
4. Wat bedüden de Begriffen "natten" un "drögen" Nedderslag? Wie warrt Nedderslag to'n Bispeel as naten oder drögen Nedderslag bekeken?
5. Wo hett dat mit den Waterkreisloop to doon, wenn Nedderslag op de Eer fallen deit? Gifft dat en sunnerlich Kennteken för all Regionen up'e Eer?

Antwoorten:
1. Nedderslag is Water, mit allens, wat dor an annere Stoffe in sitten deit, nömmt, wenn dat ut Wulken, Daak oder Smook stammen deit oder ut hoge Luftfuchtigkeit (Luft, de vullsitten deit mit Waterdamp) kummt.
2. Nedderslag kummt dör Verdampen un Sublimatschoon tostanne. Dör Kondensatschoon vun de Fuchtigkeit in de Luft kaamt Kondensatschoonskieme tostanne, dor warrt denn Wulken ut. Wenn de Waterdruppen as Nedderslag op de Eer fallen könnt, mütt se groot un swaar noog ween.
3. Ja, dat gifft natten un drögen Nedderslag. Natten Nedderslag is Regen, Iesregen, Druppen fallt hendal. Drögen Nedderslag is Snee, Hagel, Ieskoorn fallt hendal.
4. "Naten" bedüden dat, wenn Nedderslag as Regen oder Iesregen op de Eer fallen deit. "Drögen" bedüden dat, wenn Nedderslag as Sneestorm oder Sneebarge op de Eer fallen deit.
5. Wenn Nedderslag op de Eer fallen deit, kummt en Waterkreisloop tostanne. Dor is een sunnerlich Kennteken för all Regionen up'e Eer.

Fragen:
1. Wat is de Bedüden vun den Begriff "reformeerte Kark"?
2. Wie warrt de reformeerte Karken in Dütschland ünnerdeelt? Gifft dat ene Synode oder gifft dat mehrere Freekarken?
3. Welke Unnerscheden gifft dat twüschen Luthersche un Reformeerte Karken? Woans sünd se ünnerscheedlich?
4. Wie warrt de reformeerte Kark in Dütschland mit de luthersche Kark ünnerhollen? Gifft dat ene Gemeenskupp oder gifft dat annere Vördelen?
5. Woans warrt de reformeerte Kark in de Nedderlannen ünnerscheedlich? Gifft dat mehrere reformeerte Karken oder gifft dat een grote reformeerte Kark?

Antwoorten:
1. De reformeerte Kark is en tosammenfatend Utdruck för de protestansch Karken, de op dat Warken un Lehren van Johannes Calvin un Ulrich Zwingli in de Swiez torügg gahn.
2. In Dütschland gifft dat de "Evangeelsch-reformeerte Kark – Synode van de reformeerte Karken in Bayern un Noordwest-Düütschland" un welke Freekarken, as de Altreformierte Kirche un de Bund evangelisch-reformierter Kirchen in der Bundesrepublik Deutschland.
3. De Unnerscheden twüschen Luthersche un Reformeerte Karken sünd, dat de reformeerten de Upfaten hebbt, dat dat hilig Abendmahl blot en symboolsche Hanneln is un dat gifft de Prädestinatschoonslehr. De seggt ut, dat all Minschen vör dat Leven al vun Gott ten Hil oder Daud bestimmt sünd.
4. In Dütschland warrt de reformeerte Kark mit de luthersche Kark ünnerhollen, man dor gifft keen ene Gemeenskupp. De meist Lutherschen Christen in en Oort, wo dat blot en refoormeerte Gemeente gift, höört daarto.
5. In de Nedderlannen sünd de meesten protestansch Christen reformeert. Vördem sük dree protestansch Karken tosammensluten hebben, wassen de beid Gröttsten reformeerte Karken.

Fragen:
1. Wo hett dat mit den Artikel in't Plattdüütsche to doon? 
2. Wie warrt de Konjugatschoon von Verben in't Plattdüütsche billt? De Verben warrt konjugeert, wat dat meent?
3. Wo hett dat mit den Tied bi Verben to doon? Gifft dat Präsens, Präteritum, Perfekt un Plusquamperfekt, oder gifft dat noch annere Tieden?
4. Wie warrt de Hülpsverben in't Plattdüütsche bruukt? 
5. Wo hett dat mit den Mehrtall to doon in't Plattdüütsche

Antwoorten:
1. De Artikel sünd nich so as in't Hoochdüütsche, man dor gifft ok Resten vun den Genitiv un ok een Form ahne jede Endung.
2. Konjugeren heet, dat sik de Verbform ännert, je na Person (ik, du, he/se/dat, wi, ji, se) un Tiet (Präsens, Präteritum, Perfekt usw.). T.B.: ik maak, du maakst, he maakt, wi maakt, se maakt.
3. Ja, dat gifft dat. De Präsens is för dat, wat nu is. Dat Präteritum is för dat, wat weer (verleden Tiet). Dat Perfekt is för dat, wat jüst vörbi is un dat Plusquamperfekt is för dat, wat all lang vörbi is.
4. De Hülpsverben sünd: sien/wesen, hebben, wullen, schallen (sallen), doon, warrn, könen, mögen, möten, dörven.
5. De Mehrtall köönt de plattdüütschen Wöör op verschedene Wies billen, un faken is de Mehrtall denn anners as in dat Hoochdüütsche. Bi de Mehrtaal gifft dat mehr or minner een Schema. De Enn is jümmer -en bi swacken un starken Egenschapswöör.

Fragen:
1. Wo hett dat mit de Baas vun de Katholiken to doon?
2. Wie warrt de Struktuur vun de kathoolsche Kark beschreven?
3. Wo hett dat mit de Liddmaten in Düütschland to doon?
4. Wie warrt de kathoolsche Kark in Düütschland verleert?
5. Wo hett dat mit de Amtschefin vun de kathoolsche Kark to doon?

Antwoorten:
1. De Paapst is de böverste Autorität, wenn dat um de kathoolsche Lehr geiht. Katholiken glöövt, dat dat ahn den Paapst nich geiht.
2. De Struktuur vun de kathoolsche Kark is hierarchisch. Dat heet, dat dat en Reeg vun Autoritäten gifft, von'n höögsten (den Paapst) bit na'n lüttensten. Annere Karken sünd tomehrst demokraatsch verfaat.
3. In 2003 weern dor 26,16 Millionen Katholiken un dat sünd 31,7 Perzent vun den Düütschen. Meist 4 Millionen gaht Sünndags na de Kark.
4. De kathoolsche Kark verleert elk Johr 100.000 Liddmaten.
5. Dat gifft nich in'n Text en Minsch, de as Amtschefin vun de kathoolsche Kark optritt. De Text beschrifft bloß den Paapst as den Baas vun de Katholiken.

Fragen:
1. Wo hett sik de Sikhismus utbillt? 
2. Wie is de Reeg vun de Gurus in den Sikhismus?
3. Wo hett de Sikhismus sien Schrift utbillt?
4. Wie veel Anhängers hett de Sikhismus?
5. Woher kümmt de Sikhismus her?

Antwoorten:
1. De spirituellen Lehren sünd von Guru Nanak to Grundlage.
2. De Reeg vun de Gurus is so: de negen Gurus nafolgen, un den elften un letzen ewigen Guru hett de teggende Guru, Gobind Singh, as den Gurumukhi-Schrift utbillt.
3. De Gurumukhi-Schrift is de Schrift, in de de Sikh-Schriften schreven warrt.
4. Mit so wat bi 25–30 Millionen Anhängers is dat een vun de grötsten religiösen Gruppen in de Welt.
5. De Sikhismus is in de indsche Panjab-Regioon gegen Enn van dat 15. Johrhunnert opkamen.

Fragen:
1. Wo hett dat mit Latien to doon? Wat is Latien un woneem is se utkamen?
2. Wie warrt Latien syntetisch billt? Gifft dat bi Latien veel Vokativs oder ok en Ablativ?
3. Wann is Latien in de Tieden vun't Römsche Riek bruukt worrn? Wo hett se denn utbreedt?
4. Wie warrt Latien later as Spraak vun de Kark un Wetenschap bruukt worrn? Gifft dat ok Urkunnen op latiensch in de Hansetiet?
5. Woneem sünd latiensche Wöör in dat plattdüütsche kamen? To'n Bispeel, woneem is de Keuk oder de Persepter utkamen?

Antwoorten:
1. Latien is de Spraak vun de olen Römers un is ene syntetische Taal, dat betekent, dat bi naal de grammatisken Formen düür Voorsettels (Präfix) oder Anvugels (Suffix) an de Stam van de Woorden gebeld werdt.
2. Latien hett bi de Hoofdwoorden ses Naamfallen un bi de Doewoorden jüstsou aol 6 Tieden, man se worren bijna aolle sonder Hülpsdoewoorden bebeldt.
3. In de ole Tied weer Latiensch de Spraak vun de Lü ut de italiensche Landschap Latium, wo Rom in liggen deit. Mit dat Utbreeden vun dat Römsche Riek breed sik ok de Spraak ut, bit na Britannien un Germanien.
4. Na dat Enn vun dat Römsche Riek bleev Latiensch de Spraak vun de Kark un vun de Wetenschap. Wokeen op sik höll, de harr in't Medeloller latiensch snackt. Bet so 1300 weern ok in dat plattdüütsche Spraakrebeet de opschreeven Saaken op latiensch.
5. Ut ganz verscheeden Tieden sünd denn ok latiensche Wöör in dat plattdüütsche kamen, to'n Bispeel de Keuk oder de Persepter.

Fragen:
1. Wat is de Bedüden vun den Titel "Paapst" un wo kummt he vun?
2. Wie warrt de Paapst in de kathoolsche Kark sehn? Un wat is de Historie achter disse Sehn?
3. Wo hett dat mit'n Bischop vun Rom to doon? Wat is denn de Bedüden vun den Titel "Bischop vun Rom" un wo kummt he vun?
4. Wie warrt de Paapst in de Vatikaanstadt sehn? Un wat is denn de Bedüden vun den Titel "höögste Staatsmann in de Vatikaanstadt"?
5. Wat is de aktuelle Paapst un wo kummt he vun?

Antwoorten:
1. De Titel "Paapst" kummt ut ooldgreeksch "πάππας páppas", wat so veel as "Vadder" bedüden deit.
2. De Paapst warrt in de kathoolsche Kark as Nofölger vun’n Apostel Petrus sehn, wat he ok de höögste Staatsmann in de Weltkark is.
3. De Bischop vun Rom is de Hööftbischop vun de Röömsch-kathoolsche Kark un de Nofölger vun'n Apostel Petrus. Dat gifft en lange Historie achter disse Sehn, wat in den Text nich besproken warrt.
4. De Paapst is ok de höögste Staatsmann in de Vatikaanstadt. He hett de Titel "Böverpreester" un is ok de Hööftbischop vun Italien.
5. De aktuelle Paapst is Franziskus I, wat he ok de 266. Paus is.

Fragen:
1. Wo liggt de Swiez un wat gifft dat dor in?
2. Wie veel Inwahners leven in de Swiez un wat is de Rebeet vun dat Land?
3. Welke Spraken sünd Amtsspraken in de Swiez un welke Spraak warrt utnahmen?
4. Wo liggt de Rhien in de Swiez un wat gifft dat dor in?
5. Wie is de Staat in de Swiez organiseert un welche Kantone besteiht dat Land ut?

Antwoorten:
1. De Swiez liggt in Europa in de Alpen un Navers sünd Öösterriek, Liechtensteen, Düütschland, Italien un Frankriek.
2. Inwahners leven 8.544.527 up en Rebeet vun 41.285 km².
3. Amtsspraken sünd Hoochdüütsch, Franzöösch, Italieensch un Rätoromaansch. Umgangsspraak sünd verschedene Dialekte vun dat Swiezerdüütsch un dat Frankoprovenzaals.
4. De Rhien is een stroom in de Swiez. Dat gifft dor ok noch veel annere Stroomen, as den Aare, den Limmat, den Bregenstocksee un den Thunersee.
5. De Verfaten is demokraatsch. De Swiezer sünd nich inne Europääsche Union mit binnen. De Swiez besteiht ut 26 Kantone.

Fragen:
1. Wo liggt de Stadt Rom un wat is dorbi to bedüden?
2. Wie hett de Stadt Rom bi 1999 veel Inwahners? Un woneem liggt dat?
3. Wat is de Vatikan un wo hett he sien Siet in Rom?
4. Woneem is de Paapst Seet vun de röömsch-kathoolsche Kark?
5. Wo is de Malteser Ritterorden Seet vun? Un wat is dat för en Staat?

Antwoorten:
1. De Stadt liggt an’n Tiber un hett bi 2,6 Mio. Inwohners (1999). Binnen de Stadt liggt de Vatikan, dat een eegen lüttschen Staat (Vatikanstaat) is.
2. Bi 1999 hett de Stadt Rom bi 2,6 Mio. Inwahners. Dat gifft nich mehr ene klare Antwoort op de Frage, woans dat kummt, man dat warrt in de Text as "1999" schreven un dor is denn ok een Zahlenangabe för.
3. De Vatikan is de Seet vun’n Paapst, de ook Bischop vun Rom un Overhaupt vun de röömsch-kathoolsche Kark is. Denn is Rom ook Seet vun de Malteser Ritterorden, dat een eegenständig Völkerrechtssubjekt is.
4. De Paapst is Seet vun de röömsch-kathoolsche Kark in Rom.
5. Dat gifft nich mehr ene klare Antwoort op de Frage, woans dat kummt, man dat warrt in de Text as "Malteser Ritterorden" schreven un dor is denn ok een Zahlenangabe för, dat dat een eegenständig Völkerrechtssubjekt is.

Fragen:
1. Wo hett dat mit den Artikel in't Ooldsassische to doon?
2. Wie warrt de Konjugatschoon von Verben in't Ooldsassische billt? De Verben warrt konjugeert, wat dat meent?
3. Wo hett dat mit den Tied bi Verben to doon? Gifft dat Präsens, Präteritum, Perfekt un Plusquamperfekt, oder gifft dat noch annere Tieden?
4. Wie warrt de Hülpsverben in't Ooldsassische bruukt? 
5. Wo hett dat mit den Mehrtall to doon in't Ooldsassische?

Antwoorten:
1. De Artikel sünd nich so as in't Hoochdüütsche, man dor gifft ok Resten vun den Genitiv un ok een Form ahne jede Endung.
2. Dat heet, dat se sik ännert. Wenn ik wat do heet dat anners ans wenn du dat deist oder se dat doot oder gor wenn ik wat doon harr. Dat heet, dat kümmt dorop an, welk Person dat is, wat dat Eentall oder Mehrtall is un vör allens, wat för en Tiet dat is.
3. Ja, dat gifft dat. De Präsens is för dat, wat nu is. Dat Präteritum is för dat, wat weer (verleden Tiet). Dat Perfekt is för dat, wat jüst vörbi is un dat Plusquamperfekt is för dat, wat all lang vörbi is.
4. De Hülpsverben sünd: sien/wesen, hebben, wullen, schallen (sallen), doon, warrn, könen, mögen, möten, dörven. De Hülpsverben hebbt t.B. mit de Tied to doon.
5. De Mehrtall köönt de plattdüütschen Wöör op verschedene Wies billen, un faken is de Mehrtall denn anners as in dat Hoochdüütsche. Bi de Mehrtaal gifft dat mehr or minner een Schema. De Enn is jümmer -en bi swacken un starken Egenschapswöör.

Fragen:
1. Wat is de Bedüden vun dat Woort "Weertschop"?
2. Wie warrt de Weertschop in'n Text ünnerscheedelt? Gifft dat den Primärsektor, den Sekundärsektor un den Tertiärsektor?
3. Wann is Geld opkamen? Un wat hett dat mit Geld to doon?
4. Wie warrt de Bargbau in den Text beschreven? Un wannehr is he opkamen?
5. Wo hett dat mit de Industrie to doon? Un wannehr is se opkamen?

Antwoorten:
1. Weertschop is en tosaamfaten Woort för allens wat mit Produkschoon un Hannel un Deenst to doon hett.
2. Ja, dat gifft den Primärsektor (de Bueree, de Bargbau), den Sekundärsektor (Handwark, Industrie) un den Tertiärsektor (Hannel, Geldweertschop, Deenstmaker).
3. Geld keem denn wat üm 1000 v. Chr. op. Un dat Geld utleihn.
4. Den Bargbau is in den Text as en Sektion ünnerscheedelt, de in't 17. Johrhunnert Opschwung hett un later in dat 18. Johrhunnert güng.
5. Woorn is de Industrie opkamen. Dat is nich in'n Text to lesen, man dat gifft dor in den Text een Sektion för "Industrie". De Bargbau is al vörher opkamen, as de Minschen Scheep boot harrn un dat Geld utleihn weer.

Fragen:
1. Wat is en Programmeerspraak?
2. Wie warrt en Programmeerspraak dör dat Programmieren utdrückt? Gifft dat en Reeg vun Orders oder funkschonale oder logische Programmeerparadigmen?
3. Wo hett dat mit de Syntax un Semantik to doon in en Programmeerspraak? De Definitschoon sett sik tosamen ut, wat för?
4. Wie warrt en Programmeerspraak beschreven? Gifft dat Spezifikatschoonsdokumente oder Implementatschonen?
5. Wo hett dat mit den Bispill C to doon? Is dat dör en ISO-Standard fastleggt un bruukt as Referenz?

Antwoorten:
1. En Programmeerspraak is en formaal Spraak, de dorför dacht is, mit en Maschien (mehrst en Computer) to snacken.
2. De Code is en Reeg vun Orders, de en na de anner afarbeidt warrt, oder funkschonale oder logische Programmeerparadigmen ünnerstütt.
3. De Definitschoon vun en Programmeerspraak sett sik tosamen ut de Syntax (Form) un de Semantik (Bedüden).
4. Welche Spraken sünd dör en Spezifikatschoonsdokument beschreven, un annere Spraken hebbt en Implementatschoon, de mehrst överall insett warrt un de denn as Referenz bruukt warrt.
5. Dat Bispill C is dör en ISO-Standard fastleggt un bruukt as Referenz.

Fragen:
1. Wat bedütt dat Woort "Heiden" in't Plattdüütsche?
2. Wie is dat Woort "Heiden" översett ut de hebreesche Spraak vun dat Ole Testament?
3. Woneem heet dat Woort "ethnoi" in dat greeksche Nee Testament?
4. Wat bedütt, wenn en Lüe to'n Bund mit Gott tohören doot un wat nich?
5. Wie seht de Karkenvaders an den Begriff "Heiden"?

Antwoorten:
1. Dat Woord "Heiden" bedütt in't Plattdüütsche een Volk, dat nich to Gott sien neet Volk, de Christen, tohören doot.
2. Dat Woort "Gojim" is översett ut de hebreesche Spraak vun dat Ole Testament un bedüüd "Völker".
3. In dat greeksche Nee Testament heet dat Woort "ethnoi" just eben "Völker".
4. Wenn en Lüe to'n Bund mit Gott tohören doot, bedüüdt dat, dat se to de Kark tohören doot un wenn dat nich so is, denn sünd se Heiden.
5. De Karkenvaders seht den Begriff "Heiden" as een Volk an, dat nich to Gott sien neet Volk, de Christen, tohören doot.

Fragen:
1. Wo liggt Jerusalem un wat is dor ok för en Bedüden?
2. Wie hett Jerusalem sien Naam kregen un wannehr is dat to'n eersten Mol nömmt wurrn?
3. Wat gifft dat in de Ooldstadt vun Jerusalem? Un wie is se opdeelt?
4. Wo umstreden is, wat mit Jerusalem as Hööftstadt vun Israel steiht?
5. Woneem liggt Jerusalem un wat is dor ok för en Bedüden?

Antwoorten:
1. Jerusalem liggt in de Bargen vun Judäa un dat is de Hööftstadt vun den Staat Israel.
2. De Stadt is üm 1800 v. Chr. to'n eersten Mol nömmt wurrn un is en vun de öllsten bekannten Städer vun de Welt.
3. De Ooldstadt vun Jerusalem is updeelt in dat jöödsche, christliche, armeensche un musliemsche Viddel. En Muur geiht üm de ganze Ooldstadt umto.
4. Wie dat politisch um Jerusalem steiht, is heel un deel umstreden. De Stadt is Deel vun den Nahoost-Konflikt. De ööstliche Deel vun de Stadt mit siene bedüdenden Stäen för de jöödsche, christliche un musliemsche Religion schall na den Willen vun Palästinenser-Organisatschonen Hööftstadt vun en tokünftigen palästinens'schen Staat weern.
5. Jerusalem liggt in de Bargen vun Judäa un dat is de Hööftstadt vun den Staat Israel.

Fragen:
1. Wo hett dat mit dat plattdüütsche Theater in de froe neetied to doon? Weren dor Stücke up Plattdüütsch opföört?
2. Wie warrt dat plattdüütsche Theater in Noorddüütschland organiseert? Gifft dat enen Bund oder Landsverbände, de sik för dat plattdüütsche Theater inholen doot?
3. Wie warrt dat plattdüütsche Theater in Noorddüütschland finanziert? Gifft dat enen Steuern oder gifft dat anners för dat plattdüütsche Theater to doon?
4. Wo hett dat mit de Fastelavendspelen to doon? Weren dor Stücke op Plattdüütsch upföört, un wenn nich, wat is denn dorbi mit de Fastelavendspelen to doon?

Antwoorten:
1. Ja, dat gifft plattdüütsche Theaterstücken, as dat Enne vun de middelsassische Schriftsprake bleev is.
2. Dat gifft den Nedderdüütschen Bühnenbund un de noorddüütschen Bundslänner Kultuurarv bi de UNESCO, de sik för dat plattdüütsche Theater inholen doot.
3. Dat gifft keen Steuern för dat plattdüütsche Theater to doon, man dor gifft ok enen Bund Deutscher Amateurtheaters, de sik för dat plattdüütsche Theater inholen doot.
4. De Fastelavendspelen sünd ene Slag Stücke, de mit mündliche Sprake opföört warrt un dor Stücke up Plattdüütsch opföört warrn sünd.

Fragen:
1. Wo hett Helmut Schön sien Spelerloopbahn afslaten? He weer noch nah 1978 Bundstrainer?
2. Wo hett Helmut Schön mit sien Mannschap bi de Weltmeesterschap 1970 in Mexiko speelt? Gegen wennt he dorbi mit den düütsch Natschonalmannschap?
3. Wo hett Helmut Schön sien Trainerloopbahn afslaten? He weer noch nah 1978 Bundstrainer?

Antwoorten:
1. Helmut Schön is na sien Afscheed 1978 vun den Bundstrainerposten torüchtrucken in Wiesbaden torüchkamen.
2. Mit den düütsch Natschonalmannschap hett he bi de Weltmeesterschap 1970 in Mexiko speelt gegen Öösterriek, Schottland un Zypern. Gegen Öösterriek wunn he mit 5:0 Doren.
3. Helmut Schön is na sien Afscheed 1978 vun den Bundstrainerposten torüchtrucken in Wiesbaden torüchkamen.

Fragen:
1. Wo hett Jesus siene Familie in Galiläa leevt?
2. Wat is dat för en Teken, dat Jesus mit den Dämonen utdrifft un dat he sik mit de Lüde tohopenfüngen deit?
3. Wie hett Jesus sik mit de Pharisäers ümsprungen?
4. Wo hett Jesus siene Jüngers nahmen un wat is dor vun anfungen?
5. Wat is dat för en Straaf, den de Römers bi Upsternaatschen un Slaven bruukt hefft?

Antwoorten:
1. Jesus siene Familie in Galiläa leevt in Nazaret.
2. Dat Teken, dat Jesus mit den Dämonen utdrifft un dat he sik mit de Lüde tohopenfüngen deit, is dat, dat he Kranke gesund maakt un Dämonen utdrieven kann.
3. Jesus sik mit de Pharisäers ümsprungen, weil se em an’n Sabbat angrepen harrn un he dor up mit siene Jüngers gegen an streden is.
4. Jesus hett siene Jüngers nahmen, as he sik beropen harr, dat Gott sien Riek kamen deit un dat dat mit de Herrschop vun dat Quade nu to Enn geiht. Dor weer se ok för siene Familie un för den Tempel in Jerusalem verantwortlich.
5. Dat Straaf, den de Römers bi Upsternaatschen un Slaven bruukt hefft, is dat Krüüzigen. Jesus is op dat Krüüz slahn un in’t Graff leggt wurrn.

Fragen:
1. Wat is en Demokratie? Wo hett dat mit de Demokratie to doon?
2. Wie warrt de Demokratie in de Antike utbildet ween? Was hebbt Aristoteles över de Demokratie dach?
3. Wann is de Demokratie in Europa nix mehr nableven? Wo hett dat mit de Demokratie to doon in Grootbritannien?
4. Wie warrt dat Parlament inföhrt ween? Wat sünd de Grundrechten vun en modern Parlament?
5. Woneem is de Demokratie först wedder anfungen? Wo hett dat mit de Demokratie to doon in den Engelschen Börgerkrieg?

Antwoorten:
1. En Demokratie is en Form vun Herrschup, wo direkt vun dat Volk utöövt warrt.
2. Aristoteles meen, dat de Demokratie een Grundlaag vun de Freeheit hett un dat dor ok noch twee annere Saken to hören doot: Autonomia ( sik süms de Gesetten geven) un Autochthonia (ut de sülvige Eer, tagenboren).
3. De Demokratie is in Europa nix mehr nableven, as dat röömsche Riek ünnergahn weer. Bloß bi de Gemeenden leev dor noch wat vun na.
4. Dat Parlament warrt inföhrt ween, as dat Ünnerhuus tostann keem. An’n Anfang harr düt Huus nich veel to mellen un de König lä dor ok sien Hand up. As de Afsluut Monarchie opkamen weer, is de Macht vun düt Huus noch ringer wurrn.
5. De Demokratie is först wedder anfungen in Grootbritannien. Dat hett mit den Engelschen Börgerkrieg to doon. In Cromwell siene Tioeden geev dat ok Lüde, as John Lilburne, de foddern, dat Slaveree un Leibeigenschaft afschafft weern mössen un all Mannslüde en allgemeen un free Wahlrecht geneten schollen.

Fragen:
1. Wat is Riem in de Dichterie? Wo hett dat mit Riem to doon?
2. Wie warrt Riem in de Dichterie billt? Gifft dat ene Form, wo een Wöör un Lude lieker klingt?
3. Welke Formen vun Riem gifft dat in de Dichterie? Gifft dat den Beginnriem oder Alliteratschoon?
4. Wie warrt Rhythmus in een Gedicht to kriegen? Gifft dat ene faste Wiese, wo Rhythmus bruukt warrt?
5. Wat is mit de Riemstrukturen in Spraken, wo Riemstrukturen minder utbeed sünd?

Antwoorten:
1. Riem is een Element in de Dichterie, dat sik vöör, dat Gedicht klingt, tosamenhängend maakt. Dat gifft ene Form, wo een Wöör un Lude lieker klingt.
2. Riem warrt billt, wenn een Wöör un Lude lieker klingt. Faken buut een Dichter düsse lieken Wöör un Lude up besunner Steden in enen Vers in, in de tradittschonellste Form an’n Enne.
3. Gifft dat den Beginnriem oder Alliteratschoon? De meest bruukt Form is de vullstännige Riem, waarbi de gröötste Deel van dat Woord dat sülve is, so as de Wöör Lippe un Stippe. De Annern bekende Form Riem is de Beginnriem (Alliteratschoon), waarbi alleen de Anfangsluud de sülve is, so as in Lippe un Luft.
4. Wie warrt Rhythmus in een Gedicht to kriegen? Gifft dat ene faste Wiese, wo Rhythmus bruukt warrt? De Rhythmus van ’ne Sprake bestimmt för en groot Deel wo en Gedicht klingt. För völe traditschonelle Dichtformen ligt daarümme faste vovöle Silven enen VErs hebben hag.
5. Wat is mit de Riemstrukturen in Spraken, wo Riemstrukturen minder utbeed sünd? De Riekriekdom van ’ne Sprake bestimmt to enen groten Deel, wat för ne Aard Poesie, ene Sprake veel bruukt. Bi metrisch Rhythmus ligt exakt fast, wo Nadruck up Silven in Munster, de sik wedderhaalt, ligt.

Fragen:
1. Wo hett dat mit de Sprake in dat ole Grekenland to doon? 
2. Wie warrt de Tiet in't Plattdüütsche indeelt? Gifft dat Archaischen, klassische, hellenistische oder röömsche Tieden?
3. Wo hett dat mit den Staat in Grekenland to doon? 
4. Wie warrt de Kultuur in Grekenland utbreedt weern? Gifft dat en groten Deel, wat nich mehr nableven deit?
5. Wo hett dat mit den Olympschen Spele to doon?

Antwoorten:
1. De Sprake weer för Kunst un Kultuur wichtig.
2. Dat gifft Archaische Tied (ca. 750-c.489 v. Chr), klassische Tiet (ca.500-324 v. Chr) un hellenistische Tiet (324-150 v. Chr). Röömsche Grekenland weer de Tiet twüschen den Sieg vun dat Röömeriek in'n Krieg gegen Korinth 146 v. Chr un Konstantin sien Grünnen von Byzanz as Hööftstadt van Rom (325 n.
3. De olen Greken hebbt keen gemeensam Staat oder Heerscher, wat se verenige weer de gemeensame Sprake un Kultuur.
4. Dat Christendom in't late 4. bit fröhe 6. Jahrhundert is dat Christendom in't late 4. bit fröhe 6. Jahrhundert, wat mit den Afsluss von Platon sien Akademie dör Justinian I. (529) to Enn geiht un worüm ok en groten Deel ut düsse Tieden nich mehr nableven deit.
5. Alleen Manner kunn antreden un Fruen kunn nich mitmaken, se weren nich eenmaal verlövt de Spele antokieken. Olympsche Sportaarden weren Rennen, Speersmeten, Diskusmseten un Ringkamp.

Fragen:
1. Wo hett dat mit de Düütsche Bahn to doon?
2. Wat hebbt wi na de düütsche Eenheit hatt?
3. Wo sünd de Düütsche Bundsbahn un de Düütsche Rieksbahn vun de DDR nu tosamen? Hebbt se noch en Monopool?
4. Wie is dat mit den Tosamensluss von de Iesenbahn-Firmen in Düütschland? Gifft dat noch annere Firmen, as DB Feernverkehr, DB Regio un Railion?
5. Wat is denn nu mit de Düütsche Bahn passert? Is se noch en Staatsbahnen oder is se privatiseert?

Antwoorten:
1. De Düütsche Bahn is an’n 1. Januar 1994 ut de privatiseerte Düütsche Bundsbahn un de Düütsche Rieksbahn vun de DDR entstahn.
2. Na de düütsche Eenheit hebbt wi twee Staatsbahnen in Düütschland hatt, de Düütsche Bundsbahn (DB) un de Düütsche Rieksbahn vun de DDR (DR), de heel un deel ünnerscheedlich werrn.
3. Nee is dat nich mehr so. De twee Staatsbahnen hebbt den düütschen Staat denn privatiseert, wat meent, dat se nich mehr tosamen sünd.
4. Ja, dat gifft noch annere Firmen, as DB Feernverkehr, DB Regio un Railion. Un de Düütsche Bahn is opdeelt in disse dree Firmen.
5. De Düütsche Bahn is nu en privatiseerte Firma. Se is nich mehr en Staatsbahnen.

Fragen:
1. Wo hett Dresden sien Naam kregen?
2. Wat is de Bedüden vun den Naam Dresden in't Plattdüütsche? Kannst du den Naam in en annere Spraak översetten?
3. Wo liggt Dresden in Sassen?
4. Wat is de Bedüden vun den Begriff "Landshööftstadt"? Kannst du dat in't Plattdüütsche översetten?
5. Wo hett Dresden sien Historie ännert?

Antwoorten:
1. De Stadt kummt vun'n ooltsorbschen „Drežďany“.
2. De Naam Dresden is ene Stadt- oder Lännernaam un kann nich so gau översetten warrn. Dat gifft enen Naam för de Stadt in't Hoochdüütsche, de "Dresden" is.
3. Dresden liggt in'n Oosten vun Sassen, in ene Moll beidersiets vun de Elv.
4. De Begriff "Landshööftstadt" bedüden, dat de Stadt as Hööftstadt vun en Länner oder Land funktioneerert.
5. De Stadt wurr an'n 13. un 14. Februar 1945 vun US-amerikaansche un engelsche Bombenflegers angrepen un to 60 % demoleert.

Fragen:
1. Wo liggt Polen in Europa?
2. Welke Spraken warrt in Polen snackt? Un welche sünd Amtsspraken?
3. Wie is dat mit den Naam vun Polen? Warrt he ok anners schreven?
4. Wo hett Polen an’n Anfang grenzt? De Grenzen sünd nich mehr so, as se vörher weer.
5. Wie is Polen inholen? 

Antwoorten:
1. Polen liggt in’t Zentrum vun Europa un grenzt an Düütschland, Tschechien, de Slowakei, de Ukraine, Wittrussland, Litauen un en lütten Deel vun Russland.
2. Amtsspraak is Poolsch. Dat warrt in Delen vun Polen ok Hoochdüütsch, Kaschubsch un Ukrainsch snackt. Plattdüütsch warrt fast nich mehr snackt. Welke Polen snacken ok Russ’sch.
3. De Hööftstadt is Warschau. Dat warrt ok anners schreven: Wrocław, Kraków oder Gdańsk.
4. Polen grenzt an Düütschland, Tschechien un de Slowakei. In’n Noordoosten liggt en Deel vun Oostpreußen, hüt Woiwodschop Ermland-Masuren. In’n Westen liggt Grootpolen, in’n Oosten Masowien, Podlachien un de Woiwodschop Lublin un in de Mitt de Woiwodschop Lodsch.
5. Polen is indeelt in 16 Woiwodschoppen.

Fragen:
1. Wat is Mythologie? Wo hett dat mit den Artikel in't Plattdüütsche to doon?

Antwoorten:
1. Mythologie is een Vertellen, de verklöört un uutleggt. Dat gifft ok Resten vun den Genitiv in Mythen.

Fragen:
1. Wo hett de Kaiser sik an’n 8. un 9. Januar 1917 mit de Upperste Spitz vun dat Heer besnackt?
2. Wat harr Woodrow Wilson den USA-Kongress an’n 18. Dezember 1916 vörslahn?
3. Wo hett de Kaiser sik an’n 12. un 13. Januar 1917 mit den Hööfdredakteur Theodor Wolff ut’t „Berliner Tageblatt“ besnackt?
4. Wat hefft de Middelmächte an’n 30. Dezember 1916 kloorstellt?
5. Wo hett Präsident Wilson den US-Kongress opropen, um mitmaken bi den Krüüztog vun de Demokratien?

Antwoorten:
1. An’n 8. un 9. Januar 1917 hett de Kaiser sik mit de Upperste Spitz vun dat Heer besnackt.
2. Woodrow Wilson harr den USA-Kongress an’n 18. Dezember 1916 vörslahn, he woll de beiden Kriegsparteien an een Disch bringen, hefft de Middelmächte sik Schuller an Schuller stellt.
3. An’n 12. un 13. Januar 1917 hett de Kaiser sik mit den Hööfdredakteur Theodor Wolff ut’t „Berliner Tageblatt“ besnackt. Wolff noteer, dat Wilson rutseggt harr, wat de Entente antert harr.
4. De Middelmächte lehnten Wilson sien Vörslag, over Freden to verhanneln, af.
5. Präsident Wilson hett den US-Kongress opropen, um mitmaken bi den Krüüztog vun de Demokratien, de dat „up den Freden afsehn“ harrn, gegen de Autokratien up de Eer, de ehr „Militär gegen annere insetten“ döen.

Fragen:
1. Wo hett dat mit den Kaiser in'n Dartigjöhrigen Krieg to doon? He weer denn wedder stevig in'n Saddel oder is he utkniepen wurrn?
2. Wie hett Gustav II. Adolf vun Sweden den Krieg an dat Huus Habsborg verklaren dö?
3. Wat hett de Raat vun dat Riek unner Kanzler Graaf Axel Oxenstierna in den Verdrag vun Prag afslaten? Wo hett he sik denn mit den Kaiser verhannelt?
4. Wie is de Koalitschoon gegen de Habsborgers 1635 utbillt weern? Woneem sünd de Franzosen in den Krieg up een Siet stünnen?
5. Wat is de Freden vun Westfalen un wo hett se denn afslaten wurrn? Wo is dat denn mit den Krieg to Enne kamen?

Antwoorten:
1. De Kaiser weer denn wedder stevig in'n Saddel, man he is 1634 in Eger ümbringen laten.
2. Gustav II. Adolf vun Sweden hett den Krieg an dat Huus Habsborg verklaren dö, as he den Böverbefehl över de franzöös'schen Truppen övernahmen harr.
3. De Raat vun dat Riek unner Kanzler Graaf Axel Oxenstierna hett in den Verdrag vun Prag en Sunnerfreden mit de Habsborgers afslaten, wat he denn mit den Kaiser verhannelt hett, is nich bekannt.
4. De Koalitschoon gegen de Habsborgers 1635 utbillt weern as een Koalitschoon vun Frankriek un Sweden, woneem de Franzosen unner Kanzler Graaf Axel Oxenstierna in den Verdrag vun Prag en Sunnerfreden mit de Habsborgers afslaten harrn.
5. De Freden vun Westfalen is 1648 in Ossenbrügge un Mönster afslateh wurrn, wat dat denn mit den Krieg to Enne kamen is, is nich bekannt.

Fragen:
1. Wo hett dat mit de Spraak vun de Greeksche Schrift to doon? Wann is se upkamen un bit warrn is se bruukt wurrn?
2. Wie warrt de Ooltgreeksche Spraak in veer Dialekten snackt un schreven wurrn?
3. Wo hett dat mit den Indruck vun de Ooltgreeksche Spraak op annere europääsche Spraken to doon? Wann is se för Religion, Theologie un Fackspraken wichtig wurrn?
4. Wie warrt de Ooltgreeksche Spraak in de Literatur ansehn? Wann is se bit hen na dat Enne vun de Antike üm 600 n. Chr. rüm snackt wurrn?
5. Woher kummt de Ooltgreeksche Spraak? Is se en ganz egen indogermaansche Spraakform oder hett se mit annere Spraken ut düsse Familie to kriegen?

Antwoorten:
1. De Greeksche Schrift is upkamen, as dat Greeksche Volk in de Kuntreien vun de ööstliche Middellannsche See leevt harrn. Dat is ok bi den Anfang vun den Hellenismus (üm 300 v. Chr.) rüm bit to den Enne vun de Antike üm 600 n. Chr. rüm bruukt wurrn.
2. De Ooltgreeksche Spraak is in veer Dialekten snackt un schreven wurrn: Ioonsch-Attisch, Arkaadsch-Kyprisch, Äoolsch un Doorsch (Westgreeksch).
3. De Ooltgreeksche Spraak hett för Religion, Theologie un Fackspraken en grode Rull speelt. Vun dor ut hett se groden Indruck op de annern europääschen Spraken maakt.
4. In de Literatur güng dat mit düsse Spraak noch wieder bit hen na dat Enne vun de Antike üm 600 n. Chr. rüm. As besunnern Utdruck vun de klassische ooltgreeksche Spraak warrt de schreven Form vun dat Greeksch vun Attika in dat 5. un 4. Johrhunnert v. Chr. ansehn.
5. Dat is annahmen, dat de Ooltgreeksche Spraak en ganz egen indogermaansche Spraakform is. Se kummt aver ok ut den Indruck vun annere Spraken vun de vörindogermaanschen Völker her, de in Grekenland leevt harrn. Bispelen: θάλασσα thálassa „de See“ un νῆσος nē̃sos „Eiland“.

Fragen:
1. Wo hett dat mit den Satz vun’t Energiewohren to doon?
2. Wie warrt de Entropie in de Thermodynamik definiert?
3. Wo hett dat mit den Clausius-Clapeyron-Glieken to doon?
5. Wo hett dat mit den Gibbs-Helmholtz-Glieken to doon?

Antwoorten:
1. Dat Satz vun’t Energiewohren is en Grundlaag för de Thermodynamik, de sik mit de Energie beschäftigt, de free warrt, un de annere Formen vun Energie.
2. De Entropie is en Maat för den Unorden in en System, de sik op de Bewegen vun Deelken in’n leddigen ruum baseren deit.
3. De Clausius-Clapeyron-Glieken warrt bruukt, üm den Druck un Temperatur vun en Dampmaschien ut to recken.
5. De Gibbs-Helmholtz-Glieken warrt bruukt, üm den Differenz vun de fre’en Enthalpie utreken un wat över’t stoffliche Ümsetten vun Molekülen seggen.

Fragen:
1. Wat is Polytheismus? Wo hett dat mit den Gloven an mehr as een Godd to doon?

Antwoorten:
1. Polytheismus is de Gloven an mehr as een Godd. De gröttsten polytheistschen Religionen sind vandage de Hinduismus (de man ook monotheistsche Ansichten het), de traditschonelle chineesche Religioon un de Shintoismus.

Fragen:
2. Wie warrt de Demokratie in Grootbritannien utwesselt weern? In Cromwell siene Tioeden geev dat ok Lüde, as John Lilburne, de foddern, dat Slaveree un Leibeigenschaft afschafft weern mössen.
3. Wat is de „Bill of Rights“ in Grootbritannien? 
4. Wo hett dat mit de Demokratie in Europa ünnergahn? 
5. Wie is de Demokratie in Rom utwesselt weern? 

Antwoorten:
2. In Cromwell siene Tioeden geev dat ok Lüde, as John Lilburne, de foddern, dat Slaveree un Leibeigenschaft afschafft weern mössen.
3. Dat Parlament kreeg dat Recht mit, tohopen to kamen ahn den König sien Willen.
4. Bloß bi de Gemeenden leev dor noch wat vun na.
5. As dat röömsche Riek ünnergahn weer, weer vun de Demokratie nix mehr nableven.

Fragen:
1. Wo hett dat mit den Bundsraat för Nedderdüütsch to doon?
2. Wie warrt de Afornten för de acht Bundslänner in Plattdüütschland wählt? 
3. Wo hett dat mit den Spreker vun den Bundsraat to doon?
4. Wie warrt de Geschäften för den Bundsraat föhrt?
5. Wo hett dat mit de Opgaven un Telen vun den Bundsraat to doon?

Antwoorten:
1. De Bundsraat is 2002 grünnt worrn un schall de Intressen vun dat Nedderdüütsche bi’n Bund un in Europa vertreden.
2. De Afornten warrt mehrstendeels vun de Landsverbänn vun’n Bund för Heimat un Ümwelt in’n Bundesraat schickt. Per Bundsland warrt twee Delegeerten schickt, de tohoop en Stimm hebbt.
3. De Sprekersche is opstunns Saskia Luther un Spreker is Heinrich Siefer.
4. De Geschäften sünd bet 2017 vun dat Institut för Nedderdüütsche Spraak in Bremen föhrt worrn.
5. Hööftopgaven sünd dat kritische Beoordelen vun dat, woans de Sprakencharta üm- un insett warrt, as ok de konstruktive Stütt un Stöhn bi düssen Perzess.

Fragen:
1. Wo hett dat mit den Riem to doon in't Plattdüütsche?
2. Wie warrt de Alliteratschoon (Beginnriem) in't Plattdüütsche bruukt?
3. Wo hett dat mit den Rhythmus to doon in't Plattdüütsche?
4. Wie warrt de Riemstrukturen in't Plattdüütsche bruukt?
5. Wo hett dat mit den Metrum to doon in't Plattdüütsche?

Antwoorten:
1. De Riem is en wichtig Element in de Dichterie, un dorbi söök een Dichter Wöör un Lude, de minner oder mehr liek klingt.
2. De Alliteratschoon (Beginnriem) is en Form, wo Bookstaven oder Lude an de Beginn van twee oder mehr upeenfolgen Wöör wedderhaalt.
3. De Rhythmus vun 'ne Sprake bestimmt för en groot Deel wo en Gedicht klingt, un dorbi warrt de Silven fastleggt, de sik wedderhaalt.
4. De Riemstrukturen sünd in jede Spraker un dichtersche Traditschoon anners, un dorbi warrt faken en faste Wiese bruukt, döör Akzentre oder Silven.
5. De Metrum is en wichtig Element in de Dichterie, un dorbi warrt de Silven fastleggt, de sik wedderhaalt, un dat gifft faken Dubbelsinnigheed.

Fragen:
1. Wo is de Düütsche Bahn (DB) utkamen? 
2. Wat gifft dat in de DB-AG för en Vörstand? Un wat sünd de Liddmannen?
3. Wo hett de düütsche Staat den Iesenbahn-Firmen privatiseert?
4. Wat gifft dat in de DB-AG för en Opsichtsraat? Un wat is de Vörsitter vun’n Opsichtsraat?
5. Wo kann een den Fohrplan utkriegen, wenn een mit de Düütsche Bahn fohrt?

Antwoorten:
1. De is an’n 1. Januar 1994 ut de privatiseerte Düütsche Bundsbahn un de Düütsche Rieksbahn vun de DDR entstahn.
2. As en Aktiensellschop hett de DB-AG en Vorstand. De Liddmannen sünd: Dr. Rüdiger Grube (Vorsitter), Diethelm Sack, Dr. Norbert Bensel, Dr. Bernd Malmström, Klaus Daubertshäuser un Karl-Friedrich Rausch.
3. Na de düütsche Eenheit hebbt wi twee Staatsbahnen in Düütschland hatt. Un denn geev dat siet 1990 keen Monopool mehr för de Iesenbahn in Düütschland. So sünd dor nu niege Iesenbahn-Firmen entstannen, as Connex oder PEG.
4. As en Aktiensellschop hett de DB-AG en Opsichtsraat. De Liddmannen sünd: Dr. Rüdiger Grube (Vorsitter), Diethelm Sack, Dr. Norbert Bensel, Dr. Bernd Malmström, Klaus Daubertshäuser un Karl-Friedrich Rausch.
5. Een kann den Fohrplan utkriegen, wenn een mit de Düütsche Bahn fohrt, op de Siet reiseauskunft.bahn.de.

Fragen:
1. Wo is Dresden liggen?
2. Wat hett Dresden 1945 passert? 
3. Wie veel Dode hebbt in Dresden bi de Angrepen weern?
4. Wo hett Richard Gedlich sien Footballnatschonalspeler-Loop begünnt? Un wo is he doodbleven?
5. Wie is Ludwig Haach doodbleven?

Antwoorten:
1. Dresden liggt in ene Moll beidersiets vun de Elv in'n Oosten vun Sassen.
2. De Stadt wurr an'n 13. un 14. Februar 1945 vun US-amerikaansche un engelsche Bombenflegers angrepen un to 60 % demoleert.
3. Intwüschen warrt blots noch vun 35.000 snackt.
4. Richard Gedlich is doodbleven, as he in de Tiet vun den Doodslag in Dresden weer. De Text geiht aver nich op, wo he doodbleven is. Un dat is ok nich to sehn, woneem he sien Footballnatschonalspeler-Loop begünnt hett.
5. Ludwig Haach is doodbleven, as he 1842 doodbleven is. De Text geiht aver nich op, wo he doodbleven is. Un dat is ok nich to sehn, woneem he sien Maleree- un Teknerei-Loop begünnt hett.

Fragen:
1. Wat is en Bahnstieg un wo hett dat mit de Bahnhoff to doon?
2. Wie warrt de Huusbahnstieg, Siedenbahnstieg, Middelbahnstieg, Twüschenbahnstieg, Tungenbahnstieg, Tweeschenbahnstieg un Dwarsbahnstieg billt?
3. Wat is en Kombibahnstieg und wo hett dat mit de Verkehrsmiddels to doon?
4. Wo warrt de Bahnstieg von en Bahnhoff anleggt? De Bahnstieg liggt blots mit een Sied an en Gleis oder mit twee Sieden?
5. Wat is de Twüschenbahnstieg un wo hett dat mit de Togang to een Gleis to doon?

Antwoorten:
1. En Bahnstieg is en faste Plattform, de bi en Bahnhoff langs en Gleis anleggt is, dat Lüüd ut en Iesenbahn-Tog in- un utstiegen köönt.
2. De Huusbahnstieg is de Bahnstieg, de direkt vör dat Empfangsgebüüd von en Bahnhoff liggt, ahn dat een över annere Gleise röver mutt. Dat is dormit jümmer ok en Siedenbahnstieg.
De Siedenbahnstieg liggt blots mit een Sied an en Gleis un is dorüm normalerwies an’n Rand von en Bahnhoff. De Middelbahnstieg hett Gleise an beide Sieden, de Twüschenbahnstieg is en Bahnstieg, de twüschen twee Gleise liggt, aver blots Togang to een Gleis büddt.
De Tungenbahnstieg is en Middelbahnstieg, de von en Dwarsbahnstieg aftwiegt. De Tweeschenbahnstieg warrt billt von twee Bahnstieg’, de to beide Sieden von en Gleis liggen doot.
De Dwarsbahnstieg is keen echten Bahnstieg, von wegen dat dor keen Tog höllt. De Kombibahnstieg is en Bahnstieg, an den op de twee Sieden twee verscheden Verkehrsmiddels hollt (to’n Bispeel en Iesenbahn-Tog un en Stratenbahn).
3. En Kombibahnstieg is en Bahnstieg, an den op de twee Sieden twee verscheden Verkehrsmiddels hollt.
4. De Bahnstieg von en Bahnhoff warrt normalerwies mit een Sied an en Gleis anleggt. Dorüm gifft dat nich mehr Twüschenbahnstiege, de twüschen twee Gleise liggen doot un dorbi Togang to een Gleis büddt.
5. De Twüschenbahnstieg is en Bahnstieg, de twüschen twee Gleise liggt, aver blots Togang to een Gleis büddt. Dorüm gifft dat nich mehr Twüschenbahnstiege in Düütschland.

Fragen:
1. Wo liggt Polen in Europa? Un welke Länner sünd dor an’n Anfang vun Polen?
2. Welche Spraken warrt in Polen snackt? In welchen Delen vun Polen gifft dat ok noch annere Spraken?
3. Wie is de Geografie vun Polen? Wo liggt de längste Stroom un welke Landschappen besteiht Polen ut?
4. Welche Woiwodschoppen sünd in Polen indeelt? Un welke Städer sünd in Polen to finnen?
5. In welken Woiwodschoppen is Polen demokraatsch?

Antwoorten:
1. Polen liggt in’t Zentrum vun Europa, an’n Anfang vun Polen sünd Düütschland, Tschechien, de Slowakei, de Ukraine, Wittrussland, Litauen un en lütten Deel vun Russland.
2. Amtsspraak is Poolsch. Dat warrt in Delen vun Polen ok Hoochdüütsch, Kaschubsch un Ukrainsch snackt. Plattdüütsch warrt fast nich mehr snackt. Welke Polen snacken ok Russ’sch.
3. Polen erstreckt sik vun de Oostsee to de Sudeten un de Karpaten (Tatra). De längste Stroom is de Wießel. Polen besteiht ut ene Reeg vun Landschappen: De Noordwesten vun Polen (de Deel, de an’e Ostsee liggt) heet Pommern un Kujawien, in den Noordoosten liggt en Deel vun Oostpreußen, hüt Woiwodschop Ermland-Masuren. In’n Westen liggt Grootpolen, in’n Oosten Masowien, Podlachien un de Woiwodschop Lublin un in de Mitt de Woiwodschop Lodsch.
4. De Verfaten is demokraatsch. Polen is indeelt in 16 Woiwodschoppen. Dat sünd: Woiwodschop Ermland-Masuren, Woiwodschop Grootpolen, Woiwodschop Hilligkreuz, Woiwodschop Karpatenvörland, Woiwodschop Lüttpolen, Woiwodschop Kujawien-Pommern, Woiwodschop Lebus, Woiwodschop Lodsch, Woiwodschop Lublin, Woiwodschop Masowien, Woiwodschop Nedderslesien, Woiwodschop Oppeln, Woiwodschop Podlachien, Woiwodschop Pommern, Woiwodschop Slesien, Woiwodschop Westpommern.
5. De Städer sünd Warschau (Warszawa), Krakau (Krakow), Lodsch (Łódź), Breslau (Wroclaw), Posen (Poznan), Danzig (Gdansk), Stettin (Szczecin), Bromberg (Bydgoszcz), Kattowitz (Katowice), Lublin, Białystok, Gdingen (Gdynia) un Thorn (Torun).

Fragen:
1. Wat is dat Institut för Nedderdüütsche Spraak (INS) un wat doot dat?
2. Wo hett dat INS grünnt? Un woneem is dat Huus, in dat se sitt?
3. Wat gifft dat an Opgavenrebeden vun't INS? Un wat bedeelt dat för de Nedderdüütsche Spraak?
4. Wie kummt dat INS finanziell tostännig? Un woneem kemen de Middels ut?
5. Wo is dat Kooperatschoon mit'n Mekelborgsche Folklorezentrum (MFZ) in Rostock för? Un wat is dorup henkamen?

Antwoorten:
1. Dat Institut för Nedderdüütsche Spraak (INS) is en Institut, dat sik as wetenschappliche Inrichten överregional de Pleeg un den Foortbestand vun nedderdüütsche Spraak, Literatur un Kultur to Opgaav maakt hett. Dat INS koopereert mit Scholen, Kinnergoorns, Autoren, Pastern, Musikern, Medien- un Theaterlüüd, man ook mit Verenen un Verbänn.
2. Dat INS is grünnt worrn in de 1970er Johren. De eerste Grünnensversammeln hett an'n 27.4.1973 stattfunnen. Un dat Huus Schnoor 41 steiht siet 1973 ünner Denkmaalschuul.
3. Dat INS hett mehrere Opgavenrebeden, as de Bewohren un den Foortbestand vun Nedderdüütsche Spraak, Literatur un Kultur to Opgaav maken. Dorbi gifft dat ok tallrieke Projekten un Veranstalten, de mit annere Institutschonen un Nettwarken gemeensam plaant un dörföhrt warrt.
4. Dat INS kummt finanziell tostännig, wenn een Liddmaatsbidrääg, Verkoopsinnahmen, Honoraren un Spennen kümmt. 2012 umfaat de Huushoold Innahmen un Utgaven vun je wat 360.000 €.
5. Dat Kooperatschoon mit'n Mekelborgsche Folklorezentrum (MFZ) in Rostock is för den Austausch vun Ideen, Projekten un Materialien för Nedderdüütsche Spraak un Literatur. Dorup henkamen de beiden Institutionen op Initschativ vun'n Bremer Börgermeester Klaus Wedemeier.

Fragen:
1. Woneem is dat Nedderdüütsche Sekretariat in’t Bundsministerium för Innen?
2. Wie warrt den Bundsraat för Nedderdüütsch finanziert?
3. Welke Afornten sitt in’n Bundsraat un welke sünd de Vertreiders ut de acht Bundslänner, de en gröttern Andeel an dat plattdüütsche Spraakrebeet hebbt?
4. Wie warrt den Bundsraat för Nedderdüütsch opboen un plegen?
5. Woneem is de Nettwark vun’n Bundesraat för Nedderdüütsch in’t Internet to finnen?

Antwoorten:
1. Dat Nedderdüütsche Sekretariat is in’t Bundsministerium för Innen.
2. De Afornten sitt in’n Bundsraat un de Vertreiders ut de acht Bundslänner, de en gröttern Andeel an dat plattdüütsche Spraakrebeet hebbt, warrt mehrstendeels vun de Landsverbänn vun’n Bund för Heimat un Ümwelt in’n Bundesraat schickt.
3. De Afornten sitt in’n Bundsraat un de Vertreiders ut de acht Bundslänner, de en gröttern Andeel an dat plattdüütsche Spraakrebeet hebbt, warrt mehrstendeels vun de Landsverbänn vun’n Bund för Heimat un Ümwelt in’n Bundesraat schickt. De twee Afornten vun de Plautdietschen sitt in’n Bundsraat.
4. Den Bundsraat för Nedderdüütsch opboen un plegen warrt vör allen op den Billenssekter, dat he ok en Nettwark (na Europa, to’n Bund, to’n Bundsdag un in de Lännerverwalten rin) opboen un plegen will.
5. De Nettwark vun’n Bundesraat för Nedderdüütsch is in’t Internet to finnen as „Niederdeutschsekretariat“.

Fragen:
1. Wo hett dat mit de Universität in Ollnborg anfangen? Wann is se grünnt wurrn?
2. Wie warrt de Carl von Ossietzky Universität nöömt? Un wat hebbt se för en Pries kregen?
3. Wo hett dat mit den AStA in Ollnborg to doon? Wann is de AStA grünnt wurrn un wat för een sorgt dor för?
4. Wie warrt de Universität in Ollnborg utbaut? Wo gifft dat denn noch enen Hööfschooldag?
5. Wo hett dat mit den Angelus Sala-Pries to doon? Wann is he nömmt wurrn un wat för een kregen he?

Antwoorten:
1. De Universität wurr an' 7. März 1793 grünnd.
2. Se is na Carl von Ossietzky nöömt, de en Nobelpriesdräger weer. He hett in Düütschland den Wedderstand gegen den Naziregen utfohrt un is denn 1935 doodbleven. De Universität kreeg 1991 den Naam vun Ossietzky.
3. De AStA (Studentenverband) is grünnt wurrn, as de Studenten in Ollnborg sück för eenee Samenstimmung in'n Stuendenausschuss insetten kunn. Dat hett 1994 aflehnt wurrn.
4. De Universität is jümmer noch up den Hööfschooldag an' Uhlhornsweg to sehn, aver ok op den Campus Wechloy. Dor gifft dat denn ok enen Internatschonale Sömmerfest.
5. De Angelus Sala-Pries warrt jedes Johr an Schöler uttekent, de in't Fack Chemie good Leistungen schafft hebbt. He is na Angelo Sala nömmt wurrn, de en Dokter un Natuurwetenschapler weer.

Fragen:
1. Wat is en Bahnstieg un woneem gifft dat to sehn?
2. Wo hett dat mit de Formen von Bahnstiegen to doon? Gifft dat Huusbahnstieg, Siedenbahnstieg, Middelbahnstieg, Twüschenbahnstieg, Tungenbahnstieg, Tweeschenbahnstieg un Dwarsbahnstieg?
3. Wo hett dat mit den Typen von Bahnstiegen to doon? Gifft dat en Huusbahnstieg, Siedenbahnstieg, Middelbahnstieg, Twüschenbahnstieg, Tungenbahnstieg, Tweeschenbahnstieg un Dwarsbahnstieg?
4. Wo hett dat mit den Verkehrsmiddels to doon? Gifft dat en Kombibahnstieg, wo een Bahnstieg för twee verscheden Verkehrsmiddels bruukt warrt?
5. Wat is de Twüschenbahnstieg un wo hett he sien Bedüden ännert?

Antwoorten:
1. En Bahnstieg is en faste Plattform, de bi en Bahnhoff langs en Gleis anleggt is, dat Lüüd ut een Iesenbahn-Tog in- un utstiegen köönt.
2. Ja, dat gifft mehrere Formen von Bahnstiegen: Huusbahnstieg, Siedenbahnstieg, Middelbahnstieg, Twüschenbahnstieg, Tungenbahnstieg, Tweeschenbahnstieg un Dwarsbahnstieg.
3. Ja, dat gifft mehrere Typen von Bahnstiegen: Huusbahnstieg, Siedenbahnstieg, Middelbahnstieg, Twüschenbahnstieg, Tungenbahnstieg, Tweeschenbahnstieg un Dwarsbahnstieg.
4. Ja, dat gifft en Kombibahnstieg, wo een Bahnstieg för twee verscheden Verkehrsmiddels bruukt warrt. Dat kann to’n Bispeel en Iesenbahn-Tog un en Stratenbahn sünd.
5. En Twüschenbahnstieg is en Middelbahnstieg, de von en Dwarsbahnstieg aftwiegt. De Bedüden vun den Twüschenbahnstieg hett sik ännert, denn he is nich mehr so bruukt as to’n Bispeel in Düütschland.

Fragen:
1. Welke Länner hebbt in den Tweeten Weltkrieg an'n Enn' 1945 unnerlag?
2. Wie hett dat mit de Sowjetunion to'n Kollen Krieg kamen?
3. Welche Länner sünd na den Tweeten Weltkrieg wedder upstahn un warrt in de Tiet vun den Nahkriegsordnung utbaut?
4. Welke Länner hebbt in den Tweeten Weltkrieg an'n Enn' 1945 unnerlag, un welke Länner sünd doruphen wedder upstahn un warrt in de Tiet vun den Nahkriegsordnung utbaut?
5. Welche Länner hebbt in den Tweeten Weltkrieg an'n Enn' 1945 unnerlag, un welke Länner sünd doruphen wedder upstahn un warrt in de Tiet vun den Nahkriegsordnung utbaut?

Antwoorten:
1. Düütschland, Italien
2. De Sowjetunion hett mit de Westmächte in de USA un Grootbritannien to'n Kollen Krieg kamen.
3. De Vereente Natschonen sünd na den Tweeten Weltkrieg wedder upstahn un warrt in de Tiet vun den Nahkriegsordnung utbaut. Dör de Grünnen vun de USA, Grootbritannien, Frankriek un China hebbt se eenig för en düersamen Wohren vun den Weltfreeden to maken.
4. De Länner, de an'n Enn' 1945 unnerlag sünd, sünd Düütschland, Italien, Japan, Polen, Frankriek, Belgien, Luxemborg, Nedderlannen, Grootbritannien, Australien, Neeseeland, Kanada, China, Sowjetunion, Griekenland, Jugoslawien un de USA.
5. De Länner, de an'n Enn' 1945 unnerlag sünd, sünd Düütschland, Italien, Japan, Polen, Frankriek, Belgien, Luxemborg, Nedderlannen, Grootbritannien, Australien, Neeseeland, Kanada, China, Sowjetunion, Griekenland, Jugoslawien un de USA. De Länner, de wedder upstahn sünd, sünd de Vereente Natschonen (USA, Grootbritannien, Frankriek, China) un de Länner, de in den Tweeten Weltkrieg nich an'n Enn' 1945 unnerlag sünd.

Fragen:
1. Wo hett Waterstoff in dat Universum an fakensten vörkummt?
2. Wie warrt Waterstoff normalerwies för utdrückt? Un wat is denn dat Atomteken för Waterstoff?
3. Woneem steiht Waterstoff in dat Periodensystem un wat gifft dorvun anners as Protium?
4. Wo hett Waterstoff mehr de Egenschoppen vun, wenn dat fasten Waterstoff is?
5. Wat reageert Waterstoff mit Suerstoff to?

Antwoorten:
1. Dat gifft nich so veel Waterstoff in’t Universum an fakensten vörkummt as annere Elemente.
2. Waterstoff warrt normalerwies mit dat Atomteken H afkört un is ok as Protium betekend.
3. Waterstoff steiht ganz baven links an de eersten Steed in dat Periodensystem un gifft ok noch annere Isotopen, as dat latiensch Hydrogenium – Watermaker betekent warrt.
4. Fasten Waterstoff hett denn aver doch mehr de Egenschoppen vun de Metallen.
5. Waterstoff reageert mit Suerstoff to Water, wat dat Oxid vun den Waterstoff is: 2 H2 + O2 → 2 H2O

Fragen:
1. Wo hett dat mit de Vagels to doon?
2. Wie warrt de Systematik von de Vagels beschreven? Wo sünd de Ooltkeevvagels un de Neekeevvagels in de Systematik vun de Vagels tostännig?
3. Wo hett dat mit den Nesten vun de Vagels to doon?
4. Wie warrt de Grött von de Vagels beschreven? Gifft dat gröttste Vagels in Europa oder in annere Delen vun de Welt?
5. Wo hett dat mit den Flegen vun de Vagels to doon?

Antwoorten:
1. De Vagels warrt in twee Ünnerklassen indeelt: Ooltkeevvagels (Palaeognathae) mit bloots en poor Oorn: de Loopvagels (Struthioniformes, so as Struuß, Nandu un Emu), un de Neekeevvagels.
2. De Systematik vun de Vagels is nich so wichtig, as dat bi annere Deerten is. Se warrt aver ok in twee Ünnerklassen indeelt: Ooltkeevvagels (Palaeognathae) mit bloots en poor Oorn un Neekeevvagels.
3. De Vagels leggt Eier, un dor kaamt de Lütten rut. Se boot toeerst een Nest, wo se de Eier rinleggt. Denn sitt se op de Eier un hoolt se warm, dat is dat Bröden.
4. Dat gröttste Vagel is de Afrikaansche Struuß. De gröttste, de flegen kann, dat is de Kondor in de Anden in Süüdamerika.
5. Nich all de Vagels köönt noch flegen. De Pinguinen sünd goot in’t Swemmen, aver flegen köönt se nich. Un de Kiwi ut Niegseeland kann ok blots lopen.

Fragen:
1. Wo is Hamborg in Düütschland mit dat Groot-Hamborg-Gesett to en Bundsland wurrn?
2. Wie hett Hamborg vör allens sien Inkamen ut de Abtei Turholt in Flandern verloren?
3. Wo is Bischop Ansgar 845 afreist un worrn, as he dat Bisdom ut Bremen wiederregeert harr?
4. Wie hett Hamborg den Eerdboden glieks maakt, as Mistui, en Obodritenfürst, in't Johr 983 dat deed?
5. Wat is de Freebreef, de Friedrich I. Barbarossa Hamborg 1189 utstellt hebben schall?

Antwoorten:
1. 1937
2. De Wikingers
3. He hett dat Bisdom ut Bremen wiederregeert un worrn, as he dat Bisdom ut Bremen wiederregeert harr.
4. Mistui, en Obodritenfürst, hett Hamborg den Eerdboden glieks maakt.
5. De Freebreef is de Freiheit vun de Stadt un de Lüüd dor in för dat Johr 1937 utstellt wurrn. Dat heet, dat se nich mehr in'e Armee rin möten, dat se keen Toll bet in de Noordsee betahlen möten, dat keeneen 15 Kilometers üm Hamborg en Borg buen dröff un dat se Veeh hebben dröfft, Fisch fangen un Bööm roden dröfft.

Fragen:
1. Wo kummt dat Begreep "Planet" ut?
2. Wie warrt en Planet in't Plattdüütsche utdrückt? Wo hett dat mit den Begreep "Wannelsteern" to doon?
3. Woveel Planeten gifft dat in uns Sünnsystem? Un welke vun de Planeten sünd Dwargplaneten?
4. Wie is de Definitschoon för en Planet ännert wurrn? Wo hett sik dat nu ännert un wat is denn noch nich mehr so rech as „richtigen“ Planet?
5. Woveel Dwargplaneten gifft dat in uns Sünnsystem, un welke vun deen sünd noch nauer ünnersocht warrt?

Antwoorten:
1. Dat Begreep "Planet" kummt ut dat Greeksche un heet so veel as Wannelsteern.
2. De Planeten sünd nich blots Steerns, man bewegt sik allmählich un werrn mol hier to seen un mol dor.
3. In uns Sünnsystem gifft dat negen Planeten: de Merkur, Venus, Eer, Mars, Jupiter, Saturn, Uranus, Neptun un Pluto. De Pluto is blots noch en Dwargplanet.
4. De Definitschoon för en Planet is ännert wurrn. Nu is en Planet een gröttere Massen, de as een Kugel formt sünd, man anners as en Steern nich vun sülvst lüchten dot. Un dormit dat sien Richtigkeit hett, hett nu ok Pluto en Nummer kregen.
5. Opstunns sütt uns Sünnsystem nu so ut: Merkur, Venus, Eer, Mars, Jupiter, Saturn, Uranus, Neptun un Pluto. De Pluto is blots noch en Dwargplanet. Un dormit dat sien Richtigkeit hett, hett nu ok Pluto en Nummer kregen.

Fragen:
1. Wo hett Knut Kiesewetter anfungen, Musik to maken?
2. Wie hett he sik in de Politik engaagt?
3. Wo hett he Musik studeert?
4. Wie hett he 2000 uttekent?
5. Wo hett Knut Kiesewetter bi 50 Johren Rutbringen vun Schallplatten rutbrocht?

Antwoorten:
1. He weer mit 14 Johren al Basuunspeler un Jazzsinger.
2. In de laten 1970er Johre hett he bi de Grüne Liste Nordfreesland mitmaakt.
3. He hett an de Hoochschool för Musik un Theater Hamborg Kompositschoon un Textschrieven för Leeder lehrt.
4. He hett den Ridderslag as Ridder vun de Ronneborg kregenb vunwegen siene Verdeenste um de düütsche Jazzmusik.
5. Bi den Fresenhoff bi Husum arbeidt un is dor ok bekannt wurrn mit allerhand Leeder op Plattdüütsch, Noordfreesch un Hoochdüütsch.

Fragen:
1. Wat is en Dageblatt un wat gifft dat dor in?
2. Wann is dat eerste Dageblatt rutkamen? Wo hett dat upstahn?
3. Wie warrt dat Dageblatt rutgeven? Gifft dat en bestimmten Rutgevers oder is dat eenfach ut Narichten to maken?
4. Wat gifft dat in de Narichtenbulletins Acta diurna, de Gaius Julius Caesar anfungen hett?
5. Wie warrt dat Dageblatt rutbrocht? Wann is dat rutkamen?

Antwoorten:
1. En Dageblatt is en Blatt, dat tominnst veermal in'e Weken rutkummt un dor allerhand verscheden Saken in kunnig maakt warrt.
2. Dat eerste Dageblatt is an'n 1. Juli 1650 in Leipzig rutkamen.
3. Dat Dageblatt warrt rutgeven, man dat gifft ok Narichten to maken, de in Metall-Lettern druckt wurrn sünd un op en holten Druckerpress utseten wurrn sünd.
4. De Narichtenbulletins Acta diurna sünd Narichten, de Gaius Julius Caesar anfungen hett, as he röömschen Kunsel weer.
5. Dat Dageblatt warrt rutbrocht, man dat gifft ok Narichten to maken, de in Metall-Lettern druckt wurrn sünd un op en holten Druckerpress utseten wurrn sünd.

Fragen:
1. Wo hett dat mit den Naam "Protestantismus" to doon? 
2. Wie is de Protestantismus in Düütschland tohopenslaten wurrn?
3. Woneem gifft dat en Augsborger Religionsfreden, un wat hefft dor för Folgen hatt?
4. Wo hett dat mit den Begriff "Evangeelsch" to doon? Un is dat ok so as in de düütsche (un plattdüütsche) Umgangssprake datsülvige?
5. Wie warrt de Protestantismus in de Nedderlannen tohopenslaten, un woneem is dat vun 2004 af an torekent?

Antwoorten:
1. De Naam Protestanten hett to kriegen mit de Protestatschoon vun Speyer.
2. De protestantschen Karken vun de verschedenen Bundslänner hefft sik in Düütschland tohopenslaten in de EKD.
3. Dat gifft en Augsborger Religionsfreden, un dat is 1555 tostanne kamen. Dor hett dat Hillge Röömsche Riek de lutherschen Karken gellen laten un dat duer denn noch bit to'n Enne vun'n Dartigjöhrigen Krieg 1648, bit ok de reformeerte Karken in dat Riek gellen laten wurrn is.
4. De Begriff "Evangeelsch" is ok so as in de düütsche (un plattdüütsche) Umgangssprake datsülvige. Hüdigendags meent de Wöör Protestantsch un Evangeelsch in de düütsche (un plattdüütsche) Umgangssprake datsülvige.
5. In de Nedderlannen gifft dat vun 2004 af an de Protestantsche Kark in de Nedderlannen (PKN).

Fragen:
1. Woneem is dat Recht opschreven worrn, wat in dat Sassenland güllig ween is?
2. Wie hett Eike vun Repgow dat Recht opschreven?
3. Wo harr dat Landrecht Gülligkeit bit 1794?
4. Wat is dat Lehnsrecht un woneem is dat beschrifft?
5. Wann is de Sassenspegel güng in den Verfaat vun dat Lann ehrn?

Antwoorten:
1. De Sassenspegel is vun den sassischen Ridder Eike vun Repgow üm dat Johr 1225 opschreven worrn.
2. He hett dor dat Recht opschreven, wat in dat Sassenland güllig ween is un wat bit darhen dör Vertelln wiedergewen worrn is.
3. In Preußen harr de Sassenspegel Gülligkeit bit 1794, as dat Allgemeen Landrecht Gülligkeet kreeg.
4. Dat Lehnsrecht beschrifft, woans dat in dat Lann togeiht, wat de Stänn angeiht. Vun den Keunig över de Försten bit na de Ridders.
5. De Sassenspegel is güng in den Verfaat vun dat Lann ehrn bit 1900.


Fragen:
1. Wo hett dat mit den Naam vun en Hööftstadt to doon?
2. Wie warrt de Hööftstadt utwählt? Gifft dat verschedene Grünn för de Utwahl vun en Hööftstadt?
3. Wo hett dat mit den Tied to doon in en Hööftstadt? Gifft dat Präsens, Präteritum, Perfekt un Plusquamperfekt, oder gifft dat noch annere Tieden?
4. Wie warrt de Hööftstadt utwählt, wenn dat Land nich so groot is? Gifft dat verschedene Grünn för den Utwahl vun en Hööftstadt in en lüttje Land?
5. Wo hett dat mit den Strategie to doon in en Hööftstadt? Gifft dat verschedene Grünn för den Utwahl vun en Hööftstadt, wenn dat Land nich so groot is oder wenn de Regeerung dor mit dat Militär un de Regeerung dichter bi ween will?

Antwoorten:
1. De Hööftstadt kann denn nich ünnerscheedlich wesen, wenn se ok den Naam vun dat Land oder Bundsland hett.
2. Gifft dat verschedene Grünn för de Utwahl vun en Hööftstadt. Dör de politische Grünn warrt een Stadt utwählt, wo nich een bestimmte Volksgrupp in dat Seggen hett. In den Fall vun en Bundsstaat kann man ok den Naam vun en annern Bundsland nahmen.
3. Ja, dat gifft dat. De Präsens is för dat, wat nu is. Dat Präteritum is för dat, wat weer (verleden Tiet). Dat Perfekt is för dat, wat jüst vörbi is un dat Plusquamperfekt is för dat, wat all lang vörbi is.
4. Gifft dat verschedene Grünn för den Utwahl vun en Hööftstadt in en lüttje Land. En Bispeel is Abuja in Nigeria. Dat is an de Stäe vun dat veel gröttere Lagos träen, vunwegen datt dat in’e Midden vun dat Land liggt un dor verschedene Volksgruppen in wahnt.
5. Gifft dat verschedene Grünn för den Utwahl vun en Hööftstadt, wenn dat Land nich so groot is oder wenn de Regeerung dor mit dat Militär un de Regeerung dichter bi ween will. En Bispeel is Naypyidaw in Myanmar. Düsse Stadt liggt duun an en Reeg vun Gemarken, wo dat Upstänn un Unroh gifft un de Regeerung dach sik, dat weer woll passlich, dor mit dat Militär un de Regeerung dichter bi to ween.

Fragen:
1. Wat heet Monotheismus?
2. Woher kummt de Begreep „Monotheismus“ her un warrt he bruukt?
3. Welke Religionen sünd monotheistisch? Gifft dat noch annere monotheistische Religionen, as in den Text nöömt wurrn is?
4. Wat is de Differenz twuschen Monotheismus un Polytheismus?
5. Woher kummt de Begreep „Monolatrie“ her un wat heet he?

Antwoorten:
1. Monotheismus (gr. μόνος mónos „alleen“ un θεός theós „Gott“) betekent Religionen oder Lehren vun de Philosophie, de (bloß) man een Gott kennen un gellen laten doot.
2. De Begreep „Monotheismus“ is toeerst in dat 17. Johrhunnert bi den engelschen Theologen un Philosophen Henry More bruukt wurrn.
3. Hüdigendags gifft dat de monotheistischen Religionen Jodendom, Christendom, Islam, Jesidendom, Sikhismus, Bahaidom un Zoroastrismus.
4. De Begreep „Monotheismus“ is en Form vun den Theismus. De Differenz twuschen Monotheismus un Polytheismus is, dat de monotheistischen Religionen bloß een Gott kennen un gellen laten doot, während de polytheistischen Religionen allerhand verschedene Gödder kennen un verehren deit.
5. De Begreep „Monolatrie“ heet en Form vun den Monotheismus, wo blots een vun de Gödder in de Reeg vun de Gödder verehrt warrt.

Fragen:
1. Wat is de Heliand un wat vertellt dat?
2. Woneem is dat schreven worrn un woneem is dat upschreven worrn?
3. Wie hett Ludwig den Fromme den Opdrag kregen, den Text to schrieven?
4. Wo sünd de twee meist vullstännigen Handschriften vun den Heliand nableven? 
5. Woneem gifft dat Lüttjere Delen vun den Heliand?

Antwoorten:
1. De Heliand is en groot Epos in ooltsassische Spraak, wat vertellt vun dat Leven vun Jesus Christus un hett so bi 6.000 Regen in Staavriems.
2. Dat is schreven worrn vun en Mönk ut dat Ümfeld vun dat Klooster Fulda, man de Tiet is nich genau bekannt. In den Vörwoort steiht, dat Ludwig de Fromme den Opdrag geven hett, den Text to schrieven.
3. Dat is blangen de ooltsass’sche Genesis dat eenzige grote Wark ut de ole Sassentiet. All beid hebbt disse Warken de Opgaav hatt, de heidnischen Sassen to dat Christendom to bekehren.
4. Uns sünd hüüt twee meist vullstännige Handschriften vun den Heliand nableven, de een in de Bayrische Staatsbibliothek in München un de annere in de Britische Bibliothek in London. Lüttjere Delen gifft dat in Berlin, den Vatikan, Straubing un Leipzig.
5. Dat gifft nich mehr Lüttjere Delen vun den Heliand.

Fragen:
1. Woher kümmt de Naam „Joden“ un wat bedütt he?
2. Wie warrt de Kultur, de Geschicht, de Religion un de Traditschoon vun dat Volk vun de Joden verstahn?
3. Woneem is dat Jodendom as en Weltreligion ankeken?
4. Wie hett sik dat Jodendom in de Historie entwickelt?
5. Wo gellt Lüüd mit jöödsch Öllern oder Konvertee as Jöden?

Antwoorten:
1. De Naam „Joden“ bedutt an un for sik „Judäers“ un hett to kriegen mit dat Königriek Juda, wat 587 v. Chr. unnergahn is, as de Babyloniers Jerusalem innahmen hefft.
2. Dat Jodendom warrt as en vun de Weltreligionen ankeken, ofschoonst dor bloß bi 13,5 Mio. Minschen tohören doot.
3. Dat hett siene Grünn in de Historie: De christliche un de islaamsche Gloven hefft ehre Wuddeln in dat Jodendom un dat Jodendom is överhaupt de eerste Weltreligion ween.
4. Gegen dat Enne vun de Antike hefft sik jöödsche Gemeenden bit wiet över de Grenzen vun dat Röömsche Riek, bit Indien un China hen, funnen.
5. In de USA gellt siet dat 20. Jahrhunnert all Kinner mit en jöödsch Öllerndeel as Jöden.

Fragen:
1. Wat is en Staat un wat bedütt dat, wenn een Staat tosamenleggt is?
2. Wie warrt de Grenzen vun en Staat treckt un schuult?
3. Welke Elemente sünd tohopensett in en Staat un wat hefft se to doon?
4. Wat bedütt de Souveränität vun en Staat un wie kann se freewillig ingrenzt weern?
5. Wie warrt de Macht vun en Staat utöven, un welke twee grote Kategorien gifft dat dor för?

Antwoorten:
1. En Staat is de Organisatschoon, de binnen de Gemarken vun en afgrenzt Rebeet togange is un dor de Macht utöövt over de Inwahners, de in düsse Gemarken leevt.
2. De Grenzen vun en Staat warrt treckt un schuult, um sik na buten un binnen dör to setten. Dat gellt to Land, to See un ok in de Luft.
3. De Staat is tohopensett ut de Inwahnerschop, dat Staatsrebeet un de Organisatschoon vun Gesette un Politik. De Inwahnerschop besteiht ut de Unnersaten vun den Staat, dat Staatsrebeet umfaat de geograaphsche Zoon, wo en Staat siene Macht in utöven draff.
4. De Souveränität vun en Staat bedütt, dat he mit Macht un Rechte utstaffeert is, un de, wat siene Liddmaten, un sunnerlich siene Regeerung un Verwaltung angeiht, en egen unafhängig Bestahn hett. De Souveränität kann avers freewillig ingrenzt weern.
5. De Macht vun en Staat warrt utöven, um sik na buten un binnen dör to setten. Dat gifft twee grote Kategorien: de Macht, dat Tosamenleven to organiseren (Gesette) un de Macht, up sunnerliche Feller aktiv to weern (Übernimmen vun Deensten).

Fragen:
1. Wo hett dat mit de Spraken ut de indoeuropääsche Familie to doon?
2. Welke Spraken höört to de indoeuropääschen Spraken, wenn man ok Törksch, Finnisch, Eestensch, Ungaarsch un Basksch utslütt?
3. Wo hett dat mit den Albaanschen to doon?
4. Welke Dialektgruppen gifft dat bi den Albaanschen? Un wo hett dat mit de Tosk un Gheg to doon?
5. Wo hett dat mit den Armeenschen to doon?

Antwoorten:
1. De indogermaanschen Spraken sünd een grote Spraakfamilie, de mehr as 2,5 Mrd. Minschen as Modderspraak snackt un geht alle op den indoeuropääschen Oorspraak torüch.
2. Bloots Törksch, Finnisch, Eestensch, Ungaarsch, Malteesch un Basksch höört dor nich to. Ook uutstorven Spraken so as de anatoolschen oder tochaarsche Spraken tellt to de Spraakfamilie.
3. De Albaansche is – tohoop mit Greeksch un Armeensch – ene mang den indoeuropääschen Spraken, de kenen annern engen Verwandten binnen de Spraakfamilie het, man sülvststännig ut den Oorindoeuropääschen ranwussen is. Na verschedene Ansichten stammt dat Albaansche vun den illyrschen Spraken af.
4. De Albaansche deelt sik in de grote Dialektgruppen Gheg in’n Noorden vun Albanien un in’n Süden Tosk. De Shkumbin-Stroom is de Grenz twüschen beiden. Bavento givt dat den Dialekt arberesh, op dat italieensch halveiland un arvantikia in Grekenland.
5. De Armeensche is eer egen Telg binnen dat Indoeuropääsche, man hebbt ok vele iraansche Leenwöör nahmen. Dat armeensche Luudsystemm het sik stark wannelt, so dat verwandte Wöör bloot swaar wedder to kennen sünd.

Fragen:
1. Wo is Petrus ut Galiläa kamen un wo hett he Jesus beropen?
2. Wat hett Petrus to’n eersten Mol seggt, wenn Jesus em vörherseggt harr?
3. Woneem is Petrus bi den Hogen Raat upstahn un wat hett he dor seggt?
4. Wo is Petrus na Pingsten stahn un wat hett he denn maakt?
5. Wat meent Paulus mit, dat Petrus nich länger mit de Heiden an en Disch sitten woll?

Antwoorten:
1. Simon Petrus stamm ut Galiläa un is dor as Jünger to Jesus kamen.
2. „Un wenn ik mit di starven scholl, losseggen vun di do ik mi nich!“
3. He weer nich mehr bange vör den Dood un bekenn vör den Hogen Raat sien Gloven an Jesus Christus.
4. Na Pingsten hett he sik vun den Hilligen Geist föhren laten as en Mischonar un en Föhrer vun de Uurgemeende.
5. Paulus meent, dat Petrus nich länger mit de Heiden an en Disch sitten woll, wat he vördem avers maakt harr, weens, dat he sik in de „Wohrheit vun dat Evangelium“ wannelt harr."""


formatted_data = format_data(text)

# Convert to JSON (optional)
json_output = json.dumps(formatted_data, indent=2, ensure_ascii=False)  # Use ensure_ascii=False for Unicode characters

# Print the JSON output or use formatted_data as a Python list of dictionaries
print(json_output)