from os import name
from django.urls import re_path
# from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from . import views


from django.views.decorators.csrf import csrf_exempt


app_name = 'trade_auth'

loginurl = "RZqYkZRuiBaffkx"

urlpatterns = [





]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)