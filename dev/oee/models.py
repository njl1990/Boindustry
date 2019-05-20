from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId
import oee.stub
# Create your models here.

class DB:

	db_host = 'localhost'
	db_port = 27017
	db_name = 'oeedb'
	
	def DBClient():
		mongoClient = MongoClient(DB.db_host,DB.db_port)
		DBClient = mongoClient[DB.db_name]
		return DBClient

class OEEData:
	# Create
	def UpDateRecord(filters,Content):
		oeeRecord = DB.DBClient()['mainrcd']
		result=oeeRecord.update(filters,{'$set':Content}, upsert=True)
		return result

	# Load Load MainInfo
	def GetRecordByFilter(filters):
		oeeRecord = DB.DBClient()['mainrcd']
		item=oeeRecord.find_one(filters)
		return item

	def LoadMachineList(currentValue):
		oeeRecord = DB.DBClient()['basedata']
		#result=oeeRecord.aggregate([{'$group':{'_id':"$instruName"},'count':{'$sum':1},'type':{'$first':'$instruType'},'dscp':{'$first':"$description"}}])
		result=oeeRecord.aggregate([
			{'$match':{'testTime':{'$gt':currentValue}}},
			{'$group':{'_id':'$instruName','instruName':{'$first':'$instruName'},'count':{'$sum':1},'type':{'$first':'$instruType'},'dscp':{'$first':"$description"}}}
		])
		MachineList=[]
		for item in result:
			MachineList.append(item)
		return MachineList

class BaseData:
	# Load Load MainInfo
	def GetRecordByFilter(filters):
		oeeRecord = DB.DBClient()['basedata']
		item=oeeRecord.find(filters)
		return item

class OEEConfData:
	# Load ConfData
	def GetConfByFilter(filters):
		conf = DB.DBClient()['conf']
		item=conf.find_one(filters)
		return item

	# Load ConfDataList
	def LoadConfListByFilter(filters):
		conf = DB.DBClient()['conf']
		result=conf.find(filters)
		List=[]
		for item in result:
			 List.append(item)
		return List

	# Load ConfDataList
	def Delete(filters):
		conf = DB.DBClient()['conf']
		result=conf.remove(filters)
		return result

	# Update Conf
	def Update(filters,set):
		conf = DB.DBClient()['conf']
		result=conf.update(filters,set)
		return result 

	def Insert(obj):
		conf = DB.DBClient()['conf']
		result=conf.insert(obj)
		return result 
	################################
'''
class CTask:
	def CreateCTask(data):
		ctask = DB.DBClient()['CooperationTask']
		json_str=data.replace('\'','\"');
		print('CMD:'+json_str)
		obj=json_util.loads(json_str)
		obj['CTopicConf']=CTopic.CTopicGetAttr(obj['CTopicID'],'CTopicConf')
		print('result:'+str(obj))
		result=ctask.insert(obj)
		return result

	def CTaskListByfilter(filter):
		ctopic = DB.DBClient()['CooperationTask']
		ctopic_cursor=ctopic.find(filter)
		ctopic_list=[]

		for ctopic in ctopic_cursor:
			print(ctopic)
			# use title - value structure
			ctopicSelectorObject={
				'CTaskName':ctopic['CTaskName'],
				'id':ctopic['_id'],
				'CStatus':ctopic['CStatus'],
				'Cooperator':(' '.join(Cooperator.getNameByIDArray(ctopic['Cooperators']))),
				}
			ctopic_list.append(ctopicSelectorObject)
		return ctopic_list

	def UpdateStatus(ID):
		ctask = DB.DBClient()['CooperationTask']
		item=ctask.find_one({"_id": ObjectId(ID)})
		statusflag = 0
		nextStatus =item["CStatus"]

		print('CSTATUS:'+item["CStatus"])

		for status in item["CTopicConf"]:
			print(status)
			if statusflag is 1:
				nextStatus = status;
				break
				print('输出：'+nextStatus)
			elif status == item["CStatus"]:
				print('匹配到：'+status)
				statusflag=1
		# update data 
		if item["CStatus"]==nextStatus:
			return -1
		else:
			ctask.update({"_id": ObjectId(ID)},{"$set":{"CStatus":nextStatus}})
		return nextStatus
class CTopic:

	# get CTopic select items
	def CTopicSelectListByfilter(filter):
		ctopic = DB.DBClient()['CooperationTopic']
		ctopic_cursor=ctopic.find(filter)
		ctopic_list=[]

		for ctopic in ctopic_cursor:
			# use title - value structure
			ctopicSelectorObject={
				'title':ctopic['CTopicName'],
				'value':ctopic['_id'],
				'prefix':ctopic['CTopicPrefix']
				}
			ctopic_list.append(ctopicSelectorObject)
		return ctopic_list

	def CTopicById(ID):
		ctopic = DB.DBClient()['CooperationTopic']
		item=ctopic.find_one({"_id": ObjectId(ID)})
		return item

	def CreateCTopic(data):
		ctopic = DB.DBClient()['CooperationTopic']
		result=ctopic.insert(data)
		return result
	def CTopicGetAttr(ID,AttrStr):
		ctopic = DB.DBClient()['CooperationTopic']
		item=ctopic.find_one({"_id": ObjectId(ID)})
		return item[AttrStr]

class Cooperator:
	def CooperatorSelectListByfilter(filter):
		cooperatorClient = DB.DBClient()['Cooperators']

		cooperator_cursor=cooperatorClient.find(filter)
		cooperator_list=[]
		for cooperator in cooperator_cursor:
			print(cooperator)
			# use title - value structure
			cooperatorSelectorObject={
				'title':cooperator['Name'],
				'value':cooperator['_id'],
				}
			cooperator_list.append(cooperatorSelectorObject)
		return cooperator_list

	def CooperatorById(ID):
		ctopic = DB.DBClient()['Cooperators']
		ctopicSelectorObject=ctopic.find_one({"_id": ObjectId(ID)})
		return ctopicSelectorObject

	def getNameByIDArray(array):
		NameList=[]
		for item in array:
			ctopicSelectorObject=Cooperator.CooperatorById(item)
			NameList.append(ctopicSelectorObject['Name'])
		return NameList

'''