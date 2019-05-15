
from oee.models import OEEData
from oee.common import DateStr
from oee.stub import STUB
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
			OeeServcie.UpDateRecord(MachineID,Type)
			result=OEEData.GetRecordByFilter(Filter)

		#print(result)
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
		result=OEEData.UpDateRecord(Filters,Contents)
		return result

	def Compute(MachineID,Type,TodaySTR):
		return STUB.getStubData();


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

	def GetViewData(RecordData):
		xList=[]
		yList=[]

		for item in RecordData['Data']:
			print(item)
			xList.append(item['x'])
			yList.append(item['y'])
		return xList,yList