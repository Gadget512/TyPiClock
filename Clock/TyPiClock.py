import argparse, datetime, json, os, sys

# TODO what is needed here:?
import platform
import signal
import time
import locale
import re

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from Features import AnalogClock, Calendar, DateTime, Slideshow

# TODO what is needed here:?
"""
from PyQt4.QtGui import QPixmap, QMovie, QBrush, QColor, QPainter
from PyQt4.QtCore import QUrl
from PyQt4 import QtNetwork

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
		self.clocks = []
		self.datetimes = []
		
		# Set up pages
		for page in self.config['pages']:
			self.createPage(page['num'], page['background'])
		
			# Slideshows
			for ss in page['slideshows']:
				self.slideshows.append(Slideshow(self.pages[page['num']], ss))
				
			# Calendars
			for cal in page['calendars']:
				self.calendars.append(Calendar(self.pages[page['num']], cal))
		
			# Analog Clocks
			for clock in page['clocks']:
				self.clocks.append(AnalogClock(self.pages[page['num']], clock))
				
			# DateTimes
			for dt in page['datetimes']:
				self.datetimes.append(DateTime(self.pages[page['num']], dt))
		
		
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