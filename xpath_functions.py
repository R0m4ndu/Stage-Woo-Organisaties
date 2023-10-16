import xml.etree.ElementTree as ET
import re

def remove_suffixes(name):
    
    suffixes = []
    new_name = []
    
    suffixes_end = False

    for part in name.split(' ')[::-1]:
        
        if '.' not in part and part.isupper() and suffixes_end == False or part == 'MSc':
            suffixes.append(part + ' ')
        else:
            suffixes_end = True
            new_name.append(part)
            
    
    return ' '.join(new_name[::-1]), suffixes[::-1]


def remove_prefixes(name):
    
    if 'De heer.' in name:
        name = name.replace('De heer.', 'De heer')
    
    pattern = r"(?!ij|th|ph|hr|ch|jr|sr)[a-z]{2,}\.\s?"
    prefixes = re.findall(pattern, name, flags=re.IGNORECASE)
    
    name = re.sub(pattern, '', name, flags=re.IGNORECASE).strip()
    
    if name.split(' ')[0].lower() == 'mevrouw':
        name = ' '.join(name.split(' ')[1:])
        prefixes.append('mew.')
        
    
    if ' '.join(name.split(' ')[0:2]).lower() == 'de heer':
        print
        name = ' '.join(name.split(' ')[2:])
        prefixes.append('dhr.')
    
    return name, prefixes


def remove_army_titles(name):
    
    titles = []
    new_name = []
    
    # these army titles are gathered from the ministery of defense
    army_titles = {'Generaal-majoor', 'Generaal', 'Commandeur-arts', 'Brigade-generaal', 'Commodore', 'Kapitein-ter-zee', 'Brigadegeneraal', 'Kolonel-vlieger', 'Commandeur', 'Schout-bij-nacht', 'Luitenant-kolonel', 'Cdre', 'Majoor', 'Vice-admiraal', 'Kolonel', 'Luitenant-generaal'}

    multi_word_army_titles = ['Generaal-majoor der mariniers', 'Generaal-majoor der Cavalerie', 'Luitenant-generaal der mariniers', 'Brigadegeneraal der mariniers']
    
    for Title in multi_word_army_titles:
        if Title in name:
            titles.append(Title + ' ')
            name = name.split(f'{Title} ')[1]
    
    for part in name.split(' '):
        if part in army_titles:
            titles.append(part + ' ')
        else:
            new_name.append(part)
    
    return ' '.join(new_name), titles
            


def strip_titles_from_name(name):
    """
        Tries to remove all prefixes, army titles and suffixes and from the name string
        and tries to leave the initials and the rest of the name in it's place. 
    """

    # prefixes are very common among names in the XML file
    name, prefixes = remove_prefixes(name)
    
    # Sometimes the name string may contain an army title (especially in the ministry of defense)
    name, army_title = remove_army_titles(name)
    
    # Suffixes in the XML file are always fully Capitalized except if it is MSc, these are separated from the name
    name, suffixes = remove_suffixes(name)
    
    if prefixes or suffixes or army_title:
        return prefixes + army_title + suffixes, name
    
    else:
        return '', name.strip()

def xpath(element, path, namespaces):
    obj = element.find(path, namespaces)
    
    if obj is not None:
        return obj.text
    else:
        return ''

    

def xpath_adres(element, namespaces, Type):
    
    Incomplete = False
    
    if Type == 'Bezoek':
    
        obj = element.find('p:adressen/p:adres[p:type="Bezoekadres"]', namespaces)

        if obj is not None:
            
            straat = obj.find('p:straat', namespaces)
            if straat is not None:
                straat = straat.text
            else:
                Incomplete = True
            
            huisnummer = obj.find('p:huisnummer', namespaces)
            if huisnummer is not None:
                huisnummer = huisnummer.text
            else:
                Incomplete = True
            
            postcode = obj.find('p:postcode', namespaces)
            if postcode is not None:
                postcode = postcode.text
            else:
                Incomplete = True
                
            plaats = obj.find('p:plaats', namespaces)
            if plaats is not None:
                plaats = plaats.text.title()
                
            else:
                Incomplete = True
                
            if Incomplete == True:
                return ''

            return f"{straat} {huisnummer} {postcode} {plaats}"
         
        else:
            return ''
        
    if Type == 'Post':
        
        obj = element.find('p:adressen/p:adres[p:type="Postadres"]', namespaces)
        
        if obj is not None:
            postbus = obj.find('p:postbus', namespaces)
            if postbus is not None:
                postbus = postbus.text
            else:
                Incomplete = True
            
            postcode = obj.find('p:postcode', namespaces)
            if postcode is not None:
                postcode = postcode.text
            else:
                Incomplete = True
            
            plaats = obj.find('p:plaats', namespaces)
            if plaats is not None:
                plaats = plaats.text.title()
                
            else:
                Incomplete = True
                
            if Incomplete == True:
                return ''
            

            return f"{postbus} {postcode} {plaats}"
         
        else:
            return ''
        
    else:
        return ''
    
    
    
    
    
def xpath_TOOI(element, path, namespaces):
    
    dc_publisher = element.find(path, namespaces)
    if dc_publisher is not None:
        Text = dc_publisher.text.rsplit('/')[-1]
        if Text[-1].isalpha() == True:
            return ''
        
        else:
            return Text

    else:
        return ''
    
    
    
    
def xpath_naam(element, path, namespaces, functie):
    # verzamel de naam in de XML
    initial_name = element.find(path, namespaces)
    
    initial_name_txt = initial_name.text
    
    if initial_name_txt is not None:
        
        pattern = r'\((.*?)\)'
        matches = re.findall(pattern, initial_name_txt)
        
        initial_name_txt = re.sub(pattern, '', initial_name_txt)
        if " (" in initial_name_txt:
            initial_name_txt = initial_name_txt.split(' (')[0]
        
        if '  ' in initial_name_txt:
            initial_name_txt = initial_name_txt.replace('  ', ' ')

        # er staat vaak een prefix als dr. of mew. voor deze wordt verwijderd?
        prefixes, name_without_prefix = strip_titles_from_name(initial_name_txt)
        name_without_prefix = name_without_prefix.lstrip()
        
        if '.' in name_without_prefix and '. ' not in name_without_prefix:
            name_without_prefix = name_without_prefix.replace(".", ". ")
        
        if '. ' in name_without_prefix:
            c = name_without_prefix.count('. ')
            name_without_prefix = name_without_prefix.replace(". ", ".", c-1)

        initial_name_split = name_without_prefix.split(' ', 1)

        # bij gemeenten staat er een persoon in als mew. Schouten dus zonder initialen. 
        if len(initial_name_split) == 2:
            first_word = initial_name_split[0]
            if '.' not in first_word and len(first_word) != 1:

                foaf_firstName = initial_name_split[0]
                foaf_initials = foaf_firstName[0].upper() + '.'
                
            else:
                foaf_initials = initial_name_split[0]
                foaf_firstName = ''

            foaf_lastName = initial_name_split[1]
            x = foaf_lastName.split(' ')
            if x[0] != '':
                if x[0][-1] == '.':
                    foaf_lastName = ' '.join(x[1:])
                    foaf_initials = foaf_initials + x[0]
        
        else:
            foaf_initials = ''
            foaf_firstName = ''
            foaf_lastName = initial_name_split[0]
    
    # gebeurt in de praktijk niet maar maakt het wel failproof
    else:
        foaf_initials = ''
        foaf_firstName = ''
        foaf_lastName = ''
        
    prefixes = ''.join(prefixes)
    prefixes = prefixes.rstrip()
    
    if matches != []:
        if len(matches[0].split(' ')) == 1:
            foaf_firstName = matches[0]
            
            if '.' in foaf_firstName or foaf_firstName.isupper():
                foaf_firstName = ''
        
    if foaf_firstName != '':
        name_without_prefix = foaf_firstName + ' ' + foaf_lastName
    
    if foaf_firstName in ['van', 'de']:
        
        foaf_lastName = foaf_firstName + ' ' + foaf_lastName
        foaf_firstName = ''
        
    if foaf_firstName.isupper() == True:
        foaf_initials = '.'.join(foaf_firstName)
        foaf_firstName = ''

    if functie == 'Woo-contactpersoon':

        if len(name_without_prefix) != 0:
        
            if name_without_prefix[1] != ".":
                foaf_initials = ""
                foaf_firstName = ""
                foaf_lastName = ""
                prefixes = ""
        else:
            foaf_initials = ""
            foaf_firstName = ""
            foaf_lastName = ""
            prefixes = ""
            
    if foaf_lastName != "" and foaf_firstName == "" and foaf_initials == "" and prefixes == "":
        foaf_lastName = ""
        
    return foaf_initials, foaf_firstName, foaf_lastName, name_without_prefix, prefixes
