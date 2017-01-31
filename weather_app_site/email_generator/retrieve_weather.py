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
    request = urllib2.urlopen( obs_endpt + "/q/" + loc + ".json" )
    response = request.read()
    json_file = json.loads( response )
    next_obs = json_file['current_observation']
    condition = next_obs['weather']
    curr_temp_f = next_obs['temp_f']
    curr_temp_c = next_obs['temp_c']
    image_ref = next_obs['icon_url']
    station_id = next_obs['station_id']
#    archive_endpt = next_obs['history_url']
    archive_endpt = "https://www.wunderground.com/history/airport" 
    archive_endpt += '/' + station_id
    archive_endpt += '/' + prev_date.strftime( "%Y/%m/%d" )
    archive_endpt += "/DailyHistory.html"
    archive_endpt += "?req_city=" + next_recipient.us_city().title().replace( ' ', '_' ) 
    archive_endpt += "&req_state=" + next_recipient.us_state().upper() 
    archive_endpt += "&reqdb.magic=1"
    archive_endpt += "&regdb.wmo=99999"
    request.close()
    past_temp_f = 0.0
    if archive_endpt:
        # Retrieve average weather conditions.
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
            if parser.Units():
                units = parser.Units()
            else:
                raise IOError( "Incorrect format in file: " + archive_file )
            if parser.AvgTemp():
                past_temp = int( parser.AvgTemp() )
            elif parser.ActualTemp():
                past_temp = int( parser.ActualTemp() )
            elif parser.RecTemp():
                past_temp = int( parser.RecTemp() )
            else:
                raise IOError( "Incorrect format in file: " + os.path.basename(archive_file) )
            if units == 'F':
                past_temp_f = past_temp
            elif units == 'C':
                past_temp_c = past_temp
            else:
                raise IOError( "Incorrect format in file: " + os.path.basename(archive_file) )
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
