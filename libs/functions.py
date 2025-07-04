import datetime
import os
import PIL
import json
import time
import logging
import requests
import urllib.request
import re
from settings import API_KEY, SMASHRUN_KEY
from PIL import Image, ImageDraw, ImageFont
from datetime import date,datetime

data_dir='/home/pi/eink7in5/data/'

logging.basicConfig(level=logging.INFO,filename='/home/pi/eink7in5/logs/eink.log')


def get_icon(weatherID):
    """
    Get the icon for the current weather
    :return: Image of the icon
    """
    dt = datetime.now()
    thunder = (200,201,202,210,211,212,221,230,231,232)
    drizzle = (300,301,301,310,311,312,313,314)
    rain = (500,501,502,503,504,511,520,521,522,531)
    snow = (600,601,602,611,612,613,615,616,620,621,622)
    fogMist = (701,721,741)
    ptCloud = (801,802,803)
    clear = (800,999)
    cloudy = (804,998)
    if 5 <= int(dt.strftime('%H')) < 18:
        if weatherID in clear:
            return Image.open("images/jpg/day_clear.jpg")
        elif weatherID in ptCloud:
            return Image.open("images/jpg/day_partial_cloud.jpg")
        elif weatherID in cloudy:
            return Image.open("images/jpg/cloudy.jpg")
        elif weatherID in rain:
            return Image.open("images/jpg/rain.jpg")
        elif weatherID in fogMist:
            return Image.open("images/jpg/mist.jpg")
        elif weatherID in snow:
            return Image.open("images/jpg/day_snow.jpg")
        else:
            logging.info(dt.strftime('%x-%X') + ":No icon set for " + str(weatherID))
            return Image.open("images/jpg/day_clear.jpg")
    else:
        if weatherID in clear:
            return Image.open("images/jpg/night_clear.jpg")
        elif weatherID in ptCloud or weatherID in cloudy:            
            return Image.open("images/jpg/night_partial_cloud.jpg")
        elif weatherID in rain:
            return Image.open("images/jpg/night_rain.jpg")
        elif weatherID in snow:
            return Image.open("images/jpg/night_snow.jpg")
        else:
            logging.info(dt.strftime('%x-%X') + ":No icon set for " + str(weatherID))
            return Image.open("images/jpg/night_clear.jpg")


def paste(image: Image, position: tuple = (0, 0)) -> None:
    """
    Paste an image onto the buffer
    :param image: Image to paste
    :param position: tuple position to paste at
    :return: None
    """
    image.paste(image, position)


def indent(input,font,width):
    return int((width - font.getsize(input)[0]) / 2)


def indentThirds(input,font,width):
    return int(((width*1.5) - font.getsize(input)[0]) / 2)


def imageIndent(image,width):
    return int((width - image.width) / 2)

def imageIndentThirds(image,width):
    return int(((width*1.5) - image.width) / 2)

def write_weather():
    f = open(data_dir +'weather.json', 'w')
    lat = "41.902756"
    lon = "-88.337706"
    exclude = "minutely,alerts"
    units = "imperial"
    openWeatherURL = "https://api.openweathermap.org/data/3.0/onecall?lat=" + lat + "&lon=" + lon + "&exclude=" + exclude + "&units=" + units + "&appid=" + API_KEY
    response = requests.get(openWeatherURL)
    responseJson = response.json()
    responseStr = str(responseJson)
    p = re.compile('(?<!\\\\)\'')
    finalStr = p.sub('\"', responseStr)
    f.write(finalStr)
    f.close()

def write_running_month():
    today = date.today()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    f = open(data_dir +'month-running.json', 'w')
    monthRunUrlOpen = urllib.request.urlopen("https://api.smashrun.com/v1/my/stats/" + year + "/" + month + "?access_token=" + SMASHRUN_KEY).read()
    monthRunStr = monthRunUrlOpen.decode('utf-8').strip("[]")
    monthRunJson = json.loads(monthRunStr)
    f.write(monthRunStr)
    f.close()

def write_running_last():
    f = open(data_dir+'last-run.json','w')
    smashrunURL = "https://api.smashrun.com/v1/my/activities/search?count=1&access_token=" + SMASHRUN_KEY
    response = requests.get(smashrunURL)
    responseJson = response.json()
    responseStr = str(responseJson)
    p = re.compile('(?<!\\\\)\'')
    finalStr = p.sub('\"', responseStr)
    f.write(finalStr)
    f.close()

def get_desc(curID):
    dt = datetime.now()
    thunderStr = "Thunder Storm"
    thunder = (200,201,202,230,231,232)
    drizzleStr = "Drizzle"
    drizzle = (300,302,310,312,313,314)
    heavyRainStr = "Heavy Rain"
    heavyRain = (502,503,522,531)
    lightRainStr = "Light Rain"
    lightRain = (520)
    sleetStr = "Snow Rain"
    sleet = (612,615,616)
    shSnowStr = "Snow Shower"
    shSnow = (620,622) 
    if curID in thunder:
        return thunderStr
    elif curID in drizzle:
        return drizzleStr
    elif curID in heavyRain:
        return heavyRainStr
    elif curID in lightRain:
        return lightRainStr
    elif curID in sleet:
        return sleetStr
    elif curID in shSnow:
        return shSnowStr
    else:
        logging.info(dt.strftime('%x-%X') + ":No label set for " + str(weatherID))
        return "No Label?"


