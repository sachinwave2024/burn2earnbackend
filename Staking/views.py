

from calendar import month
from decimal import Decimal
from email import contentmanager
import json
from operator import and_
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic import TemplateView,View
from django.shortcuts import render,get_object_or_404,redirect
from API.models import Admin_Profit,premium_wallet_deposit, user_address_trust_wallet,Contract_address, Pin, Referral_code, UserCashWallet, Withdraw, Withdraw_history, plan, plan_purchase_history, withdraw_values,referral_level,market_price
from Staking.models import Stake_Monthly_Claim_History, Stake_history_management, Stake_market_price, Stake_monthly_history_management, Stake_referral_management, Stake_referral_reward_table, internal_transfer_admin_management, stake_claim_reward_history, stake_credit_claim_history, stake_credit_reward_history, stake_deposit_management, stake_reward_history, stake_wallet_management, staking_admin_management,internal_transfer_history, staking_monthly_admin_management,new_stake_deposit_management,stake_purchase_history,newstake_Referral_reward_History,newstakeclaim_History

from Staking.tables import Stake_Plan_Table, Stake_Referral_Table
from Staking.forms import Stake_Plan_Form, Stake_Referral_Form
from Staking.models import stake_wallet_management, staking_admin_management,internal_transfer_history,internal_transfer_admin_management,stake_claim_table

from Staking.tables import Internal_Transfer_Table, Internal_TransferFilter, Internal_TransferSearch_Form, Stake_Plan_Table
from Staking.forms import Stake_Plan_Form
from company.models import Company
from jason_wellness import settings
import pyotp

import requests

from django.db import transaction


from datetime import date,timedelta
import datetime
import time
from django.contrib import messages


from django.http.response import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from Staking.serializers import user_Active_Stake_Serializer ,stake_Referral_History_Serializers
from trade_admin_auth.models import Registration_otp, User_Management, User_two_fa


from django_tables2 import RequestConfig
from crispy_forms.layout import Submit,Reset
from django.db.models import Max

from django.db.models import Q,F,Func,Value
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from trade_admin_auth.contract import token_abi,Main_abi,token_address,main_address,admin_address_privatekey
from trade_currency.models import TradeCurrency
from django.db.models import Sum


from django.utils.decorators import method_decorator
from trade_admin_auth.mixins import check_group
from trade_master.models import Stake_Credit_History


# Edit stake month
@check_group("Staking Management")
def Edit_Staking_Plan(request):
  context = {}
  context['Title'] = 'Staking Management'
  obj_stake_manage = staking_admin_management.objects.using('second_db').get(id = 1)
  plan_obj = plan.objects.filter(status = 0).filter(~Q(plan_type = 0))
  select_plan = plan.objects.get(id = obj_stake_manage.eligible_plan)
  context['obj_stake_manage'] = obj_stake_manage
  context['plan_obj'] = plan_obj
  context['select_plan'] = select_plan
  if request.method == "POST":
    stake_period = request.POST["stake_period"]
    reward_percent = request.POST["reward_percent"]
    minimum_stake = request.POST["minimum_stake"]
    maximum_stake = request.POST["maximum_stake"]
    status = request.POST["status"]
    with_status = request.POST["withdraw_status"]
    min_withdraw = request.POST["minimum_withdraw"]
    max_withdraw = request.POST["maximum_withdraw"]
    min_with_referral = request.POST["minimum_withdraw_referal"]
    max_with_referral = request.POST["maximum_withdraw_referal"]
    eligible_plan = request.POST["eligible_plan"]
    stake_wallet_percentage = request.POST["stake_wallet_percentage"]
    withdraw_wallet_percentage = request.POST["withdraw_wallet_percentage"]
    stake_withdraw_transaction_fee = request.POST["stake_withdraw_transaction_fee"]
    if stake_period != "" and reward_percent != "" and minimum_stake != "":
      staking_admin_management.objects.using('second_db').filter(id = 1).update(stake_period = stake_period,reward_percent = reward_percent,minimum_stake = minimum_stake,maximum_stake = maximum_stake,status = status,withdraw_status = with_status,minimum_withdraw = min_withdraw,minimum_withdraw_referal = min_with_referral,eligible_plan=eligible_plan,stake_wallet_percentage=stake_wallet_percentage,withdraw_wallet_percentage=withdraw_wallet_percentage,stake_withdraw_transaction_fee=stake_withdraw_transaction_fee,maximum_withdraw_referal=max_with_referral,maximum_withdraw=max_withdraw)
      messages.add_message(request, messages.SUCCESS, 'Successfully updated.')
      return HttpResponseRedirect('/stake/Edit_Staking_Plan/1/')
    else:
      messages.add_message(request, messages.ERROR, 'Enter required field.')
      return HttpResponseRedirect('/stake/Edit_Staking_Plan/1/')
  return render(request,'stake/edit_staking_plan.html',context)



#list stake Referral management

class List_Staking_Referral(ListView):
    model = Stake_referral_management
    template_name = 'trade_master/generic_list_add.html'
    def get_queryset(self, **kwargs):
      return Stake_referral_management.objects.using('second_db').all().order_by('-id')
    
    def get_context_data(self,**kwargs):
        context=super(List_Staking_Referral, self).get_context_data(**kwargs)               
        context['Title'] = 'Staking Referral Management'
        adminactivity_qs = Stake_referral_management.objects.using('second_db').all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        Adminactivitytable = Stake_Referral_Table(adminactivity_qs)
        context['table'] = Adminactivitytable
        context['add_title'] ='Add Stake Referral'
        context['Btn_url'] = 'staking:Add_Staking_Referral'
        return context
    
    @method_decorator(check_group("Staking Management"))
    def dispatch(self, *args, **kwargs):
      return super(List_Staking_Referral, self).dispatch(*args, **kwargs)


#Add stake Referral Management

class Add_Staking_Referral(CreateView):
    model = Stake_referral_management
    form_class = Stake_Referral_Form
    template_name = 'stake/add_referral_stake.html'   
    def get_context_data(self, **kwargs):
       context = super(Add_Staking_Referral, self).get_context_data(**kwargs)
       context['Title'] = 'Add Referral Level'
       context['Btn_url'] = 'staking:List_Staking_Referral'
       plan_object = Stake_referral_management.objects.using('second_db').all()
       obj = plan_object.aggregate(Max('self_stake_Amount_range'))
       context['plan_object'] = obj
       return context
    
    @method_decorator(check_group("Staking Management"))
    def dispatch(self, *args, **kwargs):
      return super(Add_Staking_Referral, self).dispatch(*args, **kwargs)
    
    @transaction.atomic
    def form_valid(self, form):
        adminactivity_qs = Stake_referral_management.objects.using('second_db').all().order_by('-id')
        if adminactivity_qs:
            for i in adminactivity_qs:
                if i.levels == form.instance.levels: 
                    messages.add_message(self.request, messages.ERROR, 'Referral Level Already Exists')
                    return HttpResponseRedirect('/stake/List_Staking_Referral/')
        if form.instance.levels != None and form.instance.self_stake_Amount != None and form.instance.self_stake_Amount_range != None and form.instance.first_level_stake != None and form.instance.secound_level_stake != None and form.instance.status != None:
            form.instance.created_on   = datetime.datetime.now()
            form.instance.modified_on   = datetime.datetime.now()
            ins = form.save(commit = False)
            ins.save(using = 'second_db')
            messages.success(self.request, 'Referral Level created successfully.')
            return HttpResponseRedirect('/stake/List_Staking_Referral/')
        else:
            messages.error(self.request, 'Enter required field')
            return HttpResponseRedirect('/stake/Add_Staking_Referral/')


#Edit Stake Referral Management
@check_group("Staking Management")
def Edit_Staking_Referral(request,id):
  context = {}
  context['Title'] = 'Edit Referral Management'
  obj_stake_manage = Stake_referral_management.objects.using('second_db').get(id = id)
  context['obj_stake_manage'] = obj_stake_manage
  if request.method == "POST":
    levels = request.POST["levels"]
    self_stake_Amount = request.POST["self_stake_Amount"]
    self_stake_Amount_range = request.POST["self_stake_Amount_range"]
    first_level_stake = request.POST["first_level_stake"]
    secound_level_stake = request.POST["secound_level_stake"]
    status = request.POST["status"]
    if levels != "" and self_stake_Amount != "" and self_stake_Amount_range != "" and first_level_stake != "" and secound_level_stake != "" and status != "":
      Stake_referral_management.objects.using('second_db').filter(id = id).update(levels = levels,self_stake_Amount = self_stake_Amount,self_stake_Amount_range = self_stake_Amount_range,first_level_stake = first_level_stake,secound_level_stake = secound_level_stake,status = status)
      messages.add_message(request, messages.SUCCESS, 'Successfully updated.')
      return HttpResponseRedirect('/stake/List_Staking_Referral/')
    else:
      messages.add_message(request, messages.ERROR, 'Enter required field.')
      return HttpResponseRedirect('/stake/List_Staking_Referral/')
  return render(request,'stake/edit_referral_stake.html',context)


# Delete Referral Stake
class Delete_Referral_stake(View):
    def get(self, request, *args, **kwargs):
        pkey =  (self.kwargs['pk'])
        user_qs = get_object_or_404(Stake_referral_management, pk=pkey)
        
        try:
            get_user_id = Stake_referral_management.objects.using('second_db').get(id=pkey)
           
            user_qs.delete()
        except:
            user_qs.delete()

        messages.add_message(request, messages.SUCCESS, 'Successfully deleted.') 
        return HttpResponseRedirect('/stake/List_Staking_Referral/')


# Internal transfer fees update function
@check_group("Internal Transfer")
def InternalTransferFeesUpdate(request):
    context = {}
    context["Title"] = "Internal Transfer Fees Update"
    obj_internal = internal_transfer_admin_management.objects.using('second_db').get(id = 1)
    context["obj_internal"] = obj_internal
    if request.method == "POST":
        fees = request.POST["fees"]
        health_wall = request.POST.get("health_wallet")
        ref_wall = request.POST.get("ref_wallet")
        if fees != "":
            if health_wall != None:
                health_wall = True
            else:
                health_wall = False
            if ref_wall != None:
                ref_wall = True
            else:
                ref_wall = False
            internal_transfer_admin_management.objects.using('second_db').filter(id = 1).update(transaction_fees = fees,health_wallet = health_wall,referral_wallet = ref_wall,modified_on = datetime.datetime.now())
            messages.add_message(request, messages.SUCCESS, 'Successfully updated.')
            return HttpResponseRedirect('/stake/internal_transfer_fees_update/1/')
        else:
            messages.add_message(request, messages.ERROR, 'Enter required field.')
            return HttpResponseRedirect('/stake/internal_transfer_fees_update/1/')

    return render(request,'stake/inertnal_transfer_fees_update.html',context)


# Internla transfer admin side history listing
class List_Internal_Transfer_History(ListView):
    model = internal_transfer_history
    template_name = 'stake/internal_transfer_history_list.html'
    def get_queryset(self, **kwargs):
      return internal_transfer_history.objects.using('second_db').all().order_by('-id')
    
    def get_context_data(self,**kwargs):
        context=super(List_Internal_Transfer_History, self).get_context_data(**kwargs)
        context['Title'] = 'Internal Transfer History'
        adminactivity_qs = internal_transfer_history.objects.using('second_db').all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        user_count = internal_transfer_history.objects.using('second_db').all().count()
        context['user_count'] = user_count
        filter = Internal_TransferFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        filter.form.helper = Internal_TransferSearch_Form()
        filter.form.helper.add_input(Submit('submit', 'Search',css_class="btn btn-default"))
        
        filter.form.helper.add_input(Reset('Reset Search','Reset Search',css_class="btn btn-default",css_id='reset-search'))
        Adminactivitytable = Internal_Transfer_Table(filter.qs)
        RequestConfig(self.request, paginate={'per_page': 10}).configure(Adminactivitytable)
        context['table'] = Adminactivitytable
        context['filter'] = filter
        context['add_title'] ='Add BlockIp'
        context['Btn_url'] = 'staking:List_Internal_Transfer_History'
        return context
    
    @method_decorator(check_group("Internal Transfer"))
    def dispatch(self, *args, **kwargs):
      return super(List_Internal_Transfer_History, self).dispatch(*args, **kwargs)



import datetime
from decimal import Decimal
# Internal transfer API
@api_view(['POST'])
def Internal_Transfer(request):
  Token_header = request.headers['Token']
  token = Token.objects.get(key = Token_header)
  user_Detail=User_Management.objects.get(user_name = token.user)
  frm_wallet = request.data["from_wallet"]
  to_wallet = request.data["to_wallet"]
  actual_amttt = request.data["actual_amount"]
  fee = request.data["fees"]
  amount = request.data["Amount"]
  convert_amount = request.data["converted_usdt"]
  # Convert act_amount to Decimal
  actual_amttt = Decimal(actual_amttt)
  actual_amt = actual_amttt - (Decimal('0.10') * actual_amttt)
  # fee_deduct = Decimal('0.10') * actual_amttt
  today=datetime.now()
  user_plan=plan.objects.get(id=user_Detail.plan)
  if user_plan.withdraw_status == 0:
      user_data={"msg":"This Plan is not eligible to Interal Transfer",'status':'false','token':token.key}
      return Response(user_data)
  obj_wall_check = internal_transfer_admin_management.objects.using('second_db').values('health_wallet','referral_wallet').get(id = 1)
  try:
    obj_stake_wall = stake_wallet_management.objects.using('second_db').get(user = user_Detail.id)
  except:
    obj_stake_wall = 0
  try:
      obj_wallet = UserCashWallet.objects.get(userid = user_Detail)
  except:
      obj_wallet = 0
  if user_Detail.plan == 0:
    obj_plan = User_Management.objects.values('Health_Withdraw_min_value','Health_Withdraw_max_value','Referral_Withdraw_min_value','Referral_Withdraw_max_value').get(plan_type = 0)
  else:
    obj_plan = User_Management.objects.values('Health_Withdraw_min_value','Health_Withdraw_max_value','Referral_Withdraw_min_value','Referral_Withdraw_max_value').get(user_name = token.user)
  
  obj_sum_transfer = internal_transfer_history.objects.using('second_db').filter(user = user_Detail.id).aggregate(Sum('actual_amount')) 

  obj_check_transfer = internal_transfer_history.objects.using('second_db').values('user','created_on','from_wallet').filter(user = user_Detail.id,status = 0).last()

  obj_check_withdraw = Withdraw_history.objects.values('user_id','created_on','Wallet_type').filter(user_id = user_Detail).last()

  health_amt = obj_wallet.balanceone
  ref_amt = obj_wallet.referalincome
  if frm_wallet != "" and to_wallet != "" and actual_amt != "" and fee != "" and amount != "":
    if frm_wallet == "Reward_wallet":
      try:
        withdraw_last = internal_transfer_history.objects.using('second_db').filter(user = user_Detail.id,from_wallet="Reward_wallet").last()
        if withdraw_last :
            how_many_days= today - withdraw_last.created_on 
            how_many= 30 - how_many_days.days 
            if withdraw_last.created_on + timedelta(30) > today:
            # if withdraw_last.created_on + timedelta(hours=24) > today:
                user_data={"msg":"Your Transfer Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                # user_data={"msg":"Your Transfer Limit Is Over!!! Try again Later:",'status':'false','token':token.key}
                return Response(user_data)
      except:
          withdraw_last = ""
      if obj_wall_check['health_wallet'] == 1:
        if health_amt >= Decimal(actual_amttt):
          # if obj_stake_wall != 0:
            if obj_sum_transfer['actual_amount__sum'] != None or obj_check_withdraw != None:
              if obj_sum_transfer['actual_amount__sum'] != None:
                if obj_check_withdraw != None:                 
                    if obj_plan['Health_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Health_Withdraw_max_value']:
                      # if obj_check_transfer or obj_check_withdraw:
                        # if obj_check_transfer['created_on'] + timedelta(hours=24) > datetime.datetime.now(): 
                      
                        # else:
                          diff_amt = Decimal(health_amt) - Decimal(actual_amttt)
                          obj_wallet.balanceone = diff_amt
                          obj_wallet.save()
                          # add_amt = Decimal(obj_stake_wall.stake_Wallet) + Decimal(amount)
                          # obj_stake_wall.stake_Wallet = add_amt
                          # obj_stake_wall.save(using='second_db')
                          new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="health_wallet")
                          # Withdraw(userid_id = user_Detail.id,Amount = amount,Address = 'internal_transfer_premium',Wallet_type=frm_wallet,back_up_phrase="0",created_on = datetime.datetime.now(),modified_on = datetime.datetime.now())
                          internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amttt,converted_amount=0,fees = 10,amount = 0,created_on = datetime.now(),modified_on = datetime.now(),status = 0)
                          user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                          return Response(user_data)
                        
                          
                      # else:
                      #   user_data={"msg":"No records found...!!!",'status':'false','token':token.key}
                      #   return Response(user_data)
                    else:
                      # user_data={"msg":"Limit exceeds...!!!",'status':'false','token':token.key,'Data':[obj_plan]}
                      user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                      return Response(user_data) 
                else:
                  # if obj_check_transfer['created_on'] + timedelta(hours=24) < datetime.datetime.now():
                    if obj_plan['Health_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Health_Withdraw_max_value']:
                      diff_amt = Decimal(health_amt) - Decimal(actual_amttt)
                      obj_wallet.balanceone = diff_amt
                      obj_wallet.save()
                      # add_amt = Decimal(obj_stake_wall.stake_Wallet) + Decimal(amount)
                      # obj_stake_wall.stake_Wallet = add_amt
                      # obj_stake_wall.save(using='second_db')
                      new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="health_wallet")
                      # Withdraw(userid_id = user_Detail.id,Amount = amount,Address = 'internal_transfer_premium',Wallet_type=frm_wallet,back_up_phrase="0",created_on = datetime.datetime.now(),modified_on = datetime.datetime.now())
                      internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amttt,converted_amount=0,fees = 10,amount = 0,created_on = datetime.now(),modified_on = datetime.now(),status = 0)
                      # internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amt,fees = fee,converted_amount=convert_amount,amount = amount,created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 0)
                      user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                      return Response(user_data)
                    else:
                      # user_data={"msg":"Limit exceeds..!!",'status':'false','token':token.key,'Data':[obj_plan]}
                      user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                      return Response(user_data) 
                  # else:
                  #   user_data={"msg":"Your Transfer Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                  #   return Response(user_data)
              else:
                # if obj_check_withdraw['created_on'] + timedelta(hours=24) < datetime.datetime.now():
                  if obj_plan['Health_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Health_Withdraw_max_value']:
                    diff_amt = Decimal(health_amt) - Decimal(actual_amttt)
                    obj_wallet.balanceone = diff_amt
                    obj_wallet.save()
                    # add_amt = Decimal(obj_stake_wall.stake_Wallet) + Decimal(amount)
                    # obj_stake_wall.stake_Wallet = add_amt
                    # obj_stake_wall.save(using='second_db')
                    new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="health_wallet")
                    # Withdraw(userid_id = user_Detail.id,Amount = amount,Address = 'internal_transfer_premium',Wallet_type=frm_wallet,back_up_phrase="0",created_on = datetime.datetime.now(),modified_on = datetime.datetime.now())
                    internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amttt,converted_amount=0,fees = 10,amount = 0,created_on = datetime.now(),modified_on = datetime.now(),status = 0)
                    # internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amt,fees = fee,converted_amount=convert_amount,amount = amount,created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 0)
                    user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                    return Response(user_data)
                  else:
                    # user_data={"msg":"Limit exceeds..!!",'status':'false','token':token.key,'Data':[obj_plan]}
                    user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                    return Response(user_data) 
                # else:
                #   user_data={"msg":"Your Transfer Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                #   return Response(user_data)
            else:
              # if obj_check_withdraw['Wallet_type'] != 'Reward_wallet' or obj_check_withdraw['created_on'] + timedelta(hours=24) < datetime.datetime.now():
                if obj_plan['Health_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Health_Withdraw_max_value']:
                  diff_amt = Decimal(health_amt) - Decimal(actual_amttt)
                  obj_wallet.balanceone = diff_amt
                  obj_wallet.save()
                  # add_amt = Decimal(obj_stake_wall.stake_Wallet) + Decimal(amount)
                  # obj_stake_wall.stake_Wallet = add_amt
                  # obj_stake_wall.save(using='second_db')
                  new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="health_wallet")
                  # Withdraw(userid_id = user_Detail.id,Amount = amount,Address = 'internal_transfer_premium',Wallet_type=frm_wallet,back_up_phrase="0",created_on = datetime.datetime.now(),modified_on = datetime.datetime.now())
                  internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amttt,converted_amount=0,fees = 10,amount = 0,created_on = datetime.now(),modified_on = datetime.now(),status = 0)
                  # internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amt,fees = fee,converted_amount=convert_amount,amount = amount,created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 0)
                  user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                  return Response(user_data)
                else:
                  # user_data={"msg":"Limit exceeds..!!",'status':'false','token':token.key,'Data':[obj_plan]}
                  user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                  return Response(user_data) 
              # else:
              #   user_data={"Msg":"Your Transfer Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
              #   return Response(user_data)
              

          # else:
          #   user_data={"msg":"This user haven't wallet",'status':'false','token':token.key}
          #   return Response(user_data)
        else:
          user_data={"msg":"Insufficient balance",'status':'false','token':token.key,"balance" : health_amt}
          return Response(user_data)
          
      else:
        user_data={"msg":"Currently this wallet is not available...",'status':'false','token':token.key}
        return Response(user_data) 
    elif frm_wallet == "Referral_wallet":
      try:
        withdraw_last = internal_transfer_history.objects.using('second_db').filter(user = user_Detail.id,from_wallet="Referral_wallet").last()
        if withdraw_last :
            how_many_days= today - withdraw_last.created_on 
            how_many= 30 - how_many_days.days 
            # if withdraw_last.created_on + timedelta(30) > today:
            if withdraw_last.created_on + timedelta(hours=24) > today:
                # user_data={"msg":"Your Transfer Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                user_data={"msg":"Your Transfer Limit Is Over!!! Try again Later:",'status':'false','token':token.key}
                return Response(user_data)
      except:
          withdraw_last = ""
      if obj_wall_check['referral_wallet'] == 1:
        if ref_amt >= Decimal(actual_amttt):
            # if obj_stake_wall != 0:
              
              if obj_sum_transfer['actual_amount__sum'] != None or obj_check_withdraw != None:
                
                if obj_check_withdraw != None:
                  # if obj_check_withdraw['wallet_type'] 
                    # if (obj_check_withdraw['created_on'] + timedelta(hours=24) < datetime.datetime.now() and obj_check_transfer['created_on'] + timedelta(hours=24) < datetime.datetime.now()):
                      if obj_plan['Referral_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Referral_Withdraw_max_value']:
                        # if obj_check_transfer['created_on'] + timedelta(hours=24) > datetime.datetime.now() or obj_check_withdraw['created_on'] + timedelta(hours=24) > datetime.datetime.now(): 
                          
                        # else:
                          diff_amt = Decimal(ref_amt) - Decimal(actual_amttt)
                          obj_wallet.referalincome = diff_amt
                          obj_wallet.save()
                          # add_amt = Decimal(obj_stake_wall.stake_Refferal_Wallet) + Decimal(amount)
                          # obj_stake_wall.stake_Wallet = add_amt
                          # obj_stake_wall.save(using='second_db')
                          new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="referral_wallet")
                          # Withdraw(userid_id = user_Detail.id,Amount = amount,Address = 'internal_transfer_premium',Wallet_type=frm_wallet,back_up_phrase="0",created_on = datetime.datetime.now(),modified_on = datetime.datetime.now())
                          internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amttt,converted_amount=0,fees = 10,amount = 0,created_on = datetime.now(),modified_on = datetime.now(),status = 0)
                          # internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amt,fees = fee,converted_amount=convert_amount,amount = amount,created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 0)
                          user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                          return Response(user_data)
                      else:
                        # user_data={"msg":"Limit exceeds...!!!",'status':'false','token':token.key,'Data':[obj_plan]}
                        user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                        return Response(user_data) 
                    # else:
                    #   user_data={"msg":"Your Transfer Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                    #   return Response(user_data)
                else:
                  # if obj_check_transfer['created_on'] + timedelta(hours=24) < datetime.datetime.now():
                    if obj_plan['Referral_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Referral_Withdraw_max_value']:
                      # diff_amt = Decimal(health_amt) - Decimal(actual_amt)
                      # obj_wallet.balanceone = diff_amt
                      # obj_wallet.save()
                      diff_amt = Decimal(ref_amt) - Decimal(actual_amttt)
                      obj_wallet.referalincome = diff_amt
                      obj_wallet.save()
                      # add_amt = Decimal(obj_stake_wall.stake_Wallet) + Decimal(amount)
                      # obj_stake_wall.stake_Wallet = add_amt
                      # obj_stake_wall.save(using='second_db')
                      new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="referral_wallet")
                      # Withdraw(userid_id = user_Detail.id,Amount = amount,Address = 'internal_transfer_premium',Wallet_type=frm_wallet,back_up_phrase="0",created_on = datetime.datetime.now(),modified_on = datetime.datetime.now())
                      internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amttt,converted_amount=0,fees = 10,amount = 0,created_on = datetime.now(),modified_on = datetime.now(),status = 0)
                      # internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amt,fees = fee,converted_amount=convert_amount,amount = amount,created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 0)
                      user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                      return Response(user_data)
                    else:
                      # user_data={"msg":"Limit exceeds..!!",'status':'false','token':token.key,'Data':[obj_plan]}
                      user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                      return Response(user_data) 
                  # else:
                  #   user_data={"msg":"Your Transfer Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                  #   return Response(user_data)
                    
              else:
                # if obj_check_withdraw['Wallet_type'] != 'Referral_wallet' or obj_check_withdraw['created_on'] + timedelta(hours=24) < datetime.datetime.now():
                if obj_plan['Referral_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Referral_Withdraw_max_value']:
                  diff_amt = Decimal(ref_amt) - Decimal(actual_amttt)
                  obj_wallet.referalincome = diff_amt
                  obj_wallet.save()
                  # add_amt = Decimal(obj_stake_wall.stake_Wallet) + Decimal(amount)
                  # obj_stake_wall.stake_Wallet = add_amt
                  # obj_stake_wall.save(using='second_db')
                  new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="referral_wallet")
                  # Withdraw(userid_id = user_Detail.id,Amount = amount,Address = 'internal_transfer_premium',Wallet_type=frm_wallet,back_up_phrase="0",created_on = datetime.datetime.now(),modified_on = datetime.datetime.now())
                  internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amttt,converted_amount=0,fees = 10,amount = 0,created_on = datetime.now(),modified_on = datetime.now(),status = 0)
                  # internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amt,fees = fee,amount = amount,converted_amount=convert_amount,created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 0)
                  user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                  return Response(user_data)
                else:
                  # user_data={"msg":"Limit exceeds..!!",'status':'false','token':token.key,'Data':[obj_plan]}
                  user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                  return Response(user_data)
                # else:
                #   user_data={"Msg":"Your Transfer Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                #   return Response(user_data)
              
            # else:
            #     user_data={"msg":"This user haven't wallet",'status':'false','token':token.key}
            #     return Response(user_data)
        else:
            user_data={"msg":"Insufficient balance",'status':'false','token':token.key,"balance" : ref_amt}
            return Response(user_data)
        # else:
        #   user_data={"msg":"Limit exceeds...!!!",'status':'false','token':token.key}
        #   return Response(user_data)
      else:
        user_data={"msg":"Currently this wallet is not available...",'status':'false','token':token.key}
        return Response(user_data) 
    else:
        user_data={"msg":"Transfer your balance either health to stake wallet or referral to premium wallet.",'status':'false','token':token.key}
        return Response(user_data)
  else:
      user_data={"msg":"Something went wrong",'status':'false','token':token.key}
      return Response(user_data)


import datetime
from decimal import Decimal
# Internal transfer API
@api_view(['POST'])
def Internal_Transfer_premium(request):
  Token_header = request.headers['Token']
  token = Token.objects.get(key = Token_header)
  user_Detail=User_Management.objects.get(user_name = token.user)
  frm_wallet = request.data["from_wallet"]
  to_wallet = request.data["to_wallet"]
  actual_amttt = request.data["actual_amount"]
  fee = request.data["fees"]
  amount = request.data["Amount"]
  convert_amount = request.data["converted_usdt"]
  # Convert act_amount to Decimal
  actual_amttt = Decimal(actual_amttt)
  actual_amt = actual_amttt - (Decimal('0.10') * actual_amttt)
  # fee_deduct = Decimal('0.10') * actual_amttt
  today=datetime.now()
  user_plan=plan.objects.get(id=user_Detail.plan)
  if user_plan.withdraw_status == 0:
      user_data={"msg":"This Plan is not eligible to Interal Transfer",'status':'false','token':token.key}
      return Response(user_data)
  obj_wall_check = internal_transfer_admin_management.objects.using('second_db').values('health_wallet','referral_wallet').get(id = 1)
  try:
    obj_stake_wall = stake_wallet_management.objects.using('second_db').get(user = user_Detail.id)
  except:
    obj_stake_wall = 0
  try:
      obj_wallet = UserCashWallet.objects.get(userid = user_Detail)
  except:
      obj_wallet = 0
  if user_Detail.plan == 0:
    obj_plan = User_Management.objects.values('Health_Withdraw_min_value','Health_Withdraw_max_value','Referral_Withdraw_min_value','Referral_Withdraw_max_value').get(plan_type = 0)
  else:
    obj_plan = User_Management.objects.values('Health_Withdraw_min_value','Health_Withdraw_max_value','Referral_Withdraw_min_value','Referral_Withdraw_max_value').get(user_name = token.user)
  
  obj_sum_transfer = internal_transfer_history.objects.using('second_db').filter(user = user_Detail.id).aggregate(Sum('actual_amount')) 

  obj_check_transfer = internal_transfer_history.objects.using('second_db').values('user','created_on','from_wallet').filter(user = user_Detail.id,status = 0).last()

  obj_check_withdraw = Withdraw_history.objects.values('user_id','created_on','Wallet_type').filter(user_id = user_Detail).last()

  health_amt = obj_wallet.balanceone
  ref_amt = obj_wallet.referalincome
  if frm_wallet != "" and to_wallet != "" and actual_amt != "" and fee != "" and amount != "":
    if frm_wallet == "Reward_wallet":
      try:
        withdraw_last = internal_transfer_history.objects.using('second_db').filter(user = user_Detail.id,from_wallet="Reward_wallet").last()
        if withdraw_last :
            how_many_days= today - withdraw_last.created_on 
            how_many= 30 - how_many_days.days 
            if withdraw_last.created_on + timedelta(30) > today:
            # if withdraw_last.created_on + timedelta(hours=24) > today:
                user_data={"msg":"Your Transfer Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                # user_data={"msg":"Your Transfer Limit Is Over!!! Try again Later:",'status':'false','token':token.key}
                return Response(user_data)
      except:
          withdraw_last = ""
      if obj_wall_check['health_wallet'] == 1:
        if health_amt >= Decimal(actual_amttt):
          # if obj_stake_wall != 0:
            if obj_sum_transfer['actual_amount__sum'] != None or obj_check_withdraw != None:
              if obj_sum_transfer['actual_amount__sum'] != None:
                if obj_check_withdraw != None:                 
                    if obj_plan['Health_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Health_Withdraw_max_value']:
                      # if obj_check_transfer or obj_check_withdraw:
                        # if obj_check_transfer['created_on'] + timedelta(hours=24) > datetime.datetime.now(): 
                      
                        # else:
                          diff_amt = Decimal(health_amt) - Decimal(actual_amttt)
                          obj_wallet.balanceone = diff_amt
                          obj_wallet.save()
                          # add_amt = Decimal(obj_stake_wall.stake_Wallet) + Decimal(amount)
                          # obj_stake_wall.stake_Wallet = add_amt
                          # obj_stake_wall.save(using='second_db')
                          premium_wallet_deposit.objects.create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="health_wallet",create_type="Internal_Transfer_premium",withdraw_amount=Decimal(actual_amt))
                          # Withdraw(userid_id = user_Detail.id,Amount = amount,Address = 'internal_transfer_premium',Wallet_type=frm_wallet,back_up_phrase="0",created_on = datetime.datetime.now(),modified_on = datetime.datetime.now())
                          internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amttt,converted_amount=0,fees = 10,amount = 0,created_on = datetime.now(),modified_on = datetime.now(),status = 0)
                          user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                          return Response(user_data)
                        
                          
                      # else:
                      #   user_data={"msg":"No records found...!!!",'status':'false','token':token.key}
                      #   return Response(user_data)
                    else:
                      # user_data={"msg":"Limit exceeds...!!!",'status':'false','token':token.key,'Data':[obj_plan]}
                      user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                      return Response(user_data) 
                else:
                  # if obj_check_transfer['created_on'] + timedelta(hours=24) < datetime.datetime.now():
                    if obj_plan['Health_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Health_Withdraw_max_value']:
                      diff_amt = Decimal(health_amt) - Decimal(actual_amttt)
                      obj_wallet.balanceone = diff_amt
                      obj_wallet.save()
                      # add_amt = Decimal(obj_stake_wall.stake_Wallet) + Decimal(amount)
                      # obj_stake_wall.stake_Wallet = add_amt
                      # obj_stake_wall.save(using='second_db')
                      premium_wallet_deposit.objects.create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="health_wallet",create_type="Internal_Transfer_premium",withdraw_amount=Decimal(actual_amt))
                      # Withdraw(userid_id = user_Detail.id,Amount = amount,Address = 'internal_transfer_premium',Wallet_type=frm_wallet,back_up_phrase="0",created_on = datetime.datetime.now(),modified_on = datetime.datetime.now())
                      internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amttt,converted_amount=0,fees = 10,amount = 0,created_on = datetime.now(),modified_on = datetime.now(),status = 0)
                      # internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amt,fees = fee,converted_amount=convert_amount,amount = amount,created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 0)
                      user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                      return Response(user_data)
                    else:
                      # user_data={"msg":"Limit exceeds..!!",'status':'false','token':token.key,'Data':[obj_plan]}
                      user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                      return Response(user_data) 
                  # else:
                  #   user_data={"msg":"Your Transfer Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                  #   return Response(user_data)
              else:
                # if obj_check_withdraw['created_on'] + timedelta(hours=24) < datetime.datetime.now():
                  if obj_plan['Health_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Health_Withdraw_max_value']:
                    diff_amt = Decimal(health_amt) - Decimal(actual_amttt)
                    obj_wallet.balanceone = diff_amt
                    obj_wallet.save()
                    # add_amt = Decimal(obj_stake_wall.stake_Wallet) + Decimal(amount)
                    # obj_stake_wall.stake_Wallet = add_amt
                    # obj_stake_wall.save(using='second_db')
                    premium_wallet_deposit.objects.create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="health_wallet",create_type="Internal_Transfer_premium",withdraw_amount=Decimal(actual_amt))
                    # Withdraw(userid_id = user_Detail.id,Amount = amount,Address = 'internal_transfer_premium',Wallet_type=frm_wallet,back_up_phrase="0",created_on = datetime.datetime.now(),modified_on = datetime.datetime.now())
                    internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amttt,converted_amount=0,fees = 10,amount = 0,created_on = datetime.now(),modified_on = datetime.now(),status = 0)
                    # internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amt,fees = fee,converted_amount=convert_amount,amount = amount,created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 0)
                    user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                    return Response(user_data)
                  else:
                    # user_data={"msg":"Limit exceeds..!!",'status':'false','token':token.key,'Data':[obj_plan]}
                    user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                    return Response(user_data) 
                # else:
                #   user_data={"msg":"Your Transfer Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                #   return Response(user_data)
            else:
              # if obj_check_withdraw['Wallet_type'] != 'Reward_wallet' or obj_check_withdraw['created_on'] + timedelta(hours=24) < datetime.datetime.now():
                if obj_plan['Health_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Health_Withdraw_max_value']:
                  diff_amt = Decimal(health_amt) - Decimal(actual_amttt)
                  obj_wallet.balanceone = diff_amt
                  obj_wallet.save()
                  # add_amt = Decimal(obj_stake_wall.stake_Wallet) + Decimal(amount)
                  # obj_stake_wall.stake_Wallet = add_amt
                  # obj_stake_wall.save(using='second_db')
                  premium_wallet_deposit.objects.create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="health_wallet",create_type="Internal_Transfer_premium",withdraw_amount=Decimal(actual_amt))
                  # Withdraw(userid_id = user_Detail.id,Amount = amount,Address = 'internal_transfer_premium',Wallet_type=frm_wallet,back_up_phrase="0",created_on = datetime.datetime.now(),modified_on = datetime.datetime.now())
                  internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amttt,converted_amount=0,fees = 10,amount = 0,created_on = datetime.now(),modified_on = datetime.now(),status = 0)
                  # internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amt,fees = fee,converted_amount=convert_amount,amount = amount,created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 0)
                  user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                  return Response(user_data)
                else:
                  # user_data={"msg":"Limit exceeds..!!",'status':'false','token':token.key,'Data':[obj_plan]}
                  user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                  return Response(user_data) 
              # else:
              #   user_data={"Msg":"Your Transfer Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
              #   return Response(user_data)
              

          # else:
          #   user_data={"msg":"This user haven't wallet",'status':'false','token':token.key}
          #   return Response(user_data)
        else:
          user_data={"msg":"Insufficient balance",'status':'false','token':token.key,"balance" : health_amt}
          return Response(user_data)
          
      else:
        user_data={"msg":"Currently this wallet is not available...",'status':'false','token':token.key}
        return Response(user_data) 
    elif frm_wallet == "Referral_wallet":
      try:
        withdraw_last = internal_transfer_history.objects.using('second_db').filter(user = user_Detail.id,from_wallet="Referral_wallet").last()
        if withdraw_last :
            how_many_days= today - withdraw_last.created_on 
            how_many= 30 - how_many_days.days 
            # if withdraw_last.created_on + timedelta(30) > today:
            if withdraw_last.created_on + timedelta(hours=24) > today:
                # user_data={"msg":"Your Transfer Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                user_data={"msg":"Your Transfer Limit Is Over!!! Try again Later:",'status':'false','token':token.key}
                return Response(user_data)
      except:
          withdraw_last = ""
      if obj_wall_check['referral_wallet'] == 1:
        if ref_amt >= Decimal(actual_amttt):
            # if obj_stake_wall != 0:
              
              if obj_sum_transfer['actual_amount__sum'] != None or obj_check_withdraw != None:
                
                if obj_check_withdraw != None:
                  # if obj_check_withdraw['wallet_type'] 
                    # if (obj_check_withdraw['created_on'] + timedelta(hours=24) < datetime.datetime.now() and obj_check_transfer['created_on'] + timedelta(hours=24) < datetime.datetime.now()):
                      if obj_plan['Referral_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Referral_Withdraw_max_value']:
                        # if obj_check_transfer['created_on'] + timedelta(hours=24) > datetime.datetime.now() or obj_check_withdraw['created_on'] + timedelta(hours=24) > datetime.datetime.now(): 
                          
                        # else:
                          diff_amt = Decimal(ref_amt) - Decimal(actual_amttt)
                          obj_wallet.referalincome = diff_amt
                          obj_wallet.save()
                          # add_amt = Decimal(obj_stake_wall.stake_Refferal_Wallet) + Decimal(amount)
                          # obj_stake_wall.stake_Wallet = add_amt
                          # obj_stake_wall.save(using='second_db')
                          premium_wallet_deposit.objects.create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="referral_wallet",create_type="Internal_Transfer_premium",withdraw_amount=Decimal(actual_amt))
                          # Withdraw(userid_id = user_Detail.id,Amount = amount,Address = 'internal_transfer_premium',Wallet_type=frm_wallet,back_up_phrase="0",created_on = datetime.datetime.now(),modified_on = datetime.datetime.now())
                          internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amttt,converted_amount=0,fees = 10,amount = 0,created_on = datetime.now(),modified_on = datetime.now(),status = 0)
                          # internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amt,fees = fee,converted_amount=convert_amount,amount = amount,created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 0)
                          user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                          return Response(user_data)
                      else:
                        # user_data={"msg":"Limit exceeds...!!!",'status':'false','token':token.key,'Data':[obj_plan]}
                        user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                        return Response(user_data) 
                    # else:
                    #   user_data={"msg":"Your Transfer Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                    #   return Response(user_data)
                else:
                  # if obj_check_transfer['created_on'] + timedelta(hours=24) < datetime.datetime.now():
                    if obj_plan['Referral_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Referral_Withdraw_max_value']:
                      # diff_amt = Decimal(health_amt) - Decimal(actual_amt)
                      # obj_wallet.balanceone = diff_amt
                      # obj_wallet.save()
                      diff_amt = Decimal(ref_amt) - Decimal(actual_amttt)
                      obj_wallet.referalincome = diff_amt
                      obj_wallet.save()
                      # add_amt = Decimal(obj_stake_wall.stake_Wallet) + Decimal(amount)
                      # obj_stake_wall.stake_Wallet = add_amt
                      # obj_stake_wall.save(using='second_db')
                      premium_wallet_deposit.objects.create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="referral_wallet",create_type="Internal_Transfer_premium",withdraw_amount=Decimal(actual_amt))
                      # Withdraw(userid_id = user_Detail.id,Amount = amount,Address = 'internal_transfer_premium',Wallet_type=frm_wallet,back_up_phrase="0",created_on = datetime.datetime.now(),modified_on = datetime.datetime.now())
                      internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amttt,converted_amount=0,fees = 10,amount = 0,created_on = datetime.now(),modified_on = datetime.now(),status = 0)
                      # internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amt,fees = fee,converted_amount=convert_amount,amount = amount,created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 0)
                      user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                      return Response(user_data)
                    else:
                      # user_data={"msg":"Limit exceeds..!!",'status':'false','token':token.key,'Data':[obj_plan]}
                      user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                      return Response(user_data) 
                  # else:
                  #   user_data={"msg":"Your Transfer Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                  #   return Response(user_data)
                    
              else:
                # if obj_check_withdraw['Wallet_type'] != 'Referral_wallet' or obj_check_withdraw['created_on'] + timedelta(hours=24) < datetime.datetime.now():
                if obj_plan['Referral_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Referral_Withdraw_max_value']:
                  diff_amt = Decimal(ref_amt) - Decimal(actual_amttt)
                  obj_wallet.referalincome = diff_amt
                  obj_wallet.save()
                  # add_amt = Decimal(obj_stake_wall.stake_Wallet) + Decimal(amount)
                  # obj_stake_wall.stake_Wallet = add_amt
                  # obj_stake_wall.save(using='second_db')
                  premium_wallet_deposit.objects.create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="referral_wallet",create_type="Internal_Transfer_premium",withdraw_amount=Decimal(actual_amt))
                  # Withdraw(userid_id = user_Detail.id,Amount = amount,Address = 'internal_transfer_premium',Wallet_type=frm_wallet,back_up_phrase="0",created_on = datetime.datetime.now(),modified_on = datetime.datetime.now())
                  internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amttt,converted_amount=0,fees = 10,amount = 0,created_on = datetime.now(),modified_on = datetime.now(),status = 0)
                  # internal_transfer_history.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,from_wallet = frm_wallet,to_wallet = to_wallet,actual_amount = actual_amt,fees = fee,amount = amount,converted_amount=convert_amount,created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 0)
                  user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                  return Response(user_data)
                else:
                  # user_data={"msg":"Limit exceeds..!!",'status':'false','token':token.key,'Data':[obj_plan]}
                  user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                  return Response(user_data)
                # else:
                #   user_data={"Msg":"Your Transfer Limit For Today Is Over!!! Try Again Tomorrow.",'status':'false','token':token.key}
                #   return Response(user_data)
              
            # else:
            #     user_data={"msg":"This user haven't wallet",'status':'false','token':token.key}
            #     return Response(user_data)
        else:
            user_data={"msg":"Insufficient balance",'status':'false','token':token.key,"balance" : ref_amt}
            return Response(user_data)
        # else:
        #   user_data={"msg":"Limit exceeds...!!!",'status':'false','token':token.key}
        #   return Response(user_data)
      else:
        user_data={"msg":"Currently this wallet is not available...",'status':'false','token':token.key}
        return Response(user_data) 
    else:
        user_data={"msg":"Transfer your balance either health to stake wallet or referral to premium wallet.",'status':'false','token':token.key}
        return Response(user_data)
  else:
      user_data={"msg":"Something went wrong",'status':'false','token':token.key}
      return Response(user_data)


# Internal transfer wallet listing API
@api_view(['GET'])
def Internal_Transfer_Wallet_List(request):
  Token_header = request.headers['Token']
  token = Token.objects.get(key = Token_header)
  user_Detail=User_Management.objects.get(user_name = token.user) 
  wallet_list = ["health_wallet","referral_wallet","stake_wallet"]
  try:
      obj_wall = UserCashWallet.objects.get(userid = user_Detail)
  except:
      obj_wall = "None"
  try:
      obj_stake_wall = stake_wallet_management.objects.using('second_db').get(user = user_Detail.id)
  except:
      obj_stake_wall = "None"
  wall_list = []
  wallet_dict = {}
  if obj_wall != "None" and obj_stake_wall != "None":
      wallet_dict["health_wallet"] = obj_wall.balanceone
      wallet_dict["referral_wallet"] = obj_wall.referalincome
      wallet_dict["stake_wallet"] = obj_stake_wall.stake_Wallet
      wall_list.append(wallet_dict)
      user_data={'status':'true','wallet_list':wallet_list,'wallet_balance':wall_list}
      return Response(user_data)
  else:
      user_data={'msg':"User haven't wallet",'status':'false'}
      return Response(user_data)


# Internal Transfer listing
@api_view(['POST'])
def Internal_Transfer_History_List(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    usr = 0
    count = 0
    list_user = []
    start_page = request.data['pageno']
    end_value = int(start_page) * 5
    start_value = int(end_value) - 4
    internal_send_hist = internal_transfer_history.objects.using('second_db').filter(user = User.id).order_by('-created_on')
    if internal_send_hist:
        for i in internal_send_hist:
            usr = usr + 1
            dict_usr = {}
            if start_value <= usr <= end_value:
                count = count + 1
                dict_usr['from_wallet'] = (i.from_wallet)
                dict_usr['to_wallet'] = (i.to_wallet)
                dict_usr['amount'] = str(i.amount)
                dict_usr['actual_amount'] = str(i.actual_amount)
                dict_usr['created_on'] = i.created_on
                dict_usr['pageno'] = start_page
                dict_usr['fees'] = (i.fees)
                dict_usr["sno"] = usr
                list_user.append(dict_usr)
            
    user_data={"Msg":"Data Found","status":"true","Data" : list_user,"count" : internal_send_hist.count(),"Email":User.Email}
    return Response(user_data)

import math
#Stake Deposit
@api_view(['POST'])
def staking_deposit_api(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_Detail=User_Management.objects.get(user_name = token.user) 
    Amount_USDT = request.data['Amount']
    Amount_JW = request.data['Amount_JW']
    hash = request.data['Hash']
        
    try:
        user_stake_obj = stake_wallet_management.objects.using('second_db').get(user = user_Detail.id)
    except:
        user_stake_obj = 0
    
    if user_stake_obj != 0:
          user_stake_obj.stake_Wallet = Decimal(user_stake_obj.stake_Wallet) + Decimal(Amount_USDT)
          user_stake_obj.save(using='second_db')
          stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Amount_USDT,Amount_JW = Amount_JW,Hash = hash,status  = 1,type="User Create")
          user_data={'msg':"Stake Deposit Successfull",'status':'true'}
          return Response(user_data)
    else:
        user_data={'msg':"User haven't stake wallet.",'status':'false'}
        return Response(user_data)


#Stake API

@api_view(['POST'])
def stake_api(request):
  Token_header = request.headers['Token']
  token = Token.objects.get(key = Token_header)
  user_Detail=User_Management.objects.get(user_name = token.user) 
  obj_stake_wall = staking_admin_management.objects.using('second_db').get(id = 1)
  Amount_USDT = request.data['Amount']
  Amount_JW = request.data['Amount_JW']

  start_date = datetime.datetime.now()
  duration_end_date = start_date + datetime.timedelta(days=365/12*int(obj_stake_wall.stake_period))
  duration_days = (duration_end_date - start_date).days
  end_date = start_date + timedelta(days = duration_days)
  stake_market_price=Stake_market_price.objects.using('second_db').get(id=1)
  try:
      user_stake_obj = stake_wallet_management.objects.using('second_db').get(user = user_Detail.id)
  except:
      user_stake_obj = 0
  
  obj_withdraw = stake_claim_table.objects.using('second_db').filter(user = user_Detail.id).last()

  obj_stake_hist = Stake_history_management.objects.using('second_db').filter(user = user_Detail.id).last()

  obj_stake_last = Stake_history_management.objects.using('second_db').filter(user = user_Detail.id).last()
  if user_stake_obj != 0 :
    if Decimal(user_stake_obj.stake_Wallet) >= Decimal(Amount_USDT):
      if obj_stake_hist != None:
        # if Decimal(obj_stake_hist.Amount_USDT) <= Decimal(Amount_USDT):
          if Decimal(obj_stake_wall.minimum_stake) <= Decimal(Amount_USDT):
            rew_per_month = Decimal(Amount_USDT) * Decimal(obj_stake_wall.reward_percent / 100)
            max_limit = rew_per_month * obj_stake_wall.stake_period
            try:
              obj_check_stake = Stake_history_management.objects.using('second_db').filter(user = user_Detail.id,status = 0).count()
            except:
              obj_check_stake = ""
            if obj_check_stake >= 1:
              user_data={'msg':"Already There Is a Active stake",'status':'false'}
              return Response(user_data)
            date_now = obj_stake_last.start_date + timedelta(29)
            if date_now >= start_date :
              user_data={'msg':"Monthly One Stake Only",'status':'false'}
              return Response(user_data)
            else:
              user_stake_obj.stake_Wallet = Decimal(user_stake_obj.stake_Wallet) - Decimal(Amount_USDT)
              user_stake_obj.save(using='second_db')
              try:
                stake_range = Stake_referral_management.objects.using('second_db').get(status = 0,self_stake_Amount__lte = Amount_USDT,self_stake_Amount_range__gte = Amount_USDT)
              except:
                  stake_range = 0
              if stake_range != 0 :
                obj_hist_id = Stake_history_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Amount_USDT,Amount_JW = Amount_JW,period = obj_stake_wall.stake_period,reward_per_month = rew_per_month,maximum_reward = max_limit,referral_status = 0,created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),reward_percent = obj_stake_wall.reward_percent,status = 0,start_date = start_date,end_date = end_date,claim_status = 1,referral_level = stake_range.levels,market_price=stake_market_price.market_price)
                Stake_Monthly_Claim_History.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,stake_history_id = obj_hist_id,earned_stake_reward = rew_per_month,start_date = obj_hist_id.start_date,end_date = obj_hist_id.start_date + timedelta(days = 30),created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 1)
                staking_referral_two(request,Token_header,Amount_USDT)
                user_data={'msg':"Stake Successfull",'status':'true'}
                return Response(user_data)
              else:
                obj_hist_id = Stake_history_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Amount_USDT,Amount_JW = Amount_JW,period = obj_stake_wall.stake_period,reward_per_month = rew_per_month,maximum_reward = max_limit,referral_status = 0,created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),reward_percent = obj_stake_wall.reward_percent,status = 0,start_date = start_date,end_date = end_date,claim_status = 1,referral_level = 0,market_price=stake_market_price.market_price)
                Stake_Monthly_Claim_History.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,stake_history_id = obj_hist_id,earned_stake_reward = rew_per_month,start_date = obj_hist_id.start_date,end_date = obj_hist_id.start_date + timedelta(days = 30),created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 1)
                staking_referral_two(request,Token_header,Amount_USDT)
                user_data={'msg':"Stake Successfull",'status':'true'}
                return Response(user_data)
          else:
              user_data={'msg':"Minimum amount is less than Amount",'status':'false'}
              return Response(user_data)
        # else:
        #   user_data={'msg':"Your stake amount should be higher than last stake amount.",'status':'false'}
        #   return Response(user_data)
      else:
          if Decimal(obj_stake_wall.minimum_stake) <= Decimal(Amount_USDT):
            rew_per_month = Decimal(Amount_USDT) * Decimal(obj_stake_wall.reward_percent / 100)
            max_limit = rew_per_month * obj_stake_wall.stake_period
            try:
              obj_check_stake = Stake_history_management.objects.using('second_db').filter(user = user_Detail.id,status = 0).count()
            except:
              obj_check_stake = ""
            if obj_check_stake >= 1:
              user_data={'msg':"Already There Is a Active stake",'status':'false'}
              return Response(user_data)
            else:
              user_stake_obj.stake_Wallet = Decimal(user_stake_obj.stake_Wallet) - Decimal(Amount_USDT)
              user_stake_obj.save(using='second_db')
              try:
                stake_range = Stake_referral_management.objects.using('second_db').get(status = 0,self_stake_Amount__lte = Amount_USDT,self_stake_Amount_range__gte = Amount_USDT)
              except:
                  stake_range = 0
              if stake_range != 0 :
                obj_hist_id = Stake_history_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Amount_USDT,Amount_JW = Amount_JW,period = obj_stake_wall.stake_period,reward_per_month = rew_per_month,maximum_reward = max_limit,referral_status = 0,created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),reward_percent = obj_stake_wall.reward_percent,status = 0,start_date = start_date,end_date = end_date,claim_status = 1,referral_level = stake_range.levels,market_price=stake_market_price.market_price)

                Stake_Monthly_Claim_History.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,stake_history_id = obj_hist_id,earned_stake_reward = rew_per_month,start_date = obj_hist_id.start_date,end_date = obj_hist_id.start_date + timedelta(days = 30),created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 1)
                staking_referral_two(request,Token_header,Amount_USDT)
                user_data={'msg':"Stake Successfull",'status':'true'}
                return Response(user_data)
              else:
                obj_hist_id = Stake_history_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Amount_USDT,Amount_JW = Amount_JW,period = obj_stake_wall.stake_period,reward_per_month = rew_per_month,maximum_reward = max_limit,referral_status = 0,created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),reward_percent = obj_stake_wall.reward_percent,status = 0,start_date = start_date,end_date = end_date,claim_status = 1,referral_level = 0,market_price=stake_market_price.market_price)

                Stake_Monthly_Claim_History.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,stake_history_id = obj_hist_id,earned_stake_reward = rew_per_month,start_date = obj_hist_id.start_date,end_date = obj_hist_id.start_date + timedelta(days = 30),created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 1)
                staking_referral_two(request,Token_header,Amount_USDT)
                user_data={'msg':"Stake Successfull",'status':'true'}
                return Response(user_data)
          else:
              user_data={'msg':"Minimum amount is less than Amount",'status':'false'}
              return Response(user_data)
    else:
      user_data={'msg':"Insufficient Balance",'status':'false'}
      return Response(user_data)
  else:
      user_data={'msg':"User Doesn't have stake wallet.",'status':'false'}
      return Response(user_data)


@api_view(['POST'])
def stake_api_test(request):
  Token_header = request.headers['Token']
  token = Token.objects.get(key = Token_header)
  user_Detail=User_Management.objects.get(user_name = token.user) 
  Amount_USDT = request.data['Amount']
  Amount_JW = request.data['Amount_JW']

  start_date = datetime.datetime.now()
  duration_end_date = start_date + datetime.timedelta(days=365/12*36)
  duration_days = (duration_end_date - start_date).days
  end_date = start_date + timedelta(days = duration_days)

  stake_market_price=Stake_market_price.objects.using('second_db').get(id=1)
  
  try:
      user_stake_obj = stake_wallet_management.objects.using('second_db').get(user = user_Detail.id)
  except:
      user_stake_obj = 0
  
  obj_stake_wall = staking_admin_management.objects.using('second_db').get(id = 1)
  if user_stake_obj != 0 :
    if Decimal(user_stake_obj.stake_Wallet) >= Decimal(Amount_USDT):
      if Decimal(obj_stake_wall.minimum_stake) <= Decimal(Amount_USDT):
        rew_per_month = Decimal(Amount_USDT) * Decimal(obj_stake_wall.reward_percent / 100)
        max_limit = rew_per_month * obj_stake_wall.stake_period
        try:
          obj_check_stake = Stake_history_management.objects.using('second_db').filter(user = user_Detail.id,status = 0).count()
        except:
          obj_check_stake = ""
        if obj_check_stake >= 1:
          user_data={'msg':"Already There Is a Active stake",'status':'false'}
          return Response(user_data)
        else:
          user_stake_obj.stake_Wallet = Decimal(user_stake_obj.stake_Wallet) - Decimal(Amount_USDT)
          user_stake_obj.save(using='second_db')
          Stake_history_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Amount_USDT,Amount_JW = Amount_JW,period = obj_stake_wall.stake_period,reward_per_month = rew_per_month,maximum_reward = max_limit,referral_status = 0,referral_level = 0,created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),reward_percent = obj_stake_wall.reward_percent,status = 1,start_date = start_date,end_date = end_date,claim_status = 1,market_price=stake_market_price.market_price)
          staking_referral_buy_plan_method(request,Token_header,Amount_USDT)
          user_data={'msg':"Stake Successfull",'status':'true'}
          return Response(user_data)
      else:
          user_data={'msg':"Minimum amount is less than Amount",'status':'false'}
          return Response(user_data)
    else:
      user_data={'msg':"Insufficient Balance",'status':'false'}
      return Response(user_data)
  else:
      user_data={'msg':"User Doesn't have stake wallet.",'status':'false'}
      return Response(user_data)



# Stake table show API 
@api_view(['POST'])
def Staking_Deposit_History_List(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    usr = 0
    count = 0
    list_user = []
    start_page = request.data['pageno']
    end_value = int(start_page) * 10
    start_value = int(end_value) - 9
    staking_deposit_hist = Stake_history_management.objects.using('second_db').filter(user = User.id).order_by('-created_on')
    if staking_deposit_hist:
        for i in staking_deposit_hist:
            usr = usr + 1
            dict_usr = {}
            if start_value <= usr <= end_value:
                count = count + 1
                dict_usr['user'] = str(i.user)
                dict_usr['email'] = str(i.email)
                dict_usr['amount_usdt'] = (i.Amount_USDT)
                dict_usr['amount_jw'] = (i.Amount_JW)
                dict_usr['period'] = (i.period)
                dict_usr['reward_per_month'] = (i.reward_per_month)
                dict_usr['maximum_reward'] = (i.maximum_reward)
                date = i.created_on
                dict_usr['created_on'] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
                if i.status == 0:
                  status = "Active"
                else:
                  status = "Inactive"
                dict_usr['status'] = status
                dict_usr['pageno'] = start_page
                dict_usr["sno"] = usr
                list_user.append(dict_usr)
            
        user_data={"Msg":"Data Found","status":"true","Data" : list_user,"count" : staking_deposit_hist.count(),"Email":User.Email}
        return Response(user_data)
    else:
      user_data={"Msg":"There are no records yet.","Data" : list_user,"status":"false"}
      return Response(user_data)


# Stake deposit table show in admin panel
class List_Stake_Deposit_History(ListView):
    model = stake_deposit_management
    template_name = 'stake/stake_deposit_history.html'
    def get_queryset(self, **kwargs):
      return stake_deposit_management.objects.using('second_db').all()
    
    def get_context_data(self,**kwargs):
        context=super(List_Stake_Deposit_History, self).get_context_data(**kwargs)
        context['Title'] = 'Staking Deposit History'
        
        try:
          Email = self.request.GET['Email']
        except:
          Email = ""
        try:
          date = self.request.GET['date']
        except:
          date = ""
        usr = 0
        count = 0
        dict_stake_dep = {}
        start_page = self.request.GET.get('pageno', 1)
        end_value = int(start_page) * 10
        start_value = int(end_value) - 9
        if Email and date:
          obj_stake_dep = stake_deposit_management.objects.using('second_db').filter(Q(email__icontains = Email) and Q(created_on__date__icontains = date)).order_by('-id')
          for i in obj_stake_dep:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              list_usr["email"] = str(i.email)
              list_usr["Amount_USDT"] = str(i.Amount_USDT)
              list_usr["Amount_JW"] = str(i.Amount_JW)
              list_usr["hash"] = str(i.Hash)
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake_dep[count] = list_usr
   
        elif date:
          obj_stake_dep = stake_deposit_management.objects.using('second_db').filter(created_on__date__icontains = date).order_by('-id')
          for i in obj_stake_dep:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              list_usr["email"] = str(i.email)
              list_usr["Amount_USDT"] = str(i.Amount_USDT)
              list_usr["Amount_JW"] = str(i.Amount_JW)
              list_usr["hash"] = str(i.Hash)
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake_dep[count] = list_usr
        elif Email:
          obj_stake_dep = stake_deposit_management.objects.using('second_db').filter(email__icontains = Email).order_by('-id')
          for i in obj_stake_dep:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              obj_user = User_Management.objects.get(id = i.user)
              count = count + 1
              list_usr["username"] = (str(obj_user.Name))
              list_usr["email"] = str(i.email)
              list_usr["Amount_USDT"] = str(i.Amount_USDT)
              list_usr["Amount_JW"] = str(i.Amount_JW)
              list_usr["hash"] = str(i.Hash)
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake_dep[count] = list_usr
        else:
          obj_stake_dep = stake_deposit_management.objects.using('second_db').all().order_by('-id')
          for i in obj_stake_dep:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              obj_user = User_Management.objects.get(id = i.user)
              count = count + 1
              list_usr["username"] = (str(obj_user.Name))
              list_usr["email"] = str(i.email)
              list_usr["Amount_USDT"] = str(i.Amount_USDT)
              list_usr["Amount_JW"] = str(i.Amount_JW)
              list_usr["hash"] = str(i.Hash)
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake_dep[count] = list_usr
        try:
          tot_user_qs = obj_stake_dep
        except:
          tot_user_qs = ""
        w_page = self.request.GET.get('pageno', 1)
        w_paginator = Paginator(tot_user_qs, 10)
        try:
            stake_dep_qs = w_paginator.page(w_page)
        except PageNotAnInteger:
            stake_dep_qs =w_paginator.page(1)
        except EmptyPage:
            stake_dep_qs = w_paginator.page(w_paginator.num_pages)

        context["endpage"] = stake_dep_qs.number+1
        context["startpage"] = stake_dep_qs.number-1
        context['start_value'] = stake_dep_qs.start_index()
        context['end_value'] = stake_dep_qs.end_index()
        context['usr_count'] = obj_stake_dep.count()
        context['stake_dep_qs'] = stake_dep_qs
        adminactivity_qs = stake_deposit_management.objects.using('second_db').all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        context['dict_stake_dep'] = json.dumps(dict_stake_dep) 
        context['add_title'] ='Stake Deposit History'
        context['Btn_url'] = 'staking:List_Stake_Deposit_History'
        return context

    @method_decorator(check_group("Staking Management"))
    def dispatch(self, *args, **kwargs):
      return super(List_Stake_Deposit_History, self).dispatch(*args, **kwargs)

# List stake history
class List_Stake(ListView):
    model = Stake_history_management
    template_name = 'stake/stake_history.html'
    def get_queryset(self, **kwargs):
      return Stake_history_management.objects.using('second_db').all()
    
    def get_context_data(self,**kwargs):
        context=super(List_Stake, self).get_context_data(**kwargs)
        context['Title'] = 'Staking History'
       
        try:
          Email = self.request.GET['Email']
        except:
          Email = ""
        try:
          date = self.request.GET['date']
        except:
          date = ""
        usr = 0
        count = 0
        dict_stake = {}
        start_page = self.request.GET.get('pageno', 1)
        end_value = int(start_page) * 10
        start_value = int(end_value) - 9
        if Email and date:
          obj_stake = Stake_history_management.objects.using('second_db').filter(Q(email = Email) and Q(created_on__date__icontains = date)).order_by('-id')
          for i in obj_stake:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              obj_stake_wall = stake_wallet_management.objects.using('second_db').get(user = i.user)
              list_usr["email"] = str(i.email)
              list_usr["Amount_USDT"] = str(i.Amount_USDT)
              list_usr["Amount_JW"] = str(i.Amount_JW)
              list_usr["max_limit"] = str(i.maximum_reward)
              list_usr["reward_per_month"] = (str(i.reward_per_month))
              # ref_rew = (round(Decimal(obj_stake_wall.stake_Refferal_Wallet),4))
              # list_usr["ref_rew_earned"] = str(ref_rew)
              ref_rew = (round(Decimal(i.referral_reward_earned),4))
              list_usr["ref_rew_earned"] = str(ref_rew)
              list_usr["rew_earned"] = Decimal(i.reward_earned)
              # tot_rew_earned = Decimal(obj_stake_wall.stake_Refferal_Wallet) + Decimal(i.reward_earned)
              # tot_reward = (round(Decimal(tot_rew_earned),4))
              # list_usr["total_rew_earned"] = str(tot_reward)
              list_usr["total_rew_earned"] = Decimal(i.Total_reward_earned)
              list_usr["rew_blnc"] =  (i.reward_balance)
              list_usr["start_date"] = str(i.start_date.strftime('%Y-%m-%d'))
              list_usr["end_date"] = str(i.end_date.strftime('%Y-%m-%d'))
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake[count] = list_usr
        
        elif date:
          obj_stake = Stake_history_management.objects.using('second_db').filter(created_on__date__icontains = date).order_by('-id')
          for i in obj_stake:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              obj_stake_wall = stake_wallet_management.objects.using('second_db').get(user = i.user)
              list_usr["email"] = str(i.email)
              list_usr["Amount_USDT"] = str(i.Amount_USDT)
              list_usr["Amount_JW"] = str(i.Amount_JW)
              list_usr["max_limit"] = str(i.maximum_reward)
              list_usr["reward_per_month"] = (str(i.reward_per_month))
              # ref_rew = (round(Decimal(obj_stake_wall.stake_Refferal_Wallet),4))
              # list_usr["ref_rew_earned"] = str(ref_rew)

              ref_rew = (round(Decimal(i.referral_reward_earned),4))
              list_usr["ref_rew_earned"] = str(ref_rew)
              list_usr["rew_earned"] = str(i.reward_earned)
              # tot_rew_earned = Decimal(obj_stake_wall.stake_Refferal_Wallet) + Decimal(i.reward_earned)
              # tot_reward = (round(Decimal(tot_rew_earned),4))
              # list_usr["total_rew_earned"] = str(tot_reward)
              list_usr["total_rew_earned"] = str(i.Total_reward_earned)
              list_usr["rew_blnc"] = str(i.reward_balance)
              list_usr["start_date"] = str(i.start_date.strftime('%Y-%m-%d'))
              list_usr["end_date"] = str(i.end_date.strftime('%Y-%m-%d'))
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake[count] = list_usr
        elif Email:
          obj_stake = Stake_history_management.objects.using('second_db').filter(email = Email).order_by('-id')
          for i in obj_stake:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              obj_stake_wall = stake_wallet_management.objects.using('second_db').get(user = i.user)
              list_usr["email"] = str(i.email)
              list_usr["Amount_USDT"] = str(i.Amount_USDT)
              list_usr["Amount_JW"] = str(i.Amount_JW)
              list_usr["max_limit"] = str(i.maximum_reward)
              list_usr["reward_per_month"] = (str(i.reward_per_month))
              # ref_rew = (round(Decimal(obj_stake_wall.stake_Refferal_Wallet),4))
              # list_usr["ref_rew_earned"] = str(ref_rew)
              ref_rew = (round(Decimal(i.referral_reward_earned),4))
              list_usr["ref_rew_earned"] = str(ref_rew)
              list_usr["rew_earned"] = str(i.reward_earned)
              # tot_rew_earned = Decimal(obj_stake_wall.stake_Refferal_Wallet) + Decimal(i.reward_earned)
              # tot_reward = (round(Decimal(tot_rew_earned),4))
              # list_usr["total_rew_earned"] = str(tot_reward)
              list_usr["total_rew_earned"] = str(i.Total_reward_earned)
              list_usr["rew_blnc"] = str(i.reward_balance)
              list_usr["start_date"] = str(i.start_date.strftime('%Y-%m-%d'))
              list_usr["end_date"] = str(i.end_date.strftime('%Y-%m-%d'))
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake[count] = list_usr
        else:
          obj_stake = Stake_history_management.objects.using('second_db').all().order_by('-id')
          for i in obj_stake:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              obj_stake_wall = stake_wallet_management.objects.using('second_db').get(user = i.user)
              list_usr["email"] = str(i.email)
              list_usr["Amount_USDT"] = str(i.Amount_USDT)
              list_usr["Amount_JW"] = str(i.Amount_JW)
              list_usr["max_limit"] = str(i.maximum_reward)
              list_usr["reward_per_month"] = (str(i.reward_per_month))
              # ref_rew = (round(Decimal(obj_stake_wall.stake_Refferal_Wallet),4))
              # list_usr["ref_rew_earned"] = str(ref_rew)
              ref_rew = (round(Decimal(i.referral_reward_earned),4))
              list_usr["ref_rew_earned"] = str(ref_rew)
              list_usr["rew_earned"] = str(i.reward_earned)
              # tot_rew_earned = Decimal(obj_stake_wall.stake_Refferal_Wallet) + Decimal(i.reward_earned)
              # tot_reward = (round(Decimal(tot_rew_earned),4))
              # list_usr["total_rew_earned"] = str(tot_reward)
              list_usr["total_rew_earned"] = str(i.Total_reward_earned)
              list_usr["rew_blnc"] = str(i.reward_balance)
              list_usr["start_date"] = str(i.start_date.strftime('%Y-%m-%d'))
              list_usr["end_date"] = str(i.end_date.strftime('%Y-%m-%d'))
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake[count] = list_usr
        try:
          tot_user_qs = obj_stake
        except:
          tot_user_qs = ""
        w_page = self.request.GET.get('pageno', 1)
        w_paginator = Paginator(tot_user_qs, 10)
        try:
            stake_qs = w_paginator.page(w_page)
        except PageNotAnInteger:
            stake_qs =w_paginator.page(1)
        except EmptyPage:
            stake_qs = w_paginator.page(w_paginator.num_pages)

        context["endpage"] = stake_qs.number+1
        context["startpage"] = stake_qs.number-1
        context['start_value'] = stake_qs.start_index()
        context['end_value'] = stake_qs.end_index()
        context['usr_count'] = obj_stake.count()
        context['stake_qs'] = stake_qs
        adminactivity_qs = Stake_history_management.objects.using('second_db').all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        context['dict_stake'] = json.dumps(dict_stake) 
        context['add_title'] ='Staking History'
        context['Btn_url'] = 'staking:List_Stake'
        return context

    @method_decorator(check_group("Staking Management"))
    def dispatch(self, *args, **kwargs):
      return super(List_Stake, self).dispatch(*args, **kwargs)
    


class List_Stake_credit(ListView):
    model = Stake_monthly_history_management
    template_name = 'stake/stake_credit_history.html'
    def get_queryset(self, **kwargs):
      return Stake_monthly_history_management.objects.using('second_db').all()
    
    def get_context_data(self,**kwargs):
        context=super(List_Stake_credit, self).get_context_data(**kwargs)
        context['Title'] = 'Staking Credit History'
       
        try:
          Email = self.request.GET['Email']
        except:
          Email = ""
        try:
          date = self.request.GET['date']
        except:
          date = ""
        usr = 0
        count = 0
        dict_stake = {}
        start_page = self.request.GET.get('pageno', 1)
        end_value = int(start_page) * 10
        start_value = int(end_value) - 9
        if Email and date:
          obj_stake = Stake_monthly_history_management.objects.using('second_db').filter(Q(email = Email) and Q(created_on__date__icontains = date)).order_by('-id')
          for i in obj_stake:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              obj_stake_wall = stake_wallet_management.objects.using('second_db').get(user = i.user)
              list_usr["email"] = str(i.email)
              list_usr["Amount_USDT"] = str(i.Amount_USDT)
              list_usr["Amount_JW"] = str(i.Amount_JW)
              list_usr["max_limit"] = str(i.maximum_reward)
              list_usr["reward_per_month"] = (str(i.reward_per_month))
              ref_rew = (round(Decimal(obj_stake_wall.stake_Refferal_Wallet),4))
              list_usr["ref_rew_earned"] = str(ref_rew)
              list_usr["rew_earned"] = str(i.reward_earned)
              tot_rew_earned = Decimal(obj_stake_wall.stake_Refferal_Wallet) + Decimal(i.reward_earned)
              tot_reward = (round(Decimal(tot_rew_earned),4))
              list_usr["total_rew_earned"] = str(tot_reward)
              list_usr["rew_blnc"] =  (i.reward_balance)
              list_usr["start_date"] = str(i.start_date.strftime('%Y-%m-%d'))
              list_usr["end_date"] = str(i.end_date.strftime('%Y-%m-%d'))
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake[count] = list_usr
        
        elif date:
          obj_stake = Stake_monthly_history_management.objects.using('second_db').filter(created_on__date__icontains = date).order_by('-id')
          for i in obj_stake:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              obj_stake_wall = stake_wallet_management.objects.using('second_db').get(user = i.user)
              list_usr["email"] = str(i.email)
              list_usr["Amount_USDT"] = str(i.Amount_USDT)
              list_usr["Amount_JW"] = str(i.Amount_JW)
              list_usr["max_limit"] = str(i.maximum_reward)
              list_usr["reward_per_month"] = (str(i.reward_per_month))
              ref_rew = (round(Decimal(obj_stake_wall.stake_Refferal_Wallet),4))
              list_usr["ref_rew_earned"] = str(ref_rew)
              list_usr["rew_earned"] = str(i.reward_earned)
              tot_rew_earned = Decimal(obj_stake_wall.stake_Refferal_Wallet) + Decimal(i.reward_earned)
              tot_reward = (round(Decimal(tot_rew_earned),4))
              list_usr["total_rew_earned"] = str(tot_reward)
              list_usr["rew_blnc"] = str(i.reward_balance)
              list_usr["start_date"] = str(i.start_date.strftime('%Y-%m-%d'))
              list_usr["end_date"] = str(i.end_date.strftime('%Y-%m-%d'))
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake[count] = list_usr
        elif Email:
          obj_stake = Stake_monthly_history_management.objects.using('second_db').filter(email = Email).order_by('-id')
          for i in obj_stake:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              obj_stake_wall = stake_wallet_management.objects.using('second_db').get(user = i.user)
              list_usr["email"] = str(i.email)
              list_usr["Amount_USDT"] = str(i.Amount_USDT)
              list_usr["Amount_JW"] = str(i.Amount_JW)
              list_usr["max_limit"] = str(i.maximum_reward)
              list_usr["reward_per_month"] = (str(i.reward_per_month))
              ref_rew = (round(Decimal(obj_stake_wall.stake_Refferal_Wallet),4))
              list_usr["ref_rew_earned"] = str(ref_rew)
              list_usr["rew_earned"] = str(i.reward_earned)
              tot_rew_earned = Decimal(obj_stake_wall.stake_Refferal_Wallet) + Decimal(i.reward_earned)
              tot_reward = (round(Decimal(tot_rew_earned),4))
              list_usr["total_rew_earned"] = str(tot_reward)
              list_usr["rew_blnc"] = str(i.reward_balance)
              list_usr["start_date"] = str(i.start_date.strftime('%Y-%m-%d'))
              list_usr["end_date"] = str(i.end_date.strftime('%Y-%m-%d'))
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake[count] = list_usr
        else:
          obj_stake = Stake_monthly_history_management.objects.using('second_db').all().order_by('-id')
          for i in obj_stake:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              obj_stake_wall = stake_wallet_management.objects.using('second_db').get(user = i.user)
              list_usr["email"] = str(i.email)
              list_usr["Amount_USDT"] = str(i.Amount_USDT)
              list_usr["Amount_JW"] = str(i.Amount_JW)
              list_usr["max_limit"] = str(i.maximum_reward)
              list_usr["reward_per_month"] = (str(i.reward_per_month))
              ref_rew = (round(Decimal(obj_stake_wall.stake_Refferal_Wallet),4))
              list_usr["ref_rew_earned"] = str(ref_rew)
              list_usr["rew_earned"] = str(i.reward_earned)
              tot_rew_earned = Decimal(obj_stake_wall.stake_Refferal_Wallet) + Decimal(i.reward_earned)
              tot_reward = (round(Decimal(tot_rew_earned),4))
              list_usr["total_rew_earned"] = str(tot_reward)
              list_usr["rew_blnc"] = str(i.reward_balance)
              list_usr["start_date"] = str(i.start_date.strftime('%Y-%m-%d'))
              list_usr["end_date"] = str(i.end_date.strftime('%Y-%m-%d'))
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake[count] = list_usr
        try:
          tot_user_qs = obj_stake
        except:
          tot_user_qs = ""
        w_page = self.request.GET.get('pageno', 1)
        w_paginator = Paginator(tot_user_qs, 10)
        try:
            stake_qs = w_paginator.page(w_page)
        except PageNotAnInteger:
            stake_qs =w_paginator.page(1)
        except EmptyPage:
            stake_qs = w_paginator.page(w_paginator.num_pages)

        context["endpage"] = stake_qs.number+1
        context["startpage"] = stake_qs.number-1
        context['start_value'] = stake_qs.start_index()
        context['end_value'] = stake_qs.end_index()
        context['usr_count'] = obj_stake.count()
        context['stake_qs'] = stake_qs
        adminactivity_qs = Stake_monthly_history_management.objects.using('second_db').all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        context['dict_stake'] = json.dumps(dict_stake) 
        context['add_title'] ='Staking History'
        context['Btn_url'] = 'staking:List_Stake'
        return context
# List stake claim history
class List_Stake_Claim_History(ListView):
    model = stake_claim_table
    template_name = 'stake/stake_claim_history.html'
    def get_queryset(self, **kwargs):
      return stake_claim_table.objects.using('second_db').all()
    
    def get_context_data(self,**kwargs):
        context=super(List_Stake_Claim_History, self).get_context_data(**kwargs)
        context['Title'] = 'Staking Withdraw History'
        
        try:
          Email = self.request.GET['Email']
        except:
          Email = ""
        try:
          date = self.request.GET['date']
        except:
          date = ""
        usr = 0
        count = 0
        dict_stake_claim = {}
        start_page = self.request.GET.get('pageno', 1)
        end_value = int(start_page) * 10
        start_value = int(end_value) - 9
        if Email and date:
          obj_stake_claim = stake_claim_table.objects.using('second_db').filter(Q(email__icontains = Email) and Q(created_on__date__icontains = date)).order_by('-id')
          for i in obj_stake_claim:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              list_usr["email"] = str(i.email)
              list_usr["original_USDT"]=str(i.original_USDT)
              list_usr["claim_amount_USDT"] = str(i.claim_amount_USDT)
              list_usr["claim_amount_JW"] = str(i.claim_amount_JW)
              list_usr["Address"] = str(i.Address)
              list_usr["hash"] = str(i.Transaction_Hash)
              list_usr["Wallet_type"]=i.Wallet_type
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake_claim[count] = list_usr
        
        elif date:
          obj_stake_claim = stake_claim_table.objects.using('second_db').filter(created_on__date__icontains = date).order_by('-id')
          for i in obj_stake_claim:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              list_usr["email"] = str(i.email)
              list_usr["original_USDT"]=str(i.original_USDT)
              list_usr["claim_amount_USDT"] = str(i.claim_amount_USDT)
              list_usr["claim_amount_JW"] = str(i.claim_amount_JW)
              list_usr["Address"] = str(i.Address)
              list_usr["hash"] = str(i.Transaction_Hash)
              list_usr["Wallet_type"]=i.Wallet_type
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake_claim[count] = list_usr
        elif Email:
          obj_stake_claim = stake_claim_table.objects.using('second_db').filter(email__icontains = Email).order_by('-id')
          for i in obj_stake_claim:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              list_usr["email"] = str(i.email)
              list_usr["original_USDT"]=str(i.original_USDT)
              list_usr["claim_amount_USDT"] = str(i.claim_amount_USDT)
              list_usr["claim_amount_JW"] = str(i.claim_amount_JW)
              list_usr["Address"] = str(i.Address)
              list_usr["hash"] = str(i.Transaction_Hash)
              list_usr["Wallet_type"]=i.Wallet_type
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake_claim[count] = list_usr
        else:
          obj_stake_claim = stake_claim_table.objects.using('second_db').all().order_by('-id')
          for i in obj_stake_claim:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              list_usr["email"] = str(i.email)
              list_usr["original_USDT"]=str(i.original_USDT)
              list_usr["claim_amount_USDT"] = str(i.claim_amount_USDT)
              list_usr["claim_amount_JW"] = str(i.claim_amount_JW)
              list_usr["Address"] = str(i.Address)
              list_usr["hash"] = str(i.Transaction_Hash)
              list_usr["Wallet_type"]=i.Wallet_type
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake_claim[count] = list_usr
        try:
          tot_user_qs = obj_stake_claim
        except:
          tot_user_qs = ""
        w_page = self.request.GET.get('pageno', 1)
        w_paginator = Paginator(tot_user_qs, 10)
        try:
            stake_claim_qs = w_paginator.page(w_page)
        except PageNotAnInteger:
            stake_claim_qs =w_paginator.page(1)
        except EmptyPage:
            stake_claim_qs = w_paginator.page(w_paginator.num_pages)

        context["endpage"] = stake_claim_qs.number+1
        context["startpage"] = stake_claim_qs.number-1
        context['start_value'] = stake_claim_qs.start_index()
        context['end_value'] = stake_claim_qs.end_index()
        context['usr_count'] = obj_stake_claim.count()
        context['stake_claim_qs'] = stake_claim_qs
        adminactivity_qs = stake_deposit_management.objects.using('second_db').all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        context['dict_stake_claim'] = json.dumps(dict_stake_claim) 
        context['add_title'] ='Stake Claim History'
        context['Btn_url'] = 'staking:List_Stake_Claim_History'
        return context
# List stake claim history
class List_Stake_Claim_History(ListView):
    model = stake_claim_table
    template_name = 'stake/stake_claim_history.html'
    def get_queryset(self, **kwargs):
      return stake_claim_table.objects.using('second_db').all()
    
    def get_context_data(self,**kwargs):
        context=super(List_Stake_Claim_History, self).get_context_data(**kwargs)
        context['Title'] = 'Staking Claim History'
        
        try:
          Email = self.request.GET['Email']
        except:
          Email = ""
        try:
          date = self.request.GET['date']
        except:
          date = ""
        usr = 0
        count = 0
        dict_stake_claim = {}
        start_page = self.request.GET.get('pageno', 1)
        end_value = int(start_page) * 10
        start_value = int(end_value) - 9
        if Email and date:
          obj_stake_claim = stake_claim_table.objects.using('second_db').filter(Q(email__icontains = Email) and Q(created_on__date__icontains = date)).order_by('-id')
          for i in obj_stake_claim:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              list_usr["email"] = str(i.email)
              list_usr["original_USDT"]=str(i.original_USDT)
              list_usr["claim_amount_USDT"] = str(i.claim_amount_USDT)
              list_usr["claim_amount_JW"] = str(i.claim_amount_JW)
              list_usr["Address"] = str(i.Address)
              list_usr["hash"] = str(i.Transaction_Hash)
              list_usr["Wallet_type"]=i.Wallet_type
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake_claim[count] = list_usr
        
        elif date:
          obj_stake_claim = stake_claim_table.objects.using('second_db').filter(created_on__date__icontains = date).order_by('-id')
          for i in obj_stake_claim:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              list_usr["email"] = str(i.email)
              list_usr["original_USDT"]=str(i.original_USDT)
              list_usr["claim_amount_USDT"] = str(i.claim_amount_USDT)
              list_usr["claim_amount_JW"] = str(i.claim_amount_JW)
              list_usr["Address"] = str(i.Address)
              list_usr["hash"] = str(i.Transaction_Hash)
              list_usr["Wallet_type"]=i.Wallet_type
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake_claim[count] = list_usr
        elif Email:
          obj_stake_claim = stake_claim_table.objects.using('second_db').filter(email__icontains = Email).order_by('-id')
          for i in obj_stake_claim:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              list_usr["email"] = str(i.email)
              list_usr["original_USDT"]=str(i.original_USDT)
              list_usr["claim_amount_USDT"] = str(i.claim_amount_USDT)
              list_usr["claim_amount_JW"] = str(i.claim_amount_JW)
              list_usr["Address"] = str(i.Address)
              list_usr["hash"] = str(i.Transaction_Hash)
              list_usr["Wallet_type"]=i.Wallet_type
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake_claim[count] = list_usr
        else:
          obj_stake_claim = stake_claim_table.objects.using('second_db').all().order_by('-id')
          for i in obj_stake_claim:
            usr = usr + 1
            list_usr = {}
            if start_value <= usr <= end_value:
              count = count + 1
              list_usr["email"] = str(i.email)
              list_usr["original_USDT"]=str(i.original_USDT)
              list_usr["claim_amount_USDT"] = str(i.claim_amount_USDT)
              list_usr["claim_amount_JW"] = str(i.claim_amount_JW)
              list_usr["Address"] = str(i.Address)
              list_usr["hash"] = str(i.Transaction_Hash)
              list_usr["Wallet_type"]=i.Wallet_type
              list_usr["status"] = i.status
              date = i.created_on
              list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
              list_usr["pageno"] = start_page
              list_usr["sno"] = usr
              dict_stake_claim[count] = list_usr
        try:
          tot_user_qs = obj_stake_claim
        except:
          tot_user_qs = ""
        w_page = self.request.GET.get('pageno', 1)
        w_paginator = Paginator(tot_user_qs, 10)
        try:
            stake_claim_qs = w_paginator.page(w_page)
        except PageNotAnInteger:
            stake_claim_qs =w_paginator.page(1)
        except EmptyPage:
            stake_claim_qs = w_paginator.page(w_paginator.num_pages)

        context["endpage"] = stake_claim_qs.number+1
        context["startpage"] = stake_claim_qs.number-1
        context['start_value'] = stake_claim_qs.start_index()
        context['end_value'] = stake_claim_qs.end_index()
        context['usr_count'] = obj_stake_claim.count()
        context['stake_claim_qs'] = stake_claim_qs
        adminactivity_qs = stake_deposit_management.objects.using('second_db').all().order_by('-id')
        context['adminactivity_qs'] =adminactivity_qs
        context['dict_stake_claim'] = json.dumps(dict_stake_claim) 
        context['add_title'] ='Stake Claim History'
        context['Btn_url'] = 'staking:List_Stake_Claim_History'
        return context
    
    @method_decorator(check_group("Staking Management"))
    def dispatch(self, *args, **kwargs):
      return super(List_Stake_Claim_History, self).dispatch(*args, **kwargs)

class StakeHistoryManagementTable(TemplateView):
  template_name = "stake/stake_user_history_table.html"

  def get_context_data(self, **kwargs):
    context = super(StakeHistoryManagementTable, self).get_context_data(**kwargs)
    p_key = self.kwargs['pk']
    context["p_key"] = p_key
    context["Title"] = "User Stake History"
    context["Btn_url"] = "trade_admin_auth:List_User_Management"
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

    context['p_no'] = p_no
    context['p_no1'] = p_no1
    context['p_no2'] = p_no2
    context['p_no3'] = p_no3
    context['p_no4'] = p_no4
    context['p_no5'] = p_no5


    # -------------------------------------------------------------------Internal Transfer History-----------------------------------------------------

    try:
      date = self.request.GET['Date']
    except:
      date = ""


    int_usr = 0
    int_count = 0
    int_dict_users = {}
    int_start_page = self.request.GET.get('pageno', 1)
    int_end_value = int(int_start_page) * 5
    int_start_value = int(int_end_value) - 4
    
    if date:
      obj_internal_hist = internal_transfer_history.objects.using('second_db').filter(user = user_obj.id).filter(created_on__date = date).order_by('-created_on')
      for i in obj_internal_hist:
        
        int_usr = int_usr + 1
        int_list_usr = {}
        if int_start_value <= int_usr <= int_end_value:
          int_count = int_count + 1
          int_list_usr["username"] = str(user_obj.Name)
          int_list_usr["amt"] = str(i.actual_amount)
          if i.from_wallet == "Reward_wallet":
            frm_wallet = "Health_wallet"
          else:
             frm_wallet = "Referral_wallet"
          int_list_usr["frm_wallet"] = (frm_wallet)
          int_list_usr["to_wallet"] = (i.to_wallet)
          created_date = i.created_on
          int_list_usr["date"] = str(created_date.strftime("%m/%d/%Y, %H:%M:%S"))
          int_list_usr["pageno"] = int_start_page
          int_list_usr["sno"] = int_usr
          int_dict_users[int_count] = int_list_usr
    else:
      obj_internal_hist = internal_transfer_history.objects.using('second_db').filter(user = user_obj.id).order_by('-id')
      for i in obj_internal_hist:
        int_usr = int_usr + 1
        int_list_usr = {}
        if int_start_value <= int_usr <= int_end_value:
            int_count = int_count + 1
            int_list_usr["username"] = str(user_obj.Name)
            int_list_usr["amt"] = str(i.actual_amount)
            int_list_usr["frm_wallet"] = (i.from_wallet)
            int_list_usr["to_wallet"] = (i.to_wallet)
            created_date = i.created_on
            int_list_usr["date"] = str(created_date.strftime("%m/%d/%Y, %H:%M:%S"))
            int_list_usr["pageno"] = int_start_page
            int_list_usr["sno"] = int_usr
            int_dict_users[int_count] = int_list_usr

    try:
      tot_int_user_qs = obj_internal_hist
    except:
      tot_int_user_qs = ""
    w_page = self.request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_int_user_qs, 5)
    
    try:
        int_hist_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        int_hist_qs =w_paginator.page(1)
    except EmptyPage:
        int_hist_qs = w_paginator.page(w_paginator.num_pages)
    
    
    context['int_hist_qs'] = int_hist_qs
    context["int_endpage"] = int_hist_qs.number+1
    context["int_startpage"] = int_hist_qs.number-1
    context['int_start_value'] = int_hist_qs.start_index()
    context['int_end_value'] = int_hist_qs.end_index()
    context['int_usr_count'] = obj_internal_hist.count()
    context["int_dict_users"] = json.dumps(int_dict_users)


    # ------------------------------------------------------------------Deposit History-------------------------------------------------------

    try:
      dep_date = self.request.GET['date']
    except:
      dep_date = ""


    dep_usr = 0
    dep_count = 0
    dep_dict_users = {}
    dep_start_page = self.request.GET.get('pageno1', 1)
    dep_end_value = int(dep_start_page) * 5
    dep_start_value = int(dep_end_value) - 4
    
    if dep_date:
      obj_deposit_hist = stake_deposit_management.objects.using('second_db').filter(user = p_key).filter(created_on__date = dep_date).order_by('-created_on')
      for i in obj_deposit_hist:
        dep_usr = dep_usr + 1
        dep_list_usr = {}
        if dep_start_value <= dep_usr <= dep_end_value:
          dep_count = dep_count + 1
          dep_list_usr["username"] = str(user_obj.Name)
          dep_list_usr["Amount_USDT"] = str(i.Amount_USDT)
          dep_list_usr["Amount_JW"] = (i.Amount_JW)
          dep_list_usr["Hash"] = (i.Hash)
          dep_list_usr["type"] = (i.type)
          dep_list_usr["id"] = (i.id)
          created_date = i.created_on
          dep_list_usr["date"] = str(created_date.strftime("%m/%d/%Y, %H:%M:%S"))
          dep_list_usr["pageno"] = dep_start_page
          dep_list_usr["sno"] = dep_usr
          dep_dict_users[dep_count] = dep_list_usr
    else:
      obj_deposit_hist = stake_deposit_management.objects.using('second_db').filter(user = p_key).order_by('-id')
      for i in obj_deposit_hist:
        dep_usr = dep_usr + 1
        dep_list_usr = {}
        if dep_start_value <= dep_usr <= dep_end_value:
            dep_count = dep_count + 1
            dep_list_usr["username"] = str(user_obj.Name)
            dep_list_usr["Amount_USDT"] = str(i.Amount_USDT)
            dep_list_usr["Amount_JW"] = str(i.Amount_JW)
            dep_list_usr["Hash"] = (i.Hash)
            dep_list_usr["type"] = (i.type)
            dep_list_usr["id"] = (i.id)
            created_date = i.created_on
            dep_list_usr["date"] = str(created_date.strftime("%m/%d/%Y, %H:%M:%S"))
            dep_list_usr["pageno"] = dep_start_page
            dep_list_usr["sno"] = dep_usr
            dep_dict_users[dep_count] = dep_list_usr

    try:
      tot_dep_user_qs = obj_deposit_hist
    except:
      tot_dep_user_qs = ""
    w_page_1 = self.request.GET.get('pageno1', 1)
    w_paginator_1 = Paginator(tot_dep_user_qs, 5)
    
    try:
        dep_hist_qs = w_paginator_1.page(w_page_1)
    except PageNotAnInteger:
        dep_hist_qs =w_paginator_1.page(1)
    except EmptyPage:
        dep_hist_qs = w_paginator_1.page(w_paginator_1.num_pages)
    
    
    context['dep_hist_qs'] = dep_hist_qs
    context["dep_endpage"] = dep_hist_qs.number+1
    context["dep_start_page"] = dep_hist_qs.number-1
    context['dep_start_value'] = dep_hist_qs.start_index()
    context['dep_end_value'] = dep_hist_qs.end_index()
    context['dep_usr_count'] = obj_deposit_hist.count()
    context["dep_dict_users"] = json.dumps(dep_dict_users)


# ---------------------------------------------------------Staking History-------------------------------------------------

    try:
      stake_date = self.request.GET['created_on']
    except:
      stake_date = ""


    stake_usr = 0
    stake_count = 0
    stake_dict_users = {}
    stake_start_page = self.request.GET.get('pageno2', 1)
    stake_end_value = int(stake_start_page) * 5
    stake_start_value = int(stake_end_value) - 4
    
    if stake_date:
      obj_stake_hist = Stake_history_management.objects.using('second_db').filter(user = p_key).filter(created_on__date = stake_date).order_by('-created_on')
      for i in obj_stake_hist:
        stake_usr = stake_usr + 1
        stake_list_usr = {}
        if stake_start_value <= stake_usr <= stake_end_value:
          stake_count = stake_count + 1
          obj_stake_wall = stake_wallet_management.objects.using('second_db').get(user = i.user)
          stake_list_usr["email"] = str(i.email)
          stake_list_usr["Amount_USDT"] = str(i.Amount_USDT)
          stake_list_usr["Amount_JW"] = str(i.Amount_JW)
          stake_list_usr["max_limit"] = str(i.maximum_reward)
          stake_list_usr["reward_per_month"] = (str(i.reward_per_month))
          # ref_rew = (round(Decimal(obj_stake_wall.stake_Refferal_Wallet),4))
          # stake_list_usr["ref_rew_earned"] = str(ref_rew)
          ref_rew = (round(Decimal(i.referral_reward_earned),4))
          stake_list_usr["ref_rew_earned"] = str(ref_rew)
          stake_list_usr["rew_earned"] = str(i.reward_earned)
          # tot_rew_earned = Decimal(obj_stake_wall.stake_Refferal_Wallet) + Decimal(i.reward_earned)
          # tot_reward = (round(Decimal(tot_rew_earned),4))
          # stake_list_usr["total_rew_earned"] = str(tot_reward)
          stake_list_usr["total_rew_earned"] = str(i.Total_reward_earned)
          stake_list_usr["rew_blnc"] = str(i.reward_balance)
          stake_list_usr["start_date"] = str(i.start_date.strftime('%Y-%m-%d'))
          stake_list_usr["end_date"] = str(i.end_date.strftime('%Y-%m-%d'))
          stake_list_usr["status"] = i.status
          date = i.created_on
          stake_list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
          stake_list_usr["pageno"] = stake_start_page
          stake_list_usr["sno"] = stake_usr
          stake_dict_users[stake_count] = stake_list_usr
    else:
      obj_stake_hist = Stake_history_management.objects.using('second_db').filter(user = p_key).order_by('-id')
      for i in obj_stake_hist:
        stake_usr = stake_usr + 1
        stake_list_usr = {}
        if stake_start_value <= stake_usr <= stake_end_value:
            stake_count = stake_count + 1
            obj_stake_wall = stake_wallet_management.objects.using('second_db').get(user = i.user)
            stake_list_usr["email"] = str(i.email)
            stake_list_usr["Amount_USDT"] = str(i.Amount_USDT)
            stake_list_usr["Amount_JW"] = str(i.Amount_JW)
            stake_list_usr["max_limit"] = str(i.maximum_reward)
            stake_list_usr["reward_per_month"] = (str(i.reward_per_month))
            # ref_rew = (round(Decimal(obj_stake_wall.stake_Refferal_Wallet),4))
            # stake_list_usr["ref_rew_earned"] = str(ref_rew)
            ref_rew = (round(Decimal(i.referral_reward_earned),4))
            stake_list_usr["ref_rew_earned"] = str(ref_rew)
            stake_list_usr["rew_earned"] = str(i.reward_earned)
            # tot_rew_earned = Decimal(obj_stake_wall.stake_Refferal_Wallet) + Decimal(i.reward_earned)
            # tot_reward = (round(Decimal(tot_rew_earned),4))
            # stake_list_usr["total_rew_earned"] = str(tot_reward)
            stake_list_usr["total_rew_earned"] = str(i.Total_reward_earned)
            stake_list_usr["rew_blnc"] = str(i.reward_balance)
            stake_list_usr["start_date"] = str(i.start_date.strftime('%Y-%m-%d'))
            stake_list_usr["end_date"] = str(i.end_date.strftime('%Y-%m-%d'))
            stake_list_usr["status"] = i.status
            date = i.created_on
            stake_list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
            stake_list_usr["pageno"] = stake_start_page
            stake_list_usr["sno"] = stake_usr
            stake_dict_users[stake_count] = stake_list_usr

    try:
      tot_stake_user_qs = obj_stake_hist
    except:
      tot_stake_user_qs = ""
    w_page_2 = self.request.GET.get('pageno2', 1)
    w_paginator_2 = Paginator(tot_stake_user_qs, 5)
    
    try:
        stake_hist_qs = w_paginator_2.page(w_page_2)
    except PageNotAnInteger:
        stake_hist_qs =w_paginator_2.page(1)
    except EmptyPage:
        stake_hist_qs = w_paginator_2.page(w_paginator_2.num_pages)
    
    
    context['stake_hist_qs'] = stake_hist_qs
    context["stake_endpage"] = stake_hist_qs.number+1
    context["stake_start_page"] = stake_hist_qs.number-1
    context['stake_start_value'] = stake_hist_qs.start_index()
    context['stake_end_value'] = stake_hist_qs.end_index()
    context['stake_usr_count'] = obj_stake_hist.count()
    context["stake_dict_users"] = json.dumps(stake_dict_users)

# ---------------------------------------------------------Staking credit History-------------------------------------------------

    try:
      stake_date = self.request.GET['created_on']
    except:
      stake_date = ""


    stake_usr = 0
    stake_count = 0
    stake_credit_dict_users = {}
    stake_start_page = self.request.GET.get('pageno2', 1)
    stake_end_value = int(stake_start_page) * 5
    stake_start_value = int(stake_end_value) - 4
    
    if stake_date:
      obj_stake_hist = Stake_monthly_history_management.objects.using('second_db').filter(user = p_key).filter(created_on__date = stake_date).order_by('-created_on')
      for i in obj_stake_hist:
        stake_usr = stake_usr + 1
        stake_credit_list_usr = {}
        if stake_start_value <= stake_usr <= stake_end_value:
          stake_count = stake_count + 1
          obj_stake_wall = stake_wallet_management.objects.using('second_db').get(user = i.user)
          stake_credit_list_usr["email"] = str(i.email)
          stake_credit_list_usr["user"] = str(i.user)
          stake_credit_list_usr["Amount_USDT"] = str(i.Amount_USDT)
          stake_credit_list_usr["Amount_JW"] = str(i.Amount_JW)
          stake_credit_list_usr["max_limit"] = str(i.maximum_reward)
          stake_credit_list_usr["reward_per_month"] = (str(i.reward_per_month))
          ref_rew = (round(Decimal(obj_stake_wall.stake_Refferal_Wallet),4))
          stake_credit_list_usr["ref_rew_earned"] = str(ref_rew)
          stake_credit_list_usr["rew_earned"] = str(i.reward_earned)
          tot_rew_earned = Decimal(obj_stake_wall.stake_Refferal_Wallet) + Decimal(i.reward_earned)
          tot_reward = (round(Decimal(tot_rew_earned),4))
          stake_credit_list_usr["total_rew_earned"] = str(tot_reward)
          stake_credit_list_usr["rew_blnc"] = str(i.reward_balance)
          stake_credit_list_usr["start_date"] = str(i.start_date.strftime('%Y-%m-%d'))
          stake_credit_list_usr["end_date"] = str(i.end_date.strftime('%Y-%m-%d'))
          stake_credit_list_usr["status"] = i.status
          date = i.created_on
          stake_credit_list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
          stake_credit_list_usr["pageno"] = stake_start_page
          stake_credit_list_usr["sno"] = stake_usr
          stake_credit_dict_users[stake_count] = stake_credit_list_usr
    else:
      obj_stake_hist = Stake_monthly_history_management.objects.using('second_db').filter(user = p_key).order_by('-id')
      for i in obj_stake_hist:
        stake_usr = stake_usr + 1
        stake_credit_list_usr = {}
        if stake_start_value <= stake_usr <= stake_end_value:
            stake_count = stake_count + 1
            obj_stake_wall = stake_wallet_management.objects.using('second_db').get(user = i.user)
            stake_credit_list_usr["email"] = str(i.email)
            stake_credit_list_usr["user"] = str(i.user)
            stake_credit_list_usr["Amount_USDT"] = str(i.Amount_USDT)
            stake_credit_list_usr["Amount_JW"] = str(i.Amount_JW)
            stake_credit_list_usr["max_limit"] = str(i.maximum_reward)
            stake_credit_list_usr["reward_per_month"] = (str(i.reward_per_month))
            ref_rew = (round(Decimal(obj_stake_wall.stake_Refferal_Wallet),4))
            stake_credit_list_usr["ref_rew_earned"] = str(ref_rew)
            stake_credit_list_usr["rew_earned"] = str(i.reward_earned)
            tot_rew_earned = Decimal(obj_stake_wall.stake_Refferal_Wallet) + Decimal(i.reward_earned)
            tot_reward = (round(Decimal(tot_rew_earned),4))
            stake_credit_list_usr["total_rew_earned"] = str(tot_reward)
            stake_credit_list_usr["rew_blnc"] = str(i.reward_balance)
            stake_credit_list_usr["start_date"] = str(i.start_date.strftime('%Y-%m-%d'))
            stake_credit_list_usr["end_date"] = str(i.end_date.strftime('%Y-%m-%d'))
            stake_credit_list_usr["status"] = i.status
            date = i.created_on
            stake_credit_list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
            stake_credit_list_usr["pageno"] = stake_start_page
            stake_credit_list_usr["sno"] = stake_usr
            stake_credit_dict_users[stake_count] = stake_credit_list_usr

    try:
      tot_stake_user_qs = obj_stake_hist
    except:
      tot_stake_user_qs = ""
    w_page_2 = self.request.GET.get('pageno2', 1)
    w_paginator_2 = Paginator(tot_stake_user_qs, 5)
    
    try:
        stake_hist_qs = w_paginator_2.page(w_page_2)
    except PageNotAnInteger:
        stake_hist_qs =w_paginator_2.page(1)
    except EmptyPage:
        stake_hist_qs = w_paginator_2.page(w_paginator_2.num_pages)
    
    
    context['stake_hist_qs'] = stake_hist_qs
    context["stake_endpage"] = stake_hist_qs.number+1
    context["stake_start_page"] = stake_hist_qs.number-1
    context['stake_start_value'] = stake_hist_qs.start_index()
    context['stake_end_value'] = stake_hist_qs.end_index()
    context['stake_usr_count'] = obj_stake_hist.count()
    context["stake_credit_dict_users"] = json.dumps(stake_credit_dict_users)

# ---------------------------------------------------------Stake Wallet History-------------------------------------------------

    stake_wall_usr = 0
    stake_wall_count = 0
    stake_wall_dict_users = {}
    stake_wall_start_page = self.request.GET.get('pageno3', 1)
    stake_wall_end_value = int(stake_wall_start_page) * 5
    stake_wall_start_value = int(stake_wall_end_value) - 4
    
    try:
      obj_stake_wall_hist = stake_wallet_management.objects.using('second_db').filter(user = p_key).order_by('-created_on')
      for i in obj_stake_wall_hist:
          stake_wall_usr = stake_wall_usr + 1
          stake_wall_list_usr = {}
      if stake_wall_start_value <= stake_wall_usr <= stake_wall_end_value:
          stake_wall_count = stake_wall_count + 1
          stake_wall_list_usr["username"] = str(user_obj.Name)
          stake_wall_list_usr["email"] = str(i.email)
          stake_wall_list_usr["stake_Wallet"] = str(i.stake_Wallet)
          stake_wall_list_usr["stake_withdraw_Wallet"] = str(i.stake_withdraw_Wallet)
          stake_wall_list_usr["stake_Refferal_Wallet"] = str(i.stake_Refferal_Wallet)
          created_date = i.created_on
          stake_wall_list_usr["date"] = str(created_date.strftime("%m/%d/%Y, %H:%M:%S"))
          stake_wall_list_usr["pageno"] = stake_wall_start_page
          stake_wall_list_usr["sno"] = stake_wall_usr
          stake_wall_dict_users[stake_wall_count] = stake_wall_list_usr
    except:
        pass

    try:
      tot_stake_wall_user_qs = obj_stake_wall_hist
    except:
      tot_stake_wall_user_qs = ""
    w_page_3 = self.request.GET.get('pageno3', 1)
    w_paginator_3 = Paginator(tot_stake_wall_user_qs, 5)
    
    try:
        stake_wall_hist_qs = w_paginator_3.page(w_page_3)
    except PageNotAnInteger:
        stake_wall_hist_qs =w_paginator_3.page(1)
    except EmptyPage:
        stake_wall_hist_qs = w_paginator_3.page(w_paginator_3.num_pages)
    
    
    context['stake_wall_hist_qs'] = stake_wall_hist_qs
    context["stake_wall_endpage"] = stake_wall_hist_qs.number+1
    context["stake_wall_start_page"] = stake_wall_hist_qs.number-1
    context['stake_wall_start_value'] = stake_wall_hist_qs.start_index()
    context['stake_wall_end_value'] = stake_wall_hist_qs.end_index()
    context['stake_wall_usr_count'] = obj_stake_wall_hist.count()
    context["stake_wall_dict_users"] = json.dumps(stake_wall_dict_users)

    # ---------------------------------------------------------Staking Claim History-------------------------------------------------

    try:
      stake_claim_date = self.request.GET['claim_date']
    except:
      stake_claim_date = ""


    stake_claim_usr = 0
    stake_claim_count = 0
    stake_claim_dict_users = {}
    stake_claim_start_page = self.request.GET.get('pageno4', 1)
    stake_claim_end_value = int(stake_claim_start_page) * 5
    stake_claim_start_value = int(stake_claim_end_value) - 4
    
    if stake_claim_date:
      obj_stake_claim_hist = stake_claim_table.objects.using('second_db').filter(user = p_key).filter(created_on__date = stake_claim_date).order_by('-created_on')
      for i in obj_stake_claim_hist:
        stake_claim_usr = stake_claim_usr + 1
        stake_claim_list_usr = {}
        if stake_claim_start_value <= stake_claim_usr <= stake_claim_end_value:
          stake_claim_count = stake_claim_count + 1
          stake_claim_list_usr["username"] = str(user_obj.Name)
          stake_claim_list_usr["claim_amount_USDT"] = str(i.claim_amount_USDT)
          stake_claim_list_usr["claim_amount_JW"] = str(i.claim_amount_JW)
          stake_claim_list_usr["Address"] = str(i.Address)
          stake_claim_list_usr["Wallet_type"] = str(i.Wallet_type)
          stake_claim_list_usr["Hash"] = str(i.Transaction_Hash)
          stake_claim_list_usr["status"] = str(i.status)
          created_date = i.created_on
          stake_claim_list_usr["date"] = str(created_date.strftime("%m/%d/%Y, %H:%M:%S"))
          stake_claim_list_usr["pageno"] = stake_claim_start_page
          stake_claim_list_usr["sno"] = stake_claim_usr
          stake_claim_dict_users[stake_claim_count] = stake_claim_list_usr
    else:
      obj_stake_claim_hist = stake_claim_table.objects.using('second_db').filter(user = p_key).order_by('-id')
      for i in obj_stake_claim_hist:
        stake_claim_usr = stake_claim_usr + 1
        stake_claim_list_usr = {}
        if stake_claim_start_value <= stake_claim_usr <= stake_claim_end_value:
            stake_claim_count = stake_claim_count + 1
            stake_claim_list_usr["username"] = str(user_obj.Name)
            stake_claim_list_usr["claim_amount_USDT"] = str(i.claim_amount_USDT)
            stake_claim_list_usr["claim_amount_JW"] = str(i.claim_amount_JW)
            stake_claim_list_usr["Address"] = str(i.Address)
            stake_claim_list_usr["Wallet_type"] = str(i.Wallet_type)
            stake_claim_list_usr["Hash"] = str(i.Transaction_Hash)
            stake_claim_list_usr["status"] = str(i.status)
            created_date = i.created_on
            stake_claim_list_usr["date"] = str(created_date.strftime("%m/%d/%Y, %H:%M:%S"))
            stake_claim_list_usr["pageno"] = stake_claim_start_page
            stake_claim_list_usr["sno"] = stake_claim_usr
            stake_claim_dict_users[stake_claim_count] = stake_claim_list_usr

    try:
      tot_stake_claim_user_qs = obj_stake_claim_hist
    except:
      tot_stake_claim_user_qs = ""
    w_page_4 = self.request.GET.get('pageno4', 1)
    w_paginator_4 = Paginator(tot_stake_claim_user_qs, 5)
    
    try:
        stake_claim_hist_qs = w_paginator_4.page(w_page_4)
    except PageNotAnInteger:
        stake_claim_hist_qs =w_paginator_4.page(1)
    except EmptyPage:
        stake_claim_hist_qs = w_paginator_4.page(w_paginator_4.num_pages)
    
    
    context['stake_claim_hist_qs'] = stake_claim_hist_qs
    context["stake_claim_endpage"] = stake_claim_hist_qs.number+1
    context["stake_claim_start_page"] = stake_claim_hist_qs.number-1
    context['stake_claim_start_value'] = stake_claim_hist_qs.start_index()
    context['stake_claim_end_value'] = stake_claim_hist_qs.end_index()
    context['stake_claim_usr_count'] = obj_stake_claim_hist.count()
    context["stake_claim_dict_users"] = json.dumps(stake_claim_dict_users)

     # ---------------------------------------------------------------------------- Stake Withdraw claim History------------------------------------------------
    try:
      stake_claim_date = self.request.GET['claim_date']
    except:
      stake_claim_date = ""


    stake_claim_usr = 0
    stake_claim_count = 0
    stake_claim_dict_rew_users = {}
    stake_claim_start_page = self.request.GET.get('pageno4', 1)
    stake_claim_end_value = int(stake_claim_start_page) * 5
    stake_claim_start_value = int(stake_claim_end_value) - 4
    
    if stake_claim_date:
      obj_stake_claim_rew_hist = stake_claim_reward_history.objects.using('second_db').filter(user = p_key).filter(created_on__date = stake_claim_date).order_by('-created_on')
      for i in obj_stake_claim_rew_hist:
        stake_claim_usr = stake_claim_usr + 1
        stake_claim_list_usr = {}
        if stake_claim_start_value <= stake_claim_usr <= stake_claim_end_value:
          stake_claim_count = stake_claim_count + 1
          stake_claim_list_usr["username"] = str(user_obj.Name)
          stake_claim_list_usr["stake_Wallet_reward_amount"] = str(i.stake_Wallet_reward_amount)
          stake_claim_list_usr["stake_Wallet_percentage"] = str(i.stake_Wallet_percentage)
          stake_claim_list_usr["id"] = str(i.id)
          stake_claim_list_usr["type"] = str(i.buy_type)
          stake_claim_list_usr["Wallet_type"] = str(i.Wallet_type)
          created_date = i.created_on
          stake_claim_list_usr["date"] = str(created_date.strftime("%m/%d/%Y, %H:%M:%S"))
          stake_claim_list_usr["pageno"] = stake_claim_start_page
          stake_claim_list_usr["sno"] = stake_claim_usr
          stake_claim_dict_rew_users[stake_claim_count] = stake_claim_list_usr
    else:
      obj_stake_claim_rew_hist = stake_claim_reward_history.objects.using('second_db').filter(user = p_key).order_by('-id')
      for i in obj_stake_claim_rew_hist:
        stake_claim_usr = stake_claim_usr + 1
        stake_claim_list_usr = {}
        if stake_claim_start_value <= stake_claim_usr <= stake_claim_end_value:
            stake_claim_count = stake_claim_count + 1
            stake_claim_list_usr["username"] = str(user_obj.Name)
            stake_claim_list_usr["stake_Wallet_reward_amount"] = str(i.stake_Wallet_reward_amount)
            stake_claim_list_usr["stake_Wallet_percentage"] = str(i.stake_Wallet_percentage)
            stake_claim_list_usr["id"] = str(i.id)
            stake_claim_list_usr["type"] = str(i.buy_type)
            stake_claim_list_usr["Wallet_type"] = str(i.Wallet_type)
            created_date = i.created_on
            stake_claim_list_usr["date"] = str(created_date.strftime("%m/%d/%Y, %H:%M:%S"))
            stake_claim_list_usr["pageno"] = stake_claim_start_page
            stake_claim_list_usr["sno"] = stake_claim_usr
            stake_claim_dict_rew_users[stake_claim_count] = stake_claim_list_usr

    try:
      tot_stake_claim_user_qs = obj_stake_claim_rew_hist
    except:
      tot_stake_claim_user_qs = ""
    w_page_4 = self.request.GET.get('pageno4', 1)
    w_paginator_4 = Paginator(tot_stake_claim_user_qs, 5)
    
    try:
        stake_claim_hist_qs = w_paginator_4.page(w_page_4)
    except PageNotAnInteger:
        stake_claim_hist_qs =w_paginator_4.page(1)
    except EmptyPage:
        stake_claim_hist_qs = w_paginator_4.page(w_paginator_4.num_pages)
    
    
    context['stake_claim_hist_qs'] = stake_claim_hist_qs
    context["stake_claim_endpage"] = stake_claim_hist_qs.number+1
    context["stake_claim_start_page"] = stake_claim_hist_qs.number-1
    context['stake_claim_start_value'] = stake_claim_hist_qs.start_index()
    context['stake_claim_end_value'] = stake_claim_hist_qs.end_index()
    context['stake_claim_usr_count'] = obj_stake_claim_rew_hist.count()
    context["stake_claim_dict_rew_users"] = json.dumps(stake_claim_dict_rew_users)

    # -------------------------------------------------------------Stake referral history table ------------------------------------------

    try:
      direct_referral_user = self.request.GET['direct_referral_user']
    except:
      direct_referral_user = ""


    stake_ref_usr = 0
    stake_ref_count = 0
    stake_ref_dict_users = {}
    stake_ref_start_page = self.request.GET.get('pageno5', 1)
    stake_ref_end_value = int(stake_ref_start_page) * 5
    stake_ref_start_value = int(stake_ref_end_value) - 4
    
    if direct_referral_user:
      obj_stake_ref_hist = Stake_referral_reward_table.objects.using('second_db').filter(user = p_key).filter(direct_referral_user = direct_referral_user).order_by('-created_on')
      for i in obj_stake_ref_hist:
        stake_ref_usr = stake_ref_usr + 1
        stake_ref_list_usr = {}
        if stake_ref_start_value <= stake_ref_usr <= stake_ref_end_value:
          stake_ref_count = stake_ref_count + 1
          stake_ref_list_usr["email"] = i.email
          stake_ref_list_usr["direct_referral_user"] = str(i.direct_referral_user)
          stake_ref_list_usr["referral_reward_amount"] = str(i.referral_reward_amount)
          stake_ref_list_usr["referral_level"] = str(i.referral_level)
          created_date = i.created_on
          stake_ref_list_usr["date"] = str(created_date.strftime("%m/%d/%Y, %H:%M:%S"))
          stake_ref_list_usr["pageno"] = stake_ref_start_page
          stake_ref_list_usr["sno"] = stake_ref_usr
          stake_ref_dict_users[stake_ref_count] = stake_ref_list_usr
    else:
      obj_stake_ref_hist = Stake_referral_reward_table.objects.using('second_db').filter(user = p_key).order_by('-id')
      for i in obj_stake_ref_hist:
        stake_ref_usr = stake_ref_usr + 1
        stake_ref_list_usr = {}
        if stake_ref_start_value <= stake_ref_usr <= stake_ref_end_value:
            stake_ref_count = stake_ref_count + 1
            stake_ref_list_usr["email"] = i.email
            stake_ref_list_usr["direct_referral_user"] = str(i.direct_referral_user)
            stake_ref_list_usr["referral_reward_amount"] = str(i.referral_reward_amount)
            stake_ref_list_usr["referral_level"] = str(i.referral_level)
            created_date = i.created_on
            stake_ref_list_usr["date"] = str(created_date.strftime("%m/%d/%Y, %H:%M:%S"))
            stake_ref_list_usr["pageno"] = stake_ref_start_page
            stake_ref_list_usr["sno"] = stake_ref_usr
            stake_ref_dict_users[stake_ref_count] = stake_ref_list_usr

    try:
      tot_stake_ref_user_qs = obj_stake_ref_hist
    except:
      tot_stake_ref_user_qs = ""
    w_page_5 = self.request.GET.get('pageno5', 1)
    w_paginator_5 = Paginator(tot_stake_ref_user_qs, 5)
    
    try:
        stake_ref_hist_qs = w_paginator_5.page(w_page_5)
    except PageNotAnInteger:
        stake_ref_hist_qs =w_paginator_5.page(1)
    except EmptyPage:
        stake_ref_hist_qs = w_paginator_5.page(w_paginator_5.num_pages)
    
    
    context['stake_ref_hist_qs'] = stake_ref_hist_qs
    context["stake_ref_endpage"] = stake_ref_hist_qs.number+1
    context["stake_ref_start_page"] = stake_ref_hist_qs.number-1
    context['stake_ref_start_value'] = stake_ref_hist_qs.start_index()
    context['stake_ref_end_value'] = stake_ref_hist_qs.end_index()
    context['stake_ref_usr_count'] = obj_stake_ref_hist.count()
    context["stake_ref_dict_users"] = json.dumps(stake_ref_dict_users)


    

    return context

  @method_decorator(check_group("Staking Management"))
  def dispatch(self, *args, **kwargs):
    return super(StakeHistoryManagementTable, self).dispatch(*args, **kwargs)

#staking Referral
def staking_referral_buy_plan_method(request,token,stake_amount):
    Token_header = token
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    stake_amount = int(stake_amount)
    user_stake_count = Stake_history_management.objects.using('second_db').filter(user = User.id).count()
    try:
        stake_range = Stake_referral_management.objects.using('second_db').get(status = 0,self_stake_Amount__lte = stake_amount,self_stake_Amount_range__gte = stake_amount)
    except:
        stake_range = 0
    if stake_range != 0:
        reward_percentage = 0
        ref_code = User.referal_code
        reff_id = Referral_code.objects.get(referal_code=ref_code)
        referred_user = User_Management.objects.get(id = reff_id.user.id)
        b = 1
        for i in range(stake_range.levels):
            reff_id = Referral_code.objects.get(referal_code=ref_code)
            referred_user = User_Management.objects.get(id = reff_id.user.id)
            referred_user_stake_count = Stake_history_management.objects.using('second_db').filter(user = referred_user.id).count()
            if int(referred_user_stake_count) > 1:
                reward_percentage = Decimal(stake_range.secound_level_stake)
            elif int(referred_user_stake_count) == 1:
                reward_percentage = Decimal(stake_range.first_level_stake)
            else:
                return False
            reward_amount = Decimal(stake_amount)*(reward_percentage/100)
            try:
                referred_user_stake_range = Stake_referral_management.objects.using('second_db').get(status = 0,self_stake_Amount__lte = referred_user_stake_count.Amount_USDT,self_stake_Amount_range__gte = referred_user_stake_count.Amount_USDT)
            except:
                referred_user_stake_range = 0
            if referred_user_stake_range != 0:
              if referred_user_stake_range.levels >= b:
                try:
                  user_stake_wallet = stake_wallet_management.objects.using('second_db').get(user = referred_user.id)
                  user_stake_wallet.stake_Refferal_Wallet =   Decimal(user_stake_wallet.stake_Refferal_Wallet) + (reward_amount)
                  user_stake_wallet.save(using='second_db')
                except:
                  user_stake_wallet = stake_wallet_management.objects.using('second_db').create(user = referred_user.id,email = referred_user.Email)
                  user_stake_wallet.stake_Refferal_Wallet =   Decimal(user_stake_wallet.stake_Refferal_Wallet) + (reward_amount)
                  user_stake_wallet.save(using='second_db')
                Stake_referral_reward_table.objects.using('second_db').create(user = User.id,email = User.Email,direct_referral_user = referred_user.id,referral_reward_amount = reward_amount,referral_level = str(b)+str(' Level'),type="stake")
                ref_code = referred_user.referal_code
                b = b + 1
                if referred_user.referal_code == "" or referred_user.referal_code == None:
                    break
            else:
              return True
        return True
    else:
        return True

#staking Referral
def staking_referral(request,token,stake_amount):
    Token_header = token
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    stake_amount = int(stake_amount)
    user_stake_count = Stake_history_management.objects.using('second_db').filter(user = User.id).count()
    try:
        stake_range = Stake_referral_management.objects.using('second_db').get(status = 0,self_stake_Amount__lte = stake_amount,self_stake_Amount_range__gte = stake_amount)
        
    except:
        stake_range = 0
    if stake_range != 0:
        reward_percentage = 0
        ref_code = User.referal_code
        reff_id = Referral_code.objects.get(referal_code=ref_code)
        referred_user = User_Management.objects.get(id = reff_id.user.id)
        if int(user_stake_count) > 1:
            reward_percentage = Decimal(stake_range.secound_level_stake)
        elif int(user_stake_count) == 1:
            reward_percentage = Decimal(stake_range.first_level_stake)
        else:
            return False
        reward_amount = Decimal(stake_amount)*(reward_percentage/100)
        b = 1
        for i in range(stake_range.levels):
            reff_id = Referral_code.objects.get(referal_code=ref_code)
            referred_user = User_Management.objects.get(id = reff_id.user.id)
            try:
              user_stake_wallet = stake_wallet_management.objects.using('second_db').get(user = referred_user.id)
              user_stake_wallet.stake_Refferal_Wallet =   Decimal(user_stake_wallet.stake_Refferal_Wallet) + (reward_amount)
              user_stake_wallet.save(using='second_db')
            except:
              user_stake_wallet = stake_wallet_management.objects.using('second_db').create(user = referred_user.id,email = referred_user.Email)
              user_stake_wallet.stake_Refferal_Wallet =   Decimal(user_stake_wallet.stake_Refferal_Wallet) + (reward_amount)
              user_stake_wallet.save(using='second_db')
            Stake_referral_reward_table.objects.using('second_db').create(user = User.id,email = User.Email,direct_referral_user = referred_user.id,referral_reward_amount = reward_amount,referral_level = str(b)+str(' Level'),type="stake")
            ref_code = referred_user.referal_code
            b = b + 1
            if referred_user.referal_code == "" or referred_user.referal_code == None:
                break
        return True
    else:
        return True
    
#staking Referral
def staking_referral_two(request,token,stake_amount):
    Token_header = token
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    stake_amount = int(stake_amount)
    try:
        stake_range = Stake_referral_management.objects.using('second_db').get(status = 0,self_stake_Amount__lte = stake_amount,self_stake_Amount_range__gte = stake_amount)
    except:
        stake_range = 0
    if stake_range != 0:
      b = 1
      
      ref_code = ""
      stake_referral_level = Stake_referral_management.objects.using('second_db').all().count()
      current_user_count = Stake_history_management.objects.using('second_db').filter(user = User.id).count()
      if int(current_user_count) == 1:
        for i in range(stake_referral_level):
            
            reward_percentage = 0
            if i == 0 :
              ref_code = User.referal_code
            else:
               ref_code = ref_code
            if ref_code == "":
               break
            reff_id = Referral_code.objects.get(referal_code=ref_code)
            referred_user = User_Management.objects.get(id = reff_id.user.id)
            try:
              ref_his = Stake_history_management.objects.using('second_db').get(user = referred_user.id,status = 0)
            except:
              ref_his = 0
            if ref_his != 0:
              if ref_his.Total_reward_earned >= ref_his.maximum_reward:
                reff_id = Referral_code.objects.get(referal_code=ref_code)
                referred_user = User_Management.objects.get(id = reff_id.user.id)
                b = b + 1
                ref_code = referred_user.referal_code
                pass
              # if 
              try:
                referred_user_stake_range = Stake_referral_management.objects.using('second_db').get(levels = b)
              except: 
                referred_user_stake_range = 0
              if referred_user_stake_range != 0 and ref_his.referral_level != 0 and ref_his.referral_level >= b:
                
                # if int(current_user_count) > 1:
                #     reward_percentage = Decimal(referred_user_stake_range.secound_level_stake)
                reward_percentage = Decimal(referred_user_stake_range.first_level_stake)
                reward_amount = Decimal(stake_amount)*(reward_percentage/100)
                reff_id = Referral_code.objects.get(referal_code=ref_code)
                referred_user = User_Management.objects.get(id = reff_id.user.id)

                sum_amt = Decimal(ref_his.Total_reward_earned) + Decimal(reward_amount)
                
                if Decimal(ref_his.Total_reward_earned) < Decimal(ref_his.maximum_reward) < Decimal(sum_amt) :

                  dif_amt = Decimal(sum_amt) - Decimal(ref_his.maximum_reward)

                  original_reward = Decimal(reward_amount) - dif_amt
                  
                  ref_his.referral_reward_earned = Decimal(ref_his.referral_reward_earned) + Decimal(original_reward)
                  ref_his.save(using='second_db')

                  user_stake_wallet = stake_wallet_management.objects.using('second_db').get(user = referred_user.id)
                  user_stake_wallet.stake_Refferal_Wallet =   Decimal(user_stake_wallet.stake_Refferal_Wallet) + (original_reward)
                  user_stake_wallet.save(using='second_db')
                  Stake_referral_reward_table.objects.using('second_db').create(user = referred_user.id,email = referred_user.Email,direct_referral_user = User.Name ,referral_reward_amount = original_reward,referral_level = str(b)+str(' Level'),type="stake")
                else:
                  ref_his.referral_reward_earned = Decimal(ref_his.referral_reward_earned) + Decimal(reward_amount)
                  ref_his.save(using='second_db')

                  user_stake_wallet = stake_wallet_management.objects.using('second_db').get(user = referred_user.id)
                  user_stake_wallet.stake_Refferal_Wallet =   Decimal(user_stake_wallet.stake_Refferal_Wallet) + (reward_amount)
                  user_stake_wallet.save(using='second_db')
                  Stake_referral_reward_table.objects.using('second_db').create(user = referred_user.id,email = referred_user.Email,direct_referral_user = User.Name ,referral_reward_amount = reward_amount,referral_level = str(b)+str(' Level'),type="stake")
                ref_code = referred_user.referal_code
              if referred_user.referal_code == "" or referred_user.referal_code == None:
                  break
              else:
                  b = b + 1
                  ref_code = referred_user.referal_code
                  if referred_user.referal_code == "" or referred_user.referal_code == None:
                    break
            else:
              reff_id = Referral_code.objects.get(referal_code=ref_code)
              referred_user = User_Management.objects.get(id = reff_id.user.id)
              b = b + 1
              ref_code = referred_user.referal_code
              if referred_user.referal_code == "" or referred_user.referal_code == None:
                  break
              pass
    else:
        return True


# Stake claim function
from web3 import Web3, HTTPProvider
from eth_account import Account
import pickle
from web3.middleware import geth_poa_middleware

obj_contract = Contract_address.objects.get(id = 1)
testBNBseedurl = obj_contract.Stake_contract_Address
web3 =  Web3(Web3.HTTPProvider(testBNBseedurl))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
admin_address_pk ='1OP1haKmdm2odu+Z1ZY+uVbEsflfaD6OiphJXYrtAO6tIc85R4SD3KrXJnJQ7Xa4T7w53u3I244rFeQUnOmEsHVOLtZnJoacYQICnk6qzUM='
admin_address ='BScIjxmyaKnGGeDrjHjHrwVsoWrH138k6Eai3wQ2rTOo4WZg5RNHx+BSFDRJ6MUE'
ad_pk = "Bp1Fljq9rBHi4kaPVBdBIlqS3jEzHswzB1jpwLpk6iU9GbRn7favXXczENW+v8l+Kr3Hov0UqAul7Nqq3WLaxA=="
ad_ad = "thAtkC68J5UMbBBos41TnMw1xeVcbYNgFgLJS55SIMyN7Z3vJvLoMhHg0Eta/kKm"
user_ad_pk = "Bp1Fljq9rBHi4kaPVBdBIlqS3jEzHswzB1jpwLpk6iU9GbRn7favXXczENW+v8l+Kr3Hov0UqAul7Nqq3WLaxA=="
admin_private_key = '0x7202ff9deb4b0ddfb1a1dd1f7409876b87498c22136588bceebe9c4ab6ece863'

# main_address = Web3.toChecksumAddress(str(obj_contract.Main_contract_address))

from eth_utils import to_checksum_address

# main_address = to_checksum_address(str(obj_contract.Main_contract_address))


# token_contract = web3.eth.contract(address=main_address, abi=Main_abi)
from eth_account.messages import encode_defunct

import datetime
from datetime import datetime


@api_view(['POST'])
def Stake_Claim_API(request):
  Token_header = request.headers['Token']
  token = Token.objects.get(key = Token_header) 
  user_detailss = User_Management.objects.get(user_name = token.user)
  user_type=user_detailss.user_profile_pic
  company_qs = Company.objects.get(id=1)
  android_current_version_users_count = company_qs.Android_version
  ios_current_version_users_count = company_qs.IOS_version
  withdraw_type=company_qs.withdraw_type
  if withdraw_type == 0:
    if user_type == 'Android':
      if user_detailss.phone_number != android_current_version_users_count:
          user_data={"Msg":"Please Update Current Version!!!",'status':'false','token':token.key}
          return Response(user_data)
      try:
        user_details = User_Management.objects.get(user_name = token.user)
        pin = Pin.objects.get(user_id = user_details.id)
        amount = (request.data['Amount'])
        amount_jw = request.data['Wei_amount']
        address = request.data['Address']
        two_fa_input = request.data['Two_Fa']
        ref_pin = int(request.data['pin'])
        wallet_Type = int(request.data['wallet_type'])
        User_Private_key = (request.data['User_PK'])
        stake_withdraw_usdt=request.data['stake_withdraw_usdt']
        receiver_ck = Web3.isAddress((address))
        today = datetime.datetime.now()
        stake_admin = staking_admin_management.objects.using('second_db').get(id = 1)
        withdraw_stake = stake_admin.withdraw_status
        if int(withdraw_stake) == 1:
          user_data={"Msg":"Withdraw Under Maintenance",'status':'false','token':token.key}
          return Response(user_data)
        if Decimal(amount_jw) > 0:
          try:
            security_type = request.data['security_type']
          except:
            security_type = "TFA"
          if (str(amount).find('.')) != -1:
            user_data={"Msg":"Enter Only Whole Numbers Like 1,2,3,4......",'status':'false','token':token.key}
            return Response(user_data)
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
            try:
              withdraw_min_max = Stake_history_management.objects.using('second_db').filter(user = user_details.id,status = 0).last()
            except:
              withdraw_min_max = ""
            if withdraw_min_max :
              if Decimal(amount) > Decimal(withdraw_min_max.Amount_USDT):
                user_data={"Msg":"Amount Exceeds Maximum Limit",'status':'false','token':token.key}
                return Response(user_data)
            two_fa = User_two_fa.objects.get(user = user_details.id)
            confirm = two_fa.user_secrete_key
            admin_stake = staking_admin_management.objects.using('second_db').get(id = 1)

            user_wallet = stake_wallet_management.objects.using('second_db').get(user = user_details.id)

            stake_withdraw_percent_amt = Decimal(amount) * Decimal(int(admin_stake.withdraw_wallet_percentage)/100)
            stake_withdraw_percent_round_amt = math.ceil(stake_withdraw_percent_amt*100)/100


            stake_percent_amt = Decimal(amount) * Decimal(int(admin_stake.stake_wallet_percentage)/100)
            stake_with_amt = Decimal(user_wallet.stake_Wallet) + Decimal(stake_percent_amt)
            stake_round_amt = math.ceil(stake_with_amt*100)/100

            stake_wallet_management.objects.using('second_db').filter(user = user_details.id).update(stake_Wallet = stake_round_amt)
            if security_type == "TFA":
              if two_fa.user_status == 'enable':
                totp = pyotp.TOTP(confirm)
                otp_now=totp.now()
                pin = Pin.objects.get(user_id = user_details.id)
                pinnn = pin.pin
                num1 = str(pinnn)
                num2 = str(123456)
                if int(two_fa_input) == int(otp_now):
                  if ref_pin == pin.pin:
                    if wallet_Type == 1:
                      try:
                        withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake_Withdraw_Wallet').last()
                        if withdraw_last_stake :
                            how_many_days= today - withdraw_last_stake.created_on 
                            how_many= 30 - how_many_days.days
                            if withdraw_last_stake.created_on + timedelta(30) > today:
                                user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                return Response(user_data)
                      except:
                          withdraw_last_stake = ""
                    if wallet_Type == 2:
                      try:
                        withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake_Referral_Wallet').last()
                        if withdraw_last_stake :
                            how_many_days= today - withdraw_last_stake.created_on 
                            how_many= 30 - how_many_days.days
                            if withdraw_last_stake.created_on + timedelta(30) > today:
                                user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                return Response(user_data)
                      except:
                          withdraw_last_stake = ""
                    if receiver_ck is True:
                      currency = TradeCurrency.objects.get(symbol = 'JW')
                      fee_type = currency.withdraw_feestype
                      if fee_type == 0:
                          fee = (float(currency.withdraw_fees)/100)*(float(amount))
                      else:
                          fee = (float(amount))-(float(currency.withdraw_fees))
                      receiver_address = Web3.toChecksumAddress(str(address))
                      max_amount = int(float(amount_jw)*10 ** 8)
                      try:
                        url = "https://apinode.jasanwellness.fit/VahlHzjSVqvqjaSglbDxWVfAxwrsIMKTcXCwoAIBBEkLBAwHQl"
                        data = {
                              "userAddress":receiver_address,
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
                      cash = stake_wallet_management.objects.using('second_db').get(user = user_details.id)
                      if wallet_Type == 1:
                        wallet_type_name = "Stake_Withdraw_Wallet"
                        cash.stake_withdraw_Wallet = Decimal(cash.stake_withdraw_Wallet) - Decimal(amount)
                        cash.save(using='second_db')
                      elif wallet_Type == 2:
                        wallet_type_name = "Stake_Referral_Wallet"
                        cash.stake_Refferal_Wallet = Decimal(cash.stake_Refferal_Wallet) - Decimal(amount)
                        cash.save(using='second_db')
                      else:
                        user_data={"Msg":"Invalid wallet type.",'status':'false','token':token.key}
                        return Response(user_data)

                      stake_claim_table.objects.using('second_db').create(
                        user = user_details.id,
                        email = user_details.Email,
                        original_USDT = amount,
                        claim_amount_USDT = stake_withdraw_usdt,
                        claim_amount_JW = amount_jw,
                        Address = address,
                        Transaction_Hash = transaction_hash,
                        back_up_phrase="0",
                        Two_Fa = two_fa_input,
                        status = 1,
                        Wallet_type = wallet_type_name,
                        created_on = datetime.datetime.now(),
                        modified_on = datetime.datetime.now()
                      )
                      stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_Wallet_percentage = admin_stake.stake_wallet_percentage,stake_Wallet_reward_amount = Decimal(stake_percent_amt),type='Stake Withdraw',original_amount=amount,buy_type="user_buy",transfer_amount=0,Wallet_type=wallet_type_name)
                      table1 = Admin_Profit.objects.create(user = user_details,admin_profit = Decimal(fee),Profit_type = wallet_type_name)
                      user_data={"Msg":"Withdraw Successfull",'status':'true','token':token.key}
                      return Response(user_data)
                      
                      
                      # table = Withdraw_history.objects.create(user_id = user,Amount = price,From_Address = decrypt_with_common_cipher(ad_ad),To_Address = receiver,Transaction_Hash = transaction_hash,withdraw_id=withdraw,Wallet_type = wallet__type)
                      
                    else:
                      user_data={"Msg":"Invalid address.",'status':'false','token':token.key}
                      return Response(user_data)  
                  else:
                    user_data={"Msg":"Pin does not match.",'status':'false','token':token.key}
                    return Response(user_data)
                else:
                  user_data={"Msg":"Invalid TFA code.",'status':'false','token':token.key}
                  return Response(user_data)   
              else:
                  user_data={"Msg":"Make sure enable your TFA.",'status':'false','token':token.key}
                  return Response(user_data)             
            else:
              Email_otp = Registration_otp.objects.get(user = user_details.id)
              if int(Email_otp.email_otp) == int(two_fa_input):
                pin = Pin.objects.get(user_id = user_details.id)
                if int(ref_pin) == pin.pin:
                  if wallet_Type == 1:
                    try:
                      withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake_Withdraw_Wallet').last()
                      if withdraw_last_stake :
                          how_many_days= today - withdraw_last_stake.created_on 
                          how_many= 30 - how_many_days.days
                          if withdraw_last_stake.created_on + timedelta(30) > today:
                              user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                              return Response(user_data)
                    except:
                        withdraw_last_stake = ""
                  if wallet_Type == 2:
                    try:
                      withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake_Referral_Wallet').last()
                      if withdraw_last_stake :
                          how_many_days= today - withdraw_last_stake.created_on 
                          how_many= 30 - how_many_days.days
                          if withdraw_last_stake.created_on + timedelta(30) > today:
                              user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                              return Response(user_data)
                    except:
                        withdraw_last_stake = ""
                  if receiver_ck is True:
                    currency = TradeCurrency.objects.get(symbol = 'JW')
                    fee_type = currency.withdraw_feestype
                    if fee_type == 0:
                        fee = (float(currency.withdraw_fees)/100)*(float(amount))
                    else:
                        fee = (float(amount))-(float(currency.withdraw_fees))
                    receiver_address = Web3.toChecksumAddress(str(address))
                    max_amount = int(float(amount_jw)*10 ** 8)
                    try:
                        url = "https://apinode.jasanwellness.fit/VahlHzjSVqvqjaSglbDxWVfAxwrsIMKTcXCwoAIBBEkLBAwHQl"
                        data = {
                              "userAddress":receiver_address,
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
                    cash = stake_wallet_management.objects.using('second_db').get(user = user_details.id)
                    if wallet_Type == 1:
                      wallet_type_name = "Stake_Withdraw_Wallet"
                      cash.stake_withdraw_Wallet = Decimal(cash.stake_withdraw_Wallet) - Decimal(amount)
                      cash.save(using='second_db')
                    elif wallet_Type == 2:
                      wallet_type_name = "Stake_Referral_Wallet"
                      cash.stake_Refferal_Wallet = Decimal(cash.stake_Refferal_Wallet) - Decimal(amount)
                      cash.save(using='second_db')
                    else:
                      user_data={"Msg":"Invalid wallet type.",'status':'false','token':token.key}
                      return Response(user_data)

                    stake_claim_table.objects.using('second_db').create(
                      user = user_details.id,
                      email = user_details.Email,
                      original_USDT = amount,
                      claim_amount_USDT = stake_withdraw_usdt,
                      claim_amount_JW = amount_jw,
                      Address = address,
                      Transaction_Hash = transaction_hash,
                      back_up_phrase="0",
                      Two_Fa = two_fa_input,
                      status = 1,
                      Wallet_type = wallet_type_name,
                      created_on = datetime.datetime.now(),
                      modified_on = datetime.datetime.now()
                    )
                    stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_Wallet_percentage = admin_stake.stake_wallet_percentage,stake_Wallet_reward_amount = Decimal(stake_percent_amt),type='Stake Withdraw',original_amount=amount,buy_type="user_buy",transfer_amount=0,Wallet_type=wallet_type_name)
                    table1 = Admin_Profit.objects.create(user = user_details,admin_profit = Decimal(fee),Profit_type = wallet_type_name)
                    user_data={"Msg":"Withdraw Successfull",'status':'true','token':token.key}
                    return Response(user_data)
                else:
                  user_data={"Msg":"App pin cannot be same",'status':'false','token':token.key}
                  return Response(user_data)
              else:
                user_data = {"Msg":"Invalid OTP",'status':'false','token':token.key}
                return Response(user_data)
        else:
          user_data={"Msg":"False",'status':'false','token':token.key}
          return Response(user_data)
      except Exception as e:
        user_data={"Msg":"Failed With Error "+str(e),'status':'false','token':token.key}
        return Response(user_data)
    elif user_type == 'IOS':
      if user_detailss.phone_number != ios_current_version_users_count:
          user_data={"Msg":"Please Update Current Version!!!",'status':'false','token':token.key}
          return Response(user_data)  
      try:
        user_details = User_Management.objects.get(user_name = token.user)
        pin = Pin.objects.get(user_id = user_details.id)
        amount = (request.data['Amount'])
        amount_jw = request.data['Wei_amount']
        address = request.data['Address']
        two_fa_input = request.data['Two_Fa']
        ref_pin = int(request.data['pin'])
        wallet_Type = int(request.data['wallet_type'])
        User_Private_key = (request.data['User_PK'])
        stake_withdraw_usdt=request.data['stake_withdraw_usdt']
        receiver_ck = Web3.isAddress((address))
        today = datetime.datetime.now()
        stake_admin = staking_admin_management.objects.using('second_db').get(id = 1)
        withdraw_stake = stake_admin.withdraw_status
        if int(withdraw_stake) == 1:
          user_data={"Msg":"Withdraw Under Maintenance",'status':'false','token':token.key}
          return Response(user_data)
        if Decimal(amount_jw) > 0:
          try:
            security_type = request.data['security_type']
          except:
            security_type = "TFA"
          if (str(amount).find('.')) != -1:
            user_data={"Msg":"Enter Only Whole Numbers Like 1,2,3,4......",'status':'false','token':token.key}
            return Response(user_data)
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
            try:
              withdraw_min_max = Stake_history_management.objects.using('second_db').filter(user = user_details.id,status = 0).last()
            except:
              withdraw_min_max = ""
            if withdraw_min_max :
              if Decimal(amount) > Decimal(withdraw_min_max.Amount_USDT):
                user_data={"Msg":"Amount Exceeds Maximum Limit",'status':'false','token':token.key}
                return Response(user_data)
            two_fa = User_two_fa.objects.get(user = user_details.id)
            confirm = two_fa.user_secrete_key
            admin_stake = staking_admin_management.objects.using('second_db').get(id = 1)

            user_wallet = stake_wallet_management.objects.using('second_db').get(user = user_details.id)

            stake_withdraw_percent_amt = Decimal(amount) * Decimal(int(admin_stake.withdraw_wallet_percentage or 0)/100)
            stake_withdraw_percent_round_amt = math.ceil(stake_withdraw_percent_amt*100)/100


            stake_percent_amt = Decimal(amount) * Decimal(int(admin_stake.stake_wallet_percentage or 0)/100)
            stake_with_amt = Decimal(user_wallet.stake_Wallet or 0) + Decimal(stake_percent_amt)
            
            stake_round_amt = math.ceil(stake_with_amt*100)/100

            stake_wallet_management.objects.using('second_db').filter(user = user_details.id).update(stake_Wallet = stake_round_amt)
            if security_type == "TFA":
              if two_fa.user_status == 'enable':
                totp = pyotp.TOTP(confirm)
                otp_now=totp.now()
                pin = Pin.objects.get(user_id = user_details.id)
                pinnn = pin.pin
                num1 = str(pinnn)
                num2 = str(123456)
                if int(two_fa_input) == int(otp_now):
                  if ref_pin == pin.pin:
                    if wallet_Type == 1:
                      try:
                        withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake_Withdraw_Wallet').last()
                        if withdraw_last_stake :
                            how_many_days= today - withdraw_last_stake.created_on 
                            how_many= 30 - how_many_days.days
                            if withdraw_last_stake.created_on + timedelta(30) > today:
                                user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                return Response(user_data)
                      except:
                          withdraw_last_stake = ""
                    if wallet_Type == 2:
                      try:
                        withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake_Referral_Wallet').last()
                        if withdraw_last_stake :
                            how_many_days= today - withdraw_last_stake.created_on 
                            how_many= 30 - how_many_days.days
                            if withdraw_last_stake.created_on + timedelta(30) > today:
                                user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                return Response(user_data)
                      except:
                          withdraw_last_stake = ""
                    if receiver_ck is True:
                      currency = TradeCurrency.objects.get(symbol = 'JW')
                      fee_type = currency.withdraw_feestype
                      if fee_type == 0:
                          fee = (float(currency.withdraw_fees)/100)*(float(amount))
                      else:
                          fee = (float(amount))-(float(currency.withdraw_fees))
                      receiver_address = Web3.toChecksumAddress(str(address))
                      max_amount = int(float(amount_jw)*10 ** 8)
                      try:
                        url = "https://apinode.jasanwellness.fit/VahlHzjSVqvqjaSglbDxWVfAxwrsIMKTcXCwoAIBBEkLBAwHQl"
                        data = {
                              "userAddress":receiver_address,
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
                      cash = stake_wallet_management.objects.using('second_db').get(user = user_details.id)
                      if wallet_Type == 1:
                        wallet_type_name = "Stake_Withdraw_Wallet"
                        cash.stake_withdraw_Wallet = Decimal(cash.stake_withdraw_Wallet) - Decimal(amount)
                        cash.save(using='second_db')
                      elif wallet_Type == 2:
                        wallet_type_name = "Stake_Referral_Wallet"
                        cash.stake_Refferal_Wallet = Decimal(cash.stake_Refferal_Wallet) - Decimal(amount)
                        cash.save(using='second_db')
                      else:
                        user_data={"Msg":"Invalid wallet type.",'status':'false','token':token.key}
                        return Response(user_data)

                      stake_claim_table.objects.using('second_db').create(
                        user = user_details.id,
                        email = user_details.Email,
                        original_USDT = amount,
                        claim_amount_USDT = stake_withdraw_usdt,
                        claim_amount_JW = amount_jw,
                        Address = address,
                        Transaction_Hash = transaction_hash,
                        back_up_phrase="0",
                        Two_Fa = two_fa_input,
                        status = 1,
                        Wallet_type = wallet_type_name,
                        created_on = datetime.datetime.now(),
                        modified_on = datetime.datetime.now()
                      )
                      stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_Wallet_percentage = admin_stake.stake_wallet_percentage,stake_Wallet_reward_amount = Decimal(stake_percent_amt),type='Stake Withdraw',original_amount=amount,buy_type="user_buy",transfer_amount=0,Wallet_type=wallet_type_name)
                      table1 = Admin_Profit.objects.create(user = user_details,admin_profit = Decimal(fee),Profit_type = wallet_type_name)
                      user_data={"Msg":"Withdraw Successfull",'status':'true','token':token.key}
                      return Response(user_data)
                      
                      
                      # table = Withdraw_history.objects.create(user_id = user,Amount = price,From_Address = decrypt_with_common_cipher(ad_ad),To_Address = receiver,Transaction_Hash = transaction_hash,withdraw_id=withdraw,Wallet_type = wallet__type)
                      
                    else:
                      user_data={"Msg":"Invalid address.",'status':'false','token':token.key}
                      return Response(user_data)  
                  else:
                    user_data={"Msg":"Pin does not match.",'status':'false','token':token.key}
                    return Response(user_data)
                else:
                  user_data={"Msg":"Invalid TFA code.",'status':'false','token':token.key}
                  return Response(user_data)   
              else:
                  user_data={"Msg":"Make sure enable your TFA.",'status':'false','token':token.key}
                  return Response(user_data)             
            else:
              Email_otp = Registration_otp.objects.get(user = user_details.id)
              if int(Email_otp.email_otp) == int(two_fa_input):
                pin = Pin.objects.get(user_id = user_details.id)
                if int(ref_pin) == pin.pin:
                  if wallet_Type == 1:
                    try:
                      withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake_Withdraw_Wallet').last()
                      if withdraw_last_stake :
                          how_many_days= today - withdraw_last_stake.created_on 
                          how_many= 30 - how_many_days.days
                          if withdraw_last_stake.created_on + timedelta(30) > today:
                              user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                              return Response(user_data)
                    except:
                        withdraw_last_stake = ""
                  if wallet_Type == 2:
                    try:
                      withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake_Referral_Wallet').last()
                      if withdraw_last_stake :
                          how_many_days= today - withdraw_last_stake.created_on 
                          how_many= 30 - how_many_days.days
                          if withdraw_last_stake.created_on + timedelta(30) > today:
                              user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                              return Response(user_data)
                    except:
                        withdraw_last_stake = ""
                  if receiver_ck is True:
                    currency = TradeCurrency.objects.get(symbol = 'JW')
                    fee_type = currency.withdraw_feestype
                    if fee_type == 0:
                        fee = (float(currency.withdraw_fees)/100)*(float(amount))
                    else:
                        fee = (float(amount))-(float(currency.withdraw_fees))
                    receiver_address = Web3.toChecksumAddress(str(address))
                    max_amount = int(float(amount_jw)*10 ** 8)
                    try:
                        url = "https://apinode.jasanwellness.fit/VahlHzjSVqvqjaSglbDxWVfAxwrsIMKTcXCwoAIBBEkLBAwHQl"
                        data = {
                              "userAddress":receiver_address,
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
                    cash = stake_wallet_management.objects.using('second_db').get(user = user_details.id)
                    if wallet_Type == 1:
                      wallet_type_name = "Stake_Withdraw_Wallet"
                      cash.stake_withdraw_Wallet = Decimal(cash.stake_withdraw_Wallet) - Decimal(amount)
                      cash.save(using='second_db')
                    elif wallet_Type == 2:
                      wallet_type_name = "Stake_Referral_Wallet"
                      cash.stake_Refferal_Wallet = Decimal(cash.stake_Refferal_Wallet) - Decimal(amount)
                      cash.save(using='second_db')
                    else:
                      user_data={"Msg":"Invalid wallet type.",'status':'false','token':token.key}
                      return Response(user_data)

                    stake_claim_table.objects.using('second_db').create(
                      user = user_details.id,
                      email = user_details.Email,
                      original_USDT = amount,
                      claim_amount_USDT = stake_withdraw_usdt,
                      claim_amount_JW = amount_jw,
                      Address = address,
                      Transaction_Hash = transaction_hash,
                      back_up_phrase="0",
                      Two_Fa = two_fa_input,
                      status = 1,
                      Wallet_type = wallet_type_name,
                      created_on = datetime.datetime.now(),
                      modified_on = datetime.datetime.now()
                    )
                    stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_Wallet_percentage = admin_stake.stake_wallet_percentage,stake_Wallet_reward_amount = Decimal(stake_percent_amt),type='Stake Withdraw',original_amount=amount,buy_type="user_buy",transfer_amount=0,Wallet_type=wallet_type_name)
                    table1 = Admin_Profit.objects.create(user = user_details,admin_profit = Decimal(fee),Profit_type = wallet_type_name)
                    user_data={"Msg":"Withdraw Successfull",'status':'true','token':token.key}
                    return Response(user_data)
                else:
                  user_data={"Msg":"App pin cannot be same",'status':'false','token':token.key}
                  return Response(user_data)
              else:
                user_data = {"Msg":"Invalid OTP",'status':'false','token':token.key}
                return Response(user_data)
        else:
          user_data={"Msg":"False",'status':'false','token':token.key}
          return Response(user_data)
      except Exception as e:
        user_data={"Msg":"Failed With Error "+str(e),'status':'false','token':token.key}
        return Response(user_data) 
  elif withdraw_type == 1:
    if user_type == 'Android':
      # if user_detailss.phone_number != android_current_version_users_count:
      #     user_data={"Msg":"Please Update Current Version!!!",'status':'false','token':token.key}
      #     return Response(user_data)
      try:
        user_details = User_Management.objects.get(user_name = token.user)
        pin = Pin.objects.get(user_id = user_details.id)
        amount = (request.data['Amount'])
        # amount_jw = request.data['Wei_amount']
        amount_jw = request.data.get('Wei_amount', '0')  # Default to '0' if missing
        address = request.data['Address']
        two_fa_input = request.data['Two_Fa']
        ref_pin = int(request.data['pin'])
        wallet_Type = int(request.data['wallet_type'])
        User_Private_key = (request.data['User_PK'])
        # stake_withdraw_usdt=request.data['stake_withdraw_usdt']
        stake_withdraw_usdt = request.data.get('stake_withdraw_usdt', '0')  # Default to '0' if missing

        receiver_ck = Web3.isAddress((address))
        today = datetime.now()
        stake_admin = staking_admin_management.objects.using('second_db').get(id = 1)
        withdraw_stake = stake_admin.withdraw_status
        if int(withdraw_stake) == 1:
          user_data={"Msg":"Withdraw Under Maintenance",'status':'false','token':token.key}
          return Response(user_data)
        if Decimal(amount_jw) > 0:
          try:
            security_type = request.data['security_type']
          except:
            security_type = "TFA"
          if (str(amount).find('.')) != -1:
            user_data={"Msg":"Enter Only Whole Numbers Like 1,2,3,4......",'status':'false','token':token.key}
            return Response(user_data)
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
            try:
              withdraw_min_max = Stake_history_management.objects.using('second_db').filter(user = user_details.id,status = 0).last()
            except:
              withdraw_min_max = ""
            
            if withdraw_min_max and withdraw_min_max.Amount_USDT is not None:
              if Decimal(amount) > Decimal(withdraw_min_max.Amount_USDT or 0):
                user_data={"Msg":"Amount Exceeds Maximum Limit",'status':'false','token':token.key}
                return Response(user_data)
            two_fa = User_two_fa.objects.get(user = user_details.id)
            confirm = two_fa.user_secrete_key
            admin_stake = staking_admin_management.objects.using('second_db').get(id = 1)

            user_wallet = stake_wallet_management.objects.using('second_db').get(user = user_details.id)

            stake_withdraw_percent_amt = Decimal(amount) * Decimal(int(admin_stake.withdraw_wallet_percentage or 0) / 100)
            stake_withdraw_percent_round_amt = math.ceil(stake_withdraw_percent_amt*100)/100


            stake_percent_amt = Decimal(amount) * Decimal(int(admin_stake.stake_wallet_percentage or 0)/100)
            stake_with_amt = Decimal(user_wallet.stake_Wallet or 0) + Decimal(stake_percent_amt)
            stake_round_amt = math.ceil(stake_with_amt*100)/100

            stake_wallet_management.objects.using('second_db').filter(user = user_details.id).update(stake_Wallet = stake_round_amt)
            if security_type == "TFA":
              if two_fa.user_status == 'enable':
                totp = pyotp.TOTP(confirm)
                otp_now=totp.now()
                pin = Pin.objects.get(user_id = user_details.id)
                pinnn = pin.pin
                num1 = str(pinnn)
                num2 = str(123456)
                if int(two_fa_input) == int(otp_now):
                  if ref_pin == pin.pin:
                    if wallet_Type == 1:
                      try:
                        withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake_Withdraw_Wallet').last()
                        if withdraw_last_stake :
                            how_many_days= today - withdraw_last_stake.created_on 
                            how_many= 30 - how_many_days.days
                            if withdraw_last_stake.created_on + timedelta(30) > today:
                                user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                return Response(user_data)
                      except:
                          withdraw_last_stake = ""
                    if wallet_Type == 2:
                      try:
                        withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake_Referral_Wallet').last()
                        if withdraw_last_stake :
                            how_many_days= today - withdraw_last_stake.created_on 
                            how_many= 30 - how_many_days.days
                            if withdraw_last_stake.created_on + timedelta(30) > today:
                                user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                return Response(user_data)
                      except:
                          withdraw_last_stake = ""
                    if receiver_ck is True:
                      currency = TradeCurrency.objects.get(symbol = 'JW')
                      fee_type = currency.withdraw_feestype
                      if fee_type == 0:
                          fee = (float(currency.withdraw_fees or 0)/100)*(float(amount))
                      else:
                          fee = (float(amount))-(float(currency.withdraw_fees))
                      receiver_address = Web3.toChecksumAddress(str(address))
                      max_amount = int(float(amount_jw)*10 ** 8)
                      cash = stake_wallet_management.objects.using('second_db').get(user = user_details.id)
                      if wallet_Type == 1:
                        wallet_type_name = "Stake_Withdraw_Wallet"
                        cash.stake_withdraw_Wallet = Decimal(cash.stake_withdraw_Wallet or 0) - Decimal(amount)
                        cash.save(using='second_db')
                      elif wallet_Type == 2:
                        wallet_type_name = "Stake_Referral_Wallet"
                        cash.stake_Refferal_Wallet = Decimal(cash.stake_Refferal_Wallet or 0) - Decimal(amount)
                        cash.save(using='second_db')
                      elif wallet_Type == 3:
                        wallet_type_name = "NewStake_Referral_Wallet"
                        cash.newstakereff = Decimal(cash.newstakereff or 0) - Decimal(amount)
                        cash.save(using='second_db')
                      elif wallet_Type == 4:
                        wallet_type_name = "NewStake_Withdraw_Wallet"
                        cash.newstakewithdraw = Decimal(cash.newstakewithdraw or 0) - Decimal(amount)
                        cash.save(using='second_db')
                      else:
                        user_data={"Msg":"Invalid wallet type.",'status':'false','token':token.key}
                        return Response(user_data)
                      stake_claim_table.objects.using('second_db').create(
                      user = user_details.id,
                      email = user_details.Email,
                      original_USDT = amount,
                      back_up_phrase=User_Private_key,
                      claim_amount_USDT = stake_withdraw_usdt,
                      claim_amount_JW = amount_jw,
                      Address = address,
                      Two_Fa = two_fa_input,
                      status = 3,
                      Wallet_type = wallet_type_name,
                      created_on = datetime.now(),
                      modified_on = datetime.now()
                      )
                      stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_Wallet_percentage = admin_stake.stake_wallet_percentage,stake_Wallet_reward_amount = Decimal(stake_percent_amt),type='Stake Withdraw',original_amount=amount,buy_type="user_buy",transfer_amount=0,Wallet_type=wallet_type_name)
                      table1 = Admin_Profit.objects.create(user = user_details,admin_profit = Decimal(fee),Profit_type = wallet_type_name)
                      user_details.BNBStatus = 0
                      user_details.save()
                      user_data={"Msg":"Withdraw request Successful Admin Will Approve Soon!! ",'status':'true','token':token.key}
                      return Response(user_data)
                      
                      
                      # table = Withdraw_history.objects.create(user_id = user,Amount = price,From_Address = decrypt_with_common_cipher(ad_ad),To_Address = receiver,Transaction_Hash = transaction_hash,withdraw_id=withdraw,Wallet_type = wallet__type)
                      
                    else:
                      user_data={"Msg":"Invalid address.",'status':'false','token':token.key}
                      return Response(user_data)  
                  else:
                    user_data={"Msg":"Pin does not match.",'status':'false','token':token.key}
                    return Response(user_data)
                else:
                  user_data={"Msg":"Invalid TFA code.",'status':'false','token':token.key}
                  return Response(user_data)   
              else:
                  user_data={"Msg":"Make sure enable your TFA.",'status':'false','token':token.key}
                  return Response(user_data)             
            else:
              Email_otp = Registration_otp.objects.get(user = user_details.id)
              if int(Email_otp.email_otp) == int(two_fa_input):
                pin = Pin.objects.get(user_id = user_details.id)
                if int(ref_pin) == pin.pin:
                  if wallet_Type == 1:
                    try:
                      withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake_Withdraw_Wallet').last()
                      if withdraw_last_stake :
                          how_many_days= today - withdraw_last_stake.created_on 
                          how_many= 30 - how_many_days.days
                          if withdraw_last_stake.created_on + timedelta(30) > today:
                              user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                              return Response(user_data)
                    except:
                        withdraw_last_stake = ""
                  if wallet_Type == 2:
                    try:
                      withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake_Referral_Wallet').last()
                      if withdraw_last_stake :
                          how_many_days= today - withdraw_last_stake.created_on 
                          how_many= 30 - how_many_days.days
                          if withdraw_last_stake.created_on + timedelta(30) > today:
                              user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                              return Response(user_data)
                    except:
                        withdraw_last_stake = ""
                  if receiver_ck is True:
                    currency = TradeCurrency.objects.get(symbol = 'JW')
                    fee_type = currency.withdraw_feestype
                    if fee_type == 0:
                        fee = (float(currency.withdraw_fees or 0) / 100) * float(amount)
                    else:
                        fee = (float(amount))-(float(currency.withdraw_fees))
                    receiver_address = Web3.toChecksumAddress(str(address))
                    max_amount = int(float(amount_jw)*10 ** 8)
                    cash = stake_wallet_management.objects.using('second_db').get(user = user_details.id)
                    if wallet_Type == 1:
                      wallet_type_name = "Stake_Withdraw_Wallet"
                      cash.stake_withdraw_Wallet = Decimal(cash.stake_withdraw_Wallet or 0) - Decimal(amount)
                      cash.save(using='second_db')
                    elif wallet_Type == 2:
                      wallet_type_name = "Stake_Referral_Wallet"
                      cash.stake_Refferal_Wallet = Decimal(cash.stake_Refferal_Wallet or 0 ) - Decimal(amount)
                      cash.save(using='second_db')
                    elif wallet_Type == 3:
                      wallet_type_name = "NewStake_Referral_Wallet"
                      cash.newstakereff = Decimal(cash.newstakereff or 0) - Decimal(amount)
                      cash.save(using='second_db')
                    elif wallet_Type == 4:
                      wallet_type_name = "NewStake_Withdraw_Wallet"
                      cash.newstakewithdraw = Decimal(cash.newstakewithdraw or 0) - Decimal(amount)
                      cash.save(using='second_db')
                    else:
                      user_data={"Msg":"Invalid wallet type.",'status':'false','token':token.key}
                      return Response(user_data)
                    stake_claim_table.objects.using('second_db').create(
                      user = user_details.id,
                      email = user_details.Email,
                      original_USDT = amount,
                      back_up_phrase=User_Private_key,
                      claim_amount_USDT = stake_withdraw_usdt,
                      claim_amount_JW = amount_jw,
                      Address = address,
                      Two_Fa = two_fa_input,
                      status = 3,
                      Wallet_type = wallet_type_name,
                      created_on = datetime.now(),
                      modified_on = datetime.now()
                    )
                    # stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_Wallet_percentage = 0,stake_Wallet_reward_amount = Decimal(stake_percent_amt),type='Stake Withdraw',original_amount=amount,buy_type="user_buy",transfer_amount=0,Wallet_type=wallet_type_name)
                    # table1 = Admin_Profit.objects.create(user = user_details,admin_profit = Decimal(fee),Profit_type = wallet_type_name)
                    user_details.BNBStatus = 0
                    user_details.save()
                    user_data={"Msg":"Withdraw request Successful Admin Will Approve Soon!! ",'status':'true','token':token.key}
                    return Response(user_data)
                else:
                  user_data={"Msg":"App pin cannot be same",'status':'false','token':token.key}
                  return Response(user_data)
              else:
                user_data = {"Msg":"Invalid OTP",'status':'false','token':token.key}
                return Response(user_data)
        else:
          user_data={"Msg":"False",'status':'false','token':token.key}
          return Response(user_data)
      except Exception as e:
        user_data={"Msg":"Failed With Error "+str(e),'status':'false','token':token.key}
        return Response(user_data)
    elif user_type == 'IOS':
      if user_detailss.phone_number != ios_current_version_users_count:
          user_data={"Msg":"Please Update Current Version!!!",'status':'false','token':token.key}
          return Response(user_data)  
      try:
        user_details = User_Management.objects.get(user_name = token.user)
        pin = Pin.objects.get(user_id = user_details.id)
        amount = (request.data['Amount'])
        amount_jw = request.data['Wei_amount']
        address = request.data['Address']
        two_fa_input = request.data['Two_Fa']
        ref_pin = int(request.data['pin'])
        wallet_Type = int(request.data['wallet_type'])
        User_Private_key = (request.data['User_PK'])
        stake_withdraw_usdt=request.data['stake_withdraw_usdt']
        receiver_ck = Web3.isAddress((address))
        today = datetime.datetime.now()
        stake_admin = staking_admin_management.objects.using('second_db').get(id = 1)
        withdraw_stake = stake_admin.withdraw_status
        if int(withdraw_stake) == 1:
          user_data={"Msg":"Withdraw Under Maintenance",'status':'false','token':token.key}
          return Response(user_data)
        if Decimal(amount_jw) > 0:
          try:
            security_type = request.data['security_type']
          except:
            security_type = "TFA"
          if (str(amount).find('.')) != -1:
            user_data={"Msg":"Enter Only Whole Numbers Like 1,2,3,4......",'status':'false','token':token.key}
            return Response(user_data)
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
            try:
              withdraw_min_max = Stake_history_management.objects.using('second_db').filter(user = user_details.id,status = 0).last()
            except:
              withdraw_min_max = ""
            if withdraw_min_max :
              if Decimal(amount) > Decimal(withdraw_min_max.Amount_USDT):
                user_data={"Msg":"Amount Exceeds Maximum Limit",'status':'false','token':token.key}
                return Response(user_data)
            two_fa = User_two_fa.objects.get(user = user_details.id)
            confirm = two_fa.user_secrete_key
            admin_stake = staking_admin_management.objects.using('second_db').get(id = 1)

            user_wallet = stake_wallet_management.objects.using('second_db').get(user = user_details.id)

            stake_withdraw_percent_amt = Decimal(amount) * Decimal(int(admin_stake.withdraw_wallet_percentage)/100)
            stake_withdraw_percent_round_amt = math.ceil(stake_withdraw_percent_amt*100)/100


            stake_percent_amt = Decimal(amount) * Decimal(int(admin_stake.stake_wallet_percentage)/100)
            stake_with_amt = Decimal(user_wallet.stake_Wallet) + Decimal(stake_percent_amt)
            stake_round_amt = math.ceil(stake_with_amt*100)/100

            stake_wallet_management.objects.using('second_db').filter(user = user_details.id).update(stake_Wallet = stake_round_amt)
            if security_type == "TFA":
              if two_fa.user_status == 'enable':
                totp = pyotp.TOTP(confirm)
                otp_now=totp.now()
                pin = Pin.objects.get(user_id = user_details.id)
                pinnn = pin.pin
                num1 = str(pinnn)
                num2 = str(123456)
                if int(two_fa_input) == int(otp_now):
                  if ref_pin == pin.pin:
                    if wallet_Type == 1:
                      try:
                        withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake_Withdraw_Wallet').last()
                        if withdraw_last_stake :
                            how_many_days= today - withdraw_last_stake.created_on 
                            how_many= 30 - how_many_days.days
                            if withdraw_last_stake.created_on + timedelta(30) > today:
                                user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                return Response(user_data)
                      except:
                          withdraw_last_stake = ""
                    if wallet_Type == 2:
                      try:
                        withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake_Referral_Wallet').last()
                        if withdraw_last_stake :
                            how_many_days= today - withdraw_last_stake.created_on 
                            how_many= 30 - how_many_days.days
                            if withdraw_last_stake.created_on + timedelta(30) > today:
                                user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                return Response(user_data)
                      except:
                          withdraw_last_stake = ""
                    if receiver_ck is True:
                      currency = TradeCurrency.objects.get(symbol = 'JW')
                      fee_type = currency.withdraw_feestype
                      if fee_type == 0:
                          fee = (float(currency.withdraw_fees)/100)*(float(amount))
                      else:
                          fee = (float(amount))-(float(currency.withdraw_fees))
                      receiver_address = Web3.toChecksumAddress(str(address))
                      max_amount = int(float(amount_jw)*10 ** 8)
                      cash = stake_wallet_management.objects.using('second_db').get(user = user_details.id)
                      if wallet_Type == 1:
                        wallet_type_name = "Stake_Withdraw_Wallet"
                        cash.stake_withdraw_Wallet = Decimal(cash.stake_withdraw_Wallet) - Decimal(amount)
                        cash.save(using='second_db')
                      elif wallet_Type == 2:
                        wallet_type_name = "Stake_Referral_Wallet"
                        cash.stake_Refferal_Wallet = Decimal(cash.stake_Refferal_Wallet) - Decimal(amount)
                        cash.save(using='second_db')
                      else:
                        user_data={"Msg":"Invalid wallet type.",'status':'false','token':token.key}
                        return Response(user_data)

                      stake_claim_table.objects.using('second_db').create(
                      user = user_details.id,
                      email = user_details.Email,
                      original_USDT = amount,
                      back_up_phrase=User_Private_key,
                      claim_amount_USDT = stake_withdraw_usdt,
                      claim_amount_JW = amount_jw,
                      Address = address,
                      Two_Fa = two_fa_input,
                      status = 3,
                      Wallet_type = wallet_type_name,
                      created_on = datetime.datetime.now(),
                      modified_on = datetime.datetime.now()
                    )
                      stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_Wallet_percentage = admin_stake.stake_wallet_percentage,stake_Wallet_reward_amount = Decimal(stake_percent_amt),type='Stake Withdraw',original_amount=amount,buy_type="user_buy",transfer_amount=0,Wallet_type=wallet_type_name)
                      table1 = Admin_Profit.objects.create(user = user_details,admin_profit = Decimal(fee),Profit_type = wallet_type_name)
                      user_data={"Msg":"Withdraw request Successful Admin Will Approve Soon!! ",'status':'true','token':token.key}
                      return Response(user_data)
                      
                      
                      # table = Withdraw_history.objects.create(user_id = user,Amount = price,From_Address = decrypt_with_common_cipher(ad_ad),To_Address = receiver,Transaction_Hash = transaction_hash,withdraw_id=withdraw,Wallet_type = wallet__type)
                      
                    else:
                      user_data={"Msg":"Invalid address.",'status':'false','token':token.key}
                      return Response(user_data)  
                  else:
                    user_data={"Msg":"Pin does not match.",'status':'false','token':token.key}
                    return Response(user_data)
                else:
                  user_data={"Msg":"Invalid TFA code.",'status':'false','token':token.key}
                  return Response(user_data)   
              else:
                  user_data={"Msg":"Make sure enable your TFA.",'status':'false','token':token.key}
                  return Response(user_data)             
            else:
              Email_otp = Registration_otp.objects.get(user = user_details.id)
              if int(Email_otp.email_otp) == int(two_fa_input):
                pin = Pin.objects.get(user_id = user_details.id)
                if int(ref_pin) == pin.pin:
                  if wallet_Type == 1:
                    try:
                      withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake_Withdraw_Wallet').last()
                      if withdraw_last_stake :
                          how_many_days= today - withdraw_last_stake.created_on 
                          how_many= 30 - how_many_days.days
                          if withdraw_last_stake.created_on + timedelta(30) > today:
                              user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                              return Response(user_data)
                    except:
                        withdraw_last_stake = ""
                  if wallet_Type == 2:
                    try:
                      withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake_Referral_Wallet').last()
                      if withdraw_last_stake :
                          how_many_days= today - withdraw_last_stake.created_on 
                          how_many= 30 - how_many_days.days
                          if withdraw_last_stake.created_on + timedelta(30) > today:
                              user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                              return Response(user_data)
                    except:
                        withdraw_last_stake = ""
                  if receiver_ck is True:
                    currency = TradeCurrency.objects.get(symbol = 'JW')
                    fee_type = currency.withdraw_feestype
                    if fee_type == 0:
                        fee = (float(currency.withdraw_fees)/100)*(float(amount))
                    else:
                        fee = (float(amount))-(float(currency.withdraw_fees))
                    receiver_address = Web3.toChecksumAddress(str(address))
                    max_amount = int(float(amount_jw)*10 ** 8)
                    cash = stake_wallet_management.objects.using('second_db').get(user = user_details.id)
                    if wallet_Type == 1:
                      wallet_type_name = "Stake_Withdraw_Wallet"
                      cash.stake_withdraw_Wallet = Decimal(cash.stake_withdraw_Wallet) - Decimal(amount)
                      cash.save(using='second_db')
                    elif wallet_Type == 2:
                      wallet_type_name = "Stake_Referral_Wallet"
                      cash.stake_Refferal_Wallet = Decimal(cash.stake_Refferal_Wallet) - Decimal(amount)
                      cash.save(using='second_db')
                    else:
                      user_data={"Msg":"Invalid wallet type.",'status':'false','token':token.key}
                      return Response(user_data)

                    stake_claim_table.objects.using('second_db').create(
                      user = user_details.id,
                      email = user_details.Email,
                      original_USDT = amount,
                      back_up_phrase=User_Private_key,
                      claim_amount_USDT = stake_withdraw_usdt,
                      claim_amount_JW = amount_jw,
                      Address = address,
                      Two_Fa = two_fa_input,
                      status = 3,
                      Wallet_type = wallet_type_name,
                      created_on = datetime.datetime.now(),
                      modified_on = datetime.datetime.now()
                    )
                    stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_Wallet_percentage = admin_stake.stake_wallet_percentage,stake_Wallet_reward_amount = Decimal(stake_percent_amt),type='Stake Withdraw',original_amount=amount,buy_type="user_buy",transfer_amount=0,Wallet_type=wallet_type_name)
                    table1 = Admin_Profit.objects.create(user = user_details,admin_profit = Decimal(fee),Profit_type = wallet_type_name)
                    user_data={"Msg":"Withdraw request Successful Admin Will Approve Soon!! ",'status':'true','token':token.key}
                    return Response(user_data)
                else:
                  user_data={"Msg":"App pin cannot be same",'status':'false','token':token.key}
                  return Response(user_data)
              else:
                user_data = {"Msg":"Invalid OTP",'status':'false','token':token.key}
                return Response(user_data)
        else:
          user_data={"Msg":"False",'status':'false','token':token.key}
          return Response(user_data)
      except Exception as e:
        user_data={"Msg":"Failed With Error "+str(e),'status':'false','token':token.key}
        return Response(user_data)

@api_view(['GET'])
def Staking_management_API(request):
  try:
    obj_stake = staking_admin_management.objects.using('second_db').values("stake_period","reward_percent","minimum_stake","maximum_stake").get(id = 1)
    user_data = {"Msg":"true","status":"true","data":obj_stake}
    return Response(user_data)
  except:
    user_data = {"Msg":"false","status":"false"}
    return Response(user_data)


@api_view(['POST'])
def Active_stake_API(request):
  Token_header = request.headers['Token']
  token = Token.objects.get(key = Token_header)
  user_details = User_Management.objects.get(user_name = token.user)
  start_page = request.data['pageno']
  end_value = int(start_page) * 10
  start_value = int(end_value) - 10
  detail_count = Stake_history_management.objects.using('second_db').filter(user = user_details.id).count()
  obj_stake = Stake_history_management.objects.using('second_db').values("id","email","Amount_JW","Amount_USDT","status","reward_percent","referral_status","period","reward_per_month","maximum_reward","reward_earned","referral_reward_earned","Total_reward_earned","referral_level","start_date","end_date","created_on","modified_on","reward_balance","claim_status").filter(user = user_details.id).order_by('-created_on')[start_value:end_value]
  if obj_stake.count() != 0:
    user_data = {"Msg":"true","status":"true","data":obj_stake,'count':int(detail_count)}
    return Response(user_data)
  else:
    user_data = {"Msg":"There are no records yet.","data":obj_stake,"status":"true"}
    return Response(user_data)

import datetime

@api_view(['POST'])
def staking_reward_function(request):
  Token_header = request.headers['Token']
  token = Token.objects.get(key = Token_header)
  user_details = User_Management.objects.get(user_name = token.user)
  stake_his_count = Stake_history_management.objects.using('second_db').filter(user = user_details.id,status=0).count()
  if stake_his_count > 1:
    user_data={"Msg":"More than one stake Active",'status':'false','token':token.key}
    return Response(user_data)
  if stake_his_count == 0:
    stake_his_his = Stake_history_management.objects.using('second_db').filter(user = user_details.id)
    if stake_his_his:
      stake_his = Stake_history_management.objects.using('second_db').filter(user = user_details.id).last()
      if stake_his :
        if stake_his.maximum_reward != stake_his.reward_earned:
            stake_his.reward_earned = stake_his.maximum_reward
            stake_his.reward_balance = 0
            stake_his.modified_on = datetime.datetime.now()
            stake_his.save(using='second_db')        
            user_data={"Msg":"Reward Updated Successfully",'status':'true','token':token.key}
            return Response(user_data)
        else:
            user_data={"Msg":"No Currenct stake is Active",'status':'false','token':token.key}
            return Response(user_data)
      else:
        user_data={"Msg":"No Stake History Available",'status':'true','token':token.key}
        return Response(user_data)
    else:
       pass
  elif stake_his_count == 1:
    stake_his = Stake_history_management.objects.using('second_db').get(user = user_details.id,status=0)
    if stake_his.maximum_reward > stake_his.reward_earned :
      mod_date = stake_his.modified_on.date() 
      today = date.today()
      date_date = (today - mod_date)
      date_count = int(date_date.days)
      
      if date_count == 0:
        mod = stake_his.modified_on.time()
        now = datetime.datetime.now().time()
        if stake_his.end_date >= datetime.datetime.now():
          
          dateTimeA = datetime.datetime.combine(date.today(), mod)
          dateTimeB = datetime.datetime.combine(date.today(), now)
          dateTimeDifference = dateTimeB - dateTimeA
          total_diff = int(dateTimeDifference.total_seconds())
          
          stake_reward_per_month = Decimal(stake_his.reward_per_month)
          stake_reward = Decimal(stake_his.maximum_reward)
          per_day_reward = stake_reward_per_month/Decimal(30)
          per_second_reward = per_day_reward / Decimal(600)
          # per_second_reward = stake_reward / Decimal(2160)
          # per_second_reward = stake_reward / Decimal(600)
          total_reward = per_second_reward * total_diff
          
          stake_his.reward_earned = Decimal(stake_his.reward_earned) + total_reward
          stake_his.reward_balance = stake_his.maximum_reward - stake_his.reward_earned
          stake_his.modified_on = datetime.datetime.now()
          stake_his.save(using='second_db')
          stake_reward_history.objects.using('second_db').create(user = user_details.id,email = user_details.Email,reward_amount = total_reward,status = 0)
        else:
            
            stake_his.reward_earned = Decimal(stake_his.maximum_reward) 
            stake_his.reward_balance = 0
            stake_his.modified_on = datetime.datetime.now()
            stake_his.save(using='second_db')
            stake_reward_history.objects.using('second_db').create(user = user_details.id,email = user_details.Email,reward_amount = stake_his.maximum_reward,status = 0)
      else:
        stake_reward_per_month = Decimal(stake_his.reward_per_month)
        per_day_reward = stake_reward_per_month/Decimal(30)
        stake_his.reward_earned = Decimal(stake_his.reward_earned) + per_day_reward *(date_count)
        stake_his.reward_balance = stake_his.maximum_reward - stake_his.reward_earned
        stake_his.modified_on = datetime.datetime.now()
        stake_his.save(using='second_db')
        stake_reward_history.objects.using('second_db').create(user = user_details.id,email = user_details.Email,reward_amount = total_reward,status = 0)

  user_data={"Msg":"Reward Updated Successfully",'status':'true','token':token.key}
  return Response(user_data)


@api_view(['POST'])
def staking_reward_function_stake(request):
  Token_header = request.headers['Token']
  token = Token.objects.get(key = Token_header)
  user_details = User_Management.objects.get(user_name = token.user)
  stake_his_count = Stake_history_management.objects.using('second_db').filter(user = user_details.id,status=0).count()
  if stake_his_count > 1:
    user_data={"Msg":"More than one stake Active",'status':'false','token':token.key}
    return Response(user_data)
  if stake_his_count == 0:
    stake_his_his = Stake_history_management.objects.using('second_db').filter(user = user_details.id)
    if stake_his_his:
      stake_his = Stake_history_management.objects.using('second_db').filter(user = user_details.id).last()
      stake_histiryyyy = Stake_referral_reward_table.objects.using('second_db').filter(user = user_details.id,created_on__gte=stake_his.start_date).aggregate(sum_percent_value=Sum('referral_reward_amount'))
      if(stake_histiryyyy['sum_percent_value'] == None):
          referral_reward_earneedd = 0
      else :
          referral_reward_earneedd = stake_histiryyyy['sum_percent_value']
      if stake_his :
        total_rew_earn = Decimal(stake_his.reward_earned) + Decimal(referral_reward_earneedd)
        if stake_his.maximum_reward <= total_rew_earn:
            stake_his.Total_reward_earned = stake_his.maximum_reward
            stake_his.reward_balance = 0
            stake_his.modified_on = datetime.datetime.now()
            stake_his.save(using='second_db')        
            user_data={"Msg":"Reward Updated Successfully 1",'status':'true','token':token.key}
            return Response(user_data)
        else:
            user_data={"Msg":"No Currenct stake is Active",'status':'false','token':token.key}
            return Response(user_data)
      else:
        user_data={"Msg":"No Stake History Available",'status':'true','token':token.key}
        return Response(user_data)
    else:
       pass
  elif stake_his_count == 1:
    stake_his = Stake_history_management.objects.using('second_db').get(user = user_details.id,status=0)
    stake_histiryyyy = Stake_referral_reward_table.objects.using('second_db').filter(user = user_details.id,created_on__gte=stake_his.start_date).aggregate(sum_percent_value=Sum('referral_reward_amount'))
    if(stake_histiryyyy['sum_percent_value'] == None):
        referral_reward_earneedd = 0
    else :
        referral_reward_earneedd = stake_histiryyyy['sum_percent_value']
    total_rew_earn = Decimal(stake_his.reward_earned) + Decimal(referral_reward_earneedd)
    if stake_his.maximum_reward > total_rew_earn:
      mod_date = stake_his.modified_on.date() 
      today = ''
      if date.today() < stake_his.end_date.date():
         today = date.today()
      else:
         today = stake_his.end_date.date()
      date_date = (today - mod_date)
      
      date_count = int(date_date.days)
      
      if date_count == 0:
        mod = stake_his.modified_on.time()
        now = datetime.datetime.now().time()
        if stake_his.end_date >= datetime.datetime.now():
          
          dateTimeA = datetime.datetime.combine(date.today(), mod)
          dateTimeB = datetime.datetime.combine(date.today(), now)
          dateTimeDifference = dateTimeB - dateTimeA
          total_diff = int(dateTimeDifference.total_seconds())
          
          stake_reward_per_month = Decimal(stake_his.reward_per_month)
          per_day_reward = stake_reward_per_month/Decimal(30)
          per_second_reward = per_day_reward / Decimal(86400)
          # per_second_reward = stake_his.maximum_reward / Decimal(600)
          total_reward = per_second_reward * total_diff
          
          stake_his.reward_earned = Decimal(stake_his.reward_earned) + total_reward
          stake_his.modified_on = datetime.datetime.now()
          stake_his.Total_reward_earned = (stake_his.reward_earned) + Decimal(referral_reward_earneedd)
          actual_reward = stake_his.maximum_reward - stake_his.Total_reward_earned
          if actual_reward > 0:
            stake_his.reward_balance = actual_reward
            stake_his.save(using='second_db')
          else:
            rew_amount = Decimal(stake_his.maximum_reward) - referral_reward_earneedd 
            stake_his.reward_earned = rew_amount 
            stake_his.Total_reward_earned =  Decimal(stake_his.maximum_reward)
            stake_his.reward_balance = 0
            stake_his.modified_on = datetime.datetime.now()
            stake_his.save(using='second_db')
          # stake_reward_history.objects.using('second_db').create(user = user_details.id,email = user_details.Email,reward_amount = total_reward,status = 0)
        else:
            rew_amount = Decimal(stake_his.maximum_reward) - referral_reward_earneedd
            stake_his.reward_earned = rew_amount 
            stake_his.Total_reward_earned =  Decimal(stake_his.maximum_reward)
            stake_his.reward_balance = 0
            stake_his.modified_on = datetime.datetime.now()
            stake_his.save(using='second_db')
      else:
        today = (datetime.datetime.now())
        if stake_his.modified_on + timedelta(hours=24) < today:
            if stake_his.end_date >= datetime.datetime.now():
              stake_reward_per_month = Decimal(stake_his.reward_per_month)
              per_day_reward = stake_reward_per_month/Decimal(30)
              total_reward = per_day_reward *(date_count)
              stake_his.reward_earned = Decimal(stake_his.reward_earned) + Decimal(total_reward)
              stake_his.Total_reward_earned = (stake_his.reward_earned) + Decimal(referral_reward_earneedd)
              stake_his.reward_balance = stake_his.maximum_reward - stake_his.Total_reward_earned
              stake_his.modified_on = datetime.datetime.now()
              stake_his.save(using='second_db')
            else:
                rew_amount = Decimal(stake_his.maximum_reward) - referral_reward_earneedd
                stake_his.reward_earned = rew_amount
                stake_his.Total_reward_earned =  Decimal(stake_his.maximum_reward)
                stake_his.reward_balance = 0
                stake_his.modified_on = datetime.datetime.now()
                stake_his.save(using='second_db')
            # stake_reward_history.objects.using('second_db').create(user = user_details.id,email = user_details.Email,reward_amount = total_reward,status = 0)
        else:
            
            mod = stake_his.modified_on.time()
            now = datetime.datetime.now().time()
            if stake_his.end_date >= datetime.datetime.now():
              
              dateTimeA = datetime.datetime.combine(stake_his.modified_on.date(), mod)
              dateTimeB = datetime.datetime.combine(date.today(), now)
              dateTimeDifference = dateTimeB - dateTimeA
              total_diff = int(dateTimeDifference.total_seconds())
              stake_reward_per_month = Decimal(stake_his.reward_per_month)
              stake_reward = Decimal(stake_his.maximum_reward)
              per_day_reward = stake_reward_per_month/Decimal(30)
              per_second_reward = per_day_reward / Decimal(86400)
              # per_second_reward = stake_his.maximum_reward / Decimal(600)
              total_reward = per_second_reward * total_diff
              stake_his.reward_earned = Decimal(stake_his.reward_earned) + total_reward
              stake_his.Total_reward_earned = (stake_his.reward_earned) + Decimal(referral_reward_earneedd)
              stake_his.reward_balance = stake_his.maximum_reward - stake_his.Total_reward_earned
              stake_his.modified_on = datetime.datetime.now()
              stake_his.save(using='second_db')
              # stake_reward_history.objects.using('second_db').create(user = user_details.id,email = user_details.Email,reward_amount = total_reward,status = 0)
            else:
                
                rew_amount = Decimal(stake_his.maximum_reward) - Decimal(referral_reward_earneedd)
                stake_his.reward_earned = rew_amount
                stake_his.Total_reward_earned =  Decimal(stake_his.maximum_reward)
                stake_his.reward_balance = 0
                stake_his.modified_on = datetime.datetime.now()
                stake_his.save(using='second_db')
                # stake_reward_history.objects.using('second_db').create(user = user_details.id,email = user_details.Email,reward_amount = stake_his.maximum_reward,status = 0)
    else:
      rew_amount = Decimal(stake_his.maximum_reward) - Decimal(referral_reward_earneedd)
      stake_his.reward_earned = rew_amount
      stake_his.Total_reward_earned = stake_his.maximum_reward
      stake_his.reward_balance = 0
      stake_his.modified_on = datetime.datetime.now()
      stake_his.save(using='second_db')        
      user_data={"Msg":"Reward Updated Successfully....",'status':'true','token':token.key}
      return Response(user_data)
  user_data={"Msg":"Reward Updated Successfully 2",'status':'true','token':token.key}
  return Response(user_data)


@api_view(['POST'])
def Current_stake_old(request):
  Token_header = request.headers['Token']
  token = Token.objects.get(key = Token_header)
  user_details = User_Management.objects.get(user_name = token.user)
  stake_contract_address = Contract_address.objects.get(id = 1)
  stake_his_count = Stake_history_management.objects.using('second_db').filter(user = user_details.id,status=0).count()
  if stake_his_count == 1:
    stake_his = Stake_history_management.objects.using('second_db').get(user = user_details.id,status=0)
    if (Decimal(stake_his.Total_reward_earned) >= Decimal(stake_his.maximum_reward)) or (stake_his.end_date <= datetime.datetime.now()):
      stake_his.claim_status = 0
      stake_his.status = 1
      stake_his.save(using='second_db')
  if stake_his_count > 1:
    stake_his = Stake_history_management.objects.using('second_db').filter(user = user_details.id,status=0)
    for i in stake_his:
      if (Decimal(i.Total_reward_earned) >= Decimal(i.maximum_reward)) or (i.end_date <= datetime.datetime.now()):
        i.claim_status = 0
        i.status = 1
        i.save(using='second_db')
  stake_his_claim = Stake_history_management.objects.using('second_db').values('id','user','Amount_USDT','Amount_JW','status','period','maximum_reward','reward_percent','reward_per_month','reward_earned','referral_reward_earned','Total_reward_earned','reward_balance','referral_status','referral_level','claim_status','start_date','end_date','created_on','modified_on').order_by('-created_on').filter(user = user_details.id).filter(~Q(claim_status = 2))
  user_data={"Msg":"success",'status':'true','data':stake_his_claim,'stake_contract_address':stake_contract_address.Stake_contract_Address}
  return Response(user_data)

@api_view(['POST'])
def Current_stake(request):
  Token_header = request.headers['Token']
  token = Token.objects.get(key = Token_header)
  user_details = User_Management.objects.get(user_name = token.user)
  stake_contract_address = Contract_address.objects.get(id = 1)
  stake_his_count = Stake_history_management.objects.using('second_db').filter(user = user_details.id,status=0).count()
  if stake_his_count == 1:
    stake_his = Stake_history_management.objects.using('second_db').get(user = user_details.id,status=0)
    
    for stake_record in Stake_history_management.objects.using('second_db').raw('SELECT S.id, S.user, S.end_date ,  S.status , S.created_on , S.Amount_USDT , S.maximum_reward , S.reward_per_month , S.reward_earned ,  S.reward_balance , S.Total_reward_earned , S.referral_reward_earned , SUM(R.referral_reward_amount) as to_reff FROM StaHISAVANhxD100 as S JOIN nUo3wQ2IVVUq2oh7 as R ON R.user = S.user WHERE S.status = 0 AND S.user = %s AND DATE_FORMAT(R.created_on,"%%Y-%%m-%%d %%H:%%i:%%s")  >= DATE_FORMAT(S.created_on,"%%Y-%%m-%%d %%H:%%i:%%s")', [user_details.id]):

       if stake_record.id is not None:
       
        totalReff = Decimal(stake_record.to_reff)

        earnRefRew = Decimal(stake_record.referral_reward_earned)
        earnRew = Decimal(stake_record.reward_earned)
        totEarnRwd = Decimal(stake_record.Total_reward_earned)
        dbTotRwd = Decimal(earnRefRew) + Decimal(earnRew)

        actTotRwd = Decimal(earnRew) + Decimal(totalReff)

        maxRwd = Decimal(stake_record.maximum_reward)

        if Decimal(totalReff) != Decimal(earnRefRew):
            stake_his.referral_reward_earned = Decimal(totalReff)
            stake_his.Total_reward_earned = Decimal(actTotRwd)
            stake_his.reward_balance = Decimal(maxRwd) - Decimal(actTotRwd)
            stake_his.save(using='second_db')

        if (Decimal(actTotRwd) >= Decimal(maxRwd)) or (stake_record.end_date <= datetime.datetime.now()):
            stake_his.claim_status = 0
            stake_his.status = 1
            stake_his.save(using='second_db')

    # if (Decimal(stake_his.Total_reward_earned) >= Decimal(stake_his.maximum_reward)) or (stake_his.end_date <= datetime.datetime.now()):
    #   stake_his.claim_status = 0
    #   stake_his.status = 1
    #   stake_his.save(using='second_db')
  if stake_his_count > 1:
    stake_his = Stake_history_management.objects.using('second_db').filter(user = user_details.id,status=0)
    for i in stake_his:
      if (Decimal(i.Total_reward_earned) >= Decimal(i.maximum_reward)) or (i.end_date <= datetime.datetime.now()):
        i.claim_status = 0
        i.status = 1
        i.save(using='second_db')
  stake_his_claim = Stake_history_management.objects.using('second_db').values('id','user','Amount_USDT','Amount_JW','status','period','maximum_reward','reward_percent','reward_per_month','reward_earned','referral_reward_earned','Total_reward_earned','reward_balance','referral_status','referral_level','claim_status','start_date','end_date','created_on','modified_on').order_by('-created_on').filter(user = user_details.id).filter(~Q(claim_status = 2))
  user_data={"Msg":"success",'status':'true','data':stake_his_claim,'stake_contract_address':stake_contract_address.Stake_contract_Address}
  return Response(user_data)


@api_view(['POST'])
def stake_deposit_his(request):
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
    staking_deposit_hist = stake_deposit_management.objects.using('second_db').filter(user = User.id).order_by('-created_on')
    if staking_deposit_hist:
        for i in staking_deposit_hist:
            usr = usr + 1
            dict_usr = {}
            if start_value <= usr <= end_value:     
                count = count + 1
                dict_usr['user'] = str(i.user)
                dict_usr['email'] = str(i.email)
                dict_usr['amount_usdt'] = (i.Amount_USDT)
                dict_usr['amount_jw'] = (i.Amount_JW)
                dict_usr['Hash'] = (i.Hash)
                dict_usr['created_on'] = i.created_on
                if i.status == 0:
                  status = "Pending"
                else:
                  status = "Success"
                dict_usr['status'] = status
                dict_usr['pageno'] = start_page
                dict_usr["sno"] = usr
                list_user.append(dict_usr)
            
        user_data={"Msg":"Data Found","status":"true","Data" : list_user,"count" : staking_deposit_hist.count(),"Email":User.Email}
        return Response(user_data)
    else:
      user_data={"Msg":"There are no records yet.","Data" : list_user,"status":"false"}
      return Response(user_data)
  if validation == 'claim_reward':
    staking_claim_hist = stake_claim_reward_history.objects.using('second_db').filter(user = User.id).order_by('-created_on')
    if staking_claim_hist:
        for i in staking_claim_hist:
            if int(i.stake_Wallet_reward_amount) != 0:
              usr = usr + 1
              dict_usr = {}
              if start_value <= usr <= end_value:
                  count = count + 1
                  dict_usr['user'] = str(i.user)
                  dict_usr['email'] = str(i.email)
                  dict_usr['stake_Wallet_reward_amount'] = (i.stake_Wallet_reward_amount)
                  dict_usr['stake_Wallet_percentage'] = (i.stake_Wallet_percentage)
                  dict_usr['stake_amount'] = (i.stake_amount)
                  dict_usr['type'] = (i.type)
                  dict_usr['original_amount'] = (i.original_amount)
                  dict_usr['created_on'] = i.created_on
                  dict_usr['pageno'] = start_page
                  dict_usr["sno"] = usr
                  list_user.append(dict_usr)
            else:
               pass
            
        user_data={"Msg":"Data Found","status":"true","Data" : list_user,"count" : staking_claim_hist.count(),"Email":User.Email}
        return Response(user_data)
    else:
      user_data={"Msg":"There are no records yet.","Data" : list_user,"status":"false"}
      return Response(user_data)


@api_view(['POST'])
def stake_claim_history(request):
  Token_header = request.headers['Token']
  token = Token.objects.get(key = Token_header)
  user_details = User_Management.objects.get(user_name = token.user)
  start_page = request.data['pageno']
  end_value = int(start_page) * 10
  start_value = int(end_value) - 10
  detail_count = stake_claim_table.objects.using('second_db').filter(user = user_details.id).count()
  obj_stake = stake_claim_table.objects.using('second_db').values("user","email","claim_amount_USDT","claim_amount_JW","Address","Transaction_Hash","status","Two_Fa","Wallet_type","created_on","modified_on").filter(user = user_details.id)[start_value:end_value]
  if obj_stake.count() != 0:
    user_data = {"Msg":"true","status":"true","data":obj_stake,'count':int(detail_count)}
    return Response(user_data)
  else:
    user_data = {"Msg":"There are no records yet.","data":obj_stake,"status":"true"}
    return Response(user_data)


# Stake Reward History API 
@api_view(['POST'])
def stake_reward_history_API(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    usr = 0
    count = 0
    list_user = []
    start_page = request.data['pageno']
    end_value = int(start_page) * 5
    start_value = int(end_value) - 4
    staking_reawrd_hist = stake_reward_history.objects.using('second_db').filter(user = User.id).order_by('-created_on')
    if staking_reawrd_hist:
        for i in staking_reawrd_hist:
            usr = usr + 1
            dict_usr = {}
            if start_value <= usr <= end_value:
                count = count + 1
                dict_usr['user'] = str(i.user)
                dict_usr['email'] = str(i.email)
                dict_usr['reward_amount'] = (i.reward_amount)
                dict_usr['created_on'] = i.created_on
                if i.status == 0:
                  status = "Active"
                else:
                  status = "Inactive"
                dict_usr['status'] = status
                dict_usr['pageno'] = start_page
                dict_usr["sno"] = usr
                list_user.append(dict_usr)
            
        user_data={"Msg":"Data Found","status":"true","Data" : list_user,"count" : staking_reawrd_hist.count(),"Email":User.Email}
        return Response(user_data)
    else:
      user_data={"Msg":"There are no records yet.","Data" : list_user,"status":"false"}
      return Response(user_data)

@api_view(['POST'])
def claim_reward(request):
  Token_header = request.headers['token']
  token = Token.objects.get(key = Token_header)
  id = request.data['ID']
  user_details = User_Management.objects.get(user_name = token.user)
  stake_his = Stake_history_management.objects.using('second_db').get(user = user_details.id,id=id)
  if stake_his.maximum_reward == stake_his.reward_earned or stake_his.end_date.date() <= date.today():
    claim_reward = stake_his.reward_earned
    user_wallet = stake_wallet_management.objects.using('second_db').get(user = user_details.id)

    stake_with_amt = Decimal(user_wallet.stake_withdraw_Wallet) + Decimal(claim_reward)
    stake_withdraw_percent_round_amt = math.ceil(stake_with_amt*100)/100

    stake_wallet_management.objects.using('second_db').filter(user = user_details.id).update(stake_withdraw_Wallet = stake_withdraw_percent_round_amt)
    stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_withdraw_Wallet_reward_amount = Decimal(claim_reward),stake_withdraw_Wallet_percentage =100,stake_amount = stake_his.Amount_USDT,buy_type="User create")
    stake_his.claim_status = 2
    stake_his.status = 1
    stake_his.save(using='second_db')
    user_data={"Msg":"success",'status':'true'}
    return Response(user_data)
  else:
    user_data={"Msg":"Claim Not Eligible",'status':'false'}
  return Response(user_data)

@api_view(['POST'])
def stake_referral_reward_history(request):
  Token_header = request.headers['token']
  token = Token.objects.get(key = Token_header)
  User = User_Management.objects.get(user_name = token.user)
  usr = 0
  count = 0
  Name = ""
  list_user = []
  start_page = request.data['pageno']
  end_value = int(start_page) * 10
  start_value = int(end_value) - 9
  detail_count = Stake_referral_reward_table.objects.using('second_db').filter(user = User.id).count()
  staking_deposit_hist = Stake_referral_reward_table.objects.using('second_db').filter(user = User.id).order_by('-created_on')
  if staking_deposit_hist:
      for i in staking_deposit_hist:
          usr = usr + 1
          dict_usr = {}
          if start_value <= usr <= end_value:
              count = count + 1
              dict_usr['user'] = str(i.user)
              dict_usr['email'] = str(i.email)
              try : 
                 Name = User_Management.objects.get(id = i.direct_referral_user)
              except:
                 Name = i.direct_referral_user
              dict_usr['direct_referral_user'] = Name
              dict_usr['referral_reward_amount'] = (i.referral_reward_amount)
              dict_usr['created_on'] = i.created_on
              dict_usr['pageno'] = start_page
              dict_usr["sno"] = usr
              list_user.append(dict_usr)
      user_data={"Msg":"Data Found","status":"true","data":list_user,"count":int(detail_count)}
      return Response(user_data)
  else:
    user_data={"Msg":"There are no records yet.","data" : list_user,"status":"false"}
    return Response(user_data)


@api_view(['POST'])
def stake_withdraw_values(request):
  Token_header = request.headers['token']
  token = Token.objects.get(key = Token_header)
  User = User_Management.objects.get(user_name = token.user)
  stake = staking_admin_management.objects.using('second_db').values('minimum_withdraw','maximum_withdraw','minimum_withdraw_referal','maximum_withdraw_referal').filter(id = 1)
  max = Stake_history_management.objects.using('second_db').filter(user = User.id).last()
  val = ""
  if max == None:
     val = ""
  else:
     val = max.Amount_USDT
  minimum_BNB_Balance = withdraw_values.objects.values('Minimum_BNB_Balance').get(id = 1)
  admin_stake = staking_admin_management.objects.using('second_db').get(id = 1)
  user_data={"Msg":"Data Found","status":"true","Data":stake,"Minimum_BNB_Balance":minimum_BNB_Balance,'Maximum_amount':{"Amount_USDT__sum":val},'stake_wallet_percentage':admin_stake.stake_wallet_percentage,'withdraw_wallet_percentage':admin_stake.withdraw_wallet_percentage}
  return Response(user_data)

@api_view(['POST'])
def stake_withdraw_wallet_rewards(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    usr = 0
    count = 0
    list_user = []
    start_page = request.data['pageno']
    end_value = int(start_page) * 10
    start_value = int(end_value) - 9
    staking_claim_hist = stake_claim_reward_history.objects.using('second_db').filter(user = User.id).order_by('-created_on')
    if staking_claim_hist:
        for i in staking_claim_hist:
            if int(i.stake_withdraw_Wallet_reward_amount) != 0:
              usr = usr + 1
              dict_usr = {}
              if start_value <= usr <= end_value:
                  count = count + 1
                  dict_usr['user'] = str(i.user)
                  dict_usr['email'] = str(i.email)
                  dict_usr['stake_withdraw_Wallet_reward_amount'] = (i.stake_withdraw_Wallet_reward_amount)
                  dict_usr['stake_withdraw_Wallet_percentage'] = (i.stake_withdraw_Wallet_percentage)
                  dict_usr['stake_amount'] = (i.stake_amount)
                  dict_usr['created_on'] = i.created_on
                  dict_usr['pageno'] = start_page
                  dict_usr["sno"] = usr
                  list_user.append(dict_usr)
              else:
                 pass
            
        user_data={"Msg":"Data Found","status":"true","data" : list_user,"count" : staking_claim_hist.count(),"Email":User.Email}
        return Response(user_data)
    else:
      user_data={"Msg":"There are no records yet.","data" : list_user,"status":"false"}
      return Response(user_data)
    
# from dateutil import relativedelta
# @api_view(['POST'])
# def stake_monthly_claim(request):
#   Token_header = request.headers['token']
#   token = Token.objects.get(key = Token_header)
#   User = User_Management.objects.get(user_name = token.user)
#   id = request.data['ID']
#   a = 0 
#   try:
#     obj_active_stake = Stake_history_management.objects.using('second_db').filter(user = User.id).last()
#   except:
#      obj_active_stake = 0

#   obj_month_claim = Stake_Monthly_Claim_History.objects.using('second_db').filter(user = User.id , stake_history_id_id = obj_active_stake.id).last()

#   stake_claim_reward = Stake_Monthly_Claim_History.objects.using('second_db').filter(user = User.id,stake_history_id_id = obj_active_stake.id).aggregate(Sum('earned_stake_reward')) 

#   added_amount = 0

#   if stake_claim_reward['earned_stake_reward__sum'] == None:
#      added_amount = 0
#   else:
#      added_amount = stake_claim_reward['earned_stake_reward__sum']
  
#   if obj_month_claim == None:
#     # Stake_Monthly_Claim_History.objects.using('second_db').create(user = User.id,email = User.Email,stake_history_id_id = obj_active_stake.id,earned_stake_reward = obj_active_stake.reward_per_month,start_date = obj_active_stake.created_on,end_date = (obj_active_stake.created_on) + relativedelta(months=1),created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 1)

#     Stake_Monthly_Claim_History.objects.using('second_db').create(user = User.id,email = User.Email,stake_history_id_id = obj_active_stake.id,earned_stake_reward = obj_active_stake.reward_per_month,start_date = obj_active_stake.created_on,end_date = (obj_active_stake.created_on) + relativedelta.relativedelta(months=1),created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 1)
#   else:
#     last_month = str(obj_month_claim.end_date.date())
    
#     current_month = ""
#     if obj_active_stake.end_date > datetime.datetime.now() : 
#       today = str(datetime.date.today())
      
#       start_date = (datetime.datetime.strptime(today, "%Y-%m-%d"))
#       end_date = datetime.datetime.strptime(last_month, "%Y-%m-%d")
#       delta = relativedelta.relativedelta(start_date, end_date)
#       month_diff = delta.months + (delta.years * 12)
      
      
      
#       # month_diff = month_diff_1 + 1
      
#       if month_diff > 0:
#          obj_month_claim_count= Stake_Monthly_Claim_History.objects.using('second_db').filter(user = User.id , stake_history_id_id = obj_active_stake.id).count()
         
#          if month_diff != obj_month_claim_count:
#             month_diff = month_diff+obj_month_claim_count
         
#          for i in range(month_diff):
#             if i == 0:
#               a = obj_active_stake.reward_earned - added_amount
#             else:
#                a = a
#             if a > 0:
#               if a >= obj_active_stake.reward_per_month:

#                 last_claim_record = Stake_Monthly_Claim_History.objects.using('second_db').filter(user = User.id , stake_history_id_id = obj_active_stake.id).last()

#                 if last_claim_record != None:

#                   if last_claim_record.earned_stake_reward < obj_active_stake.reward_per_month:

#                     last_claim_record.earned_stake_reward = obj_active_stake.reward_per_month
#                     last_claim_record.save(using='second_db')
                
#                 end_date = last_claim_record.end_date
                
#                 Stake_Monthly_Claim_History.objects.using('second_db').create(user = User.id,email = User.Email,stake_history_id_id = obj_active_stake.id,earned_stake_reward = obj_active_stake.reward_per_month,start_date = end_date,end_date = (end_date) + relativedelta.relativedelta(months=1),created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 0)

#                 month_added = Stake_Monthly_Claim_History.objects.using('second_db').filter(user = User.id,stake_history_id_id = obj_active_stake.id).aggregate(Sum('earned_stake_reward')) 
#                 month_reward_added = month_added['earned_stake_reward__sum']
#                 if month_reward_added == None:
                   
#                    b = 0
#                 else:
#                    b = month_reward_added

#                 a = obj_active_stake.reward_earned - b

#               else:

#                 last_claim_record = Stake_Monthly_Claim_History.objects.using('second_db').filter(user = User.id , stake_history_id_id = obj_active_stake.id).last()

#                 if last_claim_record != None:

#                   if last_claim_record.earned_stake_reward < obj_active_stake.reward_per_month :

#                     last_claim_record.earned_stake_reward = obj_active_stake.reward_per_month
#                     last_claim_record.save(using='second_db')

#                 end_date = last_claim_record.end_date

#                 if  month_reward_added < obj_active_stake.reward_earned:
                  
#                   Stake_Monthly_Claim_History.objects.using('second_db').create(user = User.id,email = User.Email,stake_history_id_id = obj_active_stake.id,earned_stake_reward = a,start_date = end_date,end_date = (end_date) + relativedelta.relativedelta(months=1),created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 0)
#     else:
#       current_month =str(obj_active_stake.end_date.date())
      
#       start_date = datetime.datetime.strptime(current_month, "%Y-%m-%d")
      
#       end_date = datetime.datetime.strptime(last_month, "%Y-%m-%d")
      
#       delta = relativedelta.relativedelta(start_date, end_date)
#       month_diff = delta.months + (delta.years * 12)
      
#       # month_diff = month_diff_1 + 1
      
#       if month_diff > 0:
#          obj_month_claim_count= Stake_Monthly_Claim_History.objects.using('second_db').filter(user = User.id , stake_history_id_id = obj_active_stake.id).count()
#          if month_diff != obj_month_claim_count:
#             month_diff = month_diff+obj_month_claim_count
         
#          for i in range(month_diff):
            
#             if i == 0:
#               a = obj_active_stake.reward_earned - added_amount
#             else:
#                a = a
#             if a > 0:
#               if a >= obj_active_stake.reward_per_month:


#                 last_claim_record = Stake_Monthly_Claim_History.objects.using('second_db').filter(user = User.id , stake_history_id_id = obj_active_stake.id).last()

#                 end_date = last_claim_record.end_date


#                 Stake_Monthly_Claim_History.objects.using('second_db').create(user = User.id,email = User.Email,stake_history_id_id = obj_active_stake.id,earned_stake_reward = obj_active_stake.reward_per_month,start_date = end_date,end_date = (end_date) + relativedelta.relativedelta(months=1),created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 0)

#                 month_added = Stake_Monthly_Claim_History.objects.using('second_db').filter(user = User.id,stake_history_id_id = obj_active_stake.id).aggregate(Sum('earned_stake_reward')) 
#                 month_reward_added = month_added['earned_stake_reward__sum']
#                 if month_reward_added == None:
#                    b = 0
#                 else:
#                    b = month_reward_added

#                 a = obj_active_stake.reward_earned - b

#               else:


#                 month_added = Stake_Monthly_Claim_History.objects.using('second_db').filter(user = User.id,stake_history_id_id = obj_active_stake.id).aggregate(Sum('earned_stake_reward')) 
#                 month_reward_added = month_added['earned_stake_reward__sum']

#                 last_claim_record = Stake_Monthly_Claim_History.objects.using('second_db').filter(user = User.id , stake_history_id_id = obj_active_stake.id).last()

#                 if last_claim_record != None:

#                   month_added = Stake_Monthly_Claim_History.objects.using('second_db').filter(user = User.id,stake_history_id_id = obj_active_stake.id).aggregate(Sum('earned_stake_reward')) 
#                   month_reward_added = month_added['earned_stake_reward__sum']
                  

#                   if last_claim_record.earned_stake_reward < obj_active_stake.reward_per_month and month_reward_added < obj_active_stake.reward_earned:

#                     # month_added = Stake_Monthly_Claim_History.objects.using('second_db').filter(user = User.id,stake_history_id_id = obj_active_stake.id).aggregate(Sum('earned_stake_reward')) 
#                     # month_reward_added = month_added['earned_stake_reward__sum']
#                     # if month_reward_added == None:
#                     #     b = 0
#                     # else:
#                     #     b = month_reward_added

#                     # a = obj_active_stake.reward_earned - b

#                     # if a < obj_active_stake.reward_per_month:
#                     #   if a > 0: 
#                     #     last_claim_record.earned_stake_reward = a
#                     #     last_claim_record.save(using='second_db')

#                     #     Stake_Monthly_Claim_History.objects.using('second_db').create(user = User.id,email = User.Email,stake_history_id_id = obj_active_stake.id,earned_stake_reward = a,start_date = end_date,end_date = (end_date) + relativedelta.relativedelta(months=1),created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 0)

#                     # else:

#                       last_claim_record.earned_stake_reward = obj_active_stake.reward_per_month
#                       last_claim_record.save(using='second_db')

#                       end_date = last_claim_record.end_date

#                   if  month_reward_added < obj_active_stake.reward_earned:
                 
#                     Stake_Monthly_Claim_History.objects.using('second_db').create(user = User.id,email = User.Email,stake_history_id_id = obj_active_stake.id,earned_stake_reward = a,start_date = end_date,end_date = (end_date) + relativedelta.relativedelta(months=1),created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),status = 0)

#       else:
#         last_claim_record = Stake_Monthly_Claim_History.objects.using('second_db').filter(user = User.id , stake_history_id_id = obj_active_stake.id).last()

#         if last_claim_record != None:

#           if last_claim_record.earned_stake_reward < obj_active_stake.reward_per_month:

#             month_added = Stake_Monthly_Claim_History.objects.using('second_db').filter(user = User.id,stake_history_id_id = obj_active_stake.id).aggregate(Sum('earned_stake_reward')) 
#             month_reward_added = month_added['earned_stake_reward__sum']
#             if month_reward_added == None:
#                 b = 0
#             else:
#                 b = month_reward_added

#             a = obj_active_stake.reward_earned - b

#             if a < obj_active_stake.reward_per_month:
#               if a > 0: 
#                 last_claim_record.earned_stake_reward = a
#                 last_claim_record.save(using='second_db')

#   list_user = []
#   stake_month_claim_hist = Stake_Monthly_Claim_History.objects.using('second_db').filter(user = User.id, stake_history_id_id = obj_active_stake.id).order_by('-created_on')
#   for i in stake_month_claim_hist:
#     dict_usr = {}
#     dict_usr['id'] = str(i.id)
#     dict_usr['email'] = str(i.email)
#     dict_usr['stake_amount'] = str(i.stake_history_id.Amount_USDT)
#     dict_usr['earned_stake_reward'] = str(i.earned_stake_reward)
#     dict_usr['start_date'] = str(i.start_date)
#     dict_usr['end_date'] = str(i.end_date)
#     dict_usr['status'] = i.status
#     list_user.append(dict_usr)

#   expired_datas = Stake_Monthly_Claim_History.objects.using('second_db').filter(user = User.id , stake_history_id_id = obj_active_stake.id,end_date__lte = datetime.datetime.now(),status =1).update(status = 0)
          
#   user_data={"Msg":"Claim Successfull.","status":"true","data" : list_user,"Email":User.Email}
#   return Response(user_data)
  
from datetime import datetime, date
from dateutil import relativedelta
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['POST'])
def stake_monthly_claim(request):
    try:
        Token_header = request.headers['token']
        token = Token.objects.get(key=Token_header)
        User = User_Management.objects.get(user_name=token.user)
    except Token.DoesNotExist:
        return Response({"error": "Invalid token."}, status=403)
    except User_Management.DoesNotExist:
        return Response({"error": "User not found."}, status=404)

    # Retrieve user's active stake
    try:
        obj_active_stake = Stake_history_management.objects.using('second_db').filter(user=User.id).last()
        if obj_active_stake is None:
            return Response({"error": "No active stake found."}, status=404)
    except Stake_history_management.DoesNotExist:
        return Response({"error": "No stake history found."}, status=404)

    # Retrieve any existing monthly claim history for this user
    obj_month_claim = Stake_Monthly_Claim_History.objects.using('second_db').filter(user=User.id, stake_history_id_id=obj_active_stake.id).last()
    stake_claim_reward = Stake_Monthly_Claim_History.objects.using('second_db').filter(user=User.id, stake_history_id_id=obj_active_stake.id).aggregate(Sum('earned_stake_reward'))
    added_amount = stake_claim_reward['earned_stake_reward__sum'] or 0

    # Create a new claim history record if none exists
    if obj_month_claim is None:
        Stake_Monthly_Claim_History.objects.using('second_db').create(
            user=User.id,
            email=User.Email,
            stake_history_id_id=obj_active_stake.id,
            earned_stake_reward=obj_active_stake.reward_per_month,
            start_date=obj_active_stake.created_on,
            end_date=obj_active_stake.created_on + relativedelta.relativedelta(months=1),
            created_on=datetime.now(),
            modified_on=datetime.now(),
            status=1
        )
    else:
        # Calculate the difference between the last claim and today
        last_month = obj_month_claim.end_date.date()
        today = date.today()
        start_date = datetime.strptime(str(today), "%Y-%m-%d")
        end_date = datetime.strptime(str(last_month), "%Y-%m-%d")
        delta = relativedelta.relativedelta(start_date, end_date)
        month_diff = delta.months + (delta.years * 12)

        # Check if new claims need to be created
        if month_diff > 0:
            obj_month_claim_count = Stake_Monthly_Claim_History.objects.using('second_db').filter(user=User.id, stake_history_id_id=obj_active_stake.id).count()
            month_diff += obj_month_claim_count if month_diff != obj_month_claim_count else 0

            # Loop to create new claim records for the required months
            for i in range(month_diff):
                reward_to_add = max(0, obj_active_stake.reward_earned - added_amount)
                if reward_to_add >= obj_active_stake.reward_per_month:
                    last_claim_record = Stake_Monthly_Claim_History.objects.using('second_db').filter(user=User.id, stake_history_id_id=obj_active_stake.id).last()
                    end_date = last_claim_record.end_date if last_claim_record else obj_active_stake.created_on
                    Stake_Monthly_Claim_History.objects.using('second_db').create(
                        user=User.id,
                        email=User.Email,
                        stake_history_id_id=obj_active_stake.id,
                        earned_stake_reward=obj_active_stake.reward_per_month,
                        start_date=end_date,
                        end_date=end_date + relativedelta.relativedelta(months=1),
                        created_on=datetime.now(),
                        modified_on=datetime.now(),
                        status=0
                    )
                else:
                    break

    # Update expired claims to status 0
    Stake_Monthly_Claim_History.objects.using('second_db').filter(
        user=User.id, 
        stake_history_id_id=obj_active_stake.id,
        end_date__lte=datetime.now(),
        status=1
    ).update(status=0)

    # Prepare the response data
    list_user = []
    stake_month_claim_hist = Stake_Monthly_Claim_History.objects.using('second_db').filter(
        user=User.id, stake_history_id_id=obj_active_stake.id
    ).order_by('-created_on')

    for i in stake_month_claim_hist:
        list_user.append({
            'id': str(i.id),
            'email': str(i.email),
            'stake_amount': str(i.stake_history_id.Amount_USDT),
            'earned_stake_reward': str(i.earned_stake_reward),
            'start_date': str(i.start_date),
            'end_date': str(i.end_date),
            'status': i.status,
        })

    return Response({
        "Msg": "Claim Successful.",
        "status": "true",
        "data": list_user,
        "Email": User.Email
    })


@api_view(['POST'])
def stke_monthly_claim_update(request):
  Token_header = request.headers['token']
  id = request.data['ID']
  token = Token.objects.get(key = Token_header)
  user_details = User_Management.objects.get(user_name = token.user)
  obj_month_stake_claim = Stake_Monthly_Claim_History.objects.using('second_db').get(id = id)
  obj_stake_wallet = stake_wallet_management.objects.using('second_db').get(user = obj_month_stake_claim.user)
  stake_his = Stake_history_management.objects.using('second_db').get(id = obj_month_stake_claim.stake_history_id_id)
  if obj_month_stake_claim.status == 0:
    if obj_month_stake_claim.stake_history_id.Total_reward_earned < obj_month_stake_claim.stake_history_id.maximum_reward :
      claim_amt = Decimal(obj_month_stake_claim.earned_stake_reward) + Decimal(obj_stake_wallet.stake_withdraw_Wallet)
      obj_stake_wallet.stake_withdraw_Wallet =  claim_amt
      obj_stake_wallet.save(using='second_db')

      obj_month_stake_claim.status = 2
      obj_month_stake_claim.save(using='second_db')

      stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_withdraw_Wallet_reward_amount = Decimal(obj_month_stake_claim.earned_stake_reward),stake_withdraw_Wallet_percentage =100,stake_amount = obj_month_stake_claim.stake_history_id.Amount_USDT,buy_type="User create",type="stake_monthly claim")
    else:
      stake_claim_reward = Stake_Monthly_Claim_History.objects.using('second_db').filter(user = user_details.id,stake_history_id_id = stake_his.id,status = 2).aggregate(Sum('earned_stake_reward')) 
      actual_reward = stake_claim_reward['earned_stake_reward__sum']
      if actual_reward != None:
        actual_claim_amt = Decimal(stake_his.reward_earned)- Decimal(actual_reward)
        if actual_claim_amt < obj_month_stake_claim.earned_stake_reward:
          obj_stake_wallet.stake_withdraw_Wallet = Decimal(obj_stake_wallet.stake_withdraw_Wallet) + actual_claim_amt
          obj_stake_wallet.save(using='second_db')
          # stake_his.status = 1
          # stake_his.claim_status = 2
          # stake_his.save(using='second_db')
          obj_month_stake_claim.status = 2
          obj_month_stake_claim.save(using='second_db')

          stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_withdraw_Wallet_reward_amount = Decimal(actual_claim_amt),stake_withdraw_Wallet_percentage =100,stake_amount = obj_month_stake_claim.stake_history_id.Amount_USDT,buy_type="User create",type="stake_monthly claim")
        
        else:
          claim_amt = Decimal(obj_month_stake_claim.earned_stake_reward) + Decimal(obj_stake_wallet.stake_withdraw_Wallet)
          obj_stake_wallet.stake_withdraw_Wallet =  claim_amt
          obj_stake_wallet.save(using='second_db')
          # stake_his.status = 1
          # stake_his.claim_status = 2
          # stake_his.save(using='second_db')
          obj_month_stake_claim.status = 2
          obj_month_stake_claim.save(using='second_db')
          stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_withdraw_Wallet_reward_amount = Decimal(obj_month_stake_claim.earned_stake_reward),stake_withdraw_Wallet_percentage =100,stake_amount = obj_month_stake_claim.stake_history_id.Amount_USDT,buy_type="User create",type="stake_monthly claim")
      else:
          claim_amt = Decimal(obj_month_stake_claim.earned_stake_reward) + Decimal(obj_stake_wallet.stake_withdraw_Wallet)
          obj_stake_wallet.stake_withdraw_Wallet =  claim_amt
          obj_stake_wallet.save(using='second_db')

          obj_month_stake_claim.status = 2
          obj_month_stake_claim.save(using='second_db')
          # stake_his.status = 1
          # stake_his.claim_status = 2
          # stake_his.save(using='second_db')
          stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_withdraw_Wallet_reward_amount = Decimal(obj_month_stake_claim.earned_stake_reward),stake_withdraw_Wallet_percentage =100,stake_amount = obj_month_stake_claim.stake_history_id.Amount_USDT,buy_type="User create",type="stake_monthly claim")

    claimed_reward = Stake_Monthly_Claim_History.objects.using('second_db').filter(user = user_details.id,stake_history_id_id = stake_his.id,status = 2).aggregate(Sum('earned_stake_reward'))
    claimed_rew = claimed_reward['earned_stake_reward__sum']
    if claimed_rew != None:
       if claimed_rew == stake_his.reward_earned:
          stake_his.status = 1
          stake_his.claim_status = 2
          stake_his.save(using='second_db')
    user_data={"Msg":"Claim Successfull.","status":"true","data" : obj_month_stake_claim.status}
    return Response(user_data)


def Stake_claim_edit(request,id):
   context={}
   context['Title'] = 'Staking Claim Edit'
   if request.method == "POST":
    Amount_USDT = request.POST["Amount_USDT"]
    if Amount_USDT:
      staking_deposit_hist = stake_claim_reward_history.objects.using('second_db').get(id = id)
      staking_deposit_hist.stake_Wallet_reward_amount=Amount_USDT
      staking_deposit_hist.buy_type="Admin Edit"
      staking_deposit_hist.save()
      messages.add_message(request, messages.SUCCESS, 'Amount Updated!!!!!' )
      return redirect("/stake/user_stake_history_table/"+str(staking_deposit_hist.user)+"/")
    else:
      messages.add_message(request, messages.ERROR, 'Amount Required!!!!!' ) 
   return render(request,'stake/stake_amount_edit.html',context)

def Stake_deposit_edit(request,id):
   context={}
   context['Title'] = 'Staking Deposit Edit'
   if request.method == "POST":
    Amount_USDT = request.POST["Amount_USDT"]
    if Amount_USDT:
      staking_deposit_hist = stake_deposit_management.objects.using('second_db').get(id = id)
      staking_deposit_hist.Amount_USDT=Amount_USDT
      staking_deposit_hist.type="Admin Edit"
      staking_deposit_hist.save()
      messages.add_message(request, messages.SUCCESS, 'Amount Updated!!!!!' )
      return redirect("/stake/user_stake_history_table/"+str(staking_deposit_hist.user)+"/")
    else:
      messages.add_message(request, messages.ERROR, 'Amount Required!!!!!' ) 
   return render(request,'stake/stake_deposit_edit.html',context)



#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


                                                           #  Monthly stake 
def Stake_MarketPrice_API(request):
  context = {}
  context["Title"] = "Stake Marketprice API"
  context["market"] = Stake_market_price.objects.using('second_db').get(id = 1)
  if request.method == "POST":
    market_price_details = request.POST['market_price']
    API = request.POST['API']
    status = request.POST['status']
    market_model = Stake_market_price.objects.using('second_db').get(id = 1)
    market_model.market_price = market_price_details
    market_model.API = API
    market_model.status = status
    market_model.save()

    # dict_obj = {"market_price" : market_model.market_price,"status" : market_model.status,"API" : market_model.API}
    # red_val = json.dumps(str(dict_obj))
    # settings.REDDIS_VAR.set('market_price_key',red_val)

    messages.add_message(request, messages.SUCCESS, 'Stake Market Price Updated Successfully.')
  return render(request,'trade_admin_auth/stake_market_api.html',context)


def staking_credit_referral_two(request,token,stake_amount):
    Token_header = token
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    stake_amount = int(stake_amount)
    try:
        stake_range = Stake_referral_management.objects.using('second_db').get(status = 0,self_stake_Amount__lte = stake_amount,self_stake_Amount_range__gte = stake_amount)
    except:
        stake_range = 0
    if stake_range != 0:
      b = 1
      
      ref_code = ""
      stake_referral_level = Stake_referral_management.objects.using('second_db').all().count()
      current_user_count = Stake_monthly_history_management.objects.using('second_db').filter(user = User.id).count()
      if int(current_user_count) == 1:
        for i in range(stake_referral_level):
            reward_percentage = 0
            if i == 0 :
              ref_code = User.referal_code
            else:
               ref_code = ref_code
            if ref_code == "":
               break
            reff_id = Referral_code.objects.get(referal_code=ref_code)
            referred_user = User_Management.objects.get(id = reff_id.user.id)
            try:
              ref_his = Stake_history_management.objects.using('second_db').get(user = referred_user.id,status = 0)
            except:
              ref_his = 0
            if ref_his != 0:
              if ref_his.Total_reward_earned >= ref_his.maximum_reward:
                reff_id = Referral_code.objects.get(referal_code=ref_code)
                referred_user = User_Management.objects.get(id = reff_id.user.id)
                b = b + 1
                ref_code = referred_user.referal_code
                pass
              try:
                referred_user_stake_range = Stake_referral_management.objects.using('second_db').get(levels = b)
              except: 
                referred_user_stake_range = 0
              if referred_user_stake_range != 0 and ref_his.referral_level != 0 and ref_his.referral_level >= b:
                # if int(current_user_count) > 1:
                #     reward_percentage = Decimal(referred_user_stake_range.secound_level_stake)
                reward_percentage = Decimal(referred_user_stake_range.first_level_stake)
                reward_amount = Decimal(stake_amount)*(reward_percentage/100)
                reff_id = Referral_code.objects.get(referal_code=ref_code)
                referred_user = User_Management.objects.get(id = reff_id.user.id)

                sum_amt = Decimal(ref_his.Total_reward_earned) + Decimal(reward_amount)
                
                if Decimal(ref_his.Total_reward_earned) < Decimal(ref_his.maximum_reward) < Decimal(sum_amt) :
                  dif_amt = Decimal(sum_amt) - Decimal(ref_his.maximum_reward)

                  original_reward = Decimal(reward_amount) - dif_amt
                  
                  ref_his.referral_reward_earned = Decimal(ref_his.referral_reward_earned) + Decimal(original_reward)
                  ref_his.save(using='second_db')

                  user_stake_wallet = stake_wallet_management.objects.using('second_db').get(user = referred_user.id)
                  user_stake_wallet.stake_Refferal_Wallet =  Decimal(user_stake_wallet.stake_Refferal_Wallet) + (original_reward)
                  user_stake_wallet.save(using='second_db')
                  Stake_referral_reward_table.objects.using('second_db').create(user = referred_user.id,email = referred_user.Email,direct_referral_user = User.Name ,referral_reward_amount = original_reward,referral_level = str(b)+str(' Level'),type="stake_credit")
                else:
                  ref_his.referral_reward_earned = Decimal(ref_his.referral_reward_earned) + Decimal(reward_amount)
                  ref_his.save(using='second_db')

                  user_stake_wallet = stake_wallet_management.objects.using('second_db').get(user = referred_user.id)
                  user_stake_wallet.stake_Refferal_Wallet =   Decimal(user_stake_wallet.stake_Refferal_Wallet) + (reward_amount)
                  user_stake_wallet.save(using='second_db')
                  Stake_referral_reward_table.objects.using('second_db').create(user = referred_user.id,email = referred_user.Email,direct_referral_user = User.Name ,referral_reward_amount = reward_amount,referral_level = str(b)+str(' Level'),type="stake_credit")
                ref_code = referred_user.referal_code
              if referred_user.referal_code == "" or referred_user.referal_code == None:
                  break
              else:
                  b = b + 1
                  ref_code = referred_user.referal_code
                  if referred_user.referal_code == "" or referred_user.referal_code == None:
                    break
            else:
              reff_id = Referral_code.objects.get(referal_code=ref_code)
              referred_user = User_Management.objects.get(id = reff_id.user.id)
              b = b + 1
              ref_code = referred_user.referal_code
              if referred_user.referal_code == "" or referred_user.referal_code == None:
                  break
              pass
    else:
        return True
    
def Edit_Staking_Monthly_Plan(request):
  context = {}
  context['Title'] = 'Monthly Staking Management'
  obj_stake_manage = staking_monthly_admin_management.objects.using('second_db').get(id = 1)
  plan_obj = plan.objects.filter(status = 0).filter(~Q(plan_type = 0))
  select_plan = plan.objects.get(id = obj_stake_manage.eligible_plan)
  context['obj_stake_manage'] = obj_stake_manage
  context['plan_obj'] = plan_obj
  context['select_plan'] = select_plan
  if request.method == "POST":
    stake_period = request.POST["stake_period"]
    reward_percent = request.POST["reward_percent"]
    minimum_stake = request.POST["minimum_stake"]
    maximum_stake = request.POST["maximum_stake"]
    status = request.POST["status"]
    with_status = request.POST["withdraw_status"]
    min_withdraw = request.POST["minimum_withdraw"]
    # min_with_referral = request.POST["minimum_withdraw_referal"]
    # max_with_referral = request.POST["maximum_withdraw_referal"]
    # eligible_plan = request.POST["eligible_plan"]
    stake_wallet_percentage = request.POST["stake_wallet_percentage"]
    withdraw_wallet_percentage = request.POST["withdraw_wallet_percentage"]
    stake_withdraw_transaction_fee = request.POST["stake_withdraw_transaction_fee"]
    if stake_period != "" and reward_percent != "" and minimum_stake != "":
      staking_monthly_admin_management.objects.using('second_db').filter(id = 1).update(stake_period = stake_period,reward_percent = reward_percent,minimum_stake = minimum_stake,maximum_stake = maximum_stake,status = status,withdraw_status = with_status,minimum_withdraw = min_withdraw,stake_wallet_percentage=stake_wallet_percentage,withdraw_wallet_percentage=withdraw_wallet_percentage,stake_withdraw_transaction_fee=stake_withdraw_transaction_fee)
      messages.add_message(request, messages.SUCCESS, 'Successfully updated.')
      return HttpResponseRedirect('/stake/Edit_Staking_Monthly_Plan/1/')
    else:
      messages.add_message(request, messages.ERROR, 'Enter required field.')
      return HttpResponseRedirect('/stake/Edit_Staking_Monthly_Plan/1/')
  return render(request,'stake/edit_staking_monthly_plan.html',context)
     

import datetime
  
@api_view(['POST'])
def stake_credit_api(request):
    # user_data={'msg':"Stake Credit Model Is Now Under Maintenance.",'status':'false'}
    # return Response(user_data)
  Token_header = request.headers['Token']
  token = Token.objects.get(key = Token_header)
  user_Detail=User_Management.objects.get(user_name = token.user) 
  obj_stake_wall = staking_monthly_admin_management.objects.using('second_db').get(id = 1)
  Amount_USDT = request.data['Amount']
  # maximum_limit = request.data['maximum_limit']
  Amount_JW = request.data['Amount_JW']
  start_date = datetime.now()
  duration_end_date = start_date + timedelta(days=365/12*int(obj_stake_wall.stake_period))
  duration_days = (duration_end_date - start_date).days
  end_date = start_date + timedelta(days = duration_days)
  stake_market_price=Stake_market_price.objects.using('second_db').get(id=1)
  try:
    stake_last = Stake_monthly_history_management.objects.filter(user = user_Detail.id).last()
    if stake_last :
        how_many_days= start_date - stake_last.created_on 
        how_many= 30 - how_many_days.days 
        if stake_last.created_on + timedelta(30) > start_date:
            user_data={"Msg":"Your Stake Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
            return Response(user_data)
  except:
      stake_last = ""
  try:
      user_stake_obj = UserCashWallet.objects.get(userid = user_Detail.id)
  except:
      user_stake_obj = 0
  if user_stake_obj != 0 :
    if Decimal(user_stake_obj.balancetwo) >= Decimal(Amount_USDT):
      if Decimal(obj_stake_wall.minimum_stake) <= Decimal(Amount_USDT):
        rew_per_month = Decimal(Amount_USDT) * Decimal(obj_stake_wall.reward_percent / 100)
        max_limit = rew_per_month * obj_stake_wall.stake_period
        try:
          obj_check_stake = Stake_monthly_history_management.objects.using('second_db').filter(user = user_Detail.id,status = 0).last()
        except:
          obj_check_stake = ""
        if obj_check_stake != None:
          date_now = obj_check_stake.start_date + timedelta(29)
          if date_now >= start_date :
            user_data={'msg':"Monthly One Stake Only",'status':'false'}
            return Response(user_data)
          # stake condition removed.
          # if Decimal(obj_check_stake.Amount_USDT) > Decimal(Amount_USDT) :
          #   user_data={'msg':"Kindly Stake greater than previous Stake",'status':'false'}
          #   return Response(user_data)
          # else:
          user_stake_obj.balancetwo = Decimal(user_stake_obj.balancetwo) - Decimal(Amount_USDT)
          user_stake_obj.save()
          
          obj_hist_id = Stake_monthly_history_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Amount_USDT,Amount_JW = Amount_JW,period = obj_stake_wall.stake_period,reward_per_month = rew_per_month,referral_status = 0,created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),reward_percent = obj_stake_wall.reward_percent,status = 0,start_date = start_date,end_date = end_date,claim_status = 1,referral_level = 0,market_price=stake_market_price.market_price)
          
          staking_credit_referral_two(request,Token_header,Amount_USDT)
          user_data={'msg':"Stake Successfull",'status':'true'}
          return Response(user_data)
        else:
            user_stake_obj.balancetwo = Decimal(user_stake_obj.balancetwo) - Decimal(Amount_USDT)
            user_stake_obj.save()
            obj_hist_id = Stake_monthly_history_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Amount_USDT,Amount_JW = Amount_JW,period = obj_stake_wall.stake_period,reward_per_month = rew_per_month,referral_status = 0,created_on = datetime.datetime.now(),modified_on = datetime.datetime.now(),reward_percent = obj_stake_wall.reward_percent,status = 0,start_date = start_date,end_date = end_date,claim_status = 1,referral_level = 0,market_price=stake_market_price.market_price)
            staking_credit_referral_two(request,Token_header,Amount_USDT)
            user_data={'msg':"Stake Successfull",'status':'true'}
            return Response(user_data)  
      else:
          user_data={'msg':"Minimum amount is less than Amount",'status':'false'}
          return Response(user_data)
    else:
      user_data={'msg':"Insufficient Balance",'status':'false'}
      return Response(user_data)
  else:
      user_data={'msg':"User Doesn't have stake wallet.",'status':'false'}
      return Response(user_data)
  


@api_view(['POST'])
def Current_credit_stake(request):
  Token_header = request.headers['Token']
  token = Token.objects.get(key = Token_header)
  user_details = User_Management.objects.get(user_name = token.user)
  stake_contract_address = Contract_address.objects.get(id = 1)
  stake_his_count = Stake_monthly_history_management.objects.using('second_db').filter(user = user_details.id,status=0).count()
  if stake_his_count == 1:
    stake_his = Stake_monthly_history_management.objects.using('second_db').get(user = user_details.id,status=0)
    if (Decimal(stake_his.reward_earned) >= Decimal(stake_his.maximum_reward)):
      stake_his.claim_status = 0
      stake_his.status = 1
      stake_his.save(using='second_db')
  if stake_his_count > 1:
    stake_his = Stake_monthly_history_management.objects.using('second_db').filter(user = user_details.id,status=0)
    for i in stake_his:
      if (Decimal(i.reward_earned) >= Decimal(i.maximum_reward)):
        i.claim_status = 0
        i.status = 1
        i.save(using='second_db')
  stake_his_claim = Stake_monthly_history_management.objects.using('second_db').values('id','start_date','Amount_USDT','end_date','maximum_reward').order_by('-created_on').filter(user = user_details.id).filter(~Q(claim_status = 2))
  user_data={"Msg":"success",'status':'true','data':stake_his_claim,'stake_contract_address':stake_contract_address.Stake_contract_Address}
  return Response(user_data)



@api_view(['GET'])
def Staking_management_credit_API(request):
  try:
    obj_stake = staking_monthly_admin_management.objects.using('second_db').values("stake_period","reward_percent","minimum_stake","maximum_stake").get(id = 1)
    user_data = {"Msg":"true","status":"true","data":obj_stake}
    return Response(user_data)
  except:
    user_data = {"Msg":"false","status":"false"}
    return Response(user_data)
  


import datetime

@api_view(['POST'])
def staking_credit_reward_function(request):
  Token_header = request.headers['Token']
  token = Token.objects.get(key = Token_header)
  user_details = User_Management.objects.get(user_name = token.user)
  stake_his_count = Stake_monthly_history_management.objects.using('second_db').filter(user = user_details.id,status=0).count()
  total_reward=""
  stake_history = Stake_monthly_history_management.objects.using('second_db').filter(user = user_details.id,status=0)
  for stake_his in stake_history:
    if stake_his.maximum_reward > stake_his.reward_earned :
      mod_date = stake_his.modified_on.date() 
      today = date.today()
      date_date = (today - mod_date)
      date_count = int(date_date.days)
      
      if date_count == 0:
        mod = stake_his.modified_on.time()
        now = datetime.datetime.now().time()
        if stake_his.end_date >= datetime.datetime.now():
          
          dateTimeA = datetime.datetime.combine(date.today(), mod)
          dateTimeB = datetime.datetime.combine(date.today(), now)
          dateTimeDifference = dateTimeB - dateTimeA
          total_diff = int(dateTimeDifference.total_seconds())
          
          stake_reward_per_month = Decimal(stake_his.reward_per_month)
          stake_reward = Decimal(stake_his.maximum_reward)
          per_day_reward = stake_reward_per_month/Decimal(30)
          per_second_reward = per_day_reward / Decimal(600)
          # per_second_reward = stake_reward / Decimal(2160)
          # per_second_reward = stake_reward / Decimal(600)
          total_reward = per_second_reward * total_diff
          
          stake_his.reward_earned = Decimal(stake_his.reward_earned) + total_reward
          stake_his.reward_balance = stake_his.maximum_reward - stake_his.reward_earned
          stake_his.modified_on = datetime.datetime.now()
          stake_his.save(using='second_db')
          stake_credit_reward_history.objects.using('second_db').create(user = user_details.id,email = user_details.Email,reward_amount = total_reward,status = 0)
        else:
            stake_his.reward_earned = Decimal(stake_his.maximum_reward) 
            stake_his.reward_balance = 0
            stake_his.modified_on = datetime.datetime.now()
            stake_his.save(using='second_db')
            stake_credit_reward_history.objects.using('second_db').create(user = user_details.id,email = user_details.Email,reward_amount = stake_his.maximum_reward,status = 0)
      else:
        stake_reward_per_month = Decimal(stake_his.reward_per_month)
        per_day_reward = stake_reward_per_month/Decimal(30)
        stake_his.reward_earned = Decimal(stake_his.reward_earned) + per_day_reward *(date_count)
        stake_his.reward_balance = stake_his.maximum_reward - stake_his.reward_earned
        stake_his.modified_on = datetime.datetime.now()
        stake_his.save(using='second_db')
        stake_credit_reward_history.objects.using('second_db').create(user = user_details.id,email = user_details.Email,reward_amount = total_reward,status = 0)

  user_data={"Msg":"Reward Updated Successfully",'status':'true','token':token.key}
  return Response(user_data)



def staking_referral_two_update(request,id):
    User = User_Management.objects.get(id = id)
    stake_monthly_his = Stake_monthly_history_management.objects.using('second_db').filter(user = User.id).last()
    stake_amount = int(stake_monthly_his.Amount_USDT)
    try:
        stake_range = Stake_referral_management.objects.using('second_db').get(status = 0,self_stake_Amount__lte = stake_amount,self_stake_Amount_range__gte = stake_amount)
    except:
        stake_range = 0
    if stake_range != 0:
      b = 1
      
      ref_code = ""
      stake_referral_level = Stake_referral_management.objects.using('second_db').all().count()
      current_user_count = Stake_monthly_history_management.objects.using('second_db').filter(user = User.id).count()
      if int(current_user_count) == 1:
        for i in range(stake_referral_level):
            reward_percentage = 0
            if i == 0 :
              ref_code = User.referal_code
            else:
               ref_code = ref_code
            if ref_code == "":
               break
            reff_id = Referral_code.objects.get(referal_code=ref_code)
            referred_user = User_Management.objects.get(id = reff_id.user.id)
            current_user_count = Stake_referral_reward_table.objects.using('second_db').filter(direct_referral_user=User.Name,type="stake_credit").count()
            if int(current_user_count) >= 0 :
              try:
                ref_his = Stake_history_management.objects.using('second_db').get(user = referred_user.id,status = 0)
              except:
                ref_his = 0
              if ref_his != 0:
                if ref_his.Total_reward_earned >= ref_his.maximum_reward:
                  reff_id = Referral_code.objects.get(referal_code=ref_code)
                  referred_user = User_Management.objects.get(id = reff_id.user.id)
                  b = b + 1
                  ref_code = referred_user.referal_code
                  pass
                try:
                  referred_user_stake_range = Stake_referral_management.objects.using('second_db').get(levels = b)
                except: 
                  referred_user_stake_range = 0         
                
                if referred_user_stake_range != 0 and ref_his.referral_level != 0 and ref_his.referral_level >= b:
                  
                      reward_percentage = Decimal(referred_user_stake_range.first_level_stake)
                      reward_amount = Decimal(stake_amount)*(reward_percentage/100)
                      reff_id = Referral_code.objects.get(referal_code=ref_code)
                      referred_user = User_Management.objects.get(id = reff_id.user.id)

                      sum_amt = Decimal(ref_his.Total_reward_earned) + Decimal(reward_amount)
                      
                      if Decimal(ref_his.Total_reward_earned) < Decimal(ref_his.maximum_reward) < Decimal(sum_amt) :
                        dif_amt = Decimal(sum_amt) - Decimal(ref_his.maximum_reward)

                        original_reward = Decimal(reward_amount) - dif_amt
                        
                        ref_his.referral_reward_earned = Decimal(ref_his.referral_reward_earned) + Decimal(original_reward)
                        ref_his.save(using='second_db')

                        user_stake_wallet = stake_wallet_management.objects.using('second_db').get(user = referred_user.id)
                        user_stake_wallet.stake_Refferal_Wallet =  Decimal(user_stake_wallet.stake_Refferal_Wallet) + (original_reward)
                        user_stake_wallet.save(using='second_db')
                        Stake_referral_reward_table.objects.using('second_db').create(user = referred_user.id,email = referred_user.Email,direct_referral_user = User.Name ,referral_reward_amount = original_reward,referral_level = str(b)+str(' Level'),type="stake_credit")
                      else:
                        ref_his.referral_reward_earned = Decimal(ref_his.referral_reward_earned) + Decimal(reward_amount)
                        ref_his.save(using='second_db')

                        user_stake_wallet = stake_wallet_management.objects.using('second_db').get(user = referred_user.id)
                        user_stake_wallet.stake_Refferal_Wallet =   Decimal(user_stake_wallet.stake_Refferal_Wallet) + (reward_amount)
                        user_stake_wallet.save(using='second_db')
                        Stake_referral_reward_table.objects.using('second_db').create(user = referred_user.id,email = referred_user.Email,direct_referral_user = User.Name ,referral_reward_amount = reward_amount,referral_level = str(b)+str(' Level'),type="stake_credit")
                      ref_code = referred_user.referal_code
                if referred_user.referal_code == "" or referred_user.referal_code == None:
                    break
                else:
                    b = b + 1
                    ref_code = referred_user.referal_code
                    if referred_user.referal_code == "" or referred_user.referal_code == None:
                      break
              else:
                reff_id = Referral_code.objects.get(referal_code=ref_code)
                referred_user = User_Management.objects.get(id = reff_id.user.id)
                b = b + 1
                ref_code = referred_user.referal_code
                if referred_user.referal_code == "" or referred_user.referal_code == None:
                    break
                pass
        messages.add_message(request, messages.SUCCESS, 'Referral Reward Update!!!!!' ) 
    return HttpResponseRedirect('/stake/user_stake_history_table/'+ str(User.id)+'/')


class StakecreditHistoryManagementTable(TemplateView):
  template_name = "stake/stake_credit_history_table.html"

  def get_context_data(self, **kwargs):
    context = super(StakecreditHistoryManagementTable, self).get_context_data(**kwargs)
    p_key = self.kwargs['pk']
    context["p_key"] = p_key
    context["Title"] = "User Stake Credit History"
    context["Btn_url"] = "trade_admin_auth:List_User_Management"
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

    context['p_no'] = p_no
    context['p_no1'] = p_no1
    context['p_no2'] = p_no2
    context['p_no3'] = p_no3
    context['p_no4'] = p_no4
    context['p_no5'] = p_no5

# ---------------------------------------------------------Staking credit History-------------------------------------------------

    try:
      stake_date = self.request.GET['created_on']
    except:
      stake_date = ""


    stake_usr = 0
    stake_count = 0
    stake_credit_dict_users = {}
    stake_start_page = self.request.GET.get('pageno2', 1)
    stake_end_value = int(stake_start_page) * 5
    stake_start_value = int(stake_end_value) - 4
    
    if stake_date:
      obj_stake_hist = Stake_monthly_history_management.objects.using('second_db').filter(user = p_key).filter(created_on__date = stake_date).order_by('-created_on')
      for i in obj_stake_hist:
        stake_usr = stake_usr + 1
        stake_list_usr = {}
        if stake_start_value <= stake_usr <= stake_end_value:
          stake_count = stake_count + 1
          obj_stake_wall = stake_wallet_management.objects.using('second_db').get(user = i.user)
          stake_list_usr["email"] = str(i.email)
          stake_list_usr["user"] = str(i.user)
          stake_list_usr["Amount_USDT"] = str(i.Amount_USDT)
          stake_list_usr["Amount_JW"] = str(i.Amount_JW)
          stake_list_usr["max_limit"] = str(i.maximum_reward)
          stake_list_usr["reward_per_month"] = (str(i.reward_per_month))
          ref_rew = (round(Decimal(obj_stake_wall.stake_Refferal_Wallet),4))
          stake_list_usr["ref_rew_earned"] = str(ref_rew)
          stake_list_usr["rew_earned"] = str(i.reward_earned)
          tot_rew_earned = Decimal(obj_stake_wall.stake_Refferal_Wallet) + Decimal(i.reward_earned)
          tot_reward = (round(Decimal(tot_rew_earned),4))
          stake_list_usr["total_rew_earned"] = str(tot_reward)
          stake_list_usr["rew_blnc"] = str(i.reward_balance)
          stake_list_usr["start_date"] = str(i.start_date.strftime('%Y-%m-%d'))
          stake_list_usr["end_date"] = str(i.end_date.strftime('%Y-%m-%d'))
          stake_list_usr["status"] = i.status
          date = i.created_on
          stake_list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
          stake_list_usr["pageno"] = stake_start_page
          stake_list_usr["sno"] = stake_usr
          stake_credit_dict_users[stake_count] = stake_list_usr
    else:
      obj_stake_hist = Stake_monthly_history_management.objects.using('second_db').filter(user = p_key).order_by('-id')
      for i in obj_stake_hist:
        stake_usr = stake_usr + 1
        stake_list_usr = {}
        if stake_start_value <= stake_usr <= stake_end_value:
            stake_count = stake_count + 1
            obj_stake_wall = stake_wallet_management.objects.using('second_db').get(user = i.user)
            stake_list_usr["email"] = str(i.email)
            stake_list_usr["user"] = str(i.user)
            stake_list_usr["Amount_USDT"] = str(i.Amount_USDT)
            stake_list_usr["Amount_JW"] = str(i.Amount_JW)
            stake_list_usr["max_limit"] = str(i.maximum_reward)
            stake_list_usr["reward_per_month"] = (str(i.reward_per_month))
            ref_rew = (round(Decimal(obj_stake_wall.stake_Refferal_Wallet),4))
            stake_list_usr["ref_rew_earned"] = str(ref_rew)
            stake_list_usr["rew_earned"] = str(i.reward_earned)
            tot_rew_earned = Decimal(obj_stake_wall.stake_Refferal_Wallet) + Decimal(i.reward_earned)
            tot_reward = (round(Decimal(tot_rew_earned),4))
            stake_list_usr["total_rew_earned"] = str(tot_reward)
            stake_list_usr["rew_blnc"] = str(i.reward_balance)
            stake_list_usr["start_date"] = str(i.start_date.strftime('%Y-%m-%d'))
            stake_list_usr["end_date"] = str(i.end_date.strftime('%Y-%m-%d'))
            stake_list_usr["status"] = i.status
            date = i.created_on
            stake_list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
            stake_list_usr["pageno"] = stake_start_page
            stake_list_usr["sno"] = stake_usr
            stake_credit_dict_users[stake_count] = stake_list_usr

    try:
      tot_stake_user_qs = obj_stake_hist
    except:
      tot_stake_user_qs = ""
    w_page_2 = self.request.GET.get('pageno2', 1)
    w_paginator_2 = Paginator(tot_stake_user_qs, 5)
    
    try:
        stake_hist_qs = w_paginator_2.page(w_page_2)
    except PageNotAnInteger:
        stake_hist_qs =w_paginator_2.page(1)
    except EmptyPage:
        stake_hist_qs = w_paginator_2.page(w_paginator_2.num_pages)
    
    
    context['stake_hist_qs'] = stake_hist_qs
    context["stake_endpage"] = stake_hist_qs.number+1
    context["stake_start_page"] = stake_hist_qs.number-1
    context['stake_start_value'] = stake_hist_qs.start_index()
    context['stake_end_value'] = stake_hist_qs.end_index()
    context['stake_usr_count'] = obj_stake_hist.count()
    context["stake_credit_dict_users"] = json.dumps(stake_credit_dict_users)

    # ---------------------------------------------------------Stake Wallet History-------------------------------------------------

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
          if i.balancetwo == 0.00000000:
            wall_list_usr["pre_reward"] = int(i.balancetwo)
          else:
            wall_list_usr["pre_reward"] = str(i.balancetwo)
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

    # ---------------------------------------------------------Stake Credit Wallet History-------------------------------------------------


    try:
      date = self.request.GET['Date']
    except:
      date = ""


    int_usr = 0
    int_count = 0
    int_dict_users = {}
    int_start_page = self.request.GET.get('pageno', 1)
    int_end_value = int(int_start_page) * 5
    int_start_value = int(int_end_value) - 4
    
    if date:
      obj_internal_hist = Stake_Credit_History.objects.filter(user = user_obj.id).filter(created_on__date = date).order_by('-created_on')
      for i in obj_internal_hist:
        
        int_usr = int_usr + 1
        int_list_usr = {}
        if int_start_value <= int_usr <= int_end_value:
          int_count = int_count + 1
          int_list_usr["username"] = str(user_obj.Name)
          int_list_usr["amt"] = str(i.original_reward)
          int_list_usr["frm_wallet"] = (i.stake_percentage)
          int_list_usr["to_wallet"] = (i.percent_value)
          created_date = i.created_on
          int_list_usr["date"] = str(created_date.strftime("%m/%d/%Y, %H:%M:%S"))
          int_list_usr["pageno"] = int_start_page
          int_list_usr["sno"] = int_usr
          int_dict_users[int_count] = int_list_usr
    else:
      obj_internal_hist = Stake_Credit_History.objects.filter(user = user_obj.id).order_by('-id')
      for i in obj_internal_hist:
        int_usr = int_usr + 1
        int_list_usr = {}
        if int_start_value <= int_usr <= int_end_value:
          int_count = int_count + 1
          int_list_usr["username"] = str(user_obj.Name)
          int_list_usr["amt"] = str(i.original_reward)
          int_list_usr["frm_wallet"] = (i.stake_percentage)
          int_list_usr["to_wallet"] = (i.percent_value)
          created_date = i.created_on
          int_list_usr["date"] = str(created_date.strftime("%m/%d/%Y, %H:%M:%S"))
          int_list_usr["pageno"] = int_start_page
          int_list_usr["sno"] = int_usr
          int_dict_users[int_count] = int_list_usr

    try:
      tot_int_user_qs = obj_internal_hist
    except:
      tot_int_user_qs = ""
    w_page = self.request.GET.get('pageno', 1)
    w_paginator = Paginator(tot_int_user_qs, 5)
    
    try:
        int_hist_qs = w_paginator.page(w_page)
    except PageNotAnInteger:
        int_hist_qs =w_paginator.page(1)
    except EmptyPage:
        int_hist_qs = w_paginator.page(w_paginator.num_pages)
    
    
    context['int_hist_qs'] = int_hist_qs
    context["int_endpage"] = int_hist_qs.number+1
    context["int_startpage"] = int_hist_qs.number-1
    context['int_start_value'] = int_hist_qs.start_index()
    context['int_end_value'] = int_hist_qs.end_index()
    context['int_usr_count'] = obj_internal_hist.count()
    context["int_dict_users"] = json.dumps(int_dict_users)

    # ---------------------------------------------------------Stake Claim History-------------------------------------------------

    try:
      stake_date = self.request.GET['created_on']
    except:
      stake_date = ""


    stake_usr = 0
    stake_count = 0
    stake_credit_claim_dict_users = {}
    stake_start_page = self.request.GET.get('pageno2', 1)
    stake_end_value = int(stake_start_page) * 5
    stake_start_value = int(stake_end_value) - 4
    
    if stake_date:
      obj_stake_hist = stake_credit_claim_history.objects.using('second_db').filter(user = p_key).filter(created_on__date = stake_date).order_by('-created_on')
      for i in obj_stake_hist:
        stake_usr = stake_usr + 1
        stake_credit_claim_list_usr = {}
        if stake_start_value <= stake_usr <= stake_end_value:
          stake_count = stake_count + 1
          stake_credit_claim_list_usr["email"] = str(i.email)
          stake_credit_claim_list_usr["user"] = str(i.user)
          stake_credit_claim_list_usr["staked_amount"] = str(i.staked_amount)
          stake_credit_claim_list_usr["earned_stake_reward"] = str(i.earned_stake_reward)
          stake_credit_claim_list_usr["status"] = i.status
          date = i.created_on
          stake_credit_claim_list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
          stake_credit_claim_list_usr["pageno"] = stake_start_page
          stake_credit_claim_list_usr["sno"] = stake_usr
          stake_credit_claim_dict_users[stake_count] = stake_credit_claim_list_usr
    else:
      obj_stake_hist = stake_credit_claim_history.objects.using('second_db').filter(user = p_key).order_by('-id')
      for i in obj_stake_hist:
        stake_usr = stake_usr + 1
        stake_credit_claim_list_usr = {}
        if stake_start_value <= stake_usr <= stake_end_value:
            stake_count = stake_count + 1
            stake_credit_claim_list_usr["email"] = str(i.email)
            stake_credit_claim_list_usr["user"] = str(i.user)
            stake_credit_claim_list_usr["staked_amount"] = str(i.staked_amount)
            stake_credit_claim_list_usr["earned_stake_reward"] = str(i.earned_stake_reward)
            stake_credit_claim_list_usr["status"] = i.status
            date = i.created_on
            stake_credit_claim_list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
            stake_credit_claim_list_usr["pageno"] = stake_start_page
            stake_credit_claim_list_usr["sno"] = stake_usr
            stake_credit_claim_dict_users[stake_count] = stake_credit_claim_list_usr

    try:
      tot_stake_user_qs = obj_stake_hist
    except:
      tot_stake_user_qs = ""
    w_page_2 = self.request.GET.get('pageno2', 1)
    w_paginator_2 = Paginator(tot_stake_user_qs, 5)
    
    try:
        stake_hist_qs = w_paginator_2.page(w_page_2)
    except PageNotAnInteger:
        stake_hist_qs =w_paginator_2.page(1)
    except EmptyPage:
        stake_hist_qs = w_paginator_2.page(w_paginator_2.num_pages)
    context['stake_hist_qs'] = stake_hist_qs
    context["stake_endpage"] = stake_hist_qs.number+1
    context["stake_start_page"] = stake_hist_qs.number-1
    context['stake_start_value'] = stake_hist_qs.start_index()
    context['stake_end_value'] = stake_hist_qs.end_index()
    context['stake_usr_count'] = obj_stake_hist.count()
    context["stake_credit_claim_dict_users"] = json.dumps(stake_credit_claim_dict_users)

    # ---------------------------------------------------------Stake withdraw History-------------------------------------------------

    try:
      stake_date = self.request.GET['created_on']
    except:
      stake_date = ""


    stake_usr = 0
    stake_count = 0
    stake_credit_withdraw_dict_users = {}
    stake_start_page = self.request.GET.get('pageno2', 1)
    stake_end_value = int(stake_start_page) * 5
    stake_start_value = int(stake_end_value) - 4
    
    if stake_date:
      obj_stake_hist = stake_claim_table.objects.using('second_db').filter(user = p_key).filter(created_on__date = stake_date).order_by('-created_on')
      for i in obj_stake_hist:
        stake_usr = stake_usr + 1
        stake_credit_withdraw_list_usr = {}
        if stake_start_value <= stake_usr <= stake_end_value:
          stake_count = stake_count + 1
          stake_credit_withdraw_list_usr["email"] = str(i.email)
          stake_credit_withdraw_list_usr["original_USDT"] = str(i.original_USDT)
          stake_credit_withdraw_list_usr["claim_amount_USDT"] = str(i.claim_amount_USDT)
          stake_credit_withdraw_list_usr["claim_amount_JW"] = str(i.claim_amount_JW)
          stake_credit_withdraw_list_usr["Wallet_type"] = str(i.Wallet_type)
          stake_credit_withdraw_list_usr["Address"] = str(i.Address)
          stake_credit_withdraw_list_usr["status"] = i.status
          stake_credit_withdraw_list_usr["Hash"] = i.Transaction_Hash
          date = i.created_on
          stake_credit_withdraw_list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
          stake_credit_withdraw_list_usr["pageno"] = stake_start_page
          stake_credit_withdraw_list_usr["sno"] = stake_usr
          stake_credit_withdraw_dict_users[stake_count] = stake_credit_withdraw_list_usr
    else:
      obj_stake_hist = stake_claim_table.objects.using('second_db').filter(user = p_key,Wallet_type='Stake Credit Withdraw').order_by('-id')
      for i in obj_stake_hist:
        stake_usr = stake_usr + 1
        stake_credit_withdraw_list_usr = {}
        if stake_start_value <= stake_usr <= stake_end_value:
          stake_count = stake_count + 1
          stake_credit_withdraw_list_usr["email"] = str(i.email)
          stake_credit_withdraw_list_usr["original_USDT"] = str(i.original_USDT)
          stake_credit_withdraw_list_usr["claim_amount_USDT"] = str(i.claim_amount_USDT)
          stake_credit_withdraw_list_usr["claim_amount_JW"] = str(i.claim_amount_JW)
          stake_credit_withdraw_list_usr["Wallet_type"] = str(i.Wallet_type)
          stake_credit_withdraw_list_usr["Address"] = str(i.Address)
          stake_credit_withdraw_list_usr["status"] = i.status
          stake_credit_withdraw_list_usr["Hash"] = i.Transaction_Hash
          date = i.created_on
          stake_credit_withdraw_list_usr["date"] = str(date.strftime("%m/%d/%Y, %H:%M:%S"))
          stake_credit_withdraw_list_usr["pageno"] = stake_start_page
          stake_credit_withdraw_list_usr["sno"] = stake_usr
          stake_credit_withdraw_dict_users[stake_count] = stake_credit_withdraw_list_usr

    try:
      tot_stake_user_qs = obj_stake_hist
    except:
      tot_stake_user_qs = ""
    w_page_2 = self.request.GET.get('pageno2', 1)
    w_paginator_2 = Paginator(tot_stake_user_qs, 5)
    
    try:
        stake_hist_qs = w_paginator_2.page(w_page_2)
    except PageNotAnInteger:
        stake_hist_qs =w_paginator_2.page(1)
    except EmptyPage:
        stake_hist_qs = w_paginator_2.page(w_paginator_2.num_pages)
    context['stake_hist_qs'] = stake_hist_qs
    context["stake_endpage"] = stake_hist_qs.number+1
    context["stake_start_page"] = stake_hist_qs.number-1
    context['stake_start_value'] = stake_hist_qs.start_index()
    context['stake_end_value'] = stake_hist_qs.end_index()
    context['stake_usr_count'] = obj_stake_hist.count()
    context["stake_credit_withdraw_dict_users"] = json.dumps(stake_credit_withdraw_dict_users)

    return context

  
@api_view(['POST'])
def Stake_credit_Claim_API(request):
  Token_header = request.headers['Token']
  token = Token.objects.get(key = Token_header) 
  user_detailss = User_Management.objects.get(user_name = token.user)
  user_type=user_detailss.user_profile_pic
  company_qs = Company.objects.get(id=1)
  android_current_version_users_count = company_qs.Android_version
  ios_current_version_users_count = company_qs.IOS_version
  withdraw_type=company_qs.withdraw_type
  if withdraw_type == 0:
    if user_type == 'Android':
      if user_detailss.phone_number != android_current_version_users_count:
          user_data={"Msg":"Please Update Current Version!!!",'status':'false','token':token.key}
          return Response(user_data)
      try:
        user_details = User_Management.objects.get(user_name = token.user)
        pin = Pin.objects.get(user_id = user_details.id)
        amount = (request.data['Amount'])
        amount_jw = request.data['Wei_amount']
        address = request.data['Address']
        two_fa_input = request.data['Two_Fa']
        ref_pin = int(request.data['pin'])
        wallet_Type = int(request.data['wallet_type'])
        User_Private_key = (request.data['User_PK'])
        stake_withdraw_usdt=request.data['credit_withdraw_usdt']
        stake_credit_converted=request.data['stake_credit_converted']
        receiver_ck = Web3.isAddress((address))
        today = (datetime.datetime.now())
        stake_admin = staking_monthly_admin_management.objects.using('second_db').get(id = 1)
        withdraw_stake = stake_admin.withdraw_status
        if int(withdraw_stake) == 1:
          user_data={"Msg":"Withdraw Under Maintenance",'status':'false','token':token.key}
          return Response(user_data)
        if Decimal(amount_jw) > 0:
          try:
            security_type = request.data['security_type']
          except:
            security_type = "TFA"
          if (str(amount).find('.')) != -1:
            user_data={"Msg":"Enter Only Whole Numbers Like 1,2,3,4......",'status':'false','token':token.key}
            return Response(user_data)
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
            try:
              withdraw_min_max = staking_monthly_admin_management.objects.using('second_db').filter(user = user_details.id,status = 0).last()
            except:
              withdraw_min_max = ""
            if withdraw_min_max :
              if Decimal(amount) > Decimal(withdraw_min_max.Amount_USDT):
                user_data={"Msg":"Amount Exceeds Maximum Limit",'status':'false','token':token.key}
                return Response(user_data)
            two_fa = User_two_fa.objects.get(user = user_details.id)
            confirm = two_fa.user_secrete_key
            admin_stake = staking_monthly_admin_management.objects.using('second_db').get(id = 1)

            user_wallet = UserCashWallet.objects.get(userid_id = user_details.id)

            stake_withdraw_percent_amt = Decimal(amount) * Decimal(int(admin_stake.withdraw_wallet_percentage)/100)
            stake_withdraw_percent_round_amt = math.ceil(stake_withdraw_percent_amt*100)/100


            stake_percent_amt = Decimal(amount) * Decimal(int(admin_stake.stake_wallet_percentage)/100)
            stake_with_amt = Decimal(user_wallet.balancetwo) + Decimal(stake_percent_amt)
            stake_round_amt = math.ceil(stake_with_amt*100)/100

            stake_wallet_management.objects.using('second_db').filter(user = user_details.id).update(stake_Wallet = stake_round_amt)
            if security_type == "TFA":
              if two_fa.user_status == 'enable':
                totp = pyotp.TOTP(confirm)
                otp_now=totp.now()
                pin = Pin.objects.get(user_id = user_details.id)
                pinnn = pin.pin
                num1 = str(pinnn)
                num2 = str(123456)
                if int(two_fa_input) == int(otp_now):
                  if ref_pin == pin.pin:
                    if wallet_Type == 1:
                      try:
                        withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake Credit Withdraw').last()
                        if withdraw_last_stake :
                            how_many_days= today - withdraw_last_stake.created_on 
                            how_many= 30 - how_many_days.days
                            if withdraw_last_stake.created_on + timedelta(30) > today:
                                user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                return Response(user_data)
                      except:
                          withdraw_last_stake = ""
                    if receiver_ck is True:
                      currency = TradeCurrency.objects.get(symbol = 'JW')
                      fee_type = currency.withdraw_feestype
                      if fee_type == 0:
                          fee = (float(currency.withdraw_fees)/100)*(float(amount))
                      else:
                          fee = (float(amount))-(float(currency.withdraw_fees))
                      receiver_address = Web3.toChecksumAddress(str(address))
                      max_amount = int(float(amount_jw)*10 ** 8)
                      try:
                        url = "https://apinode.jasanwellness.fit/VahlHzjSVqvqjaSglbDxWVfAxwrsIMKTcXCwoAIBBEkLBAwHQl"
                        data = {
                              "userAddress":receiver_address,
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
                      cash = stake_wallet_management.objects.using('second_db').get(user = user_details.id)
                      if wallet_Type == 1:
                        wallet_type_name = "Stake Credit Withdraw"
                        cash.stake_credit_withdraw_Wallet = Decimal(cash.stake_credit_withdraw_Wallet) - Decimal(amount)
                        cash.save(using='second_db')
                      else:
                        user_data={"Msg":"Invalid wallet type.",'status':'false','token':token.key}
                        return Response(user_data)
                      table2 = Stake_Credit_History.objects.create(user_id = user_detailss.id,original_reward = amount,stake_percentage = admin_stake.stake_wallet_percentage,percent_value=stake_credit_converted,withdraw_type="Stake Credit Withdraw")
                      stake_claim_table.objects.using('second_db').create(
                        user = user_details.id,
                        email = user_details.Email,
                        original_USDT = amount,
                        claim_amount_USDT = stake_withdraw_usdt,
                        claim_amount_JW = amount_jw,
                        Address = address,
                        Transaction_Hash = transaction_hash,
                        back_up_phrase="0",
                        Two_Fa = two_fa_input,
                        status = 1,
                        Wallet_type = wallet_type_name,
                        created_on = datetime.datetime.now(),
                        modified_on = datetime.datetime.now()
                      )
                      stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_Wallet_percentage = admin_stake.stake_wallet_percentage,stake_Wallet_reward_amount = Decimal(stake_percent_amt),type='Stake Credit Withdraw',original_amount=amount,buy_type="user_buy",transfer_amount=0,Wallet_type=wallet_type_name)
                      table1 = Admin_Profit.objects.create(user = user_details,admin_profit = Decimal(fee),Profit_type = wallet_type_name)
                      user_data={"Msg":"Withdraw Successfull",'status':'true','token':token.key}
                      return Response(user_data)
                      
                      
                      # table = Withdraw_history.objects.create(user_id = user,Amount = price,From_Address = decrypt_with_common_cipher(ad_ad),To_Address = receiver,Transaction_Hash = transaction_hash,withdraw_id=withdraw,Wallet_type = wallet__type)
                      
                    else:
                      user_data={"Msg":"Invalid address.",'status':'false','token':token.key}
                      return Response(user_data)  
                  else:
                    user_data={"Msg":"Pin does not match.",'status':'false','token':token.key}
                    return Response(user_data)
                else:
                  user_data={"Msg":"Invalid TFA code.",'status':'false','token':token.key}
                  return Response(user_data)   
              else:
                  user_data={"Msg":"Make sure enable your TFA.",'status':'false','token':token.key}
                  return Response(user_data)             
            else:
              Email_otp = Registration_otp.objects.get(user = user_details.id)
              if int(Email_otp.email_otp) == int(two_fa_input):
                pin = Pin.objects.get(user_id = user_details.id)
                if int(ref_pin) == pin.pin:
                  if wallet_Type == 1:
                    try:
                      withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake Credit Withdraw').last()
                      if withdraw_last_stake :
                          how_many_days= today - withdraw_last_stake.created_on 
                          how_many= 30 - how_many_days.days
                          if withdraw_last_stake.created_on + timedelta(30) > today:
                              user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                              return Response(user_data)
                    except:
                        withdraw_last_stake = ""
                  if receiver_ck is True:
                    currency = TradeCurrency.objects.get(symbol = 'JW')
                    fee_type = currency.withdraw_feestype
                    if fee_type == 0:
                        fee = (float(currency.withdraw_fees)/100)*(float(amount))
                    else:
                        fee = (float(amount))-(float(currency.withdraw_fees))
                    receiver_address = Web3.toChecksumAddress(str(address))
                    max_amount = int(float(amount_jw)*10 ** 8)
                    try:
                        url = "https://apinode.jasanwellness.fit/VahlHzjSVqvqjaSglbDxWVfAxwrsIMKTcXCwoAIBBEkLBAwHQl"
                        data = {
                              "userAddress":receiver_address,
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
                    cash = stake_wallet_management.objects.using('second_db').get(user = user_details.id)
                    if wallet_Type == 1:
                      wallet_type_name = "Stake Credit Withdraw"
                      cash.stake_credit_withdraw_Wallet = Decimal(cash.stake_credit_withdraw_Wallet) - Decimal(amount)
                      cash.save(using='second_db')
                    else:
                      user_data={"Msg":"Invalid wallet type.",'status':'false','token':token.key}
                      return Response(user_data)
                    table2 = Stake_Credit_History.objects.create(user_id = user_detailss.id,original_reward = amount,stake_percentage = admin_stake.stake_wallet_percentage,percent_value=stake_credit_converted,withdraw_type="Stake Credit Withdraw")
                    stake_claim_table.objects.using('second_db').create(
                      user = user_details.id,
                      email = user_details.Email,
                      original_USDT = amount,
                      claim_amount_USDT = stake_withdraw_usdt,
                      claim_amount_JW = amount_jw,
                      Address = address,
                      Transaction_Hash = transaction_hash,
                      back_up_phrase="0",
                      Two_Fa = two_fa_input,
                      status = 1,
                      Wallet_type = wallet_type_name,
                      created_on = datetime.datetime.now(),
                      modified_on = datetime.datetime.now()
                    )
                    stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_Wallet_percentage = admin_stake.stake_wallet_percentage,stake_Wallet_reward_amount = Decimal(stake_percent_amt),type='Stake Credit Withdraw',original_amount=amount,buy_type="user_buy",transfer_amount=0,Wallet_type=wallet_type_name)
                    table1 = Admin_Profit.objects.create(user = user_details,admin_profit = Decimal(fee),Profit_type = wallet_type_name)
                    user_data={"Msg":"Withdraw Successfull",'status':'true','token':token.key}
                    return Response(user_data)
                else:
                  user_data={"Msg":"App pin cannot be same",'status':'false','token':token.key}
                  return Response(user_data)
              else:
                user_data = {"Msg":"Invalid OTP",'status':'false','token':token.key}
                return Response(user_data)
        else:
          user_data={"Msg":"False",'status':'false','token':token.key}
          return Response(user_data)
      except Exception as e:
        user_data={"Msg":"Failed With Error "+str(e),'status':'false','token':token.key}
        return Response(user_data)
    elif user_type == 'IOS':
      if user_detailss.phone_number != ios_current_version_users_count:
          user_data={"Msg":"Please Update Current Version!!!",'status':'false','token':token.key}
          return Response(user_data)  
      try:
        user_details = User_Management.objects.get(user_name = token.user)
        pin = Pin.objects.get(user_id = user_details.id)
        amount = (request.data['Amount'])
        amount_jw = request.data['Wei_amount']
        address = request.data['Address']
        two_fa_input = request.data['Two_Fa']
        ref_pin = int(request.data['pin'])
        wallet_Type = int(request.data['wallet_type'])
        User_Private_key = (request.data['User_PK'])
        stake_withdraw_usdt=request.data['credit_withdraw_usdt']
        stake_credit_converted=request.data['stake_credit_converted']
        receiver_ck = Web3.isAddress((address))
        today = (datetime.datetime.now())
        stake_admin = staking_monthly_admin_management.objects.using('second_db').get(id = 1)
        withdraw_stake = stake_admin.withdraw_status
        if int(withdraw_stake) == 1:
          user_data={"Msg":"Withdraw Under Maintenance",'status':'false','token':token.key}
          return Response(user_data)
        if Decimal(amount_jw) > 0:
          try:
            security_type = request.data['security_type']
          except:
            security_type = "TFA"
          if (str(amount).find('.')) != -1:
            user_data={"Msg":"Enter Only Whole Numbers Like 1,2,3,4......",'status':'false','token':token.key}
            return Response(user_data)
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
            try:
              withdraw_min_max = staking_monthly_admin_management.objects.using('second_db').filter(user = user_details.id,status = 0).last()
            except:
              withdraw_min_max = ""
            if withdraw_min_max :
              if Decimal(amount) > Decimal(withdraw_min_max.Amount_USDT):
                user_data={"Msg":"Amount Exceeds Maximum Limit",'status':'false','token':token.key}
                return Response(user_data)
            two_fa = User_two_fa.objects.get(user = user_details.id)
            confirm = two_fa.user_secrete_key
            admin_stake = staking_monthly_admin_management.objects.using('second_db').get(id = 1)

            user_wallet = UserCashWallet.objects.get(userid_id = user_details.id)

            stake_withdraw_percent_amt = Decimal(amount) * Decimal(int(admin_stake.withdraw_wallet_percentage)/100)
            stake_withdraw_percent_round_amt = math.ceil(stake_withdraw_percent_amt*100)/100


            stake_percent_amt = Decimal(amount) * Decimal(int(admin_stake.stake_wallet_percentage)/100)
            stake_with_amt = Decimal(user_wallet.balancetwo) + Decimal(stake_percent_amt)
            stake_round_amt = math.ceil(stake_with_amt*100)/100

            stake_wallet_management.objects.using('second_db').filter(user = user_details.id).update(stake_Wallet = stake_round_amt)
            if security_type == "TFA":
              if two_fa.user_status == 'enable':
                totp = pyotp.TOTP(confirm)
                otp_now=totp.now()
                pin = Pin.objects.get(user_id = user_details.id)
                pinnn = pin.pin
                num1 = str(pinnn)
                num2 = str(123456)
                if int(two_fa_input) == int(otp_now):
                  if ref_pin == pin.pin:
                    if wallet_Type == 1:
                      try:
                        withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake Credit Withdraw').last()
                        if withdraw_last_stake :
                            how_many_days= today - withdraw_last_stake.created_on 
                            how_many= 30 - how_many_days.days
                            if withdraw_last_stake.created_on + timedelta(30) > today:
                                user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                return Response(user_data)
                      except:
                          withdraw_last_stake = ""
                    if receiver_ck is True:
                      currency = TradeCurrency.objects.get(symbol = 'JW')
                      fee_type = currency.withdraw_feestype
                      if fee_type == 0:
                          fee = (float(currency.withdraw_fees)/100)*(float(amount))
                      else:
                          fee = (float(amount))-(float(currency.withdraw_fees))
                      receiver_address = Web3.toChecksumAddress(str(address))
                      max_amount = int(float(amount_jw)*10 ** 8)
                      try:
                        url = "https://apinode.jasanwellness.fit/VahlHzjSVqvqjaSglbDxWVfAxwrsIMKTcXCwoAIBBEkLBAwHQl"
                        data = {
                              "userAddress":receiver_address,
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
                      cash = stake_wallet_management.objects.using('second_db').get(user = user_details.id)
                      if wallet_Type == 1:
                        wallet_type_name = "Stake Credit Withdraw"
                        cash.stake_credit_withdraw_Wallet = Decimal(cash.stake_credit_withdraw_Wallet) - Decimal(amount)
                        cash.save(using='second_db')
                      else:
                        user_data={"Msg":"Invalid wallet type.",'status':'false','token':token.key}
                        return Response(user_data)
                      table2 = Stake_Credit_History.objects.create(user_id = user_detailss.id,original_reward = amount,stake_percentage = admin_stake.stake_wallet_percentage,percent_value=stake_credit_converted,withdraw_type="Stake Credit Withdraw")
                      stake_claim_table.objects.using('second_db').create(
                        user = user_details.id,
                        email = user_details.Email,
                        original_USDT = amount,
                        claim_amount_USDT = stake_withdraw_usdt,
                        claim_amount_JW = amount_jw,
                        Address = address,
                        Transaction_Hash = transaction_hash,
                        back_up_phrase="0",
                        Two_Fa = two_fa_input,
                        status = 1,
                        Wallet_type = wallet_type_name,
                        created_on = datetime.datetime.now(),
                        modified_on = datetime.datetime.now()
                      )
                      stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_Wallet_percentage = admin_stake.stake_wallet_percentage,stake_Wallet_reward_amount = Decimal(stake_percent_amt),type='Stake Credit Withdraw',original_amount=amount,buy_type="user_buy",transfer_amount=0,Wallet_type=wallet_type_name)
                      table1 = Admin_Profit.objects.create(user = user_details,admin_profit = Decimal(fee),Profit_type = wallet_type_name)
                      user_data={"Msg":"Withdraw Successfull",'status':'true','token':token.key}
                      return Response(user_data)
                      
                      
                      # table = Withdraw_history.objects.create(user_id = user,Amount = price,From_Address = decrypt_with_common_cipher(ad_ad),To_Address = receiver,Transaction_Hash = transaction_hash,withdraw_id=withdraw,Wallet_type = wallet__type)
                      
                    else:
                      user_data={"Msg":"Invalid address.",'status':'false','token':token.key}
                      return Response(user_data)  
                  else:
                    user_data={"Msg":"Pin does not match.",'status':'false','token':token.key}
                    return Response(user_data)
                else:
                  user_data={"Msg":"Invalid TFA code.",'status':'false','token':token.key}
                  return Response(user_data)   
              else:
                  user_data={"Msg":"Make sure enable your TFA.",'status':'false','token':token.key}
                  return Response(user_data)             
            else:
              Email_otp = Registration_otp.objects.get(user = user_details.id)
              if int(Email_otp.email_otp) == int(two_fa_input):
                pin = Pin.objects.get(user_id = user_details.id)
                if int(ref_pin) == pin.pin:
                  if wallet_Type == 1:
                    try:
                      withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake Credit Withdraw').last()
                      if withdraw_last_stake :
                          how_many_days= today - withdraw_last_stake.created_on 
                          how_many= 30 - how_many_days.days
                          if withdraw_last_stake.created_on + timedelta(30) > today:
                              user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                              return Response(user_data)
                    except:
                        withdraw_last_stake = ""
                  if receiver_ck is True:
                    currency = TradeCurrency.objects.get(symbol = 'JW')
                    fee_type = currency.withdraw_feestype
                    if fee_type == 0:
                        fee = (float(currency.withdraw_fees)/100)*(float(amount))
                    else:
                        fee = (float(amount))-(float(currency.withdraw_fees))
                    receiver_address = Web3.toChecksumAddress(str(address))
                    max_amount = int(float(amount_jw)*10 ** 8)
                    try:
                        url = "https://apinode.jasanwellness.fit/VahlHzjSVqvqjaSglbDxWVfAxwrsIMKTcXCwoAIBBEkLBAwHQl"
                        data = {
                              "userAddress":receiver_address,
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
                    cash = stake_wallet_management.objects.using('second_db').get(user = user_details.id)
                    if wallet_Type == 1:
                      wallet_type_name = "Stake Credit Withdraw"
                      cash.stake_credit_withdraw_Wallet = Decimal(cash.stake_credit_withdraw_Wallet) - Decimal(amount)
                      cash.save(using='second_db')
                    else:
                      user_data={"Msg":"Invalid wallet type.",'status':'false','token':token.key}
                      return Response(user_data)
                    table2 = Stake_Credit_History.objects.create(user_id = user_detailss.id,original_reward = amount,stake_percentage = admin_stake.stake_wallet_percentage,percent_value=stake_credit_converted,withdraw_type="Stake Credit Withdraw")
                    stake_claim_table.objects.using('second_db').create(
                      user = user_details.id,
                      email = user_details.Email,
                      original_USDT = amount,
                      claim_amount_USDT = stake_withdraw_usdt,
                      claim_amount_JW = amount_jw,
                      Address = address,
                      Transaction_Hash = transaction_hash,
                      back_up_phrase="0",
                      Two_Fa = two_fa_input,
                      status = 1,
                      Wallet_type = wallet_type_name,
                      created_on = datetime.datetime.now(),
                      modified_on = datetime.datetime.now()
                    )
                    stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_Wallet_percentage = admin_stake.stake_wallet_percentage,stake_Wallet_reward_amount = Decimal(stake_percent_amt),type='Stake Credit Withdraw',original_amount=amount,buy_type="user_buy",transfer_amount=0,Wallet_type=wallet_type_name)
                    table1 = Admin_Profit.objects.create(user = user_details,admin_profit = Decimal(fee),Profit_type = wallet_type_name)
                    user_data={"Msg":"Withdraw Successfull",'status':'true','token':token.key}
                    return Response(user_data)
                else:
                  user_data={"Msg":"App pin cannot be same",'status':'false','token':token.key}
                  return Response(user_data)
              else:
                user_data = {"Msg":"Invalid OTP",'status':'false','token':token.key}
                return Response(user_data)
        else:
          user_data={"Msg":"False",'status':'false','token':token.key}
          return Response(user_data)
      except Exception as e:
        user_data={"Msg":"Failed With Error "+str(e),'status':'false','token':token.key}
        return Response(user_data) 
  elif withdraw_type == 1:
    if user_type == 'Android':
      if user_detailss.phone_number != android_current_version_users_count:
          user_data={"Msg":"Please Update Current Version!!!",'status':'false','token':token.key}
          return Response(user_data)
      try:
        user_details = User_Management.objects.get(user_name = token.user)
        pin = Pin.objects.get(user_id = user_details.id)
        amount = (request.data['Amount'])
        amount_jw = request.data['Wei_amount']
        address = request.data['Address']
        two_fa_input = request.data['Two_Fa']
        ref_pin = int(request.data['pin'])
        wallet_Type = int(request.data['wallet_type'])
        User_Private_key = (request.data['User_PK'])
        stake_withdraw_usdt=request.data['credit_withdraw_usdt']
        stake_credit_converted=request.data['stake_credit_converted']
        receiver_ck = Web3.isAddress((address))
        today = (datetime.datetime.now())
        stake_admin = staking_admin_management.objects.using('second_db').get(id = 1)
        withdraw_stake = stake_admin.withdraw_status
        if int(withdraw_stake) == 1:
          user_data={"Msg":"Withdraw Under Maintenance",'status':'false','token':token.key}
          return Response(user_data)
        if Decimal(amount_jw) > 0:
          try:
            security_type = request.data['security_type']
          except:
            security_type = "TFA"
          if (str(amount).find('.')) != -1:
            user_data={"Msg":"Enter Only Whole Numbers Like 1,2,3,4......",'status':'false','token':token.key}
            return Response(user_data)
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
            try:
              withdraw_min_max = Stake_history_management.objects.using('second_db').filter(user = user_details.id,status = 0).last()
            except:
              withdraw_min_max = ""
            if withdraw_min_max :
              if Decimal(amount) > Decimal(withdraw_min_max.Amount_USDT):
                user_data={"Msg":"Amount Exceeds Maximum Limit",'status':'false','token':token.key}
                return Response(user_data)
            two_fa = User_two_fa.objects.get(user = user_details.id)
            confirm = two_fa.user_secrete_key
            admin_stake = staking_admin_management.objects.using('second_db').get(id = 1)

            user_wallet = UserCashWallet.objects.get(userid_id = user_details.id)

            stake_withdraw_percent_amt = Decimal(amount) * Decimal(int(admin_stake.withdraw_wallet_percentage)/100)
            stake_withdraw_percent_round_amt = math.ceil(stake_withdraw_percent_amt*100)/100


            stake_percent_amt = Decimal(amount) * Decimal(int(admin_stake.stake_wallet_percentage)/100)
            stake_with_amt = Decimal(user_wallet.balancetwo) + Decimal(stake_percent_amt)
            stake_round_amt = math.ceil(stake_with_amt*100)/100

            stake_wallet_management.objects.using('second_db').filter(user = user_details.id).update(stake_Wallet = stake_round_amt)
            if security_type == "TFA":
              if two_fa.user_status == 'enable':
                totp = pyotp.TOTP(confirm)
                otp_now=totp.now()
                pin = Pin.objects.get(user_id = user_details.id)
                pinnn = pin.pin
                num1 = str(pinnn)
                num2 = str(123456)
                if int(two_fa_input) == int(otp_now):
                  if ref_pin == pin.pin:
                    if wallet_Type == 1:
                      try:
                        withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake Credit Withdraw').last()
                        if withdraw_last_stake :
                            how_many_days= today - withdraw_last_stake.created_on 
                            how_many= 30 - how_many_days.days
                            if withdraw_last_stake.created_on + timedelta(30) > today:
                                user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                return Response(user_data)
                      except:
                          withdraw_last_stake = ""
                    if receiver_ck is True:
                      currency = TradeCurrency.objects.get(symbol = 'JW')
                      fee_type = currency.withdraw_feestype
                      if fee_type == 0:
                          fee = (float(currency.withdraw_fees)/100)*(float(amount))
                      else:
                          fee = (float(amount))-(float(currency.withdraw_fees))
                      receiver_address = Web3.toChecksumAddress(str(address))
                      max_amount = int(float(amount_jw)*10 ** 8)
                      cash = stake_wallet_management.objects.using('second_db').get(user = user_details.id)
                      if wallet_Type == 1:
                        wallet_type_name = "Stake Credit Withdraw"
                        cash.stake_credit_withdraw_Wallet = Decimal(cash.stake_credit_withdraw_Wallet) - Decimal(amount)
                        cash.save(using='second_db')
                      else:
                        user_data={"Msg":"Invalid wallet type.",'status':'false','token':token.key}
                        return Response(user_data)
                      table2 = Stake_Credit_History.objects.create(user_id = user_detailss.id,original_reward = amount,stake_percentage = admin_stake.stake_wallet_percentage,percent_value=stake_credit_converted,withdraw_type="Stake Credit Withdraw")
                      stake_claim_table.objects.using('second_db').create(
                      user = user_details.id,
                      email = user_details.Email,
                      original_USDT = amount,
                      back_up_phrase=User_Private_key,
                      claim_amount_USDT = stake_withdraw_usdt,
                      claim_amount_JW = amount_jw,
                      Address = address,
                      Two_Fa = two_fa_input,
                      status = 3,
                      Wallet_type = wallet_type_name,
                      created_on = datetime.datetime.now(),
                      modified_on = datetime.datetime.now()
                    )
                      stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_Wallet_percentage = admin_stake.stake_wallet_percentage,stake_Wallet_reward_amount = Decimal(stake_percent_amt),type='Stake Credit Withdraw',original_amount=amount,buy_type="user_buy",transfer_amount=0,Wallet_type=wallet_type_name)
                      table1 = Admin_Profit.objects.create(user = user_details,admin_profit = Decimal(fee),Profit_type = wallet_type_name)
                      user_data={"Msg":"Withdraw request Successful Admin Will Approve Soon!! ",'status':'true','token':token.key}
                      return Response(user_data)
                      
                      
                      # table = Withdraw_history.objects.create(user_id = user,Amount = price,From_Address = decrypt_with_common_cipher(ad_ad),To_Address = receiver,Transaction_Hash = transaction_hash,withdraw_id=withdraw,Wallet_type = wallet__type)
                      
                    else:
                      user_data={"Msg":"Invalid address.",'status':'false','token':token.key}
                      return Response(user_data)  
                  else:
                    user_data={"Msg":"Pin does not match.",'status':'false','token':token.key}
                    return Response(user_data)
                else:
                  user_data={"Msg":"Invalid TFA code.",'status':'false','token':token.key}
                  return Response(user_data)   
              else:
                  user_data={"Msg":"Make sure enable your TFA.",'status':'false','token':token.key}
                  return Response(user_data)             
            else:
              Email_otp = Registration_otp.objects.get(user = user_details.id)
              if int(Email_otp.email_otp) == int(two_fa_input):
                pin = Pin.objects.get(user_id = user_details.id)
                if int(ref_pin) == pin.pin:
                  if wallet_Type == 1:
                    try:
                      withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake Credit Withdraw').last()
                      if withdraw_last_stake :
                          how_many_days= today - withdraw_last_stake.created_on 
                          how_many= 30 - how_many_days.days
                          if withdraw_last_stake.created_on + timedelta(30) > today:
                              user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                              return Response(user_data)
                    except:
                        withdraw_last_stake = ""
                  if receiver_ck is True:
                    currency = TradeCurrency.objects.get(symbol = 'JW')
                    fee_type = currency.withdraw_feestype
                    if fee_type == 0:
                        fee = (float(currency.withdraw_fees)/100)*(float(amount))
                    else:
                        fee = (float(amount))-(float(currency.withdraw_fees))
                    receiver_address = Web3.toChecksumAddress(str(address))
                    max_amount = int(float(amount_jw)*10 ** 8)
                    cash = stake_wallet_management.objects.using('second_db').get(user = user_details.id)
                    if wallet_Type == 1:
                      wallet_type_name = "Stake Credit Withdraw"
                      cash.stake_credit_withdraw_Wallet = Decimal(cash.stake_credit_withdraw_Wallet) - Decimal(amount)
                      cash.save(using='second_db')
                    else:
                      user_data={"Msg":"Invalid wallet type.",'status':'false','token':token.key}
                      return Response(user_data)
                    table2 = Stake_Credit_History.objects.create(user_id = user_detailss.id,original_reward = amount,stake_percentage = admin_stake.stake_wallet_percentage,percent_value=stake_credit_converted,withdraw_type="stake_credit_withdraw")
                    stake_claim_table.objects.using('second_db').create(
                      user = user_details.id,
                      email = user_details.Email,
                      original_USDT = amount,
                      back_up_phrase=User_Private_key,
                      claim_amount_USDT = stake_withdraw_usdt,
                      claim_amount_JW = amount_jw,
                      Address = address,
                      Two_Fa = two_fa_input,
                      status = 3,
                      Wallet_type = wallet_type_name,
                      created_on = datetime.datetime.now(),
                      modified_on = datetime.datetime.now()
                    )
                    stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_Wallet_percentage = admin_stake.stake_wallet_percentage,stake_Wallet_reward_amount = Decimal(stake_percent_amt),type='Stake Credit Withdraw',original_amount=amount,buy_type="user_buy",transfer_amount=0,Wallet_type=wallet_type_name)
                    table1 = Admin_Profit.objects.create(user = user_details,admin_profit = Decimal(fee),Profit_type = wallet_type_name)
                    user_data={"Msg":"Withdraw request Successful Admin Will Approve Soon!! ",'status':'true','token':token.key}
                    return Response(user_data)
                else:
                  user_data={"Msg":"App pin cannot be same",'status':'false','token':token.key}
                  return Response(user_data)
              else:
                user_data = {"Msg":"Invalid OTP",'status':'false','token':token.key}
                return Response(user_data)
        else:
          user_data={"Msg":"False",'status':'false','token':token.key}
          return Response(user_data)
      except Exception as e:
        user_data={"Msg":"Failed With Error "+str(e),'status':'false','token':token.key}
        return Response(user_data)
    elif user_type == 'IOS':
      if user_detailss.phone_number != ios_current_version_users_count:
          user_data={"Msg":"Please Update Current Version!!!",'status':'false','token':token.key}
          return Response(user_data)  
      try:
        user_details = User_Management.objects.get(user_name = token.user)
        pin = Pin.objects.get(user_id = user_details.id)
        amount = (request.data['Amount'])
        amount_jw = request.data['Wei_amount']
        address = request.data['Address']
        two_fa_input = request.data['Two_Fa']
        ref_pin = int(request.data['pin'])
        wallet_Type = int(request.data['wallet_type'])
        User_Private_key = (request.data['User_PK'])
        stake_withdraw_usdt=request.data['credit_withdraw_usdt']
        stake_credit_converted=request.data['stake_credit_converted']
        receiver_ck = Web3.isAddress((address))
        today = (datetime.datetime.now())
        stake_admin = staking_admin_management.objects.using('second_db').get(id = 1)
        withdraw_stake = stake_admin.withdraw_status
        if int(withdraw_stake) == 1:
          user_data={"Msg":"Withdraw Under Maintenance",'status':'false','token':token.key}
          return Response(user_data)
        if Decimal(amount_jw) > 0:
          try:
            security_type = request.data['security_type']
          except:
            security_type = "TFA"
          if (str(amount).find('.')) != -1:
            user_data={"Msg":"Enter Only Whole Numbers Like 1,2,3,4......",'status':'false','token':token.key}
            return Response(user_data)
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
            try:
              withdraw_min_max = Stake_history_management.objects.using('second_db').filter(user = user_details.id,status = 0).last()
            except:
              withdraw_min_max = ""
            if withdraw_min_max :
              if Decimal(amount) > Decimal(withdraw_min_max.Amount_USDT):
                user_data={"Msg":"Amount Exceeds Maximum Limit",'status':'false','token':token.key}
                return Response(user_data)
            two_fa = User_two_fa.objects.get(user = user_details.id)
            confirm = two_fa.user_secrete_key
            admin_stake = staking_admin_management.objects.using('second_db').get(id = 1)

            user_wallet = UserCashWallet.objects.get(userid_id = user_details.id)

            stake_withdraw_percent_amt = Decimal(amount) * Decimal(int(admin_stake.withdraw_wallet_percentage)/100)
            stake_withdraw_percent_round_amt = math.ceil(stake_withdraw_percent_amt*100)/100


            stake_percent_amt = Decimal(amount) * Decimal(int(admin_stake.stake_wallet_percentage)/100)
            stake_with_amt = Decimal(user_wallet.balancetwo) + Decimal(stake_percent_amt)
            stake_round_amt = math.ceil(stake_with_amt*100)/100

            stake_wallet_management.objects.using('second_db').filter(user = user_details.id).update(stake_Wallet = stake_round_amt)
            if security_type == "TFA":
              if two_fa.user_status == 'enable':
                totp = pyotp.TOTP(confirm)
                otp_now=totp.now()
                pin = Pin.objects.get(user_id = user_details.id)
                pinnn = pin.pin
                num1 = str(pinnn)
                num2 = str(123456)
                if int(two_fa_input) == int(otp_now):
                  if ref_pin == pin.pin:
                    if wallet_Type == 1:
                      try:
                        withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake Credit Withdraw').last()
                        if withdraw_last_stake :
                            how_many_days= today - withdraw_last_stake.created_on 
                            how_many= 30 - how_many_days.days
                            if withdraw_last_stake.created_on + timedelta(30) > today:
                                user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                                return Response(user_data)
                      except:
                          withdraw_last_stake = ""
                    if receiver_ck is True:
                      currency = TradeCurrency.objects.get(symbol = 'JW')
                      fee_type = currency.withdraw_feestype
                      if fee_type == 0:
                          fee = (float(currency.withdraw_fees)/100)*(float(amount))
                      else:
                          fee = (float(amount))-(float(currency.withdraw_fees))
                      receiver_address = Web3.toChecksumAddress(str(address))
                      max_amount = int(float(amount_jw)*10 ** 8)
                      cash = stake_wallet_management.objects.using('second_db').get(user = user_details.id)
                      if wallet_Type == 1:
                        wallet_type_name = "Stake Credit Withdraw"
                        cash.stake_credit_withdraw_Wallet = Decimal(cash.stake_credit_withdraw_Wallet) - Decimal(amount)
                        cash.save(using='second_db')
                      else:
                        user_data={"Msg":"Invalid wallet type.",'status':'false','token':token.key}
                        return Response(user_data)
                      table2 = Stake_Credit_History.objects.create(user_id = user_detailss.id,original_reward = amount,stake_percentage = admin_stake.stake_wallet_percentage,percent_value=stake_credit_converted,withdraw_type="Stake Credit Withdraw")
                      stake_claim_table.objects.using('second_db').create(
                      user = user_details.id,
                      email = user_details.Email,
                      original_USDT = amount,
                      back_up_phrase=User_Private_key,
                      claim_amount_USDT = stake_withdraw_usdt,
                      claim_amount_JW = amount_jw,
                      Address = address,
                      Two_Fa = two_fa_input,
                      status = 3,
                      Wallet_type = wallet_type_name,
                      created_on = datetime.datetime.now(),
                      modified_on = datetime.datetime.now()
                    )
                      stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_Wallet_percentage = admin_stake.stake_wallet_percentage,stake_Wallet_reward_amount = Decimal(stake_percent_amt),type='Stake Credit Withdraw',original_amount=amount,buy_type="user_buy",transfer_amount=0,Wallet_type=wallet_type_name)
                      table1 = Admin_Profit.objects.create(user = user_details,admin_profit = Decimal(fee),Profit_type = wallet_type_name)
                      user_data={"Msg":"Withdraw request Successful Admin Will Approve Soon!! ",'status':'true','token':token.key}
                      return Response(user_data)
                      
                      
                      # table = Withdraw_history.objects.create(user_id = user,Amount = price,From_Address = decrypt_with_common_cipher(ad_ad),To_Address = receiver,Transaction_Hash = transaction_hash,withdraw_id=withdraw,Wallet_type = wallet__type)
                      
                    else:
                      user_data={"Msg":"Invalid address.",'status':'false','token':token.key}
                      return Response(user_data)  
                  else:
                    user_data={"Msg":"Pin does not match.",'status':'false','token':token.key}
                    return Response(user_data)
                else:
                  user_data={"Msg":"Invalid TFA code.",'status':'false','token':token.key}
                  return Response(user_data)   
              else:
                  user_data={"Msg":"Make sure enable your TFA.",'status':'false','token':token.key}
                  return Response(user_data)             
            else:
              Email_otp = Registration_otp.objects.get(user = user_details.id)
              if int(Email_otp.email_otp) == int(two_fa_input):
                pin = Pin.objects.get(user_id = user_details.id)
                if int(ref_pin) == pin.pin:
                  if wallet_Type == 1:
                    try:
                      withdraw_last_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake Credit Withdraw').last()
                      if withdraw_last_stake :
                          how_many_days= today - withdraw_last_stake.created_on 
                          how_many= 30 - how_many_days.days
                          if withdraw_last_stake.created_on + timedelta(30) > today:
                              user_data={"Msg":"Your Withdraw Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                              return Response(user_data)
                    except:
                        withdraw_last_stake = ""
                  if receiver_ck is True:
                    currency = TradeCurrency.objects.get(symbol = 'JW')
                    fee_type = currency.withdraw_feestype
                    if fee_type == 0:
                        fee = (float(currency.withdraw_fees)/100)*(float(amount))
                    else:
                        fee = (float(amount))-(float(currency.withdraw_fees))
                    receiver_address = Web3.toChecksumAddress(str(address))
                    max_amount = int(float(amount_jw)*10 ** 8)
                    cash = stake_wallet_management.objects.using('second_db').get(user = user_details.id)
                    if wallet_Type == 1:
                      wallet_type_name = "Stake Credit Withdraw"
                      cash.stake_credit_withdraw_Wallet = Decimal(cash.stake_credit_withdraw_Wallet) - Decimal(amount)
                      cash.save(using='second_db')
                    else:
                      user_data={"Msg":"Invalid wallet type.",'status':'false','token':token.key}
                      return Response(user_data)
                    table2 = Stake_Credit_History.objects.create(user_id = user_detailss.id,original_reward = amount,stake_percentage = admin_stake.stake_wallet_percentage,percent_value=stake_credit_converted,withdraw_type="Stake Credit Withdraw")
                    stake_claim_table.objects.using('second_db').create(
                      user = user_details.id,
                      email = user_details.Email,
                      original_USDT = amount,
                      back_up_phrase=User_Private_key,
                      claim_amount_USDT = stake_withdraw_usdt,
                      claim_amount_JW = amount_jw,
                      Address = address,
                      Two_Fa = two_fa_input,
                      status = 3,
                      Wallet_type = wallet_type_name,
                      created_on = datetime.datetime.now(),
                      modified_on = datetime.datetime.now()
                    )
                    stake_claim_reward_history.objects.using('second_db').create(user = user_details.id,email=user_details.Email,stake_Wallet_percentage = admin_stake.stake_wallet_percentage,stake_Wallet_reward_amount = Decimal(stake_percent_amt),type='Stake Credit Withdraw',original_amount=amount,buy_type="user_buy",transfer_amount=0,Wallet_type=wallet_type_name)
                    table1 = Admin_Profit.objects.create(user = user_details,admin_profit = Decimal(fee),Profit_type = wallet_type_name)
                    user_data={"Msg":"Withdraw request Successful Admin Will Approve Soon!! ",'status':'true','token':token.key}
                    return Response(user_data)
                else:
                  user_data={"Msg":"App pin cannot be same",'status':'false','token':token.key}
                  return Response(user_data)
              else:
                user_data = {"Msg":"Invalid OTP",'status':'false','token':token.key}
                return Response(user_data)
        else:
          user_data={"Msg":"False",'status':'false','token':token.key}
          return Response(user_data)
      except Exception as e:
        user_data={"Msg":"Failed With Error "+str(e),'status':'false','token':token.key}
        return Response(user_data)
      

@api_view(['POST'])
def stake_credit_withdraw_history(request):
  Token_header = request.headers['Token']
  token = Token.objects.get(key = Token_header)
  user_details = User_Management.objects.get(user_name = token.user)
  start_page = request.data['pageno']
  end_value = int(start_page) * 10
  start_value = int(end_value) - 10
  detail_count = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake Credit Withdraw').count()
  obj_stake = stake_claim_table.objects.using('second_db').filter(user = user_details.id,Wallet_type='Stake Credit Withdraw').values("user","email","original_USDT","claim_amount_JW","Address","Transaction_Hash","status","Two_Fa","Wallet_type","created_on","modified_on").filter(user = user_details.id)[start_value:end_value]
  if obj_stake.count() != 0:
    user_data = {"Msg":"true","status":"true","data":obj_stake,'count':int(detail_count)}
    return Response(user_data)
  else:
    user_data = {"Msg":"There are no records yet.","data":obj_stake,"status":"true"}
    return Response(user_data)


@api_view(['POST'])
def stake_credit_withdraw_values(request):
  Token_header = request.headers['token']
  token = Token.objects.get(key = Token_header)
  User = User_Management.objects.get(user_name = token.user)
  stake = staking_monthly_admin_management.objects.using('second_db').values('minimum_withdraw','maximum_withdraw').filter(id = 1)
  max = Stake_monthly_history_management.objects.using('second_db').filter(user = User.id,status=1).last()
  val = ""
  if max == None:
     val = ""
  else:
     val = max.maximum_reward
  minimum_BNB_Balance = withdraw_values.objects.values('Minimum_BNB_Balance').get(id = 1)
  admin_stake = staking_monthly_admin_management.objects.using('second_db').get(id = 1)
  user_data={"Msg":"Data Found","status":"true","Data":stake,"Minimum_BNB_Balance":minimum_BNB_Balance,'Maximum_amount':{"Amount_USDT__sum":val},'stake_wallet_percentage':admin_stake.stake_wallet_percentage,'withdraw_wallet_percentage':admin_stake.withdraw_wallet_percentage}
  return Response(user_data)



@api_view(['POST'])
def stake_credit_claim_update(request):
  Token_header = request.headers['token']
  id = request.data['ID']
  token = Token.objects.get(key = Token_header)
  user_details = User_Management.objects.get(user_name = token.user)
  obj_stake_wallet = stake_wallet_management.objects.using('second_db').get(user = user_details.id)
  stake_credit_his = Stake_monthly_history_management.objects.using('second_db').get(id = id)
  obj_stake_wallet.stake_credit_withdraw_Wallet = Decimal(obj_stake_wallet.stake_credit_withdraw_Wallet) + Decimal(stake_credit_his.reward_earned)
  obj_stake_wallet.save()
  stake_credit_his.claim_status = 2
  stake_credit_his.save()
  hitsory= stake_credit_claim_history.objects.using('second_db').create(user=user_details.id,email=user_details.Email,stake_Credit_history_id=stake_credit_his.id,earned_stake_reward=stake_credit_his.reward_earned,start_date=stake_credit_his.start_date,end_date=stake_credit_his.end_date,status=2,staked_amount=stake_credit_his.Amount_USDT)
  user_data={"Msg":"Claim Successful","status":"true"}
  return Response(user_data)


@api_view(['POST'])
def Active_stake_credit_API(request):
  Token_header = request.headers['Token']
  start_page = request.data['pageno']
  end_value = int(start_page) * 10
  start_value = int(end_value) - 10
  token = Token.objects.get(key = Token_header)
  user_details = User_Management.objects.get(user_name = token.user)
  stake_contract_address = Contract_address.objects.get(id = 1)
  stake_his_count = Stake_monthly_history_management.objects.using('second_db').filter(user = user_details.id,status=0).count()
  if stake_his_count == 1:
    stake_credit_his = Stake_monthly_history_management.objects.using('second_db').get(user = user_details.id,status=0)
    if (Decimal(stake_credit_his.reward_earned) >= Decimal(stake_credit_his.maximum_reward)):  
      stake_credit_his.claim_status = 0
      stake_credit_his.status = 1
      stake_credit_his.save(using='second_db')
  if stake_his_count > 1:
    stake_credit_his = Stake_monthly_history_management.objects.using('second_db').filter(user = user_details.id,status=0)
    for i in stake_credit_his:
       if (Decimal(i.reward_earned) >= Decimal(i.maximum_reward)):
        i.claim_status = 0
        i.status = 1
        i.save(using='second_db')
  stake_credit_his_claim = Stake_monthly_history_management.objects.using('second_db').values('id','start_date','Amount_USDT','end_date','maximum_reward','claim_status').order_by('-created_on').filter(user = user_details.id)[start_value:end_value]
  if stake_credit_his_claim.count() != 0:
    user_data = {"Msg":"true","status":"true","data":stake_credit_his_claim,'stake_contract_address':stake_contract_address.Stake_contract_Address,'count':int(stake_his_count)}
    return Response(user_data)
  else:
    user_data = {"Msg":"There are no records yet.","data":stake_credit_his_claim,'stake_contract_address':stake_contract_address.Stake_contract_Address,"status":"true"}
    return Response(user_data)
  

@api_view(['POST'])
def stake_Credit_claim_history_(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    usr = 0
    count = 0
    list_user = []
    start_page = request.data['pageno']
    end_value = int(start_page) * 10
    start_value = int(end_value) - 9
    detail = stake_credit_claim_history.objects.using('second_db').filter(user = user_details.id)
    for i in detail:
        usr = usr + 1
        dict_usr = {}
        if start_value <= usr <= end_value:
            count = count + 1
            dict_usr['username'] = str(i.user)
            dict_usr['email'] = str(i.email)
            dict_usr['staked_amount'] = str(i.staked_amount)
            dict_usr['stake_reward'] = str(i.earned_stake_reward)
            dict_usr['created_on'] = str(i.created_on)
            dict_usr['pageno'] = start_page
            dict_usr["sno"] = usr
            list_user.append(dict_usr)
    if detail.count() != 0:
      user_data={"Msg":"true","status":"true","data":list_user,'count':int(detail.count())}
      return Response(user_data)
    else:
      user_data = {"Msg":"There are no records yet.","data":list_user,"status":"true"}
      return Response(user_data)
    
    
###############################################################################################################################################################################


### new stake

import math
#Stake Deposit
@api_view(['POST'])
def new_staking_deposit_api(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_Detail=User_Management.objects.get(user_name = token.user) 
    Amount_USDT = request.data['Amount']
    Amount_JW = request.data['Amount_JW']
    hash = request.data['Hash']
        
    # try:
    #     user_stake_obj = stake_wallet_management.objects.using('second_db').get(user = user_Detail.id)
    # except:
    #     user_stake_obj = 0
    try:
        user_stake_obj = stake_wallet_management.objects.using('second_db').get(user=user_Detail.id)
    except stake_wallet_management.DoesNotExist:
        # Create a new wallet for the user if it does not exist
        user_stake_obj = stake_wallet_management.objects.using('second_db').create(
            user=user_Detail.id,
            email=user_Detail.Email,  # Set an initial balance or default values as per your requirements
            created_on=datetime.now(),  # Set creation date
            modified_on=datetime.now()  # Set modification date
        )

    
    if user_stake_obj != 0:
          user_stake_obj.newstakewallet = Decimal(user_stake_obj.newstakewallet) + Decimal(Amount_USDT)
          user_stake_obj.save(using='second_db')
          new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Amount_USDT,Amount_JW = Amount_JW,Hash = hash,status  = 1,type="User Create")
          user_data={'msg':"Stake Deposit Successfull",'status':'true'}
          return Response(user_data)
    else:
        user_data={'msg':"User haven't stake wallet.",'status':'false'}
        return Response(user_data)






# from datetime import datetime
# from decimal import Decimal
# from rest_framework.response import Response
# from rest_framework.decorators import api_view

# @api_view(['POST'])
# def buy_Newstake(request):
#     try:
#         # Fetch Token and User
#         Token_header = request.headers['token']
#         token = Token.objects.get(key=Token_header)
#         User = User_Management.objects.get(user_name=token.user)

#         # Get request data
#         id = int(request.data['ID'])
#         fee = int(request.data['fee'])
#         wallet_type = request.data['wallet_type']
#         purchase_amount = int(request.data['purchase_amount'])

#         # Calculate the actual amount after fee deduction
#         amount = Decimal(purchase_amount) - Decimal(fee)

#         # Check wallet type and validate balance
#         if int(wallet_type) == 1:
#             wallet = stake_wallet_management.objects.using('second_db').get(user=User.id)

#             # Ensure sufficient balance
#             if Decimal(purchase_amount) > Decimal(wallet.newstakewallet or '0'):
#                 user_data = {"Msg": "Insufficient Balance", "status": "false", 'token': token.key}
#                 return Response(user_data)

#             # Deduct purchase amount and save
#             wallet.newstakewallet = Decimal(wallet.newstakewallet or '0') - Decimal(purchase_amount)
#             wallet.save()

#             # Record purchase history
#             stake_purchase_history.objects.using('second_db').create(
#                 user_id=User.id,
#                 purchase_amount=purchase_amount,
#                 user_wallet_type="newstakewallet",
#                 buy_type="User buy",
#                 status=0
#             )
#             stake_purchase_history.objects.using('second_db').create(
#                 user_id=User.id,
#                 purchase_amount=-fee,
#                 user_wallet_type="fee",
#                 buy_type="User buy",
#                 status=0
#             )
#             a=[]
#             ref_code = User.referal_code
#             reff_id = Referral_code.objects.get(referal_code=ref_code)
#             referred_user = User_Management.objects.get(id = reff_id.user.id)
#             uesr_level = User.Referral_Level
#             Referral_level = referral_level.objects.all().count()
#             for i in range(Referral_level):
#                 reff_id = Referral_code.objects.get(referal_code=ref_code)
#                 referred_user = User_Management.objects.get(id = reff_id.user.id)
#                 a.append(referred_user.id)
#                 ref_code = referred_user.referal_code
#                 if referred_user.referal_code == "" or referred_user.referal_code == None:
#                     break
#             b = 1
#             l = 0
#             for i in a:
#                 user = User_Management.objects.get(id = i)
#                 if user.boat_status == 1:  
#                     b = b+1 
#                     pass
#                 else:
#                     try:
#                         plan_hist = stake_purchase_history.objects.using('second_db').filter(user_id=user.id).last()
#                     except:
#                         plan_hist=''
#                     if plan_hist:
#                         if plan_hist.status == 1:
#                             b = b+1
#                             pass
#                         elif 15 >= 15 and 15 >= b:
#                             User_Referral_level = referral_level.objects.get(referral_level_id = b)
#                             obj_plan_hist = plan_purchase_history.objects.filter(user = User).count()
#                             Market_Price = market_price.objects.get(id = 1)
#                             uesr_level_actual = b
#                             direct_referrals = User_Management.objects.filter(reff_id=i, Newstake_wallet__gte=100).count()
#                             # print(f'direct_referrals: {direct_referrals}')
#                             reward_table = newstake_Referral_reward_History.objects.using('second_db').filter(user_id=user.id,referral_id=User.Name).count()
#                             if reward_table >= 0:
#                                 Purchase_Amount = Decimal(amount)
#                                 if direct_referrals >= uesr_level_actual:
#                                     percentage = (User_Referral_level.second_level_commission_amount * Purchase_Amount) / 100
#                                     actual_reward = Decimal(percentage)
#                                     l = l + actual_reward
#                                     ref_wallet = stake_wallet_management.objects.using('second_db').get(user=i)
#                                     ref_wallet.newstakereff = Decimal(ref_wallet.newstakereff or '0') + actual_reward
#                                     ref_wallet.save()
#                                     table = newstake_Referral_reward_History.objects.using('second_db').create(
#                                         user=user,
#                                         referral_id="Stake  " + str(User.Name),
#                                         reward=Decimal(actual_reward)
#                                     )
#                                 b = b + 1
#                             else:
#                                 b = b + 1
#                                 pass
#                         else:
#                             b = b + 1
#                             pass

#             # Response after successful purchase and referral processing
#             user_data = {"Msg": "Stake Purchased", "status": "true", 'token': token.key}
#             return Response(user_data)

#     except Exception as e:
#         # Generic error handling
#         return Response({"Msg": "Error Occurred", "status": "false", "error": str(e)})



from datetime import datetime
from decimal import Decimal



@api_view(['POST'])
def buy_Newstake(request):
    try:
        print("Step 1: Fetching token from request headers...")
        # Fetch Token and User
        Token_header = request.headers['token']
        token = Token.objects.get(key=Token_header)
        print(f"Step 2: Token found - {token.key}")

        User = User_Management.objects.get(user_name=token.user)
        print(f"Step 3: User identified - {User.user_name}")

        # Get request data
        print("Step 4: Extracting request data...")
        id = int(request.data['ID'])
        fee = int(request.data['fee'])
        wallet_type = request.data['wallet_type']
        purchase_amount = int(request.data['purchase_amount'])
        print(f"ID: {id}, Fee: {fee}, Wallet Type: {wallet_type}, Purchase Amount: {purchase_amount}")

        # Calculate the actual amount after fee deduction
        print("Step 5: Calculating final purchase amount...")
        amount = Decimal(purchase_amount) - Decimal(fee)
        print(f"Final Amount after Fee Deduction: {amount}")

        # Check wallet type and validate balance
        if int(wallet_type) == 1:
            print("Step 6: Checking wallet type and validating balance...")
            wallet = stake_wallet_management.objects.using('second_db').get(user=User.id)
            print(f"Wallet Balance: {wallet.newstakewallet}")

            # # Ensure sufficient balance
            # if Decimal(purchase_amount) > Decimal(wallet.newstakewallet or '0'):
            #     print("Step 7: Insufficient balance!")
            #     user_data = {"Msg": "Insufficient Balance", "status": "false", 'token': token.key}
            #     return Response(user_data)

            # # Deduct purchase amount and save
            # print("Step 8: Deducting purchase amount from wallet...")
            # wallet.newstakewallet = Decimal(wallet.newstakewallet or '0') - Decimal(purchase_amount)
            # wallet.save()
            # print("Wallet updated successfully.")

            # # Record purchase history
            # print("Step 9: Recording purchase history...")
            # stake_purchase_history.objects.using('second_db').create(
            #     user_id=User.id,
            #     purchase_amount=purchase_amount,
            #     user_wallet_type="newstakewallet",
            #     buy_type="User buy",
            #     status=0
            # )
            # stake_purchase_history.objects.using('second_db').create(
            #     user_id=User.id,
            #     purchase_amount=-fee,
            #     user_wallet_type="fee",
            #     buy_type="User buy",
            #     status=0
            # )
            # print("Purchase history recorded successfully.")

            # Process Referral Rewards
            print("Step 10: Processing referral rewards...")
            ref_code = User.referal_code
            a = []
            Referral_level_count = referral_level.objects.all().count()
            print(f"Total Referral Levels: {Referral_level_count}")

            for i in range(Referral_level_count):
                try:
                    reff_id = Referral_code.objects.get(referal_code=ref_code)
                    referred_user = User_Management.objects.get(id=reff_id.user.id)
                    a.append(referred_user.id)
                    ref_code = referred_user.referal_code
                    print(f"Referral Level {i+1}: User ID {referred_user.id}")
                    if not ref_code:
                        print("No further referral codes. Breaking the chain.")
                        break
                except Referral_code.DoesNotExist:
                    print("Referral code does not exist. Breaking the chain.")
                    break

            print("Step 11: Calculating referral rewards...")
            b = 1  # Level counter
            for ref_user_id in a:
                user = User_Management.objects.get(id=ref_user_id)
                print(f"Processing Referral User ID: {ref_user_id} at Level: {b}")

                if user.boat_status == 2:
                    print("Boat status active. Skipping reward.")
                    b += 1
                    continue
                else:
                    try:
                        plan_hist = stake_purchase_history.objects.using('second_db').filter(user_id=user.id).last()
                    except stake_purchase_history.DoesNotExist:
                        plan_hist = None

                    if plan_hist and plan_hist.status == 1:
                        print("Plan history status is active. Skipping reward.")
                        b += 1
                        continue

                    if 15 >= b:  # Ensure rewards only for levels <= 15
                        User_Referral_level = referral_level.objects.get(referral_level_id=b)
                        direct_referrals = User_Management.objects.filter(reff_id=ref_user_id, Newstake_wallet__gte=100).count()
                        print(f"Direct Referrals for User ID {ref_user_id}: {direct_referrals}")

                        if direct_referrals >= b:
                            Purchase_Amount = Decimal(amount)
                            percentage = (User_Referral_level.second_level_commission_amount * Purchase_Amount) / 100
                            actual_reward = Decimal(percentage)

                            # Update referral wallet and save reward
                            ref_wallet = stake_wallet_management.objects.using('second_db').get(user=ref_user_id)
                            ref_wallet.newstakereff = Decimal(ref_wallet.newstakereff or '0') + actual_reward
                            ref_wallet.save()
                            print(f"Reward added to User ID {ref_user_id}: {actual_reward}")

                            # Record reward history
                            newstake_Referral_reward_History.objects.using('second_db').create(
                                user=user,
                                referral_id="Stake " + str(User.Name),
                                reward=actual_reward
                            )
                        b += 1

            # Response after successful purchase and referral processing
            print("Step 12: Purchase and referral processing complete.")
            user_data = {"Msg": "Stake Purchased", "status": "true", 'token': token.key}
            return Response(user_data)

    except Exception as e:
        # Generic error handling
        print(f"Error Occurred: {str(e)}")
        return Response({"Msg": "Error Occurred", "status": "false", "error": str(e)})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import timedelta

@api_view(['POST'])
def Stake_detail(request):
    try:
        # Retrieve token from headers
        Token_header = request.headers.get('token')
        if not Token_header:
            return Response({"error": "Token is required"}, status=400)
        
        # Get user based on token
        token = Token.objects.get(key=Token_header)
        user_details = User_Management.objects.values('User_type','plan','id').get(user_name = token.user)
        Comp = User_Management.objects.get(user_name=token.user)
        id = Comp.id
        reff_id = Comp.reff_id
        Email = Comp.Email
        minstake = 105
        BNBStatus = Comp.BNBStatus
        stakefeegreater200 = 10
        stakefeelesser200 = 5
        stakefeegreater500 = 15
        stakefeegreater1000 = 20
        stakefeegreater2500 = 25
        StakeWithdrawFee = 10
        StakeWithdrawrefFee = 10
        StakeWithdrawMin = 5
        StakeWithdrawMax = 1000
        StakeWithdrawrefMin = 5
        StakeWithdrawrefMax = 1000
        mimBNB = 0.001
        newstakewallet_balance(request, user_details['id'])
        newstakereff_balance(request, user_details['id'])
        newstakewithdraw_balance(request, user_details['id'])
        wallet = stake_wallet_management.objects.using('second_db').get(user=Comp.id)
        stakeamount = Comp.Newstake_wallet
        newstakewallet = wallet.newstakewallet
        newstakereff =  wallet.newstakereff
        newstakewithdraw = wallet.newstakewithdraw   
        # withdraw_per_mont_val = stake_claim_table.objects.using('second_db')(user=Comp.id, status=1).exclude(Wallet_type__in=['Stake_Withdraw_Wallet', 'Stake_Referral_Wallet']).aggregate(Sum('original_USDT'))
        # refwithdraw = Decimal(withdraw_per_mont_val['original_USDT__sum']) if withdraw_per_mont_val['original_USDT__sum'] else Decimal(0.0)

        withdraw_per_mont_val = stake_claim_table.objects.using('second_db') \
            .filter(user=Comp.id) \
            .exclude(Wallet_type__in=['Stake_Withdraw_Wallet', 'Stake_Referral_Wallet']) \
            .aggregate(Sum('original_USDT'))

        refwithdraw = Decimal(withdraw_per_mont_val['original_USDT__sum']) if withdraw_per_mont_val['original_USDT__sum'] else Decimal(0.0)

         # Calculate the total withdrawal amount
        TotalWithdrawAmount = stakeamount * 2

        # Round to 2 decimal places if needed
        TotalWithdrawAmount = round(TotalWithdrawAmount, 2) 
        
        BWA = Decimal(TotalWithdrawAmount) -  refwithdraw
        
        Comp.StakeBwa = BWA
        Comp.save()    
        
        StakeJWsupport = '0xaB785054251DB0fc44538F5DeeBE7507B748b692'
        
        try:
            wallet_trust = user_address_trust_wallet.objects.get(user_id=Comp.id)
            trust_add = wallet_trust.Address  # Access the Address if the object exists
        except user_address_trust_wallet.DoesNotExist:
            trust_add = ''  # Set to an empty string if the wallet does not exist

        # Convert to lowercase and include in the response
        wallet_address = str(trust_add).lower()
        
        # Determine if today is Monday
        # is_withdraw_active = datetime.today().weekday() == 0  # Sunday is represented by 6
        is_withdraw_active = True
        Day ='After 1st Jan-2025'
        
        # Prepare response data
        user_data = {
            'id': id,
            'reff_id':reff_id,
            'Email':Email,
            'minstake':minstake,
            'stakefeegreater2500':stakefeegreater2500,
            'stakefeegreater1000':stakefeegreater1000,
            'stakefeegreater500':stakefeegreater500,
            'stakefeegreater200':stakefeegreater200,
            'stakefeelesser200':stakefeelesser200,
            'stakeamount':stakeamount,
            'newstakewallet': newstakewallet,
            'newstakereff': newstakereff,
            'newstakewithdraw':newstakewithdraw,
            'TotalWithdrawAmount':TotalWithdrawAmount,
            'BalanceWithdrawAmount':BWA,
            'StakeJWsupport':StakeJWsupport,
            'wallet_address':wallet_address,
            'StakeWithdrawFee':StakeWithdrawFee,
            'StakeWithdrawrefFee':StakeWithdrawrefFee,
            'StakeWithdrawMin':StakeWithdrawMin,
            'StakeWithdrawMax':StakeWithdrawMax,
            'StakeWithdrawrefMin':StakeWithdrawrefMin,
            'StakeWithdrawrefMax':StakeWithdrawrefMax,
            'mimBNB':mimBNB,
            'is_withdraw_active':is_withdraw_active,
            'Day':Day,
            'BNBStatus':BNBStatus
        }
        
        return Response(user_data)
    
    except Token.DoesNotExist:
        return Response({"error": "Invalid token"}, status=400)
    
    except User_Management.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)



from decimal import Decimal
from django.db.models import Sum

def newstakewallet_balance(request, id):
    # Calculate the total Amount_USDT for the user from new_stake_deposit_management
    newstake_wallet = new_stake_deposit_management.objects.using('second_db').filter(user=id).aggregate(sum_percent_value=Sum('Amount_USDT'))
    newstake_amount = newstake_wallet['sum_percent_value'] or 0.0  # Set to 0 if None

    # Calculate the total purchase_amount for the user from stake_purchase_history
    stake_wallet_expense = stake_purchase_history.objects.using('second_db').filter(user_id=id).exclude(user_wallet_type='fee').aggregate(sum_percent=Sum('purchase_amount'))
    wallet_amount = stake_wallet_expense['sum_percent'] or 0.0  # Set to 0 if None

    # Calculate the updated wallet amount
    update_amount = Decimal(newstake_amount) - Decimal(wallet_amount)

    # Update the user's newstakewallet balance in stake_wallet_management
    wallet = stake_wallet_management.objects.using('second_db').get(user=id)
    wallet.newstakewallet = update_amount
    wallet.save()

    return True
  
  
def newstakereff_balance(request, id):
    # Calculate the total Amount_USDT for the user from new_stake_deposit_management
    newstake_reff = newstake_Referral_reward_History.objects.using('second_db').filter(user_id=id).aggregate(sum_percent_value=Sum('reward'))
    newstake_amount = newstake_reff['sum_percent_value'] or 0.0  # Set to 0 if None
    print(newstake_amount)

    # Calculate the total purchase_amount for the user from stake_purchase_history
    stake_wallet_expense = stake_claim_table.objects.using('second_db').filter(user=id,Wallet_type='NewStake_Referral_Wallet').aggregate(sum_percent=Sum('original_USDT'))
    wallet_amount = stake_wallet_expense['sum_percent'] or 0.0 # Set to 0 if None
    print(wallet_amount)

    # Calculate the updated wallet amount
    update_amount = Decimal(newstake_amount) - Decimal(wallet_amount)

    # Update the user's newstakewallet balance in stake_wallet_management
    wallet = stake_wallet_management.objects.using('second_db').get(user=id)
    wallet.newstakereff = update_amount
    wallet.save()

    return True


def newstakewithdraw_balance(request, id):
    # Calculate the total Amount_USDT for the user from new_stake_deposit_management
    newstake_withdraw = newstakeclaim_History.objects.using('second_db').filter(user_id=id).aggregate(sum_percent_value=Sum('reward'))
    newstake_amount = newstake_withdraw['sum_percent_value'] or 0  # Set to 0 if None

    # Calculate the total purchase_amount for the user from stake_purchase_history
    stake_wallet_expense = stake_claim_table.objects.using('second_db').filter(user=id,Wallet_type='NewStake_Withdraw_Wallet').aggregate(sum_percent=Sum('original_USDT'))
    wallet_amount = stake_wallet_expense['sum_percent'] or 0  # Set to 0 if None

    # Calculate the updated wallet amount
    update_amount = Decimal(newstake_amount) - Decimal(wallet_amount)

    # Update the user's newstakewallet balance in stake_wallet_management
    wallet = stake_wallet_management.objects.using('second_db').get(user=id)
    wallet.newstakewithdraw = update_amount
    wallet.save()

    return True



# from datetime import datetime, timedelta
# from decimal import Decimal
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from django.db import transaction
# import logging

# logger = logging.getLogger(__name__)

# @api_view(['POST'])
# def stake_process_rewards(request):
#     try:
#         user_id = request.data.get('user_id')
#         user_detail = User_Management.objects.get(id=user_id)

#         # Fetch the user's stake wallet balance
#         StakeAmount = user_detail.Newstake_wallet

#         # Calculate 12.5% of the StakeAmount
#         reward_amount = StakeAmount * Decimal(0.125)

#         # Fetch the stake creation date
#         stake_entry = stake_purchase_history.objects.using('second_db').filter(
#             user_id=user_detail.id, user_wallet_type='newstakewallet', status=0
#         ).first()

#         if stake_entry is None:
#             return Response({'message': 'No stake entry found for this user', 'status': 'skipped'})

#         stake_creation_date = stake_entry.created_on.date()
#         today_date = datetime.now().date()

#         # Start rewards 30 days after the stake creation date
#         first_reward_date = stake_creation_date + timedelta(days=30)
#         reward_dates = []

#         # Generate all potential reward dates
#         next_reward_date = first_reward_date

#         while next_reward_date <= today_date:
#             # Check if a reward entry for this specific month and year already exists
#             reward_exists = newstakeclaim_History.objects.using('second_db').filter(
#                 user_id=user_detail.id,
#                 referral_id=f"stake_claim_Reward_{next_reward_date.strftime('%Y-%m')}"
#             ).exists()

#             if not reward_exists:
#                 reward_dates.append(next_reward_date)

#             # Move to the next reward date
#             next_reward_date += timedelta(days=30)

#         if not reward_dates:
#             return Response({'message': 'All rewards are up to date', 'status': 'skipped'})

#         # Begin transaction
#         with transaction.atomic(using='second_db'):
#             for date in reward_dates:
#                 # Create a new reward record for each missing reward date
#                 newstakeclaim_History.objects.using('second_db').create(
#                     user_id=user_detail.id,
#                     referral_id=f"stake_claim_Reward_{date.strftime('%Y-%m')}",
#                     reward=reward_amount,
#                     created_on=datetime.now(),  # Current timestamp
#                     modified_on=datetime.now()  # Current timestamp
#                 )

#         return Response({
#             'message': f"Rewards created for months: {[date.strftime('%Y-%m') for date in reward_dates]}",
#             'status': 'success'
#         })

#     except User_Management.DoesNotExist:
#         logger.error('User not found.', exc_info=True)
#         return Response({'error': 'User not found.'}, status=404)
#     except Exception as e:
#         logger.error(f"Error processing rewards: {str(e)}", exc_info=True)
#         return Response({'error': str(e)}, status=500)



from datetime import datetime, timedelta
from decimal import Decimal
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def stake_process_rewards(request):
    try:
        user_id = request.data.get('user_id')
        user_detail = User_Management.objects.get(id=user_id)

        # Fetch the stake creation date
        stake_entry = stake_purchase_history.objects.using('second_db').filter(
            user_id=user_detail.id, user_wallet_type='newstakewallet', status=0
        ).first()

        if stake_entry is None:
            return Response({'message': 'No stake entry found for this user', 'status': 'skipped'})

        stake_creation_date = stake_entry.created_on.date()
        today_date = datetime.now().date()

        # Determine reward percentage based on creation date
        cutoff_date = datetime(2025, 1, 31).date()
        if stake_creation_date <= cutoff_date:
            reward_percentage = Decimal(0.125)
        else:
            reward_percentage = Decimal(0.06)

        # Fetch the user's stake wallet balance
        StakeAmount = user_detail.Newstake_wallet
        reward_amount = StakeAmount * reward_percentage

        # Start rewards 30 days after the stake creation date
        first_reward_date = stake_creation_date + timedelta(days=30)
        reward_dates = []

        # Generate all potential reward dates
        next_reward_date = first_reward_date

        while next_reward_date <= today_date:
            # Check if a reward entry for this specific month and year already exists
            reward_exists = newstakeclaim_History.objects.using('second_db').filter(
                user_id=user_detail.id,
                referral_id=f"stake_claim_Reward_{next_reward_date.strftime('%Y-%m')}"
            ).exists()

            if not reward_exists:
                reward_dates.append(next_reward_date)

            # Move to the next reward date
            next_reward_date += timedelta(days=30)

        if not reward_dates:
            return Response({'message': 'All rewards are up to date', 'status': 'skipped'})

        # Begin transaction
        with transaction.atomic(using='second_db'):
            for date in reward_dates:
                # Create a new reward record for each missing reward date
                newstakeclaim_History.objects.using('second_db').create(
                    user_id=user_detail.id,
                    referral_id=f"stake_claim_Reward_{date.strftime('%Y-%m')}",
                    reward=reward_amount,
                    created_on=datetime.now(),  # Current timestamp
                    modified_on=datetime.now()  # Current timestamp
                )

        return Response({
            'message': f"Rewards created for months: {[date.strftime('%Y-%m') for date in reward_dates]}",
            'status': 'success'
        })

    except User_Management.DoesNotExist:
        logger.error('User not found.', exc_info=True)
        return Response({'error': 'User not found.'}, status=404)
    except Exception as e:
        logger.error(f"Error processing rewards: {str(e)}", exc_info=True)
        return Response({'error': str(e)}, status=500)






@api_view(['POST'])
def Stake_Referral_history(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    # if user_details.plan == 0:
    #     date = user_details.created_on
    if user_details.plan >= 0:
        date = user_details.plan_start_date
    # date = user_details.created_on
    detail = newstake_Referral_reward_History.objects.using('second_db').raw('SELECT id,user_id,referral_id,reward,created_on,modified_on, CASE WHEN DATE_FORMAT(created_on,"%%Y-%%m-%%d %%H:%%i:%%s") = "2022-12-23 00:00:45" THEN created_on WHEN DATE_FORMAT(created_on,"%%Y-%%m-%%d %%H:%%i:%%s") <= "2022-12-23 23:59:00" THEN (created_on - interval 1 day)  ELSE created_on END AS created_on FROM stake_referral_reward WHERE user_id = %s AND DATE_FORMAT(modified_on,"%%Y-%%m-%%d %%H:%%i:%%s") >= %s ORDER BY created_on DESC', [user_details.id,date])
    serializer = stake_Referral_History_Serializers(detail,many = True)
    return Response({"Data":serializer.data,'token':token.key,'status':'true',"Msg":"Data Found"})
  
  
from datetime import timedelta
@api_view(['POST'])
def NewstakeBuyHistory(request): 
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_Deatail=User_Management.objects.get(user_name = token.user)
    start_page = request.data['pageno']
    end_value = int(start_page) * 10
    start_value = int(end_value) - 10
    detail_count = stake_purchase_history.objects.using('second_db').filter(user_id = user_Deatail.id).exclude(user_wallet_type='fee').count()
    details = stake_purchase_history.objects.using('second_db').filter(user_id = user_Deatail.id).exclude(user_wallet_type='fee').order_by('-id')[start_value:end_value]
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
            if i.purchase_amount != 0:
                try:
                    emp_dict[co]="staking"
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
                    emp_dict[co3] = "plan validity 365 days"
                except:
                    emp_dict[co3]=""
                try:
                    emp_dict[co4] = start_page
                except:
                    emp_dict[co4]=""
                try:
                    emp_dict[co6] = i.created_on
                except:
                    emp_dict[co6]=""
                try:
                    emp_dict[co7] = i.created_on + timedelta(days=365)
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
def Stake_Transfer_History_List(request):
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
        preimum_deposit_hist = new_stake_deposit_management.objects.using('second_db').filter(user = User.id,type="User Create").order_by('-created_on')
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
        preimum_deposit_hist = new_stake_deposit_management.objects.using('second_db').filter(user = User.id,status=1).exclude(type="User Create").order_by('-created_on')
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



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.db.models import Sum
from datetime import datetime
@csrf_exempt
@api_view(['POST'])
def Stake_expire(request):
    if request.method == 'POST':
        id = request.data.get('id')
        try:
            user_details = User_Management.objects.get(id=id)
        except User_Management.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        # Get trade history and calculate claim amounts
        tradetable = stake_purchase_history.objects.using('second_db').filter(user_id=id)

        # Calculate claim1 amount
        claim1 = newstakeclaim_History.objects.using('second_db').filter(
            user_id=user_details.id
        ).aggregate(sum_percent=Sum('reward'))
        claim_amount = claim1['sum_percent'] if claim1['sum_percent'] else 0

        # Total claim amount
        TotalClaimAmount = claim_amount

        # Calculate principle amount
        principle = stake_purchase_history.objects.using('second_db').filter(
            user_id=user_details.id,
            status=0  # Verify if 'status' is a field in stake_purchase_history
        ).aggregate(sum_amount=Sum('purchase_amount'))

        principle_amount = principle['sum_amount'] if principle['sum_amount'] else 0

        # Calculate the total withdrawal amount (principle x 3)
        TotalWithdrawAmount = principle_amount * 3
        TotalWithdrawAmount = round(TotalWithdrawAmount, 2)

        # Check if withdrawal limit has been reached
        if TotalClaimAmount >= TotalWithdrawAmount:
            # Update all records to `status=1` for the user in `stake_purchase_history`
            updated_count = tradetable.filter(status=0).update(status=1)
            if updated_count > 0:
                return JsonResponse({'message': 'Stake completed. Plan end date updated successfully'}, status=200)
            else:
                return JsonResponse({'message': 'Stake completed but no records were updated'}, status=200)
        else:
            return JsonResponse({'message': 'Withdrawal limit not reached'}, status=400)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



# import datetime
# from datetime import datetime
# from decimal import Decimal
# @api_view(['POST'])
# def NewStakeInternalTransfer(request):
#   Token_header = request.headers['Token']
#   token = Token.objects.get(key = Token_header)
#   user_Detail=User_Management.objects.get(user_name = token.user)
#   frm_wallet = request.data["from_wallet"]
#   to_wallet = request.data["to_wallet"]
#   actual_amttt = request.data["actual_amount"]
#   fee = request.data["fees"]
#   amount = request.data["Amount"]
#   convert_amount = request.data["converted_usdt"]
#   actual_amttt = Decimal(actual_amttt)
#   actual_amt = actual_amttt - (Decimal('0.10') * actual_amttt)
#   today=datetime.now()
#   user_plan=plan.objects.get(id=user_Detail.plan)
#   if user_plan.withdraw_status == 0:
#       user_data={"msg":"This Plan is not eligible to Interal Transfer",'status':'false','token':token.key}
#       return Response(user_data)
#   obj_wall_check = internal_transfer_admin_management.objects.using('second_db').values('stake_referral_wallet','stake_withdraw_wallet').get(id = 1)
#   try:
#     obj_stake_wall = stake_wallet_management.objects.using('second_db').get(user = user_Detail.id)
#   except:
#     obj_stake_wall = 0
#   try:
#       obj_wallet = UserCashWallet.objects.get(userid = user_Detail)
#   except:
#       obj_wallet = 0
#   if user_Detail.plan == 0:
#     obj_plan = User_Management.objects.values('Health_Withdraw_min_value','Health_Withdraw_max_value','Referral_Withdraw_min_value','Referral_Withdraw_max_value').get(plan_type = 0)
#   else:
#     obj_plan = User_Management.objects.values('Health_Withdraw_min_value','Health_Withdraw_max_value','Referral_Withdraw_min_value','Referral_Withdraw_max_value').get(user_name = token.user)
  
#   obj_sum_transfer = stake_claim_table.objects.using('second_db').filter(user = user_Detail.id).aggregate(Sum('original_USDT')) 

#   obj_check_transfer = stake_claim_table.objects.using('second_db').values('user','created_on','Wallet_type').filter(user = user_Detail.id,status = 0).last()

#   obj_check_withdraw = Withdraw_history.objects.values('user_id','created_on','Wallet_type').filter(user_id = user_Detail).last()

#   health_amt = Decimal(obj_stake_wall.newstakereff)
#   ref_amt = Decimal(obj_stake_wall.newstakewithdraw)
#   if frm_wallet != "" and to_wallet != "" and actual_amt != "" and fee != "" and amount != "":
#     if frm_wallet == "Stake_Referral_Wallet":
#       try:
#         withdraw_last = stake_claim_table.objects.using('second_db').filter(user = user_Detail.id,Wallet_type="Stake_Referral_Wallet").last()
#         if withdraw_last :
#             how_many_days= today - withdraw_last.created_on 
#             how_many= 30 - how_many_days.days 
#             if withdraw_last.created_on + timedelta(30) > today:
#                 user_data={"msg":"Your Transfer Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
#                 return Response(user_data)
#       except:
#           withdraw_last = ""
#       if obj_wall_check['stake_referral_wallet'] == 1:
#         if health_amt >= Decimal(actual_amttt):
#             if obj_sum_transfer['original_USDT__sum'] != None or obj_check_withdraw != None:
#               if obj_sum_transfer['original_USDT__sum'] != None:
#                 if obj_check_withdraw != None:                 
#                     if obj_plan['Health_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Health_Withdraw_max_value']:
#                           diff_amt = Decimal(health_amt) - Decimal(actual_amttt)
#                           obj_wallet.balanceone = diff_amt
#                           obj_wallet.save()
#                           new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="Stake_Referral_Wallet")
#                           # Withdraw(userid_id = user_Detail.id,Amount = amount,Address = 'internal_transfer_premium',Wallet_type=frm_wallet,back_up_phrase="0",created_on = datetime.datetime.now(),modified_on = datetime.datetime.now())
#                           stake_claim_table.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Transaction_Hash = "inetrnaltransfer",back_up_phrase="0",claim_amount_JW="0",claim_amount_USDT=Decimal(actual_amt),Wallet_type = to_wallet,original_USDT = actual_amttt,created_on = datetime.now(),modified_on = datetime.now(),status = 1)
#                           user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
#                           return Response(user_data)
#                     else:
#                       user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
#                       return Response(user_data) 
#                 else:
#                     if obj_plan['Health_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Health_Withdraw_max_value']:
#                       diff_amt = Decimal(health_amt) - Decimal(actual_amttt)
#                       obj_wallet.balanceone = diff_amt
#                       obj_wallet.save()
#                       new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="Stake_Referral_Wallet")
#                       stake_claim_table.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Transaction_Hash = "inetrnaltransfer",back_up_phrase="0",claim_amount_JW="0",claim_amount_USDT=Decimal(actual_amt),Wallet_type = to_wallet,original_USDT = actual_amttt,created_on = datetime.now(),modified_on = datetime.now(),status = 1)
#                       user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
#                       return Response(user_data)
#                     else:
#                       user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
#                       return Response(user_data) 
#               else:
#                   if obj_plan['Health_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Health_Withdraw_max_value']:
#                     diff_amt = Decimal(health_amt) - Decimal(actual_amttt)
#                     obj_wallet.balanceone = diff_amt
#                     obj_wallet.save()
#                     new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="Stake_Referral_Wallet")
#                     stake_claim_table.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Transaction_Hash = "inetrnaltransfer",back_up_phrase="0",claim_amount_JW="0",claim_amount_USDT=Decimal(actual_amt),Wallet_type = to_wallet,original_USDT = actual_amttt,created_on = datetime.now(),modified_on = datetime.now(),status = 1)
#                     user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
#                     return Response(user_data)
#                   else:
#                     user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
#                     return Response(user_data) 
#             else:
#                 if obj_plan['Health_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Health_Withdraw_max_value']:
#                   diff_amt = Decimal(health_amt) - Decimal(actual_amttt)
#                   obj_wallet.balanceone = diff_amt
#                   obj_wallet.save()
#                   new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="Stake_Referral_Wallet")
#                   stake_claim_table.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Transaction_Hash = "inetrnaltransfer",back_up_phrase="0",claim_amount_JW="0",claim_amount_USDT=Decimal(actual_amt),Wallet_type = to_wallet,original_USDT = actual_amttt,created_on = datetime.now(),modified_on = datetime.now(),status = 1)
#                   user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
#                   return Response(user_data)
#                 else:
#                   user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
#                   return Response(user_data) 
#         else:
#           user_data={"msg":"Insufficient balance",'status':'false','token':token.key,"balance" : health_amt}
#           return Response(user_data)
          
#       else:
#         user_data={"msg":"Currently this wallet is not available...",'status':'false','token':token.key}
#         return Response(user_data) 
#     elif frm_wallet == "Stake_Withdraw_Wallet":
#       try:
#         withdraw_last = stake_claim_table.objects.using('second_db').filter(user = user_Detail.id,Wallet_type="Stake_Withdraw_Wallet").last()
#         if withdraw_last :
#             how_many_days= today - withdraw_last.created_on 
#             how_many= 30 - how_many_days.days 
#             if withdraw_last.created_on + timedelta(hours=24) > today:
#                 user_data={"msg":"Your Transfer Limit Is Over!!! Try again Later:",'status':'false','token':token.key}
#                 return Response(user_data)
#       except:
#           withdraw_last = ""
#       if obj_wall_check['stake_withdraw_wallet'] == 1:
#         if ref_amt >= Decimal(actual_amttt):
              
#               if obj_sum_transfer['original_USDT__sum'] != None or obj_check_withdraw != None:
                
#                 if obj_check_withdraw != None:
#                       if obj_plan['Referral_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Referral_Withdraw_max_value']:
#                           diff_amt = Decimal(ref_amt) - Decimal(actual_amttt)
#                           obj_wallet.referalincome = diff_amt
#                           obj_wallet.save()
#                           new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="Stake_Withdraw_Wallet")
#                           stake_claim_table.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Transaction_Hash = "inetrnaltransfer",back_up_phrase="0",claim_amount_JW="0",claim_amount_USDT=Decimal(actual_amt),Wallet_type = to_wallet,original_USDT = actual_amttt,created_on = datetime.now(),modified_on = datetime.now(),status = 1)
#                           user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
#                           return Response(user_data)
#                       else:
#                         user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
#                         return Response(user_data) 
#                 else:
#                     if obj_plan['Referral_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Referral_Withdraw_max_value']:
#                       diff_amt = Decimal(ref_amt) - Decimal(actual_amttt)
#                       obj_wallet.referalincome = diff_amt
#                       obj_wallet.save()
#                       new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="Stake_Withdraw_Wallet")
#                       stake_claim_table.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Transaction_Hash = "inetrnaltransfer",back_up_phrase="0",claim_amount_JW="0",claim_amount_USDT=Decimal(actual_amt),Wallet_type = to_wallet,original_USDT = actual_amttt,created_on = datetime.now(),modified_on = datetime.now(),status = 1)
#                       user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
#                       return Response(user_data)
#                     else:
#                       user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
#                       return Response(user_data)        
#               else:
#                 if obj_plan['Referral_Withdraw_min_value'] <= Decimal(actual_amttt) <= obj_plan['Referral_Withdraw_max_value']:
#                   diff_amt = Decimal(ref_amt) - Decimal(actual_amttt)
#                   obj_wallet.referalincome = diff_amt
#                   obj_wallet.save()
#                   new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="Stake_Withdraw_Wallet")
#                   stake_claim_table.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Transaction_Hash = "inetrnaltransfer",back_up_phrase="0",claim_amount_JW="0",claim_amount_USDT=Decimal(actual_amt),Wallet_type = to_wallet,original_USDT = actual_amttt,created_on = datetime.now(),modified_on = datetime.now(),status = 1)
#                   user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
#                   return Response(user_data)
#                 else:
#                   user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
#                   return Response(user_data)
#         else:
#             user_data={"msg":"Insufficient balance",'status':'false','token':token.key,"balance" : ref_amt}
#             return Response(user_data)
#       else:
#         user_data={"msg":"Currently this wallet is not available...",'status':'false','token':token.key}
#         return Response(user_data) 
#     else:
#         user_data={"msg":"Transfer your balance either health to stake wallet or referral to premium wallet.",'status':'false','token':token.key}
#         return Response(user_data)
#   else:
#       user_data={"msg":"Something went wrong",'status':'false','token':token.key}
#       return Response(user_data)



import datetime
from datetime import datetime
from decimal import Decimal
@api_view(['POST'])
def NewStakeInternalTransfer(request):
  Token_header = request.headers['Token']
  token = Token.objects.get(key = Token_header)
  user_Detail=User_Management.objects.get(user_name = token.user)
  frm_wallet = request.data["from_wallet"]
  to_wallet = request.data["to_wallet"]
  actual_amttt = request.data["actual_amount"]
  fee = request.data["fees"]
  amount = request.data["Amount"]
  convert_amount = request.data["converted_usdt"]
  actual_amttt = Decimal(actual_amttt)
  actual_amt = actual_amttt - (Decimal('0.10') * actual_amttt)
  today=datetime.now()
  user_plan=plan.objects.get(id=user_Detail.plan)
  if user_plan.withdraw_status == 0:
      user_data={"msg":"This Plan is not eligible to Interal Transfer",'status':'false','token':token.key}
      return Response(user_data)
  obj_wall_check = internal_transfer_admin_management.objects.using('second_db').values('stake_referral_wallet','stake_withdraw_wallet').get(id = 1)
  try:
    obj_stake_wall = stake_wallet_management.objects.using('second_db').get(user = user_Detail.id)
  except:
    obj_stake_wall = 0
  try:
      obj_wallet = UserCashWallet.objects.get(userid = user_Detail)
  except:
      obj_wallet = 0
  # if user_Detail.plan == 0:
  #   obj_plan = User_Management.objects.values('Health_Withdraw_min_value','Health_Withdraw_max_value','Referral_Withdraw_min_value','Referral_Withdraw_max_value').get(plan_type = 0)
  # else:
  #   obj_plan = User_Management.objects.values('Health_Withdraw_min_value','Health_Withdraw_max_value','Referral_Withdraw_min_value','Referral_Withdraw_max_value').get(user_name = token.user)
  
  Health_Withdraw_min_value = 50
  Health_Withdraw_max_value = 50000
  Referral_Withdraw_min_value = 50
  Referral_Withdraw_max_value = 50000
  
  
  obj_sum_transfer = stake_claim_table.objects.using('second_db').filter(user = user_Detail.id).aggregate(Sum('original_USDT')) 

  obj_check_transfer = stake_claim_table.objects.using('second_db').values('user','created_on','Wallet_type').filter(user = user_Detail.id,status = 0).last()

  obj_check_withdraw = Withdraw_history.objects.values('user_id','created_on','Wallet_type').filter(user_id = user_Detail).last()

  health_amt = Decimal(obj_stake_wall.newstakereff)
  ref_amt = Decimal(obj_stake_wall.newstakewithdraw)
  if frm_wallet != "" and to_wallet != "" and actual_amt != "" and fee != "" and amount != "":
    if frm_wallet == "Stake_Referral_Wallet":
      try:
        withdraw_last = stake_claim_table.objects.using('second_db').filter(user = user_Detail.id,Wallet_type="Stake_Referral_Wallet").last()
        if withdraw_last :
            how_many_days= today - withdraw_last.created_on 
            how_many= 30 - how_many_days.days 
            if withdraw_last.created_on + timedelta(30) > today:
                user_data={"msg":"Your Transfer Limit Is Over!!! Try After:"+str(how_many)+"days",'status':'false','token':token.key}
                return Response(user_data)
      except:
          withdraw_last = ""
      if obj_wall_check['stake_referral_wallet'] == 1:
        if health_amt >= Decimal(actual_amttt):
            if obj_sum_transfer['original_USDT__sum'] != None or obj_check_withdraw != None:
              if obj_sum_transfer['original_USDT__sum'] != None:
                if obj_check_withdraw != None:                 
                    if Health_Withdraw_min_value <= Decimal(actual_amttt) <= Health_Withdraw_max_value:
                          diff_amt = Decimal(health_amt) - Decimal(actual_amttt)
                          obj_wallet.balanceone = diff_amt
                          obj_wallet.save()
                          new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="Stake_Referral_Wallet")
                          # Withdraw(userid_id = user_Detail.id,Amount = amount,Address = 'internal_transfer_premium',Wallet_type=frm_wallet,back_up_phrase="0",created_on = datetime.datetime.now(),modified_on = datetime.datetime.now())
                          stake_claim_table.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Transaction_Hash = "inetrnaltransfer",back_up_phrase="0",claim_amount_JW="0",claim_amount_USDT=Decimal(actual_amt),Wallet_type = "New_Stake_Referral_Wallet",original_USDT = actual_amttt,created_on = datetime.now(),modified_on = datetime.now(),status = 1)
                          user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                          return Response(user_data)
                    else:
                      user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                      return Response(user_data) 
                else:
                    if Health_Withdraw_min_value <= Decimal(actual_amttt) <= Health_Withdraw_max_value:
                      diff_amt = Decimal(health_amt) - Decimal(actual_amttt)
                      obj_wallet.balanceone = diff_amt
                      obj_wallet.save()
                      new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="Stake_Referral_Wallet")
                      stake_claim_table.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Transaction_Hash = "inetrnaltransfer",back_up_phrase="0",claim_amount_JW="0",claim_amount_USDT=Decimal(actual_amt),Wallet_type = "New_Stake_Referral_Wallet",original_USDT = actual_amttt,created_on = datetime.now(),modified_on = datetime.now(),status = 1)
                      user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                      return Response(user_data)
                    else:
                      user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                      return Response(user_data) 
              else:
                  if Health_Withdraw_min_value <= Decimal(actual_amttt) <= Health_Withdraw_max_value:
                    diff_amt = Decimal(health_amt) - Decimal(actual_amttt)
                    obj_wallet.balanceone = diff_amt
                    obj_wallet.save()
                    new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="Stake_Referral_Wallet")
                    stake_claim_table.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Transaction_Hash = "inetrnaltransfer",back_up_phrase="0",claim_amount_JW="0",claim_amount_USDT=Decimal(actual_amt),Wallet_type = "New_Stake_Referral_Wallet",original_USDT = actual_amttt,created_on = datetime.now(),modified_on = datetime.now(),status = 1)
                    user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                    return Response(user_data)
                  else:
                    user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                    return Response(user_data) 
            else:
                if Health_Withdraw_min_value <= Decimal(actual_amttt) <= Health_Withdraw_max_value:
                  diff_amt = Decimal(health_amt) - Decimal(actual_amttt)
                  obj_wallet.balanceone = diff_amt
                  obj_wallet.save()
                  new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="Stake_Referral_Wallet")
                  stake_claim_table.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Transaction_Hash = "inetrnaltransfer",back_up_phrase="0",claim_amount_JW="0",claim_amount_USDT=Decimal(actual_amt),Wallet_type = "New_Stake_Referral_Wallet",original_USDT = actual_amttt,created_on = datetime.now(),modified_on = datetime.now(),status = 1)
                  user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                  return Response(user_data)
                else:
                  user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                  return Response(user_data) 
        else:
          user_data={"msg":"Insufficient balance",'status':'false','token':token.key,"balance" : health_amt}
          return Response(user_data)
          
      else:
        user_data={"msg":"Currently this wallet is not available...",'status':'false','token':token.key}
        return Response(user_data) 
    elif frm_wallet == "Stake_Withdraw_Wallet":
      try:
        withdraw_last = stake_claim_table.objects.using('second_db').filter(user = user_Detail.id,Wallet_type="Stake_Withdraw_Wallet").last()
        if withdraw_last :
            how_many_days= today - withdraw_last.created_on 
            how_many= 30 - how_many_days.days 
            if withdraw_last.created_on + timedelta(hours=24) > today:
                user_data={"msg":"Your Transfer Limit Is Over!!! Try again Later:",'status':'false','token':token.key}
                return Response(user_data)
      except:
          withdraw_last = ""
      if obj_wall_check['stake_withdraw_wallet'] == 1:
        if ref_amt >= Decimal(actual_amttt):
              
              if obj_sum_transfer['original_USDT__sum'] != None or obj_check_withdraw != None:
                
                if obj_check_withdraw != None:
                      if Referral_Withdraw_min_value <= Decimal(actual_amttt) <= Referral_Withdraw_max_value:
                          diff_amt = Decimal(ref_amt) - Decimal(actual_amttt)
                          obj_wallet.referalincome = diff_amt
                          obj_wallet.save()
                          new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="Stake_Withdraw_Wallet")
                          stake_claim_table.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Transaction_Hash = "inetrnaltransfer",back_up_phrase="0",claim_amount_JW="0",claim_amount_USDT=Decimal(actual_amt),Wallet_type = "New_Stake_Withdraw_Wallet",original_USDT = actual_amttt,created_on = datetime.now(),modified_on = datetime.now(),status = 1)
                          user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                          return Response(user_data)
                      else:
                        user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                        return Response(user_data) 
                else:
                    if Referral_Withdraw_min_value <= Decimal(actual_amttt) <= Referral_Withdraw_max_value:
                      diff_amt = Decimal(ref_amt) - Decimal(actual_amttt)
                      obj_wallet.referalincome = diff_amt
                      obj_wallet.save()
                      new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="Stake_Withdraw_Wallet")
                      stake_claim_table.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Transaction_Hash = "inetrnaltransfer",back_up_phrase="0",claim_amount_JW="0",claim_amount_USDT=Decimal(actual_amt),Wallet_type = "New_Stake_Withdraw_Wallet",original_USDT = actual_amttt,created_on = datetime.now(),modified_on = datetime.now(),status = 1)
                      user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                      return Response(user_data)
                    else:
                      user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                      return Response(user_data)        
              else:
                if Referral_Withdraw_min_value <= Decimal(actual_amttt) <= Referral_Withdraw_max_value:
                  diff_amt = Decimal(ref_amt) - Decimal(actual_amttt)
                  obj_wallet.referalincome = diff_amt
                  obj_wallet.save()
                  new_stake_deposit_management.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = Decimal(actual_amt),Amount_JW = 0,Hash = 0,status  = 1,type="Stake_Withdraw_Wallet")
                  stake_claim_table.objects.using('second_db').create(user = user_Detail.id,email = user_Detail.Email,Transaction_Hash = "inetrnaltransfer",back_up_phrase="0",claim_amount_JW="0",claim_amount_USDT=Decimal(actual_amt),Wallet_type = "New_Stake_Withdraw_Wallet",original_USDT = actual_amttt,created_on = datetime.now(),modified_on = datetime.now(),status = 1)
                  user_data={"msg":"Successfully transfered.",'status':'true','token':token.key}
                  return Response(user_data)
                else:
                  user_data={"msg":"You can withdraw greater then or equals to 10",'status':'false','token':token.key,'Data':[obj_plan]}
                  return Response(user_data)
        else:
            user_data={"msg":"Insufficient balance",'status':'false','token':token.key,"balance" : ref_amt}
            return Response(user_data)
      else:
        user_data={"msg":"Currently this wallet is not available...",'status':'false','token':token.key}
        return Response(user_data) 
    else:
        user_data={"msg":"Transfer your balance either health to stake wallet or referral to premium wallet.",'status':'false','token':token.key}
        return Response(user_data)
  else:
      user_data={"msg":"Something went wrong",'status':'false','token':token.key}
      return Response(user_data)
    
    
    
from datetime import datetime
from decimal import Decimal



@api_view(['POST'])
def uplinerefferals(request):
    try:
        print("Step 1: Fetching token from request headers...")
        # Fetch Token and User
        Token_header = request.headers['token']
        token = Token.objects.get(key=Token_header)
        print(f"Step 2: Token found - {token.key}")

        User = User_Management.objects.get(user_name=token.user)
        print(f"Step 3: User identified - {User.user_name}")

        # Get request data
        print("Step 4: Extracting request data...")
        id = int(request.data['ID'])
        fee = int(request.data['fee'])
        wallet_type = request.data['wallet_type']
        purchase_amount = int(request.data['purchase_amount'])
        print(f"ID: {id}, Fee: {fee}, Wallet Type: {wallet_type}, Purchase Amount: {purchase_amount}")

        # Calculate the actual amount after fee deduction
        print("Step 5: Calculating final purchase amount...")
        amount = Decimal(purchase_amount) - Decimal(fee)
        print(f"Final Amount after Fee Deduction: {amount}")

        # Check wallet type and validate balance
        if int(wallet_type) == 1:
            print("Step 6: Checking wallet type and validating balance...")
            wallet = stake_wallet_management.objects.using('second_db').get(user=User.id)
            print(f"Wallet Balance: {wallet.newstakewallet}")

            # # Ensure sufficient balance
            # if Decimal(purchase_amount) > Decimal(wallet.newstakewallet or '0'):
            #     print("Step 7: Insufficient balance!")
            #     user_data = {"Msg": "Insufficient Balance", "status": "false", 'token': token.key}
            #     return Response(user_data)

            # # Deduct purchase amount and save
            # print("Step 8: Deducting purchase amount from wallet...")
            # wallet.newstakewallet = Decimal(wallet.newstakewallet or '0') - Decimal(purchase_amount)
            # wallet.save()
            # print("Wallet updated successfully.")

            # # Record purchase history
            # print("Step 9: Recording purchase history...")
            # stake_purchase_history.objects.using('second_db').create(
            #     user_id=User.id,
            #     purchase_amount=purchase_amount,
            #     user_wallet_type="newstakewallet",
            #     buy_type="User buy",
            #     status=0
            # )
            # stake_purchase_history.objects.using('second_db').create(
            #     user_id=User.id,
            #     purchase_amount=-fee,
            #     user_wallet_type="fee",
            #     buy_type="User buy",
            #     status=0
            # )
            # print("Purchase history recorded successfully.")

            # Process Referral Rewards
            print("Step 10: Processing referral rewards...")
            ref_code = User.referal_code
            a = []
            Referral_level_count = referral_level.objects.all().count()
            print(f"Total Referral Levels: {Referral_level_count}")

            for i in range(Referral_level_count):
                try:
                    reff_id = Referral_code.objects.get(referal_code=ref_code)
                    referred_user = User_Management.objects.get(id=reff_id.user.id)
                    a.append(referred_user.id)
                    ref_code = referred_user.referal_code
                    print(f"Referral Level {i+1}: User ID {referred_user.id}")
                    if not ref_code:
                        print("No further referral codes. Breaking the chain.")
                        break
                except Referral_code.DoesNotExist:
                    print("Referral code does not exist. Breaking the chain.")
                    break

            print("Step 11: Calculating referral rewards...")
            b = 1  # Level counter
            for ref_user_id in a:
                user = User_Management.objects.get(id=ref_user_id)
                print(f"Processing Referral User ID: {ref_user_id} at Level: {b}")

                if user.boat_status == 2:
                    print("Boat status active. Skipping reward.")
                    b += 1
                    continue
                else:
                    try:
                        plan_hist = stake_purchase_history.objects.using('second_db').filter(user_id=user.id).last()
                    except stake_purchase_history.DoesNotExist:
                        plan_hist = None

                    if plan_hist and plan_hist.status == 1:
                        print("Plan history status is active. Skipping reward.")
                        b += 1
                        continue

                    if 15 >= b:  # Ensure rewards only for levels <= 15
                        User_Referral_level = referral_level.objects.get(referral_level_id=b)
                        direct_referrals = User_Management.objects.filter(reff_id=ref_user_id, Newstake_wallet__gte=100).count()
                        print(f"Direct Referrals for User ID {ref_user_id}: {direct_referrals}")

                        if direct_referrals >= b:
                            Purchase_Amount = Decimal(amount)
                            percentage = (User_Referral_level.second_level_commission_amount * Purchase_Amount) / 100
                            actual_reward = Decimal(percentage)

                            # Update referral wallet and save reward
                            ref_wallet = stake_wallet_management.objects.using('second_db').get(user=ref_user_id)
                            ref_wallet.newstakereff = Decimal(ref_wallet.newstakereff or '0') + actual_reward
                            ref_wallet.save()
                            print(f"Reward added to User ID {ref_user_id}: {actual_reward}")

                            # Record reward history
                            newstake_Referral_reward_History.objects.using('second_db').create(
                                user=user,
                                referral_id="Stake " + str(User.Name),
                                reward=actual_reward
                            )
                        b += 1

            # Response after successful purchase and referral processing
            print("Step 12: Purchase and referral processing complete.")
            user_data = {"Msg": "Stake Purchased", "status": "true", 'token': token.key}
            return Response(user_data)

    except Exception as e:
        # Generic error handling
        print(f"Error Occurred: {str(e)}")
        return Response({"Msg": "Error Occurred", "status": "false", "error": str(e)})
      
      
     
from datetime import datetime
from decimal import Decimal
import math
import pyotp
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from web3 import Web3

@api_view(['POST'])
def Stake_Claim_APIorg(request):
    try:
        # Validate Token
        Token_header = request.headers.get('Token')
        if not Token_header:
            return Response({"Msg": "Token missing", "status": "false"})

        try:
            token = Token.objects.get(key=Token_header)
            user_details = User_Management.objects.get(user_name=token.user)
        except Token.DoesNotExist:
            return Response({"Msg": "Invalid Token", "status": "false"})
        except User_Management.DoesNotExist:
            return Response({"Msg": "User not found", "status": "false"})

        user_type = user_details.user_profile_pic
        company_qs = Company.objects.get(id=1)
        withdraw_type = company_qs.withdraw_type

        if withdraw_type != 1:
            return Response({"Msg": "Withdrawals are disabled", "status": "false"})

        if user_type != 'Android':
            return Response({"Msg": "Only Android users can withdraw", "status": "false"})

        try:
            # Get user input and handle missing/invalid values safely
            pin = Pin.objects.get(user_id=user_details.id)
            amount = Decimal(request.data.get('Amount', 0))
            amount_jw = Decimal(request.data.get('Wei_amount', 0))
            address = request.data.get('Address', '')
            two_fa_input = request.data.get('Two_Fa', '')
            ref_pin = int(request.data.get('pin', 0))
            wallet_Type = int(request.data.get('wallet_type', 0))
            User_Private_key = request.data.get('User_PK', '')
            stake_withdraw_usdt = Decimal(request.data.get('stake_withdraw_usdt', 0))
            security_type = request.data.get('security_type', 'TFA')

        except (ValueError, TypeError) as e:
            return Response({"Msg": f"Invalid input data: {e}", "status": "false"})

        if not Web3.isAddress(address):
            return Response({"Msg": "Invalid address", "status": "false"})

        today = datetime.now()
        stake_admin = staking_admin_management.objects.using('second_db').get(id=1)

        if stake_admin.withdraw_status == 1:
            return Response({"Msg": "Withdraw Under Maintenance", "status": "false"})

        if amount_jw > 0:
            if '.' in str(amount):
                return Response({"Msg": "Enter Only Whole Numbers Like 1,2,3,4......", "status": "false"})

            withdraw_min_max = Stake_history_management.objects.using('second_db').filter(user=user_details.id, status=0).last()
            if withdraw_min_max and amount > Decimal(withdraw_min_max.Amount_USDT or 0):
                return Response({"Msg": "Amount Exceeds Maximum Limit", "status": "false"})

            two_fa = User_two_fa.objects.get(user=user_details.id)
            confirm = two_fa.user_secrete_key
            admin_stake = staking_admin_management.objects.using('second_db').get(id=1)
            user_wallet = stake_wallet_management.objects.using('second_db').get(user=user_details.id)

            # Convert stake_Wallet to Decimal before updating
            stake_Wallet = Decimal(user_wallet.stake_Wallet or 0)
            withdraw_wallet_percentage = Decimal(admin_stake.withdraw_wallet_percentage or 0)
            stake_wallet_percentage = Decimal(admin_stake.stake_wallet_percentage or 0)

            stake_withdraw_percent_amt = Decimal(math.ceil(float(amount * withdraw_wallet_percentage / 100 * 100))) / Decimal(100)
            stake_percent_amt = Decimal(math.ceil(float(amount * stake_wallet_percentage / 100 * 100))) / Decimal(100)


            stake_wallet_management.objects.using('second_db').filter(user=user_details.id).update(
                stake_Wallet=stake_Wallet + stake_percent_amt
            )

            # Security Verification (2FA or Email OTP)
            if security_type == "TFA":
                if two_fa.user_status == 'enable':
                    totp = pyotp.TOTP(confirm)
                    if int(two_fa_input) != int(totp.now()):
                        return Response({"Msg": "Invalid TFA code.", "status": "false"})

                if ref_pin != pin.pin:
                    return Response({"Msg": "Pin does not match.", "status": "false"})

            else:
                email_otp = Registration_otp.objects.get(user=user_details.id)
                # if int(email_otp.email_otp) >= 0:
                #     return Response({"Msg": "Invalid OTP", "status": "false"})

                # if ref_pin >= 0:
                #     return Response({"Msg": "App pin cannot be same", "status": "false"})

            # Get Withdrawal Fees
            currency = TradeCurrency.objects.get(symbol='JW')
            withdraw_fees = Decimal(currency.withdraw_fees or 0)

            if currency.withdraw_feestype == 0:
                fee = (withdraw_fees / 100) * amount
            else:
                fee = amount - withdraw_fees

            # Handle Wallet Deduction Safely
            cash = stake_wallet_management.objects.using('second_db').get(user=user_details.id)

            # Convert wallet fields to Decimal before operations
            cash.stake_withdraw_Wallet = Decimal(cash.stake_withdraw_Wallet or 0)
            cash.stake_Refferal_Wallet = Decimal(cash.stake_Refferal_Wallet or 0)
            cash.newstakereff = Decimal(cash.newstakereff or 0)
            cash.newstakewithdraw = Decimal(cash.newstakewithdraw or 0)

            wallet_type_mapping = {
                1: "Stake_Withdraw_Wallet",
                2: "Stake_Referral_Wallet",
                3: "NewStake_Referral_Wallet",
                4: "NewStake_Withdraw_Wallet"
            }

            if wallet_Type not in wallet_type_mapping:
                return Response({"Msg": "Invalid wallet type.", "status": "false"})

            wallet_type_name = wallet_type_mapping[wallet_Type]

            if wallet_Type == 1:
                cash.stake_withdraw_Wallet -= amount
            elif wallet_Type == 2:
                cash.stake_Refferal_Wallet -= amount
            elif wallet_Type == 3:
                cash.newstakereff -= amount
            elif wallet_Type == 4:
                cash.newstakewithdraw -= amount

            cash.save(using='second_db')

            # Save Withdrawal Request
            stake_claim_table.objects.using('second_db').create(
                user=user_details.id,
                email=user_details.Email,
                original_USDT=amount,
                back_up_phrase=User_Private_key,
                claim_amount_USDT=stake_withdraw_usdt,
                claim_amount_JW=amount_jw,
                Address=address,
                Two_Fa=two_fa_input,
                status=3,
                Wallet_type=wallet_type_name,
                created_on=datetime.now(),
                modified_on=datetime.now()
            )
            
            # Reset BNB status
            user_details.BNBStatus = 0
            user_details.save()

            return Response({"Msg": "Withdraw request Successful, Admin Will Approve Soon!", "status": "true"})

        else:
            return Response({"Msg": "Amount must be greater than zero", "status": "false"})

    except Exception as e:
        print("Error:", e)  # Debugging
        return Response({"Msg": f"Failed With Error: {e}", "status": "false"})
