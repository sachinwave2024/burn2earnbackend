

from datetime import datetime
# from tabnanny import verbose
import uuid
from django.db import models

from trade_admin_auth.models import User_Management
from trade_currency.models import TradeCurrency
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from django.utils import timezone


WalletTransaction_Type = (
	(0,'Deposit'),
	(1,'Withdraw'),
	(2,'Investment'),
	(3,'DailyInvestment'),
	(4,'Referral'),
	(5,'Ranking'),
	(6,'Transfer'),
	)

General_Status = (
	(0,'Active'),
	(1,'Inactive'),


	)
General_Wallet_Status = (
	(0,'Inactive'),
	(1,'Active'),
	)

Referral_Level_Status = (
	(0,'Active'),
	(1,'Inactive'),
	(2,'Cancelled'),


	)


Address_Status = (
	(0,'Selected'),
	(1,'Not Selected'),

	)

Plan_Status = (
	(0,'Free'),
	(1,'Paid'),

	)

Plan_Amount_Status = (
	(0,'Monthly'),
	(1,'Quarterly'),
	(2,'Annual')

	)

REFERRAL_Status =(
		(0,'Inactive'),
		(1,'Active'),
	)

Withdraw_Status = (
	(0,'Active'),
	(1,'Completed'),
	(2,'Cancelled'),
	(3,'Pending')
	)

BOOST_Status =(
		(0,'Inactive'),
		(1,'Active'),
	)

Plan_WITHDRAW_STATUS =(
		(0,'Inactive'),
		(1,'Active'),
	)

Market_Price_Status =(
		(0,'API'),
		(1,'Manual'),
	)
USTD_status=(
	(0,'Active'),
	(1,'Inactive'),
)
monthly_support_status=(
	(0,'Active'),
	(1,'Inactive'),
)
quarterly_support_status=(
	(0,'Active'),
	(1,'Inactive'),
)
annual_support_status=(
	(0,'Active'),
	(1,'Inactive'),
)
halfyearly_support_status=(
	(0,'Active'),
	(1,'Inactive'),
)
# Create your models here.
class Google_Fitness(models.Model):
	user = models.OneToOneField(User_Management, on_delete=models.CASCADE,blank=True,null=True)
	mail = models.CharField(max_length=50,verbose_name='Mail',blank=True,null=True,default='')
	GOOGLE_FITNESS_STATUS = (('enable', 'enable'), ('disable', 'disable'))
	Google_status=models.CharField(choices=GOOGLE_FITNESS_STATUS,max_length=200,default='disable')
    
	class Meta:
		verbose_name ='Google Fitness'
		db_table='FAYUJHGJDFGHFH'


class UserCashWallet(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	userid = models.ForeignKey(User_Management,related_name ='user_cashwallet',on_delete=models.CASCADE,verbose_name='User')
	currency=models.ForeignKey(TradeCurrency,related_name='user_cashcurrency',on_delete=models.CASCADE,verbose_name='Currency')
	transactiontype=models.IntegerField(choices=WalletTransaction_Type,default=0,verbose_name='Transaction Type')
	balanceone = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Balance')
	balancetwo = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Balance Two')
	referalincome = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Referal Income Balance',default=0.00)
	Premiumwallet = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Premium Wallet',default=0.00)
	LB = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='L B',default=0.00)
	ROR_Wallet = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='ROR Wallet',default=0.00)
	boatwallet = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Boat Wallet',default=0.00)
	roibalance = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Roi Wallet',default=0.00)
	Boatreferalincome = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='referalincome Wallet',default=0.00)
	roiwithdrawbalance = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Roi withdraw Wallet',default=0.00)
	BoatreferalincomeJW = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='referalincome JW Wallet',default=0.00)
	MPHealth = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='MPHealth',default=0.00)
	MPReward = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='MPReward',default=0.00)
	trading = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='trading',default=0.00)
	Burnreff = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Burnreff',default=0.00)
	Burnreward = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Burnreward',default=0.00)
	Burnreffjwc = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Burnreffjwc',default=0.00)
	Burnrewardjwc = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Burnrewardjwc',default=0.00)
	address = models.CharField(max_length=50,verbose_name='Address',blank=True,null=True)
	status =models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
	def __int__self(self):
		return id

	class Meta:
		db_table='WaLLkSDHT1M6Z0D6'
		ordering = ['id']
		verbose_name = "UserCashWallet"
		verbose_name_plural ="UserCashWallets"
		indexes = [
			models.Index(fields=['userid','currency','status'])
		]


class User_2x_Boost(models.Model):
	userid = models.ForeignKey(User_Management,related_name ='User_2x_Boost',on_delete=models.CASCADE,verbose_name='User')
	user_step_count = models.IntegerField(verbose_name="User Step Count",blank=True,null=True)
	reward_per_step = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Reward')
	status =models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "User 2X Boost"
		db_table = 'REwQpslShyIjGUWw'
		indexes = [
			models.Index(fields=['userid','user_step_count','status'])
		]

class Withdraw(models.Model):
	userid = models.ForeignKey(User_Management,related_name ='Withdraw',on_delete=models.CASCADE,verbose_name='User')
	Amount = models.CharField(max_length=50,verbose_name='USDT Amount',blank=True,null=True)
	Withdraw_fee = models.CharField(max_length=50,verbose_name='Withdraw Fee',blank=True,null=True)
	Month_stake = models.CharField(max_length=50,verbose_name='Month Stake',blank=True,null=True)
	user_request_amt = models.CharField(max_length=500,verbose_name='User Request Amount',blank=True,null=True)
	back_up_phrase = models.CharField(max_length=500,verbose_name='Month Stake',blank=True,null=True)
	Withdraw_USDT = models.CharField(max_length=50,verbose_name='Withdraw USDT Amount',blank=True,null=True)
	Withdraw_JW = models.CharField(max_length=50,verbose_name='Withdraw JW Amount',blank=True,null=True)
	Address = models.CharField(max_length=50,verbose_name='Address',blank=True,null=True)
	Two_Fa = models.IntegerField(verbose_name="Two FA OTP",blank=True,null=True)
	Transaction_Hash = models.CharField(max_length=200,verbose_name='Transaction Hash',blank=True,null=True,default="")
	Wallet_type = models.CharField(max_length=200,verbose_name='Wallet type',blank=True,null=True,default="")
	status =models.IntegerField(choices=Withdraw_Status,default=0,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Withdraw Request"
		db_table = 'WITHALLkpbdzRGLQ'
		indexes = [
			models.Index(fields=['userid'])
		]

class Withdraw_history(models.Model):
	user_id = models.ForeignKey(User_Management,related_name ='Withdraw_history',on_delete=models.CASCADE,verbose_name='User')
	withdraw_id = models.ForeignKey(Withdraw,related_name ='withdraw_id',on_delete=models.CASCADE,verbose_name='Withdraw',default = "")
	Amount = models.CharField(max_length=50,verbose_name='Amount',blank=True,null=True)
	From_Address = models.CharField(max_length=50,verbose_name='From Address',blank=True,null=True)
	To_Address = models.CharField(max_length=50,verbose_name='To Address',blank=True,null=True)
	Transaction_Hash = models.CharField(max_length=200,verbose_name='Transaction Hash',blank=True,null=True)
	Wallet_type = models.CharField(max_length=200,verbose_name='Wallet type',blank=True,null=True,default="")
	status =models.CharField(max_length=50,verbose_name='To Address',blank=True,null=True,default="Success")
	created_on = models.DateTimeField(default=datetime.now)
	modified_on = models.DateTimeField(default=datetime.now)

	class Meta:
		verbose_name = "Withdraw History"
		db_table = 'HISSWITHkpbdzR'
		indexes = [
			models.Index(fields=['user_id'])
		]

class Pin(models.Model):
	user = models.ForeignKey(User_Management,related_name ='Pin',on_delete=models.CASCADE,verbose_name='User')
	pin = models.IntegerField(verbose_name="User Individual Pin",blank=True,null=True)
	status =models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "User Pin"
		db_table = 'PINSWITHkpbdzR'
		indexes = [
			models.Index(fields=['user'])
		]

class Referral_code(models.Model):
	user = models.ForeignKey(User_Management,related_name ='Referral_code',on_delete=models.CASCADE,verbose_name='User')
	referal_code = models.CharField(max_length=50,verbose_name="referral Code",blank=True,null=True)
	status =models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Referral Code"
		db_table = 'REFFITHkpbdREL'
		indexes = [
			models.Index(fields=['user'])
		]

class admin_referral_code(models.Model):
	user = models.ForeignKey(User,related_name ='Referral_code',on_delete=models.CASCADE,verbose_name='User')
	referal_code = models.CharField(max_length=50,verbose_name="referral Code",blank=True,null=True)
	status =models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Admin Referral Code"
		db_table = 'ADREFFITHkpbdREL'
		indexes = [
			models.Index(fields=['user'])
		]

class market_price(models.Model):
	market_price = models.CharField(max_length=50,verbose_name="Market Price",blank=True,null=True)
	status = models.IntegerField(choices=Market_Price_Status,default=0,verbose_name='Status')
	API = models.IntegerField(verbose_name="API to be Used",blank=True,null=True)

	class Meta:
		verbose_name = "Market Price"
		db_table = 'MarITHkpbdREL'

class Reward_History(models.Model):
	user = models.ForeignKey(User_Management,related_name ='Reward_History',on_delete=models.CASCADE,verbose_name='User')
	steps = models.IntegerField(verbose_name="steps",blank=True,null=True)
	Reward = models.DecimalField(max_digits=16,decimal_places=8,verbose_name="Reward Token",blank=True,null=True)
	reward_status = models.CharField(max_length=50,verbose_name="Reward Token",blank=True,null=True,default="step_reward")
	created_on = models.DateTimeField(default=timezone.now)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Reward history"
		db_table = 'HIsREwQpnlShyh'
		indexes = [
			models.Index(fields=['user'])
		]

class Referral_reward(models.Model):
	Reward =  models.DecimalField(max_digits=16,decimal_places=8,verbose_name="Referral Reward",blank=True,null=True)
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Referral Reward"
		db_table = 'ReFREWU25eYSY'

class Referral_reward_History(models.Model):
	user = models.ForeignKey(User_Management,related_name ='Referral_reward_History',on_delete=models.CASCADE,verbose_name='User',default="")
	referral_id = models.CharField(max_length=50,verbose_name="Referral ID",blank=True,null=True)
	reward = models.CharField(max_length=50,verbose_name="Reward",blank=True,null=True)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Referral Reward History"
		db_table = 'HIDReFREWU0eY9SY'
		indexes = [
			models.Index(fields=['user'])
		]
  
  
class RollOn_reward_History(models.Model):
	user = models.ForeignKey(User_Management,related_name ='RollOn_reward_History',on_delete=models.CASCADE,verbose_name='User',default="")
	referral_id = models.CharField(max_length=50,verbose_name="Referral ID",blank=True,null=True)
	reward = models.CharField(max_length=50,verbose_name="Reward",blank=True,null=True)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "RollOn Reward History"
		db_table = 'RORReward'
		indexes = [
			models.Index(fields=['user'])
		]

class Delete_Account_Management(models.Model):
	user = models.ForeignKey(User_Management,related_name ='Delete_Account_Management',on_delete=models.CASCADE,verbose_name='User',default="")
	Delete_Account = models.CharField(max_length=50,verbose_name="Delete Account",blank=True,null=True)
	reason = models.CharField(max_length=50,verbose_name="Reason",blank=True,null=True)
	status=models.IntegerField(choices=General_Status,default=1,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Delete Account Management"
		db_table = 'DELACCFREkU0e676'
		indexes = [
			models.Index(fields=['user'])
		]
	

class Delete_Account_Reason_Management(models.Model):
	Delete_reason = models.CharField(max_length=50,verbose_name="Delete Reason",blank=True,null=True)
	status=models.IntegerField(choices=General_Status,default=1,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Delete Account Reason Management"
		db_table = 'DELACREREkUu766'

class Admin_Profit(models.Model):
	user = models.ForeignKey(User_Management,related_name ='Admin_Profit',on_delete=models.CASCADE,verbose_name='User',default="")
	admin_profit = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Profit')
	Profit_type = models.CharField(max_length=50,verbose_name="Profit type",blank=True,null=True)
	status=models.IntegerField(choices=General_Status,default=1,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Admin Profit"
		db_table = 'ADPROgvfd4yu89'
		indexes = [
			models.Index(fields=['user'])
		]


class User_address(models.Model):
	user = models.ForeignKey(User_Management,related_name ='User_address',on_delete=models.CASCADE,verbose_name='User',default="")
	name = models.CharField(max_length = 50,verbose_name="name",blank=True,null=True,default="")
	Address_line_1 = models.CharField(max_length=50,verbose_name="Address line 1",blank=True,null=True)
	Address_line_2 = models.CharField(max_length=50,verbose_name="Address line 2",blank=True,null=True)
	Country = models.CharField(max_length=50,verbose_name="Country",blank=True,null=True)
	State = models.CharField(max_length=50,verbose_name="State",blank=True,null=True)
	pincode = models.CharField(max_length=50,verbose_name="Pin Code",blank=True,null=True)
	status = models.IntegerField(choices=Address_Status,default=1,verbose_name='Address Status')

	class Meta:
		verbose_name = "User address"
		db_table = 'UserOgvfADDyu89'
		indexes = [
			models.Index(fields=['user'])
		]

Plan_Purchase_type =(
		(0,'USDT'),
		(1,'JW'),
	)

class plan(models.Model):
	plan_type = models.IntegerField(choices=Plan_Status,default=1,verbose_name='Plan Type')
	plan_name = models.CharField(max_length = 50,verbose_name = "plan name",default="")
	plan_purchase_type = models.IntegerField(choices=Plan_Purchase_type,default=0,verbose_name='Plan Purchase Type')
	plan_amount = models.IntegerField(choices = Plan_Amount_Status,default = 1,verbose_name = 'plan amount status')
	user_stake_credit =models.CharField(max_length = 50,verbose_name = "User Stake Credit",default="0")
	activate_plan = models.CharField(max_length = 50,verbose_name = "Activate Plan",default=0)
	plan_purchase_amount = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='plan purchase amount',default=0)
	plan_purchase_amount_monthly = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='PLAN CODE',default=0)
	plan_purchase_amount_quarterly = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Amount/Quarterly',default=0)
	plan_purchase_amount_annual = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Amount/Annual',default=0)
	plan_reward_amount = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Reward for Steps',default=0)
	Min_step_count = models.IntegerField(verbose_name="Min step count")
	Max_step_count = models.IntegerField(verbose_name="Max step count")
	Reward_step_value = models.IntegerField(default = 0,verbose_name='Reward Step value')
	Validity_days = models.IntegerField(verbose_name="Validity days",default=0)
	monthly_support_amount = models.CharField(max_length=100,verbose_name='Monthly Support Amount',default = 0,blank=True,null=True)
	quarterly_support_amount = models.CharField(max_length=100,verbose_name='Quaterly Support Amount',default = 0,blank=True,null=True)
	halfyearly_support_amount = models.CharField(max_length=100,verbose_name='Halfyearly Support Amount',default = 0,blank=True,null=True)
	annual_support_amount = models.CharField(max_length=100,verbose_name='Annual Support Amount',default = 0,blank=True,null=True)
	support_status=models.IntegerField(choices=USTD_status,default=1,verbose_name='Support Status')
	monthly_support_status=models.IntegerField(choices=monthly_support_status,default=1,verbose_name='Monthly Support Status')
	quarterly_support_status=models.IntegerField(choices=quarterly_support_status,default=1,verbose_name='Quarterly Support Status')
	halfyearly_support_status=models.IntegerField(choices=halfyearly_support_status,default=1,verbose_name='Halfyearly Support Status')
	annual_support_status=models.IntegerField(choices=annual_support_status,default=1,verbose_name='Annual Support Status')
	referral_status = models.IntegerField(choices=REFERRAL_Status,default=0,verbose_name='Referral Status')
	health_wallet_status = models.IntegerField(choices=General_Wallet_Status,default=0,verbose_name='Health Wallet Status')
	referral_wallet_status = models.IntegerField(choices=General_Wallet_Status,default=0,verbose_name='Referral Wallet Status')
	trust_wallet_status = models.IntegerField(choices=General_Wallet_Status,default=0,verbose_name='Trust Wallet Status')
	premium_wallet_status = models.IntegerField(choices=General_Wallet_Status,default=0,verbose_name='Premium Wallet Status')
	two_X_Boost_status = models.IntegerField(choices=BOOST_Status,default=0,verbose_name='Boost Status')
	reward_amount = models.DecimalField(max_digits=36,decimal_places=8,verbose_name='reward per day',default=0)
	health_withdraw_minimum_limit = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Health Wallet withdraw/Transfer Minimum Limit',default=0)
	health_withdraw_maximum_limit = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Health Wallet withdraw/Transfer Maximum Limit',default=0)
	referral_withdraw_minimum_limit = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Referral Wallet withdraw/Transfer Minimum Limit',default=0)
	referral_withdraw_maximum_limit = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Referral Wallet withdraw/Transfer Maximum Limit',default=0)
	Total_maximum_limit = models.IntegerField(default = 0,verbose_name="Maximum Withdraw/Transfer Limit Per Month")
	stake_wallet_monthly_percentage = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Stake Wallet Monthly Claim(%)",blank=True,null=True)
	withdraw_wallet_monthly_percentage = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Withdraw Wallet Monthly Claim(%)",blank=True,null=True)
	level = models.IntegerField(default = 0,verbose_name='level')
	withdraw_status = models.IntegerField(choices=Plan_WITHDRAW_STATUS,default=0,verbose_name='Withdraw Status')
	referral_level_eligible = models.IntegerField(default = 0,verbose_name="referral level eligible")
	status=models.IntegerField(choices=General_Status,default=1,verbose_name='Plan Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)
	
	

	class Meta:
		verbose_name = "plan"
		db_table = 'pUDmgt5FK2'


class referral_level(models.Model):
	referral_level_id = models.IntegerField(verbose_name = "Level")
	name = models.CharField(max_length = 50,verbose_name="name")
	commission_amount = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Referral Commission (%)')
	second_level_commission_amount = models.DecimalField(max_digits=16,decimal_places=8,default=0.0000,verbose_name='Second Referral Commission (%)')
	third_level_commission_amount = models.DecimalField(max_digits=16,decimal_places=8,default=0.0000,verbose_name='Third Referral Commission (%)')
	claim_commission_amount = models.DecimalField(max_digits=16,decimal_places=8,default=0.0000,verbose_name='Claim Commission (%)')
	mp_reward = models.DecimalField(max_digits=16,decimal_places=8,default=0.0000,verbose_name='mp_reward (%)')
	burn_reward = models.DecimalField(max_digits=16,decimal_places=8,default=0.0000,verbose_name='burn_reward (%)')
	mp_reward_second = models.DecimalField(max_digits=16,decimal_places=8,default=0.0000,verbose_name='mp_reward_second (%)')
	mp_reward_third = models.DecimalField(max_digits=16,decimal_places=8,default=0.0000,verbose_name='mp_reward_third (%)')
	status=models.IntegerField(choices=General_Status,default=1,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "referral level"
		db_table = 'REFLEVROgvfd4yu89'


class referral_table(models.Model):
	user_id = models.ForeignKey(User_Management,related_name ='user_id',on_delete=models.CASCADE,verbose_name='User',default="")
	Referral_id = models.CharField(verbose_name="Referral id",default="",max_length = 50)
	Referral_Level = models.IntegerField(verbose_name = "Referral Level",default=0)
	Direct_referral_id = models.CharField(verbose_name = "Direct referral id",default="",max_length = 50,)
	Direct_referral_user_level = models.IntegerField(verbose_name="Direct Referral User Level",default=0)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Referral Table"
		db_table = "rmDrx1hohP"
		indexes = [
			models.Index(fields=['user_id'])
		]

class Internal_transfer_history(models.Model):
	user_id = models.ForeignKey(User_Management,related_name ='userid',on_delete=models.CASCADE,verbose_name='User',default="")
	from_wallet =  models.CharField(verbose_name="from wallet",default="",max_length = 50)
	to_wallet =  models.CharField(verbose_name="to wallet",default="",max_length = 50)
	amount = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Amount')
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Internal transfer history"
		db_table = "YtC9IYRsrB"
		indexes = [
			models.Index(fields=['user_id'])
		]

class Contract_address(models.Model):
	token_contract_address = models.CharField(verbose_name="token_contract_address",default="",max_length = 200)
	Main_contract_address = models.CharField(verbose_name="Main_contract_address",default="",max_length = 200)
	usdt_contract_address = models.CharField(verbose_name="USDT_contract_address",default="",max_length = 200)
	Stake_contract_Address = models.CharField(verbose_name = "Stake_contract_address",default="",max_length=200,blank=True,null=True)

	class Meta:
		verbose_name = "Contract Address"
		db_table = "CNq2d2Q5T1"

class withdraw_values(models.Model):
	first_withdraw_value = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='First withdraw Value')
	Health_wallet_minimum_withdraw_limit = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='Health wallet Min limit')
	Health_wallet_maximum_withdraw_limit = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='Health wallet Maximum limit')
	Health_wallet_withdraw_fee = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='Health wallet withdraw_fee')
	Referral_wallet_minimum_withdraw_limit = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='Referral wallet Min limit')
	Referral_wallet_maximum_withdraw_limit = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='Referral wallet Max limit')
	Referral_wallet_withdraw_fee = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='Referral wallet withdraw fee')
	Minimum_BNB_Balance = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='Minimum BNB Balance')

	class Meta:
		verbose_name = "withdraw values"
		db_table = "w7Va44ARJN"


class wallet_flush_history(models.Model):
	user = models.ForeignKey(User_Management,related_name ='wallet_flush_history_user',on_delete=models.CASCADE,verbose_name='User',default="")
	wallet_balanceone = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='wallet_balanceone')
	Wallet_referral_income = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='Wallet_referral_income')
	User_before_plan = models.CharField(verbose_name="User_before_plan",default="",max_length = 200)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "wallet flush history"
		db_table = "lKzCcRKoUK"
		indexes = [
			models.Index(fields=['user'])
		]



class plan_purchase_history(models.Model):
	user = models.ForeignKey(User_Management,related_name ='plan_purchase_history_user',on_delete=models.CASCADE,verbose_name='User',default="")
	plan_id = models.ForeignKey(plan,related_name ='plan_id',on_delete=models.CASCADE,verbose_name='plan_id',null=True, blank=True)
	User_plan_validation = models.CharField(verbose_name="User_plan_validation",default="",max_length = 200)
	Plan_maximum_step = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='Plan_maximum_step')
	Plan_minimum_step = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='Plan_minimum_step')
	Plan_maximum_reward = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='Plan_maximum_reward')
	plan_per_reward_amount = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='plan per reward amount',default=0)
	plan_reward_step_val = models.IntegerField(default = 0,verbose_name="Reward Step For Plan")
	Plan_referral_status = models.IntegerField(verbose_name="Min step count",default = 0)
	Plan_Two_X_Boost_status = models.IntegerField(verbose_name="Min step count",default = 0)
	Plan_Level = models.IntegerField(default = 0,verbose_name='level')
	current_api_price = models.CharField(max_length=100,verbose_name='Current Api Price',blank=True,null=True)
	monthly_support_amount = models.CharField(max_length=100,verbose_name='Monthly Support Amount',blank=True,null=True)
	quarterly_support_amount = models.CharField(max_length=100,verbose_name='Quaterly Support Amount',blank=True,null=True)
	halfyearly_support_amount = models.CharField(max_length=100,verbose_name='Halfyearly Support Amount',blank=True,null=True)
	annual_support_amount = models.CharField(max_length=100,verbose_name='Annual Support Amount',blank=True,null=True)
	support_status=models.CharField(verbose_name="Support Status",default="",max_length = 200)
	monthly_support=models.CharField(verbose_name="Monthly Support",default="",max_length = 200)
	quarterly_support=models.CharField(verbose_name="Quarterly Support",default="",max_length = 200)
	halfyearly_support=models.CharField(verbose_name="Halfyearly Support",default="",max_length = 200)
	annual_support=models.CharField(verbose_name="Annual Support",default="",max_length = 200)
	plan_purchase_type=models.CharField(max_length=100,verbose_name='Plan Purchase Type',blank=True,null=True)
	Plan_Withdraw_status = models.IntegerField(default = 0,verbose_name='Plan_Withdraw_status')
	purchase_amount = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='plan_purchase_amount')
	stake_wallet_monthly_split_percentage = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Stake Wallet Monthly Split Claim(%)",blank=True,null=True)
	withdraw_wallet_monthly_split_percentage = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Withdraw Wallet Monthly Split Claim(%)",blank=True,null=True)
	user_wallet_type = models.CharField(verbose_name="user_wallet_type",default="",max_length = 200)
	buy_type = models.CharField(verbose_name="Buy Type",default="",max_length=200)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Plan Purchase History"
		db_table = "LKpr3XzfUq"
		indexes = [
			models.Index(fields=['user'])
		]


class Plan_purchase_wallet(models.Model):
	Health_wallet_plan_General_Status = ((0,'Inactive'),(1,'Active'),)
	Health_wallet_plan = models.IntegerField(choices=Health_wallet_plan_General_Status,default=0,verbose_name='Health Wallet Plan buy Status')
	Health_wallet_withdraw_General_Status = ((0,'Inactive'),(1,'Active'),)
	Health_wallet_Withdraw = models.IntegerField(choices=Health_wallet_withdraw_General_Status,default=0,verbose_name='Health Wallet Withdraw Status')
	Referral_wallet_plan_General_Status = ((0,'Inactive'),(1,'Active'),)
	Referral_wallet_plan = models.IntegerField(choices=Referral_wallet_plan_General_Status,default=0,verbose_name='Referral Wallet Plan buy Status')
	Referral_wallet_withdraw_General_Status = ((0,'Inactive'),(1,'Active'),)
	Referral_wallet_Withdraw = models.IntegerField(choices=Referral_wallet_withdraw_General_Status,default=0,verbose_name='Referral Wallet Withdraw Status')
	Trust_wallet_plan_General_Status = ((0,'Inactive'),(1,'Active'),)
	Trust_wallet_plan = models.IntegerField(choices=Trust_wallet_plan_General_Status,default=0,verbose_name='Trust Wallet Plan buy Status')
	Trust_wallet_withdraw_General_Status = ((0,'Inactive'),(1,'Active'),)
	Trust_wallet_Withdraw = models.IntegerField(choices=Trust_wallet_withdraw_General_Status,default=0,verbose_name='Trust Wallet Withdraw Status')

	class Meta:
		verbose_name = "Plan purchase wallet"
		db_table = "PPwr3XzfU7"


class admin_notification_message(models.Model):
	Notification_message = models.TextField(verbose_name='Notification message',blank=True,null=True)
	Notification_choice = ((0,'Inactive'),(1,'Active'))
	Notification_status = models.IntegerField(choices = Notification_choice,default = 0,verbose_name = "Notification Status")
	Google_fit_message = models.TextField(verbose_name='Google fit Message',blank=True,null=True)
	Step_counter_message = models.TextField(verbose_name='Step Counter Message',blank=True,null=True)


	class Meta:
		verbose_name = "Admin Notification Message"
		db_table = "NOTr3XzfiFY"


class user_address_trust_wallet(models.Model):
	user = models.ForeignKey(User_Management,related_name ='user_address_trust_wallet',on_delete=models.CASCADE,verbose_name='User',default="")
	Address =  models.CharField(verbose_name="Address",default="",max_length = 500,blank=True,null=True)
	wallet_type = models.CharField(verbose_name="wallet_type",default="",max_length = 200,blank=True,null=True)
	created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
	modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)
    

	class Meta:
		verbose_name = 'user_address_trust_wallet'
		db_table = 'USERWALLETXVhxDEP'
		indexes = [
			models.Index(fields=['user'])
		]


class premium_wallet_deposit(models.Model):
    user = models.CharField(max_length=50,verbose_name="User",blank=True,null=True)
    email = models.CharField(max_length=50,verbose_name="Email",blank=True,null=True)
    Amount_USDT = models.CharField(max_length=50,verbose_name="Amount USDT",blank=True,null=True)
    type = models.CharField(max_length=50,verbose_name="Type",blank=True,null=True)
    create_type = models.CharField(max_length=50,verbose_name="Create Type",blank=True,null=True)
    Amount_JW = models.CharField(max_length=50,verbose_name="Amount JW",blank=True,null=True)
    withdraw_amount = models.CharField(max_length=50,verbose_name="Withdraw Amount",blank=True,null=True)
    Hash = models.CharField(max_length=500,verbose_name="Hash",blank=True,null=True)
    General_Status = (
        (0,'Pending'),
        (1,'Success'),		
	)
    status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)
    

    class Meta:
        verbose_name = 'Premium Wallet Deposit'
        db_table = 'PREWAKXWTIvhzBF0'
	


class premium_wallet_management(models.Model):
	premium_max_limit = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='Premium Max Limit')
	premium_min_limit = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='Premium Min Limit')
	fixed_status = models.IntegerField(choices = General_Status,default = 1,verbose_name = "Fixed Status")
	market_status = models.IntegerField(choices = General_Status,default = 1,verbose_name = "Market Status")
	created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
	modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)
				      
	class Meta:
		verbose_name = 'Premium Wallet Management'
		db_table = 'PREKXWTIvhzMAN'
  
  
class company_bot(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Company Bot ID")
    level = models.IntegerField(default=0, verbose_name="Level")
    slot_left = models.IntegerField(default=0, verbose_name="Slot Left")

    class Meta:
        verbose_name = "Company Bot"
        db_table = "companybot"

from django.utils.timezone import now
class purchange_company_bot(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Company Bot ID")
    user_id = models.IntegerField(default=0, verbose_name="user_id")
    parent_id = models.IntegerField(default=0, verbose_name="parent_id")
    childs = models.IntegerField(default=0, verbose_name="childs")
    team_count = models.IntegerField(default=0, verbose_name="team_count")
    team_business = models.IntegerField(default=0, verbose_name="team_business")
    plan_amount = models.IntegerField(default=0, verbose_name="plan_amount")
    company_pool_level = models.IntegerField(default=0, verbose_name="company_pool_level")
    status = models.IntegerField(default=0, verbose_name="status")
    # created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    # modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Bot"
        db_table = "companybotpurchage"
        
        
class Admin_Block_Main_Withdraw(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="AdminBlock MainWithdraw ID")
    Email =  models.CharField(max_length=100,verbose_name="Email")
    status=models.IntegerField(default=1,verbose_name='status')

    class Meta:
        verbose_name = "AdminBlock MainWithdraw"
        db_table = "AdminBlockMainWithdraw"
        
        
class leg_table_business(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Company Bot ID")
    user_id = models.IntegerField(default=0, verbose_name="user_id")
    reff_id = models.IntegerField(default=0, verbose_name="reff_id")
    my_business = models.IntegerField(default=0, verbose_name="my_business")
    team_business = models.IntegerField(default=0, verbose_name="team_business")
    leg1_business = models.IntegerField(default=0, verbose_name="leg1_business")
    leg2_business = models.IntegerField(default=0, verbose_name="leg2_business")
    leg3_business = models.IntegerField(default=0, verbose_name="leg3_business")
    rank = models.IntegerField(default=0, verbose_name="rank")

    class Meta:
        verbose_name = "leg_table business"
        db_table = "leg_table"


class LB_deposit(models.Model):
    user = models.CharField(max_length=50,verbose_name="User",blank=True,null=True)
    email = models.CharField(max_length=50,verbose_name="Email",blank=True,null=True)
    Amount_USDT = models.CharField(max_length=50,verbose_name="Amount USDT",blank=True,null=True)
    type = models.CharField(max_length=50,verbose_name="Type",blank=True,null=True)
    create_type = models.CharField(max_length=50,verbose_name="Create Type",blank=True,null=True)
    Amount_JW = models.CharField(max_length=50,verbose_name="Amount JW",blank=True,null=True)
    withdraw_amount = models.CharField(max_length=50,verbose_name="Withdraw Amount",blank=True,null=True)
    Hash = models.CharField(max_length=500,verbose_name="Hash",blank=True,null=True)
    General_Status = (
        (0,'Pending'),
        (1,'Success'),		
	)
    status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)
    

    class Meta:
        verbose_name = 'LB Deposit'
        db_table = 'LB_Rewards'
        
        

class ColorBet(models.Model):
    user = models.IntegerField(default=0, verbose_name="user")
    color = models.CharField(max_length=50,verbose_name="color",blank=True,null=True)
    amount = models.DecimalField(default = 0,max_digits=10,decimal_places=8,verbose_name='amount')
    bet_time = models.DateTimeField(verbose_name="bet_time",default=timezone.now)

    class Meta:
        verbose_name = 'User Bet'
        db_table = 'color_bet'

class GameResult(models.Model):
    winning_color = models.CharField(max_length=50,verbose_name="winning_color",blank=True,null=True)
    game_time = models.DateTimeField(verbose_name="bet_time",default=timezone.now)

    class Meta:
        verbose_name = 'color gameresult'
        db_table = 'color_gameresult'


class Boat_wallet(models.Model):
    user = models.CharField(max_length=50,verbose_name="User",blank=True,null=True)
    email = models.CharField(max_length=50,verbose_name="Email",blank=True,null=True)
    Amount_USDT = models.CharField(max_length=50,verbose_name="Amount USDT",blank=True,null=True)
    type = models.CharField(max_length=50,verbose_name="Type",blank=True,null=True)
    create_type = models.CharField(max_length=50,verbose_name="Create Type",blank=True,null=True)
    Amount_JW = models.CharField(max_length=50,verbose_name="Amount JW",blank=True,null=True)
    Hash = models.CharField(max_length=500,verbose_name="Hash",blank=True,null=True)
    General_Status = (
        (0,'Pending'),
        (1,'Success'),		
	)
    status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)
    paytype = models.CharField(verbose_name="Pay Type",default="",max_length=45)
    

    class Meta:
        verbose_name = 'Boat Wallet Deposit'
        db_table = 'boatwallet'
        
        
class boat_purchase_history(models.Model):
	user_id = models.IntegerField(default=0, verbose_name="user_id")
	purchase_amount = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='plan_purchase_amount')
	user_wallet_type = models.CharField(verbose_name="user_wallet_type",default="",max_length = 200)
	buy_type = models.CharField(verbose_name="Buy Type",default="",max_length=200)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)
	status=models.IntegerField(default=0,verbose_name='status')

	class Meta:
		verbose_name = "Boat Purchase History"
		db_table = "Boatpurchage"


class boat_trade_purchase_history(models.Model):
	user_id = models.IntegerField(default=0, verbose_name="user_id")
	purchase_amount = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='plan_purchase_amount')
	user_wallet_type = models.CharField(verbose_name="user_wallet_type",default="",max_length = 200)
	buy_type = models.CharField(verbose_name="Buy Type",default="",max_length=200)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)
	status=models.IntegerField(default=0,verbose_name='status')

	class Meta:
		verbose_name = "Boat Purchase trade History"
		db_table = "Boattradepurchage"


class Roi_Reward_History(models.Model):
	user = models.ForeignKey(User_Management,on_delete=models.CASCADE,verbose_name='User')
	steps = models.IntegerField(verbose_name="steps",blank=True,null=True)
	Reward = models.DecimalField(max_digits=16,decimal_places=8,verbose_name="Reward Token",blank=True,null=True)
	reward_status = models.CharField(max_length=50,verbose_name="Reward Token",blank=True,null=True,default="step_reward")
	created_on = models.DateTimeField(default=timezone.now)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Roi Reward history"
		db_table = 'boatroihistory'
		indexes = [
			models.Index(fields=['user'])
		]
  
  
class Boat_Referral_reward_History(models.Model):
	user = models.ForeignKey(User_Management,on_delete=models.CASCADE,verbose_name='User',default="")
	referral_id = models.CharField(max_length=50,verbose_name="Referral ID",blank=True,null=True)
	reward = models.CharField(max_length=50,verbose_name="Reward",blank=True,null=True)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Boat Referral Reward History"
		db_table = 'Boat_referral_reward'
		indexes = [
			models.Index(fields=['user'])
		]



class boatroi_percentage(models.Model):
	date = models.CharField(max_length=6)  # Storing '01/Jan', etc.
	reward_percentage = models.DecimalField(max_digits=16,decimal_places=8,verbose_name="Reward Token",blank=True,null=True)

	class Meta:
		verbose_name = "boatroi percentage"
		db_table = "boatroi_percentage"
  
  

class claim_trade_history(models.Model):
	user_id = models.IntegerField(default=0, verbose_name="user_id")
	amount = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='amount')
	user_wallet_type = models.CharField(verbose_name="user_wallet_type",default="",max_length = 200)
	buy_type = models.CharField(verbose_name="Buy Type",default="",max_length=200)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)
	status=models.IntegerField(default=0,verbose_name='status')

	class Meta:
		verbose_name = "claim trade History"
		db_table = "claim_trade"




class Boat_Referral_income_History(models.Model):
	user = models.ForeignKey(User_Management,on_delete=models.CASCADE,verbose_name='User',default="")
	referral_id = models.CharField(max_length=50,verbose_name="Referral ID",blank=True,null=True)
	reward = models.CharField(max_length=50,verbose_name="Reward",blank=True,null=True)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Boat Referral income History"
		db_table = 'Boat_referral_income'
		indexes = [
			models.Index(fields=['user'])
		]




##### mp plan ####



class MPRewardHistory(models.Model):
	user = models.ForeignKey(User_Management,on_delete=models.CASCADE,verbose_name='User',default="")
	referral_id = models.CharField(max_length=50,verbose_name="Referral ID",blank=True,null=True)
	reward = models.CharField(max_length=50,verbose_name="Reward",blank=True,null=True)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "MPReward History"
		db_table = 'MPReward'
		indexes = [
			models.Index(fields=['user'])
		]
  
  
  
class MPDailyRewardHistory(models.Model):
	user = models.ForeignKey(User_Management,on_delete=models.CASCADE,verbose_name='User')
	steps = models.IntegerField(verbose_name="steps",blank=True,null=True)
	Reward = models.DecimalField(max_digits=16,decimal_places=8,verbose_name="Reward Token",blank=True,null=True)
	reward_status = models.CharField(max_length=50,verbose_name="Reward Token",blank=True,null=True,default="step_reward")
	created_on = models.DateTimeField(default=timezone.now)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "MPDailyRewardHistory"
		db_table = 'MPDailyReward'
		indexes = [
			models.Index(fields=['user'])
		]
  


class MPPlanlist(models.Model):
    plan_name = models.CharField(max_length=50, db_column='PlanName')
    plan = models.IntegerField(db_column='Plan')
    fee_usdt = models.DecimalField(max_digits=10, decimal_places=2, db_column='Fee_usdt')
    fee_jw = models.DecimalField(max_digits=10, decimal_places=2, db_column='Fee_jw')
    time_period = models.CharField(max_length=20, db_column='Time_period')
    daily_reward = models.DecimalField(max_digits=10, decimal_places=2, db_column='Dailyreward')
    eligibility_level = models.IntegerField(db_column='Elegibility_level')
    direct_user = models.IntegerField(db_column='Direct_user')
    step = models.IntegerField(db_column='step')
    reward_percentage = models.DecimalField(max_digits=10, decimal_places=6, db_column='reward_percentage')

    class Meta:
        verbose_name = "MPPlanlist"
        db_table = 'MPlanList'  # Match the table name
        
        

## promo bonus

        
class promobonus_history(models.Model):
	user_id = models.IntegerField(default=0, verbose_name="user_id")
	claim_amount = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='claim_amount')
	link = models.CharField(verbose_name="link",default="",max_length = 200)
	email = models.CharField(verbose_name="email",default="",max_length=200)
	content = models.CharField(verbose_name="content",default="",max_length = 200)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)
	status=models.IntegerField(default=0,verbose_name='status')

	class Meta:
		verbose_name = "promobonus History"
		db_table = "Earnrefferbounce"
  
  
class BurnRewardHistory(models.Model):
	user = models.ForeignKey(User_Management,on_delete=models.CASCADE,verbose_name='User',default="")
	referral_id = models.CharField(max_length=50,verbose_name="Referral ID",blank=True,null=True)
	reward = models.CharField(max_length=50,verbose_name="Reward",blank=True,null=True)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "BurnReward History"
		db_table = 'BurnReward'
		indexes = [
			models.Index(fields=['user'])
		]
  
class BurnMonthRewardHistory(models.Model):
	user = models.ForeignKey(User_Management,on_delete=models.CASCADE,verbose_name='User')
	steps = models.IntegerField(verbose_name="steps",blank=True,null=True)
	Reward = models.DecimalField(max_digits=16,decimal_places=8,verbose_name="Reward Token",blank=True,null=True)
	reward_status = models.CharField(max_length=50,verbose_name="Reward Token",blank=True,null=True,default="step_reward")
	created_on = models.DateTimeField(default=timezone.now)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "BurnMonthRewardHistory"
		db_table = 'BurnMonthReward'
		indexes = [
			models.Index(fields=['user'])
		]
  

class BurnWithdraw(models.Model):
	userid = models.ForeignKey(User_Management,related_name ='BurnWithdraw',on_delete=models.CASCADE,verbose_name='User')
	Amount = models.CharField(max_length=50,verbose_name='USDT Amount',blank=True,null=True)
	Withdraw_fee = models.CharField(max_length=50,verbose_name='Withdraw Fee',blank=True,null=True)
	Month_stake = models.CharField(max_length=50,verbose_name='Month Stake',blank=True,null=True)
	user_request_amt = models.CharField(max_length=500,verbose_name='User Request Amount',blank=True,null=True)
	back_up_phrase = models.CharField(max_length=500,verbose_name='Month Stake',blank=True,null=True)
	Withdraw_USDT = models.CharField(max_length=50,verbose_name='Withdraw USDT Amount',blank=True,null=True)
	Withdraw_JW = models.CharField(max_length=50,verbose_name='Withdraw JW Amount',blank=True,null=True)
	Address = models.CharField(max_length=50,verbose_name='Address',blank=True,null=True)
	Two_Fa = models.IntegerField(verbose_name="Two FA OTP",blank=True,null=True)
	Transaction_Hash = models.CharField(max_length=200,verbose_name='Transaction Hash',blank=True,null=True,default="")
	Wallet_type = models.CharField(max_length=200,verbose_name='Wallet type',blank=True,null=True,default="")
	status =models.IntegerField(choices=Withdraw_Status,default=0,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "burn Withdraw Request"
		db_table = 'burnwithdraw'
		indexes = [
			models.Index(fields=['userid'])
		]
  
  
class swap_receivehistory(models.Model):
	userid = models.ForeignKey(User_Management,related_name ='swap_receive',on_delete=models.CASCADE,verbose_name='User')
	Amount = models.CharField(max_length=50,verbose_name='USDT Amount',blank=True,null=True)
	Withdraw_fee = models.CharField(max_length=50,verbose_name='Withdraw Fee',blank=True,null=True)
	Withdraw_USDT = models.CharField(max_length=50,verbose_name='Withdraw USDT Amount',blank=True,null=True)
	Withdraw_JWC = models.CharField(max_length=50,verbose_name='Withdraw JWC Amount',blank=True,null=True)
	Address = models.CharField(max_length=50,verbose_name='Address',blank=True,null=True)
	Transaction_Hash = models.CharField(max_length=200,verbose_name='Transaction Hash',blank=True,null=True,default="")
	status =models.IntegerField(choices=Withdraw_Status,default=0,verbose_name='Status')
	type = models.CharField(max_length=200,verbose_name='type',blank=True,null=True,default="")
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)
	

	class Meta:
		verbose_name = "swap_receivehistory"
		db_table = 'swap_receive'
		indexes = [
			models.Index(fields=['userid'])
		]
  
class swap_sendhistory(models.Model):
	userid = models.ForeignKey(User_Management,related_name ='swap_send',on_delete=models.CASCADE,verbose_name='User')
	Amount = models.CharField(max_length=50,verbose_name='USDT Amount',blank=True,null=True)
	Withdraw_fee = models.CharField(max_length=50,verbose_name='Withdraw Fee',blank=True,null=True)
	Withdraw_USDT = models.CharField(max_length=50,verbose_name='Withdraw USDT Amount',blank=True,null=True)
	Withdraw_JWC = models.CharField(max_length=50,verbose_name='Withdraw JWC Amount',blank=True,null=True)
	Address = models.CharField(max_length=50,verbose_name='Address',blank=True,null=True)
	Transaction_Hash = models.CharField(max_length=200,verbose_name='Transaction Hash',blank=True,null=True,default="")
	Transaction_Hash_recieved = models.CharField(max_length=200,verbose_name='Transaction recieve Hash',blank=True,null=True,default="")
	status =models.IntegerField(choices=Withdraw_Status,default=0,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "swap_sendhistory"
		db_table = 'swap_send'
		indexes = [
			models.Index(fields=['userid'])
		]



class CBurnRewardHistory(models.Model):
	user = models.ForeignKey(User_Management,on_delete=models.CASCADE,verbose_name='User',default="")
	referral_id = models.CharField(max_length=50,verbose_name="Referral ID",blank=True,null=True)
	reward = models.CharField(max_length=50,verbose_name="Reward",blank=True,null=True)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "CBurnReward History"
		db_table = 'CBurnReward'
		indexes = [
			models.Index(fields=['user'])
		]
  
class CBurnMonthRewardHistory(models.Model):
	user = models.ForeignKey(User_Management,on_delete=models.CASCADE,verbose_name='User')
	steps = models.IntegerField(verbose_name="steps",blank=True,null=True)
	Reward = models.DecimalField(max_digits=16,decimal_places=8,verbose_name="Reward Token",blank=True,null=True)
	reward_status = models.CharField(max_length=50,verbose_name="Reward Token",blank=True,null=True,default="step_reward")
	created_on = models.DateTimeField(default=timezone.now)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "CBurnMonthRewardHistory"
		db_table = 'CBurnMonthReward'
		indexes = [
			models.Index(fields=['user'])
		]
  
  
  

class Burnrayality_Deposit(models.Model):
    user = models.CharField(max_length=50,verbose_name="User",blank=True,null=True)
    email = models.CharField(max_length=50,verbose_name="Email",blank=True,null=True)
    Amount_USDT = models.CharField(max_length=50,verbose_name="Amount USDT",blank=True,null=True)
    type = models.CharField(max_length=50,verbose_name="Type",blank=True,null=True)
    create_type = models.CharField(max_length=50,verbose_name="Create Type",blank=True,null=True)
    Amount_JW = models.CharField(max_length=50,verbose_name="Amount JW",blank=True,null=True)
    withdraw_amount = models.CharField(max_length=50,verbose_name="Withdraw Amount",blank=True,null=True)
    Hash = models.CharField(max_length=500,verbose_name="Hash",blank=True,null=True)
    General_Status = (
        (0,'Pending'),
        (1,'Success'),		
	)
    status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)
    

    class Meta:
        verbose_name = 'Royality Deposit'
        db_table = 'Burnrayality_Rewards'