from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Address, Location
from .global_vars import NUM_CITIES, TITLE
from .forms import RegisterForm

# Create your views here.
def index( request ):
    template = 'register/index.html'
    redirect = "confirmation/" 
    error_msg = ""
    if request.method == "POST":
        # Validate the contents of the form and update the database.
        form = RegisterForm( request.POST )
        if form.is_valid():
            email_address = form.cleaned_data['email_address']
            location_id = form.cleaned_data['location_id']
            try:
                fk = Location.objects.all().filter( pk=location_id )
                if len(fk) != 1:
                    # Primary key should always be unique.
                    raise ValidationError( "Invalid primary key supplied" )
                a = Address( location=fk[0], email_address=email_address, creation_date=timezone.now() )
                # Validate e-mail once more before saving.
                a.full_clean()
                a.save()
                # Successfully entered e-mail address. Redirect to confirmation page.
                return HttpResponseRedirect( redirect )
            except ValidationError, exc:
                # Capture any unexpected error messages.
                error_msg = "%s" % exc
        else:
             error_msg = "Invalid form"
    else:
        # First time navigating to the page. Create an empty form.
        form = RegisterForm( initial={'Where do you live?': '0'} )
    context = { 'title': TITLE,
                'form': form,
                'error_msg': error_msg
              }
    return render( request, template, context )

def confirmation( request ):
    template = 'register/confirmation.html'
    result = "Successfully registered e-mail address!"
    context = { 'title': TITLE,
                'result': result,
              }
    return render( request, template, context )
