

from django.utils.timezone import now
from django.db import models

from django.conf import settings

from django.contrib.auth.models import User,Group

from auditable.models import Auditable

from datetime import date

from django.core.validators import RegexValidator
import uuid
import os

from django.urls import reverse
import os
from django.db.models import Q
from django.db.models import Count, Min, Sum, Avg ,F,DecimalField
from decimal import Decimal
import time

from locations.models import Country,State,Cities

from django.utils import timezone

General_Status = (
					(0,'Active'),
					(1,'Inactive'),
	)

General_Status = (
					(0,'Active'),
					(1,'Inactive'),					
	)

User_Role = (
		(0,'Admin'),
		(1,'SubAdmin'),
		(2,'Tradeusers')
	)
User_Status =(
		(0,'Active'),
		(1,'Inactive'),
		(2,'Deactive'),
	)

Gender = (

	(0,'Male'),
	(1,'Female'),
	)

Pattern_Status =(
  (0,'Not Updated'),
  (1,'Updated'),
  
 )

REFERRAL_Status =(
		(0,'Inactive'),
		(1,'Active'),
	)

class AdminUser_Profile(models.Model):
	user = models.OneToOneField(User,related_name ='admin_user_profile',on_delete=models.CASCADE)
	gender = models.IntegerField(choices=Gender,verbose_name='Gender',blank=True,null=True)
	date_of_birth = models.DateField(help_text='Date of Birth in mm/dd/yyyy Format',blank=True,null=True)
	emailaddress = models.CharField(max_length=100,verbose_name="Email Address",blank=True,null=True)
	address1 = models.CharField(max_length=100,verbose_name='Contact Address1')
	address2 = models.CharField(max_length=100,verbose_name='Contact Address2',blank=True,null=True)
	city = models.CharField(max_length=30,verbose_name='City',blank=True,null=True)
	state = models.CharField(max_length=50,verbose_name='State',blank=True,null=True)
	country = models.ForeignKey(Country,related_name ='admin_user_country',on_delete=models.CASCADE,verbose_name='Country',blank=True,null=True)
	agree = models.BooleanField(default=False)
	postcode = models.CharField(max_length=10,verbose_name='Pin Code',blank=True,null=True)
	phone1 = models.CharField(max_length=13,verbose_name='Phone Number',blank=True,null=True)
	photo = models.ImageField(upload_to='jsanwellness/',verbose_name='Profile Picture',blank=True,null=True)
	role = models.IntegerField(choices=User_Role,default=0,verbose_name='Role')
	pattern_code = models.IntegerField(verbose_name='Pattern Code',default=0)
	country_code = models.CharField(max_length=10,verbose_name='Country Code',blank=True,null=True)
	twofa = models.BooleanField(default=False)
	google_id = models.CharField(max_length=50,verbose_name='Google Id',blank=True,null=True)
	status = models.IntegerField(choices=User_Status,default=0,verbose_name = 'Status')
	pattern_status=models.IntegerField(choices=Pattern_Status,default=1,verbose_name = 'Pattern Status')
	def __str__(self):
		return "%s's profile" % self.user
	@property
	def image_name(self):
		return  os.path.basename(self.photo.path) if self.photo else ''
	
	class Meta:
		db_table='AYLkV0WRrgK0R9qM'
		verbose_name = "Admin Profile"
		verbose_name_plural ="Admin Profile's"
		indexes = [
		models.Index(fields=['gender','twofa','status'])

		]


class AdminUser_Activity(Auditable):
	user = models.ForeignKey(User,related_name ='admin_user_activity',on_delete=models.CASCADE)
	ip_address = models.GenericIPAddressField()
	activity=models.CharField(max_length=50,verbose_name='Activity',blank=True,null=True)
	browsername = models.CharField(max_length=50,verbose_name='Browser Name',blank=True,null=True)
	os=models.CharField(max_length=50,verbose_name='Operating System',blank=True,null=True)
	devices=models.CharField(max_length=50,verbose_name='Devices',blank=True,null=True)

	def __int__self(self):
		return id

	class Meta:
		verbose_name='AdminUser Activity'
		db_table = 'AWxn5AxwlScnvVij'


class AccessAttempt(models.Model):
	user = models.ForeignKey(User,related_name ='accessattempt',on_delete=models.CASCADE,blank=True,null=True)
	emailaddress = models.CharField(max_length=50,verbose_name='Email Address',blank=True,null=True)
	ip_address = models.GenericIPAddressField()
	activity=models.CharField(max_length=50,verbose_name='Activity',blank=True,null=True)
	browsername = models.CharField(max_length=50,verbose_name='Browser Name',blank=True,null=True)
	os=models.CharField(max_length=50,verbose_name='Operating System',blank=True,null=True)
	devices=models.CharField(max_length=50,verbose_name='Devices',blank=True,null=True)
	datetime = models.DateTimeField(default=timezone.now,verbose_name="DateTime")
	failedcount = models.IntegerField(verbose_name="Failed Logins")

	class Meta:
		verbose_name = "Access Attempt"
		db_table='AVyjW0gtKU25eYSY'
		indexes = [
		models.Index(fields=['user','failedcount','ip_address','datetime'])

		]

class Steps_Management(Auditable):
	maxi_step =  models.IntegerField(verbose_name="Maximum Step Per Day",blank=True,null=True)
	step_value = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Per Step Coin Value',default=0.00000000)
	free_plan_days = models.IntegerField(verbose_name="Free Plan Days",blank=True,null=True,default = 0)
	Step_counter_Discount = models.IntegerField(verbose_name="Step counter (Add Step %)",blank=True,null=True,default = 0)
	Step_discount = models.IntegerField(verbose_name="Google fit (Discount Step %)",blank=True,null=True)
	plan_active_status = models.IntegerField(verbose_name="plan active status",blank = True,null = True)
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
	isAdminEnablePayLater=models.IntegerField(choices=General_Status,default=0,verbose_name='isAdminEnablePayLater')
	isStakeEnable=models.IntegerField(choices=General_Status,default=0,verbose_name='isStakeEnable')
	isAdminEnablePremiumDeposit=models.IntegerField(choices=General_Status,default=0,verbose_name='isAdminEnablePremiumDeposit')
	isPremiumEnable=models.IntegerField(choices=General_Status,default=0,verbose_name='isPremiumEnable')
	isAdminEnableRrWithdraw=models.IntegerField(choices=General_Status,default=0,verbose_name='isAdminEnableRrWithdraw')
	isAdminEnableHrWithdraw=models.IntegerField(choices=General_Status,default=0,verbose_name='isAdminEnableHrWithdraw')
	
	class Meta:
		verbose_name = "Steps Management"
		db_table='STEPW0gtKU25eYSY'
		indexes = [
		models.Index(fields=['maxi_step','step_value','status'])

		]




# class Steps_Management(Auditable):
# 	maxi_step =  models.IntegerField(verbose_name="Maximum Step Per Day",blank=True,null=True)
# 	step_value = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Per Step Coin Value',default=0.00000000)
# 	free_plan_days = models.IntegerField(verbose_name="Free Plan Days",blank=True,null=True,default = 0)
# 	Step_counter_Discount = models.IntegerField(verbose_name="Step counter (Add Step %)",blank=True,null=True,default = 0)
# 	Step_discount = models.IntegerField(verbose_name="Google fit (Discount Step %)",blank=True,null=True)
# 	plan_active_status = models.IntegerField(verbose_name="plan active status",blank = True,null = True)
# 	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
#  	isAdminEnablePayLater=models.IntegerField(choices=General_Status,default=0,verbose_name='isAdminEnablePayLater')
# 	isStakeEnable=models.IntegerField(choices=General_Status,default=0,verbose_name='isStakeEnable')
# 	isAdminEnablePremiumDeposit=models.IntegerField(choices=General_Status,default=0,verbose_name='isAdminEnablePremiumDeposit')
# 	isPremiumEnable=models.IntegerField(choices=General_Status,default=0,verbose_name='isPremiumEnable')

# 	class Meta:
# 		verbose_name = "Steps Management"
# 		db_table='STEPW0gtKU25eYSY'
# 		indexes = [
# 		models.Index(fields=['maxi_step','step_value','status'])

# 		]

class Two_x_boost(Auditable):
	daily_min = models.IntegerField(verbose_name="Daily Minutes",blank=True,null=True)
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')

	class Meta:
		verbose_name = "Two X Boost"
		db_table='BOOW0gtKU25eYST'
		indexes = [
		models.Index(fields=['daily_min','status'])

		]

class User_Management(models.Model):
	user  =  models.CharField(max_length=50,verbose_name='Name',blank=True,null=True)
	user_name = models.CharField(max_length=50,verbose_name='User Name',blank=True,null=True)
	Email =  models.CharField(max_length=100,verbose_name="User Email Address",blank=True,null=True)
	Name = models.CharField(max_length=50,verbose_name='Name',blank=True,null=True)
	notes=models.TextField(max_length=1000,verbose_name='Notes',blank=True,null=True)
	fixed_status=models.CharField(max_length=100,verbose_name='Fixed Status',blank=True,null=True)
	phone_number = models.CharField(max_length=13,verbose_name='App Version',blank=True,null=True)
	user_phone_number = models.CharField(max_length=200,verbose_name='Phone Number',blank=True,null=True)
	user_profile_pic = models.CharField(max_length=200,verbose_name='Phone Type',blank=True,null=True)
	user_profile = models.CharField(max_length=400,verbose_name='user profile',blank=True,null=True,default="")
	over_all_stepcount = models.IntegerField(verbose_name="User Over All Step Count ",blank=True,null=True,default=0)
	referal_code = models.CharField(max_length=50,verbose_name="referral Code",blank=True,null=True,default ="")
	reff_id = models.CharField(max_length=50,verbose_name="referral Id",blank=True,null=True,default ="")
	User_Device_id = models.CharField(max_length=500,verbose_name="User Device id",blank=True,null=True,default ="")
	device_unique_id = models.CharField(max_length=200,verbose_name="Device Unique id",blank=True,null=True,default ="")
	request_device_id = models.CharField(max_length=500,verbose_name="Request Device id",blank=True,null=True,default ="")
	build_type=models.CharField(max_length=40,verbose_name="Bulid Type",blank=True,null=True,default ="")
	status=models.IntegerField(choices=User_Status,default=1,verbose_name='Status')
	User_type = models.CharField(max_length=200,verbose_name="User Type",blank=True,null=True,default ="")
	User_Verification_Status = models.CharField(max_length=200,verbose_name="User Verification Status",blank=True,null=True,default ="")
	Activate_Status = models.CharField(max_length=200,verbose_name="User Activate Status",blank=True,null=True,default ="0")
	User_Target =  models.CharField(max_length=200,verbose_name="User Target",blank=True,null=True,default ="5000")
	plan = models.IntegerField(verbose_name="Current Plan",blank=True,null=True,default=0)
	plan_start_date=models.DateTimeField(default=timezone.now,verbose_name='plan Start Date')
	plan_end_date=models.DateTimeField(default=timezone.now,verbose_name='plan End Date')
	referral_plan_status = models.IntegerField(choices=REFERRAL_Status,default=0,verbose_name='referral_plan_status')
	Referral_id = models.CharField(verbose_name="Referral id",default="",max_length = 50)
	Referral_Level = models.IntegerField(verbose_name = "Under Level",default=0)
	Direct_referral_id = models.CharField(verbose_name = "Red User",default="",max_length = 50,)
	Direct_referral_user_level = models.IntegerField(verbose_name="Direct Referral User Level",default=0)
	user_referral_eligible_level = models.IntegerField(verbose_name="User Referral Eligible Level",default=0)
	withdraw_count = models.IntegerField(verbose_name = "withdraw_count",default=2)
	withdraw_status = models.IntegerField(verbose_name="withdraw status",default=0)
	Two_X_Boost_status = models.IntegerField(verbose_name="Two X Boost status",default=1)
	plan_validation = models.CharField(max_length = 100,verbose_name = "Plan_Validation",default = "")
	Health_Withdraw_min_value =  models.DecimalField(max_digits=16,decimal_places=8,verbose_name="Health Withdraw min value",blank=True,null=True)
	Health_Withdraw_max_value =  models.DecimalField(max_digits=16,decimal_places=8,verbose_name="Health Withdraw max value",blank=True,null=True)
	Referral_Withdraw_min_value =  models.DecimalField(max_digits=16,decimal_places=8,verbose_name="Referral Withdraw min value",blank=True,null=True)
	Referral_Withdraw_max_value =  models.DecimalField(max_digits=16,decimal_places=8,verbose_name="Referral Withdraw max value",blank=True,null=True)
	reward_steps = models.IntegerField(verbose_name="reward_steps",default=0)
	reward_step_amount = models.DecimalField(max_digits=16,decimal_places=8,verbose_name="reward_step_amount",blank=True,null=True)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now = True)
	user_info = models.CharField(max_length=50,verbose_name="User_info",blank=True,null=True)
	team_business = models.IntegerField(default=0, verbose_name="team_business")
	leg1_business = models.IntegerField(default=0, verbose_name="leg1_business")
	leg2_business = models.IntegerField(default=0, verbose_name="leg2_business")
	leg3_business = models.IntegerField(default=0, verbose_name="leg3_business")
	rank = models.IntegerField(default=0, verbose_name="rank")
	my_business = models.IntegerField(default=0, verbose_name="my_business")
	pastleg1_business = models.IntegerField(default=0, verbose_name="pastleg1_business")
	pastleg2_business = models.IntegerField(default=0, verbose_name="pastleg2_business")
	pastleg3_business = models.IntegerField(default=0, verbose_name="pastleg3_business")
	# rewards_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	# last_reward_dates = models.CharField(max_length=100,verbose_name="last_reward_dates",blank=True,null=True)  # To track last reward dates for each rank
	# rewards_weeks_released = models.CharField(max_length=100,verbose_name="rewards_weeks_released",blank=True,null=True)
	rewards_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	last_reward_dates = models.CharField(max_length=500, blank=True, null=True)  # To track last reward dates for each rank
	rewards_weeks_released = models.CharField(max_length=500, blank=True, null=True)	
	USDT_status=models.IntegerField(verbose_name='USDT_status',default=0)	
	plan_rewards_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	plan_rewards_released = models.CharField(max_length=500, blank=True, null=True)	
	boat_status=models.IntegerField(verbose_name='boat_status',default=1)
	Newstake_wallet = models.IntegerField(default=0, verbose_name="Newstake_wallet")
	USER_INRID = models.CharField(max_length=50,verbose_name='USER INRID',blank=True,null=True)
	PlanBwa = models.IntegerField(default=0, verbose_name="PlanBwa")
	TradeBwa = models.IntegerField(default=0, verbose_name="TradeBwa")
	StakeBwa = models.IntegerField(default=0, verbose_name="StakeBwa")
	transferpw = models.IntegerField(default=0, verbose_name="transferpw")
	xvalue = models.IntegerField(default=3, verbose_name="xvalue")
	MPlan = models.IntegerField(verbose_name="MPlan Plan",blank=True,null=True,default=0)
	MPminwithdraw = models.IntegerField(verbose_name="MPminwithdraw",blank=True,null=True,default=0)
	MPmaxwithdraw = models.IntegerField(verbose_name="MPmaxwithdraw",blank=True,null=True,default=0)
	Mpuserelegilelevl = models.IntegerField(verbose_name="Mpuserelegilelevl",blank=True,null=True,default=0)
	Mpdailyreward = models.DecimalField(max_digits=10, decimal_places=2)
	MPlanBWA = models.IntegerField(default=0, verbose_name="MPlanBWA")
	Mpuserleg1 = models.IntegerField(verbose_name="Mpuserleg1",blank=True,null=True,default=0)
	Mpuserlegall = models.IntegerField(verbose_name="Mpuserlegall",blank=True,null=True,default=0)
	Mplan_start_date = models.DateTimeField(default=now,verbose_name='Mplan Start Date')
	MPlanTWA = models.IntegerField(default=0, verbose_name="MPlanTWA")
	BNBStatus=models.IntegerField(verbose_name='BNBStatus',default=0)
	Burnamount = models.IntegerField(default=0, verbose_name="Burnamount")
	Burnelegibility = models.IntegerField(verbose_name="Burnelegibility",blank=True,null=True,default=0)
	Burnamountjwc = models.IntegerField(default=0, verbose_name="Burnamountjwc")
	Burnelegibilityjwc = models.IntegerField(verbose_name="Burnelegibilityjwc",blank=True,null=True,default=0)
	burnamountafter20may = models.IntegerField(default=0, verbose_name="burnamountafter20may")
	burn_rewards_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	burn_rewards_released = models.CharField(max_length=500, blank=True, null=True)
	rewards_month_released = models.CharField(max_length=500, blank=True, null=True)
	burnteamamonthafter20may = models.IntegerField(default=0, verbose_name="burnteamamonthafter20may")

	def __str__(self):
		return "%s" % self.Name

	class Meta:
		verbose_name = "User Management"
		db_table='USPzTPzfNdmGTlER'
		indexes = [
		models.Index(fields=['user','user_name','Email','status'])

		]

class Steps_history(models.Model):
	user = models.ForeignKey(User_Management,related_name ='Steps_history',on_delete=models.CASCADE,blank=True,null=True)
	steps = models.IntegerField(verbose_name="User Steps",blank=True,null=True)
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
	reward_Status = models.IntegerField(verbose_name="Reward Status",default=0)
	Step_type = models.CharField(max_length = 100,verbose_name = "Step_type",default = "")
	created_on = models.DateTimeField(default=timezone.now)
	modified_on = models.DateTimeField(default=timezone.now)

	class Meta:
		verbose_name = "Steps History"
		db_table='STPzTPzfNdmGTlEP'
		indexes = [
		models.Index(fields=['user','steps','status'])

		]

class Registration_otp(models.Model):
	user = models.ForeignKey(User_Management,related_name ='registration_otp',on_delete=models.CASCADE,blank=True,null=True)
	email_otp = models.IntegerField(verbose_name="Email Registration OTP",blank=True,null=True)
	phone_number_opt = models.IntegerField(verbose_name="Phone Number Registration OTP",blank=True,null=True)
	status=models.IntegerField(choices=General_Status,default=1,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Registration OTP"
		db_table='OTPzTPzfNdmGTlER'
		indexes = [
		models.Index(fields=['user','status'])

		]

class User_two_fa(models.Model):
	user = models.OneToOneField(User_Management, on_delete=models.CASCADE,blank=True,null=True)
	user_secrete_key=models.CharField(max_length=128,blank=True,null=True)
	user_totp=models.CharField(max_length=128,blank=True,null=True)
	TWO_FA__STATUS = (('enable', 'enable'), ('disable', 'disable'))
	user_status = models.CharField(choices=TWO_FA__STATUS,max_length=200,default='disable')
	user_htotp=models.CharField(max_length=128,blank=True,null=True)
    
	class Meta:
		verbose_name ='User Two Fa'
		db_table='FAKJDFGHKDFH'


class PlanDateUpdateHistory(models.Model):
	user = models.CharField(max_length=100,blank=True,null=True,verbose_name="User name")
	email = models.CharField(max_length=100,blank=True,null=True,verbose_name="User email")
	plan_name = models.CharField(max_length=100,blank=True,null=True,verbose_name="Plan name")
	planstart_date = models.CharField(max_length=100,blank=True,null=True,verbose_name="Plan start Date")
	planend_date = models.CharField(max_length=100,blank=True,null=True,verbose_name="Plan End Date")
	plan_updated_end_date = models.CharField(max_length=100,blank=True,null=True,verbose_name="Plan Updated End Date")
	created_on = models.DateTimeField(auto_now_add=True)


	class Meta:
		verbose_name ='PlanDateUpdateHistory'
		db_table='HJdLcHNlnKz0'

SEND_STATUS = (
	(0,'Active'),
	(1,'Completed'),
	(2,'Cancelled'),
	(3,'Pending')
)


class WithdrawSendHistory(models.Model):
	user = models.CharField(max_length=100,blank=True,null=True,verbose_name="Username")
	email = models.ForeignKey(User_Management,related_name ='email',verbose_name="Email",on_delete=models.CASCADE,blank=True,null=True)
	claim_amount = models.CharField(max_length=100,blank=True,null=True,verbose_name="Claim Amount")
	from_address = models.CharField(max_length=50,verbose_name='From Address',blank=True,null=True)
	to_address = models.CharField(max_length=50,verbose_name='To Address',blank=True,null=True)
	Transaction_Hash = models.CharField(max_length=200,verbose_name='TransactionHash',blank=True,null=True,default="")
	send_status =models.IntegerField(choices=SEND_STATUS,default=3,verbose_name='Send Status')
	currency = models.CharField(max_length=50,verbose_name='Currency',blank=True,null=True)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)


	class Meta:
		verbose_name ='WithdrawSendHistory'
		db_table='VVGrKxGkFL8yghB'


class front_page_management(models.Model):
	Front_user_count = models.IntegerField(default = 0,blank=True,null=True,verbose_name="Front Page User Count")
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status') 
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name ='frontpagemanagement'
		db_table='FRONKxGkFL8yMAN'


class WithdrawSendUSDTHistory(models.Model):
	user = models.CharField(max_length=100,blank=True,null=True,verbose_name="Username")
	email = models.ForeignKey(User_Management,related_name ='useremail',verbose_name="Email",on_delete=models.CASCADE,blank=True,null=True)
	claim_amount = models.CharField(max_length=100,blank=True,null=True,verbose_name="Claim Amount")
	type = models.CharField(max_length=100,blank=True,null=True,verbose_name="Type")
	from_address = models.CharField(max_length=50,verbose_name='From Address',blank=True,null=True)
	to_address = models.CharField(max_length=50,verbose_name='To Address',blank=True,null=True)
	Transaction_Hash = models.CharField(max_length=200,verbose_name='TransactionHash',blank=True,null=True,default="")
	send_status =models.IntegerField(choices=SEND_STATUS,default=3,verbose_name='Send Status')
	currency = models.CharField(max_length=50,verbose_name='Currency',blank=True,null=True)
	plan_start_date=models.DateTimeField(default=timezone.now,verbose_name='plan Start Date')
	plan_end_date=models.DateTimeField(default=timezone.now,verbose_name='plan End Date')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)


	class Meta:
		verbose_name ='WithdrawSendUSDTHistory'
		db_table='USDWzWkaJsitsYeR'
  
  
class WithdrawSendUSDTHistoryboat(models.Model):
	user = models.CharField(max_length=100,blank=True,null=True,verbose_name="Username")
	email = models.ForeignKey(User_Management,verbose_name="Email",on_delete=models.CASCADE,blank=True,null=True)
	claim_amount = models.CharField(max_length=100,blank=True,null=True,verbose_name="Claim Amount")
	type = models.CharField(max_length=100,blank=True,null=True,verbose_name="Type")
	from_address = models.CharField(max_length=50,verbose_name='From Address',blank=True,null=True)
	to_address = models.CharField(max_length=50,verbose_name='To Address',blank=True,null=True)
	Transaction_Hash = models.CharField(max_length=200,verbose_name='TransactionHash',blank=True,null=True,default="")
	send_status =models.IntegerField(choices=SEND_STATUS,default=3,verbose_name='Send Status')
	currency = models.CharField(max_length=50,verbose_name='Currency',blank=True,null=True)
	plan_start_date=models.DateTimeField(default=timezone.now,verbose_name='plan Start Date')
	plan_end_date=models.DateTimeField(default=timezone.now,verbose_name='plan End Date')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)


	class Meta:
		verbose_name ='WithdrawSendUSDTHistoryboat'
		db_table='BOAT_supportusdt'
  
  

###### mp plan  


class MPfeeHistory(models.Model):
	user = models.CharField(max_length=100,blank=True,null=True,verbose_name="Username")
	email = models.ForeignKey(User_Management,verbose_name="Email",on_delete=models.CASCADE,blank=True,null=True)
	claim_amount = models.CharField(max_length=100,blank=True,null=True,verbose_name="Claim Amount")
	type = models.CharField(max_length=100,blank=True,null=True,verbose_name="Type")
	from_address = models.CharField(max_length=50,verbose_name='From Address',blank=True,null=True)
	to_address = models.CharField(max_length=50,verbose_name='To Address',blank=True,null=True)
	Transaction_Hash = models.CharField(max_length=200,verbose_name='TransactionHash',blank=True,null=True,default="")
	send_status =models.IntegerField(choices=SEND_STATUS,default=3,verbose_name='Send Status')
	currency = models.CharField(max_length=50,verbose_name='Currency',blank=True,null=True)
	plan_start_date=models.DateTimeField(default=timezone.now,verbose_name='plan Start Date')
	plan_end_date=models.DateTimeField(default=timezone.now,verbose_name='plan End Date')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)


	class Meta:
		verbose_name ='MPfeeHistory'
		db_table='MPSubFee'
  
  
class MPPLanHistory(models.Model):
	user = models.CharField(max_length=100,blank=True,null=True,verbose_name="Username")
	email = models.ForeignKey(User_Management,verbose_name="Email",on_delete=models.CASCADE,blank=True,null=True)
	plan_amount = models.CharField(max_length=100,blank=True,null=True,verbose_name="Claim Amount")
	type = models.CharField(max_length=100,blank=True,null=True,verbose_name="Type")
	from_address = models.CharField(max_length=50,verbose_name='From Address',blank=True,null=True)
	to_address = models.CharField(max_length=50,verbose_name='To Address',blank=True,null=True)
	Transaction_Hash = models.CharField(max_length=200,verbose_name='TransactionHash',blank=True,null=True,default="")
	send_status =models.IntegerField(choices=SEND_STATUS,default=3,verbose_name='Send Status')
	currency = models.CharField(max_length=50,verbose_name='Currency',blank=True,null=True)
	plan_start_date=models.DateTimeField(default=timezone.now,verbose_name='plan Start Date')
	plan_end_date=models.DateTimeField(default=timezone.now,verbose_name='plan End Date')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)


	class Meta:
		verbose_name ='MPPLanHistory'
		db_table='MPPlan'
  
  
  
class BurntoearnHistory(models.Model):
	user = models.CharField(max_length=100,blank=True,null=True,verbose_name="Username")
	email = models.ForeignKey(User_Management,verbose_name="Email",on_delete=models.CASCADE,blank=True,null=True)
	plan_amount = models.CharField(max_length=100,blank=True,null=True,verbose_name="Claim Amount")
	type = models.CharField(max_length=100,blank=True,null=True,verbose_name="Type")
	from_address = models.CharField(max_length=50,verbose_name='From Address',blank=True,null=True)
	to_address = models.CharField(max_length=50,verbose_name='To Address',blank=True,null=True)
	Transaction_Hash = models.CharField(max_length=200,verbose_name='TransactionHash',blank=True,null=True,default="")
	send_status =models.IntegerField(choices=SEND_STATUS,default=3,verbose_name='Send Status')
	currency = models.CharField(max_length=50,verbose_name='Currency',blank=True,null=True)
	plan_start_date=models.DateTimeField(default=timezone.now,verbose_name='plan Start Date')
	plan_end_date=models.DateTimeField(default=timezone.now,verbose_name='plan End Date')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)


	class Meta:
		verbose_name ='BurntoearnHistory'
		db_table='BurnToEarn'
  
  
class CBurntoearnHistory(models.Model):
	user = models.CharField(max_length=100,blank=True,null=True,verbose_name="Username")
	email = models.ForeignKey(User_Management,verbose_name="Email",on_delete=models.CASCADE,blank=True,null=True)
	plan_amount = models.CharField(max_length=100,blank=True,null=True,verbose_name="Claim Amount")
	type = models.CharField(max_length=100,blank=True,null=True,verbose_name="Type")
	from_address = models.CharField(max_length=50,verbose_name='From Address',blank=True,null=True)
	to_address = models.CharField(max_length=50,verbose_name='To Address',blank=True,null=True)
	Transaction_Hash = models.CharField(max_length=200,verbose_name='TransactionHash',blank=True,null=True,default="")
	send_status =models.IntegerField(choices=SEND_STATUS,default=3,verbose_name='Send Status')
	currency = models.CharField(max_length=50,verbose_name='Currency',blank=True,null=True)
	plan_start_date=models.DateTimeField(default=timezone.now,verbose_name='plan Start Date')
	plan_end_date=models.DateTimeField(default=timezone.now,verbose_name='plan End Date')
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)


	class Meta:
		verbose_name ='CBurntoearnHistory'
		db_table='CBurnToEarn'