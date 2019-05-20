
import json
import urllib.request
from bson import json_util
from pymongo import MongoClient
import time

class DB:

	db_host = 'localhost'
	db_port = 27017
	db_name = 'oeedb'

	def insertDB(obj):
		##print(json_util.dumps(obj))
		mongoClient = MongoClient(DB.db_host,DB.db_port)
		DBClient = mongoClient[DB.db_name]
		oeeRecord = DBClient['basedata']
		#查询是否存在
		item=oeeRecord.find_one({'instrID':obj['instrID']})
		if item is None:
			print('Save Data:'+str(obj['instrID']))
			result=oeeRecord.insert_one(obj)
			return result
		else:
			print('Update Data:'+str(obj))
			result=oeeRecord.update_many({'instrID':obj['instrID']},{'$set':{'seriesNumber':obj['seriesNumber']}})
			return result
		return

def getPostData(i):
	dataObj={
		"dbName": "atsData",
		"tableName": "instrument",
		"desc":True,
		"columnsToGet":["instrID","instruName","instruType","description","seriesNumber","message","usedTime","testTime"],
		"limit":10,
		"filter":"instrID = '"+str(i)+"'",
		}
	headersObj = {'tpye':'POST','Content-Type':'application/json;charset=utf-8','dataType':"json"}
	request = urllib.request.Request(url="http://rest.gziiot.htdata.com:7777/api/data/GetRange?tid=14220&k=cAc6GJVf4DY21g5XR5LcHnkntWH8fkpv",headers=headersObj,data=json_util.dumps(dataObj).encode("utf-8"))
	response = urllib.request.urlopen(request)
	return response.read().decode("utf-8")



## Main

def main():

	i=249718
	mongoClient = MongoClient(DB.db_host,DB.db_port)
	DBClient = mongoClient[DB.db_name]
	oeeRecord = DBClient['basedata']
	
	while i<250087:
		print(i)
		##print(json_util.dumps(obj))

		#查询是否存在
		item=oeeRecord.find_one({'instrID':i})
		#if item is None:
		if True:
			result = getPostData(i)
			print(result)
			data=json_util.loads(result)
			rows=data['rows']
			for item in rows:
				dataObj={}
				for field in item:
					dataObj[field['name']]=field['value']
				# 存库
				print('save:')
				print(dataObj)
				result = DB.insertDB(dataObj)
				time.sleep(2)
		i=i+1

if __name__ == '__main__':
	main()
