from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import json
import pandas as pd
import sys
import pickle

with open('data/config.json') as config:
    config = json.load(config)

season = int(sys.argv[1])
fromRace = int(sys.argv[2])
toRace = int(sys.argv[3])

driver = webdriver.Firefox()
driver.implicitly_wait(1)
driver.get('https://www.gpro.net/gb/RaceAnalysis.asp')
while driver.current_url != 'https://www.gpro.net/gb/RaceAnalysis.asp':
    pass

for race in range(fromRace, toRace + 1):
    driver.get(f'https://www.gpro.net/gb/RaceAnalysis.asp?SR={season},{race}')
    pd.read_html(driver.page_source)
    print(pd)

