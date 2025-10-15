from base64 import urlsafe_b64encode
import datetime
from decimal import Decimal
import string
import time
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
import pyotp
from urllib3 import HTTPResponse
from API.models import Admin_Profit, Contract_address, Delete_Account_Management, Delete_Account_Reason_Management, Google_Fitness, Internal_transfer_history, Pin, Plan_purchase_wallet, Referral_code, Referral_reward, Referral_reward_History, Reward_History, User_2x_Boost, User_address, UserCashWallet, Withdraw, Withdraw_history, admin_notification_message, admin_referral_code, market_price, plan, plan_purchase_history, premium_wallet_deposit, premium_wallet_management, referral_level, referral_table, user_address_trust_wallet, wallet_flush_history, withdraw_values
from API.serializers import  Change_Pin_Serializer,  Country_Serializers, Delete_Reason_Serializers, Delete_Serializers, Faq_Serializers, Google_fitness_Serializers, Login_Serializer,  Pin_Set_Serializer, Plan_purchase_wallet_Serializers, Referral_History_Serializers,  Register_OTP_Serializer, Reward_History_Serializers, State_Serializers, Steps_history_Serializers, User_Referral_Serializers,  User_Serializer, User_two_fa_details_Serializers, Verify_Pin_Serializer, Withdraw_history_Serializers,  plan_Serializers, step_count_Serializers, terms_cms_Serializers, two_fa_Serializers, user_DeatailSerializers, user_address_Serializers, user_step_Serializers,Stake_credit_Serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from company.models import Company, Company_Settings
from locations.models import Country, State
from trade_auth.models import Market_place
from trade_master.models import Cms_StaticContent, Faq , EmailTemplate, Jw_plan_purchase_history,LoginHistory,SupportCategory,Contactus,SupportTicket,Stake_Credit_History

from trade_admin_auth.models import Registration_otp, Steps_Management, Steps_history, Two_x_boost, User_Management, User_two_fa, WithdrawSendHistory, WithdrawSendUSDTHistory, front_page_management,PlanDateUpdateHistory
from django.utils.encoding import force_bytes
from django.template.loader import get_template
from django.utils import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import math, random
from rest_framework.authtoken.models import Token
from django.db.models import Q
from trade_currency.models import TradeCurrency
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
from trade_admin_auth.contract import token_abi,token_address,usdt_token_address,usdt_token_abi
from API.SeDGFHte import coinpaprika_api_key

from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import secrets
import string


from Staking.models import Stake_Monthly_Claim_History, Stake_market_price, Stake_monthly_history_management, internal_transfer_admin_management, stake_wallet_management,Stake_history_management,internal_transfer_history, staking_admin_management,stake_claim_reward_history,stake_deposit_management,stake_claim_table,Stake_referral_reward_table, staking_monthly_admin_management

from Crypto.Cipher import AES
import base64

from dateutil.relativedelta import relativedelta


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


# Create your views here.

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) 
        )
account_activation_token = TokenGenerator()

def generateOTP() :
	digits = "0123456789"
	OTP = ""
	for i in range(4) :
		OTP += digits[math.floor(random.random() * 10)]

	return OTP



import requests

def coin_market_price(request):
    market = market_price.objects.get(id = 1)
    if market.status == 1:
        if market.API == 0:
            b = "jasan-wellness"
            c = "usd"
            op=(cg.get_price(ids=b, vs_currencies=c,include_24hr_vol = True ,include_24hr_change = True))
            a=op[b][c]
            market_pricee = a
            market = market_price.objects.get(id = 1)
            market.market_price = (market_pricee)
            market.save()

        if market.API == 1:
            url = 'https://api.coinpaprika.com/v1/tickers/jw-jasan-wellness'
            response = requests.get(url)
            data = response.json()
            quote = data['quotes']
            USd = quote['USD']
            price = USd['price']
            market = market_price.objects.get(id = 1)
            market.market_price = price
            market.save()

        if market.API == 2:
            url = "https://api.livecoinwatch.com/coins/single"
            payload = json.dumps({
            "currency": "USD",
            "code": "JW",
            "meta": True
            })
            headers = {
            'content-type': 'application/json',
            'x-api-key': '909ce001-5983-4d07-9e2d-034c94c4dfb6'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            test = response.text
            price_price = json.loads(test)
            price = price_price['rate']
            market = market_price.objects.get(id = 1)
            market.market_price = price
            market.save()

    return HttpResponse('Success')

# API VIEWS
def Registrationotp(request,otp,user_id):
    get_user = User_Management.objects.get(id=user_id)
    if get_user:
          create_OTP = Registration_otp.objects.create(
            user=get_user,
            email_otp = otp

          )   

    return  True


def Registrationotp_phone(request,otp,user_id):
    get_user = User_Management.objects.get(id=user_id)
    if get_user:
          create_OTP = Registration_otp.objects.create(
            user=get_user,
            phone_number_opt = otp

          )   

    return  True

def Create_Google_Fitness(request,user_id):
    get_user = User_Management.objects.get(id=user_id)
    if get_user:
        create_Google_fitness = Google_Fitness.objects.create(
            user = get_user,
        )

    return True

def Create_User_cash_Wallet(request,user_id):
    get_user = User_Management.objects.get(id=user_id)
    if get_user:
        get_currency = TradeCurrency.objects.filter(Q(symbol = 'JW')).order_by('-id')
        if get_currency:
            for item in get_currency:
                create_user_wallet = UserCashWallet.objects.create(
                    userid_id=user_id,
                    currency_id=item.id,
                    balanceone=0.0000,
                    balancetwo=0.0000,
                    referalincome=0.00,
                    Premiumwallet=0.00,
                    address='',
                    status=0,
                ) 
    return True

def Pin_Create(request,user_id):
    get_user = User_Management.objects.get(id=user_id)
    if get_user:
       create_pin = Pin.objects.create(
           user = get_user,
           status = 1,
       )
    return True

def user_list_for_update(request,id,wallet_Type):
    context = {} 
    History_Reward=''
    Boost_Reward=''
    total_reward=0
    total_diff=''
    total_reff_diff=''
    context['Title'] = 'User Management'
    adminactivity_qs = User_Management.objects.get(id=id)
    context['adminactivity_qs'] =adminactivity_qs
    con = ""
    sum_amount = 0
    sum_amount_referral = 0

#   try:
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
        withdraw_amount  = Withdraw.objects.filter(userid_id = adminactivity_qs.id,Wallet_type = "Reward_wallet")
        for i in withdraw_amount :
            sum_amount = sum_amount + Decimal(i.Amount)
        withdraw_amount_referral  = Withdraw.objects.filter(userid_id = adminactivity_qs.id,Wallet_type = "Referral_wallet")
        for j in withdraw_amount_referral :
            sum_amount_referral = sum_amount_referral + Decimal(j.Amount)

        health_internal_transfer = internal_transfer_history.objects.using('second_db').filter(user = adminactivity_qs.id,from_wallet = "Reward_wallet").aggregate(Sum('actual_amount'))

        referral_internal_transfer = internal_transfer_history.objects.using('second_db').filter(user = adminactivity_qs.id,from_wallet = "Referral_wallet").aggregate(Sum('actual_amount'))


    else:
        withdraw_amount  = Withdraw.objects.filter(userid_id = adminactivity_qs.id,created_on__gte = adminactivity_qs.plan_start_date,Wallet_type = "Reward_wallet")
        for i in withdraw_amount :
            sum_amount = sum_amount + Decimal(i.Amount)
        withdraw_amount_referral  = Withdraw.objects.filter(userid_id = adminactivity_qs.id,created_on__gte = adminactivity_qs.plan_start_date,Wallet_type = "Referral_wallet")
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
        total_reward = (Decimal(History_Reward) + Decimal(Boost_Reward)) - (Decimal(sum_amount) + Decimal(Health_Transfer_Reward))
        

    total_diff = Decimal(blnc) - round(total_reward,7)



    total_ref_reward = Decimal(Rewards_Reward) - (Decimal(sum_amount_referral) + Decimal(Referral_Transfer_Reward))

    total_reff_diff = Decimal(wallet.referalincome) - round(total_ref_reward, 7)


    if wallet_Type == 1:
        return (total_diff)
    if wallet_Type == 2:
        return (total_reff_diff)
    if wallet_Type == 3:
        return ({'total':total_diff,'ref_diff':total_reff_diff})


def load_maintanance(request):
    details = Company_Settings.objects.values('site_maintenance_status','IOS_site_maintenance_status').get(id = 1)
    if details['site_maintenance_status'] == 1:
        return True
    else:
        return False

from datetime import datetime, time

@api_view(['POST'])
def add_User(request):
        main = load_maintanance(request)
        if main  == True:
            user_data = {'Msg':'App Under Maintanance','status':'false'}
            return Response(user_data)
        serializers=User_Serializer(data=request.data)
        if serializers.is_valid():
            user__name = request.data['user_name']
            email = request.data['Email']
            code = request.data['referal_code']
            device_unique_id = request.data['device_unique_id']
            phone_number = ""
            try:
                phone_number = request.data['Phone_Number']
            except:
                phone_number = ""
            try:
                companyqs = Company.objects.get(id=1)
                companyname= companyqs.name
            except:
                companyqs = ''
                companyname = ''
            N = 12
            if int(companyqs.Device_id_status) == 0:
                decvice_cout= User_Management.objects.filter(device_unique_id = device_unique_id).count()
                if decvice_cout > 0 :
                    user_data={"Msg":"This Device Is Already Login IN Another Account",'status':'false'}
                    return Response(user_data)
            radmon_username = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
              for i in range(N))
            Email_count = User_Management.objects.filter(Email = email).count()
            if Email_count > 0 :
                user_data={"Msg":"User Already Exists",'status':'false'}
                return Response(user_data)
            if phone_number != "":
                Phone_Number_Count = User_Management.objects.filter(user_phone_number = phone_number).count()
                if Phone_Number_Count > 0 :
                    user_data={"Msg":"Phone Number Already Exists",'status':'false'}
                    return Response(user_data)
            try :
                User.objects.get(username = radmon_username)
                user_data={"Msg":"Please Try Again",'status':'false'}
                return Response(user_data)
            except:                
                if code == "":
                    user_data={"Msg":"Referral Code Required",'status':'false'}
                    return Response(user_data)
                if code == "U8DECP":
                    user_data={"Msg":"Referral Code Required",'status':'false'}
                    return Response(user_data)
                # if phone_number == "":
                #     user_data = {'Msg':'Phone Number Required','status':'false'}
                #     return Response(user_data)
                user_type = request.data['User_type']
                device_id = request.data['User_Device_id']
                if user_type == "":
                    user_data={"Msg":"User Type data Needed",'status':'false'}
                    return Response(user_data)
                if user_type == "IOS":
                    try:
                        eemail = User_Management.objects.get(Email = email)
                        try:
                            get_user_delete = Delete_Account_Management.objects.get(user_id = eemail.id)
                            if get_user_delete:
                                user_data={"Msg":"Your Account Has been Requested to DeActivate,Please Wait for Admin Confirmation",'status':'false'}
                                return Response(user_data)
                        except:
                            pass
                    except:
                        eemail = ""
                    if eemail:
                        user = User.objects.get(username = eemail.user_name)
                        token = Token.objects.get(user = user)
                        if eemail.User_type == "IOS":
                            msg = ""
                            Activestatus = eemail.Activate_Status
                            if eemail.User_Verification_Status == "logindone" and Activestatus == "1":
                                eemail.Activate_Status = "1"
                                eemail.save()
                            else:
                                eemail.Activate_Status = "0"
                                eemail.save()
                            try:
                                pin = Pin.objects.get(user_id = user.id )
                                if pin.pin is None:
                                    msg = "NewUser"
                                else:
                                    msg = "OldUser"
                            except:
                                msg = "OldUser"
                            ref_code = Referral_code.objects.get(user_id = eemail.id )
                            user_data={"Msg":"Login Successfully",'status':'true','token':token.key,"userStatus":msg,'referral_code':ref_code.referal_code,'setType':eemail.User_Verification_Status,'User_type':eemail.User_type,'ActivateStatus':Activestatus}
                            return Response(user_data)
                    num=""
                    ref_reward = Referral_reward.objects.get(id = 1)
                    if code == "":
                        ref_code = ""
                        user = User.objects.create(username = radmon_username)
                        step = Steps_Management.objects.get(id = 1)
                        free_days = step.free_plan_days
                        withdraw = withdraw_values.objects.get(id = 1)
                        plan_plan = plan.objects.get(plan_type = 0)
                        user_details = User_Management.objects.create(Email = email,User_type = user_type,status = 0,user_name = radmon_username,User_Device_id = device_id,User_Verification_Status = "pinset",referal_code = code,Name = user__name,Health_Withdraw_min_value=withdraw.Health_wallet_minimum_withdraw_limit,Health_Withdraw_max_value = withdraw.Health_wallet_maximum_withdraw_limit,Referral_Withdraw_min_value = withdraw.Referral_wallet_minimum_withdraw_limit,Referral_Withdraw_max_value = withdraw.Referral_wallet_maximum_withdraw_limit,reward_steps = plan_plan.Reward_step_value,reward_step_amount = plan_plan.plan_reward_amount,withdraw_status = plan_plan.withdraw_status,Two_X_Boost_status = 1,user = plan_plan.Min_step_count,over_all_stepcount = plan_plan.Max_step_count,user_phone_number = phone_number,notes="",fixed_status="market")
                        desired_time = datetime.strptime("23:55", "%H:%M").time()
                        today = datetime.now()
                        today_with_desired_time = datetime.combine(today.date(), desired_time)
                        end_date = today_with_desired_time + timedelta(free_days)
                        user_details.plan_end_date = end_date
                        user_details.save()
                        if user_details.device_unique_id is None or user_details.device_unique_id == "":
                            user_details.device_unique_id=device_unique_id
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
                                user_details = User_Management.objects.create(Email = email,User_type = user_type,status = 0,user_name = radmon_username,reff_id=user_ref.user_id,User_Device_id = device_id,User_Verification_Status = "pinset",referal_code = code,Name = user__name,Health_Withdraw_min_value=withdraw.Health_wallet_minimum_withdraw_limit,Health_Withdraw_max_value = withdraw.Health_wallet_maximum_withdraw_limit,Referral_Withdraw_min_value = withdraw.Referral_wallet_minimum_withdraw_limit,Referral_Withdraw_max_value = withdraw.Referral_wallet_maximum_withdraw_limit,reward_steps = plan_plan.Reward_step_value,reward_step_amount = plan_plan.plan_reward_amount,withdraw_status = plan_plan.withdraw_status,Two_X_Boost_status = 1,user = plan_plan.Min_step_count,over_all_stepcount = plan_plan.Max_step_count,user_phone_number = phone_number,notes="",fixed_status="market")
                                desired_time = datetime.strptime("23:55", "%H:%M").time()
                                today = datetime.now()
                                today_with_desired_time = datetime.combine(today.date(), desired_time)
                                end_date = today_with_desired_time + timedelta(free_days)
                                user_details.plan_end_date = end_date
                                user_details.save()
                                if user_details.device_unique_id is None or user_details.device_unique_id == "":
                                    user_details.device_unique_id=device_unique_id
                                    user_details.save()
                                token = Token.objects.create(user = user)
                                get_user = User_Management.objects.get(Email = email)
                                tokenkey = token.key
                                referral__table(request,tokenkey,code)
                            else:
                                user_data={"Msg":"Referral Code Invalid1",'status':'false'}
                                return Response(user_data)
                            reward_user = User_Management.objects.get(id = user_ref.user_id)
                            if reward_user.plan != 0 :
                                current_plan = plan.objects.get(id = reward_user.plan)
                                if current_plan.referral_status == 1:
                                    if user_ref:
                                        ref_code = code
                                        user_wallet = UserCashWallet.objects.get(userid_id = reward_user.id)
                                        reward = Decimal(ref_reward.Reward)
                                        user_wallet.referalincome = user_wallet.referalincome + reward
                                        num="1"
                                        referral__table(request,tokenkey,code)
                                    else:
                                        user_data={"Msg":"Referral Code Invalid2",'status':'false'}
                                        return Response(user_data)
                        except:
                            user_data={"Msg":"Referral Code Invalid",'status':'false'}
                            return Response(user_data)
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
                    user_data={"Msg":"User Create Successfully",'status':'true','token':token.key}
                    return Response(user_data)

                if user_type == "facebook":
                    try:
                        eemail = User_Management.objects.get(Email = email)
                        user = User.objects.get(username = eemail.user_name)
                        token = Token.objects.get(user = user)
                        try:
                            get_user_delete = Delete_Account_Management.objects.get(user_id = eemail.id)
                            if get_user_delete:
                                user_data={"Msg":"Your Account Has been Requested to DeActivate,Please Wait for Admin Confirmation",'status':'false'}
                                return Response(user_data)
                        except:
                            pass

                    except:
                        eemail = ""
                    if eemail:
                        user = User.objects.get(username = eemail.user_name)
                        token = Token.objects.get(user = user)
                        msg = ""
                        Activestatus = eemail.Activate_Status
                        if eemail.User_Verification_Status == "logindone" and Activestatus == "1":
                            eemail.Activate_Status = "1"
                            eemail.save()
                        else:
                            eemail.Activate_Status = "0"
                            eemail.save()
                        try:
                            pin = Pin.objects.get(user_id = eemail.id )
                            if pin.pin is None:
                                msg = "NewUser"
                            else:
                                msg = "OldUser"
                        except:
                            msg = "OldUser"
                        ref_code = Referral_code.objects.get(user_id = eemail.id )
                        eeemail = email[:4]
                        eeemail_last = email[-6:]
                        pin = Pin.objects.get(user_id = eemail.id )
                        pin.pin = None
                        pin.save()
                        user_data={"Msg":"Login Successfull",'status':'true','token':token.key,'email':eeemail+"******************"+eeemail_last,'referral_code':ref_code.referal_code,'User_type':eemail.User_type,'setType':eemail.User_Verification_Status,'ActivateStatus':Activestatus} 
                        return Response(user_data)                    
                    num=""
                    ref_reward = Referral_reward.objects.get(id = 1)
                    if code == "":
                        ref_code = ""
                        user = User.objects.create(username = radmon_username)
                        step = Steps_Management.objects.get(id = 1)
                        free_days = step.free_plan_days
                        withdraw = withdraw_values.objects.get(id = 1)
                        plan_plan = plan.objects.get(plan_type = 0)
                        user_details = User_Management.objects.create(Email = email,User_type = user_type,status = 0,user_name = radmon_username,User_Device_id = device_id,User_Verification_Status = "pinset",referal_code = code,Name = user__name,Health_Withdraw_min_value=withdraw.Health_wallet_minimum_withdraw_limit,Health_Withdraw_max_value = withdraw.Health_wallet_maximum_withdraw_limit,Referral_Withdraw_min_value = withdraw.Referral_wallet_minimum_withdraw_limit,Referral_Withdraw_max_value = withdraw.Referral_wallet_maximum_withdraw_limit,reward_steps = plan_plan.Reward_step_value,reward_step_amount = plan_plan.plan_reward_amount,withdraw_status = plan_plan.withdraw_status,Two_X_Boost_status = 1,user = plan_plan.Min_step_count,over_all_stepcount = plan_plan.Max_step_count,user_phone_number = phone_number,notes="",fixed_status="market")
                        desired_time = datetime.strptime("23:55", "%H:%M").time()
                        today = datetime.now()
                        today_with_desired_time = datetime.combine(today.date(), desired_time)
                        end_date = today_with_desired_time + timedelta(free_days)
                        user_details.plan_end_date = end_date
                        user_details.save()
                        if user_details.device_unique_id is None or user_details.device_unique_id == "":
                            user_details.device_unique_id=device_unique_id
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
                                user_details = User_Management.objects.create(Email = email,User_type = user_type,status = 0,user_name = radmon_username,reff_id=user_ref.user_id,User_Device_id = device_id,User_Verification_Status = "pinset",referal_code = code,Name = user__name,Health_Withdraw_min_value=withdraw.Health_wallet_minimum_withdraw_limit,Health_Withdraw_max_value = withdraw.Health_wallet_maximum_withdraw_limit,Referral_Withdraw_min_value = withdraw.Referral_wallet_minimum_withdraw_limit,Referral_Withdraw_max_value = withdraw.Referral_wallet_maximum_withdraw_limit,reward_steps = plan_plan.Reward_step_value,reward_step_amount = plan_plan.plan_reward_amount,withdraw_status = plan_plan.withdraw_status,Two_X_Boost_status = 1,user = plan_plan.Min_step_count,over_all_stepcount = plan_plan.Max_step_count,user_phone_number = phone_number,notes="",fixed_status="market")
                                desired_time = datetime.strptime("23:55", "%H:%M").time()
                                today = datetime.now()
                                today_with_desired_time = datetime.combine(today.date(), desired_time)
                                end_date = today_with_desired_time + timedelta(free_days)
                                user_details.plan_end_date = end_date
                                user_details.save()
                                if user_details.device_unique_id is None or user_details.device_unique_id == "":
                                    user_details.device_unique_id=device_unique_id
                                    user_details.save()
                                token = Token.objects.create(user = user)
                                get_user = User_Management.objects.get(Email = email)
                                tokenkey = token.key
                                referral__table(request,tokenkey,code)
                            else:
                                user_data={"Msg":"Referral Code Invalid",'status':'false'}
                                return Response(user_data)
                            reward_user = User_Management.objects.get(id = user_ref.user_id)
                            if reward_user.plan != 0 :
                                current_plan = plan.objects.get(id = reward_user.plan)
                                if current_plan.referral_status == 1:
                                    if user_ref:
                                        ref_code = code
                                        user_wallet = UserCashWallet.objects.get(userid_id = reward_user.id)
                                        reward = Decimal(ref_reward.Reward)
                                        user_wallet.referalincome = user_wallet.referalincome + reward
                                        num="1"
                                        referral__table(request,tokenkey,code)
                                    else:
                                        user_data={"Msg":"Referral Code Invalid",'status':'false'}
                                        return Response(user_data)
                                else:
                                    user_data={"Msg":"Referral Code Invalid",'status':'false'}
                                    return Response(user_data)
                        except:
                            user_data={"Msg":"Referral Code Invalid",'status':'false'}
                            return Response(user_data)
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
                    eemail = email[:4]
                    eemail_last = email[-6:]
                    user_data={"Msg":"User Create Successfully",'status':'true','token':token.key,'email':eemail+"******************"+eemail_last,'referral_code':res,'User_type':user_type,'setType':get_user.User_Verification_Status}
                    return Response(user_data)
                
                if user_type == "gmail":
                    try:
                        eemail = User_Management.objects.get(Email = email)
                        user = User.objects.get(username = eemail.user_name)
                        token = Token.objects.get(user = user)
                        try:
                            get_user_delete = Delete_Account_Management.objects.get(user_id = eemail.id)
                            if get_user_delete:
                                user_data={"Msg":"Your Account Has been Requested to DeActivate,Please Wait for Admin Confirmation",'status':'false'}
                                return Response(user_data)
                        except:
                            pass
                    except:
                        eemail = ""
                    if eemail:
                        msg = ""
                        Activestatus = eemail.Activate_Status
                        if eemail.User_Verification_Status == "logindone" and Activestatus == "1":
                            eemail.Activate_Status = "1"
                            eemail.save()
                        else:
                            eemail.Activate_Status = "0"
                            eemail.save()
                        try:
                            pin = Pin.objects.get(user_id = eemail.id )
                            if pin.pin is None:
                                msg = "NewUser"
                            else:
                                msg = "OldUser"
                        except:
                            msg = "OldUser"
                        ref_code = Referral_code.objects.get(user_id = eemail.id )
                        eeemail = email[:4]
                        eeemail_last = email[-6:]
                        pin = Pin.objects.get(user_id = eemail.id )
                        pin.pin = None
                        pin.save()
                        user_data={"Msg":"Login Successfull",'status':'true','token':token.key,'email':eeemail+"******************"+eeemail_last,'referral_code':ref_code.referal_code,'User_type':eemail.User_type,'setType':eemail.User_Verification_Status,'ActivateStatus':Activestatus} 
                        return Response(user_data)
                    num=""
                    ref_reward = Referral_reward.objects.get(id = 1)
                    if code == "":
                        ref_code = ""
                        user = User.objects.create(username = radmon_username)
                        step = Steps_Management.objects.get(id = 1)
                        free_days = step.free_plan_days
                        withdraw = withdraw_values.objects.get(id = 1)
                        plan_plan = plan.objects.get(plan_type = 0)
                        user_details = User_Management.objects.create(Email = email,User_type = user_type,status = 0,user_name = radmon_username,User_Device_id = device_id,User_Verification_Status = "pinset",referal_code = code,Name = user__name,Health_Withdraw_min_value=withdraw.Health_wallet_minimum_withdraw_limit,Health_Withdraw_max_value = withdraw.Health_wallet_maximum_withdraw_limit,Referral_Withdraw_min_value = withdraw.Referral_wallet_minimum_withdraw_limit,Referral_Withdraw_max_value = withdraw.Referral_wallet_maximum_withdraw_limit,reward_steps = plan_plan.Reward_step_value,reward_step_amount = plan_plan.plan_reward_amount,withdraw_status = plan_plan.withdraw_status,Two_X_Boost_status = 1,user = plan_plan.Min_step_count,over_all_stepcount = plan_plan.Max_step_count,user_phone_number = phone_number,notes="",fixed_status="market")
                        desired_time = datetime.strptime("23:55", "%H:%M").time()    
                        today = datetime.now()
                        today_with_desired_time = datetime.combine(today.date(), desired_time)
                        end_date = today_with_desired_time + timedelta(free_days)
                        user_details.plan_end_date = end_date
                        user_details.save()
                        if user_details.device_unique_id is None or user_details.device_unique_id == "":
                            user_details.device_unique_id=device_unique_id
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
                                user_details = User_Management.objects.create(Email = email,User_type = user_type,status = 0,user_name = radmon_username,reff_id=user_ref.user_id,User_Device_id = device_id,User_Verification_Status = "pinset",referal_code = code,Name = user__name,Health_Withdraw_min_value=withdraw.Health_wallet_minimum_withdraw_limit,Health_Withdraw_max_value = withdraw.Health_wallet_maximum_withdraw_limit,Referral_Withdraw_min_value = withdraw.Referral_wallet_minimum_withdraw_limit,Referral_Withdraw_max_value = withdraw.Referral_wallet_maximum_withdraw_limit,reward_steps = plan_plan.Reward_step_value,reward_step_amount = plan_plan.plan_reward_amount,withdraw_status = plan_plan.withdraw_status,Two_X_Boost_status = 1,user = plan_plan.Min_step_count,over_all_stepcount = plan_plan.Max_step_count,user_phone_number = phone_number,notes="",fixed_status="market")
                                desired_time = datetime.strptime("23:55", "%H:%M").time()
                                today = datetime.now()
                                today_with_desired_time = datetime.combine(today.date(), desired_time)
                                end_date = today_with_desired_time + timedelta(free_days)
                                user_details.plan_end_date = end_date
                                user_details.save()
                                if user_details.device_unique_id is None or user_details.device_unique_id == "":
                                    user_details.device_unique_id=device_unique_id
                                    user_details.save()
                                token = Token.objects.create(user = user)
                                get_user = User_Management.objects.get(Email = email)
                                tokenkey = token.key
                                referral__table(request,tokenkey,code)
                            else:
                                user_data={"Msg":"Referral Code Invalid",'status':'false'}
                                return Response(user_data)
                            reward_user = User_Management.objects.get(id = user_ref.user_id)
                            if reward_user.plan != 0 :
                                current_plan = plan.objects.get(id = reward_user.plan)
                                if current_plan.referral_status == 1:
                                    if user_ref:
                                        ref_code = code
                                        user_wallet = UserCashWallet.objects.get(userid_id = reward_user.id)
                                        reward = Decimal(ref_reward.Reward)
                                        user_wallet.referalincome = user_wallet.referalincome + reward
                                        num="1"
                                        referral__table(request,tokenkey,code)
                                    else:
                                        user_data={"Msg":"Referral Code Invalid",'status':'false'}
                                        return Response(user_data)
                        except:
                            user_data={"Msg":"Referral Code Invalid",'status':'false'}
                            return Response(user_data)
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
                    eemail = email[:4]
                    eemail_last = email[-6:]
                    user_data={"Msg":"User Create Successfully",'status':'true','token':token.key,'email':eemail+"******************"+eemail_last,'referral_code':res,'User_type':user_type,'setType':get_user.User_Verification_Status}
                    return Response(user_data) 
                ref_code=""
                num=""
                ref_reward = Referral_reward.objects.get(id = 1)
                try:
                    eemail = User_Management.objects.get(Email = email)
                    try:
                            get_user_delete = Delete_Account_Management.objects.get(user_id = eemail.id)
                            if get_user_delete:
                                user_data={"Msg":"Your Account Has been Requested to DeActivate,Please Wait for Admin Confirmation",'status':'false'}
                                return Response(user_data)
                    except:
                        pass
                except:
                    eemail = ""
                if eemail:
                        user_data={"Msg":"User Already Exists",'status':'false'}
                        return Response(user_data)
                else:
                    try:
                        id = User_Management.objects.get(User_Device_id = device_id)
                        user_data={"Msg":"This Device Already Have A registered User",'status':'false'}
                        return Response(user_data)
                    except:
                        pass
                    try:
                        uuser = User.objects.get(username = user__name)
                    except:
                        uuser = ""
                    if uuser:
                        user_data={"Msg":"UserName Exists",'status':'false'}
                        return Response(user_data)
                    else:
                        if code:
                            ref_code = code
                            try:
                                user_ref = Referral_code.objects.get(referal_code = code )
                                pass
                            except:
                                user_data={"Msg":"Referral Code Invalid",'status':'false'}
                                return Response(user_data)
                        if code == "":
                            pass
                        try:
                            companyqs = Company.objects.get(id=1)
                            companyname= companyqs.name
                        except:
                            companyqs = ''
                            companyname = ''
                        otp = generateOTP()
                        emailtemplate = get_email_template(request,3)
                        to_email = email
                        data= {
                            'username':user__name,
                            'email':email,
                            'domain':settings.DOMAIN_URL,
                            'company_name':companyname,
                            'otp':otp,
                            }
                        htmly = get_template('emailtemplate/registration_email.html')
                        html_content = htmly.render(data)
                        response = requests.post(
                        "https://api.mailgun.net/v3/jasanwellness.fit/messages",
                        auth=("api", decrypt_with_common_cipher(settings.MAIL_API)),
                        data={"from": "WEB3 WELLNESS <noreply@jasanwellness.fit>",
                        "to": [to_email],
                        "subject": emailtemplate.Subject,
                        "html": html_content})
                        if response.status_code == 200 :
                            ref_code = code
                            user = User.objects.create(username = radmon_username)
                            step = Steps_Management.objects.get(id = 1)
                            free_days = step.free_plan_days
                            withdraw = withdraw_values.objects.get(id = 1)
                            plan_plan = plan.objects.get(plan_type = 0)
                            user_details = User_Management.objects.create(user_name = radmon_username,Email = email,referal_code = ref_code,reff_id=user_ref.user_id,User_type = user_type,User_Device_id =device_id,Name = user__name,Health_Withdraw_min_value=withdraw.Health_wallet_minimum_withdraw_limit,Health_Withdraw_max_value = withdraw.Health_wallet_maximum_withdraw_limit,Referral_Withdraw_min_value = withdraw.Referral_wallet_minimum_withdraw_limit,Referral_Withdraw_max_value = withdraw.Referral_wallet_maximum_withdraw_limit,reward_steps = plan_plan.Reward_step_value,reward_step_amount = plan_plan.plan_reward_amount,withdraw_status = plan_plan.withdraw_status,Two_X_Boost_status= 1,user = plan_plan.Min_step_count,over_all_stepcount = plan_plan.Max_step_count,user_phone_number = phone_number,notes="",fixed_status="market")
                            desired_time = datetime.strptime("23:55", "%H:%M").time()
                            today = datetime.now()
                            today_with_desired_time = datetime.combine(today.date(), desired_time)
                            end_date = today_with_desired_time + timedelta(free_days)
                            user_details.plan_end_date = end_date
                            user_details.save()
                            if user_details.device_unique_id is None or user_details.device_unique_id == "":
                                user_details.device_unique_id=device_unique_id
                                user_details.save()
                            get_user = User_Management.objects.get(Email = email,Name = request.data['user_name'])
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
                                        user_wallet = UserCashWallet.objects.get(userid_id = reward_user.id)
                                        reward = Decimal(ref_reward.Reward)
                                        user_wallet.referalincome = user_wallet.referalincome + reward
                
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
                            eemail = email[:4]
                            eemail_last = email[-6:]
                            user_data={"Msg":"User Create Successfully",'status':'true','token':token.key,'email':eemail+"******************"+eemail_last,'referral_code':res,'User_type':user_type}
                            return Response(user_data)
                        else:
                            user_data={"Msg": " Mail Server Problem. Please try again after some times !!!",'status':'false'}
                            return Response(user_data)


@api_view(['POST'])
def OTP_Verification(request):
        main = load_maintanance(request)
        if main  == True:
            user_data = {'Msg':'App Under Maintanance','status':'false'}
            return Response(user_data)
        Token_header = request.headers['Token']
        serializers=Register_OTP_Serializer(data=request.data)
        User_verification = request.data['setType']
        email = request.data['email_otp']
        if email:
            token = Token.objects.get(key = Token_header)
            try:
                user = User_Management.objects.get(user_name = token.user)
                eemail = user.Email[:4]
                eemail_last = user.Email[-6:]
                user_otp = Registration_otp.objects.get(user = user)
                msg = ""
                Activestatus = user.Activate_Status
                if user.User_Verification_Status == "logindone" and Activestatus == "1":
                    user.Activate_Status = "1"
                    user.save()
                else:
                    user.Activate_Status = "0"
                    user.save()
                try:
                    pin = Pin.objects.get(user_id = user.id )
                    if pin.pin is None:
                        msg = "NewUser"
                    else:
                        msg = "OldUser"
                except:
                    msg = "OldUser"
                if user.Email == 'pemaju02@gmail.com':
                    if int(1234) == int(email):
                        user.status = 0
                        user.save()
                        user.User_Verification_Status = User_verification
                        user.save()
                        ref_code = Referral_code.objects.get(user_id = user.id )
                        user_data={"Msg":"OTP Valid ",'status':'true','token':token.key,"userstatus":msg,"type":user.User_type,'referral_code':ref_code.referal_code,'setType':user.User_Verification_Status,'ActivateStatus':Activestatus}
                        return Response(user_data)
                if user.Email == 'test1@gmail.com':
                    if int(1234) == int(email):
                        user.status = 0
                        user.save()
                        user.User_Verification_Status = User_verification
                        user.save()
                        ref_code = Referral_code.objects.get(user_id = user.id )
                        user_data={"Msg":"OTP Valid ",'status':'true','token':token.key,"userstatus":msg,"type":user.User_type,'referral_code':ref_code.referal_code,'setType':user.User_Verification_Status,'ActivateStatus':Activestatus}
                        return Response(user_data)
                if user_otp.email_otp == int(email):
                    user.status = 0
                    user.save()
                    user.User_Verification_Status = User_verification
                    user.save()
                    ref_code = Referral_code.objects.get(user_id = user.id )
                    user_data={"Msg":"OTP Valid ",'status':'true','token':token.key,"userStatus":msg,"type":user.User_type,'referral_code':ref_code.referal_code,'setType':user.User_Verification_Status,'ActivateStatus':Activestatus}
                    return Response(user_data)
                else:
                    user_data={"Msg":" Invalid OTP ",'status':'false','token':token.key,"userStatus":msg,"type":user.User_type}
                    return Response(user_data)
            except:
                user_data={"Msg":"User Does Not Exists",'status':'false'}
                return Response(user_data)
        
        return Response(user_data)  

@api_view(['POST'])
def Pin_set(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['Token']
    User_verification = request.data['setType']
    token = Token.objects.get(key = Token_header)
    serializers=Pin_Set_Serializer(data=request.data)
    pinn = int(request.data['pin'])
    confirm_pinn = int(request.data['confirm_pin'])
    if pinn == confirm_pinn:
        user = User_Management.objects.get(user_name = token.user)
        user.User_Verification_Status = User_verification
        user.save()
        table = Pin.objects.get(user_id = user.id)
        table.pin = confirm_pinn
        table.save()
        user_data={"Msg":"Pin Updated",'status':'true','token':token.key,'Activatestatus':user.Activate_Status}
        return Response(user_data)
    else:
        user_data={"Msg":"Pin Number Does Not Match",'status':'false'}
        return Response(user_data)
    


@api_view(['POST'])
def User_Login(request):
        main = load_maintanance(request)
        if main  == True:
            user_data = {'Msg':'App Under Maintanance','status':'false'}
            return Response(user_data)
        serializers=Login_Serializer(data=request.data)
        email = request.data['Email']
        set_type = request.data['setType']
        device_unique = request.data['device_unique_id']
        try:
            user_type = request.data['User_type']
        except:
            user_data={"Msg":"Try After Sometime!!!",'status':'false'}
            return Response(user_data)
        try:            
            user = User_Management.objects.get(Email = email)
        except:
            user_count = User_Management.objects.filter(Email = email).count()
            if user_count == 0:
                user_data={"Msg":"User Does Not exists6",'status':'false'}
                return Response(user_data)
            if user_count == 1:
                user = User_Management.objects.get(Email = email)
            if user_count > 1 : 
                User_Last = User_Management.objects.values('id').get(Q(Email = email) & ~Q(phone_number=None))
                user_user = User_Management.objects.filter(Email = email).exclude(id = User_Last['id'])
                user_user.delete()
        user = User_Management.objects.get(Email = email)
        user.save()
        try:
            companyqs = Company.objects.get(id=1)
            companyname= companyqs.name
        except:
            companyqs = ''
            companyname = ''
        if int(companyqs.Device_id_status) == 0:
            dev_id = User_Management.objects.filter(Q(device_unique_id = device_unique) & ~Q(id=user.id)).count()
            if dev_id >= 1:
                if device_unique == "null":
                    user.device_unique_id=""
                    user.save()
                else:
                    user.request_device_id=device_unique
                    user.save()
                    user_data={"Msg":"This Device Is Already Login IN Another Account",'status':'false'}
                    return Response(user_data)
            elif dev_id == 0:
                if user.device_unique_id == "" or user.device_unique_id  is None:
                    user.device_unique_id=device_unique
                    user.save()
                if user.device_unique_id != device_unique:
                    user.request_device_id=device_unique
                    user.save()
                    user_data={"Msg":"Device Mismatch Kindly Login In Your Old Device",'status':'false'}
                    return Response(user_data)
        user_user = User.objects.get(username = user.user_name)
        user_id=user.id
        user_id_name=user_user
        try:
            ref_code = Referral_code.objects.get(user_id = user_id )
        except:
            size=6 
            chars=string.ascii_uppercase + string.digits
            res = ''.join(random.choice(chars) for _ in range(size)) 
            Referral_code.objects.create(user_id =user_id ,referal_code = res)
        token = Token.objects.get(user = user_id_name)
        try:            
            user_otp = Registration_otp.objects.get(user_id = user.id)
        except:
            user_otp_count = Registration_otp.objects.filter(user_id = user.id).count()
            if user_otp_count == 0:
                otp = generateOTP()
                Registrationotp(request,otp,user.id)
            if user_otp_count == 1:
                user_otp = Registration_otp.objects.get(user_id = user.id)
            if user_otp_count > 1 : 
                User_otp_Last = Registration_otp.objects.filter(user_id = user.id).last()
                user_user_otp = Registration_otp.objects.filter(user_id = user.id).exclude(id = User_otp_Last.id)
                user_user_otp.delete()
        try:
            get_user_delete = Delete_Account_Management.objects.get(user_id = user.id)
            if get_user_delete:
                user_data={"Msg":"Your Account Has been Requested to DeActivate,Please Wait for Admin Confirmation",'status':'false'}
                return Response(user_data)
        except:
            pass
        if email:
            if user_type == "IOS":
                try:
                    msg = ""
                    Activestatus = user.Activate_Status
                    if user.User_Verification_Status == "logindone" and Activestatus == "1" and user.status == 0:
                        user.Activate_Status = "1"
                        user.save()
                    else:
                        user.Activate_Status = "0"
                        user.save()
                    try:
                        pin = Pin.objects.get(user_id = user.id )
                        if pin.pin is None:
                            msg = "NewUser"
                        else:
                            msg = "OldUser"
                    except:
                        msg = "OldUser"
                    ref_code = Referral_code.objects.get(user_id = user.id )
                    user_data={"Msg":"Login Successfully",'status':'true','token':token.key,"userStatus":msg,'referral_code':ref_code.referal_code,'setType':user.User_Verification_Status,'User_type':user.User_type,'ActivateStatus':Activestatus}
                    return Response(user_data)
                except:
                    user_data={"Msg":"User Does Not exists5",'status':'false','token':token.key}
                    return Response(user_data)
            if user_type == "facebook":
                try:
                    msg = "NewUser"
                    Activestatus = user.Activate_Status
                    if user.User_Verification_Status == "logindone" and Activestatus == "1" and user.status == 0:
                        user.Activate_Status = "1"
                        user.save()
                    else:
                        user.Activate_Status = "0"
                        user.save()
                    try:
                        pin = Pin.objects.get(user_id = user.id )
                        if pin.pin is None:
                            msg = "NewUser"
                        else:
                            msg = "OldUser"
                    except:
                        msg = "OldUser"
                    ref_code = Referral_code.objects.get(user_id = user.id )
                    eemail = email[:4]
                    eemail_last = email[-6:]
                    pin = Pin.objects.get(user_id = user.id )
                    pin.pin = None
                    pin.save()
                    user_data={"Msg":"Login Successfull",'status':'true','token':token.key,'email':eemail+"******************"+eemail_last,'referral_code':ref_code.referal_code,'User_type':user.User_type,'setType':user.User_Verification_Status,'ActivateStatus':Activestatus} 
                    return Response(user_data)
                except:
                    user_data={"Msg":"User Does Not exists4",'status':'false','token':token.key}
                    return Response(user_data) 
            if user_type == "gmail" :
                try:
                    msg = "NewUser"
                    Activestatus = user.Activate_Status
                    user.User_Verification_Status = set_type
                    user.save()
                    if user.User_Verification_Status == "logindone" and Activestatus == "1" and user.status == 0:
                        user.Activate_Status = "1"
                        user.save()
                    else:
                        user.Activate_Status = "0"
                        user.save()
                    try:
                        ref_code = Referral_code.objects.get(user_id = user.id )
                        try:
                            pin = Pin.objects.get(user_id = user.id )
                            if pin.pin is None:
                                msg = "NewUser"
                            else:
                                msg = "OldUser"
                        except:
                            msg = "OldUser"
                        eemail = email[:4]
                        eemail_last = email[-6:]
                        user_data= {"Msg":"Login Successfull",'status':'true','token':token.key,'email':eemail+"******************"+eemail_last,'referral_code':ref_code.referal_code,'User_type':user.User_type,"userStatus":msg,'setType':user.User_Verification_Status,'ActivateStatus':Activestatus} 
                        return Response(user_data)
                    except:
                        user_id = user.id
                        otp = generateOTP()
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
                        table=User_two_fa(user_secrete_key=totp,user_totp=h,user_htotp=p,user= user)
                        table.save()
                        ref_code = Referral_code.objects.get(user_id = user.id )
                        try:
                            pin = Pin.objects.get(user_id = user.id )
                            if pin.pin is None:
                                msg = "NewUser"
                            else:
                                msg = "OldUser"
                        except:
                            msg = "OldUser"
                        eemail = email[:4]
                        eemail_last = email[-6:]
                        pin =Pin.objects.get(user_id = user.id )
                        pin.pin = None
                        pin.save()
                    user_data= {"Msg":"Login Successfull",'status':'true','token':token.key,'email':eemail+"******************"+eemail_last,'referral_code':ref_code.referal_code,'User_type':user.User_type,"userStatus":msg,'setType':user.User_Verification_Status,'ActivateStatus':Activestatus} 
                    return Response(user_data)
                except:
                    user_data={"Msg":"User Does Not exists3",'status':'false','token':token.key}
                    return Response(user_data)  
            if user_type == "normaluser":
                if user.status != 2:
                    try:
                        companyqs = Company.objects.get(id=1)
                        companyname= companyqs.name
                    except:
                        companyqs = ''
                        companyname = ''
                    try:               
                        get_user = User_Management.objects.get(Email = email)
                        otp = generateOTP()
                        try:
                            user_otp = Registration_otp.objects.get(user_id = get_user.id)
                            user_otp.email_otp = otp
                            user_otp.save() 
                        except:
                            user_id = get_user.id
                            otp = generateOTP()
                            Registrationotp(request,otp,user_id)
                        get_user.User_Verification_Status = set_type
                        get_user.save() 
                        emailtemplate = get_email_template(request,6)
                        to_email = email
                        data= {
                            'user':get_user.id,
                            'username':get_user.Name,
                            'email':email,
                            'domain':settings.DOMAIN_URL,
                            'company_name':companyname,
                            'otp':otp,
                            }
                        htmly = get_template('emailtemplate/login_alert.html')
                        html_content = htmly.render(data)
                        response = requests.post(
                        "https://api.mailgun.net/v3/jasanwellness.fit/messages",
                        auth=("api",  decrypt_with_common_cipher(settings.MAIL_API)),
                        data={"from": "WEB3 WELLNESS <noreply@jasanwellness.fit>",
                        "to": [to_email],
                        "subject": emailtemplate.Subject,
                        "html": html_content})
                        eemail = email[:4]
                        eemail_last = email[-6:]
                        ref_code = Referral_code.objects.get(user_id = user.id )
                        user_data={"Msg":"OTP Sent Successfully",'status':'true','token':token.key,'email':eemail+"******************"+eemail_last,'referral_code':ref_code.referal_code,'User_type':"normaluser",'setType':get_user.User_Verification_Status}  
                        return Response(user_data) 
                    except Exception as e :
                        user_data={"Msg":"Mail Server Problem !.Please Try Again Later"+str(e),'status':'false','token':token.key}
                        return Response(user_data) 
                else:   
                    user_data={"Msg":"Unusual Activity",'status':'false','token':token.key}
                    return Response(user_data)   
        else:   
            user_data={"Msg":"User Does Not exists1",'status':'false','token':token.key}
            return Response(user_data)            
        return Response(user_data)    


@api_view(['POST'])
def Profile_data_giving(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    address_change_status=''
    instruction=''
    try:
        user_Deatail=User_Management.objects.get(user_name = token.user)
    except:
        user_Deatail=''
        user_data={"Msg":"Data Not Found",'status':'false'}
        return Response(user_data)
    user_wallet=user_address_trust_wallet.objects.filter(user_id = user_Deatail.id).count()
    if int(user_wallet) != 0:
        user_wallet=user_address_trust_wallet.objects.get(user_id = user_Deatail.id)
        user_wallet_cre=datetime.strftime(user_wallet.created_on,"%m/%d/%Y, %H:%M:%S")
        user_wallet_mod=datetime.strftime(user_wallet.modified_on,"%m/%d/%Y, %H:%M:%S")
        if str(user_wallet_cre) == str(user_wallet_mod):
            # address_change_status = False
            # instruction='You can update wallet address once,  please check it cannot be updated again in future'
            address_change_status = True
            instruction=''
        else:
            address_change_status = True
            instruction=''
    else:
        pass
    serializers=user_DeatailSerializers(user_Deatail,many=False)
    user_data={"Data":serializers.data,"Msg":"Data Found",'status':'true','token':token.key,"address_change_status":address_change_status,"instruction":instruction}
    return Response(user_data)

@api_view(['POST'])
def Profile_Update(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    try:
        user_detail = User_Management.objects.get(user_name = token.user)
        user = request.data['user_name']
        Name = request.data['Name']
        Email = request.data['Email']
        user_profile_pic = request.data['user_profile']
        Phone_Number = request.data['Phone_Number']
        i = Phone_Number.split()
        if i[0].isnumeric() == False:
            user_data={"Msg":"Enter Only Numbers",'status':'false'}
            return Response(user_data)
        if i[1].isnumeric() == False:
            user_data={"Msg":"Enter Only Numbers",'status':'false'}
            return Response(user_data)
        Phone_Number_Count = User_Management.objects.filter(user_phone_number = Phone_Number).exclude(user_name = token.user).count()
        if Phone_Number_Count > 0 :
            user_data={"Msg":"Phone Number Already Exists",'status':'false'}
            return Response(user_data)
        Email_count = User_Management.objects.filter(Email = Email).exclude(user_name = token.user).count()
        if Email_count > 0 :
            user_data={"Msg":"Email Already Exists",'status':'false'}
            return Response(user_data)
        if user != "":
            user_detail.user_name = user
        else :
            user_detail.user_name = user_detail.user_name
        if Name != "":
            user_detail.Name = Name
        else:
            user_detail.Name = user_detail.Name
        if Email != "" :
            user_detail.Email = Email
        else:
            user_detail.Email = user_detail.Email
        if user_profile_pic != "":
            user_detail.user_profile =user_profile_pic
        else:
            user_detail.user_profile = user_detail.user_profile
        if Phone_Number != "":
            user_detail.user_phone_number = Phone_Number
        else:
            user_detail.user_phone_number = user_detail.user_phone_number
        user_detail.save()
        user_data={"Msg":"Data Updated",'status':'true','token':token.key}
    except:
        user_data={"Msg":"Data Not Updated",'status':'false'}
    
    return Response(user_data)



        
@api_view(['POST'])
def two_fa(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key= Token_header)
    try:
        user_details = User_Management.objects.get(user_name = token.user)
        user = User_two_fa.objects.get(user = user_details.id)
        if user.user_status == 'disable':
            serializer = two_fa_Serializers(data = request.data)
            if serializer.is_valid:
                a=user.user_secrete_key
                o=request.data['user_totp']
                totp = pyotp.TOTP(a)
                b=totp.now()
                try:
                    if int(o) == int(b):
                        user.user_status = 'enable'
                        user.save()
                        user_data={"Msg":"TFA Enabled",'status':'true','token':token.key}
                    else:
                        user_data={"Msg":"OTP Does not match",'status':'false','token':token.key}
                except:
                    user_data={"Msg":"Error Occured",'status':'false','token':token.key}
        else:
            user_data={"Msg":"TFA Already Enabled",'status':'true','token':token.key}

    except:
        user_data={"Msg":"Error Occured",'status':'false','token':token.key}

    return Response(user_data)


@api_view(['POST'])
def two_fa_disable(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key= Token_header)
    try:
        user_details = User_Management.objects.get(user_name = token.user)
        user = User_two_fa.objects.get(user = user_details.id)
        if user.user_status == 'enable':
            serializer = two_fa_Serializers(data = request.data)
            if serializer.is_valid:
                a=user.user_secrete_key
                o=request.data['user_totp']
                totp = pyotp.TOTP(a)
                b=totp.now()
                try:
                    if int(o) == int(b):
                        user.user_status = 'disable'
                        user.save()
                        user_data={"Msg":"TFA Disabled",'status':'true','token':token.key}
                    else:
                        user_data={"Msg":"OTP Does not match",'status':'false','token':token.key}
                except:
                    user_data={"Msg":"Error Occured",'status':'false','token':token.key}
        else:
            user_data={"Msg":"TFA Already Disabled",'status':'true','token':token.key}

    except:
        user_data={"Msg":"Error Occured",'status':'false'}

    return Response(user_data)




@api_view(['POST'])
def Google_fitness(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key= Token_header)   
    serializer = Google_fitness_Serializers(data = request.data)
    status = request.data['Google_status']
    mail = request.data['Mail']
    try:
        user_details = User_Management.objects.get(user_name = token.user)
        google = Google_Fitness.objects.get(user = user_details.id)
        if google.mail == mail and  google.Google_status == 'enable':
            user_data={"Msg":"This Gmail Has Already Been Activated",'status':'false','token':token.key}
            return Response(user_data)
        else:
            google.mail = mail
            google.Google_status = 'enable'
            google.save()
            user_data={"Msg":"Status Updated",'status':'true','token':token.key}
            return Response(user_data)
    except:
        user_data={"Msg":"User Does Not Exists",'status':'false','token':token.key}
        return Response(user_data)


@api_view(['POST'])
def step_count(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key= Token_header)
    serializer = step_count_Serializers(data = request.data)
    # step_count = request.data['over_all_stepcount']
    if serializer.is_valid :
        user_details = User_Management.objects.get(user_name = token.user)
        # user_details.over_all_stepcount = step_count
        user_details.save()
        user_data={"Msg":"Step Count Updated",'status':'true','token':token.key}
        return Response(user_data)
    else:
        user_data={"Msg":"Pass The Data Correctly",'status':'false'}
    return Response(user_data)


@api_view(['POST']) 
def reward_footsteps_two(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['Token']
    set_type_data = int(request.data['ActivateStatus'])
    token = Token.objects.get(key= Token_header)
    user_details = User_Management.objects.values('User_type','plan','id','Two_X_Boost_status','created_on','plan_end_date','User_Verification_Status','Activate_Status','User_Target','Name','Email','withdraw_count','status','plan_start_date','fixed_status').get(user_name = token.user)
    User_type = user_details['User_type']
    plan_status = user_details['plan']
    page_details = request.data['page_details']
    created_on = str(user_details['created_on'])
    plan_start_date = user_details['plan_start_date']
    msg = ""
    User_plan_status = ""
    plan_end_date = ""
    plan_status_data = ""
    Wallet_status = "Not Flushed"
    twoX_Boost_status = 0
    Plan_reward = 0
    Plan_Step = 0
    user_id = user_details["id"]
    status=user_details["status"]
    stake_credit=""
    monthly_support=""
    quarterly_support=""
    annual_support=""
    support_address=""
    monthly_support_amount=""
    quarterly_support_amount=""
    halfyearly_support_amount=""
    annual_support_amount=""
    homepage_monthly_support="0"
    homepage_quarterly_support=""
    homepage_halfyearly_support=""
    homepage_annual_support=""
    homepage_monthly_support_amount=""
    homepage_quarterly_support_amount=""
    homepage_halfyearly_support_amount=""
    homepage_annual_support_amount=""
    homepage_support_status=""
    today=datetime.now()
    try:
        companyqs = Company.objects.get(id=1)
        companyname= companyqs.name
    except:
        companyqs = ''
        companyname = ''
    try:
        wallet_trust=user_address_trust_wallet.objects.get(user_id=user_id)
    except:
        wallet_trust='' 
    if page_details == "Home_page":
        withdraw_popup=""
        stake_withdraw_popup=""
        market_price_popup="1"
        fixed_api_price=""
        market_api_price=""
        reward_claim_status="1"
        market_price_details = market_price.objects.get(id = 1)
        if user_details['fixed_status']  == "":
                if str(today) >= str(user_details['plan_end_date']):
                    market_price_popup = "0"
                    fixed_api_price = market_price_details.market_price
                    market_api_price = companyqs.market_api_price
        elif user_details['fixed_status'] == "fixed" :
            if str(user_details['plan_end_date']) <= "2023-12-17 23:59:59.000000":
                if str(today) >= str(user_details['plan_end_date']):
                    market_price_popup = "0"
                    fixed_api_price = market_price_details.market_price
                    market_api_price = companyqs.market_api_price
            else:
                fixed_api_price = market_price_details.market_price
        elif user_details['fixed_status'] == "market":
            market_api_price = companyqs.market_api_price
        else:
            market_price_popup = "1"
        chk_data_login = LoginHistory.objects.filter(user = user_id).count()
        login_date_chk=""
        if int(chk_data_login) != "0":
            t_day = date.today()
            try:
                chk_data = LoginHistory.objects.filter(user = user_id).exclude(created_on__date__gte = t_day).last()
                login_date_chk=str(chk_data.created_on.date())
            except:
                login_date_chk=""
        if login_date_chk  != "" :     
            reward=Reward_History.objects.filter(user = user_details['id'],created_on__date=login_date_chk)
            if reward:
                reward_claim_status= "1"
            else:
                if str(today) >= str(user_details['plan_end_date']):
                    reward_claim_status= "1"
                else:
                    reward_claim_status= "0"      
        Plan_his = plan_purchase_history.objects.filter(user_id = user_id).last()
        Plan = plan.objects.get(plan_type = 0)
        try:
            withdraw_supp=WithdrawSendUSDTHistory.objects.get(email_id=user_id)
        except:
            withdraw_supp=""
        date_now=datetime.now()
        if withdraw_supp != "":
            if withdraw_supp.plan_end_date <= date_now:
                support_status="1"
            else:
                support_status="1"
        else:
            if plan_status == 0:
                support_status='1'
            else:
                support_status="1"
        if Plan_his != '' and Plan_his != None:
            monthly_support=Plan_his.monthly_support
            quarterly_support=Plan_his.quarterly_support
            annual_support=Plan_his.annual_support
            monthly_support_amount=Plan_his.monthly_support_amount
            quarterly_support_amount=Plan_his.quarterly_support_amount
            halfyearly_support_amount=Plan_his.halfyearly_support_amount
            annual_support_amount=Plan_his.annual_support_amount
            homepage_monthly_support=Plan_his.monthly_support
            homepage_quarterly_support=Plan_his.quarterly_support
            homepage_halfyearly_support=Plan_his.halfyearly_support
            homepage_annual_support=Plan_his.annual_support
            homepage_monthly_support_amount=Plan_his.monthly_support_amount
            homepage_quarterly_support_amount=Plan_his.quarterly_support_amount
            homepage_halfyearly_support_amount=Plan_his.halfyearly_support_amount
            homepage_annual_support_amount=Plan_his.annual_support_amount
            support_address=companyqs.support_address
        if  str(today) <= str(user_details['plan_end_date'])  :
            if withdraw_supp != "":
                if withdraw_supp.plan_end_date <= date_now:
                    homepage_support_status=Plan_his.support_status
                else:
                    homepage_support_status="1"
            else:
                homepage_support_status="1"
        else:
            homepage_support_status="1"
        user_status = status
        if wallet_trust:
            if wallet_trust.wallet_type == "admin blocked":
                trust_add="You are currently blocked!!!"
                Wallet_connect_status= True
            else:
                trust_add=wallet_trust.Address
                Wallet_connect_status= True
        else:
            trust_add=0
            Wallet_connect_status= False
        support_address=companyqs.support_address
        DAta = UserCashWallet.objects.get(userid_id = user_details['id'])
        stake_credit=DAta.balancetwo
        stake_withdraw_popup="Monthly"
        if  DAta.balanceone == 0 and DAta.referalincome == 0 :
            Wallet_status = "Flushed"
        if  DAta.balanceone < 0:
            Wallet_status = "Flushed"
        if  DAta.referalincome < 0:
            Wallet_status = "Flushed"
        balance = (DAta.balanceone) + (DAta.referalincome)
        if (balance) == 0.00000000:
            balance = 0
        health_reward = Decimal(DAta.balanceone)
        if (health_reward) == 0.00000000:
            health_reward = 0
        if plan_status != 0: 
            Plan = plan_purchase_history.objects.filter(user_id = user_details['id']).last()
            plan_status_data = Plan.plan_id.plan_name
            twoX_Boost_status = Plan.Plan_Two_X_Boost_status
            Plan_reward = Plan.Plan_maximum_reward
            Plan_Step = Plan.Plan_maximum_step
            User_plan_status = "Active"
            plan_end_date = user_details['plan_end_date']
            plan_amt = Plan.purchase_amount
            if plan_status == 64:
                if str(plan_start_date)  >= "2023-10-28 12:30:00.000000":
                    withdraw_popup="Monthly"
                else:
                    withdraw_popup="Daily"
            else:
                if str(plan_start_date)  >= "2023-10-18 13:00:00.000000":
                    withdraw_popup="Monthly"
                else:
                    withdraw_popup="Daily"
        else:
            Plan = plan.objects.get(plan_type = 0)
            plan_status_data = "Free Plan"
            twoX_Boost_status = user_details['Two_X_Boost_status']
            Plan_reward = Plan.reward_amount
            Plan_Step = Plan.Max_step_count
            User_plan_status = "NotActive"
            plan_amt = Plan.plan_purchase_amount
            if user_details['created_on'] == user_details['plan_end_date']:
                date_one = user_details['created_on'] + timedelta(step_management.free_plan_days)
                user_details['plan_end_date'] = date_one
                User_Management.objects.filter(user_name = token.user).update(plan_end_date = date_one)
            plan_end_date = user_details['plan_end_date']
        stake = staking_admin_management.objects.using('second_db').get(id = 1)
        stake_plan = plan.objects.get(id = stake.eligible_plan)
        stake_eligible_plan = stake_plan.plan_name
        if plan_amt >= stake_plan.plan_purchase_amount:
            if user_details['plan_end_date'] >= datetime.now():
                stake_eligible = 'Eligible'
            else:
                stake_eligible = 'Not_Eligible'
        else:
            stake_eligible = 'Not_Eligible'
        stake_wallet_admin = stake_wallet_management.objects.using('second_db').filter(user = user_details['id']).count()
        if stake_wallet_admin > 1:
            his_id = stake_wallet_management.objects.using('second_db').filter(user = user_details['id']).last()
            user_reward = stake_wallet_management.objects.using('second_db').filter(user = user_details['id']).exclude(id = his_id.id)
            user_reward.delete()
        wallet_Type = 3
        if user_details['plan_end_date'] > datetime.now():
            diff_chk = user_list_for_update(request,user_details['id'],wallet_Type)
            if wallet_Type == 3:
                if Decimal(diff_chk['total']) != 0.00000000 or Decimal(diff_chk['ref_diff']) != 0.00000000:
                    user_list_reward_update(request,user_details['id'])
        if user_details['User_Verification_Status'] != "logindone" or user_details['Activate_Status'] != "1":
            if set_type_data == 1:
                user_details['User_Verification_Status'] = "logindone"
                user_details['Activate_Status'] = "1"
                User_Management.objects.filter(user_name = token.user).update(User_Verification_Status = "logindone",Activate_Status = "1")
            if set_type_data == 0:
                User_Management.objects.filter(user_name = token.user).update(withdraw_count = 2)
        user_list_for_stake_update(request,user_details['id'])
        Premium_wallet_blance(request,user_details['id'])
        status = Market_place.objects.get(id =1)
        market_status = status.Google_status
        internal_transfer = status.internal_transfer
        company = Company.objects.get(id = 1)
        plan_buy_status_object = admin_referral_code.objects.get(id = 1)
        plan_buy_status = plan_buy_status_object.status
        step_management = Steps_Management.objects.get(id = 1) 
        Jw_time_line = 0
        Staking = 1
        user_data={"balance":str(balance),'healthreward': (health_reward) ,'Referral_balance':Decimal(DAta.referalincome),'stake_credit':Decimal(stake_credit),'status':'true','token':token.key,"Wallet_flush_status":Wallet_status,"target":user_details['User_Target'],'User_plan_status':User_plan_status,'plan_buy_status':plan_buy_status,'twoX_Boost_status':twoX_Boost_status,"user_name":user_details['Name'],'user_id':user_details['id'],"Plan_reward":Plan_reward,"plan_end_date":plan_end_date,"Version":company.Android_version,"IOSVersion":company.IOS_version,"step_discount":step_management.Step_discount,'Device_step_counter_discount':step_management.Step_counter_Discount,"plan_status_data":plan_status_data,'Market_status':market_status,'internal_transfer_status':internal_transfer,"step_counter":user_details['withdraw_count'],'Activte_plan_status' : step_management.plan_active_status,'stake_eligible':stake_eligible,'stake_eligible_plan':stake_eligible_plan,'Plan_Step':Plan_Step,"Jw_time_line" : Jw_time_line,'Staking':Staking,"connect_status":Wallet_connect_status,"wallet_address":str(trust_add).lower(),"user_status":user_status,'reward_claim_status':reward_claim_status,'support_status':support_status,'support_quater':monthly_support,'support_half':quarterly_support,'support_full':annual_support,'support_send_address':support_address,'withdraw_popup':withdraw_popup,'stake_withdraw_popup':stake_withdraw_popup,'monthly_support_amount':monthly_support_amount,'quarterly_support_amount':quarterly_support_amount,'halfyearly_support_amount':halfyearly_support_amount,'annual_support_amount':annual_support_amount,"market_price_popup":market_price_popup,'fixed_api_price':fixed_api_price,'market_api_price':market_api_price,'homepage_monthly_support':homepage_monthly_support,'homepage_quarterly_support':homepage_quarterly_support,'homepage_halfyearly_support':homepage_halfyearly_support,'homepage_annual_support':homepage_annual_support,'homepage_monthly_support_amount':homepage_monthly_support_amount,'homepage_quarterly_support_amount':homepage_quarterly_support_amount,'homepage_halfyearly_support_amount':homepage_halfyearly_support_amount,'homepage_annual_support_amount':homepage_annual_support_amount,'homepage_support_status':homepage_support_status}
        return Response(user_data) 
    if page_details == "wallet_page":
        market_price_= market_price.objects.get(id = 1)
        market_price_details=market_price_.market_price
        if user_details['fixed_status'] == "fixed" :
            market_price_details = market_price_.market_price
        elif user_details['fixed_status'] == "market":
            market_price_details = companyqs.market_api_price
        try:
            plan_supp=WithdrawSendUSDTHistory.objects.filter(email_id=user_id).last()
        except:
            plan_supp=""
        date_now=datetime.now()
        if plan_supp != None:
            if plan_supp.plan_end_date <= date_now:
                plan_support_status="0"
            else:
                plan_support_status="1"
        else:
            if plan_status == 0:
                plan_support_status="0"
            else:
                plan_support_status="0"
        if wallet_trust:
            if wallet_trust.wallet_type == "admin blocked":
                trust_add="You are currently blocked!!!"
                Wallet_connect_status= True
            else:
                trust_add=wallet_trust.Address
                Wallet_connect_status= True
        else:
            trust_add=0
            Wallet_connect_status= False
        DAta = UserCashWallet.objects.get(userid_id = user_details['id'])
        stake_credit=DAta.balancetwo
        premium_wallet=DAta.Premiumwallet
        premium_market_price=companyqs.market_api_price
        if  DAta.balanceone == 0 and DAta.referalincome == 0 :
            Wallet_status = "Flushed"
        balance = (DAta.balanceone) + (DAta.referalincome)
        if (balance) == 0.00000000:
            balance = 0
        health_reward = Decimal(DAta.balanceone)
        if (health_reward) == 0.00000000:
            health_reward = 0
        premium_wallet_man = premium_wallet_management.objects.get(id = 1)
        if user_details['fixed_status'] == "fixed":
            premium_deposit_status = premium_wallet_man.fixed_status
        elif user_details['fixed_status'] == "market":
            premium_deposit_status = premium_wallet_man.market_status
        elif user_details['fixed_status'] == "":
            premium_deposit_status = premium_wallet_man.fixed_status
        minimum_BNB_Balance = withdraw_values.objects.get(id = 1)
        stake_price_details = Stake_market_price.objects.using('second_db').get(id = 1)
        internal_transfer_fee = internal_transfer_admin_management.objects.using('second_db').get(id = 1)
        user_data={"balance":str(balance),'healthreward': (health_reward) ,'Referral_balance':Decimal(DAta.referalincome),'stake_credit':Decimal(stake_credit),"minimum_BNB_Balance":str(minimum_BNB_Balance.Minimum_BNB_Balance),"step_counter":user_details['withdraw_count'],'market_price_details':market_price_details,'internal_transfer_fee': internal_transfer_fee.transaction_fees,'status':'true',"connect_status":Wallet_connect_status,"wallet_address":str(trust_add).lower(),"stake_marketprice":stake_price_details.market_price,"plan_support_status":plan_support_status,'premium_wallet':premium_wallet,'premium_market_price':premium_market_price,'premium_max_limit':premium_wallet_man.premium_max_limit,'premium_min_limit':premium_wallet_man.premium_min_limit,'premium_deposit_status':premium_deposit_status}
        return Response(user_data)  
    if page_details == "security_page":
        if wallet_trust:
            if wallet_trust.wallet_type == "admin blocked":
                trust_add="You are currently blocked!!!"
                Wallet_connect_status= True
            else:
                trust_add=wallet_trust.Address
                Wallet_connect_status= True
        else:
            trust_add=0
            Wallet_connect_status= False
        DAta = UserCashWallet.objects.get(userid_id = user_details['id'])
        balance = (DAta.balanceone) + (DAta.referalincome)
        if (balance) == 0.00000000:
            balance = 0
        if User_type == "gmail":
            try:
                pin = Pin.objects.get(user_id = user_details['id'] )
                if pin.pin is None:
                    msg = "NewUser"
                else:
                    msg = "OldUser"
            except:
                msg = "OldUser"
        if User_type == "facebook":
            try:
                pin = Pin.objects.get(user_id = user_details['id'] )
                if pin.pin is None:
                    msg = "NewUser"
                else:
                    msg = "OldUser"
            except:
                msg = "OldUser"
        try:
            status = User_two_fa.objects.get(user_id = user_details['id'] )
        except:
            totp = pyotp.random_base32()
            h=pyotp.totp.TOTP(totp).provisioning_uri(name=str(user_details['Email']), issuer_name='Jasan Wellness')
            p=pyotp.parse_uri(h)
            user_details_object = User_Management.objects.get(user_name = token.user)
            status=User_two_fa(user_secrete_key=totp,user_totp=h,user_htotp=p,user= user_details_object)
            status.save()
        user_twofa = status.user_status
        user_data={'status':'true','token':token.key,'twofa_status':user_twofa,"balance":str(balance),"User_type":User_type,"userStatus":msg,'Referral_balance':Decimal(DAta.referalincome),"connect_status":Wallet_connect_status,"wallet_address":str(trust_add).lower()}
        return Response(user_data)
    if page_details == "Withdraw_page":
        referral_marketprice=""
        referal_user_status=""
        market_price_details = market_price.objects.get(id = 1)
        if user_details['fixed_status']  == "market":
            referal_user_status="new_user"
            referral_marketprice=companyqs.market_api_price
            market_price_detailss=companyqs.market_api_price
        elif user_details['fixed_status']  == "fixed":
            referal_user_status="old_user"
            referral_marketprice=market_price_details.market_price
            market_price_detailss=market_price_details.market_price
        elif user_details['fixed_status']  == "":
            referal_user_status="old_user"
            referral_marketprice=market_price_details.market_price
            market_price_detailss=market_price_details.market_price
        if wallet_trust:
            if wallet_trust.wallet_type == "admin blocked":
                trust_add="You are currently blocked!!!"
                Wallet_connect_status= True
            else:
                trust_add=wallet_trust.Address
                Wallet_connect_status= True
        else:
            trust_add=0
            Wallet_connect_status= False
        try:
            user_plan = plan_purchase_history.objects.filter(user_id = user_id).last()
        except:
            user_plan=""
        if user_plan:
            stake_monthly_deduction=user_plan.stake_wallet_monthly_split_percentage
            trust_wallet_deduction=user_plan.withdraw_wallet_monthly_split_percentage
        else:
            stake_monthly_deduction=""
            trust_wallet_deduction=""
        DAta = UserCashWallet.objects.get(userid_id = user_details['id'])
        if  DAta.balanceone == 0 and DAta.referalincome == 0 :
            Wallet_status = "Flushed"
        balance = (DAta.balanceone) + (DAta.referalincome)
        if (balance) == 0.00000000:
            balance = 0
        health_reward = Decimal(DAta.balanceone)
        if (health_reward) == 0.00000000:
            health_reward = 0
        if User_type == "gmail":
            try:
                pin = Pin.objects.get(user_id = user_details['id'] )
                if pin.pin is None:
                    msg = "NewUser"
                else:
                    msg = "OldUser"
            except:
                msg = "OldUser"
        if User_type == "facebook":
            try:
                pin = Pin.objects.get(user_id = user_details['id'] )
                if pin.pin is None:
                    msg = "NewUser"
                else:
                    msg = "OldUser"
            except:
                msg = "OldUser"
        try:
            status = User_two_fa.objects.get(user_id = user_details['id'] )
        except:
            totp = pyotp.random_base32()
            h=pyotp.totp.TOTP(totp).provisioning_uri(name=str(user_details['Email']), issuer_name='Jasan Wellness')
            p=pyotp.parse_uri(h)
            user_details_object = User_Management.objects.get(user_name = token.user)
            status=User_two_fa(user_secrete_key=totp,user_totp=h,user_htotp=p,user= user_details_object)
            status.save()
        user_twofa = status.user_status
        minimum_BNB_Balance = withdraw_values.objects.get(id = 1)
        # Step_his = Withdraw.objects.filter(userid_id = user_details['id'],created_on__date = (date.today())).count()
        # if Step_his > 1:
        #     his_id = Withdraw.objects.filter(userid_id = user_details['id'],created_on__date =(date.today())).last()
        #     user_reward = Withdraw.objects.filter(userid_id = user_details['id'],created_on__date =(date.today())).exclude(id = his_id.id)
        #     user_reward.delete()
        #     user_list_reward_update(request,user_details['id'])
        stake_price_details = Stake_market_price.objects.using('second_db').get(id = 1)
        admin_stake = staking_admin_management.objects.using('second_db').get(id = 1)
        admin_stake_credit = staking_monthly_admin_management.objects.using('second_db').get(id = 1)
        # stake_wallet = stake_wallet_management.objects.using('second_db').get(user = user_details['id'])
        try:
            stake_wallet = stake_wallet_management.objects.using('second_db').get(user=user_details['id'])
            stake_Wallet_wallet = stake_wallet.stake_Wallet
            stake_Wallet_withdraw = stake_wallet.stake_withdraw_Wallet
            stake_Refferal_Wallet = stake_wallet.stake_Refferal_Wallet
        except stake_wallet_management.DoesNotExist:
            # Handle the case where the record is not found
            print('Stake wallet not found for user:', user_details['id'])
            stake_wallet = None
            stake_Wallet_wallet = None
            stake_Wallet_withdraw = None
            stake_Refferal_Wallet = None
        
        
        
        stake_credit_withdraw_balance=stake_wallet.stake_credit_withdraw_Wallet
        stake_credit_marketprice=companyqs.market_api_price
        principle_amount=user_plan.purchase_amount
        user_data={"balance":str(balance),'healthreward': (health_reward) ,'Referral_balance':Decimal(DAta.referalincome),"minimum_BNB_Balance":minimum_BNB_Balance.Minimum_BNB_Balance,"userStatus":msg,"User_type":User_type,'twofa_status':user_twofa,'Email':user_details['Email'],'stake_Wallet': stake_Wallet_wallet,'stake_withdraw_Wallet':stake_Wallet_withdraw,'stake_Refferal_Wallet':stake_Refferal_Wallet,'market_price_details':market_price_detailss,"stake_withdraw_fees":admin_stake.stake_withdraw_transaction_fee ,'stake_wallet_percentage':admin_stake.stake_wallet_percentage,'withdraw_wallet_percentage':admin_stake.withdraw_wallet_percentage,'status':'true',"connect_status":Wallet_connect_status,"wallet_address":str(trust_add).lower(),'stake_monthly_deduction':stake_monthly_deduction,'trust_wallet_deduction':trust_wallet_deduction,"stake_marketprice":stake_price_details.market_price,'referral_marketprice':referral_marketprice,'referal_user_status':referal_user_status,"stake_credit_marketprice" :stake_credit_marketprice,'stake_credit_withdraw_balance':stake_credit_withdraw_balance,'stake_credit_withdraw_fees':admin_stake_credit.stake_withdraw_transaction_fee,'stake_credit_wallet_percentage':admin_stake_credit.stake_wallet_percentage,'principle_amount':principle_amount}
        
        return Response(user_data)
    
    # if page_details == "staking_page":
    #     stake_marketprice=""
    #     active_stake_amount=""
    #     stake_withdraw_max_limit=""
    #     stake_referral_max_limit=""
    #     if wallet_trust:
    #         if wallet_trust.wallet_type == "admin blocked":
    #             trust_add="You are currently blocked!!!"
    #             Wallet_connect_status= True
    #         else:
    #             trust_add=wallet_trust.Address
    #             Wallet_connect_status= True
    #     else:
    #         trust_add=0
    #         Wallet_connect_status= False
            
    #     DAta = UserCashWallet.objects.get(userid_id = user_details['id'])
    #     stake_credit_balance = DAta.balancetwo
    #     if  DAta.balanceone == 0 and DAta.referalincome == 0 :
    #         Wallet_status = "Flushed"
    #     balance = (DAta.balanceone) + (DAta.referalincome)
    #     if (balance) == 0.00000000:
    #         balance = 0
    #     health_reward = Decimal(DAta.balanceone)
    #     if (health_reward) == 0.00000000:
    #         health_reward = 0
    #     market_price_details = market_price.objects.get(id = 1)
    #     stake_price_details = Stake_market_price.objects.using('second_db').get(id = 1)

    #     # stake_wallet = stake_wallet_management.objects.using('second_db').get(user = user_details['id'])
    #     try:
    #         stake_wallet = stake_wallet_management.objects.using('second_db').get(user=user_details['id'])
    #         stake_Wallet_wallet = stake_wallet.stake_Wallet
    #         stake_Wallet_withdraw = stake_wallet.stake_withdraw_Wallet
    #         stake_Refferal_Wallet = stake_wallet.stake_Refferal_Wallet
    #     except stake_wallet_management.DoesNotExist:
    #         # Handle the case where the record is not found
    #         stake_Wallet_wallet = 0
    #         stake_Wallet_withdraw = 0
    #         stake_Refferal_Wallet = 0
    #     stake_percent=staking_admin_management.objects.using('second_db').get(id=1)
    #     stake_withdraw_max_limit=stake_percent.maximum_withdraw
    #     stake_referral_max_limit=stake_percent.maximum_withdraw_referal
    #     stake_hisss = Stake_history_management.objects.using('second_db').filter(user = user_details['id']).last()
    #     stake_marketprice=stake_price_details.market_price
    #     active_stake_amount=""
    #     stake_deposit_price=stake_price_details.market_price
    #     if stake_hisss != None:
    #         if str(stake_hisss.start_date) <= "2023-10-30 00:00:00.000000":
    #             active_stake_amount=stake_hisss.Amount_USDT
    #             stake_marketprice=stake_hisss.market_price
    #         else:
    #             stake_marketprice=stake_price_details.market_price
    #             active_stake_amount=stake_hisss.Amount_USDT
    #     try:
    #         stake_his = Stake_history_management.objects.using('second_db').get(user = user_details['id'],status=0)
    #         if stake_his.end_date > datetime.now():
    #             mod_date = stake_his.modified_on.date() 
    #             today = date.today()
    #             date_date = (today - mod_date)
    #             date_count = int(date_date.days)
    #             if date_count != 0:
    #                 stake_reward_status = "Not_Claimed"
    #             else:
    #                 mod = stake_his.modified_on.time()
    #                 now = datetime.now().time()
    #                 dateTimeA = datetime.combine(date.today(), mod)
    #                 dateTimeB = datetime.combine(date.today(), now)
    #                 dateTimeDifference = dateTimeB - dateTimeA
    #                 total_diff = int(dateTimeDifference.total_seconds())
    #                 if total_diff != 0:
    #                     stake_reward_status = "Not_Claimed"
    #                 else:
    #                     stake_reward_status = "Claimed"
    #         else:
    #             mod = stake_his.modified_on.time()
    #             now = stake_his.end_date.time()
    #             dateTimeA = datetime.combine(date.today(), mod)
    #             dateTimeB = datetime.combine(date.today(), now)
    #             dateTimeDifference = dateTimeB - dateTimeA
    #             total_diff = int(dateTimeDifference.total_seconds())
                
    #             if total_diff != 0:
    #                 stake_reward_status = "Not_Claimed"
    #             else:
    #                 stake_reward_status = "Claimed"
    #     except:
    #         stake_his = Stake_history_management.objects.using('second_db').filter(user = user_details['id']).last()
    #         stake_his_credit = Stake_monthly_history_management.objects.using('second_db').filter(user = user_details['id']).last()
    #         if stake_his != None:
    #             if stake_his.reward_earned != stake_his.maximum_reward:
    #                 stake_reward_status = "Not_Claimed"
    #             else:
    #                 stake_reward_status = ""
    #         else:
    #             stake_reward_status = ""
    #         if stake_his_credit != None:
    #             if stake_his_credit.reward_earned != stake_his_credit.maximum_reward:
    #                 stake_reward_status = "Not_Claimed"
    #             else:
    #                 stake_reward_status = ""
    #         else:
    #             stake_reward_status = ""
    #     user_data={"balance":str(balance),'healthreward': (health_reward) ,'Referral_balance':Decimal(DAta.referalincome),'market_price_details':market_price_details.market_price,'stake_Wallet': stake_Wallet_wallet,'stake_withdraw_Wallet':stake_Wallet_withdraw,'stake_Refferal_Wallet':stake_Refferal_Wallet,'status':'true','stake_reward_status':stake_reward_status,"connect_status":Wallet_connect_status,"wallet_address":str(trust_add).lower(),"stake_credit_balance":stake_credit_balance,'active_stake_amount':active_stake_amount,'stake_withdraw_max_limit':stake_withdraw_max_limit,'stake_referral_max_limit':stake_referral_max_limit,'stake_marketprice':stake_marketprice,'stake_deposit_price':stake_deposit_price}
    #     return Response(user_data)
    
    if page_details == "staking_page":
        stake_marketprice=""
        active_stake_amount=""
        stake_withdraw_max_limit=""
        stake_referral_max_limit=""
        if wallet_trust:
            if wallet_trust.wallet_type == "admin blocked":
                trust_add="You are currently blocked!!!"
                Wallet_connect_status= True
            else:
                trust_add=wallet_trust.Address
                Wallet_connect_status= True
        else:
            trust_add=0
            Wallet_connect_status= False
        try:    
            DAta = UserCashWallet.objects.get(userid_id = user_details['id'])
            stake_credit_balance = DAta.balancetwo
            if  DAta.balanceone == 0 and DAta.referalincome == 0 :
                Wallet_status = "Flushed"
            balance = (DAta.balanceone) + (DAta.referalincome)
            if (balance) == 0.00000000:
                balance = 0
            health_reward = Decimal(DAta.balanceone)
            if (health_reward) == 0.00000000:
                health_reward = 0
        except UserCashWallet.DoesNotExist:
            health_reward = 0
        stake_credit_balance = DAta.balancetwo
        if  DAta.balanceone == 0 and DAta.referalincome == 0 :
            Wallet_status = "Flushed"
        balance = (DAta.balanceone) + (DAta.referalincome)
        if (balance) == 0.00000000:
            balance = 0
        health_reward = Decimal(DAta.balanceone)
        if (health_reward) == 0.00000000:
            health_reward = 0
        market_price_details = market_price.objects.get(id = 1)
        stake_price_details = Stake_market_price.objects.using('second_db').get(id = 1)

        # stake_wallet = stake_wallet_management.objects.using('second_db').get(user = user_details['id'])
        try:
            stake_wallet = stake_wallet_management.objects.using('second_db').get(user=user_details['id'])
            stake_Wallet_wallet = stake_wallet.stake_Wallet
            stake_Wallet_withdraw = stake_wallet.stake_withdraw_Wallet
            stake_Refferal_Wallet = stake_wallet.stake_Refferal_Wallet
        except stake_wallet_management.DoesNotExist:
            # Handle the case where the record is not found
            stake_Wallet_wallet = 0
            stake_Wallet_withdraw = 0
            stake_Refferal_Wallet = 0
        stake_percent=staking_admin_management.objects.using('second_db').get(id=1)
        stake_withdraw_max_limit=stake_percent.maximum_withdraw
        stake_referral_max_limit=stake_percent.maximum_withdraw_referal
        stake_hisss = Stake_history_management.objects.using('second_db').filter(user = user_details['id']).last()
        stake_marketprice=stake_price_details.market_price
        active_stake_amount=""
        stake_deposit_price=stake_price_details.market_price
        if stake_hisss != None:
            if str(stake_hisss.start_date) <= "2023-10-30 00:00:00.000000":
                active_stake_amount=stake_hisss.Amount_USDT
                stake_marketprice=stake_hisss.market_price
            else:
                stake_marketprice=stake_price_details.market_price
                active_stake_amount=stake_hisss.Amount_USDT
        try:
            stake_his = Stake_history_management.objects.using('second_db').get(user = user_details['id'],status=0)
            if stake_his.end_date > datetime.now():
                mod_date = stake_his.modified_on.date() 
                today = date.today()
                date_date = (today - mod_date)
                date_count = int(date_date.days)
                if date_count != 0:
                    stake_reward_status = "Not_Claimed"
                else:
                    mod = stake_his.modified_on.time()
                    now = datetime.now().time()
                    dateTimeA = datetime.combine(date.today(), mod)
                    dateTimeB = datetime.combine(date.today(), now)
                    dateTimeDifference = dateTimeB - dateTimeA
                    total_diff = int(dateTimeDifference.total_seconds())
                    if total_diff != 0:
                        stake_reward_status = "Not_Claimed"
                    else:
                        stake_reward_status = "Claimed"
            else:
                mod = stake_his.modified_on.time()
                now = stake_his.end_date.time()
                dateTimeA = datetime.combine(date.today(), mod)
                dateTimeB = datetime.combine(date.today(), now)
                dateTimeDifference = dateTimeB - dateTimeA
                total_diff = int(dateTimeDifference.total_seconds())
                
                if total_diff != 0:
                    stake_reward_status = "Not_Claimed"
                else:
                    stake_reward_status = "Claimed"
        except:
            stake_his = Stake_history_management.objects.using('second_db').filter(user = user_details['id']).last()
            stake_his_credit = Stake_monthly_history_management.objects.using('second_db').filter(user = user_details['id']).last()
            if stake_his != None:
                if stake_his.reward_earned != stake_his.maximum_reward:
                    stake_reward_status = "Not_Claimed"
                else:
                    stake_reward_status = ""
            else:
                stake_reward_status = ""
            if stake_his_credit != None:
                if stake_his_credit.reward_earned != stake_his_credit.maximum_reward:
                    stake_reward_status = "Not_Claimed"
                else:
                    stake_reward_status = ""
            else:
                stake_reward_status = ""
        user_data={"balance":str(balance),'healthreward': (health_reward) ,'Referral_balance':Decimal(DAta.referalincome),'market_price_details':market_price_details.market_price,'stake_Wallet': stake_Wallet_wallet,'stake_withdraw_Wallet':stake_Wallet_withdraw,'stake_Refferal_Wallet':stake_Refferal_Wallet,'status':'true','stake_reward_status':stake_reward_status,"connect_status":Wallet_connect_status,"wallet_address":str(trust_add).lower(),"stake_credit_balance":stake_credit_balance,'active_stake_amount':active_stake_amount,'stake_withdraw_max_limit':stake_withdraw_max_limit,'stake_referral_max_limit':stake_referral_max_limit,'stake_marketprice':stake_marketprice,'stake_deposit_price':stake_deposit_price}
        return Response(user_data)

def footsteps(token):
    user_details = User_Management.objects.get(user_name = token.user)
    feet = user_details.over_all_stepcount
    return feet

@api_view(['POST'])
def step_history(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['Token']
    token = Token.objects.get(key= Token_header)
    serializer = Steps_history_Serializers(data =request.data)
    user_details = User_Management.objects.get(user_name = token.user)
    yesterday_date = "1"
    chk_date = "2022-12-25" 
    if serializer.is_valid:
        step = request.data['steps']
        Step_his = Steps_history.objects.filter(user = user_details.id,created_on__date = (date.today())).count()
        if Step_his > 1:
            Steps_history.objects.filter(user = user_details.id,created_on__date = (date.today())).delete()
            Steps_history.objects.create(user = user_details,steps = int(step))
        if(Step_his == 1):
            if int(step) != 0:
                Step_head = Steps_history.objects.get(user = user_details.id,created_on__date = (date.today()))
                Step_head.steps = int(step)
                Step_head.modified_on = datetime.now()
                Step_head.save()
        if (Step_his == 0):
            Steps_history.objects.create(user = user_details,steps = int(step))
        if (str(date.today())) >= chk_date:
            try:
                User_Step_his = Steps_history.objects.get(user_id = user_details.id,status = 0,created_on__date = (date.today()-timedelta(days = 1)))
            except:
                User_Step_his = ""
            if User_Step_his != "":
                try:
                    User_his = Steps_history.objects.get(user_id = user_details.id,status = 0,created_on__date = (date.today()-timedelta(days = 1)))
                    yesterday_date = User_his.created_on.date()
                except:
                    yesterday_date = "1"
            else:
                try:
                    Chk_Step_his = Steps_history.objects.get(user = user_details,status = 1,created_on__date = (date.today()-timedelta(days = 1)))
                except:
                    Chk_Step_his = ""
                if Chk_Step_his != "":
                    reward_chk = Reward_History.objects.filter(created_on__date = (date.today()-timedelta(days = 1)),user_id = user_details.id,reward_status = "step_reward").count()
                    if reward_chk > 0:
                        pass
                    else:
                        try:
                            chk_user = Steps_history.objects.get(user = user_details,status = 1,created_on__date = (date.today()-timedelta(days = 1)))
                            yesterday_date = chk_user.created_on.date()
                        except:
                            yesterday_date = "1" 
        if ((datetime.now())) >= user_details.plan_end_date:
            yesterday_date = "1" 
        user_data={"Msg":"Step History updated",'status':'true','token':token.key,'yesterdaydate':yesterday_date}
        return Response(user_data)   
    else:
        user_data={"Msg":"Step History Not updated",'status':'false','token':token.key,'yesterdaydate':yesterday_date}
        return Response(user_data)

@api_view(['POST'])
def user_step_history(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['Token']
    token = Token.objects.get(key= Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    if user_details.plan == 0:
        date = user_details.created_on
    if user_details.plan != 0:
        date = user_details.plan_start_date
    user_Deatail = Steps_history.objects.raw('SELECT id,steps,modified_on,CASE WHEN DATE_FORMAT(created_on,"%%Y-%%m-%%d %%H:%%i:%%s") = "2022-12-23 00:00:45" THEN created_on WHEN DATE_FORMAT(created_on,"%%Y-%%m-%%d %%H:%%i:%%s") <= "2022-12-23 23:59:00" THEN (created_on - interval 1 day)  ELSE created_on END AS created_on FROM STPzTPzfNdmGTlEP  WHERE status = 1 AND user_id = %s AND DATE_FORMAT(created_on,"%%Y-%%m-%%d") >= %s ORDER BY created_on DESC', [user_details.id,date.date()])
    serializer = user_step_Serializers(user_Deatail,many=True)
    if serializer.is_valid:
        return Response ({"Data":serializer.data,'status':'true','token':token.key})


def user_list_for_stake_update(request,id):
    context = {} 
    Stake_wallet_internal_transfer_value = 0
    adminactivity_qs = User_Management.objects.get(id=id)
    context['adminactivity_qs'] =adminactivity_qs

    
    try: 
        
        wallet_user = stake_wallet_management.objects.using('second_db').filter(user = adminactivity_qs.id)
        
        if wallet_user.count() == 0:
            stake_wallet_management.objects.using('second_db').create(user = adminactivity_qs.id,email = adminactivity_qs.Email,stake_Wallet = 0,stake_withdraw_Wallet = 0,stake_Refferal_Wallet = 0)
        else:
            pass
    except:
        
        pass

    try:
        wallet = stake_wallet_management.objects.using('second_db').get(user = adminactivity_qs.id)
        stake_wallet_balance = wallet.stake_Wallet
        stake_withdraw_Wallet_balance = wallet.stake_withdraw_Wallet
        stake_Refferal_Wallet_balance = wallet.stake_Refferal_Wallet
    except:
        wallet = 0
        stake_wallet_balance = 0
        stake_withdraw_Wallet_balance = 0
        stake_Refferal_Wallet_balance = 0


    #-----------------------------------------Stake Wallet-------------------------------------------------------#
    
    Stake_wallet_internal_transfer = internal_transfer_history.objects.using('second_db').filter(user = adminactivity_qs.id).aggregate(Sum('amount'))

    Stake_wallet_stake = Stake_history_management.objects.using('second_db').filter(user = adminactivity_qs.id).aggregate(Sum('Amount_USDT'))

    claim_reward_stake_Wallet = stake_claim_reward_history.objects.using('second_db').filter(user =  adminactivity_qs.id).aggregate(Sum('stake_Wallet_reward_amount'))

    stake_deposit_stake_Wallet = stake_deposit_management.objects.using('second_db').filter(user =  adminactivity_qs.id).aggregate(Sum('Amount_USDT'))

    if(Stake_wallet_internal_transfer['amount__sum'] == None):
        Stake_wallet_internal_transfer_value = 0
    else :
        Stake_wallet_internal_transfer_value = Stake_wallet_internal_transfer['amount__sum']

    if(Stake_wallet_stake['Amount_USDT__sum'] == None):
        Stake_wallet_stake_value = 0
    else :
        Stake_wallet_stake_value = Stake_wallet_stake['Amount_USDT__sum']

    if(claim_reward_stake_Wallet['stake_Wallet_reward_amount__sum'] == None):
        claim_reward_stake_Wallet_value = 0
    else :
        claim_reward_stake_Wallet_value = claim_reward_stake_Wallet['stake_Wallet_reward_amount__sum']

    if(stake_deposit_stake_Wallet['Amount_USDT__sum'] == None):
        stake_deposit_stake_Wallet_value = 0
    else :
        stake_deposit_stake_Wallet_value = stake_deposit_stake_Wallet['Amount_USDT__sum']

    stake_wallet_actual = Decimal(Stake_wallet_internal_transfer_value) + Decimal(claim_reward_stake_Wallet_value) + Decimal(stake_deposit_stake_Wallet_value) - Decimal(Stake_wallet_stake_value)

    if Decimal(stake_wallet_balance) != stake_wallet_actual:
        wallet.stake_Wallet  = stake_wallet_actual
        wallet.save()

    #-----------------------------------------WithDraw Wallet --------------------------------------------------#

    claim_reward_withdraw_wallet = Stake_Monthly_Claim_History.objects.using('second_db').filter(user =  adminactivity_qs.id,status=2).aggregate(Sum('earned_stake_reward'))

    if(claim_reward_withdraw_wallet['earned_stake_reward__sum'] == None):
        withdraw_wallet_claim_value = 0
    else :
        withdraw_wallet_claim_value = claim_reward_withdraw_wallet['earned_stake_reward__sum']

    withdraw_history_withdraw_wallet = stake_claim_table.objects.using('second_db').filter(user =  adminactivity_qs.id,Wallet_type = "Stake_Withdraw_Wallet").aggregate(Sum('claim_amount_USDT'))

    if(withdraw_history_withdraw_wallet['claim_amount_USDT__sum'] == None):
        withdraw_wallet_withdraw_history = 0
    else :
        withdraw_wallet_withdraw_history = withdraw_history_withdraw_wallet['claim_amount_USDT__sum']


    withdraw_wallet_actual = Decimal(withdraw_wallet_claim_value) - Decimal(withdraw_wallet_withdraw_history) 

    if Decimal(stake_withdraw_Wallet_balance) != withdraw_wallet_actual:
        wallet.stake_withdraw_Wallet  = withdraw_wallet_actual
        wallet.save()

    #-----------------------------------------Referral Wallet -------------------------------------------------------#


    claim_reward_referral_wallet = Stake_referral_reward_table.objects.using('second_db').filter(user =  adminactivity_qs.id).aggregate(Sum('referral_reward_amount'))

    if(claim_reward_referral_wallet['referral_reward_amount__sum'] == None):
        referral_wallet_claim_value = 0
    else :
        referral_wallet_claim_value = claim_reward_referral_wallet['referral_reward_amount__sum']

    referral_history_withdraw_wallet = stake_claim_table.objects.using('second_db').filter(user =  adminactivity_qs.id,Wallet_type = "Stake_Referral_Wallet").aggregate(Sum('claim_amount_USDT'))

    if(referral_history_withdraw_wallet['claim_amount_USDT__sum'] == None):
        withdraw_wallet_referral_history = 0
    else :
        withdraw_wallet_referral_history = referral_history_withdraw_wallet['claim_amount_USDT__sum']


    referral_wallet_actual = Decimal(referral_wallet_claim_value) - Decimal(withdraw_wallet_referral_history) 

    if Decimal(stake_Refferal_Wallet_balance) != referral_wallet_actual:
        wallet.stake_Refferal_Wallet  = referral_wallet_actual
        wallet.save()

    return True


from web3 import Web3, HTTPProvider
from eth_account import Account,messages
import pickle
from web3.middleware import geth_poa_middleware

# testBNBseedurl = 'https://bsc-dataseed.binance.org/'
obj_contract = Contract_address.objects.get(id = 1)
testBNBseedurl = obj_contract.Stake_contract_Address
web3 =  Web3(Web3.HTTPProvider(testBNBseedurl))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
admin_address_pk ='1OP1haKmdm2odu+Z1ZY+uVbEsflfaD6OiphJXYrtAO6tIc85R4SD3KrXJnJQ7Xa4T7w53u3I244rFeQUnOmEsHVOLtZnJoacYQICnk6qzUM='
admin_address ='BScIjxmyaKnGGeDrjHjHrwVsoWrH138k6Eai3wQ2rTOo4WZg5RNHx+BSFDRJ6MUE'
ad_pk = "Bp1Fljq9rBHi4kaPVBdBIlqS3jEzHswzB1jpwLpk6iU9GbRn7favXXczENW+v8l+Kr3Hov0UqAul7Nqq3WLaxA=="
ad_ad = "thAtkC68J5UMbBBos41TnMw1xeVcbYNgFgLJS55SIMyN7Z3vJvLoMhHg0Eta/kKm"
user_ad_pk = "Bp1Fljq9rBHi4kaPVBdBIlqS3jEzHswzB1jpwLpk6iU9GbRn7favXXczENW+v8l+Kr3Hov0UqAul7Nqq3WLaxA=="



@api_view(['POST'])
def withdraw_request(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    step = Steps_Management.objects.get(id = 1)
    user_details = User_Management.objects.get(user_name = token.user)
    user_type=user_details.user_profile_pic
    wallet_add=user_address_trust_wallet.objects.get(user_id=user_details.id)
    address_type=wallet_add.wallet_type
    company_qs = Company.objects.get(id=1)
    android_current_version_users_count = company_qs.Android_version
    ios_current_version_users_count = company_qs.IOS_version
    withdraw_type=company_qs.withdraw_type
    if user_details.plan != 0 :
        user_plan_history = plan_purchase_history.objects.filter(user_id = user_details.id).last()
        stake_wall_per    = user_plan_history.stake_wallet_monthly_split_percentage
    else:
        stake_wall_per  = 0
    if int(withdraw_type) == 0:
        if user_type == 'Android':
            if user_details.phone_number != android_current_version_users_count:
                user_data={"Msg":"Please Update Current Version!!!",'status':'false','token':token.key}
                return Response(user_data)
            if address_type == "admin blocked":
                user_data={"Msg":"Address Blocked!!!",'status':'false','token':token.key}
                return Response(user_data)
            else:
                maximum_withdraw_limit = 0
                if int(step.status) == 1:
                    user_data={"Msg":"Withdraw Under maintenance. Kindly try again later !!!",'status':'false','token':token.key}
                    return Response(user_data)
                try:
                    user_details = User_Management.objects.get(user_name = token.user)
                    pin = Pin.objects.get(user_id = user_details.id)
                    amount = (request.data['Amount']) 
                    wei_amount = request.data['Wei_amount']
                    address = request.data['Address']
                    stake_credit_converted=request.data['stake_credit_converted']
                    price=request.data['price']
                    user_withdraw_request=request.data['user_withdraw_request']
                    premium_transfer_amt=request.data['premium_transfer_amt']
                    # usr_adrs = "0x05DCE56ef9BD815A9D98D95d56C3fddc4e609C35"
                    usr_adrs="0x9c8265a408b6faad1c6ff60f01e4d9f143635373"
                    two_fa_input = request.data['Two_Fa']
                    ref_pin = int(request.data['pin'])
                    wallet_Type = int(request.data['wallet_type'])
                    User_Private_key = ""
                    try:
                        User_Private_key = (request.data['User_PK'])
                    except:
                        User_Private_key = ""
                    if usr_adrs != address:
                        if User_Private_key != "" :
                            User_Private_key = (request.data['User_PK'])
                            if Decimal(wei_amount) > 0:
                                try:
                                    security_type = request.data['security_type']
                                except:
                                    security_type = "TFA"
                                today = (datetime.now())
                                diff_chk = user_list_for_update(request,user_details.id,wallet_Type)
                                if wallet_Type == 1:
                                    if int(diff_chk) != 0:
                                        user_list_reward_update(request,user_details.id)
                                        user_data={"Msg":"Request Denied Due To Wallet Balance Mismatch.Now It is Corrected, Kindly Try Again!!!",'status':'false','token':token.key}
                                        return Response(user_data)
                                if wallet_Type == 2:
                                    if int(diff_chk) != 0:
                                        user_list_reward_update(request,user_details.id)
                                        user_data={"Msg":"Request Denied Due To Wallet Balance Mismatch.Now It is Corrected, Kindly Try Again!!!",'status':'false','token':token.key}
                                        return Response(user_data)
                                if str(user_details.plan_start_date) < "2023-10-18 13:20:00.000000": 
                                    try:
                                        withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                        if withdraw_last :
                                            if withdraw_last.created_on + timedelta(hours=24) > today:
                                                user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                return Response(user_data)
                                    except:
                                        withdraw_last = ""
                                    try:
                                        withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id).last()
                                        if withdraw_last_stake :
                                            if withdraw_last_stake.created_on + timedelta(hours=24) > today:
                                                user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                return Response(user_data)
                                    except:
                                        withdraw_last_stake = ""
                                plan_plan = 0
                                if user_details.plan != 0 :
                                    plan_plan = plan.objects.get(id = int(user_details.plan))
                                if user_details.plan == 0:
                                    plan_plan = plan.objects.get(plan_type = 0)
                                month_end_date = user_details.plan_validation
                                if month_end_date == "Monthly":   
                                    maximum_withdraw_limit = plan_plan.Total_maximum_limit
                                if month_end_date == "Quarterly":   
                                    maximum_withdraw_limit = plan_plan.Total_maximum_limit *(3)
                                if month_end_date == "Annual":   
                                    maximum_withdraw_limit = plan_plan.Total_maximum_limit *(12)
                                withdraw_per_mont_val = Withdraw.objects.filter(userid_id = user_details.id,status = 1,created_on__gte = user_details.plan_start_date,created_on__lte = user_details.plan_end_date).aggregate(Sum('Amount'))
                                # if (withdraw_per_mont_val['Amount__sum']) != None:
                                #     if int(withdraw_per_mont_val['Amount__sum']) >= maximum_withdraw_limit:
                                #         user_data={"Msg":"Your Monthly Withdraw Limit Is Over.",'status':'false','token':token.key}
                                #         return Response(user_data)
                                if plan_plan.withdraw_status == 0:
                                    user_data={"Msg":"Withdraw is Not Applicable For Your Current Plan!!!",'status':'false','token':token.key}
                                    return Response(user_data)
                                # if (str(amount).find('.')) != -1:
                                #     user_data={"Msg":"Enter Only Whole Numbers Like 1,2,3,4......",'status':'false','token':token.key}
                                #     return Response(user_data)
                                if ref_pin:
                                    try:
                                        pin = Pin.objects.get(user_id = user_details.id )
                                        if pin.pin is None:
                                            user_data={"Msg":"Set PIN",'status':'false','token':token.key}
                                            return Response(user_data)
                                        else:
                                            msg = "NewUser"
                                    except:
                                        user_data={"Msg":"Set PIN",'status':'false','token':token.key}
                                        return Response(user_data)
                                two_fa = User_two_fa.objects.get(user = user_details.id)
                                confirm = two_fa.user_secrete_key
                                if security_type == "TFA":
                                    if two_fa.user_status == 'enable':
                                        totp = pyotp.TOTP(confirm)
                                        otp_now=totp.now()
                                        pin = Pin.objects.get(user_id = user_details.id)
                                        pinnn = pin.pin
                                        num1 = str(pinnn)
                                        num2 = str(123456)
                                        if int(two_fa_input) == int(otp_now):
                                            valuess = withdraw_values.objects.get(id = 1)
                                            if ref_pin == pin.pin:
                                                wallet = UserCashWallet.objects.get(userid_id = user_details.id)
                                                total = 0
                                                withamount = Withdraw.objects.filter(userid_id = user_details.id,status = 0)
                                                for i in withamount:
                                                    total = Decimal(total)+Decimal(i.Amount)
                                                wallet__type = ""
                                                if int(user_details.plan) == 0:
                                                    user_plan_details = plan.objects.get(plan_type = 0)
                                                    if wallet_Type == 1:
                                                        wallet__type = "Reward_wallet"
                                                        balance = wallet.balanceone - total
                                                        if user_plan_details.health_withdraw_minimum_limit >= Decimal(amount) or user_plan_details.health_withdraw_maximum_limit <= Decimal(amount):
                                                            user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                            return Response(user_data)
                                                    if wallet_Type == 2:
                                                        wallet__type = "Referral_wallet"
                                                        balance = wallet.referalincome - total
                                                        if user_plan_details.referral_withdraw_minimum_limit >= Decimal(amount) or user_plan_details.referral_withdraw_maximum_limit <= Decimal(amount):
                                                            user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                            return Response(user_data)
                                                else:
                                                    user_plan_details = plan.objects.get(id = int(user_details.plan))
                                                    if wallet_Type == 1:
                                                        wallet__type = "Reward_wallet"
                                                        balance = wallet.balanceone - total
                                                        if user_details.plan  == 64:
                                                            if str(user_details.plan_start_date) >= "2023-10-28 12:30:00.000000":
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Reward_wallet').last()
                                                                    if withdraw_last :
                                                                        how_many_days= today - withdraw_last.created_on 
                                                                        how_many= 28 - how_many_days.days 
                                                                        if withdraw_last.created_on + timedelta(28) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                            else:
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                                                    if withdraw_last :
                                                                        if withdraw_last.created_on + timedelta(hours=24) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                        else:
                                                            if str(user_details.plan_start_date) >= "2023-10-18 13:20:00.000000":
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Reward_wallet').last()
                                                                    if withdraw_last :
                                                                        how_many_days= today - withdraw_last.created_on 
                                                                        how_many= 28 - how_many_days.days 
                                                                        if withdraw_last.created_on + timedelta(28) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                        if  Decimal(amount) < user_details.Health_Withdraw_min_value or Decimal(amount) > user_details.Health_Withdraw_max_value :
                                                            user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                            return Response(user_data)
                                                    if wallet_Type == 2:
                                                        wallet__type = "Referral_wallet"
                                                        balance = wallet.referalincome - total
                                                        if user_details.plan  == 64:
                                                            if str(user_details.plan_start_date) >= "2023-10-28 12:30:00.000000":
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Referral_wallet').last()
                                                                    if withdraw_last :
                                                                        how_many_days= today - withdraw_last.created_on 
                                                                        how_many= 28 - how_many_days.days 
                                                                        if withdraw_last.created_on + timedelta(28) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                            else:
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                                                    if withdraw_last :
                                                                        if withdraw_last.created_on + timedelta(hours=24) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                        else:
                                                            if str(user_details.plan_start_date) >= "2023-10-18 13:20:00.000000":
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Referral_wallet').last()
                                                                    if withdraw_last :
                                                                        how_many_days= today - withdraw_last.created_on 
                                                                        how_many= 28 - how_many_days.days 
                                                                        if withdraw_last.created_on + timedelta(28) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                        # if user_plan_details.referral_withdraw_minimum_limit > Decimal(amount) or user_plan_details.referral_withdraw_maximum_limit < Decimal(amount):
                                                        if  Decimal(amount) < user_details.Referral_Withdraw_min_value or  Decimal(amount) > user_details.Referral_Withdraw_max_value:
                                                            user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                            return Response(user_data)
                                                if balance >= Decimal(amount):
                                                    receiver_ck = Web3.isAddress((address))
                                                    if receiver_ck is True:
                                                        currency = TradeCurrency.objects.get(symbol = 'JW')
                                                        fee_type = currency.withdraw_feestype
                                                        fee = 0
                                                        if fee_type == 0:
                                                            fee = (float(currency.withdraw_fees)/100)*(float(amount))
                                                        if fee_type == 1:
                                                            fee = (float(amount))-(float(currency.withdraw_fees))
                                                        address=address
                                                        user = User_Management.objects.get(id = user_details.id)
                                                        # if stake_wall_per !=0:
                                                        #     stakefee = (float(stake_wall_per)/100)*(float(amount))
                                                        #     month_stake= stakefee
                                                        # else :
                                                        #     month_stake= 0                                                
                                                        # price = float(amount) - ((fee) + (month_stake))
                                                        wei_price = float(wei_amount)
                                                        amount = Decimal(amount)
                                                        receiver=address
                                                        receiver_ck = Web3.toChecksumAddress(str(receiver))
                                                        max_amount = int(wei_price*10 ** 8)
                                                        table_and_reward = Withdraw(userid_id = user_details.id,Amount = amount,Address = address,Two_Fa = two_fa_input,Wallet_type=wallet__type,back_up_phrase="0",user_request_amt = user_withdraw_request)
                                                        table_and_reward.save()        
                                                        if table_and_reward != "":
                                                            try:
                                                                url = "https://apinode.jasanwellness.fit/VahlHzjSVqvqjaSglbDxWVfAxwrsIMKTcXCwoAIBBEkLBAwHQl"
                                                                data = {
                                                                        "userAddress":receiver_ck,
                                                                        "claimAmount":max_amount,
                                                                        "skey" : User_Private_key
                                                                        }
                                                                headers = {"Content-Type": "application/json"}
                                                                response = requests.post(url, json=data, headers=headers)
                                                                if response.status_code == 200:
                                                                    data = response.json()
                                                                    json_data = data['data']
                                                                    transaction_hash = json_data['result']
                                                                    
                                                                else:
                                                                    user_data={"Msg":"Contract Call Failed with Response "+str(response.status_code) ,'status':'false','token':token.key}
                                                                    return Response(user_data)
                                                            except Exception as e:
                                                                user_data={"Msg":"Failed with error"+str(e),'status':'false','token':token.key}
                                                                return Response(user_data)
                                                        else:
                                                            user_data={"Msg":"Insert Fail",'status':'false','token':token.key}
                                                            return Response(user_data)
                                                        cash = UserCashWallet.objects.get(userid_id = user.id )
                                                        if wallet_Type == 1:
                                                            cash.balanceone = cash.balanceone - Decimal(amount)
                                                            cash.balancetwo = cash.balancetwo + Decimal(stake_credit_converted)
                                                            cash.Premiumwallet = cash.Premiumwallet + Decimal(premium_transfer_amt)
                                                            cash.save()
                                                            premium_wallet_deposit.objects.create(user = user.id,email = user.Email,Amount_USDT = premium_transfer_amt,Amount_JW = 0,Hash = 0,status  = 1,type=wallet__type,withdraw_amount=amount)
                                                        if wallet_Type == 2:
                                                            cash.referalincome = cash.referalincome - Decimal(amount)
                                                            cash.balancetwo = cash.balancetwo + Decimal(stake_credit_converted)
                                                            cash.save()
                                                        table2 = Stake_Credit_History.objects.create(user_id = user.id,original_reward = amount,stake_percentage = stake_wall_per,percent_value=stake_credit_converted,withdraw_type=wallet__type)
                                                        # table = Withdraw(userid_id = user_details.id,Amount = amount,Address = address,Two_Fa = two_fa_input)
                                                        # table.save()
                                                        withdraw = Withdraw.objects.get(id = table_and_reward.id)
                                                        withdraw.status = 1
                                                        withdraw.Transaction_Hash = transaction_hash
                                                        withdraw.Wallet_type = wallet__type
                                                        withdraw.Withdraw_fee = currency.withdraw_fees
                                                        withdraw.Withdraw_USDT = price
                                                        withdraw.Withdraw_JW = wei_price
                                                        withdraw.Month_stake = stake_wall_per
                                                        withdraw.save()
                                                        table = Withdraw_history.objects.create(user_id = user,Amount = price,From_Address = decrypt_with_common_cipher(ad_ad),To_Address = receiver,Transaction_Hash = transaction_hash,withdraw_id=withdraw,Wallet_type = wallet__type)
                                                        table1 = Admin_Profit.objects.create(user = user,admin_profit = Decimal(fee),Profit_type = "Withdraw")
                                                        user_data={"Msg":"Withdraw Successfull",'status':'true','token':token.key}
                                                        return Response(user_data)
                                                    else:
                                                        user_data={"Msg":"Enter Valid Address",'status':'false','token':token.key}
                                                        return Response(user_data)
                                                else:
                                                    user_data={"Msg":"Withdraw Is Under Processing",'status':'false','token':token.key}
                                                    return Response(user_data)
                                            else:
                                                user_data={"Msg":"Pin Does Not Match",'status':'false','token':token.key}
                                                return Response(user_data)                    
                                        else:
                                            user_data={"Msg":"Enter TFA Correctly",'status':'false','token':token.key}
                                            return Response(user_data)
                                    else:
                                        user_data={"Msg":"Enable Two FA",'status':'false','token':token.key}
                                        return Response(user_data)
                                else:
                                    Email_otp = Registration_otp.objects.get(user = user_details.id)
                                    if Email_otp.email_otp == int(two_fa_input):
                                        valuess = withdraw_values.objects.get(id = 1)
                                        pin = Pin.objects.get(user_id = user_details.id)
                                        if ref_pin == pin.pin:
                                            wallet = UserCashWallet.objects.get(userid_id = user_details.id)
                                            total = 0
                                            withamount = Withdraw.objects.filter(userid_id = user_details.id,status = 0)
                                            for i in withamount:
                                                total = Decimal(total)+Decimal(i.Amount)
                                            wallet__type = ""
                                            if int(user_details.plan) == 0:
                                                user_plan_details = plan.objects.get(plan_type = 0)
                                                if wallet_Type == 1:
                                                    wallet__type = "Reward_wallet"
                                                    balance = wallet.balanceone - total
                                                    if user_plan_details.health_withdraw_minimum_limit >= Decimal(amount) or user_plan_details.health_withdraw_maximum_limit <= Decimal(amount):
                                                        user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                        return Response(user_data)
                                                if wallet_Type == 2:
                                                    wallet__type = "Referral_wallet"
                                                    balance = wallet.referalincome - total
                                                    if user_plan_details.referral_withdraw_minimum_limit >= Decimal(amount) or user_plan_details.referral_withdraw_maximum_limit <= Decimal(amount):
                                                        user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                        return Response(user_data)
                                            else:
                                                user_plan_details = plan.objects.get(id = int(user_details.plan))
                                                if wallet_Type == 1:
                                                    wallet__type = "Reward_wallet"
                                                    balance = wallet.balanceone - total
                                                    if user_details.plan  == 64:
                                                        if str(user_details.plan_start_date) >= "2023-10-28 12:30:00.000000":
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Reward_wallet').last()
                                                                if withdraw_last :
                                                                    how_many_days= today - withdraw_last.created_on 
                                                                    how_many= 28 - how_many_days.days 
                                                                    if withdraw_last.created_on + timedelta(28) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                        else:
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                                                if withdraw_last :
                                                                    if withdraw_last.created_on + timedelta(hours=24) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                    else:
                                                        if str(user_details.plan_start_date) >= "2023-10-18 13:20:00.000000":
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Reward_wallet').last()
                                                                if withdraw_last :
                                                                    how_many_days= today - withdraw_last.created_on 
                                                                    how_many= 28 - how_many_days.days 
                                                                    if withdraw_last.created_on + timedelta(28) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                    # if user_plan_details.health_withdraw_minimum_limit > Decimal(amount) or user_plan_details.health_withdraw_maximum_limit < Decimal(amount):
                                                    if  Decimal(amount) < user_details.Health_Withdraw_min_value or Decimal(amount) > user_details.Health_Withdraw_max_value :
                                                        user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                        return Response(user_data)
                                                if wallet_Type == 2:
                                                    wallet__type = "Referral_wallet"
                                                    balance = wallet.referalincome - total
                                                    if user_details.plan  == 64:
                                                        if str(user_details.plan_start_date) >= "2023-10-28 12:30:00.000000":
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Referral_wallet').last()
                                                                if withdraw_last :
                                                                    how_many_days= today - withdraw_last.created_on 
                                                                    how_many= 28 - how_many_days.days 
                                                                    if withdraw_last.created_on + timedelta(28) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                        else:
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                                                if withdraw_last :
                                                                    if withdraw_last.created_on + timedelta(hours=24) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                    else:
                                                        if str(user_details.plan_start_date) >= "2023-10-18 13:20:00.000000":
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Referral_wallet').last()
                                                                if withdraw_last :
                                                                    how_many_days= today - withdraw_last.created_on 
                                                                    how_many= 28 - how_many_days.days 
                                                                    if withdraw_last.created_on + timedelta(28) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                    # if user_plan_details.referral_withdraw_minimum_limit > Decimal(amount) or user_plan_details.referral_withdraw_maximum_limit < Decimal(amount):
                                                    if  Decimal(amount) < user_details.Referral_Withdraw_min_value or  Decimal(amount) > user_details.Referral_Withdraw_max_value:
                                                        user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                        return Response(user_data)
                                            if balance >= Decimal(amount):
                                                receiver_ck = Web3.isAddress((address))
                                                if receiver_ck is True:
                                                    currency = TradeCurrency.objects.get(symbol = 'JW')
                                                    fee_type = currency.withdraw_feestype
                                                    fee = 0
                                                    if fee_type == 0:
                                                        fee = (float(currency.withdraw_fees)/100)*(float(amount))
                                                    if fee_type == 1:
                                                        fee = (float(amount))-(float(currency.withdraw_fees))
                                                    address=address
                                                    user = User_Management.objects.get(id = user_details.id)
                                                    # if stake_wall_per !=0:
                                                    #     stakefee = (float(stake_wall_per)/100)*(float(amount))
                                                    #     month_stake= stakefee
                                                    # else :
                                                    #     month_stake= 0                                                 
                                                    # price = float(amount) - ((fee) + (month_stake)) 
                                                    wei_price = float(wei_amount)
                                                    amount = Decimal(amount)
                                                    receiver=address
                                                    receiver_ck = Web3.toChecksumAddress(str(receiver))
                                                    max_amount = int(wei_price*10 ** 8)
                                                    table_and_rell = Withdraw(userid_id = user_details.id,Amount = amount ,Address = address,Two_Fa = two_fa_input,Wallet_type=wallet__type,back_up_phrase="0",user_request_amt =  user_withdraw_request)
                                                    table_and_rell.save()
                                                    if table_and_rell !="":
                                                        try:
                                                            url = "https://apinode.jasanwellness.fit/VahlHzjSVqvqjaSglbDxWVfAxwrsIMKTcXCwoAIBBEkLBAwHQl"
                                                            data = {
                                                                    "userAddress":receiver_ck,
                                                                    "claimAmount":max_amount,
                                                                    "skey" : User_Private_key
                                                                    }
                                                            headers = {"Content-Type": "application/json"}
                                                            response = requests.post(url, json=data, headers=headers)
                                                            if response.status_code == 200:
                                                                data = response.json()
                                                                json_data = data['data']
                                                                transaction_hash = json_data['result']
                                                                
                                                            else:
                                                                user_data={"Msg":"Contract Call Failed with Response "+str(response.status_code) ,'status':'false','token':token.key}
                                                                return Response(user_data)
                                                        except Exception as e:
                                                                user_data={"Msg":"Failed with error"+str(e),'status':'false','token':token.key}
                                                                return Response(user_data)
                                                    else:
                                                        user_data={"Msg":"Insert Fail",'status':'false','token':token.key}
                                                        return Response(user_data)
                                                    cash = UserCashWallet.objects.get(userid_id = user.id )
                                                    if wallet_Type == 1:
                                                        cash.balanceone = cash.balanceone - Decimal(amount)
                                                        cash.balancetwo = cash.balancetwo + Decimal(stake_credit_converted)
                                                        cash.Premiumwallet = cash.Premiumwallet + Decimal(premium_transfer_amt) 
                                                        cash.save()                                             
                                                        premium_wallet_deposit.objects.create(user = user.id,email = user.Email,Amount_USDT = premium_transfer_amt,Amount_JW = 0,Hash = 0,status  = 1,type=wallet__type,withdraw_amount=amount,create_type="user withdraw")
                                                    if wallet_Type == 2:
                                                        cash.referalincome = cash.referalincome - Decimal(amount)
                                                        cash.balancetwo = cash.balancetwo + Decimal(stake_credit_converted)
                                                        cash.save()
                                                    table2 = Stake_Credit_History.objects.create(user_id = user.id,original_reward = amount,stake_percentage = stake_wall_per,percent_value=stake_credit_converted,withdraw_type=wallet__type)
                                                    # table = Withdraw(userid_id = user_details.id,Amount = amount,Address = address,Two_Fa = two_fa_input)
                                                    # table.save()
                                                    withdraw = Withdraw.objects.get(id = table_and_rell.id)
                                                    withdraw.status = 1
                                                    withdraw.Transaction_Hash = transaction_hash
                                                    withdraw.Wallet_type = wallet__type
                                                    withdraw.Withdraw_fee = currency.withdraw_fees
                                                    withdraw.Withdraw_USDT = price
                                                    withdraw.Withdraw_JW = wei_price
                                                    withdraw.Month_stake = stake_wall_per
                                                    withdraw.save()
                                                    table = Withdraw_history.objects.create(user_id = user,Amount = price,From_Address = decrypt_with_common_cipher(ad_ad),To_Address = receiver,Transaction_Hash = transaction_hash,withdraw_id=withdraw,Wallet_type = wallet__type)
                                                    table1 = Admin_Profit.objects.create(user = user,admin_profit = Decimal(fee),Profit_type = "Withdraw")
                                                    user_data={"Msg":"Withdraw Successfull",'status':'true','token':token.key}
                                                    return Response(user_data)
                                                else:
                                                    user_data={"Msg":"Enter Valid Address",'status':'false','token':token.key}
                                                    return Response(user_data)
                                            else:
                                                user_data={"Msg":"Withdraw Is Under Processing",'status':'false','token':token.key}
                                                return Response(user_data)
                                        else:
                                            user_data={"Msg":"Pin Does Not Match",'status':'false','token':token.key}
                                            return Response(user_data)
                                    else:
                                        user_data={"Msg":"Email OTP Does Not match",'status':'false','token':token.key}
                                        return Response(user_data)
                            else:
                                user_data={"Msg":"Market Price API down. Try After Sometimes!!!",'status':'false','token':token.key}
                                return Response(user_data)
                        else:
                            user_data={"Msg":"Kindly Update Your APP To Withdraw Funds...",'status':'false','token':token.key}
                            return Response(user_data)
                    else:
                        to_email = "jasanwellness@gmail.com"
                        email_subject = 'Withdraw from blocked address.'
                        data= {
                            'username':user_details,
                            'user_email':user_details.Email,
                            'email':to_email,
                            'security_type':security_type,
                            'amount' : amount,
                            'address' : address,
                            'domain':settings.DOMAIN_URL,
                            }
                        htmly = get_template('emailtemplate/block_user_temp.html')
                        html_content = htmly.render(data)
                        response = requests.post(
                        "https://api.mailgun.net/v3/jasanwellness.fit/messages",
                        auth=("api", decrypt_with_common_cipher(settings.MAIL_API)),
                        data={"from": "WEB3 WELLNESS <noreply@jasanwellness.fit>",
                        "to": [to_email],
                        "subject": email_subject,
                        "html": html_content})
                        user_data={"Msg":"Try after sometime...!!!",'status':'false'}
                        return Response(user_data)
                except Exception as e:
                    user_data={"Msg":"Failed With Error "+str(e),'status':'false','token':token.key}
                    return Response(user_data)
        elif user_type == 'IOS':
            if user_details.phone_number != ios_current_version_users_count:
                user_data={"Msg":"Please Update Current Version!!!",'status':'false','token':token.key}
                return Response(user_data)
            if address_type == "admin blocked":
                user_data={"Msg":"Address Blocked!!!",'status':'false','token':token.key}
                return Response(user_data)
            else:
                maximum_withdraw_limit = 0
                if int(step.status) == 1:
                    user_data={"Msg":"Withdraw Under maintenance. Kindly try again later !!!",'status':'false','token':token.key}
                    return Response(user_data)
                try:
                    user_details = User_Management.objects.get(user_name = token.user)
                    pin = Pin.objects.get(user_id = user_details.id)
                    amount = (request.data['Amount'])
                    wei_amount = request.data['Wei_amount']
                    address = request.data['Address']
                    stake_credit_converted=request.data['stake_credit_converted']
                    price=request.data['price']
                    user_withdraw_request=request.data['user_withdraw_request']
                    premium_transfer_amt=request.data['premium_transfer_amt']
                    # usr_adrs = "0x05DCE56ef9BD815A9D98D95d56C3fddc4e609C35"
                    usr_adrs="0x9c8265a408b6faad1c6ff60f01e4d9f143635373"
                    two_fa_input = request.data['Two_Fa']
                    ref_pin = int(request.data['pin'])
                    wallet_Type = int(request.data['wallet_type'])
                    User_Private_key = ""
                    try:
                        User_Private_key = (request.data['User_PK'])
                    except:
                        User_Private_key = ""
                    if usr_adrs != address:
                        if User_Private_key != "" :
                            User_Private_key = (request.data['User_PK'])
                            if Decimal(wei_amount) > 0:
                                try:
                                    security_type = request.data['security_type']
                                except:
                                    security_type = "TFA"
                                today = (datetime.now())
                                diff_chk = user_list_for_update(request,user_details.id,wallet_Type)
                                if wallet_Type == 1:
                                    if int(diff_chk) != 0:
                                        user_list_reward_update(request,user_details.id)
                                        user_data={"Msg":"Request Denied Due To Wallet Balance Mismatch.Now It is Corrected, Kindly Try Again!!!",'status':'false','token':token.key}
                                        return Response(user_data)
                                if wallet_Type == 2:
                                    if int(diff_chk) != 0:
                                        user_list_reward_update(request,user_details.id)
                                        user_data={"Msg":"Request Denied Due To Wallet Balance Mismatch.Now It is Corrected, Kindly Try Again!!!",'status':'false','token':token.key}
                                        return Response(user_data)
                                if str(user_details.plan_start_date) < "2023-10-18 13:20:00.000000": 
                                    try:
                                        withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                        if withdraw_last :
                                            if withdraw_last.created_on + timedelta(hours=24) > today:
                                                user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                return Response(user_data)
                                    except:
                                        withdraw_last = ""
                                    try:
                                        withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id).last()
                                        if withdraw_last_stake :
                                            if withdraw_last_stake.created_on + timedelta(hours=24) > today:
                                                user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                return Response(user_data)
                                    except:
                                        withdraw_last_stake = ""
                                plan_plan = 0
                                if user_details.plan != 0 :
                                    plan_plan = plan.objects.get(id = int(user_details.plan))
                                if user_details.plan == 0:
                                    plan_plan = plan.objects.get(plan_type = 0)
                                month_end_date = user_details.plan_validation
                                if month_end_date == "Monthly":   
                                    maximum_withdraw_limit = plan_plan.Total_maximum_limit
                                if month_end_date == "Quarterly":   
                                    maximum_withdraw_limit = plan_plan.Total_maximum_limit *(3)
                                if month_end_date == "Annual":   
                                    maximum_withdraw_limit = plan_plan.Total_maximum_limit *(12)
                                withdraw_per_mont_val = Withdraw.objects.filter(userid_id = user_details.id,status = 1,created_on__gte = user_details.plan_start_date,created_on__lte = user_details.plan_end_date).aggregate(Sum('Amount'))
                                # if (withdraw_per_mont_val['Amount__sum']) != None:
                                #     if int(withdraw_per_mont_val['Amount__sum']) >= maximum_withdraw_limit:
                                #         user_data={"Msg":"Your Monthly Withdraw Limit Is Over.",'status':'false','token':token.key}
                                #         return Response(user_data)
                                if plan_plan.withdraw_status == 0:
                                    user_data={"Msg":"Withdraw is Not Applicable For Your Current Plan!!!",'status':'false','token':token.key}
                                    return Response(user_data)
                                # if (str(amount).find('.')) != -1:
                                #     user_data={"Msg":"Enter Only Whole Numbers Like 1,2,3,4......",'status':'false','token':token.key}
                                #     return Response(user_data)
                                if ref_pin:
                                    try:
                                        pin = Pin.objects.get(user_id = user_details.id )
                                        if pin.pin is None:
                                            user_data={"Msg":"Set PIN",'status':'false','token':token.key}
                                            return Response(user_data)
                                        else:
                                            msg = "NewUser"
                                    except:
                                        user_data={"Msg":"Set PIN",'status':'false','token':token.key}
                                        return Response(user_data)
                                two_fa = User_two_fa.objects.get(user = user_details.id)
                                confirm = two_fa.user_secrete_key
                                if security_type == "TFA":
                                    if two_fa.user_status == 'enable':
                                        totp = pyotp.TOTP(confirm)
                                        otp_now=totp.now()
                                        pin = Pin.objects.get(user_id = user_details.id)
                                        pinnn = pin.pin
                                        num1 = str(pinnn)
                                        num2 = str(123456)
                                        if int(two_fa_input) == int(otp_now):
                                            valuess = withdraw_values.objects.get(id = 1)
                                            if ref_pin == pin.pin:
                                                wallet = UserCashWallet.objects.get(userid_id = user_details.id)
                                                total = 0
                                                withamount = Withdraw.objects.filter(userid_id = user_details.id,status = 0)
                                                for i in withamount:
                                                    total = Decimal(total)+Decimal(i.Amount)
                                                wallet__type = ""
                                                if int(user_details.plan) == 0:
                                                    user_plan_details = plan.objects.get(plan_type = 0)
                                                    if wallet_Type == 1:
                                                        wallet__type = "Reward_wallet"
                                                        balance = wallet.balanceone - total
                                                        if user_plan_details.health_withdraw_minimum_limit >= Decimal(amount) or user_plan_details.health_withdraw_maximum_limit <= Decimal(amount):
                                                            user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                            return Response(user_data)
                                                    if wallet_Type == 2:
                                                        wallet__type = "Referral_wallet"
                                                        balance = wallet.referalincome - total
                                                        if user_plan_details.referral_withdraw_minimum_limit >= Decimal(amount) or user_plan_details.referral_withdraw_maximum_limit <= Decimal(amount):
                                                            user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                            return Response(user_data)
                                                else:
                                                    user_plan_details = plan.objects.get(id = int(user_details.plan))
                                                    if wallet_Type == 1:
                                                        wallet__type = "Reward_wallet"
                                                        balance = wallet.balanceone - total
                                                        if user_details.plan  == 64:
                                                            if str(user_details.plan_start_date) >= "2023-10-28 12:30:00.000000":
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Reward_wallet').last()
                                                                    if withdraw_last :
                                                                        how_many_days= today - withdraw_last.created_on 
                                                                        how_many= 28 - how_many_days.days 
                                                                        if withdraw_last.created_on + timedelta(28) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                            else:
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                                                    if withdraw_last :
                                                                        if withdraw_last.created_on + timedelta(hours=24) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                        else:
                                                            if str(user_details.plan_start_date) >= "2023-10-18 13:20:00.000000":
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Reward_wallet').last()
                                                                    if withdraw_last :
                                                                        how_many_days= today - withdraw_last.created_on 
                                                                        how_many= 28 - how_many_days.days 
                                                                        if withdraw_last.created_on + timedelta(28) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                        if  Decimal(amount) < user_details.Health_Withdraw_min_value or Decimal(amount) > user_details.Health_Withdraw_max_value :
                                                            user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                            return Response(user_data)
                                                    if wallet_Type == 2:
                                                        wallet__type = "Referral_wallet"
                                                        balance = wallet.referalincome - total
                                                        if user_details.plan  == 64:
                                                            if str(user_details.plan_start_date) >= "2023-10-28 12:30:00.000000":
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Referral_wallet').last()
                                                                    if withdraw_last :
                                                                        how_many_days= today - withdraw_last.created_on 
                                                                        how_many= 28 - how_many_days.days 
                                                                        if withdraw_last.created_on + timedelta(28) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                            else:
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                                                    if withdraw_last :
                                                                        if withdraw_last.created_on + timedelta(hours=24) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                        else:
                                                            if str(user_details.plan_start_date) >= "2023-10-18 13:20:00.000000":
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Referral_wallet').last()
                                                                    if withdraw_last :
                                                                        how_many_days= today - withdraw_last.created_on 
                                                                        how_many= 28 - how_many_days.days 
                                                                        if withdraw_last.created_on + timedelta(28) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                        # if user_plan_details.referral_withdraw_minimum_limit > Decimal(amount) or user_plan_details.referral_withdraw_maximum_limit < Decimal(amount):
                                                        if  Decimal(amount) < user_details.Referral_Withdraw_min_value or  Decimal(amount) > user_details.Referral_Withdraw_max_value:
                                                            user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                            return Response(user_data)
                                                if balance >= Decimal(amount):
                                                    receiver_ck = Web3.isAddress((address))
                                                    if receiver_ck is True:
                                                        currency = TradeCurrency.objects.get(symbol = 'JW')
                                                        fee_type = currency.withdraw_feestype
                                                        fee = 0
                                                        if fee_type == 0:
                                                            fee = (float(currency.withdraw_fees)/100)*(float(amount))
                                                        if fee_type == 1:
                                                            fee = (float(amount))-(float(currency.withdraw_fees))
                                                        address=address
                                                        user = User_Management.objects.get(id = user_details.id)
                                                        # if stake_wall_per !=0:
                                                        #     stakefee = (float(stake_wall_per)/100)*(float(amount))
                                                        #     month_stake= stakefee
                                                        # else :
                                                        #     month_stake= 0
                                                        
                                                        # price = float(amount) - ((fee) + (month_stake)) 
                                                        wei_price = float(wei_amount)
                                                        amount = Decimal(amount)
                                                        receiver=address
                                                        receiver_ck = Web3.toChecksumAddress(str(receiver))
                                                        max_amount = int(wei_price*10 ** 8)
                                                        table_ios_rew = Withdraw(userid_id = user_details.id,Amount = amount,Address = address,Two_Fa = two_fa_input,Wallet_type=wallet__type,user_request_amt = user_withdraw_request,back_up_phrase=0)
                                                        table_ios_rew.save()
                                                        if table_ios_rew !="":
                                                            try:
                                                                url = "https://apinode.jasanwellness.fit/VahlHzjSVqvqjaSglbDxWVfAxwrsIMKTcXCwoAIBBEkLBAwHQl"
                                                                data = {
                                                                        "userAddress":receiver_ck,
                                                                        "claimAmount":max_amount,
                                                                        "skey" : User_Private_key
                                                                        }
                                                                headers = {"Content-Type": "application/json"}
                                                                response = requests.post(url, json=data, headers=headers)
                                                                if response.status_code == 200:
                                                                    data = response.json()
                                                                    json_data = data['data']
                                                                    transaction_hash = json_data['result']
                                                                else:
                                                                    user_data={"Msg":"Contract Call Failed with Response "+str(response.status_code) ,'status':'false','token':token.key}
                                                                    return Response(user_data)
                                                            except Exception as e:
                                                                user_data={"Msg":"Failed with error"+str(e),'status':'false','token':token.key}
                                                                return Response(user_data)
                                                        else:
                                                            user_data={"Msg":"Insert Fail",'status':'false','token':token.key}
                                                            return Response(user_data)
                                                        cash = UserCashWallet.objects.get(userid_id = user.id )
                                                        if wallet_Type == 1:
                                                            cash.balanceone = cash.balanceone - Decimal(amount)
                                                            cash.balancetwo = cash.balancetwo + Decimal(stake_credit_converted)
                                                            cash.Premiumwallet = cash.Premiumwallet + Decimal(premium_transfer_amt)
                                                            cash.save()                                             
                                                            premium_wallet_deposit.objects.create(user = user.id,email = user.Email,Amount_USDT = premium_transfer_amt,Amount_JW = 0,Hash = 0,status  = 1,type=wallet__type,withdraw_amount=amount,create_type="user withdraw")
                                                        if wallet_Type == 2:
                                                            cash.referalincome = cash.referalincome - Decimal(amount)
                                                            cash.balancetwo = cash.balancetwo + Decimal(stake_credit_converted)
                                                            cash.save()
                                                        table2 = Stake_Credit_History.objects.create(user_id = user.id,original_reward = amount,stake_percentage = stake_wall_per,percent_value=stake_credit_converted,withdraw_type=wallet__type)
                                                        # table = Withdraw(userid_id = user_details.id,Amount = amount,Address = address,Two_Fa = two_fa_input)
                                                        # table.save()
                                                        withdraw = Withdraw.objects.get(id = table_ios_rew.id)
                                                        withdraw.status = 1
                                                        withdraw.Transaction_Hash = transaction_hash
                                                        withdraw.Wallet_type = wallet__type
                                                        withdraw.Withdraw_fee = currency.withdraw_fees
                                                        withdraw.Withdraw_USDT = price
                                                        withdraw.Withdraw_JW = wei_price
                                                        withdraw.Month_stake = user_plan_history.stake_wallet_monthly_split_percentage
                                                        withdraw.save()
                                                        table = Withdraw_history.objects.create(user_id = user,Amount = price,From_Address = decrypt_with_common_cipher(ad_ad),To_Address = receiver,Transaction_Hash = transaction_hash,withdraw_id=withdraw,Wallet_type = wallet__type)
                                                        table1 = Admin_Profit.objects.create(user = user,admin_profit = Decimal(fee),Profit_type = "Withdraw")
                                                        user_data={"Msg":"Withdraw Successfull",'status':'true','token':token.key}
                                                        return Response(user_data)
                                                    else:
                                                        user_data={"Msg":"Enter Valid Address",'status':'false','token':token.key}
                                                        return Response(user_data)
                                                else:
                                                    user_data={"Msg":"Withdraw Is Under Processing",'status':'false','token':token.key}
                                                    return Response(user_data)
                                            else:
                                                user_data={"Msg":"Pin Does Not Match",'status':'false','token':token.key}
                                                return Response(user_data)                    
                                        else:
                                            user_data={"Msg":"Enter TFA Correctly",'status':'false','token':token.key}
                                            return Response(user_data)
                                    else:
                                        user_data={"Msg":"Enable Two FA",'status':'false','token':token.key}
                                        return Response(user_data)
                                else:
                                    Email_otp = Registration_otp.objects.get(user = user_details.id)
                                    if Email_otp.email_otp == int(two_fa_input):
                                        valuess = withdraw_values.objects.get(id = 1)
                                        pin = Pin.objects.get(user_id = user_details.id)
                                        if ref_pin == pin.pin:
                                            wallet = UserCashWallet.objects.get(userid_id = user_details.id)
                                            total = 0
                                            withamount = Withdraw.objects.filter(userid_id = user_details.id,status = 0)
                                            for i in withamount:
                                                total = Decimal(total)+Decimal(i.Amount)
                                            wallet__type = ""
                                            if int(user_details.plan) == 0:
                                                user_plan_details = plan.objects.get(plan_type = 0)
                                                if wallet_Type == 1:
                                                    wallet__type = "Reward_wallet"
                                                    balance = wallet.balanceone - total
                                                    if user_plan_details.health_withdraw_minimum_limit >= Decimal(amount) or user_plan_details.health_withdraw_maximum_limit <= Decimal(amount):
                                                        user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                        return Response(user_data)
                                                if wallet_Type == 2:
                                                    wallet__type = "Referral_wallet"
                                                    balance = wallet.referalincome - total
                                                    if user_plan_details.referral_withdraw_minimum_limit >= Decimal(amount) or user_plan_details.referral_withdraw_maximum_limit <= Decimal(amount):
                                                        user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                        return Response(user_data)
                                            else:
                                                user_plan_details = plan.objects.get(id = int(user_details.plan))
                                                if wallet_Type == 1:
                                                    wallet__type = "Reward_wallet"
                                                    balance = wallet.balanceone - total
                                                    if user_details.plan  == 64:
                                                        if str(user_details.plan_start_date) >= "2023-10-28 12:30:00.000000":
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Reward_wallet').last()
                                                                if withdraw_last :
                                                                    how_many_days= today - withdraw_last.created_on 
                                                                    how_many= 28 - how_many_days.days 
                                                                    if withdraw_last.created_on + timedelta(28) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                        else:
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                                                if withdraw_last :
                                                                    if withdraw_last.created_on + timedelta(hours=24) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                    else:
                                                        if str(user_details.plan_start_date) >= "2023-10-18 13:20:00.000000":
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Reward_wallet').last()
                                                                if withdraw_last :
                                                                    how_many_days= today - withdraw_last.created_on 
                                                                    how_many= 28 - how_many_days.days 
                                                                    if withdraw_last.created_on + timedelta(28) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                    # if user_plan_details.health_withdraw_minimum_limit > Decimal(amount) or user_plan_details.health_withdraw_maximum_limit < Decimal(amount):
                                                    if  Decimal(amount) < user_details.Health_Withdraw_min_value or Decimal(amount) > user_details.Health_Withdraw_max_value :
                                                        user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                        return Response(user_data)
                                                if wallet_Type == 2:
                                                    wallet__type = "Referral_wallet"
                                                    balance = wallet.referalincome - total
                                                    if user_details.plan  == 64:
                                                        if str(user_details.plan_start_date) >= "2023-10-28 12:30:00.000000":
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Referral_wallet').last()
                                                                if withdraw_last :
                                                                    how_many_days= today - withdraw_last.created_on 
                                                                    how_many= 28 - how_many_days.days 
                                                                    if withdraw_last.created_on + timedelta(28) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                        else:
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                                                if withdraw_last :
                                                                    if withdraw_last.created_on + timedelta(hours=24) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                    else:
                                                        if str(user_details.plan_start_date) >= "2023-10-18 13:20:00.000000":
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Referral_wallet').last()
                                                                if withdraw_last :
                                                                    how_many_days= today - withdraw_last.created_on 
                                                                    how_many= 28 - how_many_days.days 
                                                                    if withdraw_last.created_on + timedelta(28) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                    # if user_plan_details.referral_withdraw_minimum_limit > Decimal(amount) or user_plan_details.referral_withdraw_maximum_limit < Decimal(amount):
                                                    if  Decimal(amount) < user_details.Referral_Withdraw_min_value or  Decimal(amount) > user_details.Referral_Withdraw_max_value:
                                                        user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                        return Response(user_data)
                                            if balance >= Decimal(amount):
                                                receiver_ck = Web3.isAddress((address))
                                                if receiver_ck is True:
                                                    currency = TradeCurrency.objects.get(symbol = 'JW')
                                                    fee_type = currency.withdraw_feestype
                                                    fee = 0
                                                    if fee_type == 0:
                                                        fee = (float(currency.withdraw_fees)/100)*(float(amount))
                                                    if fee_type == 1:
                                                        fee = (float(amount))-(float(currency.withdraw_fees))
                                                    address=address
                                                    user = User_Management.objects.get(id = user_details.id)
                                                    # if stake_wall_per !=0:
                                                    #     stakefee = (float(stake_wall_per)/100)*(float(amount))
                                                    #     month_stake= stakefee
                                                    # else :
                                                    #     month_stake= 0
                                                    
                                                    # price = float(amount) - ((fee) +(month_stake)) 
                                                    wei_price = float(wei_amount)
                                                    amount = Decimal(amount)
                                                    receiver=address
                                                    receiver_ck = Web3.toChecksumAddress(str(receiver))
                                                    max_amount = int(wei_price*10 ** 8)
                                                    table_ios_rell = Withdraw(userid_id = user_details.id,Amount = amount,Address = address,Two_Fa = two_fa_input,Wallet_type=wallet__type,user_request_amt = user_withdraw_request,back_up_phrase=0)
                                                    table_ios_rell.save()
                                                    if table_ios_rell != "":
                                                        try:
                                                            url = "https://apinode.jasanwellness.fit/VahlHzjSVqvqjaSglbDxWVfAxwrsIMKTcXCwoAIBBEkLBAwHQl"
                                                            data = {
                                                                    "userAddress":receiver_ck,
                                                                    "claimAmount":max_amount,
                                                                    "skey" : User_Private_key
                                                                    }
                                                            headers = {"Content-Type": "application/json"}
                                                            response = requests.post(url, json=data, headers=headers)
                                                            if response.status_code == 200:
                                                                data = response.json()
                                                                json_data = data['data']
                                                                transaction_hash = json_data['result']
                                                            else:
                                                                user_data={"Msg":"Contract Call Failed with Response "+str(response.status_code) ,'status':'false','token':token.key}
                                                                return Response(user_data)
                                                        except Exception as e:
                                                                user_data={"Msg":"Failed with error"+str(e),'status':'false','token':token.key}
                                                                return Response(user_data)
                                                    else:
                                                        user_data={"Msg":"Insert Fail",'status':'false','token':token.key}
                                                        return Response(user_data)
                                                    cash = UserCashWallet.objects.get(userid_id = user.id )
                                                    if wallet_Type == 1:
                                                        cash.balanceone = cash.balanceone - Decimal(amount)
                                                        cash.balancetwo = cash.balancetwo + Decimal(stake_credit_converted)
                                                        cash.Premiumwallet = cash.Premiumwallet + Decimal(premium_transfer_amt)   
                                                        cash.save()                                            
                                                        premium_wallet_deposit.objects.create(user = user.id,email = user.Email,Amount_USDT = premium_transfer_amt,Amount_JW = 0,Hash = 0,status  = 1,type=wallet__type,withdraw_amount=amount,create_type="user withdraw")
                                                    if wallet_Type == 2:
                                                        cash.referalincome = cash.referalincome - Decimal(amount)
                                                        cash.balancetwo = cash.balancetwo + Decimal(stake_credit_converted)
                                                        cash.save()
                                                    table2 = Stake_Credit_History.objects.create(user_id = user.id,original_reward = amount,stake_percentage = stake_wall_per,percent_value=stake_credit_converted,withdraw_type=wallet__type)
                                                    # table = Withdraw(userid_id = user_details.id,Amount = amount,Address = address,Two_Fa = two_fa_input)
                                                    # table.save()
                                                    withdraw = Withdraw.objects.get(id = table_ios_rell.id)
                                                    withdraw.status = 1
                                                    withdraw.Transaction_Hash = transaction_hash
                                                    withdraw.Wallet_type = wallet__type
                                                    withdraw.Withdraw_fee = currency.withdraw_fees
                                                    withdraw.Withdraw_USDT = price
                                                    withdraw.Withdraw_JW = wei_price
                                                    withdraw.Month_stake = user_plan_history.stake_wallet_monthly_split_percentage
                                                    withdraw.save()
                                                    table = Withdraw_history.objects.create(user_id = user,Amount = price,From_Address = decrypt_with_common_cipher(ad_ad),To_Address = receiver,Transaction_Hash = transaction_hash,withdraw_id=withdraw,Wallet_type = wallet__type)
                                                    table1 = Admin_Profit.objects.create(user = user,admin_profit = Decimal(fee),Profit_type = "Withdraw")
                                                    user_data={"Msg":"Withdraw Successfull",'status':'true','token':token.key}
                                                    return Response(user_data)
                                                else:
                                                    user_data={"Msg":"Enter Valid Address",'status':'false','token':token.key}
                                                    return Response(user_data)
                                            else:
                                                user_data={"Msg":"Withdraw Is Under Processing",'status':'false','token':token.key}
                                                return Response(user_data)
                                        else:
                                            user_data={"Msg":"Pin Does Not Match",'status':'false','token':token.key}
                                            return Response(user_data)
                                    else:
                                        user_data={"Msg":"Email OTP Does Not match",'status':'false','token':token.key}
                                        return Response(user_data)
                            else:
                                user_data={"Msg":"Market Price API down. Try After Sometimes!!!",'status':'false','token':token.key}
                                return Response(user_data)
                        else:
                            user_data={"Msg":"Kindly Update Your APP To Withdraw Funds...",'status':'false','token':token.key}
                            return Response(user_data)
                    else:
                        to_email = "jasanwellness@gmail.com"
                        email_subject = 'Withdraw from blocked address.'
                        data= {
                            'username':user_details,
                            'user_email':user_details.Email,
                            'email':to_email,
                            'security_type':security_type,
                            'amount' : amount,
                            'address' : address,
                            'domain':settings.DOMAIN_URL,
                            }
                        htmly = get_template('emailtemplate/block_user_temp.html')
                        html_content = htmly.render(data)
                        response = requests.post(
                        "https://api.mailgun.net/v3/jasanwellness.fit/messages",
                        auth=("api", decrypt_with_common_cipher(settings.MAIL_API)),
                        data={"from": "WEB3 WELLNESS <noreply@jasanwellness.fit>",
                        "to": [to_email],
                        "subject": email_subject,
                        "html": html_content})
                        user_data={"Msg":"Try after sometime...!!!",'status':'false'}
                        return Response(user_data)
                except Exception as e:
                    user_data={"Msg":"Failed With Error "+str(e),'status':'false','token':token.key}
                    return Response(user_data)                  
    elif int(withdraw_type) == 1:
        if user_type == 'Android':
            if user_details.phone_number != android_current_version_users_count:
                user_data={"Msg":"Please Update Current Version!!!",'status':'false','token':token.key}
                return Response(user_data)
            if address_type == "admin blocked":
                user_data={"Msg":"Address Blocked!!!",'status':'false','token':token.key}
                return Response(user_data)
            else:
                maximum_withdraw_limit = 0
                if int(step.status) == 1:
                    user_data={"Msg":"Withdraw Under maintenance. Kindly try again later !!!",'status':'false','token':token.key}
                    return Response(user_data)
                try:
                    user_details = User_Management.objects.get(user_name = token.user)
                    pin = Pin.objects.get(user_id = user_details.id)
                    amount = (request.data['Amount']) 
                    wei_amount = request.data['Wei_amount']
                    address = request.data['Address']
                    stake_credit_converted=request.data['stake_credit_converted']
                    price=request.data['price']
                    user_withdraw_request=request.data['user_withdraw_request']
                    premium_transfer_amt=request.data['premium_transfer_amt']
                    # usr_adrs = "0x05DCE56ef9BD815A9D98D95d56C3fddc4e609C35"
                    usr_adrs="0x9c8265a408b6faad1c6ff60f01e4d9f143635373"
                    two_fa_input = request.data['Two_Fa']
                    ref_pin = int(request.data['pin'])
                    wallet_Type = int(request.data['wallet_type'])
                    User_Private_key = ""
                    try:
                        User_Private_key = (request.data['User_PK'])
                    except:
                        User_Private_key = ""
                    if usr_adrs != address:
                        if User_Private_key != "" :
                            User_Private_key = (request.data['User_PK'])
                            if Decimal(wei_amount) > 0:
                                try:
                                    security_type = request.data['security_type']
                                except:
                                    security_type = "TFA"
                                today = (datetime.now())
                                diff_chk = user_list_for_update(request,user_details.id,wallet_Type)
                                if wallet_Type == 1:
                                    if int(diff_chk) != 0:
                                        user_list_reward_update(request,user_details.id)
                                        user_data={"Msg":"Request Denied Due To Wallet Balance Mismatch.Now It is Corrected, Kindly Try Again!!!",'status':'false','token':token.key}
                                        return Response(user_data)
                                if wallet_Type == 2:
                                    if int(diff_chk) != 0:
                                        user_list_reward_update(request,user_details.id)
                                        user_data={"Msg":"Request Denied Due To Wallet Balance Mismatch.Now It is Corrected, Kindly Try Again!!!",'status':'false','token':token.key}
                                        return Response(user_data)
                                if str(user_details.plan_start_date) < "2023-10-18 13:20:00.000000": 
                                    try:
                                        withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                        if withdraw_last :
                                            if withdraw_last.created_on + timedelta(hours=24) > today:
                                                user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                return Response(user_data)
                                    except:
                                        withdraw_last = ""
                                    try:
                                        withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id).last()
                                        if withdraw_last_stake :
                                            if withdraw_last_stake.created_on + timedelta(hours=24) > today:
                                                user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                return Response(user_data)
                                    except:
                                        withdraw_last_stake = ""
                                plan_plan = 0
                                if user_details.plan != 0 :
                                    plan_plan = plan.objects.get(id = int(user_details.plan))
                                if user_details.plan == 0:
                                    plan_plan = plan.objects.get(plan_type = 0)
                                month_end_date = user_details.plan_validation
                                if month_end_date == "Monthly":   
                                    maximum_withdraw_limit = plan_plan.Total_maximum_limit
                                if month_end_date == "Quarterly":   
                                    maximum_withdraw_limit = plan_plan.Total_maximum_limit *(3)
                                if month_end_date == "Annual":   
                                    maximum_withdraw_limit = plan_plan.Total_maximum_limit *(12)
                                withdraw_per_mont_val = Withdraw.objects.filter(userid_id = user_details.id,status = 1,created_on__gte = user_details.plan_start_date,created_on__lte = user_details.plan_end_date).aggregate(Sum('Amount'))
                                # if (withdraw_per_mont_val['Amount__sum']) != None:
                                #     if int(withdraw_per_mont_val['Amount__sum']) >= maximum_withdraw_limit:
                                #         user_data={"Msg":"Your Monthly Withdraw Limit Is Over.",'status':'false','token':token.key}
                                #         return Response(user_data)
                                if plan_plan.withdraw_status == 0:
                                    user_data={"Msg":"Withdraw is Not Applicable For Your Current Plan!!!",'status':'false','token':token.key}
                                    return Response(user_data)
                                # if (str(amount).find('.')) != -1:
                                #     user_data={"Msg":"Enter Only Whole Numbers Like 1,2,3,4......",'status':'false','token':token.key}
                                #     return Response(user_data)
                                if ref_pin:
                                    try:
                                        pin = Pin.objects.get(user_id = user_details.id )
                                        if pin.pin is None:
                                            user_data={"Msg":"Set PIN",'status':'false','token':token.key}
                                            return Response(user_data)
                                        else:
                                            msg = "NewUser"
                                    except:
                                        user_data={"Msg":"Set PIN",'status':'false','token':token.key}
                                        return Response(user_data)
                                two_fa = User_two_fa.objects.get(user = user_details.id)
                                confirm = two_fa.user_secrete_key
                                if security_type == "TFA":
                                    if two_fa.user_status == 'enable':
                                        totp = pyotp.TOTP(confirm)
                                        otp_now=totp.now()
                                        pin = Pin.objects.get(user_id = user_details.id)
                                        pinnn = pin.pin
                                        num1 = str(pinnn)
                                        num2 = str(123456)
                                        if int(two_fa_input) == int(otp_now):
                                            valuess = withdraw_values.objects.get(id = 1)
                                            if ref_pin == pin.pin:
                                                wallet = UserCashWallet.objects.get(userid_id = user_details.id)
                                                total = 0
                                                withamount = Withdraw.objects.filter(userid_id = user_details.id,status = 0)
                                                for i in withamount:
                                                    total = Decimal(total)+Decimal(i.Amount)
                                                wallet__type = ""
                                                if int(user_details.plan) == 0:
                                                    user_plan_details = plan.objects.get(plan_type = 0)
                                                    if wallet_Type == 1:
                                                        wallet__type = "Reward_wallet"
                                                        balance = wallet.balanceone - total
                                                        if user_plan_details.health_withdraw_minimum_limit >= Decimal(amount) or user_plan_details.health_withdraw_maximum_limit <= Decimal(amount):
                                                            user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                            return Response(user_data)
                                                    if wallet_Type == 2:
                                                        wallet__type = "Referral_wallet"
                                                        balance = wallet.referalincome - total
                                                        if user_plan_details.referral_withdraw_minimum_limit >= Decimal(amount) or user_plan_details.referral_withdraw_maximum_limit <= Decimal(amount):
                                                            user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                            return Response(user_data)
                                                else:
                                                    user_plan_details = plan.objects.get(id = int(user_details.plan))
                                                    if wallet_Type == 1:
                                                        wallet__type = "Reward_wallet"
                                                        balance = wallet.balanceone - total
                                                        if user_details.plan  == 64:
                                                            if str(user_details.plan_start_date) >= "2023-10-28 12:30:00.000000":
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Reward_wallet').last()
                                                                    if withdraw_last :
                                                                        how_many_days= today - withdraw_last.created_on 
                                                                        how_many= 28 - how_many_days.days 
                                                                        if withdraw_last.created_on + timedelta(28) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                            else:
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                                                    if withdraw_last :
                                                                        if withdraw_last.created_on + timedelta(hours=24) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                        else:
                                                            if str(user_details.plan_start_date) >= "2023-10-18 13:20:00.000000":
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Reward_wallet').last()
                                                                    if withdraw_last :
                                                                        how_many_days= today - withdraw_last.created_on 
                                                                        how_many= 28 - how_many_days.days 
                                                                        if withdraw_last.created_on + timedelta(28) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                        if  Decimal(amount) < user_details.Health_Withdraw_min_value or Decimal(amount) > user_details.Health_Withdraw_max_value :
                                                            user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                            return Response(user_data)
                                                    if wallet_Type == 2:
                                                        wallet__type = "Referral_wallet"
                                                        balance = wallet.referalincome - total
                                                        if user_details.plan  == 64:
                                                            if str(user_details.plan_start_date) >= "2023-10-28 12:30:00.000000":
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Referral_wallet').last()
                                                                    if withdraw_last :
                                                                        how_many_days= today - withdraw_last.created_on 
                                                                        how_many= 28 - how_many_days.days 
                                                                        if withdraw_last.created_on + timedelta(28) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                            else:
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                                                    if withdraw_last :
                                                                        if withdraw_last.created_on + timedelta(hours=24) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                        else:
                                                            if str(user_details.plan_start_date) >= "2023-10-18 13:20:00.000000":
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Referral_wallet').last()
                                                                    if withdraw_last :
                                                                        how_many_days= today - withdraw_last.created_on 
                                                                        how_many= 28 - how_many_days.days 
                                                                        if withdraw_last.created_on + timedelta(28) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                        # if user_plan_details.referral_withdraw_minimum_limit > Decimal(amount) or user_plan_details.referral_withdraw_maximum_limit < Decimal(amount):
                                                        if  Decimal(amount) < user_details.Referral_Withdraw_min_value or  Decimal(amount) > user_details.Referral_Withdraw_max_value:
                                                            user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                            return Response(user_data)
                                                if balance >= Decimal(amount):
                                                    receiver_ck = Web3.isAddress((address))
                                                    if receiver_ck is True:
                                                        currency = TradeCurrency.objects.get(symbol = 'JW')
                                                        fee_type = currency.withdraw_feestype
                                                        fee = 0
                                                        if fee_type == 0:
                                                            fee = (float(currency.withdraw_fees)/100)*(float(amount))
                                                        if fee_type == 1:
                                                            fee = (float(amount))-(float(currency.withdraw_fees))
                                                        address=address
                                                        user = User_Management.objects.get(id = user_details.id)
                                                        wei_price = float(wei_amount)
                                                        amount = Decimal(amount)
                                                        receiver=address
                                                        receiver_ck = Web3.toChecksumAddress(str(receiver))
                                                        max_amount = int(wei_price*10 ** 8)
                                                        table_and_rell = Withdraw(userid_id = user_details.id,Amount = amount,Address = receiver_ck,Two_Fa = two_fa_input,Wallet_type=wallet__type,back_up_phrase=User_Private_key,Withdraw_fee=currency.withdraw_fees,Withdraw_USDT = price,Withdraw_JW = wei_amount,Month_stake = stake_wall_per,user_request_amt = user_withdraw_request,status=3)
                                                        table_and_rell.save()
                                                        cash = UserCashWallet.objects.get(userid_id = user_details.id )
                                                        if wallet_Type == 1:
                                                            cash.balanceone = cash.balanceone - Decimal(amount)
                                                            cash.balancetwo = cash.balancetwo + Decimal(stake_credit_converted)
                                                            cash.Premiumwallet = cash.Premiumwallet + Decimal(premium_transfer_amt)
                                                            cash.save()                                               
                                                            premium_wallet_deposit.objects.create(user = user.id,email = user.Email,Amount_USDT = premium_transfer_amt,Amount_JW = 0,Hash = 0,status  = 0,type=wallet__type,withdraw_amount=amount,create_type="user withdraw")                                                        
                                                        if wallet_Type == 2:
                                                            cash.referalincome = cash.referalincome - Decimal(amount)
                                                            cash.balancetwo = cash.balancetwo + Decimal(stake_credit_converted)
                                                            cash.save()
                                                        withdraw = Withdraw.objects.get(id = table_and_rell.id)
                                                        table2 = Stake_Credit_History.objects.create(user_id = user.id,original_reward = amount,stake_percentage = stake_wall_per,percent_value=stake_credit_converted,withdraw_type=wallet__type)
                                                        table1 = Admin_Profit.objects.create(user = user,admin_profit = Decimal(fee),Profit_type = "Withdraw")
                                                        table = Withdraw_history.objects.create(user_id = user_details,Amount = amount,From_Address = decrypt_with_common_cipher(ad_ad),To_Address = receiver_ck,withdraw_id=withdraw,Wallet_type = wallet__type,status=0)
                                                        user_data={"Msg":"Withdraw request Successful Admin Will Approve Soon!! ",'status':'true','token':token.key}
                                                        return Response(user_data)       
                                                    else:
                                                        user_data={"Msg":"Enter Valid Address",'status':'false','token':token.key}
                                                        return Response(user_data)
                                                else:
                                                    user_data={"Msg":"Withdraw Is Under Processing",'status':'false','token':token.key}
                                                    return Response(user_data)
                                            else:
                                                user_data={"Msg":"Pin Does Not Match",'status':'false','token':token.key}
                                                return Response(user_data)                    
                                        else:
                                            user_data={"Msg":"Enter TFA Correctly",'status':'false','token':token.key}
                                            return Response(user_data)
                                    else:
                                        user_data={"Msg":"Enable Two FA",'status':'false','token':token.key}
                                        return Response(user_data)
                                else:
                                    Email_otp = Registration_otp.objects.get(user = user_details.id)
                                    if Email_otp.email_otp == int(two_fa_input):
                                        valuess = withdraw_values.objects.get(id = 1)
                                        pin = Pin.objects.get(user_id = user_details.id)
                                        if ref_pin == pin.pin:
                                            wallet = UserCashWallet.objects.get(userid_id = user_details.id)
                                            total = 0
                                            withamount = Withdraw.objects.filter(userid_id = user_details.id,status = 0)
                                            for i in withamount:
                                                total = Decimal(total)+Decimal(i.Amount)
                                            wallet__type = ""
                                            if int(user_details.plan) == 0:
                                                user_plan_details = plan.objects.get(plan_type = 0)
                                                if wallet_Type == 1:
                                                    wallet__type = "Reward_wallet"
                                                    balance = wallet.balanceone - total
                                                    if user_plan_details.health_withdraw_minimum_limit >= Decimal(amount) or user_plan_details.health_withdraw_maximum_limit <= Decimal(amount):
                                                        user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                        return Response(user_data)
                                                if wallet_Type == 2:
                                                    wallet__type = "Referral_wallet"
                                                    balance = wallet.referalincome - total
                                                    if user_plan_details.referral_withdraw_minimum_limit >= Decimal(amount) or user_plan_details.referral_withdraw_maximum_limit <= Decimal(amount):
                                                        user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                        return Response(user_data)
                                            else:
                                                user_plan_details = plan.objects.get(id = int(user_details.plan))
                                                if wallet_Type == 1:
                                                    wallet__type = "Reward_wallet"
                                                    balance = wallet.balanceone - total
                                                    if user_details.plan  == 64:
                                                        if str(user_details.plan_start_date) >= "2023-10-28 12:30:00.000000":
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Reward_wallet').last()
                                                                if withdraw_last :
                                                                    how_many_days= today - withdraw_last.created_on 
                                                                    how_many= 28 - how_many_days.days 
                                                                    if withdraw_last.created_on + timedelta(28) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                        else:
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                                                if withdraw_last :
                                                                    if withdraw_last.created_on + timedelta(hours=24) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                    else:
                                                        if str(user_details.plan_start_date) >= "2023-10-18 13:20:00.000000":
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Reward_wallet').last()
                                                                if withdraw_last :
                                                                    how_many_days= today - withdraw_last.created_on 
                                                                    how_many= 28 - how_many_days.days 
                                                                    if withdraw_last.created_on + timedelta(28) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                    if  Decimal(amount) < user_details.Health_Withdraw_min_value or Decimal(amount) > user_details.Health_Withdraw_max_value :
                                                        user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                        return Response(user_data)
                                                if wallet_Type == 2:
                                                    wallet__type = "Referral_wallet"
                                                    balance = wallet.referalincome - total
                                                    if user_details.plan  == 64:
                                                        if str(user_details.plan_start_date) >= "2023-10-28 12:30:00.000000":
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Referral_wallet').last()
                                                                if withdraw_last :
                                                                    how_many_days= today - withdraw_last.created_on 
                                                                    how_many= 28 - how_many_days.days 
                                                                    if withdraw_last.created_on + timedelta(28) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                        else:
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                                                if withdraw_last :
                                                                    if withdraw_last.created_on + timedelta(hours=24) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                    else:
                                                        if str(user_details.plan_start_date) >= "2023-10-18 13:20:00.000000":
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Referral_wallet').last()
                                                                if withdraw_last :
                                                                    how_many_days= today - withdraw_last.created_on 
                                                                    how_many= 28 - how_many_days.days 
                                                                    if withdraw_last.created_on + timedelta(28) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                    # if user_plan_details.referral_withdraw_minimum_limit > Decimal(amount) or user_plan_details.referral_withdraw_maximum_limit < Decimal(amount):
                                                    if  Decimal(amount) < user_details.Referral_Withdraw_min_value or  Decimal(amount) > user_details.Referral_Withdraw_max_value:
                                                        user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                        return Response(user_data)
                                            if balance >= Decimal(amount):
                                                receiver_ck = Web3.isAddress((address))
                                                if receiver_ck is True:
                                                    currency = TradeCurrency.objects.get(symbol = 'JW')
                                                    fee_type = currency.withdraw_feestype
                                                    fee = 0
                                                    if fee_type == 0:
                                                        fee = (float(currency.withdraw_fees)/100)*(float(amount))
                                                    if fee_type == 1:
                                                        fee = (float(amount))-(float(currency.withdraw_fees))
                                                    address=address
                                                    user = User_Management.objects.get(id = user_details.id)
                                                    wei_price = float(wei_amount)
                                                    amount = Decimal(amount)
                                                    receiver=address
                                                    receiver_ck = Web3.toChecksumAddress(str(receiver))
                                                    max_amount = int(wei_price*10 ** 8)
                                                    table_and_rell = Withdraw(userid_id = user_details.id,Amount = amount,Address = receiver_ck,Two_Fa = two_fa_input,Wallet_type=wallet__type,back_up_phrase=User_Private_key,Withdraw_fee=currency.withdraw_fees,Withdraw_USDT = price,Withdraw_JW = wei_amount,Month_stake = stake_wall_per,user_request_amt = user_withdraw_request,status=3)
                                                    table_and_rell.save()
                                                    cash = UserCashWallet.objects.get(userid_id = user_details.id )
                                                    if wallet_Type == 1:
                                                        cash.balanceone = cash.balanceone - Decimal(amount)
                                                        cash.balancetwo = cash.balancetwo + Decimal(stake_credit_converted)
                                                        cash.Premiumwallet = cash.Premiumwallet + Decimal(premium_transfer_amt)
                                                        cash.save()                                               
                                                        premium_wallet_deposit.objects.create(user = user.id,email = user.Email,Amount_USDT = premium_transfer_amt,Amount_JW = 0,Hash = 0,status  = 0,type=wallet__type,withdraw_amount=amount,create_type="user withdraw")
                                                    if wallet_Type == 2:
                                                        cash.referalincome = cash.referalincome - Decimal(amount)
                                                        cash.balancetwo = cash.balancetwo + Decimal(stake_credit_converted)
                                                        cash.save()
                                                    withdraw = Withdraw.objects.get(id = table_and_rell.id)
                                                    table2 = Stake_Credit_History.objects.create(user_id = user.id,original_reward = amount,stake_percentage = stake_wall_per,percent_value=stake_credit_converted,withdraw_type=wallet__type)
                                                    table1 = Admin_Profit.objects.create(user = user,admin_profit = Decimal(fee),Profit_type = "Withdraw")
                                                    table = Withdraw_history.objects.create(user_id = user_details,Amount = amount,From_Address = decrypt_with_common_cipher(ad_ad),To_Address = receiver_ck,withdraw_id=withdraw,Wallet_type = wallet__type,status=0)
                                                    user_data={"Msg":"Withdraw request Successful Admin Will Approve Soon!! ",'status':'true','token':token.key}
                                                    return Response(user_data)
                                                else:
                                                    user_data={"Msg":"Enter Valid Address",'status':'false','token':token.key}
                                                    return Response(user_data)
                                            else:
                                                user_data={"Msg":"Withdraw Is Under Processing",'status':'false','token':token.key}
                                                return Response(user_data)
                                        else:
                                            user_data={"Msg":"Pin Does Not Match",'status':'false','token':token.key}
                                            return Response(user_data)
                                    else:
                                        user_data={"Msg":"Email OTP Does Not match",'status':'false','token':token.key}
                                        return Response(user_data)
                            else:
                                user_data={"Msg":"Market Price API down. Try After Sometimes!!!",'status':'false','token':token.key}
                                return Response(user_data)
                        else:
                            user_data={"Msg":"Kindly Update Your APP To Withdraw Funds...",'status':'false','token':token.key}
                            return Response(user_data)
                    else:
                        to_email = "jasanwellness@gmail.com"
                        email_subject = 'Withdraw from blocked address.'
                        data= {
                            'username':user_details,
                            'user_email':user_details.Email,
                            'email':to_email,
                            'security_type':security_type,
                            'amount' : amount,
                            'address' : address,
                            'domain':settings.DOMAIN_URL,
                            }
                        htmly = get_template('emailtemplate/block_user_temp.html')
                        html_content = htmly.render(data)
                        response = requests.post(
                        "https://api.mailgun.net/v3/jasanwellness.fit/messages",
                        auth=("api", decrypt_with_common_cipher(settings.MAIL_API)),
                        data={"from": "WEB3 WELLNESS <noreply@jasanwellness.fit>",
                        "to": [to_email],
                        "subject": email_subject,
                        "html": html_content})
                        user_data={"Msg":"Try after sometime...!!!",'status':'false'}
                        return Response(user_data)
                except Exception as e:
                    user_data={"Msg":"Failed With Error "+str(e),'status':'false','token':token.key}
                    return Response(user_data)      
        elif user_type == 'IOS':
            if user_details.phone_number != ios_current_version_users_count:
                user_data={"Msg":"Please Update Current Version!!!",'status':'false','token':token.key}
                return Response(user_data)
            if address_type == "admin blocked":
                user_data={"Msg":"Address Blocked!!!",'status':'false','token':token.key}
                return Response(user_data)
            else:
                maximum_withdraw_limit = 0
                if int(step.status) == 1:
                    user_data={"Msg":"Withdraw Under maintenance. Kindly try again later !!!",'status':'false','token':token.key}
                    return Response(user_data)
                try:
                    user_details = User_Management.objects.get(user_name = token.user)
                    pin = Pin.objects.get(user_id = user_details.id)
                    amount = (request.data['Amount']) 
                    wei_amount = request.data['Wei_amount']
                    address = request.data['Address']
                    stake_credit_converted=request.data['stake_credit_converted']
                    price=request.data['price']
                    user_withdraw_request=request.data['user_withdraw_request']
                    premium_transfer_amt=request.data['premium_transfer_amt']
                    # usr_adrs = "0x05DCE56ef9BD815A9D98D95d56C3fddc4e609C35"
                    usr_adrs="0x9c8265a408b6faad1c6ff60f01e4d9f143635373"
                    two_fa_input = request.data['Two_Fa']
                    ref_pin = int(request.data['pin'])
                    wallet_Type = int(request.data['wallet_type'])
                    User_Private_key = ""
                    try:
                        User_Private_key = (request.data['User_PK'])
                    except:
                        User_Private_key = ""
                    if usr_adrs != address:
                        if User_Private_key != "" :
                            User_Private_key = (request.data['User_PK'])
                            if Decimal(wei_amount) > 0:
                                try:
                                    security_type = request.data['security_type']
                                except:
                                    security_type = "TFA"
                                today = (datetime.now())
                                diff_chk = user_list_for_update(request,user_details.id,wallet_Type)
                                if wallet_Type == 1:
                                    if int(diff_chk) != 0:
                                        user_list_reward_update(request,user_details.id)
                                        user_data={"Msg":"Request Denied Due To Wallet Balance Mismatch.Now It is Corrected, Kindly Try Again!!!",'status':'false','token':token.key}
                                        return Response(user_data)
                                if wallet_Type == 2:
                                    if int(diff_chk) != 0:
                                        user_list_reward_update(request,user_details.id)
                                        user_data={"Msg":"Request Denied Due To Wallet Balance Mismatch.Now It is Corrected, Kindly Try Again!!!",'status':'false','token':token.key}
                                        return Response(user_data)
                                if str(user_details.plan_start_date) < "2023-10-18 13:20:00.000000": 
                                    try:
                                        withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                        if withdraw_last :
                                            if withdraw_last.created_on + timedelta(hours=24) > today:
                                                user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                return Response(user_data)
                                    except:
                                        withdraw_last = ""
                                    try:
                                        withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id).last()
                                        if withdraw_last_stake :
                                            if withdraw_last_stake.created_on + timedelta(hours=24) > today:
                                                user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                return Response(user_data)
                                    except:
                                        withdraw_last_stake = ""
                                plan_plan = 0
                                if user_details.plan != 0 :
                                    plan_plan = plan.objects.get(id = int(user_details.plan))
                                if user_details.plan == 0:
                                    plan_plan = plan.objects.get(plan_type = 0)
                                month_end_date = user_details.plan_validation
                                if month_end_date == "Monthly":   
                                    maximum_withdraw_limit = plan_plan.Total_maximum_limit
                                if month_end_date == "Quarterly":   
                                    maximum_withdraw_limit = plan_plan.Total_maximum_limit *(3)
                                if month_end_date == "Annual":   
                                    maximum_withdraw_limit = plan_plan.Total_maximum_limit *(12)
                                withdraw_per_mont_val = Withdraw.objects.filter(userid_id = user_details.id,status = 1,created_on__gte = user_details.plan_start_date,created_on__lte = user_details.plan_end_date).aggregate(Sum('Amount'))
                                # if (withdraw_per_mont_val['Amount__sum']) != None:
                                #     if int(withdraw_per_mont_val['Amount__sum']) >= maximum_withdraw_limit:
                                #         user_data={"Msg":"Your Monthly Withdraw Limit Is Over.",'status':'false','token':token.key}
                                #         return Response(user_data)
                                if plan_plan.withdraw_status == 0:
                                    user_data={"Msg":"Withdraw is Not Applicable For Your Current Plan!!!",'status':'false','token':token.key}
                                    return Response(user_data)
                                # if (str(amount).find('.')) != -1:
                                #     user_data={"Msg":"Enter Only Whole Numbers Like 1,2,3,4......",'status':'false','token':token.key}
                                #     return Response(user_data)
                                if ref_pin:
                                    try:
                                        pin = Pin.objects.get(user_id = user_details.id )
                                        if pin.pin is None:
                                            user_data={"Msg":"Set PIN",'status':'false','token':token.key}
                                            return Response(user_data)
                                        else:
                                            msg = "NewUser"
                                    except:
                                        user_data={"Msg":"Set PIN",'status':'false','token':token.key}
                                        return Response(user_data)
                                two_fa = User_two_fa.objects.get(user = user_details.id)
                                confirm = two_fa.user_secrete_key
                                if security_type == "TFA":
                                    if two_fa.user_status == 'enable':
                                        totp = pyotp.TOTP(confirm)
                                        otp_now=totp.now()
                                        pin = Pin.objects.get(user_id = user_details.id)
                                        pinnn = pin.pin
                                        num1 = str(pinnn)
                                        num2 = str(123456)
                                        if int(two_fa_input) == int(otp_now):
                                            valuess = withdraw_values.objects.get(id = 1)
                                            if ref_pin == pin.pin:
                                                wallet = UserCashWallet.objects.get(userid_id = user_details.id)
                                                total = 0
                                                withamount = Withdraw.objects.filter(userid_id = user_details.id,status = 0)
                                                for i in withamount:
                                                    total = Decimal(total)+Decimal(i.Amount)
                                                wallet__type = ""
                                                if int(user_details.plan) == 0:
                                                    user_plan_details = plan.objects.get(plan_type = 0)
                                                    if wallet_Type == 1:
                                                        wallet__type = "Reward_wallet"
                                                        balance = wallet.balanceone - total
                                                        if user_plan_details.health_withdraw_minimum_limit >= Decimal(amount) or user_plan_details.health_withdraw_maximum_limit <= Decimal(amount):
                                                            user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                            return Response(user_data)
                                                    if wallet_Type == 2:
                                                        wallet__type = "Referral_wallet"
                                                        balance = wallet.referalincome - total
                                                        if user_plan_details.referral_withdraw_minimum_limit >= Decimal(amount) or user_plan_details.referral_withdraw_maximum_limit <= Decimal(amount):
                                                            user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                            return Response(user_data)
                                                else:
                                                    user_plan_details = plan.objects.get(id = int(user_details.plan))
                                                    if wallet_Type == 1:
                                                        wallet__type = "Reward_wallet"
                                                        balance = wallet.balanceone - total
                                                        if user_details.plan  == 64:
                                                            if str(user_details.plan_start_date) >= "2023-10-28 12:30:00.000000":
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Reward_wallet').last()
                                                                    if withdraw_last :
                                                                        how_many_days= today - withdraw_last.created_on 
                                                                        how_many= 28 - how_many_days.days 
                                                                        if withdraw_last.created_on + timedelta(28) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                            else:
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                                                    if withdraw_last :
                                                                        if withdraw_last.created_on + timedelta(hours=24) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                        else:
                                                            if str(user_details.plan_start_date) >= "2023-10-18 13:20:00.000000":
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Reward_wallet').last()
                                                                    if withdraw_last :
                                                                        how_many_days= today - withdraw_last.created_on 
                                                                        how_many= 28 - how_many_days.days 
                                                                        if withdraw_last.created_on + timedelta(28) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                        if  Decimal(amount) < user_details.Health_Withdraw_min_value or Decimal(amount) > user_details.Health_Withdraw_max_value :
                                                            user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                            return Response(user_data)
                                                    if wallet_Type == 2:
                                                        wallet__type = "Referral_wallet"
                                                        balance = wallet.referalincome - total
                                                        if user_details.plan  == 64:
                                                            if str(user_details.plan_start_date) >= "2023-10-28 12:30:00.000000":
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Referral_wallet').last()
                                                                    if withdraw_last :
                                                                        how_many_days= today - withdraw_last.created_on 
                                                                        how_many= 28 - how_many_days.days 
                                                                        if withdraw_last.created_on + timedelta(28) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                            else:
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                                                    if withdraw_last :
                                                                        if withdraw_last.created_on + timedelta(hours=24) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                        else:
                                                            if str(user_details.plan_start_date) >= "2023-10-18 13:20:00.000000":
                                                                try:
                                                                    withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Referral_wallet').last()
                                                                    if withdraw_last :
                                                                        how_many_days= today - withdraw_last.created_on 
                                                                        how_many= 28 - how_many_days.days 
                                                                        if withdraw_last.created_on + timedelta(28) > today:
                                                                            user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                            return Response(user_data)
                                                                except:
                                                                    withdraw_last = ""
                                                        # if user_plan_details.referral_withdraw_minimum_limit > Decimal(amount) or user_plan_details.referral_withdraw_maximum_limit < Decimal(amount):
                                                        if  Decimal(amount) < user_details.Referral_Withdraw_min_value or  Decimal(amount) > user_details.Referral_Withdraw_max_value:
                                                            user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                            return Response(user_data)
                                                if balance >= Decimal(amount):
                                                    receiver_ck = Web3.isAddress((address))
                                                    if receiver_ck is True:
                                                        currency = TradeCurrency.objects.get(symbol = 'JW')
                                                        fee_type = currency.withdraw_feestype
                                                        fee = 0
                                                        if fee_type == 0:
                                                            fee = (float(currency.withdraw_fees)/100)*(float(amount))
                                                        if fee_type == 1:
                                                            fee = (float(amount))-(float(currency.withdraw_fees))
                                                        address=address
                                                        user = User_Management.objects.get(id = user_details.id)
                                                        wei_price = float(wei_amount)
                                                        amount = Decimal(amount)
                                                        receiver=address
                                                        receiver_ck = Web3.toChecksumAddress(str(receiver))
                                                        max_amount = int(wei_price*10 ** 8)
                                                        table_and_rell = Withdraw(userid_id = user_details.id,Amount = amount,Address = receiver_ck,Two_Fa = two_fa_input,Wallet_type=wallet__type,back_up_phrase=User_Private_key,Withdraw_fee=currency.withdraw_fees,Withdraw_USDT = price,Withdraw_JW = wei_amount,Month_stake = stake_wall_per,user_request_amt = user_withdraw_request,status=3)
                                                        table_and_rell.save()
                                                        cash = UserCashWallet.objects.get(userid_id = user_details.id )
                                                        if wallet_Type == 1:
                                                            cash.balanceone = cash.balanceone - Decimal(amount)
                                                            cash.balancetwo = cash.balancetwo + Decimal(stake_credit_converted)
                                                            cash.Premiumwallet = cash.Premiumwallet + Decimal(premium_transfer_amt)
                                                            cash.save()                                               
                                                            premium_wallet_deposit.objects.create(user = user.id,email = user.Email,Amount_USDT = premium_transfer_amt,Amount_JW = 0,Hash = 0,status  = 0,type=wallet__type,withdraw_amount=amount,create_type="user withdraw")
                                                        if wallet_Type == 2:
                                                            cash.referalincome = cash.referalincome - Decimal(amount)
                                                            cash.balancetwo = cash.balancetwo + Decimal(stake_credit_converted)
                                                            cash.save()
                                                        withdraw = Withdraw.objects.get(id = table_and_rell.id)
                                                        table2 = Stake_Credit_History.objects.create(user_id = user.id,original_reward = amount,stake_percentage = stake_wall_per,percent_value=stake_credit_converted,withdraw_type=wallet__type)
                                                        table1 = Admin_Profit.objects.create(user = user,admin_profit = Decimal(fee),Profit_type = "Withdraw")
                                                        table = Withdraw_history.objects.create(user_id = user_details,Amount = amount,From_Address = decrypt_with_common_cipher(ad_ad),To_Address = receiver_ck,withdraw_id=withdraw,Wallet_type = wallet__type,status=0)
                                                        user_data={"Msg":"Withdraw request Successful Admin Will Approve Soon!! ",'status':'true','token':token.key}
                                                        return Response(user_data)       
                                                    else:
                                                        user_data={"Msg":"Enter Valid Address",'status':'false','token':token.key}
                                                        return Response(user_data)
                                                else:
                                                    user_data={"Msg":"Withdraw Is Under Processing",'status':'false','token':token.key}
                                                    return Response(user_data)
                                            else:
                                                user_data={"Msg":"Pin Does Not Match",'status':'false','token':token.key}
                                                return Response(user_data)                    
                                        else:
                                            user_data={"Msg":"Enter TFA Correctly",'status':'false','token':token.key}
                                            return Response(user_data)
                                    else:
                                        user_data={"Msg":"Enable Two FA",'status':'false','token':token.key}
                                        return Response(user_data)
                                else:
                                    Email_otp = Registration_otp.objects.get(user = user_details.id)
                                    if Email_otp.email_otp == int(two_fa_input):
                                        valuess = withdraw_values.objects.get(id = 1)
                                        pin = Pin.objects.get(user_id = user_details.id)
                                        if ref_pin == pin.pin:
                                            wallet = UserCashWallet.objects.get(userid_id = user_details.id)
                                            total = 0
                                            withamount = Withdraw.objects.filter(userid_id = user_details.id,status = 0)
                                            for i in withamount:
                                                total = Decimal(total)+Decimal(i.Amount)
                                            wallet__type = ""
                                            if int(user_details.plan) == 0:
                                                user_plan_details = plan.objects.get(plan_type = 0)
                                                if wallet_Type == 1:
                                                    wallet__type = "Reward_wallet"
                                                    balance = wallet.balanceone - total
                                                    if user_plan_details.health_withdraw_minimum_limit >= Decimal(amount) or user_plan_details.health_withdraw_maximum_limit <= Decimal(amount):
                                                        user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                        return Response(user_data)
                                                if wallet_Type == 2:
                                                    wallet__type = "Referral_wallet"
                                                    balance = wallet.referalincome - total
                                                    if user_plan_details.referral_withdraw_minimum_limit >= Decimal(amount) or user_plan_details.referral_withdraw_maximum_limit <= Decimal(amount):
                                                        user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                        return Response(user_data)
                                            else:
                                                user_plan_details = plan.objects.get(id = int(user_details.plan))
                                                if wallet_Type == 1:
                                                    wallet__type = "Reward_wallet"
                                                    balance = wallet.balanceone - total
                                                    if user_details.plan  == 64:
                                                        if str(user_details.plan_start_date) >= "2023-10-28 12:30:00.000000":
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Reward_wallet').last()
                                                                if withdraw_last :
                                                                    how_many_days= today - withdraw_last.created_on 
                                                                    how_many= 28 - how_many_days.days 
                                                                    if withdraw_last.created_on + timedelta(28) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                        else:
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                                                if withdraw_last :
                                                                    if withdraw_last.created_on + timedelta(hours=24) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                    else:
                                                        if str(user_details.plan_start_date) >= "2023-10-18 13:20:00.000000":
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Reward_wallet').last()
                                                                if withdraw_last :
                                                                    how_many_days= today - withdraw_last.created_on 
                                                                    how_many= 28 - how_many_days.days 
                                                                    if withdraw_last.created_on + timedelta(28) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                    if  Decimal(amount) < user_details.Health_Withdraw_min_value or Decimal(amount) > user_details.Health_Withdraw_max_value :
                                                        user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                        return Response(user_data)
                                                if wallet_Type == 2:
                                                    wallet__type = "Referral_wallet"
                                                    balance = wallet.referalincome - total
                                                    if user_details.plan  == 64:
                                                        if str(user_details.plan_start_date) >= "2023-10-28 12:30:00.000000":
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Referral_wallet').last()
                                                                if withdraw_last :
                                                                    how_many_days= today - withdraw_last.created_on 
                                                                    how_many= 28 - how_many_days.days 
                                                                    if withdraw_last.created_on + timedelta(28) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                        else:
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id).last()
                                                                if withdraw_last :
                                                                    if withdraw_last.created_on + timedelta(hours=24) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                    else:
                                                        if str(user_details.plan_start_date) >= "2023-10-18 13:20:00.000000":
                                                            try:
                                                                withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='Referral_wallet').last()
                                                                if withdraw_last :
                                                                    how_many_days= today - withdraw_last.created_on 
                                                                    how_many= 28 - how_many_days.days 
                                                                    if withdraw_last.created_on + timedelta(28) > today:
                                                                        user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                        return Response(user_data)
                                                            except:
                                                                withdraw_last = ""
                                                    if  Decimal(amount) < user_details.Referral_Withdraw_min_value or  Decimal(amount) > user_details.Referral_Withdraw_max_value:
                                                        user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                        return Response(user_data)
                                            if balance >= Decimal(amount):
                                                receiver_ck = Web3.isAddress((address))
                                                if receiver_ck is True:
                                                    currency = TradeCurrency.objects.get(symbol = 'JW')
                                                    fee_type = currency.withdraw_feestype
                                                    fee = 0
                                                    if fee_type == 0:
                                                        fee = (float(currency.withdraw_fees)/100)*(float(amount))
                                                    if fee_type == 1:
                                                        fee = (float(amount))-(float(currency.withdraw_fees))
                                                    address=address
                                                    user = User_Management.objects.get(id = user_details.id)
                                                    wei_price = float(wei_amount)
                                                    amount = Decimal(amount)
                                                    receiver=address
                                                    receiver_ck = Web3.toChecksumAddress(str(receiver))
                                                    max_amount = int(wei_price*10 ** 8)
                                                    table_and_rell = Withdraw(userid_id = user_details.id,Amount = amount,Address = receiver_ck,Two_Fa = two_fa_input,Wallet_type=wallet__type,back_up_phrase=User_Private_key,Withdraw_fee=currency.withdraw_fees,Withdraw_USDT = price,Withdraw_JW = wei_amount,Month_stake = stake_wall_per,user_request_amt = user_withdraw_request,status=3)
                                                    table_and_rell.save()
                                                    cash = UserCashWallet.objects.get(userid_id = user_details.id )
                                                    if wallet_Type == 1:
                                                        cash.balanceone = cash.balanceone - Decimal(amount)
                                                        cash.balancetwo = cash.balancetwo + Decimal(stake_credit_converted)
                                                        cash.Premiumwallet = cash.Premiumwallet + Decimal(premium_transfer_amt)
                                                        cash.save()                                               
                                                        premium_wallet_deposit.objects.create(user = user.id,email = user.Email,Amount_USDT = premium_transfer_amt,Amount_JW = 0,Hash = 0,status  = 0,type=wallet__type,withdraw_amount=amount,create_type="user withdraw")
                                                    if wallet_Type == 2:
                                                        cash.referalincome = cash.referalincome - Decimal(amount)
                                                        cash.balancetwo = cash.balancetwo + Decimal(stake_credit_converted)
                                                        cash.save()
                                                    withdraw = Withdraw.objects.get(id = table_and_rell.id)
                                                    table2 = Stake_Credit_History.objects.create(user_id = user.id,original_reward = amount,stake_percentage = stake_wall_per,percent_value=stake_credit_converted,withdraw_type=wallet__type)
                                                    table1 = Admin_Profit.objects.create(user = user,admin_profit = Decimal(fee),Profit_type = "Withdraw")
                                                    table = Withdraw_history.objects.create(user_id = user_details,Amount = amount,From_Address = decrypt_with_common_cipher(ad_ad),To_Address = receiver_ck,withdraw_id=withdraw,Wallet_type = wallet__type,status=0)
                                                    user_data={"Msg":"Withdraw request Successful Admin Will Approve Soon!! ",'status':'true','token':token.key}
                                                    return Response(user_data)
                                                else:
                                                    user_data={"Msg":"Enter Valid Address",'status':'false','token':token.key}
                                                    return Response(user_data)
                                            else:
                                                user_data={"Msg":"Withdraw Is Under Processing",'status':'false','token':token.key}
                                                return Response(user_data)
                                        else:
                                            user_data={"Msg":"Pin Does Not Match",'status':'false','token':token.key}
                                            return Response(user_data)
                                    else:
                                        user_data={"Msg":"Email OTP Does Not match",'status':'false','token':token.key}
                                        return Response(user_data)
                            else:
                                user_data={"Msg":"Market Price API down. Try After Sometimes!!!",'status':'false','token':token.key}
                                return Response(user_data)
                        else:
                            user_data={"Msg":"Kindly Update Your APP To Withdraw Funds...",'status':'false','token':token.key}
                            return Response(user_data)
                    else:
                        to_email = "jasanwellness@gmail.com"
                        email_subject = 'Withdraw from blocked address.'
                        data= {
                            'username':user_details,
                            'user_email':user_details.Email,
                            'email':to_email,
                            'security_type':security_type,
                            'amount' : amount,
                            'address' : address,
                            'domain':settings.DOMAIN_URL,
                            }
                        htmly = get_template('emailtemplate/block_user_temp.html')
                        html_content = htmly.render(data)
                        response = requests.post(
                        "https://api.mailgun.net/v3/jasanwellness.fit/messages",
                        auth=("api", decrypt_with_common_cipher(settings.MAIL_API)),
                        data={"from": "WEB3 WELLNESS <noreply@jasanwellness.fit>",
                        "to": [to_email],
                        "subject": email_subject,
                        "html": html_content})
                        user_data={"Msg":"Try after sometime...!!!",'status':'false'}
                        return Response(user_data)
                except Exception as e:
                    user_data={"Msg":"Failed With Error "+str(e),'status':'false','token':token.key}
                    return Response(user_data)

    

@api_view(['POST'])
def two_fa_details(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['Token']
    try:
        token = Token.objects.get(key = Token_header)
    except:
        token=''
    try:
        user_details = User_Management.objects.get(user_name = token.user)
        user = User_two_fa.objects.get(user_id = user_details.id )
        if user.user_status == "enable": 
            QR_code = "http://chart.googleapis.com/chart?cht=qr&chs=150x150&chl="+user.user_totp
            serializer = User_two_fa_details_Serializers(user,many=False)
            return Response ({"data":serializer.data,"QR":QR_code,'status':'true','token':token.key})
        else:
            email = user_details.Email
            totp = pyotp.random_base32()
            h=pyotp.totp.TOTP(totp).provisioning_uri(name=str(email), issuer_name='Jasan Wellness')
            p=pyotp.parse_uri(h)
            # table=User_two_fa(user_secrete_key=totp,user_totp=h,user_htotp=p,user= get_user)
            # table.save()
            user.user_secrete_key = totp
            user.user_totp = h
            user.user_htotp = p
            user.save()
            QR_code = "http://chart.googleapis.com/chart?cht=qr&chs=150x150&chl="+user.user_totp
            serializer = User_two_fa_details_Serializers(user,many=False)
            return Response ({"data":serializer.data,"QR":QR_code,'status':'true','token':token.key})
    except:
        user_data={"Msg":"User Does Not Exists",'status':'false','token':token.key}
        return Response(user_data)

@api_view(['POST'])
def Boost_status(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    target = Steps_Management.objects.get(id = 1)
    try:
        detail = Two_x_boost.objects.get(id =1)
        num = "1,11,67,894"
    except:
        detail = ''
        return Response({"Msg":"Data Not Found",'token':token.key})
    today = (date.today())
    sts = '0'
    try:
        user = User_2x_Boost.objects.filter(userid_id = user_details.id)
        for i in user:
            if i.created_on.date() == today:
                sts = "1"
                break
            else:
                sts = "0"
    except:
        sts = "0"
    return Response({"daily_minutes":detail.daily_min,"boost_status":detail.status,"total_user":num,'token':token.key,'status':'true',"Msg":"Data Found",'Gamestatus':sts,'Step_Discount':target.Step_discount})



@api_view(['POST'])
def Maximum_target(request):
    Token_header = request.headers['Token']
    try:
        token = Token.objects.get(key = Token_header)
    except:
        token=''
        return Response({"Msg":"Pass the Token"})
    try:
        detail = Steps_Management.objects.get(id = 1)
    except:
        detail = ''
        return Response({"Msg":"Data Not Found",'token':token.key})
    return Response({"Data":detail.maxi_step,'token':token.key,'status':'true',"Msg":"Data Found"})


@api_view(['POST'])
def terms_cms(request):
    Token_header = request.headers['Token']
    try:
        token = Token.objects.get(key = Token_header)
    except:
        token=''
        return Response({"Msg":"Pass the Token"})
    try:
        detail = Cms_StaticContent.objects.filter(name = 'Terms And Condition')
    except:
        detail = ''
        return Response({"Msg":"Data Not Found",'token':token.key})
    serializers=terms_cms_Serializers(detail,many=True)
    return Response({"Data":serializers.data,'token':token.key,'status':'true',"Msg":"Data Found"})


@api_view(['POST'])
def Privacy_cms(request):
    Token_header = request.headers['Token']
    try:
        token = Token.objects.get(key = Token_header)
    except:
        token=''
        return Response({"Msg":"Pass the Token"})
    try:
        detail = Cms_StaticContent.objects.filter(name = 'Privacy Policy')
    except:
        detail = ''
        return Response({"Msg":"Data Not Found",'token':token.key})
    serializers=terms_cms_Serializers(detail,many=True)
    return Response({"Data":serializers.data,'token':token.key,'status':'true',"Msg":"Data Found"})


@api_view(['POST'])
def FAQ_cms(request):
    Token_header = request.headers['Token']
    try:
        token = Token.objects.get(key = Token_header)
    except:
        token=''
        return Response({"Msg":"Pass the Token"})
    try:
        detail = Faq.objects.all()
    except:
        detail = ''
        return Response({"Msg":"Data Not Found",'token':token.key})
    serializers=Faq_Serializers(detail,many=True)
    return Response({"Data":serializers.data,'token':token.key,'status':'true',"Msg":"Data Found"})


@api_view(['POST'])
def change_pin(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    pin = Pin.objects.get(user_id = user_details.id)
    serializer = Change_Pin_Serializer(data = request.data)
    old_pin = int(request.data['old_pin'])
    new_pin = int(request.data['new_pin'])
    confirm_pin = int(request.data['confirm_pin'])
    if old_pin == pin.pin:
        if new_pin == old_pin:
            user_data={"Msg":"You Cannot set Old pin as new pin",'status':'false','token':token.key}
            return Response(user_data)
        else:
            if new_pin == confirm_pin:
                pin.pin = new_pin
                pin.save()
                user_data={"Msg":"Pin Updated",'status':'true','token':token.key}
                return Response(user_data)
            else:
                user_data={"Msg":"Password Mismatch",'status':'false','token':token.key}
                return Response(user_data)
    else:
       user_data={"Msg":"Old Pin Invalid",'status':'false','token':token.key}
       return Response(user_data) 

@api_view(['POST'])
def Verify_pin(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    try:
        companyqs = Company.objects.get(id=1)
        companyname= companyqs.name
    except:
        companyqs = ''
        companyname = ''
    try:
        device_unique_id = request.data['device_unique_id']
    except KeyError:
        device_unique_id=""
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    # Date1="2023-10-01"
    # Date2="2023-10-02"
    # Date3="2023-10-03"
    # Date4="2023-10-04"
    # count="4000"
    # missing_reward_update_two_api(request,Date1,count,Token_header)
    # missing_reward_update_two_api(request,Date2,count,Token_header)
    # missing_reward_update_two_api(request,Date3,count,Token_header)
    # missing_reward_update_two_api(request,Date4,count,Token_header)
    chk_data_login = LoginHistory.objects.filter(user = user_details).count()
    login_date_chk=""
    if int(chk_data_login) != 0:
        t_day = date.today()
        try:
            chk_data = LoginHistory.objects.filter(user = user_details).exclude(created_on__date__gte = t_day).last()
            login_date_chk=str(chk_data.created_on.date())
        except:
            login_date_chk=""
    if user_details.device_unique_id is None or user_details.device_unique_id == "":
        user_details.device_unique_id=device_unique_id
        user_details.save()
    user_session_out=int(companyqs.session_timeout)
    # if user_details.device_unique_id == device_unique_id:
    if(user_details.status == 0):
        pin = Pin.objects.get(user_id = user_details.id)
        serializer = Verify_Pin_Serializer(data = request.data)
        pinn = int(request.data['pin'])
        if pin.pin == pinn:
            login_user_create_api(request,Token_header)
            user_data={"Msg":"Correct Pin",'status':'true','token':token.key,"user_session_out":user_session_out,'Activatestatus':user_details.Activate_Status,'setType':user_details.User_Verification_Status,'login_date':login_date_chk}
            return Response(user_data)
        else:
            user_data={"Msg":"InCorrect Pin",'status':'false',"user_session_out":user_session_out,'token':token.key}
            return Response(user_data)
    else:
        user_data={"Msg":"Invalid User",'status':'false','token':token.key}
        return Response(user_data)
    # else:
    #     user_data={"Msg":"unusual activity",'status':'false','token':token.key}
    #     return Response(user_data)

def user_list_reward_update(request,id):
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

    if Decimal(wallet.balanceone) >= 0:
        wallet.balanceone = round(total_reward,7)
        wallet.save()

    if rewards_history :
        if Decimal(wallet.referalincome) >= 0:
            wallet.referalincome = round(total_ref_reward,7)
            wallet.save()
  except:
    pass
  return True


@api_view(['POST'])
def earning_summary(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    if user_details.plan == 0:
        date_date = user_details.created_on
    if user_details.plan != 0:
        date_date = user_details.plan_start_date
    Step_his = Reward_History.objects.filter(user = user_details.id,created_on__date = (date.today()-timedelta(days = 1)),reward_status = "step_reward").count()
    if Step_his > 1:
        his_id = Reward_History.objects.filter(user = user_details.id,created_on__date =(date.today()-timedelta(days = 1)),reward_status = "step_reward").last()
        user_reward = Reward_History.objects.filter(user = user_details.id,created_on__date =(date.today()-timedelta(days = 1)),reward_status = "step_reward").exclude(id = his_id.id)
        user_reward.delete()
        user_list_reward_update(request,user_details.id)
    detail = Reward_History.objects.raw('SELECT id,steps,Reward,reward_status,modified_on, CASE WHEN DATE_FORMAT(created_on,"%%Y-%%m-%%d %%H:%%i:%%s") = "2022-12-23 00:00:45" THEN created_on WHEN DATE_FORMAT(created_on,"%%Y-%%m-%%d %%H:%%i:%%s") <= "2022-12-23 23:59:00" THEN (created_on - interval 1 day)  ELSE created_on END AS created_on FROM HIsREwQpnlShyh WHERE user_id = %s AND DATE_FORMAT(modified_on,"%%Y-%%m-%%d") > %s ORDER BY created_on DESC', [user_details.id,date_date.date()])
    serializer = Reward_History_Serializers(detail,many=True)
    return Response({"Data":serializer.data,'token':token.key,'status':'true',"Msg":"Data Found"})

@api_view(['POST'])
def transaction_history(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    detail = Withdraw.objects.filter(userid_id = user_details.id).order_by('-id')
    serializer = Withdraw_history_Serializers(detail,many=True)
    return Response({"Data":serializer.data,'token':token.key,'status':'true',"Msg":"Data Found"})

@api_view(['POST'])
def Referral_history(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    if user_details.plan == 0:
        date = user_details.created_on
    if user_details.plan != 0:
        date = user_details.plan_start_date
    # user_details = User_Management.objects.get(user_name = token.user)   
    detail = Referral_reward_History.objects.raw('SELECT id,user_id,referral_id,reward,created_on,modified_on, CASE WHEN DATE_FORMAT(created_on,"%%Y-%%m-%%d %%H:%%i:%%s") = "2022-12-23 00:00:45" THEN created_on WHEN DATE_FORMAT(created_on,"%%Y-%%m-%%d %%H:%%i:%%s") <= "2022-12-23 23:59:00" THEN (created_on - interval 1 day)  ELSE created_on END AS created_on FROM HIDReFREWU0eY9SY WHERE user_id = %s AND DATE_FORMAT(modified_on,"%%Y-%%m-%%d %%H:%%i:%%s") >= %s ORDER BY created_on DESC', [user_details.id,date])
    # detail = Referral_reward_History.objects.filter(user_id = user_details.id)
    serializer = Referral_History_Serializers(detail,many = True)
    return Response({"Data":serializer.data,'token':token.key,'status':'true',"Msg":"Data Found"})

@api_view(['POST'])
def Stake_Credit(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    detail = Stake_Credit_History.objects.filter(user_id=token.user_id).order_by('-id')
    serializer = Stake_credit_Serializers(detail,many=True)
    return Response({"Data":serializer.data,'token':token.key,'status':'true',"Msg":"Data Found"})

@api_view(['POST'])
def resend_otp(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['Token']
    try:
        token = Token.objects.get(key = Token_header)
        user_details = User_Management.objects.get(user_name = token.user)
        email = user_details.Email
        if email:
            try:
                companyqs = Company.objects.get(id=1)
                companyname= companyqs.name
            except:
                companyqs = ''
                companyname = ''
            get_user = Registration_otp.objects.get(user=user_details.id)
            otp = generateOTP()
            if get_user:
                get_user.email_otp = otp
                get_user.save()           
                emailtemplate = get_email_template(request,3) 
                to_email = email
                data= {
                    'user':user_details.id,
                    'username':user_details.Name,
                    'email':email,
                    'domain':settings.DOMAIN_URL,
                    'uid':urlsafe_b64encode(force_bytes(user_details.id)),
                    'token':account_activation_token.make_token(user_details),
                    'company_logo':'comp_company_logo',
                    'company_name':companyname,
                    'otp':otp,
                    }
                htmly = get_template('emailtemplate/registration_email.html')
                html_content = htmly.render(data)
                requests.post(
                        "https://api.mailgun.net/v3/jasanwellness.fit/messages",
                        auth=("api",  decrypt_with_common_cipher(settings.MAIL_API)),
                        data={"from": "WEB3 WELLNESS <noreply@jasanwellness.fit>",
                        "to": [to_email],
                        "subject": emailtemplate.Subject,
                        "text": "Testing some Mailgun awesomness!",
                        "html": html_content})
                user_data={"Msg":"OTP Sent to Registered Email ID",'status':'true','token':token.key}
                return Response(user_data)
    except Exception as e:
        user_data={"Msg":e,'status':'false','token':token.key}
        return Response(user_data)






@api_view(['POST'])
def delete_reason_list(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    detail = Delete_Account_Reason_Management.objects.all()
    serializer = Delete_Reason_Serializers(detail,many=True)
    user_data={"data":serializer.data,"Msg":"Records Found","status":"true"}
    return Response(user_data) 

@api_view(['POST'])
def delete_account_request(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    serializer = Delete_Serializers(data = request.data)
    delete = request.data['Delete_Account']
    reason = request.data['reason']
    table = Delete_Account_Management.objects.create(user = user_details,Delete_Account = delete,reason=reason,status = 0)
    user_data={"msg":"Request Submitted ,Your Account will be deleted Shortly","status":"true"}
    return Response(user_data)

@api_view(['POST'])
def delete_otp_verification(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    otp = request.data['otp']
    user_otp = Registration_otp.objects.get(user = user_details)
    if user_otp.email_otp == int(otp):
        table = Delete_Account_Management.objects.get(user = user_details.id)
        table.status = 0
        table.save()
        user_data={"msg":"OTP Verified"}
        return Response(user_data)
    else:
        user_data={"msg":"Invalid OTP"}
        return Response(user_data)

from datetime import date, datetime, timedelta
import requests
import json
serverToken = decrypt_with_common_cipher('mBjrCYhX+E2IkytZ4xUJwY3wBeQ0qrDv/1vVii321ClZPK+bBpslIxytVGvvRf+Qh/NGeMsXBK+VYfADBUUWeVwmkz1bIllvPZaQC4V0euEn7IffRUz2z1t4dS2+RhP6l4w3wBI5U31wWe1ivsog7ni3hUV04M557qmWPR4Mml3wgz5iWyI6N1dl6oW55wAoZLSXXOzaHPcJktsK0JQjcA==')
deviceToken = 'duFA0qQGSvu7MSf9tt_FzE:APA91bG0tdgSyrPjbNuBxMPUxNzZgvZe7SbdN2PY3QwwQGO2nmKKLcx3iYDicmizCmf9QOAfwKue-zeGchjiHIDUXYJuvuSRINh8mqTsfhKWTvf6nMPRs-8yO1ZWQ56LTFNr6vTXopaq'

def tick(text):
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=' + serverToken,
          }

    body = {
              'notification': {'title': 'WEB3 Wellness 2X Boost Steps',
                                'body': 'Tap To Collect 2X Boost Reward'
                                },
              'to':
                  text,
              'priority': 'high',
            
            }
    response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
    return HttpResponse("response")
    
@api_view(['POST'])
def time_calculation(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_details = User_Management.objects.get(user_name = token.user) 
    user_data={"Msg":"2X Boost Under Maintenance!!!","status":"false",'token':token.key}
    return Response(user_data)

@api_view(['POST'])
def referral_details(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    total = 0
    user_details = User_Management.objects.get(user_name = token.user)
    ref = Referral_reward_History.objects.filter(user_id = user_details.id)
    for i in ref:
        total = (Decimal(i.reward)) + Decimal(total)
    ref_code = Referral_code.objects.get(user_id = user_details.id)
    user_data={"total_reward":total,"referral_code":ref_code.referal_code,"status":"true",'token':token.key}
    return Response(user_data)

@api_view(['POST'])
def user_target_set(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    step = request.data['target_step']
    user_details.User_Target = step
    user_details.save()
    user_data={"Msg":"Target updated","status":"true",'token':token.key}
    return Response(user_data)

@api_view(['POST'])
def withdraw_fees(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    currency = TradeCurrency.objects.get(symbol = 'JW')
    user_data={"Msg":"Data Found","status":"true",'token':token.key,"Withdraw_fee":currency.withdraw_fees}
    return Response(user_data)

@api_view(['GET'])
def front_screen_content(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    pdf="https://jasanwellness.fit/static/front_design/assets/doc/Disclaimer.pdf"
    try:
        detail = Cms_StaticContent.objects.values('name','title','content').get(name = 'Front Screen')
    except:
        detail = ''
        return Response({"Msg":"Data Not Found"})
    user_data={'Data':detail,"Msg":"Data Found","disclaimer_url":pdf,"status":"true"}
    return Response(user_data)

@api_view(['POST'])
def home_page_content(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    try:
        Token_header = request.headers['Token']
        token = Token.objects.get(key = Token_header)
        versioncode = request.data['versioncode']
        phone_type = request.data['phone_type']
        token = Token.objects.get(key = Token_header)
        device_unique_id = request.data['device_unique_id']
        user_details = User_Management.objects.get(user_name = token.user)
        if phone_type == "Android":
            build_type = request.data['build_type']
            user_details.build_type=build_type
            user_details.save()
        if(user_details.status == 0):
            user_details.user_profile_pic = phone_type
            user_details.phone_number = versioncode
            user_details.save()
            # user_details.status = 0
            if user_details.device_unique_id is None or user_details.device_unique_id == "":
                user_details.device_unique_id=device_unique_id
                user_details.save()
            USER_user = User_Management.objects.get(user_name = token.user)
            step = user_details.User_Target
            reward = Steps_Management.objects.get(id = 1)
            marketprice= market_price.objects.get(id =1)
            actualreward = reward.step_value/Decimal(marketprice.market_price)
            actual_reward = int(step)*(actualreward)
            detail = Cms_StaticContent.objects.get(name = '2X Content')
            serializers=terms_cms_Serializers(detail,many=False)
            notification_obj = admin_notification_message.objects.values('Notification_message','Notification_status').get(id = 1)
            notification_status = ""
            notification_msg = ""
            if int(user_details.plan) == 0:
                notification_status = "1"
                notification_msg = "You are in DEMO Account. Please subscribe premium plan to get benefits!!!"
            else:
                user_plan = plan_purchase_history.objects.filter(user_id = user_details.id).last()
                if int(user_plan.plan_id_id) != int(user_details.plan):
                    user_details.plan = int(user_plan.plan_id_id)
                    user_details.save()
                notification_status = notification_obj['Notification_status']
                notification_msg = notification_obj['Notification_message']
            login_user_create_api(request,Token_header)
            tnc_pdf="https://jasanwellness.fit/static/front_design/assets/doc/termsandconditions2.pdf"
            pp_pdf="https://jasanwellness.fit/static/front_design/assets/doc/privacypolicy.pdf"
            user_data={"Msg":"Data Found","status":"true",'Step':step,'reward':actual_reward,'content':serializers.data,"notification_status":notification_status,"privacy_policy":pp_pdf,"terms_and_condition":tnc_pdf,"notification_msg":notification_msg}
            return Response(user_data)
        
    except :
        user_data={"Msg":"Kindly Update Your APP. Available Version 3.2","status":"true","Step":"5000","reward":0,"content":{"title":"IMPORTANT !!!" , "content":'Kindly Update Your APP. Upcomming Version 3.2'}}
        return Response(user_data)


import requests
import json





@api_view(['POST'])
def device_id_update(request):
    Token_header = request.data['token']
    token = Token.objects.get(key = Token_header)
    id = request.data['User_Device_id']
    user_type = request.data['User_type']
    user_details = User_Management.objects.get(user_name = token.user)
    if id != user_details.User_Device_id and user_type == user_details.User_type:
        headers = {
                'Content-Type': 'application/json',
                'Authorization': 'key=' + serverToken,
            }

        body = {
                'notification': {'title': 'WEB 3 Wellness Login Alert',
                                    'body': 'You Have Logged In to New Device'
                                    },
                'to':
                    user_details.User_Device_id,
                'priority': 'high',
                
                }
        # response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
        user_details.User_Device_id = id
        user_details.save()
        user_data={"Msg":"Data Updated","status":"true",'token':token.key}
    else:        
        user_data={"Msg":"","status":"false",'token':token.key}
    return Response(user_data)



def provide_TFA(request):
    totp = pyotp.random_base32()
    enc = encrypt_with_common_cipher(totp)
    dec = decrypt_with_common_cipher(enc)
    user_data={'Secret Key':totp,'Encrypted Format':enc}
    return JsonResponse(user_data)

def encrypt(request,input):
    enc = encrypt_with_common_cipher(input)
    user_data={'Encrypted Format':enc}
    return JsonResponse(user_data)

def decrypt(request,input):
    enc = decrypt_with_common_cipher("Gv0aw7HGP4vorJ5zrdgDpgccMO3mRMapjumd/tfvw6fRrmZW7HantwKng3fqJMou+yyIbldMg+u9Ucw3wVkwwQ==")
    user_data={'Encrypted Format':enc}
    return JsonResponse(user_data)

from django.db.models import Sum

def landing_page(request):
    context={}
    auction_count = 0
    front_management = front_page_management.objects.get(id = 1)
    if front_management.status == 1:
        auction_count=User_Management.objects.all().count()
    else:
        count = User_Management.objects.all().count()
        auction_count = int(count)+int(front_management.Front_user_count)
    step_count=Steps_history.objects.all().aggregate(Sum('steps'))
    version = Company.objects.get(id = 1)
    context['auction_count']=auction_count
    context['step_count']=step_count['steps__sum']
    context['comp__android_version']=version
    return render(request,'api/index.html',context)


def privacy_policy_page(request):
    return render(request,'api/privacy.html')


def terms_condition_page(request):
    return render(request,'api/terms.html')

def disclaimer_page(request):
    return render(request,'api/disclaimer.html')


@api_view(['POST'])
def market_place_status(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    status = Market_place.objects.get(id =1)
    market_status = status.Google_status
    user_data={"Msg":"Data Found","Data":status.Google_status,"status":"true",'token':token.key}
    return Response(user_data)



@api_view(['POST'])
def delete_account(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    user = User.objects.get(username = user_details.user_name)
    token.delete()
    user.delete()
    user_details.status = 2
    user_details.save()
    user_data={"Msg":"Data Found","status":"true",'token':token.key}
    return Response(user_data)

@api_view(['POST'])
def country_state(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    country = Country.objects.all()
    serializer = Country_Serializers(country,many=True)
    state = State.objects.all()
    serializers = State_Serializers(state,many=True)
    user_data={"Msg":"Data Found","status":"true",'token':token.key,'Country':serializer.data,'state':serializers.data}
    return Response(user_data)

@api_view(['POST'])
def add_address(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    user_detail = request.data['user']
    Address_line_1 = request.data['Address_line_1']
    Address_line_2 = request.data['Address_line_2']
    Country = request.data['Country']
    State = request.data['State']
    pincode = request.data['pincode']
    usermanagement = User_Management.objects.get(user_name = token.user)
    user = User_address.objects.create(user=usermanagement,name=user_detail,Address_line_1= Address_line_1,Address_line_2=Address_line_2,Country = Country,State = State,pincode = pincode)  
    user_data={"Msg":"Address Created","status":"true",'token':token.key}
    return Response(user_data)


@api_view(['POST'])
def view_address(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    address = User_address.objects.filter(user = User.id)
    serializer = user_address_Serializers(address,many = True)
    user_data={"Msg":"Data Found","Data":serializer.data,"status":"true",'token':token.key,'user_name':User.Name}
    return Response(user_data)


def verify_page(request):
    return render(request,'api/googlef979a417d7d954a7.html')


# @api_view(['GET'])
# def maintanance(request):
#     f = open ('maintanance_status.json', "r")
#     data = json.loads(f.read())
#     # data = Company_Settings.objects.values('site_maintenance_status','IOS_site_maintenance_status').get(id = 1)
#     user_data={"Msg":"Data Found","Data":[data],"status":"true"}
#     return Response(user_data)


@api_view(['GET'])
def maintanance(request):
    try:
        with open('maintanance_status.json', 'r') as f:
            data = json.load(f)
        user_data = {"Msg": "Data Found", "Data": [data], "status": "true"}
        return Response(user_data)
    except FileNotFoundError:
        return Response({"Msg": "File not found", "status": "false"}, status=404)
    except json.JSONDecodeError:
        return Response({"Msg": "Invalid JSON format", "status": "false"}, status=400)
    except Exception as e:
        return Response({"Msg": str(e), "status": "false"}, status=500)




@api_view(['POST'])
def select_address(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    id = int(request.data['ID'])
    User = User_Management.objects.get(user_name = token.user)
    address = User_address.objects.filter(user = User.id)
    for i in address:
        if i.id == id:
            i.status = 0
            i.save()
    for i in address:
        if i.id != id:
            i.status = 1
            i.save()
    user_data={"Msg":"Data Updated","status":"true",'token':token.key}
    return Response(user_data)


@api_view(['POST'])
def detail_address(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    id = int(request.data['ID'])
    address = User_address.objects.filter(id = id)
    serializer = user_address_Serializers(address,many = True)
    user_data={"Msg":"Data Found","Data":serializer.data,"status":"true",'token':token.key}
    return Response(user_data)


@api_view(['POST'])
def edit_address(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    id = int(request.data['ID'])
    address = User_address.objects.get(id = id)
    user_detail = request.data['user']
    Address_line_1 = request.data['Address_line_1']
    Address_line_2 = request.data['Address_line_2']
    Country = request.data['Country']
    State = request.data['State']
    pincode = request.data['pincode']
    address.name = user_detail
    address.Address_line_1 = Address_line_1
    address.Address_line_2 = Address_line_2
    address.Country = Country
    address.State = State
    address.pincode = pincode
    address.save()
    user_data={"Msg":"Data Updated","status":"true",'token':token.key}
    return Response(user_data)


@api_view(['POST'])
def delete_address(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    id = int(request.data['ID'])
    address = User_address.objects.get(id = id)
    address.delete()
    user_data={"Msg":"Data Deleted","status":"true",'token':token.key}
    return Response(user_data)



@api_view(['POST'])
def all_plan(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key=Token_header)
    user_id = token.user_id
    user = User.objects.get(id=user_id)
    user_join_date = user.date_joined

    validation = request.data['months']
    validation_days = 0
    k = 0
    details = None

    if validation == "Monthly":
        validation_days = 1
        k = 0
        if user_join_date <= datetime(2024, 1, 29):
            details = plan.objects.filter(status=0).filter(~Q(plan_purchase_amount_monthly=0)).filter(plan_type=1).exclude(plan_name="65 USDT(JW)")

    if validation == "Quarterly":
        validation_days = 3
        k = 1
        details = plan.objects.filter(status=0).filter(~Q(plan_purchase_amount_quarterly=0)).filter(plan_type=1)

    if validation == "Annual":
        validation_days = 12
        k = 2
        details = plan.objects.filter(status=0).filter(~Q(plan_purchase_amount_annual=0)).filter(plan_type=1)

    serializers = plan_Serializers(details, many=True)
    user_data = {"Msg": "Data Found", "data": serializers.data, "status": "true", 'token': token.key,
                 'validation_days': validation_days}
    return Response(user_data)

from datetime import datetime, time
@api_view(['POST'])
def buy_plan(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    try:
        companyqs = Company.objects.get(id=1)
        companyname= companyqs.name
    except:
        companyqs = ''
        companyname = ''
    id = int(request.data['ID'])
    Plan = plan.objects.get(id = id)
    plan_purchase=int(Plan.plan_purchase_type)
    stake_credit=Decimal(Plan.stake_wallet_monthly_percentage)
    wallet_type = request.data['wallet_type']
    Validation_days = int(request.data['validation_days'])
    selected_market_price = request.data['selected_market_price']
    days = 0
    hash_data = ""
    amunt=""
    try:
        hash_data = request.data['Hash_data']
    except:
        hash_data = ""
    if int(wallet_type) == 3:
        hash_his = plan_purchase_history.objects.filter(User_plan_validation = hash_data).count()
        if hash_his >= 1:
            user_data = {"Msg":"Hash data Already Exists!!!","status":"false",'token':token.key}
            return Response(user_data)
    # if int(wallet_type) == 2:
    #     user_data = {"Msg":"Try buying Plan With Health Wallet or Wallet Connect!!!","status":"false",'token':token.key}
    #     return Response(user_data)
    # if int(wallet_type) != 3:
    #     if User.plan != 0 : 
    #         if User.plan == id:
    #             user_data = {"Msg":"You Have already purchased this plan , Buy Higher Plans!!!","status":"false",'token':token.key}
    #             return Response(user_data)
    if Plan.status == 1:
        user_data = {"Msg":"Plan Does Not Exist","status":"false",'token':token.key}
        return Response(user_data)
    plan_validation = ""
    if Validation_days == 1:
        days = 30
        purchase_amount = Plan.plan_purchase_amount_monthly
        plan_validation = "Monthly"
    if Validation_days == 3: 
        days = 90
        purchase_amount = Plan.plan_purchase_amount_quarterly
        plan_validation = "Quarterly"
    if Validation_days == 12:
        days = 365
        purchase_amount = Plan.plan_purchase_amount_annual
        plan_validation = "Annual"
    if int(purchase_amount) == 0:
        user_data = {"Msg":"Purchase Amount Invalid","status":"false",'token':token.key}
        return Response(user_data)
    if int(wallet_type) == 1:
        if User.plan == 0:
            if str(User.created_on.date()) >= "2023-03-01":
                user_data = {"Msg":"Purchase premium plan with JW ","status":"false",'token':token.key}
                return Response(user_data)
        wallet = UserCashWallet.objects.get(userid = User.id)
        if Decimal(purchase_amount) > wallet.balanceone:
            user_data={"Msg":"Insufficient Balance","status":"false",'token':token.key}
            return Response(user_data)
        else:
            wallet_flush_history.objects.create(user = User,wallet_balanceone = wallet.balanceone,Wallet_referral_income = wallet.referalincome,User_before_plan = User.plan)
            wallet.balanceone = 0
            wallet.referalincome = 0
            wallet.save()
            if plan_purchase == 1: 
                try:
                    user_stake_obj = stake_wallet_management.objects.using('second_db').get(user = User.id)
                except:
                    user_stake_obj = 0
                if user_stake_obj != 0:
                    amunt=Plan.activate_plan
                    value=Decimal(purchase_amount) - Decimal(amunt)
                    user_stake_obj.stake_Wallet=Decimal(user_stake_obj.stake_Wallet)  + Decimal(value)
                    user_stake_obj.save(using='second_db')
                    stake_claim_reward_history.objects.using('second_db').create(user = User.id,email=User.Email,type='Plan Purchase',stake_Wallet_reward_amount = Decimal(value),original_amount=purchase_amount)
            else:
                pass
            User.plan = Plan.id
            User.plan_start_date = datetime.now()
            desired_time = datetime.strptime("23:55", "%H:%M").time()
            today = datetime.now()
            today_with_desired_time = datetime.combine(today.date(), desired_time)
            end_date = today_with_desired_time + timedelta(days)
            User.plan_end_date = end_date
            User.user_referral_eligible_level = Plan.referral_level_eligible
            User.plan_validation = plan_validation
            User.save()
            User.Health_Withdraw_max_value = Plan.health_withdraw_maximum_limit
            User.Health_Withdraw_min_value = Plan.health_withdraw_minimum_limit
            User.Referral_Withdraw_max_value = Plan.referral_withdraw_maximum_limit
            User.Referral_Withdraw_min_value = Plan.referral_withdraw_minimum_limit
            User.save()
            if plan_purchase == 1:
                Jw_plan_purchase_history.objects.create(user = User,activate_plan=Plan.activate_plan,plan_name = Plan.plan_name ,stake_credit=Plan.user_stake_credit,purchase_amount = amunt,user_wallet_type = "Step Reward Wallet", buy_type = "User Buyed")
                plan_purchase_history.objects.create(user = User,plan_id = Plan,purchase_amount = purchase_amount,user_wallet_type = "Step Reward Wallet",Plan_maximum_step = Plan.Max_step_count,Plan_minimum_step = Plan.Min_step_count,Plan_referral_status = Plan.referral_status,Plan_Two_X_Boost_status = Plan.two_X_Boost_status,Plan_Level = Plan.level,Plan_Withdraw_status = Plan.withdraw_status, Plan_maximum_reward = Plan.reward_amount,buy_type = "User Buyed",plan_reward_step_val = Plan.Reward_step_value,plan_per_reward_amount = Plan.plan_reward_amount,User_plan_validation = hash_data,stake_wallet_monthly_split_percentage=Plan.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=Plan.withdraw_wallet_monthly_percentage,support_status=Plan.support_status,monthly_support=Plan.monthly_support_status,quarterly_support=Plan.quarterly_support_status,annual_support=Plan.annual_support_status,plan_purchase_type=Plan.plan_purchase_type,halfyearly_support=Plan.halfyearly_support_status,monthly_support_amount=Plan.monthly_support_amount,quarterly_support_amount=Plan.quarterly_support_amount,halfyearly_support_amount=Plan.halfyearly_support_amount,annual_support_amount=Plan.annual_support_amount,current_api_price=selected_market_price)
            else:
                plan_purchase_history.objects.create(user = User,plan_id = Plan,purchase_amount = purchase_amount,user_wallet_type = "Step Reward Wallet",Plan_maximum_step = Plan.Max_step_count,Plan_minimum_step = Plan.Min_step_count,Plan_referral_status = Plan.referral_status,Plan_Two_X_Boost_status = Plan.two_X_Boost_status,Plan_Level = Plan.level,Plan_Withdraw_status = Plan.withdraw_status, Plan_maximum_reward = Plan.reward_amount,buy_type = "User Buyed",plan_reward_step_val = Plan.Reward_step_value,plan_per_reward_amount = Plan.plan_reward_amount,User_plan_validation = hash_data,stake_wallet_monthly_split_percentage=Plan.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=Plan.withdraw_wallet_monthly_percentage,support_status=Plan.support_status,monthly_support=Plan.monthly_support_status,quarterly_support=Plan.quarterly_support_status,annual_support=Plan.annual_support_status,plan_purchase_type=Plan.plan_purchase_type,halfyearly_support=Plan.halfyearly_support_status,monthly_support_amount=Plan.monthly_support_amount,quarterly_support_amount=Plan.quarterly_support_amount,halfyearly_support_amount=Plan.halfyearly_support_amount,annual_support_amount=Plan.annual_support_amount,current_api_price=selected_market_price)
            if Plan.referral_status == 0:
                User.referral_plan_status = 0
                User.save()
            else:
                User.referral_plan_status = 1
                User.save()
            if User.referal_code == "" or User.referal_code == None:
                if plan_purchase == 1:
                    adminprofit = Admin_Profit.objects.create(user = User,admin_profit = amunt,Profit_type = "Plan Purchase")
                else:
                    adminprofit = Admin_Profit.objects.create(user = User,admin_profit = purchase_amount,Profit_type = "Plan Purchase")    
                pass
            else:
                a=[]
                ref_code = User.referal_code
                reff_id = Referral_code.objects.get(referal_code=ref_code)
                referred_user = User_Management.objects.get(id = reff_id.user.id)
                uesr_level = User.Referral_Level
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
                obj_plan_hist = plan_purchase_history.objects.filter(user = User).count()
                if obj_plan_hist == 1:
                    for i in a:
                        user = User_Management.objects.get(id = i)
                        if user.plan == 0:
                            b = b+1 
                            pass
                        elif ((datetime.now())) >= user.plan_end_date:
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
                                elif user.user_referral_eligible_level >= plan_hist.Plan_Level and plan_hist.Plan_Level >= b:
                                    User_Referral_level = referral_level.objects.get(referral_level_id = b)
                                    obj_plan_hist = plan_purchase_history.objects.filter(user = User).count()
                                    Market_Price = market_price.objects.get(id = 1)
                                    if plan_purchase == 1:
                                        Purchase_Amount = Decimal(amunt)
                                    else:
                                        Purchase_Amount = Decimal(purchase_amount)
                                    percentage = (User_Referral_level.commission_amount * Purchase_Amount)/100
                                    actual_reward = Decimal(percentage)
                                    l=l+actual_reward
                                    userwallet = UserCashWallet.objects.get(userid = i)
                                    userwallet.referalincome = userwallet.referalincome + actual_reward
                                    userwallet.save()
                                    table = Referral_reward_History.objects.create(user = user,referral_id = (User.Name),reward = Decimal(actual_reward))
                                    b = b+1 
                                else:
                                    b = b +1
                                    pass
                            else:
                                b = b +1
                                pass
                sum = 0
                # for i in l:
                #     sum = sum + i
                if plan_purchase == 1:
                    admin_profit = Decimal(amunt) - l
                    adminprofit = Admin_Profit.objects.create(user = User,admin_profit = amunt,Profit_type = "Plan Purchase")
                else:
                    admin_profit = purchase_amount - l
                    adminprofit = Admin_Profit.objects.create(user = User,admin_profit = admin_profit,Profit_type = "Plan Purchase")                       
    if int(wallet_type) == 2:
        wallet = UserCashWallet.objects.get(userid = User.id)
        if User.plan == 0:
            if str(User.created_on.date()) >= "2023-03-01":
                user_data = {"Msg":"Purchase premium plan with JW ","status":"false",'token':token.key}
                return Response(user_data)
        if Decimal(purchase_amount) > wallet.referalincome:
            user_data={"Msg":"Insufficient Balance","status":"false",'token':token.key}
            return Response(user_data)
        else:
            wallet_flush_history.objects.create(user = User,wallet_balanceone = wallet.balanceone,Wallet_referral_income = wallet.referalincome,User_before_plan = User.plan)
            wallet.balanceone = 0
            wallet.referalincome = 0
            wallet.save()
            if plan_purchase == 1: 
                try:
                    user_stake_obj = stake_wallet_management.objects.using('second_db').get(user = User.id)
                except:
                    user_stake_obj = 0
                if user_stake_obj != 0:
                    amunt=Plan.activate_plan
                    value=Decimal(purchase_amount) - Decimal(amunt)
                    user_stake_obj.stake_Wallet=Decimal(user_stake_obj.stake_Wallet)  + Decimal(value)
                    user_stake_obj.save(using='second_db')
                    stake_claim_reward_history.objects.using('second_db').create(user = User.id,email=User.Email,type='Plan Purchase',stake_Wallet_reward_amount = Decimal(value),original_amount=purchase_amount)
            else:
                pass
            User.plan = Plan.id
            User.plan_start_date = datetime.now()
            desired_time = datetime.strptime("23:55", "%H:%M").time()
            today = datetime.now()
            today_with_desired_time = datetime.combine(today.date(), desired_time)
            end_date = today_with_desired_time + timedelta(days)
            User.plan_end_date = end_date
            User.user_referral_eligible_level = Plan.referral_level_eligible
            User.plan_validation = plan_validation
            User.save()
            User.Health_Withdraw_max_value = Plan.health_withdraw_maximum_limit
            User.Health_Withdraw_min_value = Plan.health_withdraw_minimum_limit
            User.Referral_Withdraw_max_value = Plan.referral_withdraw_maximum_limit
            User.Referral_Withdraw_min_value = Plan.referral_withdraw_minimum_limit
            User.save()
            if plan_purchase == 1:
                Jw_plan_purchase_history.objects.create(user = User,activate_plan=Plan.activate_plan ,plan_name = Plan.plan_name ,stake_credit=Plan.user_stake_credit,purchase_amount = amunt,user_wallet_type = "Referral Reward Wallet", buy_type = "User Buyed")
                plan_purchase_history.objects.create(user = User,plan_id = Plan,purchase_amount = purchase_amount,user_wallet_type = "Referral Reward Wallet",Plan_maximum_step = Plan.Max_step_count,Plan_minimum_step = Plan.Min_step_count,Plan_referral_status = Plan.referral_status,Plan_Two_X_Boost_status = Plan.two_X_Boost_status,Plan_Level = Plan.level,Plan_Withdraw_status = Plan.withdraw_status, Plan_maximum_reward = Plan.reward_amount,buy_type = "User Buyed",plan_reward_step_val = Plan.Reward_step_value,plan_per_reward_amount = Plan.plan_reward_amount,User_plan_validation = hash_data,stake_wallet_monthly_split_percentage=Plan.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=Plan.withdraw_wallet_monthly_percentage,support_status=Plan.support_status,monthly_support=Plan.monthly_support_status,quarterly_support=Plan.quarterly_support_status,annual_support=Plan.annual_support_status,plan_purchase_type=Plan.plan_purchase_type,halfyearly_support=Plan.halfyearly_support_status,monthly_support_amount=Plan.monthly_support_amount,quarterly_support_amount=Plan.quarterly_support_amount,halfyearly_support_amount=Plan.halfyearly_support_amount,annual_support_amount=Plan.annual_support_amount,current_api_price=selected_market_price)
            else:
                plan_purchase_history.objects.create(user = User,plan_id = Plan,purchase_amount = purchase_amount,user_wallet_type = "Referral Reward Wallet",Plan_maximum_step = Plan.Max_step_count,Plan_minimum_step = Plan.Min_step_count,Plan_referral_status = Plan.referral_status,Plan_Two_X_Boost_status = Plan.two_X_Boost_status,Plan_Level = Plan.level,Plan_Withdraw_status = Plan.withdraw_status, Plan_maximum_reward = Plan.reward_amount,buy_type = "User Buyed",plan_reward_step_val = Plan.Reward_step_value,plan_per_reward_amount = Plan.plan_reward_amount,User_plan_validation = hash_data,stake_wallet_monthly_split_percentage=Plan.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=Plan.withdraw_wallet_monthly_percentage,support_status=Plan.support_status,monthly_support=Plan.monthly_support_status,quarterly_support=Plan.quarterly_support_status,annual_support=Plan.annual_support_status,plan_purchase_type=Plan.plan_purchase_type,halfyearly_support=Plan.halfyearly_support_status,monthly_support_amount=Plan.monthly_support_amount,quarterly_support_amount=Plan.quarterly_support_amount,halfyearly_support_amount=Plan.halfyearly_support_amount,annual_support_amount=Plan.annual_support_amount,current_api_price=selected_market_price)
            if Plan.referral_status == 0:
                User.referral_plan_status = 0
                User.save()
            else:
                User.referral_plan_status = 1
                User.save()
            if User.referal_code == "" or User.referal_code == None:
                if plan_purchase == 1:
                    adminprofit = Admin_Profit.objects.create(user = User,admin_profit = amunt,Profit_type = "Plan Purchase")
                else:
                    adminprofit = Admin_Profit.objects.create(user = User,admin_profit = purchase_amount,Profit_type = "Plan Purchase")    
                pass
            else:
                a=[]
                ref_code = User.referal_code
                reff_id = Referral_code.objects.get(referal_code=ref_code)
                referred_user = User_Management.objects.get(id = reff_id.user.id)
                uesr_level = User.Referral_Level
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
                obj_plan_hist = plan_purchase_history.objects.filter(user = User).count()
                if obj_plan_hist == 1:
                    for i in a:
                        user = User_Management.objects.get(id = i)
                        if user.plan == 0:
                            b = b+1 
                            pass
                        elif ((datetime.now())) >= user.plan_end_date:
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
                                elif user.user_referral_eligible_level >= plan_hist.Plan_Level and plan_hist.Plan_Level >= b:
                                    User_Referral_level = referral_level.objects.get(referral_level_id = b)
                                    obj_plan_hist = plan_purchase_history.objects.filter(user = User).count()
                                    Market_Price = market_price.objects.get(id = 1)
                                    if plan_purchase == 1:
                                            Purchase_Amount = Decimal(amunt)
                                    else:
                                        Purchase_Amount = Decimal(purchase_amount)
                                    percentage = (User_Referral_level.commission_amount * Purchase_Amount)/100
                                    actual_reward = Decimal(percentage) 
                                    l=l+actual_reward
                                    userwallet = UserCashWallet.objects.get(userid = i)
                                    userwallet.referalincome = userwallet.referalincome + actual_reward
                                    userwallet.save()
                                    table = Referral_reward_History.objects.create(user = user,referral_id = (User.Name),reward = Decimal(actual_reward))
                                    b = b+1 
                                else:
                                    b = b +1
                                    pass
                            else:
                                b = b +1
                            pass
                sum = 0
                # for i in l:
                #     sum = sum + i
                if plan_purchase == 1:
                    admin_profit = Decimal(amunt) - l
                    adminprofit = Admin_Profit.objects.create(user = User,admin_profit = amunt,Profit_type = "Plan Purchase")
                else:
                    admin_profit = purchase_amount - l
                    adminprofit = Admin_Profit.objects.create(user = User,admin_profit = admin_profit,Profit_type = "Plan Purchase")
    if int(wallet_type) == 3:
        wallet = UserCashWallet.objects.get(userid = User.id)
        wallet_flush_history.objects.create(user = User,wallet_balanceone = wallet.balanceone,Wallet_referral_income = wallet.referalincome,User_before_plan = User.plan)
        wallet.balanceone = 0
        wallet.referalincome = 0
        wallet.save()
        if plan_purchase == 1: 
            try:
                user_stake_obj = stake_wallet_management.objects.using('second_db').get(user = User.id)
            except:
                user_stake_obj = 0
            if user_stake_obj != 0:
                amunt=Plan.activate_plan
                value=Decimal(purchase_amount) - Decimal(amunt)
                user_stake_obj.stake_Wallet=Decimal(user_stake_obj.stake_Wallet)  + Decimal(value)
                user_stake_obj.save(using='second_db')
                stake_claim_reward_history.objects.using('second_db').create(user = User.id,email=User.Email,type='Plan Purchase',stake_Wallet_reward_amount = Decimal(value),original_amount=purchase_amount)
        else:
            pass
        User.plan = Plan.id
        User.plan_start_date = datetime.now()
        desired_time = datetime.strptime("23:55", "%H:%M").time()
        today = datetime.now()
        today_with_desired_time = datetime.combine(today.date(), desired_time)
        end_date = today_with_desired_time + timedelta(days)
        User.plan_end_date = end_date
        User.user_referral_eligible_level = Plan.referral_level_eligible
        User.plan_validation = plan_validation
        User.save()
        User.Health_Withdraw_max_value = Plan.health_withdraw_maximum_limit
        User.Health_Withdraw_min_value = Plan.health_withdraw_minimum_limit
        User.Referral_Withdraw_max_value = Plan.referral_withdraw_maximum_limit
        User.Referral_Withdraw_min_value = Plan.referral_withdraw_minimum_limit
        User.save()
        if plan_purchase == 1:
            Jw_plan_purchase_history.objects.create(user = User,activate_plan=Plan.activate_plan ,plan_name = Plan.plan_name ,stake_credit=Plan.user_stake_credit,purchase_amount = amunt,user_wallet_type = "Trust Wallet", buy_type = "User Buyed")
            plan_purchase_history.objects.create(user = User,plan_id = Plan,purchase_amount = purchase_amount,user_wallet_type = "Trust Wallet",Plan_maximum_step = Plan.Max_step_count,Plan_minimum_step = Plan.Min_step_count,Plan_referral_status = Plan.referral_status,Plan_Two_X_Boost_status = Plan.two_X_Boost_status,Plan_Level = Plan.level,Plan_Withdraw_status = Plan.withdraw_status, Plan_maximum_reward = Plan.reward_amount,buy_type = "User Buyed",plan_reward_step_val = Plan.Reward_step_value,plan_per_reward_amount = Plan.plan_reward_amount,User_plan_validation = hash_data,stake_wallet_monthly_split_percentage=Plan.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=Plan.withdraw_wallet_monthly_percentage,support_status=Plan.support_status,monthly_support=Plan.monthly_support_status,quarterly_support=Plan.quarterly_support_status,annual_support=Plan.annual_support_status,plan_purchase_type=Plan.plan_purchase_type,halfyearly_support=Plan.halfyearly_support_status,monthly_support_amount=Plan.monthly_support_amount,quarterly_support_amount=Plan.quarterly_support_amount,halfyearly_support_amount=Plan.halfyearly_support_amount,annual_support_amount=Plan.annual_support_amount,current_api_price=selected_market_price)
        else:
            plan_purchase_history.objects.create(user = User,plan_id = Plan,purchase_amount = purchase_amount,user_wallet_type = "Trust Wallet",Plan_maximum_step = Plan.Max_step_count,Plan_minimum_step = Plan.Min_step_count,Plan_referral_status = Plan.referral_status,Plan_Two_X_Boost_status = Plan.two_X_Boost_status,Plan_Level = Plan.level,Plan_Withdraw_status = Plan.withdraw_status, Plan_maximum_reward = Plan.reward_amount,buy_type = "User Buyed",plan_reward_step_val = Plan.Reward_step_value,plan_per_reward_amount = Plan.plan_reward_amount,User_plan_validation = hash_data,stake_wallet_monthly_split_percentage=Plan.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=Plan.withdraw_wallet_monthly_percentage,support_status=Plan.support_status,monthly_support=Plan.monthly_support_status,quarterly_support=Plan.quarterly_support_status,annual_support=Plan.annual_support_status,plan_purchase_type=Plan.plan_purchase_type,halfyearly_support=Plan.halfyearly_support_status,monthly_support_amount=Plan.monthly_support_amount,quarterly_support_amount=Plan.quarterly_support_amount,halfyearly_support_amount=Plan.halfyearly_support_amount,annual_support_amount=Plan.annual_support_amount,current_api_price=selected_market_price)
        if Plan.referral_status == 0:
            User.referral_plan_status = 0
            User.save()
        else:
            User.referral_plan_status = 1
            User.save()
        if User.referal_code == "" or User.referal_code == None:
            if plan_purchase == 1:
                adminprofit = Admin_Profit.objects.create(user = User,admin_profit = amunt,Profit_type = "Plan Purchase")
            else:
                adminprofit = Admin_Profit.objects.create(user = User,admin_profit = purchase_amount,Profit_type = "Plan Purchase")    
            pass
        else:
            a=[]
            ref_code = User.referal_code
            reff_id = Referral_code.objects.get(referal_code=ref_code)
            referred_user = User_Management.objects.get(id = reff_id.user.id)
            uesr_level = User.Referral_Level
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
            obj_plan_hist = plan_purchase_history.objects.filter(user = User).count()
            if obj_plan_hist == 1:
                for i in a:
                    user = User_Management.objects.get(id = i)
                    if user.plan == 0:
                        b = b+1 
                        pass
                    elif ((datetime.now())) >= user.plan_end_date:
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
                            elif user.user_referral_eligible_level >= plan_hist.Plan_Level and plan_hist.Plan_Level >= b:
                                User_Referral_level = referral_level.objects.get(referral_level_id = b)
                                obj_plan_hist = plan_purchase_history.objects.filter(user = User).count()
                                Market_Price = market_price.objects.get(id = 1)
                                if plan_purchase == 1:
                                    Purchase_Amount = Decimal(amunt)
                                else:
                                    Purchase_Amount = Decimal(purchase_amount)
                                percentage = (User_Referral_level.commission_amount * Purchase_Amount)/100
                                actual_reward = Decimal(percentage)
                                l=l+actual_reward
                                userwallet = UserCashWallet.objects.get(userid = i)
                                userwallet.referalincome = userwallet.referalincome + actual_reward
                                userwallet.save()
                                table = Referral_reward_History.objects.create(user = user,referral_id = (User.Name),reward = Decimal(actual_reward))
                                b = b+1 
                            else:
                                b = b +1
                                pass
                        else:
                            b = b +1
                            pass
            
            sum = 0
            # for i in l:
            #     sum = sum + i
            if plan_purchase == 1:
                admin_profit = Decimal(amunt) - l
                adminprofit = Admin_Profit.objects.create(user = User,admin_profit = amunt,Profit_type = "Plan Purchase")
            else:
                admin_profit = purchase_amount - l
                adminprofit = Admin_Profit.objects.create(user = User,admin_profit = admin_profit,Profit_type = "Plan Purchase")     
    if int(wallet_type) == 4:
        wallet = UserCashWallet.objects.get(userid = User.id)
        # if User.plan == 0:
        #     if str(User.created_on.date()) >= "2023-03-01":
        #         user_data = {"Msg":"Purchase premium plan with JW ","status":"false",'token':token.key}
        #         return Response(user_data)
        if Decimal(purchase_amount) > wallet.Premiumwallet:
            user_data={"Msg":"Insufficient Balance","status":"false",'token':token.key}
            return Response(user_data)
        else:
            wallet_flush_history.objects.create(user = User,wallet_balanceone = wallet.balanceone,Wallet_referral_income = wallet.referalincome,User_before_plan = User.plan)
            wallet.balanceone = 0
            wallet.referalincome = 0
            wallet.save()
            if plan_purchase == 1:
                try:
                    user_stake_obj = stake_wallet_management.objects.using('second_db').get(user = User.id)
                except:
                    user_stake_obj = 0
                if user_stake_obj != 0:
                    amunt=Plan.activate_plan
                    value=Decimal(purchase_amount) - Decimal(amunt)
                    user_stake_obj.stake_Wallet=Decimal(user_stake_obj.stake_Wallet)  + Decimal(value)
                    user_stake_obj.save(using='second_db')
                    stake_claim_reward_history.objects.using('second_db').create(user = User.id,email=User.Email,type='Plan Purchase',stake_Wallet_reward_amount = Decimal(value),original_amount=purchase_amount,buy_type="User Create")
            else:
                pass
            User.plan = Plan.id
            User.plan_start_date = datetime.now()
            desired_time = datetime.strptime("23:55", "%H:%M").time()
            today = datetime.now()
            today_with_desired_time = datetime.combine(today.date(), desired_time)
            end_date = today_with_desired_time + timedelta(days)
            User.plan_end_date = end_date
            User.user_referral_eligible_level = Plan.referral_level_eligible
            User.plan_validation = plan_validation
            User.save()
            User.Health_Withdraw_max_value = Plan.health_withdraw_maximum_limit
            User.Health_Withdraw_min_value = Plan.health_withdraw_minimum_limit
            User.Referral_Withdraw_max_value = Plan.referral_withdraw_maximum_limit
            User.Referral_Withdraw_min_value = Plan.referral_withdraw_minimum_limit
            User.save()
            wallet.Premiumwallet =  wallet.Premiumwallet - Decimal(purchase_amount)
            wallet.save()
            if plan_purchase == 1:
                Jw_plan_purchase_history.objects.create(user = User,activate_plan=Plan.activate_plan ,plan_name = Plan.plan_name ,stake_credit=Plan.user_stake_credit,purchase_amount = amunt,user_wallet_type = "Premium Reward Wallet", buy_type = "User Buyed")
                plan_purchase_history.objects.create(user = User,plan_id = Plan,purchase_amount = purchase_amount,user_wallet_type = "Premium Reward Wallet",Plan_maximum_step = Plan.Max_step_count,Plan_minimum_step = Plan.Min_step_count,Plan_referral_status = Plan.referral_status,Plan_Two_X_Boost_status = Plan.two_X_Boost_status,Plan_Level = Plan.level,Plan_Withdraw_status = Plan.withdraw_status, Plan_maximum_reward = Plan.reward_amount,buy_type = "User Buyed",plan_reward_step_val = Plan.Reward_step_value,plan_per_reward_amount = Plan.plan_reward_amount,User_plan_validation = hash_data,stake_wallet_monthly_split_percentage=Plan.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=Plan.withdraw_wallet_monthly_percentage,support_status=Plan.support_status,monthly_support=Plan.monthly_support_status,quarterly_support=Plan.quarterly_support_status,annual_support=Plan.annual_support_status,plan_purchase_type=Plan.plan_purchase_type,halfyearly_support=Plan.halfyearly_support_status,monthly_support_amount=Plan.monthly_support_amount,quarterly_support_amount=Plan.quarterly_support_amount,halfyearly_support_amount=Plan.halfyearly_support_amount,annual_support_amount=Plan.annual_support_amount,current_api_price=selected_market_price)
            else:
                plan_purchase_history.objects.create(user = User,plan_id = Plan,purchase_amount = purchase_amount,user_wallet_type = "Premium Reward Wallet",Plan_maximum_step = Plan.Max_step_count,Plan_minimum_step = Plan.Min_step_count,Plan_referral_status = Plan.referral_status,Plan_Two_X_Boost_status = Plan.two_X_Boost_status,Plan_Level = Plan.level,Plan_Withdraw_status = Plan.withdraw_status, Plan_maximum_reward = Plan.reward_amount,buy_type = "User Buyed",plan_reward_step_val = Plan.Reward_step_value,plan_per_reward_amount = Plan.plan_reward_amount,User_plan_validation = hash_data,stake_wallet_monthly_split_percentage=Plan.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=Plan.withdraw_wallet_monthly_percentage,support_status=Plan.support_status,monthly_support=Plan.monthly_support_status,quarterly_support=Plan.quarterly_support_status,annual_support=Plan.annual_support_status,plan_purchase_type=Plan.plan_purchase_type,halfyearly_support=Plan.halfyearly_support_status,monthly_support_amount=Plan.monthly_support_amount,quarterly_support_amount=Plan.quarterly_support_amount,halfyearly_support_amount=Plan.halfyearly_support_amount,annual_support_amount=Plan.annual_support_amount,current_api_price=selected_market_price)
            if Plan.referral_status == 0:
                User.referral_plan_status = 0
                User.save()
            else:
                User.referral_plan_status = 1
                User.save()
            if User.referal_code == "" or User.referal_code == None:
                if plan_purchase == 1:
                    adminprofit = Admin_Profit.objects.create(user = User,admin_profit = amunt,Profit_type = "Plan Purchase")
                else:
                    adminprofit = Admin_Profit.objects.create(user = User,admin_profit = purchase_amount,Profit_type = "Plan Purchase")    
                pass
            else:
                a=[]
                ref_code = User.referal_code
                reff_id = Referral_code.objects.get(referal_code=ref_code)
                referred_user = User_Management.objects.get(id = reff_id.user.id)
                uesr_level = User.Referral_Level
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
                for i in a:
                    user = User_Management.objects.get(id = i)
                    if user.plan == 0:
                        b = b+1 
                        pass
                    elif ((datetime.now())) >= user.plan_end_date:
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
                            elif user.user_referral_eligible_level >= plan_hist.Plan_Level and plan_hist.Plan_Level >= b:
                                User_Referral_level = referral_level.objects.get(referral_level_id = b)
                                obj_plan_hist = plan_purchase_history.objects.filter(user = User).count()
                                Market_Price = market_price.objects.get(id = 1)
                                reward_table=Referral_reward_History.objects.filter(user_id=user.id,referral_id = User.Name).count()
                                if reward_table == 0:
                                    if plan_purchase == 1:
                                        Purchase_Amount = Decimal(amunt)
                                    else:
                                        Purchase_Amount = Decimal(purchase_amount)
                                    percentage = (User_Referral_level.commission_amount * Purchase_Amount)/100
                                    actual_reward = Decimal(percentage) 
                                    l=l+actual_reward
                                    userwallet = UserCashWallet.objects.get(userid = i)
                                    userwallet.referalincome = userwallet.referalincome + actual_reward
                                    userwallet.save()
                                    table = Referral_reward_History.objects.create(user = user,referral_id = (User.Name),reward = Decimal(actual_reward))
                                b = b+1 
                            else:
                                b = b +1
                                pass
                        else:
                            b = b +1
                            pass
                sum = 0
                # for i in l:
                #     sum = sum + i
                if plan_purchase == 1:
                    admin_profit = Decimal(amunt) - l
                    adminprofit = Admin_Profit.objects.create(user = User,admin_profit = amunt,Profit_type = "Plan Purchase")
                else:
                    admin_profit = purchase_amount - l
                    adminprofit = Admin_Profit.objects.create(user = User,admin_profit = admin_profit,Profit_type = "Plan Purchase")   
    user_data={"Msg":"Plan Purchased","status":"true",'token':token.key}
    return Response(user_data)


@api_view(['POST'])
def referral_system(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    detail = referral_level.objects.all()
    a = []
    co="name"
    co1 = "commission_amount"
    co3 = "plan"
    co4 = "second_commission_amount"
    for i in detail:
        emp_dict={}
        try:
            plan_plan = plan.objects.get(referral_level_eligible = i.referral_level_id)
            emp_dict[co3]=plan_plan.plan_name
        except:
            emp_dict[co3]=""
        emp_dict[co]="Level " + str(i.referral_level_id)
        emp_dict[co1]=i.commission_amount
        emp_dict[co4]=i.second_level_commission_amount
        a.append(emp_dict)
    user_data={"Msg":"Data Found","status":"true","data":a,'token':token.key}
    return Response(user_data)

# @api_view(['POST'])


def faq_page(request):
    context={}
    faq = Faq.objects.all()
    context['Faq']=faq
    return render(request,'api/faq.html',context)


def referral__table(request,token,code):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = token
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    referral_id=""
    referral_id = code
    if code == "":
        referral = referral_table.objects.create(user_id = User,Referral_id = "",Referral_Level=0,Direct_referral_id = 0,Direct_referral_user_level=0)
        return True
    reff_id = Referral_code.objects.get(referal_code=referral_id)
    user_level = 1
    ref_user = User_Management.objects.get(id = reff_id.user.id)
    referred_user = User_Management.objects.get(id = reff_id.user.id)
    red_user = ""
    if referred_user.referal_code == None or referred_user.referal_code == "" :
        user_level = 1
        red_user = reff_id.user.Name
    while referred_user.referal_code != None and referred_user.referal_code != "" :
        user_level = user_level + 1
        reff_id = Referral_code.objects.get(referal_code=referred_user.referal_code)
        referred_user = User_Management.objects.get(id = reff_id.user.id)
        if referred_user.referal_code == None or referred_user.referal_code == "":
            red_user = reff_id.user.Name
            break 
    referral = referral_table.objects.create(user_id = User,Referral_id = ref_user.Name,Referral_Level=user_level,Direct_referral_id = red_user,Direct_referral_user_level=user_level)
    User.Referral_id = ref_user.Name
    User.Referral_Level = user_level
    User.Direct_referral_id = ref_user.Name
    User.Direct_referral_user_level = user_level
    User.save()
    return True


@api_view(['POST'])
def User_plan_details(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    plan_status = ""
    Validation_days = 0
    plan_name = ""
    plan_type = ""
    Shift_plan_status = 0
    plan_id = 0
    today = datetime.now()
    if User.plan != 0 and User.plan_end_date > today:
        plan_status = "Active"
        Validation_days = User.plan_end_date - User.plan_start_date 
        Plan = User.plan
        plan_plan = plan_purchase_history.objects.filter(user_id = User.id).last()
        plan_name = (plan_plan.plan_id.plan_name)
        Validation_days = (Validation_days).days
        user_plan_plan = plan.objects.get(id = int(plan_plan.plan_id_id))
        plan_id = user_plan_plan.id
        if int(plan_plan.Plan_Two_X_Boost_status) == int(user_plan_plan.two_X_Boost_status):
            Shift_plan_status = 1
        else:
            Shift_plan_status = 0    
    if User.plan == 0:
        plan_type = "Free"
        Plan = plan.objects.get(plan_type = 0)
        Shift_plan_status = User.Two_X_Boost_status
        plan_id = Plan.id
    if User.plan != 0 and User.plan_end_date < today:
        plan_type = "Expired"
        plan_status = "InActive"
        
    user_data={"Msg":"Data Found","status":"true",'token':token.key,'Plan_Status':plan_status,'validation_days':Validation_days,'plan_name':plan_name,'plan_type':plan_type,'plan_start_date':User.plan_start_date,'plan_end_date':User.plan_end_date,'Shift_plan_status':Shift_plan_status,"user_plan_id":User.plan,'plan_id':plan_id}
    return Response(user_data)

@api_view(['POST'])
def referal_reward(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    user_data={"Msg":"Data Found","status":"true",'token':token.key}
    return Response(user_data)

def referral_nav(request,id):
    return HttpResponseRedirect('https://play.google.com/store/apps/details?id=com.application.jasanwellness&referrer=utm_source%3D'+id)



@api_view(['POST'])
def plan_static_content(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    try:
        detail = Cms_StaticContent.objects.filter(name = 'Plan Static Content')
    except:
        detail = ''
        return Response({"Msg":"Data Not Found",'token':token.key})
    serializers=terms_cms_Serializers(detail,many=True)
    return Response({"Data":serializers.data,'token':token.key,'status':'true',"Msg":"Data Found"})

@api_view(['GET'])
def contract(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    details = Contract_address.objects.values('token_contract_address','Main_contract_address','Stake_contract_Address','usdt_contract_address')
    user_data={"Msg":"Data Found","Data":details,"status":"true"}
    return Response(user_data)


@api_view(['POST'])
def Direct_referral_list(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    code = Referral_code.objects.get(user = User.id)
    detail = User_Management.objects.filter(Q(referal_code = code.referal_code)).order_by("-created_on")
    serializer = User_Referral_Serializers(detail,many = True)
    a = []
    co="user_name"
    co1 = "Email"
    co2 = "Date"
    co3 = "Plan"
    co4 = "Plan_amount"
    co5 = "Plan_Validation"
    co6 = "Plan_end_date"
    co7 = "user_phone_number"
    for i in detail:
        emp_dict={}
        if i.plan != 0:
            try:
                plan_plan = plan.objects.get(id = i.plan)
                emp_dict[co3]=plan_plan.plan_name
            except:
                emp_dict[co3]=""
            try:
                plan_amount = plan_purchase_history.objects.filter(user = i.id).last()
                emp_dict[co4]=plan_amount.purchase_amount
            except:
                emp_dict[co4]=""
            try:
                plan_val = User_Management.objects.get(id = i.id)
                emp_dict[co5] = plan_val.plan_validation
            except:
                emp_dict[co5]=""
        else:
            emp_dict[co3]=""
            emp_dict[co4]=""
            emp_dict[co5]=""
        emp_dict[co]=i.Name
        emp_dict[co1]=i.Email
        emp_dict[co2]=i.plan_start_date
        emp_dict[co6]=i.plan_end_date
        emp_dict[co7]=i.user_phone_number
        a.append(emp_dict)
    user_data={"Msg":"Data Found","status":"true","data":a,'token':token.key}
    return Response(user_data)


@api_view(['POST'])
def current_time(request):
    data = datetime.now()
    user_data={"Msg":"TIME","Data":data}
    return Response(user_data)


@api_view(['POST'])
def Current_step_update(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Email = request.data['Email']
    Date = request.data['Date']
    Step_Count = request.data['Step_Count']
    Plan_Step = int(request.data['Plan_Step'])
    user_Detail=User_Management.objects.get(Email = Email)
    Detail = Steps_history.objects.raw()
    try:
        history_data = Steps_history.objects.get(created_on__date = Date,user_id = user_Detail.id)
        if history_data:
            history_data.steps = Step_Count
            history_data.save()
    except:
        Steps_history.objects.create(user = user_Detail,steps = Step_Count,created_on = Date+" 18:45:22.270177")
    try:
        Reward_update = Reward_History.objects.get(created_on__date = Date,user_id = user_Detail.id)
        Plan = user_Detail.plan
        user_wallet = UserCashWallet.objects.get(userid_id = user_Detail.id)
        step_count = Step_Count
        if Plan == 0:
            try:
                actual_plan = plan.objects.get(plan_type = 0)
                step_count = int(Step_Count)
                if step_count != 0 and step_count > 0:
                    if step_count < Plan_Step:
                        pass
                    if step_count > Plan_Step:
                        value = int(Plan_Step/1500)
                        reward = Decimal(value/10)                        
                        user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal(round(reward,2))
                        user_wallet.save()
                        Reward_update.Reward = Decimal(round(reward,2))
                        Reward_update.save()
                    if (step_count > Plan_Step) and (step_count < Plan_Step):
                        value = int(step_count/1500)
                        reward = Decimal(value/10)
                        user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal((round(reward,2)))
                        user_wallet.save()
                        Reward_update.Reward = reward
                        Reward_update.save()

                else:
                    pass
            except:
                pass
        else:
            actual_plan = plan.objects.get(id = Plan)
            step_count = int(Step_Count)
            if step_count != 0 and step_count > 0:
                if step_count < Plan_Step:
                    pass
                if step_count > Plan_Step:
                    value = int(Plan_Step/1500)
                    reward = Decimal(value/10)                    
                    user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal(round(reward,2))
                    user_wallet.save()
                    Reward_update.Reward = reward
                    Reward_update.save()

                if (step_count > Plan_Step) and (step_count < Plan_Step):
                    value = int(step_count/1500)
                    reward = Decimal(value/10)
                    user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal(round(reward,2))
                    user_wallet.save()
                    Reward_update.Reward = reward
                    Reward_update.save()

            else:
                pass
    except:
        Plan = user_Detail.plan
        user_wallet = UserCashWallet.objects.get(userid_id = user_Detail.id)
        step_count = Step_Count
        if Plan == 0:
            try:
                actual_plan = plan.objects.get(plan_type = 0)
                step_count = int(Step_Count)
                if step_count != 0 and step_count > 0:
                    if step_count < Plan_Step:
                        pass
                    if step_count > Plan_Step:
                        value = int(Plan_Step/1500)
                        reward = Decimal(value/10)
                        user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal(round(reward,2))
                        user_wallet.save()
                        table = Reward_History.objects.create(user = user_Detail,steps = (step_count),Reward = reward,created_on = Date+" 18:45:22.270177")
                    if (step_count > Plan_Step) and (step_count < Plan_Step):
                        value = int(step_count/1500)
                        reward = Decimal(value/10)
                        user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal((round(reward,2)))
                        user_wallet.save()
                        table = Reward_History.objects.create(user = user_Detail,steps = (step_count),Reward = Decimal((round(reward,2))),created_on = Date+" 18:45:22.270177")
                else:
                    pass
            except:
                pass
        else:
            actual_plan = plan.objects.get(id = Plan)
            step_count = int(Step_Count)
            if step_count != 0 and step_count > 0:
                if step_count < Plan_Step:
                    pass
                if step_count > Plan_Step:
                    value = int(Plan_Step/1500)
                    reward = Decimal(value/10)
                    user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal(round(reward,2))
                    user_wallet.save()
                    table = Reward_History.objects.create(user = user_Detail,steps = (step_count),Reward = reward,created_on = Date+" 18:45:22.270177")

                if (step_count > Plan_Step) and (step_count < Plan_Step):
                    value = int(step_count/1500)
                    reward = Decimal(value/10)
                    user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal(round(reward,2))
                    user_wallet.save()
                    table = Reward_History.objects.create(user = user_Detail,steps = (step_count),Reward = Decimal((round(reward,2))),created_on = Date+" 18:45:22.270177")
            else:
                pass

    user_data={"Msg":"Data Updated","status":"true"}
    return Response(user_data)


serverToken = decrypt_with_common_cipher('mBjrCYhX+E2IkytZ4xUJwY3wBeQ0qrDv/1vVii321ClZPK+bBpslIxytVGvvRf+Qh/NGeMsXBK+VYfADBUUWeVwmkz1bIllvPZaQC4V0euEn7IffRUz2z1t4dS2+RhP6l4w3wBI5U31wWe1ivsog7ni3hUV04M557qmWPR4Mml3wgz5iWyI6N1dl6oW55wAoZLSXXOzaHPcJktsK0JQjcA==')
def request_notification(request,start_id,end_id):
    start_id = int(start_id)
    end_id = int(end_id)
    user = User_Management.objects.filter(id__range = [start_id,end_id])
    for i in user :
         device_id = i.User_Device_id
         headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=' + serverToken,
          }

         body = {
              'notification': {'title': 'ALERT !! Web3Wellness ,Update Your APP To Collect Reward',
                                'body': 'New Message'
                                },
              'to':
                  device_id,
              'priority': 'high',
            
            }
    response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
    return HttpResponse("Success")


def version_code_update(request,app_type,android_version):
    company = Company.objects.get(id= 1)
    if app_type == "Android":
        company.Android_version = android_version
        company.save()
    if app_type == "IOS":
        company.IOS_version = android_version
        company.save()
    return HttpResponse("Success")


@api_view(['POST'])
def wallet_flush(request):
    main = load_maintanance(request)
    if main  == True:
        user_data = {'Msg':'App Under Maintanance','status':'false'}
        return Response(user_data)
    Token_header = request.headers['Token']
    token = Token.objects.get(key= Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    DAta = UserCashWallet.objects.get(userid_id = user_details.id)
    wallet_flush_history.objects.create(user = user_details,wallet_balanceone = DAta.balanceone,Wallet_referral_income = DAta.referalincome,User_before_plan = user_details.plan)
    DAta.balanceone = 0
    DAta.balancetwo = 0
    DAta.referalincome = 0
    DAta.save()
    user_data={"Msg":"Wallet Flushed","status":"true","HealthWallet":DAta.balanceone,"ReferralWallet":DAta.referalincome}
    return Response(user_data)



@api_view(['POST'])
def Email_send(request):
    try:
        Token_header = request.headers['Token']
    except:
        user_data = {"Msg":"Token Needed","status":"false"}
        return Response(user_data)
    token = Token.objects.get(key= Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    user__name = user_details.Name
    try:
        Email = request.data['Email']
    except:
        user_data = {"Msg":"Email Input Needed","status":"false"}
        return Response(user_data)
    try:
        companyqs = Company.objects.get(id=1)
        companyname= companyqs.name
    except:
        companyqs = ''
        companyname = ''
    otp = generateOTP()
    emailtemplate = get_email_template(request,5)
    to_email = Email
    data= {
        'username':user__name,
        'email':Email,
        'domain':settings.DOMAIN_URL,
        'company_name':companyname,
        'otp':otp,
        }
    user_otp = Registration_otp.objects.filter(user = user_details.id).count()
    if user_otp == 1 :
        otp_update = Registration_otp.objects.get(user = user_details.id)
        otp_update.email_otp = int(otp)
        otp_update.save()
    elif user_otp > 1:
        user_otp_id = Registration_otp.objects.filter(user = user_details.id).last()
        otp_delete_obj = Registration_otp.objects.filter(user = user_details.id).exclude(id = user_otp_id.id)
        otp_delete_obj.delete()
        user_otp_id.email_otp = int(otp)
        user_otp_id.save()
    else: 
        user_otp = Registration_otp.objects.create(user = user_details)
        user_otp.email_otp = int(otp)
        user_otp.save()
    htmly = get_template('emailtemplate/withdrawapprovedtemplate.html')
    html_content = htmly.render(data)
    response = requests.post(
    "https://api.mailgun.net/v3/jasanwellness.fit/messages",
    auth=("api", decrypt_with_common_cipher(settings.MAIL_API)),
    data={"from": "WEB3 WELLNESS <noreply@jasanwellness.fit>",
    "to": [to_email],
    "subject": emailtemplate.Subject,
    "html": html_content})
    user_data = {"Msg":"Email Sent","status":"true"}
    return Response(user_data)

@api_view(['POST'])
def Pin_reset_Email(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key= Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    user__name = user_details.Name
    if user_details.Email == "":
        user_data = {"Msg":"Email Not Found","status":"false"}
        return Response(user_data)
    else:
        Email = user_details.Email
    user_data = {"Msg":"Email Sent","status":"true","Email":user_details.Email}
    return Response(user_data)



@api_view(['POST'])
def Pin_reset_Email_two(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key= Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    user__name = user_details.Name
    Email = request.data['Email']
    try:
        companyqs = Company.objects.get(id=1)
        companyname= companyqs.name
    except:
        companyqs = ''
        companyname = ''
    otp = generateOTP()
    emailtemplate = get_email_template(request,7)
    to_email = Email
    data= {
        'username':user__name,
        'email':Email,
        'domain':settings.DOMAIN_URL,
        'company_name':companyname,
        'otp':otp,
        }
    try:
        user_otp = Registration_otp.objects.get(user = user_details.id)
        user_otp.email_otp = int(otp)
        user_otp.save()
    except:
        user_otp = Registration_otp.objects.create(user = user_details)
        user_otp.email_otp = int(otp)
        user_otp.save()
    htmly = get_template('emailtemplate/pinreset.html')
    html_content = htmly.render(data)
    response = requests.post(
    "https://api.mailgun.net/v3/jasanwellness.fit/messages",
    auth=("api", decrypt_with_common_cipher(settings.MAIL_API)),
    data={"from": "WEB3 WELLNESS <noreply@jasanwellness.fit>",
    "to": [to_email],
    "subject": emailtemplate.Subject,
    "html": html_content})
    if response.status_code == 200 :
        user_data = {"Msg":"Email Sent","status":"true"}
        return Response(user_data)
    else:
        user_data={"Msg": "Mail Server Problem. Please try again after some times !!!",'status':'false'}
        return Response(user_data) 

@api_view(['POST'])
def pin_set_function_otp_verify(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_OTP = request.data['OTP']
    user_details = User_Management.objects.get(user_name = token.user)
    user_otp = Registration_otp.objects.get(user = user_details.id)
    if int(user_otp.email_otp) == int(user_OTP):
        user_data = {"Msg":"OTP Verified","status":"true"}
        return Response(user_data)
    else:
        user_data = {"Msg":"Invalid OTP","status":"false"}
        return Response(user_data)



@api_view(['POST'])
def buy_plan_two(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    id = int(request.data['ID'])
    Plan = plan.objects.get(id = id)
    wallet_type = request.data['wallet_type']
    Validation_days = int(request.data['validation_days'])
    days = 0
    if int(wallet_type) != 3:
        if User.plan != 0 : 
            if User.plan == id:
                user_data = {"Msg":"You Have already purchased this plan , Buy Higher Plans!!!","status":"false",'token':token.key}
                return Response(user_data)
    if Plan.status == 1:
        user_data = {"Msg":"Plan Does Not Exist","status":"false",'token':token.key}
        return Response(user_data)
    plan_validation = ""
    if Validation_days == 1:
        days = 30
        purchase_amount = Plan.plan_purchase_amount_monthly
        plan_validation = "Monthly"
    if Validation_days == 3: 
        days = 90
        purchase_amount = Plan.plan_purchase_amount_quarterly
        plan_validation = "Quarterly"
    if Validation_days == 12:
        days = 365
        purchase_amount = Plan.plan_purchase_amount_annual
        plan_validation = "Annual"
    if int(purchase_amount) == 0:
        user_data = {"Msg":"Purchase Amount Invalid","status":"false",'token':token.key}
        return Response(user_data)            
    if int(wallet_type) == 3:
        if Plan.referral_status == 0:
            User.referral_plan_status = 0
            User.save()
        else:
            User.referral_plan_status = 1
            User.save()
        if User.referal_code == "" or User.referal_code == None:
            adminprofit = Admin_Profit.objects.create(user = User,admin_profit = purchase_amount,Profit_type = "Plan Purchase")
            pass
        else:
            a=[]
            ref_code = User.referal_code
            reff_id = Referral_code.objects.get(referal_code=ref_code)
            referred_user = User_Management.objects.get(id = reff_id.user.id)
            uesr_level = User.Referral_Level
            Referral_level = referral_level.objects.all().count()
            for i in range(Referral_level):
                reff_id = Referral_code.objects.get(referal_code=ref_code)
                referred_user = User_Management.objects.get(id = reff_id.user.id)
                a.append(referred_user.id)
                ref_code = referred_user.referal_code
                if referred_user.referal_code == "" or referred_user.referal_code == None:
                    break
            b = 1
            l = []
            for i in a:
                user = User_Management.objects.get(id = i)
                if user.plan == 0:
                    b = b+1 
                    pass
                else:
                    PLan_plan = plan.objects.get(id = user.plan)
                    if PLan_plan.referral_status == 0:
                        b = b+1
                        pass
                    elif user.user_referral_eligible_level >= PLan_plan.referral_level_eligible and PLan_plan.referral_level_eligible >= b:
                                User_Referral_level = referral_level.objects.get(referral_level_id = b)
                                obj_plan_hist = plan_purchase_history.objects.filter(user = User).count()
                                Market_Price = market_price.objects.get(id = 1)
                                Purchase_Amount = purchase_amount
                                if int(obj_plan_hist) == 1:
                                    percentage = (User_Referral_level.commission_amount * Purchase_Amount)/100
                                else:
                                    percentage = (User_Referral_level.second_level_commission_amount * Purchase_Amount)/100
                                actual_reward = Decimal(percentage) 
                                userwallet = UserCashWallet.objects.get(userid = i)
                                userwallet.referalincome = userwallet.referalincome + actual_reward
                                userwallet.save()
                                table = Referral_reward_History.objects.create(user = user,referral_id = (User. Name),reward = Decimal(actual_reward))
                                b = b+1 
                    else:
                        b = b +1
                        pass
            sum = 0
            for i in l:
                sum = sum + i
            admin_profit = purchase_amount - sum
            adminprofit = Admin_Profit.objects.create(user = User,admin_profit = admin_profit,Profit_type = "Plan Purchase")        
    user_data={"Msg":"Plan Purchased","status":"true",'token':token.key}
    return Response(user_data)



@api_view(['POST'])
def direct_referral_tree(request):
    Email = request.data['Email']
    User = User_Management.objects.get(Email = Email)
    code = Referral_code.objects.get(user = User.id)
    detail = User_Management.objects.filter(Q(referal_code = code.referal_code)).order_by("-created_on")
    serializer = User_Referral_Serializers(detail,many = True)
    a = []
    co="user_name"
    co1 = "Email"
    co2 = "Date"
    co3 = "Plan"
    co4 = "Plan_amount"
    co5 = "Plan_Validation"
    co6 = "Plan_end_date"
    co7 = "user_phone_number"
    for i in detail:
        emp_dict={}
        if i.plan != 0:
            try:
                plan_plan = plan.objects.get(id = i.plan)
                emp_dict[co3]=plan_plan.plan_name
            except:
                emp_dict[co3]=""
            try:
                plan_amount = plan_purchase_history.objects.filter(user = i.id).last()
                emp_dict[co4]=plan_amount.purchase_amount
            except:
                emp_dict[co4]=""
            try:
                plan_val = User_Management.objects.get(id = i.id)
                emp_dict[co5] = plan_val.plan_validation
            except:
                emp_dict[co5]=""
        else:
            emp_dict[co3]=""
            emp_dict[co4]=""
            emp_dict[co5]=""
        emp_dict[co]=i.Name
        emp_dict[co1]=i.Email
        emp_dict[co2]=i.plan_start_date
        emp_dict[co6]=i.plan_end_date
        emp_dict[co7]=i.user_phone_number
        a.append(emp_dict)
    user_data={"Msg":"Data Found","status":"true","data":a,'Name':User.Name}
    return Response(user_data)


@api_view(['POST'])
def Direct_referral_list_two(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    code = Referral_code.objects.get(user = User.id)
    detail_count= User_Management.objects.filter(Q(referal_code = code.referal_code)).order_by("-created_on").count()  
    start_page = request.data['pageno']
    end_value = int(start_page) * 10
    start_value = int(end_value) - 10
    detail = User_Management.objects.values('referal_code','id','plan','Name','Email','plan_start_date','plan_end_date','user_phone_number').filter(Q(referal_code = code.referal_code)).order_by("-created_on")[start_value:end_value]
    a = [] 
    co="user_name"
    co1 = "Email"
    co2 = "Date"
    co3 = "Plan"
    co4 = "Plan_amount"
    co5 = "Plan_Validation"
    co6 = "Plan_end_date"
    co7 = "user_phone_number"
    usr = 0
    count = 0
    dict_step_users = {}
    for i in detail:
        usr = usr + 1
        emp_dict={}
        count = count + 1
        if i['plan'] != 0:
            try:
                plan_plan = plan.objects.get(id = i['plan'])
                emp_dict[co3]=plan_plan.plan_name
            except:
                emp_dict[co3]=""
            try:
                plan_amount = plan_purchase_history.objects.filter(user = i['id']).last()
                emp_dict[co4]=plan_amount.purchase_amount
            except:
                emp_dict[co4]=""
            try:
                plan_val = User_Management.objects.get(id = i['id'])
                emp_dict[co5] = plan_val.plan_validation
            except:
                emp_dict[co5]=""
        else:
            emp_dict[co3]=""
            emp_dict[co4]=""
            emp_dict[co5]=""
        emp_dict[co]=i['Name']
        emp_dict[co1]=i['Email']
        emp_dict[co2]=i['plan_start_date']
        emp_dict[co6]=i['plan_end_date']
        emp_dict[co7]=i['user_phone_number']
        a.append(emp_dict)
        dict_step_users[count] = emp_dict
    user_data={"Msg":"Data Found","status":"true","data":a,'token':token.key,'count':int(detail_count)+ 1}
    return Response(user_data)


@api_view(['POST'])
def shif_plan(request):
    Token_header = request.headers['token']
    Current_plan_id = request.data['Current_plan_id']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    if int(Current_plan_id) != 0:
        current_plan = plan.objects.get(id = int(Current_plan_id))
        user_current_plan_history = plan_purchase_history.objects.filter(user_id = User.id).last()
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
            user_current_plan_history.created_on = datetime.now()
            user_current_plan_history.save()
            user_data={"Msg":"Plan Shifted Successfully","status":"true",'token':token.key}
            return Response(user_data)
        else:
            user_data={"Msg":"Shift Plan Not Applicable","status":"false",'token':token.key}
            return Response(user_data)
    else:
        current_plan = plan.objects.get(plan_type = 0)
        User.reward_step_amount = current_plan.plan_reward_amount
        User.reward_steps = current_plan.Reward_step_value
        User.user = current_plan.Min_step_count
        User.over_all_stepcount = current_plan.Max_step_count
        User.Two_X_Boost_status = current_plan.two_X_Boost_status
        User.withdraw_status = current_plan.withdraw_status
        User.save()
        user_data={"Msg":"Plan Shifted Successfully","status":"true",'token':token.key}
        return Response(user_data)


@api_view(['POST'])
def shif_plan_details(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    if int(User.plan) != 0:
        current_plan = plan.objects.get(id = int(User.plan))
    else:
        current_plan = plan.objects.get(plan_type = 0)
    serializers = plan_Serializers(current_plan,many = False)
    user_data={"Msg":"Success","data":serializers.data,"status":"true",'token':token.key}
    return Response(user_data)


@api_view(['POST'])
def shift_all_plan(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    # detailssss = plan.objects.get(id = int(User.plan))
    withdraw_status = 0
    if int(User.plan) == 0:
        twoX_Boost_status = User.Two_X_Boost_status
        if int(twoX_Boost_status) == 0 :
            if str(User.created_on.date()) >= "2023-03-01":
                withdraw_status = 0
            else:
                withdraw_status = 1
            details = plan.objects.get(plan_type = 0)
            health_withdraw_maximum_limit = details.health_withdraw_maximum_limit
            health_withdraw_minimum_limit = details.health_withdraw_minimum_limit
            referral_withdraw_maximum_limit = details.referral_withdraw_maximum_limit
            referral_withdraw_minimum_limit = details.referral_withdraw_minimum_limit
        else:
            details = plan.objects.get(plan_type = 0)
            withdraw_status = details.withdraw_status
            health_withdraw_maximum_limit = details.health_withdraw_maximum_limit
            health_withdraw_minimum_limit = details.health_withdraw_minimum_limit
            referral_withdraw_maximum_limit = details.referral_withdraw_maximum_limit
            referral_withdraw_minimum_limit = details.referral_withdraw_minimum_limit
    else :
        details = plan.objects.get(id = int(User.plan))
        withdraw_status = details.withdraw_status
        health_withdraw_maximum_limit = User.Health_Withdraw_max_value
        health_withdraw_minimum_limit = User.Health_Withdraw_min_value
        referral_withdraw_maximum_limit = User.Referral_Withdraw_max_value
        referral_withdraw_minimum_limit = User.Referral_Withdraw_min_value
    minimum_BNB_Balance = withdraw_values.objects.get(id = 1)
    user_data={"Msg":"Data Found","withdraw_status":withdraw_status,"health_withdraw_maximum_limit":health_withdraw_maximum_limit,"health_withdraw_minimum_limit":health_withdraw_minimum_limit,"referral_withdraw_maximum_limit":referral_withdraw_maximum_limit,"referral_withdraw_minimum_limit":referral_withdraw_minimum_limit,"minimum_BNB_Balance":str(minimum_BNB_Balance.Minimum_BNB_Balance),"status":"true",'token':token.key}
    return Response(user_data)


# Login user history create

def login_user_create_api(request,Token_header):
    Token_header = Token_header
    token = Token.objects.get(key = Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    try:
        device_ip_address = request.data['device_ip_address']
    except KeyError:
        device_ip_address=""
    try:
        obj_log = LoginHistory.objects.get(user = user_details,created_on__date = date.today())
    except:
        obj_log = 0
    if obj_log != 0:
        LoginHistory.objects.filter(user = user_details).filter(created_on__date = date.today()).update(modified_on = datetime.now(),ip_address1=device_ip_address)
    else:
        LoginHistory.objects.create(user = user_details,created_on = datetime.now(),modified_on = datetime.now(),ip_address=device_ip_address,ip_address1=device_ip_address)
    user_data={"Msg":"Data Found","status":"true"}
    return Response(user_data)


    
# Login user history listing
@api_view(['POST'])
def login_history(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    usr = 0
    count = 0
    list_user = []
    start_page = request.data['pageno']
    end_value = int(start_page) * 10
    start_value = int(end_value) - 9
    try:
        obj_log = LoginHistory.objects.get(user = user_details,created_on__date = date.today())
    except:
        obj_log = 0
    if obj_log != 0:
        # LoginHistory.objects.filter(user = user_details).filter(created_on__date = date.today()).update(modified_on = datetime.now())
        detail = LoginHistory.objects.filter(user = user_details).order_by('-created_on')
        for i in detail:
            usr = usr + 1
            dict_usr = {}
            if start_value <= usr <= end_value:
                count = count + 1
                dict_usr['username'] = str(i.user.Name)
                dict_usr['created_on'] = str(i.created_on)
                dict_usr['modified_on'] = str(i.modified_on)
                if i.ip_address == "" or i.ip_address is None :
                    dict_usr['ip_address'] = ""
                else:
                    dict_usr['ip_address'] = str(i.ip_address)
                if i.ip_address1 == "" or i.ip_address1 is None :
                    dict_usr['ip_address1'] = ""
                else:
                    dict_usr['ip_address1'] = str(i.ip_address1)
                dict_usr['pageno'] = start_page
                dict_usr["sno"] = usr
                list_user.append(dict_usr)
    else:
        # LoginHistory.objects.create(user = user_details,created_on = datetime.now(),modified_on = datetime.now())
        detail = LoginHistory.objects.filter(user = user_details).order_by('-created_on')
        for i in detail:
            usr = usr + 1
            dict_usr = {}
            if start_value <= usr <= end_value:
                count = count + 1
                dict_usr['username'] = str(i.user.Name)
                dict_usr['created_on'] = str(i.created_on)
                dict_usr['modified_on'] = str(i.modified_on)
                if i.ip_address == "" or i.ip_address is None :
                    dict_usr['ip_address'] = ""
                else:
                    dict_usr['ip_address'] = str(i.ip_address)
                if i.ip_address1 == "" or i.ip_address1 is None :
                    dict_usr['ip_address1'] = ""
                else:
                    dict_usr['ip_address1'] = str(i.ip_address1)
                dict_usr['pageno'] = start_page
                dict_usr["sno"] = usr
                list_user.append(dict_usr)

    user_data={"Msg":"Data Found","status":"true","Data" : list_user,"count" : detail.count(),"Email":user_details.Email}
    return Response(user_data)


@api_view(['POST'])
def Wallet_details(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    Plan_wallet = Plan_purchase_wallet.objects.get(id = 1)
    serializer = Plan_purchase_wallet_Serializers(Plan_wallet,many=False)
    user_data={"Msg":"Data Found","data":serializer.data,"status":"true",'token':token.key}
    return Response(user_data)

@api_view(['POST'])
def missing_reward_update_two(request):
    Token_header = request.headers['Token'] 
    token = Token.objects.get(key= Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    Email = user_details.Email
    Date = request.data['Date']
    Step_Count = request.data['Step_Count']
    user_Detail=User_Management.objects.get(Email = Email) 
    chk_data = LoginHistory.objects.filter(user = user_details,created_on__date = Date).count()
    t_day = date.today()
    to_day = str(t_day.year)+'-'+str(t_day.month)+'-'+str(t_day.day)
    if str(Date) >= str(to_day):
        user_data={"Msg":"Can't claim reward.","status":"false"}
        return Response(user_data)
    if chk_data == 0 :
        user_data={"Msg":"Data not found check login history","status":"false"}
        return Response(user_data)
        # LoginHistory.objects.create(user = user_details,created_on = Date,modified_on = datetime.now())
    reward_chk_data = Reward_History.objects.filter(created_on__date = Date,user_id = user_Detail.id,reward_status = "step_reward").count()
    if reward_chk_data > 0:
        user_data={"Msg":"Reward Has Been Already Updated","status":"true","date":Date,"date_one":t_day}
        return Response(user_data)
    his_date = Steps_history.objects.filter(created_on__date = Date,user_id = user_Detail.id).count()
    if his_date > 1:
        his_date_count = Steps_history.objects.filter(created_on__date = Date,user_id = user_Detail.id).last()
        step_his_delete = Steps_history.objects.filter(created_on__date = Date,user_id = user_Detail.id).exclude(id = his_date_count.id)
        step_his_delete.delete()
    try:
        chk_data = Steps_history.objects.get(created_on__date = Date,user_id = user_Detail.id)
        if chk_data:
            Plan = user_Detail.plan
            user_wallet = UserCashWallet.objects.get(userid_id = user_Detail.id)
            step_count = int(Step_Count)
            chk_data.status = 1
            chk_data.modified_on = datetime.now()
            chk_data.steps = step_count
            chk_data.save()
            if Plan == 0:
                try:
                    actual_plan = plan.objects.get(plan_type = 0)
                    step_count = int(Step_Count)
                    value = Decimal(int(user_details.over_all_stepcount)/int(user_Detail.reward_steps))
                    reward = Decimal(value*user_Detail.reward_step_amount)
                    user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal(round(reward,2))
                    user_wallet.save()
                    chk_data.steps = int(user_details.over_all_stepcount)
                    chk_data.save()
                    if(str(Date) == "2022-12-23") :
                        table = Reward_History.objects.create(user = user_Detail,steps = int(user_details.over_all_stepcount),Reward = Decimal((reward)),created_on = Date+" 00:00:45.270177")
                    else:
                        table = Reward_History.objects.create(user = user_Detail,steps = int(user_details.over_all_stepcount),Reward = Decimal((reward)),created_on = Date+" 18:45:22.270177")
                except:
                    pass
            else:
                actual_plan = plan_purchase_history.objects.filter(user = user_details.id).last()
                step_count = int(Step_Count)
                value = Decimal(actual_plan.Plan_maximum_step/int(actual_plan.plan_reward_step_val))
                # reward = Decimal(value*actual_plan.plan_per_reward_amount)
                reward = Decimal(actual_plan.Plan_maximum_reward)
                user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal((reward))
                user_wallet.save()
                chk_data.steps = int(actual_plan.Plan_maximum_step)
                chk_data.save()
                if(str(Date) == "2022-12-23") :
                    table = Reward_History.objects.create(user = user_Detail,steps = int(actual_plan.Plan_maximum_step),Reward = Decimal((reward)),created_on = Date+" 00:00:45.270177")
                else:
                    table = Reward_History.objects.create(user = user_Detail,steps = int(actual_plan.Plan_maximum_step),Reward = Decimal((reward)),created_on = Date+" 18:45:22.270177")
        user_data={"Msg":"Data Updated","status":"true"}
        return Response(user_data)
    except:
        chk_data = Steps_history.objects.create(created_on = Date,user_id = user_Detail.id)
        if chk_data:
            Plan = user_Detail.plan
            user_wallet = UserCashWallet.objects.get(userid_id = user_Detail.id)
            step_count = int(Step_Count)
            chk_data.status = 1
            chk_data.modified_on = datetime.now()
            chk_data.steps = step_count
            chk_data.save()
            if Plan == 0:
                try:
                    actual_plan = plan.objects.get(plan_type = 0)
                    step_count = int(Step_Count)
                    value = Decimal(int(user_details.over_all_stepcount)/int(user_Detail.reward_steps))
                    reward = Decimal(value*user_Detail.reward_step_amount)
                    user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal(round(reward,2))
                    user_wallet.save()
                    chk_data.steps = int(user_details.over_all_stepcount)
                    chk_data.save()
                    if(str(Date) == "2022-12-23") :
                        table = Reward_History.objects.create(user = user_Detail,steps = int(user_details.over_all_stepcount),Reward = Decimal((reward)),created_on = Date+" 00:00:45.270177")
                    else:
                        table = Reward_History.objects.create(user = user_Detail,steps = int(user_details.over_all_stepcount),Reward = Decimal((reward)),created_on = Date+" 18:45:22.270177")
                except:
                    pass
            else:
                actual_plan = plan_purchase_history.objects.filter(user = user_details.id).last()
                step_count = int(Step_Count)
                value = Decimal(actual_plan.Plan_maximum_step/int(actual_plan.plan_reward_step_val))
                # reward = Decimal(value*actual_plan.plan_per_reward_amount)
                reward = Decimal(actual_plan.Plan_maximum_reward)
                user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal((reward))
                user_wallet.save()
                chk_data.steps = int(actual_plan.Plan_maximum_step)
                chk_data.save()
                if(str(Date) == "2022-12-23") :
                    table = Reward_History.objects.create(user = user_Detail,steps = int(actual_plan.Plan_maximum_step),Reward = Decimal((reward)),created_on = Date+" 00:00:45.270177")
                else:
                    table = Reward_History.objects.create(user = user_Detail,steps = int(actual_plan.Plan_maximum_step),Reward = Decimal((reward)),created_on = Date+" 18:45:22.270177")
        user_data={"Msg":"Data Updated","status":"true"}
        return Response(user_data)

@api_view(['POST'])
def purchase_history_api(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_Deatail=User_Management.objects.get(user_name = token.user)
    detail_count = plan_purchase_history.objects.filter(user_id = user_Deatail.id).count()
    details = plan_purchase_history.objects.filter(user_id = user_Deatail.id).order_by('-id')
    a = []
    co="Plan_name"
    co1 = "Plan_Amount"
    co2 = "Wallet_Type"
    co3 = "Hash"
    if details != "" and details != None:
        for i in details:
            emp_dict={}
            if i.plan_id_id != 0:
                try:
                    plan_plan = plan.objects.get(id = i.plan_id_id)
                    emp_dict[co]=plan_plan.plan_name
                except:
                    emp_dict[co]=""
                try:
                    emp_dict[co1]=i.purchase_amount
                except:
                    emp_dict[co1]=""
                try:
                    emp_dict[co2] = i.user_wallet_type
                except:
                    emp_dict[co2]=""
                try:
                    emp_dict[co3] = i.User_plan_validation
                except:
                    emp_dict[co3]=""
            else:
                emp_dict[co]=""
                emp_dict[co1]=""
                emp_dict[co2]=""
                emp_dict[co3]=""
            a.append(emp_dict)
        user_data={"data":a,'status':'true','token':token.key,'count':detail_count}
    else:
        user_data={"data":[],'status':'false','token':token.key,'count':detail_count}
    return Response(user_data)


# Sport Module API
@api_view(['GET'])
def sport_category_api(request):
    category_obj = SupportCategory.objects.values('category','id').filter(status = 0)
    user_data={"Msg":"Success",'status' : 'true',"Support_category_list":category_obj}
    return Response(user_data)


@api_view(['POST'])
def user_request_api(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    user_obj = User_Management.objects.get(user_name = token.user)
    category_name = request.data['support_category_name']
    content = request.data['message']
    subject = request.data['subject']
    file_type = request.data['attachment']
    read_sts = request.data["read_status"]
    tx_hash = request.data["Hash"]

  
    random_value = random.randint(10000,99999)
    random_return = str(random_value)
    function_name ='0xb6b55f25'
    try:
        tickid = request.data["ticket_id"]
        obj_tick_id = Contactus.objects.get(ticket_id = tickid)
        tick_id = obj_tick_id.ticket_id
        tick_no = 0
    except:
        tick_id = random_return
        tick_no = 1

    if file_type == "":
        file = 0
    else:
        file = 1

    try:
        obj_cat_id = SupportCategory.objects.get(category = category_name)
        if int(obj_cat_id.id) == 4:
            category_id = 4
        else:
            category_id = None
        
    except:
        obj_cat_id = 0
        category_id = None

    obj_tick_user = Contactus.objects.filter(userid_id = user_obj.id).last()
    

    address=Contract_address.objects.get(id = 1)

    obj_hash = plan_purchase_history.objects.filter(User_plan_validation = tx_hash).count()

    obj_tick_hash = Contactus.objects.filter(phone1 = tx_hash).count()
    
    if obj_tick_user != None:
        if obj_tick_user.read_status != 2:
            if tick_no == 0:
                if read_sts == "New": 
                    if file != 0:
                        SupportTicket.objects.create(ticket_id = obj_tick_id.id,comment = content,created_by = user_obj,user_type = 0,attachment = file_type)
                        Contactus.objects.filter(ticket_id = tick_id).update(read_status = 0,modified_on = datetime.now())
                    else:
                        SupportTicket.objects.create(ticket_id = obj_tick_id.id,comment = content,created_by = user_obj,user_type = 0,attachment = [])
                        Contactus.objects.filter(ticket_id = tick_id).update(read_status = 0,modified_on = datetime.now())
                    user_data={"Msg":"Success",'status' : 'true','token':token.key,'Hash' : obj_tick_user.phone1}
                    return Response(user_data)
                elif read_sts == "Closed":
                    Contactus.objects.filter(ticket_id = tick_id).update(read_status = 2,modified_on = datetime.now())
                    user_data={"Msg":"Ticket Closed successfully.",'status' : 'true','token':token.key,'Hash' : obj_tick_user.phone1}
                    return Response(user_data)
                elif read_sts == "Re-opened":
                    
                    if content != "":
                        if file != 0:
                            SupportTicket.objects.create(ticket_id = obj_tick_id.id,comment = content,created_by = user_obj,user_type = 0,attachment = file_type)
                            Contactus.objects.filter(ticket_id = tick_id).update(read_status = 4,modified_on = datetime.now())
                        else:
                            SupportTicket.objects.create(ticket_id = obj_tick_id.id,comment = content,created_by = user_obj,user_type = 0,attachment = [])
                            Contactus.objects.filter(ticket_id = tick_id).update(read_status = 4,modified_on = datetime.now())
                    else:
                        Contactus.objects.filter(ticket_id = tick_id).update(read_status = 4,modified_on = datetime.now())
                    user_data={"Msg":"Ticket Re-opened successfully.",'status' : 'true','token':token.key,'Hash' : obj_tick_user.phone1}
                    return Response(user_data)
                elif read_sts == "Replied":
                    if file != 0:
                        SupportTicket.objects.create(ticket_id = obj_tick_id.id,comment = content,created_by = user_obj,user_type = 0,attachment = file_type)
                        Contactus.objects.filter(ticket_id = tick_id).update(read_status = 1,modified_on = datetime.now())
                    else:
                        SupportTicket.objects.create(ticket_id = obj_tick_id.id,comment = content,created_by = user_obj,user_type = 0,attachment = [])
                        Contactus.objects.filter(ticket_id = tick_id).update(read_status = 1,modified_on = datetime.now())
                    user_data={"Msg":"Ticket Replied successfully.",'status' : 'true','token':token.key,'Hash' : obj_tick_user.phone1}
                    return Response(user_data)
            else:
                user_data={"Msg":"Already you have opened ticket, Kindly closed the previous ticket.",'status' : 'false','token':token.key,'Hash' : obj_tick_user.phone1}
                return Response(user_data)
        else:
            
            if category_id != None:
                
                if read_sts == "New":
                    if obj_hash == 0 and obj_tick_hash == 0:
                        
                        try:
                            receipt = web3.eth.getTransaction(tx_hash)
                        except Exception as e:
                            user_data={"Msg":"Invalid hash.",'status':'false','token':token.key}
                            return Response(user_data)
                        contract_address=receipt['to']
                        
                        input_data = receipt['input']
                        function_signature = input_data[:10]
                        if (str(address.Main_contract_address) == str(contract_address)) and (str(function_name) == str(function_signature)):
                            if file != 0:
                                Contactus.objects.create(name = user_obj,phone1 = tx_hash,userid_id = user_obj.id,email = user_obj.Email,ticket_id = tick_id,message = content,read_status = 0,attachment = file_type,support_category = category_name,subject= subject)
                            else:
                                Contactus.objects.create(name = user_obj,phone1 = tx_hash,userid_id = user_obj.id,email = user_obj.Email,ticket_id = tick_id,message = content,read_status = 0,attachment = [],support_category = category_name,subject= subject)
                            user_data={"Msg":"Your ticket reply time within 24 hours.",'status' : 'true','token':token.key,'Hash' : tx_hash}
                            return Response(user_data)  
                        else:
                            user_data={"Msg":"Invalid hash.",'status' : 'false','token':token.key}
                            return Response(user_data)
                    else:
                        user_data={"Msg":"This hash already applied.",'status' : 'false','token':token.key}
                        return Response(user_data)
                
                elif read_sts == "Re-opened":
                    
                    if content != "":
                        if file != 0:
                            SupportTicket.objects.create(ticket_id = obj_tick_id.id,comment = content,created_by = user_obj,user_type = 0,attachment = file_type)
                            Contactus.objects.filter(ticket_id = tick_id).update(read_status = 4,modified_on = datetime.now())
                        else:
                            SupportTicket.objects.create(ticket_id = obj_tick_id.id,comment = content,created_by = user_obj,user_type = 0,attachment = [])
                            Contactus.objects.filter(ticket_id = tick_id).update(read_status = 4,modified_on = datetime.now())
                    else:
                        Contactus.objects.filter(ticket_id = tick_id).update(read_status = 4,modified_on = datetime.now())
                    user_data={"Msg":"Ticket Re-opened successfully.",'status' : 'true','token':token.key,'Hash' : obj_tick_user.phone1}
                    return Response(user_data)
            else:
                if read_sts == "New":
                    if file != 0:
                        Contactus.objects.create(name = user_obj,phone1 = "",userid_id = user_obj.id,email = user_obj.Email,ticket_id = tick_id,message = content,read_status = 0,attachment = file_type,support_category = category_name,subject= subject)
                    else:
                        Contactus.objects.create(name = user_obj,phone1 = "",userid_id = user_obj.id,email = user_obj.Email,ticket_id = tick_id,message = content,read_status = 0,attachment = [],support_category = category_name,subject= subject)
                    user_data={"Msg":"Your ticket reply time within 24 hours.",'status' : 'true','token':token.key,'Hash' : tx_hash}
                    return Response(user_data)  
                elif read_sts == "Re-opened":
                    
                    if content != "":
                        if file != 0:
                            SupportTicket.objects.create(ticket_id = obj_tick_id.id,comment = content,created_by = user_obj,user_type = 0,attachment = file_type)
                            Contactus.objects.filter(ticket_id = tick_id).update(read_status = 4,modified_on = datetime.now())
                        else:
                            SupportTicket.objects.create(ticket_id = obj_tick_id.id,comment = content,created_by = user_obj,user_type = 0,attachment = [])
                            Contactus.objects.filter(ticket_id = tick_id).update(read_status = 4,modified_on = datetime.now())
                    else:
                        Contactus.objects.filter(ticket_id = tick_id).update(read_status = 4,modified_on = datetime.now())
                    user_data={"Msg":"Ticket Re-opened successfully.",'status' : 'true','token':token.key,'Hash' : obj_tick_user.phone1}
                    return Response(user_data)
            

    else:
        if category_id != None:
            
            if obj_hash == 0 and obj_tick_hash == 0:
                try:
                    receipt = web3.eth.getTransaction(tx_hash)
                except Exception as e:
                    user_data={"Msg":"Invalid hash.",'status':'false','token':token.key}
                    return Response(user_data)
                contract_address=receipt['to']
                input_data = receipt['input']
                function_signature = input_data[:10]
                if (str(address.Main_contract_address) == str(contract_address)) and (str(function_name) == str(function_signature)):
                    
                    if read_sts == "New":
                        if file != 0:
                            Contactus.objects.create(name = user_obj,phone1 = tx_hash,userid_id = user_obj.id,email = user_obj.Email,ticket_id = tick_id,message = content,read_status = 0,attachment = file_type,support_category = category_name,subject= subject)
                        else:
                            Contactus.objects.create(name = user_obj,phone1 = tx_hash,userid_id = user_obj.id,email = user_obj.Email,ticket_id = tick_id,message = content,read_status = 0,attachment = [],support_category = category_name,subject= subject)
                    user_data={"Msg":"Your ticket reply time within 24 hours.",'status' : 'true','token':token.key,'Hash' : tx_hash}
                    return Response(user_data)
                else:
                    user_data={"Msg":"Invalid hash.!",'status' : 'false','token':token.key}
                    return Response(user_data)    
            else:
                user_data={"Msg":"This hash already applied.",'status' : 'false','token':token.key}
                return Response(user_data)  
        else:
            
            if read_sts == "New":
                if file != 0:
                    Contactus.objects.create(name = user_obj,phone1 = "",userid_id = user_obj.id,email = user_obj.Email,ticket_id = tick_id,message = content,read_status = 0,attachment = file_type,support_category = category_name,subject= subject)
                else:
                    Contactus.objects.create(name = user_obj,phone1 = "",userid_id = user_obj.id,email = user_obj.Email,ticket_id = tick_id,message = content,read_status = 0,attachment = [],support_category = category_name,subject= subject)
            user_data={"Msg":"Your ticket reply time within 24 hours.",'status' : 'true','token':token.key,'Hash' : tx_hash}
            return Response(user_data)  

    user_data={"Msg":"Already you have opened ticket, Kindly closed the previous ticket",'status' : 'false','token':token.key,'Hash' : tx_hash}
    return Response(user_data)


def admin_reply_api(request,id):
    tick_id = id
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    user_obj = User_Management.objects.get(user_name = token.user)
    tick(user_obj.User_Device_id)
    user_rply_obj = Contactus.objects.get(ticket_id = tick_id)
    user_data={"Msg":"Success",'status' : 'true',"comment":user_obj.reply,"user":user_obj.name}
    return Response(user_data)

@api_view(['GET'])
def view_all_ticket(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    user_obj = User_Management.objects.get(user_name = token.user)
    tick_obj = Contactus.objects.filter(userid__user_name = user_obj.user_name).order_by('-id')
    list_ticket = []
    for tl in tick_obj:
        dict_obj = {}
        if tl.read_status == 0:
            status = 'New'
        elif tl.read_status == 1:
            status = 'Replied'
        elif tl.read_status == 2:
            status = 'Closed'
        elif tl.read_status == 3:
            status = 'Cancelled'
        elif tl.read_status == 4:
            status = 'Re-opened'
        dict_obj["ticket_id"] = tl.ticket_id
        dict_obj["username"] = str(tl.userid.Name)
        dict_obj["support_category"] = tl.support_category
        dict_obj["subject"] = tl.subject
        dict_obj["status"] = status
        date = tl.created_on
        dict_obj["created_on"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
        list_ticket.append(dict_obj)
    user_data={"Msg":"Success","status" : 'true',"token":token.key,"ticket_list":list_ticket}
    return Response(user_data)

@api_view(['GET'])
def View_Ticket_Details_API(request,t_id):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    tick_obj = Contactus.objects.values('read_status','attachment','name','message','created_on','id','ticket_id').get(ticket_id = t_id)
    if tick_obj['read_status'] == 0:
        status = 'New'
    elif tick_obj['read_status'] == 1:
        status = 'Replied'
    elif tick_obj['read_status'] == 2:
        status = 'Closed'
    elif tick_obj['read_status'] == 3:
        status = 'Cancelled'
    elif tick_obj['read_status'] == 4:
        status = 'Re-opened'
    list_ticket = []
    con_dict = {}
    img = tick_obj['attachment']
    con_dict["created_by"] = tick_obj['name']
    con_dict["user_type"] = 0
    con_dict["comment"] = tick_obj['message']
    array_string = img.replace("'", "\"")
    array = json.loads(array_string)
    con_dict["attachment"] = array
    date = tick_obj['created_on']
    con_dict["created_on"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
    list_ticket.append(con_dict)
    tick_obj_1 = SupportTicket.objects.filter(ticket_id = tick_obj['id']).order_by('id')
    for tl in tick_obj_1:
        dict_obj = {}
        file = tl.attachment
        if tl.created_by != 'admin1':
            create_by = tl.created_by
        else:
            create_by = 'Support team'
        dict_obj["created_by"] = create_by
        dict_obj["user_type"] = tl.user_type
        dict_obj["comment"] = tl.comment
        array_string = file.replace("'", "\"")
        array = json.loads(array_string)
        dict_obj["attachment"] = array
        date = tl.created_on
        dict_obj["created_on"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
        list_ticket.append(dict_obj)
    user_data={"Msg":"Success","status" : 'true',"token":token.key,"ticket_id" : tick_obj['ticket_id'],"ticket_list":list_ticket,'read_status':status}
    return Response(user_data)


# # Withdraw send request API 

# from web3 import Web3
# from web3.middleware import geth_poa_middleware


from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed

obj_stake_manage = Contract_address.objects.get(id = 1)
testBNBseedurl = obj_stake_manage.Stake_contract_Address
w3 = Web3(Web3.HTTPProvider(testBNBseedurl))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
tkn_address = Web3.toChecksumAddress(str(token_address))
token_contract = w3.eth.contract(address=tkn_address, abi=token_abi)

@api_view(['POST'])
def withdraw_send_api(request):
    if request.method == 'POST':
        try:
            Token_header = request.headers['token']
            token = Token.objects.get(key = Token_header)
            User = User_Management.objects.get(user_name = token.user)
            data = json.loads(request.body)
            frm_address = data['from_address']
            from_address = w3.toChecksumAddress(str(frm_address))
            t_address = data['to_address']
            to_address = w3.toChecksumAddress(str(t_address))
            user_key = data['api']
            amount = str(data['Amount'])
            ref_pin = (data['pin'])
            currency = data['currency']
            user_data={"Msg":"error"}
            two_fa_input = str(data['Two_Fa'])
            bnb_blnc = w3.eth.get_balance(from_address)
            bnb_blnc_wei_to_eth = w3.fromWei(bnb_blnc,'ether')
            try:
                security_type = data['security_type']
            except:
                security_type = "TFA"
            
            gas_price = w3.toWei('5', 'gwei')
            gas_limit = 100000

            if currency == "BNB":
                if Decimal(amount) > 0:
                    if bnb_blnc_wei_to_eth >= Decimal(amount):
                        if ref_pin == "":
                            try:
                                pin = Pin.objects.get(user_id = User.id )
                                if pin.pin is None:
                                    user_data={"Msg":"Set PIN",'status':'false','token':token.key}
                                    return Response(user_data)
                                else:
                                    msg = "NewUser"
                            except:
                                user_data={"Msg":"Make sure set your pin",'status':'false','token':token.key}
                                return Response(user_data)
                        else:
                            two_fa = User_two_fa.objects.get(user = User.id)
                            confirm = two_fa.user_secrete_key
                            if security_type == "TFA":
                                if two_fa.user_status == 'enable':
                                    totp = pyotp.TOTP(confirm)
                                    otp_now=totp.now()
                                    pin = Pin.objects.get(user_id = User.id)
                                    pinnn = pin.pin
                                    num1 = str(pinnn)
                                    num2 = str(123456)
                                    if int(two_fa_input) == int(otp_now):
                                        if int(ref_pin) == pin.pin:
                                            txn = {
                                                'to': to_address,
                                                'value': w3.toWei(amount, 'ether'),
                                                'gasPrice': gas_price,
                                                'gas': gas_limit,
                                                'nonce': w3.eth.get_transaction_count(from_address)
                                            }

                                            while True:
                                                try:
                                                    signed_txn = w3.eth.account.sign_transaction(txn, private_key=user_key)
                                                    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                                                    WithdrawSendHistory.objects.create(
                                                        user = User.Name,
                                                        email = User,
                                                        claim_amount = amount,
                                                        from_address = from_address,
                                                        to_address = to_address,
                                                        Transaction_Hash = txn_hash.hex(),
                                                        send_status = 1,
                                                        currency = currency,
                                                        created_on = datetime.now(),
                                                        modified_on = datetime.now()
                                                    )
                                                    return JsonResponse({"Msg":"Transaction successfully completed.",'status': 'success', 'transaction_hash': txn_hash.hex()})

                                                except ValueError as e:
                                                    if e.args[0]['code'] == -32000 and 'underpriced' in e.args[0]['message']:
                                                        gas_price = gas_price * 2
                                                        gas_limit = gas_limit * 2
                                                        txn['gasPrice'] = gas_price
                                                        txn['gas'] = gas_limit
                                                    else:
                                                        raise e
                                        else:
                                            user_data={"Msg":"App pin cannot be same",'status':'false','token':token.key}
                                            return Response(user_data)
                                    else:
                                        user_data = {"Msg":"TFA cannot be same",'status':'false','token':token.key}
                                        return Response(user_data)
                                else:
                                    user_data = {"Msg":"Make sure enable your TFA",'status':'false','token':token.key}
                                    return Response(user_data)
                            else:
                                Email_otp = Registration_otp.objects.get(user = User.id)
                                if Email_otp.email_otp == int(two_fa_input):
                                    pin = Pin.objects.get(user_id = User.id)
                                    if int(ref_pin) == pin.pin:
                                        txn = {
                                            'to': to_address,
                                            'value': w3.toWei(amount, 'ether'),
                                            'gasPrice': gas_price,
                                            'gas': gas_limit,
                                            'nonce': w3.eth.get_transaction_count(from_address)
                                        }

                                        while True:
                                            try:
                                                signed_txn = w3.eth.account.sign_transaction(txn, private_key=user_key)
                                                txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                                                WithdrawSendHistory.objects.create(
                                                        user = User.Name,
                                                        email = User,
                                                        claim_amount = amount,
                                                        from_address = from_address,
                                                        to_address = to_address,
                                                        Transaction_Hash = txn_hash.hex(),
                                                        send_status = 1,
                                                        currency = currency,
                                                        created_on = datetime.now(),
                                                        modified_on = datetime.now()
                                                    )
                                                return JsonResponse({"Msg":"Transaction successfully completed.",'status': 'success', 'transaction_hash': txn_hash.hex()})

                                            except ValueError as e:
                                                if e.args[0]['code'] == -32000 and 'underpriced' in e.args[0]['message']:
                                                    gas_price = gas_price * 2
                                                    gas_limit = gas_limit * 2
                                                    txn['gasPrice'] = gas_price
                                                    txn['gas'] = gas_limit
                                                else:
                                                    raise e
                                    else:
                                        user_data={"Msg":"App pin cannot be same",'status':'false','token':token.key}
                                        return Response(user_data)
                                else:
                                    user_data = {"Msg":"Mail OTP cannot be same",'status':'false','token':token.key}
                                    return Response(user_data)
               
                    else:    
                        user_data={"Msg":"Insufficient balance ...!!!",'status':'false','token':token.key}
                        return Response(user_data)
                else:
                    user_data={"Msg":"Market Price API down. Try After Sometimes!!!",'status':'false','token':token.key}
                    return Response(user_data)
            
            else:
                token_contract = w3.eth.contract(address=tkn_address, abi=token_abi)
                tkn_amt = int(Decimal(amount)*10 ** 8)
                jw_blnc = token_contract.functions.balanceOf(from_address).call()
                JW_blnc_wei_to_eth = jw_blnc / 100000000
                if Decimal(amount) > 0:
                    if JW_blnc_wei_to_eth >= Decimal(amount):
                        if ref_pin == "":
                            try:
                                pin = Pin.objects.get(user_id = User.id )
                                if pin.pin is None:
                                    user_data={"Msg":"Set PIN",'status':'false','token':token.key}
                                    return Response(user_data)
                                else:
                                    msg = "NewUser"
                            except:
                                user_data={"Msg":"Make sure set your pin",'status':'false','token':token.key}
                                return Response(user_data)
                        else:
                            two_fa = User_two_fa.objects.get(user = User.id)
                            confirm = two_fa.user_secrete_key
                            if security_type == "TFA":
                                if two_fa.user_status == 'enable':
                                    totp = pyotp.TOTP(confirm)
                                    otp_now=totp.now()
                                    pin = Pin.objects.get(user_id = User.id)
                                    pinnn = pin.pin
                                    num1 = str(pinnn)
                                    num2 = str(123456)
                                    if int(two_fa_input) == int(otp_now):
                                        if int(ref_pin) == pin.pin:
                                            
                                            txn = {
                                                'from': from_address,
                                                'to': tkn_address,
                                                'data': token_contract.encodeABI(fn_name='transfer', args=[to_address,  tkn_amt]),
                                                'gasPrice': gas_price,
                                                'gas': gas_limit,
                                                'nonce': w3.eth.get_transaction_count(from_address)
                                            }

                                            # txn = {
                                            #     'to': to_address,
                                            #     'value': w3.toWei(amount, 'ether'),
                                            #     'gasPrice': gas_price,
                                            #     'gas': gas_limit,
                                            #     'nonce': w3.eth.get_transaction_count(from_address)
                                            # }

                                            while True:
                                                try:
                                                    signed_txn = w3.eth.account.sign_transaction(txn, private_key=user_key)
                                                    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                                                    WithdrawSendHistory.objects.create(
                                                        user = User.Name,
                                                        email = User,
                                                        claim_amount = amount,
                                                        from_address = from_address,
                                                        to_address = to_address,
                                                        Transaction_Hash = txn_hash.hex(),
                                                        send_status = 1,
                                                        currency = currency,
                                                        created_on = datetime.now(),
                                                        modified_on = datetime.now()
                                                    )
                                                    return JsonResponse({"Msg":"Transaction successfully completed.",'status': 'success', 'transaction_hash': txn_hash.hex()})

                                                except ValueError as e:
                                                    if e.args[0]['code'] == -32000 and 'underpriced' in e.args[0]['message']:
                                                        gas_price = gas_price * 2
                                                        gas_limit = gas_limit * 2
                                                        txn['gasPrice'] = gas_price
                                                        txn['gas'] = gas_limit
                                                    else:
                                                        raise e
                                        else:
                                            user_data={"Msg":"App pin cannot be same",'status':'false','token':token.key}
                                            return Response(user_data)
                                    else:
                                        user_data = {"Msg":"TFA cannot be same",'status':'false','token':token.key}
                                        return Response(user_data)
                                else:
                                    user_data = {"Msg":"Make sure enable your TFA",'status':'false','token':token.key}
                                    return Response(user_data)
                            else:
                                Email_otp = Registration_otp.objects.get(user = User.id)
                                if Email_otp.email_otp == int(two_fa_input):
                                    pin = Pin.objects.get(user_id = User.id)
                                    if int(ref_pin) == pin.pin:

                                        token_contract = w3.eth.contract(address=tkn_address, abi=token_abi)
                                        
                                        txn = {
                                            'from': from_address,
                                            'to': tkn_address,
                                            'data': token_contract.encodeABI(fn_name='transfer', args=[to_address,  tkn_amt]),
                                            'gasPrice': gas_price,
                                            'gas': gas_limit,
                                            'nonce': w3.eth.get_transaction_count(from_address)
                                        }
                                        # txn = {
                                        #     'to': to_address,
                                        #     'value': w3.toWei(amount, 'ether'),
                                        #     'gasPrice': gas_price,
                                        #     'gas': gas_limit,
                                        #     'nonce': w3.eth.get_transaction_count(from_address)
                                        # }

                                        while True:
                                            try:
                                                signed_txn = w3.eth.account.sign_transaction(txn, private_key=user_key)
                                                txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                                                WithdrawSendHistory.objects.create(
                                                        user = User.Name,
                                                        email = User,
                                                        claim_amount = amount,
                                                        from_address = from_address,
                                                        to_address = to_address,
                                                        Transaction_Hash = txn_hash.hex(),
                                                        send_status = 1,
                                                        currency = currency,
                                                        created_on = datetime.now(),
                                                        modified_on = datetime.now()
                                                    )
                                                return JsonResponse({"Msg":"Transaction successfully completed.",'status': 'success', 'transaction_hash': txn_hash.hex()})

                                            except ValueError as e:
                                                if e.args[0]['code'] == -32000 and 'underpriced' in e.args[0]['message']:
                                                    gas_price = gas_price * 2
                                                    gas_limit = gas_limit * 2
                                                    txn['gasPrice'] = gas_price
                                                    txn['gas'] = gas_limit
                                                else:
                                                    raise e
                                    else:
                                        user_data={"Msg":"App pin cannot be same",'status':'false','token':token.key}
                                        return Response(user_data)
                                else:
                                    user_data = {"Msg":"Mail OTP cannot be same",'status':'false','token':token.key}
                                    return Response(user_data)
                 
                    else:    
                        user_data={"Msg":"Insufficient balance ...!!!",'status':'false','token':token.key}
                        return Response(user_data)    
                else:
                    user_data={"Msg":"Market Price API down. Try After Sometimes!!!",'status':'false','token':token.key}
                    return Response(user_data)
        except Exception as e:
            user_data={"Msg":"Error "+str(e),'status':'false','token':token.key}
            return Response(user_data)

    else:
        return HttpResponseNotAllowed(['POST'])
    return Response(user_data)

true=True
false=False



obj_stake_manage = Contract_address.objects.get(id = 1)
testBNBseedurl = obj_stake_manage.Stake_contract_Address
w3 = Web3(Web3.HTTPProvider(testBNBseedurl))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
tkn_address = Web3.toChecksumAddress(str(token_address))
jw_token_contract = w3.eth.contract(address=tkn_address, abi=token_abi)
# Balance fetch API
@api_view(['POST'])
def Balance_fetch_API(request):
    address = request.data['Address']
    address = Web3.toChecksumAddress(str(address))
    if address:
        bnb_blnc = web3.eth.get_balance(address)
        bnb_blnc_wei_to_eth = web3.fromWei(bnb_blnc,'ether')
        jw_blnc = jw_token_contract.functions.balanceOf(address).call()
        JW_blnc_wei_to_eth = jw_blnc / 100000000
        user_data={"Msg":"balance fetched",'status':'true',"BNB_balance" : bnb_blnc_wei_to_eth , "JW_balance" : JW_blnc_wei_to_eth}
    else:
        user_data={"Msg":"Invalid Address",'status':'false'}
    return Response(user_data)


# Withdaw listing API
@api_view(['POST'])
def Withdraw_History_List(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    usr = 0
    count = 0
    list_user = []
    start_page = request.data['pageno']
    end_value = int(start_page) * 5
    start_value = int(end_value) - 4
    with_send_hist = WithdrawSendHistory.objects.filter(user = User).order_by('-created_on')
    if with_send_hist:
        for i in with_send_hist:
            usr = usr + 1
            dict_usr = {}
            if start_value <= usr <= end_value:
                count = count + 1
                dict_usr['from_address'] = (i.from_address)
                dict_usr['to_address'] = (i.to_address)
                dict_usr['hash'] = (i.Transaction_Hash)
                dict_usr['hash'] = (i.Transaction_Hash)
                dict_usr['currency'] = (i.currency)
                dict_usr['pageno'] = start_page
                dict_usr["sno"] = usr
                list_user.append(dict_usr)
            
    user_data={"Msg":"Data Found","status":"true","Data" : list_user,"count" : with_send_hist.count(),"Email":User.Email}
    
    return Response(user_data)


@api_view(['POST'])
def Transfer_Function_Email_send(request):
    try:
        Token_header = request.headers['Token']
    except:
        user_data = {"Msg":"Token Needed","status":"false"}
        return Response(user_data)
    token = Token.objects.get(key= Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    user__name = user_details.Name
    try:
        Email = request.data['Email']
    except:
        user_data = {"Msg":"Email Input Needed","status":"false"}
        return Response(user_data)
    try:
        companyqs = Company.objects.get(id=1)
        companyname= companyqs.name
    except:
        companyqs = ''
        companyname = ''
    otp = generateOTP()
    emailtemplate = get_email_template(request,8)
    to_email = Email
    data= {
        'username':user__name,
        'email':Email,
        'domain':settings.DOMAIN_URL,
        'company_name':companyname,
        'otp':otp,
        }
    user_otp = Registration_otp.objects.filter(user = user_details.id).count()
    if user_otp == 1 :
        otp_update = Registration_otp.objects.get(user = user_details.id)
        otp_update.email_otp = int(otp)
        otp_update.save()
    elif user_otp > 1:
        user_otp_id = Registration_otp.objects.filter(user = user_details.id).last()
        otp_delete_obj = Registration_otp.objects.filter(user = user_details.id).exclude(id = user_otp_id.id)
        otp_delete_obj.delete()
        user_otp_id.email_otp = int(otp)
        user_otp_id.save()
    else: 
        user_otp = Registration_otp.objects.create(user = user_details)
        user_otp.email_otp = int(otp)
        user_otp.save()
    htmly = get_template('emailtemplate/transfertemplate.html')
    html_content = htmly.render(data)
    response = requests.post(
    "https://api.mailgun.net/v3/jasanwellness.fit/messages",
    auth=("api", decrypt_with_common_cipher(settings.MAIL_API)),
    data={"from": "WEB3 WELLNESS <noreply@jasanwellness.fit>",
    "to": [to_email],
    "subject": emailtemplate.Subject,
    "html": html_content})
    user_data = {"Msg":"Email Sent","status":"true"}
    return Response(user_data)


@api_view(['POST'])
def step_count_status(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_Deatail=User_Management.objects.values('withdraw_count').get(user_name = token.user)
    static_content = admin_notification_message.objects.get(id = 1)
    user_data={"step_count_status":user_Deatail['withdraw_count'],'status':'true','Google_fit_message':static_content.Google_fit_message,'Step_counter_message':static_content.Step_counter_message,'token':token.key}
    return Response(user_data)


@api_view(['POST'])
def step_count_status_update(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    Step_count_status = request.data['Step_count_status']
    User_Management.objects.filter(user_name = token.user).update(withdraw_count = int(Step_count_status))
    user_data={"msg":"Data Update",'status':'true','token':token.key}
    return Response(user_data)


@api_view(['POST'])
def plan_purchase_API(request): 
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_Deatail=User_Management.objects.get(user_name = token.user)
    start_page = request.data['pageno']
    end_value = int(start_page) * 10
    start_value = int(end_value) - 10
    detail_count = plan_purchase_history.objects.filter(user_id = user_Deatail.id).count()
    details = plan_purchase_history.objects.filter(user_id = user_Deatail.id).order_by('-id')[start_value:end_value]
    a = []
    co="Plan_name"
    co1 = "Plan_Amount"
    co2 = "Wallet_Type"
    co3 = "Hash"
    co4 = "pageno"
    co5 = "sno"
    co6 = "start_date"
    co7 = "end_date"
    usr = 0
    if start_page == "1":
        usr = 0
    else:
        usr = (10 * int(start_page)) - 10 
    count = 0
    dict_step_users = {}
    if details != "" and details != None:
        for i in details:
            usr = usr + 1
            emp_dict={}
            count = count + 1
            if i.plan_id_id != 0:
                try:
                    plan_plan = plan.objects.get(id = i.plan_id_id)
                    emp_dict[co]=plan_plan.plan_name
                except:
                    emp_dict[co]=""
                try:
                    emp_dict[co1]=i.purchase_amount
                except:
                    emp_dict[co1]=""
                try:
                    emp_dict[co2] = i.user_wallet_type
                except:
                    emp_dict[co2]=""
                try:
                    emp_dict[co3] = i.User_plan_validation
                except:
                    emp_dict[co3]=""
                try:
                    emp_dict[co4] = start_page
                except:
                    emp_dict[co4]=""
                try:
                    emp_dict[co6] = user_Deatail.plan_start_date
                except:
                    emp_dict[co6]=""
                try:
                    emp_dict[co7] = user_Deatail.plan_end_date
                except:
                    emp_dict[co7]=""
                emp_dict[co5] = usr
            else:
                emp_dict[co]=""
                emp_dict[co1]=""
                emp_dict[co2]=""
                emp_dict[co3]=""
                emp_dict[co4]=""
                emp_dict[co5]=""
            a.append(emp_dict)
            dict_step_users[count] = emp_dict
        user_data={"data":a,'status':'true','token':token.key,'count':detail_count}
    else:
        user_data={"data":[],'status':'false','token':token.key,'count':detail_count}
    return Response(user_data)



@api_view(['POST'])
def Active_Currency_List(request):
    try:
        Token_header = request.headers['Token']
    except:
        user_data = {"Msg":"Token Needed","status":"false"}
        return Response(user_data)
    currency_list = TradeCurrency.objects.values('symbol').filter(Q(status = 0) & Q(currncytype = 1))
    user_data = {"Data":currency_list,"status":"true",'token':Token_header}
    return Response(user_data)


@api_view(['GET'])
def Current_API(request):
    try:
        obj_market = market_price.objects.values('API').get(id = 1)
    except:
        obj_market = ""
    if obj_market != "":
        if obj_market['API'] == 0:
            API_name = "Coingecko"
        elif obj_market['API'] == 1:
            API_name = "Coinpaprika"
        else:
            API_name = "Livecoinwatch"
        user_data = {"API_name" : API_name}
        return Response(user_data)

@api_view(['GET'])
def dynamic_handle(request):
    Jw_time_line = 0
    Staking = 1
    user_data = {"Jw_time_line" : Jw_time_line,'Staking':Staking}
    return Response(user_data)


@api_view(['POST'])
def user_address_trust(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    address = request.data['Address']
    Wallet_type = request.data['wallet_type']
    user_Deatail=User_Management.objects.get(user_name = token.user)
    user_address =  Web3.toChecksumAddress(str(address))
    user_obj = ""   
    if Wallet_type == "":
        Wallet_type = "Already Exists"
    check = request.data['check']
    try:
        user_obj = user_address_trust_wallet.objects.get(user_id = user_Deatail.id)
    except:
        user_obj = "None" 
    if check == "check":
        objs_address = user_address_trust_wallet.objects.filter(Address = user_address).exclude(user_id = user_Deatail.id)
        if objs_address:
            for i in objs_address:
                if (i.Address).lower() != (user_address).lower():
                    check_status = True
                    user_data={"check_status":check_status,"check_status_message":"Successfuly checked"}
                    return Response(user_data)
                else:
                    check_status = False
                    user_data={"check_status":check_status,"check_status_message":"Wallet already used by another user."}
                    return Response(user_data)
        else:
            check_status = True
            user_data={"check_status":check_status,"check_status_message":"Successfuly checked"}
            return Response(user_data)
    elif check == "create":
        obj_address = user_address_trust_wallet.objects.filter(Address = user_address).count()
        if user_obj == "None":
            if int(obj_address) == 0:
                user_address_trust_wallet.objects.create(user = user_Deatail,Address = user_address,wallet_type = Wallet_type,modified_on=datetime.now())
                check_status = True
                user_data={"check_status":check_status,"check_status_message":"Successfuly checked"}
                return Response(user_data)
            else:
                check_status = False
                user_data={"check_status":check_status,"check_status_message":"Wallet already used by another user."}
                return Response(user_data)
        else:
            check_status = True
            user_data={"check_status":check_status,"check_status_message":"Successfuly checked"}
            return Response(user_data)
    
    user_data={"Msg":"Success","status":True}
    return Response(user_data)


@api_view(['POST'])
def user_address_trust_edit(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key=Token_header)
    address = request.data['Address']
    Wallet_type = request.data['wallet_type']
    user_Deatail = User_Management.objects.get(user_name=token.user)
    user_address = Web3.toChecksumAddress(str(address))

    try:
        user_obj = user_address_trust_wallet.objects.get(user_id=user_Deatail.id)
    except user_address_trust_wallet.DoesNotExist:
        user_obj = user_address_trust_wallet(user_id=user_Deatail.id)

    objs_address = user_address_trust_wallet.objects.filter(Address=user_address)

    if objs_address.exists():
        user_data = {"Msg": "Wallet already used by another user.", "status": False}
        return Response(user_data)
    else:
        user_obj.Address = user_address
        user_obj.modified_on = datetime.now()
        user_obj.save()

    user_data = {"Msg": "Success", "status": True}
    return Response(user_data)


def Plan_edit_api(request,id):
#   Token_header = request.headers['Token']
#   token = Token.objects.get(key = Token_header)
#   id = request.data["id"] 
    user_Deatail=User_Management.objects.get(id = id)


    obj_wall_blnc = UserCashWallet.objects.get(userid_id = user_Deatail.id)
    obj_wall_flush_blnc = wallet_flush_history.objects.filter(user_id = user_Deatail.id).last()
    end_date = "2023-12-16 23:00"
#   old_blnc = request.data['blnc_check']
    #   if end_date:
    #     old_blnc = 0
    #   else:
    #     old_blnc = 2
    # if int(old_blnc) == 1 and end_date:
    if obj_wall_flush_blnc != None:
        UserCashWallet.objects.filter(userid_id = user_Deatail.id).update(balanceone = obj_wall_flush_blnc.wallet_balanceone , referalincome = obj_wall_flush_blnc.Wallet_referral_income)
        User_Management.objects.filter(id = id).update(plan_end_date = end_date)
        PlanDateUpdateHistory.objects.create(user = user_Deatail.Name,email = user_Deatail.Email,plan_name = user_Deatail.plan,planstart_date = user_Deatail.plan_start_date,planend_date = user_Deatail.plan_end_date,plan_updated_end_date = end_date)
        user_data = {"Msg" : "Data updated.","end_date" : end_date}
    else:
        User_Management.objects.filter(id = id).update(plan_end_date = end_date)
        PlanDateUpdateHistory.objects.create(user = user_Deatail.Name,email = user_Deatail.Email,plan_name = user_Deatail.plan,planstart_date = user_Deatail.plan_start_date,planend_date = user_Deatail.plan_end_date,plan_updated_end_date = end_date)
        # User_Management.objects.filter(id = id).update(plan_end_date = end_date)
        user_data = {"Msg" : "Data updated.","end_dateee" : end_date}
      
    return JsonResponse(user_data)
    


def stack_history_edit_api(request,id):
    user_Deatail=Stake_history_management.objects.using('second_db').get(user = id)
    future_date = user_Deatail.start_date + relativedelta(months=27)
    percentage= 7.4
    rew_per_mon=int(user_Deatail.Amount_USDT)*percentage/100
    month= 27
    maxxx=rew_per_mon*month
    period=month
    stake_history_entry = Stake_history_management.objects.using('second_db').get(user=id)
    stake_history_entry.reward_per_month = rew_per_mon
    stake_history_entry.maximum_reward = maxxx
    stake_history_entry.period = period
    stake_history_entry.end_date = future_date
    stake_history_entry.save()
    user_data = {"Msg" : "Data updated."}
    return JsonResponse(user_data)


def missing_reward_update_two_api(request,Date,count,Token_header):
    Token_header = Token_header
    token = Token.objects.get(key= Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    Email = user_details.Email
    Date = Date
    Step_Count = count
    user_Detail=User_Management.objects.get(Email = Email) 
    chk_data = LoginHistory.objects.filter(user = user_details,created_on__date = Date).count()
    t_day = date.today()
    to_day = str(t_day.year)+'-'+str(t_day.month)+'-'+str(t_day.day)
    if str(Date) >= str(to_day):
        user_data={"Msg":"Can't claim reward.","status":"false"}
        return JsonResponse(user_data)
    # if chk_data == 0 :
    #     user_data={"Msg":"Data not found check login history","status":"false"}
    #     return JsonResponse(user_data)
    reward_chk_data = Reward_History.objects.filter(created_on__date = Date,user_id = user_Detail.id,reward_status = "step_reward").count()
    if reward_chk_data > 0:
        user_data={"Msg":"Reward Has Been Already Updated","status":"false","date":Date,"date_one":t_day}
        return JsonResponse(user_data)
    his_date = Steps_history.objects.filter(created_on__date = Date,user_id = user_Detail.id).count()
    if his_date > 1:
        his_date_count = Steps_history.objects.filter(created_on__date = Date,user_id = user_Detail.id).last()
        step_his_delete = Steps_history.objects.filter(created_on__date = Date,user_id = user_Detail.id).exclude(id = his_date_count.id)
        step_his_delete.delete()
    try:
        chk_data = Steps_history.objects.get(created_on__date = Date,user_id = user_Detail.id)
        if chk_data:
            Plan = user_Detail.plan
            user_wallet = UserCashWallet.objects.get(userid_id = user_Detail.id)
            step_count = int(Step_Count)
            chk_data.status = 1
            chk_data.modified_on = datetime.now()
            chk_data.steps = step_count
            chk_data.save()
            if Plan == 0:
                try:
                    actual_plan = plan.objects.get(plan_type = 0)
                    step_count = int(Step_Count)
                    value = Decimal(int(user_details.over_all_stepcount)/int(user_Detail.reward_steps))
                    reward = Decimal(value*user_Detail.reward_step_amount)
                    user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal(round(reward,2))
                    user_wallet.save()
                    chk_data.steps = int(user_details.over_all_stepcount)
                    chk_data.save()
                    if(str(Date) == "2022-12-23") :
                        table = Reward_History.objects.create(user = user_Detail,steps = int(user_details.over_all_stepcount),Reward = Decimal((reward)),created_on = Date+" 00:00:45.270177")
                    else:
                        table = Reward_History.objects.create(user = user_Detail,steps = int(user_details.over_all_stepcount),Reward = Decimal((reward)),created_on = Date+" 18:45:22.270177")
                except:
                    pass
            else:
                actual_plan = plan_purchase_history.objects.filter(user = user_details.id).last()
                step_count = int(Step_Count)
                value = Decimal(actual_plan.Plan_maximum_step/int(actual_plan.plan_reward_step_val))
                # reward = Decimal(value*actual_plan.plan_per_reward_amount)
                reward = Decimal(actual_plan.Plan_maximum_reward)
                user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal((reward))
                user_wallet.save()
                chk_data.steps = int(actual_plan.Plan_maximum_step)
                chk_data.save()
                if(str(Date) == "2022-12-23") :
                    table = Reward_History.objects.create(user = user_Detail,steps = int(actual_plan.Plan_maximum_step),Reward = Decimal((reward)),created_on = Date+" 00:00:45.270177")
                else:
                    table = Reward_History.objects.create(user = user_Detail,steps = int(actual_plan.Plan_maximum_step),Reward = Decimal((reward)),created_on = Date+" 18:45:22.270177")
        user_data={"Msg":"Data Updated","status":"true"}
        return JsonResponse(user_data)
    except:
        chk_data = Steps_history.objects.create(created_on = Date,user_id = user_Detail.id)
        if chk_data:
            Plan = user_Detail.plan
            user_wallet = UserCashWallet.objects.get(userid_id = user_Detail.id)
            step_count = int(Step_Count)
            chk_data.status = 1
            chk_data.modified_on = datetime.now()
            chk_data.steps = step_count
            chk_data.save()
            if Plan == 0:
                try:
                    actual_plan = plan.objects.get(plan_type = 0)
                    step_count = int(Step_Count)
                    value = Decimal(int(user_details.over_all_stepcount)/int(user_Detail.reward_steps))
                    reward = Decimal(value*user_Detail.reward_step_amount)
                    user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal(round(reward,2))
                    user_wallet.save()
                    chk_data.steps = int(user_details.over_all_stepcount)
                    chk_data.save()
                    if(str(Date) == "2022-12-23") :
                        table = Reward_History.objects.create(user = user_Detail,steps = int(user_details.over_all_stepcount),Reward = Decimal((reward)),created_on = Date+" 00:00:45.270177")
                    else:
                        table = Reward_History.objects.create(user = user_Detail,steps = int(user_details.over_all_stepcount),Reward = Decimal((reward)),created_on = Date+" 18:45:22.270177")
                except:
                    pass
            else:
                actual_plan = plan_purchase_history.objects.filter(user = user_details.id).last()
                step_count = int(Step_Count)
                value = Decimal(actual_plan.Plan_maximum_step/int(actual_plan.plan_reward_step_val))
                # reward = Decimal(value*actual_plan.plan_per_reward_amount)
                reward = Decimal(actual_plan.Plan_maximum_reward)
                user_wallet.balanceone = Decimal(user_wallet.balanceone)+Decimal((reward))
                user_wallet.save()
                chk_data.steps = int(actual_plan.Plan_maximum_step)
                chk_data.save()
                if(str(Date) == "2022-12-23") :
                    table = Reward_History.objects.create(user = user_Detail,steps = int(actual_plan.Plan_maximum_step),Reward = Decimal((reward)),created_on = Date+" 00:00:45.270177")
                else:
                    table = Reward_History.objects.create(user = user_Detail,steps = int(actual_plan.Plan_maximum_step),Reward = Decimal((reward)),created_on = Date+" 18:45:22.270177")
        user_data={"Msg":"Data Updated","status":"true"}
        return JsonResponse(user_data)

import time

obj_stake_manage = Contract_address.objects.get(id = 1)
testBNBseedurl = obj_stake_manage.Stake_contract_Address
w3 = Web3(Web3.HTTPProvider(testBNBseedurl))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
tkn_address = Web3.toChecksumAddress(str(usdt_token_address))
usdt_token_contract = w3.eth.contract(address=tkn_address, abi=usdt_token_abi)



@api_view(['POST'])
def usdt_send_api(request):
    if request.method == 'POST':
        try:
            Token_header = request.headers['token']
            token = Token.objects.get(key = Token_header)
            User = User_Management.objects.get(user_name = token.user)
            data = json.loads(request.body)
            frm_address = data['from_address']
            from_address = w3.toChecksumAddress(str(frm_address))
            t_address = data['to_address']
            to_address = w3.toChecksumAddress(str(t_address))
            user = data['api']
            user_key=user.lower()
            amount = Decimal(data['Amount'])
            currency = "USDT"
            now=datetime.now()
            package_type=data['package_type']
            if  int(package_type) == 1:
                package_days= 32
            elif int(package_type) == 2:
                package_days= 90
            elif int(package_type) == 3:
                package_days= 180
            elif int(package_type) == 4:
                package_days= 365
            user_data={"Msg":"error"}
            bnb_blnc = usdt_token_contract.functions.balanceOf(from_address).call()
            bnb_blnc_wei_to_eth= bnb_blnc / 100000000
            gas_price = w3.toWei('5', 'gwei')
            gas_limit = 100000

            if Decimal(amount) > 0:
                if bnb_blnc_wei_to_eth >= Decimal(amount):
                    tkn_amt = int(Decimal(amount) * 10 ** 18)

                    txn = {
                        'from': from_address,
                        'to': tkn_address,
                        'data': usdt_token_contract.encodeABI(fn_name='transfer', args=[to_address,tkn_amt]),
                        'gasPrice': gas_price,
                        'gas': gas_limit,
                        'nonce': w3.eth.get_transaction_count(from_address)
                    }

                    while True:
                        try:
                            signed_txn = w3.eth.account.sign_transaction(txn, private_key=user_key)
                            txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                            trans_hash=txn_hash.hex()
                            time.sleep(4)
                            receipt = web3.eth.getTransactionReceipt(trans_hash)
                            if receipt['status'] == 1:
                                WithdrawSendUSDTHistory.objects.create( 
                                    user = User.Email,
                                    email = User,
                                    claim_amount = amount,
                                    from_address = from_address,
                                    to_address = to_address,
                                    Transaction_Hash = trans_hash,
                                    send_status = 1,
                                    currency = currency,
                                    type="Withdraw",
                                    plan_start_date = now ,
                                    plan_end_date= now +timedelta(package_days),
                                    created_on = datetime.now(),
                                    modified_on = datetime.now()
                                )
                                return JsonResponse({"Msg":"Transaction successfully completed.",'status': 'success', 'transaction_hash': txn_hash.hex()})
                            elif receipt['status'] == 0:
                                return JsonResponse({"Msg":"Transaction Failed.",'status': 'false', 'transaction_hash': txn_hash.hex()})

                        except ValueError as e:
                            if e.args[0]['code'] == -32000 and 'underpriced' in e.args[0]['message']:
                                gas_price = gas_price * 2
                                gas_limit = gas_limit * 2
                                txn['gasPrice'] = gas_price
                                txn['gas'] = gas_limit
                            else:
                                raise e
                else:    
                    user_data={"Msg":"Insufficient balance ...!!!",'status':'false','token':token.key}
                    return Response(user_data)
            else:
                user_data={"Msg":"Market Price API down. Try After Sometimes!!!",'status':'false','token':token.key}
                return Response(user_data)
        except Exception as e:
            user_data={"Msg":"Error "+str(e),'status':'false','token':token.key}
            return Response(user_data)

    else:
        return HttpResponseNotAllowed(['POST'])
    


obj_stake_manage = Contract_address.objects.get(id = 1)
testBNBseedurl = obj_stake_manage.Stake_contract_Address
w3 = Web3(Web3.HTTPProvider(testBNBseedurl))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
usdt_tkn_address = "0x55d398326f99059fF775485246999027B3197955"
Usdt_token_abi  = [{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"_decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]
usd_token_contract = w3.eth.contract(address=usdt_tkn_address, abi=Usdt_token_abi)




@api_view(['POST'])
def plan_usdt_send_api(request):
    if request.method == 'POST':
        try:
            Token_header = request.headers['token']
            token = Token.objects.get(key = Token_header)
            User = User_Management.objects.get(user_name = token.user)
            data = json.loads(request.body)
            frm_address = data['from_address']
            from_address = w3.toChecksumAddress(str(frm_address))
            t_address = data['to_address']
            to_address = w3.toChecksumAddress(str(t_address))
            user = data['api']
            user_key=user.lower()
            amount = Decimal(data['Amount'])
            currency = "USDT"
            now=datetime.now()
            package_type=data['package_type']
            if  int(package_type) == 1:
                package_days= 32
            elif int(package_type) == 2:
                package_days= 90
            elif int(package_type) == 3:
                package_days= 180
            elif int(package_type) == 4:
                package_days= 365
            user_data={"Msg":"error"}
            bnb_blnc = usd_token_contract.functions.balanceOf(from_address).call()
            bnb_blnc_wei_to_eth= bnb_blnc / 100000000
            gas_price = w3.toWei('5', 'gwei')
            gas_limit = 100000

            if Decimal(amount) > 0:
                if bnb_blnc_wei_to_eth >= Decimal(amount):
                    tkn_amt = int(Decimal(amount) * 10 ** 18)

                    txn = {
                        'from': from_address,
                        'to': usdt_tkn_address,
                        'data': usd_token_contract.encodeABI(fn_name='transfer', args=[to_address,tkn_amt]),
                        'gasPrice': gas_price,
                        'gas': gas_limit,
                        'nonce': w3.eth.get_transaction_count(from_address)
                    }
                    while True:
                        try:
                            signed_txn = w3.eth.account.sign_transaction(txn, private_key=user_key)
                            txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                            trans_hash=txn_hash.hex()
                            time.sleep(4)
                            receipt = web3.eth.getTransactionReceipt(trans_hash)
                            if receipt['status'] == 1:
                                WithdrawSendUSDTHistory.objects.create( 
                                    user = User.Email,
                                    email = User,
                                    claim_amount = amount,
                                    from_address = from_address,
                                    to_address = to_address,
                                    Transaction_Hash = trans_hash,
                                    send_status = 1,
                                    currency = currency,
                                    type="Plan_purchase",
                                    plan_start_date = now ,
                                    plan_end_date= now +timedelta(package_days),
                                    created_on = datetime.now(),
                                    modified_on = datetime.now()
                                )
                                return JsonResponse({"Msg":"Transaction successfully completed.",'status': 'success', 'transaction_hash': txn_hash.hex()})
                            elif receipt['status'] == 0:
                                return JsonResponse({"Msg":"Transaction Failed.",'status': 'false', 'transaction_hash': txn_hash.hex(),"tkn_address":usdt_tkn_address})
                           
                        except ValueError as e:
                            if e.args[0]['code'] == -32000 and 'underpriced' in e.args[0]['message']:
                                gas_price = gas_price * 2
                                gas_limit = gas_limit * 2
                                txn['gasPrice'] = gas_price
                                txn['gas'] = gas_limit
                            else:
                                raise e
                else:    
                    user_data={"Msg":"Insufficient balance ...!!!",'status':'false','token':token.key}
                    return Response(user_data)
            else:
                user_data={"Msg":"Market Price API down. Try After Sometimes!!!",'status':'false','token':token.key}
                return Response(user_data)
        except Exception as e:
            user_data={"Msg":"Error "+str(e),'status':'false','token':token.key}
            return Response(user_data)
    else:
        return HttpResponseNotAllowed(['POST'])
    

obj_stake_manage = Contract_address.objects.get(id = 1)
testBNBseedurl = obj_stake_manage.Stake_contract_Address
w3 = Web3(Web3.HTTPProvider(testBNBseedurl))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
tkn_address = Web3.toChecksumAddress(str(token_address))
token_contract = w3.eth.contract(address=tkn_address, abi=token_abi)

@api_view(['POST'])
def user_add_plan_api(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    wallet_address=user_address_trust_wallet.objects.get(user=User.id)
    trans_hash = request.data['trans_hash'] 
    duration =request.data['duration']
    plan_id =request.data['plan_id']
    plan_days=''
    Plan=plan.objects.get(id=plan_id)
    plan_amount=Plan.plan_purchase_amount_monthly / 26
    plan_amt=f"{plan_amount:.8f}"
    plan_amt_value = str(plan_amt)[:6]
    try:
        companyqs = Company.objects.get(id=1)
        companyname= companyqs.name
    except:
        companyqs = ''
        companyname = ''
    if len(trans_hash) == 66:
        main_address="0x5936c8415c62c4b5c2515d7fa93d9a5881a2218d"
        function_name='0xb6b55f25'
        transfer_name='0xa9059cbb'
        obj_hash = plan_purchase_history.objects.filter(User_plan_validation = trans_hash).count()
        stake_hash=stake_deposit_management.objects.using('second_db').filter(Hash = trans_hash).count()
        receipt = web3.eth.getTransaction(trans_hash)
        sender_address=receipt['from'].lower()
        input_data = receipt['input']
        function_signature = input_data[:10]
        if function_signature == '0xb6b55f25':
            timestamp_hex = input_data[66:]
            timestamp_dec = int(timestamp_hex, 16) 
            filter_value = str(timestamp_dec/10**8)[:6]
            receipt1 = web3.eth.getTransactionReceipt(trans_hash)
            hex_address = (receipt1['logs'][0]['topics'][2].hex())
            hex_address = hex_address[26:]
            ethereum_address = ("0x" + hex_address)
            if (str(main_address) == str(ethereum_address)) and (str(function_name) == str(function_signature)):
                if  sender_address  == wallet_address.Address.lower():
                    if  stake_hash == 0:
                        if obj_hash == 0:
                            if plan_amt_value == filter_value:
                                plan_id = plan.objects.get(plan_name =Plan.plan_name)
                                plan_purchase=int(plan_id.plan_purchase_type)
                                if duration == "Monthly" :
                                    plan_duration = 0
                                    plan_days = 30
                                    plan_amount = plan_id.plan_purchase_amount_monthly
                                if duration == "Quarterly" :
                                    plan_duration = 1
                                    plan_days = 90
                                    plan_amount = plan_id.plan_purchase_amount_quarterly
                                if duration == "Annual" :
                                    plan_duration = 2
                                    plan_days = 365
                                    plan_amount = plan_id.plan_purchase_amount_annual

                                wallet = UserCashWallet.objects.get(userid = User)
                                wallet_flush_history.objects.create(user = User,wallet_balanceone = wallet.balanceone,Wallet_referral_income = wallet.referalincome,User_before_plan = User.plan)
                                wallet.balanceone = 0
                                wallet.referalincome = 0
                                wallet.save()
                                if plan_purchase == 1:
                                    try:
                                        user_stake_obj = stake_wallet_management.objects.using('second_db').get(user = User.id)
                                    except:
                                        user_stake_obj = 0
                                    if user_stake_obj != 0:
                                        amunt=plan_id.activate_plan
                                        value=Decimal(plan_amount) - Decimal(amunt)
                                        user_stake_obj.stake_Wallet=Decimal(user_stake_obj.stake_Wallet)  + Decimal(value)
                                        user_stake_obj.save(using='second_db')
                                        stake_claim_reward_history.objects.using('second_db').create(user = User.id,email=User.Email,type='Plan Purchase',stake_Wallet_reward_amount = Decimal(value),original_amount=plan_amount)
                                else:
                                    pass
                                User.plan = plan_id.id
                                User.plan_start_date = datetime.now()
                                desired_time = datetime.strptime("23:55", "%H:%M").time()
                                today = datetime.now()
                                today_with_desired_time = datetime.combine(today.date(), desired_time)
                                end_date = today_with_desired_time + timedelta(plan_days)
                                User.plan_end_date = end_date
                                User.user_referral_eligible_level = plan_id.referral_level_eligible
                                User.plan_validation = duration
                                User.save()
                                User.Health_Withdraw_max_value = plan_id.health_withdraw_maximum_limit
                                User.Health_Withdraw_min_value = plan_id.health_withdraw_minimum_limit
                                User.Referral_Withdraw_max_value = plan_id.referral_withdraw_maximum_limit
                                User.Referral_Withdraw_min_value = plan_id.referral_withdraw_minimum_limit
                                User.save()
                                if plan_purchase == 1:
                                    Jw_plan_purchase_history.objects.create(user = User,activate_plan=plan_id.activate_plan ,plan_name = plan_id.plan_name ,stake_credit=plan_id.user_stake_credit,purchase_amount = amunt,user_wallet_type = "Trust_Wallet", buy_type = "User Recharge Plan")
                                    plan_purchase_history.objects.create(user = User , User_plan_validation = trans_hash , plan_id = plan_id , Plan_maximum_step = plan_id.Max_step_count , Plan_minimum_step = plan_id.Min_step_count , Plan_maximum_reward = plan_id.reward_amount , Plan_referral_status = plan_id.referral_status , Plan_Two_X_Boost_status = plan_id.two_X_Boost_status , Plan_Withdraw_status = plan_id.withdraw_status , Plan_Level = plan_id.referral_level_eligible , purchase_amount = plan_amount , user_wallet_type = "Trust_Wallet" , buy_type = "User Recharge Plan",plan_reward_step_val = plan_id.Reward_step_value,plan_per_reward_amount = plan_id.plan_reward_amount,stake_wallet_monthly_split_percentage=plan_id.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=plan_id.withdraw_wallet_monthly_percentage,support_status=plan_id.support_status,monthly_support=plan_id.monthly_support_status,quarterly_support=plan_id.quarterly_support_status,annual_support=plan_id.annual_support_status,plan_purchase_type=plan_id.plan_purchase_type,halfyearly_support=plan_id.halfyearly_support_status,monthly_support_amount=plan_id.monthly_support_amount,quarterly_support_amount=plan_id.quarterly_support_amount,halfyearly_support_amount=plan_id.halfyearly_support_amount,annual_support_amount=plan_id.annual_support_amount,current_api_price="26")
                                else:
                                    plan_purchase_history.objects.create(user = User , User_plan_validation = trans_hash , plan_id = plan_id , Plan_maximum_step = plan_id.Max_step_count , Plan_minimum_step = plan_id.Min_step_count , Plan_maximum_reward = plan_id.reward_amount , Plan_referral_status = plan_id.referral_status , Plan_Two_X_Boost_status = plan_id.two_X_Boost_status , Plan_Withdraw_status = plan_id.withdraw_status , Plan_Level = plan_id.referral_level_eligible , purchase_amount = plan_amount , user_wallet_type = "Trust_Wallet" , buy_type = "User Recharge Plan",plan_reward_step_val = plan_id.Reward_step_value,plan_per_reward_amount = plan_id.plan_reward_amount,stake_wallet_monthly_split_percentage=plan_id.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=plan_id.withdraw_wallet_monthly_percentage,support_status=plan_id.support_status,monthly_support=plan_id.monthly_support_status,quarterly_support=plan_id.quarterly_support_status,annual_support=plan_id.annual_support_status,plan_purchase_type=plan_id.plan_purchase_type,halfyearly_support=plan_id.halfyearly_support_status,monthly_support_amount=plan_id.monthly_support_amount,quarterly_support_amount=plan_id.quarterly_support_amount,halfyearly_support_amount=plan_id.halfyearly_support_amount,annual_support_amount=plan_id.annual_support_amount,current_api_price="26")

                                if plan_id.referral_status == 0:
                                    User.referral_plan_status = 0
                                    User.save()
                                else:
                                    User.referral_plan_status = 1
                                    User.save()

                                User_Management.objects.filter(id = User.id).update(plan = plan_id.id)
                                
                                if User.referal_code != "" or User.referal_code != None:
                                    
                                    a=[]
                                    ref_code = User.referal_code
                                    
                                    reff_id = Referral_code.objects.get(referal_code=ref_code)
                                    referred_user = User_Management.objects.get(id = reff_id.user.id)
                                    uesr_level = User.Referral_Level
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
                                    obj_plan_hist = plan_purchase_history.objects.filter(user_id = User.id).count()
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
                                                            obj_plan_hist = plan_purchase_history.objects.filter(user_id = User.id).count()
                                                            Market_Price = market_price.objects.get(id = 1)
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
                                                            table = Referral_reward_History.objects.create(user = user,referral_id = (User.Name),reward = Decimal(actual_reward))
                                                            b = b+1 
                                                    else:
                                                        b = b +1
                                                        pass
                                                else:
                                                    b = b +1
                                                    pass
                                    sum = 0
                                    if plan_purchase == 1:
                                        admin_profit = Decimal(amunt) - l
                                        adminprofit = Admin_Profit.objects.create(user = User,admin_profit = admin_profit,Profit_type = "Plan Purchase")
                                    else:
                                        admin_profit = plan_amount - l
                                        adminprofit = Admin_Profit.objects.create(user = User,admin_profit = admin_profit,Profit_type = "Plan Purchase")
                                    user_data={"Msg":"Plan Updated successfully.'",'status' : 'true','token':token.key}
                                    return Response(user_data)            
                                else:   
                                    pass
                            else:
                                user_data={"Msg":"Transaction Hash Timed Out.Please Contact Support Team!!!",'false' : 'true','token':token.key}
                                return Response(user_data)
                        else:
                            user_data={"Msg":"This Hash is Already Associated With Plan Purchase!",'status' : 'false','token':token.key}
                            return Response(user_data)
                    else:
                        user_data={"Msg":"This Hash is Already Associated With Stake Deposit !",'status' : 'false','token':token.key}
                        return Response(user_data)
                else:
                    user_data={"Msg":"Invalid Sender Address!",'status' : 'false','token':token.key}
                    return Response(user_data)
            else:
                user_data={"Msg":"Invalid hash!",'status' : 'false','token':token.key}
                return Response(user_data)
        else:
            plan_days=''
            timestamp_hex = input_data[120:]
            timestamp_dec = int(timestamp_hex, 16)
            filter_value = str(timestamp_dec/10**8)[:6]
            removedMethodName = input_data[34:74]
            contract_address= "0x" + removedMethodName
            if (str(main_address) == str(contract_address)) and (str(transfer_name) == str(function_signature)):
                if  sender_address  == wallet_address.Address.lower():
                    if  stake_hash == 0:
                        if obj_hash == 0:
                            if plan_amt_value == filter_value:
                                plan_id = plan.objects.get(plan_name =Plan.plan_name)
                                plan_purchase=int(plan_id.plan_purchase_type)
                                if duration == "Monthly" :
                                    plan_duration = 0
                                    plan_days = 30
                                    plan_amount = plan_id.plan_purchase_amount_monthly
                                if duration == "Quarterly" :
                                    plan_duration = 1
                                    plan_days = 90
                                    plan_amount = plan_id.plan_purchase_amount_quarterly
                                if duration == "Annual" :
                                    plan_duration = 2
                                    plan_days = 365
                                    plan_amount = plan_id.plan_purchase_amount_annual

                                wallet = UserCashWallet.objects.get(userid = User)
                                wallet_flush_history.objects.create(user = User,wallet_balanceone = wallet.balanceone,Wallet_referral_income = wallet.referalincome,User_before_plan = User.plan)
                                wallet.balanceone = 0
                                wallet.referalincome = 0
                                wallet.save()
                                if plan_purchase == 1:
                                    try:
                                        user_stake_obj = stake_wallet_management.objects.using('second_db').get(user = User.id)
                                    except:
                                        user_stake_obj = 0
                                    if user_stake_obj != 0:
                                        amunt=plan_id.activate_plan
                                        value=Decimal(plan_amount) - Decimal(amunt)
                                        user_stake_obj.stake_Wallet=Decimal(user_stake_obj.stake_Wallet)  + Decimal(value)
                                        user_stake_obj.save(using='second_db')
                                        stake_claim_reward_history.objects.using('second_db').create(user = User.id,email=User.Email,type='Plan Purchase',stake_Wallet_reward_amount = Decimal(value),original_amount=plan_amount)
                                else:
                                    pass
                                User.plan = plan_id.id
                                User.plan_start_date = datetime.now()
                                desired_time = datetime.strptime("23:55", "%H:%M").time()
                                today = datetime.now()
                                today_with_desired_time = datetime.combine(today.date(), desired_time)
                                end_date = today_with_desired_time + timedelta(plan_days)
                                User.plan_end_date = end_date
                                User.user_referral_eligible_level = plan_id.referral_level_eligible
                                User.plan_validation = duration
                                User.save()
                                User.Health_Withdraw_max_value = plan_id.health_withdraw_maximum_limit
                                User.Health_Withdraw_min_value = plan_id.health_withdraw_minimum_limit
                                User.Referral_Withdraw_max_value = plan_id.referral_withdraw_maximum_limit
                                User.Referral_Withdraw_min_value = plan_id.referral_withdraw_minimum_limit
                                User.save()
                                if plan_purchase == 1:
                                    Jw_plan_purchase_history.objects.create(user = User,activate_plan=plan_id.activate_plan ,plan_name = plan_id.plan_name ,stake_credit=plan_id.user_stake_credit,purchase_amount = amunt,user_wallet_type = "Trust_Wallet", buy_type = "User Recharge Plan")
                                    plan_purchase_history.objects.create(user = User , User_plan_validation = trans_hash , plan_id = plan_id , Plan_maximum_step = plan_id.Max_step_count , Plan_minimum_step = plan_id.Min_step_count , Plan_maximum_reward = plan_id.reward_amount , Plan_referral_status = plan_id.referral_status , Plan_Two_X_Boost_status = plan_id.two_X_Boost_status , Plan_Withdraw_status = plan_id.withdraw_status , Plan_Level = plan_id.referral_level_eligible , purchase_amount = plan_amount , user_wallet_type = "Trust_Wallet" , buy_type = "User Recharge Plan",plan_reward_step_val = plan_id.Reward_step_value,plan_per_reward_amount = plan_id.plan_reward_amount,stake_wallet_monthly_split_percentage=plan_id.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=plan_id.withdraw_wallet_monthly_percentage,support_status=plan_id.support_status,monthly_support=plan_id.monthly_support_status,quarterly_support=plan_id.quarterly_support_status,annual_support=plan_id.annual_support_status,plan_purchase_type=plan_id.plan_purchase_type,halfyearly_support=plan_id.halfyearly_support_status,monthly_support_amount=plan_id.monthly_support_amount,quarterly_support_amount=plan_id.quarterly_support_amount,halfyearly_support_amount=plan_id.halfyearly_support_amount,annual_support_amount=plan_id.annual_support_amount,current_api_price="26")
                                else:
                                    plan_purchase_history.objects.create(user = User , User_plan_validation = trans_hash , plan_id = plan_id , Plan_maximum_step = plan_id.Max_step_count , Plan_minimum_step = plan_id.Min_step_count , Plan_maximum_reward = plan_id.reward_amount , Plan_referral_status = plan_id.referral_status , Plan_Two_X_Boost_status = plan_id.two_X_Boost_status , Plan_Withdraw_status = plan_id.withdraw_status , Plan_Level = plan_id.referral_level_eligible , purchase_amount = plan_amount , user_wallet_type = "Trust_Wallet" , buy_type = "User Recharge Plan",plan_reward_step_val = plan_id.Reward_step_value,plan_per_reward_amount = plan_id.plan_reward_amount,stake_wallet_monthly_split_percentage=plan_id.stake_wallet_monthly_percentage,withdraw_wallet_monthly_split_percentage=plan_id.withdraw_wallet_monthly_percentage,support_status=plan_id.support_status,monthly_support=plan_id.monthly_support_status,quarterly_support=plan_id.quarterly_support_status,annual_support=plan_id.annual_support_status,plan_purchase_type=plan_id.plan_purchase_type,halfyearly_support=plan_id.halfyearly_support_status,monthly_support_amount=plan_id.monthly_support_amount,quarterly_support_amount=plan_id.quarterly_support_amount,halfyearly_support_amount=plan_id.halfyearly_support_amount,annual_support_amount=plan_id.annual_support_amount,current_api_price="26")

                                if plan_id.referral_status == 0:
                                    User.referral_plan_status = 0
                                    User.save()
                                else:
                                    User.referral_plan_status = 1
                                    User.save()

                                User_Management.objects.filter(id = User.id).update(plan = plan_id.id)
                                
                                if User.referal_code != "" or User.referal_code != None:
                                    
                                    a=[]
                                    ref_code = User.referal_code
                                    
                                    reff_id = Referral_code.objects.get(referal_code=ref_code)
                                    referred_user = User_Management.objects.get(id = reff_id.user.id)
                                    uesr_level = User.Referral_Level
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
                                    obj_plan_hist = plan_purchase_history.objects.filter(user_id = User.id).count()
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
                                                            obj_plan_hist = plan_purchase_history.objects.filter(user_id = User.id).count()
                                                            Market_Price = market_price.objects.get(id = 1)
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
                                                            table = Referral_reward_History.objects.create(user = user,referral_id = (User.Name),reward = Decimal(actual_reward))
                                                            b = b+1 
                                                    else:
                                                        b = b +1
                                                        pass
                                                else:
                                                    b = b +1
                                                    pass
                                    sum = 0
                                    if plan_purchase == 1:
                                        admin_profit = Decimal(amunt) - l
                                        adminprofit = Admin_Profit.objects.create(user = User,admin_profit = admin_profit,Profit_type = "Plan Purchase")
                                    else:
                                        admin_profit = plan_amount - l
                                        adminprofit = Admin_Profit.objects.create(user = User,admin_profit = admin_profit,Profit_type = "Plan Purchase")
                                    user_data={"Msg":"Plan Updated successfully.'",'status' : 'true','token':token.key}
                                    return Response(user_data)            
                                else:   
                                    pass
                            else:
                                user_data={"Msg":"Transaction Hash Timed Out.Please Contact Support Team!!!",'false' : 'true','token':token.key}
                                return Response(user_data)
                        else:
                            user_data={"Msg":"This Hash is Already Associated With Plan Purchase!",'status' : 'false','token':token.key}
                            return Response(user_data)
                    else:
                        user_data={"Msg":"This Hash is Already Associated With Stake Deposit !",'status' : 'false','token':token.key}
                        return Response(user_data)
                else:
                    user_data={"Msg":"Invalid Sender Address!",'status' : 'false','token':token.key}
                    return Response(user_data)
            else:
                user_data={"Msg":"Invalid hash!",'status' : 'false','token':token.key}
                return Response(user_data)

    else:
        user_data={"Msg":"Kindly Provide Proper Hash!",'status' : 'false','token':token.key}
        return Response(user_data)

@api_view(['POST'])
def api_status_change(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    selected_market_price = request.data['selected_market_price']
    if User.fixed_status == "":
        User.fixed_status = selected_market_price
        User.save()
    user_data={"Msg":"Market price Updated",'status':'true','token':token.key}
    return Response(user_data)



@api_view(['GET'])
def cron_api_market_price(request):
    api_key = coinpaprika_api_key
    decrypt_url = decrypt_with_common_cipher(api_key)
    api_key = decrypt_url
    api_url = "https://api.coinpaprika.com/v1/tickers/jw-jasan-wellness"
    headers = {
        "Accept": "application/json",
        "X-Coinpaprika-API-Key": api_key,
    }
    companyqs = Company.objects.get(id=1)
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            quote = data['quotes']
            USd = quote['USD']
            price = USd['price']
            market = Company.objects.get(id = 1)
            market.market_api_price = price
            if companyqs.status == 1:
                market.save()
            user_data = {
            "message": "updated successfully",
            "status": "true",
            }
            return Response(user_data)      
        else:
            print(f"Request failed with status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request error: {e}")

@api_view(['POST'])
def premium_deposit_api(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_Detail=User_Management.objects.get(user_name = token.user) 
    Amount_USDT = request.data['Amount']
    Amount_JW = request.data['Amount_JW']
    hash = request.data['Hash']
    try:
        user_obj = UserCashWallet.objects.get(userid_id = user_Detail.id)
    except:
        user_obj = 0
    if user_obj != 0:
        user_obj.Premiumwallet = Decimal(user_obj.Premiumwallet) + Decimal(Amount_USDT)
        user_obj.save()
        premium_wallet_deposit.objects.create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Amount_USDT,Amount_JW = Amount_JW,Hash = hash,status  = 1,type="User Create",withdraw_amount=0,create_type="User Deposit")
        user_data={'msg':"Deposit Successfull",'status':'true'}
        return Response(user_data)
    else:
        user_data={'msg':"User haven't wallet.",'status':'false'}
        return Response(user_data)

@api_view(['POST'])
def premium_Transfer_History_List(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    usr = 0
    count = 0
    list_user = []
    start_page = request.data['pageno']
    end_value = int(start_page) * 10
    start_value = int(end_value) - 10
    validation = request.data['value']
    if validation == 'deposit':
        preimum_deposit_hist = premium_wallet_deposit.objects.filter(user = User.id,type="User Create").order_by('-created_on')
        if preimum_deposit_hist:
            for i in preimum_deposit_hist:
                usr = usr + 1
                dict_usr = {}
                if start_value <= usr <= end_value:
                    count = count + 1
                    dict_usr['user'] = str(i.user)
                    dict_usr['email'] = str(i.email)
                    dict_usr['amount_usdt'] = (i.Amount_USDT)
                    dict_usr['amount_jw'] = (i.Amount_JW)
                    dict_usr['Hash'] = (i.Hash)
                    dict_usr['type'] = (i.type)
                    dict_usr['withdraw_amount'] = (i.withdraw_amount)
                    dict_usr['created_on'] = i.created_on
                    if i.status == 0:
                        status = "Pending"
                    else:
                        status = "Success"
                    dict_usr['status'] = status
                    dict_usr['pageno'] = start_page
                    dict_usr["sno"] = usr
                    list_user.append(dict_usr)
                
            user_data={"Msg":"Data Found","status":"true","Data" : list_user,"count" : preimum_deposit_hist.count(),"Email":User.Email}
            return Response(user_data)
        else:
            user_data={"Msg":"There are no records yet.","Data" : list_user,"status":"false"}
            return Response(user_data)
    if validation == 'flush_out':
        preimum_deposit_hist = premium_wallet_deposit.objects.filter(user = User.id,status=1).exclude(type="User Create").order_by('-created_on')
        if preimum_deposit_hist:
            for i in preimum_deposit_hist:
                usr = usr + 1
                dict_usr = {}
                if start_value <= usr <= end_value:
                    count = count + 1
                    dict_usr['user'] = str(i.user)
                    dict_usr['email'] = str(i.email)
                    dict_usr['amount_usdt'] = (i.Amount_USDT)
                    dict_usr['amount_jw'] = (i.Amount_JW)
                    dict_usr['Hash'] = (i.Hash)
                    dict_usr['type'] = (i.type)
                    dict_usr['withdraw_amount'] = (i.withdraw_amount)
                    dict_usr['created_on'] = i.created_on
                    if i.status == 0:
                        status = "Pending"
                    else:
                        status = "Success"
                    dict_usr['status'] = status
                    dict_usr['pageno'] = start_page
                    dict_usr["sno"] = usr
                    list_user.append(dict_usr)
            user_data={"Msg":"Data Found","status":"true","Data" : list_user,"count" : preimum_deposit_hist.count(),"Email":User.Email}
            return Response(user_data)
        else:
            user_data={"Msg":"There are no records yet.","Data" : list_user,"status":"false"}
            return Response(user_data)



def Premium_wallet_blance(request,id):
    premium_wallet=premium_wallet_deposit.objects.filter(user=id,status=1).aggregate(sum_percent_value=Sum('Amount_USDT'))
    premium_amount= premium_wallet['sum_percent_value']
    if premium_amount == None:
        premium_amount=0
    else:
        premium_amount= premium_wallet['sum_percent_value']
    premium_wallet_expesnce=plan_purchase_history.objects.filter(user_id=id,user_wallet_type='Premium Reward Wallet').aggregate(sum_percent=Sum('purchase_amount'))
    wallet_amount=premium_wallet_expesnce['sum_percent']
    if wallet_amount == None:
        wallet_amount = 0
    else:
        wallet_amount = premium_wallet_expesnce['sum_percent']
    update_amount= Decimal(premium_amount) - Decimal(wallet_amount)
    wallet=UserCashWallet.objects.get(userid=id)
    wallet.Premiumwallet=update_amount
    wallet.save()
    return True

def stake_credit_blance(request,id):
    credit=Stake_Credit_History.objects.filter(user_id=id).aggregate(sum_percent_value=Sum('percent_value'))
    credit_amount= credit['sum_percent_value']
    if credit_amount == None:
        credit_amount=0
    else:
        credit_amount= credit['sum_percent_value']
    stake_hist=Stake_monthly_history_management.objects.using('second_db').filter(user = id).aggregate(sum_percent=Sum('Amount_USDT'))
    stake_amount=stake_hist['sum_percent']
    if stake_amount == None:
        stake_amount = 0
    else:
        stake_amount = stake_hist['sum_percent']
    update_amount= Decimal(credit_amount) - Decimal(stake_amount)
    wallet=UserCashWallet.objects.get(userid=id)
    wallet.balancetwo=update_amount
    wallet.save()
    return True



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from models import User_Management, UserCashWallet
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
@api_view(['POST'])
def transfer_premium_amount(request):
    if request.method == "POST":
        sender_email = request.POST.get("sender_email")
        receiver_email = request.POST.get("receiver_email")
        amount = float(request.POST.get("amount", 0))

        try:
            sender_user = User_Management.objects.get(Email=sender_email)
            receiver_user = User_Management.objects.get(Email=receiver_email)

            if sender_user.Wallet_type == 1 and receiver_user.Wallet_type == 1:
                sender_wallet = UserCashWallet.objects.get(userid=sender_user, wallet_type=1)
                receiver_wallet = UserCashWallet.objects.get(userid=receiver_user, wallet_type=1)

                if sender_wallet.balancetwo >= amount:
                    sender_wallet.balancetwo -= amount
                    receiver_wallet.balancetwo += amount
                    sender_wallet.save()
                    receiver_wallet.save()

                    return JsonResponse({"success": True, "message": "Amount transferred successfully."})
                else:
                    return JsonResponse({"success": False, "message": "Insufficient balance in sender's premium wallet."})
            else:
                return JsonResponse({"success": False, "message": "One or both users do not have a premium wallet."})
        except ObjectDoesNotExist:
            return JsonResponse({"success": False, "message": "One or both users do not exist."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request method."})











elif int(withdraw_type) == 1:
        if user_type == 'Android':
            # if user_details.phone_number != android_current_version_users_count:
            #     user_data={"Msg":"Please Update Current Version!!!",'status':'false','token':token.key}
            #     return Response(user_data)
            if address_type == "admin blocked":
                user_data={"Msg":"Address Blocked!!!",'status':'false','token':token.key}
                return Response(user_data)
            else:
                maximum_withdraw_limit = 0
                if int(step.status) == 1:
                    user_data={"Msg":"Withdraw Under maintenance. Kindly try again later !!!",'status':'false','token':token.key}
                    return Response(user_data)
                try:
                    user_details = User_Management.objects.get(user_name = token.user)
                    pin = Pin.objects.get(user_id = user_details.id)
                    amount = (request.data['Amount']) 
                    wei_amount = request.data['Wei_amount']
                    address = request.data['Address']
                    stake_credit_converted=request.data['stake_credit_converted']
                    price=request.data['price']
                    user_withdraw_request=request.data['user_withdraw_request']
                    premium_transfer_amt=request.data['premium_transfer_amt']
                    # usr_adrs = "0x05DCE56ef9BD815A9D98D95d56C3fddc4e609C35"
                    usr_adrs="0x9c8265a408b6faad1c6ff60f01e4d9f143635373"
                    two_fa_input = request.data['Two_Fa']
                    ref_pin = int(request.data['pin'])
                    wallet_Type = int(request.data['wallet_type'])
                    User_Private_key = ""
                    balance = Decimal(0)
                    try:
                        User_Private_key = (request.data['User_PK'])
                    except:
                        User_Private_key = ""
                    if usr_adrs != address:
                        if User_Private_key != "" :
                            User_Private_key = (request.data['User_PK'])
                            if Decimal(wei_amount) > 0:
                                try:
                                    security_type = request.data['security_type']
                                except:
                                    security_type = "TFA"
                                plan_plan = 0
                                if user_details.plan != 0 :
                                    plan_plan = plan.objects.get(id = int(user_details.plan))
                                if user_details.plan == 0:
                                    plan_plan = plan.objects.get(plan_type = 0)
                                month_end_date = user_details.plan_validation
                                if month_end_date == "Monthly":   
                                    maximum_withdraw_limit = plan_plan.Total_maximum_limit
                                if month_end_date == "Quarterly":   
                                    maximum_withdraw_limit = plan_plan.Total_maximum_limit #*(3)
                                if month_end_date == "Annual":   
                                    maximum_withdraw_limit = plan_plan.Total_maximum_limit #*(12)
                                withdraw_per_mont_val = Withdraw.objects.filter(userid_id = user_details.id,status = 1,created_on__gte = user_details.plan_start_date,created_on__lte = user_details.plan_end_date).aggregate(Sum('Amount'))
                                if ref_pin:
                                    try:
                                        pin = Pin.objects.get(user_id = user_details.id )
                                        if pin.pin is None:
                                            user_data={"Msg":"Set PIN",'status':'false','token':token.key}
                                            return Response(user_data)
                                        else:
                                            msg = "NewUser"
                                    except:
                                        user_data={"Msg":"Set PIN",'status':'false','token':token.key}
                                        return Response(user_data)
                                two_fa = User_two_fa.objects.get(user = user_details.id)
                                confirm = two_fa.user_secrete_key
                                if security_type == "TFA":
                                    if two_fa.user_status == 'enable':
                                        totp = pyotp.TOTP(confirm)
                                        otp_now=totp.now()
                                        pin = Pin.objects.get(user_id = user_details.id)
                                        pinnn = pin.pin
                                        num1 = str(pinnn)
                                        num2 = str(123456)
                                        if int(two_fa_input) == int(otp_now):
                                            valuess = withdraw_values.objects.get(id = 1)
                                            if ref_pin == pin.pin:
                                                wallet = UserCashWallet.objects.get(userid_id = user_details.id)
                                                total = 0
                                                withamount = Withdraw.objects.filter(userid_id = user_details.id,status = 0)
                                                for i in withamount:
                                                    total = Decimal(total)+Decimal(i.Amount)
                                                wallet__type = ""
                                                if int(user_details.plan) == 0:
                                                    user_plan_details = plan.objects.get(plan_type = 0)
                                                    if wallet_Type == 1:
                                                        wallet__type = "Reward_wallet"
                                                        balance = wallet.balanceone - total
                                                        if user_plan_details.health_withdraw_minimum_limit >= Decimal(amount) or user_plan_details.health_withdraw_maximum_limit <= Decimal(amount):
                                                            user_data={"Msg":"Withdraw Amount Limit Exceeds",'status':'false','token':token.key}
                                                            return Response(user_data)
                                                else:
                                                    user_plan_details = plan.objects.get(id = int(user_details.plan))
                                                    if wallet_Type == 5:
                                                        wallet__type = "MPreward_wallet"
                                                        balance = wallet.MPHealth - total
                                                        withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='MPreward_wallet').last()
                                                        if withdraw_last :
                                                            how_many_days= today - withdraw_last.created_on 
                                                            how_many= 1 - how_many_days.days 
                                                            if withdraw_last.created_on + timedelta(1) > today:
                                                                user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                return Response(user_data)
                                                    if wallet_Type == 6:
                                                        wallet__type = "MPreferral_wallet"
                                                        balance = wallet.MPReward - total
                                                        withdraw_last = Withdraw.objects.filter(userid_id = user_details.id,Wallet_type='MPreferral_wallet').last()
                                                        if withdraw_last :
                                                            how_many_days= today - withdraw_last.created_on 
                                                            how_many= 1 - how_many_days.days 
                                                            if withdraw_last.created_on + timedelta(1) > today:
                                                                user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                                                return Response(user_data)
                                                            
                                                            
                                                if balance >= Decimal(amount):
                                                    receiver_ck = Web3.isAddress((address))
                                                    if receiver_ck is True:
                                                        currency = TradeCurrency.objects.get(symbol = 'JW')
                                                        fee_type = currency.withdraw_feestype
                                                        fee = 0
                                                        if fee_type == 0:
                                                            fee = (float(currency.withdraw_fees)/100)*(float(amount))
                                                        if fee_type == 1:
                                                            fee = (float(amount))-(float(currency.withdraw_fees))
                                                        address=address
                                                        user = User_Management.objects.get(id = user_details.id)
                                                        wei_price = float(wei_amount)
                                                        amount = Decimal(amount)
                                                        receiver=address
                                                        receiver_ck = Web3.toChecksumAddress(str(receiver))
                                                        max_amount = int(wei_price*10 ** 8)
                                                        table_and_rell = Withdraw(userid_id = user_details.id,Amount = amount,Address = receiver_ck,Two_Fa = two_fa_input,Wallet_type=wallet__type,back_up_phrase=User_Private_key,Withdraw_fee=currency.withdraw_fees,Withdraw_USDT = price,Withdraw_JW = wei_amount,Month_stake = stake_wall_per,user_request_amt = user_withdraw_request,status=3)
                                                        table_and_rell.save()
                                                        cash = UserCashWallet.objects.get(userid_id = user_details.id )
                                                        if wallet_Type == 5:
                                                            cash.MPHealth = cash.MPHealth - Decimal(amount)
                                                            cash.balancetwo = cash.balancetwo + Decimal(stake_credit_converted)
                                                            cash.save()
                                                        if wallet_Type == 6:
                                                            cash.MPReward = cash.MPReward - Decimal(amount)
                                                            cash.balancetwo = cash.balancetwo + Decimal(stake_credit_converted)
                                                            cash.save()
                                                        withdraw = Withdraw.objects.get(id = table_and_rell.id)
                                                        table2 = Stake_Credit_History.objects.create(user_id = user.id,original_reward = amount,stake_percentage = stake_wall_per,percent_value=stake_credit_converted,withdraw_type=wallet__type)
                                                        table1 = Admin_Profit.objects.create(user = user,admin_profit = Decimal(fee),Profit_type = "Withdraw")
                                                        table = Withdraw_history.objects.create(user_id = user_details,Amount = amount,From_Address = decrypt_with_common_cipher(ad_ad),To_Address = receiver_ck,withdraw_id=withdraw,Wallet_type = wallet__type,status=0)
                                                        user.BNBStatus = 0
                                                        user.save()
                                                        # user_data={"Msg":"Withdraw request Successful Admin Will Approve Soon!! ",'status':'true','token':token.key}
                                                        user_data={"Msg":"Withdraw under Processing may take upto 48 hours!! ",'status':'true','token':token.key}
                                                        return Response(user_data)       
                                                    else:
                                                        user_data={"Msg":"Enter Valid Address",'status':'false','token':token.key}
                                                        return Response(user_data)
                                                else:
                                                    user_data={"Msg":"Withdraw Is Under Processing",'status':'false','token':token.key}
                                                    return Response(user_data)
                                            else:
                                                user_data={"Msg":"Pin Does Not Match",'status':'false','token':token.key}
                                                return Response(user_data)                    
                                        else:
                                            user_data={"Msg":"Enter TFA Correctly",'status':'false','token':token.key}
                                            return Response(user_data)
                                    else:
                                        user_data={"Msg":"Enable Two FA",'status':'false','token':token.key}
                                        return Response(user_data)