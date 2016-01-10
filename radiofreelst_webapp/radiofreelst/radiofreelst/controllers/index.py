#!/usr/bin/python

import os

import flask
import ephem
#from flask import request, render_template, send_from_directory
from flask import current_app, render_template, request
from . import valueFromRequest
from ..code.radiofreelst import Source, findLST
#from ..model.ModelClasses import Observatory

index_page = flask.Blueprint("index_page", __name__)

@index_page.route("/")
@index_page.route("/lst", methods=['GET'])
def index():
	''' Index page. '''
	
	templateDict = {}

	observatory = valueFromRequest(key="observatory", request=request, default=None)
	horizon = valueFromRequest(key="observatory_horizon", request=request, default="30")

	single_target_name = valueFromRequest(key="single_target_name", request=request, default=None)
	single_target_ra = valueFromRequest(key="single_target_ra", request=request, default=None)
	single_target_dec = valueFromRequest(key="single_target_dec", request=request, default=None)

	mode = valueFromRequest(key="mode", request=request, default=None)

	# defaults
	# --------
#	if observatory is None:
#		observatory = "GBT"

	# ------------------------------------
	# Hard code observatory for the moment
	# ------------------------------------
	observatory = ephem.Observer()

	# GBT data from proposer's guide
	observatory.lon =  "-79:50:23.406" # negative sign because west
	observatory.lat = "38:25:59.236"  
	observatory.elevation =  807.43 # m
	observatory.date = "2015/10/1" # This date is arbitrary and shouldn't matter
	observatory.horizon = ephem.degrees(horizon) # for some reason, the argument has to be a string
	# ------------------------------------

	if mode == "single_target":
		source = Source()
		source.ra = single_target_ra
		source.dec = single_target_dec
		source.name = "target name"
		
		sourceList = [source]
		
		findLST(observatory, sourceList)

		templateDict["sourceList"] = sourceList;
	
	return render_template("index.html", **templateDict)

# This will provide the favicon for the whole site. Can be overridden for
# a single page with something like this on the page:
#    <link rel="shortcut icon" href="static/images/favicon.ico">
#
@index_page.route('/favicon.ico')
def favicon():
	static_images_dir = directory=os.path.join(app.root_path, 'static', 'images')
	return send_from_directory(static_images_dir, filename='favicon.ico')#, mimetype='image/vnd.microsoft.icon')

@index_page.route('/robots.txt')
def robots():
	robots_path = os.path.join(current_app.root_path, 'static')
	return send_from_directory(robots_path, "robots.txt")
