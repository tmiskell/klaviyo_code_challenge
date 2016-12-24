from __future__ import unicode_literals
from django.db import models
from .global_vars import US_CITY_MAX_LEN, US_STATE_MAX_LEN, EMAIL_MAX_LEN

# Create your models here.
class Location( models.Model ):
    """
       Currently, longest U.S. city name is 22 characters. 
       Add extra space for names of future cities.
       There are currently 19,354 incorporated places in the U.S.
    """
    us_city = models.CharField( max_length=US_CITY_MAX_LEN )
    """
        2 character abbreviation for U.S. state.
        There are currently 50 U.S. states.
    """
    us_state = models.CharField( max_length=US_STATE_MAX_LEN )
    # U.S. city population. Do not allow negative values.
    population = models.PositiveIntegerField( default=0 )
    def __str__( self ):
        # Adjust the string representation of the model for the drop down menu.
        return self.us_city + ", " + self.us_state

class Address( models.Model ):
    # Relate each address to a location
    location = models.ForeignKey( Location, on_delete=models.CASCADE )
    """
       E-mail address. Maximum length is 254.
       EmailField uses EmailValidator to validate the input.
       Ensure that only one no duplicate e-mail addresses are entered.
    """
    email_address = models.EmailField( max_length=EMAIL_MAX_LEN, unique=True )
    # Creation date for the e-mail address
    creation_date = models.DateTimeField( "Creation Date" )

# class weather_image( models.Model ):
    # Image associated with each type of weather condition.
#    weather_image = ImageField()
