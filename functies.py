from xpath_functions import xpath, xpath_adres, xpath_TOOI, xpath_naam

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import json
from bs4 import BeautifulSoup
from urllib.parse import unquote
    

def json_create_single_layer(tree, namespaces):
    
    list_of_dicts = []

    # Verzamel datum en jaar
    foi_retrievedDate = datetime.today().strftime('%Y-%m-%d')
    dc_date_year = foi_retrievedDate[:4]

    # Verkrijg alle organisatie elementen bij dit type
    organisatie_elements = tree.findall(f'p:organisaties/p:organisatie', namespaces)
    
    # loop over deze elementen en verzamel gegevens
    for organisatie in organisatie_elements:

        # Verzamel nodige data over organisaties
        dc_publisher = xpath_TOOI(organisatie, './/p:identificatiecodes/p:resourceIdentifier[@p:naam="resourceIdentifierTOOI"]', namespaces) 
        dc_publisher_name = xpath(organisatie, 'p:naam', namespaces)
        website_txt = xpath(organisatie, './/p:contact/p:internetadressen/p:internetadres/p:url', namespaces)
        Type = xpath(organisatie, 'p:types/p:type', namespaces)
        foi_endDate = xpath(organisatie, 'p:eindDatum', namespaces)

        
        # vind alle functies
        functie_element = organisatie.findall('.//p:functies/p:functie', namespaces)

        for functie in functie_element:

            foi_count = 0
            DICT = {}

            foaf_function_type = xpath(functie, 'p:naam', namespaces)

            # vindt alle medewerkers die bij deze functie horen
            medewerker_element = functie.findall('p:medewerkers/p:medewerker', namespaces)
            
            for medewerker in medewerker_element:
                
                # verzamel data van de medewerkers
                foi_party = xpath(medewerker, 'p:partijLidmaatschap', namespaces)
                foaf_initials, foaf_firstName, foaf_lastName, name_without_prefix, prefixes = xpath_naam(medewerker, 'p:naam', namespaces, foaf_function_type)
                foi_startDate = xpath(medewerker, 'p:startDatum', namespaces)
                foaf_phone = xpath(medewerker, 'p:contact/p:telefoonnummers/p:telefoonnummer/p:nummer', namespaces)
                foaf_mbox = xpath(medewerker, 'p:contact/p:emailadressen/p:emailadres/p:email', namespaces)
                foi_Woo_URL = xpath(medewerker, 'p:contact/p:internetadressen/p:internetadres/p:url', namespaces)
                foi_bezoekadres = xpath_adres(medewerker, namespaces, 'Bezoek')
                foi_postadres = xpath_adres(medewerker, namespaces, 'Post')
                
                if foi_Woo_URL == website_txt:
                    foi_Woo_URL = ""

                # genereer beschikbaarheidsgegevens
                if Type == 'Waterschap':
                    bereikbaarheidsgegevens = f"Bereikbaarheidsgegevens van {name_without_prefix}, {foaf_function_type} voor {Type.lower()} {dc_publisher_name}"
                else:
                    if foi_party != '':
                        bereikbaarheidsgegevens = f"Bereikbaarheidsgegevens van {name_without_prefix}, {foaf_function_type} voor {foi_party} in de {dc_publisher_name}"
                    else:
                        bereikbaarheidsgegevens = f"bereikbaarheidsgegevens van {name_without_prefix}, {foaf_function_type} voor {dc_publisher_name}"
                
                    
                # vul de dictionary in
                Dict = {
                        'dc_identifier': f"nl.{dc_publisher}.{foaf_function_type}.{dc_date_year}.{foi_count + 1}",
                        'dc_title': f"{name_without_prefix} - {dc_publisher_name}",
                        'dc_type': Type,
                        'dc_description': bereikbaarheidsgegevens,
                        'dc_source': "https://organisaties.overheid.nl/archive/exportOO.xml",
                        'dc_publisher': dc_publisher,
                        'dc_creator': "R0m4ndu",
                        'foi_retrievedDate': foi_retrievedDate,
                        'dc_date_year': dc_date_year,
                        'dc_publisher_name': dc_publisher_name,
                        'foi_title': prefixes,
                        'foaf_initials': foaf_initials,
                        'foaf_firstName': foaf_firstName,
                        'foaf_lastName': foaf_lastName,
                        'foaf_name': name_without_prefix,
                        'foaf_mbox': foaf_mbox,
                        'foaf_phone': foaf_phone,
                        'foi_visitAddress': foi_bezoekadres,
                        'foi_mailAddress': foi_postadres,
                        'foi_Woo_URL': foi_Woo_URL,
                        'foi_linkedin': '',
                        'foi_twitter': '',
                        'foi_wikipedia': '',
                        'foaf_workplaceHomepage': website_txt,
                        'foi_startDate': foi_startDate,
                        'foi_party': foi_party,
                        'foi_function': foaf_function_type,
                        'foi_files': [] ,
                    }
                
                # en voeg de dictionary toe aan als de organisatie nog bestaat
                if foi_endDate == "" and dc_publisher != "":
                
                    DICT[foi_count] = Dict

                    foi_count+=1
            


                list_of_dicts.append(Dict)
            
    return list_of_dicts


def laatste_versie_medewerkers():
    # Download de recentste versie van het export00 bestand
    xml_url = 'https://organisaties.overheid.nl/archive/exportOO.xml'
    
    # Download de XML file
    response = requests.get(xml_url)
    xml_content = response.content
    
    # Save de XML File
    with open('exportOO_full.xml', 'wb') as file:
        file.write(xml_content)
    
    # Parse de XML file
    tree = ET.parse('exportOO_full.xml')
    root = tree.getroot()
    schema = str(root.tag.split('}')[0][1:])
    
    # Bepaal de namespaces
    namespaces = {
        "p":schema
    }
    
    fd = json_create_single_layer(tree, namespaces)
    
    Json = json.dumps(fd, indent=4)
    with open(f"Bewijs.json", "w") as file:
        file.write(Json)

    return "Done"