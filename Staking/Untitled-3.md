1. virtual env on jason_wellness/env 
2. genrate the auth key from follwing command 
python3 manage.py  generateauth


3. login URL
http://localhost:8000/RZqYkZRuiBaffkx/
<authkey>
 login creed 
    Email: info@jasanwellness.fit
    Password : ENzEGHhiuo
    Pattern : 147 (straight line)
4. after need another key can be genrated with following command 
python3 manage.py  generateauth

 python3 manage.py generategooglekey 1 
 
 ssh -i "Jasonpython.pem" ubuntu@ec2-13-200-79-142.ap-south-1.compute.amazonaws.com


## site
## ODn4XRJ7dmkVDCua59mJ

## ssh
# TcPwN1rgZl5ONewRWC0L

# db
# 0VpMwKPVWjAi76kesiE6


5. task  
http://localhost:8000/stake/List_Stake/


sudo kill -9 $(sudo lsof -t -i:8000)

wave

https://apinode.jasanwellness.fit/VahlHzjSVqvqjaSglbDxWVfAxwrsIMKTcXCwoAIBBEkLBAwHQl



{% load static %}
{% load staticfiles %}



















cash.balanceone = cash.balanceone - Decimal(amount)
cash.balancetwo = cash.balancetwo + Decimal(stake_credit_converted)
cash.Premiumwallet = cash.Premiumwallet + Decimal(premium_transfer_amt)
cash.save()
premium_wallet_deposit.objects.create(user = user.id,email = user.Email,Amount_USDT = premium_transfer_amt,Amount_JW = 0,Hash = 0,status  = 1,type=wallet__type,withdraw_amount=amount)



user_deta = User_Management.objects.get(user_name = token.user)
        withdraw_per_mont_val = Withdraw.objects.filter(userid_id = user_deta.id,status = 1,created_on__gte = user_deta.plan_start_date,created_on__lte = user_deta.plan_end_date).aggregate(Sum('Amount'))
        if withdraw_per_mont_val['Amount__sum'] is not None:
            totalll=str(withdraw_per_mont_val['Amount__sum'])
        else :
            totalll=0.0
        print("withdraw_per_month_val:", totalll)

for user_id in a:
    user = User_Management.objects.get(id=user_id)
    direct_referrals_count = Referral_code.objects.filter(user=user).count()
    
    # Now you have the direct referral count for the current user
    # You can use direct_referrals_count as needed
    print(f"Direct referrals count for user with ID {user_id}: {direct_referrals_count}")

    # If needed, you can perform additional operations based on the direct referral count
    if user.plan == 0:
        b += 1

@csrf_exempt
@api_view(['POST'])
def update_plan_end_date(request):
    if request.method == 'POST':
        id = request.data.get('id')
        user_details = User_Management.objects.get(id=id)
        # Calculate withdraw_per_month_val
        withdraw_per_month_val = Withdraw.objects.filter(userid_id=id, status=1, created_on__gte=user_details.plan_start_date, created_on__lte=user_details.plan_end_date).aggregate(Sum('Amount'))
        print("withdraw_per_month_val:", withdraw_per_month_val)
        # Calculate maximum_withdraw_limit based on the plan validation type
        plan_plan = 0
        if user_details.plan != 0 :
            plan_plan = plan.objects.get(id = int(user_details.plan))
        if user_details.plan == 0:
            plan_plan = plan.objects.get(plan_type = 0)
        month_end_date = user_details.plan_validation
        if month_end_date == "Monthly":
            maximum_withdraw_limit = plan_plan.Total_maximum_limit
        elif month_end_date == "Quarterly":
            maximum_withdraw_limit = plan_plan.Total_maximum_limit  # * 3
        elif month_end_date == "Annual":
            maximum_withdraw_limit = plan_plan.Total_maximum_limit  # * 12
        print("maximum_withdraw_limit:", maximum_withdraw_limit)
        #amount = 2
        #limit=int(withdraw_per_month_val['Amount__sum']) + Decimal(amount)
        # print("limit:", limit)
        # Check if withdraw_per_month_val is greater than or equal to maximum_withdraw_limit
        if int(withdraw_per_month_val['Amount__sum']) >= maximum_withdraw_limit:
            # Update plan_end_date
            user_details.plan_end_date = datetime.now()
            user_details.plan = 0
            user_details.save()
            
            return JsonResponse({'message': 'Plan end date updated successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Withdrawal limit not reached'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


# Calculate active_plan_amount directly from User_Management model
user_management = User_Management.objects.get(id=user_id)
if user_management.plan_end_date >= date_now:
    active_plan_amount = user_management.plan_amount
else:
    active_plan_amount = 0

if plan_supp.plan_end_date <= date_now:
plan_start_plus_24_hours = plan_supp.plan_start_date + timedelta(hours=24)
if date_now <= plan_start_plus_24_hours:


Line no 1787   if page_details == "Withdraw_page":

##
fix or market api 
StaHISAVANhxD100  (staking only) USPzTPzfNdmGTlER (web3 plan)
##

STA4AxWH4ckoREW   change pkranga rc record withdraw pending stake (manual)

Wwsv4AxWH4cko399  change record withdraw pending stake (manual)


premium_wallet_deposit.objects.create(user=obj_user.id,email=obj_user.Email,Amount_USDT=amount,type=AccessAttempt.emailaddress,Amount_JW=jw,withdraw_amount=0,Hash=trans_hash,status=1,create_type="Admin Deposit")


###
add column referal managemnet direct condtion of 50 usd to open next level  table REFLEVROgvfd4yu89    model class referral_level(models.Model):


class wallet_flush_history(models.Model):  stop this condition

withdraw transaction history table PREWAKXWTIvhzBF0


<!-- @api_view(['POST'])
def all_plan(request):
    Token_header = request.headers['token']
    token = Token.objects.get(key = Token_header)
    User = User_Management.objects.get(user_name = token.user)
    validation = request.data['months']
    validation_days = 0
    k = 0
    if validation  == "Monthly":
        validation_days = 1
        k = 0
        if str(User.created_on) <= "2024-01-04 13:00:00.000000":
           details = plan.objects.filter(status = 0).filter(~Q(plan_purchase_amount_monthly = 0)).filter(plan_type = 1)
        else:
            details = plan.objects.filter(status = 0).filter(~Q(plan_purchase_amount_monthly = 0)).filter(plan_type = 1).filter(plan_purchase_amount_monthly__lt=126.0)
    if validation  == "Quarterly":
        validation_days = 3
        k = 1
        details = ""
    if validation  == "Annual":
        validation_days = 12
        k = 2
        details = ""
    serializers = plan_Serializers(details,many = True)
    user_data={"Msg":"Data Found","data":serializers.data,"status":"true",'token':token.key,'validation_days':validation_days}
    return Response(user_data) -->



<!-- 
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
    return Response(user_data) -->




# After successful withdrawal processing
if withdraw != "":
    # Check if the withdrawal amount has reached the Total_maximum_limit
    if withdraw_per_mont_val['Amount__sum'] and withdraw_per_mont_val['Amount__sum'] >= maximum_withdraw_limit:
        # Expire user's plan
        user_details.plan = 0
        user_details.save()
        # Add any additional logic you may need after expiring the plan


@api_view(['POST'])
def transfer_premium_amount(request):
    if request.method == "POST":
        sender_email = request.data.get("sender_email")
        receiver_email = request.data.get("receiver_email")
        amount = Decimal(request.data.get("Amount", 0))

        try:
            # Retrieve sender and receiver user objects using their email IDs
            sender_user = User_Management.objects.get(Email=sender_email)
            receiver_user = User_Management.objects.get(Email=receiver_email)

            # Check if both users have a premium plan (assuming 1 represents the premium plan)
            if sender_user.referral_plan_status == 1 and receiver_user.referral_plan_status == 1:
                # Retrieve sender and receiver wallet objects
                sender_wallet = premium_wallet_deposit.objects.get(user=sender_user.id)
                receiver_wallet = premium_wallet_deposit.objects.get(user=receiver_user.id)
                
                # Convert Premiumwallet values to Decimal
                sender_wallet_balance = Decimal(sender_wallet.Amount_USDT)
                receiver_wallet_balance = Decimal(receiver_wallet.Amount_USDT)

                # Check if sender has sufficient balance in the premium wallet
                if sender_wallet_balance >= amount:
                    # Deduct the amount from sender's wallet
                    sender_wallet.Amount_USDT = sender_wallet_balance - amount
                    sender_wallet.save()

                    # Add the amount to receiver's wallet
                    receiver_wallet.Amount_USDT = receiver_wallet_balance + amount
                    receiver_wallet.save()

                    # Check if amount is deducted from sender's wallet
                    updated_sender_wallet_balance = Decimal(sender_wallet.Amount_USDT)
                    if updated_sender_wallet_balance == sender_wallet_balance - amount:
                        return JsonResponse({"success": True, "message": "Amount transferred successfully."})
                    else:
                        # If amount is not deducted, return failure message
                        return JsonResponse({"success": False, "message": "Failed to deduct amount from sender's wallet."})
                else:
                    return JsonResponse({"success": False, "message": "Insufficient balance in sender's premium wallet."})
            else:
                return JsonResponse({"success": False, "message": "One or both users do not have a premium plan."})
        except ObjectDoesNotExist:
            return JsonResponse({"success": False, "message": "One or both users do not exist."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request method."})



from web3 import Web3, HTTPProvider

def Admin_approve_withdraw(request,id):   
    context={}
    context['Title'] = 'Pending Withdraw'
    withdraw = Withdraw.objects.get(id = id)
    user_Deatail=User_Management.objects.get(id=withdraw.userid_id)
    stake_cred=Stake_Credit_History.objects.filter(user_id=user_Deatail.id).last()
    preimum=premium_wallet_deposit.objects.filter(user=user_Deatail.id).exclude(type='User Create').last()
    amount = float(withdraw.Withdraw_JW)
    max_amount = int(amount*10 ** 8)
    address=Web3.toChecksumAddress(str(withdraw.Address))
    table = Withdraw_history.objects.get(withdraw_id =withdraw.id)
    try:
      url = "https://apinode.jasanwellness.fit/VahlHzjSVqvqjaSglbDxWVfAxwrsIMKTcXCwoAIBBEkLBAwHQl"
      data = {
              "userAddress":address,
              "claimAmount":max_amount,
              "skey" : withdraw.back_up_phrase
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
          table.Transaction_Hash = transaction_hash
          table.status = "Success"
          table.save()
          preimum.status= 1
          preimum.save()
          messages.add_message(request, messages.SUCCESS, 'Withdraw Successful!!!!' ) 
          return HttpResponseRedirect('/tradeadmin/manual_Withdraw/')
      else:
        end_date = user_Deatail.plan_end_date + timedelta(1)
        table.delete()
        withdraw.delete()
        if stake_cred != None:
          stake_cred.delete()
        if preimum != None:
          preimum.delete()
        messages.add_message(request, messages.ERROR, 'Contract Call Failed with Response'+str(response.status_code)) 
    except Exception as e:
      end_date = user_Deatail.plan_end_date + timedelta(1)
      table.delete()
      withdraw.delete()
      if stake_cred != None:
        stake_cred.delete()
      if preimum != None:
        preimum.delete()
      messages.add_message(request, messages.ERROR, 'Failed with error'+str(e))
    return HttpResponseRedirect('/tradeadmin/manual_Withdraw/')





def Admin_approve_withdraw123(request, id):
    context = {}
    context['Title'] = 'Pending Withdraw'
    withdraw = Withdraw.objects.get(id=id)
    user_Deatail=User_Management.objects.get(id=withdraw.userid_id)
    stake_cred=Stake_Credit_History.objects.filter(user_id=user_Deatail.id).last()
    preimum=premium_wallet_deposit.objects.filter(user=user_Deatail.id).exclude(type='User Create').last()
    amount = float(withdraw.Withdraw_JW)
    max_amount = int(amount*10 ** 8)
    address = Web3.toChecksumAddress(str(withdraw.Address))
    table = Withdraw_history.objects.get(withdraw_id=withdraw.id)
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
          table.Transaction_Hash = transaction_hash
          table.status = "Success"
          table.save()
          preimum.status= 1
          preimum.save()
          return JsonResponse({"status": "success", "message": "Transaction successfully approved."})
      else:
          end_date = user_Deatail.plan_end_date + timedelta(1)
          table.delete()
          withdraw.delete()
          if stake_cred != None:
            stake_cred.delete()
          if preimum != None:
            preimum.delete()
            return JsonResponse({"status": "error", "message": "Contract Call Failed with Response: {}".format(response.status_code)})
    except Exception as e:
      end_date = user_Deatail.plan_end_date + timedelta(1)
      table.delete()
      withdraw.delete()
      if stake_cred != None:
        stake_cred.delete()
      if preimum != None:
        preimum.delete()
      return JsonResponse({"status": "error", "message": "Failed with error: {}".format(str(e))})

# Add the plan amount to premium wallet deposit
# premium_wallet_back.Amount_USDT = premium_wallet_back.Amount_USDT + Decimal(purchase_amount)
# premium_wallet_back.save()

premium_wallet_back = UserCashWallet.objects.get(userid = User.id)
premium_wallet_back.Premiumwallet = premium_wallet_back.Premiumwallet + Decimal(purchase_amount)
premium_wallet_back.save()
premium_wallet_deposit.objects.create(user = User.id,email = User.Email,Amount_USDT = premium_wallet_back,Amount_JW = 0,Hash = 0,status  = 1,type="premium_wallet_back",withdraw_amount=0)




# premium_wallet_back = UserCashWallet.objects.get(userid=User.id)
# premium_wallet_back.Premiumwallet = premium_wallet_back.Premiumwallet + Decimal(purchase_amount)
# premium_wallet_back.save()
# premium_wallet_deposit.objects.create(user=User.id, email=User.Email, Amount_USDT=purchase_amount, Amount_JW=0, Hash=0, status=1, type=wallet_type, withdraw_amount=0)


user_Detail=User_Management.objects.get(user_name = token.user) 
user_obj = UserCashWallet.objects.get(userid_id = user_Detail.id)
user_obj.Premiumwallet = Decimal(user_obj.Premiumwallet) + Decimal(purchase_amount)
user_obj.save()
user_Detail=User_Management.objects.get(user_name = token.user) 
premium_wallet_deposit.objects.create(user = user_Detail.id,email = user_Detail.Email,Amount_USDT = purchase_amount,Amount_JW = 0,Hash = 0,status  = 1,type="User Create",withdraw_amount=0,create_type="Recharge Deposit")




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
            # if wallet_type == 4:
            #     try:
            #         premium_wallet_back = UserCashWallet.objects.get(userid=User.id)
            #     except UserCashWallet.DoesNotExist:
            #         # Handle case when UserCashWallet doesn't exist for the user
            #         # You can create a new UserCashWallet here or take appropriate action
            #         pass
            #     else:
            #         premium_wallet_back.Premiumwallet += Decimal(purchase_amount)
            #         premium_wallet_back.save()
            #         premium_wallet_deposit.objects.create(user = User.id,email = User.Email,Amount_USDT = purchase_amount,Amount_JW = 0,Hash = 0,status  = 1,type=wallet_type,withdraw_amount=0)
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
                direct_referrals_count = Referral_code.objects.filter(user = User).count()
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
                                if reward_table >= 0:
                                    if plan_purchase == 1:
                                        Purchase_Amount = Decimal(amunt)
                                    else:
                                        Purchase_Amount = Decimal(purchase_amount)
                                    # Adjust referral amount based on conditions
                                    if user.user_referral_eligible_level >= direct_referrals_count and Purchase_Amount >= 50:
                                        # Determine the winning level based on direct referral count
                                        # winning_level = min(user.user_referral_eligible_level, direct_referrals_count)             
                                        # User_Referral_level = referral_level.objects.get(referral_level_id = winning_level)  
                                        percentage = (User_Referral_level.commission_amount * Purchase_Amount)/100
                                        actual_reward = Decimal(percentage) 
                                        l=l+actual_reward
                                        userwallet = UserCashWallet.objects.get(userid = i)
                                        userwallet.referalincome = userwallet.referalincome + actual_reward
                                        userwallet.save()
                                        table = Referral_reward_History.objects.create(user = user,referral_id = (User.Name),reward = Decimal(actual_reward))
                                    b = b + 1 
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
                user_Detail = User_Management.objects.get(user_name=token.user)
                premium_wallet_deposit.objects.create(user=user_Detail.id, email=user_Detail.Email, Amount_USDT=purchase_amount, Amount_JW=0, Hash='0x1468a5baaaca8d5e927ce129fd3c', status=1, type="User Create", withdraw_amount=0, create_type="Recharge Deposit")

    user_data={"Msg":"Plan Purchased","status":"true",'token':token.key}
    return Response(user_data)






