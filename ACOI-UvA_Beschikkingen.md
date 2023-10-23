# ACOI-UvA_Beschikkingen

____

* marx
* 2023-10-23
* Doel: afstemming metingen met Ramon

____


### Beschikkingen

1. Van welke soorten bestuursorganen zijn die er op zoek officiele bekendmakingen?
    2. waterschap
    3. provincie
    4. gemeente
    5. ???
6. Ramon haalt ze op naar Woogle, en maakt crawlers. (eind oktober)

### Transformator

* Van overheid XML metadata formaat naar dat van Woogle (eind oktober)


### Analyse

1. Doe voor elk attribuut in onze json
    2. Geef de naam
    3. Geef de source XML element naam in de source XML
    4. Geef een voorbeeld
    5. Geef missing data, liefst groupby organsiatie sort
        6. `beslisdf.groupby('dc_publisher_zonder de getallen').dc_title_isnull().mean()` zoiets 
        7. Groepeer ook eens er extra per jaar bij, om te zien of het beter wordt (dus minder missing).
    7. Voor de geo-data, kijk je even wat zinvol is, allicht
        8. of het er is
        9. het soort (point/adres, line, aantal.weet ik het)
        10. je hoeft niet heel precies te kijken hoe vaak een huisnummer etc. 
10. Voor de externe documenten:
    11. wie (welk bestuursrogaan dus) doet dat, sinds wanneer?
    12. en voor wie het doen, hoeveel missing data? (dus bschikkingen zonder externe docs)
    13. hoeveel van die docs dan per bescjikking, (.describe())
    14. wat voor bestandsformaten kom je tegen (plus telingen)
    15. aantal paginas totaal .describe()
16. Voor het XML document (dat dus ook in PDF is)
    17. "Hoe informatief is het?"
        18. Voor zover ik het zie zijn er 2 soorten
            19. zo'n aankondiging waarin niet veel meer dstaat dan in de titel, en dat je dan naar het gemeetehuis kan komen om de stukken in te zien.
            20. echt iets met veel meer infromatie zoals <https://zoek.officielebekendmakingen.nl//wsb-2023-9505.xml>
        21. **Kan je een simpele classifier maken die deze 2 aardig accuraat uit elkaar kan halen?**
    22. "Hoe rijk aan tekst en opmaak is het?"
        23. Tel aantal woorden
        24. Tel aantal tags per tagsoort.
            25. Je kan ze ook groeperen, die tags, allicht zie je dat in het schema terug. 
        25. **Toegankelijkheidsfouten** Misschien "tel verkeerd gebruik": bijv in bovenstaand XML wordt `<al>
<nadruk type="vet">Contact</nadruk>
</al>` gebruikt vor een tussenkopje (had dus een `h` element moeten zijn).
            * Trouwens, hier ook een opssoming die niet als lijst is weergegeven: `<al>De volgende bestanden maken deel uit van het besluit tot leggerwijziging LEGGER2023-D-14:</al>
<al>- DMS#2212889 – Partiële leggerwijziging LEGGER2023-D-14; en</al>
<al>- DMS#2212446 – Leggerwijzigingsdatabase LEGGER2023-D-14.</al>
<al/>` maar het wel wil zijn, en ook zo gedrukt wordt. 
    1. Is het XML valide mbt zijn schema (zoals gespecificeert in `xsi:noNamespaceSchemaLocation`).
        2. Dat vogel je uit met `xmllint` `$ xmllint --noout --schema my.xsd my.xml.` zo makkelijk. 
