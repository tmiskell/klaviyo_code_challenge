def change_subject( next_weather ):
    """
       (2) Change the subject of the email based upon the weather.  
        (c) If the weather doesn't meet either of the previous conditions, it's an average weather and the email subject
            will simply read "Enjoy a discount on us."
    """
    precip_types = ["rain",
                    "drizzle",
                    "snow",
                    "sleet",
                    "hail",
                    "graupel",
                    "ice needles",
                   ]
    new_subject = "Enjoy a discount on us."
    if (("sunny" in next_weather.condition().lower()) or 
        (next_weather.curr_temp_f() - next_weather.past_temp_f() > 5.0)):
        """
            (a) If it's nice outside, either sunny or 5 degrees warmer than the average temperature for that location at that
                time of year, the email's subject will be "It's nice out! Enjoy a discount on us."  
        """
        new_subject = "It's nice out! Enjoy a discount on us."
    elif (any(precip_type in next_weather.condition().lower() for precip_type in precip_types) or 
             (next_weather.curr_temp_f() - next_weather.past_temp_f() < 5.0)):
        """
            (b) If it's not so nice out, either precipitating or 5 degrees cooler than the average temperature, the subject
                will be "Not so nice out? That's okay, enjoy a discount on us."
        """
        new_subject = "Not so nice out? That's okay, enjoy a discount on us."
            
    return new_subject
