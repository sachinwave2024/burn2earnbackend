from django.urls import include, path,re_path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
app_name = 'locations'

from . import views

loginurl='/Vl6A7bJZuN9UUox5/'

urlpatterns = [

	
	 
	 re_path(r'^insert_countries/$', views.insert_countries, name='insert_countries'),
	


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)