
from django.shortcuts import render,redirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib import messages
import datetime

from trade_admin_auth.mixins import get_client_ip
from company.models import Company,Company_Settings

from django.http.response import HttpResponseRedirect
from django.http import HttpResponse,Http404

from trade_master.models import Cms_StaticContent,Faq,Roadmap,EmailTemplate,Currencylist
from trade_master.models import Blockip

from django.db.models import Q,F,Func,Value
from Crypto.Cipher import AES
import base64
import math
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.http.response import HttpResponseRedirect
from django.views import View

from django.http import JsonResponse

from django.views.generic import TemplateView

from django.shortcuts import get_list_or_404, get_object_or_404

from trade_currency.models import TradeCurrency

from django.core.mail import send_mail
from requests import get


from bs4 import BeautifulSoup
import csv

def get_hbdtoken(request):
  try:
    hbdtoken = TradeCurrency.objects.get(Q(symbol='HBD'))
  except TradeCurrency.DoesNotExist:
    hbdtoken = ''
  return hbdtoken

def maintenance(function):
    def wrap(request, *args, **kwargs):
        site = Company_Settings.objects.get(id=1)
        if site.site_maintenance_status == 1:
            return redirect("/mainimg/")
        else:
            return function(request, *args, **kwargs)
    return wrap

def block_by_ip(view_func):
    def authorize(request, *args, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            user_ip = x_forwarded_for.split(',')[0]
        else:
            user_ip = request.META.get('REMOTE_ADDR')
        allowedIps = Blockip.objects.filter(Q(status=0) & Q(ip_level="User"))
        for ip in allowedIps:
            if ip.ip_address == user_ip:
                return HttpResponseRedirect("/ipblock/")
        return view_func(request, *args, **kwargs)
    return authorize

def maintenance_img(request):
	return render(request,"default_theme/hbdtheme/maintenance.html")

def blockip(request):
    user_ip = get_client_ip(request)
    allowedIps = Blockip.objects.filter(Q(status=1) & Q(ip_level="User"))
    for ip in allowedIps:
        if ip.ip_address == user_ip:
            return HttpResponseRedirect("/")
    return render(request,"default_theme/hbdtheme/ipblock.html")

def foo(request):
	 return render_to_response("default_theme/base/sample.html")

def get_email_template(request,email_temp_id):
    email_template = EmailTemplate.objects.get(id = email_temp_id)
    if email_template:
        email_template_qs =email_template
    else:
        email_template_qs = ''
    return email_template_qs

def get_common_cipher():
    return AES.new(settings.COMMON_ENCRYPTION_KEY.encode("utf8"),AES.MODE_CBC,settings.COMMON_16_BYTE_IV_FOR_AES.encode("utf8"))

def decrypt_with_common_cipher(ciphertext):
    common_cipher = get_common_cipher()
    raw_ciphertext = base64.b64decode(ciphertext)
    decrypted_message_with_padding = common_cipher.decrypt(raw_ciphertext)
    return decrypted_message_with_padding.decode('utf-8').strip()


def encrypt_with_common_cipher(cleartext):
    common_cipher = get_common_cipher() 
    cleartext_length = len(cleartext)
    nearest_multiple_of_16 = 16 * math.ceil(cleartext_length/16)
    padded_cleartext = cleartext.rjust(nearest_multiple_of_16)
    raw_ciphertext = common_cipher.encrypt(padded_cleartext.encode("utf8"))
    return base64.b64encode(raw_ciphertext).decode('utf-8')



@maintenance
@block_by_ip
def home(request):
    context = {}
    context['Title'] = 'Home'
    context['activecls']='homeshow'
    return render(request,"default_theme/fronttheme/home.html",context)

@maintenance
@block_by_ip
def aboutus(request):
    context={}
    context['Title'] = 'Aboutus'
    context['activecls']='aboutusshow'
    return render(request,"default_theme/fronttheme/aboutuspage.html",context)


@maintenance
@block_by_ip
def howitworks(request):
    context={}
    context['Title'] = 'How it Works'
    context['activecls']='howitworkshow'
    return render(request,"default_theme/fronttheme/howitworks.html",context)

@maintenance
@block_by_ip
def faqshow(request):
    context={}
    context['Title'] = 'FAQ'
    context['activecls']='faqshow'
    return render(request,"default_theme/fronttheme/faqpage.html",context)
@maintenance
@block_by_ip
def terms(request):
    context={}
    context['Title'] = 'Terms'
    context['activecls']='termsshow'
    return render(request,"default_theme/fronttheme/__terms.html",context)


def error_404_view(request, exception):
    return render(request,'default_theme/fronttheme/404.html')


def read_gunicorn_access(request):
    f=open('/var/www/teslagreen/public_html/teslagreenenv/logs/gunicorn_supervisor.log', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content,content_type="text/plain")

def delete_read_gunicorn_delete(request):
    try:
        f = open('/var/www/teslagreen/public_html/teslagreenenv/logs/gunicorn_supervisor.log', 'r+')
        f.truncate()
        f.close()
    except Exception as e:
        pass
    return JsonResponse({'status':'access log cleared'})
