A Flask Application Template
============================

Copying the template
--------------------

Make a copy of this repository and run:

    % /bin/bash rename_this_app.sh NEW_NAME

to change filenames, paths, and statements inside from "radiofreelst"
to a new name of your choice.

Python Dependendies
-------------------

Make sure that [Flask](https://pypi.python.org/pypi/Flask/) is installed:

    % sudo pip install Flask
    
If you are using the [Anaconda Python distribution](http://www.continuum.io), Flask is already installed; you can make sure you are running the current version with:

    % conda update flask

DMFlaskTemplate has these Python dependencies:

 * [uWSGI](https://pypi.python.org/pypi/uWSGI) (if planning to deploy under Nginx)
 * [SQLAlchemy](http://www.sqlalchemy.org)
 * [psycopg2](https://pypi.python.org/pypi/psycopg2) (if using PostgreSQL)
 * [termcolor](https://pypi.python.org/pypi/termcolor) (for color printing while debugging)
 
If you plan to incoporate Sentry for production logging, add these:

 * [raven](https://pypi.python.org/pypi/raven)
 * [blinker](https://pypi.python.org/pypi/blinker)

Run the application in debug mode
---------------------------------

From inside the top level directory, start the app from the command line:

    % ./run_radiofreelst.py -d

Add new pages
-------------

* Create a new file in the `controller` directory.
* Add the name of the file to the `all` list in `controllers/__init__.py`
* Add a new template for the page as needed in `templates`.

The `@app.route('/')` decorator defines the URL. To create a page
at `http://your.domain.com/somePage`, the decorator would be

    @app.route('/somePage')
    
The decorated function immediately below that will typically have the same
name as the page, but it doesn't have to. The decorator just binds the function
to the name that it’s given.

Controllers or views?
---------------------

Flask calls the code that takes HTTP requests and returns HTML responses
"views". In the [MVC](http://en.wikipedia.org/wiki/Model–view–controller) design pattern
(which Flask clearly follows), these parts of the code are called
"controllers". In MVC, the HTML responses are actually the views, so this is
terribly confusing. That is why the folder that contains the Python
code is called `controllers`. Just so you know.

Typically, there will be one controller file per web page, but this is not required.

Configuration Files
-------------------
There are two levels of configuration files that I use:

 * site-specific configuration files
 * app-level configuration files
 
I recommend creating a configuration file for each server that the app will be run on. It’s handy to keep all such files in the app module so they can be tracked under version control. You will then need to know which configuration file to choose at run time.

I'm assuming the application will be served under uWSGI. At the top level of the app I’ve made a `uwsgi_configuration_files` directory which will contain the uWSGI startup configuration for each server. This is an example:

	[uwsgi]
	base = /var/www/myapp
	socket = /tmp/uwsgi_myappi.sock
	chmod-socket = 666
	master = true
	sharedarea = 4
	memory-report = true
	daemonize = %(base)/uwsgi_myapp.log
	pidfile = %(base)/uwsgi_myapp.pid
	file = %(base)/run_myapp.py
	callable = app
	module = myapp
	
	# This key/value will be read in the Flask application
	# to indicate which server the application is running on.
	# Don't add more server-specific options here; place them
	# in the sdssapi/server_config_files files.
	
	flask-config-file = myserver.cfg

Rather than place all of the parameters for the Flask app for the site in this file (which would be messy), only define a custom parameter that contains the name of the configuration file for that site. This file will then be found in the folder `configuration_files` in the Flask app package.

To determine at runtime which configuration file to load:

    try:
        import uwsgi
        server_conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
									     'configuration_files',
									     uwsgi.opt['flask-config-file'])
	except ImportError:
		print_error("Trying to run in production mode, but not running under uWSGI.\n"
				   "You might try running again with the '--debug' flag.")
		sys.exit(1)

Calling `import uwsgi` is a way to tell if the app is being served from uWSGI.

References:

<https://uwsgi-docs.readthedocs.org/en/latest/Configuration.html#placeholders>  
<http://uwsgi-docs.readthedocs.org/en/latest/PythonModule.html#uwsgi.opt>







