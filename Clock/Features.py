import datetime
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

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
				QtGui.QMatrix().scale(
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
			QtGui.QMatrix().scale(
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
			QtGui.QMatrix().scale(
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
	
	def __init__(self, page, clockName, images, coords):
	
		self.secondhand = None
		self.clockface = images[0]
		self.hourhand = images[1]
		self.minutehand = images[2]
		self.secondhand = images[3] # May be None (null)
		
		# Create new frame on page for clock
		self.clockFrame = QtGui.QFrame(page)
		self.clockFrame.setObjectName(clockName)
		# specify (x, y, w, h) where x,y is the top-left corner, w is the width, h is the height
		self.clockFrameRect = QtCore.QRect(coords[0],  coords[1],  coords[2], coords[3])
		
		# Display clock background
		self.clockFrame.setGeometry(self.clockFrameRect)
		self.clockFrame.setStyleSheet("#"+clockName+" { background-color: transparent; border-image: url("+self.clockface+") 0 0 0 0 stretch stretch;}")
		
		# Set up second hand
		self.second = None
		self.secpixmap = None
		if self.secondhand:
			self.second = QtGui.QLabel(page) # create label on page
			self.second.setObjectName(clockName+"second") # name label
			self.second.setStyleSheet("#"+clockName+"second { background-color: transparent; }")
			self.secpixmap = QtGui.QPixmap(self.secondhand) # create pixmap with image
			
		# Set up minute hand
		self.minute = QtGui.QLabel(page) # create label on page
		self.minute.setObjectName(clockName+"minute") # name label
		self.minute.setStyleSheet("#"+clockName+"minute { background-color: transparent; }")
		self.minpixmap = QtGui.QPixmap(self.minutehand) # create pixmap with image
		
		# Set up hour hand
		self.hour = QtGui.QLabel(page) # create label on page
		self.hour.setObjectName(clockName+"hour") # name label
		self.hour.setStyleSheet("#"+clockName+"hour { background-color: transparent; }")
		self.hourpixmap = QtGui.QPixmap(self.hourhand) # create pixmap with image
		
		# Start clock
		self.ctimer = QtCore.QTimer() # QTimer calls the specified function every specified number of milliseconds (parallel?)
		self.ctimer.timeout.connect(self.tick)
		self.ctimer.start(1000)
	
	
class DigitalClock():
	
	def __init__(self): # TODO NO IDEA WHAT THIS DOES
		
		now = datetime.datetime.now()
		
		clockface = QtGui.QLabel(frame1)
		clockface.setObjectName("clockface")
		clockrect = QtCore.QRect(
			width / 2 - height * .4,
			height * .45 - height * .4,
			height * .8,
			height * .8)
			
		clockface.setGeometry(clockrect)
		#dcolor = QColor(Config.digitalcolor).darker(0).name()
		#lcolor = QColor(Config.digitalcolor).lighter(120).name()
		dcolor = QColor("#50CBEB").darker(0).name()
		lcolor = QColor("#50CBEB").lighter(120).name()
		
		clockface.setStyleSheet(
			"#clockface { background-color: transparent; font-family:sans-serif;" +
			" font-weight: light; color: " +
			lcolor +
			"; background-color: transparent; font-size: " +
			str(int(Config.digitalsize * xscale)) +
			"px; " +
			Config.fontattr +
			"}")
		clockface.setAlignment(Qt.AlignCenter)
		clockface.setGeometry(clockrect)
		glow = QtGui.QGraphicsDropShadowEffect()
		glow.setOffset(0)
		glow.setBlurRadius(50)
		glow.setColor(QColor(dcolor))
		clockface.setGraphicsEffect(glow)
		
		#timestr = Config.digitalformat.format(now)
		timestr = "{0:%I:%M\n%S %p}".format(now)
		if Config.digitalformat.find("%I") > -1:
			if timestr[0] == '0':
				timestr = timestr[1:99]
		if lasttimestr != timestr:
			clockface.setText(timestr.lower())
		lasttimestr = timestr


class DateTime():
	
	def tick():
		return 0
	
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
		
		now = datetime.datetime.now()
		
		self.textLabel = QtGui.QLabel(page)
		self.textLabel.setObjectName(properties['name'])
		self.textLabel.setStyleSheet("#"+properties['name']+" font-family:"+properties['font']+"; color: "+
			properties['color'] + "; background-color: transparent; fontsize: "+
			properties['fontsize']+"px; "+
			properties['fontattr']+"}")
			
		self.textLabel.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
		self.textLabel.setGeometry(0,0, 1920, 100) # TODO *********************
		
		text = properties['format'].format(now)
		self.textLabel.setText(text)
		
		
		"""
		# ---------------------------------------------------------------------
		# I think this goes here
		datex = QtGui.QLabel(frame1)
		datex.setObjectName("datex")
		datex.setStyleSheet("#datex { font-family:sans-serif; color: " +
			Config.textcolor +
			"; background-color: transparent; font-size: " +
			str(int(50 * xscale)) +
			"px; " +
			Config.fontattr +
			"}")
		datex.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
		datex.setGeometry(0, 0, width, 100)

		datex2 = QtGui.QLabel(frame2)
		datex2.setObjectName("datex2")
		datex2.setStyleSheet("#datex2 { font-family:sans-serif; color: " +
			Config.textcolor +
			"; background-color: transparent; font-size: " +
			str(int(50 * xscale)) + "px; " +
			Config.fontattr +
			"}")
		datex2.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
		datex2.setGeometry(800 * xscale, 780 * yscale, 640 * xscale, 100)
		
		datey2 = QtGui.QLabel(frame2)
		datey2.setObjectName("datey2")
		datey2.setStyleSheet("#datey2 { font-family:sans-serif; color: " +
			Config.textcolor +
			"; background-color: transparent; font-size: " +
			str(int(50 * xscale)) +
			"px; " +
			Config.fontattr +
			"}")
		datey2.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
		datey2.setGeometry(800 * xscale, 840 * yscale, 640 * xscale, 100)
		# ---------------------------------------------------------------------------
		
		dy = "{0:%I:%M %p}".format(now)
		if dy != pdy:
			pdy = dy
			datey2.setText(dy)

		if now.day != lastday:
			lastday = now.day
			# date
			sup = 'th'
			if (now.day == 1 or now.day == 21 or now.day == 31):
				sup = 'st'
			if (now.day == 2 or now.day == 22):
				sup = 'nd'
			if (now.day == 3 or now.day == 23):
				sup = 'rd'
			if Config.DateLocale != "":
				sup = ""
			ds = "{0:%A %B} {0.day}<sup>{1}</sup> {0.year}".format(now, sup)
			datex.setText(ds)
			datex2.setText(ds)
		"""


class Text():
	
	def __init__(self):
		return 0


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