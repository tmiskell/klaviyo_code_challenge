import os
import sys
import json
import urllib
import urllib2
import datetime

def retrieve_past_weather( ):
    """
        (1) The script fetches the current weather for that recipient's location 
    """   
    API_KEY = "950398e05e71a9c0"
    WEATHER_BASE_URL = "http://api.wunderground.com/api"
    us_state = "FL"
    us_city = "Tampa"
    obs_endpt = WEATHER_BASE_URL + '/' + API_KEY + "/conditions"
    loc = us_state.upper() + '/' + us_city.title().replace( ' ', '_' )
    num_days = 1
    prev_date = datetime.datetime.now() - datetime.timedelta( num_days )
    # Retrieve current weather for given location.
    request = urllib2.urlopen( obs_endpt + "/q/" + loc + ".json" )
    print obs_endpt + "/q/" + loc + ".json"
    response = request.read()
    json_file = json.loads( response )
    print( json.dumps( response, indent=4, sort_keys=True ) )
    next_obs = json_file['current_observation']
    condition = next_obs['weather']
    print condition
    curr_temp_f = next_obs['temp_f']
    print curr_temp_f
    curr_temp_c = next_obs['temp_c']
    print curr_temp_c
    image_ref = next_obs['icon_url']
    print image_ref
    archive_endpt = next_obs['history_url']
    print archive_endpt
    request.close()
    # Retrieve average weather conditions.
    image = None
    if image_ref:
        # Retrieve image
        curr_base_dir = os.path.dirname( os.path.realpath(__file__) )
        image_base_dir = os.path.join( curr_base_dir, "images" )
        if not os.path.exists( image_base_dir ):
            os.path.makedirs( image_base_dir )
        image_file = image_ref.split('/')[-1]        
        image_file = os.path.join( image_base_dir, image_file )        
        urllib.urlretrieve( image_ref, image_file )
        input_file = open( image_file, 'rb' )
        image = input_file.read()
        input_file.close()
    return

if __name__ == "__main__":
    retrieve_past_weather()
    sys.exit()
