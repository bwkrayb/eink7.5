import os
import time
import logging
import requests
import json
from libs.functions import get_icon, indent, indentThirds,  paste, write_weather, get_desc, imageIndent, imageIndentThirds
from datetime import datetime
from libs.waveshare_epd import epd7in5b_V2
from PIL import Image, ImageDraw, ImageFont
from settings import API_KEY

pic_dir = '/home/pi/eink7in5/pics'
data_dir = '/home/pi/eink7in5/data/'
img_dir = '/home/pi/eink7in5/images/jpg/'

FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'

try:
    # Display init, clear
    epd = epd7in5b_V2.EPD()
    epd.init()
    epd.Clear() # 0: Black, 255: White

    h = epd.height #480
    w = epd.width #800
    #print('width:', w) #800
    #print('height:', h) #480
    hHalf = epd.height / 2
    wHalf = epd.width / 2


    #### IMAGE CODE ####
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
    dt = datetime.now()

    write_weather()
    time.sleep(5)
    f = open(data_dir + 'weather.json')
    responseStr = f.read()
    responseJson = json.loads(responseStr)
    responseCurr = responseJson['current']
    responseNow = responseJson['hourly'][0]

    if int(dt.strftime('%H')) > 21:
        responseDailySS = responseJson['daily'][1]
        sunsetText = 'Tomorrow'
    else:
        responseDailySS = responseJson['daily'][0]
        sunsetText = 'Today'

    if int(dt.strftime('%H')) > 8:
        responseDailySR = responseJson['daily'][1]
        sunriseText = 'Tomorrow'
    else:
        responseDailySR = responseJson['daily'][0]
        sunriseText = 'Today'

    responseNextHour = responseJson['hourly'][1]

    nextHourTs = responseNextHour['dt']
    nextHourDt = datetime.fromtimestamp(nextHourTs)
    nextHourStr = nextHourDt.strftime("%-I%p")
    nextHourTemp = str(round(responseNextHour['temp']))+'°'

    responseNextHour2 = responseJson['hourly'][2]
    nextHourTs2 = responseNextHour2['dt']
    nextHourDt2 = datetime.fromtimestamp(nextHourTs2)
    nextHourStr2 = nextHourDt2.strftime("%-I%p")
    nextHourTemp2 = str(round(responseNextHour2['temp']))+'°'

    responseHiLo = responseJson['daily'][0]
    lowTemp = str(round(responseHiLo['temp']['min']))+'°'
    highTemp = str(round(responseHiLo['temp']['max']))+'°'


    curTs = responseCurr['dt']
    curDt = datetime.fromtimestamp(curTs)
    curDtStr = curDt.strftime("%-I:%M%p")
    #curDtStr = curDt.strftime("%c")
    print(curDtStr)

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
    curDesc = responseNow['weather'][0]['description'].title().split()
    #curID = responseCurr['weather'][0]['id']
    curID = responseNow['weather'][0]['id']

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
    drawRed.text((indent('Current: '+curDtStr,bodyText,wHalf)-50,0),'Current: '+curDtStr,font=bodyText,fill=0,align='left')
    drawBlack.text((indent(curTemp,tempText,wHalf)-50, 2), curTemp, font=tempText, fill=0, align='left')
    drawRed.text((250, 10), '°', font=iconText, fill=0, align='left') 

###CONDITION TEXT###
    drawBlack.text((indent(curDesc1,condText,wHalf)-50, 160), curDesc1, font=condText, fill=0, align='left')
    if len(curDesc) > 1:
        drawBlack.text((indent(curDesc2,condText,wHalf)-50, 210), curDesc2, font=condText, fill=0, align='left')

###LOW TEXT###
    drawRed.text((indent('Low',bodyText,wHalf/2),265),'Low',font=bodyText,fill=0,align='left')
    drawBlack.text((indent(lowTemp,iconText,wHalf/2),280),lowTemp,font=iconText,fill=0,align='left')

###HIGH TEXT###
    drawRed.text((indent('High',bodyText,wHalf/2),380),'High',font=bodyText,fill=0,align='left')
    drawBlack.text((indent(highTemp,iconText,wHalf/2),395),highTemp,font=iconText,fill=0,align='left')

###NEXT HOUR TEXT###
    drawRed.text((indent(nextHourStr,bodyText,wHalf/2)+200,265),nextHourStr,font=bodyText,fill=0,align='left')
    drawBlack.text((indent(nextHourTemp,iconText,wHalf/2)+200,280),nextHourTemp,font=iconText,fill=0,align='left')

###NEXT HOUR 2 TEXT###
    drawRed.text((indent(nextHourStr2,bodyText,wHalf/2)+200,380),nextHourStr2,font=bodyText,fill=0,align='left')
    drawBlack.text((indent(nextHourTemp2,iconText,wHalf/2)+200,395),nextHourTemp2,font=iconText,fill=0,align='left')

###SUNRISE TEXT###
    drawRed.text((indent(sunriseText,bodyText,400)+400,0),sunriseText,font=bodyText,fill=0,align='left')
    drawBlack.text((indent(sunriseFull,sunText,400)+400,20),sunriseFull, font=sunText, fill=0, align='left')

###SUNSET TEXT###
    drawRed.text((indent(sunsetText,bodyText,400)+400,80), sunsetText,font=bodyText,fill=0,align='left')
    drawBlack.text((indent(sunsetFull,sunText,400)+400,100),sunsetFull, font=sunText, fill=0, align='left')




    epd.display(epd.getbuffer(imageBlack),epd.getbuffer(imageRed))
    
    epd.sleep()
    f.close()



except IOError as e:
    print(e)
    f.close()
