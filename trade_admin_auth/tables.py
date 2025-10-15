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

from django.contrib.auth.models import User
from API.models import Admin_Profit, Delete_Account_Management, Delete_Account_Reason_Management, Plan_purchase_wallet, Referral_reward, Withdraw, admin_notification_message, plan, referral_level, referral_table, withdraw_values,Reward_History
from trade_auth.models import Market_place

from trade_admin_auth.models import AdminUser_Profile,AdminUser_Activity, Steps_Management, Steps_history, Two_x_boost, User_Management, front_page_management

from trade_master.models import Blockip

def next_count():
    return next(counter)

         

class DeactivateUserTable(tables.Table):
     
     class Meta:
         model =  User
         orderable = False
         attrs = {'class': 'table table-bordered table-striped','id':'example'}
         fields=['username','email','is_active','']        

class DashboardAdminActivityTable(tables.Table):
     
     class Meta:
         model =  AdminUser_Activity
         orderable = False
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['user','ip_address','activity','browsername','os','devices','created_on']

class AdminActivityTable(tables.Table):
     counter = tables.Column(empty_values=(),verbose_name='S.No', orderable=False)
     def render_counter(self):
      self.row_counter = getattr(self, 'row_counter', itertools.count(self.page.start_index()))
      return next(self.row_counter)
     class Meta:
         model =  AdminUser_Activity
         orderable = False
         attrs = {'class': 'table table-bordered table-striped','id':'example'}
         fields=['counter','user','ip_address','activity','browsername','os','devices','created_on']

class AdminActivityTableFilter(django_filters.FilterSet):
    user = django_filters.ModelChoiceFilter(queryset=User.objects.all(),label ='Client Name')
    
    class Meta:
        model = AdminUser_Activity
        fields=['user']
class AdminActivitySearch_Form(FormHelper):
        model = AdminUser_Activity
        form_id = 'Bill_Search_Form'
        form_method = 'get'
        form_class = 'form-horizontal'
        form_role = 'form'
        label_class = 'col-md-3'
        field_class = 'col-md-5'



class BlockIPTable(tables.Table):
     
     BUTTON_TEMPLATE = """

        <a href="/tradeadmin/editblockip/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>
     
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)    
     class Meta:
         model =  Blockip
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','ip_address','ip_level','status'] 

'''
class UserAddressTable(tables.Table):
     BUTTON_TEMPLATE = """

        <a href="/tradeadmin/walletdetail/{{record.id}}/" title="Edit"><i class="fa fa-info"></i></a>
     
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )

     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',) 
     class Meta:
         model =  UserAddress
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','useraddress','created_on','modified_on']
'''

class Step_Management_Table(tables.Table):
     
     BUTTON_TEMPLATE = """

        <a href="/tradeadmin/edit_Step_Management/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>
     
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)    
     class Meta:
         model =  Steps_Management
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','step_value','Step_discount','Step_counter_Discount','free_plan_days']   

class Referral_reward_Table(tables.Table):
     
     BUTTON_TEMPLATE = """

        <a href="/tradeadmin/Edit_Referral_Reward_Management/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>
     
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)    
     class Meta:
         model =  Referral_reward
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','Reward','status']


class Two_x_boost_Table(tables.Table):
     
     BUTTON_TEMPLATE = """

        <a href="/tradeadmin/Edit_2X_Management/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>
     
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)    
     class Meta:
         model =  Two_x_boost
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','daily_min','status']

class User_Management_Table(tables.Table):
     
     BUTTON_TEMPLATE = """

        <a href="/tradeadmin/Edit_User_Management/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>
     
     """
     
     BUTTON_TEMPLATE8 = """

        <a href="/tradeadmin/User_Wallet_Address_Detail/{{record.id}}/" title="Detail"><i class="fa fa-list"></i></a>
     
     """
     BUTTON_TEMPLATE1 = """

        <a href="/tradeadmin/user_history_table/{{record.id}}/" title="Edit"><i class="fa fa-history"></i></a>
     
     """

     BUTTON_TEMPLATE3 = """

        <a href="/tradeadmin/Add_User_Plan/{{record.id}}/" title="Edit"><i class="fa fa-briefcase"></i></a>
     
     """

     BUTTON_TEMPLATE4 = """

        <a href="/tradeadmin/step_update_user/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>

     
     """

     BUTTON_TEMPLATE5 = """

    <a href="/tradeadmin/user_referal_history_table/{{record.id}}/" title="Edit"><i class="fa fa-history"></i></a>

    
    """


     BUTTON_TEMPLATE6 = """

        <a href="/tradeadmin/missing_reward_update_admin/{{record.id}}/" title="Edit"><i class="fa fa-history"></i></a>

    
    """
     
     BUTTON_TEMPLATE7 = """

        <a href="/stake/user_stake_history_table/{{record.id}}/" title="Staking History"><i class="fa fa-history"></i></a>

     
     """
     
     
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     
     Wallet_address = tables.TemplateColumn(BUTTON_TEMPLATE8,orderable=False )

     History = tables.TemplateColumn(BUTTON_TEMPLATE1,orderable=False )

     Add_Plan = tables.TemplateColumn(BUTTON_TEMPLATE3,orderable=False )

     Step_Update = tables.TemplateColumn(BUTTON_TEMPLATE4,orderable=False )

     Referal_History = tables.TemplateColumn(BUTTON_TEMPLATE5,orderable=False )

     Missing_reward_update = tables.TemplateColumn(BUTTON_TEMPLATE6,orderable=False )

     Staking_history = tables.TemplateColumn(BUTTON_TEMPLATE7,orderable=False )
     
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
         model =  User_Management
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example'}
         fields=['counter','Name','Email','Referral_id','Direct_referral_id','phone_number','user_profile_pic','created_on','User_type']

class UserManagementFilter(django_filters.FilterSet):
    # user = django_filters.ModelChoiceFilter(queryset=User_Management.objects.all(),label ='User Name')
    Name = django_filters.CharFilter(lookup_expr='icontains')
    Email = django_filters.CharFilter(lookup_expr='icontains')
    Referral_id = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = User_Management
        fields=['Name','Email','Referral_id']
class UserManagementSearch_Form(FormHelper):
        model = User_Management
        form_id = 'Bill_Search_Form'
        form_method = 'get'
        form_class = 'form-horizontal'
        form_role = 'form'
        label_class = 'col-md-3'
        field_class = 'col-md-5'

class Steps_history_Table(tables.Table):
     
     BUTTON_TEMPLATE = """

        # <a href="/tradeadmin/Edit_User_Management/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>
     
     """
    
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)    
     class Meta:
         model =  Steps_history 
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','user','steps','created_on']

class Delete_Account_Reason_Management_Table(tables.Table):
     
     BUTTON_TEMPLATE = """

        <a href="/tradeadmin/Edit_Delete_Reason_Management/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>
     
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)    
     class Meta:
         model =  Delete_Account_Reason_Management 
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','Delete_reason','status']

class Delete_Account_Request_Management_Table(tables.Table):
     
     BUTTON_TEMPLATE = """

        # <a href="/tradeadmin/Detail_Delete_Request/{{record.id}}/" title="Edit"><i class="fa fa-eye"></i></a>
     
     """
    #  Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)    
     class Meta:
         model =  Delete_Account_Management 
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','user','Delete_Account','reason','status']


# class Withdraw_Request_Table(tables.Table):
     
#      BUTTON_TEMPLATE = """

#          <a href="/tradeadmin/Edit_User_Management/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>
     
#      """
#      Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
#      def render_counter(self):
#       self.row_counter = getattr(self, 'row_counter', itertools.count(self.page.start_index()))
#       return next(self.row_counter)
#      def get_start_index(self):
#         start_page= self.page.start_index() 
#         return start_page
#      def get_end_index(self):
#         end_page= self.page.end_index()
#         return end_page
#      counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)    
#      class Meta:
#          model =  Withdraw 
#          orderable = True
#          attrs = {'class': 'table table-bordered table-striped','id':'example2'}
#          fields=['counter','userid','Amount','Withdraw_fee','Withdraw_USDT','Withdraw_JW','Address','status']


class Admin_Profit_Table(tables.Table):
    
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
         model =  Admin_Profit 
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example'}
         fields=['counter','user','admin_profit','Profit_type','created_on']



class AdminProfitFilter(django_filters.FilterSet):
    # user = django_filters.ModelChoiceFilter(queryset=User_Management.objects.all(),label ='User Name')
    user = django_filters.CharFilter(lookup_expr='icontains', field_name='user__user_name')
    # Email = django_filters.CharFilter(lookup_expr='icontains')
    # Referral_id = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Admin_Profit
        fields=['user']
class AdminProfitSearch_Form(FormHelper):
        model = Admin_Profit
        form_id = 'Bill_Search_Form'
        form_method = 'get'
        form_class = 'form-horizontal'
        form_role = 'form'
        label_class = 'col-md-3'
        field_class = 'col-md-5'


class Plan_Table(tables.Table):
     
     BUTTON_TEMPLATE = """

         <a href="/tradeadmin/Edit_Plan_Management/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>&nbsp;&nbsp;

         <a href="{% url 'trade_admin_auth:Delete_Plan' record.id %}" title="Delete" class="btn btn-danger btn-xs">Delete</a>
     
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)    
     class Meta:
         model =  plan 
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','plan_name','plan_purchase_amount_monthly','plan_purchase_amount_quarterly','plan_purchase_amount_annual','Max_step_count','reward_amount','referral_status','withdraw_status','status','Actions']



class Referral_level_Table(tables.Table):
     
     BUTTON_TEMPLATE = """

         <a href="/tradeadmin/Edit_Referral_level_Management/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>&nbsp;&nbsp;

         <a href="{% url 'trade_admin_auth:Delete_Referral' record.id %}" title="Delete" class="btn btn-danger btn-xs">Delete</a>

     
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
  
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)   
     class Meta:
         model =  referral_level 
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','referral_level_id','direct_level_id','commission_amount','second_level_commission_amount','status']



         
# class Referral_level_Table(tables.Table):
#     BUTTON_TEMPLATE = """
#         <a href="/tradeadmin/Edit_Referral_level_Management/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>&nbsp;&nbsp;
#         <a href="{% url 'trade_admin_auth:Delete_Referral' record.id %}" title="Delete" class="btn btn-danger btn-xs">Delete</a>
#     """
#     Actions = tables.TemplateColumn(BUTTON_TEMPLATE, orderable=False)
    
#     def render_counter(self, record):
#         records = list(self.data)
#         index = records.index(record)
#         counter = index + 1
#         return counter
  
#     def render_direct_level_id(self, record):
#         # Example: Render 'N/A' if direct_level_id is None
#         if record.direct_level_id is None:
#             return 0
#         else:
#             # Add your custom conditions here
#             # Example: Render the direct_level_id value if it meets certain criteria
#             if record.direct_level_id > 10:
#                 return record.direct_level_id
#             else:
#                 return 'Condition not met'
            
#     counter = tables.Column(verbose_name='S.No', orderable=False, accessor='pk')   
   
#     class Meta:
#         model = referral_level 
#         orderable = True
#         attrs = {'class': 'table table-bordered table-striped', 'id': 'example2'}
#         fields = ['counter', 'referral_level_id', 'direct_level_id', 'commission_amount', 'second_level_commission_amount', 'status']         
         
         

class User_Referral_Table(tables.Table):
     
     BUTTON_TEMPLATE = """

         <a href="/tradeadmin/Edit_Plan_Management/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>&nbsp;&nbsp;

         <a href="{% url 'trade_admin_auth:Delete_Plan' record.id %}" title="Delete" class="btn btn-danger btn-xs">Delete</a>
     
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)    
     class Meta:
         model =  referral_table 
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','user_id','Referral_id','Referral_Level','Direct_referral_id','Direct_referral_user_level','Actions']


class List_market_internal_Table(tables.Table):
     
     BUTTON_TEMPLATE = """

         <a href="/tradeadmin/Edit_market_internal_Management/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>&nbsp;&nbsp;

        
     
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)    
     class Meta:
         model =  Market_place 
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','Google_status','internal_transfer','Actions']

class List_withdraw_Value_Table(tables.Table):
     
     BUTTON_TEMPLATE = """

         <a href="/tradeadmin/Edit_Withdraw_value_Management/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>&nbsp;&nbsp;

        
     
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)    
     class Meta:
         model =  withdraw_values 
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','first_withdraw_value','Health_wallet_minimum_withdraw_limit','Health_wallet_maximum_withdraw_limit','Referral_wallet_minimum_withdraw_limit','Referral_wallet_maximum_withdraw_limit','Minimum_BNB_Balance','Actions']


class Wallet_Table(tables.Table):
     
     BUTTON_TEMPLATE = """

         <a href="/tradeadmin/Edit_List_wallet/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>
     
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)    
     class Meta:
         model =  Plan_purchase_wallet 
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','Health_wallet_plan','Health_wallet_Withdraw','Referral_wallet_plan','Referral_wallet_Withdraw','Trust_wallet_plan']


class List_admin_notification_message_Table(tables.Table):
     
     BUTTON_TEMPLATE = """

         <a href="/tradeadmin/Edit_admin_notification_message/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>&nbsp;&nbsp;
     
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)    
     class Meta:
         model =  admin_notification_message 
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','Notification_message','Notification_status','Actions']


class List_front_page_management_Table(tables.Table):
     
     BUTTON_TEMPLATE = """

         <a href="/tradeadmin/Edit_front_page_management/{{record.id}}/" title="Edit"><i class="fa fa-edit"></i></a>&nbsp;&nbsp;
     
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)    
     class Meta:
         model =  front_page_management 
         orderable = True
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','Front_user_count','status','Actions']

