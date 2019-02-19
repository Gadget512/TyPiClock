import datetime
from PyQt4.QtCore import Qt

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
		
class TyAlign():
	
	def __init__(self):
		pass
	
	def align(self, gridnum):
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