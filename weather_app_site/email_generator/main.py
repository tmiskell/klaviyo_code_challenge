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

              To run:
              > cd ~/klaviyo_code_challenge/weather_app_site
              > python -m email_generator.main

              Note: Leverages the Wunderground API to retrieve each recipient's weather by their location.
              Note: Logs all activity within:
                 ~/klaviyo_code_challenge/weather_app_site/email_generator/log/

        Arguments:
            argv: A vector to the command line arguments.
            
        Variables:
            status_code:    The status code to return to the OS.            
            num_sent:       Number of e-mails successfully sent.
            obs_endpt:      URL endpoint for the weather observation to be requested.
            curr_dir:       The current directory.
            log_dir:        Directory to store the log file in.
            log_file:       The file to log entries to.
            logger:         Used to update the log file entries.
            log_handle:     File handle to use for the log file entries.
            log_format:     Format to use when logging entries.
            archive_dir:    Directory to store archive files from previous runs.
            html_dir:       Directory to store HTML files.
            email_dir:      Directory to store sent e-mails.
            image_dir:      Directory to store images.
            recipient_list: List of e-mail recipients
            next_recipient: Instance of type Recipient containing details for next e-mail recipient.
            next_weather:   Instance of Weather containing weather details for the current location.
            next_subject:   The conditionally defined subject to use for the e-mail
            result:         Details as to why a specific subject was chosen
            next_body:      The body of the next e-mail
            next_email:     The generated e-mail to send to the recipient.
            email_file:     Filename to use when saving the e-mail.

        Returns:
            status_code: The status code to return to the OS.
"""
import os
import sys
import time
import errno
import django
import logging
from urllib2 import HTTPError
from .classes import Recipient
from .save_email import save_email
from socket import error as socket_error
from .send_out_email import send_out_email
from .change_subject import change_subject
from .create_email import create_email
from .retrieve_weather import retrieve_weather
from .create_email_body import create_email_body
from .global_vars import DJANGO_APP, AUTHOR_ADDRESS, SMTP_SERVER_IP, API_KEY
from .global_vars import WEATHER_BASE_URL, NUM_DAYS, TITLE, DEGREE_SYMBOL, PRECIP_TYPES

def main( argv ):
    # Initialize variables
    status_code = os.EX_OK
    num_sent = 0
    obs_endpt = WEATHER_BASE_URL + '/' + API_KEY + "/conditions"
    curr_dir = os.path.dirname( os.path.realpath(__file__) )
    archive_dir = os.path.join( curr_dir, "archive" )
    html_dir = os.path.join( archive_dir, "html" )
    email_dir = os.path.join( archive_dir, "email" )
    image_dir = os.path.join( archive_dir, "images" )
    # Setup directory to store log files
    log_dir = os.path.join( curr_dir, "log" )
    if not os.path.exists( log_dir ):
        os.makedirs( log_dir )
    # Setup logging
    log_file = "email_generator_%s.log" % ( time.strftime("%Y_%m_%d_%H_%M_%S") )
    log_file = os.path.join( log_dir, log_file )
    logger = logging.getLogger( TITLE )
    log_handle = logging.FileHandler( log_file )
    log_format = logging.Formatter( "%(asctime)s %(levelname)s %(message)s" )
    log_handle.setFormatter( log_format )
    logger.addHandler( log_handle )
    logger.setLevel( logging.INFO )
    # Setup archive directory
    if not os.path.exists( archive_dir ):
        logger.info( "Creating directory: %s" % (archive_dir) )
        os.makedirs( archive_dir )    
    # Setup directory to store html files containing historical weather data
    if not os.path.exists( html_dir ):
        logger.info( "Creating directory: %s" % (html_dir) )
        os.makedirs( html_dir )
    # Setup directory to store previously sent e-mails
    if not os.path.exists( email_dir ):
        logger.info( "Creating directory: %s" % (email_dir) )
        os.makedirs( email_dir )
    # Setup directory to store weather image files
    if not os.path.exists( image_dir ):
        logger.info( "Creating directory: %s" % (image_dir) )
        os.makedirs( image_dir )
    # Retrieve recipient list
    try:
        # Setup Django database connection
        os.environ.setdefault( "DJANGO_SETTINGS_MODULE", DJANGO_APP + ".settings" )
        django.setup()
        from register.models import Address
    except:
        logger.critical( "Unable to initialize database connection" )
        return os.EX_IOERR
    recipient_list = Address.objects.all()
    logger.info( "Retrieved %d emails" % (len(recipient_list)) )
    # Generate and send e-mails
    for recipient in recipient_list:
        # Collect recipient info
        next_recipient = Recipient( address=recipient.email_address, us_city=recipient.location.us_city, 
                                    us_state=recipient.location.us_state, airport=recipient.location.airport )
        logger.info( "Next recipient: %s" % (next_recipient.address()) )
        # Retrieve weather for current recipient
        try:
            next_weather = retrieve_weather( next_recipient, obs_endpt, html_dir, image_dir, NUM_DAYS )
        except (ValueError, IOError, HTTPError) as exc:
            logger.error( "%s" % exc )
            logger.error( "Unable to retrieve weather in %s, %s" %  
                          (next_recipient.us_city(), next_recipient.us_state()) )
            status_code = os.EX_IOERR
            continue
        logger.info( "Retrieved weather in %s, %s:" % 
                     (next_recipient.us_city(), next_recipient.us_state()) )
        logger.info( "Current conditions: %.1f %sF, %s, %.2f in precip." % 
                     (next_weather.curr_temp_f(), DEGREE_SYMBOL, next_weather.condition(), next_weather.curr_precip()) )
        logger.info( "Average conditions: %.1f %sF" % 
                     (next_weather.avg_temp_f(), DEGREE_SYMBOL) )                          
        # Personalize e-mail
        (next_subject, result) = change_subject( next_weather, PRECIP_TYPES )
        logger.info( "Personalized email subject based on %s: %s" % (result, next_subject) )
        next_body = create_email_body( next_recipient, next_weather, DEGREE_SYMBOL )
        logger.info( "Personalized email body: %s" % 
                     (next_body.replace("\t", "").replace("\n", "")) )
        # Collect email contents and generate e-mail.
        next_email = create_email( AUTHOR_ADDRESS, next_recipient.address(), next_subject, 
                                   next_body, next_weather.image(), TITLE )
        # Send out e-mail
        try:
            send_out_email( next_email, SMTP_SERVER_IP )
        except socket_error as exc:
            logger.error( "%s" % exc )
            status_code = os.EX_IOERR
            continue
        logger.info( "Sent email to %s from %s" % (next_recipient.address(), AUTHOR_ADDRESS) )
        num_sent += 1
        # Save e-mail
        try:
            email_file = save_email( next_email, email_dir )
        except IOError as exc:
            logger.warning( "%s" % exc )
            status_code = os.EX_IOERR
        logger.info( "Saved %s" % (os.path.basename(email_file)) )
    logger.info( "Sent %d emails" % (num_sent) )
    return status_code

if __name__ == "__main__":
    sys.exit( main(sys.argv) )
