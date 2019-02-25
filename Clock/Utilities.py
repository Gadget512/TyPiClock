import datetime
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QColor, QGraphicsDropShadowEffect, QLabel

class Log():
	
	def __init__(self, name="MAIN()", level="error"):
		self.level = level
		self.name = name
		
	def log(self, message, lvl):
		ts = "{:%x %X} ".format(datetime.datetime.now())
		nm = "{:<20}".format(self.name)
		
		if lvl == "debug":
			tag = "{:^16}".format("DEBUG")
		elif lvl == "info":
			tag = "{:^16}".format("INFO")
		elif lvl == "warning":
			tag = "{:^16}".format("-WARNING-")
		elif lvl == "error":
			tag = "{:*^16}".format("ERROR")
		
		if self.level == "debug":
			print (ts + nm + tag + message)
			
		elif self.level == "info":
			if lvl == "info" or lvl == "warning" or lvl == "error":
				print (ts + nm + tag + message)
				
		elif self.level == "warning":
			if lvl == "warning" or lvl == "error":
				print (ts + nm + tag + message)
				
		elif self.level == "error":
			if lvl == "error":
				print (ts + nm + tag + message)
			
	def debug(self, message):
		self.log(message, "debug")
		
	def info(self, message):
		self.log(message, "info")
		
	def warning(self, message):
		self.log(message, "warning")
		
	def error(self, message):
		self.log(message, "error")
		
	
def align(gridnum):
	if gridnum == 1:
		return (Qt.AlignLeft | Qt.AlignTop)
	elif gridnum == 2:
		return (Qt.AlignHCenter | Qt.AlignTop)
	elif gridnum == 3:
		return (Qt.AlignRight | Qt.AlignTop)
	elif gridnum == 4:
		return (Qt.AlignLeft | Qt.AlignVCenter)
	elif gridnum == 5:
		return (Qt.AlignHCenter | Qt.AlignVCenter)
	elif gridnum == 6:
		return (Qt.AlignRight | Qt.AlignVCenter)
	elif gridnum == 7:
		return (Qt.AlignLeft | Qt.AlignBottom)
	elif gridnum == 8:
		return (Qt.AlignHCenter | Qt.AlignBottom)
	elif gridnum == 9:
		return (Qt.AlignRight | Qt.AlignBottom)
	else:
		return (Qt.AlignHCenter | Qt.AlignVCenter)
		
def createTextLabel(page, frameName, properties):
	textLabel = QLabel(page)
	textLabel.setObjectName(frameName+properties['name'])
	textLabel.setStyleSheet("#"+frameName+properties['name']+"{ font-family:"+properties['font']+"; color: "+
		properties['color'] + "; background-color: transparent; font-size: "+
		properties['fontsize']+"px; "+
		properties['fontattr']+"}")
	textLabel.setAlignment(align(properties['alignment']))
	if properties['shadow']:
		textEffect = QGraphicsDropShadowEffect()
		textEffect.setOffset(properties['shadow']['offset'])
		textEffect.setBlurRadius(properties['shadow']['blur'])
		textEffect.setColor(QColor(properties['shadow']['color']))
		textLabel.setGraphicsEffect(textEffect)
	textLabel.setGeometry(properties['location'][0], properties['location'][1], properties['location'][2], properties['location'][3])
	
	return textLabel
	
def createImageLabel(page, frameName, properties):
	imageLabel = QLabel(page)
	imageLabel.setObjectName(frameName+properties['name'])
	imageLabel.setStyleSheet("#"+frameName+properties['name']+" { background-color: transparent; }")
	if properties['shadow']:
		textEffect = QGraphicsDropShadowEffect()
		textEffect.setOffset(properties['shadow']['offset'])
		textEffect.setBlurRadius(properties['shadow']['blur'])
		textEffect.setColor(QColor(properties['shadow']['color']))
		imageLabel.setGraphicsEffect(textEffect)
	imageLabel.setGeometry(properties['location'][0], properties['location'][1], properties['location'][2], properties['location'][3])
		
	return imageLabel