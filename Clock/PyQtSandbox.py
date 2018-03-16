import sys
import os
import platform
import signal
import datetime
import time
import json
import locale
import random
import re
import argparse

from PyQt4 import QtGui, QtCore #, QtNetwork
from PyQt4.QtCore import Qt

from Features import AnalogClock, DateTime

"""
from PyQt4.QtGui import QPixmap, QMovie, QBrush, QColor, QPainter
from PyQt4.QtCore import QUrl

from PyQt4.QtNetwork import QNetworkReply
from PyQt4.QtNetwork import QNetworkRequest
from subprocess import Popen
"""

# ------------------------------------------------------------------------------------------------------------------------------------------------------------
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
	
	configFile = None
	
	parser.add_argument('-c', '--c', '--config', dest="configFile", required=True)
	
	args = parser.parse_args()
	
	configFile = args.configFile
	
	return configFile
	
def parseJson(configFile):
	
	
	return None
	
		
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
		
		# Set up pages
		for page in self.config['pages']:
			self.createPage(page['num'], page['background'])
		
		# Display page0
		self.pages[0].setVisible(True)
		
		# Analog Clocks
		self.clocks = []
		for page in self.config['pages']:
			for clock in page['clocks']:
				clockImages = [clock['face'], clock['hour'], clock['minute'], clock['second']]
				self.clocks.append(AnalogClock(self.pages[page['num']], clock['name'], clockImages, clock['coords']))
				
		# DateTimes
		
		self.datetimes = []
		for page in self.config['pages']:
			for dt in page['datetimes']:
				#properties = [dt['name'], dt['format'], dt['font'], dt['fontsize'], dt['fontattr'], dt['color'], dt['effect'], dt['location']]
				#self.datetimes.append(DateTime(self.pages[page['num']], properties))
				self.datetimes.append(DateTime(self.pages[page['num']], dt))
		
		
		# Calendars
		
		# Display window, in full screen
		self.show()
		self.showFullScreen()
		
	def keyPressEvent(self, event):
	
		if isinstance(event, QtGui.QKeyEvent):
			
			# EXIT:
			if event.key() == Qt.Key_F4:
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
				self.switchPage(page=0)
					
	def mousePressEvent(self, event):
		if type(event) == QtGui.QMouseEvent:
			self.switchPage(next="R")
			
	def createPage(self, index, background):
		page = QtGui.QFrame(self)
		page.setObjectName("page%s" % index)
		page.setGeometry(0, 0, self.width, self.height)
		page.setStyleSheet("#page"+str(index)+" { background-color: black; border-image: url("+background+") 0 0 0 0 stretch stretch;}")
		page.setVisible(False)
		self.pages.append(page)
			
	def switchPage(self, next=None, page=0): # nextframe in original code (basically)
		nextPage = 0
		if next:
			if next == "R":
				nextPage = self.currentPage + 1
			elif next == "L":
				nextPage = self.currentPage - 1
				
		else:
			nextPage = page
		
		# If page selection is outside range, go to page 1:	
		if nextPage >= len(self.pages) :
			nextPage = 0
		elif nextPage < 0:
			nextPage = len(self.pages) - 1
		self.setPage(nextPage)
		
	def setPage(self, page): # fixupframe in original code (basically?)
		
		self.pages[self.currentPage].setVisible(False)
		self.pages[page].setVisible(True)
		
		# TODO RADAR?
		
		self.currentPage = page
		

def startWindow(config):
	
	app = QtGui.QApplication(sys.argv)
	
	# Get desktop resolution
	desktop = app.desktop()
	res = desktop.screenGeometry()
	height = res.height()
	width = res.width()
	
	window = Window(height=height, width=width, config=config)
	
	sys.exit(app.exec_())

def main():
	
	configFile = parseArgs()
	
	configuration = json.load(open(configFile))
	
	startWindow(configuration)
	
if __name__ == "__main__":
	main()