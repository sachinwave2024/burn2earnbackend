from django.db import models
from django.core.validators import RegexValidator
from datetime import date
from django.urls import reverse
import os


View_Type = (
                (0,'Live'),
                (1,'Under Maintenance'),

    )


General_Status = (
	(0,'Enable'),
	(1,'Disable'),
	)

Market_Price_Status =(
		(0,'API'),
		(1,'Manual'),
	)
Withdraw =(
		(0,'Auto'),
		(1,'Manual'),
	)
class Company(models.Model):
    name = models.CharField(max_length=50,default='HotBitDeal',verbose_name='Site Name')
    caption = models.CharField(max_length=60,default='',verbose_name='Site Caption',blank=True,null=True)
    director = models.CharField(max_length=60,default='',verbose_name='Director',blank=True,null=True)
    
    reg_info = models.CharField(max_length=60,default='',verbose_name='Site Registration Info',blank=True,null=True)
   
    address1=models.CharField(max_length=100,verbose_name='Contact Address')
    city = models.CharField(max_length=50,verbose_name='City',blank=True,null=True)
    state = models.CharField(max_length=50,verbose_name='State',blank=True,null=True)
    country = models.CharField(max_length=50,verbose_name='Country',blank=True,null=True)
    postcode = models.CharField(max_length=10,verbose_name='Pin Code',blank=True,null=True)
    session_timeout = models.CharField(max_length=10,verbose_name='Session Time Out',blank=True,null=True)
    withdraw_type = models.IntegerField(choices=Withdraw,default=0,verbose_name='Withdraw Type')
    Device_id_status=models.IntegerField(choices=General_Status,default=0,verbose_name='Device Id Status')
    support_address =  models.CharField(verbose_name="Support Address",default="",max_length = 500,blank=True,null=True) 
    market_api_price= models.CharField(max_length=100,verbose_name='Market Api Price',blank=True,null=True)
    status = models.IntegerField(choices=Market_Price_Status,default=0,verbose_name='Status')
    API = models.IntegerField(verbose_name="API to be Used",blank=True,null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 13 digits allowed.")
    phone1 = models.CharField(max_length=13,help_text='Phone number Format : 0xxxxxxxxxx',verbose_name='Phone Number',blank=True,null=True)
    website = models.CharField(max_length=200,blank=True,null=True)
    email = models.EmailField(max_length=60,blank=True,null=True)
    
    company_logo = models.ImageField(upload_to='logo',verbose_name='Site Logo',blank=True,null=True)
    company_fav = models.ImageField(upload_to='favicons',verbose_name='Site Favicon',blank=True,null=True)
    copy_right =  models.CharField(max_length=200,verbose_name='Copy Rights',blank=True,null=True)
    admin_redirect = models.CharField(max_length=100,verbose_name='Admin Redirect',blank=True,null=True)
    fb = models.CharField(max_length=200,verbose_name='Facebook',blank=True,null=True)
    twitter = models.CharField(max_length=200,verbose_name='Twitter',blank=True,null=True)
    telegram = models.CharField(max_length=200,verbose_name='Telegram',blank=True,null=True) 
    instagram = models.CharField(max_length=200,verbose_name='Instagram',blank=True,null=True) 
    linkedin =  models.CharField(max_length=200,verbose_name='Linkedin',blank=True,null=True)
    
    Android_version = models.CharField(max_length=200,verbose_name='Android Version',blank=True,null=True)
    IOS_version = models.CharField(max_length=200,verbose_name='IOS Version',blank=True,null=True)
    privatekey = models.CharField(max_length=200,verbose_name='privatekey Version',blank=True,null=True)
    securitykey = models.CharField(max_length=200,verbose_name='securitykey Version',blank=True,null=True)
    withaddress = models.CharField(max_length=200,verbose_name='withaddress Version',blank=True,null=True)
    
    facebookpromo = models.IntegerField(verbose_name="facebookpromo to be Used",blank=True,null=True)
    instapromo = models.IntegerField(verbose_name="instapromo to be Used",blank=True,null=True)
    twitterpromo = models.IntegerField(verbose_name="twitterpromo to be Used",blank=True,null=True)
    cmcpromo = models.IntegerField(verbose_name="cmcpromo to be Used",blank=True,null=True)
    
    created_on = models.DateTimeField(auto_now_add = True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def companyimage_name(self):
        return  os.path.basename(self.company_logo.path) if self.company_logo else ''

    @property
    def companyfav_name(self):
        return  os.path.basename(self.company_fav.path) if self.company_fav else ''

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        db_table='CMRaaNrAUFW1I04S'


class Company_Settings(models.Model):
    company_settings_name=models.OneToOneField(Company,related_name='company_settings',on_delete=models.CASCADE)
    
    site_maintenance_status= models.IntegerField(choices=View_Type,default=1,verbose_name='Android Site Maintenance')
    IOS_site_maintenance_status= models.IntegerField(choices=View_Type,default=1,verbose_name='IOS Site Maintenance')
    site_maintenance =models.TextField(blank=True,null=True)
    adminipaddress =  models.CharField(max_length=50,verbose_name='Admin IP Address',blank=True,null=True)

    
    def __int__self(self):
        return self.id

    class Meta:
        verbose_name = "CompanySetting"
        verbose_name_plural = "CompanySetting"
        db_table='cX0ZvTLd47wUtoWT'


