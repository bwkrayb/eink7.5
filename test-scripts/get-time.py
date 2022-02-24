import json
from datetime import datetime

data_dir = '/home/pi/eink7in5/data/'


f = open(data_dir + 'weather.json')
responseStr = f.read()
responseJson = json.loads(responseStr)
responseCurr = responseJson['current']
responseDaily = responseJson['daily'][1]


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
