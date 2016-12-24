from django.shortcuts import render
from django.http import HttpResponse
from .models import Address, Location
from .global_vars import NUM_CITIES, TITLE
from django.utils import timezone

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
        a = Address( email_address=request.POST['email_address'], create_date=timezone.now() )
        # Ensure that e-mail is validated before saving.
        a.full_clean()
        a.save()
    except (django.db.IntegrityError):
        result = "E-mail address has already been registered"
    except (ValidationError):
        result = "Invalid e-mail address"
    context = { 'title': TITLE,
                'result': result,
                'email_address': email_address
              }
    return render( request, template, context )
