#!/usr/bin/env python
from selenium import webdriver
keyWords=['Catalonia','Puigdemont']
options = webdriver.ChromeOptions()
options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
options.add_argument('headless')
options.add_argument('window-size=600x400')
driver=webdriver.Chrome(chrome_options=options)
driver.get('http://hvper.com')
def act_on_link(link):
    print ("["+link.text+"]("+link.get_attribute("href")+")")
    print ()
for word in keyWords:
    links = driver.find_elements_by_xpath("//a[@href]")
    [ act_on_link(link) for link in links if any(word in link.text for word in keyWords)]


#driver.quit()
