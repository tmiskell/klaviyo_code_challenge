# klaviyo_code_challenge
Klaviyo Code Challenge

To run the weather powered e-mail generator application:
              > cd ~/klaviyo_code_challenge/weather_app_site
              > python -m email_generator.main

To run the weather powered e-mail registration server:
              > cd ~/klaviyo_code_challenge/weather_app_site
              > python manage.py runserver &
              > firefox http://127.0.0.1:8000/register/

To pre-populate the database of selectable locations for the weather powered e-mail registration server:
              > cd ~/klaviyo_code_challenge/weather_app_site/register/
              > $EDITOR_OF_CHOICE us_city_state.csv 
              > ./create_fixture.py 
              > python manage.py loaddata register/pre_load_db.yaml 

Assumptions:
   Partly sunny or mostly sunny is still to be considered "sunny".
   If the precipation measurement is non-negative then it is considered to be "precipating".

Notes: 
   Leverages the Wunderground API to retrieve each recipient's weather by their location.
   Pulls average/historical weather data via the Wunderground website utilizing the airport in
   closest proximity to the corresponding location as a key and parsing the returned HTML page.
   E-mail generator application logs all activity within:
              ~/klaviyo_code_challenge/weather_app_site/email_generator/log/