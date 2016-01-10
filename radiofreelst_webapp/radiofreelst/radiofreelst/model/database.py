#!/usr/bin/python

''' This file handles a database connection. It can simply be deleted if not needed.
	
	The example given is for a PostgreSQL database, but can be modified for any other.
'''

import psycopg2

from ..config import AppConfig
from ..designpatterns import singleton

config = AppConfig()

@singleton
class MyApplicationDatabase(object):
	
	def __init__(self):
		self.pool = None
		
	def pool(self, release):
		''' Return the pool of database connections for the database connected. '''
	
		# -----------------------------------
		# Database connection setup & methods
		# -----------------------------------
		# Ref: http://initd.org/psycopg/docs/module.html
		# Ref: http://packages.python.org/psycopg2/pool.html#module-psycopg2.pool
		# dsn = data source name
		
		if self.pool is None:
			
			db_info = {}
			#for key in self.config.options(""):
			#	db_info[key] = config.
		
		return self.pool
		
	
	### etc. ###
	
	## TODO: create a sample db file for PostgreSQL, SQLite, and SQLAlchemy