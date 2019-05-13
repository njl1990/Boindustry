from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from django.template import loader
from oee.common import ResponseMsg
from oee.chart import OeeChart
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
	context = {
		'xFeilds': OeeChart.getXFields(),
		'yValues': OeeServcie.LoadOeeData(MachineID,"OEE")	
		}
	return HttpResponse(ResponseMsg.success(context))


def LoadProductionEfficiencyRate(request):
	MachineID=request.POST['MachineID']
	# Load oee data from db	
	context = {
		'xFeilds': OeeChart.getXFields(),
		'yValues': OeeServcie.LoadOeeData(MachineID,"PER")	
		}
	return HttpResponse(ResponseMsg.success(context))

def LoadTimeUtilizationRate(request):
	MachineID=request.POST['MachineID']
	# Load oee data from db	
	context = {
		'xFeilds': OeeChart.getXFields(),
		'yValues': OeeServcie.LoadOeeData(MachineID,"TUR")	
		}
	return HttpResponse(ResponseMsg.success(context))


def LoadYieldRate(request):
	MachineID=request.POST['MachineID']
	# Load oee data from db	
	context = {
		'xFeilds': OeeChart.getXFields(),
		'yValues': OeeServcie.LoadOeeData(MachineID,"YR")	
		}
	return HttpResponse(ResponseMsg.success(context))