class Email( object ):
    def __init__( self, send_addr, rcv_addr, subject, body ):
        self._send_addr = send_addr
        self._rcv_addr = rcv_addr
        self._subject = subject
        self._body = body
    def send_addr( self ):
        return self._send_addr
    def rcv_addr( self ):
        return self._rcv_addr
    def subject( self ):
        return self._subject
    def body( self ):
        return self._body

class Weather( object ):
    def __init__( self, curr_temp_f=0.0, past_temp_f=0.0, curr_temp_c=0.0, condition="", image=None ):
        # Ensure that current temperature is valid.
        try:
            self._curr_temp_f = float( curr_temp_f )
        except ValueError:
            # Attempt to continue, using Celsius version.
            curr_temp_f = None
        try:
            self._curr_temp_c = float( curr_temp_c )
        except ValueError:
            # Attempt to continue, using Farenheit version.
            curr_temp_c = None
        if curr_temp_f is None:
            if curr_temp_c is None:
                raise ValueError( 'Invalid value for current temperature' )
            else:
                self._curr_temp_f = self._celsius_to_far( )
        elif curr_temp_c is None:
            self._curr_temp_c = self._far_to_celsius( )
        try:
            self._past_temp_f = float( past_temp_f )
        except ValueError:
            raise ValueError( 'Invalid value for average temperature' )
        self._condition = condition
        self._image = image
    def _far_to_celsius( self ):
        return (5.0 / 9.0) * (self._curr_temp_f - 32.0)
    def _celsius_to_far( self ):
        return (9.0 / 5.0) * (self._curr_temp_c + 32.0)
    def __str__( self ):
        return self.condition + ", " + self.curr_temp_f + " F, (" + self.curr_temp_c + " C)"
    def curr_temp_f( self ):
        return self._curr_temp_f
    def past_temp_f( self ):
        return self._past_temp_f
    def condition( self ):
        return self._condition
    def image( self ):
        return self._image
    def curr_temp_c( self ):
        return self._curr_temp_c

class Recipient( object ):
    def __init__( self, address, us_city, us_state ):
        self._address = address
        self._us_city = us_city
        self._us_state = us_state
        self._us_state_full_name = self.us_state_convert
    def address( self ):
        return self._address
    def us_city( self ):
        return self._us_city
    def us_state( self ):
        return self._us_state 
    def us_state_convert( self ):
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
