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
               (3) An image or animated FIG of the current weather.

              Leverages the Wunderground API to retrieve each recipient's weather by their location.
"""
import os
import sys

class Email( object ):
    def __init__( self, address, subject, body ):
        self._address = address
        self._subject = subject
        self._body = body
    def address( ):
        return self._address
    def subject( ):
        return self._subject
    def body( ):
        return self._body

def retrieve_list( ):
    recipient_list = []
    return recipient_list

def retrieve_weather( recipient_location ):
    current_weather = ""
    return current_weather

def change_subject( current_weather ):
    new_subject = "Enjoy a discount on us."
    return new_subject

def create_email_body( recipient_location, current_weather, weather_image ):
    email_body = ""
    return email_body

def send_email( next_email ):
    return

def main( argv ):
    status_code = os.EX_OK
    sys.stdout.write( "Generating email\n" )
    recipient_list = retrieve_list( )
    for recipient in recipient_list:
        recipient_location = ""
        recipient_address = ""
        recipient_address = ""
        current_weather = retrieve_weather( recipient_location )
        weather_image = retrieve_image( current_weather )
        next_subject = change_subject( current_weather )
        next_body = create_email_body( recipient_location, current_weather, weather_image )
        next_email = Email( recipient_address, next_subject, next_body )
        send_email( next_email )
    return status_code

if __name__ == "__main__":
    sys.exit( main(sys.argv) )
