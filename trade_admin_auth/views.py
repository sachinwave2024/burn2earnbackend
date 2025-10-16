from multiprocessing import context
# from pickle import TRUE
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.views.generic import TemplateView,View

from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.template.context_processors import csrf
from django.shortcuts import redirect
from django.http import JsonResponse
from django.http import HttpResponse
from datetime import date,timedelta
import datetime
import string
import random

from django.db.models import Q
from django.db.models import Count,Sum


from django.db import transaction

from django.contrib import auth
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView

from API.views import Create_Google_Fitness, Create_User_cash_Wallet, Pin_Create, Registrationotp, generateOTP, referral__table

from Crypto.Cipher import AES
import base64
import math
from django.template.loader import get_template
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.http.response import HttpResponseRedirect

from django_tables2 import RequestConfig
from crispy_forms.layout import Submit,Reset
from API.models import Admin_Profit, Contract_address,company_bot,purchange_company_bot, Delete_Account_Management, Delete_Account_Reason_Management, Plan_purchase_wallet, Referral_code, Referral_reward, Referral_reward_History, Reward_History, UserCashWallet, Withdraw, Withdraw_history, admin_notification_message, admin_referral_code, market_price, plan, premium_wallet_deposit, premium_wallet_management, referral_level, referral_table, user_address_trust_wallet, wallet_flush_history, withdraw_values,User_2x_Boost,plan_purchase_history, Boat_wallet,boat_purchase_history,boat_trade_purchase_history,Roi_Reward_History,Boat_Referral_reward_History,boatroi_percentage,Boat_Referral_income_History,MPRewardHistory,MPPlanlist,MPDailyRewardHistory,BurnWithdraw,promobonus_history,BurnRewardHistory,swap_sendhistory,CBurnRewardHistory

from API.serializers import  User_device_see, User_see, User_stake_withdraw_see, User_withdraw_see, user_DeatailSerializers, user_ref_upline,UserDetailSerializer,User_BurnWithdraw_see

from trade_auth.models import Market_place

from django.utils.decorators import method_decorator
from trade_admin_auth.mixins import SubAdminRequiredMixin,CheckIpaddressAdminRequiredMixin
from trade_admin_auth.mixins import get_client_ip,get_browser_type,get_browser_os_type,get_browser_device_type,allow_by_ip,check_adminip,check_group,check_group_sub_menu,check_group_icon_menu
from trade_admin_auth.mixins import ManageUserAdminRequiredMixin,BlockIpaddressAdminRequiredMixin


from company.models import Company
from trade_admin_auth.models import AdminUser_Profile,AdminUser_Activity,AccessAttempt, Steps_Management, Steps_history, Two_x_boost, User_Management,PlanDateUpdateHistory, User_two_fa, WithdrawSendHistory, WithdrawSendUSDTHistory, front_page_management,WithdrawSendUSDTHistoryboat,MPPLanHistory,MPfeeHistory,BurntoearnHistory,CBurntoearnHistory

from trade_admin_auth.tables import Admin_Profit_Table, AdminActivityTable,DeactivateUserTable, Delete_Account_Reason_Management_Table, Delete_Account_Request_Management_Table, List_admin_notification_message_Table, List_front_page_management_Table, List_market_internal_Table, List_withdraw_Value_Table, Plan_Table, Referral_level_Table, Referral_reward_Table, Step_Management_Table, Steps_history_Table, Two_x_boost_Table, User_Management_Table, User_Referral_Table, Wallet_Table
from trade_admin_auth.tables import AdminActivityTableFilter,AdminActivitySearch_Form,UserManagementFilter,UserManagementSearch_Form,AdminProfitFilter,AdminProfitSearch_Form
from trade_admin_auth.tables import DashboardAdminActivityTable,BlockIPTable
from django.contrib.auth.forms import PasswordChangeForm

from trade_master.models import Blockip,EmailTemplate, LoginHistory,Faq,MenuModule,MenuPermission,IconMenuModule, Stake_Credit_History,SubMenuPermission,IconMenuPermission,SubMenuModule,Jw_plan_purchase_history, plan_purchase_history_edited
from Staking .models import  Stake_market_price, stake_wallet_management,stake_claim_reward_history,new_stake_deposit_management,new_stake_deposit_management,stake_purchase_history,newstake_Referral_reward_History,newstakeclaim_History

from trade_admin_auth.forms import Delete_aAccount_Reason_Form,EditCompanyMultiForm, List_Wallet_Form, Market_Internal_Form, Plan_Form, Referral_Level_Form, Referral_Reward_Form, Steps_Management_Form, Two_x_boost_Form, User_Management_Form, User_Referral_Level_Form, admin_notification_message_Form, front_page_management_Form, withdraw_values_Form
from trade_admin_auth.forms import AdminUserAddMultiForm
from trade_admin_auth.forms import AdminUserProfileeditform,ChangePatternForm,AdminUserEditSubadminMultiForm,SubAdminUserProfileeditform
from trade_admin_auth.forms import GoogleTokenVerificationForm,BlockipForm
from trade_admin_auth.forms import Passwordreset,SetPasswordForm
import requests
import pyotp
import json


from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_text
from django.utils.encoding import force_bytes, force_str

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

from decimal import Decimal
import os
import decimal
from django.contrib.auth import authenticate,logout
from trade_currency.models import TradeCurrency
from API.SeDGFHte import encrypted_format
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


import secrets

from rest_framework.authtoken.models import Token

from Staking.models import Stake_history_management,stake_deposit_management,internal_transfer_history,stake_claim_table

# def allow_by_ip(view_func):
#     def authorize(request, *args, **kwargs):
#         user_ip = get_client_ip(request)
#         allowedIps = Blockip.objects.filter(Q(status=0) & Q(ip_level="Admin"))
#         for ip in allowedIps:
#             if ip.ip_address == user_ip:
#                 return HttpResponseRedirect("/tradeadmin/adminblockip404/")
#         return view_func(request, *args, **kwargs)
#     return authorize

from django.http import HttpResponseRedirect

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def allow_by_ip(view_func):
    # Define the list of allowed IP prefixes
    allowed_ip_prefixes = [
        '77.111.244.',
        '127.0.0.1',
        # Add more prefixes as needed
    ]

    def authorize(request, *args, **kwargs):
        user_ip = get_client_ip(request)
        # print('user_ip', user_ip)
        # Check if the user_ip starts with any of the allowed prefixes
        if not any(user_ip.startswith(prefix) for prefix in allowed_ip_prefixes):
            return HttpResponseRedirect("/tradeadmin/adminblockip404/")
        return view_func(request, *args, **kwargs)

    return authorize


# def allow_by_ip(view_func):
#     # Define the list of allowed IP addresses
#     allowed_ips = [
#         '77.111.244.13',
#         '77.111.244.19',
#         '77.111.244.49',
#         '127.0.0.1',
#         # Add more IPs as needed
#     ]

#     def authorize(request, *args, **kwargs):
#         user_ip = get_client_ip(request)
#         print('user_ip',user_ip)
#         if user_ip not in allowed_ips:
#             return HttpResponseRedirect("/tradeadmin/adminblockip404/")
#         return view_func(request, *args, **kwargs)

#     return authorize


def Page403View(request):
	return render(request,'trade_admin_auth/403page.html',status=403)

def Page404View(request):
	return render(request,'trade_admin_auth/404page.html',status=404)

def Page500View(request):
	return render(request,'trade_admin_auth/500page.html',status=500)


def IPBlock404View(request):
  try:
    companyqs = Company.objects.get(id=1)
    companyname= companyqs.name
    companyipaddress = companyqs.company_settings.adminipaddress
  except Company.DoesNotExist:
    companyqs = 'HotBitDeal Auction'
    companyname = 'HotBitDeal Auction'
    companyipaddress = ''
  user_ip = get_client_ip(request)
  if companyipaddress is None or companyipaddress == '':
    return HttpResponseRedirect("/RZqYkZRuiBaffkx/")
  if companyipaddress == user_ip:
    return HttpResponseRedirect("/RZqYkZRuiBaffkx/")
  if companyipaddress is not None and companyipaddress != '':
    if companyipaddress != user_ip:
      pass
  return render(request,'trade_admin_auth/ipblock404.html',status=404)


def adminblockip404(request):
    user_ip = get_client_ip(request)
    allowedIps = Blockip.objects.filter(Q(status=1) & Q(ip_level="Admin"))
    for ip in allowedIps:
        if ip.ip_address == user_ip:
            return HttpResponseRedirect("/RZqYkZRuiBaffkx/")
    return render(request,"trade_admin_auth/ipblock.html")


def blockipadmin(request):
    attempt = check_attempts(request)
    if attempt == 2:
        return HttpResponseRedirect("/RZqYkZRuiBaffkx/")
    elif attempt == 1:
        return render(request,"trade_admin_auth/ipblock.html")


def check_attempts(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    attempt = AccessAttempt.objects.filter(ip_address=ip)
    access_count = len(attempt)
    a = ''
    if access_count >= 5 :
        a = 1
    else:
        a = 2
    return a


def get_email_template(request,email_temp_id):
    email_template = EmailTemplate.objects.get(id = email_temp_id)
    if email_template:
        email_template_qs =email_template
    else:
        email_template_qs = ''
    return email_template_qs



def get_common_cipher():
    return AES.new(settings.COMMON_ENCRYPTION_KEY,
                   AES.MODE_CBC,
                   settings.COMMON_16_BYTE_IV_FOR_AES)

def encrypt_with_common_cipher(cleartext):
    common_cipher = get_common_cipher() 
    cleartext_length = len(cleartext)
    nearest_multiple_of_16 = 16 * math.ceil(cleartext_length/16)
    padded_cleartext = cleartext.rjust(nearest_multiple_of_16)
    raw_ciphertext = common_cipher.encrypt(padded_cleartext.encode("utf8"))
    return base64.b64encode(raw_ciphertext).decode('utf-8')

def decrypt_with_common_cipher(ciphertext):
    common_cipher = get_common_cipher()
    raw_ciphertext = base64.urlsafe_b64decode(ciphertext)
    decrypted_message_with_padding = common_cipher.decrypt(raw_ciphertext)
    return decrypted_message_with_padding.decode('utf-8').strip()

@allow_by_ip
@check_adminip('checkadminip')
def adminloginn(request,id):
    context ={}
    context.update(csrf(request))
    attempt = check_attempts(request)
    if attempt == 1:
        return HttpResponseRedirect("/tradeadmin/ipblockadmin/")
    elif attempt == 2:
        key = decrypt_with_common_cipher(encrypted_format)
        totp = pyotp.TOTP(key)
        b=totp.now()
        if int(b) == id :
          return render(request, 'trade_admin_auth/login.html', context)
        
        
        else:
          return HttpResponseRedirect('/RZqYkZRuiBaffkx/')

@allow_by_ip
@check_adminip('checkadminip')
def adminlogin(request):
    context ={}
    context.update(csrf(request))
    attempt = check_attempts(request)
    if attempt == 1:
        return HttpResponseRedirect("/tradeadmin/ipblockadmin/")
    elif attempt == 2:
          return render(request, 'trade_admin_auth/login.html', context)
      







# from django.conf import settings
# from django.contrib import auth, messages
# from django.contrib.auth.models import User
# from django.core.mail import send_mail
# from django.http import HttpResponseRedirect
# import math
# import random

# # Helper function to send OTP email
# def send_otp_email(email, otp):
#     subject = 'Admin login OTP Code'
#     message = f'Admin login OTP code is {otp}.'
#     email_from = settings.DEFAULT_FROM_EMAIL  # Use the default email from settings
#     recipient_list = [email]
#     send_mail(subject, message, email_from, recipient_list)

# def generateOTP():
#     digits = "123456789"  # First digit should be between 1 and 9
#     first_digit = digits[math.floor(random.random() * 9)]
    
#     remaining_digits = "0123456789"
#     OTP = first_digit
#     for i in range(3):
#         OTP += remaining_digits[math.floor(random.random() * 10)]
    
#     return OTP

# @allow_by_ip
# def adminlogin_auth(request):
#     attempt = check_attempts(request)
#     if attempt == 1:
#         return HttpResponseRedirect("/tradeadmin/ipblockadmin/")
    
#     get_username_enc = request.POST.get('username', '')
#     get_username = encrypt_with_common_cipher(get_username_enc)
#     get_password = request.POST.get('password', '')
#     get_patterncode = request.POST.get('pattern_code', '')
#     get_otp = request.POST.get('otp', '')

#     try:
#         if '@' in get_username_enc:
#             try:
#                 userprofile = AdminUser_Profile.objects.get(emailaddress=get_username)
#                 if userprofile:
#                     useremail = userprofile.user.username
#                     username = User.objects.get(username=useremail).username
#                 else:
#                     username = ''
#             except AdminUser_Profile.DoesNotExist:
#                 userprofile = ''
#                 username = ''
#         else:
#             username = ''

#         user = auth.authenticate(request=request, username=username, password=get_password)
#     except User.DoesNotExist:
#         user = None

#     if user is not None:
#         user_id = user.id
#         get_userprofile = AdminUser_Profile.objects.get(user_id=user_id)
#         user_pattern = get_userprofile.pattern_code
#     else:
#         user_pattern = ''

#     if user is not None:
#         if user_pattern is not None and user_pattern == int(get_patterncode):
#             if user.is_active:
#                 userid = user.id
#                 userprofile = AdminUser_Profile.objects.get(user=userid)
#                 userprofile2fa = userprofile.twofa

#                 if 'otp_sent' not in request.session or request.session['otp_sent'] != userid:
#                     # Generate and send OTP
#                     otp = generateOTP()
#                     send_otp_email(userprofile.emailaddress, otp)
#                     request.session['otp'] = otp
#                     request.session['otp_sent'] = userid
#                     messages.add_message(request, messages.SUCCESS, 'OTP sent to your email. Please check your inbox.')
#                     return HttpResponseRedirect('/tradeadmin/otp_verify/')

#                 if get_otp and int(get_otp) == request.session.get('otp'):
#                     del request.session['otp']
#                     del request.session['otp_sent']

#                     if not userprofile2fa:
#                         auth.login(request, user)
#                         next_URL = '/tradeadmin/dashboard/'
#                         admin_activity_history(request, user.id, typelogin='Login')
#                         messages.add_message(request, messages.SUCCESS, 'Successfully Logged In!')
#                         return HttpResponseRedirect(next_URL)
#                     else:
#                         next_URL = f'/tradeadmin/twofaadmin/{userid}/'
#                         return HttpResponseRedirect(next_URL)
#                 else:
#                     messages.add_message(request, messages.ERROR, 'Invalid OTP')
#                     return HttpResponseRedirect('/tradeadmin/otp_verify/')
#             else:
#                 return handle_failed_login(request, get_username_enc)
#         else:
#             return handle_failed_login(request, get_username_enc)
#     else:
#         return handle_failed_login(request, get_username_enc)

# def handle_failed_login(request, username_enc):
#     ip = get_client_ip(request)
#     if AccessAttempt.objects.filter(ip_address=ip).count() >= 5:
#         return HttpResponseRedirect("/tradeadmin/ipblockadmin/")
#     else:
#         tradeadmin_attempt_history(request, username_enc, typelogin='Invalid Admin Login')
#         messages.add_message(request, messages.ERROR, 'Login Details are invalid')
#         key = decrypt_with_common_cipher(encrypted_format)
#         totp = pyotp.TOTP(key)
#         return HttpResponseRedirect(f'/RZqYkZRuiBaffkx/{totp.now()}/')

# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip


@allow_by_ip
def adminlogin_auth(request):
    attempt = check_attempts(request)
    if attempt == 1:
        return HttpResponseRedirect("/tradeadmin/ipblockadmin/")
    elif attempt == 2:
        get_username_enc = request.POST.get('username', '')
        get_username = encrypt_with_common_cipher(get_username_enc)
        get_password = request.POST.get('password', '')
        get_patterncode = request.POST.get('pattern_code', '')
        try:
            if '@' in get_username_enc:
              try:
                userprofile= AdminUser_Profile.objects.get(emailaddress =get_username)
                if userprofile:
                  useremail = userprofile.user.username
                  username = User.objects.get(username=useremail).username
                  
                else:
                  username =''
              except AdminUser_Profile.DoesNotExist:
                userprofile =''
                username =''
            else:
                username = ''
            user = auth.authenticate(request=request,username=username,
                                     password=get_password)

        except User.DoesNotExist:
            user = None
        if user is not None:
            user_id = user.id
            get_userprofile = AdminUser_Profile.objects.get(user_id=user_id)
            user_pattern = get_userprofile.pattern_code
        else:
            user_pattern = ''
            
        if user is not None:
          
            if user_pattern is not None and user_pattern == int(get_patterncode):
                if user is not None and user.is_active:
                    userid = user.id
                    userprofile = AdminUser_Profile.objects.get(user = userid)
                    userprofile2fa = userprofile.twofa
                    if userprofile2fa == False:
                      auth.login(request, user)
                      next_URL = '/tradeadmin/dashboard/'
                      
                      admin_activity_history(request, user.id,
                            typelogin='Login')
                      messages.add_message(request, messages.SUCCESS, 'Successfully Logged In!')
                      return HttpResponseRedirect(next_URL)
                    elif userprofile2fa == True:
                      next_URL= '/tradeadmin/twofaadmin/'+str(userid)+'/'
                      return HttpResponseRedirect(next_URL)
                    
                else:
                    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                    if x_forwarded_for:
                        ip = x_forwarded_for.split(',')[0]
                    else:
                        ip = request.META.get('REMOTE_ADDR')
                    attempt = AccessAttempt.objects.filter(ip_address=ip)
                    access_count = len(attempt)
                    if access_count >= 5 :
                        return HttpResponseRedirect("/tradeadmin/ipblockadmin/")
                    else:
                        tradeadmin_attempt_history(request,get_username_enc ,typelogin='Invalid Admin Login')
                        messages.add_message(request, messages.ERROR, 'Login Details are invalid')
                        key = decrypt_with_common_cipher(encrypted_format)
                        totp = pyotp.TOTP(key)
                        b=str(totp.now())
                        return HttpResponseRedirect('/RZqYkZRuiBaffkx/'+b+'/')
            else:
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                attempt = AccessAttempt.objects.filter(ip_address=ip)
                access_count = len(attempt)
                if access_count >= 5 :
                    return HttpResponseRedirect("/tradeadmin/ipblockadmin/")
                else:
                    tradeadmin_attempt_history(request,get_username_enc ,typelogin='Invalid Admin Login')
                    messages.add_message(request, messages.ERROR, 'Login Details are invalid')
                    key = decrypt_with_common_cipher(encrypted_format)
                    totp = pyotp.TOTP(key)
                    b=str(totp.now())
                    return HttpResponseRedirect('/RZqYkZRuiBaffkx/'+b+'/')
        else:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            attempt = AccessAttempt.objects.filter(ip_address=ip)
            access_count = len(attempt)
            if access_count >= 5 :
                return HttpResponseRedirect("/tradeadmin/ipblockadmin/")
            else:
                tradeadmin_attempt_history(request,get_username_enc ,typelogin='Invalid Admin Login')
                messages.add_message(request, messages.ERROR, 'Login Details are invalid')
                key = decrypt_with_common_cipher(encrypted_format)
                totp = pyotp.TOTP(key)
                b=str(totp.now())
                return HttpResponseRedirect('/RZqYkZRuiBaffkx/'+b+'/')


def tradeadmin_attempt_history(request,get_email,typelogin):
    try:
        get_user = User.objects.get(email=get_email)
        if get_user:
            create_admin_login = AccessAttempt.objects.create(
                user = get_user,
                emailaddress = get_email,
                ip_address=get_client_ip(request),
                activity=typelogin,
                browsername=get_browser_type(request),
                os=get_browser_os_type(request),
                devices=get_browser_device_type(request),
                datetime=datetime.datetime.now(),
                failedcount = 1
              )  
    except:
        create_admin_login = AccessAttempt.objects.create(
            emailaddress = get_email,
            ip_address=get_client_ip(request),
            activity=typelogin,
            browsername=get_browser_type(request),
            os=get_browser_os_type(request),
            devices=get_browser_device_type(request),
            datetime=datetime.datetime.now(),
            failedcount = 1
          )
    return  True

from datetime import datetime
def admintwofa(request,uid):
    context={}
    context = {
    'Title':'Two Factor Authenticator',
    'keywords':'Enable Google Authenticator,QR Code',
    'content':'Enable Google Authenticator  for additional security for user.',
    }
    if request.method == 'POST':
        form = GoogleTokenVerificationForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(pk=uid)
                user_id = user.id
                get_userprofile = AdminUser_Profile.objects.get(user = user_id)
            except User.DoesNotExist:
                user = None
                get_userprofile = None
            if user is not None and get_userprofile is not None:
                secertkey = get_userprofile.google_id
                authtoken = pyotp.TOTP(secertkey)
                verification = authtoken.now()
                token = request.POST['token']
                if token == verification:
                    auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')
                    admin_activity_history(request,user_id,typelogin='Login')
                    messages.add_message(request, messages.SUCCESS, 'two factor authentication login successfully.')
                    return HttpResponseRedirect('/tradeadmin/dashboard/')
                else:
                    messages.add_message(request, messages.ERROR,'Invalid 2FA Code')
                    return HttpResponseRedirect('/tradeadmin/twofaadmin/'+str(user_id)+'/')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid user!')
                return HttpResponseRedirect('/tradeadmin/twofaadmin/'+str(user_id)+'/')
    else:
        form = GoogleTokenVerificationForm()
    return render(request, 'trade_admin_auth/twofalogin.html', {'form': form})



def log_out(request):
    admin_activity_history(request,request.user.id,typelogin='Logout')
    auth.logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logout Successfull!')
    key = decrypt_with_common_cipher(encrypted_format)
    totp = pyotp.TOTP(key)
    b=str(totp.now())
    return HttpResponseRedirect('/RZqYkZRuiBaffkx/'+b+'/')

def user_date_charts(request):
    today = datetime.datetime.today()
    long_ago = today + timedelta(days=-7)
    d=date.today()-timedelta(days=6)
    adminactivity_list = []
    json_result=''
    adminactivity = AdminUser_Activity.objects.filter(Q(activity='Login') & Q(user__admin_user_profile__role=2) & Q(created_on__gte=d)).extra({'date_created':"date(modified_on)"}).values('date_created').order_by('modified_on__date').annotate(tot_deposit_amt=Count('id'))
    
    if adminactivity:
      for adminitem in adminactivity:
        adminday = adminitem['date_created']
        admindayname = adminday.strftime("%a")
        adminactivity_sub_list =[]
        admincount= int(adminitem['tot_deposit_amt'])
        adminactivity_sub_list.append(admindayname)
        adminactivity_sub_list.append(admincount)
        adminactivity_list.append(adminactivity_sub_list)
      json_result = adminactivity_list
    else:
      json_result ='0'  
    return json_result

import datetime
def admin_activity_history(request,user_id,typelogin):
    get_user = User.objects.get(id=user_id)
    if get_user:
          create_admin_login = AdminUser_Activity.objects.create(
            user_id=user_id,
            ip_address=get_client_ip(request),
            activity=typelogin,
            browsername=get_browser_type(request),
            os=get_browser_os_type(request),
            devices=get_browser_device_type(request),
            created_on=datetime.now(),
            created_by_id = get_user.id,
            modified_by_id = get_user.id

          )   

    return  True

import datetime
# @allow_by_ip
@check_adminip('checkadminip')
def dashboard(request):
    attempt = check_attempts(request)
    if attempt == 1:
        return HttpResponseRedirect("/tradeadmin/ipblockadmin/")
    elif attempt == 2:
        context={}
        context['Title'] = 'Dashboard'
        adminactivity_qs = AdminUser_Activity.objects.filter(user__admin_user_profile__role=0).order_by('-id')[:10]
        context['adminactivity_qs'] =adminactivity_qs
        Adminactivitytable = DashboardAdminActivityTable(adminactivity_qs)
        context['table'] = Adminactivitytable
        context['dashboardshow'] = 'Yes'
        cms_count = User_Management.objects.filter(~Q(plan = 0)).count()
        context['cms_count'] =cms_count
        faq_count = Faq.objects.filter(status=0)
        context['faq_count'] = len(faq_count)
        user_count=User_Management.objects.all().count()
        context['user_count']=user_count
        auction_count=User_Management.objects.filter(status = 0).count()
        context['auction_count']=auction_count
        bids_count=User_Management.objects.filter(status = 1).count()
        context['bids_count']=bids_count
        winner_count=User_Management.objects.filter(status = 2).count()
        context['wiiners_count']=winner_count
        support_count=1
        context['support_count']=support_count
        
        today = datetime.today()
        yesterday = today - timedelta(days = 1)
        checkfromdate = yesterday.strftime('%Y-%m-%d')

        plan_exp_users_count = User_Management.objects.filter(plan_end_date__gte = today).count()
        context['plan_exp_users_count'] = plan_exp_users_count
        
        steps_total_user_count = Steps_history.objects.filter(created_on__date = checkfromdate).count()
        context['steps_total_user_count'] = steps_total_user_count
        steps_active_total_user_count = Steps_history.objects.filter(steps__lte = 3000).filter(created_on__date = checkfromdate).count()
        context['steps_active_total_user_count'] = steps_active_total_user_count
        steps_inactive_total_user_count = Steps_history.objects.filter(steps__gte = 3000).filter(created_on__date = checkfromdate).count()
        context['steps_inactive_total_user_count'] = steps_inactive_total_user_count
        steps_less_reward_total_user_count = Steps_history.objects.filter(Q(status = 0) & Q(steps__gte = 3000)).filter(created_on__date = checkfromdate).count()
        context['steps_less_reward_total_user_count'] = steps_less_reward_total_user_count
        steps_greater_reward_total_user_count = Steps_history.objects.filter(Q(status = 1) & Q(steps__gte = 3000)).filter(created_on__date = checkfromdate).count()
        context['steps_greater_reward_total_user_count'] = steps_greater_reward_total_user_count
        company_qs = Company.objects.get(id=1)
        android_current_version_users_count = company_qs.Android_version
        context['android_current_version_users_count'] = android_current_version_users_count
        ios_current_version_users_count = company_qs.IOS_version
        context['ios_current_version_users_count'] = ios_current_version_users_count
        android_users_count = User_Management.objects.filter(Q(phone_number = company_qs.Android_version) & Q(user_profile_pic = 'Android')).filter(status = 0).count()
        context['android_users_count'] = android_users_count
        ios_users_count = User_Management.objects.filter(Q(phone_number = company_qs.IOS_version) & Q(user_profile_pic = 'IOS')).filter(status = 0).count()
        context['ios_users_count'] = ios_users_count


        # Staking count
        stake_user_count = Stake_history_management.objects.using('second_db').filter(status = 0).count()
        context['stake_user_count'] = stake_user_count

        stake_deposit_user_count = stake_deposit_management.objects.using('second_db').filter(status = 1).count()
        context["stake_deposit_user_count"] = stake_deposit_user_count

        internal_transfer_user_count = internal_transfer_history.objects.using('second_db').filter(status = 0).count()
        context["internal_transfer_user_count"] = internal_transfer_user_count

        claimed_user_count = stake_claim_table.objects.using('second_db').filter(status = 1).count()
        context['claimed_user_count'] = claimed_user_count



        return render(request,"trade_admin_auth/dashboard.html",context)


def randomString(stringLength=16):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def adminforgotpassword(request):
  attempt = check_attempts(request)
  if attempt == 1:
    return HttpResponseRedirect("/tradeadmin/ipblockadmin/")
  elif attempt == 2:
    context ={}
    if  request.method == 'POST':
        form = Passwordreset(request.POST)
        if form.is_valid():
          get_email = request.POST.get('email','')
          try:
            companyqs = Company.objects.get(id=1)
            copyright= companyqs.copy_right
            comp_logo = companyqs.company_logo
          except:
            companyqs = ''
            copyright = ''
            comp_logo=''
          try:
            get_user = User.objects.get(Q(email = get_email) & Q(is_superuser=True))
            checkemail = get_user.email
            checkuser_id = get_user
          except:
            get_user = None
            checkemail = None
            checkuser_id = None
          if checkemail is not None:

            emailtemplate = get_email_template(request,1)
            text_file = open("trade_master/templates/emailtemplate/forgot_mail.html", "w")
            text_file.write(emailtemplate.content)
            text_file.close()           
            email_subject = emailtemplate.Subject
            to_email = checkemail
            
            data= {
              'username':checkuser_id,
              'company_logo':comp_logo,
              'copyright':copyright,
              'domain':get_current_site(request),
              'uid':urlsafe_base64_encode(force_bytes(get_user.pk)),
              'token':default_token_generator.make_token(get_user),
              'protocol': 'http',
              }
            text_content = 'This is an important message.'
            htmly = get_template('emailtemplate/forgot_mail.html')
            html_content = htmly.render(data)
            requests.post(
                "https://api.mailgun.net/v3/jasanwellness.fit/messages",
                auth=("api",  decrypt_with_common_cipher(settings.MAIL_API)),
                data={"from": "WEB3 WELLNESS <noreply@jasanwellness.fit>",
                "to": [to_email],
                "subject": emailtemplate.Subject,
                "text": "Testing some Mailgun awesomness!",
                "html": html_content})
            messages.add_message(request, messages.SUCCESS, 'Your Password Link sent to  your EmailId.')
            key = decrypt_with_common_cipher(encrypted_format)
            totp = pyotp.TOTP(key)
            b=str(totp.now())
            return HttpResponseRedirect('/RZqYkZRuiBaffkx/'+b+'/')
          else:
            messages.add_message(request, messages.ERROR, 'Invalid EmailID')  
            return HttpResponseRedirect(reverse('trade_admin_auth:adminforgotpassword'))
        else:
          messages.add_message(request,messages.INFO,'Error Occured.')
    else:
        form = Passwordreset()
    return render(request,"trade_admin_auth/adminforgot.html",context)    


def Admin_passwordresetconfirm(request, uidb64, token):
    username = request.user.username
    if username != None and username !='':
      return HttpResponseRedirect('/tradeadmin/dashboard/')
    else:
      if request.method == 'POST':
          form = SetPasswordForm(request.POST)
          if form.is_valid():
            UserModel = get_user_model()
            assert uidb64 is not None and token is not None
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = UserModel._default_manager.get(pk=uid)
            except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
                user = None
            if user is not None and default_token_generator.check_token(user, token):
                try:
                    new_password = form.cleaned_data['new_password2']
                    user.set_password(new_password)
                    user.is_active =True
                    user.save()
                    get_userprofile = AdminUser_Profile.objects.get(user = user.id)
                    get_userprofile.status = 1
                    get_userprofile.save()
                    messages.add_message(request,messages.SUCCESS,'Your Password Reset Successfully Now You Login ')
                    key = decrypt_with_common_cipher(encrypted_format)
                    totp = pyotp.TOTP(key)
                    b=str(totp.now())
                    return HttpResponseRedirect('/RZqYkZRuiBaffkx/'+b+'/')
                except KeyError:
                    messages.add_message(messages.ERROR,'Two Password Fields Did not match')
            else:
                messages.add_message(request, messages.ERROR, 'Reset link already used !!')
                key = decrypt_with_common_cipher(encrypted_format)
                totp = pyotp.TOTP(key)
                b=str(totp.now())
                return HttpResponseRedirect('/RZqYkZRuiBaffkx/'+b+'/')
          else:
              messages.add_message(request,messages.ERROR,form.errors)
              key = decrypt_with_common_cipher(encrypted_format)
              totp = pyotp.TOTP(key)
              b=str(totp.now())
              return HttpResponseRedirect('/RZqYkZRuiBaffkx/'+b+'/')
      else:
          form = SetPasswordForm()
          UserModel = get_user_model()
          assert uidb64 is not None and token is not None
          try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = UserModel._default_manager.get(pk=uid)
          except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
          if user is not None and default_token_generator.check_token(user, token):
            pass
          else:
            messages.add_message(request, messages.ERROR, 'Reset link already used !!')
            key = decrypt_with_common_cipher(encrypted_format)
            totp = pyotp.TOTP(key)
            b=str(totp.now())
            return HttpResponseRedirect('/RZqYkZRuiBaffkx/'+b+'/')
    return render(request,"trade_admin_auth/adminpasswordconfirm.html",{'form':form})

# @allow_by_ip
def adminforgotpattern(request):
  context ={}
  if  request.method == 'POST':
    get_email = request.POST.get('email','')
    try:
      companyqs = Company.objects.get(id=1)
      copyright= companyqs.copy_right
      comp_logo = companyqs.company_logo
    except:
      companyqs = ''
      copyright = ''
      comp_logo=''
    try:
      get_user = User.objects.get(Q(email = get_email) & Q(is_superuser=True))
      checkemail = get_user.email
      checkuser_id = get_user
    except:
      get_user = None
      checkemail = None
      checkuser_id = None
    if checkemail is not None:
      profile = AdminUser_Profile.objects.get(user=get_user)
      profile.pattern_status = 0
      profile.save()
      emailtemplate = get_email_template(request,2)
      text_file = open("trade_master/templates/emailtemplate/forgotpattern_mail.html", "w")
      text_file.write(emailtemplate.content)
      text_file.close()           
      email_subject = emailtemplate.Subject
      to_email = checkemail
      
      data= {
        'username':checkuser_id,
        'company_logo':comp_logo,
        'copyright':copyright,
        'domain':get_current_site(request),
        'protocol':'http',
        'userid':get_user.id,
        'uid':urlsafe_base64_encode(force_bytes(get_user.pk)),
        'token':default_token_generator.make_token(get_user),
        }
      text_content = 'This is an important message.'
      htmly = get_template('emailtemplate/forgotpattern_mail.html')
      html_content = htmly.render(data)
      requests.post(
                "https://api.mailgun.net/v3/jasanwellness.fit/messages",
                auth=("api",  decrypt_with_common_cipher(settings.MAIL_API)),
                data={"from": "WEB3 WELLNESS <noreply@jasanwellness.fit>",
                "to": [to_email],
                "subject": emailtemplate.Subject,
                "text": "Testing some Mailgun awesomness!",
                "html": html_content})
      messages.add_message(request, messages.SUCCESS, 'Pattern Reset Link Send To Your Email')
      key = decrypt_with_common_cipher(encrypted_format)
      totp = pyotp.TOTP(key)
      b=str(totp.now())
      return HttpResponseRedirect('/RZqYkZRuiBaffkx/'+b+'/')
    else:
      messages.add_message(request, messages.ERROR, 'Invalid EmailID')  
      return HttpResponseRedirect(reverse('trade_admin_auth:adminforgotpattern'))
  else:
    return render(request,"trade_admin_auth/adminforgotpattern.html",context)    

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()


def Adminpatternupdate(request, uidb64, token):
  username = request.user.username
  if username != None and username !='':
    return HttpResponseRedirect('/tradeadmin/dashboard/')
  else:
    if request.method == 'POST':
        UserModel = get_user_model()
        assert uidb64 is not None and token is not None
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        profile = AdminUser_Profile.objects.get(user=user)
        patternstatus = profile.pattern_status
        if user is not None and patternstatus == 0:
            patrn_upt = AdminUser_Profile.objects.get(user=user)
            ptn_id=user.id
            get_pattern_code = int(request.POST['pattern_code'])
            get_confirmpattern = int(request.POST['confirmpattern_code'])
            patterncode = get_pattern_code
            confirmpattern = get_confirmpattern
            if patterncode == confirmpattern:
              update_patterncode = AdminUser_Profile.objects.get(id = patrn_upt.id)
              update_patterncode.pattern_code = patterncode
              update_patterncode.pattern_status = 1
              update_patterncode.save()
              messages.add_message(request,messages.SUCCESS,'Pattern Updated Success')
              key = decrypt_with_common_cipher(encrypted_format)
              totp = pyotp.TOTP(key)
              b=str(totp.now())
              return HttpResponseRedirect('/RZqYkZRuiBaffkx/'+b+'/')
            else:
              messages.add_message(request, messages.ERROR, 'Confirm pattern is mismatch')
        else:
            messages.add_message(request, messages.ERROR, 'Reset link already used !!')
            next_URL = '/RZqYkZRuiBaffkx/'
            return HttpResponseRedirect(next_URL)
    else:
        UserModel = get_user_model()
        assert uidb64 is not None and token is not None
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        profile = AdminUser_Profile.objects.get(user=user)
        patternstatus = profile.pattern_status
        if user is not None and patternstatus == 0:
            pass
        else:
            messages.add_message(request, messages.ERROR, 'Reset link already used !!')
            key = decrypt_with_common_cipher(encrypted_format)
            totp = pyotp.TOTP(key)
            b=str(totp.now())
            return HttpResponseRedirect('/RZqYkZRuiBaffkx/'+b+'/')
  return render(request,'trade_admin_auth/forgotpatternconfirm.html')


import stat

class EditCompanySetting(CheckIpaddressAdminRequiredMixin,UpdateView):
    permission_required = ('trade_perms.Trade_Admin')
    
    model=Company
    form_class = EditCompanyMultiForm
    template_name = 'trade_admin_auth/settings.html'

    def get_context_data(self, **kwargs):
       context = super(EditCompanySetting, self).get_context_data(**kwargs)
       try:
         obj_withdraw_status = Steps_Management.objects.get(id = 1)
       except:
         obj_withdraw_status = ""

       context['obj_withdraw_status'] = obj_withdraw_status
       context['Title']='General Settings'
       context["market"] = Company.objects.get(id = 1)
       return context
    def get_form_kwargs(self):
      
          kwargs = super(EditCompanySetting, self).get_form_kwargs()
          kwargs.update(instance={
              'form1': self.object,
              'form2': self.object.company_settings,
          })
          dict_obj = {'site_maintenance_status' : self.object.company_settings.site_maintenance_status , 'IOS_site_maintenance_status' : self.object.company_settings.IOS_site_maintenance_status}
          with open("maintanance_status.json", "w") as outfile:
            os.chmod("maintanance_status.json", stat.S_IWRITE)
            json.dump(dict_obj, outfile)
            
          return kwargs
        

    def get_success_url(self, **kwargs):
        p_key = int(self.kwargs['pk'])
        messages.add_message(self.request, messages.SUCCESS, 'Setting Updated Successfully.')
        return '{}'.format(reverse('trade_admin_auth:general_settings', kwargs={'pk': p_key}))
      

# @allow_by_ip
@check_adminip('checkadminip')
def editprofilesetting(request,user_id):
    attempt = check_attempts(request)
    if attempt == 1:
        return HttpResponseRedirect("/tradeadmin/ipblockadmin/")
    elif attempt == 2:
        context={}
        user= User.objects.get(id=user_id)
        usermail = user.email
        userprofile= AdminUser_Profile.objects.get(user=user.id)
        user_profile_id = userprofile.id
        user_decrypt_emailaddress =userprofile.emailaddress  
        decrypt_user_emailaddress=decrypt_with_common_cipher(user_decrypt_emailaddress)
        phoneno = userprofile.phone1
        profilepic = userprofile.photo
        if request.method == 'POST':
           profile_form = AdminUserProfileeditform(request.POST,request.FILES,instance=userprofile)
           getemail = request.POST['email']
           val = request.POST['backval']
           if int(val) == 0:
             messages.add_message(request, messages.ERROR, "Enter Correct Image Format")
             return HttpResponseRedirect('/tradeadmin/profile_settings/'+str(user_id)+'/')
           if getemail and User.objects.filter(Q(email=getemail) & Q(is_superuser=False)).count() > 0:
               messages.add_message(request, messages.ERROR, "This Email Address Already Registered")
               return HttpResponseRedirect('/tradeadmin/profile_settings/'+str(user_id)+'/')
           else:
               if profile_form.is_valid():
                 getusername = request.POST['username']
                 userupdateform = User.objects.filter(id=user_id).update(email = getemail , username = getusername)
                 get_emailaddress = getemail
                 profile_form.instance.created_by_id = request.user.id
                 profile_form.instance.modified_by_id = request.user.id
                 profile_form.save()
                 if get_emailaddress != "":
                    encrypt_useremail=encrypt_with_common_cipher(get_emailaddress)
                    update_emailaddress = AdminUser_Profile.objects.get(id = user_profile_id)
                    update_emailaddress.emailaddress = encrypt_useremail
                    update_emailaddress.save()
                   
                 else:
                    messages.add_message(request, messages.ERROR, 'Email address must required.')
                    return HttpResponseRedirect('/tradeadmin/profile_settings/'+str(user_id)+'/')
                 messages.add_message(request, messages.SUCCESS, 'Admin Profile updated Successfully.')
                 return HttpResponseRedirect('/tradeadmin/profile_settings/'+str(user_id)+'/')
               else:
                messages.add_message(request, messages.ERROR, user_form.errors)
                return HttpResponseRedirect('/tradeadmin/profile_settings/'+str(user_id)+'/')
        else:
            context={
                'Title':'Profile Setting',
                'decrypt_user_emailaddress':decrypt_user_emailaddress,
                'phoneno':phoneno,
                'profilepic':profilepic,
                'usermail':usermail
              }
        return render(request,'trade_admin_auth/profile.html', context)

class ChangePasswordView(PasswordChangeView):
  
    template_name = 'trade_admin_auth/changepassword.html'
    form_class = PasswordChangeForm
   
    def get_context_data(self, **kwargs):
       context = super(ChangePasswordView, self).get_context_data(**kwargs)
       context['Title']='Change Password'
       return context
   
    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, 'Change password updated Successfully.')
        return '{}'.format(reverse('trade_admin_auth:change_password'))

class ChangePatternView(UpdateView):
    model= AdminUser_Profile
    template_name = 'trade_admin_auth/changepattern.html'
    form_class = ChangePatternForm
   
    def get_context_data(self, **kwargs):
       context = super(ChangePatternView, self).get_context_data(**kwargs)
       context['Title']='Change Pattern'
       return context
    @transaction.atomic
    def form_valid(self, form):
        formsave=form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Change pattern updated Successfully.')
        return HttpResponseRedirect(reverse('trade_admin_auth:patternchange',kwargs={'pk': formsave.id}))
    

def change_pattern_view(request,user_id):
    context={}
    user= User.objects.get(id=user_id)
    user_profile_id = user.admin_user_profile.id
    user_profile_pattern = user.admin_user_profile.pattern_code
  
    if request.method == 'POST':
       pattern_code = int(request.POST['pattern_code'])
       oldpattern = int(request.POST['old_pattern_code'])
       confirmpattern = int(request.POST['confirmpattern_code'])

       if oldpattern != "" and oldpattern == user_profile_pattern:
        if oldpattern !="" and confirmpattern != "" and pattern_code != "":
          if pattern_code == confirmpattern:
      
           if pattern_code != "":
              update_patterncode = AdminUser_Profile.objects.get(id = user_profile_id)
              update_patterncode.pattern_code = pattern_code
              update_patterncode.save()
              messages.add_message(request, messages.SUCCESS, 'Change pattern updated Successfully.')
           else:
              messages.add_message(request, messages.ERROR, 'New pattern must required.')
              return HttpResponseRedirect('/tradeadmin/patternchange/'+str(user_id)+'/')
         
          else:
            messages.add_message(request, messages.ERROR, 'Confirm pattern is mismatch')
            return HttpResponseRedirect('/tradeadmin/patternchange/'+str(user_id)+'/')
        else:
          messages.add_message(request, messages.ERROR, 'Pattern Code must required')
          return HttpResponseRedirect('/tradeadmin/patternchange/'+str(user_id)+'/')
       else:
        messages.add_message(request, messages.ERROR, 'Old pattern is mismatch')
        return HttpResponseRedirect('/tradeadmin/patternchange/'+str(user_id)+'/')
       
       return HttpResponseRedirect('/tradeadmin/patternchange/'+str(user_id)+'/')
    else:
          
        
        context={
            'Title':'Change Pattern',
            'patterncode':user_profile_pattern,
           }
        
    return render(request,'trade_admin_auth/changepattern.html', context)

def admintwofaupdate(request):
    form = GoogleTokenVerificationForm()
    if request.method == 'POST':
        form = GoogleTokenVerificationForm(request.POST)
        if form.is_valid():
            token = request.POST['token']
            secertkey = request.POST['secertkey']
            authtoken = pyotp.TOTP(secertkey)
            verification = authtoken.now()
            msg=''
            if token == verification:
                uid =request.user.id
                try:
                    user = User.objects.get(pk=uid)
                    user_id = user.id
                    get_userprofile = AdminUser_Profile.objects.get(user = user_id)

                except User.DoesNotExist:
                    user = None
                    get_userprofile = None
                if user is not None and get_userprofile is not None:
                    if get_userprofile.twofa == False:
                        get_userprofile.twofa = True
                        get_userprofile.google_id = secertkey
                        get_userprofile.save()
                        msg='two factor authentication enabled successfully.'
                    elif get_userprofile.twofa == True:
                        get_userprofile.twofa = False
                        get_userprofile.google_id = '' 
                        get_userprofile.save()
                        msg='two factor authentication disabled successfully.'

                    messages.add_message(request, messages.SUCCESS, msg)
                    return HttpResponseRedirect('/tradeadmin/admin2fa/')
                else:
                   messages.add_message(request, messages.ERROR, 'Already status updated.')
                   return HttpResponseRedirect('/tradeadmin/admin2fa/')
            else:
                messages.add_message(request, messages.ERROR,'Invalid 2FA Code')
                return HttpResponseRedirect('/tradeadmin/admin2fa/')
        else:
           messages.add_message(request, messages.ERROR,form.errors)
           return HttpResponseRedirect('/tradeadmin/admin2fa/') 
    else:
        try:
          get_userprofile = AdminUser_Profile.objects.get(user = request.user.id)
        except AdminUser_Profile.DoesNotExist:
         get_userprofile  = ''
        secertkey =''
        if get_userprofile.google_id != None and get_userprofile.google_id !='':
          secertkey = get_userprofile.google_id
        else:
          secertkey = pyotp.random_base32()

        pytop =pyotp.totp.TOTP(secertkey).provisioning_uri(name=request.user.email, issuer_name='Jasan Wellness Admin 2FA')
        verification = pyotp.TOTP(secertkey)
        authtoken = verification.now()
        usertwofastatus = get_userprofile.twofa
        usersecertkey = ''
        if usertwofastatus == True:
          usersecertkey = get_userprofile.google_id
        else:
          usersecertkey = secertkey

        context ={
          'Title':'Two Factor Authentication',
          'userpytop':pytop,
          'secertkey':usersecertkey,
          'get_userprofile':get_userprofile,
          'form5':GoogleTokenVerificationForm()

        }
    return render(request,'trade_admin_auth/enable2fa.html', context)


class ListAdminactivity(SubAdminRequiredMixin,ListView):
    model = AdminUser_Activity
    template_name = 'trade_admin_auth/subadmin_activity_list.html'
    def get_queryset(self, **kwargs):
      return AdminUser_Activity.objects.filter(Q(user__admin_user_profile__role=1) | Q(user__admin_user_profile__role=0)).order_by('-id')
    def get_context_data(self,**kwargs):
        context=super(ListAdminactivity, self).get_context_data(**kwargs)
        context['Title'] = 'Admin Login History'
        tradeuser_qs = AdminUser_Activity.objects.filter(Q(user__admin_user_profile__role=1) | Q(user__admin_user_profile__role=0)).order_by('-id')
        filter = AdminActivityTableFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        filter.form.helper = AdminActivitySearch_Form()
        filter.form.helper.add_input(Submit('submit', 'Search',css_class="btn btn-default"))
        filter.form.helper.add_input(Reset('Reset Search','Reset Search',css_class="btn btn-default",css_id='reset-search'))
        contenttable = AdminActivityTable(filter.qs)
        context['tradeuser_qs'] =tradeuser_qs
        context['table'] = contenttable
        RequestConfig(self.request, paginate={'per_page': 15}).configure(contenttable)
        context['filter'] = filter
        context['Reset_url'] = 'trade_admin_auth:subadminactivity'
        context['activecls']='subdetailadmin'
        
        return context


class ListSubAdmin(ListView):
    model = User
    template_name = 'trade_admin_auth/sub_admin_list.html'
    def get_queryset(self, **kwargs):
      return User.objects.filter(admin_user_profile__role=1)
    
    def get_context_data(self,**kwargs):
        context=super(ListSubAdmin, self).get_context_data(**kwargs)
        context['Title'] = 'Sub Admin List'
        subadmin_qs = User.objects.filter(admin_user_profile__role=1)
        context['subadmin_qs'] =subadmin_qs
        context['activecls']='subdetailadmin'
        return context

    @method_decorator(check_group("Manage Sub Admin"))
    def dispatch(self, *args, **kwargs):
      return super(ListSubAdmin, self).dispatch(*args, **kwargs)



class CreateSubadminUser(CreateView):
    form_class = AdminUserAddMultiForm
    template_name = 'trade_admin_auth/subadmin_add_form.html'
    raise_exception  = True
    def get_context_data(self, **kwargs):
       context = super(CreateSubadminUser, self).get_context_data(**kwargs)
       user_id = self.request.user.id
       menuqs = MenuModule.objects.filter(status = 0)
       context['Title'] = 'Create SubAdmin'
       context['Btn_url']='trade_admin_auth:subadminlist'
       context['activecls']='subdetailadmin'
       context['menuqs']=menuqs
       context['menu_qs_count'] = menuqs.count()
       return context
    
    @method_decorator(check_group("Manage Sub Admin"))
    def dispatch(self, *args, **kwargs):
      return super(CreateSubadminUser, self).dispatch(*args, **kwargs)
    
    @transaction.atomic
    def form_valid(self, form):
        form1 = form['form1']
        form2 = form['form2']
        get_email = form2.cleaned_data["emailaddress"]
        form1.instance.email = get_email
        form1.instance.is_staff = 1
        form1.instance.is_superuser = 1
        user_form = form1.save()
        
        encypt_email=encrypt_with_common_cipher(get_email)
        user_id=user_form.id
        group = Group.objects.get(name='Sub Admin')
        user_form.groups.add(group)
        
        
        form2.instance.user = user_form
        form2.instance.role=1
        form2.instance.emailaddress=encypt_email
        form2.instance.status=1
        form2.save()
        menu_perm_val = self.request.POST.get('menu_perm_list')
        obj_val = json.loads(menu_perm_val)
        list_val = []
        for item in obj_val.values():
          for i in item:
            list_val.append(int(i))
        
        menu_qs = MenuModule.objects.all()
        for j in menu_qs:
          if j.id in list_val:
            create_menu_permissions(self.request,user_id,j.id,0)
          else:
            create_menu_permissions(self.request,user_id,j.id,1)
        messages.add_message(self.request, messages.SUCCESS, 'Subadmin  created Successfully.')
        return HttpResponseRedirect('/tradeadmin/subadmin_sub_menu_add/'+str(user_id)+'/')
    
import datetime
@check_group("Manage Sub Admin")
def CreateSubAdmin_SubMenu_User(request,id):
  context = {}
  context["Title"] = "Create Sub Menu Permission"
  user_obj = User.objects.get(id = id)
  user_obj_perm_id = MenuPermission.objects.filter(user_permissions_id = user_obj.id).filter(access_status = 0)
  menu_list = []
  for item in user_obj_perm_id:
    obj_sub_menu = SubMenuModule.objects.filter(main_module_name_id = item.access_modules.id)
    for item1 in obj_sub_menu:
      menu_list.append(str(item1.sub_module_name))
  context["obj_sub_menu"] = menu_list
  context["menu_qs_count"] = len(menu_list)

  if request.method == "POST":
    menu_perm_val = request.POST.get('menu_perm_list')
    obj_val = json.loads(menu_perm_val)
    list_val = []
    for item in obj_val.values():
      for i in item:
        list_val.append(str(i))
    menu_qs_sub = SubMenuModule.objects.all()
    
    for j in menu_qs_sub:
      
      if j.sub_module_name in list_val:
        menu_sub_obj = SubMenuModule.objects.get(sub_module_name = j.sub_module_name)
        menu_qs = MenuModule.objects.get(id = menu_sub_obj.main_module_name.id)
        menu_perm_qs = MenuPermission.objects.get(access_modules_id= menu_qs.id,user_permissions = user_obj.id)
        # for menu in menu_perm_qs:
        SubMenuPermission.objects.create(
          user_permissions_id=user_obj.id,
          main_access_modules_id = menu_perm_qs.id,
          sub_menu_name = menu_sub_obj,
          access_permissions=0,
          access_status = 0,
          created_on=datetime.now(),
          created_by_id = request.user.id,
          modified_by_id = request.user.id
        )  
      else:
        # for menu in menu_perm_qs:
        menu_sub_obj = SubMenuModule.objects.get(sub_module_name = j.sub_module_name)
        menu_qs = MenuModule.objects.get(id = menu_sub_obj.main_module_name.id)
        menu_perm_qs = MenuPermission.objects.get(access_modules_id= menu_qs.id,user_permissions = user_obj.id)
        SubMenuPermission.objects.create(
          user_permissions_id=user_obj.id,
          main_access_modules_id = menu_perm_qs.id,
          sub_menu_name = menu_sub_obj,
          access_permissions=0,
          access_status = 1,
          created_on=datetime.now(),
          created_by_id = request.user.id,
          modified_by_id = request.user.id
        ) 
    messages.add_message(request, messages.SUCCESS, 'Sub Menu access given Successfully.')
    return HttpResponseRedirect('/tradeadmin/subadmin_iconmenu_add/'+str(user_obj.id)+'/')
  return render(request,'trade_admin_auth/subadmin_submenu_add_form.html', context)


@check_group("Manage Sub Admin")
def Subadmin_SubMenu_EditPermission(request,user_id):
  context = {}
  user= User.objects.get(id=user_id)
  menuqs = SubMenuPermission.objects.filter(user_permissions_id = user.id)
  context['Title'] = 'Sub Menu Permissions'
  context['menuqs']=menuqs
  context["user"] = user
  context['menu_qs_count'] = menuqs.count()
  if request.method =="POST":
    menu_perm_val = request.POST.get('menu_perm_list')
    obj_val = json.loads(menu_perm_val)
    list_val = []
    for item in obj_val.values():
      for i in item:
        list_val.append(int(i))
    menu_qs = SubMenuPermission.objects.filter(user_permissions_id = user.id)
    for j in menu_qs:
      if j.id in list_val:
        SubMenuPermission.objects.filter(id = j.id).update(access_status = 0)  
      else:
        SubMenuPermission.objects.filter(id = j.id).update(access_status = 1) 
    messages.add_message(request, messages.SUCCESS, 'Sub Menu Permission updated Successfully.')
    return HttpResponseRedirect('/tradeadmin/subadmin_submenu_edit_permission/'+str(user.id)+'/')
    
  return render(request,'trade_admin_auth/subadmin_submenu_edit_permission.html', context)

import datetime

@check_group("Manage Sub Admin")
def CreateSubAdmin_IconMenu_User(request,id):
  context = {}
  context["Title"] = "Create Icon Menu Permission"
  user_obj = User.objects.get(id = id)
  user_obj_perm_id = SubMenuPermission.objects.filter(user_permissions_id = user_obj.id).filter(access_status = 0)
  menu_list = []
  for item in user_obj_perm_id:
    obj_icon_menu = IconMenuModule.objects.filter(sub_module_name_id = item.sub_menu_name.id)
    for item1 in obj_icon_menu:
      menu_list.append(str(item1.icon_module_name))
  context["obj_icon_menu"] = menu_list
  context["menu_qs_count"] = len(menu_list)

  if request.method == "POST":
    menu_perm_val = request.POST.get('menu_perm_list')
    obj_val = json.loads(menu_perm_val)
    list_val = []
    for item in obj_val.values():
      for i in item:
        list_val.append(str(i))
    menu_qs_sub = IconMenuModule.objects.all()
    
    for j in menu_qs_sub:
      
      if j.icon_module_name in list_val:
        menu_icon_obj = IconMenuModule.objects.get(icon_module_name = j.icon_module_name)
        menu_sub_obj = SubMenuModule.objects.get(id = menu_icon_obj.sub_module_name.id)
        menu_perm_qs = SubMenuPermission.objects.get(sub_menu_name_id= menu_sub_obj.id,user_permissions = user_obj.id)
        # for icon in menu_perm_qs:
        IconMenuPermission.objects.create(
          user_permissions_id=user_obj.id,
          submenu_access_modules_id = menu_perm_qs.id,
          icon_menu_name = menu_icon_obj,
          access_permissions=0,
          access_status = 0,
          created_on=datetime.now(),
          created_by_id = request.user.id,
          modified_by_id = request.user.id
        )  
      else:
        # IconMenuPermission.objects.filter(user_permissions_id = user_obj.id).filter(main_access_modules__access_modules_id = menu_qs.id).update(icon_menu_name = menu_qs_sub.id)
        
        menu_icon_obj = IconMenuModule.objects.get(icon_module_name = j.icon_module_name)
        
        menu_sub_obj = SubMenuModule.objects.get(id = menu_icon_obj.sub_module_name.id)
        menu_perm_qs = SubMenuPermission.objects.get(sub_menu_name = menu_sub_obj.id,user_permissions = user_obj.id)
        # for icon in menu_perm_qs:
        IconMenuPermission.objects.create(
          user_permissions_id=user_obj.id,
          submenu_access_modules_id = menu_perm_qs.id,
          icon_menu_name = menu_icon_obj,
          access_permissions=0,
          access_status = 1,
          created_on=datetime.now(),
          created_by_id = request.user.id,
          modified_by_id = request.user.id
        ) 
    messages.add_message(request, messages.SUCCESS, 'Icon Menu access given Successfully.')
    return HttpResponseRedirect('/tradeadmin/subadminlist/')
  return render(request,'trade_admin_auth/subadmin_iconmenu_add.html', context)


@check_group("Manage Sub Admin")
def Subadmin_IconMenu_EditPermission(request,user_id):
  context = {}
  user= User.objects.get(id=user_id)
  menuqs = IconMenuPermission.objects.filter(user_permissions_id = user.id)
  context['Title'] = 'Icon Menu Permissions'
  context['menuqs']=menuqs
  context["user"] = user
  context['menu_qs_count'] = menuqs.count()
  if request.method =="POST":
    menu_perm_val = request.POST.get('menu_perm_list')
    obj_val = json.loads(menu_perm_val)
    list_val = []
    for item in obj_val.values():
      for i in item:
        list_val.append(int(i))
    menu_qs = IconMenuPermission.objects.filter(user_permissions_id = user.id)
    for j in menu_qs:
      if j.id in list_val:
        IconMenuPermission.objects.filter(id = j.id).update(access_status = 0)  
      else:
        IconMenuPermission.objects.filter(id = j.id).update(access_status = 1) 
    messages.add_message(request, messages.SUCCESS, 'Icon Menu Permission updated Successfully.')
    return HttpResponseRedirect('/tradeadmin/subadmin_iconmenu_edit_permission/'+str(user.id)+'/')
    
  return render(request,'trade_admin_auth/subadmin_iconmenu_edit_permission.html', context)

@check_group("Manage Sub Admin")
def edit_subadmin_profilesetting(request,user_id):
    context={}
    user= User.objects.get(id=user_id)
    usermail = user.email
    userprofile= AdminUser_Profile.objects.get(user=user.id)
    user_profile_id = userprofile.id
    user_decrypt_emailaddress =userprofile.emailaddress  
    decrypt_user_emailaddress=decrypt_with_common_cipher(user_decrypt_emailaddress)
    if request.method == 'POST':
        profile_form = SubAdminUserProfileeditform(request.POST,instance=userprofile)
        getemail = request.POST['email']
        if getemail and User.objects.filter(Q(email=getemail) & Q(is_superuser=False)).count() > 0:
            messages.add_message(request, messages.ERROR, "This Email Address Already Registered")
            return HttpResponseRedirect('/tradeadmin/sub_admin_profile_settings/'+str(user_id)+'/')
        else:
            if profile_form.is_valid():
              
              getusername = request.POST['username']
              userupdateform = User.objects.filter(id=user_id).update(email = getemail , username = getusername)
              get_emailaddress = getemail
              profile_form.instance.created_by_id = request.user.id
              profile_form.instance.modified_by_id = request.user.id
              profile_form.save()
              if get_emailaddress != "":
                encrypt_useremail=encrypt_with_common_cipher(get_emailaddress)
                update_emailaddress = AdminUser_Profile.objects.get(id = user_profile_id)
                update_emailaddress.emailaddress = encrypt_useremail
                update_emailaddress.save()
                
              else:
                messages.add_message(request, messages.ERROR, 'Email address must required.')
                return HttpResponseRedirect('/tradeadmin/sub_admin_profile_settings/'+str(user_id)+'/')
              messages.add_message(request, messages.SUCCESS, 'Sub Admin Profile updated Successfully.')
              return HttpResponseRedirect('/tradeadmin/sub_admin_profile_settings/'+str(user_id)+'/')
            else:
              messages.add_message(request, messages.ERROR, "gfhd")
              return HttpResponseRedirect('/tradeadmin/sub_admin_profile_settings/'+str(user_id)+'/')
    else:
        context={
            'Title':'Profile Setting',
            'decrypt_user_emailaddress':decrypt_user_emailaddress,
            'usermail':usermail,
            'user' : user
          }
    return render(request,'trade_admin_auth/subadmin_edit_profile.html', context)


@check_group("Manage Sub Admin")
def SubAdminChangePasswordView(request,user_id):
    context={}
    user = User.objects.get(id = user_id)
    if request.method == "POST":
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            auth.update_session_auth_hash(request, form)
            messages.add_message(request, messages.SUCCESS, 'Change password updated Successfully.')
            return HttpResponseRedirect('/tradeadmin/subadmin_change_password/'+str(user_id)+'/')
        else:
            messages.add_message(request, messages.ERROR, 'Password Does Not Match.')
            return HttpResponseRedirect('/tradeadmin/subadmin_change_password/'+str(user_id)+'/')
    else:
        form = SetPasswordForm(user)
    context['user'] = user
    context['Title']= 'Change Password'
    return render(request,'trade_admin_auth/subadmin_changepassword.html',context)


@check_group("Manage Sub Admin")
def sub_adminchange_pattern_view(request,user_id):
    context={}
    
    user= User.objects.get(id=user_id)
    user_profile_id = user.admin_user_profile.id
    user_profile_pattern = user.admin_user_profile.pattern_code
    if request.method == 'POST':
       pattern_code = int(request.POST['pattern_code'])
       oldpattern = int(request.POST['old_pattern_code'])
       confirmpattern = int(request.POST['confirmpattern_code'])
       if oldpattern != "" and oldpattern == user_profile_pattern:
        if oldpattern !="" and confirmpattern != "" and pattern_code != "":
          if pattern_code == confirmpattern:
           if pattern_code != "": 
              update_patterncode = AdminUser_Profile.objects.get(id = user_profile_id)
              update_patterncode.pattern_code = pattern_code
              update_patterncode.save()
              messages.add_message(request, messages.SUCCESS, 'Change pattern updated Successfully.')
           else:
              messages.add_message(request, messages.ERROR, 'New pattern must required.')
              return HttpResponseRedirect('/tradeadmin/subadmin_patternchange/'+str(user_id)+'/')
         
          else:
            messages.add_message(request, messages.ERROR, 'Confirm pattern is mismatch')
            return HttpResponseRedirect('/tradeadmin/subadmin_patternchange/'+str(user_id)+'/')
        else:
          messages.add_message(request, messages.ERROR, 'Pattern Code must required')
          return HttpResponseRedirect('/tradeadmin/subadmin_patternchange/'+str(user_id)+'/')
       else:
        messages.add_message(request, messages.ERROR, 'Old pattern is mismatch')
        return HttpResponseRedirect('/tradeadmin/subadmin_patternchange/'+str(user_id)+'/')
       
       return HttpResponseRedirect('/tradeadmin/subadmin_patternchange/'+str(user_id)+'/')
    else:
          
        
        context={
            'Title':'Change Pattern',
            'patterncode':user_profile_pattern,
            'user' : user
           }
        
    return render(request,'trade_admin_auth/subadmin_changepattern.html', context)


@check_group("Manage Sub Admin")
def SubadminEditPermission(request,user_id):
  context = {}
  user= User.objects.get(id=user_id)
  menuqs = MenuPermission.objects.filter(user_permissions_id = user.id)
  context['Title'] = 'Menu Permissions'
  context['menuqs']=menuqs
  context["user"] = user
  context['menu_qs_count'] = menuqs.count()
  if request.method =="POST":
    menu_perm_val = request.POST.get('menu_perm_list')
    obj_val = json.loads(menu_perm_val)
    list_val = []
    for item in obj_val.values():
      for i in item:
        if i is not None:
          list_val.append(int(i))
    menu_qs = MenuPermission.objects.filter(user_permissions_id = user.id)
    for j in menu_qs:
      if j.id in list_val:
        MenuPermission.objects.filter(id = j.id).update(access_status = 0)  
      else:
        MenuPermission.objects.filter(id = j.id).update(access_status = 1) 
    messages.add_message(request, messages.SUCCESS, 'Permission  updated Successfully.')
    return HttpResponseRedirect('/tradeadmin/subadmin_edit_permission/'+str(user.id)+'/')
    
  return render(request,'trade_admin_auth/subadmin_permissions.html', context)
 


def create_menu_permissions(request,user_id,list_val,access_status):
    menu_perm_val = list_val
    create_menu = MenuPermission.objects.create(
      user_permissions_id=user_id,
      access_modules_id=menu_perm_val,
      access_permissions=0,
      access_status = access_status,
      created_on=datetime.now(),
      created_by_id = request.user.id,
      modified_by_id = request.user.id

    )   

    return  True

def SubAdmin_FormView(request,user_id):
    context={}
    user= User.objects.get(id=user_id)
    menu_permission_qs = MenuPermission.objects.filter(user_permissions = user_id)
    if request.method == 'POST':
       messages.add_message(request, messages.SUCCESS, 'Assign permissions successfully updated.')
       return HttpResponseRedirect('/tradeadmin/subadminlist/')
    else:
        context={
            'Title':'Assign Permissions',
            'menu_permission_qs':menu_permission_qs,
            'activecls':'subdetailadmin'
           }
        
    return render(request,'trade_admin_auth/subadmin_permissions.html', context)



class DeleteSubAdmin(SubAdminRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        pkey =  (self.kwargs['pk'])
        
        user_qs = get_object_or_404(User, pk=pkey)
        if user_qs.is_active == False:
            user_qs.is_active = True
            status = 'activated'
        elif user_qs.is_active == True:    
            user_qs.is_active = False
            status = 'deactivated'
        user_qs.save()
        
        messages.add_message(request, messages.SUCCESS, 'SubAdmin '+status+' status updated successfully.') 
        return HttpResponseRedirect(reverse('trade_admin_auth:subadminlist'))

           

class DeleteTwoFAAdmin(ManageUserAdminRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        pkey =  (self.kwargs['pk'])
        user_qs = get_object_or_404(User, pk=pkey)
        get_userprofile = AdminUser_Profile.objects.get(user = user_qs.id)
        if get_userprofile.twofa == True:
          get_userprofile.twofa = False
          get_userprofile.save()
        
        messages.add_message(request, messages.SUCCESS, 'User twofa  status updated successfully.') 
        return HttpResponseRedirect(reverse('trade_admin_auth:twofalist'))



class ListTradeUserAdmin(ManageUserAdminRequiredMixin,ListView):
    model = User
    template_name = 'trade_admin_auth/manage_user_list.html'
    def get_queryset(self, **kwargs):
      return User.objects.filter(Q(admin_user_profile__role=2) & Q(is_active=True)).order_by('-id')
    def get_context_data(self,**kwargs):
        context=super(ListTradeUserAdmin, self).get_context_data(**kwargs)
        context['Title'] = 'User List'
        tradeuser_qs = User.objects.filter(Q(admin_user_profile__role=2) & Q(is_active=True)).order_by('-id')
        context['tradeuser_qs'] =tradeuser_qs
        contenttable = TradeUserTable(tradeuser_qs)
        context['table'] = contenttable
        context['Reset_url'] = 'trade_admin_auth:tradeuserlist'
        context['activecls']='userdetailadmin'
        return context




class ListTradeDeactiveUserAdmin(BlockIpaddressAdminRequiredMixin,ListView):
    model = User
    template_name = 'trade_admin_auth/deactivateuser_list.html'
    def get_queryset(self, **kwargs):
      return User.objects.filter(Q(admin_user_profile__role=2) & Q(is_active=False) & (Q(admin_user_profile__status=2) | Q(admin_user_profile__status=0))).order_by('-id')
    
    def get_context_data(self,**kwargs):
        context=super(ListTradeDeactiveUserAdmin, self).get_context_data(**kwargs)
        context['Title'] = 'Deactivate User List'
        tradeuser_qs = User.objects.filter(Q(admin_user_profile__role=2) & Q(is_active=False) & (Q(admin_user_profile__status=2) | Q(admin_user_profile__status=0))).order_by('-id')
        context['subadmin_qs'] =tradeuser_qs
        deativateuser=DeactivateUserTable(tradeuser_qs)
        context['table'] = deativateuser
        context['activecls']='userdetailadmin'
        return context


class ListTwoFAUserAdmin(BlockIpaddressAdminRequiredMixin,ListView):
    model = User
    template_name = 'trade_admin_auth/2fauserlist.html'
    def get_queryset(self, **kwargs):
      return User.objects.filter(Q(admin_user_profile__role=2)).order_by('-id')
    
    def get_context_data(self,**kwargs):
        context=super(ListTwoFAUserAdmin, self).get_context_data(**kwargs)
        context['Title'] = 'TwoFA User List'
        tradeuser_qs = User.objects.filter(Q(admin_user_profile__role=2)).order_by('-id')
        context['subadmin_qs'] =tradeuser_qs
        deativateuser=DeactivateUserTable(tradeuser_qs)
        context['table'] = deativateuser
        context['activecls']='userdetailadmin'
        return context


class DeleteTradeuserAdmin(BlockIpaddressAdminRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        pkey =  (self.kwargs['pk'])
        user_qs = get_object_or_404(User, pk=pkey)
        user_id = user_qs.id
        get_userprofile = AdminUser_Profile.objects.get(user = user_id)
        if user_qs.is_active == False:
            user_qs.is_active = True
            get_userprofile.status = 1
            get_userprofile.save()
            status = 'activated'
            messages.add_message(request, messages.SUCCESS, 'User Activate status updated successfully.') 
        elif user_qs.is_active == True:    
            user_qs.is_active = False
            get_userprofile.status = 2
            get_userprofile.save()
            messages.add_message(request, messages.ERROR, 'User Deactivate status updated successfully.')
            status = 'deactivated'
        user_qs.save()
        
        
        return HttpResponseRedirect(reverse('trade_admin_auth:tradeuserlist'))


class DetailTradeUser(BlockIpaddressAdminRequiredMixin,DetailView):
    model = User 
    template_name = 'trade_admin_auth/user_profile.html'
    def get_context_data(self, **kwargs):
       context = super(DetailTradeUser, self).get_context_data(**kwargs)
       p_key = int(self.kwargs['pk'])
       user_qs = User.objects.get(id=p_key)
       context['Title'] = 'User Info'
       context['user_qs']=user_qs
       context['activecls']='userdetailadmin'

       return context

class ListUseractivity(BlockIpaddressAdminRequiredMixin,ListView):
    model = AdminUser_Activity
    template_name = 'trade_admin_auth/tradeuseractivitylist.html'
    def get_queryset(self, **kwargs):
      return AdminUser_Activity.objects.filter(user__admin_user_profile__role=2).order_by('-id')
    def get_context_data(self,**kwargs):
        context=super(ListUseractivity, self).get_context_data(**kwargs)
        context['Title'] = 'User Login History'
        tradeuser_qs = AdminUser_Activity.objects.filter(user__admin_user_profile__role=2).order_by('-id')
        context['tradeuser_qs'] =tradeuser_qs
        contenttable = AdminActivityTable(tradeuser_qs)        
        context['table'] = contenttable
        RequestConfig(self.request, paginate={'per_page': 15}).configure(contenttable)
        context['Reset_url'] = 'trade_admin_auth:activityuserlist'
        context['activecls']='userdetailadmin'
        
        return context 



class ListBlockIp(BlockIpaddressAdminRequiredMixin,ListView):
    model = Blockip
    template_name = 'trade_master/generic_list_add.html'
    def get_queryset(self, **kwargs):
      return Blockip.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(ListBlockIp, self).get_context_data(**kwargs)
        context['Title'] = 'Block IPAddress'
        adminactivity_qs = Blockip.objects.all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        Adminactivitytable = BlockIPTable(adminactivity_qs)
        context['table'] = Adminactivitytable
        context['add_title'] ='Add BlockIp'
        context['Btn_url'] = 'trade_admin_auth:addblockip'
        return context


class AddBlockIp(BlockIpaddressAdminRequiredMixin,CreateView):
    model = Blockip
    form_class = BlockipForm
    template_name = 'trade_admin_auth/addblockip.html'   
    def get_context_data(self, **kwargs):
       context = super(AddBlockIp, self).get_context_data(**kwargs)
       context['Title'] = 'Add Blockip'
       context['Btn_url'] = 'trade_admin_auth:blockiplist'
       return context

    @transaction.atomic
    def form_valid(self, form):
        
       form.instance.created_on   = datetime.datetime.now()
       form.instance.created_by_id = self.request.user.id
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()
       
       messages.add_message(self.request, messages.SUCCESS, 'Blockip created successfully.')
       return HttpResponseRedirect('/tradeadmin/blockiplist/')


class EditBlockIp(BlockIpaddressAdminRequiredMixin,UpdateView):
    model = Blockip
    form_class = BlockipForm
    template_name = 'trade_admin_auth/editblockip.html'   
    def get_context_data(self, **kwargs):
       context = super(EditBlockIp, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       context['Title'] = 'Edit BlockIP'
       context['Btn_url'] = 'trade_admin_auth:blockiplist'
       return context

    @transaction.atomic
    def form_valid(self, form):
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Blockip updated successfully.')
       return HttpResponseRedirect('/tradeadmin/blockiplist/')



class ListAttemptIPBlock(BlockIpaddressAdminRequiredMixin,ListView):
    model = AccessAttempt
    template_name = 'trade_admin_auth/attemptlist.html'
    def get_queryset(self, **kwargs):
      return AccessAttempt.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(ListAttemptIPBlock, self).get_context_data(**kwargs)
        context['Title'] = 'Admin Login Attempt'
        attempt_qs = AccessAttempt.objects.all().order_by('-id')
        context['attempt_qs'] =attempt_qs
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        context['ip'] = ip
        return context

    @method_decorator(check_group("Admin Login Attempt"))
    def dispatch(self, *args, **kwargs):
      return super(ListAttemptIPBlock, self).dispatch(*args, **kwargs)

class DeleteAttemptIPBlock(BlockIpaddressAdminRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        pkey =  (self.kwargs['pk'])
        
        user_qs = get_object_or_404(AccessAttempt, pk=pkey)
        user_qs.delete()
        messages.add_message(request, messages.SUCCESS, 'Attempt BlockIP Address deleted successfully.') 
        return HttpResponseRedirect(reverse('trade_admin_auth:attemptiplist'))
'''
class ListUserAddress(ListView):
    model = UserAddress
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return UserAddress.objects.all().order_by('-id')
    
    def get_context_data(self,**kwargs):
        context=super(ListUserAddress, self).get_context_data(**kwargs)
        context['Title'] = 'User Address List'
        content_qs = UserAddress.objects.all().order_by('-id')
        context['content_qs'] =content_qs
        contenttable = UserAddressTable(content_qs)
        context['table'] = contenttable
        context['activecls']='useraddressadmin'
        return context
'''

def get_hbdtoken(request):
  try:
    hbdtoken = TradeCurrency.objects.get(Q(symbol='HBD'))
  except TradeCurrency.DoesNotExist:
    hbdtoken = ''
  return hbdtoken
'''
class WalletDetail(DetailView):
    model = UserAddress 
    template_name = 'trade_admin_auth/wallet_detail.html'
    def get_context_data(self, **kwargs):
       context = super(WalletDetail, self).get_context_data(**kwargs)
       p_key = int(self.kwargs['pk'])
       staticcontent_qs = UserAddress.objects.get(id=p_key)
       context['Title'] = 'User Address Detail'
       context['staticcontent_qs']=staticcontent_qs
       wallet_qs = UserWallet.objects.filter(useraddress = staticcontent_qs.id)
       context['wallet_qs']=wallet_qs
       bid_qs = Bids.objects.filter(useraddress = staticcontent_qs.id)
       total_bid_qs = Bids.objects.filter(useraddress = staticcontent_qs.id).count()
       bid_token_values = bid_qs.aggregate(bidtokensum=Sum('bidamount'))
       bid_token = bid_token_values['bidtokensum'] if bid_token_values['bidtokensum'] else Decimal(0)
       total_winning_bid_qs = Bids.objects.filter(Q(useraddress = staticcontent_qs.id) & Q(status=1)).count()
       try:
            hbdtoken = TradeCurrency.objects.get(Q(symbol='HBD'))
       except TradeCurrency.DoesNotExist:
            hbdtoken = ''
       context['hbdtoken']=hbdtoken
       context['bid_qs']=bid_qs
       context['total_bid_qs'] = total_bid_qs
       context['bid_token']=bid_token
       context['total_winning_bid_qs']=total_winning_bid_qs
       context['activecls']='useraddressadmin'
       return context

'''

class ListSteps_Management(ListView):
    model = Steps_Management
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return Steps_Management.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(ListSteps_Management, self).get_context_data(**kwargs)
        context['Title'] = 'Step Management'
        adminactivity_qs = Steps_Management.objects.all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        Adminactivitytable = Step_Management_Table(adminactivity_qs)
        context['table'] = Adminactivitytable
        context['add_title'] ='Add BlockIp'
        context['Btn_url'] = 'trade_admin_auth:addblockip'
        return context
    
    @method_decorator(check_group("Step Management"))
    def dispatch(self, *args, **kwargs):
      return super(ListSteps_Management, self).dispatch(*args, **kwargs)

class Edit_Step_Management(UpdateView):
    model = Steps_Management
    form_class = Steps_Management_Form
    template_name = 'trade_admin_auth/edit_step_management.html'   
    def get_context_data(self, **kwargs):
       context = super(Edit_Step_Management, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       context['Title'] = 'Edit Step Management'
       context['Btn_url'] = 'trade_admin_auth:ListSteps_Management'
       return context
    
    @method_decorator(check_group("Step Management"))
    def dispatch(self, *args, **kwargs):
      return super(Edit_Step_Management, self).dispatch(*args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Step Management updated successfully.')
       return HttpResponseRedirect('/tradeadmin/ListSteps_Management/')

class List2X_Boost(ListView):
    model = Two_x_boost
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return Two_x_boost.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(List2X_Boost, self).get_context_data(**kwargs)
        context['Title'] = '2X Boost Management'
        adminactivity_qs = Two_x_boost.objects.all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        Adminactivitytable = Two_x_boost_Table(adminactivity_qs)
        context['table'] = Adminactivitytable
        context['add_title'] ='Add BlockIp'
        context['Btn_url'] = 'trade_admin_auth:addblockip'
        return context



class List_Referral_reward(ListView):
    model = Referral_reward
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return Referral_reward.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(List_Referral_reward, self).get_context_data(**kwargs)
        context['Title'] = 'Referral Reward Management'
        adminactivity_qs = Referral_reward.objects.all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        Adminactivitytable = Referral_reward_Table(adminactivity_qs)
        context['table'] = Adminactivitytable
        context['add_title'] ='Add BlockIp'
        context['Btn_url'] = 'trade_admin_auth:addblockip'
        return context
    
    @method_decorator(check_group("Referral Reward Management"))
    def dispatch(self, *args, **kwargs):
      return super(List_Referral_reward, self).dispatch(*args, **kwargs)

class Edit_Referral_Reward_Management(UpdateView):
    model = Referral_reward
    form_class = Referral_Reward_Form
    template_name = 'trade_admin_auth/edit_referral_reward.html'   
    def get_context_data(self, **kwargs):
       context = super(Edit_Referral_Reward_Management, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       context['Title'] = 'Edit Referral Reward Management'
       context['Btn_url'] = 'trade_admin_auth:List_Referral_reward'
       return context
    
    @method_decorator(check_group("Referral Reward Management"))
    def dispatch(self, *args, **kwargs):
      return super(Edit_Referral_Reward_Management, self).dispatch(*args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Referral Reward updated successfully.')
       return HttpResponseRedirect('/tradeadmin/List_Referral_reward/')

class Edit_2X_Management(UpdateView):
    model = Two_x_boost
    form_class = Two_x_boost_Form
    template_name = 'trade_admin_auth/edit_2x_management.html'   
    def get_context_data(self, **kwargs):
       context = super(Edit_2X_Management, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       context['Title'] = 'Edit 2X Management'
       context['Btn_url'] = 'trade_admin_auth:List2X_Boost'
       return context

    @transaction.atomic
    def form_valid(self, form):
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, '2X Management updated successfully.')
       return HttpResponseRedirect('/tradeadmin/List2X_Boost/')

    
    @method_decorator(check_group("Manage User"))
    def dispatch(self, *args, **kwargs):
      return super(List_User_Management, self).dispatch(*args, **kwargs)
    

class List_User_Management(TemplateView):
    template_name = "trade_admin_auth/usermanagement_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Title'] = 'User Management'
        context["Btn_url"] = "trade_admin_auth: List_User_Management"
        return context
        
def getUsers(request):

  start = int(request.POST['start'])
  draw = int(request.POST['draw'])
  length = int(request.POST['length'])
  search_type = (request.POST['search_type'])
  search_value = (request.POST['search_value'])

  if search_value !='':
    if int(search_type) == 1:
      obj_username = User_Management.objects.raw('SELECT U.id , U.Name,U.Email, U2.Email as User_Verification_Status , U.Direct_referral_id ,U.phone_number, U.user_profile_pic,U.request_device_id,U.USER_INRID, U.status, U.created_on, U.User_type FROM USPzTPzfNdmGTlER as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.user_id FROM REFFITHkpbdREL R where R.referal_code = U.referal_code) WHERE U.Name LIKE %s ORDER BY U.id DESC LIMIT %s , %s', ["%" + search_value + "%",start,length])

      serializer = User_see(obj_username,many=True)

      for total_count in User_Management.objects.raw('SELECT U.id , COUNT(*) as counts FROM USPzTPzfNdmGTlER as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.user_id FROM REFFITHkpbdREL R where R.referal_code = U.referal_code) WHERE U.Name LIKE %s', ["%" + search_value + "%"]):

        totalRecords = total_count.counts

        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))

        tt = (list(set_object))

        tt.sort(reverse=False)
      
    elif int(search_type) == 2:
      obj_username = User_Management.objects.raw('SELECT U.id , U.Name,U.Email, U2.Email as User_Verification_Status , U.Direct_referral_id ,U.phone_number, U.user_profile_pic,U.request_device_id, U.USER_INRID,U.status, U.created_on, U.User_type FROM USPzTPzfNdmGTlER as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.user_id FROM REFFITHkpbdREL R where R.referal_code = U.referal_code) WHERE U.Email LIKE %s ORDER BY U.id DESC LIMIT %s , %s', ["%" + search_value + "%", start,length])

      serializer = User_see(obj_username,many=True)

      for total_count in User_Management.objects.raw('SELECT U.id , COUNT(*) as counts FROM USPzTPzfNdmGTlER as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.user_id FROM REFFITHkpbdREL R where R.referal_code = U.referal_code) WHERE U.Email LIKE %s', ["%" + search_value + "%"]):

        totalRecords = total_count.counts

        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))

        tt = (list(set_object))

        tt.sort(reverse=False)


    elif int(search_type) == 3:
        obj_username = User_Management.objects.raw('SELECT U.id , U.Name,U.Email, U2.Email as User_Verification_Status , U.Direct_referral_id ,U.phone_number, U.user_profile_pic,U.request_device_id,U.USER_INRID, U.status, U.created_on, U.User_type FROM USPzTPzfNdmGTlER as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.user_id FROM REFFITHkpbdREL R where R.referal_code = U.referal_code) WHERE U.device_unique_id LIKE %s ORDER BY U.id DESC LIMIT %s , %s', ["%" + search_value + "%", start,length])

        serializer = User_see(obj_username,many=True)

        for total_count in User_Management.objects.raw('SELECT U.id , COUNT(*) as counts FROM USPzTPzfNdmGTlER as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.user_id FROM REFFITHkpbdREL R where R.referal_code = U.referal_code) WHERE U.device_unique_id LIKE %s', ["%" + search_value + "%"]):

          totalRecords = total_count.counts

          set_object = set(range(int(start)+1, (int(start)+1 + int(length))))

          tt = (list(set_object))

          tt.sort(reverse=False)

    elif int(search_type) == 4:


      for ref_code in User_Management.objects.raw('SELECT U.id , R.referal_code as ref_codes FROM USPzTPzfNdmGTlER as U JOIN REFFITHkpbdREL AS R ON R.user_id = U.id AND U.Email = %s',[search_value]):

        obj_username = User_Management.objects.raw('SELECT U.id , U.Name,U.Email, U2.Email as User_Verification_Status , U.Direct_referral_id ,U.phone_number, U.user_profile_pic,U.request_device_id,U.USER_INRID, U.status, U.created_on, U.User_type FROM USPzTPzfNdmGTlER as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.user_id FROM REFFITHkpbdREL R where R.referal_code = U.referal_code) WHERE U.referal_code = %s ORDER BY U.id DESC LIMIT %s , %s', [ref_code.ref_codes, start,length])

        serializer = User_see(obj_username,many=True)

        for total_count in User_Management.objects.raw('SELECT U.id , COUNT(*) as counts FROM USPzTPzfNdmGTlER as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.user_id FROM REFFITHkpbdREL R where R.referal_code = U.referal_code) WHERE U.referal_code = %s', [ref_code.ref_codes]):

          totalRecords = total_count.counts

          set_object = set(range(int(start)+1, (int(start)+1 + int(length))))

          tt = (list(set_object))

          tt.sort(reverse=False)
  else:
    obj_username = User_Management.objects.raw('SELECT U.id , U.Name,U.Email, U2.Email as User_Verification_Status , U.Direct_referral_id ,U.phone_number, U.user_profile_pic,U.request_device_id, U.USER_INRID,U.status, U.created_on, U.User_type FROM USPzTPzfNdmGTlER as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.user_id FROM REFFITHkpbdREL R where R.referal_code = U.referal_code) ORDER BY U.id DESC LIMIT %s , %s', [start,length])

    serializer = User_see(obj_username,many=True)
    
    for total_count in User_Management.objects.raw('SELECT U.id, COUNT(*) as counts FROM USPzTPzfNdmGTlER as U'):

      totalRecords = total_count.counts
 
      set_object = set(range(int(start)+1, (int(start)+1 + int(length))))

      tt = (list(set_object))

      tt.sort(reverse=False)

  return JsonResponse({'data':serializer.data,"draw": draw,"recordsTotal": totalRecords,"recordsFiltered": totalRecords,"tt":tt})

class Edit_User_Management(UpdateView):
    model = User_Management
    form_class = User_Management_Form
    template_name = 'trade_admin_auth/edit_user.html'   
    def get_context_data(self, **kwargs):
       context = super(Edit_User_Management, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       user = User_Management.objects.get(id = p_key )
       context['Pic'] = user.user_profile_pic
       context['Title'] = 'Edit User'
       context['Btn_url'] = 'trade_admin_auth:List_User_Management'
       return context
    
    @method_decorator(check_group_icon_menu("Actions"))
    def dispatch(self, *args, **kwargs):
      return super(Edit_User_Management, self).dispatch(*args, **kwargs)



    @transaction.atomic
    def form_valid(self, form):
       form.instance.modified_by_id = self.request.user.id
       form_email = form.instance.Email
       form_device_id=form.instance.device_unique_id
       form_USER_INRID=form.instance.USER_INRID
       obj_device_id = User_Management.objects.filter(device_unique_id = form_device_id).exclude(id = form.instance.id)
       decvice_cout= User_Management.objects.filter(device_unique_id = form_device_id).count()
       if decvice_cout == 1 :
        if obj_device_id.exists():
          messages.add_message(self.request, messages.ERROR, 'Device id already exists.')
          return HttpResponseRedirect('/tradeadmin/Edit_User_Management/'+str(form.instance.id))
        else:
          formsave=form.save()
       else:
        obj_email = User_Management.objects.filter(Email = form_email).exclude(id = form.instance.id)
        if obj_email.exists():
            messages.add_message(self.request, messages.ERROR, 'Email already exists.')
            return HttpResponseRedirect('/tradeadmin/Edit_User_Management/'+str(form.instance.id))
        else:
            formsave=form.save()
       messages.add_message(self.request, messages.SUCCESS, 'User Details updated successfully.')
       return HttpResponseRedirect('/tradeadmin/Edit_User_Management/'+str(form.instance.id))


class List_Steps_history(ListView):
    model = Steps_history
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return Steps_history.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(List_Steps_history, self).get_context_data(**kwargs)
        context['Title'] = 'Step History Management'
        p_key = self.kwargs['pk']
        adminactivity_qs = Steps_history.objects.filter(user_id = p_key )
        context['adminactivity_qs'] =adminactivity_qs
        Adminactivitytable = Steps_history_Table(adminactivity_qs)
        context['table'] = Adminactivitytable
        context['add_title'] ='Add BlockIp'
        context['Btn_url'] = 'trade_admin_auth:addblockip'
        return context

class List_Delete_Account_Reason(ListView):
    model = Delete_Account_Reason_Management
    template_name = 'trade_master/generic_list_add.html'
    def get_queryset(self, **kwargs):
      return Delete_Account_Reason_Management.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(List_Delete_Account_Reason, self).get_context_data(**kwargs)
        context['Title'] = 'Delete Account Reason Management'
        adminactivity_qs = Delete_Account_Reason_Management.objects.all()
        context['adminactivity_qs'] =adminactivity_qs
        Adminactivitytable = Delete_Account_Reason_Management_Table(adminactivity_qs)
        context['table'] = Adminactivitytable
        context['add_title'] ='Add Reason'
        context['Btn_url'] = 'trade_admin_auth:AddDeleteReason'
        return context
    
    @method_decorator(check_group("Delete Account reason"))
    def dispatch(self, *args, **kwargs):
      return super(List_Delete_Account_Reason, self).dispatch(*args, **kwargs)

class AddDeleteReason(BlockIpaddressAdminRequiredMixin,CreateView):
    model = Delete_Account_Reason_Management
    form_class = Delete_aAccount_Reason_Form
    template_name = 'trade_admin_auth/add_delete_reason.html'   
    def get_context_data(self, **kwargs):
       context = super(AddDeleteReason, self).get_context_data(**kwargs)
       context['Title'] = 'Add Reason'
       context['Btn_url'] = 'trade_admin_auth:AddDeleteReason'
       return context

    @method_decorator(check_group("Delete Account reason"))
    def dispatch(self, *args, **kwargs):
      return super(AddDeleteReason, self).dispatch(*args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
        
       form.instance.created_on   = datetime.datetime.now()
       form.instance.modified_on = datetime.datetime.now()
       formsave=form.save()
       
       messages.add_message(self.request, messages.SUCCESS, 'Reason created successfully.')
       return HttpResponseRedirect('/tradeadmin/List_Delete_Account_Reason/')

class Edit_Delete_Reason_Management(UpdateView):
    model = Delete_Account_Reason_Management
    form_class = Delete_aAccount_Reason_Form
    template_name = 'trade_admin_auth/edit_reason.html'   
    def get_context_data(self, **kwargs):
       context = super(Edit_Delete_Reason_Management, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       user = Delete_Account_Reason_Management.objects.get(id = p_key )
       context['Btn_url'] = 'trade_admin_auth:List_Delete_Account_Reason'
       context['Title'] = 'Edit Reason'
       return context
    
    @method_decorator(check_group("Delete Account reason"))
    def dispatch(self, *args, **kwargs):
      return super(Edit_Delete_Reason_Management, self).dispatch(*args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
       
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Reason updated successfully.')
       return HttpResponseRedirect('/tradeadmin/List_Delete_Account_Reason/')

class List_Withdraw_Request(ListView):
    template_name = 'trade_admin_auth/withdraw_request.html'
    def get_queryset(self, **kwargs):
      return Withdraw.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['Title'] = 'Withdraw Request Management'
        context['Btn_url'] = 'trade_admin_auth:List_Withdraw_Request'
        return context

    @method_decorator(check_group("Transaction"))
    def dispatch(self, *args, **kwargs):
      return super(List_Withdraw_Request, self).dispatch(*args, **kwargs)
  
class BurnList_Withdraw_Request(ListView):
    template_name = 'trade_admin_auth/burnwithdraw_request.html'
    def get_queryset(self, **kwargs):
      return burnwithdraw.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['Title'] = 'Burn Withdraw Request Management'
        context['Btn_url'] = 'trade_admin_auth:BurnList_Withdraw_Request'
        return context

    @method_decorator(check_group("Transaction"))
    def dispatch(self, *args, **kwargs):
      return super(BurnList_Withdraw_Request, self).dispatch(*args, **kwargs)
    

class List_Admin_profit_Request(ListView):
    model = Admin_Profit
    template_name = 'trade_admin_auth/admin_profit_list.html'
    def get_queryset(self, **kwargs):
      return Admin_Profit.objects.all().order_by('-id')
    
    def get_context_data(self,**kwargs):
        context=super(List_Admin_profit_Request, self).get_context_data(**kwargs)
        context['Title'] = 'Admin Profit List'
        adminactivity_qs = Admin_Profit.objects.all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        user_count = Admin_Profit.objects.all().count()
        context['user_count'] = user_count
        filter = AdminProfitFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        filter.form.helper = AdminProfitSearch_Form()
        filter.form.helper.add_input(Submit('submit', 'Search',css_class="btn btn-default"))
        
        filter.form.helper.add_input(Reset('Reset Search','Reset Search',css_class="btn btn-default",css_id='reset-search'))
        Adminactivitytable = Admin_Profit_Table(filter.qs)
        RequestConfig(self.request, paginate={'per_page': 10}).configure(Adminactivitytable)
        
        context['table'] = Adminactivitytable
        context['filter'] = filter
        context['add_title'] ='Add BlockIp'
        context['Btn_url'] = 'trade_admin_auth:List_Admin_profit_Request'
        return context
    
    @method_decorator(check_group("Admin profit"))
    def dispatch(self, *args, **kwargs):
      return super(List_Admin_profit_Request, self).dispatch(*args, **kwargs)
    

class DetailWithdraw(DetailView):
    model = Withdraw 
    template_name = 'trade_admin_auth/withdraw_detail.html'
    def get_context_data(self, **kwargs):
       context = super(DetailWithdraw, self).get_context_data(**kwargs)
       p_key = int(self.kwargs['pk'])
       staticcontent_qs = Withdraw.objects.get(id=p_key)
       context['Title'] = 'Withdraw Detail'
       context['staticcontent_qs']=staticcontent_qs
       context['activecls']='cmsstaticadmin'
       return context

class List_Delete_Account_Request(ListView):
    model = Delete_Account_Management
    template_name = 'trade_admin_auth/delete_request_list.html'
    def get_queryset(self, **kwargs):
      return Delete_Account_Management.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(List_Delete_Account_Request, self).get_context_data(**kwargs)
        context['Title'] = 'Delete Account Reason Management'
        adminactivity_qs = Delete_Account_Management.objects.all()
        context['adminactivity_qs'] =adminactivity_qs
        Adminactivitytable = Delete_Account_Request_Management_Table(adminactivity_qs)
        context['table'] = Adminactivitytable
        context['add_title'] ='Add Reason'
        context['Btn_url'] = 'trade_admin_auth:AddDeleteReason'
        return context

    @method_decorator(check_group("Delete Account Requests"))
    def dispatch(self, *args, **kwargs):
      return super(List_Delete_Account_Request, self).dispatch(*args, **kwargs)

class Detail_Delete_Request(DetailView):
    model = Delete_Account_Management 
    template_name = 'trade_admin_auth/delete_request.html'
    def get_context_data(self, **kwargs):
       context = super(Detail_Delete_Request, self).get_context_data(**kwargs)
       p_key = int(self.kwargs['pk'])
       staticcontent_qs = Delete_Account_Management.objects.get(id=p_key)
       context['Title'] = 'Request Detail Management'
       context['staticcontent_qs']=staticcontent_qs
       context['activecls']='cmsstaticadmin'
       return context


class Delete_Request(View):
    def get(self, request, *args, **kwargs):
        pkey =  (self.kwargs['pk'])
        user_qs = get_object_or_404(Delete_Account_Management, pk=pkey)
        try:
            get_user_id = Delete_Account_Management.objects.get(id=pkey)
            user_qs.delete()
        except:
            user_qs.delete()
            

        messages.add_message(request, messages.SUCCESS, 'Record deleted successfully.') 
        return HttpResponseRedirect('/tradeadmin/List_Delete_Account_Request/')

class List_plan(ListView):
    model = plan
    template_name = 'trade_master/generic_list_add.html'
    def get_queryset(self, **kwargs):
      return plan.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(List_plan, self).get_context_data(**kwargs)
        context['Title'] = 'Plan List'
        adminactivity_qs = plan.objects.all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        Adminactivitytable = Plan_Table(adminactivity_qs)
        context['table'] = Adminactivitytable
        context['add_title'] ='Add Plan'
        context['Btn_url'] = 'trade_admin_auth:Addplan'
        return context
    
    @method_decorator(check_group("Plan Management"))
    def dispatch(self, *args, **kwargs):
      return super(List_plan, self).dispatch(*args, **kwargs)


class Addplan(BlockIpaddressAdminRequiredMixin,CreateView):
    model = plan
    form_class = Plan_Form
    template_name = 'trade_admin_auth/add_plan.html'   
    def get_context_data(self, **kwargs):
       context = super(Addplan, self).get_context_data(**kwargs)
       context['Title'] = 'Add Plan'
       context['Btn_url'] = 'trade_admin_auth:Addplan'
       try:
        step = Steps_Management.objects.get(id = 1)
        step_reward = step.step_value
        context['step_reward'] = step_reward
       except:
         step = Steps_Management.objects.get(id = 1)
         step_reward = step.step_value
         context['step_reward'] = step_reward
       plan_object = plan.objects.filter(referral_status = 1)
       Plan=plan.objects.filter(plan_purchase_type=0).order_by("-id")
       plan_object_count = plan.objects.filter(plan_type = 0).count()
       reff = referral_level.objects.all()
       for i in plan_object:        
        Referral = reff.filter(~Q(referral_level_id = i.referral_level_eligible) & Q(status=0))
        reff = Referral
       context['Referral'] = reff
       context['Plan'] =Plan
       context['plan_object_count'] = plan_object_count
       return context

    @transaction.atomic
    def form_valid(self, form):
       try:
         plan_plan = plan.objects.get(plan_name = form.instance.plan_name)
         if plan_plan:
           messages.add_message(self.request, messages.ERROR, 'This Plan Name Already Exists')
           return HttpResponseRedirect('/tradeadmin/List_plan/')
         else:
           formsave=form.save()
           messages.add_message(self.request, messages.SUCCESS, 'Plan created successfully.')
           return HttpResponseRedirect('/tradeadmin/List_plan/')
       except:
        form.instance.two_X_Boost_status = 1
        formsave=form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Plan created successfully.')
        return HttpResponseRedirect('/tradeadmin/List_plan/')


class Edit_Plan_Management(UpdateView):
    model = plan
    form_class = Plan_Form
    template_name = 'trade_admin_auth/edit_plan.html'   
    def get_context_data(self, **kwargs):
       context = super(Edit_Plan_Management, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       user = plan.objects.get(id = p_key )
       Plan=plan.objects.filter(plan_purchase_type=0).order_by("-id")
       reff = referral_level.objects.all()
       plan_object = plan.objects.filter(referral_status = 1)
       plan_object_count = plan.objects.filter(plan_type = 0).count()
       for i in plan_object:
        Referral = reff.filter(~Q(referral_level_id = i.referral_level_eligible) & Q(status=0))
        reff = Referral
       try:
        step = Steps_Management.objects.get(id = 1)
        step_reward = step.step_value
        context['step_reward'] = step_reward
       except:
        step = Steps_Management.objects.get(id = 1)
        step_reward = step.step_value
        context['step_reward'] = step_reward
       context['Referral'] = reff
       context['user'] = user
       context['Plan'] = Plan
       context['plan_object_count'] = plan_object_count
       context['Btn_url'] = 'trade_admin_auth:List_plan'
       context['Title'] = 'Edit Plan'
       return context

    @transaction.atomic
    def form_valid(self, form):
       if form.instance.referral_status == 0:
         form.instance.level = 0
         form.instance.referral_level_eligible = 0
       formsave=form.save()
       messages.add_message(self.request, messages.SUCCESS, 'Plan updated successfully.')
       return HttpResponseRedirect('/tradeadmin/List_plan/')

class Delete_Plan(View):
    def get(self, request, *args, **kwargs):
        pkey =  (self.kwargs['pk'])
        user_qs = get_object_or_404(plan, pk=pkey)
        try:
            get_user_id = plan.objects.get(id=pkey)
           
            user_qs.delete()
        except:
            user_qs.delete()

        messages.add_message(request, messages.SUCCESS, 'Plan deleted successfully.') 
        return HttpResponseRedirect('/tradeadmin/List_plan/')


class List_referral_level(ListView):
    model = referral_level
    template_name = 'trade_master/generic_list_add.html'
    def get_queryset(self, **kwargs):
      return referral_level.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(List_referral_level, self).get_context_data(**kwargs)
        context['Title'] = 'Referral Level List'
        adminactivity_qs = referral_level.objects.all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        Adminactivitytable = Referral_level_Table(adminactivity_qs)
        context['table'] = Adminactivitytable
        context['add_title'] ='Add Referral Level'
        context['Btn_url'] = 'trade_admin_auth:Add_referral_level'
        return context
    
    @method_decorator(check_group("Referral Management"))
    def dispatch(self, *args, **kwargs):
      return super(List_referral_level, self).dispatch(*args, **kwargs)


class Add_referral_level(BlockIpaddressAdminRequiredMixin,CreateView):
    model = referral_level
    form_class = Referral_Level_Form
    template_name = 'trade_admin_auth/add_referral_level.html'   
    def get_context_data(self, **kwargs):
       context = super(Add_referral_level, self).get_context_data(**kwargs)
       adminactivity_qs = referral_level.objects.all().order_by('-id')
       context['adminactivity_qs'] =adminactivity_qs
       context['Title'] = 'Add Referral Level'
       context['Btn_url'] = 'trade_admin_auth:Add_referral_level'
       return context
    
    @method_decorator(check_group("Referral Management"))
    def dispatch(self, *args, **kwargs):
      return super(Add_referral_level, self).dispatch(*args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
       adminactivity_qs = referral_level.objects.all().order_by('-id')
       if adminactivity_qs:
        for i in adminactivity_qs:
          if i.referral_level_id == form.instance.referral_level_id: 
            messages.add_message(self.request, messages.ERROR, 'Referral Level Already Exists')
            return HttpResponseRedirect('/tradeadmin/List_referral_level/')
          else:
            formsave=form.save()      
            messages.add_message(self.request, messages.SUCCESS, 'Referral Level created successfully.')
            return HttpResponseRedirect('/tradeadmin/List_referral_level/')
       else:
           formsave=form.save()      
           messages.add_message(self.request, messages.SUCCESS, 'Referral Level created successfully.')
           return HttpResponseRedirect('/tradeadmin/List_referral_level/')


class Edit_Referral_level_Management(UpdateView):
    model = referral_level
    form_class = Referral_Level_Form
    template_name = 'trade_admin_auth/edit_referral_level.html'   
    def get_context_data(self, **kwargs):
       context = super(Edit_Referral_level_Management, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       user = referral_level.objects.get(id = p_key )
       context['Btn_url'] = 'trade_admin_auth:List_referral_level'
       context['Title'] = 'Edit Referral Level'
       return context
    
    @method_decorator(check_group("Referral Management"))
    def dispatch(self, *args, **kwargs):
      return super(Edit_Referral_level_Management, self).dispatch(*args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Referral Level updated successfully.')
       return HttpResponseRedirect('/tradeadmin/List_referral_level/')

class Delete_Referral(View):
    def get(self, request, *args, **kwargs):
        pkey =  (self.kwargs['pk'])
        user_qs = get_object_or_404(referral_level, pk=pkey)
        try:
            get_user_id = referral_level.objects.get(id=pkey)
            plan_object = plan.objects.filter(referral_status = 1)
            if plan_object :
              for i in plan_object:
                if i.level == get_user_id.referral_level_id:
                  messages.add_message(request, messages.ERROR, 'Level Synced With Plan Cannot Be Deleted.') 
                  return HttpResponseRedirect('/tradeadmin/List_referral_level/')                
            else:
              try:
                plan_plan = plan.objects.filter(level = get_user_id.referral_level_id)
                if plan_plan :
                  for i in plan_plan:
                    i.level = 0
                    i.referral_level_eligible = 0
                    i.save()
                else:
                  user_qs.delete()
                  messages.add_message(request, messages.SUCCESS, 'Referral Level deleted successfully.')
              except:
                user_qs.delete()
                messages.add_message(request, messages.SUCCESS, 'Referral Level deleted successfully.')
                pass
               
        except:
            user_qs.delete()
            messages.add_message(request, messages.SUCCESS, 'Referral Level deleted successfully.') 
            return HttpResponseRedirect('/tradeadmin/List_referral_level/')
        user_qs.delete()
        messages.add_message(request, messages.SUCCESS, 'Referral Level deleted successfully.')
        return HttpResponseRedirect('/tradeadmin/List_referral_level/') 

class List_user_referral(ListView):
  model = referral_table
  form_class = User_Referral_Level_Form
  template_name = 'trade_admin_auth/referral_user_list.html'
  def get_queryset(self, **kwargs):
      return plan.objects.all()
    
  def get_context_data(self,**kwargs):
      context=super(List_user_referral, self).get_context_data(**kwargs)
      context['Title'] = 'Plan List'
      adminactivity_qs = referral_table.objects.all().order_by('-id')
      context['adminactivity_qs'] =adminactivity_qs
      useractivity_qs = User_Management.objects.all()
      context['useractivity_qs'] =useractivity_qs
      Adminactivitytable = User_Referral_Table(adminactivity_qs)
      context['table'] = Adminactivitytable
      context['add_title'] ='Add Plan'
      context['Btn_url'] = 'trade_admin_auth:Addplan'
      return context


class List_market_internal(ListView):
    model = Market_place
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return Market_place.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(List_market_internal, self).get_context_data(**kwargs)
        context['Title'] = 'Management List'
        adminactivity_qs = Market_place.objects.all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        Adminactivitytable = List_market_internal_Table(adminactivity_qs)
        context['table'] = Adminactivitytable
        context['add_title'] ='Add Plan'
        context['Btn_url'] = 'trade_admin_auth:Addplan'
        return context

class Edit_market_internal_Management(UpdateView):
    model = Market_place
    form_class = Market_Internal_Form
    template_name = 'trade_admin_auth/edit_management.html'   
    def get_context_data(self, **kwargs):
       context = super(Edit_market_internal_Management, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       user = Market_place.objects.get(id = p_key )
       context['Btn_url'] = 'trade_admin_auth:List_market_internal'
       context['Title'] = 'Edit'
       return context

    @transaction.atomic
    def form_valid(self, form):
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Updated successfully.')
       return HttpResponseRedirect('/tradeadmin/List_market_internal/')


class List_Withdraw_values_internal(ListView):
    model = withdraw_values
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return withdraw_values.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(List_Withdraw_values_internal, self).get_context_data(**kwargs)
        context['Title'] = 'Management List'
        adminactivity_qs = withdraw_values.objects.all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        Adminactivitytable = List_withdraw_Value_Table(adminactivity_qs)
        context['table'] = Adminactivitytable
        context['add_title'] ='Add Plan'
        context['Btn_url'] = 'trade_admin_auth:Addplan'
        return context

    @method_decorator(check_group("Withdraw Management"))
    def dispatch(self, *args, **kwargs):
      return super(List_Withdraw_values_internal, self).dispatch(*args, **kwargs)


class Edit_Withdraw_value_Management(UpdateView):
    model = withdraw_values
    form_class = withdraw_values_Form
    template_name = 'trade_admin_auth/edit_withdraw_values_list.html'   
    def get_context_data(self, **kwargs):
       context = super(Edit_Withdraw_value_Management, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       user = withdraw_values.objects.get(id = p_key )
       context['Btn_url'] = 'trade_admin_auth:List_Withdraw_values_internal'
       context['Title'] = 'Edit'
       return context
    
    @method_decorator(check_group("Withdraw Management"))
    def dispatch(self, *args, **kwargs):
      return super(Edit_Withdraw_value_Management, self).dispatch(*args, **kwargs)
    
    @transaction.atomic
    def form_valid(self, form):
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Updated successfully.')
       return HttpResponseRedirect('/tradeadmin/List_Withdraw_values_internal/')


@check_group("Manage User")
def user_list_management(request,data):
  context = {}
  company_qs = Company.objects.get(id=1)
  try:
    usr_name = request.GET['username']
  except:
    usr_name = ""
  try:
    email = request.GET['Email']
  except:
    email = ""
  usr = 0
  count = 0
  dict_users = {}
  start_page = request.GET.get('pageno', 1)
  end_value = int(start_page) * 10
  start_value = int(end_value) - 9

  if data == "alluser":    
    adminactivity_qs = User_Management.objects.filter(status = 0).order_by('-id')
    context['adminactivity_qs'] =adminactivity_qs
    context['Title'] = 'Total Users'
    if usr_name and email:
      obj_username = User_Management.objects.filter(Q(Name__icontains = usr_name) and Q(Email__icontains = email)).filter(status=0).order_by('-id')
      for i in obj_username:
       
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          if i.plan != 0:
            plan_plan = plan.objects.get(id = int(i.plan))
            list_usr["Plan"] = (plan_plan.plan_name)
          else:
            list_usr["Plan"] = "Free Plan"
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    elif email:
      obj_username = User_Management.objects.filter(Email__icontains = email).filter(status=0).order_by('-id')
      for i in obj_username:
       
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          if i.plan != 0:
            plan_plan = plan.objects.get(id = int(i.plan))
            list_usr["Plan"] = (plan_plan.plan_name)
          else:
            list_usr["Plan"] = "Free Plan"
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    elif usr_name:
      obj_username = User_Management.objects.filter(Name__icontains = usr_name).filter(status=0).order_by('-id')
      for i in obj_username:
       
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          if i.plan != 0:
            plan_plan = plan.objects.get(id = int(i.plan))
            list_usr["Plan"] = (plan_plan.plan_name)
          else:
            list_usr["Plan"] = "Free Plan"
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    else:
      obj_username = User_Management.objects.filter(Name__icontains = usr_name).filter(status=0).order_by('-id')
      for i in obj_username:
       
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          if i.plan != 0:
            plan_plan = plan.objects.get(id = int(i.plan))
            list_usr["Plan"] = (plan_plan.plan_name)
          else:
            list_usr["Plan"] = "Free Plan"
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    try:
      tot_user_qs = obj_username
    except:
      tot_user_qs = ""
    w_page = request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_user_qs, 10)
    try:
        trade_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        trade_qs =w_paginator.page(1)
    except EmptyPage:
        trade_qs = w_paginator.page(w_paginator.num_pages)
    context['trade_qs'] = trade_qs

  if data == "activeuser":
    adminactivity_qs = User_Management.objects.filter(status = 0).order_by('-id')
    context['adminactivity_qs'] =adminactivity_qs
    context['Title'] = 'Active Users'
    if usr_name and email:
      obj_username = User_Management.objects.filter(status = 0).filter(Q(Name__icontains = usr_name) and Q(Email__icontains = email)).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          if i.plan != 0:
            plan_plan = plan.objects.get(id = int(i.plan))
            list_usr["Plan"] = (plan_plan.plan_name)
          else:
            list_usr["Plan"] = "Free Plan"
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    elif email:
      obj_username = User_Management.objects.filter(status = 0).filter(Email__icontains = email).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.user_name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          if i.plan != 0:
            plan_plan = plan.objects.get(id = int(i.plan))
            list_usr["Plan"] = (plan_plan.plan_name)
          else:
            list_usr["Plan"] = "Free Plan"
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    elif usr_name:
      obj_username = User_Management.objects.filter(status = 0).filter(Name__icontains = usr_name).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          if i.plan != 0:
            plan_plan = plan.objects.get(id = int(i.plan))
            list_usr["Plan"] = (plan_plan.plan_name)
          else:
            list_usr["Plan"] = "Free Plan"
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    else:
      obj_username = User_Management.objects.filter(status = 0).filter(Name__icontains = usr_name).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          if i.plan != 0:
            plan_plan = plan.objects.get(id = int(i.plan))
            list_usr["Plan"] = (plan_plan.plan_name)
          else:
            list_usr["Plan"] = "Free Plan"
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    try:
      tot_user_qs = obj_username
    except:
      tot_user_qs = ""
    w_page = request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_user_qs, 10)
    try:
        trade_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        trade_qs =w_paginator.page(1)
    except EmptyPage:
        trade_qs = w_paginator.page(w_paginator.num_pages)
    context['trade_qs'] = trade_qs

  if data == "Inactiveuser":
    adminactivity_qs = User_Management.objects.filter(status = 1).order_by('-id')
    context['adminactivity_qs'] =adminactivity_qs
    context['Title'] = 'Inactive Users'
    if usr_name and email:
      obj_username = User_Management.objects.filter(status = 1).filter(Q(Name__icontains = usr_name) and Q(Email__icontains = email)).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          list_usr["Plan"] = (i.plan)
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    elif email:
      obj_username = User_Management.objects.filter(status = 1).filter(Email__icontains = email).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.user_name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          list_usr["Plan"] = (i.plan)
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    elif usr_name:
      obj_username = User_Management.objects.filter(status = 1).filter(Name__icontains = usr_name).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          list_usr["Plan"] = (i.plan)
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    else:
      obj_username = User_Management.objects.filter(status = 1).filter(Name__icontains = usr_name).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          list_usr["Plan"] = (i.plan)
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    try:
      tot_user_qs = obj_username
    except:
      tot_user_qs = ""
    w_page = request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_user_qs, 10)
    try:
        trade_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        trade_qs =w_paginator.page(1)
    except EmptyPage:
        trade_qs = w_paginator.page(w_paginator.num_pages)
    context['trade_qs'] = trade_qs

  if data == "Planactiveuser":
    adminactivity_qs = User_Management.objects.filter(~Q(plan = 0)).order_by('-id')
    context['adminactivity_qs'] =adminactivity_qs
    context['Title'] = 'Plan Active Users'
    if usr_name and email:
      obj_username = User_Management.objects.filter(~Q(plan = 0)).filter(Q(Name__icontains = usr_name) and Q(Email__icontains = email)).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          list_usr["Plan"] = (i.plan)
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    elif email:
      obj_username = User_Management.objects.filter(~Q(plan = 0)).filter(Email__icontains = email).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.user_name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          list_usr["Plan"] = (i.plan)
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    elif usr_name:
      obj_username = User_Management.objects.filter(~Q(plan = 0)).filter(Name__icontains = usr_name).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          list_usr["Plan"] = (i.plan)
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    else:
      obj_username = User_Management.objects.filter(~Q(plan = 0)).filter(Name__icontains = usr_name).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          list_usr["Plan"] = (i.plan)
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    try:
      tot_user_qs = obj_username
    except:
      tot_user_qs = ""
    w_page = request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_user_qs, 10)
    try:
        trade_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        trade_qs =w_paginator.page(1)
    except EmptyPage:
        trade_qs = w_paginator.page(w_paginator.num_pages)
    context['trade_qs'] = trade_qs

  if data == "android_current_version_users_list":    
    adminactivity_qs = User_Management.objects.filter(Q(phone_number = company_qs.Android_version) & Q(user_profile_pic = 'Android')).filter(status = 0).order_by('-id')
    context['adminactivity_qs'] =adminactivity_qs
    context['Title'] = 'Android Currenct Version Users'
    if usr_name and email:
      obj_username = User_Management.objects.filter(Q(phone_number = company_qs.Android_version) & Q(user_profile_pic = 'Android')).filter(status = 0).filter(Q(Name__icontains = usr_name) and Q(Email__icontains = email)).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          list_usr["Plan"] = (i.plan)
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    elif email:
      obj_username = User_Management.objects.filter(Q(phone_number = company_qs.Android_version) & Q(user_profile_pic = 'Android')).filter(status = 0).filter(Email__icontains = email).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          list_usr["Plan"] = (i.plan)
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    elif usr_name:
      obj_username = User_Management.objects.filter(Q(phone_number = company_qs.Android_version) & Q(user_profile_pic = 'Android')).filter(status = 0).filter(Name__icontains = usr_name).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          list_usr["Plan"] = (i.plan)
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    else:
      obj_username = User_Management.objects.filter(Q(phone_number = company_qs.Android_version) & Q(user_profile_pic = 'Android')).filter(status = 0).filter(Name__icontains = usr_name).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          list_usr["Plan"] = (i.plan)
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    try:
      tot_user_qs = obj_username
    except:
      tot_user_qs = ""
    w_page = request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_user_qs, 10)
    try:
        trade_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        trade_qs =w_paginator.page(1)
    except EmptyPage:
        trade_qs = w_paginator.page(w_paginator.num_pages)
    context['trade_qs'] = trade_qs

  if data == "ios_current_version_users_list":
    adminactivity_qs = User_Management.objects.filter(Q(phone_number = company_qs.IOS_version) & Q(user_profile_pic = 'IOS')).filter(status = 0).order_by('-id')
    context['adminactivity_qs'] =adminactivity_qs
    context['Title'] = 'IOS Currenct Version Users'
    if usr_name and email:
      obj_username = User_Management.objects.filter(Q(phone_number = company_qs.IOS_version) & Q(user_profile_pic = 'IOS')).filter(status = 0).filter(Q(Name__icontains = usr_name) and Q(Email__icontains = email)).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          list_usr["Plan"] = (i.plan)
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    elif email:
      obj_username = User_Management.objects.filter(Q(phone_number = company_qs.IOS_version) & Q(user_profile_pic = 'IOS')).filter(status = 0).filter(Email__icontains = email).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          list_usr["Plan"] = (i.plan)
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    elif usr_name:
      obj_username = User_Management.objects.filter(Q(phone_number = company_qs.IOS_version) & Q(user_profile_pic = 'IOS')).filter(status = 0).filter(Name__icontains = usr_name).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          list_usr["Plan"] = (i.plan)
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr
    else:
      obj_username = User_Management.objects.filter(Q(phone_number = company_qs.IOS_version) & Q(user_profile_pic = 'IOS')).filter(status = 0).filter(Name__icontains = usr_name).order_by('-id')
      for i in obj_username:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["id"] = (i.id)
          list_usr["username"] = (i.Name)
          list_usr["email"] = (i.Email)
          list_usr["ref_id"] = (i.Referral_id)
          list_usr["ref_user"] = (i.Direct_referral_id)
          list_usr["App_version"] = (i.phone_number)
          list_usr["Plan"] = (i.plan)
          list_usr["phone_type"] = (i.user_profile_pic)
          list_usr["status"] = (i.status)
          list_usr["date"] = (str(i.created_on))
          list_usr["user_type"] = (i.User_type)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_users[count] = list_usr

   
    try:
      tot_user_qs = obj_username
    except:
      tot_user_qs = ""
    w_page = request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_user_qs, 10)
    try:
        trade_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        trade_qs =w_paginator.page(1)
    except EmptyPage:
        trade_qs = w_paginator.page(w_paginator.num_pages)
    context['trade_qs'] = trade_qs
  
  context["endpage"] = trade_qs.number+1
  context["startpage"] = trade_qs.number-1
  context['start_value'] = trade_qs.start_index()
  context['end_value'] = trade_qs.end_index()
  context['usr_count'] = obj_username.count()
  context['dict_users_list'] = json.dumps(dict_users)  
  return render(request,'trade_admin_auth/list_user.html',context)

def user_list_for_update(request):
  context = {} 
  context['Title'] = 'User Audit Management'
  sum_amount = 0
  sum_amount_referral = 0
  co = 0
  audit_user_dict = {}
  try:
    email = request.GET['Email']
  except:
    email = ""
  start_page = request.GET.get('pageno', 1)
  end_value = int(start_page) * 10
  start_value = int(end_value) - 9
  
  if email:
    user_obj = User_Management.objects.filter(status = 0).filter(Email__icontains = email).order_by('-id')
    for i in user_obj:
      audit_dict = {}
      co = co+1
      if start_value <= co <= end_value:
        try:
          wallet = UserCashWallet.objects.get(userid_id = i.id)
          blnc = wallet.balanceone
          reff_blnc = wallet.referalincome
        except:
          wallet = ""
          blnc = 0
          reff_blnc = 0
        audit_dict["balance"] = blnc
        audit_dict["referal_balance"] = reff_blnc

        if i.plan == 0:
          History_Reward = Reward_History.objects.filter(user_id = i.id,reward_status="step_reward").aggregate(Sum('Reward'))
          Boost_Reward = Reward_History.objects.filter(user_id = i.id,reward_status="2XBoost").aggregate(Sum('Reward'))
          withdraw_amount  = Withdraw.objects.filter(userid = i.id,created_on__gte = i.plan_start_date,Wallet_type = "Reward_wallet")
          rewards_history = Referral_reward_History.objects.filter(user = i.id).aggregate(Sum('reward'))
          for k in withdraw_amount :
            sum_amount = sum_amount + Decimal(k.Amount)
          withdraw_amount_referral  = Withdraw.objects.filter(userid = i.id,created_on__gte = i.plan_start_date,Wallet_type = "Referral_wallet")
          for j in withdraw_amount_referral :
            sum_amount_referral = sum_amount_referral + Decimal(j.Amount)
          ref_rew = 0.1
          audit_dict["ref_rew"] = ref_rew
        else:
          History_Reward = Reward_History.objects.filter(user_id = i.id,reward_status="step_reward",created_on__date__gte = i.plan_start_date.date()).aggregate(Sum('Reward'))
          Boost_Reward = Reward_History.objects.filter(user_id = i.id,reward_status="2XBoost",created_on__date__gte = i.plan_start_date.date()).aggregate(Sum('Reward'))
          withdraw_amount  = Withdraw.objects.filter(userid = i.id,created_on__gte = i.plan_start_date,Wallet_type = "Reward_wallet")
          rewards_history = Referral_reward_History.objects.filter(user = i.id,created_on__date__gte = i.plan_start_date.date()).aggregate(Sum('reward'))
          for k in withdraw_amount :
            sum_amount = sum_amount + Decimal(k.Amount)
          withdraw_amount_referral  = Withdraw.objects.filter(userid = i.id,created_on__gte = i.plan_start_date,Wallet_type = "Referral_wallet")
          for j in withdraw_amount_referral :
            sum_amount_referral = sum_amount_referral + Decimal(j.Amount)
          ref_rew = 0
          audit_dict["ref_rew"] = ref_rew

        if(History_Reward['Reward__sum'] == None):
          History_Reward = 0
        else :
          History_Reward = History_Reward['Reward__sum']

        if(Boost_Reward['Reward__sum'] == None):
          Boost_Reward = 0
        else :
          Boost_Reward = Boost_Reward['Reward__sum']

        if(rewards_history['reward__sum'] == None):
          Rewards_Reward = 0
        else :
          Rewards_Reward = rewards_history['reward__sum']

        total_reward = (Decimal(History_Reward) + Decimal(Boost_Reward) + Decimal(ref_rew)) - Decimal(sum_amount)

        total_diff = Decimal(blnc) - round(total_reward,7)

        total_ref_reward = Decimal(Rewards_Reward) - Decimal(sum_amount_referral)

        total_reff_diff = Decimal(reff_blnc) - round(total_ref_reward, 7)

        audit_dict["referral_income"] = total_diff
        audit_dict["Referral_diff"] = total_reff_diff
        audit_dict["total_reff"] = total_ref_reward
        audit_dict["referral_his_income"] = Rewards_Reward
        audit_dict["total_reward"] = total_reward
        audit_dict["step"] = History_Reward
        audit_dict["2x_boost"] = Boost_Reward
        audit_dict["health_rew_withdraw"] = sum_amount
        audit_dict["sum_amount_referral"] = sum_amount_referral
        audit_dict["co"] = co
        
        audit_user_dict[i.Email] = audit_dict

    context["audit_user_dict"] = audit_user_dict
  else:
    user_obj = User_Management.objects.filter(status = 0).order_by('-id')
    for i in user_obj:
      audit_dict = {}
      co = co+1
      if start_value <= co <= end_value:
        try:
          wallet = UserCashWallet.objects.get(userid_id = i.id)
          blnc = wallet.balanceone
          reff_blnc = wallet.referalincome
        except:
          wallet = ""
          blnc = 0
          reff_blnc = 0
        audit_dict["balance"] = blnc
        audit_dict["referal_balance"] = reff_blnc

        if i.plan == 0:
          History_Reward = Reward_History.objects.filter(user_id = i.id,reward_status="step_reward").aggregate(Sum('Reward'))
          Boost_Reward = Reward_History.objects.filter(user_id = i.id,reward_status="2XBoost").aggregate(Sum('Reward'))
          withdraw_amount  = Withdraw.objects.filter(userid = i.id,created_on__gte = i.plan_start_date,Wallet_type = "Reward_wallet")
          rewards_history = Referral_reward_History.objects.filter(user = i.id).aggregate(Sum('reward'))
          for k in withdraw_amount :
            sum_amount = sum_amount + Decimal(k.Amount)
          withdraw_amount_referral  = Withdraw.objects.filter(userid = i.id,created_on__gte = i.plan_start_date,Wallet_type = "Referral_wallet")
          for j in withdraw_amount_referral :
            sum_amount_referral = sum_amount_referral + Decimal(j.Amount)
          ref_rew = 0.1
          audit_dict["ref_rew"] = ref_rew
        else:
          History_Reward = Reward_History.objects.filter(user_id = i.id,reward_status="step_reward",created_on__date__gte = i.plan_start_date.date()).aggregate(Sum('Reward'))
          Boost_Reward = Reward_History.objects.filter(user_id = i.id,reward_status="2XBoost",created_on__date__gte = i.plan_start_date.date()).aggregate(Sum('Reward'))
          withdraw_amount  = Withdraw.objects.filter(userid = i.id,created_on__gte = i.plan_start_date,Wallet_type = "Reward_wallet")
          rewards_history = Referral_reward_History.objects.filter(user = i.id,created_on__date__gte = i.plan_start_date.date()).aggregate(Sum('reward'))
          for k in withdraw_amount :
            sum_amount = sum_amount + Decimal(k.Amount)
          withdraw_amount_referral  = Withdraw.objects.filter(userid = i.id,created_on__gte = i.plan_start_date,Wallet_type = "Referral_wallet")
          for j in withdraw_amount_referral :
            sum_amount_referral = sum_amount_referral + Decimal(j.Amount)
          ref_rew = 0
          audit_dict["ref_rew"] = ref_rew

        if(History_Reward['Reward__sum'] == None):
          History_Reward = 0
        else :
          History_Reward = History_Reward['Reward__sum']

        if(Boost_Reward['Reward__sum'] == None):
          Boost_Reward = 0
        else :
          Boost_Reward = Boost_Reward['Reward__sum']

        if(rewards_history['reward__sum'] == None):
          Rewards_Reward = 0
        else :
          Rewards_Reward = rewards_history['reward__sum']

        total_reward = (Decimal(History_Reward) + Decimal(Boost_Reward) + Decimal(ref_rew)) - Decimal(sum_amount)

        total_diff = Decimal(blnc) - round(total_reward,7)

        total_ref_reward = Decimal(Rewards_Reward) - Decimal(sum_amount_referral)

        total_reff_diff = Decimal(reff_blnc) - round(total_ref_reward, 7)

        audit_dict["referral_income"] = total_diff
        audit_dict["Referral_diff"] = total_reff_diff
        audit_dict["total_reff"] = total_ref_reward
        audit_dict["referral_his_income"] = Rewards_Reward
        audit_dict["total_reward"] = total_reward
        audit_dict["step"] = History_Reward
        audit_dict["2x_boost"] = Boost_Reward
        audit_dict["health_rew_withdraw"] = sum_amount
        audit_dict["sum_amount_referral"] = sum_amount_referral
        audit_dict["co"] = co
        
        audit_user_dict[i.Email] = audit_dict
    context["audit_user_dict"] = audit_user_dict

  try:
    tot_user_qs = user_obj
  except:
    tot_user_qs = ""
  w_page = request.GET.get('pageno', 1)
  w_paginator = Paginator(tot_user_qs, 10)
  try:
      trade_qs = w_paginator.page(w_page)
  except PageNotAnInteger:
      trade_qs =w_paginator.page(1)
  except EmptyPage:
      trade_qs = w_paginator.page(w_paginator.num_pages)
  context['trade_qs'] = trade_qs

  context["endpage"] = trade_qs.number+1
  context["startpage"] = trade_qs.number-1
  context["start_value"] = trade_qs.start_index()
  context["end_value"] = trade_qs.end_index()
  context["usr_count"] = user_obj.count()
    


  return render(request,'trade_admin_auth/list_user_update.html',context)



def user_list_update(request,id):
  context = {} 
  History_Reward=''
  Boost_Reward=''
  total_reward=0
  total_diff=''
  context['Title'] = 'User Management'
  adminactivity_qs = User_Management.objects.get(id=id)
  context['adminactivity_qs'] =adminactivity_qs
  con = ""
  sum_amount = 0
  sum_amount_referral = 0

  try:
    wallet = UserCashWallet.objects.get(userid_id = adminactivity_qs.id)
    blnc = wallet.balanceone
    reff_blnc = wallet.referalincome
    if adminactivity_qs.plan == 0:
      History_Reward = Reward_History.objects.filter(user_id = adminactivity_qs.id,reward_status="step_reward").aggregate(Sum('Reward'))
      Boost_Reward = Reward_History.objects.filter(user_id = adminactivity_qs.id,reward_status="2XBoost").aggregate(Sum('Reward'))
    else :
      History_Reward = Reward_History.objects.filter(user_id = adminactivity_qs.id,reward_status="step_reward",created_on__date__gte = adminactivity_qs.plan_start_date.date()).aggregate(Sum('Reward'))
      Boost_Reward = Reward_History.objects.filter(user_id = adminactivity_qs.id,reward_status="2XBoost",created_on__date__gte = adminactivity_qs.plan_start_date.date()).aggregate(Sum('Reward'))

    if adminactivity_qs.plan == 0:
      rewards_history = Referral_reward_History.objects.filter(user = adminactivity_qs.id).aggregate(Sum('reward'))
    else :
      rewards_history = Referral_reward_History.objects.filter(user = adminactivity_qs.id,created_on__gte = adminactivity_qs.plan_start_date.date()).aggregate(Sum('reward'))
    
    if adminactivity_qs.plan == 0:
      con = 0.1
    else:
      con = 0

    if adminactivity_qs == 0 :
      withdraw_amount  = Withdraw.objects.filter(userid = adminactivity_qs.id,Wallet_type = "Reward_wallet")
      for i in withdraw_amount :
        sum_amount = sum_amount + Decimal(i.Amount)
      withdraw_amount_referral  = Withdraw.objects.filter(userid = adminactivity_qs.id,Wallet_type = "Referral_wallet")
      for j in withdraw_amount_referral :
        sum_amount_referral = sum_amount_referral + Decimal(j.Amount)

      health_internal_transfer = internal_transfer_history.objects.using('second_db').filter(user = adminactivity_qs.id,from_wallet = "Reward_wallet").aggregate(Sum('actual_amount'))

      referral_internal_transfer = internal_transfer_history.objects.using('second_db').filter(user = adminactivity_qs.id,from_wallet = "Referral_wallet").aggregate(Sum('actual_amount'))


    else:
      withdraw_amount  = Withdraw.objects.filter(userid = adminactivity_qs.id,created_on__gte = adminactivity_qs.plan_start_date,Wallet_type = "Reward_wallet")
      for i in withdraw_amount :
        sum_amount = sum_amount + Decimal(i.Amount)
      withdraw_amount_referral  = Withdraw.objects.filter(userid = adminactivity_qs.id,created_on__gte = adminactivity_qs.plan_start_date,Wallet_type = "Referral_wallet")
      for j in withdraw_amount_referral :
        sum_amount_referral = sum_amount_referral + Decimal(j.Amount)
    
      health_internal_transfer = internal_transfer_history.objects.using('second_db').filter(user = adminactivity_qs.id,created_on__gte = adminactivity_qs.plan_start_date,from_wallet = "Reward_wallet").aggregate(Sum('actual_amount'))

      referral_internal_transfer = internal_transfer_history.objects.using('second_db').filter(user = adminactivity_qs.id,created_on__gte = adminactivity_qs.plan_start_date,from_wallet = "Referral_wallet").aggregate(Sum('actual_amount'))
    

    if(History_Reward['Reward__sum'] == None):
      History_Reward = 0
    else :
      History_Reward = History_Reward['Reward__sum']

    if(Boost_Reward['Reward__sum'] == None):
      Boost_Reward = 0
    else :
      Boost_Reward = Boost_Reward['Reward__sum']

    if(rewards_history['reward__sum'] == None):
      Rewards_Reward = 0
    else :
      Rewards_Reward = rewards_history['reward__sum']

    if(health_internal_transfer['actual_amount__sum'] == None):
      Health_Transfer_Reward = 0
    else :
      Health_Transfer_Reward = health_internal_transfer['actual_amount__sum']

    if(referral_internal_transfer['actual_amount__sum'] == None):
      Referral_Transfer_Reward = 0
    else :
      Referral_Transfer_Reward = referral_internal_transfer['actual_amount__sum']
      
    if adminactivity_qs.plan == 0:
      total_reward = (Decimal(History_Reward) + Decimal(Boost_Reward) + Decimal(0.1)) - (Decimal(sum_amount) + Decimal(Health_Transfer_Reward))
    else:
      total_reward = (Decimal(History_Reward) + Decimal(Boost_Reward)) -(Decimal(sum_amount) + Decimal(Health_Transfer_Reward))
 
    total_diff = Decimal(blnc) - round(total_reward,7)

    total_ref_reward = Decimal(Rewards_Reward) - (round(sum_amount_referral,7) + Decimal(Referral_Transfer_Reward))

    total_reff_diff = Decimal(wallet.referalincome) - total_ref_reward

    wallet.balanceone = round(total_reward,7)
    wallet.save()

    if rewards_history :
      wallet.referalincome = round(total_ref_reward,7)
      wallet.save()
  except:
    pass
  context['Boost_Reward'] = Boost_Reward
  context['History_Reward'] = History_Reward
  context['con'] = con
  context['Withdraw'] = sum_amount
  context['total_reward'] = round(total_reward,7)
  context['blnc'] = blnc
  context['total_diff'] = total_diff
  

  context['referral_his_income'] = round(Rewards_Reward,7)
  context['Withdraw_referral'] = round(sum_amount_referral,7)
  context['total_reff'] = round(total_ref_reward,7)
  context['Referral_diff'] = round(total_reff_diff,7)
  context['referral_income'] = wallet.referalincome


  return render(request,'trade_admin_auth/list_user_update.html',context)


class HistoryManagementTable(TemplateView):
  template_name = "trade_admin_auth/history_table.html"

  def get_context_data(self, **kwargs):
    context = super(HistoryManagementTable, self).get_context_data(**kwargs)
    p_key = self.kwargs['pk']
    context["p_key"] = p_key
    try:
      user_obj = User_Management.objects.get(id = p_key)
    except:
      user_obj = ""

    try:
      p_no = self.request.GET['pageno']
    except:
      p_no=1
    try:
      p_no1 = self.request.GET['pageno1']
    except:
      p_no1=1 
    try:
      p_no2 = self.request.GET['pageno2']
    except:
      p_no2=1
    try:
      p_no3 = self.request.GET['pageno3']
    except:
      p_no3=1
    try:
      p_no4 = self.request.GET['pageno4']
    except:
      p_no4=1   
    try:
      p_no5 = self.request.GET['pageno5']
    except:
      p_no5=1 
    try:
      p_no6 = self.request.GET['pageno6']
    except:
      p_no6=1   
    try:
      p_no7 = self.request.GET['pageno7']
    except:
      p_no7=1   

    context['p_no'] = p_no
    context['p_no1'] = p_no1
    context['p_no2'] = p_no2
    context['p_no3'] = p_no3
    context['p_no4'] = p_no4
    context['p_no5'] = p_no5
    context['p_no6'] = p_no6
    context['p_no7'] = p_no7

    try:
      s_step = self.request.GET['steps']
    except:
      s_step = ""

    

    s_usr = 0
    s_count = 0
    s_dict_users = {}
    s_start_page = self.request.GET.get('pageno', 1)
    s_end_value = int(s_start_page) * 5
    s_start_value = int(s_end_value) - 4
    
    if s_step:
      obj_step_hist = Steps_history.objects.filter(user_id = p_key).filter(steps__icontains = s_step).order_by('-id')
      for i in obj_step_hist:
        
        s_usr = s_usr + 1
        s_list_usr = {}
        if s_start_value <= s_usr <= s_end_value:
          s_count = s_count + 1
          s_list_usr["username"] = str(i.user.Name)
          s_list_usr["steps"] = (i.steps)
          s_list_usr["date"] = (str(i.created_on))
          s_list_usr["pageno"] = s_start_page
          s_list_usr["sno"] = s_usr
          s_dict_users[s_count] = s_list_usr
    else:
      obj_step_hist = Steps_history.objects.filter(user_id = p_key).order_by('-id')
      for i in obj_step_hist:
      
        s_usr = s_usr + 1
        s_list_usr = {}
        if s_start_value <= s_usr <= s_end_value:
          s_count = s_count + 1
          s_list_usr["username"] = str(i.user.Name)
          s_list_usr["steps"] = (i.steps)
          s_list_usr["date"] = (str(i.created_on))
          s_list_usr["pageno"] = s_start_page
          s_list_usr["sno"] = s_usr
          s_dict_users[s_count] = s_list_usr

    try:
      tot_step_user_qs = obj_step_hist
    except:
      tot_step_user_qs = ""
    w_page = self.request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_step_user_qs, 5)
    
    try:
        step_hist_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        step_hist_qs =w_paginator.page(1)
    except EmptyPage:
        step_hist_qs = w_paginator.page(w_paginator.num_pages)
    
    
    context['step_hist_qs'] = step_hist_qs
    context["s_endpage"] = step_hist_qs.number+1
    context["s_startpage"] = step_hist_qs.number-1
    context['s_start_value'] = step_hist_qs.start_index()
    context['s_end_value'] = step_hist_qs.end_index()
    context['s_usr_count'] = obj_step_hist.count()
    context["s_dict_users"] = json.dumps(s_dict_users)



    try:
      r_step = self.request.GET['r_steps']
    except:
      r_step = ""

    r_usr = 0
    r_count = 0
    r_dict_users = {}
    r_start_page = self.request.GET.get('pageno1', 1)
    r_end_value = int(r_start_page) * 5
    r_start_value = int(r_end_value) - 4
    if r_step:
      obj_rew_hist = Reward_History.objects.filter(user_id = p_key).filter(steps__icontains = r_step).order_by('-id')
      for i in obj_rew_hist:
        r_usr = r_usr + 1
        r_list_usr = {}
        if r_start_value <= r_usr <= r_end_value:
          r_count = r_count + 1
          r_list_usr["username"] = str(i.user.Name)
          r_list_usr["steps"] = (i.steps)
          r_list_usr["Reward"] = str(i.Reward)
          r_list_usr["date"] = (str(i.created_on))
          r_list_usr["claim_date"] = (str(i.modified_on))
          r_list_usr["pageno"] = r_start_page
          r_list_usr["sno"] = r_usr
          r_dict_users[r_count] = r_list_usr
    else:
      obj_rew_hist = Reward_History.objects.filter(user_id = p_key).order_by('-id')
      for i in obj_rew_hist:
        r_usr = r_usr + 1
        r_list_usr = {}
        if r_start_value <= r_usr <= r_end_value:
          r_count = r_count + 1
          r_list_usr["username"] = str(i.user.Name)
          r_list_usr["steps"] = (i.steps)
          r_list_usr["Reward"] = str(i.Reward)
          r_list_usr["date"] = (str(i.created_on))
          r_list_usr["claim_date"] = (str(i.modified_on))
          r_list_usr["pageno"] = r_start_page
          r_list_usr["sno"] = r_usr
          r_dict_users[r_count] = r_list_usr
    try:
      tot_rew_user_qs = obj_rew_hist
    except:
      tot_rew_user_qs = ""
    w_page_1 = self.request.GET.get('pageno1', 1)
    w_paginator_1 = Paginator(tot_rew_user_qs, 5)
    try:
        rew_hist_qs = w_paginator_1.page(w_page_1)
    except PageNotAnInteger:
        rew_hist_qs =w_paginator_1.page(1)
    except EmptyPage:
        rew_hist_qs = w_paginator_1.page(w_paginator_1.num_pages)

    context['rew_hist_qs'] = rew_hist_qs
    context["r_endpage"] = rew_hist_qs.number+1
    context["r_startpage"] = rew_hist_qs.number-1
    context['r_start_value'] = rew_hist_qs.start_index()
    context['r_end_value'] = rew_hist_qs.end_index()
    context['r_usr_count'] = obj_rew_hist.count()
    context["r_dict_users"] = json.dumps(r_dict_users)

    pre_usr = 0
    pre_count = 0
    pre_dict_users = {}
    pre_start_page = self.request.GET.get('pageno', 1)
    pre_end_value = int(pre_start_page) * 5
    pre_start_value = int(pre_end_value) - 4
    
    obj_pre_hist = premium_wallet_deposit.objects.filter(user = p_key,type="User Create").order_by('-id')
    for i in obj_pre_hist: 
      pre_usr = pre_usr + 1
      pre_list_usr = {}
      if pre_start_value <= pre_usr <= pre_end_value:
        pre_count = pre_count + 1
        pre_list_usr["username"] = str(user_obj.Name)
        pre_list_usr["create_type"] = (i.create_type)
        pre_list_usr["steps"] = (i.Amount_USDT)
        pre_list_usr["jw"] = (i.Amount_JW)
        pre_list_usr["Hash"] = (i.Hash)
        pre_list_usr["date"] = (str(i.created_on))
        pre_list_usr["pageno"] = pre_start_page
        pre_list_usr["sno"] = pre_usr
        pre_dict_users[pre_count] = pre_list_usr
    try:
      tot_step_user_qs = obj_pre_hist
    except:
      tot_step_user_qs = ""
    w_page = self.request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_step_user_qs, 5)
    
    try:
        step_hist_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        step_hist_qs =w_paginator.page(1)
    except EmptyPage:
        step_hist_qs = w_paginator.page(w_paginator.num_pages)
    
    
    context['step_hist_qs'] = step_hist_qs
    context["pre_endpage"] = step_hist_qs.number+1
    context["pre_startpage"] = step_hist_qs.number-1
    context['pre_start_value'] = step_hist_qs.start_index()
    context['pre_end_value'] = step_hist_qs.end_index()
    context['pre_usr_count'] = obj_pre_hist.count()
    context["pre_dict_users"] = json.dumps(pre_dict_users)


    pre_r_usr = 0
    pre_r_count = 0
    pre_req_dict_users = {}
    pre_r_start_page = self.request.GET.get('pageno1', 1)
    pre_r_end_value = int(pre_r_start_page) * 5
    pre_r_start_value = int(pre_r_end_value) - 4
    obj_rew_hist = premium_wallet_deposit.objects.filter(user = p_key).exclude(type="User Create").order_by('-created_on')
    for i in obj_rew_hist:
      pre_r_usr = pre_r_usr + 1
      r_list_usr = {}
      if pre_r_start_value <= pre_r_usr <= pre_r_end_value:
        pre_r_count = pre_r_count + 1
        r_list_usr["username"] = str(user_obj.Name)
        r_list_usr["steps"] = (i.type)
        r_list_usr["Hash"] = (i.Hash)
        r_list_usr["Reward"] = str(i.Amount_USDT)
        r_list_usr["date"] = (str(i.created_on))
        r_list_usr["pageno"] = pre_r_start_page
        r_list_usr["sno"] = pre_r_usr
        pre_req_dict_users[pre_r_count] = r_list_usr
    try:
      tot_rew_user_qs = obj_rew_hist
    except:
      tot_rew_user_qs = ""
    w_page_1 = self.request.GET.get('pageno1', 1)
    w_paginator_1 = Paginator(tot_rew_user_qs, 5)
    try:
        rew_hist_qs = w_paginator_1.page(w_page_1)
    except PageNotAnInteger:
        rew_hist_qs =w_paginator_1.page(1)
    except EmptyPage:
        rew_hist_qs = w_paginator_1.page(w_paginator_1.num_pages)

    context['rew_hist_qs'] = rew_hist_qs
    context["pre_r_endpage"] = rew_hist_qs.number+1
    context["pre_r_startpage"] = rew_hist_qs.number-1
    context['pre_r_start_value'] = rew_hist_qs.start_index()
    context['pre_r_end_value'] = rew_hist_qs.end_index()
    context['pre_r_usr_count'] = obj_rew_hist.count()
    context["pre_req_dict_users"] = json.dumps(pre_req_dict_users)

    try:
      two_x_step = self.request.GET['tx_steps']
    except:
      two_x_step = ""

    tx_usr = 0
    tx_count = 0
    tx_dict_users = {}
    tx_start_page = self.request.GET.get('pageno2', 1)
    tx_end_value = int(tx_start_page) * 5
    tx_start_value = int(tx_end_value) - 4
    if two_x_step:
      obj_two_x_hist = User_2x_Boost.objects.filter(userid_id = p_key).filter(user_step_count__icontains = two_x_step).order_by('-id')
      for i in obj_two_x_hist:
        tx_usr = tx_usr + 1
        tx_list_usr = {}
        if tx_start_value <= tx_usr <= tx_end_value:
          tx_count = tx_count + 1
          tx_list_usr["username"] = str(i.userid.Name)
          tx_list_usr["steps"] = (i.user_step_count)
          tx_list_usr["Reward"] = str(i.reward_per_step)
          tx_list_usr["date"] = (str(i.created_on))
          tx_list_usr["pageno"] = tx_start_page
          tx_list_usr["sno"] = tx_usr
          tx_dict_users[tx_count] = tx_list_usr
    else:
      obj_two_x_hist = User_2x_Boost.objects.filter(userid_id = p_key).order_by('-id')
      for i in obj_two_x_hist:
        tx_usr = tx_usr + 1
        tx_list_usr = {}
        if tx_start_value <= tx_usr <= tx_end_value:
          tx_count = tx_count + 1
          tx_list_usr["username"] = str(i.userid.Name)
          tx_list_usr["steps"] = (i.user_step_count)
          tx_list_usr["Reward"] = str(i.reward_per_step)
          tx_list_usr["date"] = (str(i.created_on))
          tx_list_usr["pageno"] = tx_start_page
          tx_list_usr["sno"] = tx_usr
          tx_dict_users[tx_count] = tx_list_usr
    try:
      tot_tx_user_qs = obj_two_x_hist
    except:
      tot_tx_user_qs = ""
    w_page_2 = self.request.GET.get('pageno2', 1)
    w_paginator_2 = Paginator(tot_tx_user_qs, 5)
    try:
        two_x_hist_qs = w_paginator_2.page(w_page_2)
    except PageNotAnInteger:
        two_x_hist_qs =w_paginator_2.page(1)
    except EmptyPage:
        two_x_hist_qs = w_paginator_2.page(w_paginator_2.num_pages)

    context['two_x_hist_qs'] = two_x_hist_qs
    context["tx_endpage"] = two_x_hist_qs.number+1
    context["tx_startpage"] = two_x_hist_qs.number-1
    context['tx_start_value'] = two_x_hist_qs.start_index()
    context['tx_end_value'] = two_x_hist_qs.end_index()
    context['tx_usr_count'] = obj_two_x_hist.count()
    context["tx_dict_users"] = json.dumps(tx_dict_users)



    try:
      buy_plan_name = self.request.GET['plan_name']
    except:
      buy_plan_name = ""

    plan_usr = 0
    plan_count = 0
    plan_dict_users = {}
    plan_start_page = self.request.GET.get('pageno3', 1)
    plan_end_value = int(plan_start_page) * 5
    plan_start_value = int(plan_end_value) - 4
    Comp_User = boat_trade_purchase_history.objects.filter(user_id=p_key).last()
    # Handle case where no trade purchase history exists
    if Comp_User is None:
        trade_status = "1"
    else: 
        trade_status = str(Comp_User.status)
    if buy_plan_name:
      obj_plan_hist = plan_purchase_history.objects.filter(user_id = p_key).filter(plan_id__plan_name = buy_plan_name).order_by('-id')
      for i in obj_plan_hist:
        plan_usr = plan_usr + 1
        plan_list_usr = {}
        if plan_start_value <= plan_usr <= plan_end_value:
          plan_count = plan_count + 1
          plan_list_usr["id"] = str(p_key)
          plan_list_usr["username"] = str(i.user.Name)
          plan_list_usr["plan"] = (i.plan_id.plan_name)
          plan_list_usr["plan_amt"] = int(i.purchase_amount)
          plan_list_usr["price"] = str(user_obj.fixed_status)
          plan_list_usr["USDT_JW"] = str(user_obj.USDT_status)
          plan_list_usr["PlanBwa"] = str(user_obj.PlanBwa)
          plan_list_usr["Bot_status"] = str(user_obj.boat_status)
          plan_list_usr["xvalue"] = str(user_obj.xvalue)
          plan_list_usr["Trade_status"] = trade_status
          plan_list_usr["start_date"] = (str(user_obj.plan_start_date))
          plan_list_usr["end_date"] = (str(user_obj.plan_end_date))
          plan_list_usr["wallet_type"] = (i.user_wallet_type)
          plan_list_usr["health_max"] = (str(user_obj.Health_Withdraw_max_value))
          plan_list_usr["health_min"] = (str(user_obj.Health_Withdraw_min_value))
          plan_list_usr["referral_max"] = (str(user_obj.Referral_Withdraw_max_value))
          plan_list_usr["referral_min"] = (str(user_obj.Referral_Withdraw_min_value))
          plan_list_usr["buy_type"] = (i.buy_type)
          plan_list_usr["hash"] = (str(i.User_plan_validation))
          plan_list_usr["pageno"] = plan_start_page
          plan_list_usr["sno"] = plan_usr
          plan_dict_users[plan_count] = plan_list_usr
    else:
      obj_plan_hist = plan_purchase_history.objects.filter(user_id = p_key).order_by('-id')
      for i in obj_plan_hist:
        plan_usr = plan_usr + 1
        plan_list_usr = {}
        if plan_start_value <= plan_usr <= plan_end_value:
          plan_count = plan_count + 1
          plan_list_usr["id"] = str(p_key)
          plan_list_usr["username"] = str(i.user.Name)
          plan_list_usr["plan"] = (i.plan_id.plan_name)
          plan_list_usr["plan_amt"] = int(i.purchase_amount)
          plan_list_usr["price"] = str(user_obj.fixed_status)
          plan_list_usr["USDT_JW"] = str(user_obj.USDT_status)
          plan_list_usr["PlanBwa"] = str(user_obj.PlanBwa)
          plan_list_usr["Bot_status"] = str(user_obj.boat_status)
          plan_list_usr["xvalue"] = str(user_obj.xvalue)
          plan_list_usr["Trade_status"] = trade_status
          plan_list_usr["start_date"] = (str(user_obj.plan_start_date))
          plan_list_usr["end_date"] = (str(user_obj.plan_end_date))
          plan_list_usr["wallet_type"] = (i.user_wallet_type)
          plan_list_usr["health_max"] = (str(user_obj.Health_Withdraw_max_value))
          plan_list_usr["health_min"] = (str(user_obj.Health_Withdraw_min_value))
          plan_list_usr["referral_max"] = (str(user_obj.Referral_Withdraw_max_value))
          plan_list_usr["referral_min"] = (str(user_obj.Referral_Withdraw_min_value))
          plan_list_usr["buy_type"] = (i.buy_type)
          plan_list_usr["hash"] = (str(i.User_plan_validation))
          plan_list_usr["pageno"] = plan_start_page
          plan_list_usr["sno"] = plan_usr
          plan_dict_users[plan_count] = plan_list_usr
    try:
      tot_plan_user_qs = obj_plan_hist
    except:
      tot_plan_user_qs = ""
    w_page_3 = self.request.GET.get('pageno3', 1)
    w_paginator_3 = Paginator(tot_plan_user_qs, 5)
    try:
        plan_hist_qs = w_paginator_3.page(w_page_3)
    except PageNotAnInteger:
        plan_hist_qs =w_paginator_3.page(1)
    except EmptyPage:
        plan_hist_qs = w_paginator_3.page(w_paginator_3.num_pages)\

    context['plan_hist_qs'] = plan_hist_qs
    context["plan_endpage"] = plan_hist_qs.number+1
    context["plan_startpage"] = plan_hist_qs.number-1
    context['plan_start_value'] = plan_hist_qs.start_index()
    context['plan_end_value'] = plan_hist_qs.end_index()
    context['plan_usr_count'] = obj_plan_hist.count()
    context["plan_dict_users"] = json.dumps(plan_dict_users)


    try:
      usr_addrs = self.request.GET['address']
    except:
      usr_addrs = ""

    try:
      status = self.request.GET['status']
     
      if status == 'Active':
       
        status = 0
      if status == 'Completed':
        status = 1
      if status == 'Cancelled':
        status = 2
    except:
      status = ""

    try:
      date = self.request.GET['date']
    except:
      date = ""

    withdraw_usr = 0
    withdraw_count = 0
    withdraw_dict_users = {}
    withdraw_start_page = self.request.GET.get('pageno4', 1)
    withdraw_end_value = int(withdraw_start_page) * 5
    withdraw_start_value = int(withdraw_end_value) - 4
    if usr_addrs and status and date:
      obj_withdraw_hist = Withdraw.objects.filter(userid_id = p_key).filter(Q(Address__icontains = usr_addrs) and Q(status__icontains = status) and Q(created_on__date__icontains = date)).exclude(Wallet_type__in=[ 'Trade_Referral_wallet', 'Bot_Referral_wallet','trade_withdraw_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    elif usr_addrs:
      obj_withdraw_hist = Withdraw.objects.filter(userid_id = p_key).filter(Address__icontains = usr_addrs).exclude(Wallet_type__in=[ 'Trade_Referral_wallet', 'Bot_Referral_wallet','trade_withdraw_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    elif date:
      obj_withdraw_hist = Withdraw.objects.filter(userid_id = p_key).filter(created_on__date__icontains = date).exclude(Wallet_type__in=[ 'Trade_Referral_wallet', 'Bot_Referral_wallet','trade_withdraw_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    elif status:
      obj_withdraw_hist = Withdraw.objects.filter(userid_id = p_key).filter(status__icontains = status).exclude(Wallet_type__in=[ 'Trade_Referral_wallet', 'Bot_Referral_wallet','trade_withdraw_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    else:
      obj_withdraw_hist = Withdraw.objects.filter(userid_id = p_key).exclude(Wallet_type__in=[ 'Trade_Referral_wallet', 'Bot_Referral_wallet','trade_withdraw_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    try:
      tot_withdraw_user_qs = obj_withdraw_hist
    except:
      tot_withdraw_user_qs = ""
    w_page_4 = self.request.GET.get('pageno4', 1)
    w_paginator_4 = Paginator(tot_withdraw_user_qs, 5)
    try:
        withdraw_hist_qs = w_paginator_4.page(w_page_4)
    except PageNotAnInteger:
        withdraw_hist_qs =w_paginator_4.page(1)
    except EmptyPage:
        withdraw_hist_qs = w_paginator_4.page(w_paginator_4.num_pages)

    context['withdraw_hist_qs'] = withdraw_hist_qs
    context["withdraw_endpage"] = withdraw_hist_qs.number+1
    context["withdraw_startpage"] = withdraw_hist_qs.number-1
    context['withdraw_start_value'] = withdraw_hist_qs.start_index()
    context['withdraw_end_value'] = withdraw_hist_qs.end_index()
    context['withdraw_usr_count'] = obj_withdraw_hist.count()
    context["withdraw_dict_users"] = json.dumps(withdraw_dict_users)

     
    try:
      ref_user = self.request.GET['name']
    except:
      ref_user = ""


    ref_usr = 0
    ref_count = 0
    ref_dict_users = {}
    ref_start_page = self.request.GET.get('pageno5', 1)
    ref_end_value = int(ref_start_page) * 5
    ref_start_value = int(ref_end_value) - 4
    try:
      if ref_user:
        obj_ref_hist = Referral_reward_History.objects.filter(user_id = p_key).filter(referral_id__icontains = ref_user).order_by('-id')
        for i in obj_ref_hist:
          
          ref_usr = ref_usr + 1
          ref_list_usr = {}
          if ref_start_value <= ref_usr <= ref_end_value:
            ref_count = ref_count + 1
            # ref_list_usr["id"] = str(p_key)
            ref_list_usr["id"] = i.id
            ref_list_usr["username"] = str(i.user.Name)
            ref_list_usr["ref_id"] = i.referral_id
            ref_list_usr["reward_amt"] = i.reward
            ref_list_usr["date"] = (str(i.created_on))
            ref_list_usr["pageno"] = ref_start_page
            ref_list_usr["sno"] = ref_usr
            ref_dict_users[ref_count] = ref_list_usr
        
      else:
        obj_ref_hist = Referral_reward_History.objects.filter(user_id = p_key).order_by('-id')
        for i in obj_ref_hist:
          ref_usr = ref_usr + 1
          ref_list_usr = {}
          if ref_start_value <= ref_usr <= ref_end_value:
            ref_count = ref_count + 1
            ref_list_usr["id"] = i.id
            ref_list_usr["username"] = str(i.user.Name)
            ref_list_usr["ref_id"] = i.referral_id
            ref_list_usr["reward_amt"] = i.reward
            ref_list_usr["date"] = (str(i.created_on))
            ref_list_usr["pageno"] = ref_start_page
            ref_list_usr["sno"] = ref_usr
            ref_dict_users[ref_count] = ref_list_usr
        

      context['ref_usr_count'] = obj_ref_hist.count()
    except:
      obj_ref_hist = ""
      context['ref_usr_count'] = 0
    try:
      tot_ref_user_qs = obj_ref_hist
    except:
      tot_ref_user_qs = ""
    w_page_5 = self.request.GET.get('pageno5', 1)
    w_paginator_5 = Paginator(tot_ref_user_qs, 5)
    try:
        ref_hist_qs = w_paginator_5.page(w_page_5)
    except PageNotAnInteger:
        ref_hist_qs =w_paginator_5.page(1)
    except EmptyPage:
        ref_hist_qs = w_paginator_5.page(w_paginator_5.num_pages)

    context['ref_hist_qs'] = ref_hist_qs
    context["ref_endpage"] = ref_hist_qs.number+1
    context["ref_startpage"] = ref_hist_qs.number-1
    context['ref_start_value'] = ref_hist_qs.start_index()
    context['ref_end_value'] = ref_hist_qs.end_index()
    context["ref_dict_users"] = json.dumps(ref_dict_users)

    wall_usr = 0
    wall_count = 0
    wall_dict_users = {}
    wall_start_page = self.request.GET.get('pageno6', 1)
    wall_end_value = int(wall_start_page) * 5
    wall_start_value = int(wall_end_value) - 4
    try:
      obj_wall_hist = UserCashWallet.objects.filter(userid_id = p_key).order_by('-id')
      for i in obj_wall_hist:
        wall_usr = wall_usr + 1
        wall_list_usr = {}
        if wall_start_value <= wall_usr <= wall_end_value:
          wall_count = wall_count + 1
          wall_list_usr["username"] = str(i.userid.Name)
          if i.balanceone == 0.00000000:
            wall_list_usr["health_reward"] = int(i.balanceone)
          else:
            wall_list_usr["health_reward"] = str(i.balanceone)
          if i.referalincome == 0.00000000:
            wall_list_usr["ref_reward"] = int(i.referalincome)
          else:
            wall_list_usr["ref_reward"] = str(i.referalincome)
          if i.Premiumwallet == 0.00000000:
            wall_list_usr["pre_reward"] = int(i.Premiumwallet)
          else:
            wall_list_usr["pre_reward"] = str(i.Premiumwallet)
          wall_list_usr["pageno"] = wall_start_page
          wall_list_usr["sno"] = wall_usr
          wall_dict_users[wall_count] = wall_list_usr
    except:
      obj_wall_hist = ""
    try:
      tot_wall_user_qs = obj_wall_hist
    except:
      tot_wall_user_qs = ""
    w_page_6 = self.request.GET.get('pageno6', 1)
    w_paginator_6 = Paginator(tot_wall_user_qs, 5)
    try:
        wall_hist_qs = w_paginator_6.page(w_page_6)
    except PageNotAnInteger:
        wall_hist_qs =w_paginator_6.page(1)
    except EmptyPage:
        wall_hist_qs = w_paginator_6.page(w_paginator_6.num_pages)

    context['wall_hist_qs'] = wall_hist_qs
    context["wall_endpage"] = wall_hist_qs.number+1
    context["wall_startpage"] = wall_hist_qs.number-1
    context['wall_start_value'] = wall_hist_qs.start_index()
    context['wall_end_value'] = wall_hist_qs.end_index()
    context['wall_usr_count'] = obj_wall_hist.count()
    context["wall_dict_users"] = json.dumps(wall_dict_users)


    login_usr = 0
    login_count = 0
    login_dict_users = {}
    login_start_page = self.request.GET.get('pageno7', 1)
    login_end_value = int(login_start_page) * 5
    login_start_value = int(login_end_value) - 4
    try:
      obj_login_hist = LoginHistory.objects.filter(user_id = p_key).order_by('-created_on')
      for i in obj_login_hist:
        login_usr = login_usr + 1
        login_list_usr = {}
        if login_start_value <= login_usr <= login_end_value:
          login_count = login_count + 1
          login_list_usr["username"] = str(i.user.Name)
          login_list_usr["created_on"] = str(i.created_on)
          login_list_usr["modified_on"] = str(i.modified_on)
          login_list_usr["pageno"] = login_start_page
          login_list_usr["sno"] = login_usr
          login_dict_users[login_count] = login_list_usr
    except:
      obj_login_hist = ""
    try:
      tot_login_user_qs = obj_login_hist
    except:
      tot_login_user_qs = ""
    w_page_7 = self.request.GET.get('pageno7', 1)
    w_paginator_7 = Paginator(tot_login_user_qs, 5)
    try:
        login_hist_qs = w_paginator_7.page(w_page_7)
    except PageNotAnInteger:
        login_hist_qs =w_paginator_7.page(1)
    except EmptyPage:
        login_hist_qs = w_paginator_7.page(w_paginator_7.num_pages)

    context['login_hist_qs'] = login_hist_qs
    context["login_endpage"] = login_hist_qs.number+1
    context["login_startpage"] = login_hist_qs.number-1
    context['login_start_value'] = login_hist_qs.start_index()
    context['login_end_value'] = login_hist_qs.end_index()
    context['login_usr_count'] = obj_login_hist.count()
    context["login_dict_users"] = json.dumps(login_dict_users)

    
    context['Title'] = 'Users History Table'
    context["Btn_url"] = "trade_admin_auth:List_User_Management"
    return context


  @method_decorator(check_group_icon_menu("History")) 
  def dispatch(self, *args, **kwargs):
    return super(HistoryManagementTable, self).dispatch(*args, **kwargs)





class TradeHistoryManagementTable(TemplateView):
  template_name = "trade_admin_auth/trade_history_table.html"

  def get_context_data(self, **kwargs):
    context = super(TradeHistoryManagementTable, self).get_context_data(**kwargs)
    p_key = self.kwargs['pk']
    context["p_key"] = p_key
    try:
      user_obj = User_Management.objects.get(id = p_key)
    except:
      user_obj = ""

    try:
      p_no = self.request.GET['pageno']
    except:
      p_no=1
    try:
      p_no1 = self.request.GET['pageno1']
    except:
      p_no1=1 
    try:
      p_no2 = self.request.GET['pageno2']
    except:
      p_no2=1
    try:
      p_no3 = self.request.GET['pageno3']
    except:
      p_no3=1
    try:
      p_no4 = self.request.GET['pageno4']
    except:
      p_no4=1   
    try:
      p_no5 = self.request.GET['pageno5']
    except:
      p_no5=1 
    try:
      p_no6 = self.request.GET['pageno6']
    except:
      p_no6=1   
    try:
      p_no7 = self.request.GET['pageno7']
    except:
      p_no7=1   

    context['p_no'] = p_no
    context['p_no1'] = p_no1
    context['p_no2'] = p_no2
    context['p_no3'] = p_no3
    context['p_no4'] = p_no4
    context['p_no5'] = p_no5
    context['p_no6'] = p_no6
    context['p_no7'] = p_no7

    try:
      s_step = self.request.GET['steps']
    except:
      s_step = ""

    

    s_usr = 0
    s_count = 0
    s_dict_users = {}
    s_start_page = self.request.GET.get('pageno', 1)
    s_end_value = int(s_start_page) * 5
    s_start_value = int(s_end_value) - 4
    
    if s_step:
      obj_step_hist = Steps_history.objects.filter(user_id = p_key).filter(steps__icontains = s_step).order_by('-id')
      for i in obj_step_hist:
        
        s_usr = s_usr + 1
        s_list_usr = {}
        if s_start_value <= s_usr <= s_end_value:
          s_count = s_count + 1
          s_list_usr["username"] = str(i.user.Name)
          s_list_usr["steps"] = (i.steps)
          s_list_usr["date"] = (str(i.created_on))
          s_list_usr["pageno"] = s_start_page
          s_list_usr["sno"] = s_usr
          s_dict_users[s_count] = s_list_usr
    else:
      obj_step_hist = Steps_history.objects.filter(user_id = p_key).order_by('-id')
      for i in obj_step_hist:
      
        s_usr = s_usr + 1
        s_list_usr = {}
        if s_start_value <= s_usr <= s_end_value:
          s_count = s_count + 1
          s_list_usr["username"] = str(i.user.Name)
          s_list_usr["steps"] = (i.steps)
          s_list_usr["date"] = (str(i.created_on))
          s_list_usr["pageno"] = s_start_page
          s_list_usr["sno"] = s_usr
          s_dict_users[s_count] = s_list_usr

    try:
      tot_step_user_qs = obj_step_hist
    except:
      tot_step_user_qs = ""
    w_page = self.request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_step_user_qs, 5)
    
    try:
        step_hist_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        step_hist_qs =w_paginator.page(1)
    except EmptyPage:
        step_hist_qs = w_paginator.page(w_paginator.num_pages)
    
    
    context['step_hist_qs'] = step_hist_qs
    context["s_endpage"] = step_hist_qs.number+1
    context["s_startpage"] = step_hist_qs.number-1
    context['s_start_value'] = step_hist_qs.start_index()
    context['s_end_value'] = step_hist_qs.end_index()
    context['s_usr_count'] = obj_step_hist.count()
    context["s_dict_users"] = json.dumps(s_dict_users)



    try:
      r_step = self.request.GET['r_steps']
    except:
      r_step = ""

    r_usr = 0
    r_count = 0
    r_dict_users = {}
    r_start_page = self.request.GET.get('pageno1', 1)
    r_end_value = int(r_start_page) * 5
    r_start_value = int(r_end_value) - 4
    if r_step:
      obj_rew_hist = Reward_History.objects.filter(user_id = p_key).filter(steps__icontains = r_step).order_by('-id')
      for i in obj_rew_hist:
        r_usr = r_usr + 1
        r_list_usr = {}
        if r_start_value <= r_usr <= r_end_value:
          r_count = r_count + 1
          r_list_usr["username"] = str(i.user.Name)
          r_list_usr["steps"] = (i.steps)
          r_list_usr["Reward"] = str(i.Reward)
          r_list_usr["date"] = (str(i.created_on))
          r_list_usr["claim_date"] = (str(i.modified_on))
          r_list_usr["pageno"] = r_start_page
          r_list_usr["sno"] = r_usr
          r_dict_users[r_count] = r_list_usr
    else:
      obj_rew_hist = Reward_History.objects.filter(user_id = p_key).order_by('-id')
      for i in obj_rew_hist:
        r_usr = r_usr + 1
        r_list_usr = {}
        if r_start_value <= r_usr <= r_end_value:
          r_count = r_count + 1
          r_list_usr["username"] = str(i.user.Name)
          r_list_usr["steps"] = (i.steps)
          r_list_usr["Reward"] = str(i.Reward)
          r_list_usr["date"] = (str(i.created_on))
          r_list_usr["claim_date"] = (str(i.modified_on))
          r_list_usr["pageno"] = r_start_page
          r_list_usr["sno"] = r_usr
          r_dict_users[r_count] = r_list_usr
    try:
      tot_rew_user_qs = obj_rew_hist
    except:
      tot_rew_user_qs = ""
    w_page_1 = self.request.GET.get('pageno1', 1)
    w_paginator_1 = Paginator(tot_rew_user_qs, 5)
    try:
        rew_hist_qs = w_paginator_1.page(w_page_1)
    except PageNotAnInteger:
        rew_hist_qs =w_paginator_1.page(1)
    except EmptyPage:
        rew_hist_qs = w_paginator_1.page(w_paginator_1.num_pages)

    context['rew_hist_qs'] = rew_hist_qs
    context["r_endpage"] = rew_hist_qs.number+1
    context["r_startpage"] = rew_hist_qs.number-1
    context['r_start_value'] = rew_hist_qs.start_index()
    context['r_end_value'] = rew_hist_qs.end_index()
    context['r_usr_count'] = obj_rew_hist.count()
    context["r_dict_users"] = json.dumps(r_dict_users)

    pre_usr = 0
    pre_count = 0
    pre_dict_users = {}
    pre_start_page = self.request.GET.get('pageno', 1)
    pre_end_value = int(pre_start_page) * 5
    pre_start_value = int(pre_end_value) - 4
    
    obj_pre_hist = Boat_wallet.objects.filter(user = p_key,type="User Create").order_by('-id')
    for i in obj_pre_hist: 
      pre_usr = pre_usr + 1
      pre_list_usr = {}
      if pre_start_value <= pre_usr <= pre_end_value:
        pre_count = pre_count + 1
        pre_list_usr["username"] = str(user_obj.Name)
        pre_list_usr["create_type"] = (i.create_type)
        pre_list_usr["steps"] = (i.Amount_USDT)
        pre_list_usr["jw"] = (i.Amount_JW)
        pre_list_usr["Hash"] = (i.Hash)
        pre_list_usr["date"] = (str(i.created_on))
        pre_list_usr["pageno"] = pre_start_page
        pre_list_usr["sno"] = pre_usr
        pre_dict_users[pre_count] = pre_list_usr
    try:
      tot_step_user_qs = obj_pre_hist
    except:
      tot_step_user_qs = ""
    w_page = self.request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_step_user_qs, 5)
    
    try:
        step_hist_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        step_hist_qs =w_paginator.page(1)
    except EmptyPage:
        step_hist_qs = w_paginator.page(w_paginator.num_pages)
    
    
    context['step_hist_qs'] = step_hist_qs
    context["pre_endpage"] = step_hist_qs.number+1
    context["pre_startpage"] = step_hist_qs.number-1
    context['pre_start_value'] = step_hist_qs.start_index()
    context['pre_end_value'] = step_hist_qs.end_index()
    context['pre_usr_count'] = obj_pre_hist.count()
    context["pre_dict_users"] = json.dumps(pre_dict_users)


    pre_r_usr = 0
    pre_r_count = 0
    pre_req_dict_users = {}
    pre_r_start_page = self.request.GET.get('pageno1', 1)
    pre_r_end_value = int(pre_r_start_page) * 5
    pre_r_start_value = int(pre_r_end_value) - 4
    obj_rew_hist = Boat_wallet.objects.filter(user = p_key).exclude(type="User Create").order_by('-created_on')
    for i in obj_rew_hist:
      pre_r_usr = pre_r_usr + 1
      r_list_usr = {}
      if pre_r_start_value <= pre_r_usr <= pre_r_end_value:
        pre_r_count = pre_r_count + 1
        r_list_usr["username"] = str(user_obj.Name)
        r_list_usr["steps"] = (i.type)
        r_list_usr["Reward"] = str(i.Amount_USDT)
        r_list_usr["date"] = (str(i.created_on))
        r_list_usr["pageno"] = pre_r_start_page
        r_list_usr["sno"] = pre_r_usr
        pre_req_dict_users[pre_r_count] = r_list_usr
    try:
      tot_rew_user_qs = obj_rew_hist
    except:
      tot_rew_user_qs = ""
    w_page_1 = self.request.GET.get('pageno1', 1)
    w_paginator_1 = Paginator(tot_rew_user_qs, 5)
    try:
        rew_hist_qs = w_paginator_1.page(w_page_1)
    except PageNotAnInteger:
        rew_hist_qs =w_paginator_1.page(1)
    except EmptyPage:
        rew_hist_qs = w_paginator_1.page(w_paginator_1.num_pages)

    context['rew_hist_qs'] = rew_hist_qs
    context["pre_r_endpage"] = rew_hist_qs.number+1
    context["pre_r_startpage"] = rew_hist_qs.number-1
    context['pre_r_start_value'] = rew_hist_qs.start_index()
    context['pre_r_end_value'] = rew_hist_qs.end_index()
    context['pre_r_usr_count'] = obj_rew_hist.count()
    context["pre_req_dict_users"] = json.dumps(pre_req_dict_users)

    try:
      two_x_step = self.request.GET['tx_steps']
    except:
      two_x_step = ""

    tx_usr = 0
    tx_count = 0
    tx_dict_users = {}
    tx_start_page = self.request.GET.get('pageno2', 1)
    tx_end_value = int(tx_start_page) * 5
    tx_start_value = int(tx_end_value) - 4
    if two_x_step:
      obj_two_x_hist = User_2x_Boost.objects.filter(userid_id = p_key).filter(user_step_count__icontains = two_x_step).order_by('-id')
      for i in obj_two_x_hist:
        tx_usr = tx_usr + 1
        tx_list_usr = {}
        if tx_start_value <= tx_usr <= tx_end_value:
          tx_count = tx_count + 1
          tx_list_usr["username"] = str(i.userid.Name)
          tx_list_usr["steps"] = (i.user_step_count)
          tx_list_usr["Reward"] = str(i.reward_per_step)
          tx_list_usr["date"] = (str(i.created_on))
          tx_list_usr["pageno"] = tx_start_page
          tx_list_usr["sno"] = tx_usr
          tx_dict_users[tx_count] = tx_list_usr
    else:
      obj_two_x_hist = User_2x_Boost.objects.filter(userid_id = p_key).order_by('-id')
      for i in obj_two_x_hist:
        tx_usr = tx_usr + 1
        tx_list_usr = {}
        if tx_start_value <= tx_usr <= tx_end_value:
          tx_count = tx_count + 1
          tx_list_usr["username"] = str(i.userid.Name)
          tx_list_usr["steps"] = (i.user_step_count)
          tx_list_usr["Reward"] = str(i.reward_per_step)
          tx_list_usr["date"] = (str(i.created_on))
          tx_list_usr["pageno"] = tx_start_page
          tx_list_usr["sno"] = tx_usr
          tx_dict_users[tx_count] = tx_list_usr
    try:
      tot_tx_user_qs = obj_two_x_hist
    except:
      tot_tx_user_qs = ""
    w_page_2 = self.request.GET.get('pageno2', 1)
    w_paginator_2 = Paginator(tot_tx_user_qs, 5)
    try:
        two_x_hist_qs = w_paginator_2.page(w_page_2)
    except PageNotAnInteger:
        two_x_hist_qs =w_paginator_2.page(1)
    except EmptyPage:
        two_x_hist_qs = w_paginator_2.page(w_paginator_2.num_pages)

    context['two_x_hist_qs'] = two_x_hist_qs
    context["tx_endpage"] = two_x_hist_qs.number+1
    context["tx_startpage"] = two_x_hist_qs.number-1
    context['tx_start_value'] = two_x_hist_qs.start_index()
    context['tx_end_value'] = two_x_hist_qs.end_index()
    context['tx_usr_count'] = obj_two_x_hist.count()
    context["tx_dict_users"] = json.dumps(tx_dict_users)



    try:
      buy_plan_name = self.request.GET['plan_name']
    except:
      buy_plan_name = ""

    plan_usr = 0
    plan_count = 0
    plan_dict_users = {}
    plan_start_page = self.request.GET.get('pageno3', 1)
    plan_end_value = int(plan_start_page) * 5
    plan_start_value = int(plan_end_value) - 4
    Comp = boat_trade_purchase_history.objects.filter(user_id = p_key).order_by('-id')
    if buy_plan_name:
      obj_plan_hist = boat_trade_purchase_history.objects.filter(user_id = p_key).order_by('-id')
      for i in obj_plan_hist:
        plan_usr = plan_usr + 1
        plan_list_usr = {}
        if plan_start_value <= plan_usr <= plan_end_value:
          plan_count = plan_count + 1
          plan_list_usr["id"] = str(p_key)
          plan_list_usr["username"] = str(i.user_id)
          plan_list_usr["plan"] = "TRADE"#int(i.purchase_amount)
          plan_list_usr["plan_amt"] = int(i.purchase_amount)
          plan_list_usr["start_date"] = (str(user_obj.created_on))
          # plan_list_usr["end_date"] = (str(user_obj.plan_end_date))
          plan_list_usr["wallet_type"] = (i.user_wallet_type)
          # plan_list_usr["health_max"] = (str(user_obj.Health_Withdraw_max_value))
          # plan_list_usr["health_min"] = (str(user_obj.Health_Withdraw_min_value))
          # plan_list_usr["referral_max"] = (str(user_obj.Referral_Withdraw_max_value))
          # plan_list_usr["referral_min"] = (str(user_obj.Referral_Withdraw_min_value))
          plan_list_usr["buy_type"] = (i.buy_type)
          plan_list_usr["TradeBwa"] = str(user_obj.TradeBwa)
          # plan_list_usr["hash"] = (str(i.User_plan_validation))
          plan_list_usr["pageno"] = plan_start_page
          plan_list_usr["sno"] = plan_usr
          plan_dict_users[plan_count] = plan_list_usr
    else:
      obj_plan_hist = boat_trade_purchase_history.objects.filter(user_id = p_key).order_by('-id')
      for i in obj_plan_hist:
        plan_usr = plan_usr + 1
        plan_list_usr = {}
        if plan_start_value <= plan_usr <= plan_end_value:
          plan_count = plan_count + 1
          plan_list_usr["id"] = str(p_key)
          plan_list_usr["username"] = str(i.user_id)
          plan_list_usr["plan"] = "TRADE"#int(i.purchase_amount)
          plan_list_usr["plan_amt"] = int(i.purchase_amount)
          # plan_list_usr["price"] = str(user_obj.fixed_status)
          plan_list_usr["start_date"] = (str(user_obj.created_on))
          # plan_list_usr["end_date"] = (str(user_obj.plan_end_date))
          plan_list_usr["wallet_type"] = (i.user_wallet_type)
          # plan_list_usr["health_max"] = (str(user_obj.Health_Withdraw_max_value))
          # plan_list_usr["health_min"] = (str(user_obj.Health_Withdraw_min_value))
          # plan_list_usr["referral_max"] = (str(user_obj.Referral_Withdraw_max_value))
          # plan_list_usr["referral_min"] = (str(user_obj.Referral_Withdraw_min_value))
          plan_list_usr["buy_type"] = (i.buy_type)
          plan_list_usr["TradeBwa"] = str(user_obj.TradeBwa)
          # plan_list_usr["hash"] = (str(i.User_plan_validation))
          plan_list_usr["pageno"] = plan_start_page
          plan_list_usr["sno"] = plan_usr
          plan_dict_users[plan_count] = plan_list_usr
    try:
      tot_plan_user_qs = obj_plan_hist
    except:
      tot_plan_user_qs = ""
    w_page_3 = self.request.GET.get('pageno3', 1)
    w_paginator_3 = Paginator(tot_plan_user_qs, 5)
    try:
        plan_hist_qs = w_paginator_3.page(w_page_3)
    except PageNotAnInteger:
        plan_hist_qs =w_paginator_3.page(1)
    except EmptyPage:
        plan_hist_qs = w_paginator_3.page(w_paginator_3.num_pages)\

    context['plan_hist_qs'] = plan_hist_qs
    context["plan_endpage"] = plan_hist_qs.number+1
    context["plan_startpage"] = plan_hist_qs.number-1
    context['plan_start_value'] = plan_hist_qs.start_index()
    context['plan_end_value'] = plan_hist_qs.end_index()
    context['plan_usr_count'] = obj_plan_hist.count()
    context["plan_dict_users"] = json.dumps(plan_dict_users)


    try:
      usr_addrs = self.request.GET['address']
    except:
      usr_addrs = ""

    try:
      status = self.request.GET['status']
     
      if status == 'Active':
       
        status = 0
      if status == 'Completed':
        status = 1
      if status == 'Cancelled':
        status = 2
    except:
      status = ""

    try:
      date = self.request.GET['date']
    except:
      date = ""

    withdraw_usr = 0
    withdraw_count = 0
    withdraw_dict_users = {}
    withdraw_start_page = self.request.GET.get('pageno4', 1)
    withdraw_end_value = int(withdraw_start_page) * 5
    withdraw_start_value = int(withdraw_end_value) - 4
    if usr_addrs and status and date:
      obj_withdraw_hist = Withdraw.objects.filter(userid_id = p_key).filter(Q(Address__icontains = usr_addrs) and Q(status__icontains = status) and Q(created_on__date__icontains = date)).exclude(Wallet_type__in=[ 'Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    elif usr_addrs:
      obj_withdraw_hist = Withdraw.objects.filter(userid_id = p_key).filter(Address__icontains = usr_addrs).exclude(Wallet_type__in=[ 'Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    elif date:
      obj_withdraw_hist = Withdraw.objects.filter(userid_id = p_key).filter(created_on__date__icontains = date).exclude(Wallet_type__in=[ 'Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    elif status:
      obj_withdraw_hist = Withdraw.objects.filter(userid_id = p_key).filter(status__icontains = status).exclude(Wallet_type__in=[ 'Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    else:
      obj_withdraw_hist = Withdraw.objects.filter(userid_id = p_key).exclude(Wallet_type__in=[ 'Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    try:
      tot_withdraw_user_qs = obj_withdraw_hist
    except:
      tot_withdraw_user_qs = ""
    w_page_4 = self.request.GET.get('pageno4', 1)
    w_paginator_4 = Paginator(tot_withdraw_user_qs, 5)
    try:
        withdraw_hist_qs = w_paginator_4.page(w_page_4)
    except PageNotAnInteger:
        withdraw_hist_qs =w_paginator_4.page(1)
    except EmptyPage:
        withdraw_hist_qs = w_paginator_4.page(w_paginator_4.num_pages)

    context['withdraw_hist_qs'] = withdraw_hist_qs
    context["withdraw_endpage"] = withdraw_hist_qs.number+1
    context["withdraw_startpage"] = withdraw_hist_qs.number-1
    context['withdraw_start_value'] = withdraw_hist_qs.start_index()
    context['withdraw_end_value'] = withdraw_hist_qs.end_index()
    context['withdraw_usr_count'] = obj_withdraw_hist.count()
    context["withdraw_dict_users"] = json.dumps(withdraw_dict_users)

     
    try:
      ref_user = self.request.GET['name']
    except:
      ref_user = ""


    ref_usr = 0
    ref_count = 0
    ref_dict_users = {}
    ref_start_page = self.request.GET.get('pageno5', 1)
    ref_end_value = int(ref_start_page) * 5
    ref_start_value = int(ref_end_value) - 4
    try:
      if ref_user:
        obj_ref_hist = Boat_Referral_reward_History.objects.filter(user_id = p_key).filter(referral_id__icontains = ref_user).order_by('-id')
        for i in obj_ref_hist:
          
          ref_usr = ref_usr + 1
          ref_list_usr = {}
          if ref_start_value <= ref_usr <= ref_end_value:
            ref_count = ref_count + 1
            # ref_list_usr["id"] = str(p_key)
            ref_list_usr["id"] = i.id
            ref_list_usr["username"] = str(i.user.Name)
            ref_list_usr["ref_id"] = i.referral_id
            ref_list_usr["reward_amt"] = i.reward
            ref_list_usr["date"] = (str(i.created_on))
            ref_list_usr["pageno"] = ref_start_page
            ref_list_usr["sno"] = ref_usr
            ref_dict_users[ref_count] = ref_list_usr
        
      else:
        obj_ref_hist = Boat_Referral_reward_History.objects.filter(user_id = p_key).order_by('-id')
        for i in obj_ref_hist:
          ref_usr = ref_usr + 1
          ref_list_usr = {}
          if ref_start_value <= ref_usr <= ref_end_value:
            ref_count = ref_count + 1
            ref_list_usr["id"] = i.id
            ref_list_usr["username"] = str(i.user.Name)
            ref_list_usr["ref_id"] = i.referral_id
            ref_list_usr["reward_amt"] = i.reward
            ref_list_usr["date"] = (str(i.created_on))
            ref_list_usr["pageno"] = ref_start_page
            ref_list_usr["sno"] = ref_usr
            ref_dict_users[ref_count] = ref_list_usr
        

      context['ref_usr_count'] = obj_ref_hist.count()
    except:
      obj_ref_hist = ""
      context['ref_usr_count'] = 0
    try:
      tot_ref_user_qs = obj_ref_hist
    except:
      tot_ref_user_qs = ""
    w_page_5 = self.request.GET.get('pageno5', 1)
    w_paginator_5 = Paginator(tot_ref_user_qs, 5) 
    try:
        ref_hist_qs = w_paginator_5.page(w_page_5)
    except PageNotAnInteger:
        ref_hist_qs =w_paginator_5.page(1)
    except EmptyPage:
        ref_hist_qs = w_paginator_5.page(w_paginator_5.num_pages)

    context['ref_hist_qs'] = ref_hist_qs
    context["ref_endpage"] = ref_hist_qs.number+1
    context["ref_startpage"] = ref_hist_qs.number-1
    context['ref_start_value'] = ref_hist_qs.start_index()
    context['ref_end_value'] = ref_hist_qs.end_index()
    context["ref_dict_users"] = json.dumps(ref_dict_users)

    wall_usr = 0
    wall_count = 0
    wall_dict_users = {}
    wall_start_page = self.request.GET.get('pageno6', 1)
    wall_end_value = int(wall_start_page) * 5
    wall_start_value = int(wall_end_value) - 4
    try:
      obj_wall_hist = UserCashWallet.objects.filter(userid_id = p_key).order_by('-id')
      for i in obj_wall_hist:
        wall_usr = wall_usr + 1
        wall_list_usr = {}
        if wall_start_value <= wall_usr <= wall_end_value:
          wall_count = wall_count + 1
          wall_list_usr["username"] = str(i.userid.Name)
          if i.roibalance == 0.00000000:
            wall_list_usr["health_reward"] = int(i.roibalance)
          else:
            wall_list_usr["health_reward"] = str(i.roibalance)
          if i.Boatreferalincome == 0.00000000:
            wall_list_usr["ref_reward"] = int(i.Boatreferalincome)
          else:
            wall_list_usr["ref_reward"] = str(i.Boatreferalincome)
          if i.boatwallet == 0.00000000:
            wall_list_usr["pre_reward"] = int(i.boatwallet)
          else:
            wall_list_usr["pre_reward"] = str(i.boatwallet)
          wall_list_usr["pageno"] = wall_start_page
          wall_list_usr["sno"] = wall_usr
          wall_dict_users[wall_count] = wall_list_usr
    except:
      obj_wall_hist = ""
    try:
      tot_wall_user_qs = obj_wall_hist
    except:
      tot_wall_user_qs = ""
    w_page_6 = self.request.GET.get('pageno6', 1)
    w_paginator_6 = Paginator(tot_wall_user_qs, 5)
    try:
        wall_hist_qs = w_paginator_6.page(w_page_6)
    except PageNotAnInteger:
        wall_hist_qs =w_paginator_6.page(1)
    except EmptyPage:
        wall_hist_qs = w_paginator_6.page(w_paginator_6.num_pages)

    context['wall_hist_qs'] = wall_hist_qs
    context["wall_endpage"] = wall_hist_qs.number+1
    context["wall_startpage"] = wall_hist_qs.number-1
    context['wall_start_value'] = wall_hist_qs.start_index()
    context['wall_end_value'] = wall_hist_qs.end_index()
    context['wall_usr_count'] = obj_wall_hist.count()
    context["wall_dict_users"] = json.dumps(wall_dict_users)


    login_usr = 0
    login_count = 0
    login_dict_users = {}
    login_start_page = self.request.GET.get('pageno7', 1)
    login_end_value = int(login_start_page) * 5
    login_start_value = int(login_end_value) - 4
    try:
      obj_login_hist = LoginHistory.objects.filter(user_id = p_key).order_by('-created_on')
      for i in obj_login_hist:
        login_usr = login_usr + 1
        login_list_usr = {}
        if login_start_value <= login_usr <= login_end_value:
          login_count = login_count + 1
          login_list_usr["username"] = str(i.user.Name)
          login_list_usr["created_on"] = str(i.created_on)
          login_list_usr["modified_on"] = str(i.modified_on)
          login_list_usr["pageno"] = login_start_page
          login_list_usr["sno"] = login_usr
          login_dict_users[login_count] = login_list_usr
    except:
      obj_login_hist = ""
    try:
      tot_login_user_qs = obj_login_hist
    except:
      tot_login_user_qs = ""
    w_page_7 = self.request.GET.get('pageno7', 1)
    w_paginator_7 = Paginator(tot_login_user_qs, 5)
    try:
        login_hist_qs = w_paginator_7.page(w_page_7)
    except PageNotAnInteger:
        login_hist_qs =w_paginator_7.page(1)
    except EmptyPage:
        login_hist_qs = w_paginator_7.page(w_paginator_7.num_pages)

    context['login_hist_qs'] = login_hist_qs
    context["login_endpage"] = login_hist_qs.number+1
    context["login_startpage"] = login_hist_qs.number-1
    context['login_start_value'] = login_hist_qs.start_index()
    context['login_end_value'] = login_hist_qs.end_index()
    context['login_usr_count'] = obj_login_hist.count()
    context["login_dict_users"] = json.dumps(login_dict_users)

    
    context['Title'] = 'Trade History Table'
    context["Btn_url"] = "trade_admin_auth:List_User_Management"
    return context


  @method_decorator(check_group_icon_menu("History"))
  def dispatch(self, *args, **kwargs):
    return super(TradeHistoryManagementTable, self).dispatch(*args, **kwargs)





class StakeHistoryManagementTable(TemplateView):
  template_name = "trade_admin_auth/stake_history_table.html"

  def get_context_data(self, **kwargs):
    context = super(StakeHistoryManagementTable, self).get_context_data(**kwargs)
    p_key = self.kwargs['pk']
    context["p_key"] = p_key
    try:
      user_obj = User_Management.objects.get(id = p_key)  
    except:
      user_obj = ""

    try:
      p_no = self.request.GET['pageno']
    except:
      p_no=1
    try:
      p_no1 = self.request.GET['pageno1']
    except:
      p_no1=1 
    try:
      p_no2 = self.request.GET['pageno2']
    except:
      p_no2=1
    try:
      p_no3 = self.request.GET['pageno3']
    except:
      p_no3=1
    try:
      p_no4 = self.request.GET['pageno4']
    except:
      p_no4=1   
    try:
      p_no5 = self.request.GET['pageno5']
    except:
      p_no5=1 
    try:
      p_no6 = self.request.GET['pageno6']
    except:
      p_no6=1   
    try:
      p_no7 = self.request.GET['pageno7']
    except:
      p_no7=1   

    context['p_no'] = p_no
    context['p_no1'] = p_no1
    context['p_no2'] = p_no2
    context['p_no3'] = p_no3
    context['p_no4'] = p_no4
    context['p_no5'] = p_no5
    context['p_no6'] = p_no6
    context['p_no7'] = p_no7

    try:
      s_step = self.request.GET['steps']
    except:
      s_step = ""

    

    s_usr = 0
    s_count = 0
    s_dict_users = {}
    s_start_page = self.request.GET.get('pageno', 1)
    s_end_value = int(s_start_page) * 5
    s_start_value = int(s_end_value) - 4
    
    if s_step:
      obj_step_hist = Steps_history.objects.filter(user_id = p_key).filter(steps__icontains = s_step).order_by('-id')
      for i in obj_step_hist:
        
        s_usr = s_usr + 1
        s_list_usr = {}
        if s_start_value <= s_usr <= s_end_value:
          s_count = s_count + 1
          s_list_usr["username"] = str(i.user.Name)
          s_list_usr["steps"] = (i.steps)
          s_list_usr["date"] = (str(i.created_on))
          s_list_usr["pageno"] = s_start_page
          s_list_usr["sno"] = s_usr
          s_dict_users[s_count] = s_list_usr
    else:
      obj_step_hist = Steps_history.objects.filter(user_id = p_key).order_by('-id')
      for i in obj_step_hist:
      
        s_usr = s_usr + 1
        s_list_usr = {}
        if s_start_value <= s_usr <= s_end_value:
          s_count = s_count + 1
          s_list_usr["username"] = str(i.user.Name)
          s_list_usr["steps"] = (i.steps)
          s_list_usr["date"] = (str(i.created_on))
          s_list_usr["pageno"] = s_start_page
          s_list_usr["sno"] = s_usr
          s_dict_users[s_count] = s_list_usr

    try:
      tot_step_user_qs = obj_step_hist
    except:
      tot_step_user_qs = ""
    w_page = self.request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_step_user_qs, 5)
    
    try:
        step_hist_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        step_hist_qs =w_paginator.page(1)
    except EmptyPage:
        step_hist_qs = w_paginator.page(w_paginator.num_pages)
    
    
    context['step_hist_qs'] = step_hist_qs
    context["s_endpage"] = step_hist_qs.number+1
    context["s_startpage"] = step_hist_qs.number-1
    context['s_start_value'] = step_hist_qs.start_index()
    context['s_end_value'] = step_hist_qs.end_index()
    context['s_usr_count'] = obj_step_hist.count()
    context["s_dict_users"] = json.dumps(s_dict_users)



    try:
      r_step = self.request.GET['r_steps']
    except:
      r_step = ""

    r_usr = 0
    r_count = 0
    r_dict_users = {}
    r_start_page = self.request.GET.get('pageno1', 1)
    r_end_value = int(r_start_page) * 5
    r_start_value = int(r_end_value) - 4
    if r_step:
      obj_rew_hist = Reward_History.objects.filter(user_id = p_key).filter(steps__icontains = r_step).order_by('-id')
      for i in obj_rew_hist:
        r_usr = r_usr + 1
        r_list_usr = {}
        if r_start_value <= r_usr <= r_end_value:
          r_count = r_count + 1
          r_list_usr["username"] = str(i.user.Name)
          r_list_usr["steps"] = (i.steps)
          r_list_usr["Reward"] = str(i.Reward)
          r_list_usr["date"] = (str(i.created_on))
          r_list_usr["claim_date"] = (str(i.modified_on))
          r_list_usr["pageno"] = r_start_page
          r_list_usr["sno"] = r_usr
          r_dict_users[r_count] = r_list_usr
    else:
      obj_rew_hist = Reward_History.objects.filter(user_id = p_key).order_by('-id')
      for i in obj_rew_hist:
        r_usr = r_usr + 1
        r_list_usr = {}
        if r_start_value <= r_usr <= r_end_value:
          r_count = r_count + 1
          r_list_usr["username"] = str(i.user.Name)
          r_list_usr["steps"] = (i.steps)
          r_list_usr["Reward"] = str(i.Reward)
          r_list_usr["date"] = (str(i.created_on))
          r_list_usr["claim_date"] = (str(i.modified_on))
          r_list_usr["pageno"] = r_start_page
          r_list_usr["sno"] = r_usr
          r_dict_users[r_count] = r_list_usr
    try:
      tot_rew_user_qs = obj_rew_hist
    except:
      tot_rew_user_qs = ""
    w_page_1 = self.request.GET.get('pageno1', 1)
    w_paginator_1 = Paginator(tot_rew_user_qs, 5)
    try:
        rew_hist_qs = w_paginator_1.page(w_page_1)
    except PageNotAnInteger:
        rew_hist_qs =w_paginator_1.page(1)
    except EmptyPage:
        rew_hist_qs = w_paginator_1.page(w_paginator_1.num_pages)

    context['rew_hist_qs'] = rew_hist_qs
    context["r_endpage"] = rew_hist_qs.number+1
    context["r_startpage"] = rew_hist_qs.number-1
    context['r_start_value'] = rew_hist_qs.start_index()
    context['r_end_value'] = rew_hist_qs.end_index()
    context['r_usr_count'] = obj_rew_hist.count()
    context["r_dict_users"] = json.dumps(r_dict_users)

    pre_usr = 0
    pre_count = 0
    pre_dict_users = {}
    pre_start_page = self.request.GET.get('pageno', 1)
    pre_end_value = int(pre_start_page) * 5
    pre_start_value = int(pre_end_value) - 4
    
    obj_pre_hist = new_stake_deposit_management.objects.using('second_db').filter(user = p_key,type="User Create").order_by('-id')
    for i in obj_pre_hist: 
      pre_usr = pre_usr + 1
      pre_list_usr = {}
      if pre_start_value <= pre_usr <= pre_end_value:
        pre_count = pre_count + 1
        pre_list_usr["username"] = str(user_obj.Name)
        pre_list_usr["create_type"] = (i.type)
        pre_list_usr["steps"] = (i.Amount_USDT)
        pre_list_usr["jw"] = (i.Amount_JW)
        pre_list_usr["Hash"] = (i.Hash)
        pre_list_usr["date"] = (str(i.created_on))
        pre_list_usr["pageno"] = pre_start_page
        pre_list_usr["sno"] = pre_usr
        pre_dict_users[pre_count] = pre_list_usr
    try:
      tot_step_user_qs = obj_pre_hist
    except:
      tot_step_user_qs = ""
    w_page = self.request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_step_user_qs, 5)
    
    try:
        step_hist_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        step_hist_qs =w_paginator.page(1)
    except EmptyPage:
        step_hist_qs = w_paginator.page(w_paginator.num_pages)
    
    
    context['step_hist_qs'] = step_hist_qs
    context["pre_endpage"] = step_hist_qs.number+1
    context["pre_startpage"] = step_hist_qs.number-1
    context['pre_start_value'] = step_hist_qs.start_index()
    context['pre_end_value'] = step_hist_qs.end_index()
    context['pre_usr_count'] = obj_pre_hist.count()
    context["pre_dict_users"] = json.dumps(pre_dict_users)


    pre_r_usr = 0
    pre_r_count = 0
    pre_req_dict_users = {}
    pre_r_start_page = self.request.GET.get('pageno1', 1)
    pre_r_end_value = int(pre_r_start_page) * 5
    pre_r_start_value = int(pre_r_end_value) - 4
    obj_rew_hist = new_stake_deposit_management.objects.using('second_db').filter(user = p_key).exclude(type="User Create").order_by('-created_on')
    for i in obj_rew_hist:
      pre_r_usr = pre_r_usr + 1
      r_list_usr = {}
      if pre_r_start_value <= pre_r_usr <= pre_r_end_value:
        pre_r_count = pre_r_count + 1
        r_list_usr["username"] = str(user_obj.Name)
        r_list_usr["steps"] = (i.type)
        r_list_usr["Reward"] = str(i.Amount_USDT)
        r_list_usr["date"] = (str(i.created_on))
        r_list_usr["pageno"] = pre_r_start_page
        r_list_usr["sno"] = pre_r_usr
        pre_req_dict_users[pre_r_count] = r_list_usr
    try:
      tot_rew_user_qs = obj_rew_hist
    except:
      tot_rew_user_qs = ""
    w_page_1 = self.request.GET.get('pageno1', 1)
    w_paginator_1 = Paginator(tot_rew_user_qs, 5)
    try:
        rew_hist_qs = w_paginator_1.page(w_page_1)
    except PageNotAnInteger:
        rew_hist_qs =w_paginator_1.page(1)
    except EmptyPage:
        rew_hist_qs = w_paginator_1.page(w_paginator_1.num_pages)

    context['rew_hist_qs'] = rew_hist_qs
    context["pre_r_endpage"] = rew_hist_qs.number+1
    context["pre_r_startpage"] = rew_hist_qs.number-1
    context['pre_r_start_value'] = rew_hist_qs.start_index()
    context['pre_r_end_value'] = rew_hist_qs.end_index()
    context['pre_r_usr_count'] = obj_rew_hist.count()
    context["pre_req_dict_users"] = json.dumps(pre_req_dict_users)

    try:
      two_x_step = self.request.GET['tx_steps']
    except:
      two_x_step = ""

    tx_usr = 0
    tx_count = 0
    tx_dict_users = {}
    tx_start_page = self.request.GET.get('pageno2', 1)
    tx_end_value = int(tx_start_page) * 5
    tx_start_value = int(tx_end_value) - 4
    if two_x_step:
      obj_two_x_hist = User_2x_Boost.objects.filter(userid_id = p_key).filter(user_step_count__icontains = two_x_step).order_by('-id')
      for i in obj_two_x_hist:
        tx_usr = tx_usr + 1
        tx_list_usr = {}
        if tx_start_value <= tx_usr <= tx_end_value:
          tx_count = tx_count + 1
          tx_list_usr["username"] = str(i.userid.Name)
          tx_list_usr["steps"] = (i.user_step_count)
          tx_list_usr["Reward"] = str(i.reward_per_step)
          tx_list_usr["date"] = (str(i.created_on))
          tx_list_usr["pageno"] = tx_start_page
          tx_list_usr["sno"] = tx_usr
          tx_dict_users[tx_count] = tx_list_usr
    else:
      obj_two_x_hist = User_2x_Boost.objects.filter(userid_id = p_key).order_by('-id')
      for i in obj_two_x_hist:
        tx_usr = tx_usr + 1
        tx_list_usr = {}
        if tx_start_value <= tx_usr <= tx_end_value:
          tx_count = tx_count + 1
          tx_list_usr["username"] = str(i.userid.Name)
          tx_list_usr["steps"] = (i.user_step_count)
          tx_list_usr["Reward"] = str(i.reward_per_step)
          tx_list_usr["date"] = (str(i.created_on))
          tx_list_usr["pageno"] = tx_start_page
          tx_list_usr["sno"] = tx_usr
          tx_dict_users[tx_count] = tx_list_usr
    try:
      tot_tx_user_qs = obj_two_x_hist
    except:
      tot_tx_user_qs = ""
    w_page_2 = self.request.GET.get('pageno2', 1)
    w_paginator_2 = Paginator(tot_tx_user_qs, 5)
    try:
        two_x_hist_qs = w_paginator_2.page(w_page_2)
    except PageNotAnInteger:
        two_x_hist_qs =w_paginator_2.page(1)
    except EmptyPage:
        two_x_hist_qs = w_paginator_2.page(w_paginator_2.num_pages)

    context['two_x_hist_qs'] = two_x_hist_qs
    context["tx_endpage"] = two_x_hist_qs.number+1
    context["tx_startpage"] = two_x_hist_qs.number-1
    context['tx_start_value'] = two_x_hist_qs.start_index()
    context['tx_end_value'] = two_x_hist_qs.end_index()
    context['tx_usr_count'] = obj_two_x_hist.count()
    context["tx_dict_users"] = json.dumps(tx_dict_users)



    try:
      buy_plan_name = self.request.GET['plan_name']
    except:
      buy_plan_name = ""

    plan_usr = 0
    plan_count = 0
    plan_dict_users = {}
    plan_start_page = self.request.GET.get('pageno3', 1)
    plan_end_value = int(plan_start_page) * 5
    plan_start_value = int(plan_end_value) - 4
    if buy_plan_name:
      obj_plan_hist = stake_purchase_history.objects.using('second_db').filter(user_id = p_key,user_wallet_type ='newstakewallet').order_by('-id')
      for i in obj_plan_hist:
        plan_usr = plan_usr + 1
        plan_list_usr = {}
        if plan_start_value <= plan_usr <= plan_end_value:
          plan_count = plan_count + 1
          plan_list_usr["id"] = str(p_key)
          plan_list_usr["username"] = str(i.user_id)
          plan_list_usr["plan"] = "STAKE"#int(i.purchase_amount)
          plan_list_usr["plan_amt"] = int(i.purchase_amount)
          # plan_list_usr["price"] = str(user_obj.fixed_status)
          plan_list_usr["start_date"] = (str(user_obj.created_on))
          # plan_list_usr["end_date"] = (str(user_obj.plan_end_date))
          plan_list_usr["wallet_type"] = (i.user_wallet_type)
          # plan_list_usr["health_max"] = (str(user_obj.Health_Withdraw_max_value))
          # plan_list_usr["health_min"] = (str(user_obj.Health_Withdraw_min_value))
          # plan_list_usr["referral_max"] = (str(user_obj.Referral_Withdraw_max_value))
          # plan_list_usr["referral_min"] = (str(user_obj.Referral_Withdraw_min_value))
          plan_list_usr["buy_type"] = (i.buy_type)
          plan_list_usr["StakeBwa"] = str(user_obj.StakeBwa)
          # plan_list_usr["hash"] = (str(i.User_plan_validation))
          plan_list_usr["pageno"] = plan_start_page
          plan_list_usr["sno"] = plan_usr
          plan_dict_users[plan_count] = plan_list_usr
    else:
      obj_plan_hist = stake_purchase_history.objects.using('second_db').filter(user_id = p_key,user_wallet_type ='newstakewallet').order_by('-id')
      for i in obj_plan_hist:
        plan_usr = plan_usr + 1
        plan_list_usr = {}
        if plan_start_value <= plan_usr <= plan_end_value:
          plan_count = plan_count + 1
          plan_list_usr["id"] = str(p_key)
          plan_list_usr["username"] = str(i.user_id)
          plan_list_usr["plan"] = "STAKE"#int(i.purchase_amount)
          plan_list_usr["plan_amt"] = int(i.purchase_amount)
          # plan_list_usr["price"] = str(user_obj.fixed_status)
          plan_list_usr["start_date"] = (str(user_obj.created_on))
          # plan_list_usr["end_date"] = (str(user_obj.plan_end_date))
          plan_list_usr["wallet_type"] = (i.user_wallet_type)
          # plan_list_usr["health_max"] = (str(user_obj.Health_Withdraw_max_value))
          # plan_list_usr["health_min"] = (str(user_obj.Health_Withdraw_min_value))
          # plan_list_usr["referral_max"] = (str(user_obj.Referral_Withdraw_max_value))
          # plan_list_usr["referral_min"] = (str(user_obj.Referral_Withdraw_min_value))
          plan_list_usr["buy_type"] = (i.buy_type)
          plan_list_usr["StakeBwa"] = str(user_obj.StakeBwa)
          # plan_list_usr["hash"] = (str(i.User_plan_validation))
          plan_list_usr["pageno"] = plan_start_page
          plan_list_usr["sno"] = plan_usr
          plan_dict_users[plan_count] = plan_list_usr
    try:
      tot_plan_user_qs = obj_plan_hist
    except:
      tot_plan_user_qs = ""
    w_page_3 = self.request.GET.get('pageno3', 1)
    w_paginator_3 = Paginator(tot_plan_user_qs, 5)
    try:
        plan_hist_qs = w_paginator_3.page(w_page_3)
    except PageNotAnInteger:
        plan_hist_qs =w_paginator_3.page(1)
    except EmptyPage:
        plan_hist_qs = w_paginator_3.page(w_paginator_3.num_pages)\

    context['plan_hist_qs'] = plan_hist_qs
    context["plan_endpage"] = plan_hist_qs.number+1
    context["plan_startpage"] = plan_hist_qs.number-1
    context['plan_start_value'] = plan_hist_qs.start_index()
    context['plan_end_value'] = plan_hist_qs.end_index()
    context['plan_usr_count'] = obj_plan_hist.count()
    context["plan_dict_users"] = json.dumps(plan_dict_users)


    try:
      usr_addrs = self.request.GET['address']
    except:
      usr_addrs = ""

    try:
      status = self.request.GET['status']
     
      if status == 'Active':
       
        status = 0
      if status == 'Completed':
        status = 1
      if status == 'Cancelled':
        status = 2
    except:
      status = ""

    try:
      date = self.request.GET['date']
    except:
      date = ""

    withdraw_usr = 0
    withdraw_count = 0
    withdraw_dict_users = {}
    withdraw_start_page = self.request.GET.get('pageno4', 1)
    withdraw_end_value = int(withdraw_start_page) * 5
    withdraw_start_value = int(withdraw_end_value) - 4
    if usr_addrs and status and date:
      obj_withdraw_hist = stake_claim_table.objects.using('second_db').filter(user = p_key).filter(Q(Address__icontains = usr_addrs) and Q(status__icontains = status) and Q(created_on__date__icontains = date)).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.email)
          withdraw_list_usr["amount"] = str(i.original_USDT)
          withdraw_list_usr["Withdraw_fee"] = 'asperreq' #str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.claim_amount_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.claim_amount_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    elif usr_addrs:
      obj_withdraw_hist =stake_claim_table.objects.using('second_db').filter(user = p_key).filter(Address__icontains = usr_addrs).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.email)
          withdraw_list_usr["amount"] = str(i.original_USDT)
          withdraw_list_usr["Withdraw_fee"] = 'asperreq' #str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.claim_amount_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.claim_amount_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    elif date:
      obj_withdraw_hist = stake_claim_table.objects.using('second_db').filter(user = p_key).filter(created_on__date__icontains = date).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.email)
          withdraw_list_usr["amount"] = str(i.original_USDT)
          withdraw_list_usr["Withdraw_fee"] = 'asperreq' #str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.claim_amount_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.claim_amount_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    elif status:
      obj_withdraw_hist = stake_claim_table.objects.using('second_db').filter(user = p_key).filter(status__icontains = status).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.email)
          withdraw_list_usr["amount"] = str(i.original_USDT)
          withdraw_list_usr["Withdraw_fee"] = 'asperreq' #str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.claim_amount_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.claim_amount_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    else:
      obj_withdraw_hist = stake_claim_table.objects.using('second_db').filter(user = p_key).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.email)
          withdraw_list_usr["amount"] = str(i.original_USDT)
          withdraw_list_usr["Withdraw_fee"] = 'asperreq' #str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.claim_amount_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.claim_amount_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    try:
      tot_withdraw_user_qs = obj_withdraw_hist
    except:
      tot_withdraw_user_qs = ""
    w_page_4 = self.request.GET.get('pageno4', 1)
    w_paginator_4 = Paginator(tot_withdraw_user_qs, 5)
    try:
        withdraw_hist_qs = w_paginator_4.page(w_page_4)
    except PageNotAnInteger:
        withdraw_hist_qs =w_paginator_4.page(1)
    except EmptyPage:
        withdraw_hist_qs = w_paginator_4.page(w_paginator_4.num_pages)

    context['withdraw_hist_qs'] = withdraw_hist_qs
    context["withdraw_endpage"] = withdraw_hist_qs.number+1
    context["withdraw_startpage"] = withdraw_hist_qs.number-1
    context['withdraw_start_value'] = withdraw_hist_qs.start_index()
    context['withdraw_end_value'] = withdraw_hist_qs.end_index()
    context['withdraw_usr_count'] = obj_withdraw_hist.count()
    context["withdraw_dict_users"] = json.dumps(withdraw_dict_users)

     
    try:
      ref_user = self.request.GET['name']
    except:
      ref_user = ""


    ref_usr = 0
    ref_count = 0
    ref_dict_users = {}
    ref_start_page = self.request.GET.get('pageno5', 1)
    ref_end_value = int(ref_start_page) * 5
    ref_start_value = int(ref_end_value) - 4
    try:
      if ref_user:
        obj_ref_hist = newstake_Referral_reward_History.objects.using('second_db').filter(referral_id__icontains = ref_user).order_by('-id')
        for i in obj_ref_hist:
          
          ref_usr = ref_usr + 1
          ref_list_usr = {}
          if ref_start_value <= ref_usr <= ref_end_value:
            ref_count = ref_count + 1
            # ref_list_usr["id"] = str(p_key)
            ref_list_usr["id"] = i.id
            ref_list_usr["username"] = str(i.user.Name)
            ref_list_usr["ref_id"] = i.referral_id
            ref_list_usr["reward_amt"] = i.reward
            ref_list_usr["date"] = (str(i.created_on))
            ref_list_usr["pageno"] = ref_start_page
            ref_list_usr["sno"] = ref_usr
            ref_dict_users[ref_count] = ref_list_usr
        
      else:
        obj_ref_hist = newstake_Referral_reward_History.objects.using('second_db').filter(user_id = p_key).order_by('-id')
        for i in obj_ref_hist:
          ref_usr = ref_usr + 1
          ref_list_usr = {}
          if ref_start_value <= ref_usr <= ref_end_value:
            ref_count = ref_count + 1
            ref_list_usr["id"] = i.id
            ref_list_usr["username"] = str(i.user.Name)
            ref_list_usr["ref_id"] = i.referral_id
            ref_list_usr["reward_amt"] = i.reward
            ref_list_usr["date"] = (str(i.created_on))
            ref_list_usr["pageno"] = ref_start_page
            ref_list_usr["sno"] = ref_usr
            ref_dict_users[ref_count] = ref_list_usr
        

      context['ref_usr_count'] = obj_ref_hist.count()
    except:
      obj_ref_hist = ""
      context['ref_usr_count'] = 0
    try:
      tot_ref_user_qs = obj_ref_hist
    except:
      tot_ref_user_qs = ""
    w_page_5 = self.request.GET.get('pageno5', 1)
    w_paginator_5 = Paginator(tot_ref_user_qs, 5)
    try:
        ref_hist_qs = w_paginator_5.page(w_page_5)
    except PageNotAnInteger:
        ref_hist_qs =w_paginator_5.page(1)
    except EmptyPage:
        ref_hist_qs = w_paginator_5.page(w_paginator_5.num_pages)

    context['ref_hist_qs'] = ref_hist_qs
    context["ref_endpage"] = ref_hist_qs.number+1
    context["ref_startpage"] = ref_hist_qs.number-1
    context['ref_start_value'] = ref_hist_qs.start_index()
    context['ref_end_value'] = ref_hist_qs.end_index()
    context["ref_dict_users"] = json.dumps(ref_dict_users)

    wall_usr = 0
    wall_count = 0
    wall_dict_users = {}
    wall_start_page = self.request.GET.get('pageno6', 1)
    wall_end_value = int(wall_start_page) * 5
    wall_start_value = int(wall_end_value) - 4
    try:
      obj_wall_hist = stake_wallet_management.objects.using('second_db').filter(user = p_key).order_by('-id')
      for i in obj_wall_hist:
        wall_usr = wall_usr + 1
        wall_list_usr = {}
        if wall_start_value <= wall_usr <= wall_end_value:
          wall_count = wall_count + 1
          wall_list_usr["username"] = str(i.user.Name)
          if i.newstakewithdraw == 0:
            wall_list_usr["health_reward"] = int(i.newstakewithdraw)
          else:
            wall_list_usr["health_reward"] = str(i.newstakewithdraw)
          if i.newstakereff == 0:
            wall_list_usr["ref_reward"] = int(i.newstakereff)
          else:
            wall_list_usr["ref_reward"] = str(i.newstakereff)
          if i.newstakewithdraw == 0:
            wall_list_usr["pre_reward"] = int(i.newstakewithdraw)
          else:
            wall_list_usr["pre_reward"] = str(i.newstakewithdraw)
          wall_list_usr["pageno"] = wall_start_page
          wall_list_usr["sno"] = wall_usr
          wall_dict_users[wall_count] = wall_list_usr       
    except:
      obj_wall_hist = ""
    try:
      tot_wall_user_qs = obj_wall_hist
    except:
      tot_wall_user_qs = ""
    w_page_6 = self.request.GET.get('pageno6', 1)
    w_paginator_6 = Paginator(tot_wall_user_qs, 5)
    try:
        wall_hist_qs = w_paginator_6.page(w_page_6)
    except PageNotAnInteger:
        wall_hist_qs =w_paginator_6.page(1)
    except EmptyPage:
        wall_hist_qs = w_paginator_6.page(w_paginator_6.num_pages)

    context['wall_hist_qs'] = wall_hist_qs
    context["wall_endpage"] = wall_hist_qs.number+1
    context["wall_startpage"] = wall_hist_qs.number-1
    context['wall_start_value'] = wall_hist_qs.start_index()
    context['wall_end_value'] = wall_hist_qs.end_index()
    context['wall_usr_count'] = obj_wall_hist.count() if obj_wall_hist else 0
    context["wall_dict_users"] = json.dumps(wall_dict_users)

    # wall_usr = 0
    # wall_count = 0
    # wall_dict_users = {}
    # wall_start_page = self.request.GET.get('pageno6', 1)
    # wall_end_value = int(wall_start_page) * 5
    # wall_start_value = int(wall_end_value) - 4
    # try:
    #   obj_wall_hist = UserCashWallet.objects.filter(userid_id = p_key).order_by('-id')
    #   for i in obj_wall_hist:
    #     wall_usr = wall_usr + 1
    #     wall_list_usr = {}
    #     if wall_start_value <= wall_usr <= wall_end_value:
    #       wall_count = wall_count + 1
    #       wall_list_usr["username"] = str(i.userid.Name)
    #       if i.roibalance == 0.00000000:
    #         wall_list_usr["health_reward"] = int(i.roibalance)
    #       else:
    #         wall_list_usr["health_reward"] = str(i.roibalance)
    #       if i.Boatreferalincome == 0.00000000:
    #         wall_list_usr["ref_reward"] = int(i.Boatreferalincome)
    #       else:
    #         wall_list_usr["ref_reward"] = str(i.Boatreferalincome)
    #       if i.boatwallet == 0.00000000:
    #         wall_list_usr["pre_reward"] = int(i.boatwallet)
    #       else:
    #         wall_list_usr["pre_reward"] = str(i.boatwallet)
    #       wall_list_usr["pageno"] = wall_start_page
    #       wall_list_usr["sno"] = wall_usr
    #       wall_dict_users[wall_count] = wall_list_usr
    # except:
    #   obj_wall_hist = ""
    # try:
    #   tot_wall_user_qs = obj_wall_hist
    # except:
    #   tot_wall_user_qs = ""
    # w_page_6 = self.request.GET.get('pageno6', 1)
    # w_paginator_6 = Paginator(tot_wall_user_qs, 5)
    # try:
    #     wall_hist_qs = w_paginator_6.page(w_page_6)
    # except PageNotAnInteger:
    #     wall_hist_qs =w_paginator_6.page(1)
    # except EmptyPage:
    #     wall_hist_qs = w_paginator_6.page(w_paginator_6.num_pages)

    # context['wall_hist_qs'] = wall_hist_qs
    # context["wall_endpage"] = wall_hist_qs.number+1
    # context["wall_startpage"] = wall_hist_qs.number-1
    # context['wall_start_value'] = wall_hist_qs.start_index()
    # context['wall_end_value'] = wall_hist_qs.end_index()
    # context['wall_usr_count'] = obj_wall_hist.count()
    # context["wall_dict_users"] = json.dumps(wall_dict_users)

    # wall_usr = 0
    # wall_count = 0
    # wall_dict_users = {}
    # wall_start_page = int(self.request.GET.get('pageno6', 1))
    # wall_end_value = wall_start_page * 5
    # wall_start_value = wall_end_value - 4

    # try:
    #     # Fetch the wallet history for the given user from the secondary database
    #     obj_wall_hist = stake_wallet_management.objects.using('second_db').filter(user=p_key).order_by('id')
    # except stake_wallet_management.DoesNotExist:
    #     obj_wall_hist = ""

    # # Create a list of user data for the given range
    # for index, i in enumerate(obj_wall_hist[wall_start_value - 1:wall_end_value], start=wall_start_value):
    #     wall_list_usr = {
    #         "username": str(i.email),
    #         "health_reward": int(float(i.newstakewithdraw)) if i.newstakewithdraw else 0,  # Convert to float, then int
    #         "ref_reward": int(float(i.newstakereff)) if i.newstakereff else 0,
    #         "pre_reward": int(float(i.newstakewallet)) if i.newstakewallet else 0,
    #         "pageno": wall_start_page,
    #         "sno": index,
    #     }
    #     wall_dict_users[index] = wall_list_usr
    
    # # Create a list of user data for the given range

    # # Paginate the queryset
    # paginator = Paginator(obj_wall_hist, 5)
    # try:
    #     wall_hist_qs = paginator.page(wall_start_page)
    # except PageNotAnInteger:
    #     wall_hist_qs = paginator.page(1)
    # except EmptyPage:
    #     wall_hist_qs = paginator.page(paginator.num_pages)

    # # Add data to the context
    # context = {}
    # context['wall_hist_qs'] = wall_hist_qs
    # context["wall_endpage"] = wall_hist_qs.next_page_number() if wall_hist_qs.has_next() else None
    # context["wall_startpage"] = wall_hist_qs.previous_page_number() if wall_hist_qs.has_previous() else None
    # context['wall_start_value'] = wall_hist_qs.start_index()
    # context['wall_end_value'] = wall_hist_qs.end_index()
    # context['wall_usr_count'] = obj_wall_hist.count() if obj_wall_hist else 0
    # context["wall_dict_users"] = json.dumps(wall_dict_users)


    login_usr = 0
    login_count = 0
    login_dict_users = {}
    login_start_page = self.request.GET.get('pageno7', 1)
    login_end_value = int(login_start_page) * 5
    login_start_value = int(login_end_value) - 4
    try:
      obj_login_hist = LoginHistory.objects.filter(user_id = p_key).order_by('-created_on')
      for i in obj_login_hist:
        login_usr = login_usr + 1
        login_list_usr = {}
        if login_start_value <= login_usr <= login_end_value:
          login_count = login_count + 1
          login_list_usr["username"] = str(i.user.Name)
          login_list_usr["created_on"] = str(i.created_on)
          login_list_usr["modified_on"] = str(i.modified_on)
          login_list_usr["pageno"] = login_start_page
          login_list_usr["sno"] = login_usr
          login_dict_users[login_count] = login_list_usr
    except:
      obj_login_hist = ""
    try:
      tot_login_user_qs = obj_login_hist
    except:
      tot_login_user_qs = ""
    w_page_7 = self.request.GET.get('pageno7', 1)
    w_paginator_7 = Paginator(tot_login_user_qs, 5)
    try:
        login_hist_qs = w_paginator_7.page(w_page_7)
    except PageNotAnInteger:
        login_hist_qs =w_paginator_7.page(1)
    except EmptyPage:
        login_hist_qs = w_paginator_7.page(w_paginator_7.num_pages)

    context['login_hist_qs'] = login_hist_qs
    context["login_endpage"] = login_hist_qs.number+1
    context["login_startpage"] = login_hist_qs.number-1
    context['login_start_value'] = login_hist_qs.start_index()
    context['login_end_value'] = login_hist_qs.end_index()
    context['login_usr_count'] = obj_login_hist.count()
    context["login_dict_users"] = json.dumps(login_dict_users)

    
    context['Title'] = 'Stake History Table'
    context["Btn_url"] = "trade_admin_auth:List_User_Management"
    return context


  @method_decorator(check_group_icon_menu("History"))
  def dispatch(self, *args, **kwargs):
    return super(StakeHistoryManagementTable, self).dispatch(*args, **kwargs)





####################################################################################################
################################################ MP Plan ###########################################




class MPlanHistoryManagementTable(TemplateView):
  template_name = "trade_admin_auth/mp_history_table.html"

  def get_context_data(self, **kwargs):
    context = super(MPlanHistoryManagementTable, self).get_context_data(**kwargs)
    p_key = self.kwargs['pk']
    context["p_key"] = p_key
    try:
      user_obj = User_Management.objects.get(id = p_key)
    except:
      user_obj = ""

    try:
      p_no = self.request.GET['pageno']
    except:
      p_no=1
    try:
      p_no1 = self.request.GET['pageno1']
    except:
      p_no1=1 
    try:
      p_no2 = self.request.GET['pageno2']
    except:
      p_no2=1
    try:
      p_no3 = self.request.GET['pageno3']
    except:
      p_no3=1
    try:
      p_no4 = self.request.GET['pageno4']
    except:
      p_no4=1   
    try:
      p_no5 = self.request.GET['pageno5']
    except:
      p_no5=1 
    try:
      p_no6 = self.request.GET['pageno6']
    except:
      p_no6=1   
    try:
      p_no7 = self.request.GET['pageno7']
    except:
      p_no7=1   

    context['p_no'] = p_no
    context['p_no1'] = p_no1
    context['p_no2'] = p_no2
    context['p_no3'] = p_no3
    context['p_no4'] = p_no4
    context['p_no5'] = p_no5
    context['p_no6'] = p_no6
    context['p_no7'] = p_no7

    try:
      s_step = self.request.GET['steps']
    except:
      s_step = ""

    

    s_usr = 0
    s_count = 0
    s_dict_users = {}
    s_start_page = self.request.GET.get('pageno', 1)
    s_end_value = int(s_start_page) * 5
    s_start_value = int(s_end_value) - 4
    
    if s_step:
      obj_step_hist = Steps_history.objects.filter(user_id = p_key).filter(steps__icontains = s_step).order_by('-id')
      for i in obj_step_hist:
        
        s_usr = s_usr + 1
        s_list_usr = {}
        if s_start_value <= s_usr <= s_end_value:
          s_count = s_count + 1
          s_list_usr["username"] = str(i.user.Name)
          s_list_usr["steps"] = (i.steps)
          s_list_usr["date"] = (str(i.created_on))
          s_list_usr["pageno"] = s_start_page
          s_list_usr["sno"] = s_usr
          s_dict_users[s_count] = s_list_usr
    else:
      obj_step_hist = Steps_history.objects.filter(user_id = p_key).order_by('-id')
      for i in obj_step_hist:
      
        s_usr = s_usr + 1
        s_list_usr = {}
        if s_start_value <= s_usr <= s_end_value:
          s_count = s_count + 1
          s_list_usr["username"] = str(i.user.Name)
          s_list_usr["steps"] = (i.steps)
          s_list_usr["date"] = (str(i.created_on))
          s_list_usr["pageno"] = s_start_page
          s_list_usr["sno"] = s_usr
          s_dict_users[s_count] = s_list_usr

    try:
      tot_step_user_qs = obj_step_hist
    except:
      tot_step_user_qs = ""
    w_page = self.request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_step_user_qs, 5)
    
    try:
        step_hist_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        step_hist_qs =w_paginator.page(1)
    except EmptyPage:
        step_hist_qs = w_paginator.page(w_paginator.num_pages)
    
    
    context['step_hist_qs'] = step_hist_qs
    context["s_endpage"] = step_hist_qs.number+1
    context["s_startpage"] = step_hist_qs.number-1
    context['s_start_value'] = step_hist_qs.start_index()
    context['s_end_value'] = step_hist_qs.end_index()
    context['s_usr_count'] = obj_step_hist.count()
    context["s_dict_users"] = json.dumps(s_dict_users)



    try:
      r_step = self.request.GET['r_steps']
    except:
      r_step = ""

    r_usr = 0
    r_count = 0
    r_dict_users = {}
    r_start_page = self.request.GET.get('pageno1', 1)
    r_end_value = int(r_start_page) * 5
    r_start_value = int(r_end_value) - 4
    if r_step:
      obj_rew_hist = MPRewardHistory.objects.filter(user_id = p_key).filter(steps__icontains = r_step).order_by('-id')
      for i in obj_rew_hist:
        r_usr = r_usr + 1
        r_list_usr = {}
        if r_start_value <= r_usr <= r_end_value:
          r_count = r_count + 1
          r_list_usr["username"] = str(i.user.Name)
          r_list_usr["steps"] = 3000
          r_list_usr["Reward"] = str(i.reward)
          r_list_usr["date"] = (str(i.created_on))
          r_list_usr["claim_date"] = (str(i.modified_on))
          r_list_usr["pageno"] = r_start_page
          r_list_usr["sno"] = r_usr
          r_dict_users[r_count] = r_list_usr
    else:
      obj_rew_hist = MPRewardHistory.objects.filter(user_id = p_key).order_by('-id')
      for i in obj_rew_hist:
        r_usr = r_usr + 1
        r_list_usr = {}
        if r_start_value <= r_usr <= r_end_value:
          r_count = r_count + 1
          r_list_usr["username"] = str(i.user.Name)
          r_list_usr["steps"] = 3000
          r_list_usr["Reward"] = str(i.reward)
          r_list_usr["date"] = (str(i.created_on))
          r_list_usr["claim_date"] = (str(i.modified_on))
          r_list_usr["pageno"] = r_start_page
          r_list_usr["sno"] = r_usr
          r_dict_users[r_count] = r_list_usr
    try:
      tot_rew_user_qs = obj_rew_hist
    except:
      tot_rew_user_qs = ""
    w_page_1 = self.request.GET.get('pageno1', 1)
    w_paginator_1 = Paginator(tot_rew_user_qs, 5)
    try:
        rew_hist_qs = w_paginator_1.page(w_page_1)
    except PageNotAnInteger:
        rew_hist_qs =w_paginator_1.page(1)
    except EmptyPage:
        rew_hist_qs = w_paginator_1.page(w_paginator_1.num_pages)

    context['rew_hist_qs'] = rew_hist_qs
    context["r_endpage"] = rew_hist_qs.number+1
    context["r_startpage"] = rew_hist_qs.number-1
    context['r_start_value'] = rew_hist_qs.start_index()
    context['r_end_value'] = rew_hist_qs.end_index()
    context['r_usr_count'] = obj_rew_hist.count()
    context["r_dict_users"] = json.dumps(r_dict_users)

    pre_usr = 0
    pre_count = 0
    pre_dict_users = {}
    pre_start_page = self.request.GET.get('pageno', 1)
    pre_end_value = int(pre_start_page) * 5
    pre_start_value = int(pre_end_value) - 4
    
    obj_pre_hist = Boat_wallet.objects.filter(user = p_key,type="User Create").order_by('-id')
    for i in obj_pre_hist: 
      pre_usr = pre_usr + 1
      pre_list_usr = {}
      if pre_start_value <= pre_usr <= pre_end_value:
        pre_count = pre_count + 1
        pre_list_usr["username"] = str(user_obj.Name)
        pre_list_usr["create_type"] = (i.create_type)
        pre_list_usr["steps"] = (i.Amount_USDT)
        pre_list_usr["jw"] = (i.Amount_JW)
        pre_list_usr["Hash"] = (i.Hash)
        pre_list_usr["date"] = (str(i.created_on))
        pre_list_usr["pageno"] = pre_start_page
        pre_list_usr["sno"] = pre_usr
        pre_dict_users[pre_count] = pre_list_usr
    try:
      tot_step_user_qs = obj_pre_hist
    except:
      tot_step_user_qs = ""
    w_page = self.request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_step_user_qs, 5)
    
    try:
        step_hist_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        step_hist_qs =w_paginator.page(1)
    except EmptyPage:
        step_hist_qs = w_paginator.page(w_paginator.num_pages)
    
    
    context['step_hist_qs'] = step_hist_qs
    context["pre_endpage"] = step_hist_qs.number+1
    context["pre_startpage"] = step_hist_qs.number-1
    context['pre_start_value'] = step_hist_qs.start_index()
    context['pre_end_value'] = step_hist_qs.end_index()
    context['pre_usr_count'] = obj_pre_hist.count()
    context["pre_dict_users"] = json.dumps(pre_dict_users)


    pre_r_usr = 0
    pre_r_count = 0
    pre_req_dict_users = {}
    pre_r_start_page = self.request.GET.get('pageno1', 1)
    pre_r_end_value = int(pre_r_start_page) * 5
    pre_r_start_value = int(pre_r_end_value) - 4
    obj_rew_hist = Boat_wallet.objects.filter(user = p_key).exclude(type="User Create").order_by('-created_on')
    for i in obj_rew_hist:
      pre_r_usr = pre_r_usr + 1
      r_list_usr = {}
      if pre_r_start_value <= pre_r_usr <= pre_r_end_value:
        pre_r_count = pre_r_count + 1
        r_list_usr["username"] = str(user_obj.Name)
        r_list_usr["steps"] = (i.type)
        r_list_usr["Reward"] = str(i.Amount_USDT)
        r_list_usr["date"] = (str(i.created_on))
        r_list_usr["pageno"] = pre_r_start_page
        r_list_usr["sno"] = pre_r_usr
        pre_req_dict_users[pre_r_count] = r_list_usr
    try:
      tot_rew_user_qs = obj_rew_hist
    except:
      tot_rew_user_qs = ""
    w_page_1 = self.request.GET.get('pageno1', 1)
    w_paginator_1 = Paginator(tot_rew_user_qs, 5)
    try:
        rew_hist_qs = w_paginator_1.page(w_page_1)
    except PageNotAnInteger:
        rew_hist_qs =w_paginator_1.page(1)
    except EmptyPage:
        rew_hist_qs = w_paginator_1.page(w_paginator_1.num_pages)

    context['rew_hist_qs'] = rew_hist_qs
    context["pre_r_endpage"] = rew_hist_qs.number+1
    context["pre_r_startpage"] = rew_hist_qs.number-1
    context['pre_r_start_value'] = rew_hist_qs.start_index()
    context['pre_r_end_value'] = rew_hist_qs.end_index()
    context['pre_r_usr_count'] = obj_rew_hist.count()
    context["pre_req_dict_users"] = json.dumps(pre_req_dict_users)

    try:
      two_x_step = self.request.GET['tx_steps']
    except:
      two_x_step = ""

    tx_usr = 0
    tx_count = 0
    tx_dict_users = {}
    tx_start_page = self.request.GET.get('pageno2', 1)
    tx_end_value = int(tx_start_page) * 5
    tx_start_value = int(tx_end_value) - 4
    if two_x_step:
      obj_two_x_hist = User_2x_Boost.objects.filter(userid_id = p_key).filter(user_step_count__icontains = two_x_step).order_by('-id')
      for i in obj_two_x_hist:
        tx_usr = tx_usr + 1
        tx_list_usr = {}
        if tx_start_value <= tx_usr <= tx_end_value:
          tx_count = tx_count + 1
          tx_list_usr["username"] = str(i.userid.Name)
          tx_list_usr["steps"] = (i.user_step_count)
          tx_list_usr["Reward"] = str(i.reward_per_step)
          tx_list_usr["date"] = (str(i.created_on))
          tx_list_usr["pageno"] = tx_start_page
          tx_list_usr["sno"] = tx_usr
          tx_dict_users[tx_count] = tx_list_usr
    else:
      obj_two_x_hist = User_2x_Boost.objects.filter(userid_id = p_key).order_by('-id')
      for i in obj_two_x_hist:
        tx_usr = tx_usr + 1
        tx_list_usr = {}
        if tx_start_value <= tx_usr <= tx_end_value:
          tx_count = tx_count + 1
          tx_list_usr["username"] = str(i.userid.Name)
          tx_list_usr["steps"] = (i.user_step_count)
          tx_list_usr["Reward"] = str(i.reward_per_step)
          tx_list_usr["date"] = (str(i.created_on))
          tx_list_usr["pageno"] = tx_start_page
          tx_list_usr["sno"] = tx_usr
          tx_dict_users[tx_count] = tx_list_usr
    try:
      tot_tx_user_qs = obj_two_x_hist
    except:
      tot_tx_user_qs = ""
    w_page_2 = self.request.GET.get('pageno2', 1)
    w_paginator_2 = Paginator(tot_tx_user_qs, 5)
    try:
        two_x_hist_qs = w_paginator_2.page(w_page_2)
    except PageNotAnInteger:
        two_x_hist_qs =w_paginator_2.page(1)
    except EmptyPage:
        two_x_hist_qs = w_paginator_2.page(w_paginator_2.num_pages)

    context['two_x_hist_qs'] = two_x_hist_qs
    context["tx_endpage"] = two_x_hist_qs.number+1
    context["tx_startpage"] = two_x_hist_qs.number-1
    context['tx_start_value'] = two_x_hist_qs.start_index()
    context['tx_end_value'] = two_x_hist_qs.end_index()
    context['tx_usr_count'] = obj_two_x_hist.count()
    context["tx_dict_users"] = json.dumps(tx_dict_users)



    try:
      buy_plan_name = self.request.GET['plan_name']
    except:
      buy_plan_name = ""

    plan_usr = 0
    plan_count = 0
    plan_dict_users = {}
    plan_start_page = self.request.GET.get('pageno3', 1)
    plan_end_value = int(plan_start_page) * 5
    plan_start_value = int(plan_end_value) - 4
    Comp = MPPLanHistory.objects.filter(email_id = p_key).order_by('-id')
    if buy_plan_name:
      obj_plan_hist = MPPLanHistory.objects.filter(email_id = p_key).order_by('-id')
      for i in obj_plan_hist:
        plan_usr = plan_usr + 1
        plan_list_usr = {}
        if plan_start_value <= plan_usr <= plan_end_value:
          plan_count = plan_count + 1
          plan_list_usr["id"] = str(p_key)
          plan_list_usr["username"] = str(i.user)
          plan_list_usr["plan"] = "MP"#int(i.purchase_amount)
          plan_list_usr["plan_amt"] = int(i.plan_amount)
          plan_list_usr["start_date"] = (str(i.plan_start_date))
          # plan_list_usr["end_date"] = (str(user_obj.plan_end_date))
          plan_list_usr["wallet_type"] = (str(i.Transaction_Hash))
          # plan_list_usr["health_max"] = (str(user_obj.Health_Withdraw_max_value))
          # plan_list_usr["health_min"] = (str(user_obj.Health_Withdraw_min_value))
          # plan_list_usr["referral_max"] = (str(user_obj.Referral_Withdraw_max_value))
          # plan_list_usr["referral_min"] = (str(user_obj.Referral_Withdraw_min_value))
          plan_list_usr["hash"] = (str(i.Transaction_Hash))
          plan_list_usr["buy_type"] = (i.currency)
          plan_list_usr["TradeBwa"] = str(user_obj.MPlanBWA)
          # plan_list_usr["hash"] = (str(i.User_plan_validation))
          plan_list_usr["pageno"] = plan_start_page
          plan_list_usr["sno"] = plan_usr
          plan_dict_users[plan_count] = plan_list_usr
    else:
      obj_plan_hist = MPPLanHistory.objects.filter(email_id = p_key).order_by('-id')
      for i in obj_plan_hist:
        plan_usr = plan_usr + 1
        plan_list_usr = {}
        if plan_start_value <= plan_usr <= plan_end_value:
          plan_count = plan_count + 1
          plan_list_usr["id"] = str(p_key)
          plan_list_usr["username"] = str(i.user)
          plan_list_usr["plan"] = "MP"#int(i.purchase_amount)
          plan_list_usr["plan_amt"] = int(i.plan_amount)
          # plan_list_usr["price"] = str(user_obj.fixed_status)
          plan_list_usr["start_date"] = (str(i.plan_start_date))
          # plan_list_usr["end_date"] = (str(user_obj.plan_end_date))
          plan_list_usr["wallet_type"] = (str(i.Transaction_Hash))
          # plan_list_usr["health_max"] = (str(user_obj.Health_Withdraw_max_value))
          # plan_list_usr["health_min"] = (str(user_obj.Health_Withdraw_min_value))
          # plan_list_usr["referral_max"] = (str(user_obj.Referral_Withdraw_max_value))
          # plan_list_usr["referral_min"] = (str(user_obj.Referral_Withdraw_min_value))
          plan_list_usr["hash"] = (str(i.Transaction_Hash))
          plan_list_usr["buy_type"] = (i.currency)
          plan_list_usr["TradeBwa"] = str(user_obj.MPlanBWA)
          plan_list_usr["pageno"] = plan_start_page
          plan_list_usr["sno"] = plan_usr
          plan_dict_users[plan_count] = plan_list_usr
    try:
      tot_plan_user_qs = obj_plan_hist
    except:
      tot_plan_user_qs = ""
    w_page_3 = self.request.GET.get('pageno3', 1)
    w_paginator_3 = Paginator(tot_plan_user_qs, 5)
    try:
        plan_hist_qs = w_paginator_3.page(w_page_3)
    except PageNotAnInteger:
        plan_hist_qs =w_paginator_3.page(1)
    except EmptyPage:
        plan_hist_qs = w_paginator_3.page(w_paginator_3.num_pages)\

    context['plan_hist_qs'] = plan_hist_qs
    context["plan_endpage"] = plan_hist_qs.number+1
    context["plan_startpage"] = plan_hist_qs.number-1
    context['plan_start_value'] = plan_hist_qs.start_index()
    context['plan_end_value'] = plan_hist_qs.end_index()
    context['plan_usr_count'] = obj_plan_hist.count()
    context["plan_dict_users"] = json.dumps(plan_dict_users)


    try:
      usr_addrs = self.request.GET['address']
    except:
      usr_addrs = ""

    try:
      status = self.request.GET['status']
     
      if status == 'Active':
       
        status = 0
      if status == 'Completed':
        status = 1
      if status == 'Cancelled':
        status = 2
    except:
      status = ""

    try:
      date = self.request.GET['date']
    except:
      date = ""

    withdraw_usr = 0
    withdraw_count = 0
    withdraw_dict_users = {}
    withdraw_start_page = self.request.GET.get('pageno4', 1)
    withdraw_end_value = int(withdraw_start_page) * 5
    withdraw_start_value = int(withdraw_end_value) - 4
    if usr_addrs and status and date:
      obj_withdraw_hist = Withdraw.objects.filter(userid_id = p_key).filter(Q(Address__icontains = usr_addrs) and Q(status__icontains = status) and Q(created_on__date__icontains = date)).exclude(Wallet_type__in=[ 'Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet','Bot_Referral_wallet','trade_withdraw_wallet','Trade_Referral_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    elif usr_addrs:
      obj_withdraw_hist = Withdraw.objects.filter(userid_id = p_key).filter(Address__icontains = usr_addrs).exclude(Wallet_type__in=['Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet','Bot_Referral_wallet','trade_withdraw_wallet','Trade_Referral_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on)) 
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    elif date:
      obj_withdraw_hist = Withdraw.objects.filter(userid_id = p_key).filter(created_on__date__icontains = date).exclude(Wallet_type__in=['Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet','Bot_Referral_wallet','trade_withdraw_wallet','Trade_Referral_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    elif status:
      obj_withdraw_hist = Withdraw.objects.filter(userid_id = p_key).filter(status__icontains = status).exclude(Wallet_type__in=['Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet','Bot_Referral_wallet','trade_withdraw_wallet','Trade_Referral_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    else:
      obj_withdraw_hist = Withdraw.objects.filter(userid_id = p_key).exclude(Wallet_type__in=[ 'Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet','Bot_Referral_wallet','trade_withdraw_wallet','Trade_Referral_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    try:
      tot_withdraw_user_qs = obj_withdraw_hist
    except:
      tot_withdraw_user_qs = ""
    w_page_4 = self.request.GET.get('pageno4', 1)
    w_paginator_4 = Paginator(tot_withdraw_user_qs, 5)
    try:
        withdraw_hist_qs = w_paginator_4.page(w_page_4)
    except PageNotAnInteger:
        withdraw_hist_qs =w_paginator_4.page(1)
    except EmptyPage:
        withdraw_hist_qs = w_paginator_4.page(w_paginator_4.num_pages)

    context['withdraw_hist_qs'] = withdraw_hist_qs
    context["withdraw_endpage"] = withdraw_hist_qs.number+1
    context["withdraw_startpage"] = withdraw_hist_qs.number-1
    context['withdraw_start_value'] = withdraw_hist_qs.start_index()
    context['withdraw_end_value'] = withdraw_hist_qs.end_index()
    context['withdraw_usr_count'] = obj_withdraw_hist.count()
    context["withdraw_dict_users"] = json.dumps(withdraw_dict_users)

     
    try:
      ref_user = self.request.GET['name']
    except:
      ref_user = ""


    ref_usr = 0
    ref_count = 0
    ref_dict_users = {}
    ref_start_page = self.request.GET.get('pageno5', 1)
    ref_end_value = int(ref_start_page) * 5
    ref_start_value = int(ref_end_value) - 4
    try:
      if ref_user:
        obj_ref_hist = MPRewardHistory.objects.filter(user_id = p_key).filter(referral_id__icontains = ref_user).order_by('-id')
        for i in obj_ref_hist:
          
          ref_usr = ref_usr + 1
          ref_list_usr = {}
          if ref_start_value <= ref_usr <= ref_end_value:
            ref_count = ref_count + 1
            # ref_list_usr["id"] = str(p_key)
            ref_list_usr["id"] = i.id
            ref_list_usr["username"] = str(i.user.Name)
            ref_list_usr["ref_id"] = i.referral_id
            ref_list_usr["reward_amt"] = i.reward
            ref_list_usr["date"] = (str(i.created_on))
            ref_list_usr["pageno"] = ref_start_page
            ref_list_usr["sno"] = ref_usr
            ref_dict_users[ref_count] = ref_list_usr
        
      else:
        obj_ref_hist = MPRewardHistory.objects.filter(user_id = p_key).order_by('-id')
        for i in obj_ref_hist:
          ref_usr = ref_usr + 1
          ref_list_usr = {}
          if ref_start_value <= ref_usr <= ref_end_value:
            ref_count = ref_count + 1
            ref_list_usr["id"] = i.id
            ref_list_usr["username"] = str(i.user.Name)
            ref_list_usr["ref_id"] = i.referral_id
            ref_list_usr["reward_amt"] = i.reward
            ref_list_usr["date"] = (str(i.created_on))
            ref_list_usr["pageno"] = ref_start_page
            ref_list_usr["sno"] = ref_usr 
            ref_dict_users[ref_count] = ref_list_usr
        

      context['ref_usr_count'] = obj_ref_hist.count()
    except:
      obj_ref_hist = ""
      context['ref_usr_count'] = 0
    try:
      tot_ref_user_qs = obj_ref_hist
    except:
      tot_ref_user_qs = ""
    w_page_5 = self.request.GET.get('pageno5', 1)
    w_paginator_5 = Paginator(tot_ref_user_qs, 5) 
    try:
        ref_hist_qs = w_paginator_5.page(w_page_5)
    except PageNotAnInteger:
        ref_hist_qs =w_paginator_5.page(1)
    except EmptyPage:
        ref_hist_qs = w_paginator_5.page(w_paginator_5.num_pages)

    context['ref_hist_qs'] = ref_hist_qs
    context["ref_endpage"] = ref_hist_qs.number+1
    context["ref_startpage"] = ref_hist_qs.number-1
    context['ref_start_value'] = ref_hist_qs.start_index()
    context['ref_end_value'] = ref_hist_qs.end_index()
    context["ref_dict_users"] = json.dumps(ref_dict_users)

    wall_usr = 0
    wall_count = 0
    wall_dict_users = {}
    wall_start_page = self.request.GET.get('pageno6', 1)
    wall_end_value = int(wall_start_page) * 5
    wall_start_value = int(wall_end_value) - 4
    try:
      obj_wall_hist = UserCashWallet.objects.filter(userid_id = p_key).order_by('-id')
      for i in obj_wall_hist:
        wall_usr = wall_usr + 1
        wall_list_usr = {}
        if wall_start_value <= wall_usr <= wall_end_value:
          wall_count = wall_count + 1
          wall_list_usr["username"] = str(i.userid.Name)
          if i.MPHealth == 0.00000000:
            wall_list_usr["health_reward"] = int(i.MPHealth)
          else:
            wall_list_usr["health_reward"] = str(i.MPHealth)
          if i.MPReward == 0.00000000:
            wall_list_usr["ref_reward"] = int(i.MPReward)
          else:
            wall_list_usr["ref_reward"] = str(i.MPReward)
          wall_list_usr["pageno"] = wall_start_page
          wall_list_usr["sno"] = wall_usr
          wall_dict_users[wall_count] = wall_list_usr
    except:
      obj_wall_hist = ""
    try:
      tot_wall_user_qs = obj_wall_hist
    except:
      tot_wall_user_qs = ""
    w_page_6 = self.request.GET.get('pageno6', 1)
    w_paginator_6 = Paginator(tot_wall_user_qs, 5)
    try:
        wall_hist_qs = w_paginator_6.page(w_page_6)
    except PageNotAnInteger:
        wall_hist_qs =w_paginator_6.page(1)
    except EmptyPage:
        wall_hist_qs = w_paginator_6.page(w_paginator_6.num_pages)

    context['wall_hist_qs'] = wall_hist_qs
    context["wall_endpage"] = wall_hist_qs.number+1
    context["wall_startpage"] = wall_hist_qs.number-1
    context['wall_start_value'] = wall_hist_qs.start_index()
    context['wall_end_value'] = wall_hist_qs.end_index()
    context['wall_usr_count'] = obj_wall_hist.count()
    context["wall_dict_users"] = json.dumps(wall_dict_users)


    login_usr = 0
    login_count = 0
    login_dict_users = {}
    login_start_page = self.request.GET.get('pageno7', 1)
    login_end_value = int(login_start_page) * 5
    login_start_value = int(login_end_value) - 4
    try:
      obj_login_hist = LoginHistory.objects.filter(user_id = p_key).order_by('-created_on')
      for i in obj_login_hist:
        login_usr = login_usr + 1
        login_list_usr = {}
        if login_start_value <= login_usr <= login_end_value:
          login_count = login_count + 1
          login_list_usr["username"] = str(i.user.Name)
          login_list_usr["created_on"] = str(i.created_on)
          login_list_usr["modified_on"] = str(i.modified_on)
          login_list_usr["pageno"] = login_start_page
          login_list_usr["sno"] = login_usr
          login_dict_users[login_count] = login_list_usr
    except:
      obj_login_hist = ""
    try:
      tot_login_user_qs = obj_login_hist
    except:
      tot_login_user_qs = ""
    w_page_7 = self.request.GET.get('pageno7', 1)
    w_paginator_7 = Paginator(tot_login_user_qs, 5)
    try:
        login_hist_qs = w_paginator_7.page(w_page_7)
    except PageNotAnInteger:
        login_hist_qs =w_paginator_7.page(1)
    except EmptyPage:
        login_hist_qs = w_paginator_7.page(w_paginator_7.num_pages)

    context['login_hist_qs'] = login_hist_qs
    context["login_endpage"] = login_hist_qs.number+1
    context["login_startpage"] = login_hist_qs.number-1
    context['login_start_value'] = login_hist_qs.start_index()
    context['login_end_value'] = login_hist_qs.end_index()
    context['login_usr_count'] = obj_login_hist.count()
    context["login_dict_users"] = json.dumps(login_dict_users)

    
    context['Title'] = 'MPlan History Table'
    context["Btn_url"] = "trade_admin_auth:List_User_Management"
    return context


  @method_decorator(check_group_icon_menu("History"))
  def dispatch(self, *args, **kwargs):
    return super(MPlanHistoryManagementTable, self).dispatch(*args, **kwargs)



##############################################                   ##########################################
##############################################    Burn History   ##########################################

class BurnHistoryManagementTable(TemplateView):
  template_name = "trade_admin_auth/burn_history_table.html"

  def get_context_data(self, **kwargs):
    context = super(BurnHistoryManagementTable, self).get_context_data(**kwargs)
    p_key = self.kwargs['pk']
    context["p_key"] = p_key
    try:
      user_obj = User_Management.objects.get(id = p_key)
    except:
      user_obj = ""

    try:
      p_no = self.request.GET['pageno']
    except:
      p_no=1
    try:
      p_no1 = self.request.GET['pageno1']
    except:
      p_no1=1 
    try:
      p_no2 = self.request.GET['pageno2']
    except:
      p_no2=1
    try:
      p_no3 = self.request.GET['pageno3']
    except:
      p_no3=1
    try:
      p_no4 = self.request.GET['pageno4']
    except:
      p_no4=1   
    try:
      p_no5 = self.request.GET['pageno5']
    except:
      p_no5=1 
    try:
      p_no6 = self.request.GET['pageno6']
    except:
      p_no6=1
    try:
      p_no7 = self.request.GET['pageno7']
    except:
      p_no7=1

    context['p_no'] = p_no
    context['p_no1'] = p_no1
    context['p_no2'] = p_no2
    context['p_no3'] = p_no3
    context['p_no4'] = p_no4
    context['p_no5'] = p_no5
    context['p_no6'] = p_no6
    context['p_no7'] = p_no7

    try:
      s_step = self.request.GET['steps']
    except:
      s_step = ""

    

    s_usr = 0
    s_count = 0
    s_dict_users = {}
    s_start_page = self.request.GET.get('pageno', 1)
    s_end_value = int(s_start_page) * 5
    s_start_value = int(s_end_value) - 4
    
    if s_step:
      obj_step_hist = Steps_history.objects.filter(user_id = p_key).filter(steps__icontains = s_step).order_by('-id')
      for i in obj_step_hist:
        
        s_usr = s_usr + 1
        s_list_usr = {}
        if s_start_value <= s_usr <= s_end_value:
          s_count = s_count + 1
          s_list_usr["username"] = str(i.user.Name)
          s_list_usr["steps"] = (i.steps)
          s_list_usr["date"] = (str(i.created_on))
          s_list_usr["pageno"] = s_start_page
          s_list_usr["sno"] = s_usr
          s_dict_users[s_count] = s_list_usr
    else:
      obj_step_hist = Steps_history.objects.filter(user_id = p_key).order_by('-id')
      for i in obj_step_hist:
      
        s_usr = s_usr + 1
        s_list_usr = {}
        if s_start_value <= s_usr <= s_end_value:
          s_count = s_count + 1
          s_list_usr["username"] = str(i.user.Name)
          s_list_usr["steps"] = (i.steps)
          s_list_usr["date"] = (str(i.created_on))
          s_list_usr["pageno"] = s_start_page
          s_list_usr["sno"] = s_usr
          s_dict_users[s_count] = s_list_usr

    try:
      tot_step_user_qs = obj_step_hist
    except:
      tot_step_user_qs = ""
    w_page = self.request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_step_user_qs, 5)
    
    try:
        step_hist_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        step_hist_qs =w_paginator.page(1)
    except EmptyPage:
        step_hist_qs = w_paginator.page(w_paginator.num_pages)
    
    
    context['step_hist_qs'] = step_hist_qs
    context["s_endpage"] = step_hist_qs.number+1
    context["s_startpage"] = step_hist_qs.number-1
    context['s_start_value'] = step_hist_qs.start_index()
    context['s_end_value'] = step_hist_qs.end_index()
    context['s_usr_count'] = obj_step_hist.count()
    context["s_dict_users"] = json.dumps(s_dict_users)



    try:
      r_step = self.request.GET['r_steps']
    except:
      r_step = ""

    r_usr = 0
    r_count = 0
    r_dict_users = {}
    r_start_page = self.request.GET.get('pageno1', 1)
    r_end_value = int(r_start_page) * 5
    r_start_value = int(r_end_value) - 4
    if r_step:
      obj_rew_hist = BurnRewardHistory.objects.filter(user_id = p_key).filter(steps__icontains = r_step).order_by('-id')
      for i in obj_rew_hist:
        r_usr = r_usr + 1
        r_list_usr = {}
        if r_start_value <= r_usr <= r_end_value:
          r_count = r_count + 1
          r_list_usr["username"] = str(i.user.Name)
          r_list_usr["steps"] = 3000
          r_list_usr["Reward"] = str(i.reward)
          r_list_usr["date"] = (str(i.created_on))
          r_list_usr["claim_date"] = (str(i.modified_on))
          r_list_usr["pageno"] = r_start_page
          r_list_usr["sno"] = r_usr
          r_dict_users[r_count] = r_list_usr
    else:
      obj_rew_hist = BurnRewardHistory.objects.filter(user_id = p_key).order_by('-id')
      for i in obj_rew_hist:
        r_usr = r_usr + 1
        r_list_usr = {}
        if r_start_value <= r_usr <= r_end_value:
          r_count = r_count + 1
          r_list_usr["username"] = str(i.user.Name)
          r_list_usr["steps"] = 3000
          r_list_usr["Reward"] = str(i.reward)
          r_list_usr["date"] = (str(i.created_on))
          r_list_usr["claim_date"] = (str(i.modified_on))
          r_list_usr["pageno"] = r_start_page
          r_list_usr["sno"] = r_usr
          r_dict_users[r_count] = r_list_usr
    try:
      tot_rew_user_qs = obj_rew_hist
    except:
      tot_rew_user_qs = ""
    w_page_1 = self.request.GET.get('pageno1', 1)
    w_paginator_1 = Paginator(tot_rew_user_qs, 5)
    try:
        rew_hist_qs = w_paginator_1.page(w_page_1)
    except PageNotAnInteger:
        rew_hist_qs =w_paginator_1.page(1)
    except EmptyPage:
        rew_hist_qs = w_paginator_1.page(w_paginator_1.num_pages)

    context['rew_hist_qs'] = rew_hist_qs
    context["r_endpage"] = rew_hist_qs.number+1
    context["r_startpage"] = rew_hist_qs.number-1
    context['r_start_value'] = rew_hist_qs.start_index()
    context['r_end_value'] = rew_hist_qs.end_index()
    context['r_usr_count'] = obj_rew_hist.count()
    context["r_dict_users"] = json.dumps(r_dict_users)

    pre_usr = 0
    pre_count = 0
    pre_dict_users = {}
    pre_start_page = self.request.GET.get('pageno', 1)
    pre_end_value = int(pre_start_page) * 5
    pre_start_value = int(pre_end_value) - 4
    
    obj_pre_hist = Boat_wallet.objects.filter(user = p_key,type="User Create").order_by('-id')
    for i in obj_pre_hist: 
      pre_usr = pre_usr + 1
      pre_list_usr = {}
      if pre_start_value <= pre_usr <= pre_end_value:
        pre_count = pre_count + 1
        pre_list_usr["username"] = str(user_obj.Name)
        pre_list_usr["create_type"] = (i.create_type)
        pre_list_usr["steps"] = (i.Amount_USDT)
        pre_list_usr["jw"] = (i.Amount_JW)
        pre_list_usr["Hash"] = (i.Hash)
        pre_list_usr["date"] = (str(i.created_on))
        pre_list_usr["pageno"] = pre_start_page
        pre_list_usr["sno"] = pre_usr
        pre_dict_users[pre_count] = pre_list_usr
    try:
      tot_step_user_qs = obj_pre_hist
    except:
      tot_step_user_qs = ""
    w_page = self.request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_step_user_qs, 5)
    
    try:
        step_hist_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        step_hist_qs =w_paginator.page(1)
    except EmptyPage:
        step_hist_qs = w_paginator.page(w_paginator.num_pages)
    
    
    context['step_hist_qs'] = step_hist_qs
    context["pre_endpage"] = step_hist_qs.number+1
    context["pre_startpage"] = step_hist_qs.number-1
    context['pre_start_value'] = step_hist_qs.start_index()
    context['pre_end_value'] = step_hist_qs.end_index()
    context['pre_usr_count'] = obj_pre_hist.count()
    context["pre_dict_users"] = json.dumps(pre_dict_users)


    pre_r_usr = 0
    pre_r_count = 0
    pre_req_dict_users = {}
    pre_r_start_page = self.request.GET.get('pageno1', 1)
    pre_r_end_value = int(pre_r_start_page) * 5
    pre_r_start_value = int(pre_r_end_value) - 4
    obj_rew_hist = Boat_wallet.objects.filter(user = p_key).exclude(type="User Create").order_by('-created_on')
    for i in obj_rew_hist:
      pre_r_usr = pre_r_usr + 1
      r_list_usr = {}
      if pre_r_start_value <= pre_r_usr <= pre_r_end_value:
        pre_r_count = pre_r_count + 1
        r_list_usr["username"] = str(user_obj.Name)
        r_list_usr["steps"] = (i.type)
        r_list_usr["Reward"] = str(i.Amount_USDT)
        r_list_usr["date"] = (str(i.created_on))
        r_list_usr["pageno"] = pre_r_start_page
        r_list_usr["sno"] = pre_r_usr
        pre_req_dict_users[pre_r_count] = r_list_usr
    try:
      tot_rew_user_qs = obj_rew_hist
    except:
      tot_rew_user_qs = ""
    w_page_1 = self.request.GET.get('pageno1', 1)
    w_paginator_1 = Paginator(tot_rew_user_qs, 5)
    try:
        rew_hist_qs = w_paginator_1.page(w_page_1)
    except PageNotAnInteger:
        rew_hist_qs =w_paginator_1.page(1)
    except EmptyPage:
        rew_hist_qs = w_paginator_1.page(w_paginator_1.num_pages)

    context['rew_hist_qs'] = rew_hist_qs
    context["pre_r_endpage"] = rew_hist_qs.number+1
    context["pre_r_startpage"] = rew_hist_qs.number-1
    context['pre_r_start_value'] = rew_hist_qs.start_index()
    context['pre_r_end_value'] = rew_hist_qs.end_index()
    context['pre_r_usr_count'] = obj_rew_hist.count()
    context["pre_req_dict_users"] = json.dumps(pre_req_dict_users)

    try:
      two_x_step = self.request.GET['tx_steps']
    except:
      two_x_step = ""

    tx_usr = 0
    tx_count = 0
    tx_dict_users = {}
    tx_start_page = self.request.GET.get('pageno2', 1)
    tx_end_value = int(tx_start_page) * 5
    tx_start_value = int(tx_end_value) - 4
    if two_x_step:
      obj_two_x_hist = User_2x_Boost.objects.filter(userid_id = p_key).filter(user_step_count__icontains = two_x_step).order_by('-id')
      for i in obj_two_x_hist:
        tx_usr = tx_usr + 1
        tx_list_usr = {}
        if tx_start_value <= tx_usr <= tx_end_value:
          tx_count = tx_count + 1
          tx_list_usr["username"] = str(i.userid.Name)
          tx_list_usr["steps"] = (i.user_step_count)
          tx_list_usr["Reward"] = str(i.reward_per_step)
          tx_list_usr["date"] = (str(i.created_on))
          tx_list_usr["pageno"] = tx_start_page
          tx_list_usr["sno"] = tx_usr
          tx_dict_users[tx_count] = tx_list_usr
    else:
      obj_two_x_hist = User_2x_Boost.objects.filter(userid_id = p_key).order_by('-id')
      for i in obj_two_x_hist:
        tx_usr = tx_usr + 1
        tx_list_usr = {}
        if tx_start_value <= tx_usr <= tx_end_value:
          tx_count = tx_count + 1
          tx_list_usr["username"] = str(i.userid.Name)
          tx_list_usr["steps"] = (i.user_step_count)
          tx_list_usr["Reward"] = str(i.reward_per_step)
          tx_list_usr["date"] = (str(i.created_on))
          tx_list_usr["pageno"] = tx_start_page
          tx_list_usr["sno"] = tx_usr
          tx_dict_users[tx_count] = tx_list_usr
    try:
      tot_tx_user_qs = obj_two_x_hist
    except:
      tot_tx_user_qs = ""
    w_page_2 = self.request.GET.get('pageno2', 1)
    w_paginator_2 = Paginator(tot_tx_user_qs, 5)
    try:
        two_x_hist_qs = w_paginator_2.page(w_page_2)
    except PageNotAnInteger:
        two_x_hist_qs =w_paginator_2.page(1)
    except EmptyPage:
        two_x_hist_qs = w_paginator_2.page(w_paginator_2.num_pages)

    context['two_x_hist_qs'] = two_x_hist_qs
    context["tx_endpage"] = two_x_hist_qs.number+1
    context["tx_startpage"] = two_x_hist_qs.number-1
    context['tx_start_value'] = two_x_hist_qs.start_index()
    context['tx_end_value'] = two_x_hist_qs.end_index()
    context['tx_usr_count'] = obj_two_x_hist.count()
    context["tx_dict_users"] = json.dumps(tx_dict_users)



    try:
      buy_plan_name = self.request.GET['plan_name']
    except:
      buy_plan_name = ""

    plan_usr = 0
    plan_count = 0
    plan_dict_users = {}
    plan_start_page = self.request.GET.get('pageno3', 1)
    plan_end_value = int(plan_start_page) * 5
    plan_start_value = int(plan_end_value) - 4
    Comp = BurntoearnHistory.objects.filter(email_id = p_key).order_by('-id')
    if buy_plan_name:
      obj_plan_hist = BurntoearnHistory.objects.filter(email_id = p_key).order_by('-id')
      for i in obj_plan_hist:
        plan_usr = plan_usr + 1
        plan_list_usr = {}
        if plan_start_value <= plan_usr <= plan_end_value:
          plan_count = plan_count + 1
          plan_list_usr["id"] = str(p_key)
          plan_list_usr["username"] = str(i.user)
          plan_list_usr["plan"] = "Burn"#int(i.purchase_amount)
          plan_list_usr["plan_amt"] = int(i.plan_amount)
          plan_list_usr["start_date"] = (str(i.plan_start_date))
          # plan_list_usr["end_date"] = (str(user_obj.plan_end_date))
          plan_list_usr["wallet_type"] = (str(i.Transaction_Hash))
          # plan_list_usr["health_max"] = (str(user_obj.Health_Withdraw_max_value))
          # plan_list_usr["health_min"] = (str(user_obj.Health_Withdraw_min_value))
          # plan_list_usr["referral_max"] = (str(user_obj.Referral_Withdraw_max_value))
          # plan_list_usr["referral_min"] = (str(user_obj.Referral_Withdraw_min_value))
          plan_list_usr["hash"] = (str(i.Transaction_Hash))
          plan_list_usr["buy_type"] = (i.currency)
          plan_list_usr["TradeBwa"] = str(user_obj.MPlanBWA)
          # plan_list_usr["hash"] = (str(i.User_plan_validation))
          plan_list_usr["pageno"] = plan_start_page
          plan_list_usr["sno"] = plan_usr
          plan_dict_users[plan_count] = plan_list_usr
    else:
      obj_plan_hist = BurntoearnHistory.objects.filter(email_id = p_key).order_by('-id')
      for i in obj_plan_hist:
        plan_usr = plan_usr + 1
        plan_list_usr = {}
        if plan_start_value <= plan_usr <= plan_end_value:
          plan_count = plan_count + 1
          plan_list_usr["id"] = str(p_key)
          plan_list_usr["username"] = str(i.user)
          plan_list_usr["plan"] = "Burn"#int(i.purchase_amount)
          plan_list_usr["plan_amt"] = int(i.plan_amount)
          # plan_list_usr["price"] = str(user_obj.fixed_status)
          plan_list_usr["start_date"] = (str(i.plan_start_date))
          # plan_list_usr["end_date"] = (str(user_obj.plan_end_date))
          plan_list_usr["wallet_type"] = (str(i.Transaction_Hash))
          # plan_list_usr["health_max"] = (str(user_obj.Health_Withdraw_max_value))
          # plan_list_usr["health_min"] = (str(user_obj.Health_Withdraw_min_value))
          # plan_list_usr["referral_max"] = (str(user_obj.Referral_Withdraw_max_value))
          # plan_list_usr["referral_min"] = (str(user_obj.Referral_Withdraw_min_value))
          plan_list_usr["hash"] = (str(i.Transaction_Hash))
          plan_list_usr["buy_type"] = (i.currency)
          plan_list_usr["TradeBwa"] = str(user_obj.MPlanBWA)
          plan_list_usr["pageno"] = plan_start_page
          plan_list_usr["sno"] = plan_usr
          plan_dict_users[plan_count] = plan_list_usr
    try:
      tot_plan_user_qs = obj_plan_hist
    except:
      tot_plan_user_qs = ""
    w_page_3 = self.request.GET.get('pageno3', 1)
    w_paginator_3 = Paginator(tot_plan_user_qs, 5)
    try:
        plan_hist_qs = w_paginator_3.page(w_page_3)
    except PageNotAnInteger:
        plan_hist_qs =w_paginator_3.page(1)
    except EmptyPage:
        plan_hist_qs = w_paginator_3.page(w_paginator_3.num_pages)\

    context['plan_hist_qs'] = plan_hist_qs
    context["plan_endpage"] = plan_hist_qs.number+1
    context["plan_startpage"] = plan_hist_qs.number-1
    context['plan_start_value'] = plan_hist_qs.start_index()
    context['plan_end_value'] = plan_hist_qs.end_index()
    context['plan_usr_count'] = obj_plan_hist.count()
    context["plan_dict_users"] = json.dumps(plan_dict_users)


    try:
      usr_addrs = self.request.GET['address']
    except:
      usr_addrs = ""

    try:
      status = self.request.GET['status']
     
      if status == 'Active':
       
        status = 0
      if status == 'Completed':
        status = 1
      if status == 'Cancelled':
        status = 2
    except:
      status = ""

    try:
      date = self.request.GET['date']
    except:
      date = ""

    withdraw_usr = 0
    withdraw_count = 0
    withdraw_dict_users = {}
    withdraw_start_page = self.request.GET.get('pageno4', 1)
    withdraw_end_value = int(withdraw_start_page) * 5
    withdraw_start_value = int(withdraw_end_value) - 4
    if usr_addrs and status and date:
      obj_withdraw_hist = BurnWithdraw.objects.filter(userid_id = p_key).filter(Q(Address__icontains = usr_addrs) and Q(status__icontains = status) and Q(created_on__date__icontains = date)).exclude(Wallet_type__in=[ 'Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet','Bot_Referral_wallet','trade_withdraw_wallet','Trade_Referral_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    elif usr_addrs:
      obj_withdraw_hist = BurnWithdraw.objects.filter(userid_id = p_key).filter(Address__icontains = usr_addrs).exclude(Wallet_type__in=['Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet','Bot_Referral_wallet','trade_withdraw_wallet','Trade_Referral_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on)) 
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    elif date:
      obj_withdraw_hist = BurnWithdraw.objects.filter(userid_id = p_key).filter(created_on__date__icontains = date).exclude(Wallet_type__in=['Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet','Bot_Referral_wallet','trade_withdraw_wallet','Trade_Referral_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    elif status:
      obj_withdraw_hist = WiBurnWithdrawthdraw.objects.filter(userid_id = p_key).filter(status__icontains = status).exclude(Wallet_type__in=['Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet','Bot_Referral_wallet','trade_withdraw_wallet','Trade_Referral_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    else:
      obj_withdraw_hist = BurnWithdraw.objects.filter(userid_id = p_key).exclude(Wallet_type__in=[ 'Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet','Bot_Referral_wallet','trade_withdraw_wallet','Trade_Referral_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    try:
      tot_withdraw_user_qs = obj_withdraw_hist
    except:
      tot_withdraw_user_qs = ""
    w_page_4 = self.request.GET.get('pageno4', 1)
    w_paginator_4 = Paginator(tot_withdraw_user_qs, 5)
    try:
        withdraw_hist_qs = w_paginator_4.page(w_page_4)
    except PageNotAnInteger:
        withdraw_hist_qs =w_paginator_4.page(1)
    except EmptyPage:
        withdraw_hist_qs = w_paginator_4.page(w_paginator_4.num_pages)

    context['withdraw_hist_qs'] = withdraw_hist_qs
    context["withdraw_endpage"] = withdraw_hist_qs.number+1
    context["withdraw_startpage"] = withdraw_hist_qs.number-1
    context['withdraw_start_value'] = withdraw_hist_qs.start_index()
    context['withdraw_end_value'] = withdraw_hist_qs.end_index()
    context['withdraw_usr_count'] = obj_withdraw_hist.count()
    context["withdraw_dict_users"] = json.dumps(withdraw_dict_users)

     
    try:
      ref_user = self.request.GET['name']
    except:
      ref_user = ""


    ref_usr = 0
    ref_count = 0
    ref_dict_users = {}
    ref_start_page = self.request.GET.get('pageno5', 1)
    ref_end_value = int(ref_start_page) * 5
    ref_start_value = int(ref_end_value) - 4
    try:
      if ref_user:
        obj_ref_hist = BurnRewardHistory.objects.filter(user_id = p_key).filter(referral_id__icontains = ref_user).order_by('-id')
        for i in obj_ref_hist:
          
          ref_usr = ref_usr + 1
          ref_list_usr = {}
          if ref_start_value <= ref_usr <= ref_end_value:
            ref_count = ref_count + 1
            # ref_list_usr["id"] = str(p_key)
            ref_list_usr["id"] = i.id
            ref_list_usr["username"] = str(i.user.Name)
            ref_list_usr["ref_id"] = i.referral_id
            ref_list_usr["reward_amt"] = i.reward
            ref_list_usr["date"] = (str(i.created_on))
            ref_list_usr["pageno"] = ref_start_page
            ref_list_usr["sno"] = ref_usr
            ref_dict_users[ref_count] = ref_list_usr
        
      else:
        obj_ref_hist = BurnRewardHistory.objects.filter(user_id = p_key).order_by('-id')
        for i in obj_ref_hist:
          ref_usr = ref_usr + 1
          ref_list_usr = {}
          if ref_start_value <= ref_usr <= ref_end_value:
            ref_count = ref_count + 1
            ref_list_usr["id"] = i.id
            ref_list_usr["username"] = str(i.user.Name)
            ref_list_usr["ref_id"] = i.referral_id
            ref_list_usr["reward_amt"] = i.reward
            ref_list_usr["date"] = (str(i.created_on))
            ref_list_usr["pageno"] = ref_start_page
            ref_list_usr["sno"] = ref_usr 
            ref_dict_users[ref_count] = ref_list_usr
        

      context['ref_usr_count'] = obj_ref_hist.count()
    except:
      obj_ref_hist = ""
      context['ref_usr_count'] = 0
    try:
      tot_ref_user_qs = obj_ref_hist
    except:
      tot_ref_user_qs = ""
    w_page_5 = self.request.GET.get('pageno5', 1)
    w_paginator_5 = Paginator(tot_ref_user_qs, 5) 
    try:
        ref_hist_qs = w_paginator_5.page(w_page_5)
    except PageNotAnInteger:
        ref_hist_qs =w_paginator_5.page(1)
    except EmptyPage:
        ref_hist_qs = w_paginator_5.page(w_paginator_5.num_pages)

    context['ref_hist_qs'] = ref_hist_qs
    context["ref_endpage"] = ref_hist_qs.number+1
    context["ref_startpage"] = ref_hist_qs.number-1
    context['ref_start_value'] = ref_hist_qs.start_index()
    context['ref_end_value'] = ref_hist_qs.end_index()
    context["ref_dict_users"] = json.dumps(ref_dict_users)

    wall_usr = 0
    wall_count = 0
    wall_dict_users = {}
    wall_start_page = self.request.GET.get('pageno6', 1)
    wall_end_value = int(wall_start_page) * 5
    wall_start_value = int(wall_end_value) - 4
    try:
      obj_wall_hist = UserCashWallet.objects.filter(userid_id = p_key).order_by('-id')
      for i in obj_wall_hist:
        wall_usr = wall_usr + 1
        wall_list_usr = {}
        if wall_start_value <= wall_usr <= wall_end_value:
          wall_count = wall_count + 1
          wall_list_usr["username"] = str(i.userid.Name)
          if i.Burnreward == 0.00000000:
            wall_list_usr["burn_reward"] = int(i.Burnreward)
          else:
            wall_list_usr["burn_reward"] = str(i.Burnreward)
          if i.Burnreff == 0.00000000:
            wall_list_usr["burn_reff"] = int(i.Burnreff)
          else:
            wall_list_usr["burn_reff"] = str(i.Burnreff)  
          wall_list_usr["pageno"] = wall_start_page
          wall_list_usr["sno"] = wall_usr
          wall_dict_users[wall_count] = wall_list_usr
    except:
      obj_wall_hist = ""
    try:
      tot_wall_user_qs = obj_wall_hist
    except:
      tot_wall_user_qs = ""
    w_page_6 = self.request.GET.get('pageno6', 1)
    w_paginator_6 = Paginator(tot_wall_user_qs, 5)
    try:
        wall_hist_qs = w_paginator_6.page(w_page_6)
    except PageNotAnInteger:
        wall_hist_qs =w_paginator_6.page(1)
    except EmptyPage:
        wall_hist_qs = w_paginator_6.page(w_paginator_6.num_pages)

    context['wall_hist_qs'] = wall_hist_qs
    context["wall_endpage"] = wall_hist_qs.number+1
    context["wall_startpage"] = wall_hist_qs.number-1
    context['wall_start_value'] = wall_hist_qs.start_index()
    context['wall_end_value'] = wall_hist_qs.end_index()
    context['wall_usr_count'] = obj_wall_hist.count()
    context["wall_dict_users"] = json.dumps(wall_dict_users)


    login_usr = 0
    login_count = 0
    login_dict_users = {}
    login_start_page = self.request.GET.get('pageno7', 1)
    login_end_value = int(login_start_page) * 5
    login_start_value = int(login_end_value) - 4
    try:
      obj_login_hist = LoginHistory.objects.filter(user_id = p_key).order_by('-created_on')
      for i in obj_login_hist:
        login_usr = login_usr + 1
        login_list_usr = {}
        if login_start_value <= login_usr <= login_end_value:
          login_count = login_count + 1
          login_list_usr["username"] = str(i.user.Name)
          login_list_usr["created_on"] = str(i.created_on)
          login_list_usr["modified_on"] = str(i.modified_on)
          login_list_usr["pageno"] = login_start_page
          login_list_usr["sno"] = login_usr
          login_dict_users[login_count] = login_list_usr
    except:
      obj_login_hist = ""
    try:
      tot_login_user_qs = obj_login_hist
    except:
      tot_login_user_qs = ""
    w_page_7 = self.request.GET.get('pageno7', 1)
    w_paginator_7 = Paginator(tot_login_user_qs, 5)
    try:
        login_hist_qs = w_paginator_7.page(w_page_7)
    except PageNotAnInteger:
        login_hist_qs =w_paginator_7.page(1)
    except EmptyPage:
        login_hist_qs = w_paginator_7.page(w_paginator_7.num_pages)

    context['login_hist_qs'] = login_hist_qs
    context["login_endpage"] = login_hist_qs.number+1
    context["login_startpage"] = login_hist_qs.number-1
    context['login_start_value'] = login_hist_qs.start_index()
    context['login_end_value'] = login_hist_qs.end_index()
    context['login_usr_count'] = obj_login_hist.count()
    context["login_dict_users"] = json.dumps(login_dict_users)

    
    context['Title'] = 'Burn History Table'
    context["Btn_url"] = "trade_admin_auth:List_User_Management"
    return context


  @method_decorator(check_group_icon_menu("History"))
  def dispatch(self, *args, **kwargs):
    return super(BurnHistoryManagementTable, self).dispatch(*args, **kwargs)



############## JWC ###########


class BurnjwcHistoryManagementTable(TemplateView):
  template_name = "trade_admin_auth/burnjwc_history_table.html"

  def get_context_data(self, **kwargs):
    context = super(BurnjwcHistoryManagementTable, self).get_context_data(**kwargs)
    p_key = self.kwargs['pk']
    context["p_key"] = p_key
    try:
      user_obj = User_Management.objects.get(id = p_key)
    except:
      user_obj = ""

    try:
      p_no = self.request.GET['pageno']
    except:
      p_no=1
    try:
      p_no1 = self.request.GET['pageno1']
    except:
      p_no1=1 
    try:
      p_no2 = self.request.GET['pageno2']
    except:
      p_no2=1
    try:
      p_no3 = self.request.GET['pageno3']
    except:
      p_no3=1
    try:
      p_no4 = self.request.GET['pageno4']
    except:
      p_no4=1   
    try:
      p_no5 = self.request.GET['pageno5']
    except:
      p_no5=1 
    try:
      p_no6 = self.request.GET['pageno6']
    except:
      p_no6=1
    try:
      p_no7 = self.request.GET['pageno7']
    except:
      p_no7=1

    context['p_no'] = p_no
    context['p_no1'] = p_no1
    context['p_no2'] = p_no2
    context['p_no3'] = p_no3
    context['p_no4'] = p_no4
    context['p_no5'] = p_no5
    context['p_no6'] = p_no6
    context['p_no7'] = p_no7

    try:
      s_step = self.request.GET['steps']
    except:
      s_step = ""

    

    s_usr = 0
    s_count = 0
    s_dict_users = {}
    s_start_page = self.request.GET.get('pageno', 1)
    s_end_value = int(s_start_page) * 5
    s_start_value = int(s_end_value) - 4
    
    if s_step:
      obj_step_hist = Steps_history.objects.filter(user_id = p_key).filter(steps__icontains = s_step).order_by('-id')
      for i in obj_step_hist:
        
        s_usr = s_usr + 1
        s_list_usr = {}
        if s_start_value <= s_usr <= s_end_value:
          s_count = s_count + 1
          s_list_usr["username"] = str(i.user.Name)
          s_list_usr["steps"] = (i.steps)
          s_list_usr["date"] = (str(i.created_on))
          s_list_usr["pageno"] = s_start_page
          s_list_usr["sno"] = s_usr
          s_dict_users[s_count] = s_list_usr
    else:
      obj_step_hist = Steps_history.objects.filter(user_id = p_key).order_by('-id')
      for i in obj_step_hist:
      
        s_usr = s_usr + 1
        s_list_usr = {}
        if s_start_value <= s_usr <= s_end_value:
          s_count = s_count + 1
          s_list_usr["username"] = str(i.user.Name)
          s_list_usr["steps"] = (i.steps)
          s_list_usr["date"] = (str(i.created_on))
          s_list_usr["pageno"] = s_start_page
          s_list_usr["sno"] = s_usr
          s_dict_users[s_count] = s_list_usr

    try:
      tot_step_user_qs = obj_step_hist
    except:
      tot_step_user_qs = ""
    w_page = self.request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_step_user_qs, 5)
    
    try:
        step_hist_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        step_hist_qs =w_paginator.page(1)
    except EmptyPage:
        step_hist_qs = w_paginator.page(w_paginator.num_pages)
    
    
    context['step_hist_qs'] = step_hist_qs
    context["s_endpage"] = step_hist_qs.number+1
    context["s_startpage"] = step_hist_qs.number-1
    context['s_start_value'] = step_hist_qs.start_index()
    context['s_end_value'] = step_hist_qs.end_index()
    context['s_usr_count'] = obj_step_hist.count()
    context["s_dict_users"] = json.dumps(s_dict_users)



    try:
      r_step = self.request.GET['r_steps']
    except:
      r_step = ""

    r_usr = 0
    r_count = 0
    r_dict_users = {}
    r_start_page = self.request.GET.get('pageno1', 1)
    r_end_value = int(r_start_page) * 5
    r_start_value = int(r_end_value) - 4
    if r_step:
      obj_rew_hist = CBurnRewardHistory.objects.filter(user_id = p_key).filter(steps__icontains = r_step).order_by('-id')
      for i in obj_rew_hist:
        r_usr = r_usr + 1
        r_list_usr = {}
        if r_start_value <= r_usr <= r_end_value:
          r_count = r_count + 1
          r_list_usr["username"] = str(i.user.Name)
          r_list_usr["steps"] = 3000
          r_list_usr["Reward"] = str(i.reward)
          r_list_usr["date"] = (str(i.created_on))
          r_list_usr["claim_date"] = (str(i.modified_on))
          r_list_usr["pageno"] = r_start_page
          r_list_usr["sno"] = r_usr
          r_dict_users[r_count] = r_list_usr
    else:
      obj_rew_hist = CBurnRewardHistory.objects.filter(user_id = p_key).order_by('-id')
      for i in obj_rew_hist:
        r_usr = r_usr + 1
        r_list_usr = {}
        if r_start_value <= r_usr <= r_end_value:
          r_count = r_count + 1
          r_list_usr["username"] = str(i.user.Name)
          r_list_usr["steps"] = 3000
          r_list_usr["Reward"] = str(i.reward)
          r_list_usr["date"] = (str(i.created_on))
          r_list_usr["claim_date"] = (str(i.modified_on))
          r_list_usr["pageno"] = r_start_page
          r_list_usr["sno"] = r_usr
          r_dict_users[r_count] = r_list_usr
    try:
      tot_rew_user_qs = obj_rew_hist
    except:
      tot_rew_user_qs = ""
    w_page_1 = self.request.GET.get('pageno1', 1)
    w_paginator_1 = Paginator(tot_rew_user_qs, 5)
    try:
        rew_hist_qs = w_paginator_1.page(w_page_1)
    except PageNotAnInteger:
        rew_hist_qs =w_paginator_1.page(1)
    except EmptyPage:
        rew_hist_qs = w_paginator_1.page(w_paginator_1.num_pages)

    context['rew_hist_qs'] = rew_hist_qs
    context["r_endpage"] = rew_hist_qs.number+1
    context["r_startpage"] = rew_hist_qs.number-1
    context['r_start_value'] = rew_hist_qs.start_index()
    context['r_end_value'] = rew_hist_qs.end_index()
    context['r_usr_count'] = obj_rew_hist.count()
    context["r_dict_users"] = json.dumps(r_dict_users)

    pre_usr = 0
    pre_count = 0
    pre_dict_users = {}
    pre_start_page = self.request.GET.get('pageno', 1)
    pre_end_value = int(pre_start_page) * 5
    pre_start_value = int(pre_end_value) - 4
    
    obj_pre_hist = Boat_wallet.objects.filter(user = p_key,type="User Create").order_by('-id')
    for i in obj_pre_hist: 
      pre_usr = pre_usr + 1
      pre_list_usr = {}
      if pre_start_value <= pre_usr <= pre_end_value:
        pre_count = pre_count + 1
        pre_list_usr["username"] = str(user_obj.Name)
        pre_list_usr["create_type"] = (i.create_type)
        pre_list_usr["steps"] = (i.Amount_USDT)
        pre_list_usr["jw"] = (i.Amount_JW)
        pre_list_usr["Hash"] = (i.Hash)
        pre_list_usr["date"] = (str(i.created_on))
        pre_list_usr["pageno"] = pre_start_page
        pre_list_usr["sno"] = pre_usr
        pre_dict_users[pre_count] = pre_list_usr
    try:
      tot_step_user_qs = obj_pre_hist
    except:
      tot_step_user_qs = ""
    w_page = self.request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_step_user_qs, 5)
    
    try:
        step_hist_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        step_hist_qs =w_paginator.page(1)
    except EmptyPage:
        step_hist_qs = w_paginator.page(w_paginator.num_pages)
    
    
    context['step_hist_qs'] = step_hist_qs
    context["pre_endpage"] = step_hist_qs.number+1
    context["pre_startpage"] = step_hist_qs.number-1
    context['pre_start_value'] = step_hist_qs.start_index()
    context['pre_end_value'] = step_hist_qs.end_index()
    context['pre_usr_count'] = obj_pre_hist.count()
    context["pre_dict_users"] = json.dumps(pre_dict_users)


    pre_r_usr = 0
    pre_r_count = 0
    pre_req_dict_users = {}
    pre_r_start_page = self.request.GET.get('pageno1', 1)
    pre_r_end_value = int(pre_r_start_page) * 5
    pre_r_start_value = int(pre_r_end_value) - 4
    obj_rew_hist = Boat_wallet.objects.filter(user = p_key).exclude(type="User Create").order_by('-created_on')
    for i in obj_rew_hist:
      pre_r_usr = pre_r_usr + 1
      r_list_usr = {}
      if pre_r_start_value <= pre_r_usr <= pre_r_end_value:
        pre_r_count = pre_r_count + 1
        r_list_usr["username"] = str(user_obj.Name)
        r_list_usr["steps"] = (i.type)
        r_list_usr["Reward"] = str(i.Amount_USDT)
        r_list_usr["date"] = (str(i.created_on))
        r_list_usr["pageno"] = pre_r_start_page
        r_list_usr["sno"] = pre_r_usr
        pre_req_dict_users[pre_r_count] = r_list_usr
    try:
      tot_rew_user_qs = obj_rew_hist
    except:
      tot_rew_user_qs = ""
    w_page_1 = self.request.GET.get('pageno1', 1)
    w_paginator_1 = Paginator(tot_rew_user_qs, 5)
    try:
        rew_hist_qs = w_paginator_1.page(w_page_1)
    except PageNotAnInteger:
        rew_hist_qs =w_paginator_1.page(1)
    except EmptyPage:
        rew_hist_qs = w_paginator_1.page(w_paginator_1.num_pages)

    context['rew_hist_qs'] = rew_hist_qs
    context["pre_r_endpage"] = rew_hist_qs.number+1
    context["pre_r_startpage"] = rew_hist_qs.number-1
    context['pre_r_start_value'] = rew_hist_qs.start_index()
    context['pre_r_end_value'] = rew_hist_qs.end_index()
    context['pre_r_usr_count'] = obj_rew_hist.count()
    context["pre_req_dict_users"] = json.dumps(pre_req_dict_users)

    try:
      two_x_step = self.request.GET['tx_steps']
    except:
      two_x_step = ""

    tx_usr = 0
    tx_count = 0
    tx_dict_users = {}
    tx_start_page = self.request.GET.get('pageno2', 1)
    tx_end_value = int(tx_start_page) * 5
    tx_start_value = int(tx_end_value) - 4
    if two_x_step:
      obj_two_x_hist = User_2x_Boost.objects.filter(userid_id = p_key).filter(user_step_count__icontains = two_x_step).order_by('-id')
      for i in obj_two_x_hist:
        tx_usr = tx_usr + 1
        tx_list_usr = {}
        if tx_start_value <= tx_usr <= tx_end_value:
          tx_count = tx_count + 1
          tx_list_usr["username"] = str(i.userid.Name)
          tx_list_usr["steps"] = (i.user_step_count)
          tx_list_usr["Reward"] = str(i.reward_per_step)
          tx_list_usr["date"] = (str(i.created_on))
          tx_list_usr["pageno"] = tx_start_page
          tx_list_usr["sno"] = tx_usr
          tx_dict_users[tx_count] = tx_list_usr
    else:
      obj_two_x_hist = User_2x_Boost.objects.filter(userid_id = p_key).order_by('-id')
      for i in obj_two_x_hist:
        tx_usr = tx_usr + 1
        tx_list_usr = {}
        if tx_start_value <= tx_usr <= tx_end_value:
          tx_count = tx_count + 1
          tx_list_usr["username"] = str(i.userid.Name)
          tx_list_usr["steps"] = (i.user_step_count)
          tx_list_usr["Reward"] = str(i.reward_per_step)
          tx_list_usr["date"] = (str(i.created_on))
          tx_list_usr["pageno"] = tx_start_page
          tx_list_usr["sno"] = tx_usr
          tx_dict_users[tx_count] = tx_list_usr
    try:
      tot_tx_user_qs = obj_two_x_hist
    except:
      tot_tx_user_qs = ""
    w_page_2 = self.request.GET.get('pageno2', 1)
    w_paginator_2 = Paginator(tot_tx_user_qs, 5)
    try:
        two_x_hist_qs = w_paginator_2.page(w_page_2)
    except PageNotAnInteger:
        two_x_hist_qs =w_paginator_2.page(1)
    except EmptyPage:
        two_x_hist_qs = w_paginator_2.page(w_paginator_2.num_pages)

    context['two_x_hist_qs'] = two_x_hist_qs
    context["tx_endpage"] = two_x_hist_qs.number+1
    context["tx_startpage"] = two_x_hist_qs.number-1
    context['tx_start_value'] = two_x_hist_qs.start_index()
    context['tx_end_value'] = two_x_hist_qs.end_index()
    context['tx_usr_count'] = obj_two_x_hist.count()
    context["tx_dict_users"] = json.dumps(tx_dict_users)



    try:
      buy_plan_name = self.request.GET['plan_name']
    except:
      buy_plan_name = ""

    plan_usr = 0
    plan_count = 0
    plan_dict_users = {}
    plan_start_page = self.request.GET.get('pageno3', 1)
    plan_end_value = int(plan_start_page) * 5
    plan_start_value = int(plan_end_value) - 4
    Comp = CBurntoearnHistory.objects.filter(email_id = p_key).order_by('-id')
    if buy_plan_name:
      obj_plan_hist = CBurntoearnHistory.objects.filter(email_id = p_key).order_by('-id')
      for i in obj_plan_hist:
        plan_usr = plan_usr + 1
        plan_list_usr = {}
        if plan_start_value <= plan_usr <= plan_end_value:
          plan_count = plan_count + 1
          plan_list_usr["id"] = str(p_key)
          plan_list_usr["username"] = str(i.user)
          plan_list_usr["plan"] = "Burn"#int(i.purchase_amount)
          plan_list_usr["plan_amt"] = int(i.plan_amount)
          plan_list_usr["start_date"] = (str(i.plan_start_date))
          # plan_list_usr["end_date"] = (str(user_obj.plan_end_date))
          plan_list_usr["wallet_type"] = (str(i.Transaction_Hash))
          # plan_list_usr["health_max"] = (str(user_obj.Health_Withdraw_max_value))
          # plan_list_usr["health_min"] = (str(user_obj.Health_Withdraw_min_value))
          # plan_list_usr["referral_max"] = (str(user_obj.Referral_Withdraw_max_value))
          # plan_list_usr["referral_min"] = (str(user_obj.Referral_Withdraw_min_value))
          plan_list_usr["hash"] = (str(i.Transaction_Hash))
          plan_list_usr["buy_type"] = (i.currency)
          plan_list_usr["TradeBwa"] = str(user_obj.MPlanBWA)
          # plan_list_usr["hash"] = (str(i.User_plan_validation))
          plan_list_usr["pageno"] = plan_start_page
          plan_list_usr["sno"] = plan_usr
          plan_dict_users[plan_count] = plan_list_usr
    else:
      obj_plan_hist = CBurntoearnHistory.objects.filter(email_id = p_key).order_by('-id')
      for i in obj_plan_hist:
        plan_usr = plan_usr + 1
        plan_list_usr = {}
        if plan_start_value <= plan_usr <= plan_end_value:
          plan_count = plan_count + 1
          plan_list_usr["id"] = str(p_key)
          plan_list_usr["username"] = str(i.user)
          plan_list_usr["plan"] = "Burn"#int(i.purchase_amount)
          plan_list_usr["plan_amt"] = int(i.plan_amount)
          # plan_list_usr["price"] = str(user_obj.fixed_status)
          plan_list_usr["start_date"] = (str(i.plan_start_date))
          # plan_list_usr["end_date"] = (str(user_obj.plan_end_date))
          plan_list_usr["wallet_type"] = (str(i.Transaction_Hash))
          # plan_list_usr["health_max"] = (str(user_obj.Health_Withdraw_max_value))
          # plan_list_usr["health_min"] = (str(user_obj.Health_Withdraw_min_value))
          # plan_list_usr["referral_max"] = (str(user_obj.Referral_Withdraw_max_value))
          # plan_list_usr["referral_min"] = (str(user_obj.Referral_Withdraw_min_value))
          plan_list_usr["hash"] = (str(i.Transaction_Hash))
          plan_list_usr["buy_type"] = (i.currency)
          plan_list_usr["TradeBwa"] = str(user_obj.MPlanBWA)
          plan_list_usr["pageno"] = plan_start_page
          plan_list_usr["sno"] = plan_usr
          plan_dict_users[plan_count] = plan_list_usr
    try:
      tot_plan_user_qs = obj_plan_hist
    except:
      tot_plan_user_qs = ""
    w_page_3 = self.request.GET.get('pageno3', 1)
    w_paginator_3 = Paginator(tot_plan_user_qs, 5)
    try:
        plan_hist_qs = w_paginator_3.page(w_page_3)
    except PageNotAnInteger:
        plan_hist_qs =w_paginator_3.page(1)
    except EmptyPage:
        plan_hist_qs = w_paginator_3.page(w_paginator_3.num_pages)\

    context['plan_hist_qs'] = plan_hist_qs
    context["plan_endpage"] = plan_hist_qs.number+1
    context["plan_startpage"] = plan_hist_qs.number-1
    context['plan_start_value'] = plan_hist_qs.start_index()
    context['plan_end_value'] = plan_hist_qs.end_index()
    context['plan_usr_count'] = obj_plan_hist.count()
    context["plan_dict_users"] = json.dumps(plan_dict_users)


    try:
      usr_addrs = self.request.GET['address']
    except:
      usr_addrs = ""

    try:
      status = self.request.GET['status']
     
      if status == 'Active':
       
        status = 0
      if status == 'Completed':
        status = 1
      if status == 'Cancelled':
        status = 2
    except:
      status = ""

    try:
      date = self.request.GET['date']
    except:
      date = ""

    withdraw_usr = 0
    withdraw_count = 0
    withdraw_dict_users = {}
    withdraw_start_page = self.request.GET.get('pageno4', 1)
    withdraw_end_value = int(withdraw_start_page) * 5
    withdraw_start_value = int(withdraw_end_value) - 4
    if usr_addrs and status and date:
      obj_withdraw_hist = BurnWithdraw.objects.filter(userid_id = p_key).filter(Q(Address__icontains = usr_addrs) and Q(status__icontains = status) and Q(created_on__date__icontains = date)).exclude(Wallet_type__in=[ 'Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet','Bot_Referral_wallet','trade_withdraw_wallet','Trade_Referral_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    elif usr_addrs:
      obj_withdraw_hist = BurnWithdraw.objects.filter(userid_id = p_key).filter(Address__icontains = usr_addrs).exclude(Wallet_type__in=['Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet','Bot_Referral_wallet','trade_withdraw_wallet','Trade_Referral_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on)) 
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    elif date:
      obj_withdraw_hist = BurnWithdraw.objects.filter(userid_id = p_key).filter(created_on__date__icontains = date).exclude(Wallet_type__in=['Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet','Bot_Referral_wallet','trade_withdraw_wallet','Trade_Referral_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    elif status:
      obj_withdraw_hist = WiBurnWithdrawthdraw.objects.filter(userid_id = p_key).filter(status__icontains = status).exclude(Wallet_type__in=['Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet','Bot_Referral_wallet','trade_withdraw_wallet','Trade_Referral_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    else:
      obj_withdraw_hist = BurnWithdraw.objects.filter(userid_id = p_key).exclude(Wallet_type__in=[ 'Referral_wallet', 'Reward_wallet','ROR_wallet','LB_wallet','Bot_Referral_wallet','trade_withdraw_wallet','Trade_Referral_wallet']).order_by('-id')
      for i in obj_withdraw_hist:
        withdraw_usr = withdraw_usr + 1
        withdraw_list_usr = {}
        if withdraw_start_value <= withdraw_usr <= withdraw_end_value:
          withdraw_count = withdraw_count + 1
          withdraw_list_usr["username"] = str(i.userid.Name)
          withdraw_list_usr["amount"] = str(i.Amount)
          withdraw_list_usr["Withdraw_fee"] = str(i.Withdraw_fee)
          withdraw_list_usr["Withdraw_USDT"] = str(i.Withdraw_USDT)
          withdraw_list_usr["Withdraw_JW"] = str(i.Withdraw_JW)
          withdraw_list_usr["Address"] = str(i.Address)
          withdraw_list_usr["wallet"] = str(i.Wallet_type)
          withdraw_list_usr["Transaction_Hash"] = str(i.Transaction_Hash)
          withdraw_list_usr["id"] = str(i.id)
          withdraw_list_usr["status"] = str(i.status)
          withdraw_list_usr["date"] = (str(i.created_on))
          withdraw_list_usr["pageno"] = withdraw_start_page
          withdraw_list_usr["sno"] = withdraw_usr
          withdraw_dict_users[withdraw_count] = withdraw_list_usr
    try:
      tot_withdraw_user_qs = obj_withdraw_hist
    except:
      tot_withdraw_user_qs = ""
    w_page_4 = self.request.GET.get('pageno4', 1)
    w_paginator_4 = Paginator(tot_withdraw_user_qs, 5)
    try:
        withdraw_hist_qs = w_paginator_4.page(w_page_4)
    except PageNotAnInteger:
        withdraw_hist_qs =w_paginator_4.page(1)
    except EmptyPage:
        withdraw_hist_qs = w_paginator_4.page(w_paginator_4.num_pages)

    context['withdraw_hist_qs'] = withdraw_hist_qs
    context["withdraw_endpage"] = withdraw_hist_qs.number+1
    context["withdraw_startpage"] = withdraw_hist_qs.number-1
    context['withdraw_start_value'] = withdraw_hist_qs.start_index()
    context['withdraw_end_value'] = withdraw_hist_qs.end_index()
    context['withdraw_usr_count'] = obj_withdraw_hist.count()
    context["withdraw_dict_users"] = json.dumps(withdraw_dict_users)

     
    try:
      ref_user = self.request.GET['name']
    except:
      ref_user = ""


    ref_usr = 0
    ref_count = 0
    ref_dict_users = {}
    ref_start_page = self.request.GET.get('pageno5', 1)
    ref_end_value = int(ref_start_page) * 5
    ref_start_value = int(ref_end_value) - 4
    try:
      if ref_user:
        obj_ref_hist = BurnRewardHistory.objects.filter(user_id = p_key).filter(referral_id__icontains = ref_user).order_by('-id')
        for i in obj_ref_hist:
          
          ref_usr = ref_usr + 1
          ref_list_usr = {}
          if ref_start_value <= ref_usr <= ref_end_value:
            ref_count = ref_count + 1
            # ref_list_usr["id"] = str(p_key)
            ref_list_usr["id"] = i.id
            ref_list_usr["username"] = str(i.user.Name)
            ref_list_usr["ref_id"] = i.referral_id
            ref_list_usr["reward_amt"] = i.reward
            ref_list_usr["date"] = (str(i.created_on))
            ref_list_usr["pageno"] = ref_start_page
            ref_list_usr["sno"] = ref_usr
            ref_dict_users[ref_count] = ref_list_usr
        
      else:
        obj_ref_hist = BurnRewardHistory.objects.filter(user_id = p_key).order_by('-id')
        for i in obj_ref_hist:
          ref_usr = ref_usr + 1
          ref_list_usr = {}
          if ref_start_value <= ref_usr <= ref_end_value:
            ref_count = ref_count + 1
            ref_list_usr["id"] = i.id
            ref_list_usr["username"] = str(i.user.Name)
            ref_list_usr["ref_id"] = i.referral_id
            ref_list_usr["reward_amt"] = i.reward
            ref_list_usr["date"] = (str(i.created_on))
            ref_list_usr["pageno"] = ref_start_page
            ref_list_usr["sno"] = ref_usr 
            ref_dict_users[ref_count] = ref_list_usr
        

      context['ref_usr_count'] = obj_ref_hist.count()
    except:
      obj_ref_hist = ""
      context['ref_usr_count'] = 0
    try:
      tot_ref_user_qs = obj_ref_hist
    except:
      tot_ref_user_qs = ""
    w_page_5 = self.request.GET.get('pageno5', 1)
    w_paginator_5 = Paginator(tot_ref_user_qs, 5) 
    try:
        ref_hist_qs = w_paginator_5.page(w_page_5)
    except PageNotAnInteger:
        ref_hist_qs =w_paginator_5.page(1)
    except EmptyPage:
        ref_hist_qs = w_paginator_5.page(w_paginator_5.num_pages)

    context['ref_hist_qs'] = ref_hist_qs
    context["ref_endpage"] = ref_hist_qs.number+1
    context["ref_startpage"] = ref_hist_qs.number-1
    context['ref_start_value'] = ref_hist_qs.start_index()
    context['ref_end_value'] = ref_hist_qs.end_index()
    context["ref_dict_users"] = json.dumps(ref_dict_users)

    wall_usr = 0
    wall_count = 0
    wall_dict_users = {}
    wall_start_page = self.request.GET.get('pageno6', 1)
    wall_end_value = int(wall_start_page) * 5
    wall_start_value = int(wall_end_value) - 4
    try:
      obj_wall_hist = UserCashWallet.objects.filter(userid_id = p_key).order_by('-id')
      for i in obj_wall_hist:
        wall_usr = wall_usr + 1
        wall_list_usr = {}
        if wall_start_value <= wall_usr <= wall_end_value:
          wall_count = wall_count + 1
          wall_list_usr["username"] = str(i.userid.Name)
          if i.Burnrewardjwc == 0.00000000:
            wall_list_usr["burn_reward"] = int(i.Burnrewardjwc)
          else:
            wall_list_usr["burn_reward"] = str(i.Burnrewardjwc)
          if i.Burnreffjwc == 0.00000000:
            wall_list_usr["burn_reff"] = int(i.Burnreffjwc)
          else:
            wall_list_usr["burn_reff"] = str(i.Burnreffjwc)  
          wall_list_usr["pageno"] = wall_start_page
          wall_list_usr["sno"] = wall_usr
          wall_dict_users[wall_count] = wall_list_usr
    except:
      obj_wall_hist = ""
    try:
      tot_wall_user_qs = obj_wall_hist
    except:
      tot_wall_user_qs = ""
    w_page_6 = self.request.GET.get('pageno6', 1)
    w_paginator_6 = Paginator(tot_wall_user_qs, 5)
    try:
        wall_hist_qs = w_paginator_6.page(w_page_6)
    except PageNotAnInteger:
        wall_hist_qs =w_paginator_6.page(1)
    except EmptyPage:
        wall_hist_qs = w_paginator_6.page(w_paginator_6.num_pages)

    context['wall_hist_qs'] = wall_hist_qs
    context["wall_endpage"] = wall_hist_qs.number+1
    context["wall_startpage"] = wall_hist_qs.number-1
    context['wall_start_value'] = wall_hist_qs.start_index()
    context['wall_end_value'] = wall_hist_qs.end_index()
    context['wall_usr_count'] = obj_wall_hist.count()
    context["wall_dict_users"] = json.dumps(wall_dict_users)


    login_usr = 0
    login_count = 0
    login_dict_users = {}
    login_start_page = self.request.GET.get('pageno7', 1)
    login_end_value = int(login_start_page) * 5
    login_start_value = int(login_end_value) - 4
    try:
      obj_login_hist = LoginHistory.objects.filter(user_id = p_key).order_by('-created_on')
      for i in obj_login_hist:
        login_usr = login_usr + 1
        login_list_usr = {}
        if login_start_value <= login_usr <= login_end_value:
          login_count = login_count + 1
          login_list_usr["username"] = str(i.user.Name)
          login_list_usr["created_on"] = str(i.created_on)
          login_list_usr["modified_on"] = str(i.modified_on)
          login_list_usr["pageno"] = login_start_page
          login_list_usr["sno"] = login_usr
          login_dict_users[login_count] = login_list_usr
    except:
      obj_login_hist = ""
    try:
      tot_login_user_qs = obj_login_hist
    except:
      tot_login_user_qs = ""
    w_page_7 = self.request.GET.get('pageno7', 1)
    w_paginator_7 = Paginator(tot_login_user_qs, 5)
    try:
        login_hist_qs = w_paginator_7.page(w_page_7)
    except PageNotAnInteger:
        login_hist_qs =w_paginator_7.page(1)
    except EmptyPage:
        login_hist_qs = w_paginator_7.page(w_paginator_7.num_pages)

    context['login_hist_qs'] = login_hist_qs
    context["login_endpage"] = login_hist_qs.number+1
    context["login_startpage"] = login_hist_qs.number-1
    context['login_start_value'] = login_hist_qs.start_index()
    context['login_end_value'] = login_hist_qs.end_index()
    context['login_usr_count'] = obj_login_hist.count()
    context["login_dict_users"] = json.dumps(login_dict_users)

    
    context['Title'] = 'Burn JWC History Table'
    context["Btn_url"] = "trade_admin_auth:List_User_Management"
    return context


  @method_decorator(check_group_icon_menu("History"))
  def dispatch(self, *args, **kwargs):
    return super(BurnjwcHistoryManagementTable, self).dispatch(*args, **kwargs)


################################################################################################################################################
################################################################################################################################################



@check_group("Step Management")
def StepHistoryManagement(request,data):
  context = {}
  today = datetime.datetime.today()
  yesterday = today - timedelta(days = 1)
  checkfromdate = yesterday.strftime('%Y-%m-%d')
  try:
    usr_name = request.GET['username']
  except:
    usr_name = ""
  try:
    email = request.GET['Email']
  except:
    email = ""
  usr = 0
  count = 0
  dict_step_users = {}
  start_page = request.GET.get('pageno', 1)
  end_value = int(start_page) * 10
  start_value = int(end_value) - 9

  if data == "total_step_history":    
    trade_qs = Steps_history.objects.filter(created_on__date = checkfromdate).order_by('-id')
    context['trade_qs'] =trade_qs
    context['Title'] = 'Yesterday Active Users'
    if usr_name and email:
      obj_step_hist = Steps_history.objects.filter(created_on__date = checkfromdate).filter(Q(user__icontains = usr_name) and Q(user__Email__icontains = email)).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    elif email:
      obj_step_hist = Steps_history.objects.filter(created_on__date = checkfromdate).filter(user__Email__icontains = email).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    elif usr_name:
      obj_step_hist = Steps_history.objects.filter(created_on__date = checkfromdate).filter(user__user_name__icontains = usr_name).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    else:
      obj_step_hist = Steps_history.objects.filter(created_on__date = checkfromdate).filter(user__user_name__icontains = usr_name).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    try:
      tot_user_qs = obj_step_hist
    except:
      tot_user_qs = ""
    w_page = request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_user_qs, 10)
    try:
        adminuser_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        adminuser_qs =w_paginator.page(1)
    except EmptyPage:
        adminuser_qs = w_paginator.page(w_paginator.num_pages)
    context['adminuser_qs'] = adminuser_qs

  if data == "below_3000_step_users":
    trade_qs = Steps_history.objects.filter(steps__lte = 3000).filter(created_on__date = checkfromdate).order_by('-id')
    context['trade_qs'] =trade_qs
    context['Title'] = 'Below 3000 Step Users'
    if usr_name and email:
      obj_step_hist = Steps_history.objects.filter(steps__lte = 3000).filter(created_on__date = checkfromdate).filter(Q(user__icontains = usr_name) and Q(user__Email__icontains = email)).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    elif email:
      obj_step_hist = Steps_history.objects.filter(steps__lte = 3000).filter(created_on__date = checkfromdate).filter(user__Email__icontains = email).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    elif usr_name:
      obj_step_hist = Steps_history.objects.filter(steps__lte = 3000).filter(created_on__date = checkfromdate).filter(user__user_name__icontains = usr_name).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    else:
      obj_step_hist = Steps_history.objects.filter(steps__lte = 3000).filter(created_on__date = checkfromdate).filter(user__user_name__icontains = usr_name).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    try:
      tot_user_qs = obj_step_hist
    except:
      tot_user_qs = ""
    w_page = request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_user_qs, 10)
    try:
        adminuser_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        adminuser_qs =w_paginator.page(1)
    except EmptyPage:
        adminuser_qs = w_paginator.page(w_paginator.num_pages)
    context['adminuser_qs'] = adminuser_qs

  if data == "above_3000_step_users":
    trade_qs = Steps_history.objects.filter(steps__gte = 3000).filter(created_on__date = checkfromdate).order_by('-id')
    context['trade_qs'] =trade_qs
    context['Title'] = 'Above 3000 Step Users'
    if usr_name and email:
      obj_step_hist = Steps_history.objects.filter(steps__gte = 3000).filter(created_on__date = checkfromdate).filter(Q(user__icontains = usr_name) and Q(user__Email__icontains = email)).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    elif email:
      obj_step_hist = Steps_history.objects.filter(steps__gte = 3000).filter(created_on__date = checkfromdate).filter(user__Email__icontains = email).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    elif usr_name:
      obj_step_hist = Steps_history.objects.filter(steps__gte = 3000).filter(created_on__date = checkfromdate).filter(user__user_name__icontains = usr_name).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    else:
      obj_step_hist = Steps_history.objects.filter(steps__gte = 3000).filter(created_on__date = checkfromdate).filter(user__user_name__icontains = usr_name).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    try:
      tot_user_qs = obj_step_hist
    except:
      tot_user_qs = ""
    w_page = request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_user_qs, 10)
    try:
        adminuser_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        adminuser_qs =w_paginator.page(1)
    except EmptyPage:
        adminuser_qs = w_paginator.page(w_paginator.num_pages)
    context['adminuser_qs'] = adminuser_qs

  if data == "reward_unclaimed_users":
    trade_qs = Steps_history.objects.filter(Q(status = 0) & Q(steps__gte = 3000)).filter(created_on__date = checkfromdate).order_by('-id')
    context['trade_qs'] =trade_qs
    context['Title'] = 'Reward Unclaimed Users'
    if usr_name and email:
      obj_step_hist = Steps_history.objects.filter(Q(status = 0) & Q(steps__gte = 3000)).filter(created_on__date = checkfromdate).filter(Q(user__icontains = usr_name) and Q(user__Email__icontains = email)).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    elif email:
      obj_step_hist = Steps_history.objects.filter(Q(status = 0) & Q(steps__gte = 3000)).filter(created_on__date = checkfromdate).filter(user__Email__icontains = email).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    elif usr_name:
      obj_step_hist = Steps_history.objects.filter(Q(status = 0) & Q(steps__gte = 3000)).filter(created_on__date = checkfromdate).filter(user__user_name__icontains = usr_name).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    else:
      obj_step_hist = Steps_history.objects.filter(Q(status = 0) & Q(steps__gte = 3000)).filter(created_on__date = checkfromdate).filter(user__user_name__icontains = usr_name).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    try:
      tot_user_qs = obj_step_hist
    except:
      tot_user_qs = ""
    w_page = request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_user_qs, 10)
    try:
        adminuser_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        adminuser_qs =w_paginator.page(1)
    except EmptyPage:
        adminuser_qs = w_paginator.page(w_paginator.num_pages)
    context['adminuser_qs'] = adminuser_qs

  if data == "reward_claimed_users":
    trade_qs = Steps_history.objects.filter(Q(status = 1) & Q(steps__gte = 3000)).filter(created_on__date = checkfromdate).order_by('-id')
    context['trade_qs'] =trade_qs
    context['Title'] = 'Reward Claimed Users'
    if usr_name and email:
      obj_step_hist = Steps_history.objects.filter(Q(status = 1) & Q(steps__gte = 3000)).filter(created_on__date = checkfromdate).filter(Q(user__icontains = usr_name) and Q(user__Email__icontains = email)).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    elif email:
      obj_step_hist = Steps_history.objects.filter(Q(status = 1) & Q(steps__gte = 3000)).filter(created_on__date = checkfromdate).filter(user__Email__icontains = email).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    elif usr_name:
      obj_step_hist = Steps_history.objects.filter(Q(status = 1) & Q(steps__gte = 3000)).filter(created_on__date = checkfromdate).filter(user__user_name__icontains = usr_name).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    else:
      obj_step_hist = Steps_history.objects.filter(Q(status = 1) & Q(steps__gte = 3000)).filter(created_on__date = checkfromdate).filter(user__user_name__icontains = usr_name).order_by('-id')
      for i in obj_step_hist:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["username"] = (str(i.user))
          list_usr["email"] = (str(i.user.Email))
          list_usr["status"] = (i.status)
          list_usr["steps"] = (i.steps)
          list_usr["date"] = (str(i.created_on))
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_step_users[count] = list_usr
    try:
      tot_user_qs = obj_step_hist
    except:
      tot_user_qs = ""
    w_page = request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_user_qs, 10)
    try:
        adminuser_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        adminuser_qs =w_paginator.page(1)
    except EmptyPage:
        adminuser_qs = w_paginator.page(w_paginator.num_pages)
    context['adminuser_qs'] = adminuser_qs

  context["endpage"] = adminuser_qs.number+1
  context["startpage"] = adminuser_qs.number-1
  context['start_value'] = adminuser_qs.start_index()
  context['end_value'] = adminuser_qs.end_index()
  context['usr_count'] = obj_step_hist.count()
  context['dict_step_users_list'] = json.dumps(dict_step_users)  
  return render(request,'trade_admin_auth/step_history_list_user.html',context)


class ReferalHistoryTable(TemplateView):
  template_name = "trade_admin_auth/referal_history_table.html"

  def get_context_data(self, **kwargs):
    context = super(ReferalHistoryTable, self).get_context_data(**kwargs)
    p_key = self.kwargs['pk']

    user_obj = User_Management.objects.get(id = p_key)

    try:
      ref_mail = self.request.GET['email']
    except:
      ref_mail = ""

    ref_usr = 0
    ref_count = 0
    ref_dict_users = {}
    ref_start_page = self.request.GET.get('pageno', 1)
    ref_end_value = int(ref_start_page) * 5
    ref_start_value = int(ref_end_value) - 4
    
    if ref_mail:
      obj_ref_his = User_Management.objects.filter(Direct_referral_id = user_obj.Name).filter(Email__icontains = ref_mail).order_by('-id')
      for i in obj_ref_his:
        ref_usr = ref_usr + 1
        ref_list_usr = {}
        if ref_start_value <= ref_usr <= ref_end_value:
          ref_count = ref_count + 1
          ref_list_usr["id"] = str(i.id)
          ref_list_usr["username"] = str(i.Name)
          ref_list_usr["email"] = (i.Email)
          ref_list_usr["Referral_id"] = (i.Referral_id)
          ref_list_usr["Direct_referral_id"] = (i.Direct_referral_id)
          ref_list_usr["phone_number"] = str(i.phone_number)
          ref_list_usr["phone_type"] = (i.user_profile_pic)
          ref_list_usr["date"] = (str(i.created_on))
          ref_list_usr["User_type"] = (i.User_type)
          ref_list_usr["plan_start_date"] = str(i.plan_start_date)
          ref_list_usr["plan_end_date"] = str(i.plan_end_date)
          ref_list_usr["pageno"] = ref_start_page
          ref_list_usr["sno"] = ref_usr
          ref_dict_users[ref_count] = ref_list_usr
    else:
      obj_ref_his = User_Management.objects.filter(Direct_referral_id = user_obj.Name).order_by('-id')
      for i in obj_ref_his:
        ref_usr = ref_usr + 1
        ref_list_usr = {}
        if ref_start_value <= ref_usr <= ref_end_value:
          ref_count = ref_count + 1
          ref_list_usr["id"] = str(i.id)
          ref_list_usr["username"] = str(i.Name)
          ref_list_usr["email"] = (i.Email)
          ref_list_usr["Referral_id"] = (i.Referral_id)
          ref_list_usr["Direct_referral_id"] = (i.Direct_referral_id)
          ref_list_usr["phone_number"] = str(i.phone_number)
          ref_list_usr["phone_type"] = (i.user_profile_pic)
          ref_list_usr["date"] = (str(i.created_on))
          ref_list_usr["User_type"] = (i.User_type)
          ref_list_usr["plan_start_date"] = str(i.plan_start_date)
          ref_list_usr["plan_end_date"] = str(i.plan_end_date)
          ref_list_usr["pageno"] = ref_start_page
          ref_list_usr["sno"] = ref_usr
          ref_dict_users[ref_count] = ref_list_usr

    try:
      tot_ref_user_qs = obj_ref_his
    except:
      tot_ref_user_qs = ""
    w_page = self.request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_ref_user_qs, 5)
    
    try:
        ref_hist_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        ref_hist_qs =w_paginator.page(1)
    except EmptyPage:
        ref_hist_qs = w_paginator.page(w_paginator.num_pages)
    
    
    context['ref_hist_qs'] = ref_hist_qs
    context["ref_endpage"] = ref_hist_qs.number+1
    context["ref_startpage"] = ref_hist_qs.number-1
    context['ref_start_value'] = ref_hist_qs.start_index()
    context['ref_end_value'] = ref_hist_qs.end_index()
    context['ref_usr_count'] = obj_ref_his.count()
    context["ref_dict_users"] = json.dumps(ref_dict_users)

    context['user_name'] = (user_obj.Name).upper()
    context['Title'] = 'Direct User History Table'
    context["Btn_url"] = "trade_admin_auth:List_User_Management"
    return context

  @method_decorator(check_group_icon_menu("Referal History"))
  def dispatch(self, *args, **kwargs):
    return super(ReferalHistoryTable, self).dispatch(*args, **kwargs)
  
# from Staking.models import  stake_wallet_management,stake_claim_reward_history
# @check_group_icon_menu("Add Plan")
# def Add_User_Plan(request,id):
#   context = {}
#   try:
#     obj_user = User_Management.objects.get(id = id)
    
#   except:
#     obj_user = ""
#   obj_plan = plan.objects.filter(plan_type = 1)
#   try:
#     companyqs = Company.objects.get(id=1)
#     companyname= companyqs.name
#   except:
#     companyqs = ''
#     companyname = ''
#   Market_Price = market_price.objects.get(id = 1)
#   if request.method == "POST":
#     plan_name = request.POST["plan_name"]
#     plan_period = request.POST["plan_duration"]
#     price = request.POST["price"]
#     if price == Market_Price.market_price:
#       tag="fixed"
#     elif price == companyqs.market_api_price:
#       tag="market"
#     user_wallet_type = request.POST["wallet_type"]
#     trans_hash = request.POST["transaction_hash"]
#     if trans_hash:
#       try:
#         obj_plan_purchase_history = plan_purchase_history.objects.get(User_plan_validation = trans_hash)
#       except:
#         obj_plan_purchase_history = 0
#     else:
#       obj_plan_purchase_history = 0
#     plan_id = plan.objects.get(plan_name = plan_name)
#     plan_purchase=int(plan_id.plan_purchase_type)
#     if plan_period == "Monthly":
#       plan_duration = 0
#       plan_days = 30
#       plan_amount = plan_id.plan_purchase_amount_monthly
#     if plan_period == "Quarterly":
#       plan_duration = 1
#       plan_days = 90
#       plan_amount = plan_id.plan_purchase_amount_quarterly
#     if plan_period == "Annual":
#       plan_duration = 2
#       plan_days = 365
#       plan_amount = plan_id.plan_purchase_amount_annual

#     wallet = UserCashWallet.objects.get(userid = obj_user)
    
#     if obj_plan_purchase_history == 0:
#       if Decimal(wallet.balanceone) >= 0 or Decimal(wallet.referalincome) >= 0:
#         wallet_flush_history.objects.create(user = obj_user,wallet_balanceone = wallet.balanceone,Wallet_referral_income = wallet.referalincome,User_before_plan = obj_user.plan)
#         wallet.balanceone = 0
#         wallet.referalincome = 0
#         wallet.save()
#       if plan_purchase == 1:
#           try:
#               user_stake_obj = stake_wallet_management.objects.using('second_db').get(user = obj_user.id)
#           except:
#               user_stake_obj = 0
#           if user_stake_obj != 0:
#               amunt=plan_id.activate_plan
#               value=Decimal(plan_amount) - Decimal(amunt)
#               user_stake_obj.stake_Wallet=Decimal(user_stake_obj.stake_Wallet)  + Decimal(value)
#               user_stake_obj.save(using='second_db')
#               stake_claim_reward_history.objects.using('second_db').create(user = obj_user.id,email=obj_user.Email,type='Plan Purchase',stake_Wallet_reward_amount = Decimal(value),original_amount=plan_amount)
#       else:
#           pass
#       obj_user.plan = plan_id.id
#       obj_user.plan_start_date = datetime.datetime.now()
#       today = datetime.datetime.now()
#       desired_time = datetime.time(23, 55)
#       today_with_desired_time = datetime.datetime.combine(today.date(), desired_time)
#       end_date = today_with_desired_time + timedelta(plan_days)
#       obj_user.plan_end_date = end_date
#       obj_user.user_referral_eligible_level = plan_id.referral_level_eligible
#       obj_user.plan_validation = plan_period
#       obj_user.save()
#       obj_user.Health_Withdraw_max_value = plan_id.health_withdraw_maximum_limit
#       obj_user.Health_Withdraw_min_value = plan_id.health_withdraw_minimum_limit
#       obj_user.Referral_Withdraw_max_value = plan_id.referral_withdraw_maximum_limit
#       obj_user.Referral_Withdraw_min_value = plan_id.referral_withdraw_minimum_limit
#       obj_user.fixed_status=tag
#       obj_user.save()
#       if plan_purchase == 1:
#         Jw_plan_purchase_history.objects.create(user = obj_user,activate_plan=plan_id.activate_plan ,plan_name = plan_id.plan_name ,stake_credit=plan_id.user_stake_credit,purchase_amount = amunt,user_wallet_type = user_wallet_type, buy_type = "Admin Plan Buy")
#         plan_purchase_history.objects.create(user = obj_user , User_plan_validation = trans_hash , plan_id = plan_id , Plan_maximum_step = plan_id.Max_step_count , Plan_minimum_step = plan_id.Min_step_count , Plan_maximum_reward = plan_id.reward_amount , Plan_referral_status = plan_id.referral_status , Plan_Two_X_Boost_status = plan_id.two_X_Boost_status , Plan_Withdraw_status = plan_id.withdraw_status , Plan_Level = plan_id.referral_level_eligible , purchase_amount = plan_amount , user_wallet_type = user_wallet_type , buy_type = "Admin Plan Buy",plan_reward_step_val = plan_id.Reward_step_value,plan_per_reward_amount = plan_id.plan_reward_amount,stake_wallet_monthly_split_percentage=plan_id.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=plan_id.withdraw_wallet_monthly_percentage,support_status=plan_id.support_status,monthly_support=plan_id.monthly_support_status,quarterly_support=plan_id.quarterly_support_status,annual_support=plan_id.annual_support_status,plan_purchase_type=plan_id.plan_purchase_type,halfyearly_support=plan_id.halfyearly_support_status,monthly_support_amount=plan_id.monthly_support_amount,quarterly_support_amount=plan_id.quarterly_support_amount,halfyearly_support_amount=plan_id.halfyearly_support_amount,annual_support_amount=plan_id.annual_support_amount,current_api_price=price)
#       else:
#         plan_purchase_history.objects.create(user = obj_user , User_plan_validation = trans_hash , plan_id = plan_id , Plan_maximum_step = plan_id.Max_step_count , Plan_minimum_step = plan_id.Min_step_count , Plan_maximum_reward = plan_id.reward_amount , Plan_referral_status = plan_id.referral_status , Plan_Two_X_Boost_status = plan_id.two_X_Boost_status , Plan_Withdraw_status = plan_id.withdraw_status , Plan_Level = plan_id.referral_level_eligible , purchase_amount = plan_amount , user_wallet_type = user_wallet_type , buy_type = "Admin Plan Buy",plan_reward_step_val = plan_id.Reward_step_value,plan_per_reward_amount = plan_id.plan_reward_amount,stake_wallet_monthly_split_percentage=plan_id.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=plan_id.withdraw_wallet_monthly_percentage,support_status=plan_id.support_status,monthly_support=plan_id.monthly_support_status,quarterly_support=plan_id.quarterly_support_status,annual_support=plan_id.annual_support_status,plan_purchase_type=plan_id.plan_purchase_type,halfyearly_support=plan_id.halfyearly_support_status,monthly_support_amount=plan_id.monthly_support_amount,quarterly_support_amount=plan_id.quarterly_support_amount,halfyearly_support_amount=plan_id.halfyearly_support_amount,annual_support_amount=plan_id.annual_support_amount,current_api_price=price)

#       if plan_id.referral_status == 0:
#           obj_user.referral_plan_status = 0
#           obj_user.save()
#       else:
#           obj_user.referral_plan_status = 1
#           obj_user.save()

#       User_Management.objects.filter(id = obj_user.id).update(plan = plan_id.id)
      
#       if obj_user.referal_code != "" or obj_user.referal_code != None:
        
#         a=[]
#         ref_code = obj_user.referal_code
        
#         reff_id = Referral_code.objects.get(referal_code=ref_code)
#         referred_user = User_Management.objects.get(id = reff_id.user.id)
#         uesr_level = obj_user.Referral_Level
#         Referral_level = referral_level.objects.all().count()
#         for i in range(Referral_level):
#             reff_id = Referral_code.objects.get(referal_code=ref_code)
#             referred_user = User_Management.objects.get(id = reff_id.user.id)
#             a.append(referred_user.id)
#             ref_code = referred_user.referal_code
#             if referred_user.referal_code == "" or referred_user.referal_code == None:
#                 break
#         b = 1
#         l = 0
#         obj_plan_hist = plan_purchase_history.objects.filter(user_id = obj_user.id).count()
#         if obj_plan_hist == 1:
#           for i in a:
#               user = User_Management.objects.get(id = i)
#               if user.plan == 0:
#                   b = b+1 
#                   pass
#               else:
#                   # PLan_plan = plan.objects.get(id = user.plan)
#                   try:
#                       plan_hist=plan_purchase_history.objects.filter(plan_id=user.plan).last()
#                   except:
#                       plan_hist=''
#                   if plan_hist:
#                       # if PLan_plan.referral_status == 0:
#                       if plan_hist.Plan_referral_status == 0:
#                           b = b+1
#                           pass
#                   # elif user.user_referral_eligible_level >= plan_hist.Plan_Level and plan_hist.Plan_Level >= b:
#                       elif plan_hist.Plan_referral_status == 1:
#                           if user.user_referral_eligible_level >= plan_hist.Plan_Level and plan_hist.Plan_Level >= b:
#                             User_Referral_level = referral_level.objects.get(referral_level_id = b)
#                             Market_Price = market_price.objects.get(id = 1)
#                             if plan_purchase == 1:
#                                 Purchase_Amount = Decimal(amunt)
#                             else:
#                                 Purchase_Amount = Decimal(plan_amount)
#                             percentage = (User_Referral_level.commission_amount * Purchase_Amount)/100
#                             actual_reward = Decimal(percentage)
#                             l=l+actual_reward
#                             userwallet = UserCashWallet.objects.get(userid = i)
#                             userwallet.referalincome = userwallet.referalincome + actual_reward
#                             userwallet.save()
#                             table = Referral_reward_History.objects.create(user = user,referral_id = (obj_user.Name),reward = Decimal(actual_reward))
#                             b = b+1 
#                       else:
#                         b = b +1
#                         pass
#                   else:
#                       b = b +1
#                       pass
#         sum = 0
#         # for i in l:
#         #     sum = sum + i
#         if plan_purchase == 1:
#           admin_profit = Decimal(amunt) - l
#           adminprofit = Admin_Profit.objects.create(user = obj_user,admin_profit = admin_profit,Profit_type = "Plan Purchase")
#         else:
#           admin_profit = plan_amount - l
#           adminprofit = Admin_Profit.objects.create(user = obj_user,admin_profit = admin_profit,Profit_type = "Plan Purchase")            
#         messages.add_message(request, messages.SUCCESS, 'Plan was added to '+str(obj_user.Name)+' successfully.')
#       else:   
#         pass
#     else:
#       usr_mail = obj_plan_purchase_history.user.Email
#       messages.add_message(request, messages.ERROR, 'Transaction hash already applied for this user: '+str(usr_mail))
#   context["obj_plan"] = obj_plan
#   context["Title"] = "Add User Plan"
#   context["obj_user"] = obj_user  
#   context["market"]=companyqs.market_api_price 
#   context["fixed"]=Market_Price.market_price
  
#   return render(request,"trade_admin_auth/add_user_plan.html",context)
from datetime import datetime, timedelta, time
from Staking.models import  stake_wallet_management,stake_claim_reward_history
@check_group_icon_menu("Add Plan")
def Add_User_Plan(request,id):
  context = {}
  try:
    obj_user = User_Management.objects.get(id = id)
    
  except:
    obj_user = ""
  obj_plan = plan.objects.filter(plan_type = 1)
  try:
    companyqs = Company.objects.get(id=1)
    companyname= companyqs.name
  except:
    companyqs = ''
    companyname = ''
  Market_Price = market_price.objects.get(id = 1)
  if request.method == "POST":
    plan_name = request.POST["plan_name"]
    plan_period = request.POST["plan_duration"]
    price = request.POST["price"]
    if price == Market_Price.market_price:
      tag="fixed"
    elif price == companyqs.market_api_price:
      tag="market"
    user_wallet_type = request.POST["wallet_type"]
    trans_hash = request.POST["transaction_hash"]
    if trans_hash:
      try:
        obj_plan_purchase_history = plan_purchase_history.objects.get(User_plan_validation = trans_hash)
      except:
        obj_plan_purchase_history = 0
    else:
      obj_plan_purchase_history = 0
    plan_id = plan.objects.get(plan_name = plan_name)
    plan_purchase=int(plan_id.plan_purchase_type)
    if plan_period == "Monthly":
      plan_duration = 0
      plan_days = 30
      plan_amount = plan_id.plan_purchase_amount_monthly
    if plan_period == "Quarterly":
      plan_duration = 1
      plan_days = 90
      plan_amount = plan_id.plan_purchase_amount_quarterly
    if plan_period == "Annual":
      plan_duration = 2
      plan_days = 365
      plan_amount = plan_id.plan_purchase_amount_annual

    wallet = UserCashWallet.objects.get(userid = obj_user)
    
    if obj_plan_purchase_history == 0:
      if Decimal(wallet.balanceone) >= 0 or Decimal(wallet.referalincome) >= 0:
        wallet_flush_history.objects.create(user = obj_user,wallet_balanceone = wallet.balanceone,Wallet_referral_income = wallet.referalincome,User_before_plan = obj_user.plan)
        wallet.balanceone = 0
        wallet.referalincome = 0
        wallet.save()
      if plan_purchase == 1:
          try:
              user_stake_obj = stake_wallet_management.objects.using('second_db').get(user = obj_user.id)
          except:
              user_stake_obj = 0
          if user_stake_obj != 0:
              amunt=plan_id.activate_plan
              value=Decimal(plan_amount) - Decimal(amunt)
              user_stake_obj.stake_Wallet=Decimal(user_stake_obj.stake_Wallet)  + Decimal(value)
              user_stake_obj.save(using='second_db')
              stake_claim_reward_history.objects.using('second_db').create(user = obj_user.id,email=obj_user.Email,type='Plan Purchase',stake_Wallet_reward_amount = Decimal(value),original_amount=plan_amount)
      else:
          pass
      obj_user.plan = plan_id.id
      obj_user.plan_start_date = datetime.now()
      today = datetime.now()
      desired_time = time(23, 55)
      today_with_desired_time = datetime.combine(today.date(), desired_time)
      end_date = today_with_desired_time + timedelta(plan_days)
      obj_user.plan_end_date = end_date
      obj_user.user_referral_eligible_level = plan_id.referral_level_eligible
      obj_user.plan_validation = plan_period
      obj_user.save()
      obj_user.Health_Withdraw_max_value = plan_id.health_withdraw_maximum_limit
      obj_user.Health_Withdraw_min_value = plan_id.health_withdraw_minimum_limit
      obj_user.Referral_Withdraw_max_value = plan_id.referral_withdraw_maximum_limit
      obj_user.Referral_Withdraw_min_value = plan_id.referral_withdraw_minimum_limit
      obj_user.fixed_status=tag
      obj_user.save()
      direct_referrals_count = Referral_code.objects.filter(user=obj_user).count()
      if plan_purchase == 1:
        Jw_plan_purchase_history.objects.create(user = obj_user,activate_plan=plan_id.activate_plan ,plan_name = plan_id.plan_name ,stake_credit=plan_id.user_stake_credit,purchase_amount = amunt,user_wallet_type = user_wallet_type, buy_type = "Admin Plan Buy")
        plan_purchase_history.objects.create(user = obj_user , User_plan_validation = trans_hash , plan_id = plan_id , Plan_maximum_step = plan_id.Max_step_count , Plan_minimum_step = plan_id.Min_step_count , Plan_maximum_reward = plan_id.reward_amount , Plan_referral_status = plan_id.referral_status , Plan_Two_X_Boost_status = plan_id.two_X_Boost_status , Plan_Withdraw_status = plan_id.withdraw_status , Plan_Level = plan_id.referral_level_eligible , purchase_amount = plan_amount , user_wallet_type = user_wallet_type , buy_type = "Admin Plan Buy",plan_reward_step_val = plan_id.Reward_step_value,plan_per_reward_amount = plan_id.plan_reward_amount,stake_wallet_monthly_split_percentage=plan_id.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=plan_id.withdraw_wallet_monthly_percentage,support_status=plan_id.support_status,monthly_support=plan_id.monthly_support_status,quarterly_support=plan_id.quarterly_support_status,annual_support=plan_id.annual_support_status,plan_purchase_type=plan_id.plan_purchase_type,halfyearly_support=plan_id.halfyearly_support_status,monthly_support_amount=plan_id.monthly_support_amount,quarterly_support_amount=plan_id.quarterly_support_amount,halfyearly_support_amount=plan_id.halfyearly_support_amount,annual_support_amount=plan_id.annual_support_amount,current_api_price=price)
      else:
        plan_purchase_history.objects.create(user = obj_user , User_plan_validation = trans_hash , plan_id = plan_id , Plan_maximum_step = plan_id.Max_step_count , Plan_minimum_step = plan_id.Min_step_count , Plan_maximum_reward = plan_id.reward_amount , Plan_referral_status = plan_id.referral_status , Plan_Two_X_Boost_status = plan_id.two_X_Boost_status , Plan_Withdraw_status = plan_id.withdraw_status , Plan_Level = plan_id.referral_level_eligible , purchase_amount = plan_amount , user_wallet_type = user_wallet_type , buy_type = "Admin Plan Buy",plan_reward_step_val = plan_id.Reward_step_value,plan_per_reward_amount = plan_id.plan_reward_amount,stake_wallet_monthly_split_percentage=plan_id.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=plan_id.withdraw_wallet_monthly_percentage,support_status=plan_id.support_status,monthly_support=plan_id.monthly_support_status,quarterly_support=plan_id.quarterly_support_status,annual_support=plan_id.annual_support_status,plan_purchase_type=plan_id.plan_purchase_type,halfyearly_support=plan_id.halfyearly_support_status,monthly_support_amount=plan_id.monthly_support_amount,quarterly_support_amount=plan_id.quarterly_support_amount,halfyearly_support_amount=plan_id.halfyearly_support_amount,annual_support_amount=plan_id.annual_support_amount,current_api_price=price)

      if plan_id.referral_status == 0:
          obj_user.referral_plan_status = 0
          obj_user.save()
      else:
          obj_user.referral_plan_status = 1
          obj_user.save()

      User_Management.objects.filter(id = obj_user.id).update(plan = plan_id.id)
      
      if obj_user.referal_code != "" or obj_user.referal_code != None:
        
        a=[]
        ref_code = obj_user.referal_code
        
        reff_id = Referral_code.objects.get(referal_code=ref_code)
        referred_user = User_Management.objects.get(id = reff_id.user.id)
        user_level = obj_user.Referral_Level
        Referral_level = referral_level.objects.all().count()
        #Referral_level = 1
        # direct_referrals_count = Referral_code.objects.filter(user=user).count()
        for i in range(Referral_level):
            reff_id = Referral_code.objects.get(referal_code=ref_code)
            referred_user = User_Management.objects.get(id = reff_id.user.id)
            a.append(referred_user.id)
            ref_code = referred_user.referal_code
            if referred_user.referal_code == "" or referred_user.referal_code == None:
                break
        b = 1
        l = 0
        obj_plan_hist = plan_purchase_history.objects.filter(user_id = obj_user.id).count()
        if obj_plan_hist == 1:
          for i in a:
              user = User_Management.objects.get(id = i)
              if user.plan == 0:
                  b = b+1 
                  pass
              else:
                  # for i in a:
                  #     #user = User_Management.objects.get(id=i)
                  #     #direct_referrals = Referral_code.objects.filter(user=i).count()
                  #     direct_referrals = User_Management.objects.filter(reff_id=i,referral_plan_status=1).count()
                      
                  #     # Now you have the direct referral count for the current user
                  #     # You can use direct_referrals_count as needed
                  #     print(f"Direct referrals count for user with ID {direct_referrals}")

                  #     # # If needed, you can perform additional operations based on the direct referral count
                  #     # if user.plan == 0:
                  #     #     b += 1
                  #   # PLan_plan = plan.objects.get(id = user.plan)
                  try:
                      plan_hist=plan_purchase_history.objects.filter(plan_id=user.plan).last()
                  except:
                      plan_hist=''
                  if plan_hist:
                      # if PLan_plan.referral_status == 0:
                      if plan_hist.Plan_referral_status == 0:
                          b = b+1
                          pass
                  # elif user.user_referral_eligible_level >= plan_hist.Plan_Level and plan_hist.Plan_Level >= b:
                                                
                      elif plan_hist.Plan_referral_status == 1:
                          if user.user_referral_eligible_level >= plan_hist.Plan_Level and plan_hist.Plan_Level >= b:
                              User_Referral_level = referral_level.objects.get(referral_level_id=b)
                              uesr_level_actual = b
                              # direct_referrals = User_Management.objects.filter(reff_id=i,referral_plan_status=1).count()
                              direct_referrals = User_Management.objects.filter(reff_id=i,plan__gte=50).count()
                              direct_referrals_count = Referral_code.objects.filter(user=user).count()
                              Market_Price = market_price.objects.get(id=1)
                              if plan_purchase == 1:
                                  Purchase_Amount = Decimal(amunt)
                              else:
                                  Purchase_Amount = Decimal(plan_amount)
                              if direct_referrals >= uesr_level_actual:
                                  winning_level = min(user.user_referral_eligible_level, direct_referrals_count )           
                                  User_Referral_level = referral_level.objects.get(referral_level_id=winning_level)
                                  # print("user_referral_eligible_level:", user.user_referral_eligible_level)
                                  # print("direct_referrals_count:", direct_referrals_count)
                                  # print("direct_referrals:", direct_referrals)
                                  # print("Referral_level:", Referral_level)
                                  # print("User_Referral_level:", User_Referral_level)
                                  # print("referred_user:", referred_user)
                                  # print("uesr_level:", user_level)
                                  # print("uesr_level_actual:", uesr_level_actual)
                                  percentage = (User_Referral_level.commission_amount * Purchase_Amount) / 100
                                  actual_reward = Decimal(percentage)
                                  l = l + actual_reward
                                  userwallet = UserCashWallet.objects.get(userid=i)
                                  userwallet.referalincome = userwallet.referalincome + actual_reward
                                  userwallet.save()
                                  table = Referral_reward_History.objects.create(user=user, referral_id=(obj_user.Name), reward=Decimal(actual_reward))
                              b = b + 1 
                          else:
                              b = b + 1
                              pass
                  else:
                      b = b + 1
                      pass
        sum = 0
        # for i in l:
        #     sum = sum + i
        if plan_purchase == 1:
          admin_profit = Decimal(amunt) - l
          adminprofit = Admin_Profit.objects.create(user = obj_user,admin_profit = admin_profit,Profit_type = "Plan Purchase")
        else:
          admin_profit = plan_amount - l
          adminprofit = Admin_Profit.objects.create(user = obj_user,admin_profit = admin_profit,Profit_type = "Plan Purchase")   
          #user_Detail = User_Management.objects.get(user_name=obj_user.user)
          premium_wallet_deposit.objects.create(user=obj_user.id, email=obj_user.Email, Amount_USDT=plan_amount, Amount_JW=0, Hash='0x1468a5baaaca8d5e927ce129fd3c', status=1, type="User Create", withdraw_amount=0, create_type="Recharge Deposit")
        messages.add_message(request, messages.SUCCESS, 'Plan was added to '+str(obj_user.Name)+' successfully.')
      else:   
        pass
    else:
      usr_mail = obj_plan_purchase_history.user.Email
      messages.add_message(request, messages.ERROR, 'Transaction hash already applied for this user: '+str(usr_mail))
  context["obj_plan"] = obj_plan
  context["Title"] = "Add User Plan"
  context["obj_user"] = obj_user  
  context["market"]=companyqs.market_api_price 
  context["fixed"]=Market_Price.market_price
  
  return render(request,"trade_admin_auth/add_user_plan.html",context)




@check_group_icon_menu("Step Update")
def StepUpdate(request,id):
  context = {}
  context["Title"] = "StepUpdate"
  context["id"] = id
  if request.method == "POST": 
    access_token = request.POST['access_token']
    Date = request.POST['Date']
    epoch_start_time = datetime.datetime.strptime(Date+' 00:00:00', '%Y-%m-%d %H:%M:%S')
    epoch_start_time_milli = int(epoch_start_time.timestamp() * 1000 )
    epoch_end_time = datetime.datetime.strptime(Date+' 23:59:59', '%Y-%m-%d %H:%M:%S')
    epoch_end_time_milli = int(epoch_end_time.timestamp() * 1000 + 999)
    session = requests.Session()
    headers = { 'content-type': 'application/json',
            'Authorization': 'Bearer %s' % access_token }
    payload = {
    "aggregateBy": [{
    "dataTypeName": "com.google.step_count.delta",
    "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
    }],
    "bucketByTime": { "durationMillis": 86400000 },
    "startTimeMillis": epoch_start_time_milli,
    "endTimeMillis": epoch_end_time_milli
    }
    response = session.post("https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate",headers=headers, json=payload)
    if response.status_code != 200:
      context["access_token"] = access_token
      context["Date"] = Date
      messages.add_message(request, messages.ERROR, 'Access Token Expired')
      return render(request, 'trade_admin_auth/step_update.html',context)
    res = response.__dict__['_content'].decode()
    result = json.loads(res)
    bucketresult = result['bucket']
    dataset = bucketresult[0].get('dataset')
    point = dataset[0].get('point')
    if point != []:
      value = point[0].get('value')
      stepvalue = value[0].get('intVal')
    else:
      messages.add_message(request, messages.ERROR, 'No Step Found in Google Fit')
      return render(request, 'trade_admin_auth/step_update.html',context)
    context["stepvalue"] = stepvalue
    context["access_token"] = access_token
    context["Date"] = Date
  return render(request, 'trade_admin_auth/step_update.html',context)


def step_update_access_token(request,id,Date,val):
  context = {}
  context["Title"] = "StepUpdate"
  steps = int(val)
  Date = Date
  user = User_Management.objects.get(id = id)
  try:
    user_step_update_chk = Steps_history.objects.get(user=id,created_on__date = Date)
  except:
    user_step_update_chk = ""
  if user_step_update_chk:
    user_step_update_chk.steps = int(steps)
    user_step_update_chk.save()
    Step_Count = int(steps)
    discount_model = Steps_Management.objects.get(id = 1)
    discount_percent = int(discount_model.Step_discount)
    if discount_percent == 0:
        Step_Count = int(Step_Count)
    else:
      try:
        chk_data = Reward_History.objects.get(created_on__date = Date,user_id = user.id,reward_status = "step_reward")
        if chk_data:
            messages.add_message(request, messages.ERROR, 'Reward was Already Updated to '+str(user.Name))
            return render(request, 'trade_admin_auth/step_update.html',context)
      except:
        Discount_Steps = int((Step_Count * discount_percent) / 100)
        Step_Count = int(Step_Count) - int(Discount_Steps)
        user_step_update_chk.steps = Step_Count
        user_step_update_chk.save()
        Plan = user.plan
        user_wallet = UserCashWallet.objects.get(userid_id = user.id)
        step_count = Step_Count
        if Plan == 0:
            try:
                actual_plan = plan.objects.get(plan_type = 0)
                step_count = int(Step_Count)
                if step_count != 0 and step_count > 0:
                    if step_count < actual_plan.Min_step_count:
                        pass
                    if step_count >= actual_plan.Max_step_count:
                        value = int(actual_plan.Max_step_count/1500)
                        reward = Decimal(value/10)
                        user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal(round(reward,2))
                        user_wallet.save()
                        table = Reward_History.objects.create(user = user,steps = (step_count),Reward = Decimal(round(reward,2)),created_on = Date+" 00:00:45.270177")
                    if (step_count > actual_plan.Min_step_count) and (step_count < actual_plan.Max_step_count):
                        value = int(step_count/1500)
                        reward = Decimal(value/10)
                        user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal((round(reward,2)))
                        user_wallet.save()
                        table = Reward_History.objects.create(user = user,steps = (step_count),Reward = Decimal(round(reward,2)),created_on = Date+" 00:00:45.270177")
                else:
                    pass
            except:
                pass
            messages.add_message(request, messages.SUCCESS, 'Reward was Updated to '+str(user.Name)+' successfully.')
            return HttpResponseRedirect("/tradeadmin/List_User_Management/")
        else:
            actual_plan = plan_purchase_history.objects.filter(user = user.id).last()
            step_count = int(Step_Count)
            if step_count != 0 and step_count > 0:
                if step_count <  actual_plan.Plan_minimum_step:
                    pass
                if step_count >= actual_plan.Plan_maximum_step:
                    value = int(actual_plan.Plan_maximum_step/1500)
                    reward = Decimal(value/10)
                    user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal(round(reward,2))
                    user_wallet.save()
                    table = Reward_History.objects.create(user = user,steps = (step_count),Reward = Decimal(round(reward,2)),created_on = Date+" 00:00:45.270177")
                if (step_count > actual_plan.Plan_minimum_step) and (step_count < actual_plan.Plan_maximum_step):
                    value = int(step_count/1500)
                    reward = Decimal(value/10)
                    user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal(round(reward,2))
                    user_wallet.save()
                    table = Reward_History.objects.create(user = user,steps = (step_count),Reward = Decimal(round(reward,2)),created_on = Date+" 00:00:45.270177")
            else:
                pass
            messages.add_message(request, messages.SUCCESS, 'Reward was Updated to '+str(user.Name)+' successfully.')
            return HttpResponseRedirect("/tradeadmin/List_User_Management/")


def check_valid(request,id,Date,val):
  context = {}
  context["Title"] = "StepUpdate"
  context["stepvalue"] = val
  context["id"] = id
  context["Date"] = Date
  User = User_Management.objects.get(id = id)
  Date = Date
  try:
    steps = Steps_history.objects.get(user = User.id,created_on__date = Date)
    if steps:
      context["sum"] = 0
      messages.add_message(request, messages.SUCCESS, str(User.Name)+' is Eligible for Recover Steps')
      return render(request, 'trade_admin_auth/step_update.html',context)
  except:
      context["sum"] = 1
      messages.add_message(request, messages.ERROR, str(User.Name)+' is Not Eligible for Recover Steps')
      return render(request, 'trade_admin_auth/step_update.html',context)
  return render(request, 'trade_admin_auth/step_update.html',context)


@check_group("Manage User")
def PlanDateEdit(request,id):
  context = {}
  try:
    obj_user = User_Management.objects.get(id = id)
  except:
    obj_user = ""
  obj_wall_blnc = UserCashWallet.objects.get(userid_id = obj_user.id)
  obj_wall_flush_blnc = wallet_flush_history.objects.filter(user_id = obj_user.id).last()
  if request.method == "POST":
    end_date = request.POST["plan_end_date"] 
    try:
      old_blnc = request.POST['blnc_check']
    except: 
      if end_date:
        old_blnc = 0
      else:
        old_blnc = 2
    if int(old_blnc) == 1 and end_date:
      UserCashWallet.objects.filter(userid_id = obj_user.id).update(balanceone = obj_wall_flush_blnc.wallet_balanceone , referalincome = obj_wall_flush_blnc.Wallet_referral_income)
      User_Management.objects.filter(id = id).update(plan_end_date = end_date)
      PlanDateUpdateHistory.objects.create(user = obj_user.Name,email = obj_user.Email,plan_name = obj_user.plan,planstart_date = obj_user.plan_start_date,planend_date = obj_user.plan_end_date,plan_updated_end_date = end_date)
      messages.add_message(request, messages.SUCCESS,'Plan Date and Balance Updated successfully')
      return HttpResponseRedirect("/tradeadmin/user_history_table/"+(id)+"/")
    elif int(old_blnc) == 1:
      UserCashWallet.objects.filter(userid_id = obj_user.id).update(balanceone = obj_wall_flush_blnc.wallet_balanceone , referalincome = obj_wall_flush_blnc.Wallet_referral_income)
      User_Management.objects.filter(id = id).update(plan_end_date = obj_user.plan_end_date)
      PlanDateUpdateHistory.objects.create(user = obj_user.Name,email = obj_user.Email,plan_name = obj_user.plan,planstart_date = obj_user.plan_start_date,planend_date = obj_user.plan_end_date,plan_updated_end_date = end_date)
      messages.add_message(request, messages.SUCCESS,'Balance Updated successfully')
      return HttpResponseRedirect("/tradeadmin/user_history_table/"+(id)+"/")
    elif end_date:
      User_Management.objects.filter(id = id).update(plan_end_date = end_date)
      PlanDateUpdateHistory.objects.create(user = obj_user.Name,email = obj_user.Email,plan_name = obj_user.plan,planstart_date = obj_user.plan_start_date,planend_date = obj_user.plan_end_date,plan_updated_end_date = end_date)
      messages.add_message(request, messages.SUCCESS,'Plan Date Updated successfully')
      return HttpResponseRedirect("/tradeadmin/user_history_table/"+(id)+"/")
    else:
      1
    
  
  context["obj_wall_blnc"] = obj_wall_blnc
  context['obj_wall_flush_blnc'] = obj_wall_flush_blnc
  context["obj_user"] = obj_user
  context["Title"] = "Plan Date Edit"
  return render(request,'trade_admin_auth/plan_edit_date.html',context)




def disable_withdraw(request):
  status = Steps_Management.objects.get(id = 1)
  if int(status.status) == 0:
    status.status = 1
    status.save()
    messages.add_message(request, messages.SUCCESS,' Withdraw Disabled')
    return redirect('/tradeadmin/dashboard')
  if int(status.status) == 1:
    status.status = 0
    status.save()
    messages.add_message(request, messages.SUCCESS,' Withdraw Enabled')
    return redirect('/tradeadmin/dashboard')
  
def disable_pay_later(request):
  status = Steps_Management.objects.get(id = 1)
  if int(status.isAdminEnablePayLater) == 0:
    status.isAdminEnablePayLater = 1
    status.save()
    messages.add_message(request, messages.SUCCESS,' Pay later Disabled')
    return redirect('/tradeadmin/dashboard')
  if int(status.isAdminEnablePayLater) == 1:
    status.isAdminEnablePayLater = 0
    status.save()
    messages.add_message(request, messages.SUCCESS,' Pay later Enabled')
    return redirect('/tradeadmin/dashboard')
  
  
  
def isStakeEnable(request):
  status = Steps_Management.objects.get(id = 1)
  if int(status.isStakeEnable) == 0:
    status.isStakeEnable = 1
    status.save()
    messages.add_message(request, messages.SUCCESS,' isStake Disabled')
    return redirect('/tradeadmin/dashboard')
  if int(status.isStakeEnable) == 1:
    status.isStakeEnable = 0
    status.save()
    messages.add_message(request, messages.SUCCESS,' isStake Enabled')
    return redirect('/tradeadmin/dashboard')
  
  
def isPremiumEnable(request):
  status = Steps_Management.objects.get(id = 1)
  if int(status.isPremiumEnable) == 0:
    status.isPremiumEnable = 1
    status.save()
    messages.add_message(request, messages.SUCCESS,' isPremium Disabled')
    return redirect('/tradeadmin/dashboard')
  if int(status.isPremiumEnable) == 1:
    status.isPremiumEnable = 0
    status.save()
    messages.add_message(request, messages.SUCCESS,' isPremium Enabled')
    return redirect('/tradeadmin/dashboard')


def isAdminEnableRrWithdraw(request):
  status = Steps_Management.objects.get(id = 1)
  if int(status.isAdminEnableRrWithdraw) == 0:
    status.isAdminEnableRrWithdraw = 1
    status.save()
    messages.add_message(request, messages.SUCCESS,' isAdminEnableRrWithdraw Disabled')
    return redirect('/tradeadmin/dashboard')
  if int(status.isAdminEnableRrWithdraw) == 1:
    status.isAdminEnableRrWithdraw = 0
    status.save()
    messages.add_message(request, messages.SUCCESS,' isAdminEnableRrWithdraw Enabled')
    return redirect('/tradeadmin/dashboard')
  
def isAdminEnableHrWithdraw(request):
  status = Steps_Management.objects.get(id = 1)
  if int(status.isAdminEnableHrWithdraw) == 0:
    status.isAdminEnableHrWithdraw = 1
    status.save()
    messages.add_message(request, messages.SUCCESS,' isAdminEnableHrWithdraw Disabled')
    return redirect('/tradeadmin/dashboard')
  if int(status.isAdminEnableHrWithdraw) == 1:
    status.isAdminEnableHrWithdraw = 0
    status.save()
    messages.add_message(request, messages.SUCCESS,' isAdminEnableHrWithdraw Enabled')
    return redirect('/tradeadmin/dashboard')

@check_group("Plan Management")
def Plan_Expired_Date_Users_List(request):
  context = {}
  plan_usr = 0
  plan_count = 0
  plan_dict_users = {}
  plan_start_page = request.GET.get('pageno', 1)
  plan_end_value = int(plan_start_page) * 10
  plan_start_value = int(plan_end_value) - 9

  today = datetime.datetime.now()

  try:
    email_search = request.GET['Email']
  except:
    email_search = ""

  if email_search:
    user_obj = User_Management.objects.filter(plan_end_date__date = today.date()).filter(Email__icontains = email_search).order_by('plan_end_date')
    for i in user_obj:
      if i.plan == 0:
        plan_id = "Free plan"
      else:
        plan_ins = plan.objects.get(id = i.plan)
        plan_id = plan_ins.plan_name
      plan_usr = plan_usr + 1
      plan_list_usr = {}
      if plan_start_value <= plan_usr <= plan_end_value:
        plan_count = plan_count + 1
        plan_list_usr["id"] = str(i.id)
        plan_list_usr["username"] = (i.Name)
        plan_list_usr["plan"] = (plan_id)
        plan_list_usr["email"] = (i.Email)
        plan_list_usr["start_date"] = (str(i.plan_start_date))
        plan_list_usr["end_date"] = (str(i.plan_end_date))
        plan_list_usr["pageno"] = plan_start_page
        plan_list_usr["sno"] = plan_usr
        plan_dict_users[plan_count] = plan_list_usr
  else:
    user_obj = User_Management.objects.filter(plan_end_date__date = today.date()).order_by('plan_end_date')
    for i in user_obj:
      if i.plan == 0:
        plan_id = "Free plan"
      else:
        plan_ins = plan.objects.get(id = i.plan)
        plan_id = plan_ins.plan_name
      plan_usr = plan_usr + 1
      plan_list_usr = {}
      if plan_start_value <= plan_usr <= plan_end_value:
        plan_count = plan_count + 1
        plan_list_usr["id"] = str(i.id)
        plan_list_usr["username"] = (i.Name)
        plan_list_usr["plan"] = (plan_id)
        plan_list_usr["email"] = (i.Email)
        plan_list_usr["start_date"] = (str(i.plan_start_date))
        plan_list_usr["end_date"] = (str(i.plan_end_date))
        plan_list_usr["pageno"] = plan_start_page
        plan_list_usr["sno"] = plan_usr
        plan_dict_users[plan_count] = plan_list_usr
  try:
    tot_plan_user_qs = user_obj
  except:
    tot_plan_user_qs = ""
  w_page_3 = request.GET.get('pageno', 1)
  w_paginator_3 = Paginator(tot_plan_user_qs, 10)
  try:
      plan_hist_qs = w_paginator_3.page(w_page_3)
  except PageNotAnInteger:
      plan_hist_qs =w_paginator_3.page(1)
  except EmptyPage:
      plan_hist_qs = w_paginator_3.page(w_paginator_3.num_pages)

  context['plan_hist_qs'] = plan_hist_qs
  context["plan_endpage"] = plan_hist_qs.number+1
  context["plan_startpage"] = plan_hist_qs.number-1
  context['plan_start_value'] = plan_hist_qs.start_index()
  context['plan_end_value'] = plan_hist_qs.end_index()
  context['plan_usr_count'] = user_obj.count()
  context["plan_dict_users"] = json.dumps(plan_dict_users)
  context["Title"] = "Plan Expired Users List"
  return render(request,'trade_admin_auth/plan_expired_users_list.html',context)




def disable_buy_plan(request):
  status = admin_referral_code.objects.get(id = 1)
  if int(status.status) == 0:
    status.status = 1
    status.save()
    messages.add_message(request, messages.SUCCESS,' Buy Plan Disabled')
    return redirect('/tradeadmin/dashboard')
  if int(status.status) == 1:
    status.status = 0
    status.save()
    messages.add_message(request, messages.SUCCESS,' Buy Plan Enabled')
    return redirect('/tradeadmin/dashboard')


def admin_user_shift_plan(request,id):
  User = User_Management.objects.get(id = int(id))
  Current_plan_id = int(User.plan)
  if int(Current_plan_id) != 0:
      current_plan = plan.objects.get(id = int(Current_plan_id))
      user_current_plan_history = plan_purchase_history.objects.filter(user_id = User.id).last()
      if int(user_current_plan_history.Plan_Two_X_Boost_status) == 1:
        messages.add_message(request, messages.ERROR, str(User.Name)+'  Plan Already Shifted')
        return HttpResponseRedirect('/tradeadmin/List_User_Management/')
      if int(user_current_plan_history.plan_id_id) == int(Current_plan_id):
          user_current_plan_history.Plan_maximum_step = current_plan.Max_step_count
          user_current_plan_history.Plan_minimum_step = current_plan.Min_step_count
          user_current_plan_history.Plan_maximum_reward = current_plan.reward_amount
          user_current_plan_history.plan_per_reward_amount = current_plan.plan_reward_amount
          user_current_plan_history.plan_reward_step_val = current_plan.Reward_step_value
          user_current_plan_history.Plan_Two_X_Boost_status = current_plan.two_X_Boost_status
          user_current_plan_history.Plan_referral_status = current_plan.referral_status
          user_current_plan_history.Plan_Level = current_plan.level
          user_current_plan_history.Plan_Withdraw_status = current_plan.withdraw_status
          user_current_plan_history.created_on = datetime.datetime.now()
          user_current_plan_history.save()
          messages.add_message(request, messages.SUCCESS, str(User.Name)+'  Plan Shifted Successfully')
          return HttpResponseRedirect('/tradeadmin/List_User_Management/')
      else:
          messages.add_message(request, messages.ERROR, str(User.Name)+'  Shift Plan Not Applicable')
          return HttpResponseRedirect('/tradeadmin/List_User_Management/')
  else:
      if int(User.Two_X_Boost_status) == 1:
        messages.add_message(request, messages.ERROR, str(User.Name)+'  Plan Already Shifted')
        return HttpResponseRedirect('/tradeadmin/List_User_Management/')
      current_plan = plan.objects.get(plan_type = 0)
      User.reward_step_amount = current_plan.plan_reward_amount
      User.reward_steps = current_plan.Reward_step_value
      User.user = current_plan.Min_step_count
      User.over_all_stepcount = current_plan.Max_step_count
      User.Two_X_Boost_status = current_plan.two_X_Boost_status
      User.withdraw_status = current_plan.withdraw_status
      User.save()
      messages.add_message(request, messages.SUCCESS, str(User.Name)+'  Plan Shifted Successfully')
      return HttpResponseRedirect('/tradeadmin/List_User_Management/')



class List_wallet(ListView):
    model = Plan_purchase_wallet
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return Plan_purchase_wallet.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(List_wallet, self).get_context_data(**kwargs)
        context['Title'] = 'Wallet List'
        adminactivity_qs = Plan_purchase_wallet.objects.all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        Adminactivitytable = Wallet_Table(adminactivity_qs)
        context['table'] = Adminactivitytable
        context['add_title'] ='Add Plan'
        context['Btn_url'] = 'trade_admin_auth:Addplan'
        context['activecls']='Listwallet'
        return context
    
    @method_decorator(check_group("Wallet Management"))
    def dispatch(self, *args, **kwargs):
      return super(List_wallet, self).dispatch(*args, **kwargs)



class Edit_wallet(UpdateView):
    model = Plan_purchase_wallet
    form_class = List_Wallet_Form
    template_name = 'trade_admin_auth/edit_wallet_status.html'   
    def get_context_data(self, **kwargs):
       context = super(Edit_wallet, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
      #  user = Plan_purchase_wallet.objects.get(id = p_key )
      #  context['Pic'] = user.user_profile_pic
       context['Title'] = 'Edit User'
       context['Btn_url'] = 'trade_admin_auth:List_wallet'
       return context

    @method_decorator(check_group("Wallet Management"))
    def dispatch(self, *args, **kwargs):
      return super(Edit_wallet, self).dispatch(*args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Wallet Details updated successfully.')
       return HttpResponseRedirect('/tradeadmin/List_wallet')


import datetime
# Missing reward update function
@check_group_icon_menu("Missing reward update")
def missing_reward_update_admin(request,id):
  context = {}
  if request.method == "POST":
    Date =  request.POST['Date']
    date_obj = datetime.strptime(Date, '%Y-%m-%d %H:%M:%S')
    user_details=User_Management.objects.get(id = id) 
    try:
        chk_data = Reward_History.objects.get(created_on__date = (date_obj.date()),user_id = user_details.id,reward_status = "step_reward")
        if chk_data:
          messages.add_message(request, messages.SUCCESS, 'Reward already updated')
          return HttpResponseRedirect('/tradeadmin/List_User_Management')
    except:
        try:
            chk_data = Steps_history.objects.get(created_on__date = (date_obj.date()),user_id = user_details.id)
            if chk_data:
                Plan = user_details.plan
                user_wallet = UserCashWallet.objects.get(userid_id = user_details.id)
                chk_data.status = 1
                chk_data.modified_on = datetime.now()
                chk_data.save()
                if Plan == 0:
                    try:
                        actual_plan = plan.objects.get(plan_type = 0)
                        value = Decimal(int(user_details.over_all_stepcount)/int(user_details.reward_steps))
                        reward = Decimal(value*user_details.reward_step_amount)
                        user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal(round(reward,2))
                        user_wallet.save()
                        chk_data.steps = int(user_details.over_all_stepcount)
                        chk_data.save()
                        if(str(date_obj.date()) == "2022-12-23") :
                            table = Reward_History.objects.create(user = user_details,steps = int(user_details.over_all_stepcount),Reward = Decimal((reward)),created_on = str(date_obj.date())+" 00:00:45.270177")
                        else:
                            table = Reward_History.objects.create(user = user_details,steps = int(user_details.over_all_stepcount),Reward = Decimal((reward)),created_on = str(date_obj.date())+" 18:45:22.270177")
                    except:
                        pass
                else:
                    actual_plan = plan_purchase_history.objects.filter(user = user_details.id).last()
                    value = Decimal(actual_plan.Plan_maximum_step/int(actual_plan.plan_reward_step_val))
                    # reward = Decimal(value*actual_plan.plan_per_reward_amount)
                    reward = Decimal(actual_plan.Plan_maximum_reward)
                    user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal((reward))
                    user_wallet.save()
                    chk_data.steps = int(actual_plan.Plan_maximum_step)
                    chk_data.save()
                    if(str(date_obj.date()) == "2022-12-23") :
                        table = Reward_History.objects.create(user = user_details,steps = int(actual_plan.Plan_maximum_step),Reward = Decimal((reward)),created_on = str(date_obj.date())+" 00:00:45.270177")
                    else:
                        table = Reward_History.objects.create(user = user_details,steps = int(actual_plan.Plan_maximum_step),Reward = Decimal((reward)),created_on = str(date_obj.date())+" 18:45:22.270177")
            messages.add_message(request, messages.SUCCESS, 'Reward updated')
            return HttpResponseRedirect('/tradeadmin/List_User_Management')
        except:
            chk_data = Steps_history.objects.create(created_on = str(date_obj)+".000000",user_id = user_details.id)
            if chk_data:
                Plan = user_details.plan
                user_wallet = UserCashWallet.objects.get(userid_id = user_details.id)
                chk_data.status = 1
                chk_data.modified_on = datetime.now()
                chk_data.save()
                if Plan == 0:
                    try:
                        actual_plan = plan.objects.get(plan_type = 0)
                        value = Decimal(int(user_details.over_all_stepcount)/int(user_details.reward_steps))
                        reward = Decimal(value*user_details.reward_step_amount)
                        user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal(round(reward,2))
                        user_wallet.save()
                        chk_data.steps = int(user_details.over_all_stepcount)
                        chk_data.save()
                        if(str(date_obj.date()) == "2022-12-23") :
                            table = Reward_History.objects.create(user = user_details,steps = int(user_details.over_all_stepcount),Reward = Decimal((reward)),created_on = str(date_obj.date())+" 00:00:45.270177")
                        else:
                            table = Reward_History.objects.create(user = user_details,steps = int(user_details.over_all_stepcount),Reward = Decimal((reward)),created_on = str(date_obj.date())+" 18:45:22.270177")
                    except:
                        pass
                else:
                    actual_plan = plan_purchase_history.objects.filter(user = user_details.id).last()
                    value = Decimal(actual_plan.Plan_maximum_step/int(actual_plan.plan_reward_step_val))
                    # reward = Decimal(value*actual_plan.plan_per_reward_amount)
                    reward = Decimal(actual_plan.Plan_maximum_reward)
                    user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal((reward))
                    user_wallet.save()
                    chk_data.steps = int(actual_plan.Plan_maximum_step)
                    chk_data.save()
                    if(str(date_obj.date()) == "2022-12-23") :
                        table = Reward_History.objects.create(user = user_details,steps = int(actual_plan.Plan_maximum_step),Reward = Decimal((reward)),created_on = str(date_obj.date())+" 00:00:45.270177")
                    else:
                        table = Reward_History.objects.create(user = user_details,steps = int(actual_plan.Plan_maximum_step),Reward = Decimal((reward)),created_on = str(date_obj.date())+" 18:45:22.270177")
            messages.add_message(request, messages.SUCCESS, 'Reward updated')
            return HttpResponseRedirect('/tradeadmin/List_User_Management')
  context["Title"] = "Missing Reward Update"
  return render(request,'trade_admin_auth/missing_reward_update.html',context)




# Download CSV for all users file function

def download_CSV(request):
 
  if request.method == "POST":
    try:
      str_date = request.POST["start_date"]
      end_date = request.POST["end_date"]
    except:
      str_date = ""
      end_date = ""

    try:
      obj_withdraw = Withdraw.objects.values('userid__Name','userid__Email','Wallet_type','Amount','Withdraw_USDT','Withdraw_JW','Address','Transaction_Hash','created_on').filter(created_on__date__gte = str_date , created_on__date__lte = end_date).order_by('created_on')
    except:
      obj_withdraw = ""

    if obj_withdraw:
      re_count = obj_withdraw.count()

      if(re_count > 0):
        data = list(obj_withdraw)
        res_data = {"status" : "true" , "data" : data , "start_date" : str_date , "end_date" : end_date}
      else:
        data =''
        res_data = {"status" : "false" , "data" : data}
    else:
      data =''
      res_data = {"status" : "false" , "data" : data , "start_date" : str_date , "end_date" : end_date}

    return JsonResponse(res_data)


# Download CSV for individual users file function

def download_CSV_single_user(request,id):
 
  if request.method == "POST":
    try:
      str_date = request.POST["start_date"]
      end_date = request.POST["end_date"]
    except:
      str_date = ""
      end_date = ""

    try:
      # obj_user = User_Management.objects.get(id = id)
      obj_withdraw = Withdraw.objects.values('userid__Name','userid__Email','Amount','Withdraw_USDT','Withdraw_JW','Address','Transaction_Hash','created_on').filter(created_on__date__gte = str_date , created_on__date__lte = end_date).filter(userid_id = id).order_by('created_on')
    except:
      obj_withdraw = ""

    if obj_withdraw:
      re_count = obj_withdraw.count()

      if(re_count > 0):
        data = list(obj_withdraw)
        res_data = {"status" : "true" , "data" : data , "start_date" : str_date , "end_date" : end_date}
      else:
        data =''
        res_data = {"status" : "true" , "data" : data}
    else:
      data =''
      res_data = {"status" : "false" , "data" : data , "start_date" : str_date , "end_date" : end_date}

    return JsonResponse(res_data)


# Download CSV for user_management file function
def download_CSV_user_report(request):
  if request.method == "POST":
    try:
      str_date = request.POST["start_date"]
      end_date = request.POST["end_date"]
    except:
      str_date = ""
      end_date = ""

    try:
      obj_user = User_Management.objects.values('Name','Email','Referral_id','Direct_referral_id','User_type','created_on').filter(created_on__date__gte = str_date , created_on__date__lte = end_date).order_by('created_on')
    except:
      obj_user = ""

    if obj_user:
      re_count = obj_user.count()

      if(re_count > 0):
        data = list(obj_user)
        res_data = {"status" : "true" , "data" : data , "start_date" : str_date , "end_date" : end_date}
      else:
        data =''
        res_data = {"status" : "true" , "data" : data}
    else:
      data =''
      res_data = {"status" : "false" , "data" : data , "start_date" : str_date , "end_date" : end_date}

    return JsonResponse(res_data)

# Download CSV for send withdraw request file function
def download_CSV_sendwithdraw_report(request):
  if request.method == "POST":
    try:
      str_date = request.POST["start_date"]
      end_date = request.POST["end_date"]
    except:
      str_date = ""
      end_date = ""

    try:
      obj_user = WithdrawSendHistory.objects.values('user','claim_amount','from_address','to_address','Transaction_Hash','currency','created_on').filter(created_on__date__gte = str_date , created_on__date__lte = end_date).order_by('created_on')
    except:
      obj_user = ""

    if obj_user:
      re_count = obj_user.count()

      if(re_count > 0):
        data = list(obj_user)
        res_data = {"status" : "true" , "data" : data , "start_date" : str_date , "end_date" : end_date}
      else:
        data =''
        res_data = {"status" : "true" , "data" : data}
    else:
      data =''
      res_data = {"status" : "false" , "data" : data , "start_date" : str_date , "end_date" : end_date}

    return JsonResponse(res_data)


def download_CSV_device_id(request):
 
  if request.method == "POST":
    try:
      unique = request.POST["device_id"]
    except:
      unique = ""
    try:
      obj_user = User_Management.objects.values('Name','Email','device_unique_id','User_type','user_phone_number','created_on').filter(device_unique_id = unique).order_by('created_on')
    except:
      obj_user = ""

    if obj_user:
      re_count = obj_user.count()

      if(re_count > 0):
        data = list(obj_user)
        res_data = {"status" : "true" , "data" : data , "device_id" : unique}
      else:
        data =''
        res_data = {"status" : "true" , "data" : data}
    else:
      data =''
      res_data = {"status" : "false" , "data" : data , "device_id" : unique}
    return JsonResponse(res_data)
  
def download_CSV_full_device_id(request):
  if request.method == "POST":
    try:
      obj_username = User_Management.objects.raw('SELECT id, Email , Name , user_phone_number,status , device_unique_id ,COUNT(*) as user_profile_pic FROM `USPzTPzfNdmGTlER` GROUP by device_unique_id HAVING user_profile_pic >= 2 ORDER BY user_profile_pic')
    except:
      obj_username = ""
    serializer = User_device_see(obj_username,many=True)
    obj_user=serializer.data
    for total_count in User_Management.objects.raw(' SELECT id,COUNT(*) as counts FROM (SELECT id ,COUNT(*) as user_profile_pic FROM USPzTPzfNdmGTlER GROUP by device_unique_id HAVING user_profile_pic >= 2 ) AS DerivedTableAlias '):
      if obj_user:
        re_count = total_count.counts
        if(re_count > 0):
          data = list(obj_user)
          res_data = {"status" : "true" , "data" : data , "device_id" : obj_user}
        else:
          data =''
          res_data = {"status" : "true" , "data" : data}
      else:
        data =''
        res_data = {"status" : "false" , "data" : data , "device_id" : obj_user}
    return JsonResponse(res_data)

# Withdraw send request listing
class List_Send_Withdraw_History(ListView):
    model = WithdrawSendHistory
    template_name = 'trade_admin_auth/sendwithdrawhistory_list.html'
    def get_queryset(self, **kwargs):
      return WithdrawSendHistory.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(List_Send_Withdraw_History, self).get_context_data(**kwargs)
        context['Title'] = 'Send Withdraw Management'
  
        try:
          wallet_address = self.request.GET['wallet_address']
        except:
          wallet_address = ""
        try:
          email = self.request.GET['email']
        except:
          email = ""
        usr = 0
        count = 0
        dict_withdraw = {}
        start_page = self.request.GET.get('pageno', 1)
        end_value = int(start_page) * 10
        start_value = int(end_value) - 9
        if wallet_address:
          obj_withdraw = WithdrawSendHistory.objects.filter(from_address = wallet_address).order_by('-id')
          for i in obj_withdraw:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              list_usr["username"] = (i.user)
              list_usr["email"] = str(i.email.Email)
              list_usr["Amount"] = str(i.claim_amount)
              list_usr["frm_addrs"] = (i.from_address)
              list_usr["to_addrs"] = (i.to_address)
              list_usr["Transaction_Hash"] = (i.Transaction_Hash)
              list_usr["status"] = i.send_status
              list_usr["date"] = str(i.created_on)
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_withdraw[count] = list_usr
        elif email:
          obj_withdraw = WithdrawSendHistory.objects.filter(email__Email__icontains = email).order_by('-id')
          for i in obj_withdraw:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              list_usr["username"] = (i.user)
              list_usr["email"] = str(i.email.Email)
              list_usr["Amount"] = str(i.claim_amount)
              list_usr["frm_addrs"] = (i.from_address)
              list_usr["to_addrs"] = (i.to_address)
              list_usr["Transaction_Hash"] = (i.Transaction_Hash)
              list_usr["status"] = i.send_status
              list_usr["date"] = str(i.created_on)
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_withdraw[count] = list_usr
        else:
          obj_withdraw = WithdrawSendHistory.objects.all().order_by('-id')
          for i in obj_withdraw:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              list_usr["username"] = (i.user)
              list_usr["email"] = str(i.email.Email)
              list_usr["Amount"] = str(i.claim_amount)
              list_usr["frm_addrs"] = (i.from_address)
              list_usr["to_addrs"] = (i.to_address)
              list_usr["Transaction_Hash"] = (i.Transaction_Hash)
              list_usr["status"] = i.send_status
              list_usr["date"] = str(i.created_on)
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_withdraw[count] = list_usr
        try:
          tot_user_qs = obj_withdraw
        except:
          tot_user_qs = ""
        w_page = self.request.GET.get('pageno', 1)
        w_paginator = Paginator(tot_user_qs, 10)
        try:
            withdraw_qs = w_paginator.page(w_page)
        except PageNotAnInteger:
            withdraw_qs =w_paginator.page(1)
        except EmptyPage:
            withdraw_qs = w_paginator.page(w_paginator.num_pages)

        context["endpage"] = withdraw_qs.number+1
        context["startpage"] = withdraw_qs.number-1
        context['start_value'] = withdraw_qs.start_index()
        context['end_value'] = withdraw_qs.end_index()
        context['usr_count'] = obj_withdraw.count()
        context['withdraw_qs'] = withdraw_qs
        context['dict_withdraw'] = json.dumps(dict_withdraw) 
        context['add_title'] ='Withdraw Table'
        context['Btn_url'] = 'trade_admin_auth:List_Send_Withdraw_History'
        return context
    

    @method_decorator(check_group("Transfer Management"))
    def dispatch(self, *args, **kwargs):
      return super(List_Send_Withdraw_History, self).dispatch(*args, **kwargs)

class List_admin_notification_message(ListView):
    model = admin_notification_message
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return plan.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(List_admin_notification_message, self).get_context_data(**kwargs)
        context['Title'] = 'Notification List'
        adminactivity_qs = admin_notification_message.objects.all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        Adminactivitytable = List_admin_notification_message_Table(adminactivity_qs)
        context['table'] = Adminactivitytable
        context['add_title'] ='Add Plan'
        context['Btn_url'] = 'trade_admin_auth:Addplan'
        return context
    
    @method_decorator(check_group("Notification Management"))
    def dispatch(self, *args, **kwargs):
      return super(List_admin_notification_message, self).dispatch(*args, **kwargs)


class Edit_admin_notification_message(UpdateView):
    model = admin_notification_message
    form_class = admin_notification_message_Form
    template_name = 'trade_admin_auth/edit_notification_management.html'   
    def get_context_data(self, **kwargs):
       context = super(Edit_admin_notification_message, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       user = admin_notification_message.objects.get(id = p_key )
       context['Btn_url'] = 'trade_admin_auth:List_admin_notification_message'
       context['Title'] = 'Edit Notification Management'
       return context
    
    @method_decorator(check_group("Notification Management"))
    def dispatch(self, *args, **kwargs):
      return super(Edit_admin_notification_message, self).dispatch(*args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Notification Management updated successfully.')
       return HttpResponseRedirect('/tradeadmin/List_admin_notification_message/')




# Add Duplicate Users
@check_group("Manage User")
def Add_Register_User(request):
  context = {}
  context["Title"] = "Add Register User"
  if request.method == "POST":
    user__name = request.POST['user_name']
    email = request.POST['email']
    code = request.POST['ref_code']
    user_type = request.POST['user_type']
    
    phone_number = ""
    try:
        phone_number = request.POST['Phone_Number']
    except:
        phone_number = ""
    N = 12
    radmon_username = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
      for i in range(N))
    Email_count = User_Management.objects.filter(Email = email).count()
    if Email_count > 0 :
      messages.add_message(request, messages.ERROR, 'User Already Exists')
      return HttpResponseRedirect('/tradeadmin/Add_Register_User/')
    if phone_number != "":
        Phone_Number_Count = User_Management.objects.filter(user_phone_number = phone_number).count()
        if Phone_Number_Count > 0 :
          messages.add_message(request, messages.ERROR, 'Phone Number Already Exists')
          return HttpResponseRedirect('/tradeadmin/Add_Register_User/')
    try :
        User.objects.get(username = radmon_username)
        messages.add_message(request, messages.ERROR, 'Please Try Again')
        return HttpResponseRedirect('/tradeadmin/Add_Register_User/')
    except:                
        if code == "" and user__name == "" and email == "" and user_type == "":
          messages.add_message(request, messages.ERROR, 'Enter required field')
          return HttpResponseRedirect('/tradeadmin/Add_Register_User/')
        device_id = radmon_username
        if user_type == "IOS":
            if code == "":
                ref_code = ""
                user = User.objects.create(username = radmon_username)
                step = Steps_Management.objects.get(id = 1)
                free_days = step.free_plan_days
                withdraw = withdraw_values.objects.get(id = 1)
                plan_plan = plan.objects.get(plan_type = 0)
                user_details = User_Management.objects.create(Email = email,User_type = user_type,status = 0,user_name = radmon_username,User_Device_id = device_id,User_Verification_Status = "pinset",referal_code = code,Name = user__name,Health_Withdraw_min_value=withdraw.Health_wallet_minimum_withdraw_limit,Health_Withdraw_max_value = withdraw.Health_wallet_maximum_withdraw_limit,Referral_Withdraw_min_value = withdraw.Referral_wallet_minimum_withdraw_limit,Referral_Withdraw_max_value = withdraw.Referral_wallet_maximum_withdraw_limit,reward_steps = plan_plan.Reward_step_value,reward_step_amount = plan_plan.plan_reward_amount,withdraw_status = plan_plan.withdraw_status,Two_X_Boost_status = 1,user = plan_plan.Min_step_count,over_all_stepcount = plan_plan.Max_step_count,user_phone_number = phone_number,user_info = "Admin")
                date = user_details.created_on + timedelta(free_days)
                user_details.plan_end_date = date
                user_details.save()
                token = Token.objects.create(user = user)
                get_user = User_Management.objects.get(Email = email)
                tokenkey = token.key
                referral__table(request,tokenkey,code)
            else:
                try:
                    user_ref = Referral_code.objects.get(referal_code = code )
                    if user_ref:
                        user = User.objects.create(username = radmon_username)
                        step = Steps_Management.objects.get(id = 1)
                        free_days = step.free_plan_days
                        withdraw = withdraw_values.objects.get(id = 1)
                        plan_plan = plan.objects.get(plan_type = 0)
                        user_details = User_Management.objects.create(Email = email,User_type = user_type,status = 0,user_name = radmon_username,User_Device_id = device_id,User_Verification_Status = "pinset",referal_code = code,Name = user__name,Health_Withdraw_min_value=withdraw.Health_wallet_minimum_withdraw_limit,Health_Withdraw_max_value = withdraw.Health_wallet_maximum_withdraw_limit,Referral_Withdraw_min_value = withdraw.Referral_wallet_minimum_withdraw_limit,Referral_Withdraw_max_value = withdraw.Referral_wallet_maximum_withdraw_limit,reward_steps = plan_plan.Reward_step_value,reward_step_amount = plan_plan.plan_reward_amount,withdraw_status = plan_plan.withdraw_status,Two_X_Boost_status = 1,user = plan_plan.Min_step_count,over_all_stepcount = plan_plan.Max_step_count,user_phone_number = phone_number,user_info = "Admin")
                        date = user_details.created_on + timedelta(free_days)
                        user_details.plan_end_date = date
                        user_details.save()
                        token = Token.objects.create(user = user)
                        get_user = User_Management.objects.get(Email = email)
                        tokenkey = token.key
                        referral__table(request,tokenkey,code)
                    else:
                      messages.add_message(request, messages.ERROR, 'Referral Code Invalid1')
                      return HttpResponseRedirect('/tradeadmin/Add_Register_User/') 
                    reward_user = User_Management.objects.get(id = user_ref.user_id)
                    if reward_user.plan != 0 :
                        current_plan = plan.objects.get(id = reward_user.plan)
                        if current_plan.referral_status == 1:
                            if user_ref:
                                ref_code = code
                                referral__table(request,tokenkey,code)
                            else:
                              messages.add_message(request, messages.ERROR, 'Referral Code Invalid2')
                              return HttpResponseRedirect('/tradeadmin/Add_Register_User/') 
                except:
                  messages.add_message(request, messages.ERROR, 'Referral Code Invalid')
                  return HttpResponseRedirect('/tradeadmin/Add_Register_User/')
            user_id = get_user.id
            Create_Google_Fitness(request,user_id)
            Create_User_cash_Wallet(request,user_id)
            Pin_Create(request,user_id)
            size=6 
            chars=string.ascii_uppercase + string.digits
            res = ''.join(random.choice(chars) for _ in range(size))
            Referral_code.objects.create(user_id =user_id,referal_code = res)
            marketprice = market_price.objects.get(id = 1)
            wallet = UserCashWallet.objects.get(userid = user_id)
            wallet.balanceone = Decimal(0.1)
            wallet.save()
            totp = pyotp.random_base32()
            h=pyotp.totp.TOTP(totp).provisioning_uri(name=str(email), issuer_name='Jasan Wellness')
            p=pyotp.parse_uri(h)
            table=User_two_fa(user_secrete_key=totp,user_totp=h,user_htotp=p,user= get_user)
            table.save()
            messages.add_message(request, messages.SUCCESS, 'User Create Successfully')
            return HttpResponseRedirect('/tradeadmin/List_User_Management/')

                
        if user_type == "gmail":
            if code == "":
                ref_code = ""
                user = User.objects.create(username = radmon_username)
                step = Steps_Management.objects.get(id = 1)
                free_days = step.free_plan_days
                withdraw = withdraw_values.objects.get(id = 1)
                plan_plan = plan.objects.get(plan_type = 0)
                user_details = User_Management.objects.create(Email = email,User_type = user_type,status = 0,user_name = radmon_username,User_Device_id = device_id,User_Verification_Status = "pinset",referal_code = code,Name = user__name,Health_Withdraw_min_value=withdraw.Health_wallet_minimum_withdraw_limit,Health_Withdraw_max_value = withdraw.Health_wallet_maximum_withdraw_limit,Referral_Withdraw_min_value = withdraw.Referral_wallet_minimum_withdraw_limit,Referral_Withdraw_max_value = withdraw.Referral_wallet_maximum_withdraw_limit,reward_steps = plan_plan.Reward_step_value,reward_step_amount = plan_plan.plan_reward_amount,withdraw_status = plan_plan.withdraw_status,Two_X_Boost_status = 1,user = plan_plan.Min_step_count,over_all_stepcount = plan_plan.Max_step_count,user_phone_number = phone_number,user_info = "Admin")
                date = user_details.created_on + timedelta(free_days)
                user_details.plan_end_date = date
                user_details.save()
                token = Token.objects.create(user = user)
                get_user = User_Management.objects.get(Email = email)
                tokenkey = token.key
                referral__table(request,tokenkey,code)
            else:
                try:
                    user_ref = Referral_code.objects.get(referal_code = code )
                    if user_ref:
                        user = User.objects.create(username = radmon_username)
                        step = Steps_Management.objects.get(id = 1)
                        free_days = step.free_plan_days
                        withdraw = withdraw_values.objects.get(id = 1)
                        plan_plan = plan.objects.get(plan_type = 0)
                        user_details = User_Management.objects.create(Email = email,User_type = user_type,status = 0,user_name = radmon_username,User_Device_id = device_id,User_Verification_Status = "pinset",referal_code = code,Name = user__name,Health_Withdraw_min_value=withdraw.Health_wallet_minimum_withdraw_limit,Health_Withdraw_max_value = withdraw.Health_wallet_maximum_withdraw_limit,Referral_Withdraw_min_value = withdraw.Referral_wallet_minimum_withdraw_limit,Referral_Withdraw_max_value = withdraw.Referral_wallet_maximum_withdraw_limit,reward_steps = plan_plan.Reward_step_value,reward_step_amount = plan_plan.plan_reward_amount,withdraw_status = plan_plan.withdraw_status,Two_X_Boost_status = 1,user = plan_plan.Min_step_count,over_all_stepcount = plan_plan.Max_step_count,user_phone_number = phone_number,user_info = "Admin")
                        date = user_details.created_on + timedelta(free_days)
                        user_details.plan_end_date = date
                        user_details.save()
                        token = Token.objects.create(user = user)
                        get_user = User_Management.objects.get(Email = email)
                        tokenkey = token.key
                        referral__table(request,tokenkey,code)
                    else:
                      messages.add_message(request, messages.ERROR, 'Referral Code Invalid')
                      return HttpResponseRedirect('/tradeadmin/Add_Register_User/')
                    reward_user = User_Management.objects.get(id = user_ref.user_id)
                    if reward_user.plan != 0 :
                        current_plan = plan.objects.get(id = reward_user.plan)
                        if current_plan.referral_status == 1:
                            if user_ref:
                                ref_code = code
                                referral__table(request,tokenkey,code)
                            else:
                              messages.add_message(request, messages.ERROR, 'Referral Code Invalid')
                              return HttpResponseRedirect('/tradeadmin/Add_Register_User/')
                except:
                  messages.add_message(request, messages.ERROR, 'Referral Code Invalid')
                  return HttpResponseRedirect('/tradeadmin/Add_Register_User/')
            get_user = User_Management.objects.get(Email = email)                
            user_id = get_user.id
            Create_Google_Fitness(request,user_id)
            Create_User_cash_Wallet(request,user_id)
            Pin_Create(request,user_id)
            size=6 
            chars=string.ascii_uppercase + string.digits
            res = ''.join(random.choice(chars) for _ in range(size))
            Referral_code.objects.create(user_id =user_id,referal_code = res)
            marketprice = market_price.objects.get(id = 1)
            marketprice.market_price
            wallet = UserCashWallet.objects.get(userid = user_id)
            wallet.balanceone = Decimal(0.1)
            wallet.save()
            totp = pyotp.random_base32()
            h=pyotp.totp.TOTP(totp).provisioning_uri(name=str(email), issuer_name='Jasan Wellness')
            p=pyotp.parse_uri(h)
            table=User_two_fa(user_secrete_key=totp,user_totp=h,user_htotp=p,user= get_user)
            table.save()
            messages.add_message(request, messages.SUCCESS, 'User Create Successfully')
            return HttpResponseRedirect('/tradeadmin/List_User_Management/')
        ref_code=""
        num=""
        try:
            eemail = User_Management.objects.get(Email = email)
        except:
            eemail = ""
        if eemail:
          messages.add_message(request, messages.ERROR, 'User Already Exists')
          return HttpResponseRedirect('/tradeadmin/Add_Register_User/')
        else:
            try:
                id = User_Management.objects.get(User_Device_id = device_id)
                messages.add_message(request, messages.ERROR, 'This Device Already Have A registered User')
                return HttpResponseRedirect('/tradeadmin/Add_Register_User/')
            except:
                pass
            try:
                uuser = User.objects.get(username = user__name)
            except:
                uuser = ""
            if uuser:
              messages.add_message(request, messages.ERROR, 'UserName Exists')
              return HttpResponseRedirect('/tradeadmin/Add_Register_User/')
            else:
              if code:
                  ref_code = code
                  try:
                      user_ref = Referral_code.objects.get(referal_code = code )
                      pass
                  except:
                    messages.add_message(request, messages.ERROR, 'Referral Code Invalid')
                    return HttpResponseRedirect('/tradeadmin/Add_Register_User/')
              if code == "":
                  pass
              otp = generateOTP()
              ref_code = code
              user = User.objects.create(username = radmon_username)
              step = Steps_Management.objects.get(id = 1)
              free_days = step.free_plan_days
              withdraw = withdraw_values.objects.get(id = 1)
              plan_plan = plan.objects.get(plan_type = 0)
              user_details = User_Management.objects.create(user_name = radmon_username,Email = email,referal_code = ref_code,User_type = user_type,status = 0,User_Device_id =device_id,Name = user__name,Health_Withdraw_min_value=withdraw.Health_wallet_minimum_withdraw_limit,Health_Withdraw_max_value = withdraw.Health_wallet_maximum_withdraw_limit,Referral_Withdraw_min_value = withdraw.Referral_wallet_minimum_withdraw_limit,Referral_Withdraw_max_value = withdraw.Referral_wallet_maximum_withdraw_limit,reward_steps = plan_plan.Reward_step_value,reward_step_amount = plan_plan.plan_reward_amount,withdraw_status = plan_plan.withdraw_status,Two_X_Boost_status= 1,user = plan_plan.Min_step_count,over_all_stepcount = plan_plan.Max_step_count,user_phone_number = phone_number,user_info = "Admin")
              date = user_details.created_on + timedelta(free_days)
              user_details.plan_end_date = date
              user_details.save()
              get_user = User_Management.objects.get(Email = email,Name = user__name)
              token = Token.objects.create(user = user)
              tokenkey = token.key
              if code == "":
                  ref_code = ""
              else:
                  reward_user = User_Management.objects.get(id = user_ref.user_id)
                  referral__table(request,tokenkey,code)
                  if reward_user.plan != 0 :
                      current_plan = plan.objects.get(id = reward_user.plan)
                      if current_plan.referral_status == 1:
                          ref_code = code
  
              user_id = get_user.id
              Registrationotp(request,otp,user_id)
              Create_Google_Fitness(request,user_id)
              Create_User_cash_Wallet(request,user_id)
              Pin_Create(request,user_id)
              size=6 
              chars=string.ascii_uppercase + string.digits
              res = ''.join(random.choice(chars) for _ in range(size))
              Referral_code.objects.create(user_id =user_id,referal_code = res)
              marketprice = market_price.objects.get(id = 1)
              marketprice.market_price
              wallet = UserCashWallet.objects.get(userid = user_id)
              wallet.balanceone = Decimal(0.1)
              wallet.save()
              totp = pyotp.random_base32()
              h=pyotp.totp.TOTP(totp).provisioning_uri(name=str(email), issuer_name='Jasan Wellness')
              p=pyotp.parse_uri(h)
              table=User_two_fa(user_secrete_key=totp,user_totp=h,user_htotp=p,user= get_user)
              table.save()
              messages.add_message(request, messages.SUCCESS, 'User Create Successfully')
              return HttpResponseRedirect('/tradeadmin/List_User_Management/')
  return render(request,'trade_admin_auth/register_user_add.html',context)

# Marketprice api function

@check_group("Marketprice")
def MarketPrice_API(request):
  context = {}
  context["Title"] = "Marketprice API"
  context["market"] = market_price.objects.get(id = 1)
  if request.method == "POST":
    market_price_details = request.POST['market_price']
    API = request.POST['API']
    status = request.POST['status']
    market_model = market_price.objects.get(id = 1)
    market_model.market_price = market_price_details
    market_model.API = API
    market_model.status = status
    market_model.save()
    messages.add_message(request, messages.SUCCESS, 'Market Price Updated Successfully.')
  return render(request,'trade_admin_auth/marketprice_api.html',context)



class List_front_page_management(ListView):
    model = front_page_management
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return plan.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(List_front_page_management, self).get_context_data(**kwargs)
        context['Title'] = 'Front Page List'
        adminactivity_qs = front_page_management.objects.all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        Adminactivitytable = List_front_page_management_Table(adminactivity_qs)
        context['table'] = Adminactivitytable
        context['add_title'] ='Add Plan'
        context['Btn_url'] = 'trade_admin_auth:Addplan'
        return context

    @method_decorator(check_group("Front Page Management"))
    def dispatch(self, *args, **kwargs):
      return super(List_front_page_management, self).dispatch(*args, **kwargs)


class Edit_front_page_management(UpdateView):
    model = front_page_management
    form_class = front_page_management_Form
    template_name = 'trade_admin_auth/edit_front_page_management.html'   
    def get_context_data(self, **kwargs):
       context = super(Edit_front_page_management, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       user = front_page_management.objects.get(id = p_key )
       context['Btn_url'] = 'trade_admin_auth:List_front_page_management'
       context['Title'] = 'Edit Front Page Management'
       return context
    
    @method_decorator(check_group("Front Page Management"))
    def dispatch(self, *args, **kwargs):
      return super(Edit_front_page_management, self).dispatch(*args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Front Page updated successfully.')
       return HttpResponseRedirect('/tradeadmin/List_front_page_management/')

@check_group("RPC Management")
def Edit_RPC(request):
  context = {}
  context['Title'] = 'RPC URL Management'
  obj_stake_manage = Contract_address.objects.get(id = 1)
  context['obj_stake_manage'] = obj_stake_manage
  if request.method == "POST":
    rpc_url = request.POST["RPC_URL"]
    if rpc_url != "" :
      Contract_address.objects.filter(id = 1).update(Stake_contract_Address = rpc_url)
      url = "https://apinode.jasanwellness.fit/fetchRPC"
      data = {
              "url" : rpc_url
              }
      headers = {"Content-Type": "application/json"}
      response = requests.post(url, json=data, headers=headers)
      data = response.json()
      messages.add_message(request, messages.SUCCESS, 'Successfully updated.')
      return HttpResponseRedirect('/tradeadmin/Edit_RPC/1/')
    else:
      messages.add_message(request, messages.ERROR, 'Enter required field.')
      return HttpResponseRedirect('/tradeadmin/Edit_RPC/1/')
  return render(request,'trade_admin_auth/edit_rpc.html',context)




class User_Wallet_Address_Detail(TemplateView):
  template_name = "trade_admin_auth/user_wallet_address_detail.html"

  def get_context_data(self, **kwargs):
    context = super(User_Wallet_Address_Detail, self).get_context_data(**kwargs)
    p_key = self.kwargs['pk']
    context["p_key"] = p_key
    obj_user = User_Management.objects.get(id = p_key)
    try:
      staticcontent_qs = user_address_trust_wallet.objects.get(user_id = obj_user.id)
    except:
      staticcontent_qs = "None"
    
    
    context['staticcontent_qs'] = staticcontent_qs
    context['Title'] = 'User Wallet Address Details'
    context['id'] = obj_user.id

    return context

  
  @method_decorator(check_group_icon_menu("Wallet address"))
  def dispatch(self, *args, **kwargs):
    return super(User_Wallet_Address_Detail, self).dispatch(*args, **kwargs)


def wallet_edit_address(request,id):
    if request.method =="POST":
      wall_address=json.loads(request.body.decode('UTF-8'))
      if wall_address:
        user_objs=User_Management.objects.get(id=id)
        try:
          wallet = user_address_trust_wallet.objects.get(user_id = id)
        except:
          wallet = "None"
        try:
          obj_wall_address = user_address_trust_wallet.objects.get(Address = wall_address)
        except:
           obj_wall_address = 0
        wallet_objs = user_address_trust_wallet.objects.filter(Address = wall_address ).count()
        if wallet != "None":
          if int(wallet_objs) == 0:
            wallet.Address=wall_address
            wallet.save()
            messages.add_message(request, messages.SUCCESS, 'Wallet updated successful. Kindly inform the user to reinstall the application.')
            return HttpResponse('success')
          else:
            obj_user_email =obj_wall_address.user.Email
            messages.add_message(request, messages.ERROR, 'Address already applied to this '+str(obj_user_email))    
            return HttpResponse('error')

        else:
          try:
            wallet_address = user_address_trust_wallet.objects.get(Address = wall_address )
          except:
            wallet_address= "None"
          if wallet_address == "None":
            user_address_trust_wallet.objects.create(user_id=user_objs.id,Address=wall_address,wallet_type="Admin Update")   
            messages.add_message(request, messages.SUCCESS, 'Wallet created successful. Kindly inform the user to reinstall the application.')
            return HttpResponse('success')
          else:
            obj_user_email =obj_wall_address.user.Email
            messages.add_message(request, messages.ERROR, 'Address already applied to this '+str(obj_user_email))
            return HttpResponse('error')
      else:
        messages.add_message(request, messages.ERROR, 'Field required.')
        return HttpResponse('success')


    return HttpResponseRedirect('/tradeadmin/User_Wallet_Address_Detail/'+str(id)+'/')



class Delete_Request(View):
    def get(self, request, *args, **kwargs):
        pkey =  (self.kwargs['pk'])
        user_qs = get_object_or_404(Delete_Account_Management, pk=pkey)
        try:
            get_user_id = Delete_Account_Management.objects.get(id=pkey)
            user_qs.delete()
        except:
            user_qs.delete()
        messages.add_message(request, messages.SUCCESS, 'deleted successfully.') 
        return HttpResponseRedirect('/tradeadmin/List_Delete_Account_Request/')
    

class Delete_inactive(View):
    def get(self, request, *args, **kwargs):
        pkey =  (self.kwargs['pk'])
        user_qs = get_object_or_404(Delete_Account_Management, pk=pkey)
        get_user_id = Delete_Account_Management.objects.get(id=pkey)
        get_user_id.status = 0
        get_user_id.save()
        messages.add_message(request, messages.SUCCESS, 'Updated successfully.') 
        return HttpResponseRedirect('/tradeadmin/List_Delete_Account_Request/')

@check_group_sub_menu("Wallet Address List")
def Wallet_Address_Users_List(request):
  context = {}
  context["Title"] = "Wallet Address List"

  try:
    wallet_address = request.GET['Address']
  except:
    wallet_address = ""
  try:
    email = request.GET['email']
  except:
    email = ""
  usr = 0
  count = 0
  dict_address = {}
  start_page = request.GET.get('pageno', 1)
  end_value = int(start_page) * 10
  start_value = int(end_value) - 9
  if wallet_address:
    obj_wallet_address = user_address_trust_wallet.objects.filter(Address = wallet_address).order_by('-created_on')
    for i in obj_wallet_address:
      usr = usr + 1
      list_usr = {}
      if start_value <= usr <= end_value:
        count = count + 1
        list_usr["email"] = str(i.user.Email)
        list_usr["address"] = (i.Address)
        list_usr["wallet_type"] = i.wallet_type
        list_usr["date"] = str(i.created_on)
        list_usr["id"] = str(i.id)
        list_usr["pageno"] = start_page
        list_usr["sno"] = usr
        dict_address[count] = list_usr
  elif email:
    obj_wallet_address = user_address_trust_wallet.objects.filter(user__Email__icontains = email).order_by('-created_on')
    for i in obj_wallet_address:
      usr = usr + 1
      list_usr = {}
      if start_value <= usr <= end_value:
        count = count + 1
        list_usr["email"] = str(i.user.Email)
        list_usr["address"] = (i.Address)
        list_usr["wallet_type"] = i.wallet_type
        list_usr["date"] = str(i.created_on)
        list_usr["id"] = str(i.id)
        list_usr["pageno"] = start_page
        list_usr["sno"] = usr
        dict_address[count] = list_usr
  else:
    obj_wallet_address = user_address_trust_wallet.objects.all().order_by('-created_on')
    for i in obj_wallet_address:
      usr = usr + 1
      list_usr = {}
      if start_value <= usr <= end_value:
        count = count + 1
        list_usr["email"] = str(i.user.Email)
        list_usr["address"] = (i.Address)
        list_usr["wallet_type"] = i.wallet_type
        list_usr["date"] = str(i.created_on)
        list_usr["id"] = str(i.id)
        list_usr["pageno"] = start_page
        list_usr["sno"] = usr
        dict_address[count] = list_usr
  try:
    tot_user_qs = obj_wallet_address
  except:
    tot_user_qs = ""
  w_page = request.GET.get('pageno', 1)
  w_paginator = Paginator(tot_user_qs, 10)
  try:
      wallet_qs = w_paginator.page(w_page)
  except PageNotAnInteger:
      wallet_qs =w_paginator.page(1)
  except EmptyPage:
      wallet_qs = w_paginator.page(w_paginator.num_pages)

  context["endpage"] = wallet_qs.number+1
  context["startpage"] = wallet_qs.number-1
  context['start_value'] = wallet_qs.start_index()
  context['end_value'] = wallet_qs.end_index()
  context['usr_count'] = obj_wallet_address.count()
  context['wallet_qs'] = wallet_qs
  context['dict_address'] = json.dumps(dict_address) 
  context['Btn_url'] = 'trade_admin_auth:wallet_address_users_listing'
  
  return render(request, 'trade_admin_auth/wallet_address_users_list.html',context)


@check_group_sub_menu("Wallet Address List")
def delete_wallet_address(request, id):
    wallet = get_object_or_404(user_address_trust_wallet, id=id)
    wallet.delete()
    messages.success(request, "Wallet address deleted successfully.")
    return redirect('trade_admin_auth:wallet_address_users_listing')


from django.utils import timezone
class UplineReferalHistoryTable(TemplateView):
  template_name = "trade_admin_auth/upline_refferal_table.html"

  def get_context_data(self, **kwargs):
    context = super(UplineReferalHistoryTable, self).get_context_data(**kwargs)
    p_key = self.kwargs['pk']
    user_obj = User_Management.objects.get(id = p_key) 

    obj_username = User_Management.objects.raw('SELECT T2.id, T2.Name,T2.Email,T2.referal_code,T1.lvl - 1 as user, T2.plan_start_date , T2.plan_end_date , ( CASE WHEN T2.plan = 0 THEN "FREE" ELSE ( SELECT plan_name FROM pUDmgt5FK2 WHERE id = T2.plan ) END ) as user_name FROM ( SELECT @r AS _id,(SELECT @r := reff_id FROM USPzTPzfNdmGTlER WHERE id = _id) AS referal_code, @l := @l + 1 AS lvl FROM (SELECT @r := %s, @l := 0) vars, USPzTPzfNdmGTlER m WHERE @r <> 0) T1 JOIN USPzTPzfNdmGTlER T2 ON T1._id = T2.id ', [p_key])
    serializer = user_ref_upline(obj_username,many=True)  


    ref_usr = 0
    ref_count = 0
    ref_start_page = self.request.GET.get('pageno', 1)
    ref_end_value = int(ref_start_page) * 5
    ref_start_value = int(ref_end_value) - 4
    ref_dict_uplineusers={}
    user_plam = plan_purchase_history.objects.filter(user=p_key).last()
    level_com=plan_purchase_history.objects.filter(user=p_key).count()
    # Use the created_on date from user_plam if it exists, otherwise use today's date
    created_on_date = user_plam.created_on.date() if user_plam else timezone.now().date()

    user_ref = Referral_reward_History.objects.filter(referral_id=user_obj.Name, created_on__date=created_on_date)
    # user_ref = Referral_reward_History.objects.filter(referral_id = user_obj.Name,created_on__date=user_plam.created_on.date())
    for i in user_ref:
      ref_usr = ref_usr + 1
      ref_list_usr={}
      ref_count = ref_count + 1
      ref_list_usr["username"]= i.user.Name
      ref_list_usr["Reward"]=i.reward
      ref_list_usr["marekt_api"]=i.user.fixed_status
      ref_list_usr["level"]="First Commission"
      ref_list_usr["created_on"]=(str(i.created_on))
      ref_list_usr["sno"] = ref_usr
      ref_list_usr["id"] = i.id
      ref_dict_uplineusers[ref_count] = ref_list_usr
    try:
      tot_ref_user_qs = user_ref
    except:
      tot_ref_user_qs = ""
    w_page = self.request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_ref_user_qs, 5)
    
    try:
        ref_hist_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        ref_hist_qs =w_paginator.page(1)
    except EmptyPage:
        ref_hist_qs = w_paginator.page(w_paginator.num_pages)

    context['ref_hist_qs'] = ref_hist_qs
    context["ref_endpage"] = ref_hist_qs.number+1
    context["ref_startpage"] = ref_hist_qs.number-1
    context['ref_start_value'] = ref_hist_qs.start_index()
    context['ref_end_value'] = ref_hist_qs.end_index()
    context['ref_usr_count'] = user_ref.count()
    context['ref_dict_uplineusers']=json.dumps(ref_dict_uplineusers)
    context['upline_referral']=serializer.data
    context['user_name'] = (user_obj.Name).upper()
    context['Title'] = 'Upline Referral Table'
    context["Btn_url"] = "trade_admin_auth: Upline_Referral_History"
    return context
  
  
  
from django.utils import timezone
class mpUplineReferalHistoryTable(TemplateView):
  template_name = "trade_admin_auth/mpupline_refferal_table.html"

  def get_context_data(self, **kwargs):
    context = super(mpUplineReferalHistoryTable, self).get_context_data(**kwargs)
    p_key = self.kwargs['pk']
    user_obj = User_Management.objects.get(id = p_key) 

    obj_username = User_Management.objects.raw('SELECT T2.id, T2.Name,T2.Email,T2.referal_code,T1.lvl - 1 as user, T2.plan_start_date , T2.plan_end_date , ( CASE WHEN T2.plan = 0 THEN "FREE" ELSE ( SELECT plan_name FROM pUDmgt5FK2 WHERE id = T2.plan ) END ) as user_name FROM ( SELECT @r AS _id,(SELECT @r := reff_id FROM USPzTPzfNdmGTlER WHERE id = _id) AS referal_code, @l := @l + 1 AS lvl FROM (SELECT @r := %s, @l := 0) vars, USPzTPzfNdmGTlER m WHERE @r <> 0) T1 JOIN USPzTPzfNdmGTlER T2 ON T1._id = T2.id ', [p_key])
    serializer = user_ref_upline(obj_username,many=True)  


    ref_usr = 0
    ref_count = 0
    ref_start_page = self.request.GET.get('pageno', 1)
    ref_end_value = int(ref_start_page) * 5
    ref_start_value = int(ref_end_value) - 4
    ref_dict_uplineusers={}
    user_plam = MPPLanHistory.objects.filter(email_id=user_obj.id).last()
    level_com=MPPLanHistory.objects.filter(email_id=user_obj.id).count()
    created_on_date = user_plam.created_on.date() if user_plam else timezone.now().date()
    user_ref = MPRewardHistory.objects.filter(referral_id="MP " + user_obj.Name, created_on__date=created_on_date)
    for i in user_ref:
      ref_usr = ref_usr + 1
      ref_list_usr={}
      ref_count = ref_count + 1
      ref_list_usr["username"]= i.user.Name
      ref_list_usr["Reward"]=i.reward
      ref_list_usr["marekt_api"]=i.user.fixed_status
      ref_list_usr["level"]="First Commission"
      ref_list_usr["created_on"]=(str(i.created_on))
      ref_list_usr["sno"] = ref_usr
      ref_list_usr["id"] = i.id
      ref_dict_uplineusers[ref_count] = ref_list_usr
    try:
      tot_ref_user_qs = user_ref
    except:
      tot_ref_user_qs = ""
    w_page = self.request.GET.get('pageno', 1)
    w_paginator = Paginator(user_ref.order_by('-created_on'), 5)

    
    try:
        ref_hist_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        ref_hist_qs =w_paginator.page(1)
    except EmptyPage:
        ref_hist_qs = w_paginator.page(w_paginator.num_pages)

    context['ref_hist_qs'] = ref_hist_qs
    context["ref_endpage"] = ref_hist_qs.number+1
    context["ref_startpage"] = ref_hist_qs.number-1
    context['ref_start_value'] = ref_hist_qs.start_index()
    context['ref_end_value'] = ref_hist_qs.end_index()
    context['ref_usr_count'] = user_ref.count()
    context['ref_dict_uplineusers']=json.dumps(ref_dict_uplineusers)
    context['upline_referral']=serializer.data
    context['user_name'] = (user_obj.Name).upper()
    context['Title'] = 'mpUpline Referral Table'
    context["Btn_url"] = "trade_admin_auth: mpUpline_Referral_History"
    return context



  
  
from django.utils import timezone
class burnUplineReferalHistoryTable(TemplateView):
  template_name = "trade_admin_auth/burnupline_refferal_table.html"

  def get_context_data(self, **kwargs):
    context = super(burnUplineReferalHistoryTable, self).get_context_data(**kwargs)
    p_key = self.kwargs['pk']
    user_obj = User_Management.objects.get(id = p_key) 

    obj_username = User_Management.objects.raw('SELECT T2.id, T2.Name,T2.Email,T2.referal_code,T1.lvl - 1 as user, T2.plan_start_date , T2.plan_end_date , ( CASE WHEN T2.plan = 0 THEN "FREE" ELSE ( SELECT plan_name FROM pUDmgt5FK2 WHERE id = T2.plan ) END ) as user_name FROM ( SELECT @r AS _id,(SELECT @r := reff_id FROM USPzTPzfNdmGTlER WHERE id = _id) AS referal_code, @l := @l + 1 AS lvl FROM (SELECT @r := %s, @l := 0) vars, USPzTPzfNdmGTlER m WHERE @r <> 0) T1 JOIN USPzTPzfNdmGTlER T2 ON T1._id = T2.id ', [p_key])
    serializer = user_ref_upline(obj_username,many=True)  


    ref_usr = 0
    ref_count = 0
    ref_start_page = self.request.GET.get('pageno', 1)
    ref_end_value = int(ref_start_page) * 5
    ref_start_value = int(ref_end_value) - 4
    ref_dict_uplineusers={}
    user_plam = BurntoearnHistory.objects.filter(email_id=user_obj.id).last()
    level_com=BurntoearnHistory.objects.filter(email_id=user_obj.id).count()
    created_on_date = user_plam.created_on.date() if user_plam else timezone.now().date()
    user_ref = BurnRewardHistory.objects.filter(referral_id="BURN " + user_obj.Name, created_on__date=created_on_date)
    for i in user_ref:
      ref_usr = ref_usr + 1
      ref_list_usr={}
      ref_count = ref_count + 1
      ref_list_usr["username"]= i.user.Name
      ref_list_usr["Reward"]=i.reward
      ref_list_usr["marekt_api"]=i.user.fixed_status
      ref_list_usr["level"]="First Commission"
      ref_list_usr["created_on"]=(str(i.created_on))
      ref_list_usr["sno"] = ref_usr
      ref_list_usr["id"] = i.id
      ref_dict_uplineusers[ref_count] = ref_list_usr
    try:
      tot_ref_user_qs = user_ref
    except:
      tot_ref_user_qs = ""
    w_page = self.request.GET.get('pageno', 1)
    w_paginator = Paginator(user_ref.order_by('-created_on'), 5)

    
    try:
        ref_hist_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        ref_hist_qs =w_paginator.page(1)
    except EmptyPage:
        ref_hist_qs = w_paginator.page(w_paginator.num_pages)

    context['ref_hist_qs'] = ref_hist_qs
    context["ref_endpage"] = ref_hist_qs.number+1
    context["ref_startpage"] = ref_hist_qs.number-1
    context['ref_start_value'] = ref_hist_qs.start_index()
    context['ref_end_value'] = ref_hist_qs.end_index()
    context['ref_usr_count'] = user_ref.count()
    context['ref_dict_uplineusers']=json.dumps(ref_dict_uplineusers)
    context['upline_referral']=serializer.data
    context['user_name'] = (user_obj.Name).upper()
    context['Title'] = 'BurnUpline Referral Table'
    context["Btn_url"] = "trade_admin_auth: burnUpline_Referral_History"
    return context

def transcation_hash_List(request):
  context = {}
  context["Title"] = "Transcation Hash List"

  try:
    hash_user = request.GET['hash']
  except:
    hash_user = ""
  try:
    type_status = request.GET['read_status']
  except:
    type_status = ""
  if type_status == "0":  
    usr = 0
    count = 0
    dict_address = {}
    start_page = request.GET.get('pageno', 1)
    end_value = int(start_page) * 10
    start_value = int(end_value) - 9
    if hash_user:
      obj_hash_user = plan_purchase_history.objects.filter(User_plan_validation = hash_user)
      for i in obj_hash_user:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["email"] = str(i.user.Email)
          list_usr["hash"] = (i.User_plan_validation)
          list_usr["wallettype"] = i.user_wallet_type
          list_usr["date"] = str(i.created_on)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_address[count] = list_usr
    try:
      tot_user_qs = obj_hash_user
    except:
      tot_user_qs = ""
    w_page = request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_user_qs, 10)
    try:
        wallet_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        wallet_qs =w_paginator.page(1)
    except EmptyPage:
        wallet_qs = w_paginator.page(w_paginator.num_pages)

    context["endpage"] = wallet_qs.number+1
    context["startpage"] = wallet_qs.number-1
    context['start_value'] = wallet_qs.start_index()
    context['end_value'] = wallet_qs.end_index()
    context['usr_count'] = obj_hash_user.count()
    context['wallet_qs'] = wallet_qs
    context['dict_address'] = json.dumps(dict_address) 
    context['Btn_url'] = 'trade_admin_auth:hash_users_listing'
  elif type_status == "1" :
    usr = 0
    count = 0
    dict_address = {}
    start_page = request.GET.get('pageno', 1)
    end_value = int(start_page) * 10
    start_value = int(end_value) - 9
    if hash_user:
      obj_hash_user = Withdraw_history.objects.filter(Transaction_Hash = hash_user)
      for i in obj_hash_user:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["email"] = str(i.user_id.Email)
          list_usr["hash"] = (i.Transaction_Hash)
          list_usr["wallettype"] = i.Wallet_type
          list_usr["date"] = str(i.created_on)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_address[count] = list_usr

    try:
      tot_user_qs = obj_hash_user
    except:
      tot_user_qs = ""
    w_page = request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_user_qs, 10)
    try:
        wallet_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        wallet_qs =w_paginator.page(1)
    except EmptyPage:
        wallet_qs = w_paginator.page(w_paginator.num_pages)

    context["endpage"] = wallet_qs.number+1
    context["startpage"] = wallet_qs.number-1
    context['start_value'] = wallet_qs.start_index()
    context['end_value'] = wallet_qs.end_index()
    context['usr_count'] = obj_hash_user.count()
    context['wallet_qs'] = wallet_qs
    context['dict_address'] = json.dumps(dict_address) 
    context['Btn_url'] = 'trade_admin_auth:hash_users_listing'
  elif type_status == "2" :
    usr = 0
    count = 0
    dict_address = {}
    start_page = request.GET.get('pageno', 1)
    end_value = int(start_page) * 10
    start_value = int(end_value) - 9
    if hash_user:
      obj_hash_user = stake_deposit_management.objects.using('second_db').filter(Hash = hash_user)
      for i in obj_hash_user:
        usr = usr + 1
        list_usr = {}
        if start_value <= usr <= end_value:
          count = count + 1
          list_usr["email"] = str(i.email)
          list_usr["hash"] = (i.Hash)
          list_usr["wallettype"] = 'Trust Wallet'
          list_usr["date"] = str(i.created_on)
          list_usr["pageno"] = start_page
          list_usr["sno"] = usr
          dict_address[count] = list_usr

    try:
      tot_user_qs = obj_hash_user
    except:
      tot_user_qs = ""
    w_page = request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_user_qs, 10)
    try:
        wallet_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        wallet_qs =w_paginator.page(1)
    except EmptyPage:
        wallet_qs = w_paginator.page(w_paginator.num_pages)

    context["endpage"] = wallet_qs.number+1
    context["startpage"] = wallet_qs.number-1
    context['start_value'] = wallet_qs.start_index()
    context['end_value'] = wallet_qs.end_index()
    context['usr_count'] = obj_hash_user.count()
    context['wallet_qs'] = wallet_qs
    context['dict_address'] = json.dumps(dict_address) 
    context['Btn_url'] = 'trade_admin_auth:hash_users_listing'
  return render(request, 'trade_admin_auth/hash_user_list.html',context)


def wallet_address_block(request):
  context = {}
  context["Title"] = "Wallet Address Block"
  if request.method == "POST":
    try:
      address = request.POST['address']
    except:
      address = ""
    if address:
      wallet_add = user_address_trust_wallet.objects.get(Address = address)
      wallet_objs = user_address_trust_wallet.objects.filter(Address = address).count()
      if int(wallet_objs) == 0:
            messages.add_message(request, messages.ERROR, 'Address doesn`t exist For Anyusers.')
      else:
        wallet_add.wallet_type="admin blocked"
        wallet_add.modified_on=datetime.datetime.now()
        wallet_add.save()
        messages.add_message(request, messages.SUCCESS, 'Address Block successfully.')  
    else:
      messages.add_message(request, messages.ERROR, 'Address Field Required.')
  return render(request,'trade_admin_auth/wallet_address_block.html',context)



def unblock_address(request,id):
  wallet_add = user_address_trust_wallet.objects.get(user_id = id)
  wallet_add.wallet_type="import"
  wallet_add.modified_on=datetime.datetime.now()
  wallet_add.save()
  messages.add_message(request, messages.SUCCESS, 'Address UnBlock successfully.')  
  return HttpResponseRedirect("/tradeadmin/wallet_address_block_list/")






   
def wallet_address_block_list(request):
  context = {}
  context["Title"] = "Block History List"
  try:
    address = request.GET['Address']
  except:
    address = ""
  usr = 0
  count = 0
  dict_address = {}
  start_page = request.GET.get('pageno', 1)
  end_value = int(start_page) * 10
  start_value = int(end_value) - 9
  if address:
    obj_address_user = user_address_trust_wallet.objects.filter(Q(Address = address) & Q(wallet_type = "admin blocked"))
    for i in obj_address_user:
      usr = usr + 1
      list_usr = {}
      if start_value <= usr <= end_value:
        count = count + 1
        list_usr["id"] = str(i.user.id)
        list_usr["email"] = str(i.user.Email)
        list_usr["address"] = (i.Address)
        list_usr["wallettype"] = i.wallet_type
        list_usr["date"] = str(i.modified_on)
        list_usr["pageno"] = start_page
        list_usr["sno"] = usr
        dict_address[count] = list_usr
  else:
    obj_address_user = user_address_trust_wallet.objects.filter(wallet_type = "admin blocked")
    for i in obj_address_user:
      usr = usr + 1
      list_usr = {}
      if start_value <= usr <= end_value:
        count = count + 1
        list_usr["id"] = str(i.user.id)
        list_usr["email"] = str(i.user.Email)
        list_usr["address"] = (i.Address)
        list_usr["wallettype"] = i.wallet_type
        list_usr["date"] = str(i.modified_on)
        list_usr["pageno"] = start_page
        list_usr["sno"] = usr
        dict_address[count] = list_usr
  try:
    tot_user_qs = obj_address_user
  except:
    tot_user_qs = ""
  w_page = request.GET.get('pageno', 1)
  w_paginator = Paginator(tot_user_qs, 10)
  try:
      wallet_qs = w_paginator.page(w_page)
  except PageNotAnInteger:
      wallet_qs =w_paginator.page(1)
  except EmptyPage:
      wallet_qs = w_paginator.page(w_paginator.num_pages)

  context["endpage"] = wallet_qs.number+1
  context["startpage"] = wallet_qs.number-1
  context['start_value'] = wallet_qs.start_index()
  context['end_value'] = wallet_qs.end_index()
  context['usr_count'] = obj_address_user.count()
  context['wallet_qs'] = wallet_qs
  context['dict_address'] = json.dumps(dict_address) 
  context['Btn_url'] = 'trade_admin_auth:wallet_address_block_list'
  return render(request, 'trade_admin_auth/wallet_address_block_list.html',context)


def getwithdrawUsers(request):

  start = int(request.POST['start'])
  draw = int(request.POST['draw'])
  length = int(request.POST['length'])
  id_Address = (request.POST['id_Address'])
  email = (request.POST['id_email'])
  date = (request.POST['id_date'])
  status = (request.POST['id_status'])
 

  if id_Address !='' or date != "" or email !="" or status !=""  :
    if id_Address and date and email  :
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as Wallet_type , U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.Amount LIKE %s ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%","%" + date + "%","%" + email + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address  LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.status LIKE %s', ["%" + id_Address +"%","%" + date + "%","%" + email + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif id_Address and date  :
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as Wallet_type , U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%","%" + date + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address  LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s', ["%" + id_Address +"%","%" + date + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif id_Address:
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as Wallet_type , U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s', ["%" + id_Address + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif (date):
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as Wallet_type , U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s ORDER BY U.id DESC LIMIT %s , %s', ["%" + date + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s', ["%" + date + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif email:
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as Wallet_type , U2.Email as Month_stake , U.status ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U2.Email LIKE %s ORDER BY U.id DESC LIMIT %s , %s', ["%" + email + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U2.Email LIKE %s', ["%" + email + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif status:
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as Wallet_type , U2.Email as Month_stake , U.status ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.status LIKE %s ORDER BY U.id DESC LIMIT %s , %s', ["%" + status + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.status LIKE %s', ["%" + status + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
  else:
    obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as Wallet_type , U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%", start,length])
    serializer = User_withdraw_see(obj_username,many=True)
    for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U'):
      totalRecords = total_count.counts
      set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
      tt = (list(set_object))
      tt.sort(reverse=False)
       
  return JsonResponse({'data':serializer.data,"draw": draw,"recordsTotal": totalRecords,"recordsFiltered": totalRecords,"tt":tt})



def bgetwithdrawUsers(request):

  start = int(request.POST['start'])
  draw = int(request.POST['draw'])
  length = int(request.POST['length'])
  id_Address = (request.POST['id_Address'])
  email = (request.POST['id_email'])
  date = (request.POST['id_date'])
  status = (request.POST['id_status'])
 

  if id_Address !='' or date != "" or email !="" or status !=""  :
    if id_Address and date and email  :
      obj_username = burnwithdraw.objects.raw('SELECT U.id, U2.Name as Wallet_type , U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.Amount LIKE %s ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%","%" + date + "%","%" + email + "%", start,length])
      serializer = User_BurnWithdraw_see(obj_username,many=True)
      for total_count in burnwithdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address  LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.status LIKE %s', ["%" + id_Address +"%","%" + date + "%","%" + email + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif id_Address and date  :
      obj_username = burnwithdraw.objects.raw('SELECT U.id, U2.Name as Wallet_type , U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%","%" + date + "%", start,length])
      serializer = User_BurnWithdraw_see(obj_username,many=True)
      for total_count in burnwithdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address  LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s', ["%" + id_Address +"%","%" + date + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif id_Address:
      obj_username = burnwithdraw.objects.raw('SELECT U.id, U2.Name as Wallet_type , U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%", start,length])
      serializer = User_BurnWithdraw_see(obj_username,many=True)
      for total_count in burnwithdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s', ["%" + id_Address + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif (date):
      obj_username = burnwithdraw.objects.raw('SELECT U.id, U2.Name as Wallet_type , U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s ORDER BY U.id DESC LIMIT %s , %s', ["%" + date + "%", start,length])
      serializer = User_BurnWithdraw_see(obj_username,many=True)
      for total_count in burnwithdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s', ["%" + date + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif email:
      obj_username = burnwithdraw.objects.raw('SELECT U.id, U2.Name as Wallet_type , U2.Email as Month_stake , U.status ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U2.Email LIKE %s ORDER BY U.id DESC LIMIT %s , %s', ["%" + email + "%", start,length])
      serializer = User_BurnWithdraw_see(obj_username,many=True)
      for total_count in burnwithdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U2.Email LIKE %s', ["%" + email + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif status:
      obj_username = burnwithdraw.objects.raw('SELECT U.id, U2.Name as Wallet_type , U2.Email as Month_stake , U.status ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.status LIKE %s ORDER BY U.id DESC LIMIT %s , %s', ["%" + status + "%", start,length])
      serializer = User_BurnWithdraw_see(obj_username,many=True)
      for total_count in burnwithdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.status LIKE %s', ["%" + status + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
  else:
    obj_username = burnwithdraw.objects.raw('SELECT U.id, U2.Name as Wallet_type , U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%", start,length])
    serializer = User_BurnWithdraw_see(obj_username,many=True)
    for total_count in burnwithdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM burnwithdraw as U'):
      totalRecords = total_count.counts
      set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
      tt = (list(set_object))
      tt.sort(reverse=False)
       
  return JsonResponse({'data':serializer.data,"draw": draw,"recordsTotal": totalRecords,"recordsFiltered": totalRecords,"tt":tt})

def device_unique(request):
  context={}
  if request.method == "POST":
    device=request.POST['device']
    if device:
      user_details=User_Management.objects.filter(device_unique_id=device)
      for i in user_details:
        if i.status != 2: 
          i.status = 2
          i.save()
        else:
          i.status = 0
          i.save()
      messages.add_message(request, messages.SUCCESS, 'Successfully Updated!!!!!')
    else:
      messages.add_message(request, messages.ERROR,'Device ID Required')
  context["Title"] = "Device Unique Id"
  return render(request,"trade_admin_auth/device_unique_id.html",context)
  

def user_device_id(request):
  start = int(request.POST['start'])
  draw = int(request.POST['draw'])
  length = int(request.POST['length'])

  obj_username = User_Management.objects.raw('SELECT id, Email , Name , user_phone_number ,status, device_unique_id ,COUNT(*) as user_profile_pic FROM `USPzTPzfNdmGTlER` GROUP by device_unique_id HAVING user_profile_pic >= 2 ORDER BY user_profile_pic DESC LIMIT %s , %s',[start,length])
  serializer = User_device_see(obj_username,many=True)
  for total_count in User_Management.objects.raw(' SELECT id,COUNT(*) as counts FROM (SELECT id ,COUNT(*) as user_profile_pic FROM USPzTPzfNdmGTlER GROUP by device_unique_id HAVING user_profile_pic >= 2 ) AS DerivedTableAlias '):
    serializer = User_device_see(obj_username,many=True)
    totalRecords =total_count.counts
    set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
    tt = (list(set_object))
    tt.sort(reverse=False)
       
  return JsonResponse({'data':serializer.data,"draw": draw,"recordsTotal": totalRecords,"recordsFiltered": totalRecords,"tt":tt})


def device_empty_unique(request):
  context={}
  context["Title"] = "Empty Device Id"
  return render(request,"trade_admin_auth/device_empty_unique_id.html",context)

def user_empty_device_id(request):
  start = int(request.POST['start'])
  draw = int(request.POST['draw'])
  length = int(request.POST['length'])
  obj_username = User_Management.objects.raw("SELECT id, Email, Name, user_phone_number, device_unique_id ""FROM `USPzTPzfNdmGTlER` ""WHERE device_unique_id = '' LIMIT %s , %s",[start,length])
  for total_count in User_Management.objects.raw("SELECT U.id ,COUNT(*) as counts FROM USPzTPzfNdmGTlER as U"):
    serializer = User_device_see(obj_username,many=True)
    totalRecords =total_count.counts
    set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
    tt = (list(set_object))
    tt.sort(reverse=False)
       
  return JsonResponse({'data':serializer.data,"draw": draw,"recordsTotal": totalRecords,"recordsFiltered": totalRecords,"tt":tt})

def Edit_User_Plan(request,id):
  context = {}
  try:
    obj_user = User_Management.objects.get(id = id)
  except:
    obj_user = ""
  obj_plan = plan.objects.filter(plan_type = 1)
  try:
      companyqs = Company.objects.get(id=1)
      companyname= companyqs.name
  except:
      companyqs = ''
      companyname = ''
  Market_Price = market_price.objects.get(id = 1)
  if request.method == "POST":
    plan_name = request.POST["plan_name"]
    plan_period = request.POST["plan_duration"]
    price = request.POST["price"]
    plan_hist_mann=plan_purchase_history.objects.filter(user_id=obj_user.id).last()
    plan_days=''
    if plan_name:
      if plan_period:  
        if plan_hist_mann:
          plan_hist_man=plan_purchase_history.objects.values('plan_id','user_id','User_plan_validation','user_wallet_type','created_on','Plan_maximum_reward','plan_purchase_type').filter(user_id=obj_user.id).last()
          date_del=plan_hist_man['created_on']
          plan_id_id = plan.objects.get(id =plan_hist_man['plan_id'])
          user_ref = Referral_reward_History.objects.filter(referral_id = obj_user.Name,created_on__date__gte=date_del.date())
          plan_id = plan.objects.get(plan_name = plan_name)
          plan_purchase=int(plan_id.plan_purchase_type)
          if plan_period == "Monthly":
            plan_duration = 0
            plan_days = 30
            plan_amount = plan_id.plan_purchase_amount_monthly
          if plan_period == "Quarterly":
            plan_duration = 1
            plan_days = 90
            plan_amount = plan_id.plan_purchase_amount_quarterly
          if plan_period == "Annual":
            plan_duration = 2
            plan_days = 365
            plan_amount = plan_id.plan_purchase_amount_annual
          
          plan_edit=plan_purchase_history_edited.objects.create(user=obj_user,old_plan=plan_id_id.plan_name,new_plan=plan_name,user_wallet_type=plan_hist_man['user_wallet_type'],buy_type="Admin Edit plan",trans_hash=plan_hist_man['User_plan_validation'],created_on=plan_hist_man['created_on'],modified_on=datetime.datetime.now(),plan_start_date=obj_user.plan_start_date,plan_end_date=obj_user.plan_end_date,old_plan_type=plan_purchase,new_plan_type=plan_hist_man['plan_purchase_type'])
          new_type=int(plan_edit.new_plan_type)
          wallet = UserCashWallet.objects.get(userid = obj_user)
          wallet_flush_history.objects.create(user = obj_user,wallet_balanceone = wallet.balanceone,Wallet_referral_income = wallet.referalincome,User_before_plan = obj_user.plan)
          wallet.balanceone = 0
          wallet.referalincome = 0
          wallet.save()
          if new_type == 1:
            try:
              stake_his=stake_claim_reward_history.objects.using('second_db').filter(user = obj_user.id,type="Plan Purchase").last()
              stake_his.delete()
            except:
              stake_his=0
          if plan_edit.old_plan_type == 1:
            try:
                user_stake_obj = stake_wallet_management.objects.using('second_db').get(user = obj_user.id)
            except:
                user_stake_obj = 0
            if user_stake_obj != 0:
                try:
                  stake_his=stake_claim_reward_history.objects.using('second_db').filter(user = obj_user.id,type="Plan Purchase").last()
                  stake_his.delete()
                except:
                  stake_his=0
                amunt=plan_id.activate_plan
                value=Decimal(plan_amount) - Decimal(amunt)
                user_stake_obj.stake_Wallet=Decimal(user_stake_obj.stake_Wallet)  + Decimal(value)
                user_stake_obj.save(using='second_db')
                stake_claim_reward_history.objects.using('second_db').create(user = obj_user.id,email=obj_user.Email,type='Plan Purchase',stake_Wallet_reward_amount = Decimal(value),original_amount=plan_amount)
          obj_user.plan = plan_id.id
          obj_user.plan_start_date = plan_edit.plan_start_date
          now = plan_edit.plan_start_date
          desired_time = datetime.time(23, 55)
          today_with_desired_time = datetime.datetime.combine(now.date(), desired_time)
          end_date = today_with_desired_time + timedelta(plan_days)
          obj_user.plan_end_date = end_date
          obj_user.user_referral_eligible_level = plan_id.referral_level_eligible
          obj_user.plan_validation = plan_period
          obj_user.save()
          obj_user.Health_Withdraw_max_value = plan_id.health_withdraw_maximum_limit
          obj_user.Health_Withdraw_min_value = plan_id.health_withdraw_minimum_limit
          obj_user.Referral_Withdraw_max_value = plan_id.referral_withdraw_maximum_limit
          obj_user.Referral_Withdraw_min_value = plan_id.referral_withdraw_minimum_limit
          obj_user.save()
          plan_hist_mann.delete()
          user_ref.delete()
          if plan_edit.old_plan_type == 1:
            try:
              jw_hist=Jw_plan_purchase_history.objects.filter(user_id=obj_user.id).last()
              jw_hist.delete()
            except:
              jw_hist=0
            Jw_plan_purchase_history.objects.create(user = obj_user,activate_plan=plan_id.activate_plan ,plan_name = plan_id.plan_name ,stake_credit=plan_id.user_stake_credit,purchase_amount = amunt,user_wallet_type = plan_edit.user_wallet_type, buy_type = "Admin Edit Buy")
            plan_purchase_history.objects.create(user = obj_user , User_plan_validation =plan_edit.trans_hash , plan_id = plan_id , Plan_maximum_step = plan_id.Max_step_count , Plan_minimum_step = plan_id.Min_step_count , Plan_maximum_reward = plan_id.reward_amount , Plan_referral_status = plan_id.referral_status , Plan_Two_X_Boost_status = plan_id.two_X_Boost_status , Plan_Withdraw_status = plan_id.withdraw_status , Plan_Level = plan_id.referral_level_eligible , purchase_amount = plan_amount , user_wallet_type = plan_edit.user_wallet_type , buy_type = "Admin Edit Plan ",plan_reward_step_val = plan_id.Reward_step_value,plan_per_reward_amount = plan_id.plan_reward_amount,stake_wallet_monthly_split_percentage=plan_id.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=plan_id.withdraw_wallet_monthly_percentage,created_on=plan_edit.created_on,support_status=plan_id.support_status,monthly_support=plan_id.monthly_support_status,quarterly_support=plan_id.quarterly_support_status,annual_support=plan_id.annual_support_status,plan_purchase_type=plan_purchase,halfyearly_support=plan_id.halfyearly_support_status,monthly_support_amount=plan_id.monthly_support_amount,quarterly_support_amount=plan_id.quarterly_support_amount,halfyearly_support_amount=plan_id.halfyearly_support_amount,annual_support_amount=plan_id.annual_support_amount,current_api_price=price)
          else:
             plan_purchase_history.objects.create(user = obj_user , User_plan_validation =plan_edit.trans_hash , plan_id = plan_id , Plan_maximum_step = plan_id.Max_step_count , Plan_minimum_step = plan_id.Min_step_count , Plan_maximum_reward = plan_id.reward_amount , Plan_referral_status = plan_id.referral_status , Plan_Two_X_Boost_status = plan_id.two_X_Boost_status , Plan_Withdraw_status = plan_id.withdraw_status , Plan_Level = plan_id.referral_level_eligible , purchase_amount = plan_amount , user_wallet_type = plan_edit.user_wallet_type , buy_type = "Admin Edit Plan ",plan_reward_step_val = plan_id.Reward_step_value,plan_per_reward_amount = plan_id.plan_reward_amount,stake_wallet_monthly_split_percentage=plan_id.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=plan_id.withdraw_wallet_monthly_percentage,created_on=plan_edit.created_on,support_status=plan_id.support_status,monthly_support=plan_id.monthly_support_status,quarterly_support=plan_id.quarterly_support_status,annual_support=plan_id.annual_support_status,plan_purchase_type=plan_purchase,halfyearly_support=plan_id.halfyearly_support_status,monthly_support_amount=plan_id.monthly_support_amount,quarterly_support_amount=plan_id.quarterly_support_amount,halfyearly_support_amount=plan_id.halfyearly_support_amount,annual_support_amount=plan_id.annual_support_amount,current_api_price=price)
          step_reward=Reward_History.objects.filter(user_id=obj_user.id,created_on__date__gte=plan_edit.plan_start_date.date())
          for i in step_reward:
            i.Reward= plan_id.reward_amount
            i.save()
          User_Management.objects.filter(id = obj_user.id).update(plan = plan_id.id)

          if obj_user.referal_code != "" or obj_user.referal_code != None:
            
            a=[]
            ref_code = obj_user.referal_code
            
            reff_id = Referral_code.objects.get(referal_code=ref_code)
            referred_user = User_Management.objects.get(id = reff_id.user.id)
            uesr_level = obj_user.Referral_Level
            Referral_level = referral_level.objects.all().count()
            for i in range(Referral_level):
                reff_id = Referral_code.objects.get(referal_code=ref_code)
                referred_user = User_Management.objects.get(id = reff_id.user.id)
                a.append(referred_user.id)
                ref_code = referred_user.referal_code
                if referred_user.referal_code == "" or referred_user.referal_code == None:
                    break
            b = 1
            l = 0
            obj_plan_hist = plan_purchase_history.objects.filter(user_id = obj_user.id).count()
            if obj_plan_hist == 1:
              for i in a:
                  user = User_Management.objects.get(id = i)
                  if user.plan == 0:
                      b = b+1 
                      pass
                  else:
                      try:
                          plan_hist=plan_purchase_history.objects.filter(plan_id=user.plan).last()
                      except:
                          plan_hist=''
                      if plan_hist:
                          if plan_hist.Plan_referral_status == 0:
                              b = b+1
                              pass      
                          elif plan_hist.Plan_referral_status == 1:
                            if user.user_referral_eligible_level >= plan_hist.Plan_Level and plan_hist.Plan_Level >= b:
                              User_Referral_level = referral_level.objects.get(referral_level_id = b)
                              if plan_purchase == 1:
                                  Purchase_Amount = Decimal(amunt)
                              else:
                                  Purchase_Amount = Decimal(plan_amount)
                              percentage = (User_Referral_level.commission_amount * Purchase_Amount)/100
                              actual_reward = Decimal(percentage) 
                              l=l+actual_reward
                              userwallet = UserCashWallet.objects.get(userid = i)
                              userwallet.referalincome = userwallet.referalincome + actual_reward
                              userwallet.save()
                              table = Referral_reward_History.objects.create(user = user,referral_id = (obj_user.Name),reward = Decimal(actual_reward))
                              b = b+1 
                            else:
                              b = b +1
                              pass
                      else:
                          b = b +1
                          pass
            sum = 0
            if plan_edit.old_plan_type == 1:
              admin_profit = Decimal(amunt) - l
              adminprofit = Admin_Profit.objects.create(user = obj_user,admin_profit = admin_profit,Profit_type = "Plan Purchase")
            else:
              admin_profit = plan_amount - l
              adminprofit = Admin_Profit.objects.create(user = obj_user,admin_profit = admin_profit,Profit_type = "Plan Purchase")           
            messages.add_message(request, messages.SUCCESS, 'Plan Edited to '+str(obj_user.Name)+' successfully.')
            return HttpResponseRedirect('/tradeadmin/user_history_table/'+str(id)+'/')
          else:
            pass
        else:
          messages.add_message(request, messages.ERROR, 'No plan to edit')
      else:
        messages.add_message(request, messages.ERROR, 'Plan Period required')
    else:
        messages.add_message(request, messages.ERROR, 'Plan Name required')
  plan_hist_user=plan_purchase_history.objects.filter(user_id=obj_user.id).last()
  context["obj_plan"] = obj_plan
  context["Title"] = "Edit User Plan"
  context["obj_user"] = obj_user  
  context["plan_hist_user"] = plan_hist_user
  context["plan_start_date"]=obj_user.plan_start_date
  context["plan_end_date"]=obj_user.plan_end_date
  context["market"]=companyqs.market_api_price 
  context["fixed"]=Market_Price.market_price
  return render(request,"trade_admin_auth/edit_user_plan.html",context)



from django.utils import timezone

def user_add_usdt(request, id):
    context = {}

    try:
        obj_user = User_Management.objects.get(id=id)
    except User_Management.DoesNotExist:
        obj_user = None

    if request.method == "POST":
        amount = request.POST["Amount"]
        trans_hash = request.POST["transaction_hash"]
        duration = request.POST["duration"]
        address = request.POST["Address"]
        if amount:
          if trans_hash:
            if address: 
              if int(duration) == 1:
                  package_days = 30 
              elif int(duration) == 2:
                  package_days = 90
              elif int(duration) == 3:
                  package_days = 180
              elif int(duration) == 4:
                  package_days = 365

              try:
                  companyqs = Company.objects.get(id=1)
                  companyname = companyqs.name
                  support_address = companyqs.support_address
              except Company.DoesNotExist:
                  companyname = ''
                  support_address = ''

              currency = "USDT"
              withdraw_status = WithdrawSendUSDTHistory.objects.filter(Transaction_Hash=trans_hash).count()
              withdraw_email = WithdrawSendUSDTHistory.objects.filter(Transaction_Hash=trans_hash)
              for i in withdraw_email:
                email=i.user
              if withdraw_status == 0:
                  plan_start_date = timezone.now()
                  plan_end_date = plan_start_date + timezone.timedelta(days=package_days)
                  
                  WithdrawSendUSDTHistory.objects.create(
                      user=obj_user.Email,
                      email=obj_user,  # This should be the ForeignKey field, assuming it relates to User_Management
                      claim_amount=amount,
                      from_address=address,
                      to_address=support_address,
                      Transaction_Hash=trans_hash,
                      type="Admin_add_usdt",
                      send_status=1,
                      currency=currency,
                      plan_start_date=plan_start_date,
                      plan_end_date=plan_end_date,
                      created_on=timezone.now(),
                      modified_on=timezone.now()
                  )
                  messages.add_message(request, messages.SUCCESS, 'History Created Successfully!!!')
              else:
                  messages.add_message(request, messages.ERROR, 'This Hash has already been applied to user: '+str(email))
            else:
              messages.add_message(request, messages.ERROR, 'Address Required!!!')
          else:
            messages.add_message(request, messages.ERROR, 'Transcation Hash Required!!!')
        else:
              messages.add_message(request, messages.ERROR, 'Amount Required!!!')

    context['Title'] = 'Add USDT History'
    return render(request, "trade_admin_auth/add_user_usdt.html", context)
  
  

from django.utils import timezone
from decimal import Decimal
from django.contrib import messages

def purchase_bot(request, id):
    context = {}

    try:
        obj_user = User_Management.objects.get(id=id)
    except User_Management.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'User does not exist')
        return render(request, "trade_admin_auth/add_user_usdt.html", context)

    if request.method == "POST":
        amount = request.POST.get("Amount")
        trans_hash = request.POST.get("transaction_hash")
        duration = request.POST.get("duration")
        address = request.POST.get("Address")

        if not amount:
            messages.add_message(request, messages.ERROR, 'Amount Required!!!')
        elif not trans_hash:
            messages.add_message(request, messages.ERROR, 'Transaction Hash Required!!!')
        elif not address:
            messages.add_message(request, messages.ERROR, 'Address Required!!!')
        else:
            # Determine package days based on duration
            package_days_map = {1: 30, 2: 90, 3: 180, 4: 365}
            package_days = package_days_map.get(int(duration), 30)  # default to 30 days if invalid duration

            # Fetch company details
            try:
                companyqs = Company.objects.get(id=1)
                companyname = companyqs.name
                support_address = companyqs.support_address
            except Company.DoesNotExist:
                companyname = ''
                support_address = ''

            # Check if the transaction hash has been used already
            withdraw_status = WithdrawSendUSDTHistoryboat.objects.filter(Transaction_Hash=trans_hash).exists()
            if not withdraw_status:
                plan_start_date = timezone.now()
                plan_end_date = plan_start_date + timezone.timedelta(days=package_days)

                # Create new transaction record
                WithdrawSendUSDTHistoryboat.objects.create(
                    user=obj_user.Email,
                    email=obj_user,  # Assuming this is a ForeignKey to User_Management
                    claim_amount=amount,
                    from_address=address,
                    to_address=support_address,
                    Transaction_Hash=trans_hash,
                    type="Admin_add_usdt",
                    send_status=1,
                    currency="JW",
                    plan_start_date=plan_start_date,
                    plan_end_date=plan_end_date,
                    created_on=timezone.now(),
                    modified_on=timezone.now()
                )

                # Create boat purchase history
                boat_purchase_history.objects.create(
                    user_id=obj_user.id,
                    purchase_amount=100,
                    user_wallet_type="Boat Reward Wallet",
                    buy_type="Admin buy",
                    status=0
                )
                obj_user.boat_status = 0
                obj_user.save()

                # Referral processing logic
                ref_code = obj_user.referal_code
                try:
                    reff_id = Referral_code.objects.get(referal_code=ref_code)
                    referred_user = User_Management.objects.get(id=reff_id.user.id)
                except Referral_code.DoesNotExist:
                    referred_user = None

                a = []
                if referred_user:
                    while referred_user and referred_user.referal_code:
                        a.append(referred_user.id)
                        try:
                            reff_id = Referral_code.objects.get(referal_code=referred_user.referal_code)
                            referred_user = User_Management.objects.get(id=reff_id.user.id)
                        except (Referral_code.DoesNotExist, User_Management.DoesNotExist):
                            break

                # Reward calculation logic
                b = 1
                l = 0
                for i in a:
                    user = User_Management.objects.get(id=i)
                    if user.boat_status == 1:
                        b += 1
                        continue

                    # Check if the user has an active plan
                    try:
                        plan_hist = boat_purchase_history.objects.filter(user_id=user.id).last()
                    except boat_purchase_history.DoesNotExist:
                        plan_hist = None

                    if plan_hist and plan_hist.status == 1:
                        b += 1
                        continue

                    # Referral reward logic
                    if 10 >= b:
                        try:
                            User_Referral_level = referral_level.objects.get(referral_level_id=b)
                        except referral_level.DoesNotExist:
                            continue

                        Purchase_Amount = Decimal(amount)
                        direct_referrals = User_Management.objects.filter(reff_id=i, boat_status=0).count()

                        if direct_referrals >= b:
                            percentage = (User_Referral_level.second_level_commission_amount * Purchase_Amount) / 100
                            actual_reward = Decimal(percentage)
                            l += actual_reward

                            # Update user wallet with referral income
                            userwallet = UserCashWallet.objects.get(userid=i)
                            userwallet.Boatreferalincome += actual_reward
                            userwallet.save()

                            # Create a reward history entry
                            Boat_Referral_income_History.objects.create(
                                user=user,
                                referral_id="BOT  "+str(obj_user.Name),
                                reward=actual_reward
                            )

                        b += 1

                messages.add_message(request, messages.SUCCESS, 'History Created Successfully!!!')
            else:
                email = withdraw_email.first().user if withdraw_email.exists() else 'unknown user'
                messages.add_message(request, messages.ERROR, f'This Hash has already been applied to user: {email}')

    context['Title'] = 'Purchase Bot  :-' + str(obj_user.Email)
    return render(request, "trade_admin_auth/purchase_bot.html", context)


def download_CSV_deposit_user(request,id):
 
  if request.method == "POST":
    try:
      str_date = request.POST["start_date"]
      end_date = request.POST["end_date"]
    except:
      str_date = ""
      end_date = ""

    try:
      obj_withdraw = stake_deposit_management.objects.using('second_db').values('user','email','Amount_USDT','type','Amount_JW','Hash','created_on').filter(created_on__date__gte = str_date , created_on__date__lte = end_date).order_by('-id')
    except:
      obj_withdraw = ""
    if obj_withdraw:
      re_count = obj_withdraw.count()

      if(re_count > 0):
        data = list(obj_withdraw)
        res_data = {"status" : "true" , "data" : data , "start_date" : str_date , "end_date" : end_date}
      else:
        data =''
        res_data = {"status" : "true" , "data" : data}
    else:
      data =''
      res_data = {"status" : "false" , "data" : data , "start_date" : str_date , "end_date" : end_date}

    return JsonResponse(res_data)


def download_csv_stake_history(request):
  if request.method == "POST":
    try:
      str_date = request.POST["start_date"]
      end_date = request.POST["end_date"]
    except:
      str_date = ""
      end_date = ""

    try:
      obj_user = Stake_history_management.objects.using('second_db').values('user','email','Amount_USDT','Amount_JW','market_price','period','maximum_reward','reward_percent','reward_per_month','reward_earned','referral_reward_earned','Total_reward_earned','reward_balance','referral_status','referral_level','claim_status','start_date','end_date').filter(created_on__date__gte = str_date , created_on__date__lte = end_date).order_by('created_on')
    except:
      obj_user = ""

    if obj_user:
      re_count = obj_user.count()

      if(re_count > 0):
        data = list(obj_user)
        res_data = {"status" : "true" , "data" : data , "start_date" : str_date , "end_date" : end_date}
      else:
        data =''
        res_data = {"status" : "true" , "data" : data}
    else:
      data =''
      res_data = {"status" : "false" , "data" : data , "start_date" : str_date , "end_date" : end_date}

    return JsonResponse(res_data)

def download_csv_deposit_history(request):
  if request.method == "POST":
    try:
      str_date = request.POST["start_date"]
      end_date = request.POST["end_date"]
    except:
      str_date = ""
      end_date = ""

    try:
      obj_user = stake_deposit_management.objects.using('second_db').values('user','email','Amount_USDT','Amount_JW','Hash','created_on').filter(created_on__date__gte = str_date , created_on__date__lte = end_date).order_by('created_on')
    except:
      obj_user = ""
    if obj_user:
      re_count = obj_user.count()

      if(re_count > 0):
        data = list(obj_user)
        res_data = {"status" : "true" , "data" : data , "start_date" : str_date , "end_date" : end_date}
      else:
        data =''
        res_data = {"status" : "true" , "data" : data}
    else:
      data =''
      res_data = {"status" : "false" , "data" : data , "start_date" : str_date , "end_date" : end_date}

    return JsonResponse(res_data)
  
def download_csv_claim_history(request):
  if request.method == "POST":
    try:
      str_date = request.POST["start_date"]
      end_date = request.POST["end_date"]
    except:
      str_date = ""
      end_date = ""

    try:
      obj_user = stake_claim_table.objects.using('second_db').values('user','email','original_USDT','claim_amount_USDT','claim_amount_JW','Address','Transaction_Hash','Wallet_type','created_on').filter(created_on__date__gte = str_date , created_on__date__lte = end_date).order_by('created_on')
    except:
      obj_user = ""
    if obj_user:
      re_count = obj_user.count()

      if(re_count > 0):
        data = list(obj_user)
        res_data = {"status" : "true" , "data" : data , "start_date" : str_date , "end_date" : end_date}
      else:
        data =''
        res_data = {"status" : "true" , "data" : data}
    else:
      data =''
      res_data = {"status" : "false" , "data" : data , "start_date" : str_date , "end_date" : end_date}

    return JsonResponse(res_data)
  
  
def add_user_deposit(request, id):
    context = {}
    try:
        obj_user = User_Management.objects.get(id=id)
    except User_Management.DoesNotExist:
        obj_user = None
    stake_price_details = Stake_market_price.objects.using('second_db').get(id = 1)
    market_price=stake_price_details.market_price
    if request.method == "POST":
        amount_JW = request.POST["Amount"]
        trans_hash = request.POST["transaction_hash"]
        if amount_JW:
          if trans_hash:
              withdraw_status = stake_deposit_management.objects.using('second_db').filter(Hash=trans_hash).count()
              if withdraw_status == 0:
                  price=Decimal(amount_JW) * Decimal(market_price)
                  amount=round(price, 2)
                  stake_deposit_management.objects.using('second_db').create(
                  user=obj_user.id,         
                  email=obj_user.Email,      
                  Amount_USDT=amount,      
                  type="Admin Create",        
                  Amount_JW=amount_JW,     
                  Hash=trans_hash,          
                  status=1,                 
              )
                  messages.add_message(request, messages.SUCCESS, 'Deposit  History Created Successfully!!!')
              else:
                  messages.add_message(request, messages.ERROR, 'This Hash has already been applied to user: '+obj_user.Email)
          else:
            messages.add_message(request, messages.ERROR, 'Transcation Hash Required!!!')
        else:
              messages.add_message(request, messages.ERROR, 'Amount Required!!!')

    context['Title'] = 'Add Deposit History'
    context['obj_user'] = obj_user
    context['market_price'] = market_price
  
    return render(request, "trade_admin_auth/add_user_deposit.html", context)

def delete_withdraw_history(request,id):
  withdraw=Withdraw.objects.get(id=id)
  user_Deatail=User_Management.objects.get(id = withdraw.userid_id)
  obj_wall_blnc = UserCashWallet.objects.get(userid_id = user_Deatail.id)
  obj_wall_flush_blnc = wallet_flush_history.objects.filter(user_id = user_Deatail.id).last()
  end_date = user_Deatail.plan_end_date + timedelta(1) 
  if obj_wall_flush_blnc != None:
      UserCashWallet.objects.filter(userid_id = user_Deatail.id).update(balanceone = obj_wall_flush_blnc.wallet_balanceone , referalincome = obj_wall_flush_blnc.Wallet_referral_income)
      User_Management.objects.filter(id = withdraw.userid_id).update(plan_end_date = end_date)
  else:
      User_Management.objects.filter(id = withdraw.userid_id).update(plan_end_date = end_date)
  withdraw.delete()
  messages.add_message(request, messages.SUCCESS, 'Record Delete Successfully!!!')
  return HttpResponseRedirect("/tradeadmin/user_history_table/"+str(withdraw.userid_id)+"/")



def delete_all_withdraw_history(request,id):
  withdraw=Withdraw.objects.get(id=id)
  user_Deatail=User_Management.objects.get(id = withdraw.userid_id)
  obj_wall_blnc = UserCashWallet.objects.get(userid_id = user_Deatail.id)
  obj_wall_flush_blnc = wallet_flush_history.objects.filter(user_id = user_Deatail.id).last()
  end_date = user_Deatail.plan_end_date + timedelta(1) 
  if obj_wall_flush_blnc != None:
      UserCashWallet.objects.filter(userid_id = user_Deatail.id).update(balanceone = obj_wall_flush_blnc.wallet_balanceone , referalincome = obj_wall_flush_blnc.Wallet_referral_income)
      User_Management.objects.filter(id = withdraw.userid_id).update(plan_end_date = end_date)
  else:
      User_Management.objects.filter(id = withdraw.userid_id).update(plan_end_date = end_date)
  withdraw.delete()
  messages.add_message(request, messages.SUCCESS, 'Record Delete Successfully!!!')
  return HttpResponseRedirect("/tradeadmin/List_Withdraw_Request/")


def Edit_withdraw_history(request,id):
  context={}
  context['Title'] = 'Withdraw History Edit'
  stake_credit_amount=""
  if request.method == "POST":
    Transaction_Hash = request.POST["Transaction_Hash"]
    try:
      companyqs = Company.objects.get(id=1)
      companyname= companyqs.name
    except:
        companyqs = ''
        companyname = ''
    if Transaction_Hash:
      withdraw=Withdraw.objects.get(id=id)
      obj_user = User_Management.objects.get(id=withdraw.userid_id)
      withdraw_hash=Withdraw.objects.filter(Transaction_Hash=Transaction_Hash).count()
      if withdraw_hash == 0:          
        marketprice= market_price.objects.get(id = 1)
        user_plan_history = plan_purchase_history.objects.filter(user_id = withdraw.userid_id).last()
        stake_wall_per  =  0#user_plan_history.stake_wallet_monthly_split_percentage
        currency = TradeCurrency.objects.get(symbol = 'JW')
        stake_credit_amount=Decimal(withdraw.Amount)*stake_wall_per/100
        if str(obj_user.created_on) >= str("2023-11-11 12:00:00.000000"):
          converted_price=stake_credit_amount
        else:
          converted_price= (stake_credit_amount) / Decimal(marketprice.market_price) * Decimal(companyqs.market_api_price)

        fees=Decimal(withdraw.Amount)*currency.withdraw_fees/100
        withdraw_usdt = Decimal(withdraw.Amount) - ((fees)+ (stake_credit_amount))
        wei_priceee=Decimal(withdraw_usdt) / Decimal(marketprice.market_price)
        wei_price=f"{wei_priceee:.8f}"
        cash = UserCashWallet.objects.get(userid_id = withdraw.userid_id )
        if withdraw.Wallet_type == 'Reward_wallet':
            cash.balanceone = cash.balanceone - Decimal(withdraw.Amount)
            cash.balancetwo = cash.balancetwo + Decimal(converted_price)
            cash.save()
        if withdraw.Wallet_type == 'Referral_wallet':
            cash.referalincome = cash.referalincome - Decimal(withdraw.Amount)
            cash.balancetwo = cash.balancetwo + Decimal(converted_price)
            cash.save()
        # table2 = Stake_Credit_History.objects.create(user_id = withdraw.userid_id,original_reward = withdraw.Amount,stake_percentage = stake_wall_per,percent_value=converted_price)
        withdraw.Transaction_Hash=Transaction_Hash
        withdraw.status=1
        withdraw.Withdraw_fee = currency.withdraw_fees
        withdraw.Withdraw_USDT = withdraw_usdt
        withdraw.Withdraw_JW = wei_price
        withdraw.Month_stake = stake_wall_per
        withdraw.save()
        messages.add_message(request, messages.SUCCESS, 'Hash Updated Successfully!!!!!!!!!' )
        return redirect("/tradeadmin/user_history_table/"+str(withdraw.userid_id)+"/")
      else:
        messages.add_message(request, messages.ERROR, 'Transaction hash already applied for this user: '+str(obj_user.Email))
    else:
      messages.add_message(request, messages.ERROR, 'Hash Required!!!!!' ) 
  return render(request,'trade_admin_auth/withdraw_history_edit.html',context)

def Edit_User_Plan_reward(request,id,plan_name,plan_period,user_id,name):
  context = {}
  try:
    obj_user = User_Management.objects.get(id = id)
  except:
    obj_user = ""
  obj_reff=user_id
  obj_plan = plan.objects.filter(plan_type = 1)
  try:
      companyqs = Company.objects.get(id=1)
      companyname= companyqs.name
  except:
      companyqs = ''
      companyname = ''
  Market_Price = market_price.objects.get(id = 1)
  plan_name = plan_name
  plan_period = plan_period
  price = "26"
  plan_hist_mann=plan_purchase_history.objects.filter(user_id=obj_user.id).last()
  plan_days=''
  plan_hist_man=plan_purchase_history.objects.values('plan_id','user_id','User_plan_validation','user_wallet_type','created_on','Plan_maximum_reward','plan_purchase_type').filter(user_id=obj_user.id).last()
  date_del=plan_hist_man['created_on']
  plan_id_id = plan.objects.get(id =plan_hist_man['plan_id'])
  user_ref = Referral_reward_History.objects.filter(referral_id = obj_user.Name,created_on__date__gte=date_del.date())
  plan_id = plan.objects.get(plan_name = plan_name)
  plan_purchase=int(plan_id.plan_purchase_type)
  if plan_period == "Monthly":
    plan_duration = 0
    plan_days = 30
    plan_amount = plan_id.plan_purchase_amount_monthly
  if plan_period == "Quarterly":
    plan_duration = 1
    plan_days = 90
    plan_amount = plan_id.plan_purchase_amount_quarterly
  if plan_period == "Annual":
    plan_duration = 2
    plan_days = 365
    plan_amount = plan_id.plan_purchase_amount_annual
  
  plan_edit=plan_purchase_history_edited.objects.create(user=obj_user,old_plan=plan_id_id.plan_name,new_plan=plan_name,user_wallet_type=plan_hist_man['user_wallet_type'],buy_type="Admin Edit plan",trans_hash=plan_hist_man['User_plan_validation'],created_on=plan_hist_man['created_on'],modified_on=datetime.datetime.now(),plan_start_date=obj_user.plan_start_date,plan_end_date=obj_user.plan_end_date,old_plan_type=plan_purchase,new_plan_type=plan_hist_man['plan_purchase_type'])
  new_type=int(plan_edit.new_plan_type)
  wallet = UserCashWallet.objects.get(userid = obj_user)
  wallet_flush_history.objects.create(user = obj_user,wallet_balanceone = wallet.balanceone,Wallet_referral_income = wallet.referalincome,User_before_plan = obj_user.plan)

  wallet.balanceone = 0
  wallet.referalincome = 0
  wallet.save()
  if new_type == 1:
    try:
      stake_his=stake_claim_reward_history.objects.using('second_db').filter(user = obj_user.id,type="Plan Purchase").last()
      stake_his.delete()
    except:
      stake_his=0
  if plan_edit.old_plan_type == 1:
    try:
        user_stake_obj = stake_wallet_management.objects.using('second_db').get(user = obj_user.id)
    except:
        user_stake_obj = 0
    if user_stake_obj != 0:
        try:
          stake_his=stake_claim_reward_history.objects.using('second_db').filter(user = obj_user.id,type="Plan Purchase").last()
          stake_his.delete()
        except:
          stake_his=0
        amunt=plan_id.activate_plan
        value=Decimal(plan_amount) - Decimal(amunt)
        user_stake_obj.stake_Wallet=Decimal(user_stake_obj.stake_Wallet)  + Decimal(value)
        user_stake_obj.save(using='second_db')
        stake_claim_reward_history.objects.using('second_db').create(user = obj_user.id,email=obj_user.Email,type='Plan Purchase',stake_Wallet_reward_amount = Decimal(value),original_amount=plan_amount,buy_type="user_buy")
  obj_user.plan = plan_id.id
  obj_user.plan_start_date = plan_edit.plan_start_date
  now = plan_edit.plan_start_date
  desired_time = datetime.time(23, 55)
  today_with_desired_time = datetime.datetime.combine(now.date(), desired_time)
  end_date = today_with_desired_time + timedelta(plan_days)
  obj_user.plan_end_date = end_date
  obj_user.user_referral_eligible_level = plan_id.referral_level_eligible
  obj_user.plan_validation = plan_period
  obj_user.save()
  obj_user.Health_Withdraw_max_value = plan_id.health_withdraw_maximum_limit
  obj_user.Health_Withdraw_min_value = plan_id.health_withdraw_minimum_limit
  obj_user.Referral_Withdraw_max_value = plan_id.referral_withdraw_maximum_limit
  obj_user.Referral_Withdraw_min_value = plan_id.referral_withdraw_minimum_limit
  obj_user.save()
  plan_hist_mann.delete()
  if plan_edit.old_plan_type == 1:
    try:
      jw_hist=Jw_plan_purchase_history.objects.filter(user_id=obj_user.id).last()
      jw_hist.delete()
    except:
      jw_hist=0
    Jw_plan_purchase_history.objects.create(user = obj_user,activate_plan=plan_id.activate_plan ,plan_name = plan_id.plan_name ,stake_credit=plan_id.user_stake_credit,purchase_amount = amunt,user_wallet_type = plan_edit.user_wallet_type, buy_type = "Admin Edit Buy")
    plan_purchase_history.objects.create(user = obj_user , User_plan_validation =plan_edit.trans_hash , plan_id = plan_id , Plan_maximum_step = plan_id.Max_step_count , Plan_minimum_step = plan_id.Min_step_count , Plan_maximum_reward = plan_id.reward_amount , Plan_referral_status = plan_id.referral_status , Plan_Two_X_Boost_status = plan_id.two_X_Boost_status , Plan_Withdraw_status = plan_id.withdraw_status , Plan_Level = plan_id.referral_level_eligible , purchase_amount = plan_amount , user_wallet_type = plan_edit.user_wallet_type , buy_type = "Admin Edit Plan ",plan_reward_step_val = plan_id.Reward_step_value,plan_per_reward_amount = plan_id.plan_reward_amount,stake_wallet_monthly_split_percentage=plan_id.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=plan_id.withdraw_wallet_monthly_percentage,created_on=plan_edit.created_on,support_status=plan_id.support_status,monthly_support=plan_id.monthly_support_status,quarterly_support=plan_id.quarterly_support_status,annual_support=plan_id.annual_support_status,plan_purchase_type=plan_purchase,halfyearly_support=plan_id.halfyearly_support_status,monthly_support_amount=plan_id.monthly_support_amount,quarterly_support_amount=plan_id.quarterly_support_amount,halfyearly_support_amount=plan_id.halfyearly_support_amount,annual_support_amount=plan_id.annual_support_amount,current_api_price=price)
  else:
      plan_purchase_history.objects.create(user = obj_user , User_plan_validation =plan_edit.trans_hash , plan_id = plan_id , Plan_maximum_step = plan_id.Max_step_count , Plan_minimum_step = plan_id.Min_step_count , Plan_maximum_reward = plan_id.reward_amount , Plan_referral_status = plan_id.referral_status , Plan_Two_X_Boost_status = plan_id.two_X_Boost_status , Plan_Withdraw_status = plan_id.withdraw_status , Plan_Level = plan_id.referral_level_eligible , purchase_amount = plan_amount , user_wallet_type = plan_edit.user_wallet_type , buy_type = "Admin Edit Plan ",plan_reward_step_val = plan_id.Reward_step_value,plan_per_reward_amount = plan_id.plan_reward_amount,stake_wallet_monthly_split_percentage=plan_id.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=plan_id.withdraw_wallet_monthly_percentage,created_on=plan_edit.created_on,support_status=plan_id.support_status,monthly_support=plan_id.monthly_support_status,quarterly_support=plan_id.quarterly_support_status,annual_support=plan_id.annual_support_status,plan_purchase_type=plan_purchase,halfyearly_support=plan_id.halfyearly_support_status,monthly_support_amount=plan_id.monthly_support_amount,quarterly_support_amount=plan_id.quarterly_support_amount,halfyearly_support_amount=plan_id.halfyearly_support_amount,annual_support_amount=plan_id.annual_support_amount,current_api_price=price)
  step_reward=Referral_reward_History.objects.filter(user_id = obj_reff,referral_id=name)
  for i in step_reward:
    i.reward= plan_id.reward_amount
    i.save()


def reward_update_api(request,id):
  obj_ref_hist = Referral_reward_History.objects.filter(user_id = id)
  for i in obj_ref_hist:
    user_Deatail=User_Management.objects.get(Name = i.referral_id)
    plan_details=plan.objects.get(id=user_Deatail.plan)
    Edit_User_Plan_reward(request,user_Deatail.id,plan_details.plan_name,"Monthly",id,user_Deatail.Name)
  messages.add_message(request, messages.SUCCESS, 'Reward Updated Successfully')
  return HttpResponseRedirect('/tradeadmin/user_history_table/'+str(id)+'/')



def delete_referral(request,id):
  ref_reward=Referral_reward_History.objects.get(id=id)
  ref_reward.delete()
  messages.add_message(request, messages.SUCCESS, 'Reward Delete Successfully')
  return HttpResponseRedirect('/tradeadmin/List_User_Management/')


def botdelete_referral(request,id):
  ref_reward=Boat_Referral_reward_History.objects.get(id=id)
  ref_reward.delete()
  messages.add_message(request, messages.SUCCESS, 'Reward Delete Successfully')
  return HttpResponseRedirect('/tradeadmin/List_User_Management/')

def mpdelete_referral(request,id):
  ref_reward=MPRewardHistory.objects.get(id=id)
  ref_reward.delete()
  messages.add_message(request, messages.SUCCESS, 'Reward Delete Successfully')
  return HttpResponseRedirect('/tradeadmin/List_User_Management/')

def burndelete_referral(request,id):
  ref_reward=BurnRewardHistory.objects.get(id=id)
  ref_reward.delete()
  messages.add_message(request, messages.SUCCESS, 'Reward Delete Successfully')
  return HttpResponseRedirect('/tradeadmin/List_User_Management/')


def settings_price(request):
  if request.method == "POST":
    market_price_details = request.POST['market_price']
    API = request.POST['API']
    status = request.POST['status']
    market_model = Company.objects.get(id = 1)
    market_model.market_api_price = market_price_details
    market_model.API = API
    market_model.status = status
    market_model.save()
    messages.add_message(request, messages.SUCCESS, 'Market Price Updated Successfully.')
    return HttpResponseRedirect('/tradeadmin/general_settings/1/')


  
def user_plan_edit(request, id):
    context = {}
    context['Title'] = 'User Plan Edit'
    user_details = User_Management.objects.get(id=id)

    if request.method == "POST": 
        health_max = request.POST.get('health_max')
        health_min = request.POST.get('health_min')
        referral_max = request.POST.get('referral_max')
        referral_min = request.POST.get('referral_min')
        USDT_JW = request.POST.get('USDT_JW')
        Withdraw_X = request.POST.get('Withdraw_X')
        bnbstatus = request.POST.get('bnbstatus')

        try:
            # Update only the provided fields
            if health_min and health_min.isdigit():
                user_details.Health_Withdraw_min_value = int(health_min)

            if health_max and health_max.isdigit():
                user_details.Health_Withdraw_max_value = int(health_max)

            if referral_min and referral_min.isdigit():
                user_details.Referral_Withdraw_min_value = int(referral_min)

            if referral_max and referral_max.isdigit():
                user_details.Referral_Withdraw_max_value = int(referral_max)

            if USDT_JW:  # Assuming this is a string field
                user_details.USDT_status = USDT_JW

            if Withdraw_X and Withdraw_X.strip():  # Check if Withdraw_X is not empty or whitespace
                user_details.xvalue = int(Withdraw_X)
                
            if bnbstatus and bnbstatus.strip():  # Check if Withdraw_X is not empty or whitespace
                user_details.BNBStatus = int(bnbstatus)
            # Save the updated user details
            user_details.save()
            messages.success(request, 'Successfully Updated!')
            return HttpResponseRedirect('/tradeadmin/user_history_table/' + str(user_details.id) + '/')

        except ValueError as e:
            # Handle cases where an invalid value is provided
            messages.add_message(request, messages.ERROR, f"Invalid input: {e}")

    return render(request, 'trade_admin_auth/user_plan_edit.html', context)


# def user_plan_edit(request, id):
#     context = {}
#     context['Title'] = 'User Plan Edit'
#     user_details = User_Management.objects.get(id=id)

#     if request.method == "POST": 
#         health_max = request.POST.get('health_max')
#         health_min = request.POST.get('health_min')
#         referral_max = request.POST.get('referral_max')
#         referral_min = request.POST.get('referral_min')
#         USDT_JW = request.POST.get('USDT_JW')
#         Withdraw_X = request.POST.get('Withdraw_X')

#         # Check if all values are digits and Withdraw_X is not empty
#         if all(val.isdigit() for val in [health_max, health_min, referral_max, referral_min]):
#             try:
#                 # Check if Withdraw_X is empty, if so, set a default value
#                 if Withdraw_X.strip() == '':
#                     raise ValueError("Withdraw_X cannot be empty")

#                 # Convert Withdraw_X to an integer
#                 user_details.Health_Withdraw_min_value = health_min
#                 user_details.Health_Withdraw_max_value = health_max
#                 user_details.Referral_Withdraw_min_value = referral_min
#                 user_details.Referral_Withdraw_max_value = referral_max
#                 user_details.USDT_status = USDT_JW
#                 user_details.xvalue = int(Withdraw_X)  # Now this is safe
#                 user_details.save()

#                 messages.success(request, 'Successfully Updated!')
#                 return HttpResponseRedirect('/tradeadmin/user_history_table/' + str(user_details.id) + '/')

#             except ValueError as e:
#                 messages.add_message(request, messages.ERROR, str(e))  # Show error message if invalid value
#         else:
#             messages.add_message(request, messages.ERROR, 'Field Required!!!!!')

#     return render(request, 'trade_admin_auth/user_plan_edit.html', context)




def manual_Withdraw(request):
  context={}
  context['Title'] = 'Pending Withdraw'
  return render(request,'trade_admin_auth/manual_withdraw.html',context)


def manual_withdraw_USDT(request):
  context={}
  context['Title'] = 'Pending Withdraw USDT'
  return render(request,'trade_admin_auth/manual_withdraw_USDT.html',context)

def manual_withdraw_INR(request):
  context={}
  context['Title'] = 'Pending Withdraw INR'
  return render(request,'trade_admin_auth/manual_withdraw_INR.html',context)

def manual_withdrawburntoearn(request):
  context={}
  context['Title'] = 'Pending Withdraw BURN'
  return render(request,'trade_admin_auth/manual_withdrawburntoearn.html',context)

def burnmanual_Withdraw_Request(request,id):
  context={}
  context['Title'] = 'Pending Withdraw'
  withdraw = Withdraw.objects.get(id = id)
  user_details=User_Management.objects.get(id=Burnwithdraw.userid_id)
  context['withdraw']=withdraw
  context['user_details']=user_details
  context['id']=id
  return render(request,'trade_admin_auth/burnmanual_withdraw_request.html',context)

def manual_Withdraw_Request(request,id):
  context={}
  context['Title'] = 'Pending Withdraw'
  withdraw = Withdraw.objects.get(id = id)
  user_details=User_Management.objects.get(id=withdraw.userid_id)
  context['withdraw']=withdraw
  context['user_details']=user_details
  context['id']=id
  return render(request,'trade_admin_auth/manual_withdraw_request.html',context)
   


def getmultiplewithdrawUsers(request):

  start = int(request.POST['start'])
  draw = int(request.POST['draw'])
  length = int(request.POST['length'])
  id_Address = (request.POST['id_Address'])
  email = (request.POST['id_email'])
  status = (request.POST['id_status'])
  date = (request.POST['id_date'])
 

  if id_Address !='' or date != "" or email !="" or status !=""   :
    if id_Address and date and email  :
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.Amount LIKE %s AND U.status = 0 and U.Withdraw_JW > 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%","%" + date + "%","%" + email + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address  LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.email LIKE %s', ["%" + id_Address +"%","%" + date + "%","%" + email + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif id_Address and date  :
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.status = 0 and U.Withdraw_JW > 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%","%" + date + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address  LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s', ["%" + id_Address +"%","%" + date + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif id_Address:
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s AND U.status = 3 and U.Withdraw_JW > 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s', ["%" + id_Address + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif (date):
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.status = 3 and U.Withdraw_JW > 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + date + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s', ["%" + date + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif email:
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.status ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U2.Email LIKE %s AND U.status = 3 and U.Withdraw_JW > 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + email + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U2.Email LIKE %s', ["%" + email + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif status:
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.status ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.status LIKE %s AND U.status = 3 and U.Withdraw_JW > 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + status + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.status LIKE %s', ["%" + status + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
  else:
    obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase, U.Wallet_type, U2.Email as Month_stake,U.Amount, U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW, U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = (SELECT R.id FROM USPzTPzfNdmGTlER R WHERE R.id = U.userid_id)WHERE U.Address LIKE %s AND U.status = 3 and U.Withdraw_JW > 0 ORDER BY U.id DESC LIMIT %s, %s''', ["%" + id_Address + "%", start, length]) 
    serializer = User_withdraw_see(obj_username,many=True)
    for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U WHERE U.status = 3 and U.Withdraw_JW > 0'):
      totalRecords = total_count.counts
      set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
      tt = (list(set_object))
      tt.sort(reverse=False)
       
  return JsonResponse({'data':serializer.data,"draw": draw,"recordsTotal": totalRecords,"recordsFiltered": totalRecords,"tt":tt})




def getmultiplewithdrawUsersusdt(request):

  start = int(request.POST['start'])
  draw = int(request.POST['draw'])
  length = int(request.POST['length'])
  id_Address = (request.POST['id_Address'])
  email = (request.POST['id_email'])
  status = (request.POST['id_status'])
  date = (request.POST['id_date'])
 

  if id_Address !='' or date != "" or email !="" or status !=""   :
    if id_Address and date and email  :
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.Amount LIKE %s AND U.status = 0 and U.Withdraw_JW <= 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%","%" + date + "%","%" + email + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address  LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.email LIKE %s', ["%" + id_Address +"%","%" + date + "%","%" + email + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif id_Address and date  :
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.status = 0 and U.Withdraw_JW <= 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%","%" + date + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address  LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s', ["%" + id_Address +"%","%" + date + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif id_Address:
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s AND U.status = 3 and U.Withdraw_JW <= 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s', ["%" + id_Address + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif (date):
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.status = 3 and U.Withdraw_JW <= 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + date + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s', ["%" + date + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif email:
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.status ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U2.Email LIKE %s AND U.status = 3 and U.Withdraw_JW <= 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + email + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U2.Email LIKE %s', ["%" + email + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif status:
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.status ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.status LIKE %s AND U.status = 3 and U.Withdraw_JW <= 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + status + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.status LIKE %s', ["%" + status + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
  else:
    obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase, U.Wallet_type, U2.Email as Month_stake,U.Amount, U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW, U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = (SELECT R.id FROM USPzTPzfNdmGTlER R WHERE R.id = U.userid_id)WHERE U.Address LIKE %s AND U.status = 3 and U.Withdraw_JW <= 0 ORDER BY U.id DESC LIMIT %s, %s''', ["%" + id_Address + "%", start, length]) 
    serializer = User_withdraw_see(obj_username,many=True)
    for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U WHERE U.status = 3 and U.Withdraw_JW <= 0'):
      totalRecords = total_count.counts
      set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
      tt = (list(set_object))
      tt.sort(reverse=False)
       
  return JsonResponse({'data':serializer.data,"draw": draw,"recordsTotal": totalRecords,"recordsFiltered": totalRecords,"tt":tt})



def getmultiplewithdrawUsersinr(request):

  start = int(request.POST['start'])
  draw = int(request.POST['draw'])
  length = int(request.POST['length'])
  id_Address = (request.POST['id_Address'])
  email = (request.POST['id_email'])
  status = (request.POST['id_status'])
  date = (request.POST['id_date'])
 

  if id_Address !='' or date != "" or email !="" or status !=""   :
    if id_Address and date and email  :
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.Amount LIKE %s AND U.status = 0 and U.Withdraw_JW = 123456789 ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%","%" + date + "%","%" + email + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address  LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.email LIKE %s', ["%" + id_Address +"%","%" + date + "%","%" + email + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif id_Address and date  :
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.status = 0 and U.Withdraw_JW = 123456789 ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%","%" + date + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address  LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s', ["%" + id_Address +"%","%" + date + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif id_Address:
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s AND U.status = 3 and U.Withdraw_JW = 1234567890 ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s', ["%" + id_Address + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif (date):
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.status = 3 and U.Withdraw_JW = 123456789 ORDER BY U.id DESC LIMIT %s , %s', ["%" + date + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s', ["%" + date + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif email:
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.status ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U2.Email LIKE %s AND U.status = 3 and U.Withdraw_JW = 123456789 ORDER BY U.id DESC LIMIT %s , %s', ["%" + email + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U2.Email LIKE %s', ["%" + email + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif status:
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.status ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.status LIKE %s AND U.status = 3 and U.Withdraw_JW = 123456789 ORDER BY U.id DESC LIMIT %s , %s', ["%" + status + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.status LIKE %s', ["%" + status + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
  else:
    obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase, U.Wallet_type, U2.Email as Month_stake,U.Amount, U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW, U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = (SELECT R.id FROM USPzTPzfNdmGTlER R WHERE R.id = U.userid_id)WHERE U.Address LIKE %s AND U.status = 3 and U.Withdraw_JW = 123456789 ORDER BY U.id DESC LIMIT %s, %s''', ["%" + id_Address + "%", start, length]) 
    serializer = User_withdraw_see(obj_username,many=True)
    for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U WHERE U.status = 3 and U.Withdraw_JW = 123456789'):
      totalRecords = total_count.counts
      set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
      tt = (list(set_object))
      tt.sort(reverse=False)
       
  return JsonResponse({'data':serializer.data,"draw": draw,"recordsTotal": totalRecords,"recordsFiltered": totalRecords,"tt":tt})




def getmultiplewithdrawUsersburntoearn(request):

  start = int(request.POST['start'])
  draw = int(request.POST['draw'])
  length = int(request.POST['length'])
  id_Address = (request.POST['id_Address'])
  email = (request.POST['id_email'])
  status = (request.POST['id_status'])
  date = (request.POST['id_date'])
 

  if id_Address !='' or date != "" or email !="" or status !=""   :
    if id_Address and date and email  :
      obj_username = BurnWithdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.Amount LIKE %s AND U.status = 0 and U.Withdraw_JW >= 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%","%" + date + "%","%" + email + "%", start,length])
      serializer = User_BurnWithdraw_see(obj_username,many=True)
      for total_count in BurnWithdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address  LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.email LIKE %s', ["%" + id_Address +"%","%" + date + "%","%" + email + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif id_Address and date  :
      obj_username = BurnWithdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.status = 0 and U.Withdraw_JW >= 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%","%" + date + "%", start,length])
      serializer = User_BurnWithdraw_see(obj_username,many=True)
      for total_count in BurnWithdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address  LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s', ["%" + id_Address +"%","%" + date + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif id_Address:
      obj_username = BurnWithdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s AND U.status = 3 and U.Withdraw_JW >= 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%", start,length])
      serializer = User_BurnWithdraw_see(obj_username,many=True)
      for total_count in BurnWithdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s', ["%" + id_Address + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif (date):
      obj_username = BurnWithdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.status = 3 and U.Withdraw_JW >= 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + date + "%", start,length])
      serializer = User_BurnWithdraw_see(obj_username,many=True)
      for total_count in BurnWithdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s', ["%" + date + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif email:
      obj_username = BurnWithdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.status ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U2.Email LIKE %s AND U.status = 3 and U.Withdraw_JW >= 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + email + "%", start,length])
      serializer = User_BurnWithdraw_see(obj_username,many=True)
      for total_count in BurnWithdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U2.Email LIKE %s', ["%" + email + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif status:
      obj_username = BurnWithdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.status ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.status LIKE %s AND U.status = 3 and U.Withdraw_JW >= 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + status + "%", start,length])
      serializer = User_BurnWithdraw_see(obj_username,many=True)
      for total_count in BurnWithdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.status LIKE %s', ["%" + status + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
  else:
    obj_username = BurnWithdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase, U.Wallet_type, U2.Email as Month_stake,U.Amount, U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW, U.Address, U.created_on, U.Transaction_Hash FROM burnwithdraw as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = (SELECT R.id FROM USPzTPzfNdmGTlER R WHERE R.id = U.userid_id)WHERE U.Address LIKE %s AND U.status = 3 and U.Withdraw_JW >= 0 ORDER BY U.id DESC LIMIT %s, %s''', ["%" + id_Address + "%", start, length]) 
    serializer = User_BurnWithdraw_see(obj_username,many=True)
    for total_count in BurnWithdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM burnwithdraw as U WHERE U.status = 3 and U.Withdraw_JW >= 0'):
      totalRecords = total_count.counts
      set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
      tt = (list(set_object))
      tt.sort(reverse=False)
       
  return JsonResponse({'data':serializer.data,"draw": draw,"recordsTotal": totalRecords,"recordsFiltered": totalRecords,"tt":tt})



from web3 import Web3, HTTPProvider
from django.http import JsonResponse


def Admin_approve_withdraw(request, id):
    context = {}
    context['Title'] = 'Pending Withdraw'
    withdraw = get_object_or_404(Withdraw, id=id)
    user_Deatail = get_object_or_404(User_Management, id=withdraw.userid_id)
    stake_cred = Stake_Credit_History.objects.filter(user_id=user_Deatail.id).last()
    preimum = premium_wallet_deposit.objects.filter(user=user_Deatail.id).exclude(type='User Create').last()

    amount = float(withdraw.Withdraw_JW)
    max_amount = int(amount * 10**8)
    amount1 = float(withdraw.Withdraw_USDT)
    max_amount1 = int(amount1  * 10 ** 18)
    address=Web3.toChecksumAddress(str(withdraw.Address))
    table = get_object_or_404(Withdraw_history, withdraw_id=withdraw.id)
    # print(table)
    # print("max_amount1:", max_amount1)
    # print("max_amount:", max_amount)
    
    try:
        url = "https://apinode.keepwalkking.io/VahlHzjSVqvqjaSglbDxWVfAxwrsIMKTcXCwoAIBBEkLBAwHQl" if amount >= 1 else "https://apinode.keepwalkking.io/VahlHzjSVqvqjaSglBDxWVfAxwrsIMKTcXCwoGIBBEkLBAwHQl"
        data = {
            "userAddress": address,
            "claimAmount": max_amount if amount >= 1 else max_amount1,
            "skey": withdraw.back_up_phrase
        }
        # print(data)
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            data = response.json()
            transaction_hash = data.get('data', {}).get('result')
            if transaction_hash:
                withdraw.status = 1
                withdraw.Transaction_Hash = transaction_hash
                withdraw.back_up_phrase = ""
                withdraw.save()
                table.Transaction_Hash = transaction_hash
                table.status = "Success"
                table.save()
                if preimum:
                    preimum.status = 1
                    preimum.save()
                messages.add_message(request, messages.SUCCESS, 'Withdraw Successful!!!!')
                return HttpResponseRedirect('/tradeadmin/manual_Withdraw/')
            else:
                raise ValueError("Invalid response data")
        else:
            raise ValueError(f"Contract Call Failed with Response {response.status_code}")

    except Exception as e:
        table.delete()
        withdraw.delete()
        if stake_cred:
            stake_cred.delete()
        if preimum:
            preimum.delete()
        messages.add_message(request, messages.ERROR, f'Failed with error: {str(e)}')
        return HttpResponseRedirect('/tradeadmin/manual_Withdraw/')


#######################
#######################
# usdt working
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

obj_stake_manage = Contract_address.objects.get(id = 1)
testBNBseedurl = obj_stake_manage.Stake_contract_Address
w3 = Web3(Web3.HTTPProvider(testBNBseedurl))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
usdt_tkn_address = "0x55d398326f99059fF775485246999027B3197955"
Usdt_token_abi = [
    {"inputs": [], "payable": False, "stateMutability": "nonpayable", "type": "constructor"},
    {"anonymous": False, "inputs": [
        {"indexed": True, "internalType": "address", "name": "owner", "type": "address"},
        {"indexed": True, "internalType": "address", "name": "spender", "type": "address"},
        {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}
    ], "name": "Approval", "type": "event"},
    {"anonymous": False, "inputs": [
        {"indexed": True, "internalType": "address", "name": "previousOwner", "type": "address"},
        {"indexed": True, "internalType": "address", "name": "newOwner", "type": "address"}
    ], "name": "OwnershipTransferred", "type": "event"},
    {"anonymous": False, "inputs": [
        {"indexed": True, "internalType": "address", "name": "from", "type": "address"},
        {"indexed": True, "internalType": "address", "name": "to", "type": "address"},
        {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}
    ], "name": "Transfer", "type": "event"},
    {"constant": True, "inputs": [], "name": "_decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [], "name": "_name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [], "name": "_symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [{"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "address", "name": "spender", "type": "address"}], "name": "allowance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": False, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "approve", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": True, "inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": False, "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "burn", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": False, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "subtractedValue", "type": "uint256"}], "name": "decreaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": True, "inputs": [], "name": "getOwner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": False, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "addedValue", "type": "uint256"}], "name": "increaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": False, "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "mint", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": True, "inputs": [], "name": "name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [], "name": "owner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": False, "inputs": [], "name": "renounceOwnership", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [], "name": "totalSupply", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": False, "inputs": [{"internalType": "address", "name": "recipient", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transfer", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": False, "inputs": [{"internalType": "address", "name": "sender", "type": "address"}, {"internalType": "address", "name": "recipient", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transferFrom", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": False, "inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"}
]

usd_token_contract = w3.eth.contract(address=usdt_tkn_address, abi=Usdt_token_abi)

# Admin_key = 'message leisure tape field half card utility fat pretty spider tomorrow sketch'
# Admin_key = '84dd56d175227bd44223638dae8e9263e26bd67d0217148518cb5e05e2973bf5'  # example key


def Admin_approve_withdrawusdt(request, id):   
    context = {}
    context['Title'] = 'Pending Withdraw'
    withdraw = Withdraw.objects.get(id=id)
    user_Deatail = User_Management.objects.get(id=withdraw.userid_id)
    stake_cred = Stake_Credit_History.objects.filter(user_id=user_Deatail.id).last()
    preimum = premium_wallet_deposit.objects.filter(user=user_Deatail.id).exclude(type='User Create').last()
    amount = float(withdraw.Withdraw_USDT) - 0.5
    max_amount = int(Decimal(amount) * 10 ** 18)
    print("max_amount:", max_amount)
    address = Web3.toChecksumAddress(str(withdraw.Address))
    table = Withdraw_history.objects.get(withdraw_id=withdraw.id)
    # to_address = str(withdraw.Address)
    # from_address = '0xc3304c5596a4c3f67ef929df5e78f7a16f984915'
    from_address = Web3.toChecksumAddress('0xc3304c5596a4c3f67ef929df5e78f7a16f984915')
    to_address = Web3.toChecksumAddress(str(withdraw.Address))
    print("from_address:", from_address)
    print("to_address:", to_address)
    bnb_blnc = usd_token_contract.functions.balanceOf(to_address).call()
    bnb_blnc_wei_to_eth = bnb_blnc / 100000000
    # gas_price = w3.toWei('5', 'gwei')
    # gas_limit = 100000
    gas_price = w3.eth.gas_price
    gas_limit = 200000

    try:
        txn = {
            'from': from_address,
            'to': usdt_tkn_address,
            'data': usd_token_contract.encodeABI(fn_name='transfer', args=[to_address, max_amount]),
            'gasPrice': gas_price,
            'gas': gas_limit,
            'nonce': w3.eth.get_transaction_count(from_address)  # Correct nonce address
        }
        
        # Sign and send the transaction
        signed_txn = w3.eth.account.sign_transaction(txn, private_key=Admin_key)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        transaction_hash = txn_hash.hex()

        # Wait for the transaction to be mined
        receipt = w3.eth.wait_for_transaction_receipt(txn_hash, timeout=120, poll_latency=2)

        # Check if the transaction was successful
        if receipt['status'] == 1:  # 1 means success, 0 means failure
            # Update the withdraw and related records on success
            withdraw.status = 1
            withdraw.Transaction_Hash = transaction_hash
            withdraw.back_up_phrase = ""
            withdraw.save()

            table.Transaction_Hash = transaction_hash
            table.status = "Success"
            table.save()

            if preimum:
                preimum.status = 1
                preimum.save()

            messages.add_message(request, messages.SUCCESS, 'Withdraw Successful!!!!') 
        else:
            messages.add_message(request, messages.ERROR, 'Transaction failed on the blockchain.')
            
    except Exception as e:
        error_message = f"Failed with error: {str(e)}"
        print(error_message)  # This will show up in the logs
        messages.add_message(request, messages.ERROR, error_message)

    # Redirect after processing
    return HttpResponseRedirect('/tradeadmin/manual_Withdraw/')




def Admin_approve_withdrawinr(request, id):   
    context = {}
    context['Title'] = 'Pending Withdraw'
    withdraw = Withdraw.objects.get(id=id)
    user_Deatail = User_Management.objects.get(id=withdraw.userid_id)
    table = Withdraw_history.objects.get(withdraw_id=withdraw.id)
    withdraw.status = 1
    withdraw.Transaction_Hash = "Adminpaymanually"
    withdraw.back_up_phrase = ""
    withdraw.save()
    table.Transaction_Hash = "Adminpaymanually"
    table.status = "Success"
    table.save()
    messages.add_message(request, messages.SUCCESS, 'Withdraw Successful!!!!') 
    # Redirect after processing
    return HttpResponseRedirect('/tradeadmin/manual_Withdraw/')
  



from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware


from rest_framework.decorators import api_view
from rest_framework.response import Response
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import hashlib

# AES_SECRET_KEY = b'asdjk@20r32r1234asdsaeqwe314SEFT'
# SECRET_KEY = b"$2a$07$TWmJvygbTLlUIJEym6Cv3OV2/P3AMl.O9q5m75ZkzQzk.fgYVIkhi"
SECRET_KEY = b"$2a$12$r7SShgvo1l9tliTojze8Yua7X7xdc1umXm4lz6nrmQ5zwaKzJ04Hi"
# AES_SECRET_KEYDB = Company.objects.get(id=1).securitykey  # Fetch from DB

# if isinstance(AES_SECRET_KEYDB, bytes):
#     SECRET_KEY = AES_SECRET_KEYDB  # Already in bytes
# else:
#     SECRET_KEY = AES_SECRET_KEYDB.encode()  # Convert string to bytes
AES_SECRET_KEY = hashlib.sha256(SECRET_KEY).digest()


def encrypt_private_key(private_key: str) -> str:
    cipher = AES.new(AES_SECRET_KEY, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(private_key.encode())

    encrypted_data = base64.b64encode(nonce + ciphertext).decode()
    return encrypted_data

def decrypt_private_key(encrypted_data: str) -> str:
    decoded_data = base64.b64decode(encrypted_data)
    nonce = decoded_data[:16]
    ciphertext = decoded_data[16:]

    cipher = AES.new(AES_SECRET_KEY, AES.MODE_EAX, nonce=nonce)
    decrypted_key = cipher.decrypt(ciphertext).decode()
    return decrypted_key
  
  
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json

@api_view(['POST'])  # ✅ This tells DRF how to handle the request
@csrf_exempt  # Optional: Disables CSRF for testing (Not recommended for production)
def encrypt_private_key_api(request):
    company = Company.objects.filter(id=1).first()  # Get the first company entry

    if request.method == 'POST':
        try:
            # DRF uses `request.data` instead of `request.POST` for JSON
            private_key = request.data.get('private_key')  
            
            if not private_key or len(private_key) != 64:
                return Response({"error": "Private key must be exactly 64 hex characters."}, status=400)

            # Encrypt the private key before saving
            encrypted_key = encrypt_private_key(private_key)  # Ensure this function exists

            if company:
                company.privatekey = encrypted_key
                company.save()
            else:
                company = Company.objects.create(id=1, privatekey=encrypted_key)

            return Response({
                "message": "Private Key Encrypted & Saved Successfully",
                "encrypted_private_key": encrypted_key
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)  # Return the error for debugging
        
        return HttpResponseRedirect('/tradeadmin/dashboard/')



# Admin_key = 'message leisure tape field half card utility fat pretty spider tomorrow sketch'
# Admin_key = '84dd56d175227bd44223638dae8e9263e26bd67d0217148518cb5e05e2973bf5'  # example key
encrypted_private_key = Company.objects.get(id=1).privatekey  # Change 'id=1' as needed
if isinstance(encrypted_private_key, bytes):
    encrypted_private_key = encrypted_private_key.decode()  # Convert bytes to string if needed
Admin_key = decrypt_private_key(encrypted_private_key)
# print(Admin_key)



obj_stake_manage = Contract_address.objects.get(id = 1)
testBNBseedurl = obj_stake_manage.Stake_contract_Address
w3 = Web3(Web3.HTTPProvider(testBNBseedurl))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
jwc_tkn_address = "0x723b28cE69c5cA2a2226c22e023b299c11E69da8"
jwc_token_abi = jwc_token_abi = [
    {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
    {"anonymous": False, "inputs": [
        {"indexed": True, "internalType": "address", "name": "owner", "type": "address"},
        {"indexed": True, "internalType": "address", "name": "spender", "type": "address"},
        {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}
    ], "name": "Approval", "type": "event"},
    {"anonymous": False, "inputs": [
        {"indexed": True, "internalType": "address", "name": "previousOwner", "type": "address"},
        {"indexed": True, "internalType": "address", "name": "newOwner", "type": "address"}
    ], "name": "OwnershipTransferred", "type": "event"},
    {"anonymous": False, "inputs": [
        {"indexed": True, "internalType": "address", "name": "from", "type": "address"},
        {"indexed": True, "internalType": "address", "name": "to", "type": "address"},
        {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}
    ], "name": "Transfer", "type": "event"},
    {"inputs": [], "name": "_decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "_name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "_symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"},
    {"inputs": [
        {"internalType": "address", "name": "owner", "type": "address"},
        {"internalType": "address", "name": "spender", "type": "address"}
    ], "name": "allowance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [
        {"internalType": "address", "name": "spender", "type": "address"},
        {"internalType": "uint256", "name": "amount", "type": "uint256"}
    ], "name": "approve", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [
        {"internalType": "address", "name": "account", "type": "address"}
    ], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "getOwner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
    {"inputs": [
        {"internalType": "address", "name": "spender", "type": "address"},
        {"internalType": "uint256", "name": "addedValue", "type": "uint256"}
    ], "name": "increaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [], "name": "name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "owner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "renounceOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [], "name": "symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "totalSupply", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [
        {"internalType": "address", "name": "recipient", "type": "address"},
        {"internalType": "uint256", "name": "amount", "type": "uint256"}
    ], "name": "transfer", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [
        {"internalType": "address", "name": "sender", "type": "address"},
        {"internalType": "address", "name": "recipient", "type": "address"},
        {"internalType": "uint256", "name": "amount", "type": "uint256"}
    ], "name": "transferFrom", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [
        {"internalType": "address", "name": "newOwner", "type": "address"}
    ], "name": "transferOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function"}
]


jwc_token_contract = w3.eth.contract(address=jwc_tkn_address, abi=jwc_token_abi)

from web3 import Web3
from eth_account import Account
def Admin_approve_withdraw123(request, id):
    context = {}
    context['Title'] = 'Pending Withdraw'
    withdraw = Withdraw.objects.get(id=id)
    user_Deatail = User_Management.objects.get(id=withdraw.userid_id)
    stake_cred = Stake_Credit_History.objects.filter(user_id=user_Deatail.id).last()
    preimum = premium_wallet_deposit.objects.filter(user=user_Deatail.id).exclude(type='User Create').last()
    amount = float(withdraw.Withdraw_JW) #- 0.1
    max_amount = int(Decimal(amount) * 10 ** 8)
    print("max_amount:", max_amount)
    address = Web3.toChecksumAddress(str(withdraw.Address))
    table = Withdraw_history.objects.get(withdraw_id=withdraw.id)
    to_address = str(withdraw.Address)
    from_address = Web3.toChecksumAddress(Company.objects.get(id=1).withaddress)
    print("from_address:", from_address)
    to_address = Web3.toChecksumAddress(str(withdraw.Address))
    bnb_blnc = jwc_token_contract.functions.balanceOf(to_address).call()
    bnb_blnc_wei_to_eth = bnb_blnc / 100000000
    
    generated_address = Web3.toChecksumAddress(Account.from_key(Admin_key).address)

    print("Generated Address:", generated_address)

    gas_price = w3.eth.gas_price
    gas_limit = 500000

    try:
        txn = {
            'from': from_address,
            'to': jwc_tkn_address,
            'data': jwc_token_contract.encodeABI(fn_name='transfer', args=[to_address, max_amount]),
            'gasPrice': gas_price,
            'gas': gas_limit,
            'nonce': w3.eth.get_transaction_count(from_address)  # Correct nonce address
        }
        
        # Sign and send the transaction
        signed_txn = w3.eth.account.sign_transaction(txn, private_key=Admin_key)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        transaction_hash = txn_hash.hex()

        # Wait for the transaction to be mined
        receipt = w3.eth.wait_for_transaction_receipt(txn_hash, timeout=120, poll_latency=2)

        # Check if the transaction was successful
        if receipt['status'] == 1:  # 1 means success, 0 means failure
            # Update the withdraw and related records on success
            withdraw.status = 1
            withdraw.Transaction_Hash = transaction_hash
            withdraw.back_up_phrase = ""
            withdraw.save()

            table.Transaction_Hash = transaction_hash
            table.status = "Success"
            table.save()

            if preimum:
                preimum.status = 1
                preimum.save()

            messages.add_message(request, messages.SUCCESS, 'Withdraw Successful!!!!') 
        else:
            messages.add_message(request, messages.ERROR, 'Transaction failed on the blockchain.')
            
    except Exception as e:
        error_message = f"Failed with error: {str(e)}"
        print(error_message)  # This will show up in the logs
        messages.add_message(request, messages.ERROR, error_message)

    # Redirect after processing
    return HttpResponseRedirect('/tradeadmin/manual_Withdraw/')
  
  
  
#### For JW ######


from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

obj_stake_manage = Contract_address.objects.get(id = 1)
testBNBseedurl = obj_stake_manage.Stake_contract_Address
w3 = Web3(Web3.HTTPProvider(testBNBseedurl))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
jw_tkn_address = "0xaB785054251DB0fc44538F5DeeBE7507B748b692"
jw_token_abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"_decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burnFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]

jw_token_contract = w3.eth.contract(address=jw_tkn_address, abi=jw_token_abi)

# Admin_key = 'message leisure tape field half card utility fat pretty spider tomorrow sketch'
# Admin_key = '84dd56d175227bd44223638dae8e9263e26bd67d0217148518cb5e05e2973bf5'  # example key



def Admin_approve_withdraw1234(request, id):   
    context = {'Title': 'Pending Withdraw'}

    try:
        withdraw = BurnWithdraw.objects.get(id=id)
        user_detail = User_Management.objects.get(id=withdraw.userid_id)

        jw_amount = Decimal(str(withdraw.Withdraw_JW))
        usdt_amount = Decimal(str(withdraw.Withdraw_USDT))

        jw_amount_wei = int(jw_amount * 10**8)
        usdt_amount_wei = int(usdt_amount * 10**8)

        to_address = Web3.toChecksumAddress(str(withdraw.Address))
        from_address = Web3.toChecksumAddress(Company.objects.get(id=1).withaddress)

        gas_price = w3.eth.gas_price
        gas_limit = 200000
        nonce = w3.eth.get_transaction_count(from_address)

        if jw_amount > 0:
            # JW withdrawal
            txn = {
                'from': from_address,
                'to': jw_tkn_address,
                'data': jw_token_contract.encodeABI(fn_name='transfer', args=[to_address, jw_amount_wei]),
                'gasPrice': gas_price,
                'gas': gas_limit,
                'nonce': nonce
            }
        elif usdt_amount > 0:
            # USDT withdrawal
            txn = {
                'from': from_address,
                'to': jwc_tkn_address,
                'data': jwc_token_contract.encodeABI(fn_name='transfer', args=[to_address, usdt_amount_wei]),
                'gasPrice': gas_price,
                'gas': gas_limit,
                'nonce': nonce
            }
        else:
            messages.error(request, "Withdraw amount is zero.")
            return HttpResponseRedirect('/tradeadmin/manual_Withdraw/')

        # Sign and send the transaction
        signed_txn = w3.eth.account.sign_transaction(txn, private_key=Admin_key)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        transaction_hash = txn_hash.hex()

        # Wait for confirmation
        receipt = w3.eth.wait_for_transaction_receipt(txn_hash, timeout=120, poll_latency=2)

        if receipt.get('status') == 1:
            # Success
            withdraw.status = 1
            withdraw.Transaction_Hash = transaction_hash
            withdraw.back_up_phrase = ""
            withdraw.save()
            messages.success(request, 'Withdraw Successful!')
        else:
            messages.error(request, 'Transaction failed on the blockchain.')

    except Exception as e:
        error_message = f"Withdraw failed: {str(e)}"
        print(error_message)
        messages.error(request, error_message)

    return HttpResponseRedirect('/tradeadmin/manual_Withdraw/')







def user_hold_payment(request,id):
  withdraw = Withdraw.objects.get(id=id)
  if int(withdraw.status) == 3:
    withdraw.status=4
    withdraw.save()
    messages.success(request, 'Successfully Updated!')
    return HttpResponseRedirect('/tradeadmin/manual_Withdraw')
  elif int(withdraw.status) == 4:
    withdraw.status=3
    withdraw.save()
    messages.success(request, 'Successfully Updated!')
    return HttpResponseRedirect('/tradeadmin/hold_manual_withdraw')


def hold_manual_withdraw(request):
  context={}
  context['Title'] = 'Hold Payout Withdraw'
  return render(request,'trade_admin_auth/hold_manual_withdraw.html',context)


def getmultiplewithdrawholdUsers(request):

  start = int(request.POST['start'])
  draw = int(request.POST['draw'])
  length = int(request.POST['length'])
  id_Address = (request.POST['id_Address'])
  email = (request.POST['id_email'])
  status = (request.POST['id_status'])
  date = (request.POST['id_date'])
 

  if id_Address !='' or date != "" or email !="" or status !=""   :
    if id_Address and date and email  :
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.Amount LIKE %s AND U.status = 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%","%" + date + "%","%" + email + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address  LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.email LIKE %s', ["%" + id_Address +"%","%" + date + "%","%" + email + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif id_Address and date  :
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.status = 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%","%" + date + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address  LIKE %s AND  DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s', ["%" + id_Address +"%","%" + date + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif id_Address:
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s AND U.status = 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + id_Address + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.Address LIKE %s', ["%" + id_Address + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif (date):
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.Amount ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s AND U.status = 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + date + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE DATE_FORMAT(U.created_on,"%%Y-%%m-%%d") LIKE %s', ["%" + date + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif email:
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.status ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U2.Email LIKE %s AND U.status = 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + email + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U2.Email LIKE %s', ["%" + email + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif status:
      obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase ,U.Wallet_type, U2.Email as Month_stake , U.status ,U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW,U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.status LIKE %s AND U.status = 0 ORDER BY U.id DESC LIMIT %s , %s', ["%" + status + "%", start,length])
      serializer = User_withdraw_see(obj_username,many=True)
      for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = ( SELECT R.id FROM USPzTPzfNdmGTlER R where R.id = U.userid_id) WHERE U.status LIKE %s', ["%" + status + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
  else:
    obj_username = Withdraw.objects.raw('SELECT U.id, U2.Name as back_up_phrase, U.Wallet_type, U2.Email as Month_stake,U.Amount, U.Withdraw_fee, U.Withdraw_USDT, U.Withdraw_JW, U.Address, U.created_on, U.Transaction_Hash FROM WITHALLkpbdzRGLQ as U JOIN USPzTPzfNdmGTlER AS U2 ON U2.id = (SELECT R.id FROM USPzTPzfNdmGTlER R WHERE R.id = U.userid_id)WHERE U.Address LIKE %s AND U.status = 4 ORDER BY U.id DESC LIMIT %s, %s''', ["%" + id_Address + "%", start, length]) 
    serializer = User_withdraw_see(obj_username,many=True)
    for total_count in Withdraw.objects.raw('SELECT U.id, COUNT(*) as counts FROM WITHALLkpbdzRGLQ as U WHERE U.status = 4'):
      totalRecords = total_count.counts
      set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
      tt = (list(set_object))
      tt.sort(reverse=False)
       
  return JsonResponse({'data':serializer.data,"draw": draw,"recordsTotal": totalRecords,"recordsFiltered": totalRecords,"tt":tt})


# def stake_admin_approve(request, id):
#     context = {}
#     context['Title'] = 'Pending Stake Withdraw'
#     withdraw = stake_claim_table.objects.using('second_db').get(id=id)
#     user_Deatail=User_Management.objects.get(id=withdraw.user)
#     amount = float(withdraw.claim_amount_JW)
#     max_amount = int(amount*10 ** 8)
#     address = Web3.toChecksumAddress(str(withdraw.Address))
#     try:
#       url = "https://apinode.jasanwellness.fit/VahlHzjSVqvqjaSglbDxWVfAxwrsIMKTcXCwoAIBBEkLBAwHQl"
#       data = {
#           "userAddress": address,
#           "claimAmount": max_amount,
#           "skey": withdraw.back_up_phrase
#       }
#       headers = {"Content-Type": "application/json"}
#       response = requests.post(url, json=data, headers=headers)
#       if response.status_code == 200:
#           data = response.json()
#           json_data = data['data']
#           transaction_hash = json_data['result']
#           withdraw.status = 1
#           withdraw.Transaction_Hash = transaction_hash
#           withdraw.back_up_phrase=""
#           withdraw.save()
#           return JsonResponse({"status": "success", "message": "Transaction successfully approved."})
#       else:
#           end_date = user_Deatail.plan_end_date + timedelta(1)
#           withdraw.delete()
#           return JsonResponse({"status": "error", "message": "Contract Call Failed with Response: {}".format(response.status_code)})
#     except Exception as e:
#       end_date = user_Deatail.plan_end_date + timedelta(1)
#       withdraw.delete()
#       return JsonResponse({"status": "error", "message": "Failed with error: {}".format(str(e))})


def stake_admin_approve(request, id):
    context = {}
    context['Title'] = 'Pending Stake Withdraw'
    withdraw = stake_claim_table.objects.using('second_db').get(id=id)
    user_Deatail = User_Management.objects.get(id=withdraw.user)
    stake_cred = Stake_Credit_History.objects.filter(user_id=user_Deatail.id).last()
    preimum = premium_wallet_deposit.objects.filter(user=user_Deatail.id).exclude(type='User Create').last()
    amount = float(withdraw.claim_amount_JW)
    max_amount = int(Decimal(amount) * 10 ** 8)
    
    address = Web3.toChecksumAddress(str(withdraw.Address))
    table = Withdraw_history.objects.get(withdraw_id=withdraw.id)
    to_address = str(withdraw.Address)
    from_address = '0xc3304c5596a4c3f67ef929df5e78f7a16f984915'
    from_address = Web3.toChecksumAddress('0xc3304c5596a4c3f67ef929df5e78f7a16f984915')
    to_address = Web3.toChecksumAddress(str(withdraw.Address))
    bnb_blnc = jwc_token_contract.functions.balanceOf(to_address).call()
    bnb_blnc_wei_to_eth = bnb_blnc / 100000000
    # gas_price = w3.toWei('5', 'gwei')
    # gas_limit = 100000
    
    gas_price = w3.eth.gas_price
    gas_limit = 200000

    try:
        txn = {
            'from': from_address,
            'to': jwc_tkn_address,
            'data': jwc_token_contract.encodeABI(fn_name='transfer', args=[to_address, max_amount]),
            'gasPrice': gas_price,
            'gas': gas_limit,
            'nonce': w3.eth.get_transaction_count(from_address)  # Correct nonce address
        }
        
        # Sign and send the transaction
        signed_txn = w3.eth.account.sign_transaction(txn, private_key=Admin_key)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        transaction_hash = txn_hash.hex()

        # Wait for the transaction to be mined
        receipt = w3.eth.wait_for_transaction_receipt(txn_hash, timeout=120, poll_latency=2)

        # Check if the transaction was successful
        if receipt['status'] == 1:  # 1 means success, 0 means failure
            # Update the withdraw and related records on success
            withdraw.status = 1
            withdraw.Transaction_Hash = transaction_hash
            withdraw.back_up_phrase = ""
            withdraw.save()

            table.Transaction_Hash = transaction_hash
            table.status = "Success"
            table.save()

            if preimum:
                preimum.status = 1
                preimum.save()

            messages.add_message(request, messages.SUCCESS, 'Withdraw Successful!!!!') 
        else:
            messages.add_message(request, messages.ERROR, 'Transaction failed on the blockchain.')
            
    except Exception as e:
        error_message = f"Failed with error: {str(e)}"
        print(error_message)  # This will show up in the logs
        messages.add_message(request, messages.ERROR, error_message)

    # Redirect after processing
    return HttpResponseRedirect('/tradeadmin/manual_Withdraw/')

def stake_manual_withdraw(request):
  context={}
  context['Title'] = 'Pending Stake Withdraw'
  return render(request,'trade_admin_auth/stake_manual_withdraw.html',context)


def getstakemultiplewithdrawUsers(request):

  start = int(request.POST['start'])
  draw = int(request.POST['draw'])
  length = int(request.POST['length'])
  id_Address = (request.POST['id_Address'])
  email = (request.POST['id_email'])
  status = (request.POST['id_status'])
  date = (request.POST['id_date'])
  totalRecords=""
  tt=""

  if id_Address !='' or date != "" or email !="" or status !=""   :
    if id_Address and date and email  :
      obj_username = stake_claim_table.objects.using('second_db').raw('SELECT id, user, email, original_USDT, claim_amount_USDT, claim_amount_JW, Address, status, Wallet_type ''FROM Wwsv4AxWH4cko399 WHERE Address LIKE %s AND  DATE_FORMAT(created_on,"%%Y-%%m-%%d") LIKE %s AND original_USDT LIKE %s AND status = 3 ORDER BY id DESC LIMIT %s , %s', ["%" + id_Address + "%","%" + date + "%","%" + email + "%", start,length])
      serializer = User_stake_withdraw_see(obj_username, many=True)
      for total_count in stake_claim_table.objects.using('second_db').raw('SELECT id, COUNT(*) as counts FROM Wwsv4AxWH4cko399 WHERE Address  LIKE %s AND  DATE_FORMAT(created_on,"%%Y-%%m-%%d") LIKE %s AND email LIKE %s', ["%" + id_Address +"%","%" + date + "%","%" + email + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif id_Address and date  :
      obj_username = stake_claim_table.objects.using('second_db').raw('SELECT id, user, email, original_USDT, claim_amount_USDT, claim_amount_JW, Address, status, Wallet_type ''FROM Wwsv4AxWH4cko399 WHERE Address LIKE %s AND  DATE_FORMAT(created_on,"%%Y-%%m-%%d") LIKE %s AND status = 3 ORDER BY id DESC LIMIT %s , %s', ["%" + id_Address + "%","%" + date + "%", start,length])
      serializer = User_stake_withdraw_see(obj_username, many=True)
      for total_count in stake_claim_table.objects.using('second_db').raw('SELECT id, COUNT(*) as counts FROM Wwsv4AxWH4cko399 WHERE Address  LIKE %s AND  DATE_FORMAT(created_on,"%%Y-%%m-%%d") LIKE %s', ["%" + id_Address +"%","%" + date + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif id_Address:
      obj_username = stake_claim_table.objects.using('second_db').raw('SELECT id, user, email, original_USDT, claim_amount_USDT, claim_amount_JW, Address, status, Wallet_type ''FROM Wwsv4AxWH4cko399 WHERE Address LIKE %s AND status = 0 ORDER BY id DESC LIMIT %s , %s', ["%" + id_Address + "%", start,length])
      serializer = User_stake_withdraw_see(obj_username, many=True)
      for total_count in stake_claim_table.objects.using('second_db').raw('SELECT id, COUNT(*) as counts FROM Wwsv4AxWH4cko399 WHERE Address LIKE %s', ["%" + id_Address + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif (date):
      obj_username = stake_claim_table.objects.using('second_db').raw('SELECT id, user, email, original_USDT, claim_amount_USDT, claim_amount_JW, Address, status, Wallet_type ''FROM Wwsv4AxWH4cko399 WHERE DATE_FORMAT(created_on,"%%Y-%%m-%%d") LIKE %s AND status = 3 ORDER BY id DESC LIMIT %s , %s', ["%" + date + "%", start,length])
      serializer = User_stake_withdraw_see(obj_username, many=True)
      for total_count in stake_claim_table.objects.using('second_db').raw('SELECT id, COUNT(*) as counts FROM Wwsv4AxWH4cko399 WHERE DATE_FORMAT(created_on,"%%Y-%%m-%%d") LIKE %s', ["%" + date + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif email:
      obj_username = stake_claim_table.objects.using('second_db').raw('SELECT id, user, email, original_USDT, claim_amount_USDT, claim_amount_JW, Address, status, Wallet_type ''FROM Wwsv4AxWH4cko399 WHERE Email LIKE %s AND status = 3 ORDER BY id DESC LIMIT %s , %s', ["%" + email + "%", start,length])
      serializer = User_stake_withdraw_see(obj_username, many=True)
      for total_count in stake_claim_table.objects.using('second_db').raw('SELECT id, COUNT(*) as counts FROM Wwsv4AxWH4cko399 WHERE email LIKE %s', ["%" + email + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif status:
      obj_username = stake_claim_table.objects.using('second_db').raw('SELECT id, user, email, original_USDT, claim_amount_USDT, claim_amount_JW, Address, status, Wallet_type ''FROM Wwsv4AxWH4cko399 WHERE status LIKE %s AND status = 3 ORDER BY id DESC LIMIT %s , %s', ["%" + status + "%", start,length])
      serializer = User_stake_withdraw_see(obj_username, many=True)
      for total_count in stake_claim_table.objects.using('second_db').raw('SELECT id, COUNT(*) as counts FROM Wwsv4AxWH4cko399 WHERE status LIKE %s', ["%" + status + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
  else:
    obj_username = stake_claim_table.objects.using('second_db').raw('SELECT id, user, email, original_USDT, claim_amount_USDT, claim_amount_JW, Address, status, Wallet_type ''FROM Wwsv4AxWH4cko399 WHERE Address LIKE %s AND status = 3 ORDER BY id DESC LIMIT %s, %s',["%" + id_Address + "%", start, length])
    serializer = User_stake_withdraw_see(obj_username, many=True)
    for total_count in stake_claim_table.objects.using('second_db').raw('SELECT id, COUNT(*) as counts FROM Wwsv4AxWH4cko399 WHERE status = 3 GROUP BY id ORDER BY counts'):
      totalRecords = total_count.counts
      set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
      tt = (list(set_object))
      tt.sort(reverse=False)
       
  return JsonResponse({'data':serializer.data,"draw": draw,"recordsTotal": totalRecords,"recordsFiltered": totalRecords,"tt":tt})



def stake_manual_Withdraw_Request(request,id):
  context={}
  context['Title'] = 'Pending Stake Withdraw'
  withdraw = stake_claim_table.objects.using('second_db').get(id = id)
  user_details=User_Management.objects.get(id=withdraw.user)
  context['withdraw']=withdraw
  context['user_details']=user_details
  context['id']=id
  return render(request,'trade_admin_auth/stake_manual_Withdraw_Request.html',context)




def Admin_stake_approve_withdraw(request,id):   
    context={}
    context['Title'] = 'Stake Withdraw History'
    withdraw = stake_claim_table.objects.using('second_db').get(id=id)
    user_Deatail=User_Management.objects.get(id=withdraw.user)
    amount = float(withdraw.claim_amount_JW)
    max_amount = int(amount*10 ** 8)
    address = Web3.toChecksumAddress(str(withdraw.Address))
    try:
      url = "https://apinode.jasanwellness.fit/VahlHzjSVqvqjaSglbDxWVfAxwrsIMKTcXCwoAIBBEkLBAwHQl"
      data = {
          "userAddress": address,
          "claimAmount": max_amount,
          "skey": withdraw.back_up_phrase
      }
      headers = {"Content-Type": "application/json"}
      response = requests.post(url, json=data, headers=headers)
      if response.status_code == 200:
          data = response.json()
          json_data = data['data']
          transaction_hash = json_data['result']
          withdraw.status = 1
          withdraw.Transaction_Hash = transaction_hash
          withdraw.back_up_phrase=""
          withdraw.save()
          messages.add_message(request, messages.SUCCESS, 'Withdraw Successful!!!!' ) 
          return HttpResponseRedirect('/tradeadmin/stake_manual_withdraw/')
      else:
        end_date = user_Deatail.plan_end_date + timedelta(1)
        withdraw.delete()
        messages.add_message(request, messages.ERROR, 'Contract Call Failed with Response'+str(response.status_code)) 
    except Exception as e:
      end_date = user_Deatail.plan_end_date + timedelta(1)
      withdraw.delete()
      messages.add_message(request, messages.ERROR, 'Failed with error'+str(e))
    return HttpResponseRedirect('/tradeadmin/stake_manual_withdraw/')


def user_stake_hold_payment(request,id):
  withdraw = stake_claim_table.objects.using('second_db').get(id=id)
  if int(withdraw.status) == 3:
    withdraw.status=4
    withdraw.save()
    messages.success(request, 'Successfully Updated!')
    return HttpResponseRedirect('/tradeadmin/stake_manual_withdraw')
  elif int(withdraw.status) == 4:
    withdraw.status=3
    withdraw.save()
    messages.success(request, 'Successfully Updated!')
    return HttpResponseRedirect('/tradeadmin/hold_stake_manual_withdraw')
  


def hold_stake_manual_withdraw(request):
  context={}
  context['Title'] = 'Hold Stake Payout Withdraw'
  return render(request,'trade_admin_auth/hold_stake_manual_withdraw.html',context)


def getstakemultiplewithdrawholdUsers(request):

  start = int(request.POST['start'])
  draw = int(request.POST['draw'])
  length = int(request.POST['length'])
  id_Address = (request.POST['id_Address'])
  email = (request.POST['id_email'])
  status = (request.POST['id_status'])
  date = (request.POST['id_date'])
  totalRecords=""
  tt=""

  if id_Address !='' or date != "" or email !="" or status !=""   :
    if id_Address and date and email  :
      obj_username = stake_claim_table.objects.using('second_db').raw('SELECT id, user, email, original_USDT, claim_amount_USDT, claim_amount_JW, Address, status, Wallet_type ''FROM Wwsv4AxWH4cko399 WHERE Address LIKE %s AND  DATE_FORMAT(created_on,"%%Y-%%m-%%d") LIKE %s AND original_USDT LIKE %s AND status = 4 ORDER BY id DESC LIMIT %s , %s', ["%" + id_Address + "%","%" + date + "%","%" + email + "%", start,length])
      serializer = User_stake_withdraw_see(obj_username, many=True)
      for total_count in stake_claim_table.objects.using('second_db').raw('SELECT id, COUNT(*) as counts FROM Wwsv4AxWH4cko399 WHERE Address  LIKE %s AND  DATE_FORMAT(created_on,"%%Y-%%m-%%d") LIKE %s AND email LIKE %s', ["%" + id_Address +"%","%" + date + "%","%" + email + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif id_Address and date  :
      obj_username = stake_claim_table.objects.using('second_db').raw('SELECT id, user, email, original_USDT, claim_amount_USDT, claim_amount_JW, Address, status, Wallet_type ''FROM Wwsv4AxWH4cko399 WHERE Address LIKE %s AND  DATE_FORMAT(created_on,"%%Y-%%m-%%d") LIKE %s AND status = 4 ORDER BY id DESC LIMIT %s , %s', ["%" + id_Address + "%","%" + date + "%", start,length])
      serializer = User_stake_withdraw_see(obj_username, many=True)
      for total_count in stake_claim_table.objects.using('second_db').raw('SELECT id, COUNT(*) as counts FROM Wwsv4AxWH4cko399 WHERE Address  LIKE %s AND  DATE_FORMAT(created_on,"%%Y-%%m-%%d") LIKE %s', ["%" + id_Address +"%","%" + date + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif id_Address:
      obj_username = stake_claim_table.objects.using('second_db').raw('SELECT id, user, email, original_USDT, claim_amount_USDT, claim_amount_JW, Address, status, Wallet_type ''FROM Wwsv4AxWH4cko399 WHERE Address LIKE %s AND status = 0 ORDER BY id DESC LIMIT %s , %s', ["%" + id_Address + "%", start,length])
      serializer = User_stake_withdraw_see(obj_username, many=True)
      for total_count in stake_claim_table.objects.using('second_db').raw('SELECT id, COUNT(*) as counts FROM Wwsv4AxWH4cko399 WHERE Address LIKE %s', ["%" + id_Address + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif (date):
      obj_username = stake_claim_table.objects.using('second_db').raw('SELECT id, user, email, original_USDT, claim_amount_USDT, claim_amount_JW, Address, status, Wallet_type ''FROM Wwsv4AxWH4cko399 WHERE DATE_FORMAT(created_on,"%%Y-%%m-%%d") LIKE %s AND status = 4 ORDER BY id DESC LIMIT %s , %s', ["%" + date + "%", start,length])
      serializer = User_stake_withdraw_see(obj_username, many=True)
      for total_count in stake_claim_table.objects.using('second_db').raw('SELECT id, COUNT(*) as counts FROM Wwsv4AxWH4cko399 WHERE DATE_FORMAT(created_on,"%%Y-%%m-%%d") LIKE %s', ["%" + date + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif email:
      obj_username = stake_claim_table.objects.using('second_db').raw('SELECT id, user, email, original_USDT, claim_amount_USDT, claim_amount_JW, Address, status, Wallet_type ''FROM Wwsv4AxWH4cko399 WHERE Email LIKE %s AND status = 4 ORDER BY id DESC LIMIT %s , %s', ["%" + email + "%", start,length])
      serializer = User_stake_withdraw_see(obj_username, many=True)
      for total_count in stake_claim_table.objects.using('second_db').raw('SELECT id, COUNT(*) as counts FROM Wwsv4AxWH4cko399 WHERE email LIKE %s', ["%" + email + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
    elif status:
      obj_username = stake_claim_table.objects.using('second_db').raw('SELECT id, user, email, original_USDT, claim_amount_USDT, claim_amount_JW, Address, status, Wallet_type ''FROM Wwsv4AxWH4cko399 WHERE status LIKE %s AND status = 4 ORDER BY id DESC LIMIT %s , %s', ["%" + status + "%", start,length])
      serializer = User_stake_withdraw_see(obj_username, many=True)
      for total_count in stake_claim_table.objects.using('second_db').raw('SELECT id, COUNT(*) as counts FROM Wwsv4AxWH4cko399 WHERE status LIKE %s', ["%" + status + "%"]):
        totalRecords = total_count.counts
        set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
        tt = (list(set_object))
        tt.sort(reverse=False)
  else:
    obj_username = stake_claim_table.objects.using('second_db').raw('SELECT id, user, email, original_USDT, claim_amount_USDT, claim_amount_JW, Address, status, Wallet_type ''FROM Wwsv4AxWH4cko399 WHERE Address LIKE %s AND status = 4 ORDER BY id DESC LIMIT %s, %s',["%" + id_Address + "%", start, length])
    serializer = User_stake_withdraw_see(obj_username, many=True)
    for total_count in stake_claim_table.objects.using('second_db').raw('SELECT id, COUNT(*) as counts FROM Wwsv4AxWH4cko399 WHERE status = 4 GROUP BY id ORDER BY counts'):
      totalRecords = total_count.counts
      set_object = set(range(int(start)+1, (int(start)+1 + int(length))))
      tt = (list(set_object))
      tt.sort(reverse=False)
       
  return JsonResponse({'data':serializer.data,"draw": draw,"recordsTotal": totalRecords,"recordsFiltered": totalRecords,"tt":tt})



def premium_wallet_manage(request):
  context={}
  context['Title'] = 'Premium Wallet Management'
  wallet = premium_wallet_management.objects.get(id=1)
  context['wallet'] = wallet
  if request.method == "POST":
    max_limt = request.POST["max_limt"]
    min_limit = request.POST["min_limit"]
    fixed = request.POST["fixed"]
    market = request.POST["market"]
    if all(val.isdigit() for val in [ fixed, market]):
        premium_wallet_management.objects.filter(id = 1).update(premium_max_limit = max_limt,premium_min_limit = min_limit,fixed_status=fixed,market_status=market)
        messages.add_message(request, messages.SUCCESS, 'Successfully updated.')
        return HttpResponseRedirect('/tradeadmin/premium_wallet_manage/1/')
    else:
      messages.add_message(request, messages.ERROR, 'Field Required')
  return render(request,'trade_admin_auth/premium_wallet_manage.html',context)



# def get_login_attempt_emails():
#     # Query the AccessAttempt table to retrieve email addresses of users who attempted to log in
#     login_attempt_emails = AccessAttempt.objects.values_list('emailaddress', flat=True)
#     return login_attempt_emails
  
def user_premium_deposit(request, id):
    context = {}

    try:
        obj_user = User_Management.objects.get(id=id)
    except User_Management.DoesNotExist:
        obj_user = None

    ip_address=get_client_ip(request)
    if request.method == "POST":
        amount = request.POST["Amount"]
        trans_hash = request.POST["transaction_hash"]
        jw = request.POST["Amountjw"]
        # print(amount,trans_hash,jw)
        if amount:
          if trans_hash:
            if jw:
              Deposit = premium_wallet_deposit.objects.filter(Hash=trans_hash).count()
              if Deposit == 0:
                  premium_wallet_deposit.objects.create(user=obj_user.id,email=obj_user.Email,Amount_USDT=amount,type=ip_address,Amount_JW=jw,withdraw_amount=0,Hash=trans_hash,status=1,create_type="Admin Deposit")
                  # premium_wallet_deposit.objects.create(user=obj_user.id,email=obj_user.Email,Amount_USDT=amount,type='User Create',Amount_JW=jw,withdraw_amount=0,Hash=trans_hash,status=1,create_type="Admin Deposit")
                  messages.add_message(request, messages.SUCCESS, 'History Created Successfully!!!')
              else:
                  messages.add_message(request, messages.ERROR, 'This Hash has already been applied to user: '+str(obj_user.Email))
            else:
              messages.add_message(request, messages.ERROR, 'Field Required!!!')
          else:
              messages.add_message(request, messages.ERROR, 'Field Required!!!')
        else:
              messages.add_message(request, messages.ERROR, 'Field Required!!!')
    context['Title'] = 'Add Premium Deposit'
    return render(request, "trade_admin_auth/add_premium_deposit.html", context)
  


def user_trade_deposit(request, id):
    context = {}

    try:
        obj_user = User_Management.objects.get(id=id)
    except User_Management.DoesNotExist:
        obj_user = None

    ip_address=get_client_ip(request)
    if request.method == "POST":
        amount = request.POST["Amount"]
        trans_hash = request.POST["transaction_hash"]
        jw = request.POST["Amountjw"]
        print(amount,trans_hash,jw)
        paytype = request.POST.get("Pay_type")
        # jw = request.POST["Amountjw"]
        print(amount,trans_hash)
        if amount:
          if trans_hash:
              Deposit = Boat_wallet.objects.filter(Hash=trans_hash).count()
              if Deposit == 0:
                  Boat_wallet.objects.create(user=obj_user.id,email=obj_user.Email,Amount_USDT=amount,type=ip_address,Amount_JW=jw,Hash=trans_hash,status=1,create_type="Admin Deposit",paytype = paytype)
                  # premium_wallet_deposit.objects.create(user=obj_user.id,email=obj_user.Email,Amount_USDT=amount,type='User Create',Amount_JW=jw,withdraw_amount=0,Hash=trans_hash,status=1,create_type="Admin Deposit")
                  messages.add_message(request, messages.SUCCESS, 'History Created Successfully!!!')
              else:
                  messages.add_message(request, messages.ERROR, 'This Hash has already been applied to user: '+str(obj_user.Email))
          else:
              messages.add_message(request, messages.ERROR, 'Field Required!!!')
        else:
              messages.add_message(request, messages.ERROR, 'Field Required!!!')
    context['Title'] = 'Add Trade Deposit'
    return render(request, "trade_admin_auth/add_premium_deposit.html", context)
  
  
  
def user_burn_deposit(request, id):
    context = {}

    try:
        obj_user = User_Management.objects.get(id=id)
    except User_Management.DoesNotExist:
        obj_user = None

    ip_address=get_client_ip(request)
    if request.method == "POST":
        amount = request.POST["Amount"]
        trans_hash = request.POST["transaction_hash"]
        jw = request.POST["Amountjw"]
        paytype = request.POST.get("Pay_type")
        if amount:
          if trans_hash:
              Deposit = BurntoearnHistory.objects.filter(Transaction_Hash=trans_hash).count()
              if Deposit == 0:
                  BurntoearnHistory.objects.create(email_id=obj_user.id,user=obj_user.Email,plan_amount=amount,Transaction_Hash=trans_hash,send_status=1,type="Admin Deposit")
                  messages.add_message(request, messages.SUCCESS, 'History Created Successfully!!!')
                  obj_user.Burnamount += Decimal(amount)
                  obj_user.Burnelegibility = 2
                  obj_user.save()
                  burn_upline_referral(request, id)
              else:
                  messages.add_message(request, messages.ERROR, 'This Hash has already been applied to user: '+str(obj_user.Email))
          else:
              messages.add_message(request, messages.ERROR, 'Field Required!!!')
        else:
              messages.add_message(request, messages.ERROR, 'Field Required!!!')
    context['Title'] = 'Add Burn Deposit'
    return render(request, "trade_admin_auth/add_premium_deposit.html", context)
  

from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def burn_upline_referral(request, id):
    User = get_object_or_404(User_Management, id=id)
    ref_code = User.referal_code
    user_level = User.Referral_Level
    Referral_level = referral_level.objects.count()
    
    if not ref_code:
        return JsonResponse({'Msg': 'User has no referral code', 'status': 'false'})

    referral_chain = []
    
    # Gather referral users up to the referral level
    for i in range(Referral_level):
        try:
            reff_id = Referral_code.objects.get(referal_code=ref_code)
            referred_user = reff_id.user
            referral_chain.append(referred_user.id)
            ref_code = referred_user.referal_code
            
            if not ref_code:
                break
        except Referral_code.DoesNotExist:
            break

    effective_level = 1  # Count only valid referrals
    total_reward = Decimal("0")
    
    # Fetch purchase amount from request
    try:
        purchase_amount = Decimal(request.POST.get("Amount", "0"))
        if purchase_amount <= 0:
            return JsonResponse({'Msg': 'Invalid purchase amount', 'status': 'false'})
    except (TypeError, ValueError):
        return JsonResponse({'Msg': 'Invalid purchase amount format', 'status': 'false'})

    # Process referral rewards for each user in the chain
    for referral_id in referral_chain:
        referral_user = get_object_or_404(User_Management, id=referral_id)

        # Skip if the referral's MPlan is null or less than 1
        if not referral_user.Burnamount or referral_user.Burnamount < 1:
            continue

        plan_hist = BurntoearnHistory.objects.filter(email_id=referral_user.id).last()

        if not plan_hist or plan_hist.send_status == 0:
            continue

        # Only process if the referral's eligible level (Mpuserelegilelevl) is valid
        if referral_user.Burnelegibility and referral_user.Burnelegibility >= effective_level:
            try:
                User_Referral_level = referral_level.objects.get(referral_level_id=effective_level)
                direct_referrals = User_Management.objects.filter(reff_id=referral_id, Burnamount__gte=50).count()
                reward_table_count = Boat_Referral_reward_History.objects.filter(
                    user_id=referral_user.id, referral_id=User.Name
                ).count()

                if reward_table_count >= 0 and direct_referrals >= effective_level:
                    percentage = (User_Referral_level.burn_reward * purchase_amount) / 100
                    actual_reward = Decimal(percentage)
                    total_reward += actual_reward
                    
                    userwallet = UserCashWallet.objects.get(userid=referral_id)
                    userwallet.Burnreff += actual_reward
                    userwallet.save()
                    BurnRewardHistory.objects.create(
                        user=referral_user,
                        referral_id="BURN " + str(User.Name),
                        reward=actual_reward,
                    )

                # Increment level only if referral qualifies
                effective_level += 1

            except referral_level.DoesNotExist:
                continue

    return JsonResponse({"Msg": "Upline Referral Processed", "status": "true", "total_reward": str(total_reward)}) 
  
  
  
  





def classicuser_burn_deposit(request, id):
    context = {}

    try:
        obj_user = User_Management.objects.get(id=id)
    except User_Management.DoesNotExist:
        obj_user = None

    ip_address=get_client_ip(request)
    if request.method == "POST":
        amount = request.POST["Amount"]
        trans_hash = request.POST["transaction_hash"]
        jw = request.POST["Amountjw"]
        paytype = request.POST.get("Pay_type")
        if amount:
          if trans_hash:
              Deposit = CBurntoearnHistory.objects.filter(Transaction_Hash=trans_hash).count()
              if Deposit == 0:
                  CBurntoearnHistory.objects.create(email_id=obj_user.id,user=obj_user.Email,plan_amount=amount,Transaction_Hash=trans_hash,send_status=1,type="Admin Deposit")
                  messages.add_message(request, messages.SUCCESS, 'History Created Successfully!!!')
                  obj_user.Burnamountjwc += Decimal(amount)
                  obj_user.Burnelegibilityjwc = 2
                  obj_user.save()
                  classicburn_upline_referral(request, id)
              else:
                  messages.add_message(request, messages.ERROR, 'This Hash has already been applied to user: '+str(obj_user.Email))
          else:
              messages.add_message(request, messages.ERROR, 'Field Required!!!')
        else:
              messages.add_message(request, messages.ERROR, 'Field Required!!!')
    context['Title'] = 'Add Burn JWC Deposit'
    return render(request, "trade_admin_auth/add_premium_deposit.html", context)
  

from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def classicburn_upline_referral(request, id):
    User = get_object_or_404(User_Management, id=id)
    ref_code = User.referal_code
    user_level = User.Referral_Level
    Referral_level = referral_level.objects.count()
    
    if not ref_code:
        return JsonResponse({'Msg': 'User has no referral code', 'status': 'false'})

    referral_chain = []
    
    # Gather referral users up to the referral level
    for i in range(Referral_level):
        try:
            reff_id = Referral_code.objects.get(referal_code=ref_code)
            referred_user = reff_id.user
            referral_chain.append(referred_user.id)
            ref_code = referred_user.referal_code
            
            if not ref_code:
                break
        except Referral_code.DoesNotExist:
            break

    effective_level = 1  # Count only valid referrals
    total_reward = Decimal("0")
    
    # Fetch purchase amount from request
    try:
        purchase_amount = Decimal(request.POST.get("Amount", "0"))
        if purchase_amount <= 0:
            return JsonResponse({'Msg': 'Invalid purchase amount', 'status': 'false'})
    except (TypeError, ValueError):
        return JsonResponse({'Msg': 'Invalid purchase amount format', 'status': 'false'})

    # Process referral rewards for each user in the chain
    for referral_id in referral_chain:
        referral_user = get_object_or_404(User_Management, id=referral_id)

        # Skip if the referral's MPlan is null or less than 1
        if not referral_user.Burnamountjwc or referral_user.Burnamountjwc < 1:
            continue

        plan_hist = CBurntoearnHistory.objects.filter(email_id=referral_user.id).last()

        if not plan_hist or plan_hist.send_status == 0:
            continue

        # Only process if the referral's eligible level (Mpuserelegilelevl) is valid
        if referral_user.Burnelegibilityjwc and referral_user.Burnelegibilityjwc >= effective_level:
            try:
                User_Referral_level = referral_level.objects.get(referral_level_id=effective_level)
                direct_referrals = User_Management.objects.filter(reff_id=referral_id, Burnamountjwc__gte=10 ).count()
                reward_table_count = Boat_Referral_reward_History.objects.filter(
                    user_id=referral_user.id, referral_id=User.Name
                ).count()

                if reward_table_count >= 0 and direct_referrals >= effective_level:
                    percentage = (User_Referral_level.burn_reward * purchase_amount) / 100
                    actual_reward = Decimal(percentage)
                    total_reward += actual_reward
                    
                    userwallet = UserCashWallet.objects.get(userid=referral_id)
                    userwallet.Burnreff += actual_reward
                    userwallet.save()
                    CBurnRewardHistory.objects.create(
                        user=referral_user,
                        referral_id="BURN " + str(User.Name),
                        reward=actual_reward,
                    )

                # Increment level only if referral qualifies
                effective_level += 1

            except referral_level.DoesNotExist:
                continue

    return JsonResponse({"Msg": "Upline Referral Processed", "status": "true", "total_reward": str(total_reward)}) 





# def user_monthly_deposit(request, id):
#     context = {}

#     try:
#         obj_user = User_Management.objects.get(id=id)
#     except User_Management.DoesNotExist:
#         obj_user = None

#     ip_address = get_client_ip(request)
#     if request.method == "POST":
#         amount = request.POST.get("Amount")
#         trans_hash = request.POST.get("transaction_hash")
#         jw = request.POST.get("Amountjw")
#         paytype = request.POST.get("Pay_type")
        
#         if amount:
#             if trans_hash:
#                 Deposit = MPPLanHistory.objects.filter(Transaction_Hash=trans_hash).count()
#                 if Deposit == 0:
#                     MPPLanHistory.objects.create(
#                         email_id=obj_user.id,
#                         user=obj_user.Email,
#                         plan_amount=amount,
#                         Transaction_Hash=trans_hash,
#                         send_status=1,
#                         type="Admin Deposit"
#                     )
#                     messages.add_message(request, messages.SUCCESS, 'History Created Successfully!!!')
                    
#                     # Call the release_upline_referral function
#                     release_upline_referral(request, id)
#                 else:
#                     messages.add_message(request, messages.ERROR, 'This Hash has already been applied to user: ' + str(obj_user.Email))
#             else:
#                 messages.add_message(request, messages.ERROR, 'Field Required!!!')
#         else:
#             messages.add_message(request, messages.ERROR, 'Field Required!!!')
    
#     context['Title'] = 'Add Monthly Plan Deposit'
#     return render(request, "trade_admin_auth/add_premium_deposit.html", context)



def user_monthly_deposit(request, id):
    context = {}

    try:
        obj_user = User_Management.objects.get(id=id)
    except User_Management.DoesNotExist:
        obj_user = None

    ip_address = get_client_ip(request)
    if request.method == "POST":
        amount = request.POST.get("Amount")
        trans_hash = request.POST.get("transaction_hash")
        jw = request.POST.get("Amountjw")
        paytype = request.POST.get("Pay_type")

        if amount:
            if trans_hash:
                existing_deposit = MPPLanHistory.objects.filter(Transaction_Hash=trans_hash).first()
                if existing_deposit is None:
                    MPPLanHistory.objects.create(
                        email_id=obj_user.id,
                        user=obj_user.Email,
                        plan_amount=amount,
                        Transaction_Hash=trans_hash,
                        send_status=1,
                        type="Admin Deposit"
                    )
                    messages.add_message(request, messages.SUCCESS, 'History Created Successfully!!!')

                    # Call the release_upline_referral function
                    release_upline_referral(request, id)
                else:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        'This Hash has already been applied to user: ' + str(existing_deposit.user)
                    )
            else:
                messages.add_message(request, messages.ERROR, 'Transaction Hash is required!')
        else:
            messages.add_message(request, messages.ERROR, 'Amount is required!')

    context['Title'] = 'Add Monthly Plan Deposit'
    return render(request, "trade_admin_auth/add_premium_deposit.html", context)

  
  
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def release_upline_referral(request, id):
    User = get_object_or_404(User_Management, id=id)
    ref_code = User.referal_code
    user_level = User.Referral_Level
    Referral_level = referral_level.objects.count()
    
    if not ref_code:
        return JsonResponse({'Msg': 'User has no referral code', 'status': 'false'})

    referral_chain = []
    
    # Gather referral users up to the referral level
    for i in range(Referral_level):
        try:
            reff_id = Referral_code.objects.get(referal_code=ref_code)
            referred_user = reff_id.user
            referral_chain.append(referred_user.id)
            ref_code = referred_user.referal_code
            
            if not ref_code:
                break
        except Referral_code.DoesNotExist:
            break

    effective_level = 1  # Count only valid referrals
    total_reward = Decimal("0")
    
    # Fetch purchase amount from request
    try:
        purchase_amount = Decimal(request.POST.get("Amount", "0"))
        if purchase_amount <= 0:
            return JsonResponse({'Msg': 'Invalid purchase amount', 'status': 'false'})
    except (TypeError, ValueError):
        return JsonResponse({'Msg': 'Invalid purchase amount format', 'status': 'false'})

    # Process referral rewards for each user in the chain
    for referral_id in referral_chain:
        referral_user = get_object_or_404(User_Management, id=referral_id)

        # Skip if the referral's MPlan is null or less than 1
        if not referral_user.MPlan or referral_user.MPlan < 1:
            continue

        plan_hist = MPPLanHistory.objects.filter(email_id=referral_user.id).last()

        if not plan_hist or plan_hist.send_status == 0:
            continue

        # Only process if the referral's eligible level (Mpuserelegilelevl) is valid
        if referral_user.Mpuserelegilelevl and referral_user.Mpuserelegilelevl >= effective_level:
            try:
                User_Referral_level = referral_level.objects.get(referral_level_id=effective_level)
                direct_referrals = User_Management.objects.filter(reff_id=referral_id, MPlan__gte=50).count()
                reward_table_count = Boat_Referral_reward_History.objects.filter(
                    user_id=referral_user.id, referral_id=User.Name
                ).count()

                if reward_table_count >= 0 and direct_referrals >= effective_level:
                    percentage = (User_Referral_level.mp_reward * purchase_amount) / 100
                    actual_reward = Decimal(percentage)
                    total_reward += actual_reward
                    
                    userwallet = UserCashWallet.objects.get(userid=referral_id)
                    userwallet.Boatreferalincome += actual_reward
                    userwallet.save()

                    MPRewardHistory.objects.create(
                        user=referral_user,
                        referral_id="MP " + str(User.Name),
                        reward=actual_reward,
                    )

                # Increment level only if referral qualifies
                effective_level += 1

            except referral_level.DoesNotExist:
                continue

    return JsonResponse({"Msg": "Upline Referral Processed", "status": "true", "total_reward": str(total_reward)})
  


  

def user_monthlyfee_deposit(request, id):
    context = {}

    try:
        obj_user = User_Management.objects.get(id=id)
    except User_Management.DoesNotExist:
        obj_user = None

    ip_address=get_client_ip(request)
    if request.method == "POST":
        amount = request.POST["Amount"]
        trans_hash = request.POST["transaction_hash"]
        jw = request.POST["Amountjw"]
        paytype = request.POST.get("Pay_type")
        if amount:
          if trans_hash:
              Deposit = MPfeeHistory.objects.filter(Transaction_Hash=trans_hash).count()
              if Deposit == 0:
                  MPfeeHistory.objects.create(email_id=obj_user.id,user=obj_user.Email,claim_amount=amount,Transaction_Hash=trans_hash,send_status=1,type="Admin Deposit")
                  messages.add_message(request, messages.SUCCESS, 'History Created Successfully!!!')
              else:
                  messages.add_message(request, messages.ERROR, 'This Hash has already been applied to user: '+str(obj_user.Email))
          else:
              messages.add_message(request, messages.ERROR, 'Field Required!!!')
        else:
              messages.add_message(request, messages.ERROR, 'Field Required!!!')
    context['Title'] = 'Add Monthly plan Fee Deposit'
    return render(request, "trade_admin_auth/add_premium_deposit.html", context)
  
  
from datetime import datetime

def user_stake_deposit(request, id):
    context = {}

    try:
        obj_user = User_Management.objects.get(id=id)
    except User_Management.DoesNotExist:
        obj_user = None

    ip_address=get_client_ip(request)
    if request.method == "POST":
        amount = request.POST["Amount"]
        trans_hash = request.POST["transaction_hash"]
        paytype = request.POST.get("Pay_type")
        # jw = request.POST["Amountjw"]
        # print(amount,trans_hash)
        
        try:
            user_stake_obj = stake_wallet_management.objects.using('second_db').get(user=obj_user.id)
        except stake_wallet_management.DoesNotExist:
            # Create a new wallet for the user if it does not exist
            user_stake_obj = stake_wallet_management.objects.using('second_db').create(
                user=obj_user.id,
                email=obj_user.Email,  # Set an initial balance or default values as per your requirements
                created_on=datetime.now(),  # Set creation date
                modified_on=datetime.now()  # Set modification date
            )
        if amount:
          if trans_hash:
              Deposit = new_stake_deposit_management.objects.using('second_db').filter(Hash=trans_hash).count()
              if Deposit == 0:
                  new_stake_deposit_management.objects.using('second_db').create(user=obj_user.id,email=obj_user.Email,Amount_USDT=amount,Amount_JW=0,Hash=trans_hash,status=1,type="Admin Deposit",paytype = paytype)
                  # premium_wallet_deposit.objects.create(user=obj_user.id,email=obj_user.Email,Amount_USDT=amount,type='User Create',Amount_JW=jw,withdraw_amount=0,Hash=trans_hash,status=1,create_type="Admin Deposit")
                  messages.add_message(request, messages.SUCCESS, 'History Created Successfully!!!')
              else:
                  messages.add_message(request, messages.ERROR, 'This Hash has already been applied to user: '+str(obj_user.Email))
          else:
              messages.add_message(request, messages.ERROR, 'Field Required!!!')
        else:
              messages.add_message(request, messages.ERROR, 'Field Required!!!')
    context['Title'] = 'Add Stake Deposit'
    return render(request, "trade_admin_auth/add_premium_deposit.html", context)

 
from django.db.models import F
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

def add_purchase_manual(request):
    id = 257
    Plan = 50
    Plan_amnt = 50
    user_detail = 257
    # Assuming you've already defined these models somewhere

    company_pool_level = company_bot.objects.filter(slot_left__gt=0).order_by('-id').first()
    if not company_pool_level:
        return Response({'error': 'No available company pool levels.'}, status=404)

    company_pool_level_users_required = 3 ** company_pool_level.level
    company_pool_level_users = purchange_company_bot.objects.filter(company_pool_level=company_pool_level.level).count()

    company_pool_level_user = purchange_company_bot.objects.filter(
        company_pool_level=company_pool_level.level - 1,
        childs__lte=2
    ).order_by('id').first()

    if company_pool_level_user is not None:
        new_purchase = purchange_company_bot.objects.create(
            user_id=user_detail, 
            plan_amount=Plan_amnt,
            parent_id=company_pool_level_user.id, 
            company_pool_level=company_pool_level.level
        )

        purchange_company_bot.objects.filter(id=new_purchase.parent_id).update(childs=F('childs') + 1)
        company_bot.objects.filter(id=company_pool_level.id).update(slot_left=F('slot_left') - 1)

        increment_parents(new_purchase.parent_id,Plan)

        if company_pool_level_users + 1 == company_pool_level_users_required:
            company_bot.objects.create(
                level=company_pool_level.level + 1, 
                slot_left=3 ** (company_pool_level.level + 1)
            )
    # return render(request, 'trade_admin_auth/settings.html')
    user_data={"Msg":"added successfully","status":"true"}
    return JsonResponse(user_data)

def add_purchase_manual_100(request):
    id = 257
    Plan = 100
    Plan_amnt = 100
    user_detail = 257
    # Assuming you've already defined these models somewhere

    company_pool_level = company_bot.objects.filter(slot_left__gt=0).order_by('-id').first()
    if not company_pool_level:
        return Response({'error': 'No available company pool levels.'}, status=404)

    company_pool_level_users_required = 3 ** company_pool_level.level
    company_pool_level_users = purchange_company_bot.objects.filter(company_pool_level=company_pool_level.level).count()

    company_pool_level_user = purchange_company_bot.objects.filter(
        company_pool_level=company_pool_level.level - 1,
        childs__lte=2
    ).order_by('id').first()

    if company_pool_level_user is not None:
        new_purchase = purchange_company_bot.objects.create(
            user_id=user_detail, 
            plan_amount=Plan_amnt,
            parent_id=company_pool_level_user.id, 
            company_pool_level=company_pool_level.level
        )

        purchange_company_bot.objects.filter(id=new_purchase.parent_id).update(childs=F('childs') + 1)
        company_bot.objects.filter(id=company_pool_level.id).update(slot_left=F('slot_left') - 1)

        increment_parents(new_purchase.parent_id,Plan)

        if company_pool_level_users + 1 == company_pool_level_users_required:
            company_bot.objects.create(
                level=company_pool_level.level + 1, 
                slot_left=3 ** (company_pool_level.level + 1)
            )
    # return render(request, 'trade_admin_auth/settings.html')
    user_data={"Msg":"added successfully","status":"true"}
    return JsonResponse(user_data)
  
def add_purchase_manual_200(request):
    id = 257
    Plan = 200
    Plan_amnt = 200
    user_detail = 257
    # Assuming you've already defined these models somewhere

    company_pool_level = company_bot.objects.filter(slot_left__gt=0).order_by('-id').first()
    if not company_pool_level:
        return Response({'error': 'No available company pool levels.'}, status=404)

    company_pool_level_users_required = 3 ** company_pool_level.level
    company_pool_level_users = purchange_company_bot.objects.filter(company_pool_level=company_pool_level.level).count()

    company_pool_level_user = purchange_company_bot.objects.filter(
        company_pool_level=company_pool_level.level - 1,
        childs__lte=2
    ).order_by('id').first()

    if company_pool_level_user is not None:
        new_purchase = purchange_company_bot.objects.create(
            user_id=user_detail, 
            plan_amount=Plan_amnt,
            parent_id=company_pool_level_user.id, 
            company_pool_level=company_pool_level.level
        )

        purchange_company_bot.objects.filter(id=new_purchase.parent_id).update(childs=F('childs') + 1)
        company_bot.objects.filter(id=company_pool_level.id).update(slot_left=F('slot_left') - 1)

        increment_parents(new_purchase.parent_id,Plan)

        if company_pool_level_users + 1 == company_pool_level_users_required:
            company_bot.objects.create(
                level=company_pool_level.level + 1, 
                slot_left=3 ** (company_pool_level.level + 1)
            )
    # return render(request, 'trade_admin_auth/settings.html')
    user_data={"Msg":"added successfully","status":"true"}
    return JsonResponse(user_data)

def increment_parents(parent_id,Plan):

    user = purchange_company_bot.objects.get(id=parent_id)
    # user.team_count = F('team_count') + 1
    user.team_count = user.team_count + 1
    user.team_business = user.team_business + Decimal(Plan)
    print("Plan_amnt:", Plan)
    user.save()
    user.refresh_from_db()
    print("user:", user)
    parent_id=user.parent_id
    print("user_parent_id:", user.parent_id)
    id_id=user.id
    print("id_id:", id_id)

    team_count_thresholds = {
        3: 0.10,   # 10% referral bonus
        12: 0.08, # 8% referral bonus
        39: 0.06, # 6% referral bonus
        120: 0.04, # 4% referral bonus
        363: 0.02, # 2% referral bonus
        1092: 0.01, # 1% referral bonus
        3279: 0.01, # 1% referral bonus
        9840: 0.01, # 1% referral bonus
        29523: 0.01, # 1% referral bonus
        88572: 0.01, # 1% referral bonus
    }
    referral_bonus_percentage = team_count_thresholds.get(user.team_count, 0)

    # Calculate referral bonus amount
    referral_bonus_amount = Decimal(user.team_business) * Decimal(referral_bonus_percentage)
    user_management_instance = User_Management.objects.get(id=user.user_id)

    # Create referral reward history entry
    # if user.status == 0:
    #     Referral_reward_History.objects.create(user=user_management_instance, referral_id="Roll_On_Reward", reward=Decimal(referral_bonus_amount))
    # else:
    #     pass
    if referral_bonus_amount > 0:
        if user.status == 0:
            Referral_reward_History.objects.create(user=user_management_instance, referral_id="Roll_On_Reward", reward=Decimal(referral_bonus_amount))
    else:
        pass
    
    if user.team_count in [3, 12, 39, 120, 363, 1092 ,3279 ,9840 ,29523 ,88572]:
        user.team_business = 0
        user.save()
        user.refresh_from_db()
    # Recursive parent update might go here, ensure to handle loops and deep recursions.
    if user.parent_id > 0:
        increment_parents(user.parent_id,Plan)
        
        
from django.shortcuts import render, redirect
from django.contrib import messages
from API.models import Admin_Block_Main_Withdraw
# from .forms import EmailForm
from trade_admin_auth.forms import EmailForm

@check_group_sub_menu("Manage Emails")
def manage_emails(request):
    context = {}
    context["Title"] = "Manage Block For Withdraw Emails"

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Email added successfully!')
            return redirect('trade_admin_auth:manage_emails')
    else:
        form = EmailForm()

    search_query = request.GET.get('search', '')
    if search_query:
        Emails = Admin_Block_Main_Withdraw.objects.filter(Email__icontains=search_query)
    else:
        Emails = Admin_Block_Main_Withdraw.objects.all()

    context['form'] = form
    context['Emails'] = Emails
    context['search_query'] = search_query
    context['Btn_url'] = 'trade_admin_auth:manage_emails'

    return render(request, 'trade_admin_auth/manage_emails.html', context)

def delete_email(request, id):
    Email = Admin_Block_Main_Withdraw.objects.get(id=id)
    Email.delete()
    messages.success(request, 'Email deleted successfully!')
    return redirect('/tradeadmin/manage_emails')
  
  
from django.shortcuts import render
from django.http import JsonResponse
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from decimal import Decimal
from django.db.models import Sum

@csrf_exempt
def get_user_pwdetails(request):
    start = int(request.POST.get('start', 0))
    length = int(request.POST.get('length', 10))
    draw = int(request.POST.get('draw', 1))

    # Retrieve filter values
    email_filter = request.POST.get('email', '')
    plan_filter = request.POST.get('plan', '')
    lock_date_filter = request.POST.get('lock_date', '')
    premium_wallet_filter = request.POST.get('premium_wallet', '')
    transferpw_filter = request.POST.get('transferpw', '')

    # Queryset base filter
    queryset = User_Management.objects.all()

    # Apply filters
    if email_filter:
        queryset = queryset.filter(Email__icontains=email_filter)
    # if plan_filter:
    #     queryset = queryset.filter(plan__icontains=plan_filter)
    # Apply plan filter (handle >= case)
    if plan_filter:
        try:
            # Check if the plan filter is a number for the `>=` comparison
            plan_value = Decimal(plan_filter)
            queryset = queryset.filter(plan__gte=plan_value)
        except (ValueError, Decimal.InvalidOperation):
            # If it's not a number, apply the regular `icontains` filter
            queryset = queryset.filter(plan__icontains=plan_filter)
    if lock_date_filter:
        queryset = queryset.filter(plan_start_date__date=lock_date_filter)
    if premium_wallet_filter:
        try:
            premium_wallet_value = Decimal(premium_wallet_filter)
            queryset = queryset.filter(user_cashwallet__Premiumwallet__gte=premium_wallet_value)
        except (ValueError, Decimal.InvalidOperation):
            pass
    if transferpw_filter:
        try:
            transferpw_value = Decimal(transferpw_filter)
            queryset = queryset.filter(transferpw__gte=transferpw_value)
        except (ValueError, Decimal.InvalidOperation):
            pass

    # Calculate totals
    total_premium_wallet = queryset.aggregate(Sum('user_cashwallet__Premiumwallet'))['user_cashwallet__Premiumwallet__sum'] or 0
    total_transferpw = queryset.aggregate(Sum('transferpw'))['transferpw__sum'] or 0

    # Paginate results
    filtered_queryset = queryset[start:start + length]

    # Build the response data
    data = []
    for user in filtered_queryset:
        # Calculate lock_date as plan_start_date + 365 days
        lock_date = user.plan_start_date + timedelta(days=365) if user.plan_start_date else None

        # Fetch Premiumwallet from UserCashWallet
        user_cash_wallet = user.user_cashwallet.first()  # Related name should match the ForeignKey's related_name
        premium_wallet_value = user_cash_wallet.Premiumwallet if user_cash_wallet else 0.0

        # Append formatted row
        data.append({
            "email": user.Email,
            "plan": user.plan,
            "lock_date": lock_date,
            "premium_wallet": float(premium_wallet_value),
            "transferpw": float(user.transferpw),
        })

    # Total records count
    total_records = User_Management.objects.all().count()

    return JsonResponse({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": queryset.count(),
        "data": data,
        "total_premium_wallet": float(total_premium_wallet),
        "total_transferpw": float(total_transferpw),
    })

def USERPW(request):
    context = {}
    context['Title'] = ''
    return render(request, 'trade_admin_auth/USERPW.html', context)
    








from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Sum
from decimal import Decimal, InvalidOperation

@csrf_exempt
def get_promobonus_details(request):
    start = int(request.POST.get('start', 0))
    length = int(request.POST.get('length', 10))
    draw = int(request.POST.get('draw', 1))

    # Retrieve filters
    email_filter = request.POST.get('email', '')
    claim_amount_filter = request.POST.get('claim_amount', '')
    created_on_filter = request.POST.get('created_on', '')
    status_filter = request.POST.get('status', '')

    # Queryset
    queryset = promobonus_history.objects.all()

    if email_filter:
        queryset = queryset.filter(email__icontains=email_filter)

    if status_filter != '':  # ✅ Fix for 0 status issue
        try:
            status_value = int(status_filter)
            queryset = queryset.filter(status=status_value)
        except ValueError:
            pass
    
    if created_on_filter:  # ✅ Apply date filter
      queryset = queryset.filter(created_on__date=created_on_filter)

    # Pagination
    filtered_queryset = queryset[start:start + length]

    # Data response
    data = [
        {
            "id": record.id,
            "user_id": record.user_id,
            "email": record.email,
            "claim_amount": float(record.claim_amount),
            "link": record.link,
            "content": record.content,
            "created_on": record.created_on.strftime("%Y-%m-%d %H:%M:%S"),
            "status": record.status,
        }
        for record in filtered_queryset
    ]

    return JsonResponse({
        "draw": draw,
        "recordsTotal": promobonus_history.objects.count(),
        "recordsFiltered": queryset.count(),
        "data": data,
        "total_claim_amount": float(queryset.aggregate(Sum('claim_amount'))['claim_amount__sum'] or 0),
    })


def PROMOBONUS(request):
    context = {'Title': 'Promo Bonus History'}
    return render(request, 'trade_admin_auth/PROMOBONUS.html', context)



from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from decimal import Decimal

@csrf_exempt
def update_promobonus_status(request):
    if request.method == "POST":
        promo_id = request.POST.get("id")
        new_status = request.POST.get("status")

        try:
            new_status = int(new_status)
            promo = get_object_or_404(promobonus_history, id=promo_id)
            user_Deatail = get_object_or_404(User_Management, id=promo.user_id)

            if new_status == 1:  # Approve
                # promo.status = 1
                # promo.save()

                # ✅ Create BurnRewardHistory
                MPRewardHistory.objects.create(
                    user=user_Deatail,
                    referral_id="PROMOBONUS",
                    reward=promo.claim_amount
                )
                promo.status = 1
                promo.save()
                message = "Promo Bonus Approved!"

            elif new_status == 2:  # Reject
                promo.status = 2
                promo.save()
                message = "Promo Bonus Rejected!"

            else:
                return JsonResponse({"error": "Invalid status"}, status=400)

            return JsonResponse({"success": True, "message": message})

        except ValueError:
            return JsonResponse({"error": "Invalid data"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)





##############################################################################################
#######################      Swap     ########################################################
##############################################################################################

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Sum
from decimal import Decimal, InvalidOperation
@csrf_exempt
def get_Swap_details(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method."}, status=405)

    try:
        # Pagination
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10))
        draw = int(request.POST.get('draw', 1))
    except ValueError:
        return JsonResponse({"error": "Invalid pagination values."}, status=400)

    # Filters
    email_filter = request.POST.get('email', '').strip()
    claim_amount_filter = request.POST.get('claim_amount', '').strip()
    created_on_filter = request.POST.get('created_on', '').strip()
    status_filter = request.POST.get('status', '').strip()

    # Base queryset
    queryset = swap_sendhistory.objects.select_related('userid').all()

    # Apply filters
    if email_filter:
        queryset = queryset.filter(userid__Email__icontains=email_filter)

    if status_filter:
        try:
            queryset = queryset.filter(status=int(status_filter))
        except ValueError:
            pass  # ignore invalid status

    if created_on_filter:
        queryset = queryset.filter(created_on__date=created_on_filter)

    # Total amount from filtered results
    total_claim = queryset.aggregate(Sum('Amount'))['Amount__sum'] or 0

    # Count before and after filtering
    records_total = swap_sendhistory.objects.count()
    records_filtered = queryset.count()

    # Pagination
    paginated_queryset = queryset.order_by('-id')[start:start + length]

    # Prepare response data
    data = [
        {
            "id": record.id,
            "user_id": record.userid.id if record.userid else None,
            "email": record.userid.Email if record.userid else "",
            "amount": float(record.Amount),
            "claim_amountusdt": float(record.Withdraw_USDT),
            "claim_amountjwc": float(record.Withdraw_JWC),
            "Transaction_Hash": record.Transaction_Hash or "",
            "Transaction_Hash_recieved": record.Transaction_Hash_recieved or "",
            "Address": record.Address or "",
            "created_on": record.created_on.strftime("%Y-%m-%d %H:%M:%S"),
            "status": record.status,
        }
        for record in paginated_queryset
    ]

    # Final response
    return JsonResponse({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": data,
        "total_claim_amount": float(total_claim),
    })



# @csrf_exempt
# def get_Swap_details(request):
#     start = int(request.POST.get('start', 0))
#     length = int(request.POST.get('length', 10))
#     draw = int(request.POST.get('draw', 1))

#     # Retrieve filters
#     email_filter = request.POST.get('email', '')
#     claim_amount_filter = request.POST.get('claim_amount', '')
#     created_on_filter = request.POST.get('created_on', '')
#     status_filter = request.POST.get('status', '')

#     # Queryset
#     queryset = swap_sendhistory.objects.select_related('userid') 
#     if email_filter:
#         queryset = queryset.filter(userid__email__icontains=email_filter) 

#     if status_filter != '':  
#         try:
#             status_value = int(status_filter)
#             queryset = queryset.filter(status=status_value)
#         except ValueError:
#             pass
    
#     if created_on_filter: 
#         queryset = queryset.filter(created_on__date=created_on_filter)

#     # Pagination
#     filtered_queryset = queryset[start:start + length]

#     # Data response
#     data = [
#         {
#             "id": record.id,
#             "user_id": record.userid_id,
#             "email": record.userid.Email, 
#             "amount": float(record.Amount),
#             "claim_amountusdt": float(record.Withdraw_USDT),
#             "claim_amountjwc": float(record.Withdraw_JWC),
#             "Transaction_Hash": record.Transaction_Hash,
#             "Transaction_Hash_recieved": record.Transaction_Hash_recieved,
#             "Address": record.Address,
#             "created_on": record.created_on.strftime("%Y-%m-%d %H:%M:%S"),
#             "status": record.status,
#         }
#         for record in filtered_queryset
#     ]

#     return JsonResponse({
#         "draw": draw,
#         "recordsTotal": swap_sendhistory.objects.count(),
#         "recordsFiltered": queryset.count(),
#         "data": data,
#         "total_claim_amount": float(queryset.aggregate(Sum('Amount'))['Amount__sum'] or 0),
#     })



def SWAP(request):
    context = {'Title': 'SWAP History'}
    return render(request, 'trade_admin_auth/swap.html', context)

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum

@csrf_exempt
def Approve_swap(request):
    if request.method == "POST":
        promo_id = request.POST.get("id")
        new_status = request.POST.get("status")

        try:
            new_status = int(new_status)
            promo = get_object_or_404(swap_sendhistory, id=promo_id)
            user_detail = get_object_or_404(User_Management, id=promo.userid_id)

            if new_status == 1:  # Approve
                if float(promo.Withdraw_USDT) > 0:
                    return swapusdtapprove(request, promo.id)  # ✅ Call function properly
                else:
                    return swapjwcapprove(request, promo.id)  # ✅ Call function properly

            elif new_status == 2:  # Reject
                promo.status = 2
                promo.save()
                return JsonResponse({"success": True, "message": "SWAP Rejected!"})

            elif new_status == 4:  # Hold
                promo.status = 4
                promo.save()
                return JsonResponse({"success": True, "message": "SWAP Put on Hold!"})

            else:
                return JsonResponse({"error": "Invalid status"}, status=400)

        except ValueError:
            return JsonResponse({"error": "Invalid data"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


def swapusdtapprove(request, id):
    try:
        withdraw = swap_sendhistory.objects.get(id=id)
        user_detail = User_Management.objects.get(id=withdraw.userid_id)
        amount = float(withdraw.Withdraw_USDT)
        max_amount = int(Decimal(amount) * 10 ** 18)

        from_address = Web3.toChecksumAddress(Company.objects.get(id=1).withaddress)
        to_address = Web3.toChecksumAddress(str(withdraw.Address))

        gas_price = w3.eth.gas_price
        gas_limit = 500000

        txn = {
            'from': from_address,
            'to': usdt_tkn_address,
            'data': usd_token_contract.encodeABI(fn_name='transfer', args=[to_address, max_amount]),
            'gasPrice': gas_price,
            'gas': gas_limit,
            'nonce': w3.eth.get_transaction_count(from_address)
        }

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=Admin_key)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        transaction_hash = txn_hash.hex()

        receipt = w3.eth.wait_for_transaction_receipt(txn_hash, timeout=120, poll_latency=2)

        if receipt['status'] == 1:
            withdraw.status = 1
            withdraw.Transaction_Hash = transaction_hash
            withdraw.save()
            return JsonResponse({"success": True, "message": "SWAP Successful!"})
        else:
            return JsonResponse({"error": "Transaction failed on the blockchain."}, status=400)

    except Exception as e:
        return JsonResponse({"error": f"Failed with error: {str(e)}"}, status=400)


def swapjwcapprove(request, id):
    try:
        withdraw = swap_sendhistory.objects.get(id=id)
        user_detail = User_Management.objects.get(id=withdraw.userid_id)
        amount = float(withdraw.Withdraw_JWC)
        max_amount = int(Decimal(amount) * 10 ** 8)

        from_address = Web3.toChecksumAddress(Company.objects.get(id=1).withaddress)
        to_address = Web3.toChecksumAddress(str(withdraw.Address))

        gas_price = w3.eth.gas_price
        gas_limit = 500000

        txn = {
            'from': from_address,
            'to': jwc_tkn_address,
            'data': jwc_token_contract.encodeABI(fn_name='transfer', args=[to_address, max_amount]),
            'gasPrice': gas_price,
            'gas': gas_limit,
            'nonce': w3.eth.get_transaction_count(from_address)
        }

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=Admin_key)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        transaction_hash = txn_hash.hex()

        receipt = w3.eth.wait_for_transaction_receipt(txn_hash, timeout=120, poll_latency=2)

        if receipt['status'] == 1:
            withdraw.status = 1
            withdraw.Transaction_Hash = transaction_hash
            withdraw.save()
            return JsonResponse({"success": True, "message": "SWAP Successful!"})
        else:
            return JsonResponse({"error": "Transaction failed on the blockchain."}, status=400)

    except Exception as e:
        return JsonResponse({"error": f"Failed with error: {str(e)}"}, status=400)



#################################
################### burn withdraw detail  



from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Sum
from decimal import Decimal, InvalidOperation

@csrf_exempt
def get_Burn_details(request):
    start = int(request.POST.get('start', 0))
    length = int(request.POST.get('length', 10))
    draw = int(request.POST.get('draw', 1))

    email_filter = request.POST.get('email', '')
    claim_amount_filter = request.POST.get('claim_amount', '')
    created_on_filter = request.POST.get('created_on', '')
    status_filter = request.POST.get('status', '')

    # Base queryset
    queryset = BurnWithdraw.objects.select_related('userid')

    # Apply filters
    if email_filter:
        queryset = queryset.filter(userid__Email__icontains=email_filter)

    if status_filter != '':
        try:
            status_value = int(status_filter)
            queryset = queryset.filter(status=status_value)
        except ValueError:
            pass

    if created_on_filter:
        queryset = queryset.filter(created_on__date=created_on_filter)

    if claim_amount_filter:
        try:
            claim_value = Decimal(claim_amount_filter)
            queryset = queryset.filter(Amount__gte=claim_value)
        except InvalidOperation:
            pass

    total_filtered = queryset.count()
    total_claim_amount = queryset.aggregate(Sum('Amount'))['Amount__sum'] or 0

    paginated_queryset = queryset[start:start + length]

    data = [
        {
            "id": record.id,
            "user_id": record.userid_id,
            "email": record.userid.Email,  
            "amount": float(record.Amount),
            "Claim_JW": float(record.Withdraw_JW),
            "Claim_JWC": float(record.Withdraw_USDT),
            "Transaction_Hash": record.Transaction_Hash,
            "Address": record.Address,
            "created_on": record.created_on.strftime("%Y-%m-%d %H:%M:%S"),
            "status": record.status,
        }
        for record in paginated_queryset
    ]

    return JsonResponse({
        "draw": draw,
        "recordsTotal": BurnWithdraw.objects.count(),
        "recordsFiltered": total_filtered,
        "data": data,
        "total_claim_amount": float(total_claim_amount),
    })


def BURNWITHDRAW(request):
    context = {'Title': 'Burn Withdraw History'}
    return render(request, 'trade_admin_auth/burnwithdraw_request.html', context)
