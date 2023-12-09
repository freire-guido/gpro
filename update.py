from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json

with open('data/config.json') as config:
    config = json.load(config)

driver = webdriver.Firefox()
driver.implicitly_wait(1)

driver.get('https://www.gpro.net/gb/RaceAnalysis.asp?')
driver.find_element(By.NAME, 'textLogin').send_keys(config['username'])
driver.find_element(By.NAME, 'textPassword').send_keys(config['password'])
print('tf')
driver.find_element(By.NAME, 'LogonFake').click()
