from django.db import models

from django.conf import settings


from datetime import date

from django.core.validators import RegexValidator
from auditable.models import Auditable

from django.urls import reverse
import os
from django.db.models import Q
from django.db.models import Count, Min, Sum, Avg ,F,DecimalField
from decimal import Decimal
import time

from django.utils import timezone

from ckeditor.fields import RichTextField
from trade_admin_auth.models import User_Management

from django.contrib.auth.models import User,Group



General_Status = (
					(0,'Active'),
					(1,'Inactive'),
					
	)

ip_type = (
	(0,'User'),
	(1,'Admin'),
					
	)

Content_type = (
	(0,'page'),
	(1,'content')

	)
Read_Status = (
	(0,'New'),
	(1,'Replied'),
	(2,'Closed'),
	(3,'Cancelled'),
	(4,'Re-opened')
	)

class Cms_StaticContent(Auditable):
	name = models.CharField(max_length=50,verbose_name='Name',blank=True,null=True)
	title = models.CharField(max_length=50,verbose_name='Title')
	content = RichTextField(help_text='Content',verbose_name='Content',blank=True,null=True)
	contenttype=models.IntegerField(choices=Content_type,default=0,verbose_name='Content')
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')

	def __int__self(self):
		return id
	class Meta:
		verbose_name='Cms_StaticContent'
		db_table='C9bDIAkN3dlB5T1b'


class Faq(Auditable):
	title = models.CharField(max_length=100,verbose_name='Question')
	content = models.TextField(help_text='Content',verbose_name='Content',blank=True,null=True)
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')

	def __int__self(self):
		return id
	class Meta:
		verbose_name='Faq'
		db_table='fOfwvYRmmHVwm48s'


class Roadmap(Auditable):
	title = models.CharField(max_length=50,verbose_name='Title')
	year = models.CharField(max_length=50,verbose_name='Year')
	content = models.TextField(help_text='Content',verbose_name='Content',blank=True,null=True)
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')

	def __int__self(self):
		return id
	class Meta:
		verbose_name='Roadmap'
		db_table='RQ99aE1KxKWQ2o1D'



class SupportCategory(models.Model):
	category = models.CharField(max_length=200,verbose_name="Category",blank=True,null=True)
	status = models.IntegerField(choices=General_Status,default=0,verbose_name='Status')


	def __int__self(self):
		return "%s" % self.category
	class Meta:
		verbose_name = 'SupportCategory'
		db_table = 'SCate721GFH27LOW22'



class Contactus(models.Model):
	phone1=models.CharField(max_length=130,verbose_name='Hash',blank=True,null=True)
	ticket_id = models.CharField(max_length=10,verbose_name='Ticket Id',blank=True,null=True)
	name =models.CharField(max_length=50,verbose_name='Name')
	userid = models.ForeignKey(User_Management,related_name ='Contactus_User',on_delete=models.CASCADE,verbose_name='User',blank=True,null=True)
	email = models.CharField(max_length=50,verbose_name='Email')
	subject = models.CharField(max_length=50,verbose_name='Subject')
	message = models.TextField(help_text='Message',verbose_name='Message')
	reply = models.TextField(help_text='Message',verbose_name='Reply',blank=True,null=True)
	status =models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
	read_status =models.IntegerField(choices=Read_Status,default=0,verbose_name='Read Status')
	attachment = models.TextField(help_text='ex : [a,b,1,2]',verbose_name='Attachment',blank=True,null=True)
	support_category = models.CharField(max_length=200,verbose_name="Category Name",blank=True,null=True)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	def __int__self(self):
		return id
	class Meta:
		verbose_name='Contactus'
		db_table='cSlmuii55R4oLi9Q'


USER_TYPE = (
	(0,'User'),
	(1,'Admin')
)

class SupportTicket(models.Model):
	ticket = models.ForeignKey(Contactus,related_name='TicketId',on_delete=models.CASCADE,verbose_name='TicketID')
	created_by =models.CharField(max_length=50,verbose_name='Created by')
	comment = RichTextField(help_text='Comment',verbose_name='Comment')
	attachment = models.TextField(help_text='ex : [a,b,1,2]',verbose_name='attachment',blank=True,null=True)
	user_type = models.IntegerField(choices=USER_TYPE,default=0,verbose_name='User Type')
	created_on = models.DateTimeField(auto_now_add = True)

	class Meta:
		verbose_name='SupportTicket'
		db_table='SupportN563gf8n2Ve'	


class EmailTemplate(Auditable):
	
	name = models.CharField(max_length=50,verbose_name='Name')
	Subject = models.CharField(max_length=300,verbose_name='Subject')
	content = RichTextField(help_text='Content',verbose_name='Content')
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')

	def __int__self(self):
		return id
	class Meta:
		verbose_name='EmailTemplate'
		db_table='E5w4yMqjVXoTQlty'



class Currencylist(Auditable):
	name = models.CharField(max_length=50,verbose_name='Name')
	softcap = models.CharField(max_length=50,verbose_name='Soft cap')
	hardcap = models.CharField(max_length=50,verbose_name="Hard cap")
	attachement = models.FileField(verbose_name='WhitePaper',blank=True,null=True)
	timer_date = models.DateTimeField()
	buytoken_url = models.CharField(max_length=100,verbose_name="Buy Token Url",blank=True,null=True)
	content = models.TextField(help_text='Content',verbose_name='Content',blank=True,null=True)
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')

	def __int__self(self):
		return id
	class Meta:
		verbose_name='Currencylist'
		db_table='c2plLP6av1pk3STI'



class Blockip(Auditable):
	ip_address = models.GenericIPAddressField()
	ip_option = models.IntegerField(choices=ip_type,default=0,verbose_name="IP Option")
	ip_level = models.CharField(max_length=50,verbose_name='Ip Level',blank=True,null=True)
	status = models.IntegerField(choices=General_Status,default=0,verbose_name="Status")
	
	def __int__self(self):
		return id

	class Meta:
		verbose_name='Blockip'
		db_table = 'BjRI3yQGhisBCfnZ'



class AccessLog(Auditable):
	Type = models.CharField(max_length=50,verbose_name='Type')
	name = models.CharField(max_length=50,verbose_name='Name',blank=True,null=True)
	title = models.CharField(max_length=50,verbose_name='Title')
	content = models.TextField(help_text='Content',verbose_name='Content',blank=True,null=True)
	datetime = models.DateTimeField(default=timezone.now)
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')

	def __int__self(self):
		return id
	class Meta:
		verbose_name='AccessLog'
		db_table='AbFQAh45sPZK86hd'


class LoginHistory(models.Model):
	user = models.ForeignKey(User_Management,related_name='Userid',on_delete=models.CASCADE,verbose_name='Username')
	ip_address = models.GenericIPAddressField()
	ip_address1 = models.GenericIPAddressField()
	created_on = models.DateTimeField(verbose_name="Created On")
	modified_on = models.DateTimeField(verbose_name="Modified On")


	class Meta:
		verbose_name='LoginHistory'
		db_table='Avfy3ZYuyC2l2BA'


class MenuModule(models.Model):
	module_code =models.CharField(max_length=20,verbose_name='Module Code')
	module_name = models.CharField(max_length=50,verbose_name='Module Name')
	created_on = models.DateTimeField(auto_now_add = True)
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')

	def __int__self(self):
		return id
	
	class Meta:
		verbose_name = 'MenuModules'
		db_table='21HbadiSPqTR4E0L'


class SubMenuModule(models.Model):
	main_module_name = models.ForeignKey(MenuModule,related_name ='main_menu_module',on_delete=models.CASCADE)
	sub_module_name = models.CharField(max_length=50,verbose_name='Sub Module Name')
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
	created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)


	def __int__self(self):
		return "%s" % self.sub_module_name
	class Meta:
		verbose_name = 'SubMenuModules'
		db_table='31HbadiSPqTRSub'


class IconMenuModule(models.Model):
	sub_module_name = models.ForeignKey(SubMenuModule,related_name ='main_menu_module',on_delete=models.CASCADE)
	icon_module_name = models.CharField(max_length=50,verbose_name='Icon Module Name')
	status=models.IntegerField(choices=General_Status,default=0,verbose_name='Status')
	created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)


	def __int__self(self):
		return "%s" % self.icon_module_name
	class Meta:
		verbose_name = 'IconMenuModule'
		db_table='41HbadiSPqTRicon'




class MenuPermission(Auditable):
	user_permissions = models.ForeignKey(User,related_name ='admin_user_menupermissions',on_delete=models.CASCADE)
	access_modules = models.ForeignKey(MenuModule,on_delete=models.CASCADE)
	Permission_Access =(
		(0,'NotAssign'),
		(1,'Write'),
		(2,'Read'),
	)
	access_permissions=models.IntegerField(choices=Permission_Access,verbose_name='Access Permissions',blank=True,null=True)
	ACCESS_STATUS = (
		(0,'Access'),
		(1,'Denied')
	)
	access_status=models.IntegerField(choices=ACCESS_STATUS,verbose_name='Access Status',blank=True,null=True)

	def __int__self(self):
		return id
	
	class Meta:
		verbose_name ='MenuPermissions'
		db_table='12s8VH6oGW3Zh7F0'


class SubMenuPermission(Auditable):
	user_permissions = models.ForeignKey(User,related_name ='sub_user_menupermissions',on_delete=models.CASCADE)
	main_access_modules = models.ForeignKey(MenuPermission,related_name ='main_access_modules',on_delete=models.CASCADE)
	sub_menu_name = models.ForeignKey(SubMenuModule,related_name ='sub_menu_name',on_delete=models.CASCADE)
	Permission_Access =(
		(0,'NotAssign'),
		(1,'Write'),
		(2,'Read'),
	)
	access_permissions=models.IntegerField(choices=Permission_Access,verbose_name='Access Permissions',blank=True,null=True)
	ACCESS_STATUS = (
		(0,'Access'),
		(1,'Denied')
	)
	access_status=models.IntegerField(choices=ACCESS_STATUS,verbose_name='Access Status',blank=True,null=True)
	def __int__self(self):
		return id
	class Meta:
		verbose_name ='SubMenuPermissions'
		db_table='51s8VpermoGW3Zh7F0sub'


class IconMenuPermission(Auditable):
	user_permissions = models.ForeignKey(User,related_name ='icon_user_menupermissions',on_delete=models.CASCADE)
	submenu_access_modules = models.ForeignKey(SubMenuPermission,related_name ='submenu_access_modules',on_delete=models.CASCADE)
	icon_menu_name = models.ForeignKey(IconMenuModule,related_name ='icon_menu_name',on_delete=models.CASCADE)
	Permission_Access =(
		(0,'NotAssign'),
		(1,'Write'),
		(2,'Read'),
	)
	access_permissions=models.IntegerField(choices=Permission_Access,verbose_name='Access Permissions',blank=True,null=True)
	ACCESS_STATUS = (
		(0,'Access'),
		(1,'Denied')
	)
	access_status=models.IntegerField(choices=ACCESS_STATUS,verbose_name='Access Status',blank=True,null=True)
	def __int__self(self):
		return id
	class Meta:
		verbose_name ='IconMenuPermissions'
		db_table='61s8Vperm3Zh7F0icon'



class Stake_Credit_History(models.Model):
	user = models.ForeignKey(User_Management,related_name ='Stake_Credit_History',on_delete=models.CASCADE,verbose_name='User stake',default="")
	original_reward = models.CharField(max_length=50,verbose_name="Original Reward",blank=True,null=True)
	stake_percentage = models.CharField(max_length=50,verbose_name='Stake Percentage',blank=True,null=True)
	percent_value=models.CharField(max_length=50,verbose_name="Percent Value",blank=True,null=True)
	created_on = models.DateTimeField(verbose_name="Created On",default=timezone.now)
	modified_on = models.DateTimeField(verbose_name="Modified On",default=timezone.now)

	class Meta:
		verbose_name = "Stake Credit History"
		db_table = 'STACREmImmeUXB'
		# indexes = [
		# 	models.Index(fields=['user'])
		# ]

class Jw_plan_purchase_history(models.Model):
	user = models.ForeignKey(User_Management,related_name ='jw_plan_purchase_history_user',on_delete=models.CASCADE,verbose_name='User',default="")
	plan_name = models.CharField(max_length = 50,verbose_name = "plan name",default="")
	activate_plan = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name="Activate Plan")
	purchase_amount = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='plan_purchase_amount')
	stake_credit = models.DecimalField(default = 0,max_digits=16,decimal_places=8,verbose_name='stake_credit')
	user_wallet_type = models.CharField(verbose_name="user_wallet_type",default="",max_length = 200)
	buy_type = models.CharField(verbose_name="Buy Type",default="",max_length=200)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)

	class Meta:		
		verbose_name = " JW Plan Purchase History"
		db_table = "JWPLyZDDVZHkiQ"


class plan_purchase_history_edited(models.Model):
	user = models.ForeignKey(User_Management,related_name ='plan_purchase_history_edited_user',on_delete=models.CASCADE,verbose_name='User',default="")
	old_plan = models.CharField(verbose_name="Old Plan",default="",max_length=200)
	new_plan = models.CharField(verbose_name="New Plan",default="",max_length=200)
	user_wallet_type = models.CharField(verbose_name="user_wallet_type",default="",max_length = 200)
	buy_type = models.CharField(verbose_name="Buy Type",default="",max_length=200)
	trans_hash = models.CharField(verbose_name="Transcation Hash",default="",max_length = 200)
	created_on = models.DateTimeField(auto_now_add = True)
	modified_on = models.DateTimeField(auto_now=True)
	plan_start_date=models.DateTimeField(default=timezone.now,verbose_name='plan Start Date')
	plan_end_date=models.DateTimeField(default=timezone.now,verbose_name='plan End Date')
	old_plan_type= models.CharField(verbose_name="Plan Type",default="",max_length=200)
	new_plan_type= models.CharField(verbose_name="New Plan Type",default="",max_length=200)


	class Meta:		
		verbose_name = "Plan Purchase History Edited"
		db_table = "ETDPlakjjsr3XzfUq"