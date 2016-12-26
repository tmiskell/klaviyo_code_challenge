from django import forms
from .models import Location
from .global_vars import NUM_CITIES

class RegisterForm( forms.Form ):
    # Add the email form.
    email_address = forms.EmailField( )
    # Pull the top NUM_CITIES cities by population.    
    top_pop_cities = Location.objects.order_by('-population')[:NUM_CITIES]
    # Add the city drop down box.
    choices = []
    for next_city in top_pop_cities:
        choices.append( (next_city.id, str(next_city)) )
    location_id = forms.ChoiceField( choices=choices )
