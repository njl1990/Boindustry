from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('Createtask', views.Createtask, name='Createtask'),
	path('Tasklist', views.Tasklist, name='Tasklist'),


	# API
	path('loadCooperator', views.loadCooperator, name='loadCooperator'),
	path('loadTopic', views.loadTopic, name='loadTopic'),
	path('taskSubmit', views.taskSubmit, name='taskSubmit'),
	path('updateStatus', views.updateStatus, name='updateStatus'),
]