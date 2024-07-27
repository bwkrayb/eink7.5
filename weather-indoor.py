import os
import time
import logging
import requests
import urllib.request
import json
import bme680
from libs.functions import get_icon, indent, indentThirds,  paste, write_weather, write_running_month, write_running_last, get_desc, imageIndent, imageIndentThirds
from datetime import datetime,date
from dateutil import parser
from libs.waveshare_epd import epd7in5b_V2
from PIL import Image, ImageDraw, ImageFont
from settings import API_KEY,SMASHRUN_KEY


# Display init, clear
epd = epd7in5b_V2.EPD()
epd.init()
epd.Clear() # 0: Black, 255: White

# setup directories
pic_dir = '/home/pi/eink7in5/pics'
data_dir = '/home/pi/eink7in5/data/'
img_dir = '/home/pi/eink7in5/images/jpg/'

# screen size variables
h = epd.height #480
w = epd.width #800
wHalf = w/2

# date variables
dt = datetime.now()
today=date.today()
month=today.strftime("%m")
monthText=today.strftime("%B")
year=today.strftime("%Y")

########## font variables
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
tempText = ImageFont.truetype(FONT, 150, index=0)
iconText = ImageFont.truetype(FONT, 80, index=0)
indoorText = ImageFont.truetype(FONT, 100, index=0)
bodyText = ImageFont.truetype(FONT, 20, index=0)
timeText = ImageFont.truetype(FONT, 20, index=0)
condText = ImageFont.truetype(FONT, 45, index=0)
sunText = ImageFont.truetype(FONT,50,index=0)
dateText = ImageFont.truetype(FONT,35,index=0)
rightText = ImageFont.truetype(FONT,65,index=0)

########## image variables
imageBlack = Image.new(mode='1', size=(w, h), color=255)
drawBlack = ImageDraw.Draw(imageBlack)
imageRed = Image.new(mode='1', size=(w, h), color=255)
drawRed = ImageDraw.Draw(imageRed)

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

# added merica units temp
fTemp = str(round((sensor.data.temperature * 1.8) + 32))+'°'
pressure = str(sensor.data.pressure)+'hPa'
humidity = str(round(sensor.data.humidity))+'%'


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

def drawSmallTemp(hourText,temp,width,height):
    drawRed.text((indent(hourText,bodyText,w/4)+ width, height),hourText,font=bodyText,fill=0,align='left')
    drawBlack.text((indent(temp,iconText,w/4)+ width, height+15),temp,font=iconText,fill=0,align='left')

def drawSmallTempRight(hourText,temp,width,height):
    drawRed.text((indent(hourText,bodyText,w/2)+ width, height),hourText,font=bodyText,fill=0,align='left')
    drawBlack.text((indent(temp,indoorText,w/2)+ width, height+15),temp,font=indoorText,fill=0,align='left')

def leftScreenPrint(textPrint,dataPrint,width,height):
    drawRed.text((indent(textPrint,bodyText,w/2)+width,height),textPrint,font=bodyText,fill=0,align='left')
    drawBlack.text((indent(dataPrint,sunText,w/2)+width,height+20),dataPrint, font=sunText, fill=0, align='left')

def rightDataPrint(dataPrint,width,height):
    drawBlack.text((indent(dataPrint,rightText,w/2)+width,height),dataPrint, font=rightText, fill=0, align='left')

def rightLabelPrint(textPrint,width,height):
    drawRed.text((indent(textPrint,bodyText,w/2)+width,height),textPrint,font=bodyText,fill=0,align='left')


#font.getsize(input)[1]

try:
    write_weather()
    readWeather()


    if int(dt.strftime('%H')) > 21:
        responseDailySS = responseTomorrow
        sunsetText = 'Sunset - Tomorrow'
    else:
        responseDailySS = responseToday
        sunsetText = 'Sunset - Today'

    if int(dt.strftime('%H')) > 8:
        responseDailySR = responseTomorrow
        sunriseText = 'Sunrise - Tomorrow'
    else:
        responseDailySR = responseToday
        sunriseText = 'Sunrise - Today'


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
    sunriseFull = sunriseStr

    sunsetTs = responseDailySS['sunset']
    sunsetDt = datetime.fromtimestamp(sunsetTs)
    sunsetStr = sunsetDt.strftime("%-I:%M%p")
    sunsetFull = sunsetStr

    curTemp = str(round(responseCurr['temp']))# + '°'
    curFeel = str(round(responseCurr['feels_like']))# + '°'
    curDesc = responseCurr['weather'][0]['description'].title().split()
    #curDesc = responseThisHour['weather'][0]['description'].title().split()
    curID = responseCurr['weather'][0]['id']
    #curID = responseThisHour['weather'][0]['id']

    if len(curDesc) > 2:
        custDesc = get_desc(curID).split()
        curDesc1 = custDesc[0]
        curDesc2 = custDesc[1]
    elif len(curDesc) == 2:
        curDesc1 = curDesc[0]
        curDesc2 = curDesc[1]
    else:
        curDesc1 = curDesc[0] 


    logo = get_icon(curID)
    logoLg = logo.resize((64,64))
    imageRed.paste(logoLg, (imageIndent(logo,w)-50,60))


###TEMP TEXT###
    drawRed.text((indent('Current: '+curDtStr,bodyText,w/2)-50,0),'Current: '+curDtStr,font=bodyText,fill=0,align='left')
    drawBlack.text((indent(curTemp,tempText,w/2)-50, 2), curTemp, font=tempText, fill=0, align='left')
    drawRed.text((250, 10), '°', font=iconText, fill=0, align='left') 

###CONDITION TEXT###
    drawBlack.text((indent(curDesc1,condText,w/2)-50, 160), curDesc1, font=condText, fill=0, align='left')
    if len(curDesc) > 1:
       drawBlack.text((indent(curDesc2,condText,w/2)-50, 210), curDesc2, font=condText, fill=0, align='left')


    drawSmallTemp('Low',lowTemp,0,265)
    drawSmallTemp('High',highTemp,0,380)
    drawSmallTemp(nextHourStr,nextHourTemp,170,265)
    drawSmallTemp(nextHourStr2,nextHourTemp2,170,380)

    leftScreenPrint(sunriseText,sunriseFull,400,0)
    leftScreenPrint(sunsetText,sunsetFull,400,80)

    runHorPos=400
    #rightLabelPrint('Indoor Temp',runHorPos,160)
    # rightDataPrint(fTemp,runHorPos,240)
    # rightDataPrint(humidity,runHorPos,320)
    # rightDataPrint(pressure,runHorPos,400)

    drawSmallTempRight('Indoor Temp',fTemp,runHorPos,180)
    drawSmallTempRight('Humidity',humidity,runHorPos,330)
    #drawSmallTempRight('Pressure',pressure,runHorPos,385)


    epd.display(epd.getbuffer(imageBlack),epd.getbuffer(imageRed))
    
    epd.sleep()



except IOError as e:
    print(e)
