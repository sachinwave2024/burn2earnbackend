import django_tables2 as tables
from django_tables2.utils import A
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import django_filters
from django_filters import DateRangeFilter,DateFilter
from django import forms
from datetime import date
from django.db.models import Q
import itertools


from Staking.models import Stake_referral_management, stake_deposit_management, staking_admin_management
from Staking.models import internal_transfer_history, staking_admin_management

class Stake_Plan_Table(tables.Table):
     
     BUTTON_TEMPLATE = """

         <a href="/stake/Edit_Staking_Plan/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>&nbsp;&nbsp;

         <a href="{% url 'staking:Delete_Staking_Plan' record.id %}" title="Delete" class="btn btn-danger btn-xs">Delete</a>
     
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)    
     class Meta:
         model =  staking_admin_management 
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','stake_period','reward_percent','status','Actions']


class Stake_Referral_Table(tables.Table):
     
     BUTTON_TEMPLATE = """

         <a href="/stake/Edit_Staking_Referral/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>&nbsp;&nbsp;
     
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)    
     class Meta:
         model =  Stake_referral_management 
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','levels','self_stake_Amount','self_stake_Amount_range','first_level_stake','secound_level_stake','status','Actions']


class Internal_Transfer_Table(tables.Table):
     def render_counter(self):
      self.row_counter = getattr(self, 'row_counter', itertools.count(self.page.start_index()))
      return next(self.row_counter)
     def get_start_index(self):
        start_page= self.page.start_index() 
        return start_page
     def get_end_index(self):
        end_page= self.page.end_index()
        return end_page
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)    
     class Meta:
         model =  internal_transfer_history
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example'}
         fields=['counter','email','from_wallet','to_wallet','actual_amount','fees','amount','status','created_on']

class Internal_TransferFilter(django_filters.FilterSet):
    # user = django_filters.ModelChoiceFilter(queryset=User_Management.objects.all(),label ='User Name')
    email = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = internal_transfer_history
        fields=['email','from_wallet','created_on']
class Internal_TransferSearch_Form(FormHelper):
        model = internal_transfer_history
        form_id = 'Bill_Search_Form'
        form_method = 'get'
        form_class = 'form-horizontal'
        form_role = 'form'
        label_class = 'col-md-3'
        field_class = 'col-md-5'


