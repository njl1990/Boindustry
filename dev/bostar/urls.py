from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('ics/', include('ics.urls')),
    path('admin/', admin.site.urls),
    path('oee/',include('oee.urls')),
]