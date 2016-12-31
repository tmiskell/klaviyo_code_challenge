import os
import django

def setup():
    module = os.path.split( os.path.dirname(__file__) )[-1]
    os.environ.setdefault( "DJANGO_SETTINGS_MODULE", "{}.settings".format(module) )
    django.setup()
