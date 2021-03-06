import datetime, json, random, os, operator
import requests
from textwrap import fill # TODO put in Utilities

import Utilities as Ut

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QColor, QFrame, QLabel, QMatrix, QPixmap
"""
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
"""
class AnalogClock():
	"""
	Creates an analog clock on the specified 'page', with the specified attributes
	
	page - QFrame object to display the clock
	clockName - unique name for clock object names
	images - array of relative paths to clock images, do not need to have a second hand
	coords - array of integers (x,y,w,h) within which to display the clock
	"""
	
	def tick(self):
		self.dlog.debug("_tick()")
		now = datetime.datetime.now()
		
		secangle = now.second * 6 # seconds converted to angle (in degrees)
		minangle = now.minute * 6 # minutes converted to angle (in degrees)
		hourangle = ((now.hour % 12) + now.minute / 60.0) * 30.0
		
		# Display second hand
		if self.secondhand:
			secsize = self.secpixmap.size()
			secpixmap2 = self.secpixmap.transformed(
				QMatrix().scale(
					float(self.clockFrameRect.width()) / secsize.height(),
					float(self.clockFrameRect.height()) / secsize.height()).rotate(secangle),
				Qt.SmoothTransformation) # rotate the image
			self.second.setPixmap(secpixmap2)
			secsize = secpixmap2.size()
			self.second.setGeometry(
				self.clockFrameRect.center().x() - secsize.width() / 2,
				self.clockFrameRect.center().y() - secsize.height() / 2,
				secsize.width(),
				secsize.height()) # display the image
			
		# Display minute hand
		minsize = self.minpixmap.size()
		minpixmap2 = self.minpixmap.transformed(
			QMatrix().scale(
				float(self.clockFrameRect.width()) / minsize.height(),
				float(self.clockFrameRect.height()) / minsize.height()).rotate(minangle),
			Qt.SmoothTransformation) # rotate the image
		self.minute.setPixmap(minpixmap2)
		minsize = minpixmap2.size()
		self.minute.setGeometry(
			self.clockFrameRect.center().x() - minsize.width() / 2,
			self.clockFrameRect.center().y() - minsize.height() / 2,
			minsize.width(),
			minsize.height()) # display the image
		
		# Display hour hand
		hoursize = self.hourpixmap.size()
		hourpixmap2 = self.hourpixmap.transformed(
			QMatrix().scale(
				float(self.clockFrameRect.width()) / hoursize.height(),
				float(self.clockFrameRect.height()) / hoursize.height()).rotate(hourangle),
			Qt.SmoothTransformation) # rotate the image
		self.hour.setPixmap(hourpixmap2)
		hoursize = hourpixmap2.size()
		self.hour.setGeometry(
			self.clockFrameRect.center().x() - hoursize.width() / 2,
			self.clockFrameRect.center().y() - hoursize.height() / 2,
			hoursize.width(),
			hoursize.height()) # display the image
	
	def __init__(self, page, properties):
		self.dlog = Ut.Log(name = "AnalogClock()", level="warning")
		
		self.clockface = properties['face']
		self.hourhand = properties['hour']
		self.minutehand = properties['minute']
		self.secondhand = properties['second'] # May be None (null)
		
		# Create new frame on page for clock
		self.dlog.debug("Creating " + properties['name'])
		self.clockFrame = QFrame(page)
		self.clockFrame.setObjectName(properties['name'])
		# specify (x, y, w, h) where x,y is the top-left corner, w is the width, h is the height
		self.clockFrameRect = QtCore.QRect(properties['location'][0],  properties['location'][1],  properties['location'][2], properties['location'][3])
		
		# Display clock background
		self.clockFrame.setGeometry(self.clockFrameRect)
		self.clockFrame.setStyleSheet("#"+properties['name']+" { background-color: transparent; border-image: url("+self.clockface+") 0 0 0 0 stretch stretch;}")
		
		# Set up second hand
		self.second = None
		self.secpixmap = None
		if self.secondhand:
			self.dlog.debug("Creating " + properties['name'] + " second")
			self.second = QLabel(page) # create label on page
			self.second.setObjectName(properties['name']+"second") # name label
			self.second.setStyleSheet("#"+properties['name']+"second { background-color: transparent; }")
			self.secpixmap = QPixmap(self.secondhand) # create pixmap with image
			
		# Set up minute hand
		self.dlog.debug("Creating " + properties['name'] + " minute")
		self.minute = QLabel(page) # create label on page
		self.minute.setObjectName(properties['name']+"minute") # name label
		self.minute.setStyleSheet("#"+properties['name']+"minute { background-color: transparent; }")
		self.minpixmap = QPixmap(self.minutehand) # create pixmap with image
		
		# Set up hour hand
		self.dlog.debug("Creating " + properties['name'] + " hour")
		self.hour = QLabel(page) # create label on page
		self.hour.setObjectName(properties['name']+"hour") # name label
		self.hour.setStyleSheet("#"+properties['name']+"hour { background-color: transparent; }")
		self.hourpixmap = QPixmap(self.hourhand) # create pixmap with image
		
		# Start clock
		self.ctimer = QtCore.QTimer() # QTimer calls the specified function every specified number of milliseconds (parallel?)
		self.ctimer.timeout.connect(self.tick)
		self.ctimer.start(properties['interval']*1000)


class DateTime():
	
	def tick(self):
		self.dlog.debug("_tick()")
		now = datetime.datetime.now()
		text = self.textFormat.format(now)
		self.textLabel.setText(text)
	
	def __init__(self, page, properties): 
		"""
		Displays text based on the given properties
		
		properties - dict {name, format, font, fontsize, fontattr, color, effect, location}
			name - name of the text object
			format - string that specifies the data to be displayed as well as the format, e.g. {0:%I:%M\n%S %p} for a digitial clock
			font - font-family for the text
			fontsize - size of the font
			fontattr - attributes in Qt-style notation
			color - color for the text, e.g. #50CBEB
			effect - Qt object?
			location - list of coordinates (x, y, w, h)
		"""
		self.dlog = Ut.Log(name = "DateTime()", level="warning")
		
		self.textFormat = properties['format']
		
		# Create text frame
		self.dlog.debug("Creating frame " + properties['name'])
		self.textFrame = QFrame(page)
		self.textFrame.setObjectName(properties['name']+"frame")
		self.textFrameRect = QtCore.QRect(properties['location'][0], properties['location'][1], properties['location'][2], properties['location'][3])
		
		# Display text frame (with background if specified)
		self.textFrame.setGeometry(self.textFrameRect)
		if properties['background']:
			self.textFrame.setStyleSheet("#"+properties['name']+"frame { background-color: transparent; border-image: url("+properties['background']+") 0 0 0 0 stretch stretch;}")
		else:
			self.textFrame.setStyleSheet("#"+properties['name']+"frame { background-color: transparent;}")
		
		# Create text stylesheet based on given properties
		self.dlog.debug("Creating label " + properties['name'])
		self.textLabel = Ut.createTextLabel(page, properties['name'], properties)
		
		# Display text
		now = datetime.datetime.now()
		text = self.textFormat.format(now)
		self.textLabel.setText(text)
		
		# Start timer
		self.timer = QtCore.QTimer() # QTimer calls the specified function every specified number of milliseconds
		self.timer.timeout.connect(self.tick)
		self.timer.start(properties['interval']*1000)


class Timer(): # TODO
	
	def tick(self):
		self.dlog.debug("_tick()")
		displayDate = None
		
		if self.startTime == 0:
			now = datetime.datetime.now()
			#displayDate = datetime.timedelta(seconds = self.stopTime - now)
			displayDate = self.stopTime - now
			
		#TODO text = self.textFormat.format(datetime.datetime.fromtimestamp(displayDate.total_seconds()))
		#text = "{:0d} days {:%H:%M:%S}".format(displayDate.days, datetime.time(displayDate.seconds/3600, (displayDate.seconds%3600)/60, (displayDate.seconds%3600)%60))
		text = self.textFormat.format(displayDate.days, datetime.time(displayDate.seconds/3600, (displayDate.seconds%3600)/60, (displayDate.seconds%3600)%60))
		self.textLabel.setText(text)
		
	def __init__(self, page, properties):
		self.dlog = Ut.Log(name = "Timer()", level="info")
		
		self.textFormat = properties['format']
		self.startTime = None
		self.stopTime = None
		
		# Create text frame
		self.dlog.info("Creating frame " + properties['name'])
		self.textFrame = QFrame(page)
		self.textFrame.setObjectName(properties['name']+"frame")
		self.textFrameRect = QtCore.QRect(properties['location'][0], properties['location'][1], properties['location'][2], properties['location'][3])
		
		# Display text frame (with background if specified)
		self.textFrame.setGeometry(self.textFrameRect)
		if properties['background']:
			self.textFrame.setStyleSheet("#"+properties['name']+"frame { background-color: transparent; border-image: url("+properties['background']+") 0 0 0 0 stretch stretch;}")
		else:
			self.textFrame.setStyleSheet("#"+properties['name']+"frame { background-color: transparent;}")
		
		# Create text stylesheet based on given properties
		self.dlog.debug("Creating label " + properties['name'])
		self.textLabel = Ut.createTextLabel(page, properties['name'], properties)
		
		if properties['startTime'] == 0:
			self.startTime = 0
		if properties['stopTime']:
			self.stopTime = datetime.datetime.fromtimestamp(properties['stopTime'])
			#self.stopTime = properties['stopTime']
		""" TODO
		if properties['type'] == "up":
			pass
		elif properties['type'] == "down":
		"""
			
		
		# Display text
		# TODO
		if properties['timerStart'] == 0: # start the timer NOW
			pass
		elif properties['timerStart'] > 0: # start the timer at a later date
			pass
		"""
		now = datetime.datetime.now()
		text = self.textFormat.format(now)
		self.textLabel.setText(text)
		"""
		
		# Start timer
		self.timer = QtCore.QTimer() # QTimer calls the specified function every specified number of milliseconds
		self.timer.timeout.connect(self.tick)
		self.timer.start(properties['interval']*1000)


class Text(): # TODO
	
	def update(self):
		pass
	
	def __init__(self, page, properties):
		self.dlog = Ut.Log(name = "Text()", level="warning")
		self.dlog.debug("Creating frame " + properties['name'])
		
		# Create text frame
		self.textFrame = QFrame(page)
		self.textFrame.setObjectName(properties['name']+"frame")
		self.textFrameRect = QtCore.QRect(properties['location'][0], properties['location'][1], properties['location'][2], properties['location'][3])
		
		# Display text frame (with background if specified)
		self.textFrame.setGeometry(self.textFrameRect)
		if properties['background']:
			self.textFrame.setStyleSheet("#"+properties['name']+"frame { background-color: transparent; border-image: url("+properties['background']+") 0 0 0 0 stretch stretch;}")
		else:
			self.textFrame.setStyleSheet("#"+properties['name']+"frame { background-color: transparent;}")
		
		# Create text stylesheet based on given properties
		self.dlog.debug("Creating label " + properties['name'])
		self.textLabel = Ut.createTextLabel(page, properties['name'], properties)
		
		# Display text
		# TODO
		self.textLabel.setText(properties['text'])
		
	def setText(self, properties):
		# TODO
		return 0
		
class Image():
	
	def __init__(self, page, properties):
		
		self.dlog = Ut.Log(name = "Image()", level="warning")
		self.dlog.debug("Creating frame " + properties['name'])
		
		# Create picture frame
		self.picFrame = QFrame(page)
		self.picFrame.setObjectName(properties['name']+"frame")
		self.picFrameRect = QtCore.QRect(properties['location'][0], properties['location'][1], properties['location'][2], properties['location'][3])
		
		# Display picture frame
		self.picFrame.setGeometry(self.picFrameRect)
		self.picFrame.setStyleSheet("#"+properties['name']+"frame { background-color: transparent; border-image: url("+properties['image']+") 0 0 0 0 stretch stretch;}")
		
class Slideshow():
	
	def switchPicture(self):
		if self.isRandom:
			self.picFrame.setStyleSheet("#"+self.name+"frame { background-color: transparent; border-image: url("+self.pictures[random.randint(0,len(self.pictures)-1)]+") 0 0 0 0 stretch stretch;}")
		else:
			self.picFrame.setStyleSheet("#"+self.name+"frame { background-color: transparent; border-image: url("+self.pictures[self.index]+") 0 0 0 0 stretch stretch;}")
			if self.index+1 == len(self.pictures):
				self.index = 0
			else:
				self.index = self.index+1
			
	
	def __init__(self, page, properties):
		
		# Initialize member variables
		self.name = properties['name']
		self.isRandom = properties['random']
		self.pictures = []
		self.index = 0
		
		# Get picture filenames
		for file in os.listdir(properties['directory']):
			self.pictures.append(properties['directory']+file)
		
		# Create picture frame
		self.picFrame = QFrame(page)
		self.picFrame.setObjectName(self.name+"frame")
		self.picFrameRect = QtCore.QRect(properties['location'][0], properties['location'][1], properties['location'][2], properties['location'][3])
		
		# Display picture frame
		self.picFrame.setGeometry(self.picFrameRect)
		self.picFrame.setStyleSheet("#"+self.name+"frame { background-color: transparent; border-image: url("+self.pictures[0]+") 0 0 0 0 stretch stretch;}")
		
		# Start timer
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.switchPicture)
		self.timer.start(properties['interval']*1000)


class CalendarDisplay():
	
	def update(self):
		return 0
	
	def __init__(self, page, properties):
		
		# Get credentials
		# TODO
		"""
		self.credentials = self.getCredentials()
		http = self.credentials.authorize(httplib2.Http())
		self.service = discovery.build('calendar', 'v3', http=http)
		"""
		
		now = datetime.datetime.now()
		
		# Initialize member variables
		self.type = properties['type']
		self.cell = properties['cell']
		self.cells = []
		
		# Create calendar frame
		self.calFrame = QFrame(page)
		self.calFrame.setObjectName(properties['name']+"frame")
		self.calFrameRect = QtCore.QRect(properties['location'][0], properties['location'][1], properties['location'][2], properties['location'][3])
		
		# Display calendar frame (with background if specified)
		self.calFrame.setGeometry(self.calFrameRect)
		if properties['background']:
			self.calFrame.setStyleSheet("#"+properties['name']+"frame { background-color: transparent; border-image: url("+properties['background']+") 0 0 0 0 stretch stretch;}")
		else:
			self.calFrame.setStyleSheet("#"+properties['name']+"frame { background-color: transparent;}")
			
		if self.type == "1day":
			pass
			# TODO
		elif self.type == "7day":
			pass
			# TODO
			
		elif self.type == "14day":
			pass
			# TODO
			
		elif self.type == "28day":
			for y in range(0,4):
				for x in range (0,7):
					cellLabel = QLabel(page)
					cellLabel.setObjectName(properties['name']+str(y+x))
					cellLabel.setStyleSheet("#"+properties['name']+str(y+x)+"") # TODO
					
					"""
					self.topSummaryFormat = d['format']
					self.topSummaryWidth = d['width']
					self.topSummary = QLabel(page)
					self.topSummary.setObjectName(self.name+d['name'])
					self.topSummary.setStyleSheet("#"+self.name+d['name']+"{ font-family:"+d['font']+"; color: "+
					d['color'] + "; background-color: transparent; font-size: "+
					d['fontsize']+"px; "+
					d['fontattr']+"}")
					self.topSummary.setAlignment(self.align(d['alignment']))
					self.topSummary.setText(fill(self.weatherData['summary'], width=self.topSummaryWidth))
					self.topSummary.setGeometry(d['location'][0], d['location'][1], d['location'][2], d['location'][3])
					"""
		
		# Start timer
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.update)
		self.timer.start(properties['interval']*1000)
			
	def getEvents(self, day=None, month=None, year=None):
		""" Gets all of the events based on keyword arg datetime object passed
		
		The [date] datetime object passed will be stripped of any time data
		and converted to isoformat
		
		Returns:
			events, a list(?) of  calendar events
		"""
		
		# TODO Week?
		
		# TODO 
		offset = '-06:00' # MST (winter), -06:00 MDT (summer)
		# TODO DST, need to know day of week. DST begins 2nd Sunday in March, ends 1st Sunday in November
		
		
		if day:
			# Convert date to 12:00 AM, create date_end for 11:59 PM
			day = day.replace(hour=0, minute=0, second=0)
			day_end = day.replace(hour=23, minute=59, second=59) # End of day
			
			#print ("Getting:", day, day_end)
			
			# Convert dates to isoformat
			day = day.isoformat() + offset
			day_end = day_end.isoformat() + offset
			
			# Call Google Calendar API
			eventsResult = self.service.events().list(calendarId='primary', timeMin=date, timeMax=date_end, singleEvents=True, orderBy='startTime').execute()
			events = eventsResult.get('items', [])
			
			return events
			
		#elif month:
			
			
		#elif year:
		
		
		
	def getEventsMonth(self, date):
		""" Gets all of the events for the given month
		
		The [date] datetime object passed will be stripped of any time and day data
		and converted to isoformat
		
		Returns:
			events, a list(?) of calendar events
		"""
		
		# TODO get list of calendar IDs
		#calendarID = 'primary'
		calendarID = 'tstrqefn0hqmncbmqp30mfqcek@group.calendar.google.com' # Avalanche Calendar
		
		last_day = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31,  8:31, 9:30, 10:31, 11:30, 12:31}
		
		# Leap years
		if (date.year - 2000) % 4 == 0:
			last_day[2] = 29
			print("LEAP YEAR") # TODO DEBUG
		
		# Convert date to 12:00 AM day 1, create date_end for 11:59 PM last day of month
		date = date.replace(day=1, hour=0, minute=0, second=0)
		date_end = date.replace(day=last_day[date.month], hour=23, minute=59, second=59) # End of day
		
		print ("Getting:", date, date_end) # TODO DEBUG
		
		# Convert dates to isoformat TODO DST
		date = date.isoformat() + '-06:00'
		date_end = date_end.isoformat() + '-06:00'
		
		# Call Google Calendar API
		eventsResult = self.service.events().list(calendarId=calendarID, timeMin=date, timeMax=date_end, singleEvents=True, orderBy='startTime').execute()
		events = eventsResult.get('items', [])
		
		return events
	
	def getCredentials(self):
		"""Gets valid user credentials from storage.

		If nothing has been stored, or if the stored credentials are invalid,
		the OAuth2 flow is completed to obtain the new credentials.

		Returns:
			credentials, the obtained credential.
		"""
		home_dir = os.path.expanduser('~')
		credential_dir = os.path.join(home_dir, '.credentials')
		
		if not os.path.exists(credential_dir):
			os.makedirs(credential_dir)
			
		credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

		store = Storage(credential_path)
		credentials = store.get()
		if not credentials or credentials.invalid:
			flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
			flow.user_agent = APPLICATION_NAME
			if flags:
				credentials = tools.run_flow(flow, store, flags)
			else: # Needed only for compatibility with Python 2.6
				credentials = tools.run(flow, store)
			print('Storing credentials to ' + credential_path)
		return credentials
		
		
class Weather():
	
	def update(self):
		self.dlog.debug("_Weather.update()")
		
		# Request Weather
		try:
			self.dlog.info("Requesting weather: "+self.weatherURI)
			self.weatherReply = requests.get(self.weatherURI, timeout=10)
			
			self.dlog.debug("Updating lastUpdated")
			self.lastUpdated = datetime.datetime.now()
		except:
			self.dlog.error("Error requesting weather update!")
		finally:
			pass
			
		# Get Weather Data
		try:
			self.dlog.debug("Parsing weather")
			if self.weatherReply.status_code == 200:
				self.dlog.info("Weather Response Code: " + str(self.weatherReply.status_code))
				self.weatherData = self.weatherReply.json()
			else:
				self.dlog.warning("Weather Response Code: " + str(self.weatherReply.status_code))
		except:
			self.dlog.error("Error getting weather data!")
		
		# TODO not needed?
		"""
		dataFile = open(self.weatherFile, 'w')
		dataFile.write(self.weatherReply)
		dataFile.close()
		"""
	
	def __init__(self, properties, latlng):
		
		self.dlog = Ut.Log(name = "Weather()", level="debug")
		self.weatherData = {}
		self.weatherFile = "weatherData.json"
		self.lastUpdated = None
		self.weatherHeader = None
		
		self.weatherURI = properties['uri'] + properties['api'] +"/" + latlng['lat'] + "," + latlng['lng']
		
		# TODO MUST SUCCEED
		self.update()
		
		# TODO
		"""
		try:
			self.weatherReply = self.http.request(self.weatherURI)
			
			self.weatherData = json.loads(self.weatherReply[1])
			#self.weatherHeader = json.loads(self.weatherReply[0])
			self.lastUpdated = datetime.datetime.now()
		except:
			ts = "{:%x %X}".format(datetime.datetime.now())
			print (ts + " Error requesting initial weather!")
		finally:
			pass
		"""
		
		# Write weather to file
		"""
		dataFile = open(self.weatherFile, 'w')
		dataFile.write(str(self.weatherReply))
		dataFile.close()
		"""
		
		# Start timer
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.update)
		self.timer.start(properties['interval']*1000)
		
	def getCurrently(self):
		self.dlog.debug("_Weather.getCurrently()")
		return self.weatherData['currently']
		
	def getMinutely(self):
		self.dlog.debug("_Weather.getMinutely()")
		return self.weatherData['minutely']
		
	def getHourly(self):
		self.dlog.debug("_Weather.getHourly()")
		return self.weatherData['hourly']
		
	def getDaily(self):
		self.dlog.debug("_Weather.getDaily()")
		return self.weatherData['daily']
		
	def getLastUpdated(self):
		self.dlog.debug("_Weather.getLastUpdated()")
		return self.lastUpdated
		
	def getHeader(self):
		self.dlog.debug("_Weather.getHeader()")
		return self.weatherHeader
		
		
class WeatherDisplay():
	
	def update(self):
		self.dlog.debug("_WeatherDisplay.update(" + self.name + ")")
		# Last Updated
		if self.lastUpdated:
			self.lastUpdated.setText(self.lastUpdatedFormat.format(self.wObj.getLastUpdated()))
		
		# CURRENTLY
		elif self.type == "currently":
			self.weatherData = self.wObj.getCurrently()
			
			# Temperature
			if self.temperature:
				self.temperature.setText(self.temperatureFormat.format(self.weatherData['temperature']))
			
			# Icon
			if self.icon:
				if self.weatherData['icon'] in self.supportedIcons:
					self.icon.setPixmap(QPixmap(self.images[self.weatherData['icon']]).scaled(self.icon.size().width(), self.icon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
				else:
					self.icon.setPixmap(QPixmap(self.images['default']).scaled(self.icon.size().width(), self.icon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
			
			# Summary
			if self.summary:
				self.summary.setText(fill(self.summaryFormat.format(self.weatherData['summary']), width=self.summaryWidth))
				
			# Apparent Temperature
			if self.apparentTemperature:
				self.apparentTemperature.setText(self.apparentTemperatureFormat.format(self.weatherData['apparentTemperature']))
				
			# Humidity
			if self.humidity:
				self.humidity.setText(self.humidityFormat.format(self.weatherData['humidity']))
			
			# Pressure
			if self.pressure:
				self.pressure.setText(self.pressureFormat.format(self.weatherData['pressure']))
			
			# Wind Speed
			if self.windSpeed:
				self.windSpeed.setText(self.windSpeedFormat.format(self.weatherData['windSpeed']))
			
			# Wind Bearing
			if self.windBearing:
				self.windBearing.setText(self.windBearingFormat.format(self.weatherData['windBearing']))
				
		# MINUTELY
		elif self.type == "minutely":
			self.weatherData = self.wObj.getMinutely()
			# TODO
		
		# HOURLY
		elif self.type == "hourly":
			self.weatherData = self.wObj.getHourly()
			hoursData = self.weatherData['data']
			hoursData.sort(key=operator.itemgetter('time'))
			
			if self.subtype == "hour0":
				hourData = hoursData[0]
			elif self.subtype == "hour1":
				hourData = hoursData[1]
			elif self.subtype == "hour2":
				hourData = hoursData[2]
			elif self.subtype == "hour3":
				hourData = hoursData[3]
			elif self.subtype == "hour4":
				hourData = hoursData[4]
			elif self.subtype == "hour5":
				hourData = hoursData[5]
			elif self.subtype == "hour6":
				hourData = hoursData[6]
			elif self.subtype == "hour7":
				hourData = hoursData[7]
			elif self.subtype == "hour8":
				hourData = hoursData[8]
			elif self.subtype == "hour9":
				hourData = hoursData[9]
			elif self.subtype == "hour10":
				hourData = hoursData[10]
			elif self.subtype == "hour11":
				hourData = hoursData[11]
			elif self.subtype == "hour12":
				hourData = hoursData[12]
			elif self.subtype == "hour13":
				hourData = hoursData[13]
			elif self.subtype == "hour14":
				hourData = hoursData[14]
			elif self.subtype == "hour15":
				hourData = hoursData[15]
			elif self.subtype == "hour16":
				hourData = hoursData[16]
			elif self.subtype == "hour17":
				hourData = hoursData[17]
			elif self.subtype == "hour18":
				hourData = hoursData[18]
			elif self.subtype == "hour19":
				hourData = hoursData[19]
			elif self.subtype == "hour20":
				hourData = hoursData[20]
			elif self.subtype == "hour21":
				hourData = hoursData[21]
			elif self.subtype == "hour22":
				hourData = hoursData[22]
			elif self.subtype == "hour23":
				hourData = hoursData[23]
			elif self.subtype == "hour24":
				hourData = hoursData[24]
			
			# Top Summary
			if self.topSummary:
				self.topSummary.setText(fill(self.topSummaryFormat.format(self.weatherData['summary']), width=self.topSummaryWidth))
				
			# Top Icon
			if self.topIcon:
				if self.weatherData['icon'] in self.supportedIcons:
					self.topIcon.setPixmap(QPixmap(self.images[self.weatherData['icon']]).scaled(self.topIcon.size().width(), self.topIcon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
				else:
					self.topIcon.setPixmap(QPixmap(self.images['default']).scaled(self.topIcon.size().width(), self.topIcon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
				
			# Time
			if self.timeData:
				hourTime = datetime.datetime.fromtimestamp(hourData['time'])
				self.timeData.setText(self.timeFormat.format(hourTime))
				
			# Summary
			if self.summary:
				self.summary.setText(fill(self.summaryFormat.format(hourData['summary']), width=self.summaryWidth))
			
			# Icon
			if self.icon:
				if hourData['icon'] in self.supportedIcons:
					self.icon.setPixmap(QPixmap(self.images[hourData['icon']]).scaled(self.icon.size().width(), self.icon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
				else:
					self.icon.setPixmap(QPixmap(self.images['default']).scaled(self.icon.size().width(), self.icon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
			
			# Temperature
			if self.temperature:
				self.temperature.setText(self.temperatureFormat.format(hourData['temperature']))
				
			# Humidity
			if self.humidity:
				self.humidity.setText(self.humidityFormat.format(hourData['humidity']))
				
			# Pressure
			if self.pressure:
				self.pressure.setText(self.pressureFormat.format(hourData['pressure']))
				
			# Wind Speed
			if self.windSpeed:
				self.windSpeed.setText(self.windSpeedFormat.format(self.weatherData['windSpeed']))
			
			# Wind Bearing
			if self.windBearing:
				self.windBearing.setText(self.windBearingFormat.format(self.weatherData['windBearing']))
		
		# DAILY
		elif self.type == "daily":
			self.weatherData = self.wObj.getDaily()
			daysData = self.weatherData['data']
			daysData.sort(key=operator.itemgetter('time'))
			
			if self.subtype == "day0":
				dayData = daysData[0]
			elif self.subtype == "day1":
				dayData = daysData[1]
			elif self.subtype == "day2":
				dayData = daysData[2]
			elif self.subtype == "day3":
				dayData = daysData[3]
			elif self.subtype == "day4":
				dayData = daysData[4]
			elif self.subtype == "day5":
				dayData = daysData[5]
			elif self.subtype == "day6":
				dayData = daysData[6]
			elif self.subtype == "day7":
				dayData = daysData[7]
			
			# Top Summary
			if self.topSummary:
				self.topSummary.setText(fill(self.topSummaryFormat.format(self.weatherData['summary']), width=self.topSummaryWidth))
				
			# Top Icon
			if self.topIcon:
				if self.weatherData['icon'] in self.supportedIcons:
					self.topIcon.setPixmap(QPixmap(self.images[self.weatherData['icon']]).scaled(self.topIcon.size().width(), self.topIcon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
				else:
					self.topIcon.setPixmap(QPixmap(self.images['default']).scaled(self.topIcon.size().width(), self.topIcon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
				
			# Time
			if self.timeData:
				dayTime = datetime.datetime.fromtimestamp(dayData['time'])
				self.timeData.setText(self.timeFormat.format(dayTime))
				
			# Summary
			if self.summary:
				self.summary.setText(fill(self.summaryFormat.format(dayData['summary']), width=self.summaryWidth))
			
			# Icon
			if self.icon:
				if dayData['icon'] in self.supportedIcons:
					self.icon.setPixmap(QPixmap(self.images[dayData['icon']]).scaled(self.icon.size().width(), self.icon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
				else:
					self.icon.setPixmap(QPixmap(self.images['default']).scaled(self.icon.size().width(), self.icon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
			
			# Temperature High
			if self.temperatureHigh:
				self.temperatureHigh.setText(self.temperatureHighFormat.format(dayData['temperatureHigh']))
			
			# Temperature Low
			if self.temperatureLow:
				self.temperatureLow.setText(self.temperatureLowFormat.format(dayData['temperatureLow']))
				
			# Humidity
			if self.humidity:
				self.humidity.setText(self.humidityFormat.format(dayData['humidity']))
				
			# Pressure
			if self.pressure:
				self.pressure.setText(self.pressureFormat.format(dayData['pressure']))
				
			# Wind Speed
			if self.windSpeed:
				self.windSpeed.setText(self.windSpeedFormat.format(self.weatherData['windSpeed']))
			
			# Wind Bearing
			if self.windBearing:
				self.windBearing.setText(self.windBearingFormat.format(self.weatherData['windBearing']))
				
		
	def __init__(self, page, properties, wObj):
		
		self.dlog = Ut.Log(name = "WeatherDisplay()", level="debug")
		
		# Initialize member variables
		self.wObj = wObj
		self.name = properties['name']
		self.type = properties['type']
		self.subtype = properties['subtype']
		self.images = properties['images']
		self.weatherData = {}
		self.dataToDisplay = properties['data']
		self.supportedIcons = ["clear-day", "clear-night", "rain", "snow", "sleet", "wind", "fog", "cloudy", "partly-cloudy-day", "partly-cloudy-night"]
		
		self.lastUpdated = None
		self.lastUpdatedFormat = None
		
		# Potential weather data
		self.timeData = None
		self.timeFormat = None
		
		self.topSummary = None
		self.topSummaryFormat = None
		self.topSummaryWidth = None
		
		self.summary = None
		self.summaryFormat = None
		self.summaryWidth = None
		
		self.topIcon = None
		self.icon = None
		
		self.temperature = None
		self.temperatureFormat = None
		
		self.apparentTemperature = None
		self.apparentTemperatureFormat = None
		
		self.humidity = None
		self.humidityFormat = None
		
		self.pressure = None
		self.pressureFormat = None
		
		self.windSpeed = None
		self.windSpeedFormat = None
		
		self.windBearing = None
		self.windBearingFormat = None
		
		self.temperatureHigh = None # only in daily
		self.temperatureHighFormat = None
		self.temperatureLow = None # only in daily
		self.temperatureLowFormat = None
		
		# Create weather frame
		self.dlog.debug("Creating weather frame " + self.name)
		self.wFrame = QFrame(page)
		self.wFrame.setObjectName(self.name+"frame")
		self.wFrameRect = QtCore.QRect(properties['location'][0], properties['location'][1], properties['location'][2], properties['location'][3])
		
		# Display weather frame
		self.wFrame.setGeometry(self.wFrameRect)
		if properties['background']:
			self.wFrame.setStyleSheet("#"+self.name+"frame { background-color: transparent; border-image: url("+properties['background']+") 0 0 0 0 stretch stretch;}")
		else:
			self.wFrame.setStyleSheet("#"+self.name+"frame { background-color: transparent;}")
		
		# Set up displays
		if self.type == "lastUpdated":
			for d in self.dataToDisplay:
				self.dlog.debug("Creating " + d['name'])
				if d['type'] == "lastUpdated":
					self.lastUpdatedFormat = d['format']
					self.lastUpdated = Ut.createTextLabel(page, self.name, d)
					self.lastUpdated.setText(self.lastUpdatedFormat.format(self.wObj.getLastUpdated()))
		
		elif self.type == "currently":
			self.weatherData = wObj.getCurrently()
			for d in self.dataToDisplay:
				self.dlog.debug("Creating " + d['name'])
				if d['type'] == "summary":
					self.summaryFormat = d['format']
					self.summaryWidth = d['width']
					self.summary = Ut.createTextLabel(page, self.name, d)
					self.summary.setText(fill(self.summaryFormat.format(self.weatherData['summary']), width=self.summaryWidth))
				
				elif d['type'] == "icon":
					self.icon = Ut.createImageLabel(page, self.name, d)
					if self.weatherData['icon'] in self.supportedIcons:
						self.icon.setPixmap(QPixmap(self.images[self.weatherData['icon']]).scaled(self.icon.size().width(), self.icon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
					else:
						self.icon.setPixmap(QPixmap(self.images['default']).scaled(self.icon.size().width(), self.icon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
					
				elif d['type'] == "temperature":
					self.temperatureFormat = d['format']
					self.temperature = Ut.createTextLabel(page, self.name, d)
					self.temperature.setText(self.temperatureFormat.format(self.weatherData['temperature']))
					
				elif d['type'] == "apparentTemperature":
					self.apparentTemperatureFormat = d['format']
					self.apparentTemperature = Ut.createTextLabel(page, self.name, d)
					self.apparentTemperature.setText(self.apparentTemperatureFormat.format(self.weatherData['apparentTemperature']))
					
				elif d['type'] == "humidity":
					self.humidityFormat = d['format']
					self.humidity = Ut.createTextLabel(page, self.name, d)
					self.humidity.setText(self.humidityFormat.format(self.weatherData['humidity']))
					
				elif d['type'] == "pressure":
					self.pressureFormat = d['format']
					self.pressure = Ut.createTextLabel(page, self.name, d)
					self.pressure.setText(self.pressureFormat.format(self.weatherData['pressure']))
					
				elif d['type'] == "windSpeed":
					self.windSpeedFormat = d['format']
					self.windSpeed = Ut.createTextLabel(page, self.name, d)
					self.windSpeed.setText(self.windSpeedFormat.format(self.weatherData['windSpeed']))
					
				elif d['type'] == "windBearing":
					self.windBearingFormat = d['format']
					self.windBearing = Ut.createTextLabel(page, self.name, d)
					self.windBearing.setText(self.windBearingFormat.format(self.weatherData['windBearing']))
					
		elif self.type == "minutely":
			self.weatherData = wObj.getMinutely()
			# TODO
			
		elif self.type == "hourly":
			self.weatherData = wObj.getHourly()
			hoursData = self.weatherData['data']
			hoursData.sort(key=operator.itemgetter('time'))
			
			if self.subtype == "hour0":
				hourData = hoursData[0]
			elif self.subtype == "hour1":
				hourData = hoursData[1]
			elif self.subtype == "hour2":
				hourData = hoursData[2]
			elif self.subtype == "hour3":
				hourData = hoursData[3]
			elif self.subtype == "hour4":
				hourData = hoursData[4]
			elif self.subtype == "hour5":
				hourData = hoursData[5]
			elif self.subtype == "hour6":
				hourData = hoursData[6]
			elif self.subtype == "hour7":
				hourData = hoursData[7]
			elif self.subtype == "hour8":
				hourData = hoursData[8]
			elif self.subtype == "hour9":
				hourData = hoursData[9]
			elif self.subtype == "hour10":
				hourData = hoursData[10]
			elif self.subtype == "hour11":
				hourData = hoursData[11]
			elif self.subtype == "hour12":
				hourData = hoursData[12]
			elif self.subtype == "hour13":
				hourData = hoursData[13]
			elif self.subtype == "hour14":
				hourData = hoursData[14]
			elif self.subtype == "hour15":
				hourData = hoursData[15]
			elif self.subtype == "hour16":
				hourData = hoursData[16]
			elif self.subtype == "hour17":
				hourData = hoursData[17]
			elif self.subtype == "hour18":
				hourData = hoursData[18]
			elif self.subtype == "hour19":
				hourData = hoursData[19]
			elif self.subtype == "hour20":
				hourData = hoursData[20]
			elif self.subtype == "hour21":
				hourData = hoursData[21]
			elif self.subtype == "hour22":
				hourData = hoursData[22]
			elif self.subtype == "hour23":
				hourData = hoursData[23]
			elif self.subtype == "hour24":
				hourData = hoursData[24]
			
			for d in self.dataToDisplay:
				self.dlog.debug("Creating " + d['name'])
				
				# TOP DATA
				if d['type'] == "topSummary":
					self.topSummaryFormat = d['format']
					self.topSummaryWidth = d['width']
					self.topSummary = Ut.createTextLabel(page, self.name, d)
					self.topSummary.setText(fill(self.topSummaryFormat.format(self.weatherData['summary']), width=self.topSummaryWidth))
					
				elif d['type'] == "topIcon":
					self.topIcon = Ut.createImageLabel(page, self.name, d)
					if self.weatherData['icon'] in self.supportedIcons:
						self.topIcon.setPixmap(QPixmap(self.images[self.weatherData['icon']]).scaled(self.topIcon.size().width(), self.topIcon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
					else:
						self.topIcon.setPixmap(QPixmap(self.images['default']).scaled(self.topIcon.size().width(), self.topIcon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
						
				# DATA BLOCKS
				elif d['type'] == "time":
					self.timeFormat = d['format']
					self.timeData = Ut.createTextLabel(page, self.name, d)
					hourTime = datetime.datetime.fromtimestamp(hourData['time'])
					self.timeData.setText(self.timeFormat.format(hourTime))
					
				elif d['type'] == "summary":
					self.summaryFormat = d['format']
					self.summaryWidth = d['width']
					self.summary = Ut.createTextLabel(page, self.name, d)
					self.summary.setText(fill(self.summaryFormat.format(hourData['summary']), width=self.summaryWidth))
					
				elif d['type'] == "icon":
					self.icon = Ut.createImageLabel(page, self.name, d)
					if hourData['icon'] in self.supportedIcons:
						self.icon.setPixmap(QPixmap(self.images[hourData['icon']]).scaled(self.icon.size().width(), self.icon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
					else:
						self.icon.setPixmap(QPixmap(self.images['default']).scaled(self.icon.size().width(), self.icon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
					
				elif d['type'] == "temperature":
					self.temperatureFormat = d['format']
					self.temperature = Ut.createTextLabel(page, self.name, d)
					self.temperature.setText(self.temperatureFormat.format(hourData['temperature']))
					
				elif d['type'] == "humidity":
					self.humidityFormat = d['format']
					self.humidity = Ut.createTextLabel(page, self.name, d)
					self.humidity.setText(self.humidityFormat.format(hourData['humidity']))
					
				elif d['type'] == "pressure":
					self.pressureFormat = d['format']
					self.pressure = Ut.createTextLabel(page, self.name, d)
					self.pressure.setText(self.pressureFormat.format(hourData['pressure']))
					
				elif d['type'] == "windSpeed":
					self.windSpeedFormat = d['format']
					self.windSpeed = Ut.createTextLabel(page, self.name, d)
					self.windSpeed.setText(self.windSpeedFormat.format(self.weatherData['windSpeed']))
					
				elif d['type'] == "windBearing":
					self.windBearingFormat = d['format']
					self.windBearing = Ut.createTextLabel(page, self.name, d)
					self.windBearing.setText(self.windBearingFormat.format(self.weatherData['windBearing']))
					
		elif self.type == "daily":
			self.weatherData = wObj.getDaily()
			daysData = self.weatherData['data']
			daysData.sort(key=operator.itemgetter('time'))
			
			if self.subtype == "day0":
				dayData = daysData[0]
			elif self.subtype == "day1":
				dayData = daysData[1]
			elif self.subtype == "day2":
				dayData = daysData[2]
			elif self.subtype == "day3":
				dayData = daysData[3]
			elif self.subtype == "day4":
				dayData = daysData[4]
			elif self.subtype == "day5":
				dayData = daysData[5]
			elif self.subtype == "day6":
				dayData = daysData[6]
			elif self.subtype == "day7":
				dayData = daysData[7]
				
			for d in self.dataToDisplay:
				self.dlog.debug("Creating " + d['name'])
				
				# TOP DATA
				if d['type'] == "topSummary":
					self.topSummaryFormat = d['format']
					self.topSummaryWidth = d['width']
					self.topSummary = Ut.createTextLabel(page, self.name, d)
					self.topSummary.setText(fill(self.weatherData['summary'], width=self.topSummaryWidth))
					
				elif d['type'] == "topIcon":
					self.topIcon = Ut.createImageLabel(page, self.name, d)
					if self.weatherData['icon'] in self.supportedIcons:
						self.topIcon.setPixmap(QPixmap(self.images[self.weatherData['icon']]).scaled(self.topIcon.size().width(), self.topIcon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
					else:
						self.topIcon.setPixmap(QPixmap(self.images['default']).scaled(self.topIcon.size().width(), self.topIcon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
					
				# DATA BLOCKS
				elif d['type'] == "time":
					self.timeFormat = d['format']
					self.timeData = Ut.createTextLabel(page, self.name, d)
					dayTime = datetime.datetime.fromtimestamp(dayData['time'])
					self.timeData.setText(self.timeFormat.format(dayTime))
					
				elif d['type'] == "summary":
					self.summaryFormat = d['format']
					self.summaryWidth = d['width']
					self.summary = Ut.createTextLabel(page, self.name, d)
					self.summary.setText(fill(self.summaryFormat.format(dayData['summary']), width=self.summaryWidth))
					
				elif d['type'] == "icon":
					self.icon = Ut.createImageLabel(page, self.name, d)
					if dayData['icon'] in self.supportedIcons:
						self.icon.setPixmap(QPixmap(self.images[dayData['icon']]).scaled(self.icon.size().width(), self.icon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
					else:
						self.icon.setPixmap(QPixmap(self.images['default']).scaled(self.icon.size().width(), self.icon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
					
				elif d['type'] == "temperatureHigh":
					self.temperatureHighFormat = d['format']
					self.temperatureHigh = Ut.createTextLabel(page, self.name, d)
					self.temperatureHigh.setText(self.temperatureHighFormat.format(dayData['temperatureHigh']))
					
				elif d['type'] == "temperatureLow":
					self.temperatureLowFormat = d['format']
					self.temperatureLow = Ut.createTextLabel(page, self.name, d)
					self.temperatureLow.setText(self.temperatureLowFormat.format(dayData['temperatureLow']))
					
				elif d['type'] == "humidity":
					self.humidityFormat = d['format']
					self.humidity = Ut.createTextLabel(page, self.name, d)
					self.humidity.setText(self.humidityFormat.format(dayData['humidity']))
					
				elif d['type'] == "pressure":
					self.pressureFormat = d['format']
					self.pressure = Ut.createTextLabel(page, self.name, d)
					self.pressure.setText(self.pressureFormat.format(dayData['pressure']))
					
				elif d['type'] == "windSpeed":
					self.windSpeedFormat = d['format']
					self.windSpeed = Ut.createTextLabel(page, self.name, d)
					self.windSpeed.setText(self.windSpeedFormat.format(self.weatherData['windSpeed']))
					
				elif d['type'] == "windBearing":
					self.windBearingFormat = d['format']
					self.windBearing = Ut.createTextLabel(page, self.name, d)
					self.windBearing.setText(self.windBearingFormat.format(self.weatherData['windBearing']))
				
		
		# Start timer
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.update)
		self.timer.start(properties['interval']*1000)
