import os
import time
from email.mime.multipart import MIMEMultipart

def save_email( email ):
    t_stamp = time.strftime( "%Y_%m_%d_%H_%M_%S" )
    email_file = "%s_%s" % (email['To'], t_stamp)
    email_file = os.path.join( os.getcwd(), email_file )

    with open( email_file, 'w' ) as output_file:
        output_file.writelines( "%s\n" % (email.as_string()) )

    return email_file
