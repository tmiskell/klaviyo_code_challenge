import smtplib

def send_out_email( next_email, smtp_server_ip ):
    """
        Function to send out the e-mail to the next recipient.

        Arguments:
            next_email:     The next email to be sent out
            smtp_server_ip: The IP address of the SMTP server.
            
        Variables:
            smtp_server:    The SMTP server
    """
    # Initialize variables
    smtp_server = smtplib.SMTP( smtp_server_ip )
    # Send the next email
    smtp_server.sendmail( next_email['From'], next_email['To'], next_email.as_string() )
    smtp_server.quit()

    return
