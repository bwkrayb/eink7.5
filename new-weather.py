import os
import time
import logging
import requests
import urllib.request
import json
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
pic_dir = '/home/pi/eink7in5/pics'
data_dir = '/home/pi/eink7in5/data/'
img_dir = '/home/pi/eink7in5/images/jpg/'
h = epd.height #480
w = epd.width #800
wHalf = w/2
dt = datetime.now()
today=date.today()
month=today.strftime("%m")
monthText=today.strftime("%B")
year=today.strftime("%Y")
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
tempText = ImageFont.truetype(FONT, 150, index=0)
iconText = ImageFont.truetype(FONT, 80, index=0)
bodyText = ImageFont.truetype(FONT, 20, index=0)
timeText = ImageFont.truetype(FONT, 20, index=0)
condText = ImageFont.truetype(FONT, 45, index=0)
sunText = ImageFont.truetype(FONT,50,index=0)
dateText = ImageFont.truetype(FONT,35,index=0)
runText = ImageFont.truetype(FONT,65,index=0)
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

def drawSmallTemp(hourText,temp,width,height):
    drawRed.text((indent(hourText,bodyText,w/4)+ width, height),hourText,font=bodyText,fill=0,align='left')
    drawBlack.text((indent(temp,iconText,w/4)+ width, height+15),temp,font=iconText,fill=0,align='left')

def leftScreenPrint(textPrint,dataPrint,width,height):
    drawRed.text((indent(textPrint,bodyText,w/2)+width,height),textPrint,font=bodyText,fill=0,align='left')
    drawBlack.text((indent(dataPrint,sunText,w/2)+width,height+20),dataPrint, font=sunText, fill=0, align='left')

def runDataPrint(dataPrint,width,height):
    drawBlack.text((indent(dataPrint,runText,w/2)+width,height),dataPrint, font=runText, fill=0, align='left')

def printVert(textPrint,startHeight,width):
    i=0
    changeHeight=0
    while i < len(textPrint):
        drawRed.text((indent(textPrint[i],bodyText,w)+width,startHeight+changeHeight),textPrint[i],font=bodyText,fill=0,align='left')
        changeHeight+=bodyText.getsize(textPrint[i])[1]-5
        i+=1


#font.getsize(input)[1]

try:
    write_weather()
    readLastRun()
    check_last_run()
    if lastRunID != lastRunJson[0]['activityId']:
        print('now updating run file')
        write_running_month()
        write_running_last()
    else:
        print('no update needed.')
    

    readMonthRun()
    readLastRun()
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
    nextHourTemp = str(round(responseNextHour['temp']))+'??'

    nextHourTs2 = responseNextHour2['dt']
    nextHourDt2 = datetime.fromtimestamp(nextHourTs2)
    nextHourStr2 = nextHourDt2.strftime("%-I%p")
    nextHourTemp2 = str(round(responseNextHour2['temp']))+'??'

    lowTemp = str(round(responseToday['temp']['min']))+'??'
    highTemp = str(round(responseToday['temp']['max']))+'??'


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

    curTemp = str(round(responseCurr['temp']))# + '??'
    curFeel = str(round(responseCurr['feels_like']))# + '??'
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
    drawRed.text((250, 10), '??', font=iconText, fill=0, align='left') 

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

    if 14 <= int(dt.strftime('%H')) < 17:
        time = parser.parse(lastRunJson[0]['startDateTimeLocal'])
        timeStr = time.strftime("%x")
        today = date.today().strftime("%x")
        if timeStr == today:
            runDate = "Today"
        else:
            runDate = timeStr

        drawRed.text((indent("Last",dateText,w)+35, 360), "Last", font=dateText, fill=0, align='left')
        drawRed.text((indent("Run",dateText,w)+35, 400), "Run", font=dateText, fill=0, align='left')
        drawRed.text((indent(runDate,dateText,w)+35, 440), runDate, font=dateText, fill=0, align='left')
    
        distanceInt = round((lastRunJson[0]['distance'] * 0.621), 2)
        distance = str(distanceInt)
        duration = lastRunJson[0]['duration']
        timeMin = str(int(duration / 60))
        timeSec = str(int(duration % 60))
        calories = str(lastRunJson[0]['calories'])
        paceMin = str(int((duration / distanceInt) / 60)) 
        paceSec = str(int((duration / distanceInt) % 60)).zfill(2)
        data1=distance+"mi"
        label1="Dist"
        data2=timeMin+":"+timeSec
        label2="Time"
        data3=paceMin+":"+paceSec
        label3="Pace"
        data4=calories
        label4="Cals"   
    else:
        drawRed.text((indent("Stats:",dateText,w)+35, 360), "Stats:", font=dateText, fill=0, align='left')
        drawRed.text((indent(monthText,dateText,w)+35, 400), monthText, font=dateText, fill=0, align='left')
        drawRed.text((indent(year,dateText,w)+35, 440), year, font=dateText, fill=0, align='left')
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
        data1=runCount+" runs"
        label1="Cnt"
        data2=totalDist+"mi"
        label2="Dist"
        data3=longRun+"mi"
        label3="Long"
        data4=avgLen+"mi"
        label4="Avg"


    runHorPos=430
    labelHorPos=375
    runDataPrint(data1,runHorPos,160)
    printVert(label1,170,labelHorPos)
    runDataPrint(data2,runHorPos,240)
    printVert(label2,240,labelHorPos)
    runDataPrint(data3,runHorPos,320)
    printVert(label3,320,labelHorPos)
    runDataPrint(data4,runHorPos,400)
    printVert(label4,410,labelHorPos)


    epd.display(epd.getbuffer(imageBlack),epd.getbuffer(imageRed))
    
    epd.sleep()



except IOError as e:
    print(e)
