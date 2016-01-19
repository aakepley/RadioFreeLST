#!/usr/bin/python

from .DatabaseConnection import DatabaseConnection

from datetime import datetime
import ephem
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, relation, exc, column_property, validates
from sqlalchemy import orm
from sqlalchemy.orm.session import Session
from astropy.coordinates import UnitSphericalRepresentation
import astropy.units as u

dbc = DatabaseConnection()

# ========================
# Define database classes
# ========================
Base = declarative_base(bind=dbc.engine)

class Observatory(Base):
	
	__tablename__ = 'observatory'
	__table_args__ = {'autoload' : True, 'schema' : 'radiofreelst'}

	def __init__(self):
		self._location = None
		self._observer = None
	
	# Ref: http://docs.sqlalchemy.org/en/latest/orm/constructors.html
	@orm.reconstructor
	def init_on_load(self):
		self._location = None
		self._observer = None
		
	@property
	def observer(self, date=None):
		''' This is a PyEphem object representing this observatory. '''
		if self._observer is None:
			if date is None:
				# default date is now
				date = datetime.now() # TODO set date string from this below
	
			observer = ephem.Observer()
			#observer.lat = self.latitude_deg # "38:25:59.236"
			#observer.lon = self.longitude_deg # "-79:50:23.406" # negative sign because west
			
			# lat, lon must be in DMS, HMS format, respectively
			observer.lat = "{0[0]:02.0f}:{0[1]:02.0f}:{0[2]:.4f}".format(self.location.lat.dms)
			observer.lon = "{0[0]:02.0f}:{0[1]:02.0f}:{0[2]:.4f}".format(self.location.lat.hms)
			
			print("observer: {0} {1}".format(observer.lat, observer.lon))
			
			observer.elevation = self.elevation # 807.43 # m
			observer.date = "{0.year}/{0.month:02d}/{0.day:02d}".format(date) # "2015/10/1" # This date is arbitrary and shouldn't matter
			
			if self.horizon_limit_lower:
				observer.horizon = ephem.degrees(str(self.horizon_limit_lower)) # for some reason, the argument has to be a string
			else:
				observer.horizon = "30"
				
			self._observer = observer
			
		return self._observer

	@property
	def location(self):
		if self._location is None:
			self._location = UnitSphericalRepresentation(lat=self.latitude_deg * u.deg, lon=self.longitude_deg * u.deg)
		return self._location
	
# =========================
# Define relationships here
# =========================

# no relationships