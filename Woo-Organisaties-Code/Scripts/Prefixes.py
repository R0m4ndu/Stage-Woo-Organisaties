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