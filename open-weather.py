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
    iconText = ImageFont.truetype(FONT, 90, index=0)
    bodyText = ImageFont.truetype(FONT, 30, index=0)
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

    curTs = responseCurr['dt']
    curDt = datetime.fromtimestamp(curTs)
    curDtStr = curDt.strftime("%-I:%M:%S %p")
    #curDtStr = curDt.strftime("%c")
    print(curDtStr)

    sunriseTs = responseDailySR['sunrise']
    sunriseDt = datetime.fromtimestamp(sunriseTs)
    sunriseStr = sunriseDt.strftime("%-I:%M:%S %p")
    print('SR ' + sunriseText + ' ' + sunriseStr)

    sunsetTs = responseDailySS['sunset']
    sunsetDt = datetime.fromtimestamp(sunsetTs)
    sunsetStr = sunsetDt.strftime("%-I:%M:%S %p")
    print('SS ' + sunsetText + ' ' + sunsetStr)

    curTemp = str(round(responseCurr['temp']))# + '°'
    curFeel = str(round(responseCurr['feels_like']))# + '°'
    curDesc = responseCurr['weather'][0]['description'].title().split()
    curID = responseCurr['weather'][0]['id']

    if len(curDesc) > 2:
        custDesc = get_desc(curID).split()
        curDesc1 = custDesc[0]
        curDesc2 = custDesc[1]
    elif len(curDesc) == 2:
        curDesc1 = curDesc[0]
        curDesc2 = curDesc[1]
    else:
        curDesc1 = curDesc[0] 

    drawBlack.rectangle((400,240,800,480), fill=1, outline=0)
    drawRed.rectangle((300, 0, 600, 240), fill=1, outline=0)

    logo = get_icon(curID)
    #imageRed.paste(logo, (20, 30))
    imageRed.paste(logo, (imageIndent(logo,w)+50,30))

    drawBlack.text((indent(curTemp,tempText,wHalf)-50, 2), curTemp, font=tempText, fill=0, align='left')

    #drawBlack.text((20, 2), curTemp, font=tempText, fill=0, align='left')
    drawBlack.text((250, 2), '°', font=iconText, fill=0, align='left') 

    drawBlack.text((indent(curDesc1,condText,wHalf)-50, 160), curDesc1, font=condText, fill=0, align='left')
    if len(curDesc) > 1:
        drawBlack.text((indent(curDesc2,condText,wHalf)-50, 200), curDesc2, font=condText, fill=0, align='left')

    drawBlack.text((indent('Sunrise:',sunText,300)+500,0),'Sunrise:',font=sunText,fill=0,align='left')
    drawBlack.text((indent(sunriseStr,sunText,300)+500,80),sunriseStr, font=sunText, fill=0, align='left')
    drawBlack.text((indent('Sunset:',sunText,300)+500,160),'Sunset:',font=sunText,fill=0,align='left')
    drawBlack.text((indent(sunsetStr,sunText,300)+500,240),sunsetStr, font=sunText, fill=0, align='left')


    epd.display(epd.getbuffer(imageBlack),epd.getbuffer(imageRed))
    




    f.close()

except IOError as e:
    print(e)
    f.close()
