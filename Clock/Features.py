import datetime, random, os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QColor, QFrame, QLabel, QMatrix, QPixmap

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
			
		#self.textLabel.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
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


class Text():
	
	def __init__(self, page, properties):
		return 0
		
	def setText():
		return 0
		
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


class Calendar():
	
	def __init__(self):
		
		self.credentials = self.getCredentials()
		
		http = self.credentials.authorize(httplib2.Http())
		self.service = discovery.build('calendar', 'v3', http=http)
			
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