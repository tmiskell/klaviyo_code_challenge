import sys
import HTMLParser

class Weather( object ):
    """
        Class to all weather related data associated with a given observation for a given location.
        Includes average weather conditions.
    """
    def __init__( self, curr_temp_f=None, avg_temp_f=None, curr_temp_c=None, avg_temp_c=None, condition="", image=None,
                  curr_precip=None ):
        """
            Initializer function.
        """
        # Ensure that current temperature is valid.
        try:
            self._curr_temp_f = float( curr_temp_f )
        except (ValueError, TypeError):
            # Attempt to continue, using Celsius version.
            curr_temp_f = None
        try:
            self._curr_temp_c = float( curr_temp_c )
        except (ValueError, TypeError):
            # Attempt to continue, using Farenheit version.
            curr_temp_c = None
        if curr_temp_f is None:
            if curr_temp_c is None:
                raise ValueError( "Invalid value for current temperature" )
            else:
                self._curr_temp_f = self._celsius_to_far( self.curr_temp_c() )
        elif curr_temp_c is None:
            self._curr_temp_c = self._far_to_celsius( self.curr_temp_f() )
        try:
            self._avg_temp_f = float( avg_temp_f )
        except (ValueError, TypeError):
            # Attempt to continue, using Celsius version.
            avg_temp_f = None
        try:
            self._avg_temp_c = float( avg_temp_c )
        except (ValueError, TypeError):
            # Attempt to continue, using Farenheit version.
            avg_temp_c = None
        if avg_temp_f is None:
            if avg_temp_c is None:
                raise ValueError( "Invalid value for current temperature" )
            else:
                self._avg_temp_f = self._celsius_to_far( self.avg_temp_c() )
        elif avg_temp_c is None:
            self._avg_temp_c = self._far_to_celsius( self.avg_temp_f() )
        try:
            self._curr_precip = float( curr_precip )
            if self._curr_precip < 0.0:
                # Precipation measurement should be non-negative
                raise ValueError
        except ValueError:
            raise ValueError( "Invalid value for current precipation measurement." )
        self._condition = condition
        self._image = image

    def _far_to_celsius( self, x ):
        """
            Helper function to convert Farenheit to Celsius.
        """
        return (5.0 / 9.0) * (x - 32.0)

    def _celsius_to_far( self, x ):
        """
            Helper function to convert Celsius to Farenheit.
        """
        return (9.0 / 5.0) * (x + 32.0)

    def __str__( self ):
        """
            Function to return a string representative of the class.
        """
        return self.condition + ", " + self.curr_temp_f + " F, (" + self.curr_temp_c + " C)"

    def curr_temp_f( self ):
        """
            Accessor function for the current temperature in Farenheit.
        """
        return self._curr_temp_f

    def avg_temp_f( self ):
        """
            Accessor function for the average temperature in Farenheit.
        """
        return self._avg_temp_f

    def avg_temp_c( self ):
        """
            Accessor function for the average temperature in Celsius.
        """
        return self._avg_temp_c

    def condition( self ):
        """
            Accessor function for the current weather conditions.
        """
        return self._condition

    def image( self ):
        """
            Accessor function for the image associated with the current weather.
        """
        return self._image

    def curr_temp_c( self ):
        """
            Accessor function for the current temperature in Celsius.
        """
        return self._curr_temp_c

    def curr_precip( self ):
        """
            Accessor function for the current precipitation in inches.
        """
        return self._curr_precip

class Recipient( object ):
    """
        Class to store data related to the recipient of the next e-mail to be generated.
    """
    def __init__( self, address, us_city, us_state, airport ):
        """
            Initializer function.
        """
        self._address = address
        self._us_city = us_city
        self._us_state = us_state
        self._us_state_full_name = self.us_state_convert
        self._airport = airport

    def address( self ):
        """
            Accessor function to return the e-mail address.
        """
        return self._address

    def us_city( self ):
        """
            Accessor function to return the U.S. city.
        """
        return self._us_city

    def us_state( self ):
        """
            Accessor function to return the U.S. state.
        """
        return self._us_state 

    def airport( self ):
        """
            Accessor function to return the airport in closest proximity for the given
            U.S. city and state.
        """
        return self._airport

    def us_state_convert( self ):
        """
            Helper function to convert a two letter state abbreviation to the full state name.
        """
        us_dict = { 'AL': 'Alabama',
                    'AK': 'Alaska',
                    'AZ': 'Arizona',
                    'AR': 'Arkansas',
                    'CA': 'California',
                    'CO': 'Colorado',
                    'CT': 'Connecticut',
                    'DE': 'Delaware',
                    'FL': 'Florida',
                    'GA': 'Georgia',
                    'HI': 'Hawaii',
                    'ID': 'Idaho',
                    'IL': 'Illinois',
                    'IN': 'Indiana',
                    'IA': 'Iowa',
                    'KS': 'Kansas',
                    'KY': 'Kentucky',
                    'LA': 'Louisiana',
                    'ME': 'Maine',
                    'MD': 'Maryland',
                    'MA': 'Massachusetts',
                    'MI': 'Michigan',
                    'MN': 'Minnesota',
                    'MS': 'Mississippi',
                    'MO': 'Missouri',
                    'MT': 'Montana',
                    'NE': 'Nebraska',
                    'NV': 'Nevada',
                    'NH': 'New Hampshire',
                    'NJ': 'New Jersey',
                    'NM': 'New Mexico',
                    'NY': 'New York',
                    'NC': 'North Carolina',
                    'ND': 'North Dakota',
                    'OH': 'Ohio',
                    'OK': 'Oklahoma',
                    'OR': 'Oregon',
                    'PA': 'Pennsylvania',
                    'RI': 'Rhode Island',
                    'SC': 'South Carolina',
                    'SD': 'South Dakota',
                    'TN': 'Tennessee',
                    'TX': 'Texas',
                    'UT': 'Utah',
                    'VT': 'Vermont',
                    'VA': 'Virginia',
                    'WA': 'Washington',
                    'WV': 'West Virginia',
                    'WI': 'Wisconsin',
                    'WY': 'Wyoming',
                    'AS': 'American Samoa',
                    'DC': 'District of Columbia',
                    'FM': 'Federated States of Micronesia',
                    'GU': 'Guam',
                    'MH': 'Marshall Islands',
                    'MP': 'Northern Mariana Islands',
                    'PW': 'Palau',
                    'PR': 'Puerto Rico',
                    'VI': 'Virgin Islands',
                    'AE': 'Armed Forces Africa',
                    'AA': 'Armed Forces Americas',
                    'AE': 'Armed Forces Canada',
                    'AE': 'Armed Forces Europe',
                    'AE': 'Armed Forces Middle East',
                    'AP': 'Armed Forces Pacific',
                  }
        return us_dict[self._us_state]

class ArchiveWeatherParser( HTMLParser.HTMLParser ):
    """ 
        Class to parse archive weather HTML pages in order to extract the
        average weather conditions. 
    """
    def __init__( self ):
        """
            Initializer function.
        """
        HTMLParser.HTMLParser.__init__( self )
        self._n_col = 0
        self._n_row = 0
        self._finished = False
        self._mean_loc = None
        self._actual_loc = None
        self._avg_loc = None
        self._rec_loc = None
        self._actual_temp = None
        self._avg_temp = None
        self._rec_temp = None
        self._units = ""

    def _is_int( self, x ):
        """
            Helper function to test if the given argument is an integer.
        """
        try:
            int( x )
            return True
        except (ValueError, TypeError):
            return False

    def actual_temp( self ):
        """
            Accessor function for the actual temperature.
        """
        return self._actual_temp

    def avg_temp( self ):
        """
            Accessor function for the average temperature.
        """
        return self._avg_temp

    def rec_temp( self ):
        """
            Accessor function for the record temperature.
        """
        return self._rec_temp

    def units( self ):
        """
            Accessor function for the temperature measurement units.
        """
        return self._units
    
    def handle_starttag( self, tag, attrs ):
        """
            Overloaded function to handle the HTML start tag.
            Used to track temperature measurement locations, in terms of rows and columns,
            within a given table.
        """
        if self._finished:
            return
        if tag == "table":
            #sys.stdout.write( "Detected start of next table.\n" )            
            self._n_row = 0
            self._n_col = 0
            self._mean_loc = None
            self._actual_loc = None
            self._avg_loc = None
            self._rec_loc = None
        elif tag == "tr":
            self._n_col = 0
            self._n_row += 1
            #sys.stdout.write( "Row number: %d\n" % (self._n_row) )            
        elif tag == "th":
            self._n_col += 1
            #sys.stdout.write( "Column number: %d\n" % (self._n_row) )            
        elif tag == "td":
            self._n_col += 1
            #sys.stdout.write( "Column number: %d\n" % (self._n_row) )            
        return
            
    def handle_endtag( self, tag ):
        """
            Overloaded function to handle the HTML end tags.
            Used to track when the average temperature data has been extracted
            from the HTML file.
        """
        if self._finished:
            return
        if tag == "tr":
            if self.actual_temp() or self.avg_temp() or self.rec_temp():
                #sys.stdout.write( "Found temperature\n" )            
                self._finished = True
        return
            
    def handle_data( self, data ):
        """
            Overloaded function to define handling of HTML data.
            Used to retrieve the location and value for the average temperature.
        """
        if self._finished:
            return
        cleaned_data = data.strip().lower()
        if cleaned_data:
            if self._mean_loc:
                if self._n_row == self._mean_loc:
                    # Currently reading the mean temperature row
                    if self._is_int( cleaned_data ):
                        if self._actual_loc:
                            if self._n_col == self._actual_loc:
                                # Currently reading the actual temperature column
                                self._actual_temp = int( cleaned_data )
                                #sys.stdout.write( "Actual temperature: %d\n" % (self.actual_temp()) )            
                        if self._avg_loc:
                            if self._n_col == self._avg_loc:
                                # Currently reading the average temperature column
                                self._avg_temp = int( cleaned_data )
                                #sys.stdout.write( "Average temperature: %d\n" % (self.avg_temp()) )            
                        if self._rec_loc:
                            if self._n_col == self._rec_loc:
                                # Currently reading the record temperature column
                                self._rec_temp = int( cleaned_data )
                                #sys.stdout.write( "Record temperature: %d\n" % (self.rec_temp()) )            
                    elif ("f" in cleaned_data) or ("c" in cleaned_data):
                        self._units = cleaned_data.replace("&nbps;", "").replace("&deg;", "")
                        #sys.stdout.write( "Units: %s\n" % (self.units()) )            
            elif cleaned_data == "mean temperature":
                self._mean_loc = self._n_row
                #sys.stdout.write( "Mean temperature row: %d\n" % (self._mean_loc) )            
            elif cleaned_data == "actual":
                self._actual_loc = self._n_col
                #sys.stdout.write( "Actual temperature column: %d\n" % (self._actual_loc) )            
            elif cleaned_data == "average":
                self._avg_loc = self._n_col
                #sys.stdout.write( "Average temperature column: %d\n" % (self._avg_loc) )            
            elif cleaned_data == "record":
                self._rec_loc = self._n_col
                #sys.stdout.write( "Record temperature column: %d\n" % (self._rec_loc) )            
        return
