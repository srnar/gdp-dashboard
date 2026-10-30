import requests
import pandas as pd

# Základní URL pro API
KATALOG_URL = "https://data.csu.gov.cz/api/katalog/v1"
DOTAZ_URL = "https://data.csu.gov.cz/api/dotaz/v1"

# 1. NAJÍT SADA KÓD PRO HDP
def find_gdp_dataset():
    response = requests.get(f"{KATALOG_URL}/sady")
    sady = response.json()
    
    for sada in sady:
        nazev = sada.get("nazev", "").lower()
        if "hrubý domácí produkt" in nazev or "hdp" in nazev:
            print(f"Nalezena sada: {sada['kod']} - {sada['nazev']}")
            return sada['kod']
    return None

# 2. ZÍSKAT INFORMACE O DIMENZÍCH SADY
def get_dataset_metadata(sada_kod):
    # Získání dimenzí (časová řada, ukazatele atd.)
    response = requests.get(f"{KATALOG_URL}/sady/{sada_kod}/dimenze")
    dimenze = response.json()
    print("Dostupné dimenze:", dimenze)
    return dimenze

# 3. STÁHNOUT CELOU DATOVOU SADU (NEJEDNODUŠŠÍ CESTA)
def download_full_dataset(sada_kod):
    """
    DataStat umožňuje stáhnout kompletní datovou sadu v JSON-STAT nebo CSV.
    """
    url = f"{DOTAZ_URL}/data/sady/{sada_kod}?format=JSON_STAT"
    response = requests.get(url)
    
    if response.status_code == 200:        
        return response.json()
    else:
        print(f"Chyba při stahování: {response.status_code}")
        print(f"URL: {url}")
        return None

# --- SPUŠTĚNÍ ---
sada_kod = find_gdp_dataset()

if sada_kod:
    # Prohlédnutí metadat sady
    get_dataset_metadata(sada_kod)
    
    # Stažení kompletních dat
    data = download_full_dataset(sada_kod)
    print("Data stažena úspěšně!")
    print(data)