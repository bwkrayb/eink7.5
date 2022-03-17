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

def check_last_run():
    global lastRunID
    smashrunURL = "https://api.smashrun.com/v1/my/activities/search/ids?count=1&access_token=" + SMASHRUN_KEY
    response = requests.get(smashrunURL)
    responseJson = response.json()
    lastRunID = responseJson[0]

def readLastRun():
    global lastRunJson
    lastRunFile = open(data_dir + 'last-run.json')
    lastRunStr = lastRunFile.read()
    lastRunJson = json.loads(lastRunStr)
    lastRunFile.close()

def readMonthRun():
    global monthRunJson
    monthRunFile = open(data_dir + 'month-running.json')
    monthRunStr = monthRunFile.read()
    monthRunJson = json.loads(monthRunStr)
    monthRunFile.close()


#write_running_month()
#write_running_last()
check_last_run()

readLastRun()
readMonthRun()

if lastRunID != lastRunJson[0]['activityId']:
    print('now updating run file')
    write_running_month()
    write_running_last()
else:
    print('no update needed.')

totalDist = str(round((monthRunJson['totalDistance']*.621),2))

runCount = str(monthRunJson['runCount'])

if monthRunJson['longestRun'] == None:
    longRun = '0'
else:
    longRun = str(round((monthRunJson['longestRun'] * 0.621),2))

if monthRunJson['averageRunLength'] == None:
    avgLen = '0'
else:
    avgLen = str(round((monthRunJson['averageRunLength'] * 0.621),2))

print(longRun)
print(avgLen)
print(totalDist)
print(runCount)
print(lastRunJson[0]['activityId'])


