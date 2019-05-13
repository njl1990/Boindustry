from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from django.template import loader
from ics.models import CTopic
from ics.models import Cooperator
from ics.models import CTask
from bson.objectid import ObjectId
from bson import json_util

# Create your views here.
def Createtask(request):
	# Get topiclist
	
	context = {
		# Selector items
		'CTopicSelectList': CTopic.CTopicSelectListByfilter({'CreatorID':ObjectId("5cbd7e1a0f2200064403b313")}),
		'CooperatorList':Cooperator.CooperatorSelectListByfilter({"Cooperation": ObjectId("5cbd7e1a0f2200064403b313")}),
		'result':'ok'
	}
	print(context)
	return render(request, 'createtask.html', context)


def Tasklist(request):
	# Get topiclist

	context = {
		'CTopicTaskList': CTask.CTaskListByfilter({'CreatorID':"5cbd7e1a0f2200064403b313"}),
		'result':'ok'
	}
	print(context)
	return render(request, 'tasklist.html', context)


def index(request):
	context = {'projectList': 'indexPageModelList'}
	return render(request, 'index.html', context)




# API:

def loadCooperator(request):
	ID=request.POST['ID']
	Item=Cooperator.CooperatorById(ID);
	if Item is not None:
		return HttpResponse(json_util.dumps(Item))
	else:
		return HttpResponse("None")

def loadTopic(request):
	ID=request.POST['ID']
	Item=CTopic.CTopicById(ID);
	if Item is not None:
		return HttpResponse(json_util.dumps(Item))
	else:
		return HttpResponse("None")

def taskSubmit(request):
	Task=request.POST['Task']
	result=CTask.CreateCTask(Task.replace('\"','\''));
	return HttpResponse("result")

def updateStatus(request):
	ID=request.POST['ID']
	result=CTask.UpdateStatus(ID);
	return HttpResponse(result)
