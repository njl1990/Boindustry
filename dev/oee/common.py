from bson import json_util
import time


class ResponseMsg:
	def success(data):
		context={
			'code':0,
			'msg':'success',
			'data':data,
		}
		return context

	def failed(msg):
		context={
			'code':-1,
			'msg':msg,
			'data':None,
		}
		return json_util.dumps(context)

class DateStr:
	def getTodayStr():
		return time.strftime('%Y-%m-%d',time.localtime(time.time()))

	def currentTime():
		return time.mktime(time.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),("%Y-%m-%d %H:%M:%S")))

	def currentTimeValue():
		currentStr=DateStr.currentTimeStr();
		return DateStr.getTimeValue(currentStr)

	def currentTimeStr():
		return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

	def strpCurrentTime(timeStr):
		return time.strptime(timeStr,("%Y-%m-%d %H:%M:%S"))

	def commpareTime(time1,time2):
		t1 = time.mktime(time.strptime(time1,("%Y-%m-%d %H:%M:%S")))
		t2 = time.mktime(time.strptime(time2,("%Y-%m-%d %H:%M:%S")))
		return int(t1) - int(t2)

	def getStartTimeValue(DateStr):
		# XXXX-XX-XX
		TodayStartDateTimeStr=DateStr+' 00:00:00'
		timeValue=time.mktime(time.strptime(TodayStartDateTimeStr,("%Y-%m-%d %H:%M:%S")))
		return timeValue

	def getTimeValue(DateStr):
		return time.mktime(time.strptime(DateStr,("%Y-%m-%d %H:%M:%S")))

	def getCurrentHour():
		return int(time.strftime("%H", time.localtime()))