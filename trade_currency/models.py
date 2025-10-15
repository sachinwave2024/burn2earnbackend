from django.db import models
from django.conf import settings

import uuid
from datetime import date

from django.core.validators import RegexValidator
from auditable.models import Auditable

from django.urls import reverse
import os
from django.db.models import Q
from django.db.models import Count, Min, Sum, Avg ,F,DecimalField
from decimal import Decimal
import time

General_Status = (
					(0,'Active'),
					(1,'Inactive'),
	)
Currency_type = (
	(0,'Crypto'),
	(1,'Fiat')

	)
Deposit_status = (
	(0,'Yes'),
	(1,'No')

	)
Withdraw_status = (
	(0,'Yes'),
	(1,'No')

	)
Withdraw_Percentagestatus = (
	(0,'Percentage'),
	(1,'Amount')

	)
lend_status =(
	(0,'Yes'),
	(1,'No')
	)
limit_status =(
	(0,'+ (Plus)'),
	(1,'- (Minus)')
	)

class TradeCurrency(Auditable):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=20,verbose_name='Name')
	symbol = models.CharField(max_length=20,verbose_name='Symbol')
	currency_label = models.CharField(max_length=20,verbose_name='Api Name',blank=True,null=True)
	currency_symbol = models.CharField(max_length=20,verbose_name='Api Symbol',blank=True,null=True)
	currncytype=models.IntegerField(choices=Currency_type,default=0,verbose_name='Currency Type')
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
	min_withdraw = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Minimum Withdraw Limit',default=0.00000000)
	max_withdraw = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Maximum Withdraw Limit',default=0.00000000)
	min_deposit = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Minimum Deposit Limit',default=0.00000000)
	max_deposi = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Maximum Deposit Limit',default=0.00000000)
	withdraw_feestype=models.IntegerField(choices=Withdraw_Percentagestatus,default=0,verbose_name='Withdraw Feestype')
	withdraw_fees = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Withdraw Fees ',default=0.00000000)
	currency_image = models.ImageField(upload_to='currencyimage',verbose_name='Currency Image',blank=True,null=True)

	deposit_status=models.IntegerField(choices=Deposit_status,default=0,verbose_name='Deposit Status')
	withdraw_status=models.IntegerField(choices=Withdraw_status,default=0,verbose_name='Withdraw Status')

	deposit_content = models.TextField(verbose_name='Deposit Content',blank=True,null=True)
	withdraw_content = models.TextField(verbose_name='Withdraw Content',blank=True,null=True)

	deposit_maintenance = models.TextField(verbose_name='Deposit Maintenance',blank=True,null=True)
	withdraw_maintenance = models.TextField(verbose_name='Withdraw Maintenance',blank=True,null=True)

	deposit_alert = models.TextField(verbose_name='Deposit Alert',blank=True,null=True)
	withdraw_alert = models.TextField(verbose_name='Withdraw Alert',blank=True,null=True)

	alert_deposit =models.BooleanField(default=False)

	usd_value = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='USD Price ',default=0.00000000)
	big_image =  models.ImageField(upload_to='bigcurrencyimage',verbose_name='Big Currency Image',blank=True,null=True)

	lend_status =models.IntegerField(choices=lend_status,default=0,verbose_name='Lending Status')

	lending_min = models.DecimalField(max_digits=16,decimal_places=2,verbose_name='Minimum Lending ',default=0.00)
	trans_min = models.DecimalField(max_digits=16,decimal_places=2,verbose_name='Block Count ',default=0.00)

	lend_duration = models.IntegerField(verbose_name='Lend Duration',default=0)
	lend_loanrate = models.IntegerField(verbose_name='Lend Rate',default=0)
	balance_minimum = models.IntegerField(verbose_name='Maximum Leverage',default=0)
	depositcontent_one = models.CharField(max_length=100,verbose_name='Deposit Content 1',blank=True,null=True)
	depositcontent_two = models.CharField(max_length=100,verbose_name='Deposit Content 2',blank=True,null=True)
	depositcontent_three = models.CharField(max_length=100,verbose_name='Deposit Content 3',blank=True,null=True)
	withdrawcontent_one = models.CharField(max_length=100,verbose_name='Withdraw Content 1',blank=True,null=True)
	withdrawcontent_two = models.CharField(max_length=100,verbose_name='Withdraw Content 2',blank=True,null=True)
	countryname = models.CharField(max_length=20,verbose_name='Country Name',blank=True,null=True)
	def __str__(self):
		return "%s" % self.symbol
	class Meta:
		ordering = ['name']
		db_table='bUUEq7GKGRvh402t'
		verbose_name = "TradeCurrency"
		verbose_name_plural ="TradeCurrencys"
		indexes = [
			models.Index(fields=['name','status'])
		]

class TradePairs(Auditable):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	from_symbol = models.ForeignKey(TradeCurrency,related_name='from_tradecurrency',on_delete=models.CASCADE,verbose_name='From Symbol')
	two_symbol = models.ForeignKey(TradeCurrency,related_name='to_tradecurrency',on_delete=models.CASCADE,verbose_name='To Symbol')
	pair_name= models.CharField(max_length=20,verbose_name='Pair Name')
	pair_url = models.CharField(max_length=20,verbose_name='Pair Url')
	maker_fees = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Buy Limit Value (%)',default=0.00000000)
	taker_fees = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Sell Limit Value (%)',default=0.00000000)
	referal_fees = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Service Fee for Exchange(%)',default=0.00000000)
	min_amount = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Minimum Amount ',default=0.00000000)
	min_price = models.DecimalField(max_digits=32,decimal_places=8,verbose_name='Minimum Price ',default=0.00000000)
	max_price = models.DecimalField(max_digits=32,decimal_places=8,verbose_name='maximum Price ',default=0.00000000)
	margin_min_price = models.DecimalField(max_digits=32,decimal_places=8,verbose_name='Margin Minimum Price ',default=0.00000000)
	margin_max_price = models.DecimalField(max_digits=32,decimal_places=8,verbose_name='Margin Maximum Price ',default=0.00000000)
	margin_loan_duration =models.IntegerField(verbose_name='Margin Loan Duration')
	margin_loan_rate =models.IntegerField(verbose_name='Margin Loan Rate')
	last_price = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Last Price ',default=0.00000000)
	change_price = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Buy Rate Value ',default=0.00000000)
	volume_price = models.DecimalField(max_digits=16,decimal_places=8,verbose_name='Sell Rate value',default=0.00000000)
	high_price = models.DecimalField(max_digits=32,decimal_places=8,verbose_name='24h High Price ',default=0.00000000)
	low_price = models.DecimalField(max_digits=32,decimal_places=8,verbose_name='24h Low Price ',default=0.00000000)

	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
	min_withdraw = models.DecimalField(max_digits=32,decimal_places=8,verbose_name='Minimum Withdraw ',default=0.00000000)
	buylimit=models.IntegerField(choices=limit_status,default=0,verbose_name='Buy Limit')
	selllimit=models.IntegerField(choices=limit_status,default=0,verbose_name='Sell Limit')
	
	def __str__(self):
		return "%s" % self.pair_name

	class Meta:
		ordering = ['pair_name']
		db_table='eqBIRAHxs8eqW4Xu'
		verbose_name = "TradePairs"
		verbose_name_plural ="TradePairs"
		indexes = [
			models.Index(fields=['from_symbol','two_symbol','status'])
		]