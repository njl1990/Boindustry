
from oee.models import OEEData
from oee.models import BaseData
from oee.models import OEEConfData
from oee.common import DateStr
from oee.stub import STUB
from bson import json_util
from bson.objectid import ObjectId
import string

class OeeServcie:
#Load Method 

	def LoadOeeData(MachineID,Type):
		TodaySTR=DateStr.getTodayStr()
		Filter ={
			"MachineID":MachineID,
			"Date":TodaySTR,
			"Type":Type
			} 
		## load from dbcatch
		result=OEEData.GetRecordByFilter(Filter)

		## judgement update
		if OeeServcie.CheckUpdate(result):
			# updateD data
			OeeServcie.UpDateRecord(MachineID,Type)
			result=OEEData.GetRecordByFilter(Filter)
		return result;

	def LoadMachineList():
		currentValue=DateStr.getStartTimeValue(DateStr.getTodayStr())*1000
		result=OEEData.LoadMachineList(currentValue)
		return result

	def LoadMachineInfo(instruName):
		currentValue=DateStr.getStartTimeValue(DateStr.getTodayStr())*1000
		MachineList=OEEData.LoadMachineList(currentValue)
		for item in MachineList:
			if item['instruName'] == instruName:
				return item;
		return None;

	## OeeConfig
	def LoadWorkingTime():
		WT=None
		WTObj=OeeServcie.GetOeeConf({'type':'WT'})
		WT=WTObj['value']
		## print('WT=')
		## print(WTObj)
		return WT

	def LoadStandardTimeList():
		StandardTimeList=OeeServcie.LoadOeeConfList({'type':'ST'})
		List=[]
		for item in StandardTimeList:
			conf={
					'id':item['_id'],
					'value':item['value'],
				}
			List.append(conf)
		return List

	def LoadTransactionData():
		DtObj=OeeServcie.GetOeeConf({'type':'DT','date':DateStr.getTodayStr()})
		DT = 0
		if DtObj is not None:
			DT = DtObj['value']

		CotObj=OeeServcie.GetOeeConf({'type':'COT','date':DateStr.getTodayStr()})
		COT = 0
		if CotObj is not None:
			COT = CotObj['value']

		AtObj=OeeServcie.GetOeeConf({'type':'AT','date':DateStr.getTodayStr()})
		AT = 0
		if AtObj is not None:
			AT = AtObj['value']

		RhtObj=OeeServcie.GetOeeConf({'type':'RHT','date':DateStr.getTodayStr()})
		RHT = 0
		if RhtObj is not None:
			RHT = RhtObj['value']


		PdtObj=OeeServcie.GetOeeConf({'type':'PDT','date':DateStr.getTodayStr()})
		PDT = 0
		if PdtObj is not None:
			PDT = PdtObj['value']

		WT=OeeServcie.GetAttr('WT')

		result = {
			'DT': DT,
			'COT': COT,
			'AT': AT,
			'RHT': RHT,
			'PDT': PDT,
			'WT':WT,
		}

		return result

	def LoadOeeConfList(filters):
		ConfList = OEEConfData.LoadConfListByFilter(filters)
		return ConfList

	def GetOeeConf(filters):
		Conf = OEEConfData.GetConfByFilter(filters)
		return Conf

#Update&Delete Method
	def DeleteOeeConf(ID):
		result=OEEConfData.Delete({'_id':ObjectId(ID)})
		return None

	def UpdateOeeConf(ConfObj):
		if ConfObj['_id'] == '':		
			filters = {
				"type": ConfObj['type']
			}
		else:
			filters = {
				"_id": ObjectId(ConfObj['_id']),
				"type": ConfObj['type'],
			}
		sets={"$set":{"value":ConfObj['value']}}
		if ConfObj['type']=='ST':
			#Get value first
			oldObj = OeeServcie.GetOeeConf(filters)
			oldObj['value']['value']=int(ConfObj['value'])
			newValue=oldObj['value']
			sets={"$set":{"value":newValue}}
			result=OEEConfData.Update(filters,sets)
		else:	
			result=OEEConfData.Update(filters,sets)
		return result

	def CreateOeeConf(ConfObj):
		result=OEEConfData.Insert(ConfObj)
		return result

	def UpdateOeeTransaction(ConfObj):
		filters = {
				'type':ConfObj['type'],
				'date':DateStr.getTodayStr(),
			}

		oldObj = OeeServcie.GetOeeConf(filters)

		if oldObj is None:
			dataObj={
				'type':ConfObj['type'],
				'date':DateStr.getTodayStr(),
				'value':ConfObj['value'],
			}
			result=OEEConfData.Insert(dataObj)
			return result
		sets={"$set":{"value":ConfObj['value']}}
		result=OEEConfData.Update(filters,sets)
		return result
	
#Compute Method
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

		# print('ComputeResult:')
		# print(Contents)
		
		result=OEEData.UpDateRecord(Filters,Contents)
		return result

	def ComputeToHours(timeValue,hour,datalist,FIST_PRODUCT_TIME,TUR_attr):


		#实际产出数量
		ACTUAL_OUTPUTE=0
		
		#良品数量
		YIELD=0

		#统计不良数/良品数
		for item in datalist:
			if item['testTime']/1000<(timeValue+int(hour)*3600):
				ACTUAL_OUTPUTE=ACTUAL_OUTPUTE+1
				#计算良品率
				if 'No error' in item['message']:
					YIELD=YIELD+1;

		#不良数量
		REJECTS=ACTUAL_OUTPUTE-YIELD
		#产出统计时间
		OUTPUT_TIME=(DateStr.currentTimeValue()+int(hour)*3600)-FIST_PRODUCT_TIME 


		#标准工时
		STANDARD_TIME=STUB.getStandardTime();	

		#计算性能稼动率
		PER=""
		if ACTUAL_OUTPUTE>0:
			PER=round(ACTUAL_OUTPUTE/((3600/STANDARD_TIME)*OUTPUT_TIME),4)	#性能稼动率

		#计算良品率
		YR =""
		if ACTUAL_OUTPUTE > 0:
			YR = YIELD/ACTUAL_OUTPUTE

		#计算时间稼动率
		DT=TUR_attr['DT']
		COT=TUR_attr['COT']
		AT=TUR_attr['AT']
		RHT=TUR_attr['RHT']
		WT=TUR_attr['WT']
		PDT=TUR_attr['PDT']

		TUR=""
		if ACTUAL_OUTPUTE > 0:
			if WT-PDT > 0:
				TUR=1-(DT+COT+AT+RHT)/(WT-PDT)

		#计算OEE
		OEE=""
		if ACTUAL_OUTPUTE > 0:
			OEE = TUR*PER*YIELD

		#输出结果

		result={
			'OEE':OEE,
			'TUR':TUR,
			'YR':YR,
			'PER':PER,
			'ACTUAL_OUTPUTE':ACTUAL_OUTPUTE,
			'YIELD':YIELD,
			'OUTPUT_TIME':OUTPUT_TIME,
			'REJECTS':REJECTS,
			'STANDARD_TIME':STANDARD_TIME,
			'FIST_PRODUCT_TIME':FIST_PRODUCT_TIME,
		}
		'''
		print('-----------------------------')
		print('H='+str(hour))
		print('TUR_ATTR='+str(TUR_attr))
		print(result)
		print('-----------------------------')
		'''
		return result

	# 计算数据
	def Compute(MachineID,Type,TodaySTR):
		#拉取数据

		##获取当天00点时间戳
		timeValue=DateStr.getStartTimeValue(TodaySTR)
		datalist=BaseData.GetRecordByFilter({'instruName':MachineID,'testTime':{'$gte':(timeValue*1000)}})
		


		# 根据当天的每个小时来计算数据
		# 起点时间
		StartTimePoint = timeValue
		# 当前小时数
		EndHour =DateStr.getCurrentHour()+1

		# 首件时间
		FIST_PRODUCT_TIME = None

		DataCatch = []

		for item in datalist:
			DataCatch.append(item)
			if FIST_PRODUCT_TIME is None:
				FIST_PRODUCT_TIME=item['testTime']/1000
			elif  FIST_PRODUCT_TIME<item['testTime']/1000:
				FIST_PRODUCT_TIME=item['testTime']/1000

		#print ('FIST_PRODUCT_TIME='+str(FIST_PRODUCT_TIME))

		OEEList=[]
		YRList=[]
		PERList=[]
		TURList=[]
		i=0


		DT=OeeServcie.GetAttr('DT')
		COT=OeeServcie.GetAttr('COT')
		AT=OeeServcie.GetAttr('AT')
		RHT=OeeServcie.GetAttr('RHT')
		WT=OeeServcie.GetAttr('WT')
		PDT=OeeServcie.GetAttr('PDT')

		TUR_attr = {
			'DT': DT,
			'COT': COT,
			'AT': AT,
			'RHT': RHT,
			'PDT': PDT,
			'WT':WT,
		}

		while i<EndHour:
			result=OeeServcie.ComputeToHours(timeValue,i,DataCatch,FIST_PRODUCT_TIME,TUR_attr)
			OEEList.append({'x':i,'y':result['OEE']})
			YRList.append({'x':i,'y':result['YR']})
			PERList.append({'x':i,'y':result['PER']})
			TURList.append({'x':i,'y':result['TUR']})
			i=i+1

		# Save 

		# return 

		if Type is 'OEE':
			return OEEList
		if Type is 'YR':
			return YRList
		if Type is 'PER':
			return PERList
		if Type is 'TUR':
			return TURList
#Other Method


	def GetAttr(type):
		if type == 'WT':
			obj=OeeServcie.GetOeeConf({'type':'WT'})
			return int(obj['value'])
		obj=OeeServcie.GetOeeConf({'type':type,'date':DateStr.getTodayStr()})
		if obj is None:
			return 0
		return int(obj['value'])
	# Others
	def CheckUpdate(Record):
		if Record is None:
			return True
		lastTimeStr=Record['LastUpdate']
		result=DateStr.commpareTime(lastTimeStr,DateStr.currentTimeStr())
		if (result+0)>0:
			return False
		else:
			return True 

	def GetViewData(xFeilds,RecordData):
		yList=[]
		for item in xFeilds:
			Y=None	
			for value in RecordData['Data']:
				if int(value['x'])==int(item):
					Y=value['y']*100
			if Y is None:
				Y=0
			yList.append(Y)
		return yList

#Test 
## OeeServcie.LoadWorkingTime();
## OeeServcie.LoadStandardTimeList();