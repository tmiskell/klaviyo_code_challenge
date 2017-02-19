from __future__ import with_statement
import os
import time
from email.mime.multipart import MIMEMultipart

def save_email( email, email_dir ):
    """
        Function to save e-mail

        Arguments:
            email:     The next email to be saved
            email_dir: The directory in which to save the email
            
        Variables:
            email_file:     The name of the saved email file.

        Returns:
            email_file:     The name of the saved email file.
    """
    # Initialize variablies
    email_file = "%s_%s.txt" % ( email['To'], time.strftime( "%Y_%m_%d_%H_%M_%S" ) )
    email_file = os.path.join( email_dir, email_file )
    # Save the email
    with open( email_file, 'w' ) as output_file:
        output_file.writelines( "%s\n" % (email.as_string()) )

    return email_file
