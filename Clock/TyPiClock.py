"""
Author: Gadget512 (https://github.com/Gadget512)

This project is adapted from n0bel's PiClock: https://github.com/n0bel/PiClock
"""

import argparse, datetime, json, os, sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from Features import AnalogClock, CalendarDisplay, DateTime, Image, Slideshow, Timer, Weather, WeatherDisplay

# TODO what is needed here:?
import platform
import signal
import time
import locale
import re

"""
from PyQt4.QtGui import QPixmap, QMovie, QBrush, QColor, QPainter
from PyQt4.QtCore import QUrl
from PyQt4 import QtNetwork

from PyQt4.QtNetwork import QNetworkReply
from PyQt4.QtNetwork import QNetworkRequest
from subprocess import Popen
"""

# ------------------------------------------------------------------------------------------------------------------------------------------------------------
# For google calendar API stuff
"""
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
"""
# ------------------------------------------------------------------------------------------------------------------------------------------------------------

#sys.dont_write_bytecode = True

def parseArgs():
	parser = argparse.ArgumentParser()
	
	# TODO default configFile?
	
	parser.add_argument('-c', '--c', '--config', dest="configFile", required=True)
	
	args = parser.parse_args()
	
	return args.configFile
	
		
class Window(QtGui.QWidget):
	
	def __init__(self, width, height, config):
		super(Window, self).__init__()
		self.width = width
		self.height = height
		self.config = config
		self.currentPage = 0 # index of current page
		self.pages = []
	
		self.initUI()
	
	
	def initUI(self):
		self.setWindowTitle(os.path.basename(__file__))
		self.setStyleSheet("QWidget { background-color: blue;}")
		
		self.slideshows = []
		self.calendars = []
		self.images = []
		self.clocks = []
		self.datetimes = []
		self.timers = []
		self.weathers = []
		
		# Weather data (independent of pages, feature objects pull data as needed)
		loc = {"lat": str(self.config['config']['location']['lat']), "lng": str(self.config['config']['location']['lng'])}
		if self.config['config']['weather']['api']:
			self.weather = Weather(self.config['config']['weather'], loc)
			
		# Calendar data
		# TODO
		
		# About Page
		self.createAboutPage()
		
		# Set up pages
		for page in self.config['pages']:
			self.createPage(page['num'], page['background'])
		
			# Slideshows
			if 'slideshows' in page.keys():
				for ss in page['slideshows']:
					self.slideshows.append(Slideshow(self.pages[page['num']], ss))
				
			# Images
			if 'images' in page.keys():
				for image in page['images']:
					self.images.append(Image(self.pages[page['num']], image))
				
			# Calendars TODO
			"""
			if 'calendars' in page.keys():
				for cal in page['calendars']:
					self.calendars.append(CalendarDisplay(self.pages[page['num']], cal))
					for weather in cal['weathers']:
						self.weathers.append(self.weather.addWeather(weather)) # TODO need to keep a list here, or let Weather handle them? (below)
						self.weather.addWeather(weather)
			"""
			
			# Analog Clocks
			if 'clocks' in page.keys():
				for clock in page['clocks']:
					self.clocks.append(AnalogClock(self.pages[page['num']], clock))
				
			# DateTimes
			if 'datetimes' in page.keys():
				for dt in page['datetimes']:
					self.datetimes.append(DateTime(self.pages[page['num']], dt))
				
			# Timers
			if 'timers' in page.keys():
				for timer in page['timers']:
					self.timers.append(Timer(self.pages[page['num']], timer))
				
			# Weathers
			if 'weathers' in page.keys():
				if self.config['config']['weather']['api']:
					for wtr in page['weathers']:
						self.weathers.append(WeatherDisplay(self.pages[page['num']], wtr, self.weather))
		
		
		# Display page0
		self.pages[0].setVisible(True)
		
		# Display window, in full screen
		self.show()
		self.showFullScreen()
		
	def keyPressEvent(self, event):
	
		if isinstance(event, QtGui.QKeyEvent):
			
			# EXIT:
			if event.key() == Qt.Key_F4:
				QtGui.QApplication.exit(0)
			if event.key() == Qt.Key_Escape:
				QtGui.QApplication.exit(0)
			
			# Cycle Pages:
			if event.key() == Qt.Key_Space:
				self.switchPage(next="R")
			if event.key() == Qt.Key_Left:
				self.switchPage(next="L")
			if event.key() == Qt.Key_Right:
				self.switchPage(next="R")
				
			# Select Page:
			if event.key() == Qt.Key_1:
				self.switchPage(page=0)
			if event.key() == Qt.Key_2:
				self.switchPage(page=1)
			if event.key() == Qt.Key_3:
				self.switchPage(page=2)
			if event.key() == Qt.Key_4:
				self.switchPage(page=3)
			if event.key() == Qt.Key_5:
				self.switchPage(page=4)
			if event.key() == Qt.Key_6:
				self.switchPage(page=5)
			if event.key() == Qt.Key_7:
				self.switchPage(page=6)
			if event.key() == Qt.Key_8:
				self.switchPage(page=7)
			if event.key() == Qt.Key_9:
				self.switchPage(page=8)
			if event.key() == Qt.Key_0:
				self.switchPage(page=9)
				
			# About Page:
			if event.key() == Qt.Key_A:
				self.showAboutPage()
			if event.key() == Qt.Key_Up:
				self.showAboutPage()
			if event.key() == Qt.Key_Down:
				self.showAboutPage()
					
	def mousePressEvent(self, event):
		if type(event) == QtGui.QMouseEvent:
			self.switchPage(next="R")
			
	def createPage(self, index, background):
		page = QtGui.QFrame(self)
		page.setObjectName("page%s" % index)
		page.setGeometry(0, 0, self.width, self.height)
		page.setStyleSheet("#page"+str(index)+" { background-color: black; border-image: url("+background+") 0 0 0 0 stretch stretch;}")
		page.setVisible(False)
		self.pages.insert(index, page)
			
	def switchPage(self, next=None, page=0):
		nextPage = 0
		if next:
			if next == "R":
				nextPage = self.currentPage + 1
			elif next == "L":
				nextPage = self.currentPage - 1
				
		else:
			nextPage = page
		
		# If page selection is outside range, go to page 0:	
		if nextPage >= len(self.pages) :
			nextPage = 0
		elif nextPage < 0:
			nextPage = len(self.pages) - 1
		self.setPage(nextPage)
		
	def setPage(self, page):
		
		if self.currentPage == 99: # About Page
			self.aboutPage.setVisible(False)
		else:
			self.pages[self.currentPage].setVisible(False)
		self.pages[page].setVisible(True)
		
		self.currentPage = page
		
	def createAboutPage(self):
		self.aboutPage = QtGui.QFrame(self)
		self.aboutPage.setObjectName("AboutPage")
		self.aboutPage.setGeometry(0, 0, self.width, self.height)
		self.aboutPage.setStyleSheet("#AboutPage { background-color: black; border-image: url(images/default/DenverSkyline_1080.jpg) 0 0 0 0 stretch stretch;}")
		self.aboutPage.setVisible(False)
		
		logo = {"name": "TyPiLogo",
				"image": "images/default/TyPiClockLogo.png",
				"location": [0, 0, 1028, 256]}
		self.images.append(Image(self.aboutPage, logo))
		darksky = {"name": "WeatherAtt",
					"image": "images/default/poweredby_small_green.png",
					"shadow": False,
					"location": [0, 500, 250, 90]}
		self.images.append(Image(self.aboutPage, darksky))
		
		lastUpdated = { "name": "AboutLastUpdated",
						"type": "lastUpdated",
						"subtype": None,
						"interval": 60,
						"background": "images/default/background_shade.png",
						"images": {},
						"data": [{"name": "AboutLastUpdatedText",
								"type": "lastUpdated",
								"format": "Last Updated: {:%x %X}",
								"font": "sans-serif",
								"fontsize": "30",
								"fontattr": "",
								"color": "#1ECB7C",
								"alignment": 4,
								"shadow": False,
								"location": [250, 500, 800, 90]}],
						"location": [0, 500, 1050, 90]}
		self.weathers.append(WeatherDisplay(self.aboutPage, lastUpdated, self.weather))
							
		
	def showAboutPage(self):
		# TODO Cycle pages???
		if self.currentPage != 99: # Already on About Page
			self.pages[self.currentPage].setVisible(False)
			self.aboutPage.setVisible(True)
		
			self.currentPage = 99 # Makes nextPage 0
		

def startWindow(config):
	
	app = QtGui.QApplication(sys.argv)
	
	# Get desktop resolution
	desktop = app.desktop()
	res = desktop.screenGeometry()
	height = res.height()
	width = res.width()
	
	# Create window
	window = Window(height=height, width=width, config=config)
	
	# Exit app (ctrl-F4)
	sys.exit(app.exec_())

def main():
	
	# Get config file name
	configFile = parseArgs()
	
	# Parse config file
	configuration = json.load(open(configFile))
	
	# Start app
	startWindow(configuration)
	
if __name__ == "__main__":
	main()
