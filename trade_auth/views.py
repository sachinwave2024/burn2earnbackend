from django.shortcuts import render
from django.shortcuts import render, get_object_or_404


from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import View


from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect


import datetime


from decimal import *


from django.db import transaction

from django.contrib import auth
from django.contrib import messages



from trade_currency.models import TradeCurrency

def trade_log_out(request):
    user_id = request.user.id
    if user_id:
        tradeuser_activity_history(request,request.user.id,typelogin='Logout')
        auth.logout(request)
    else:
        auth.logout(request)
    return HttpResponseRedirect('/',)




