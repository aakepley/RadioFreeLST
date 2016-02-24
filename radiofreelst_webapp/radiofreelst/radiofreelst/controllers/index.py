#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from datetime import datetime

import flask
import ephem
from astropy.coordinates import SkyCoord, ICRS
#from flask import request, render_template, send_from_directory
from flask import current_app, render_template, request
from . import valueFromRequest
from ..code.radiofree import Source, findLST

from ..model.databasePostgreSQL import db
from ..model.ModelClasses import Observatory

index_page = flask.Blueprint("index_page", __name__)

@index_page.route("/")
@index_page.route("/lst", methods=['GET'])
def index():
	''' Index page. '''
	
	templateDict = {}

	# default form values (don't use the " character here without escaping it)
	single_target_form_value_name = "M31"
	single_target_form_value_ra = "00h 42m 44.3s"
	single_target_form_value_dec = unicode("41° 16′ 9\"", 'utf-8')

	# Fetch full list of observatories from database.
	session = db.Session()
	observatories = session.query(Observatory).order_by(Observatory.name).all()
	templateDict["observatories"] = observatories

	selected_obs_short_name = valueFromRequest(key="observatory", request=request, default=None)
	horizon = valueFromRequest(key="observatory_horizon", request=request, default="30")

	# Possible modes: "single_target", "multiple_target", None = initial page load
	mode = valueFromRequest(key="mode", request=request, default=None)

	source_list = list()

	# if observatory has been selected, retain selection
	if selected_obs_short_name is not None:
		templateDict["selectedObservatory"] = selected_obs_short_name
		
	# At the end of this block, the source list (if given) should be built.
	# This will be an array of Source objects.
	if mode == "single_target":
		single_target_name = valueFromRequest(key="single_target_name", request=request, default=None)
		single_target_ra = valueFromRequest(key="single_target_ra", request=request, default=None)
		single_target_dec = valueFromRequest(key="single_target_dec", request=request, default=None)
		
		# ratain form values
		if single_target_name is not None:
			single_target_form_value_name = single_target_name
		if single_target_form_value_ra is not None:
			single_target_form_value_ra = single_target_ra
		if single_target_form_value_dec is not None:
			single_target_form_value_dec = single_target_dec
		
		# We will accept in our form anything that Astropy can accept.
		# Need to do error checking here.
		coordinate = SkyCoord(frame=ICRS, ra=single_target_ra, dec=single_target_dec)
		
		# create Source object
		source = Source()
		source.j2000coord = coordinate
		#source.ra = single_target.ra
		#source.dec = single_target.dec
		source.name = single_target_name
		
		source_list.append(source)
		
	elif mode == "multiple_targets":
		# parse input here
		target_list_input = valueFromRequest(key="target_list_input", request=request, default=None)

	# defaults
	# --------
#	if observatory is None:
#		observatory = "GBT"
	
	# Astropy coordinate frames
	astropy_coordinate_frames = ["ICRS", "Galactic", "FK5"]
	templateDict["frames"] = astropy_coordinate_frames
	
	# Create the observatory object for ephem (only if there is a source list)
	if len(source_list) > 0:
		hard_coded_observatory = False
		if hard_coded_observatory:
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
		else:
			#observatory = ephem.Observer()
			# get the matching Observatory object (they're all loaded from above)
			obs_from_db = [x for x in observatories if x.short_name == selected_obs_short_name][0]
			observatory = obs_from_db.observer
			observatory.horizon = horizon # needs to be a string
			#observatory.lon = obs_from_db.longitude
			#observatory.lat = obs_from_db.latitude
			#observatory.elevation = obs_from_db.elevation
			#observatory.date = "{0.year}/{0.month:02d}/{0.day:02d}".format(datetime.now())
			#observatory.horizon = ephem.degrees(horizon) # TODO - pull from database (or input?)
		
		print("obs: {0}".format(observatory))
		findLST(observatory, source_list)
		print("----> {0.riseLST}, {0.setLST}".format(source_list[0]))

	templateDict["single_target_form_value_name"] = single_target_form_value_name
	templateDict["single_target_form_value_ra"] = single_target_form_value_ra
	templateDict["single_target_form_value_dec"] = single_target_form_value_dec
	templateDict["sourceList"] = [x for x in source_list if x.neverUp is False]
	templateDict["neverUpSourceList"] = [x for x in source_list if x.neverUp is True]
	
	print("sources never up: {0}".format( [x for x in source_list if x.neverUp is True]))
	
	templateDict["now"] = datetime.now()
	
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
