from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
import time
from collections import Counter
import re
import json
import os
import urllib.parse
import string

def remove_punctuation(input_string):

    translator = str.maketrans('', '', string.punctuation)

    no_punct = input_string.translate(translator)
    return no_punct



def search_yahoo(Query):
    
    url = "http://search.yahoo.com/search?p=%s"
    r = requests.get(url % Query) 
    soup = BeautifulSoup(r.text, features="lxml")
    hrefs = [a['href'] for a in soup.find_all('a', href=True)]
    hrefs = [href for href in hrefs if 'yahoo' not in hrefs]

    new_hrefs = [href for href in hrefs if "yahoo" not in href and '#' not in href and 'bingj' not in href and '.pdf' not in href]
    
    return new_hrefs





def extract_urls(hrefs, site, last_name, functie = '', organisatie = ''):
    
    possible = False
    
    last_names = set()
    last_names.add(last_name)
    
    if '-' in last_name:
        parts = last_name.split('-')
        for i in parts:
            last_names.add(i)
            last_names.add(unidecode(i))
            
    if ' ' in last_name:
        last_names.add(last_name.replace(' ', ''))
        last_names.add(last_name.replace(' ', '-'))
        last_names.add(last_name.replace(' ', '_'))
        last_names.add(last_name.replace(' ', '+'))
        
    if site in ['twitter.com', 'nl.linkedin.com', 'nl.wikipedia.org']:
        for href in hrefs[:5]:
            
            href_copy = href
            href = href.lower()
            if 'bingj' in href:
                continue

            if site == 'nl.linkedin.com':
                if '/in/' not in href_copy:
                    continue

            if site == 'nl.wikipedia.org':
                if '/wiki/' not in href:
                    continue

            if site == 'twitter.com':
                if '/status' in href or '/hashtag' in href:
                    continue
                    
            for ln in last_names:
                if ln.lower() in href:
                    if site in href:
                        
                        if site == 'nl.wikipedia.org':
                            return href_copy
                    
                        return href
    
    if site not in ['twitter.com', 'nl.linkedin.com', 'nl.wikipedia.org']:

        possibilities = [url for url in hrefs[:10] for ln in last_names if ln.lower() in url]
        possibilities2 = [url for url in hrefs[:10] if functie.lower() in url]
        pos = set(possibilities).union(set(possibilities2))

        pos = [p for p in pos if not 'nieuws' in p and not 'news' in p]

        if pos != []:  
            ws = min(pos, key=len)
            if not '.pdf' in ws:
                return ws


        p = [h for h in hrefs if 'dagelijks-bestuur' in h.lower()]

        if len(p) == 1:
            return p[0]

        elif len(p) > 1:
            p2 = [i for i in p if 'leden' in i or 'overzicht' in i or 'samenstelling' in i]
            if len(p2) == 1:
                return p2[0]

            elif len(p2) > 1:
                return ws

    return ''




def find_firstName(hrefs, last_name, initials, double_check, double_check2):
    
    if double_check == False:
        treshold = 1
    else:
        treshold = 0
        
    if initials == '':
        return ''
    
        
    
    initials = initials.replace('.','').lower()

    last_name = last_name.lower()
    
    last_names = set()
    last_names.add(last_name)
    last_names.add(unidecode(last_name))

    if ' ' in last_name:
        last_names.add(last_name.replace(' ', ''))
        last_names.add(last_name.replace(' ', '-'))
        last_names.add(last_name.replace(' ', '_'))
        last_names.add(last_name.replace(' ', '+'))
    
    possible_firstNames = []
    wrong_names = []
    
    for href in hrefs:

        href = href.lower()
        href = href.split('/')
        for part in href:
            found_last_names = [last_name for last_name in last_names if last_name in part]
            if found_last_names:
                part = part.split(found_last_names[0])[0]
                part = re.split(r"[-_]", part)
                part = [p for p in part if p != '']
                if len(part) > 0:
                    if part[-1][0] == initials[0]:
                        possible_firstNames.append(part[-1])
                    else:
                        wrong_names.append(part[-1])
                        if len(part) > 1:
                            if part[-2][0] == initials[0]:
                                possible_firstNames.append(part[-2] + '-' + part[-1])
                    
                    
    
    names = [naam for naam in possible_firstNames if any(letter in 'aeiouy' for letter in naam) and len(naam) > 1]

    names_with_dash = {name.replace('-', ''): name for name in names if '-' in name}
    names = [names_with_dash.get(name, name) for name in names]
    
    names = [name for name in names if re.sub(r'[^\w\s]', '', name) != initials]
    
    if names != []:
        first_option = Counter(names).most_common(1)
        if first_option[0][1] > treshold:
            name = first_option[0][0]
            if '-' in name:
                names = name.split('-')
                names = [n for n in names if len(n) > 1 and n not in ['van', 'de']]
                name = "-".join(names)
            
            return name.title()
        
    if double_check2 == True:
        if len(wrong_names) > 0:
            return wrong_names[0]
        
    return ''




def update_social_media(Organisatie):
    
    if (os.path.exists(f"Files/Json/Medewerkers/Social Media/Social_Media_{Organisatie}.json")) == False:
        return None
    
    with open(f"Files/Json/Medewerkers/Social Media/Social_Media_{Organisatie}.json", "r") as file:
        json_data = json.load(file)
        
    all_empty_count = 0
    
    for k, v in json_data.items():
        
        if v["up_to_date"] == False and v['foaf_lastName'] != '':
            
            if Organisatie != 'Hoog College van Staat':
                query = f'"{v["foaf_name"]}" {v["dc_publisher_name"]} {v["foaf_function_type"]} {Organisatie}'

            else: 
                query = f'"{v["foaf_name"]}" {v["dc_publisher_name"]} {v["foaf_function_type"]}'
                
                
            print(query)
                

            linkedin_hrefs = search_yahoo('site:nl.linkedin.com ' + query)
            if linkedin_hrefs == []:
                linkedin_hrefs = search_yahoo('linkedin ' + query)

            foi_linkedin = extract_urls(linkedin_hrefs, 'nl.linkedin.com', v['foaf_lastName'])


            twitter_hrefs = search_yahoo('site:twitter.com ' + query)

            foi_twitter = extract_urls(twitter_hrefs,'twitter.com', v['foaf_lastName'], '', Organisatie)

            wikipedia_hrefs = search_yahoo('site:nl.wikipedia.org ' + query)

            foi_wikipedia = extract_urls(wikipedia_hrefs, 'nl.wikipedia.org',v['foaf_lastName'])
            
            all_empty = all(not lst for lst in [linkedin_hrefs, twitter_hrefs, wikipedia_hrefs])
            if all_empty:
                all_empty_count+=1
                if all_empty_count == 2:
                    json_data[k]['up_to_date'] = False
                    print('Yahoo Cooldown')
                    break
                
            if not all_empty:
                all_empty_count = 0

            if v['foaf_firstName'] == '':
                query = f'"{v["foaf_name"]}" {v["dc_publisher_name"]} {v["foaf_function_type"]}'
                hrefs = search_yahoo(query)
                foaf_firstName = find_firstName(hrefs, v['foaf_lastName'], v['foaf_initials'], False, False)
                json_data[k]['foaf_firstName'] = foaf_firstName
                
            json_data[k]['foi_linkedin'] = foi_linkedin
            json_data[k]['foi_twitter'] = foi_twitter
            json_data[k]['foi_wikipedia'] = foi_wikipedia

            # omdat ministeries altijd dezelfde website hebben is dit op een andere manier op te lossen
            if Organisatie != 'Ministerie':

                site = v['website']

                if site.startswith("http://"):
                    # Split the URL asfter "http://"
                    site = site.split("://", 1)[1]
                elif site.startswith("https://"):
                    # Split the URL after "https://"
                    site = site.split("://", 1)[1]

                website_hrefs = search_yahoo(f"site:{site} " + k)
                foi_website = extract_urls(website_hrefs, site, v['foaf_lastName'], k.split(' ')[-1])

                json_data[k]['foaf_workplaceHomepage'] = foi_website   

            json_data[k]['up_to_date'] = True
        
        
            Json = json.dumps(json_data, indent=4)

            with open(f"Files/Json/Medewerkers/Social Media/Social_Media_{Organisatie}.json", "w") as file:
                file.write(Json)
        
    return json_data



def extract_urls_orgs(hrefs, site, org_name, afkorting, org_type):
    
    orgs = set()
        
    capital_words = [word for word in re.split(r'[ -]', org_name) if (len(word) == 0 or word[0].isupper())]
    capital_words = [word for word in capital_words if word != '']
    
    # bekende organisaties gaan altijd een pagina hebben.
    if org_type in ['Ministerie', 'Provincie', 'Waterschap', 'Gemeente', 'Hoog College van Staat']:
        for cw in capital_words:
            orgs.add(cw.lower())
    
    if afkorting != '':
        orgs.add(afkorting.lower())
    else:
        abbr = [word[0] for word in capital_words]
        afkorting = ''.join(capital_words)
        orgs.add(afkorting.lower())
        
    org_name = org_name.lower()
    orgs.add(org_name)
    
    if ' ' in org_name:
        orgs.add(org_name.replace(' ', ''))
        orgs.add(org_name.replace(' ', '-'))
        orgs.add(org_name.replace(' ', '_'))
        orgs.add(org_name.replace(' ', '+'))

    if site == 'twitter.com':
        hrefs = [h.split('/status')[0] if '/status/' in h else h for h in hrefs]
    
    for href in hrefs[:1]:
    
        if site not in href:
            continue
            
        else:
            
            if site == 'nl.linkedin.com':
                if '/company/' not in href:
                    continue
        
            if site == 'twitter.com':
                if 'status' in href:
                    continue

            for o in orgs:
                if o in href.lower():
                    return href

                
        return ''
    return ''

def find_woo_adres(hrefs, site):
    
    url = hrefs[0].lower()
    
    site = site.split("//")[1]
    
    woo_woorden = ['woo', 'wet open overheid', 'wet+open+overheid', 'wet-open-overheid', 'wet_open_overheid', 'wob']
    
    if site in url:
        for w in woo_woorden:
            if w in url:
                return url
            
    
    return ''
        
    




def update_social_media_organisaties():
    
    if (os.path.exists(f"Files/Json/Organisaties/alle_organisaties.json")) == False:
        print('Organisatie File bestaat nog niet')
        return None
    
    with open(f"Files/Json/Organisaties/alle_organisaties.json", "r") as file:
        json_data = json.load(file)
    
    for k, v in json_data['infobox']['foi_dossiers'].items():
        
        if v['Social_Media_Bool'] == False and v['dc_publisher'] != '':
            query = f'{v["dc_title"]}'

            print(query)
            
            org_type = v['dc_type']

            twitter_hrefs = search_yahoo('twitter.com ' + query)
    
            foi_twitter = extract_urls_orgs(twitter_hrefs,'twitter.com', v["dc_publisher_name"], v["dc_publisher_afkorting"], org_type)

            wikipedia_hrefs = search_yahoo('nl.wikipedia.org ' + query)

            foi_wikipedia = extract_urls_orgs(wikipedia_hrefs, 'nl.wikipedia.org', v["dc_publisher_name"], v["dc_publisher_afkorting"], org_type)
            
            if v['foi_website'] != '':
            
                woo_hrefs = search_yahoo(v["foi_website"] + "woo verzoek")

                foi_Woo_URL = find_woo_adres(woo_hrefs, v["foi_website"])
                
                json_data['infobox']['foi_dossiers'][k]['foi_Woo_URL'] = foi_Woo_URL
                

            linkedin_hrefs = search_yahoo('site:nl.linkedin.com ' + query)
            if linkedin_hrefs == []:
                linkedin_hrefs = search_yahoo('linkedin ' + query)
            
            foi_linkedin = extract_urls_orgs(linkedin_hrefs, 'nl.linkedin.com', v["dc_publisher_name"], v["dc_publisher_afkorting"], org_type)
                   
            all_empty = all(not lst for lst in [linkedin_hrefs, twitter_hrefs, wikipedia_hrefs])
            if all_empty:
                print('Yahoo Cooldown')
                break
            
            
            json_data['infobox']['foi_dossiers'][k]['foi_linkedin'] = foi_linkedin
            json_data['infobox']['foi_dossiers'][k]['foi_twitter'] = foi_twitter
            json_data['infobox']['foi_dossiers'][k]['foi_wikipedia'] = foi_wikipedia
            json_data['infobox']['foi_dossiers'][k]['Social_Media_Bool'] = True
            
            Json = json.dumps(json_data, indent=4)

            with open(f"Files/Json/Organisaties/alle_organisaties.json", "w") as file:
                file.write(Json)
    
    return json_data


def double_checker(Organisatie):
    if (os.path.exists(f"Files/Json/Medewerkers/Social Media/Social_Media_{Organisatie}.json")) == False:
        return None
    
    with open(f"Files/Json/Medewerkers/Social Media/Social_Media_{Organisatie}.json", "r") as file:
        json_data = json.load(file)
        
    counter = 0
    for k, v in json_data.items():
        if v["up_to_date"] == True:
            
            HREFS = [v['foi_linkedin'], v['foi_wikipedia'], v['foi_twitter'], v['foaf_workplaceHomepage']]
            
            first_name1 = (v['foaf_firstName'])
            first_name2 = (find_firstName(HREFS, v['foaf_lastName'],v['foaf_initials'], True, False))
            
            if first_name1 != '':
                continue
            
            if first_name2 == '':
                continue
                
            else:
                foaf_firstName = urllib.parse.unquote(first_name2)
                json_data[k]['foaf_firstName'] = foaf_firstName
                counter+=1
                
        
    Json = json.dumps(json_data, indent=4)

    with open(f"Files/Json/Medewerkers/Social Media/Social_Media_{Organisatie}.json", "w") as file:
        file.write(Json)
    
    return f"{counter} names changed"




def double_checker2(Organisatie):
    if (os.path.exists(f"Files/Json/Medewerkers/Social Media/Social_Media_{Organisatie}.json")) == False:
        return None
    
    with open(f"Files/Json/Medewerkers/Social Media/Social_Media_{Organisatie}.json", "r") as file:
        json_data = json.load(file)
    
    counter = 0
    for k, v in json_data.items():
        if v["up_to_date"] == True and v['foaf_initials'] != '':
            HREFS = ['foi_linkedin', 'foi_wikipedia', 'foi_twitter', 'foaf_workplaceHomepage']
        
            
            for href_type in HREFS:
                
                href = v[href_type]
                
                if href != '':
                    first_name2 = find_firstName([href], v['foaf_lastName'],v['foaf_initials'], True, True)
                    if first_name2 != '' and v['foaf_firstName'] != '':
                        
                        FN2 = unidecode(urllib.parse.unquote(first_name2).lower())
                        FN2 = remove_punctuation(FN2)
                        first_name = unidecode(urllib.parse.unquote(v['foaf_firstName'])).lower()
                        first_name = remove_punctuation(first_name)
                        
                        if FN2 not in first_name and first_name not in FN2:
                            
                            counter +=1
                            json_data[k][href_type] = ''


    
    Json = json.dumps(json_data, indent=4)

    with open(f"Files/Json/Medewerkers/Social Media/Social_Media_{Organisatie}.json", "w") as file:
        file.write(Json)
                
    return(f"{counter} names changed")



def update_org_files(Organisatie):
    
    if (os.path.exists(f"Files/Json/Medewerkers/Personen/{Organisatie}.json")) == False:
        return None
    
    with open(f"Files/Json/Medewerkers/Personen/{Organisatie}.json", "r") as file:
        json_data = json.load(file)
        
    if (os.path.exists(f"Files/Json/Medewerkers/Social Media/Social_Media_{Organisatie}.json")) == False:
        return None
    
    with open(f"Files/Json/Medewerkers/Social Media/Social_Media_{Organisatie}.json", "r") as social_media_file:
        social_media = json.load(social_media_file)
        
    for count, data in enumerate(json_data):
        for k, v in data['infobox']['foi_dossiers'].items():
            identifier = f"{v['foaf_name']} {v['dc_publisher_name']} {v['foi_function']}"
            if identifier in social_media:
                json_data[count]['infobox']['foi_dossiers'][k]['foaf_firstName'] = social_media[identifier]['foaf_firstName']
                json_data[count]['infobox']['foi_dossiers'][k]['foi_linkedin'] = social_media[identifier]['foi_linkedin']
                json_data[count]['infobox']['foi_dossiers'][k]['foi_twitter'] = social_media[identifier]['foi_twitter']
                json_data[count]['infobox']['foi_dossiers'][k]['foi_wikipedia'] = social_media[identifier]['foi_wikipedia']
                json_data[count]['infobox']['foi_dossiers'][k]['foaf_workplaceHomepage'] = social_media[identifier]['foaf_workplaceHomepage']
                json_data[count]['infobox']['foi_dossiers'][k]['foaf_name'] = f"{social_media[identifier]['foaf_firstName']} {social_media[identifier]['foaf_lastName']}"
                    
                if social_media[identifier]['foaf_firstName'] != '':
                    json_data[count]['infobox']['foi_dossiers'][k]['dc_description'] = json_data[count]['infobox']['foi_dossiers'][k]['dc_description'].replace(social_media[identifier]['foaf_name'], f"{social_media[identifier]['foaf_firstName']} {social_media[identifier]['foaf_lastName']}")
                    json_data[count]['infobox']['foi_dossiers'][k]['dc_title'] = json_data[count]['infobox']['foi_dossiers'][k]['dc_title'].replace(social_media[identifier]['foaf_name'], f"{social_media[identifier]['foaf_firstName']} {social_media[identifier]['foaf_lastName']}")
                    
    Json = json.dumps(json_data, indent=4)

    with open(f"Files/Json/Medewerkers/Personen/{Organisatie}.json", "w") as file:
        file.write(Json)
        
    return f"Update {Organisatie} compleet"
