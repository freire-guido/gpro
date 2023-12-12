from bs4 import BeautifulSoup
from selenium import webdriver

import pandas as pd
import os

def wait_login(driver):
    driver.implicitly_wait(1)
    driver.get('https://www.gpro.net/gb/RaceAnalysis.asp')
    while driver.current_url != 'https://www.gpro.net/gb/RaceAnalysis.asp':
        pass
    return True

def update_data(driver, season, race, tables):
    driver.get(f'https://www.gpro.net/gb/RaceAnalysis.asp?SR={season},{race}')
    soup_tables = BeautifulSoup(driver.page_source, "lxml").find_all('table')
    for name, index in tables.items():
        dir = f'data/{season}/{race}_{name}'
        os.makedirs(os.path.dirname(dir), exist_ok = True)
        pd.read_html(str(soup_tables[index]))[0].to_pickle(dir)

def set_header(df, row):
    df.columns = df.iloc[row]
    df.drop(df.index[:(row+1)], inplace = True)
    return df

def merge_data(season, tables):
    for table in tables:
        if table == 'practice':
            header = 1
        elif table == 'laps':
            header = 0
        elif table == 'setup':
            header = 0
        else:
            header = None
        races = [file.split('_')[0] for file in os.listdir(f'data/{season}') if file.split('_')[1] == 'laps' and file.split('_')[0] != 'merge']
        if header != None:
            dfs = [set_header(pd.read_pickle(f'data/{season}/{race}_{table}'), header) for race in races]
        else:
            dfs = [pd.read_pickle(f'data/{season}/{race}_{table}') for race in races]
        pd.concat(dfs, keys = races).to_pickle(f'data/{season}/merge_{table}')