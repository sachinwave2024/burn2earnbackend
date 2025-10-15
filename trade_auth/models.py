from django.db import models


from trade_currency.models import TradeCurrency
from django.utils import timezone

Address_Status = (
		(0,'Active'),
		(1,'Inactive'),
		(2,'Cancelled')
	)

# Create your models here.
class UserAddress(models.Model):
	useraddress = models.CharField(max_length=100,verbose_name='Address')
	userbtcaddress = models.CharField(max_length=100,verbose_name='BTC Address',blank=True,null=True)
	contractid=models.IntegerField(verbose_name='Contract ID',default=0)
	status=models.IntegerField(choices=Address_Status,default=0,verbose_name='Status')
	created_on = models.DateTimeField(auto_now_add = True,verbose_name='Created on')
	modified_on = models.DateTimeField(auto_now=True,verbose_name='Last Login')
	def __str__(self):
		return self.useraddress
	class Meta:
		verbose_name = 'Useraddress'
		db_table ='APLegJVs5IOqnDex'



class UserWallet(models.Model):
	useraddress = models.ForeignKey(UserAddress,related_name ='userwalletaddress',on_delete=models.CASCADE,verbose_name='Address')
	currency = models.ForeignKey(TradeCurrency,related_name ='Currency',on_delete=models.CASCADE,verbose_name='Currency')
	address = models.CharField(max_length=300,verbose_name='Address',blank=True,null=True)
	status=models.IntegerField(choices=Address_Status,default=0,verbose_name='Status')

	def __str__(self):
		return self.address
	class Meta:
		verbose_name = 'UserWallet'
		db_table ='p2Gw2fGKotK7NcaN'

		
class Market_place(models.Model):
	Market_STATUS = (('enable', 'enable'), ('disable', 'disable'))
	Google_status=models.CharField(choices=Market_STATUS,max_length=200,default='disable')
	internal_transfer = models.CharField(choices=Market_STATUS,max_length=200,default='disable')
    
	class Meta:
		verbose_name ='Market place'
		db_table='MAKUJ546JDFGHET'

