# Commentaar ORI ibabs verslag Ramon

* marx, 2023-12-13

Heel erg goed Ramon! Veel dank. Je hebt weer een aantal rake observaties, en een hoop uitgedokterd.

Natuurlijk heb ik wat vragen en opmerkingen. Komen ze

1. In het stukje **API** bespreek je de 2 objecten "reports en meetings". Heel nuttig. Maar in de uitleg eeronder leg je met behup van ibabs uit wat een rapport nou is of kan zijn. Maar die meetings en reports zijn toch objecten in ORI? Dus breder dan ibabs? **RD: Het is natuurlijk eigenlijk inderdaad een ORI object, maar daar hebben ze volgens mij gewoon de naam van Ibabs overgenomen, maar ik zeg wel gewoon ORI zodat het sowieso goed is.** 
2. Je schrijft bij nadelen: 
    3. *Bij de meetings ontbreekt vaak echter wel een identifier dat het mogelijk maakt om de agenda terug te vinden op de website. Als deze ontbreekt is een agenda eigenlijk redelijk onbruikbaar.*
    4. Kan je hier een voorbeeld van geven, en liefst ook tellingen wanneer wel en wanneer niet. 
    5. En is het zo dat dat gerelateerd is aan een "provider"? Dus bijvoorbeeld bij ibabs nooit of juist altijd, etc?
    5. Is het onbruikbaar omdat we dan niet vanuit Woogle naar die agenda kunnen **verwijzen**? bedoel je dat?
       **RD: ja hier moet ik ook nog wat nader onderzoek over uitvoeren, dit zou ook nog in mijn agenda kopje komen, dus zodra ik die aanvul hoop ik hier ook duidelijkheid over te kunnen geven**
3. Het stuk over ibabs en Hoorn en Utrecht is heel helder.

### Analyse alle Rapporten

1. Hier ga je denk ik weer naar de ORI API. **RD: Dat klopt inderdaad**
2. Mijn vfragen
    3. Je hebt het over 107 gemeentes. Zitten er evenveel gemenetes in de API als op de website? **RD: De 107 gemeenten zijn alle gemeenten met minstens 1 rapport in de API. En alleen de gemeenten die een TOOI code hebben (er zitten bijvoorbeeld ook veel oude gemeenten in die al niet meer waar ik dus ook niet de rapporten van verzamel)**
    4. Kan je een argument geven dat je **alle rapporteren die in ORI zitten** nu ook hebt opghaald? En dus ook alle attachments die daarbij horen?

**RD: Bij organisaties met minder dan 10.000 items verzamel ik altijd ALLES dus is het onmogelijk dat ik rapporten mis. Bij organisaties met meer dan 10.000 items verzamel ik eerst ALLE attachments (mediaobjecten) en daaruit verzamel ik alle rapporten waar die bijhoren want ze hebben een ispartof attribuut dus hiermee kan ik niet verzekeren dus de enige manier waarop ik een rapport zou kunnen missen is als deze of geen mediaobjecten heeft of dat er een fout is in de API waar een mediaobject die wel bij een rapport hoort geen of geen juiste ispartof relatie heeft, maar dit zou wel in gaan tegen het hele principe van de API. Maar ik kan het niet garanderen want er zitten wel wat fouten in de API.**
    5. Die analyse over de 262 verschilende termen voor rapporten zie ik heel erg graag!!! Probeer ze te clusteren door te normalisren en extra text weg te gooien. Voor **Woogle** hebben we natuurlijk die genormaliseerde termen nodig.
    6. En ja, hoe zit het nu met de agendas en de besluitenlijsten? En ook met de koppeling die je beschrijft. Want in het begin zeg je dat rapporten (bijv een motie) vaak gekoppeld zijn aan een agenda, en wel aan een agendapunt. **RD: Ja maar er bestaat eigenlijk geen koppeling tussen de rapporten en agenda's dit zijn twee verschillende losstaande objecten. Bij de ene organisatie zijn de moties dus rapporten en bij de ander zijn het weer agendapunten en er is vast ook een mix mogelijk. Maar je moet het echt zien als losstaande dingen!**
    7. We zouden die koppeling natuurlijk heel graag in Woogle opnemen. **Ook als er geen directe plek op het web is voor die agendas!!** Jij hebt ze dan wel??

**RD: De koppeling is vooral tussen de agenda's en agendapunten met de bijbehorende objecten niet echt tussen de rapporten en de agenda's denk ik.**

    
### Ibabs crawl

1. Ik mis daar nog wat over.
2. Jij had toch een lijst van die urls
3. Of zit daar per gemeente nog handwerk bij? 
4. We hebben ook 7 of 11 ibabs waterschappen meen ik. En vast ook een paar provincies. 
5. Schrijf in ieder geval kort op wat er voor nodig is om alle ibabs websites apart, dus naast de ORI API, te crawlen. **Want dat is toch wat je in het begin zegt: dat dit heel nutiig zou zijn, omdat je dan veel meer informatie kunt pakken.**

**RD: Dit is allemaal makkelijk aan te passen en uit te leggen: We kunnen inderdaad met een bepaalde API query een lijst van alle organisaties krijgen. We hebben inderdaad flink wat andere ibabs organisaties, maar deze zijn dus nog niet te vinden in de API. Bij de provincies is dat vreemd want ze zijn wel te vinden op de website (maar dus niet in de API, wat ik niet begrijp). Eigenlijk kan je alle ibabs pagina's op exact dezelfde manier scrapen, maar daarvoor zijn wel al die url's nodig die ik bij de rapporten eigenlijk altijd al netjes heb. Eigenlijk zou ik ORI aanraden om meer ibabs organisaties te verzamelen ook gewoon van de waterschappen en missende provincies (en deze in de API te gooien zodat ze ons werk een stuk makkelijker maken) oh ja en de missende urls waar ze ook mogen missen aanvullen want dat mag echt niet ontbreken wat mij betreft.**
