#!/usr/bin/env python
from selenium import webdriver
#import pdb; pdb.set_trace()
keyWords=['Catalonia','Puigdemont']


def run_browser(headless=True,site='http://hvper.com'):
    options = webdriver.ChromeOptions()
    options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    if headless: options.add_argument('headless')
    options.add_argument('window-size=600x400')
    driver=webdriver.Chrome(chrome_options=options)
    driver.get(site)
    return driver

def act_on_link(link):
    print ("["+link.text+"]("+link.get_attribute("href")+")")
    print ()

driver = run_browser()

for word in keyWords:
    links = driver.find_elements_by_xpath("//a[@href]")
    linksTrobats = [ link for link in links if any(word in link.text for word in keyWords)]
    [act_on_link(link) for link in linksTrobats ]

#driver.quit()
