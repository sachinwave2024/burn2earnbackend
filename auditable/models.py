from django.db import models
from django.conf import settings
from django.contrib.auth.models import User,Group

class Auditable(models.Model):
	created_on = models.DateTimeField(auto_now_add = True)
	created_by = models.ForeignKey(User,related_name='%(class)s_created_by_user',on_delete=models.CASCADE)
	modified_on = models.DateTimeField(auto_now=True)
	modified_by = models.ForeignKey(User,related_name ='%(class)s_modified_by_user',on_delete=models.CASCADE)

	class Meta:
		abstract=True

	
