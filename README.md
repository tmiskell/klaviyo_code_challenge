# klaviyo_code_challenge
Klaviyo Code Challenge

To run the email generator:
              > cd ~/klaviyo_code_challenge/weather_app_site
              > python -m email_generator.main

To pre-populate the database of selectable locations:
              > cd ~/klaviyo_code_challenge/weather_app_site/register/
              > $EDITOR_OF_CHOICE us_city_state.csv 
              > ./create_fixture.py 
              > python manage.py loaddata register/pre_load_db.yaml 

Assumptions:
   Partly sunny or mostly sunny is still to be considered "sunny".
   If the precipation measurement is non-negative then it is considered to be "precipating".

Notes: 
   Leverages the Wunderground API to retrieve each recipient's weather by their location.
   Logs all activity within:
              ~/klaviyo_code_challenge/weather_app_site/email_generator/log/