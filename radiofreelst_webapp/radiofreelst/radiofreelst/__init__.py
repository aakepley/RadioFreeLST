#!/usr/bin/python

from __future__ import division
from __future__ import print_function

import sys
import socket

from flask import Flask

from . import jinja_filters
from . import _app_setup_utils
from .utilities.color_print import print_warning, print_error, print_info, yellow_text, green_text, red_text

# ================================================================================

def register_blueprints(app=None):
	'''
	Register the code associated with each URL paths. Manually add each new
	controller file you create here.
	'''
	from .controllers.index import index_page
	#from .controllers.controller1 import xxx

	app.register_blueprint(index_page)
	#app.register_blueprint(xxx)

# ================================================================================

def create_app(debug=False, conf=dict()):
	
	app = Flask(__name__) # creates the app instance using the name of the module
	app.debug = debug

	# --------------------------------------------------
	# Read configuration files.
	# -------------------------
	# You can define a different configuration
	# file based on the host the app is running on.
	#
	# Configuration files are located in the "configuration_files" directory.
	# -----------------------------------------------------------------------
	server_config_file = None
	
	if app.debug:
		hostname = socket.gethostname()		
		if "your_host" in hostname:
			server_config_file = _app_setup_utils.getConfigFile("your_host.cfg")
		else:
			server_config_file = _app_setup_utils.getConfigFile("default.cfg") # default
		
	else:
		if conf["usingUWSGI"]:
			try:
				import uwsgi
				# The uWSGI configuration file defines a key value pair to point
				# to a particular configuration file in this module under "configuration_files".
				# The key is 'flask_config_file', and the value is the name of the configuration
				# file.
				server_config_file = _app_setup_utils.getConfigFile(uwsgi.opt['flask-config-file'])
			except ImportError:
				print("Trying to run in production mode, but not running under uWSGI.\n"
					  "You might try running again with the '--debug' (or '-d') flag.")
				sys.exit(1)
	
	if server_config_file:
		print(green_text("Loading config file: "), yellow_text(server_config_file))
		app.config.from_pyfile(server_config_file)
	
	# -----------------------------
	# Perform app setup below here.
	# -----------------------------
	
	if app.debug:
		#print("{0}App '{1}' created.{2}".format('\033[92m', __name__, '\033[0m'))
		print_info("Application '{0}' created.".format(__name__))
	else:
		if conf["usingSentry"]:
			_app_setup_utils.setupSentry(app, dsn=sentryDSN)

	# Change the implementation of "decimal" to a C-based version (much! faster)
	try:
		import cdecimal
		sys.modules["decimal"] = cdecimal
	except ImportError:
		pass # not available

	if conf["usingSQLAlchemy"]:
		if conf["usingPostgreSQL"]:
			_app_setup_utils.setupJSONandDecimal()
	
	    # This "with" is necessary to prevent exceptions of the form:
	    #    RuntimeError: working outside of application context
	    #    (i.e. the app object doesn't exist yet - being created here)
		
			with app.app_context():
				from .model.databasePostgreSQL import db

	# Register all paths (URLs) available.
	register_blueprints(app=app)

	# Register all Jinja filters in the file.
	app.register_blueprint(jinja_filters.blueprint)

	return app
	

	
	