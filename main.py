from gptools import GPDriver
import json, sys

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
    if config['tracks']:
        driver.update_tracks(season)
    print('Success')

else:
    print('Qualifying')
    driver.update_qualifying()
    print('Success')