from selenium import webdriver
import gptools as gp
import json, sys

season = int(sys.argv[1])
fromRace = int(sys.argv[2])
toRace = int(sys.argv[3])
with open('data/config.json') as config:
    config = json.load(config)

with webdriver.Firefox() as driver:
    gp.wait_login(driver)
    for race in range(fromRace, toRace + 1):
        gp.update_data(driver, season, race, config['tables'])
    if config['merge']:
        gp.merge_data(season, config['tables'])
    if config['tracks']:
        gp.update_tracks(driver, season)