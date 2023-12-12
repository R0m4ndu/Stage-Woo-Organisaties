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

Hoewel de documentatie van deze API redelijk beperkt was en veel referenties naar onderdelen van de documentatie bestonden ook niet meer is het toch gelukt om deze API werkend te krijgen zodat deze bruikbaar wordt voor Woogle. Op deze API staan allerlei objecten van verschillende soorten. Voor woogle zijn vooral de attachments (MediaObjects) interessant want dit zijn de documenten met een bodytext waar naar gezocht kan worden. Al deze attachments horen eigenlijk bij twee andere soorten objecten. Dat zijn de Reports en de Meetings. Dit zijn grotere objecten die vaak meerdere attachments kunnen bevatten. Door eerst metadata van de rapporten te verzamelen en daarna pas de metadata van de bijbehorende attachments kan volledig worden voldaan aan de structuur van Woogle. Wat ook altijd een dossier is met bijbehorende files. 

Maar wat zijn deze rapporten en meetings nou eigenlijk? De rapporten is een term die Ibabs gebruikt voor alle opgeslagen voor alle items op de [overzichten pagina](https://hoorn.bestuurlijkeinformatie.nl/Reports). Zoals ook op deze webpagina te zien hebben deze rapporten verschillende functies, ook wel de classificaties genoemd. Dit kunnen gewoon belangrijke documenten zijn, maar dus ook de standaard items die verwacht mogen worden bij een gemeenteraad zoals vragen, moties en besluitenlijsten. De Meetings zijn een stuk makkelijker uit te leggen. Dit zijn gewoon alle vergaderingen onderverdeeld in agendapunten en ieder agendapunt heeft zijn eigen bijbehorende documenten. 

### Nadelen van de API
Hoewel het natuurlijk fantastisch is dat deze API bestaat zijn er toch nog wel een aantal nadelen te vinden.
- Het maximaal aantal hits op deze API is 10.000 dus als er meer documenten zijn dan is er een omweg nodig om alsnog alles te verzamelen.
- Hoewel een aantal provincies al wel staan op de website van Open Raadsinformatie zijn deze nog niet beschikbaar in de API. Op dit moment zijn het dus alleen gemeenten.
- Alle mediaobjecten die machineleesbaar zijn hebben een attribuut voor bodytext, maar in veel gevallen is het document niet-machineleesbaar en dat betekent dat voor gebruik op Woogle alsnog OCR moet plaatsvinden op veel documenten en dat kost tijd.
- De hoeveelheid metadata vooral bij rapporten is in de API veel beperkter dan wat er op de Ibabs website te vinden is. Vaak staat op de website heel veel nuttige informatie zoals de indieners, de portefeuillehouder, het onderwerp, datums en vaak nog veel meer. Terwijl de metadata in de API eigenlijk altijd beperkt is tot een publicatiedatum, een titel, een classificatie en soms een omschrijving. Bij de meetings is dit vaak wel een stuk beter.
- Bij de meetings ontbreekt vaak echter wel een identifier dat het mogelijk maakt om de agenda terug te vinden op de website. Als deze ontbreekt is een agenda eigenlijk redelijk onbruikbaar.

### Ibabs Analyse
Dit vierde nadeel is wellicht het meest interessant om te onderzoeken. Omdat de structuur van Ibabs eigenlijk voor iedere organisatie hetzelfde is zal het niet moeilijk zijn om al deze webpagina's van de rapporten te scrapen. Op deze manier wordt er een indicatie gegeven van welke metadata wordt misgelopen in de API. Op deze manier leren we ook hoe deze rapporten worden ingevuld. Kunnen medewerkers zelf kiezen wat ze invullen of zijn hier gestandaardiseerde termen voor? Door dit te doen voor twee verschillende gemeenten Hoorn en Utrecht kunnen ook verschillen worden waargenomen. Hoe uniform zijn deze gegevens voor verschillende gemeenten? 

Voor het verzamelen van de Ibabs gegevens zijn een aantal wel bestaande attributen niet meegenomen omdat ze niet heel interessant zijn om te verzamelen. Dat zijn het zaaknummer, het vergaderschema en de bijlagen (want deze staan gewoon met meer metadata in de API zelf). Over alle rapporten heeft de gemeente Hoorn 24 verschillende Ibabs attributen en de gemeente Utrecht slechts 18. Dit is vrij vreemd omdat de gemeente Utrecht veel meer rapporten heeft dan de gemeente Hoorn (meer dan 16.000 t.o.v 2500). Het blijkt dan ook dat de gemeente Hoorn deze attributen veel vaker invult. Een rapport bij de gemeente Hoorn heeft namelijk gemiddeld bijna 4.5 ibabs attributen per rapport. Terwijl de gemeente Utrecht het met een schamele 2 attributen per rapport moet doen (tabel 1).

|   aantal attributen |   count Utecht |   count Hoorn |
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

