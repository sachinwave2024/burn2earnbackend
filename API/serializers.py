from rest_framework import serializers
from API.models import Contract_address, Delete_Account_Management, Delete_Account_Reason_Management, Google_Fitness, Internal_transfer_history, Pin, Plan_purchase_wallet, Referral_reward_History, Reward_History, User_2x_Boost, User_address, UserCashWallet, Withdraw, Withdraw_history, plan, referral_level,Boat_Referral_reward_History,Roi_Reward_History,Boat_Referral_income_History,MPPlanlist,MPRewardHistory,MPDailyRewardHistory,BurnRewardHistory,BurnMonthRewardHistory,BurnWithdraw,CBurnRewardHistory,CBurnMonthRewardHistory
from locations.models import Country,State
from trade_master.models import Cms_StaticContent, Faq,SupportCategory,Stake_Credit_History
from trade_admin_auth.models import Registration_otp,  Steps_history,  User_Management, User_two_fa
from Staking.models import stake_claim_table


class User_Serializer(serializers.ModelSerializer):

    class Meta:
        model = User_Management
        fields=['user_name','Email','referal_code','User_type']

class Register_OTP_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Registration_otp
        fields=['email_otp']

class Login_Serializer(serializers.ModelSerializer):

    class Meta:
        model = User_Management
        fields = ['Email']

class user_DeatailSerializers(serializers.ModelSerializer):
  
    class Meta:
        model=User_Management
        fields = ['user_name','Name','Email','user_phone_number','user_profile']

class User_see(serializers.ModelSerializer):
    class Meta:
        model= User_Management
        fields = ['id','user_name','Name','Email','User_Verification_Status','Direct_referral_id','phone_number','user_profile_pic','device_unique_id','request_device_id','USER_INRID','created_on','User_type']

class two_fa_Serializers(serializers.ModelSerializer):
  
    class Meta:
        model=User_two_fa
        fields = ['user_totp']

# class user_ref_upline(serializers.ModelSerializer):

#     class Meta:
#         model= User_Management
#         fields = ['id','Name','Email','user','user_name','plan_start_date','plan_end_date','plan','Newstake_wallet','TradeBwa']


class user_ref_upline(serializers.ModelSerializer):
    # Define a computed field for TradeBwa divided by 3, rounded to 2 decimal places
    TradeBwa_divided = serializers.SerializerMethodField()

    class Meta:
        model = User_Management
        fields = ['id', 'Name', 'Email', 'user', 'user_name', 'plan_start_date', 'plan_end_date', 'plan', 'Newstake_wallet', 'TradeBwa', 'TradeBwa_divided','MPlan','Burnamount','Burnamountjwc']

    def get_TradeBwa_divided(self, obj):
        # Divide TradeBwa by 3 and round to 2 decimal places
        return round(obj.TradeBwa / 3, 2) if obj.TradeBwa is not None else 0


class Google_fitness_Serializers(serializers.ModelSerializer):

    class Meta:
        model = Google_Fitness
        fields = ['Google_status']

class step_count_Serializers(serializers.ModelSerializer):

    class Meta:
        model = User_Management
        fields = ['over_all_stepcount']


class Steps_history_Serializers(serializers.ModelSerializer):

    class Meta:
        model =Steps_history
        fields = ['steps']

class user_step_Serializers(serializers.ModelSerializer):

    class Meta:
        model = Steps_history
        fields = '__all__' 


class User_two_fa_details_Serializers(serializers.ModelSerializer):

    class Meta:
        model= User_two_fa
        fields = '__all__'


class terms_cms_Serializers(serializers.ModelSerializer):

    class Meta:
        model= Cms_StaticContent
        fields = '__all__'

class Faq_Serializers(serializers.ModelSerializer):

    class Meta:
        model= Faq
        fields = '__all__'

class Pin_Set_Serializer(serializers.ModelSerializer):

    class Meta:
        fields=['pin','confirm_pin']

class Change_Pin_Serializer(serializers.ModelSerializer):

    class Meta:
        fields=['old_pin','new_pin','confirm_pin']

class Verify_Pin_Serializer(serializers.ModelSerializer):

    class Meta:
        fields=['pin']

class Reward_History_Serializers(serializers.ModelSerializer):

    class Meta:
        model= Reward_History
        fields = '__all__'

class Withdraw_history_Serializers(serializers.ModelSerializer):

    class Meta:
        model= Withdraw
        fields = '__all__'
        
class burnWithdraw_history_Serializers(serializers.ModelSerializer):

    class Meta:
        model= BurnWithdraw
        fields = '__all__'

class User_withdraw_see(serializers.ModelSerializer):
    class Meta:
        model= Withdraw
        fields = ['id','userid','Amount','Withdraw_fee','Withdraw_USDT','Withdraw_JW','Address','Transaction_Hash', 'created_on', 'Month_stake', 'Wallet_type' , 'status','back_up_phrase']

class User_BurnWithdraw_see(serializers.ModelSerializer):
    class Meta:
        model= BurnWithdraw
        fields = ['id','userid','Amount','Withdraw_fee','Withdraw_USDT','Withdraw_JW','Address','Transaction_Hash', 'created_on', 'Month_stake', 'Wallet_type' , 'status','back_up_phrase']

class User_stake_withdraw_see(serializers.ModelSerializer):
    class Meta:
        model= stake_claim_table
        fields = ['id','user','email','original_USDT','claim_amount_USDT','claim_amount_JW','Address','status','Wallet_type', 'created_on']

class Referral_History_Serializers(serializers.ModelSerializer):

    class Meta:
        model = Referral_reward_History
        fields = '__all__'
class Stake_credit_Serializers(serializers.ModelSerializer):

    class Meta:
        model= Stake_Credit_History
        fields = '__all__'

class Delete_Reason_Serializers(serializers.ModelSerializer):

    class Meta:
        model = Delete_Account_Reason_Management
        fields = '__all__'

class Delete_Serializers(serializers.ModelSerializer):

    class Meta:
        model= Delete_Account_Management
        fields = ['Delete_Account','reason']

class Country_Serializers(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'

class State_Serializers(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = '__all__'


class user_address_Serializers(serializers.ModelSerializer):

    class Meta:
        model = User_address
        fields = '__all__'

class plan_Serializers(serializers.ModelSerializer):

    class Meta:
        model = plan
        fields = '__all__'

      
class User_Referral_Serializers(serializers.ModelSerializer):

    class Meta:
        model = User_Management
        fields = ['user_name','Email','plan']


class Plan_purchase_wallet_Serializers(serializers.ModelSerializer):

    class Meta:
        model = Plan_purchase_wallet
        fields = ['Health_wallet_plan','Health_wallet_Withdraw','Referral_wallet_plan','Referral_wallet_Withdraw','Trust_wallet_plan','Trust_wallet_Withdraw']
class User_device_see(serializers.ModelSerializer):

    class Meta:
        model= User_Management
        fields = ['id','Name','Email','user_phone_number','device_unique_id','user_profile_pic','status']
        
class Trade_Referral_History_Serializers(serializers.ModelSerializer):

    class Meta:
        model = Boat_Referral_reward_History
        fields = '__all__'

class Bot_Referral_history_Serializers(serializers.ModelSerializer):

    class Meta:
        model = Boat_Referral_income_History
        fields = '__all__'

class Trade_Reward_History_Serializers(serializers.ModelSerializer):

    class Meta:
        model= Roi_Reward_History
        fields = '__all__'





class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Management
        fields = ['Email', 'plan', 'plan_start_date', 'transferpw']  # Add the columns you want to show



class MPPlanlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = MPPlanlist
        fields = '__all__'
        
        

class MPlan_Reward_History_Serializers(serializers.ModelSerializer):
    class Meta:
        model= MPDailyRewardHistory
        fields = '__all__'
        
class MPlan_Referral_history_Serializers(serializers.ModelSerializer):
    class Meta:
        model = MPRewardHistory
        fields = '__all__'
        
        
class User_Management_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User_Management
        fields = ['id', 'Email', 'User_type']  # Add the fields you want to return
        
 
 
        
class burn_Reward_History_Serializers(serializers.ModelSerializer):
    class Meta:
        model= BurnMonthRewardHistory
        fields = '__all__'
        
class burn_Referral_history_Serializers(serializers.ModelSerializer):
    class Meta:
        model = BurnRewardHistory
        fields = '__all__'
        
class Cburn_Reward_History_Serializers(serializers.ModelSerializer):
    class Meta:
        model= CBurnMonthRewardHistory
        fields = '__all__'
        
class Cburn_Referral_history_Serializers(serializers.ModelSerializer):
    class Meta:
        model = CBurnRewardHistory
        fields = '__all__'
        