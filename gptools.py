from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os

def set_header(df, row):
    df.columns = df.iloc[row]
    df.drop(df.index[:(row+1)], inplace = True)
    return df

class GPDriver:
    def __init__(self, config, season):
        self.config = config
        self.season = season
        self.driver = webdriver.Firefox()
        print('Waiting for login...')
        self.driver.get('https://www.gpro.net/gb/RaceAnalysis.asp')
        while self.driver.current_url != 'https://www.gpro.net/gb/RaceAnalysis.asp':
            pass
        print('Logged in')

    def update_data(self, race):
        self.driver.get(f'https://www.gpro.net/gb/RaceAnalysis.asp?SR={self.season},{race}')
        soup_tables = BeautifulSoup(self.driver.page_source, "lxml").find_all('table')
        for name, index in self.config['tables'].items():
            dir = f'data/{self.season}/{race}_{name}'
            os.makedirs(os.path.dirname(dir), exist_ok = True)
            pd.read_html(str(soup_tables[index]))[0].to_pickle(dir)
        print(f'Updated race {race}')

    def update_races(self, races):
        for race in races:
            self.update_data(race)
        print(f'All races updated')

    def update_tracks(self):
        self.driver.get('https://www.gpro.net/gb/ViewTracks.asp?mode=calendar')
        soup_tables = BeautifulSoup(self.driver.page_source, "lxml").find_all('table')
        pd.read_html(str(soup_tables[0]))[0].to_pickle(f'data/{self.season}/tracks')
        print('Updated tracks')

    def merge_data(self):
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

            races = [file.split('_')[0] for file in os.listdir(f'data/{self.season}') if file.split('_')[1] == 'laps' and file.split('_')[0] != 'merge']
            if header != None:
                dfs = [set_header(pd.read_pickle(f'data/{self.season}/{race}_{table}'), header) for race in races]
            else:
                dfs = [pd.read_pickle(f'data/{self.season}/{race}_{table}') for race in races]
            pd.concat(dfs, keys = races).to_pickle(f'data/{self.season}/merge_{table}')
        print('Data merged')