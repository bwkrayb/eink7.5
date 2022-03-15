import datetime
import os
import PIL
import time
import logging
import urllib.request
import requests
import re
import json
from settings import API_KEY, SMASHRUN_KEY
from PIL import Image, ImageDraw, ImageFont
from datetime import date,datetime

data_dir='/home/pi/eink7in5/data/'

def remove_nulls(d):
    return {k: v for k, v in d.iteritems() if v is not None}

#res = json.loads(json_value, object_hook=remove_nulls)

def write_running_month():
    today = date.today()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    f = open(data_dir +'running-month.json', 'w')
    monthRunUrlOpen = urllib.request.urlopen("https://api.smashrun.com/v1/my/stats/" + year + "/" + month + "?access_token=" + SMASHRUN_KEY).read()
    monthRunStr = monthRunUrlOpen.decode('utf-8').strip("[]")
    monthRunJson = json.loads(monthRunStr)
    f.write(monthRunStr)
    f.close()

    #smashrunURL = "https://api.smashrun.com/v1/my/stats/" + year + "/" + month + "?access_token=" + SMASHRUN_KEY
    #response = requests.get(smashrunURL)
    #responseJson = response.json()
    #responseStr = str(responseJson)
    #p = re.compile('(?<!\\\\)\'')
    #finalStr = p.sub('\"', responseStr)
    #f.write(finalStr)
    #f.close()

def write_running_last():
    f = open(data_dir+'running-last.json','w')
    smashrunURL = "https://api.smashrun.com/v1/my/activities/search?count=1&access_token=" + SMASHRUN_KEY
    response = requests.get(smashrunURL)
    responseJson = response.json()
    responseStr = str(responseJson)
    p = re.compile('(?<!\\\\)\'')
    finalStr = p.sub('\"', responseStr)
    f.write(finalStr)
    f.close()

def check_last_run():
    global lastRunID
    smashrunURL = "https://api.smashrun.com/v1/my/activities/search/ids?count=1&access_token=" + SMASHRUN_KEY
    response = requests.get(smashrunURL)
    responseJson = response.json()
    lastRunID = responseJson[0]



#write_running_month()
#write_running_last()
check_last_run()


lastRunFile = open(data_dir + 'running-last.json')
lastRunStr = lastRunFile.read()
lastRunJson = json.loads(lastRunStr)
lastRunFile.close()

monthRunFile = open(data_dir + 'running-month.json')
monthRunStr = monthRunFile.read()
monthRunJson = json.loads(monthRunStr)
print(monthRunJson['runCount'])
print(type(monthRunJson))
monthRunFile.close()

if lastRunID != lastRunJson[0]['activityId']:
    print('now updating run file')
    write_running_month()
    write_running_last()
else:
    print('no update needed.')


print(lastRunJson[0]['activityId'])


print(monthRunJson['runCount'])
print(monthRunJson['longestRun'])
print(monthRunJson['averageRunLength'])
print(monthRunJson['totalDistance'])


