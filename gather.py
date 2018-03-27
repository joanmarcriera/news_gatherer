#!/usr/bin/env python
from selenium import webdriver
import argparse
#import pdb; pdb.set_trace()
keyWords=['Catalonia','Puigdemont']
file_output='../joanmarcriera.github.io/index.md'

parser = argparse.ArgumentParser()
parser.add_argument("-s", dest='site',default='http://hvper.com', help="Site to gather links from.")
parser.add_argument("-f", dest='file',default='../joanmarcriera.github.io/index.md', help="File where to add the links.")
parser.add_argument("-w", dest='words',default='Catalonia,Puidemont',help="Words to search for, comma separed")
group = parser.add_argument_group('group')
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
args = parser.parse_args()

file_output=args.file
keyWords=args.words.split(",")
site=args.site

def run_browser(headless=True,site=site):
    options = webdriver.ChromeOptions()
    options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    if headless: options.add_argument('headless')
    options.add_argument('window-size=600x400')
    driver=webdriver.Chrome(chrome_options=options)
    driver.get(site)
    return driver

def act_on_link(link,file=file_output):
    f=open(file_output,'a')
    f.write("[%s](%s)" % link.text , link.get_attribute("href"))

    print ("["+link.text+"]("+link.get_attribute("href")+")")


driver = run_browser()

for word in keyWords:
    links = driver.find_elements_by_xpath("//a[@href]")
    linksTrobats = [ link for link in links if any(word in link.text for word in keyWords)]
    linksNous = [ link for link in linksTrobats  if (link.text in open(file_output).read()) ]
    for link in linksNous: act_on_link(link)

#driver.quit()
