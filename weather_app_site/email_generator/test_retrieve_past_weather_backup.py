import os
import sys
import json
import urllib2
import datetime

def retrieve_past_weather(  ):
    API_KEY = "2tab9fyvrvuiYrReaH0hE"
    SECRET_KEY = "PIUgxrZ53NwHNdV71yyQF7PfA6r2laPyNLj99pfL"
    WEATHER_BASE_URL = "http://api.aerisapi.com"
    us_city = "Tampa"
    us_state = "FL"
    keys = "&client_id=" + API_KEY + "&client_secret=" + SECRET_KEY
    obs_endpt = WEATHER_BASE_URL + "/observations"
    archive_endpt = obs_endpt + "/archive/search"
    num_days = 1
    prev_date = datetime.datetime.now() - datetime.timedelta( num_days )
    # Retrieve average weather conditions.
    query = "?query=name:" + us_city.lower().replace(" ", "")
    query += "&state=" + us_state.lower().replace(" ", "")
    query += "&from=" + prev_date.strftime( "%m/%d/%Y" )
    try: 
        request = urllib2.urlopen( archive_endpt + '/'+ query + keys )
    except urllib2.HTTPError as exc:
        print exc
        print archive_endpt + '/' + query + keys
        return
    response = request.read()
    json_file = json.loads( response )
    if json_file['success']:
        print (json.dumps( json_file, indent=4, sort_keys=True ))
        next_obs = json_file['response'][0]['ob']
        past_temp_f = next_obs['tempF']
        past_temp_c = next_obs['tempC']
        print past_temp_f
    else:
        print json_file['error']['description']
        print archive_endpt + '/' + query + keys
    request.close()
    print archive_endpt + '/' + query + keys
    return
 
if __name__ == "__main__":
    retrieve_past_weather()
    sys.exit()
