import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from .global_vars import TITLE

def send_out_email( next_email, next_image ):
    smtp_server_ip = 'localhost'
    email = MIMEMultipart()
    email['Subject'] = next_email.subject()
    email['From'] = next_email.send_addr()
    email['To'] = next_email.rcv_addr()
    email.preamble = TITLE
    # Use unicode encoding when generating the email body
    email.attach( MIMEText(next_email.body().encode('utf-8'), "html") )
    if next_image:
        email.attach( MIMEImage(next_image) )
    email_server = smtplib.SMTP( smtp_server_ip )
    email_server.sendmail( email['From'], email['To'], email.as_string() )
    email_server.quit()

    return email
