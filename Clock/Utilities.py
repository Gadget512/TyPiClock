import datetime

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