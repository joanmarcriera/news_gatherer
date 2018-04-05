#!/usr/bin/env python
from selenium import webdriver
import argparse
import logging
import logging.handlers
import os
import inspect

#import pdb; pdb.set_trace()

logger = logging.getLogger('owl.args.example')
logger.setLevel(logging.DEBUG)

# always write everything to the rotating log files
if not os.path.exists('logs'): os.mkdir('logs')
log_file_handler = logging.handlers.TimedRotatingFileHandler('logs/args.log', when='M', interval=2)
log_file_handler.setFormatter( logging.Formatter('%(asctime)s [%(levelname)s](%(name)s:%(funcName)s:%(lineno)d): %(message)s') )
log_file_handler.setLevel(logging.DEBUG)
logger.addHandler(log_file_handler)

# also log to the console at a level determined by the --verbose flag
console_handler = logging.StreamHandler() # sys.stderr
console_handler.setLevel(logging.CRITICAL) # set later by set_log_level_from_verbose() in interactive sessions
console_handler.setFormatter( logging.Formatter('[%(levelname)s](%(name)s): %(message)s') )
logger.addHandler(console_handler)


parser = argparse.ArgumentParser(description="performs a variety of operations on a file.", epilog="pretty neat, huh?", fromfile_prefix_chars='@',)
parser.add_argument('-V', '--version', action="version", version="%(prog)s 0.17.2")
parser.add_argument("-s", dest='site',default='http://hvper.com', help="Site to gather links from.")
parser.add_argument("-f", dest='file',default='../joanmarcriera.github.io/index.md', help="File where to add the links.")
parser.add_argument("-w", dest='words',default='Catalonia,Puigdemont,Catalan,Ponsati,Ponsatí',help="Words to search for, comma separed")
group = parser.add_argument_group('group')
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
group.add_argument("-d", "--debug", action="store_true")

def autolog(message):
    "Automatically log the current function details."
    # Get the previous frame in the stack, otherwise it would
    # be this function!!!
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logging.debug("%s: %s in %s:%i" % (
        message,
        func.co_name,
        func.co_filename,
        func.co_firstlineno
    ))


def set_log_level_from_verbose(args):
    if not args.verbose:
        console_handler.setLevel('ERROR')
    elif args.verbose == 1:
        console_handler.setLevel('WARNING')
    elif args.verbose == 2:
        console_handler.setLevel('INFO')
    elif args.verbose >= 3:
        console_handler.setLevel('DEBUG')
    else:
        logger.critical("UNEXPLAINED NEGATIVE COUNT!")


def run_browser(args):
    autolog("inside run browser")
    options = webdriver.ChromeOptions()
    options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    if args.quiet: options.add_argument('headless')
    options.add_argument('window-size=600x400')
    driver=webdriver.Chrome(chrome_options=options)
    driver.get(args.site)
    return driver

def act_on_link(args,link):
    logger.info("Inside act on link")
    autolog("inside act on link")
    f=open(args.file,'a')
    f.write("[{0}]({1})\n\n".format(link.text , link.get_attribute("href")))
    print ("["+link.text+"]("+link.get_attribute("href")+")")



if __name__ == '__main__':
    args = parser.parse_args()

    if args.debug: import pdb; pdb.set_trace()
    keyWords=args.words.split(",")
    site=args.site

    set_log_level_from_verbose(args)
    logger.info("Site to gather : {}".format(args.site))

    driver = run_browser(args)
    logger.info("Browser running")
    links = driver.find_elements_by_xpath("//a[@href]")
    logger.info("Before for loop with links : {}".format(len(links)))

    for word in keyWords:
        logger.info("Inside for loop with word : {}".format(word))
        linksTrobats = [ link for link in links if any(word in link.text for word in keyWords)]
        logger.info("Inside for loop with linksTrobats : {}".format(linksTrobats))
        linksNous = [ link for link in linksTrobats  if (link.text not in open(args.file).read()) ]
        logger.info("Inside for loop with linksNous: {}".format(linksNous))
        for link in linksNous: act_on_link(args,link)

    driver.quit()
