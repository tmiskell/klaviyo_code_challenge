import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def send_out_email( next_email, next_image ):
    smtp_server_ip = 'localhost'
    email = MIMEMultipart()
    email['Subject'] = next_email.subject()
    email['From'] = next_email.send_addr()
    email['To'] = next_email.rcv_addr()
    email.preamble = next_email.subject
    if next_image:
        email.attach( MIMEImage(next_image) )
    email_server = smtplib.SMTP( smtp_server_ip )
    email_server.sendmail( email['From'], email['To'], email.as_string() )
    email_server.quit()

    return
