from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def create_email( from_addr, to_addr, next_subject, next_body, next_image, title ):
    """
    Function to generate the e-mail for the next recipient.
    Note: Unicode encoding is used when generating the HTML formatted email body.

        Arguments:
            from_addr:    The originating author address for the e-mail.
            to_addr:      The receipient of the e-mail.
            next_subject: The conditionally defined subject to use for the e-mail
            next_body:    The body of the e-mail
            next_image:   The image, if present, to include within the e-mail
            title:        The title for the project
            
        Variables:
            email:        The generated e-mail to send to the recipient.

        Returns:
            email:        The generated e-mail to sent to the recipient.
    """
    # Initialize variables
    email = MIMEMultipart()
    # Generate the e-mail
    email['Subject'] = next_subject
    # In all cases:
    # (1) The email will be sent to the recipient's entered email address 
    email['To'] = to_addr
    # (2) Come from the author's email address.             
    email['From'] = from_addr
    email.preamble = title
    email.attach( MIMEText(next_body.encode('utf-8'), "html") )
    if next_image:
        email.attach( MIMEImage(next_image) )

    return email
