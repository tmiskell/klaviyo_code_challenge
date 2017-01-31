from django import forms
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from .models import Address, Location
from .global_vars import NUM_CITIES, DEFAULT_OPTION

class Default_opt_disabled_widget( forms.Select ):

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        option_label = option_label.replace( ':', '' )
        if option_value == DEFAULT_OPTION:
            return format_html('<option value="{}"{} selected="selected" disabled>{}</option>', 
                               option_value, selected_html, force_text(option_label))
        else:
            return format_html('<option value="{}"{}>{}</option>', option_value, selected_html, force_text(option_label))

class RegisterForm( forms.Form ):
    # Add the email form.
    email_address = forms.EmailField( label="Email Address", 
                                      required=True 
                                    )
    # Pull the top NUM_CITIES cities by population.    
    top_pop_cities = Location.objects.order_by('-population')[:NUM_CITIES]
    # Add the city drop down box.
    choices = []
    choices.append( (DEFAULT_OPTION, DEFAULT_OPTION) )
    for next_city in top_pop_cities:
        choices.append( (next_city.id, str(next_city)) )
    location_id = forms.ChoiceField( label="Location", 
                                     choices=choices, 
                                     widget=Default_opt_disabled_widget,
                                     required=True 
                                   )

    def clean( self ):
        """
            Include an error message when an email address has already
            been registered
        """
        cleaned_data = super( RegisterForm, self ).clean()
        email_address = cleaned_data.get( 'email_address' )
        location_id = cleaned_data.get( 'location_id' )
        addresses = Address.objects.all()
        for address in addresses:
            if email_address == address.email_address:
                self.add_error( 'email_address', 'Email address has already registered' )
