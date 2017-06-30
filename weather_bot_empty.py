# coding=UTF-8
__author__ = 'fernandolourenco'
import version

import datetime
import time
import dateutil.parser

import telepot
import codecs
import sys
import os

import requests
import urllib
import pprint

from ConfigParser import SafeConfigParser

#Constants
# ##########################################################################
SETTINGSFILE = 'weather.ini'
##########################################################################

#Globals
##########################################################################
global bot
global WEATHER_API_KEY
##########################################################################

##########################################################################
def main():
    global bot
    global WEATHER_API_KEY

    # Read config file
    parser = SafeConfigParser()

    # Open the file with the correct encoding
    with codecs.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), SETTINGSFILE), 'r', encoding='utf-8') as f:
        parser.readfp(f)

    try:
	WEATHER_API_KEY = parser.get('Weather', 'api_key')
    except:
	print u'Cannot get weather endpoint API Key.'
	sys.exit(1)

    try:
        # Create access to bot
        bot = telepot.Bot(parser.get('Telegram', 'token'))
        bot.message_loop(handle)
    except:
        print u'Cannot access Telegram. Please do /start'
        sys.exit(1)
    print "Telegram bot started..."
    # Keep the program running.
    while 1:
        time.sleep(10)
##########################################################################


if __name__ == "__main__":
    main()
