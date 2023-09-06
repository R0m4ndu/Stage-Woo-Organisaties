from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from rdflib import Graph, URIRef
import requests


def create_tll_files():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    for t in ['zbo_compleet','overige_overheidsorganisaties_compleet']:

        url = f"https://standaarden.overheid.nl/tooi/waardelijsten/work?work_uri=https%3A%2F%2Fidentifier.overheid.nl%2Ftooi%2Fset%2Frwc_{t}"

        driver.get(url)

        element = driver.find_element(By.CLASS_NAME, "align-center")

        URL = element.find_element(By.TAG_NAME, 'a').get_attribute('href')

        driver.get(URL)

        elements = driver.find_elements(By.TAG_NAME, "a")

        for element in elements:
            if element.text == 'TTL':
                download_file = element.get_attribute('href')

        response = requests.get(download_file)
        with open(f"Files/TTL/{t}.ttl", "wb") as file:
            file.write(response.content)


def zbo_dict():

    t = 'zbo_compleet'
    
    g = Graph()
    
    g.parse(f'Files/TTL/{t}.ttl', format='turtle')

    # Get the sorted list of triples
    sorted_triples = sorted(g, key=lambda triple: triple)


    ZBO = dict()
    # Iterate over the sorted triples and print them
    for subj, pred, obj in sorted_triples:
        if pred == URIRef('http://www.w3.org/2000/01/rdf-schema#label'):
            code = subj.split('/')[-1]
            ZBO[str(obj)] = code
            
    return ZBO
    
def oorg_dict():
    t = 'overige_overheidsorganisaties_compleet'
    
    g = Graph()
    
    g.parse(f'Files/TTL/{t}.ttl', format='turtle')

    # Get the sorted list of triples
    sorted_triples = sorted(g, key=lambda triple: triple)


    OORG = dict()
    # Iterate over the sorted triples and print them
    for subj, pred, obj in sorted_triples:
        if pred == URIRef('http://www.w3.org/2000/01/rdf-schema#label'):
            code = subj.split('/')[-1]
            OORG[str(obj)] = code
            
    return OORG

    