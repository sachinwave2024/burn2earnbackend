from django.urls import re_path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

app_name = 'trade_currency'

from .views import Add_tradecurrency, Listtradecurrency, Update_tradecurrency


loginurl='/RZqYkZRuiBaffkx/'

urlpatterns = [
	
	 re_path(r'^addcurrency/$', login_required(Add_tradecurrency.as_view(),login_url=loginurl), name='addcurrency'),	
	 re_path(r'^edit_currency/(?P<pk>[-\w]+)/$', login_required(Update_tradecurrency.as_view(),login_url=loginurl), name='edit_currency'),
	 re_path(r'^currencylist/$', login_required(Listtradecurrency.as_view(),login_url=loginurl), name='currencylist'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)