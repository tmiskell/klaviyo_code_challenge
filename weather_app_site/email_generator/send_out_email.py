import os
import sys
import subprocess

def send_out_email( from_addr, from_pass, smtp_server, to_addr, next_subject, next_body, next_image, msg_fmt ):
    """
        Function to send out the e-mail to the next recipient.

        Arguments:
            from_addr:    The author of the e-mail.
            from_pass:    The password for the author e-mail to use when connecting to the SMTP server.
            smtp_server:  The FQDN and port number for the SMTP server.
            to_addr:      The receipient of the e-mail.
            next_subject: The conditionally defined subject to use for the e-mail
            next_body:    The body of the e-mail
            next_image:   The image file, if present, to include within the e-mail
            msg_fmt:      The message format for the e-mail either auto, text, or HTML.
            
        Variables:
            cmd:         Command to execute
    """

    # Initialize variables
    cmd = ["sendEmail",
           "-f",
           from_addr,
           "-t",
           to_addr,
           "-u",
           "\"" + next_subject + "\"",
           "-m",
           "\"" + next_body + "\"",
           "-s",
           smtp_server,
           "-o",
           "tls=yes",
           "-o",
           "message-content-type=" + msg_fmt,
           "-xu",
           from_addr,
           "-xp",
           from_pass,
           "-a",
           next_image]
    # Send the next email
    subprocess.call( cmd )

    return
