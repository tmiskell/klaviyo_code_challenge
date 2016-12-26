from django.shortcuts import render
from django.http import HttpResponse
from .models import Address, Location
from .global_vars import NUM_CITIES, TITLE
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your views here.
def index( request ):
    # Pull the top NUM_CITIES cities by population.    
    top_pop_cities = Location.objects.order_by('-population')[:NUM_CITIES]
    template = 'register/index.html'
    context = { 'title': TITLE,
                'top_pop_cities' : top_pop_cities
              }
    return render( request, template, context )

def confirmation( request ):
    template = 'register/confirmation.html'
    result = "Successfully registered e-mail address"
    try:
        try:
            pk = int( request.POST.get('next_city_pk', None) )
        except TypeError:
            raise ValidationError( "Invalid primary key supplied" )
        fk = Location.objects.all().filter( pk=pk )
        if len(fk) != 1:
            # Primary key supplied should be valid, and should be a unique ID.
            raise ValidationError("Server side error")
        email_address = request.POST.get( 'email_address', '')
        a = Address( location=fk[0], email_address=email_address, creation_date=timezone.now() )
        # Validate e-mail before saving.
        a.full_clean()
        a.save()
    except ValidationError, exc:
        # Email was invalid or not unique. Capture the error message.
        if isinstance( exc, dict ):
            result = ""
            for key, value in exc.items():
                result += value + " "
            result = result.rstrip()
        else:
            result = "%s" % exc
    context = { 'title': TITLE,
                'result': result,
                'email_address': email_address
              }
    return render( request, template, context )
