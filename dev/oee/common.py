from bson import json_util

class ResponseMsg:
	code = 0
	msg  = 'success'
	data = None

	def success(self,data):
		self.code=0
		self.msg='success'
		self.data=data
		return json_util.dumps(self)

	def failed(self,msg):
		self.code=-1
		self.msg=msg
		self.data=None
		return json_util.dumps(self)