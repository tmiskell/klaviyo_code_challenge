import os
import sys
import json
import urllib2
import datetime
from .classes import Weather
from .global_vars import API_KEY, SECRET_KEY, WEATHER_BASE_URL

def retrieve_weather( next_recipient ):
    """
        (1) The script fetches the current weather for that recipient's location 
    """   
    loc = next_recipient.us_city().lower().replace(" ", "") + ',' + next_recipient.us_state().lower().replace(" ", "")
    keys = "?client_id=" + API_KEY + "&client_secret=" + SECRET_KEY
    obs_endpt = WEATHER_BASE_URL + "/observations"
    archive_endpt = obs_endpt + "/search"
    num_days = 1
    prev_date = datetime.datetime.now() - datetime.timedelta( num_days )
    # Retrieve current weather for given location.
    request = urllib2.urlopen( obs_endpt + '/' + loc + keys )
    response = request.read()
    json_file = json.loads( response )
    if json_file['success']:
        next_obs = json_file['response']['ob']
        condition = next_obs['weather']
        curr_temp_f = next_obs['tempF']
        curr_temp_c = next_obs['tempC']
        image_ref = next_obs['icon']
        request.close()
    else:
        error_msg = json_file['error']['description']
        request.close()
        raise IOError( error_msg )
    # Retrieve average weather conditions.
    query = "?query=name:" + next_recipient.us_city().lower().replace(" ", "")
    query += "&state=" + next_recipient.us_state().lower().replace(" ", "")
    query += "&from=" + prev_date.strftime( "%m/%d/%Y" )
    request = urllib2.urlopen( archive_endpt + '/' + query + keys )
    json_file = json.loads( response )
    if json_file['success']:
        next_obs = json_file['periods'][0]['ob']
        past_temp_f = next_obs['tempF']
        past_temp_c = next_obs['tempC']
        request.close()
    else:
        error_msg = json_file['error']['description']
        request.close()
        raise IOError( error_msg )
    image = None
    if image_ref:
        curr_base_dir = os.path.dirname( os.path.realpath(__file__) )
        image_base_dir = os.path.join( curr_base_dir, "AerisIcons", "Aeris_WxIcons_55x55" )
        image_file = os.path.join( image_base_dir, image_ref )
        if os.path.exists( image_file ):
            # Retrieve image
            input_file = open( image_file, 'rb' )
            image = input_file.read()
            input_file.close()
    next_weather = Weather( curr_temp_f=curr_temp_f, curr_temp_c=curr_temp_c, condition=condition, image=image )
    return next_weather
