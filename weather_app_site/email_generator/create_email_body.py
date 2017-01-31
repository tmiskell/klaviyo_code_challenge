def create_email_body( next_recipient, next_weather ):
    """
        For each email, the body of the email will contain:
        (1) A readable version of the recipient's location
        (2) The current temperature and weather. Ex: "55 degrees, sunny."
        (3) An image or animated GIF of the current weather.
        Note: An image, if present, will be attached to the e-mail
              upon sending out the corresponding e-mail.
    """
    degree_symbol = u"\N{DEGREE SIGN}"
    email_body = "<html>\n"
    email_body += "\t<head>\n"
    email_body += "\t</head>\n"
    email_body += "\t<body>\n"
    email_body += "\t\t<p>Recipient's Location: "
    email_body += next_recipient.us_city() + ", " + next_recipient.us_state() 
    email_body += "</p>\n"
    email_body += "\t\t<p>Current temperature and weather:\t"
    email_body += str( next_weather.curr_temp_f() ) + " " + degree_symbol + "F"
    email_body += " (" + str( next_weather.curr_temp_c() ) + " " + degree_symbol + "C)"
    email_body += ", "+ next_weather.condition()
    email_body += "</p>\n"
    email_body += "\t</body>\n"
    email_body += "</html>\n"

    return email_body
