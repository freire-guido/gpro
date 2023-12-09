from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import json
import pandas as pd
import sys, os
import pickle

season = int(sys.argv[1])
fromRace = int(sys.argv[2])
toRace = int(sys.argv[3])
with open('data/config.json') as config:
    config = json.load(config)

driver = webdriver.Firefox()
driver.implicitly_wait(1)
driver.get('https://www.gpro.net/gb/RaceAnalysis.asp')
while driver.current_url != 'https://www.gpro.net/gb/RaceAnalysis.asp':
    pass

for race in range(fromRace, toRace + 1):
    driver.get(f'https://www.gpro.net/gb/RaceAnalysis.asp?SR={season},{race}')
    soup_tables = BeautifulSoup(driver.page_source).find_all('table')
    for table in config['tables']:
        dir = f'data/{season}/{race}_{table}'
        os.makedirs(os.path.dirname(dir), exist_ok = True)
        pd.read_html(str(soup_tables[table]))[0].to_pickle(dir)
