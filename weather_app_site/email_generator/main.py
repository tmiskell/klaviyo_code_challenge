#!/usr/bin/python
"""
    Purpose:  A python script designed to send out a personalized email to each email address within a given subscriber list.
              For each recipient:
               (1) The script fetches the current weather for that recipient's location 
               (2) Changes the subject of the email based upon the weather.  
                (a) If it's nice outside, either sunny or 5 degrees warmer than the average temperature for that location at that
                    time of year, the email's subject will be "It's nice out! Enjoy a discount on us."  
                (b) If it's not so nice out, either precipitating or 5 degrees cooler than the average temperature, the subject
                    will be "Not so nice out? That's okay, enjoy a discount on us."
                (c) If the weather doesn't meet either of the previous conditions, it's an average weather and the email subject
                    will simply read "Enjoy a discount on us."
              In all cases: 
               (1) The email will be sent to the recipient's entered email address 
               (2) Come from the author's email address.
             
              For each email, the body of the email will contain:
               (1) A readable version of the recipient's location
               (2) The current temperature and weather. Ex: "55 degrees, sunny."
               (3) An image or animated GIF of the current weather.

              Leverages the Aeris API to retrieve each recipient's weather by their location.
"""
import os
import sys
import errno
import django
from .global_vars import DJANGO_APP, AUTHOR_ADDRESS
from .classes import Email, Weather, Recipient
from .retrieve_list import retrieve_list
from .retrieve_weather import retrieve_weather
from .change_subject import change_subject
from .create_email_body import create_email_body
from .send_out_email import send_out_email
from weather_app_site import setup
from socket import error as socket_error

def main( argv ):
    status_code = os.EX_OK
    try:
        # Setup Django database connection
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_APP + ".settings")
        django.setup()
    except:
        sys.stderr.write( "Unable to initialize database connection\n" )
        status_code = os.EX_IOERR
        return status_code
    sender_address = AUTHOR_ADDRESS
    num_sent = 0
    sys.stdout.write( "Retrieving recipient list\n" )
    recipient_list = retrieve_list( )
    sys.stdout.write( "Retrieved %d emails\n" % (len(recipient_list)) )
    for recipient in recipient_list:
        next_recipient = Recipient( recipient.email_address, recipient.location.us_city, recipient.location.us_state )
        sys.stdout.write( "\tRetrieving weather in %s, %s for %s\n" % 
                          (next_recipient.us_city(), next_recipient.us_state(), next_recipient.address()) )
        try:
            next_weather = retrieve_weather( next_recipient )
        except (ValueError, IOError) as exc:
            sys.stderr.write( "\t%s\n" % exc )
            sys.stderr.write( "\tUnable to retrieve weather for %s, %s\n" %  
                              (next_recipient.us_city(), next_recipient.us_state()) )
            continue
        sys.stdout.write( "\tPersonalizing email subject for %s\n" % (next_recipient.address()) )
        next_subject = change_subject( next_weather )
        sys.stdout.write( "\tPersonalizing email body for %s\n" % (next_recipient.address()) )
        next_body = create_email_body( next_recipient, next_weather )
        next_email = Email( sender_address, next_recipient.address(), next_subject, next_body )
        sys.stdout.write( "\tSending email to %s\n" % (next_recipient.address()) )
        try:
            send_out_email( next_email, next_weather.image() )
            num_sent += 1
        except socket_error as exc:
            sys.stderr.write( "\t%s\n" % exc )
    sys.stdout.write( "Sent %d emails\n" % (num_sent) )
    return status_code

if __name__ == "__main__":
    sys.exit( main(sys.argv) )
