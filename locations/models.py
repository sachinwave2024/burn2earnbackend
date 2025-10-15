from django.db import models
import time

flag_value=(
	(1,'Yes'),
	(0,'No'),

	)

class Country(models.Model):
	name = models.CharField(max_length=50,verbose_name='Country Name')
	iso3 = models.CharField(max_length=10,verbose_name='ISO3',blank=True,null=True)
	iso2 = models.CharField(max_length=10,verbose_name='ISO2',blank=True,null=True)
	phone_code = models.CharField(max_length=20,verbose_name='Phone Code',blank=True,null=True)
	capital = models.CharField(max_length=30,verbose_name='Capital Name',blank=True,null=True)
	currency = models.CharField(max_length=10,verbose_name='Currency',blank=True,null=True)
	native = models.CharField(max_length=10,verbose_name='Native',blank=True,null=True)
	emoji = models.CharField(max_length=30,verbose_name='emoji',blank=True,null=True)
	emojiU = models.CharField(max_length=30,verbose_name='emojiU',blank=True,null=True)
	created_at = models.DateTimeField(verbose_name ='Created Date')
	updated_at = models.DateTimeField(verbose_name ='Updated Date')
	flag = models.IntegerField(choices=flag_value,verbose_name='flas')
	wikiDataId = models.CharField(max_length=30,verbose_name='wikiDataId',blank=True,null=True)

	def __str__(self):
		return f'{self.name}'
	class Meta:
		verbose_name = 'Country'
		verbose_name_plural = 'Countries'
		db_table='YUE90HH8WIZY76Tm'

class State(models.Model):
	name = models.CharField(max_length=50,verbose_name='State Name')
	country_id = models.ForeignKey(Country,related_name='countries_list',on_delete=models.CASCADE)
	country_code =models.CharField(max_length=10,verbose_name='Country Code',blank=True,null=True)
	state_code =models.CharField(max_length=10,verbose_name='State Code',blank=True,null=True)
	fips_code =models.CharField(max_length=10,verbose_name='Flip Code',blank=True,null=True)
	iso2 = models.CharField(max_length=10,verbose_name='ISO2',blank=True,null=True)
	created_at = models.DateTimeField(verbose_name ='Created Date')
	updated_at = models.DateTimeField(verbose_name ='Updated Date')
	flag = models.IntegerField(choices=flag_value,verbose_name='flas')
	wikiDataId = models.CharField(max_length=30,verbose_name='wikiDataId',blank=True,null=True)
	def __str__(self):
		return self.name
	class Meta:
		verbose_name ='State'
		verbose_name_plural = 'States'
		db_table='bBTLVprWaUrBQRnZ'


class Cities(models.Model):
	name = models.CharField(max_length=50,verbose_name='City Name')
	country_id = models.ForeignKey(Country,related_name='city_countries_list',on_delete=models.CASCADE)
	country_code =models.CharField(max_length=10,verbose_name='Country Code',blank=True,null=True)
	state_id = models.ForeignKey(State,related_name='city_state_list',on_delete=models.CASCADE)
	state_code =models.CharField(max_length=10,verbose_name='State Code',blank=True,null=True)
	latitude = models.CharField(max_length=20,verbose_name='Latitude',blank=True,null=True)
	longitude = models.CharField(max_length=20,verbose_name='Longitude',blank=True,null=True)
	created_at = models.DateTimeField(verbose_name ='Created Date')
	updated_at = models.DateTimeField(verbose_name ='Updated Date')
	flag = models.IntegerField(choices=flag_value,verbose_name='flas')
	wikiDataId = models.CharField(max_length=30,verbose_name='wikiDataId',blank=True,null=True)
	def __str__(self):
		return self.name
	class Meta:
		verbose_name ='City'
		verbose_name_plural = 'Cities'
		db_table='aB238pPacUxQduGK'


