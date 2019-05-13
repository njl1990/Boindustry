from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from django.template import loader

from common import ResponseMsg
from bson.objectid import ObjectId
from bson import json_util


#PageLoad
def index(request):
	context = {'data': 'data'}
	return render(request, 'OeeInfo.html', ResponseMsg.success(contex))


def OeeInfo(request):
	context = {'data': 'data'}
	return render(request, 'OeeInfo.html', context)

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
	context = {'data': 'data'}
	return render(request, 'OeeMachineList.html', context)

# API
## Load
def LoadOee(request):
	# ID=request.POST['ID']
	data = "data"
	return HttpResponse(json_util.dumps(data))


def LoadProductionEfficiencyRate(request):
	# ID=request.POST['ID']
	data = "data"
	return HttpResponse(json_util.dumps(data))

def LoadTimeUtilizationRate(request):
	# ID=request.POST['ID']
	data = "data"
	return HttpResponse(json_util.dumps(data))


def LoadYieldRate(request):
	# ID=request.POST['ID']
	data = "data"
	return HttpResponse(json_util.dumps(data))