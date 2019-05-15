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
def index(request):
	context = {'data': 'data'}
	return render(request, 'OeeInfo.html',context)


def OeeInfo(request):
	context = None
	return render(request, 'OeeInfo.html', ResponseMsg.success(context))

def OeeReport(request):
	context = {'data': 'data'}
	return render(request, 'OeeReport.html', context)

def OeeTransaction(request):
	context = {'data': 'data'}
	return render(request, 'OeeTransaction.html', context)

def OeeConfig(request):
	context = {'data': 'data'}
	return render(request, 'OeeConfig.html', context)

def OeeMachineList(request):

	return render(request, 'OeeMachineList.html', context)

# API
## Load
def LoadOee(request):
	MachineID=request.POST['MachineID']
	# Load oee data from db	

	recordData = OeeServcie.LoadOeeData(MachineID,"OEE")
	xFeilds,yValues = OeeServcie.GetViewData(recordData)
	context = {
		'xFeilds': xFeilds,
		'yValues': yValues
		}
	result=ResponseMsg.success(context)
	print(result)
	return HttpResponse(json_util.dumps(result))


def LoadProductionEfficiencyRate(request):
	MachineID=request.POST['MachineID']
	# Load oee data from db	
	context = {
		'xFeilds': OeeChart.getXFields(),
		'yValues': OeeServcie.LoadOeeData(MachineID,"PER")	
		}
	result=ResponseMsg.success(context)
	print(result)
	return HttpResponse(json_util.dumps(result))

def LoadTimeUtilizationRate(request):
	MachineID=request.POST['MachineID']
	# Load oee data from db	
	context = {
		'xFeilds': OeeChart.getXFields(),
		'yValues': OeeServcie.LoadOeeData(MachineID,"TUR")	
		}
	result=ResponseMsg.success(context)
	print(result)
	return HttpResponse(json_util.dumps(result))


def LoadYieldRate(request):
	MachineID=request.POST['MachineID']
	# Load oee data from db	
	context = {
		'xFeilds': OeeChart.getXFields(),
		'yValues': OeeServcie.LoadOeeData(MachineID,"YR")	
		}
	result=ResponseMsg.success(context)
	print(result)
	return HttpResponse(json_util.dumps(result))
