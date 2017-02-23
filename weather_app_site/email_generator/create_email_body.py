import base64

def create_email_body( next_recipient, next_weather, degree_symbol, msg_title ):
    """
        Function to generate the body of the email.

        Arguments:
            next_recipient: Instance of type Recipient containing details for next e-mail recipient.
            next_weather:   Instance of Weather containing weather details for the current location.
            degree_symbol:  Symbol to use for degrees for temperature measurements.
            
        Variables:
            email_body:     The body of the e-mail

        Returns:
            email_body:     The body of the e-mail
    """
    # Initialize variables
    email_body = "%s\n" % ( "<html>" )
    email_body += "\t%s\n" % ( "<head>" )
    email_body += "\t\t%s%s%s\n" % ( "<title>", msg_title, "</title>" )
    email_body += "\t%s\n" % ( "</head>" )
    email_body += "\t%s\n" % ( "<body>" )
    email_body += "\t\t%s%s:\t%s, %s%s\n" % ( "<p>", "Recipient's Location", 
                 next_recipient.us_city(), next_recipient.us_state(), "</p>" )
    # Generate the e-mail body
    # Each e-mail body will contain:
    # (1) A readable version of the recipient's location
    # (2) The current temperature and weather. Ex: "55 degrees, sunny."
    email_body += "\t\t%s%s:\t%.1f %c%c (%.1f %c%c), %s%s\n" % ( "<p>", 
                   "Current temperature and weather", next_weather.curr_temp_f(), 
                   degree_symbol, 'F', next_weather.curr_temp_c(), 
                   degree_symbol, 'C', next_weather.condition(), "</p>" )
    # (3) An image or animated GIF of the current weather.
    #     Note: An image, if present, will be attached to the body
    #           while the e-mail is in the process of being sent out 
    #           in the function send_email.
    email_body += "\t%s\n" % ( "</body>" )
    email_body += "%s\n" % ( "</html>" )

    return email_body
