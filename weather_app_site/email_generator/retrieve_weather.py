from __future__ import with_statement

import os
import sys
import json
import urllib
import urllib2
import datetime
from .classes import Weather, ArchiveWeatherParser
from .global_vars import API_KEY, WEATHER_BASE_URL

def retrieve_weather( next_recipient ):
    """
        (1) The script fetches the current weather for that recipient's location 
    """   
    obs_endpt = WEATHER_BASE_URL + '/' + API_KEY + "/conditions"
    loc = next_recipient.us_state().upper() + '/' + next_recipient.us_city().title().replace( ' ', '_' )
    num_days = 1
    prev_date = datetime.datetime.now() - datetime.timedelta( num_days )
    # Retrieve current weather for given location.
    sys.stdout.write( "Requesting: " + obs_endpt + "/q/" + loc + ".json" )
    request = urllib2.urlopen( obs_endpt + "/q/" + loc + ".json" )
    response = request.read()
#    json_file = json.loads( response )
#    sys.stdout.write( json.dumps(json_file, sort_keys=True, indent=4, separators=(",", ": ")) )
    json_file = json.loads( response )
    next_obs = json_file['current_observation']
    condition = next_obs['weather']
    curr_temp_f = next_obs['temp_f']
    curr_temp_c = next_obs['temp_c']
    image_ref = next_obs['icon_url']
    request.close()
    # Retrieve average weather conditions.
    archive_endpt = "http://www.wunderground.com"
    archive_endpt += "/history"
    archive_endpt += "/airport" 
    archive_endpt += "/K" + next_recipient.airport().upper()
    archive_endpt += '/' + prev_date.strftime( "%Y/%m/%d" ) 
    archive_endpt += "/DailyHistory.html"
    past_temp_f = 0.0
    if archive_endpt:
        curr_base_dir = os.path.dirname( os.path.realpath(__file__) )
        archive_base_dir = os.path.join( curr_base_dir, "archive" )
        if not os.path.exists( archive_base_dir ):
            os.makedirs( archive_base_dir )
        archive_file = next_recipient.us_city().replace( ' ', '_' ) + '_' + next_recipient.us_state() + ".html"
        archive_file = os.path.join( archive_base_dir, archive_file )                
        sys.stdout.write( "Retrieving: %s\n" % archive_endpt )
        urllib.urlretrieve( archive_endpt, archive_file )
        # Parse archive file to retrieve average temperature.
        past_temp_f = None
        past_temp_c = None
        units = ''
        if os.path.exists( archive_file ):
            lines = ""
            with open( archive_file, 'r' ) as input_file:
                lines_array = input_file.readlines()
                for next_line in lines_array:
                    lines += next_line
            parser = ArchiveWeatherParser()            
            parser.feed( lines )
            if parser.units():
                units = parser.units()
            else:
                raise IOError( "No units. Incorrect format in file: " + archive_file )
            if parser.avg_temp():
                past_temp = int( parser.avg_temp() )
            elif parser.actual_temp():
                past_temp = int( parser.actual_temp() )
            elif parser.rec_temp():
                past_temp = int( parser.rec_temp() )
            else:
                raise IOError( "No temperature. Incorrect format in file: " + os.path.basename(archive_file) )
            if units.lower() == 'f':
                past_temp_f = past_temp
            elif units.lower() == 'c':
                past_temp_c = past_temp
            else:
                raise IOError( "Incorrect units. Incorrect format in file: " + os.path.basename(archive_file) )
        else:
            raise IOError( "*** Unable to determine average temperature ***" )
    image = None
    if image_ref:
        # Retrieve image
        curr_base_dir = os.path.dirname( os.path.realpath(__file__) )
        image_base_dir = os.path.join( curr_base_dir, "images" )
        if not os.path.exists( image_base_dir ):
            os.makedirs( image_base_dir )
        image_file = image_ref.split('/')[-1]        
        image_file = os.path.join( image_base_dir, image_file )        
        urllib.urlretrieve( image_ref, image_file )
        input_file = open( image_file, 'rb' )
        image = input_file.read()
        input_file.close()
        os.remove( image_file )
    next_weather = Weather( curr_temp_f=curr_temp_f, curr_temp_c=curr_temp_c, condition=condition, image=image,
                            past_temp_f=past_temp_f, past_temp_c=past_temp_c )
    return next_weather
