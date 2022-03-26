## Running/Weather Display ##

This is yet another e-ink project of mine using a 7.5 inch waveshare screen. It pulls weather data from openweather api and pulls running data from smashrun's api. 

It is automated by setting a crontab entry that will run the bin/start.sh script every hour.
This should allow for easier control over the frequency of updates overnight, and also the possibility of having it run different screens. 

For now, it simply runs the new-weather.py at 5 minutes past the hour every hour. Below the main temperature, it displays the forecasted high and low, along with forecasted temperatures for the next 2 hours. It writes all of the weather and running data to json files in the data directory.
