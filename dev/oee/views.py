from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from django.template import loader
from oee.common import ResponseMsg
from oee.chart import OeeChart
from oee.service import OeeServcie
from bson.objectid import ObjectId
from bson import json_util



#PageLoad
## Index
def index(request):
	MachineName='TLZH-01-08-3000416'
	return render(request, 'OeeInfo.html',context)

def OeeInfo(request):
	MachineName='TLZH-01-08-3000416'
	if request.GET.__contains__('MachineName'):
		MachineName=request.GET['MachineName']
		MachineInfo=OeeServcie.LoadMachineInfo(MachineName)
		MachineList=OeeServcie.LoadMachineList()
	context = {
					'MachineName':MachineName,
					'MachineInfo':MachineInfo,
					'MachineList':MachineList
				}
	##print(context)
	return render(request, 'OeeInfo.html', context)

def OeeReport(request):
	context = {'data': 'data'}
	return render(request, 'OeeReport.html', context)

def OeeTransaction(request):
	context = {'data': 'data'}
	return render(request, 'OeeTransaction.html', context)

def OeeConfig(request):
	context = {
		'WorkingTime': OeeServcie.LoadWorkingTime(),
		'StandardTimeList':OeeServcie.LoadStandardTimeList(),
	}
	print(context)
	return render(request, 'OeeConfig.html', context)

def OeeMachineList(request):
	context = {'MachineList': OeeServcie.LoadMachineList()}
	##print(context)
	return render(request, 'OeeMachineList.html', context)

# API
## Load
def LoadOee(request):
	MachineID=request.POST['MachineID']
	# Load oee data from db	
	context = {
		'xFeilds': OeeChart.getXFields(),
		'yValues': OeeServcie.GetViewData(OeeChart.getXFields(),OeeServcie.LoadOeeData(MachineID,"OEE"))
		}
	result=ResponseMsg.success(context)
	#print(result)
	return HttpResponse(json_util.dumps(result))

def LoadProductionEfficiencyRate(request):
	MachineID=request.POST['MachineID']
	# Load oee data from db	
	context = {
		'xFeilds': OeeChart.getXFields(),
		'yValues': OeeServcie.GetViewData(OeeChart.getXFields(),OeeServcie.LoadOeeData(MachineID,"PER"))
		}
	result=ResponseMsg.success(context)
	#print(result)
	return HttpResponse(json_util.dumps(result))

def LoadTimeUtilizationRate(request):
	MachineID=request.POST['MachineID']
	# Load oee data from db	
	context = {
		'xFeilds': OeeChart.getXFields(),
		'yValues': OeeServcie.GetViewData(OeeChart.getXFields(),OeeServcie.LoadOeeData(MachineID,"TUR"))
		}
	result=ResponseMsg.success(context)
	#print(result)
	return HttpResponse(json_util.dumps(result))

def LoadYieldRate(request):
	MachineID=request.POST['MachineID']
	# Load oee data from db	
	context = {
		'xFeilds': OeeChart.getXFields(),
		'yValues': OeeServcie.GetViewData(OeeChart.getXFields(),OeeServcie.LoadOeeData(MachineID,"YR"))
		}
	result=ResponseMsg.success(context)
	#print(result)
	return HttpResponse(json_util.dumps(result))

def LoadMachineInfo(request):
	MachineName=request.POST['MachineName']
	MachineInfo=OeeServcie.LoadMachineInfo(MachineName)
	context = {'MachineInfo':MachineInfo}
	##print(context)
	result=ResponseMsg.success(context)
	return HttpResponse(json_util.dumps(result))

def DeleteOeeConf(request):
	MachineName=request.POST['MachineName']
	MachineInfo=OeeServcie.LoadMachineInfo(MachineName)
	context = {'MachineInfo':MachineInfo}
	##print(context)
	result=ResponseMsg.success(context)
	return HttpResponse(json_util.dumps(result))

def UpdateOeeConf(request):
	MachineName=request.POST['MachineName']
	MachineInfo=OeeServcie.LoadMachineInfo(MachineName)
	context = {'MachineInfo':MachineInfo}
	##print(context)
	result=ResponseMsg.success(context)
	return HttpResponse(json_util.dumps(result))