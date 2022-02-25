import json
from datetime import datetime

data_dir = '/home/pi/eink7in5/data/'


f = open(data_dir + 'weather.json')
responseStr = f.read()
responseJson = json.loads(responseStr)
responseCurr = responseJson['current']
responseDaily = responseJson['daily'][1]
responseHiLo = responseJson['daily'][0]
responseHourlyOne = responseJson['hourly'][0]
responseHourlyTwo = responseJson['hourly'][1]

hourOneTs = responseHourlyOne['dt']
hourOneDt = datetime.fromtimestamp(hourOneTs)
hourOneStr = hourOneDt.strftime("%-I:%M:%S %p")
print('Hour1: ' + hourOneStr)

hourTwoTs = responseHourlyTwo['dt']
hourTwoDt = datetime.fromtimestamp(hourTwoTs)
hourTwoStr = hourTwoDt.strftime("%-I:%M:%S %p")
print('Hour2: ' + hourTwoStr)


print(responseHiLo['temp']['max'])


curTemp = str(round(responseCurr['temp']))# + '°'
curFeel = str(round(responseCurr['feels_like']))# + '°'
curDesc = responseCurr['weather'][0]['description'].title().split()
curID = responseCurr['weather'][0]['id']

curTs = responseCurr['dt']
curDt = datetime.fromtimestamp(curTs)
#curDtStr = curDt.strftime("%-I:%M:%S %p")
curDtStr = curDt.strftime("%c")
print(curDtStr)

sunriseTs = responseDaily['sunrise']
sunriseDt = datetime.fromtimestamp(sunriseTs)
sunriseStr = sunriseDt.strftime("%-I:%M:%S %p")
dailyDate = sunriseDt.strftime("%c")

sunsetTs = responseDaily['sunset']
sunsetDt = datetime.fromtimestamp(sunsetTs)
sunsetStr = sunsetDt.strftime("%-I:%M:%S %p")


print(dailyDate)
print("Sunrise: " + sunriseStr)
print("Sunset: " + sunsetStr)


f.close()
