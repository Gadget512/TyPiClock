import datetime, httplib2, json, random, os, operator
from textwrap import fill

from Utilities import Log

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
		
		self.clockface = properties['face']
		self.hourhand = properties['hour']
		self.minutehand = properties['minute']
		self.secondhand = properties['second'] # May be None (null)
		
		# Create new frame on page for clock
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
			self.second = QLabel(page) # create label on page
			self.second.setObjectName(properties['name']+"second") # name label
			self.second.setStyleSheet("#"+properties['name']+"second { background-color: transparent; }")
			self.secpixmap = QPixmap(self.secondhand) # create pixmap with image
			
		# Set up minute hand
		self.minute = QLabel(page) # create label on page
		self.minute.setObjectName(properties['name']+"minute") # name label
		self.minute.setStyleSheet("#"+properties['name']+"minute { background-color: transparent; }")
		self.minpixmap = QPixmap(self.minutehand) # create pixmap with image
		
		# Set up hour hand
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
		
		self.textFormat = properties['format']
		
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
		self.textLabel = QLabel(page)
		self.textLabel.setObjectName(properties['name'])
		self.textLabel.setStyleSheet("#"+properties['name']+"{ font-family:"+properties['font']+"; color: "+
			properties['color'] + "; background-color: transparent; font-size: "+
			properties['fontsize']+"px; "+
			properties['fontattr']+"}")
			
		if properties['alignment'] == 1:
			self.textLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)
		elif properties['alignment'] == 2:
			self.textLabel.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
		elif properties['alignment'] == 3:
			self.textLabel.setAlignment(Qt.AlignRight | Qt.AlignTop)
		elif properties['alignment'] == 4:
			self.textLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
		elif properties['alignment'] == 5:
			self.textLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		elif properties['alignment'] == 6:
			self.textLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		elif properties['alignment'] == 7:
			self.textLabel.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
		elif properties['alignment'] == 8:
			self.textLabel.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
		elif properties['alignment'] == 9:
			self.textLabel.setAlignment(Qt.AlignRight | Qt.AlignBottom)
		
		self.textLabel.setGeometry(properties['location'][0], properties['location'][1], properties['location'][2], properties['location'][3])
		
		# Set the text effect, if specified
		for effect in properties['effects']:
			if effect['type'] == "glow":
				textEffect = QtGui.QGraphicsDropShadowEffect()
				textEffect.setOffset(0)
				textEffect.setBlurRadius(effect['typeattr']['radius'])
				textEffect.setColor(QColor(effect['typeattr']['color']))
				self.textLabel.setGraphicsEffect(textEffect)
				
			elif effect['type'] == "shadow":
				textEffect = QtGui.QGraphicsDropShadowEffect()
				textEffect.setOffset(effect['typeattr']['offset'])
				textEffect.setBlurRadius(effect['typeattr']['blur'])
				textEffect.setColor(QColor(effect['typeattr']['color']))
				self.textLabel.setGraphicsEffect(textEffect)
		
		# Display text
		now = datetime.datetime.now()
		text = self.textFormat.format(now)
		self.textLabel.setText(text)
		
		# Start timer
		self.timer = QtCore.QTimer() # QTimer calls the specified function every specified number of milliseconds (parallel?)
		self.timer.timeout.connect(self.tick)
		self.timer.start(properties['interval']*1000)


class Text(): # TODO
	
	def __init__(self, page, properties):
		return 0
		
	def setText():
		return 0
		
class Image():
	
	def __init__(self, page, properties):
		
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
			self.dlog.info("Requesting weather...")
			self.weatherReply = self.http.request(self.weatherURI)
			
			self.dlog.debug("Updating lastUpdated")
			self.lastUpdated = datetime.datetime.now()
		except:
			self.dlog.error("Error requesting weather update!")
		finally:
			pass
			
		# Get Weather Data
		try:
			self.dlog.debug("Parsing weather")
			self.weatherHeader = self.weatherReply[0]
			if self.weatherHeader['status'] == '200':
				self.dlog.info("Weather Response Code: " + self.weatherHeader['status'])
				self.weatherData = json.loads(self.weatherReply[1])
			else:
				self.dlog.warning("Weather Response Code: " + self.weatherHeader['status'])
		except:
			self.dlog.error("Error getting weather data!")
		
		# TODO not needed?
		"""
		dataFile = open(self.weatherFile, 'w')
		dataFile.write(self.weatherReply)
		dataFile.close()
		"""
	
	def __init__(self, properties, latlng):
		
		self.dlog = Log(name = "Weather()", level="debug")
		self.http = httplib2.Http()
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
				# TODO
			
			# Wind Bearing
				# TODO
				
		# MINUTELY
		elif self.type == "minutely":
			self.weatherData = self.wObj.getMinutely()
			# TODO
		
		# HOURLY
		elif self.type == "hourly":
			self.weatherData = self.wObj.getHourly()
			
			# Top Summary
			if self.topSummary:
				self.topSummary.setText(fill(self.topSummaryFormat.format(self.weatherData['summary']), width=self.topSummaryWidth))
				
			# TODO
		
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
				# TODO
				
			# Wind Bearing
				# TODO
				
		
	def __init__(self, page, properties, wObj):
		
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
		# TODO effects
		if self.type == "lastUpdated":
			for d in self.dataToDisplay:
				if d['type'] == "lastUpdated":
					self.lastUpdatedFormat = d['format']
					self.lastUpdated = QLabel(page)
					self.lastUpdated.setObjectName(self.name+d['name'])
					self.lastUpdated.setStyleSheet("#"+self.name+d['name']+"{ font-family:"+d['font']+"; color: "+
					d['color'] + "; background-color: transparent; font-size: "+
					d['fontsize']+"px; "+
					d['fontattr']+"}")
					self.lastUpdated.setAlignment(self.align(d['alignment']))
					self.lastUpdated.setText(self.lastUpdatedFormat.format(self.wObj.getLastUpdated()))
					self.lastUpdated.setGeometry(d['location'][0], d['location'][1], d['location'][2], d['location'][3])
		
		elif self.type == "currently":
			self.weatherData = wObj.getCurrently()
			for d in self.dataToDisplay:
				if d['type'] == "summary":
					self.summaryFormat = d['format']
					self.summaryWidth = d['width']
					self.summary = QLabel(page)
					self.summary.setObjectName(self.name+d['name'])
					self.summary.setStyleSheet("#"+self.name+d['name']+"{ font-family:"+d['font']+"; color: "+
					d['color'] + "; background-color: transparent; font-size: "+
					d['fontsize']+"px; "+
					d['fontattr']+"}")
					self.summary.setAlignment(self.align(d['alignment']))
					self.summary.setText(fill(self.summaryFormat.format(self.weatherData['summary']), width=self.summaryWidth))
					self.summary.setGeometry(d['location'][0], d['location'][1], d['location'][2], d['location'][3])
				
				elif d['type'] == "icon":
					self.icon = QLabel(page)
					self.icon.setObjectName(self.name+d['name'])
					self.icon.setStyleSheet("#"+self.name+d['name']+" { background-color: transparent; }")
					self.icon.setGeometry(d['location'][0], d['location'][1], d['location'][2], d['location'][3])
					if self.weatherData['icon'] in self.supportedIcons:
						self.icon.setPixmap(QPixmap(self.images[self.weatherData['icon']]).scaled(self.icon.size().width(), self.icon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
					else:
						self.icon.setPixmap(QPixmap(self.images['default']).scaled(self.icon.size().width(), self.icon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
					
				elif d['type'] == "temperature":
					self.temperatureFormat = d['format']
					self.temperature = QLabel(page)
					self.temperature.setObjectName(self.name+d['name'])
					self.temperature.setStyleSheet("#"+self.name+d['name']+"{ font-family:"+d['font']+"; color: "+
					d['color'] + "; background-color: transparent; font-size: "+
					d['fontsize']+"px; "+
					d['fontattr']+"}")
					self.temperature.setAlignment(self.align(d['alignment']))
					self.temperature.setText(self.temperatureFormat.format(self.weatherData['temperature']))
					self.temperature.setGeometry(d['location'][0], d['location'][1], d['location'][2], d['location'][3])
					
				elif d['type'] == "apparentTemperature":
					self.apparentTemperatureFormat = d['format']
					self.apparentTemperature = QLabel(page)
					self.apparentTemperature.setObjectName(self.name+d['name'])
					self.apparentTemperature.setStyleSheet("#"+self.name+d['name']+"{ font-family:"+d['font']+"; color: "+
					d['color'] + "; background-color: transparent; font-size: "+
					d['fontsize']+"px; "+
					d['fontattr']+"}")
					self.apparentTemperature.setAlignment(self.align(d['alignment']))
					self.apparentTemperature.setText(self.apparentTemperatureFormat.format(self.weatherData['apparentTemperature']))
					self.apparentTemperature.setGeometry(d['location'][0], d['location'][1], d['location'][2], d['location'][3])
					
				elif d['type'] == "humidity":
					self.humidityFormat = d['format']
					self.humidity = QLabel(page)
					self.humidity.setObjectName(self.name+d['name'])
					self.humidity.setStyleSheet("#"+self.name+d['name']+"{ font-family:"+d['font']+"; color: "+
					d['color'] + "; background-color: transparent; font-size: "+
					d['fontsize']+"px; "+
					d['fontattr']+"}")
					self.humidity.setAlignment(self.align(d['alignment']))
					self.humidity.setText(self.humidityFormat.format(self.weatherData['humidity']))
					self.humidity.setGeometry(d['location'][0], d['location'][1], d['location'][2], d['location'][3])
					
				elif d['type'] == "pressure":
					self.pressureFormat = d['format']
					self.pressure = QLabel(page)
					self.pressure.setObjectName(self.name+d['name'])
					self.pressure.setStyleSheet("#"+self.name+d['name']+"{ font-family:"+d['font']+"; color: "+
					d['color'] + "; background-color: transparent; font-size: "+
					d['fontsize']+"px; "+
					d['fontattr']+"}")
					self.pressure.setAlignment(self.align(d['alignment']))
					self.pressure.setText(self.pressureFormat.format(self.weatherData['pressure']))
					self.pressure.setGeometry(d['location'][0], d['location'][1], d['location'][2], d['location'][3])
					
				elif d['type'] == "windSpeed":
					self.windSpeed = QLabel(page)
					# TODO
					
				elif d['type'] == "windBearing":
					self.windBearing = QLabel(page)
					# TODO
					
		elif self.type == "minutely":
			self.weatherData = wObj.getMinutely()
			# TODO
			
		elif self.type == "hourly":
			self.weatherData = wObj.getHourly()
			for d in self.dataToDisplay:
				if d['type'] == "topSummary":
					self.topSummaryFormat = d['format']
					self.topSummaryWidth = d['width']
					self.topSummary = QLabel(page)
					self.topSummary.setObjectName(self.name+d['name'])
					self.topSummary.setStyleSheet("#"+self.name+d['name']+"{ font-family:"+d['font']+"; color: "+
					d['color'] + "; background-color: transparent; font-size: "+
					d['fontsize']+"px; "+
					d['fontattr']+"}")
					self.topSummary.setAlignment(self.align(d['alignment']))
					self.topSummary.setText(fill(self.topSummaryFormat.format(self.weatherData['summary']), width=self.topSummaryWidth))
					self.topSummary.setGeometry(d['location'][0], d['location'][1], d['location'][2], d['location'][3])
					
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
				# TOP DATA
				if d['type'] == "topSummary":
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
					
				elif d['type'] == "topIcon":
					self.topIcon = QLabel(page)
					self.topIcon.setObjectName(self.name+d['name'])
					self.topIcon.setStyleSheet("#"+self.name+d['name']+" { background-color: transparent; }")
					self.topIcon.setGeometry(d['location'][0], d['location'][1], d['location'][2], d['location'][3])
					if self.weatherData['icon'] in self.supportedIcons:
						self.topIcon.setPixmap(QPixmap(self.images[self.weatherData['icon']]).scaled(self.topIcon.size().width(), self.topIcon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
					else:
						self.topIcon.setPixmap(QPixmap(self.images['default']).scaled(self.topIcon.size().width(), self.topIcon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
					
				# DATA BLOCKS
				elif d['type'] == "time":
					self.timeFormat = d['format']
					self.timeData = QLabel(page)
					self.timeData.setObjectName(self.name+d['name'])
					self.timeData.setStyleSheet("#"+self.name+d['name']+"{ font-family:"+d['font']+"; color: "+
					d['color'] + "; background-color: transparent; font-size: "+
					d['fontsize']+"px; "+
					d['fontattr']+"}")
					self.timeData.setAlignment(self.align(d['alignment']))
					dayTime = datetime.datetime.fromtimestamp(dayData['time'])
					self.timeData.setText(self.timeFormat.format(dayTime))
					self.timeData.setGeometry(d['location'][0], d['location'][1], d['location'][2], d['location'][3])
					
				elif 	d['type'] == "summary":
					self.summaryFormat = d['format']
					self.summaryWidth = d['width']
					self.summary = QLabel(page)
					self.summary.setObjectName(self.name+d['name'])
					self.summary.setStyleSheet("#"+self.name+d['name']+"{ font-family:"+d['font']+"; color: "+
					d['color'] + "; background-color: transparent; font-size: "+
					d['fontsize']+"px; "+
					d['fontattr']+"}")
					self.summary.setAlignment(self.align(d['alignment']))
					self.summary.setText(fill(self.summaryFormat.format(dayData['summary']), width=self.summaryWidth))
					self.summary.setGeometry(d['location'][0], d['location'][1], d['location'][2], d['location'][3])
					
				elif d['type'] == "icon":
					self.icon = QLabel(page)
					self.icon.setObjectName(self.name+d['name'])
					self.icon.setStyleSheet("#"+self.name+d['name']+" { background-color: transparent; }")
					self.icon.setGeometry(d['location'][0], d['location'][1], d['location'][2], d['location'][3])
					if self.weatherData['icon'] in self.supportedIcons:
						self.icon.setPixmap(QPixmap(self.images[dayData['icon']]).scaled(self.icon.size().width(), self.icon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
					else:
						self.icon.setPixmap(QPixmap(self.images['default']).scaled(self.icon.size().width(), self.icon.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
					
				elif d['type'] == "temperatureHigh":
					self.temperatureHighFormat = d['format']
					self.temperatureHigh = QLabel(page)
					self.temperatureHigh.setObjectName(self.name+d['name'])
					self.temperatureHigh.setStyleSheet("#"+self.name+d['name']+"{ font-family:"+d['font']+"; color: "+
					d['color'] + "; background-color: transparent; font-size: "+
					d['fontsize']+"px; "+
					d['fontattr']+"}")
					self.temperatureHigh.setAlignment(self.align(d['alignment']))
					self.temperatureHigh.setText(self.temperatureHighFormat.format(dayData['temperatureHigh']))
					self.temperatureHigh.setGeometry(d['location'][0], d['location'][1], d['location'][2], d['location'][3])
					
				elif d['type'] == "temperatureLow":
					self.temperatureLowFormat = d['format']
					self.temperatureLow = QLabel(page)
					self.temperatureLow.setObjectName(self.name+d['name'])
					self.temperatureLow.setStyleSheet("#"+self.name+d['name']+"{ font-family:"+d['font']+"; color: "+
					d['color'] + "; background-color: transparent; font-size: "+
					d['fontsize']+"px; "+
					d['fontattr']+"}")
					self.temperatureLow.setAlignment(self.align(d['alignment']))
					self.temperatureLow.setText(self.temperatureLowFormat.format(dayData['temperatureLow']))
					self.temperatureLow.setGeometry(d['location'][0], d['location'][1], d['location'][2], d['location'][3])
					
				elif d['type'] == "humidity":
					self.humidityFormat = d['format']
					self.humidity = QLabel(page)
					self.humidity.setObjectName(self.name+d['name'])
					self.humidity.setStyleSheet("#"+self.name+d['name']+"{ font-family:"+d['font']+"; color: "+
					d['color'] + "; background-color: transparent; font-size: "+
					d['fontsize']+"px; "+
					d['fontattr']+"}")
					self.humidity.setAlignment(self.align(d['alignment']))
					self.humidity.setText(self.humidityFormat.format(dayData['humidity']))
					self.humidity.setGeometry(d['location'][0], d['location'][1], d['location'][2], d['location'][3])
					
				elif d['type'] == "pressure":
					self.pressureFormat = d['format']
					self.pressure = QLabel(page)
					self.pressure.setObjectName(self.name+d['name'])
					self.pressure.setStyleSheet("#"+self.name+d['name']+"{ font-family:"+d['font']+"; color: "+
					d['color'] + "; background-color: transparent; font-size: "+
					d['fontsize']+"px; "+
					d['fontattr']+"}")
					self.pressure.setAlignment(self.align(d['alignment']))
					self.pressure.setText(self.pressureFormat.format(dayData['pressure']))
					self.pressure.setGeometry(d['location'][0], d['location'][1], d['location'][2], d['location'][3])
					
				elif d['type'] == "windSpeed":
					self.windSpeed = QLabel(page)
					# TODO
					
				elif d['type'] == "windBearing":
					self.windBearing = QLabel(page)
					# TODO
				
		
		# Start timer
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.update)
		self.timer.start(properties['interval']*1000)
		
	def align(self, a):
		# TODO move to Utils?
		if a == 1:
			return (Qt.AlignLeft | Qt.AlignTop)
		elif a == 2:
			return (Qt.AlignHCenter | Qt.AlignTop)
		elif a == 3:
			return (Qt.AlignRight | Qt.AlignTop)
		elif a == 4:
			return (Qt.AlignLeft | Qt.AlignVCenter)
		elif a == 5:
			return (Qt.AlignHCenter | Qt.AlignVCenter)
		elif a == 6:
			return (Qt.AlignRight | Qt.AlignVCenter)
		elif a == 7:
			return (Qt.AlignLeft | Qt.AlignBottom)
		elif a == 8:
			return (Qt.AlignHCenter | Qt.AlignBottom)
		elif a == 9:
			return (Qt.AlignRight | Qt.AlignBottom)
