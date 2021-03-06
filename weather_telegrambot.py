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

from ConfigParser import SafeConfigParser #python 2
#from configparser import SafeConfigParser #python 3

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
def handle(msg):

	#pprint.pprint(msg)
	uid = msg['chat']['id']
	message = msg['text']
	commands = message.upper().split(" ")
	if not commands[0].startswith('/'):
		return
	if commands[0] == '/STATUS':
		bot.sendMessage(uid, text=u"Ok. Running\n%s" % version.__version__)
	elif commands[0] == '/START':
		bot.sendMessage(uid, text=u"Started. Time now\n%s" % datetime.datetime.now())
	elif commands[0] == '/WEATHER':
		if len(commands) == 1:
			location = "Hong Kong"
		else:
			location = "%s" % message.split(' ', 1)[1]
		query = "http://api.openweathermap.org/data/2.5/weather?q=%s&APPID=%s" % (location, WEATHER_API_KEY)
		print("Weather call: %s" % query)
		weatherData = requests.get(query).json()
		bot.sendMessage(uid, text=u"Weather of %s measured from %s in country %s is %s degree celcius" % (location, weatherData['name'], weatherData['sys']['country'], weatherData['main']['temp']-273.15))
	elif commands[0] == '/FORECAST':
		if len(commands) == 1:
			location = "Hong Kong"
		else:
			location = "%s" % message.split(' ', 1)[1]
		query = "http://api.openweathermap.org/data/2.5/forecast?q=%s&APPID=%s&mode=json" % (location, WEATHER_API_KEY)
		print("Forecast call: %s" % query)
		weatherData = requests.get(query).json()
		text = u"5 days Forecast of weather of %s:\n" % location
		for i in range(0, len(weatherData['list']), 8):
			text+= u"%s\t%s degree celcius\t%s\n" % (weatherData['list'][i]['dt_txt'].split(' ')[0], weatherData['list'][i]['main']['temp']-273.15, weatherData['list'][i]['weather'][0]['description'])
			bot.sendMessage(uid, text=text)
	elif commands[0] == '/HELP':
		bot.sendMessage(uid, text=u"Available commands for %s:\n /status \n/start \n/weather {location} \n/forecast {location} \n/help" % os.path.basename(sys.argv[0]))
	else:
		bot.sendMessage(uid, text=u"Unknown command" )
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
		print(u'Cannot get weather endpoint API Key.')
		sys.exit(1)

	try:
		# Create access to bot
		bot = telepot.Bot(parser.get('Telegram', 'token'))
		bot.message_loop(handle)
	except:
		print(u'Cannot access Telegram. Please do /start')
		sys.exit(1)
	print("Telegram bot started...")
	# Keep the program running.
	while 1:
		time.sleep(10)
##########################################################################


if __name__ == "__main__":
	main()
