"""
    Global variables

    Variables:
        API_KEY:          Key used to access the weather API.
        wEATHER_BASE_URL: The base URL for the weather API.
        DJANGO_APP:       The Django application for this project.
        AUTHOR_ADDRESS:   The originating author address for all e-mails sent out.
        TITLE:            The title for the project.
        SMTP_SERVER_IP:   IP address for the SMTP server.
        NUM_DAYS:         Number of days prior to current day to use for retrieving average weather conditions.
        DEGREE_SYMBOL:    Symbol to use for degrees for temperature measurements.
        PRECIP_TYPES:     List of precipitation types.
"""
API_KEY = "950398e05e71a9c0"
WEATHER_BASE_URL = "http://api.wunderground.com/api"
DJANGO_APP = "weather_app_site"
AUTHOR_ADDRESS = "tmiskell@morphotrust.com"
TITLE = "Weather Powered Email"
SMTP_SERVER_IP = "localhost"
NUM_DAYS = 365
DEGREE_SYMBOL = u"\N{DEGREE SIGN}"
PRECIP_TYPES = ["rain",
                "drizzle",
                "snow",
                "sleet",
                "hail",
                "graupel",
                "ice needles",
               ]
# Aeris API keys and URLs (deprecated)
#API_KEY = "2tab9fyvrvuiYrReaH0hE"
#SECRET_KEY = "PIUgxrZ53NwHNdV71yyQF7PfA6r2laPyNLj99pfL"
#WEATHER_BASE_URL = "http://api.aerisapi.com"
