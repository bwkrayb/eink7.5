This is yet another e-ink weather display, using a 7.5 inch waveshare screen. 

It is automated by setting a crontab entry that will run the bin/start.sh script every 20 minutes. This should allow for easier control over the frequency of updates overnight, and also the possibility of having it run different screens. For now, it simply runs the weather.py and not many other files are used despite their existance.
