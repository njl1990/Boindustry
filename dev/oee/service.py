
from oee.models import OEEData
from oee.models import BaseData
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
		## load from dbcatch
		result=OEEData.GetRecordByFilter(Filter)

		## judgement update
		if OeeServcie.CheckUpdate(result):
			print('--- [Update Record] --- ')
			# updateD data
			OeeServcie.UpDateRecord(MachineID,Type)
			result=OEEData.GetRecordByFilter(Filter)
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

		# print('ComputeResult:')
		# print(Contents)
		
		result=OEEData.UpDateRecord(Filters,Contents)
		return result


	def ComputeToHours(timeValue,hour,datalist,FIST_PRODUCT_TIME):

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
			print('fault:' + str(item['testTime']/1000)+'<'+str((timeValue+int(hour)*3600)))


		#不良数量
		REJECTS=ACTUAL_OUTPUTE-YIELD
		print('H='+str(hour)+';YIELD='+str(YIELD))
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
		TUR=""
		if ACTUAL_OUTPUTE > 0:
			TUR=1

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
		print(result)
		return result


	# 计算数据
	def Compute(MachineID,Type,TodaySTR):
		#拉取数据

		##获取当天00点时间戳
		timeValue=DateStr.getStartTimeValue(TodaySTR)
		datalist=BaseData.GetRecordByFilter({'instruName':MachineID,'testTime':{'$gte':timeValue}})


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

		while i<EndHour:
			result=OeeServcie.ComputeToHours(timeValue,i,DataCatch,FIST_PRODUCT_TIME)
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


######################################

	# Others
	def CheckUpdate(Record):
		if Record is None:
			return True
		lastTimeStr=Record['LastUpdate']
		result=DateStr.commpareTime(lastTimeStr,DateStr.currentTimeStr())
		if (result+3000)>0:
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

#OeeServcie.Compute('TLZH-01-08-3000416','YR',DateStr.getTodayStr())