#!/usr/bin/python

from .DatabaseConnection import DatabaseConnection

import datetime
import ephem
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, relation, exc, column_property, validates
from sqlalchemy import orm
from sqlalchemy.orm.session import Session

dbc = DatabaseConnection()

# ========================
# Define database classes
# ========================
Base = declarative_base(bind=dbc.engine)

class Observatory(Base):
	
	__tablename__ = 'observatory'
	__table_args__ = {'autoload' : True}

	def observer(self, date=None):
		''' This is a PyEphem object representing this observatory. '''
		if date is None:
			# default date is now
			date = datetime.now() # TODO set date string from this below

		observer = ephem.Observer()
    # GBT data from proposer's guide
    observer.lon = self.longitude # "-79:50:23.406" # negative sign because west
    observer.lat = self.latitude # "38:25:59.236"  
    observer.elevation = self.elevation # 807.43 # m
    observer.date = "2015/10/1" # This date is arbitrary and shouldn't matter
    observer.horizon = ephem.degrees(str(horizon)) # for some reason, the argument has to be a string
		
		return observer
	
# =========================
# Define relationships here
# =========================

# no relationships