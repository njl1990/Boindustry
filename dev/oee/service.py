
from models import OEEData
from common import DateStr
import string

class OeeServcie:
	# Load 类
	def LoadOeeData(MachineID,Type):
		TodaySTR=DateStr.getTodayStr()
		Filter ={
			"MachineID":MachineID,
			"Date":TodaySTR,
			"Type":Type
			} 
		result=OEEData.GetRecordByFilter(Filter)

		if OeeServcie.CheckUpdate(result):
			result=OeeServcie.UpDateRecord(MachineID,Type)
		return result;

######################################
	
	# Compute
	def UpDateRecord(MachineID,Type):
		TodaySTR=DateStr.getTodayStr()
		Filters={
			"MachineID":MachineID,
			"Date":TodaySTR,
			"Type":Type
		}

		Contents={
			'Data':OeeServcie.Compute(MachineID,Type,TodaySTR),
			'LastUpdate':DateStr.currentTimeStr()
		}
		print(Contents)
		OEEData.UpDateRecord(Filters,Contents)

	def Compute(MachineID,Type,TodaySTR):
		return 5


######################################

	# Others
	def CheckUpdate(Record):
		if Record is None:
			return True
		lastTimeStr=Record['LastUpdate']
		result=DateStr.commpareTime(lastTimeStr,DateStr.currentTimeStr())
		if (result+300)>0:
			return False
		else:
			return True 

OeeServcie.LoadOeeData('134SV20','OEE')
