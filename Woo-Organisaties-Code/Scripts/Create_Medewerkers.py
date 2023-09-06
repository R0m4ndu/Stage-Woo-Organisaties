import xml.etree.ElementTree as ET
from datetime import datetime
import json
import os
from collections import Counter

from Scripts.xpath_functions import xpath, xpath_adres, xpath_TOOI, xpath_naam

def json_create_single_layer(organisatie_type, tree, namespaces, OORG_ZBO_Dict):
    
    list_of_dicts = []

    # Verzamel datum en jaar
    foi_retrievedDate = datetime.today().strftime('%Y-%m-%d')
    dc_date_year = foi_retrievedDate[:4]

    # Verkrijg alle organisatie elementen bij dit type
    organisatie_elements = tree.findall(f'.//p:organisaties/p:organisatie/[p:types = "{organisatie_type}"]', namespaces)
    
    # loop over deze elementen en verzamel gegevens
    for organisatie in organisatie_elements:

        # Verzamel nodige data over organisaties
        dc_publisher = xpath_TOOI(organisatie, './/p:identificatiecodes/p:resourceIdentifier[@p:naam="resourceIdentifierTOOI"]', namespaces) 
        dc_publisher_name = xpath(organisatie, 'p:naam', namespaces)
        website_txt = xpath(organisatie, './/p:contact/p:internetadressen/p:internetadres/p:url', namespaces)
        Type = xpath(organisatie, 'p:types/p:type', namespaces)
        foi_endDate = xpath(organisatie, 'p:eindDatum', namespaces)
        
        if dc_publisher == '':
            if dc_publisher_name.lower() in OORG_ZBO_Dict:
                dc_publisher = OORG_ZBO_Dict[dc_publisher_name.lower()]
        
        # vind alle functies
        functie_element = organisatie.findall('p:functies/p:functie', namespaces)

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
                if organisatie_type == 'Waterschap':
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
            
            # als er een TOOI bekend is wordt de medewerker toegevoegd. 
            if DICT != {}:
            
                # uiteindelijk hoeft de dict van alle medewerkers alleen maar toegevoegd te worden aan de volledige dict.
                final_dict = {'resource': f"nl.{dc_publisher}.{foaf_function_type}.{dc_date_year}",
                            'infobox': {'foi_totalDossiers': len(DICT),
                                         'foi_dossiers': DICT}}


                list_of_dicts.append(final_dict)
                
    number_of_people = sum(i['infobox']['foi_totalDossiers'] for i in list_of_dicts)
        
    return number_of_people, list_of_dicts







def json_create_multi_layer(organisatie_type, tree, namespaces, OORG_ZBO_Dict):
    
    list_of_dicts = []
    
    # Verzamel datum en jaar
    foi_retrievedDate = datetime.today().strftime('%Y-%m-%d')
    dc_date_year = foi_retrievedDate[:4]

    # Verkrijg alle organisatie elementen bij dit type
    organisatie_elements = tree.findall(f'.//p:organisaties/p:organisatie/[p:types = "{organisatie_type}"]', namespaces)

    # loop over deze elementen en verzamel gegevens
    for organisatie in organisatie_elements:
        
        # verzamel gegevens van de organisatie
        dc_publisher = xpath_TOOI(organisatie, './/p:identificatiecodes/p:resourceIdentifier[@p:naam="resourceIdentifierTOOI"]', namespaces) 
        dc_publisher_name = xpath(organisatie, 'p:naam', namespaces)
        website_txt = xpath(organisatie, './/p:contact/p:internetadressen/p:internetadres/p:url''p:types/p:type', namespaces)
        Type = xpath(organisatie, 'p:types/p:type', namespaces)
        foi_endDate1 = xpath(organisatie, 'p:eindDatum', namespaces)
        organisatie_elements2 = organisatie.findall('.//p:organisaties/p:organisatie', namespaces)
        
        if dc_publisher == '':
            if dc_publisher_name.lower() in OORG_ZBO_Dict:
                dc_publisher = OORG_ZBO_Dict[dc_publisher_name.lower()]
        
        for organisatie2 in organisatie_elements2:
            
            organisatie_naam = xpath(organisatie2, 'p:naam', namespaces)
        
            # vind alle functies
            functie_element = organisatie2.findall('p:functies/p:functie', namespaces)

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
                    foi_endDate2 = xpath(organisatie, 'p:eindDatum', namespaces)
                    foi_startDate = xpath(medewerker, 'p:startDatum', namespaces)
                    foaf_phone = xpath(medewerker, 'p:contact/p:telefoonnummers/p:telefoonnummer/p:nummer', namespaces)
                    foaf_mbox = xpath(medewerker, 'p:contact/p:emailadressen/p:emailadres/p:email', namespaces)
                    foi_Woo_URL = xpath(medewerker, 'p:contact/p:internetadressen/p:internetadres/p:url', namespaces)
                    foi_bezoekadres = xpath_adres(medewerker, namespaces, 'Bezoek')
                    foi_postadres = xpath_adres(medewerker, namespaces, 'Post')


                    # genereer beschikbaarheidsgegevens
                    if organisatie_type != 'Provincies':
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
                            'foi_party': organisatie_naam,
                            'foi_function': foaf_function_type,
                            'foi_files': [] ,
                        }


                    # indien de organisaties nog bestaan voeg deze toe
                    if foi_endDate1 == '' and foi_endDate2 == '' and dc_publisher != '':
            
                    
                        resource = f"nl.{dc_publisher}.{foaf_function_type}.{dc_date_year}"

                        resources = [d['resource'] for d in list_of_dicts]

                        if resource in resources:
                            for c,d in enumerate(list_of_dicts):
                                if d['resource'] == resource:
                                    index = c

                            total = list_of_dicts[index]['infobox']['foi_totalDossiers']

                            list_of_dicts[index]['infobox']['foi_dossiers'][total+1] = Dict
                            list_of_dicts[index]['infobox']['foi_totalDossiers'] += 1


                        else:
                            final_dict = {'resource': f"nl.{dc_publisher}.{foaf_function_type}.{dc_date_year}",
                                        'infobox': {'foi_totalDossiers': 1,
                                                     'foi_dossiers': {"0":Dict}}}


                            list_of_dicts.append(final_dict)

    number_of_people = sum(i['infobox']['foi_totalDossiers'] for i in list_of_dicts)
        
    return number_of_people, list_of_dicts



def remove_fractievoorzitters():
    if (os.path.exists(f"Files/Json/Medewerkers/Personen/Gemeente.json")) == False:
        return None

    with open(f"Files/Json/Medewerkers/Personen/Gemeente.json", "r") as file:
        json_data = json.load(file)
        
    number_of_people_before = sum(i['infobox']['foi_totalDossiers'] for i in json_data)

    for count, dct in enumerate(json_data):

        if 'Fractievoorzitter' in dct['resource']:
            titles = []
            for k, v in dct['infobox']['foi_dossiers'].items():

                titles.append(f"{v['foi_title']} {v['dc_title']} {v['foi_party']}")

        if 'Raadslid' in dct['resource']:

            counter = 0
            new_raadslid = dict()

            for k, v in dct['infobox']['foi_dossiers'].items():
                if f"{v['foi_title']} {v['dc_title']} {v['foi_party']}" not in titles:
                    v['dc_identifier'] = f"{dct['resource']}.{counter}"
                    new_raadslid[counter] = v
                    counter+=1


            final_dict = {'resource': dct['resource'],
                                'infobox': {'foi_totalDossiers': counter,
                                             'foi_dossiers': new_raadslid}}

            json_data[count] = final_dict


    number_of_people_after = sum(i['infobox']['foi_totalDossiers'] for i in json_data)

    Json = json.dumps(json_data, indent=4)

    with open(f"Files/Json/Medewerkers/Personen/gemeente.json", "w") as file:
            file.write(Json)

    return number_of_people_before, number_of_people_after



def create_org_social_media(Organisatie):
    ### Because the gathering of (social) media might take a while create a separate dict just for this.
    if os.path.exists(f"Files/Json/Medewerkers/Social Media/Social_Media_{Organisatie}.json"):
    
        with open(f"Files/Json/Medewerkers/Social Media/Social_Media_{Organisatie}.json", "r") as file:
            social_media_dict = json.load(file)
            people_in_dict = list(social_media_dict.keys())
           
    
    else:
        social_media_dict = dict()
        people_in_dict = []
        
    if (os.path.exists(f"Files/Json/Medewerkers/Personen/{Organisatie}.json")) == False:
        return None

    with open(f"Files/Json/Medewerkers/Personen/{Organisatie}.json", "r") as file:
        dict_list = json.load(file)
    
    for p in dict_list:
        persons_per_func = p['infobox']['foi_dossiers']
        for k, v in persons_per_func.items():
            Identifier = f"{v['foaf_name']} {v['dc_publisher_name']} {v['foi_function']}"
            
            if Identifier not in people_in_dict:
                person_dict = {
                                  'foaf_name': v['foaf_name'],
                                  'foaf_function_type': v['foi_function'],
                                  'dc_publisher_name': v['dc_publisher_name'],
                                  'foaf_firstName': v['foaf_firstName'],
                                  'foaf_lastName': v['foaf_lastName'],
                                  'foaf_initials': v['foaf_initials'],
                                  'website': v['foaf_workplaceHomepage'],
                                  'foi_linkedin': '',
                                  'foi_twitter': '',
                                  'foi_wikipedia': '',
                                  'foaf_workplaceHomepage': '',
                                  'foi_party': v['foi_party'],
                                  'up_to_date': False}
            
                social_media_dict[f"{v['foaf_name']} {v['dc_publisher_name']} {v['foi_function']}"] = person_dict
    
    
    Json = json.dumps(social_media_dict, indent=4)

    # Write JSON string to a text file
    with open(f"Files/Json/Medewerkers/Social Media/Social_Media_{Organisatie}.json", "w") as file:
        file.write(Json)
        
        return 'Done'



def extract_all_medewerkers(Organisatie, tree, namespaces, OORG_ZBO_Dict, multi_layer = True):
    
    ### This section is for creating the JSON file of the organisation
    people1, dict_list = json_create_single_layer(Organisatie, tree, namespaces, OORG_ZBO_Dict)
    
    if multi_layer == True:
        people2, dict_list2 = json_create_multi_layer(Organisatie, tree, namespaces, OORG_ZBO_Dict)
    
        dict_list = dict_list + dict_list2
        
    Json = json.dumps(dict_list, indent=4)

    # Write JSON string to a text file
    with open(f"Files/Json/Medewerkers/Personen/{Organisatie}.json", "w") as file:
        file.write(Json)
        
    organisatie_elements = tree.findall(f'.//p:organisaties/p:organisatie/[p:types = "{Organisatie}"]', namespaces)
    list_of_peoples = [organisatie_element.findall('.//p:medewerker', namespaces) for organisatie_element in organisatie_elements]
    people = sum(len(lst) for lst in list_of_peoples)
            
    print(f'aantal medewerkers in XML: {people}')
    
    if multi_layer == True:
        print(f'aantal medewerkers extracted in JSON: {people1 + people2}')
    else:
        print(f'aantal medewerkers extracted in JSON: {people1}')     
          
    if Organisatie == 'Gemeente':
        
        # groepeer de fractievoorzitters die ook raadsleden zijn bij de gemeenten. 1/3 minder raadsleden hierdoor.
        before, after = remove_fractievoorzitters()
        print('')
        print('resultaten verwijderen fractievoorzitters uit de raadsleden:')
        print(f"Before: {before}")
        print(f"After: {after}")
        print(f"Less items: {before-after}")
    
    create_org_social_media(Organisatie)
    
    ### Here the check for the amount of elements gathered compared to the amount of elements in the XML tree.
    ### if multi_layer == True this will always both be equal
    
     