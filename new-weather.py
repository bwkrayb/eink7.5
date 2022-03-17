import os
import time
import logging
import requests
import json
from libs.functions import get_icon, indent, indentThirds,  paste, write_weather, write_running_month, write_running_last, get_desc, imageIndent, imageIndentThirds
from datetime import datetime
from libs.waveshare_epd import epd7in5b_V2
from PIL import Image, ImageDraw, ImageFont
from settings import API_KEY,SMASHRUN_KEY
# Display init, clear
epd = epd7in5b_V2.EPD()
epd.init()
epd.Clear() # 0: Black, 255: White
pic_dir = '/home/pi/eink7in5/pics'
data_dir = '/home/pi/eink7in5/data/'
img_dir = '/home/pi/eink7in5/images/jpg/'
h = epd.height #480
w = epd.width #800
wHalf = w/2
dt = datetime.now()
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
tempText = ImageFont.truetype(FONT, 150, index=0)
iconText = ImageFont.truetype(FONT, 80, index=0)
bodyText = ImageFont.truetype(FONT, 20, index=0)
timeText = ImageFont.truetype(FONT, 20, index=0)
condText = ImageFont.truetype(FONT, 45, index=0)
sunText = ImageFont.truetype(FONT,45,index=0)
imageBlack = Image.new(mode='1', size=(w, h), color=255)
drawBlack = ImageDraw.Draw(imageBlack)
imageRed = Image.new(mode='1', size=(w, h), color=255)
drawRed = ImageDraw.Draw(imageRed)

def readWeather():
    global responseCurr
    global responseThisHour
    global responseToday
    global responseTomorrow
    global responseNextHour
    global responseNextHour2
    f = open(data_dir + 'weather.json')
    responseStr = f.read()
    responseJson = json.loads(responseStr)
    responseCurr = responseJson['current']
    responseThisHour = responseJson['hourly'][0]
    responseNextHour = responseJson['hourly'][1]
    responseNextHour2 = responseJson['hourly'][2]
    responseToday = responseJson['daily'][0]
    responseTomorrow = responseJson['daily'][1]
    f.close()

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

def check_last_run():
    global lastRunID
    smashrunURL = "https://api.smashrun.com/v1/my/activities/search/ids?count=1&access_token=" + SMASHRUN_KEY
    response = requests.get(smashrunURL)
    responseJson = response.json()
    lastRunID = responseJson[0]

def drawSmallTemp(text,temp,width,height):
    drawRed.text((indent(text,bodyText,w/4)+width,height),text,font=bodyText,fill=0,align='left')
    drawBlack.text((indent(temp,iconText,w/4),height+15),temp,font=iconText,fill=0,align='left')

try:
    write_weather()
    readLastRun()
    readMonthRun()
    check_last_run()
    if lastRunID != lastRunJson[0]['activityId']:
        print('now updating run file')
        write_running_month()
        write_running_last()
    else:
        print('no update needed.')

    readWeather()


    if int(dt.strftime('%H')) > 21:
        responseDailySS = responseTomorrow
        sunsetText = 'Tomorrow'
    else:
        responseDailySS = responseToday
        sunsetText = 'Today'

    if int(dt.strftime('%H')) > 8:
        responseDailySR = responseTomorrow
        sunriseText = 'Tomorrow'
    else:
        responseDailySR = responseToday
        sunriseText = 'Today'


    nextHourTs = responseNextHour['dt']
    nextHourDt = datetime.fromtimestamp(nextHourTs)
    nextHourStr = nextHourDt.strftime("%-I%p")
    nextHourTemp = str(round(responseNextHour['temp']))+'°'

    nextHourTs2 = responseNextHour2['dt']
    nextHourDt2 = datetime.fromtimestamp(nextHourTs2)
    nextHourStr2 = nextHourDt2.strftime("%-I%p")
    nextHourTemp2 = str(round(responseNextHour2['temp']))+'°'

    lowTemp = str(round(responseToday['temp']['min']))+'°'
    highTemp = str(round(responseToday['temp']['max']))+'°'


    curTs = responseCurr['dt']
    curDt = datetime.fromtimestamp(curTs)
    curDtStr = curDt.strftime("%-I:%M%p")
    #curDtStr = curDt.strftime("%c")

    sunriseTs = responseDailySR['sunrise']
    sunriseDt = datetime.fromtimestamp(sunriseTs)
    sunriseStr = sunriseDt.strftime("%-I:%M%p")
    sunriseFull = 'SR ' + sunriseStr

    sunsetTs = responseDailySS['sunset']
    sunsetDt = datetime.fromtimestamp(sunsetTs)
    sunsetStr = sunsetDt.strftime("%-I:%M%p")
    sunsetFull = 'SS ' + sunsetStr

    curTemp = str(round(responseCurr['temp']))# + '°'
    curFeel = str(round(responseCurr['feels_like']))# + '°'
    #curDesc = responseCurr['weather'][0]['description'].title().split()
    curDesc = responseThisHour['weather'][0]['description'].title().split()
    #curID = responseCurr['weather'][0]['id']
    curID = responseThisHour['weather'][0]['id']

    if len(curDesc) > 2:
        custDesc = get_desc(curID).split()
        curDesc1 = custDesc[0]
        curDesc2 = custDesc[1]
    elif len(curDesc) == 2:
        curDesc1 = curDesc[0]
        curDesc2 = curDesc[1]
    else:
        curDesc1 = curDesc[0] 

    #drawBlack.rectangle((400,240,800,480), fill=1, outline=0)
    #drawRed.rectangle((300, 0, 600, 240), fill=1, outline=0)

    logo = get_icon(curID)
    logoLg = logo.resize((64,64))
    imageRed.paste(logoLg, (imageIndent(logo,w)-50,60))

###TEMP TEXT###
    drawRed.text((indent('Current: '+curDtStr,bodyText,w/2)-50,0),'Current: '+curDtStr,font=bodyText,fill=0,align='left')
    drawBlack.text((indent(curTemp,tempText,w/2)-50, 2), curTemp, font=tempText, fill=0, align='left')
    drawRed.text((250, 10), '°', font=iconText, fill=0, align='left') 

###CONDITION TEXT###
#    drawBlack.text((indent(curDesc1,condText,w/2)-50, 160), curDesc1, font=condText, fill=0, align='left')
#    if len(curDesc) > 1:
#       drawBlack.text((indent(curDesc2,condText,w/2)-50, 210), curDesc2, font=condText, fill=0, align='left')

###CONDITION TEXT###
    drawBlack.text((indent(curDesc1,condText,wHalf)-50, 160), curDesc1, font=condText, fill=0, align='left')
    if len(curDesc) > 1:
        drawBlack.text((indent(curDesc2,condText,wHalf)-50, 210), curDesc2, font=condText, fill=0, align='left')


###LOW TEXT###
#   drawRed.text((indent('Low',bodyText,w/4),265),'Low',font=bodyText,fill=0,align='left')
#   drawBlack.text((indent(lowTemp,iconText,w/4),280),lowTemp,font=iconText,fill=0,align='left')

#drawSmallTemp('Low',lowTemp,0,265)

###HIGH TEXT###
#   drawRed.text((indent('High',bodyText,w/4),380),'High',font=bodyText,fill=0,align='left')
#   drawBlack.text((indent(highTemp,iconText,w/4),395),highTemp,font=iconText,fill=0,align='left')

drawSmallTemp('High',highTemp,0,380)

###NEXT HOUR TEXT###
#   drawRed.text((indent(nextHourStr,bodyText,w/4)+200,265),nextHourStr,font=bodyText,fill=0,align='left')
#   drawBlack.text((indent(nextHourTemp,iconText,w/4)+200,280),nextHourTemp,font=iconText,fill=0,align='left')

drawSmallTemp(nextHourStr,nextHourTemp,200,265)

###NEXT HOUR 2 TEXT###
#    drawRed.text((indent(nextHourStr2,bodyText,w/4)+200,380),nextHourStr2,font=bodyText,fill=0,align='left')
#    drawBlack.text((indent(nextHourTemp2,iconText,w/4)+200,395),nextHourTemp2,font=iconText,fill=0,align='left')

drawSmallTemp(nextHourStr2,nextHourTemp2,200,380)


###SUNRISE TEXT###
    drawRed.text((indent(sunriseText,bodyText,w/2)+400,0),sunriseText,font=bodyText,fill=0,align='left')
    drawBlack.text((indent(sunriseFull,sunText,w/2)+400,20),sunriseFull, font=sunText, fill=0, align='left')

###SUNSET TEXT###
    drawRed.text((indent(sunsetText,bodyText,w/2)+400,80), sunsetText,font=bodyText,fill=0,align='left')
    drawBlack.text((indent(sunsetFull,sunText,w/2)+400,100),sunsetFull, font=sunText, fill=0, align='left')



    epd.display(epd.getbuffer(imageBlack),epd.getbuffer(imageRed))
    
    epd.sleep()



except IOError as e:
    print(e)
