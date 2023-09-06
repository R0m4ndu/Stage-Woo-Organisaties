from Scripts.xpath_functions import xpath_TOOI, xpath, xpath_adres, xpath_naam
from datetime import datetime
import json
import xml.etree.ElementTree as ET
import os
from collections import Counter

from Scripts.tll_functions import zbo_dict, oorg_dict, create_tll_files


def create_organisatie_json(organisatie, namespaces):
    
    ministeries = {
        'Algemene Zaken': 'mnre1010',
        'Binnenlandse Zaken en Koninkrijksrelaties': 'mnre1034',
        'Buitenlandse Zaken': 'mnre1013',
        'Defensie': 'mnre1018',
        'Economische Zaken en Klimaat': 'mnre1045',
        'Financiën': 'mnre1090',
        'Infrastructuur en Waterstaat': 'mnre1130',
        'Justitie en Veiligheid': 'mnre1058',
        'Landbouw, Natuur en Voedselkwaliteit': 'mnre1153',
        'Onderwijs, Cultuur en Wetenschap': 'mnre1109',
        'Sociale Zaken en Werkgelegenheid': 'mnre1073',
        'Volksgezondheid, Welzijn en Sport': 'mnre1025',
    }
    
    
    foi_bezoekadres = xpath_adres(organisatie, namespaces, 'Bezoek')
    foi_postadres = xpath_adres(organisatie, namespaces, 'Post')
    
    foaf_phone = xpath(organisatie, 'p:contact/p:telefoonnummers/p:telefoonnummer/p:nummer', namespaces)

    foaf_mbox = xpath(organisatie, 'p:contact/p:emailadressen/p:emailadres/p:email', namespaces)
    
    foi_fax = xpath(organisatie, 'p:contact/p:fax', namespaces)
    
    foi_lastUpdate = xpath(organisatie, 'p:datumMutatie', namespaces)
    
    dc_publisher = xpath_TOOI(organisatie, './p:identificatiecodes/p:resourceIdentifier[@p:naam="resourceIdentifierTOOI"]', namespaces) 
        
    dc_publisher_name = xpath(organisatie, 'p:naam', namespaces)
    
    afkorting = xpath(organisatie, 'p:afkorting', namespaces)
    
    foi_typeOfAdviescollege = xpath(organisatie, 'p:soortAdviescollege', namespaces)
    
    foi_typeOfZbo = xpath(organisatie, 'p:soortZbo', namespaces)
    
    mini = xpath(organisatie, 'p:relatieMetMinisterie', namespaces)
    
    if mini != '':
        foi_relatieMetMinisterie = f'nl.{ministeries[mini]}'
    else:
        foi_relatieMetMinisterie = mini

    
    foi_hoortBijGemeenschappelijkeRegeling = xpath(organisatie, 'p:hoortBijGemeenschappelijkeRegeling', namespaces)

    website_txt = xpath(organisatie, './/p:contact/p:internetadressen/p:internetadres/p:url', namespaces)
    
    contact_txt = xpath(organisatie, './/p:contact/p:contactpaginas/p:contactpagina/p:url', namespaces)

    Type = xpath(organisatie, 'p:types/p:type', namespaces)
    
    foi_retrievedDate = datetime.today().strftime('%Y-%m-%d')

    dc_date_year = foi_retrievedDate[:4]
    
    foi_startDate = xpath(organisatie, 'p:startDatum', namespaces)
    
    foi_endDate = xpath(organisatie, 'p:eindDatum', namespaces)
    
    if Type.lower() in dc_publisher_name.lower():
        bereikbaarheidsgegevens = f"Bereikbaarheidsgegevens van {dc_publisher_name}"
    else:
        bereikbaarheidsgegevens = f"Bereikbaarheidsgegevens van {Type} {dc_publisher_name}"
    
    if foi_endDate == "":
    
        Dict = {
            'dc_identifier': f"nl.{dc_publisher}",
            'dc_title': f"{Type} - {dc_publisher_name}",
            'dc_publisher': dc_publisher,
            'dc_type': Type,
            'dc_description': bereikbaarheidsgegevens, 
            'dc_source': "https://organisaties.overheid.nl/archive/exportOO.xml",
            'dc_creator': "Ramon Duursma",
            'foi_retrievedDate': foi_retrievedDate,
            'dc_date_year': dc_date_year,
            'dc_publisher_name': dc_publisher_name,
            'dc_publisher_afkorting': afkorting,
            'foi_website': website_txt,
            'foi_contactpagina': contact_txt,
            'foaf_mbox': foaf_mbox,
            'foaf_phone': foaf_phone,
            'foi_bezoekadres': foi_bezoekadres,
            'foi_postadres': foi_postadres,
            'foi_fax': foi_fax,
            'foi_linkedin': '',
            'foi_twitter': '',
            'foi_wikipedia':'',
            'foi_Woo_URL': '',
            'foi_startDate': foi_startDate,
            'foi_endDate': foi_endDate,
            'foi_lastUpdate': foi_lastUpdate,
            'foi_soortZBO': foi_typeOfZbo,
            'foi_soortAdviescollege': foi_typeOfAdviescollege,
            'foi_relatieMetMinisterie': foi_relatieMetMinisterie,
            'foi_hoortBijGemeenschappelijkeRegeling': foi_hoortBijGemeenschappelijkeRegeling,
            'Social_Media_Bool': False,
            'foi_files': [],
        }

        return Dict
    else:
        return ''
    


def json_alle_organisaties(tree, namespaces):
    org_dict = {}
    
    Types = []
    TOOIs = []
    
    count = 0
    
    # Verkrijg alle organisatie elementen (gemeenten, waterschappen etc.)
    organisatie_elements = tree.findall(f'.//p:organisaties/p:organisatie', namespaces)
    
    for organisatie  in organisatie_elements:
        
        Type = xpath(organisatie, 'p:types/p:type', namespaces)
        
        Dict = create_organisatie_json(organisatie, namespaces)
        
        if Dict != '' and Type != 'Organisatieonderdeel':
            org_dict[count] = Dict
            Types.append(Type)
            count+=1

    
    final_dict = {'infobox':
                    {
                        'foi_totalDossiers': count,
                        'foi_dossiers': org_dict,
                    }
                 }
        
    
    Json = json.dumps(final_dict, indent=4)
    
    return final_dict





def create_organisations(tree, namespaces):
    all_orgs = json_alle_organisaties(tree, namespaces)

    tl_file = create_tll_files()

    ZBOs = zbo_dict()
    OORGs = oorg_dict()
    
    Dictionary = {**ZBOs, **OORGs}
    Dictionary = {key.lower(): value for key, value in Dictionary.items()}

    for k, v in all_orgs['infobox']['foi_dossiers'].items():
        if v['dc_publisher_name'].lower() in Dictionary and v['dc_publisher'] == '':

            all_orgs['infobox']['foi_dossiers'][k]['dc_publisher'] = Dictionary[v['dc_publisher_name'].lower()]
            all_orgs['infobox']['foi_dossiers'][k]['dc_identifier'] = f"nl.{Dictionary[v['dc_publisher_name'].lower()]}"
            
            
    dc_publishers_new = [dossier["dc_publisher"] for dossier in all_orgs["infobox"]["foi_dossiers"].values()]
    
    print(f"Newest Version: {len(dc_publishers_new)}")
    
    
    if os.path.exists(f"Files/Json/Organisaties/alle_organisaties.json"):
        all_orgs_final = dict()
        with open(f"Files/Json/Organisaties/alle_organisaties.json", "r") as file:
            old_version = json.load(file)
            
            dc_publisher_names_old = [dossier["dc_publisher_name"].lower() for dossier in old_version["infobox"]["foi_dossiers"].values()]
            print(f"Older Version: {len(dc_publisher_names_old)}")
           
           
             
            count = 0
            for k,v in old_version['infobox']['foi_dossiers'].items():
                if v['dc_publisher'] in dc_publishers_new:
                    all_orgs_final[count] = v
                    count+=1
                    
                else:
                    pass
                
           
            for k,v in all_orgs['infobox']['foi_dossiers'].items():
                if v['dc_publisher_name'].lower() not in dc_publisher_names_old:
                    all_orgs_final[count] = v
                    count+=1
                    
                    
                
        final_dict = {'infobox':
                    {
                        'foi_totalDossiers': len(all_orgs_final),
                        'foi_dossiers': all_orgs_final,
                    }
                 }
            
        Json = json.dumps(final_dict, indent=4)
    
    else:
        Json = json.dumps(all_orgs, indent=4)
        
    with open(f"Files/Json/Organisaties/alle_organisaties.json", "w") as file:
        file.write(Json)
        
    return Dictionary