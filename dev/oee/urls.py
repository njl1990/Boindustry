from django.urls import path
from . import views

urlpatterns = [
    path('', views.OeeMachineList, name='OeeMachineList'),
	path('OeeInfo', views.OeeInfo, name='OeeInfo'),
	path('OeeReport', views.OeeReport, name='OeeReport'),
	path('OeeTransaction', views.OeeTransaction, name='OeeTransaction'),
	path('OeeConfig', views.OeeConfig, name='OeeConfig'),
	path('OeeMachineList', views.OeeMachineList, name='OeeMachineList'),


	# API
	## Load 
	path('LoadOee', views.LoadOee, name='LoadOee'),
	path('LoadProductionEfficiencyRate', views.LoadProductionEfficiencyRate, name='LoadProductionEfficiencyRate'),
	path('LoadTimeUtilizationRate', views.LoadTimeUtilizationRate, name='LoadTimeUtilizationRate'),
	path('LoadYieldRate', views.LoadYieldRate, name='LoadYieldRate'),
	path('LoadMachineInfo', views.LoadMachineInfo, name='LoadMachineInfo'),
	path('UpdateOeeConf', views.UpdateOeeConf, name='UpdateOeeConf'),
	path('DeleteOeeConf', views.DeleteOeeConf, name='DeleteOeeConf'),
	path('CreateOeeConf', views.CreateOeeConf, name='CreateOeeConf'),
	path('UpdateOeeTransaction', views.UpdateOeeTransaction, name='UpdateOeeTransaction'),
	
]