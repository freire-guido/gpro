from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os

def set_header(df, row):
    df.columns = df.iloc[row]
    df.drop(df.index[:(row+1)], inplace = True)
    return df

class GPDriver:
    def __init__(self, config):
        self.config = config
        self.driver = webdriver.Firefox()
        print('Waiting for login...')
        self.driver.get('https://www.gpro.net/gb/RaceAnalysis.asp')
        while self.driver.current_url != 'https://www.gpro.net/gb/RaceAnalysis.asp':
            pass
        print('Logged in')

    def get_tables(self, url):
        self.driver.get(url)
        return BeautifulSoup(self.driver.page_source, "lxml").find_all('table')

    def update_data(self, season, race):
        tables = self.get_tables(f'https://www.gpro.net/gb/RaceAnalysis.asp?SR={season},{race}')
        for name, index in self.config['tables'].items():
            dir = f'data/{season}/{race}_{name}'
            os.makedirs(os.path.dirname(dir), exist_ok = True)
            pd.read_html(str(tables[index]))[0].to_pickle(dir)
        print(f'Updated race {race}')

    def update_races(self, season, races):
        for race in races:
            self.update_data(season, race)
        print(f'All races updated')

    def update_tracks(self, season):
        tables = self.get_tables('https://www.gpro.net/gb/ViewTracks.asp?mode=calendar')
        pd.read_html(str(tables[0]))[0].to_pickle(f'data/{season}/tracks')
        print('Updated tracks')

    def merge_data(self, season):
        print('Merging data')
        for table in self.config['tables']:
            if table == 'practice':
                header = 1
            elif table == 'laps':
                header = 0
            elif table == 'setup':
                header = 0
            else:
                header = None

            races = [file.split('_')[0] for file in os.listdir(f'data/{season}')
                     if file.split('_')[0] not in ['tracks', 'merge'] and file.split('_')[1] == 'laps']
            if header != None:
                dfs = [set_header(pd.read_pickle(f'data/{season}/{race}_{table}'), header) for race in races]
            else:
                dfs = [pd.read_pickle(f'data/{season}/{race}_{table}') for race in races]
            pd.concat(dfs, keys = races).to_pickle(f'data/{season}/merge_{table}')
        print('Data merged')
    
    def update_qualifying(self):
        tables = self.get_tables('https://www.gpro.net/gb/Qualify.asp')
        for name, index in self.config['quali'].items():
            dir = f'data/quali_{name}'
            os.makedirs(os.path.dirname(dir), exist_ok = True)
            if name == 'practice':
                set_header(pd.read_html(str(tables[index]))[0], 1).to_pickle(dir)
            else:
                pd.read_html(str(tables[index]))[0].to_pickle(dir)
        print('Updated qualifying')