from __future__ import with_statement
import os
import sys
import json
import urllib
import urllib2
import datetime
from .classes import Weather, ArchiveWeatherParser

def retrieve_weather( next_recipient, obs_endpt, html_dir, image_dir, num_days ):
    """
        Function to retrieve both the current and the average weather conditions
        for the current recipient's location.
        Note: Derives average weather conditions based on airport in closest
              proximity to the given city.

        Arguments:
            next_recipient: Instance of type Recipient containing details for next e-mail recipient.
            obs_endpt:      URL endpoint for the weather observation to be requested.
            html_dir:       Directory to store retrieved HTML files.
            image_dir:      Directory to store retrieved images.
            num_days:       Number of days prior to current day to use for retrieving average weather conditions.
            
        Variables:
            loc:            Location to use as part of URL request.
            url_request:    URL endpoint, with current location, to use for request for current weather conditions.
            avg_temp_f:     Average temperature in Farenheit.
            avg_temp_c:     Average temperature in Celsius.
            units:          Units for temperature measurement.
            image:          Image associated with current weather conditions.
            prev_date:      Calculated previous date to use when requesting average weather conditions.
            archive_endpt:  Endpoint used for requesting average weather conditions.
            archive_file:   HTML file to store the requested average weather conditions.
            request:        URL requested in order to retrieve current weather conditions.
            response:       Response retrieved from the requested URL
            json_file:      JSON file containing current weather conditions.
            next_obs:       Current weather observations for the given location.
            condition:      Weather conditions based on the current weather observation.
            curr_temp_f:    Current temperature in Farenheit.
            curr_temp_c:    Current temperature in Celsius.
            curr_precip:    Current precipitation measurement in inches.
            image_url:      URL to use when retrieving the associated image.
            lines:          A string of lines read from a file.
            lines_array:    An array of lines read from a file.
            parser:         An instance of ArchiveWeatherPaser used to parse the HTML file.
            avg_temp:       Average temperature, which may be in Farenheit or Celsius.
            image_file:     File containing the image data associated with the current weather conditions.
            input_file:     File to read image data from.

        Returns:
            next_weather: Instance of Weather containing weather details for the current location.
    """   
    # Initialize variables
    image = None
    avg_temp_f = None
    avg_temp_c = None
    lines = ""
    parser = ArchiveWeatherParser()            
    loc = "%s/%s" % ( next_recipient.us_state().upper(), 
          next_recipient.us_city().title().replace(' ', '_') )
    url_request = "%s/%c/%s%s" % ( obs_endpt, 'q', loc, ".json" )
    prev_date = datetime.datetime.now() - datetime.timedelta( num_days )
    archive_endpt = "%s/%s/%s/%s" % ( "http://www.wunderground.com/history/airport",
                    next_recipient.airport().upper(), prev_date.strftime( "%Y/%m/%d" ), "DailyHistory.html" )
    archive_file = "%s_%s%s" % ( next_recipient.us_city().replace( ' ', '_' ), 
                   next_recipient.us_state(), ".html" )
    archive_file = os.path.join( html_dir, archive_file )                
    # (1) The script fetches the current weather for that recipient's location 
    request = urllib2.urlopen( url_request )
    response = request.read()
    json_file = json.loads( response )
    next_obs = json_file['current_observation']
    condition = next_obs['weather']
    curr_temp_f = next_obs['temp_f']
    curr_temp_c = next_obs['temp_c']
    curr_precip = next_obs['precip_today_in']
    image_url = next_obs['icon_url']
    request.close()
    # Retrieve average weather conditions.
    urllib.urlretrieve( archive_endpt, archive_file )
    if not os.path.exists( archive_file ):
        raise IOError( "Unable to determine average temperature" )
    # Parse archive file to retrieve average temperature.
    with open( archive_file, 'r' ) as input_file:
        lines_array = input_file.readlines()
    for next_line in lines_array:
            lines += next_line
    parser.feed( lines )
    if not parser.units():
        raise IOError( "Unable to determine units. Incorrect format in file: %s" % 
                           (os.path.basename(archive_file)) )
    units = parser.units()
    # Use one of the following for the "average" temperature in order of preference:
    #  (1) Average temperature reading
    #  (2) Actual temperature reading
    #  (3) Record temperature reading
    if parser.avg_temp():
        avg_temp = int( parser.avg_temp() )
    elif parser.actual_temp():
        avg_temp = int( parser.actual_temp() )
    elif parser.rec_temp():
        avg_temp = int( parser.rec_temp() )
    else:
        raise IOError( "Unable to determine average temperature. Incorrect format in file: %s" %
                       (os.path.basename(archive_file)) )
    # Determine units for average temperature
    if units.lower() == 'f':
        avg_temp_f = avg_temp
    elif units.lower() == 'c':
        avg_temp_c = avg_temp
    else:
        raise IOError( "Incorrect units. Incorrect format in file:%s" % (os.path.basename(archive_file)) )
    os.remove( archive_file )
    if image_url:
        # Retrieve image
        image_file = image_url.split('/')[-1]        
        image_file = os.path.join( image_dir, image_file )        
        urllib.urlretrieve( image_url, image_file )
        input_file = open( image_file, 'rb' )
        image = input_file.read()
        input_file.close()
        os.remove( image_file )
    next_weather = Weather( curr_temp_f=curr_temp_f, curr_temp_c=curr_temp_c, condition=condition, image=image,
                            avg_temp_f=avg_temp_f, avg_temp_c=avg_temp_c, curr_precip=curr_precip )

    return next_weather
