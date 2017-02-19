def change_subject( next_weather, precip_types ):
    """
        Function to:
        (2) Change the subject of the email based upon the weather.  

        Arguments:
            next_weather: Instance of Weather containing weather details for the current location.
            precip_types: A list of recognized precipiation types.
            
        Variables:
            new_subject:  The conditionally defined subject to use for the e-mail
            result:       Details as to why a specific subject was chosen

        Returns:
            new_subject:  The conditionally defined subject to use for the e-mail
            result:       Details as to why a specific subject was chosen
    """
    # Initialize variables:
    # (c) If the weather doesn't meet either of the previous conditions, it's an average weather day
    #     and the email subject will simply read "Enjoy a discount on us."
    new_subject = "Enjoy a discount on us."
    result = "Case c: It's an average weather day."
    # Adjust the subject as needed based on weather conditions
    if ( (next_weather.curr_temp_f() - next_weather.avg_temp_f() > 5.0) or 
         ("sunny" in next_weather.condition().lower()) ):
        # (a) If it's nice outside, either sunny or 5 degrees warmer than the average temperature for that location at that
        #     time of year, the email's subject will be "It's nice out! Enjoy a discount on us."  
        #     (Assume partly sunny or mostly sunny is still considered "sunny".)
        new_subject = "It's nice out! Enjoy a discount on us."
        result = "Case a: It's sunny or current temp exceeds average by 5 degrees."
    elif ( (next_weather.curr_temp_f() - next_weather.avg_temp_f() < 5.0) or 
           (next_weather.curr_precip() > 0.0) or
           (any(precip_type in next_weather.condition().lower() for precip_type in precip_types)) ):
        # (b) If it's not so nice out, either precipitating or 5 degrees cooler than the average temperature, the subject
        #     will be "Not so nice out? That's okay, enjoy a discount on us."
        #     (Assume that if the precipation measurement is non-negative then it is considered to be "precipating".)
        new_subject = "Not so nice out? That's okay, enjoy a discount on us."
        result = "Case b: It's precipitating or current temp is below average by 5 degrees."
            
    return new_subject, result
