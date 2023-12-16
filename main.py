from selenium import webdriver
from gptools import GPDriver
import json, sys

season = int(sys.argv[1])
fromRace = int(sys.argv[2])
toRace = int(sys.argv[3])
with open('data/config.json') as config:
    config = json.load(config)

driver = GPDriver(config, season)
driver.update_races(range(fromRace, toRace + 1))
if config['merge']:
    driver.merge_data()
if config['tracks']:
    driver.update_tracks()