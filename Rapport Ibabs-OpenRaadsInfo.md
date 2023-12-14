Stagerapport: Openraadsinformatie + Ibabs

Naam: Ramon Duursma
UvANetID: 12851779

## Open Raadsinformatie

Een van de informatiecategorieën met verplichte actieve openbaarmaking door de Wet Open Overheid (Woo) is "vergaderstukken en verslagen van provinciale staten, gemeenteraden en algemene besturen van waterschappen, 
algemene besturen van openbare lichamen, besturen van bedrijfsvoeringsorganisaties en gemeenschappelijke organen als bedoeld in de Wet gemeenschappelijke regelingen en hun commissies". Verder in dit verslag zal gebruik
worden gemaakt van een kortere term namelijk raadsstukken. 

Deze raadsstukken zijn eigenlijk alle documenten die gebruikt worden tijdens de vergaderingen van het bestuur van alle verschillende overheidsorganisaties. Hierbij kan men denken aan ingezonden brieven, raadsvragen,
maar ook bijvoorbeeld besluitenlijsten en zo zijn er nog veel meer soorten documenten die hier onder vallen. Deze documenten worden over het algemeen verzameld op het bestuurslijke informatie deel van de website van de organisatie. 

Om al deze raadsstukken overzichtelijk te krijgen en zo dus de besluitvorming van gemeenten transparanter te maken bestaat er een eigen initiatief van de Vereniging Nederlandse Gemeenten (VNG). Dit initiatief heet 
Open Raadsinformatie en dit is eigenlijk een API dat het voor geinteresseerde mogelijk maakt om zelf door al deze raadsstukken heen te zoeken of deze raadsstukken te gebruiken voor hun eigen applicatie. Dit tweede is wat ik heb 
gedaan tijdens deze periode en zal dus ook voor een groot deel zijn waar mijn verslag overgaat. 

### Woogle

Woogle is dus die "eigen applicatie" waar deze API precies voor van toepassing zou kunnen zijn. Woogle is namelijk een zoekmachine voor alle informatiecategorieën die onder de Woo vallen. Hier horen de raadsstukken 
natuurlijk ook bij en het zou dus fijn zijn als deze API gebruikt kan worden voor het verzamelen van al deze raadsstukken voor Woogle. 

### API

Hoewel de documentatie van deze API redelijk beperkt was en veel referenties naar onderdelen van de documentatie bestonden ook niet meer is het toch gelukt om deze API werkend te krijgen zodat deze bruikbaar wordt voor Woogle. Op deze API staan allerlei objecten van verschillende soorten. Voor woogle zijn vooral de attachments (MediaObjects) interessant want dit zijn de documenten met een bodytext waar naar gezocht kan worden. Al deze attachments horen eigenlijk bij twee andere soorten objecten. Dat zijn de Reports en de Meetings. Dit zijn grotere objecten die vaak meerdere attachments kunnen bevatten. Door eerst metadata van de rapporten te verzamelen en daarna pas de metadata van de bijbehorende attachments kan volledig worden voldaan aan de structuur van Woogle. Wat ook altijd een dossier is met bijbehorende files. Om aan de identifiers van alle organisaties te komen kan men een speciale query uitvoeren, waarna de resultaten een lijst van alle identifiers zijn. Op basis van deze lijst van identifiers kan er met een andere speciale query gecontroleerd worden hoeveel items er precies in de API zijn voor deze organisatie. Vervolgens kan voor ieder item in de lijst metadata van rapporten en agenda's worden verzameld.

Maar wat zijn deze rapporten en meetings nou eigenlijk? De rapporten is een term die Ibabs gebruikt voor alle opgeslagen voor alle items op de [overzichten pagina](https://hoorn.bestuurlijkeinformatie.nl/Reports). Zoals ook op deze webpagina te zien hebben deze rapporten verschillende functies, ook wel de classificaties genoemd. Dit kunnen gewoon belangrijke documenten zijn, maar dus ook de standaard items die verwacht mogen worden bij een gemeenteraad zoals vragen, moties en besluitenlijsten. De Meetings zijn een stuk makkelijker uit te leggen. Dit zijn gewoon alle Notubiz vergaderingen onderverdeeld in agendapunten en ieder agendapunt heeft zijn eigen bijbehorende documenten. 

### Nadelen van de API
Hoewel het natuurlijk fantastisch is dat deze API bestaat zijn er toch nog wel een aantal nadelen te vinden.
- Het maximaal aantal hits op deze API is 10.000 dus als er meer documenten zijn dan is er een omweg nodig om alsnog alles te verzamelen.
- Hoewel een aantal provincies al wel staan op de website van Open Raadsinformatie zijn deze nog niet beschikbaar in de API. Op dit moment zijn het dus alleen gemeenten.
- Alle mediaobjecten die machineleesbaar zijn hebben een attribuut voor bodytext, maar in veel gevallen is het document niet-machineleesbaar en dat betekent dat voor gebruik op Woogle alsnog OCR moet plaatsvinden op veel documenten en dat kost tijd.
- De hoeveelheid metadata vooral bij rapporten is in de API veel beperkter dan wat er op de Ibabs website te vinden is. Vaak staat op de website heel veel nuttige informatie zoals de indieners, de portefeuillehouder, het onderwerp, datums en vaak nog veel meer. Terwijl de metadata in de API eigenlijk altijd beperkt is tot een publicatiedatum, een titel, een classificatie en soms een omschrijving. Bij de meetings is dit vaak wel een stuk beter.
- De identifier om een agenda of rapport terug te vinden op de website bestaat in verschillende formaten. Dit is afhankelijk van het soort platform dat gebruikt wordt en in bepaalde gevallen werkt dit zelfs helemaal niet. Hiermee wordt het laatste deel van een url als deze ([https://hoorn.bestuurlijkeinformatie.nl/Reports/Item//f8f94938-ce1a-4353-85bb-cec31dac8bf2](https://hoorn.bestuurlijkeinformatie.nl/Reports/Item//f8f94938-ce1a-4353-85bb-cec31dac8bf2)) of deze ([https://zaanstad.notubiz.nl/vergadering/436378](https://zaanstad.notubiz.nl/vergadering/436378)) bedoeld. Dit zijn de twee standaardformaten voor de ibabs rapporten en de notubiz agenda's. Soms is dit echter in een ander formaat waarvan de rest van de URL eigenlijk ontraceerbaar is.

### Ibabs Analyse
Dit vierde nadeel is wellicht het meest interessant om te onderzoeken. Omdat de structuur van Ibabs eigenlijk voor iedere organisatie hetzelfde is zal het niet moeilijk zijn om al deze webpagina's van de rapporten te scrapen. Op deze manier wordt er een indicatie gegeven van welke metadata wordt misgelopen in de API. Op deze manier leren we ook hoe deze rapporten worden ingevuld. Kunnen medewerkers zelf kiezen wat ze invullen of zijn hier gestandaardiseerde termen voor? Door dit te doen voor twee verschillende gemeenten Hoorn en Utrecht kunnen ook verschillen worden waargenomen. Hoe uniform zijn deze gegevens voor verschillende gemeenten? 

Voor het verzamelen van de Ibabs gegevens zijn een aantal wel bestaande attributen niet meegenomen omdat ze niet heel interessant zijn om te verzamelen. Dat zijn het zaaknummer, het vergaderschema en de bijlagen (want deze staan gewoon met meer metadata in de API zelf). Over alle rapporten heeft de gemeente Hoorn 24 verschillende Ibabs attributen en de gemeente Utrecht slechts 18. Dit is vrij vreemd omdat de gemeente Utrecht veel meer rapporten heeft dan de gemeente Hoorn (meer dan 16.000 t.o.v 2500). Het blijkt dan ook dat de gemeente Hoorn deze attributen veel vaker invult. Een rapport bij de gemeente Hoorn heeft namelijk gemiddeld bijna 4.5 ibabs attributen per rapport. Terwijl de gemeente Utrecht het met een schamele 2 attributen per rapport moet doen (tabel 1).

|   attributen |   count Utecht |   count Hoorn |
|----------------------:|----------------:|----------------:|
|                   0 |            4823 |            357  |
|                   1 |            2167 |            368  |
|                   2 |            5047 |            124  |
|                   3 |             944 |            119  |
|                   4 |            1145 |             93  |
|                   5 |             304 |            225  |
|                   6 |            1621 |            307  |
|                   7 |             114 |            550  |
|                   8 |              96 |            229  |
|                   9 |              35 |             78  |
|                  10 |              15 |             35  |
|                  11 |               4 |              4  |
|                  12 |             0 |              1  |

** Tabel 1: Het aantal keer dat een rapport een bepaald aantal attributen heeft bij de gemeenten Utrecht (N = 16315) en Hoorn (N = 2490) **

Het is echter zeer aannemelijk dat het aantal attributen afhangt van het type rapport waar deze aan toebehoort. Het is bijvoorbeeld aannemelijk dat een motie veel meer metadata heeft dan een besluitenlijst. Bij de motie zijn er vaak indieners en allerlei datums terwijl een besluitenlijst toch vaak een besluitenlijst is. In eerste instantie moeten we hiervoor weten wat voor soort rapporten beiden organisaties hebben. 

| Rapport Typen Utrecht               |   aantal |   attributen per rapport |
|:----------------------------------|---------:|-------------:|
| Raadsbrieven                     |    8426 |         1.30 |
| Schriftelijke vragen             |    3989 |         4.93 |
| RSS                              |    1390 |         0.02 |
| Memo's                           |     945 |         1.78 |
| Verslagen M&S                    |     576 |         0.00 |
| Verslagen S&R                    |     406 |         0.00 |
| Verslagen Vragenuur              |     233 |         1.82 |
| Besluitenlijst B&W               |     191 |         0.01 |
| Archief                          |      59 |         0.15 |
| Vragen Coronavirus               |      51 |         3.00 |
| Export                           |      30 |         2.23 |
| Referendumcommissie              |      10 |         0.00 |
| Coalitievorming 2022             |       5 |         0.00 |
| Geheimhoudingsregister            |       4 |         0.75 |

** Tabel 2: Gemiddeld aantal attributen per type rapport voor de gemeente Utrecht **

| Rapport Typen Hoorn               |   aantal |   attributen per rapport |
|:----------------------------------|---------:|-------------:|
| Moties                           |     651 |         6.14 |
| RSS                              |     450 |         3.94 |
| Toezeggingen                     |     365 |         6.82 |
| Artikel 36 vragen                |     349 |         7.14 |
| Ingekomen stukken - College      |     326 |         1.06 |
| Besluitenlijst B&W               |     309 |         0.00 |
| Financiële documenten            |      35 |         0.14 |
| Verordeningen Raad en Commissies |       5 |         0.00 |

** Tabel 3: Gemiddeld aantal attributen per type rapport voor de gemeente Hoorn **

Als eerste blijkt het dat de rapport typen niet heel erg goed overeenkomen. Eigenlijk zijn er maar twee hetzelfde, dat zijn de besluitenlijst B&W en de RSS attributen. Verder zijn er ook grote verschillen in de aantallen. Bij Utrecht zijn de aantallen niet heel evenredig verdeeld. Er zijn heel veel Raadsbrieven en Schrijftelijke vragen, maar hierna zijn er een aantal attributen met redelijk aantal, maar er zijn nog meer soorten Rapporten met minder dan 100 items. Bij Hoorn zijn de aantallen een stuk evenrediger verdeeld er zijn van alle documenten ongeveer evenveel, op een aantal na. De hypothese dat bepaalde soorten rapporten meer ibabs attributen hebben wordt hiermee bevestigd besluitenlijsten hebben namelijk (quasi) nooit attributen terwijl moties er bij Hoorn gemiddeld meer dan zes hebben. Het valt op dat bij Utrecht eigenlijk alleen de Schrijftelijke vragen een gemiddeld vergelijkbaar aantal attributen heeft dan het gemiddelde van Hoorn. Er blijken hier dus op alle fronten grote verschillen te zijn tussen Utrecht en Hoorn. 

Maar welke ibabs attributen hebben deze organisaties eigenlijk? Eerder was al genoemd dat Hoorn en 24 had en Utrecht slechts 18. Hiervan blijken er X overeen te komen, dat zijn: Gerelateerde items, Portefeuillehouder, Afgedaan, Deadline, Omschrijving, Onderwerp, Datum beantwoording en Opmerking. 

| ibabs_column                            |   aantal |
|:------------------------------------------|---------:|
| ibabs_Gerelateerde items                 |       90 |
| ibabs_Toelichting                        |      576 |
| ibabs_Partijen                           |     1431 |
| ibabs_Portefeuillehouder                 |     1357 |
| ibabs_Status                             |      631 |
| ibabs_Afgedaan                           |     1349 |
| ibabs_Agendapunt                         |      977 |
| ibabs_Domein                             |      226 |
| ibabs_Stemmen                            |      363 |
| ibabs_Stand van zaken                    |      443 |
| ibabs_Datum afgedaan                     |      276 |
| ibabs_Medewerker                         |      366 |
| ibabs_Deadline                           |       82 |
| ibabs_Afzender                           |      324 |
| ibabs_Omschrijving                       |        1 |
| ibabs_Onderwerp                          |        9 |
| ibabs_Datum uiterlijke beantwoording    |      521 |
| ibabs_Steller                            |      506 |
| ibabs_Datum B&W                          |      162 |
| ibabs_Datum beantwoording                |      605 |
| ibabs_Opmerking                          |       17 |
| ibabs_Datum tussenbericht                |       80 |
| ibabs_Datum ingekomen                    |      348 |
| ibabs_Toezegging                         |      362 |

** Tabel 4: Het aantal rapporten met een bepaald ibabs attribuut bij de gemeente Hoorn **

In tabel 4 is te zien hoe vaak bepaalde ibabs items voorkomen bij de gemeente Hoorn. Aangezien Hoorn in totaal bijna 2500 rapporten heeft blijkt al gelijk dat het grootste deel van de attributen niet veelvuldig voorkomen. Het attribuut omschrijving komt bijvoorbeeld slechts 1 keer voor. Eigenlijk zijn er maar drie attributen die bij meer dan de helft van de rapporten voorkomen. Dit is natuurlijk te verklaren door het feit dat er ook veel rapporten zijn zonder attributen. 

| ibabs_column               |   aantal |
|:-----------------------------|---------:|
| ibabs_Kenmerk                |     3929 |
| ibabs_Indiener(s)            |     3951 |
| ibabs_Mede-indieners         |       91 |
| ibabs_Onderwerp              |       78 |
| ibabs_Beleidsveld            |     7311 |
| ibabs_Portefeuillehouder     |    10513 |
| ibabs_Deadline               |       66 |
| ibabs_Datum beantwoording    |     1527 |
| ibabs_Afgedaan               |      126 |
| ibabs_Relatie met            |       77 |
| ibabs_Thema                  |     3672 |
| ibabs_Datum invoer           |        3 |
| ibabs_Gerelateerde items     |      109 |
| ibabs_Opmerking              |      357 |
| ibabs_Datum wijziging        |      729 |
| ibabs_Omschrijving           |      234 |
| ibabs_Opmerkingen            |        9 |
| ibabs_Inhoud                 |      212 |

** Tabel 5: Het aantal rapporten met een bepaald ibabs attribuut bij de gemeente Utrecht **

Uit tabel 5 blijkt dat de attributen bij Utrecht nog veel minder voorkomen er zijn namelijk bijna 16000 rapporten en eigenlijk alleen portefeuillehouder en beleidsveld komen hier redelijk vaak voor. Terwijl er nog drie andere attributen zijn die in ongeveer een kwart van de rapporten voorkomen. Verder zijn er ook veel attributen die minder dan 500 keer voorkomen. Dit is bij 11 van de 18 (61%) van de attributen zo. 

# Analyse alle Rapporten

Uiteindelijk zijn de rapporten van alle gemeenten uit de API verzameld. Hierbij horen de volgende statistieken. Van in totaal 107 gemeenten zijn rapporten verzameld. 
Dit zijn eigenlijk alle gemeenten met minstens één rapport met minstens één bijlage, dit is zeker het geval omdat bij de organisaties met minder dan 10.000 items elk document is verzameld en bij de organisaties met meer dan 10.000 items eerst alle bijlagen zijn verzameld en vervolgens uit de metadata van de bijlagen de identifiers van de rapporten zijn verzameld. Zodoende hebben we een lijst van de identifiers van alle rapporten met minstens één bijlage en worden hiermee ook alle rapporten verzameld. Een andere vereiste van deze gemeenten is dat deze een eigen [TOOI code](https://standaarden.overheid.nl/tooi/waardelijsten/expression?lijst_uri=https%3A%2F%2Fidentifier.overheid.nl%2Ftooi%2Fset%2Frwc_gemeenten_compleet%2F3) hebben en dat deze gemeente nog steeds bestaat. Dit zijn in totaal 158.378 rapporten met 251.185 verschillende documenten. Samen hebben deze 1.601.812 pagina's. 

Tot slot is er nogmaals een analyse gedaan over het type rapport, maar nu voor al deze gemeenten. Het blijkt dat er in totaal 262 verschillende soorten termen worden gebruikt om deze rapporten te classificeren. Dit is dus niet heel uniform. Zo worden er bijvoorbeeld veel verschillende termen gebruikt voor dezelfde soort documenten:

TODO: analyse voor vergelijkbare termen voor bijvoorbeeld besluitenlijsten moties etc. Zoals in de scriptie van Maik.

TODO: Wellicht nog een subkopje over de agenda's. 

# Conclusie

Allereerst is het duidelijk dat de ori API een waardevolle toevoeging is voor de Woogle, want het geeft veel overheidsdocumeten voor een tot op heden nauwelijks verzamelde informatiesoort. Het is verder volkomen begrijpelijk waarom gekozen is voor het schrappen van veel van de metadata die wel op de website te vinden is. Deze metadata is nauwelijks uniform en zal daarom waarschijnlijk verschillen van organisatie tot organisatie en dat komt de herbruikbaarheid zeker niet ten goede, terwijl dat natuurlijk juist het streven was van die hele API. Deze slechte uniformiteit is ook aanwezig voor de verschillende typen rapporten, maar deze zijn typen zijn wel noodzakelijk. Naast het gebrek aan uniformiteit was bij alleen al Hoorn en Utrecht ook al een groot verschil te zien in de hoeveelheid ibabs metadata bij de rapporten. De gemeente Hoorn vulde deze veel vaker in en de verschillen tussen de typen rapporten waren hierbij zoals verwacht er groot. 

Het grootste nadeel van de ORI api is eigenlijk nog wel het gebrek aan een grote hoeveelheid informatie. Er zijn namelijk nog een stuk meer organisaties die het standaard ibabs of notubiz model gebruiken. Denk hierbij aan de gemeenten die nog niet op de API te vinden zijn maar wel in de zoekmachine, maar ook aan de meeste waterschappen en vast nog een stuk meer andere gemeenten. 
