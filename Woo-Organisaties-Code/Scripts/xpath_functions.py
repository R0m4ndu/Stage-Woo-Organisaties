import xml.etree.ElementTree as ET

import re

from Scripts.Prefixes import strip_titles_from_name

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
        if name_without_prefix[1] != ".":
            foaf_initials = ""
            foaf_firstName = ""
            foaf_lastName = ""
            prefixes = ""
            
    if foaf_lastName != "" and foaf_firstName == "" and foaf_initials == "" and prefixes == "":
        foaf_lastName = ""
        
    return foaf_initials, foaf_firstName, foaf_lastName, name_without_prefix, prefixes
