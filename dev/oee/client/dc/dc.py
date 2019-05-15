
import json
import urllib.request
from bson import json_util

dataObj={"dbName": "atsData","tableName": "instrument","desc":True,"columnsToGet":["instrID","instruName","instruType","description","message","usedTime","testTime"],"limit":10,"exclusiveEndPrimaryKey":[{"name": "instrID", "type": "integer", "value": -1}]}
headersObj = {'tpye':'POST','Content-Type':'application/json;charset=utf-8','dataType':"json"}
request = urllib.request.Request(url="http://rest.gziiot.htdata.com:7777/api/data/GetRange?tid=14220&k=cAc6GJVf4DY21g5XR5LcHnkntWH8fkpv",headers=headersObj,data=json_util.dumps(dataObj).encode("utf-8"))
response = urllib.request.urlopen(request)
result = str(response.read())

with open('data.txt',"w") as f:
	f.write(result)
