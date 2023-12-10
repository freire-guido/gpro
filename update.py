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
    soup_tables = BeautifulSoup(driver.page_source, "lxml").find_all('table')
    for name, index in config['tables'].items():
        dir = f'data/{season}/{race}_{name}'
        os.makedirs(os.path.dirname(dir), exist_ok = True)
        pd.read_html(str(soup_tables[index]))[0].to_pickle(dir)

def set_header(df, row):
    df.columns = df.iloc[row]
    df.drop(df.index[:(row+1)], inplace = True)
    return df

for table in config['tables']:
    if table == 'practice':
        header = 1
    elif table == 'setup':
        header = 0
    else:
        header = None
    races = [file.split('_')[0] for file in os.listdir(f'data/{season}') if file.split('_')[1] == 'laps']
    if header != None:
        dfs = [set_header(pd.read_pickle(f'data/{season}/{file}'), header)
               for file in os.listdir(f'data/{season}') if file.split('_')[1] == table]
    else:
        dfs = [pd.read_pickle(f'data/{season}/{file}')
               for file in os.listdir(f'data/{season}') if file.split('_')[1] == table]

    pd.concat(dfs, keys = races).to_pickle(f'data/{season}/merge_{table}')