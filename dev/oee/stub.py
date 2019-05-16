class STUB:
	def getStubData():
		List=[]
		i=0
		while i<24:
			List.append({'x':i,'y':0.03*i})
			i=i+1
		return List

	def getStandardTime():
		return 3000