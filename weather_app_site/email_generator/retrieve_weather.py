import os
import sys
import json
import urllib2
from .classes import Weather
from .global_vars import API_KEY, SECRET_KEY, WEATHER_BASE_URL

def retrieve_weather( next_recipient ):
    """
        (1) The script fetches the current weather for that recipient's location 
    """
    loc = next_recipient.us_city().lower().replace(" ", "") + ',' + next_recipient.us_state().lower().replace(" ", "")
    keys = "?client_id=" + API_KEY + "&client_secret=" + SECRET_KEY
    obs_endpt = WEATHER_BASE_URL + "/observations"
    archive_endpt = obs_endpt + "/archive"
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
        raise IOError(json_file['error']['description'])
        request.close()
        next_weather = Weather()
        return next_weather
    # Retrieve average weather conditions.
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


