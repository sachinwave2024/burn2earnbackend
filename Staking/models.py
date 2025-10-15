from tabnanny import verbose
from xml.parsers.expat import model
from django.db import models
from trade_admin_auth.models import User_Management
from django.utils import timezone



class stake_wallet_management(models.Model):
    user = models.CharField(max_length=50,verbose_name="User",blank=True,null=True)
    email = models.CharField(max_length=50,verbose_name="Email",blank=True,null=True)
    stake_Wallet = models.CharField(max_length=50,verbose_name="Stake Wallet",blank=True,null=True)
    stake_withdraw_Wallet = models.CharField(max_length=50,verbose_name="Stake Withdraw Wallet",blank=True,null=True)
    stake_Refferal_Wallet = models.CharField(max_length=50,verbose_name="Stake Refferal Wallet",blank=True,null=True)
    stake_credit_withdraw_Wallet = models.CharField(max_length=50,verbose_name="Stake Credit Withdraw Wallet",blank=True,null=True)
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)
    newstakewallet = models.CharField(max_length=50,verbose_name="newstakewallet",blank=True,null=True)
    newstakereff = models.CharField(max_length=50,verbose_name="Stake newstakereff ",blank=True,null=True)
    newstakewithdraw = models.CharField(max_length=50,verbose_name="newstakewithdraw",blank=True,null=True)
    
    class Meta:
        verbose_name='Staking_Wallet_Management'
        db_table='7qWVxWgylCRXqUdz'
        indexes = [
			models.Index(fields=['user'])
		]



class staking_admin_management(models.Model):
    stake_period = models.IntegerField(blank=True,verbose_name="Stake Period")
    reward_percent = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Reward Percent",blank=True,null=True)
    General_Status = (
        (0,'Active'),
        (1,'Inactive'),		
	)
    status=models.IntegerField(choices=General_Status,default=0,verbose_name='Stake Status')
    minimum_stake = models.DecimalField(max_digits=36,decimal_places=8,verbose_name="Min Stake Amount",blank= True,null= True)
    maximum_stake = models.DecimalField(max_digits=36,decimal_places=8,verbose_name="Max Stake Amount",blank= True,null= True)
    minimum_withdraw = models.DecimalField(max_digits=36,decimal_places=8,verbose_name="Min Withdraw Amount",blank= True,null= True)
    maximum_withdraw = models.DecimalField(max_digits=36,decimal_places=8,verbose_name="Max Withdraw Amount",blank= True,null= True)
    minimum_withdraw_referal = models.DecimalField(max_digits=36,decimal_places=8,verbose_name="Min Withdraw Amount (Referral Wallet)",blank= True,null= True)
    maximum_withdraw_referal = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Max Withdraw Amount (Referral Wallet)",blank= True,null= True)
    Referral_Status = (
        (0,'Active'),
        (1,'Inactive'),		
	)
    referral_status = models.IntegerField(choices=Referral_Status,default=0,verbose_name='Referral Status')
    referral_level = models.IntegerField(blank=True,null= True,verbose_name="Maximum Referral Eligible Level")
    Withdraw_Status = (
        (0,'Active'),
        (1,'Inactive'),		
	)
    withdraw_status = models.IntegerField(choices=Withdraw_Status,default=0,verbose_name='Withdraw Status')
    stake_withdraw_transaction_fee = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Withdraw Fee",blank=True,null=True)
    eligible_plan = models.IntegerField(default=0,verbose_name='Stake Eligible Plan')
    stake_wallet_percentage = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Stake wallet claim(%)",blank=True,null=True)
    withdraw_wallet_percentage = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Withdraw Wallet claim(%)",blank=True,null=True)
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)


    class Meta:
        verbose_name = 'Staking_Admin_Management'
        db_table = 'KE4EfjPravJ6mH3g'
        indexes = [
			models.Index(fields=['status','withdraw_status'])
		]


class internal_transfer_admin_management(models.Model):
    transaction_fees = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Reward Percent",blank=True,null=True)
    health_wallet = models.BooleanField(default=True)
    referral_wallet = models.BooleanField(default=True)
    stake_referral_wallet = models.BooleanField(default=False)
    stake_withdraw_wallet = models.BooleanField(default=False)
    General_Status = (
        (0,'Active'),
        (1,'Inactive'),		
	)
    status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
    minimum_internal = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Minimum Internal Transfer Amount(Health)",blank= True,null= True)
    maximum_internal = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Maximum Internal Transfer Amount(Health)",blank= True,null= True)
    minimum_internal_referal = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Minimum Internal Transfer Amount(Referral)",blank= True,null= True)
    maximum_internal_referal = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Maximum Internal Transfer Amount(Refarral)",blank= True,null= True)
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)

    class Meta:
        verbose_name = 'Internal_Transfer_Admin_Management'
        db_table = 'aUOX702n6UQNFnwE'
        indexes = [
			models.Index(fields=['status'])
		]



class internal_transfer_history(models.Model):
    user = models.CharField(max_length=50,verbose_name="User",blank=True,null=True)
    email = models.CharField(max_length=50,verbose_name="Email",blank=True,null=True)
    from_wallet = models.CharField(max_length=50,verbose_name="From Wallet",blank=True,null=True)
    to_wallet = models.CharField(max_length=50,verbose_name="To Wallet",blank=True,null=True)
    actual_amount = models.CharField(max_length=50,verbose_name="Actual Amount(USDT)",blank=True,null=True)
    converted_amount = models.CharField(max_length=50,verbose_name=" Converted Amount(USDT)",blank=True,null=True)
    fees = models.CharField(max_length=50,verbose_name="Fees(%)",blank=True,null=True)
    amount = models.CharField(max_length=50,verbose_name="Amount(JW)",blank=True,null=True)
    INTERNAL_TRANSFER_STATUS = (
        (0,'Completed'),
        (1,'Pending')
    )
    status = models.IntegerField(choices=INTERNAL_TRANSFER_STATUS,default=1,verbose_name='Status')
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)
    


    class Meta:
        verbose_name = 'Internal_Transfer_History'
        db_table = 'tEKgX0xAVANhx8U3'
        indexes = [
			models.Index(fields=['user'])
		]


#Stake Deposit

class stake_deposit_management(models.Model):
    user = models.CharField(max_length=50,verbose_name="User",blank=True,null=True)
    email = models.CharField(max_length=50,verbose_name="Email",blank=True,null=True)
    Amount_USDT = models.CharField(max_length=50,verbose_name="Amount USDT",blank=True,null=True)
    Amount_JW = models.CharField(max_length=50,verbose_name="Amount JW",blank=True,null=True)
    type = models.CharField(max_length=50,verbose_name="Type",blank=True,null=True)
    Hash = models.CharField(max_length=500,verbose_name="Hash",blank=True,null=True)
    General_Status = (
        (0,'Pending'),
        (1,'Success'),		
	)
    status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)
    

    class Meta:
        verbose_name = 'Stake_Deposit_Management'
        db_table = 'StagX0xAVANhxDEP'
        indexes = [
			models.Index(fields=['user'])
		]


#stake_history

class Stake_history_management(models.Model):
    user = models.CharField(max_length=50,verbose_name="User",blank=True,null=True)
    email = models.CharField(max_length=50,verbose_name="Email",blank=True,null=True)
    Amount_USDT = models.CharField(max_length=50,verbose_name="Amount USDT",blank=True,null=True)
    Amount_JW = models.CharField(max_length=50,verbose_name="Amount JW",blank=True,null=True)
    market_price = models.CharField(max_length=50,verbose_name="Market Price",blank=True,null=True)
    General_Status = (
        (0,'Active'),
        (1,'Inactive'),		
	)
    status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
    period = models.IntegerField(blank=True,verbose_name="Period")
    maximum_reward = models.DecimalField(max_digits=36,decimal_places=8,verbose_name='Maximum Reward',default=0)
    reward_percent = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Reward Percent",blank=True,null=True)
    reward_per_month = models.DecimalField(max_digits=36,decimal_places=8,verbose_name='Reward Per Month',default=0)
    referral_reward_earned = models.DecimalField(max_digits=36,decimal_places=8,verbose_name='Referral Rewards Earned',default=0)
    Total_reward_earned = models.DecimalField(max_digits=36,decimal_places=8,verbose_name='Total Reward Earned',default=0)
    reward_earned = models.DecimalField(max_digits=36,decimal_places=8,verbose_name='Rewards Earned',default=0)
    reward_balance = models.DecimalField(max_digits=36,decimal_places=8,verbose_name='Rewards Balance',default=0)
    referral_status = models.IntegerField(blank=True,verbose_name="User Referral Status")
    referral_level = models.IntegerField(blank=True,null= True,verbose_name=" User Maximum Referral Eligible Level")
    CLAIM_Status = (
        (0,'Enable'),
        (1,'Disable'),
        (2,'Claimed')		
	)
    claim_status=models.IntegerField(choices=CLAIM_Status,default=1,verbose_name='Status')
    start_date = models.DateTimeField(verbose_name="Start date",default=timezone.now)
    end_date = models.DateTimeField(verbose_name="End date",default=timezone.now)
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)
    

    class Meta:
        verbose_name = "Stake_history_management"
        db_table = "StaHISAVANhxD100"
        indexes = [
			models.Index(fields=['user'])
		]


#stake Referral Management

class Stake_referral_management(models.Model):
    levels = models.IntegerField(blank=True,null=True,default = 0,verbose_name="Referral Levels")
    self_stake_Amount = models.IntegerField(blank=True,null=True,default = 0 , verbose_name="Self Stake Amount (USDT)")
    self_stake_Amount_range = models.IntegerField(blank=True,null=True,default = 0 , verbose_name="Self Stake Amount Range (USDT)")
    first_level_stake = models.DecimalField(max_digits=36,decimal_places=8,blank=True,null=True,default = 0,verbose_name="First Level Stake Reward (%)")
    secound_level_stake = models.DecimalField(max_digits=36,decimal_places=8,blank=True,null=True,default = 0,verbose_name="Second Level Stake Onwards Reward (%)")
    General_Status = (
        (0,'Active'),
        (1,'Inactive'),		
	)
    status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)

    class Meta:
        verbose_name = "Stake_referral_management"
        db_table = "StaREFAVANhxD200"
        indexes = [
			models.Index(fields=['levels'])
		]


# Stake Referral reward DB

class Stake_referral_reward_table(models.Model):
    user = models.CharField(max_length=50,verbose_name="User",blank=True,null=True)
    email = models.CharField(max_length=50,verbose_name="Email",blank=True,null=True)
    type = models.CharField(max_length=50,verbose_name="Type",blank=True,null=True)
    direct_referral_user = models.CharField(max_length=50,verbose_name="Direct Referral User",blank=True,null=True)
    referral_reward_amount = models.CharField(max_length=50,verbose_name="Referral Reward Amount",blank=True,null=True)
    referral_level = models.CharField(max_length=50,verbose_name="Referral Level",blank=True,null=True)
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)
    General_Status = (
        (0,'Active'),
        (1,'Inactive'),		
	)
    status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')


    class Meta:
        verbose_name = "Stake_Referral_Reward_Table"
        db_table = "nUo3wQ2IVVUq2oh7"
        indexes = [
			models.Index(fields=['user'])
		]


# Stake claim DB

class stake_claim_table(models.Model):
    user = models.CharField(max_length=50,verbose_name="User",blank=True,null=True)
    email = models.CharField(max_length=50,verbose_name="Email",blank=True,null=True)
    back_up_phrase = models.CharField(max_length=500,verbose_name='Month Stake',blank=True,null=True)
    original_USDT =  models.CharField(max_length=50,verbose_name='Original claim Amount USDT',blank=True,null=True)
    claim_amount_USDT = models.CharField(max_length=50,verbose_name='Claim Amount USDT',blank=True,null=True)
    claim_amount_JW = models.CharField(max_length=50,verbose_name='Claim Amount JW',blank=True,null=True)
    Address = models.CharField(max_length=50,verbose_name='Address',blank=True,null=True)
    Transaction_Hash = models.CharField(max_length=200,verbose_name='Transaction Hash',blank=True,null=True,default="")
    Withdraw_Status = (
        (0,'Pending'),
        (1,'Completed'),
        (2,'Cancelled'),
	)
    status =models.IntegerField(choices=Withdraw_Status,default=0,verbose_name='Status')
    Two_Fa = models.IntegerField(verbose_name="Two FA OTP",blank=True,null=True)
    Wallet_type = models.CharField(max_length=200,verbose_name='Wallet type',blank=True,null=True,default="")
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)


    class Meta:
        verbose_name = "Stake_Claim_Table"
        db_table = "Wwsv4AxWH4cko399"
        indexes = [
			models.Index(fields=['user'])
		]


class stake_reward_history(models.Model):
    user = models.CharField(max_length=50,verbose_name="User",blank=True,null=True)
    email = models.CharField(max_length=50,verbose_name="Email",blank=True,null=True)
    reward_amount = models.DecimalField(max_digits=36,decimal_places=8,blank=True,null=True,default = 0,verbose_name="Reward Amount")
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)
    Status = (
        (0,'Active'),
        (1,'Inactive'),	
	)
    status =models.IntegerField(choices=Status,default=0,verbose_name='Status')

    class Meta:
        verbose_name = "Stake_Reward_History"
        db_table = "STA4AxWH4ckoREW"
        indexes = [
			models.Index(fields=['user'])
		]

class stake_claim_reward_history(models.Model):
    user = models.CharField(max_length=50,verbose_name="User",blank=True,null=True)
    email = models.CharField(max_length=50,verbose_name="Email",blank=True,null=True)
    buy_type = models.CharField(max_length=50,verbose_name="Buy Type",blank=True,null=True)
    type = models.CharField(max_length=50,verbose_name="Type",blank=True,null=True)
    Wallet_type = models.CharField(max_length=200,verbose_name='Wallet type',blank=True,null=True,default="")
    original_amount = models.DecimalField(max_digits=36,decimal_places=8,blank=True,null=True,default = 0,verbose_name="Original Amount")
    transfer_amount = models.DecimalField(max_digits=36,decimal_places=8,blank=True,null=True,default = 0,verbose_name="Transfer Amount")
    stake_Wallet_reward_amount = models.DecimalField(max_digits=36,decimal_places=8,blank=True,null=True,default = 0,verbose_name="stake Wallet Reward Amount")
    stake_withdraw_Wallet_reward_amount = models.DecimalField(max_digits=36,decimal_places=8,blank=True,null=True,default = 0,verbose_name="stake Withdraw Wallet Reward Amount")
    stake_Wallet_percentage = models.DecimalField(max_digits=36,decimal_places=8,blank=True,null=True,default = 0,verbose_name="stake Wallet percentage")
    stake_withdraw_Wallet_percentage = models.DecimalField(max_digits=36,decimal_places=8,blank=True,null=True,default = 0,verbose_name="stake withdraw Wallet percentage")
    stake_amount= models.DecimalField(max_digits=36,decimal_places=8,blank=True,null=True,default = 0,verbose_name="stake amount")
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)
    Status = (
        (0,'Active'),
        (1,'Inactive'),	
	)
    status =models.IntegerField(choices=Status,default=0,verbose_name='Status')

    class Meta:
        verbose_name = "Stake_Reward_History"
        db_table = "STACLAIH4ckoREW"
        indexes = [
			models.Index(fields=['user'])
		]


class Stake_Monthly_Claim_History(models.Model):
    user = models.CharField(max_length=50,verbose_name="User",blank=True,null=True)
    email = models.CharField(max_length=50,verbose_name="Email",blank=True,null=True)
    stake_history_id = models.ForeignKey(Stake_history_management,related_name ='stake_id',on_delete=models.CASCADE,verbose_name='Stake History Id',default="")
    earned_stake_reward = models.DecimalField(max_digits=16,decimal_places=8,blank=True,null=True,default = 0.0000,verbose_name="Earned Stake Reward Amount")
    start_date = models.DateTimeField(verbose_name="Start date",default=timezone.now)
    end_date = models.DateTimeField(verbose_name="End date",default=timezone.now)
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)
    Status = (
        (0,'Active'),
        (1,'Inactive'),	
        (2,'Claimed'),
	)
    status =models.IntegerField(choices=Status,default=0,verbose_name='Status')


    class Meta:
        verbose_name = "Stake_Monthly_Claim_History"
        db_table = "STAH4ckMONoREWCLAI"
        indexes = [
			models.Index(fields=['user'])
		]
# Create your models here.



# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                                                    #Stake credit wallet    

Stake_Market_Price_Status =(
		(0,'API'),
		(1,'Manual'),
	)

class Stake_market_price(models.Model):
	market_price = models.CharField(max_length=50,verbose_name="Stake Market Price",blank=True,null=True)
	status = models.IntegerField(choices=Stake_Market_Price_Status,default=0,verbose_name='Status')
	API = models.IntegerField(verbose_name="API to be Used",blank=True,null=True)

	class Meta:
		verbose_name = "Stake Market Price"
		db_table = 'STAMarITHkpbdREL'

class stake_monthly_wallet_management(models.Model):
    user = models.CharField(max_length=50,verbose_name="User",blank=True,null=True)
    email = models.CharField(max_length=50,verbose_name="Email",blank=True,null=True)
    stake_month_withdraw_Wallet = models.CharField(max_length=50,verbose_name="Stake Month Withdraw Wallet",blank=True,null=True)
    stake_month_Refferal_Wallet = models.CharField(max_length=50,verbose_name="Stake Month Refferal Wallet",blank=True,null=True)
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)
    
    class Meta:
        verbose_name='Staking_Monthly_Wallet_Management'
        db_table='STMOWA17c9KmWtBI'
        indexes = [
			models.Index(fields=['user'])
		]

class staking_monthly_admin_management(models.Model):
    stake_period = models.IntegerField(blank=True,verbose_name="Stake Period")
    reward_percent = models.DecimalField(max_digits=4,decimal_places=2,verbose_name="Reward Percent",blank=True,null=True)
    General_Status = (
        (0,'Active'),
        (1,'Inactive'),		
	)
    status=models.IntegerField(choices=General_Status,default=0,verbose_name='Stake Status')
    minimum_stake = models.DecimalField(max_digits=36,decimal_places=8,verbose_name="Min Stake Amount",blank= True,null= True)
    maximum_stake = models.DecimalField(max_digits=36,decimal_places=8,verbose_name="Max Stake Amount",blank= True,null= True)
    minimum_withdraw = models.DecimalField(max_digits=36,decimal_places=8,verbose_name="Min Withdraw Amount",blank= True,null= True)
    maximum_withdraw = models.DecimalField(max_digits=36,decimal_places=8,verbose_name="Max Withdraw Amount",blank= True,null= True)
    minimum_withdraw_referal = models.DecimalField(max_digits=36,decimal_places=8,verbose_name="Min Withdraw Amount (Referral Wallet)",blank= True,null= True)
    maximum_withdraw_referal = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Max Withdraw Amount (Referral Wallet)",blank= True,null= True)
    withdraw_fees = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Withdraw Fees",blank= True,null= True,default=0.0)
    Referral_Status = (
        (0,'Active'),
        (1,'Inactive'),		
	)
    referral_status = models.IntegerField(choices=Referral_Status,default=0,verbose_name='Referral Status')
    referral_level = models.IntegerField(blank=True,null= True,verbose_name="Maximum Referral Eligible Level")
    Withdraw_Status = (
        (0,'Active'),
        (1,'Inactive'),		
	)
    withdraw_status = models.IntegerField(choices=Withdraw_Status,default=0,verbose_name='Withdraw Status')
    stake_withdraw_transaction_fee = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Withdraw Fee",blank=True,null=True)
    eligible_plan = models.IntegerField(default=0,verbose_name='Stake Eligible Plan')
    stake_wallet_percentage = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Stake wallet claim(%)",blank=True,null=True)
    withdraw_wallet_percentage = models.DecimalField(max_digits=4,decimal_places=1,verbose_name="Withdraw Wallet claim(%)",blank=True,null=True)
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)


    class Meta:
        verbose_name = 'Staking_Monthly_Admin_Management'
        db_table = 'STAMOP2J7vB1skmq'
        indexes = [
			models.Index(fields=['status','withdraw_status'])
		]



#monthly_stake_history

class Stake_monthly_history_management(models.Model):
    user = models.CharField(max_length=50,verbose_name="User",blank=True,null=True)
    email = models.CharField(max_length=50,verbose_name="Email",blank=True,null=True)
    Amount_USDT = models.CharField(max_length=50,verbose_name="Amount USDT",blank=True,null=True)
    Amount_JW = models.CharField(max_length=50,verbose_name="Amount JW",blank=True,null=True)
    market_price = models.CharField(max_length=50,verbose_name="Market Price",blank=True,null=True)
    General_Status = (
        (0,'Active'),
        (1,'Inactive'),		
	)
    status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
    period = models.IntegerField(blank=True,verbose_name="Period")
    maximum_reward = models.DecimalField(max_digits=36,decimal_places=8,verbose_name='Maximum Reward',default=0)
    reward_percent = models.DecimalField(max_digits=4,decimal_places=2,verbose_name="Reward Percent",blank=True,null=True)
    reward_per_month = models.DecimalField(max_digits=36,decimal_places=8,verbose_name='Reward Per Month',default=0)
    reward_earned = models.DecimalField(max_digits=36,decimal_places=8,verbose_name='Stake Rewards Earned',default=0)
    referral_reward_earned = models.DecimalField(max_digits=36,decimal_places=8,verbose_name='Referral Rewards Earned',default=0)
    Total_reward_earned = models.DecimalField(max_digits=36,decimal_places=8,verbose_name='Total Reward Earned',default=0)
    reward_balance = models.DecimalField(max_digits=36,decimal_places=8,verbose_name='Rewards Balance',default=0)
    referral_status = models.IntegerField(blank=True,verbose_name="User Referral Status")
    referral_level = models.IntegerField(blank=True,null= True,verbose_name=" User Maximum Referral Eligible Level")
    CLAIM_Status = (
        (0,'Enable'),
        (1,'Disable'),
        (2,'Claimed')		
	)
    claim_status=models.IntegerField(choices=CLAIM_Status,default=1,verbose_name='Status')
    start_date = models.DateTimeField(verbose_name="Start date",default=timezone.now)
    end_date = models.DateTimeField(verbose_name="End date",default=timezone.now)
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)
    

    class Meta:
        verbose_name = "Stake_monthly_history_management"
        db_table = "StaHISAVANhxDMON"
    





class stake_credit_reward_history(models.Model):
    user = models.CharField(max_length=50,verbose_name="User",blank=True,null=True)
    email = models.CharField(max_length=50,verbose_name="Email",blank=True,null=True)
    reward_amount = models.DecimalField(max_digits=36,decimal_places=8,blank=True,null=True,default = 0,verbose_name="Reward Amount")
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)
    Status = (
        (0,'Active'),
        (1,'Inactive'),	
	)
    status =models.IntegerField(choices=Status,default=0,verbose_name='Status')

    class Meta:
        verbose_name = "Stake_Credit_Reward_History"
        db_table = "STACRExWH4ckoREW"
        indexes = [
			models.Index(fields=['user'])
		]


class stake_credit_claim_history(models.Model):
    user = models.CharField(max_length=100,verbose_name="user",blank=True,null=True)
    email = models.CharField(max_length=50,verbose_name="Email",blank=True,null=True)
    staked_amount = models.CharField(max_length=50,verbose_name="Staked Amount",blank=True,null=True)
    stake_Credit_history_id = models.CharField(max_length=50,verbose_name="Stake Credit History",blank=True,null=True)
    earned_stake_reward = models.DecimalField(max_digits=16,decimal_places=8,blank=True,null=True,default = 0.0000,verbose_name="Earned Stake Reward Amount")
    start_date = models.DateTimeField(verbose_name="Start date",default=timezone.now)
    end_date = models.DateTimeField(verbose_name="End date",default=timezone.now)
    created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
    modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)
    Status = (
        (0,'Active'),
        (1,'Inactive'),	
        (2,'Claimed'),
	)
    status =models.IntegerField(choices=Status,default=0,verbose_name='Status')
    class Meta:
        verbose_name = "Stake Credit Claim History"
        db_table = 'STCRCLAXhUkKRlwLkw'
        
        
        



#########################
#######################    new stake


class new_stake_deposit_management(models.Model):
    user = models.CharField(max_length=50,verbose_name="User",blank=True,null=True)
    email = models.CharField(max_length=50,verbose_name="Email",blank=True,null=True)
    Amount_USDT = models.CharField(max_length=50,verbose_name="Amount USDT",blank=True,null=True)
    Amount_JW = models.CharField(max_length=50,verbose_name="Amount JW",blank=True,null=True)
    type = models.CharField(max_length=50,verbose_name="Type",blank=True,null=True)
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
        verbose_name = 'New_Stake_Deposit_Management'
        db_table = 'StakeDeposite'
        indexes = [
			models.Index(fields=['user'])
		]
        
        
        
class stake_purchase_history(models.Model):
	user_id = models.IntegerField(default=0, verbose_name="user_id")
	purchase_amount = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='plan_purchase_amount')
	user_wallet_type = models.CharField(verbose_name="user_wallet_type",default="",max_length = 200)
	buy_type = models.CharField(verbose_name="Buy Type",default="",max_length=200)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)
	status=models.IntegerField(default=0,verbose_name='status')

	class Meta:
		verbose_name = "Stake Purchase History"
		db_table = "newstake"



class newstake_Referral_reward_History(models.Model):
	user = models.ForeignKey(User_Management,on_delete=models.CASCADE,verbose_name='User',default="")
	referral_id = models.CharField(max_length=50,verbose_name="Referral ID",blank=True,null=True)
	reward = models.CharField(max_length=50,verbose_name="Reward",blank=True,null=True)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "stake_referral_reward History"
		db_table = 'stake_referral_reward'
		indexes = [
			models.Index(fields=['user'])
		]


  
class newstakeclaim_History(models.Model):
	user = models.ForeignKey(User_Management,related_name ='newstakeclaim_History',on_delete=models.CASCADE,verbose_name='User',default="")
	referral_id = models.CharField(max_length=50,verbose_name="Referral ID",blank=True,null=True)
	reward = models.CharField(max_length=50,verbose_name="Reward",blank=True,null=True)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "newstake claim_History "
		db_table = 'stakeclaimreward'
		indexes = [
			models.Index(fields=['user'])
		]
