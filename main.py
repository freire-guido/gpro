from gptools import GPDriver
from preprocessing import clean
import json, sys, os

mode = sys.argv[1]
with open('data/config.json') as config:
    config = json.load(config)

driver = GPDriver(config)

if mode != "quali":
    season = int(mode)
    fromRace = int(sys.argv[2])
    toRace = int(sys.argv[3])
    print(f'Season {season}')
    driver.update_races(season, range(fromRace, toRace + 1))
    if config['merge']:
        driver.merge_data(season)
        os.makedirs(os.path.dirname(f'clean/{season}/'), exist_ok = True)
        for table in config['tables']:
            if table in clean.keys():
                clean[table](f'data/{season}/merge_{table}', f'clean/{season}/{table}')
    if config['tracks']:
        driver.update_tracks(season)
        if config['merge']:
            clean['tracks'](f'data/{season}/tracks', f'clean/{season}/tracks')
    print('Success')

else:
    print('Qualifying')
    driver.update_qualifying()
    print('Success')