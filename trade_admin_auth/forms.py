# from django.forms import ModelForm
# from django import forms
# from django.contrib.auth.forms import UserCreationForm,PasswordResetForm

# # from django.forms import ModelChoiceField

# from django.forms import widgets
# from django.core.exceptions import ValidationError

# from django.contrib.auth.models import User
# from API.models import Plan_purchase_wallet, Referral_reward,Delete_Account_Reason_Management, admin_notification_message, plan, referral_level, referral_table, withdraw_values
# from company.models import Company,Company_Settings
# from trade_auth.models import Market_place
# from trade_admin_auth.models import AdminUser_Profile, Steps_Management, Two_x_boost, User_Management, front_page_management

# from betterforms.multiform import MultiModelForm
# from django.core.validators import MinValueValidator
# from collections import OrderedDict
# from django.contrib.auth.forms import UserCreationForm

# from trade_master.models import Blockip
# from API.views import encrypt_with_common_cipher


# class Passwordreset(PasswordResetForm):
#     class Meta:
#         model = User
#         fields = ['email']

# class SetPasswordForm1(forms.Form):
#     new_password1 = forms.CharField(widget=forms.PasswordInput),
#     new_password2 = forms.CharField(widget=forms.PasswordInput)
    
#     def clean_new_password2(self):
#         password1 = self.cleaned_data.get('new_password1')
#         passowrd2 = self.cleaned_data.get('new_password2')
#         if password1 and passowrd2:
#             if len(passowrd2) < 8:
#                 raise forms.ValidationError(
#                     self.error_messages['password_length'],
#                     code='password_length',
#                 )
#             if password1 != password2:
#                 raise forms.ValidationError(
#                         self.error_messages['password_mismatch'],
#                         code='password_mismatch'
#                     )
#         return passowrd2
#     error_messages = {
#     'password_length' : ("Password Must Have 8 Characters"),
#     'password_mismatch' : ("Two Password Fieslds Does not match")
#     }



# class SetPasswordForm(forms.Form):
    
#     error_messages = {
#         'password_mismatch': ("The two password fields didn't match."),
#         }
#     new_password1 = forms.CharField(label=("New password * "),
#                                     widget=forms.PasswordInput)
#     new_password2 = forms.CharField(label=("New password confirmation * "),
#                                     widget=forms.PasswordInput)

#     def clean_new_password2(self):
#         password1 = self.cleaned_data.get('new_password1')
#         password2 = self.cleaned_data.get('new_password2')
#         if password1 and password2:
#             if password1 != password2:
#                 raise forms.ValidationError(
#                     self.error_messages['password_mismatch'],
#                     code='password_mismatch',
#                     )
#         return password2


# class EditCompanyForm(forms.ModelForm):
#     class Meta:
#         model= Company
        
#         fields=['name','email','phone1','company_logo','company_fav','copy_right','telegram','fb','twitter','instagram','linkedin','session_timeout','Device_id_status','support_address','withdraw_type','Android_version']

#         exclude=['created_on','modified_on','state','admin_redirect','address1','city','country','postcode']

# class EditCompanySettingsForm(forms.ModelForm):
    
#     site_maintenance = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 30}),required = False)
#     class Meta:
#         model= Company_Settings
        
#         fields=['site_maintenance_status','IOS_site_maintenance_status','adminipaddress']

#         exclude=['company_settings_name','site_maintenance']


# class EditCompanyMultiForm(MultiModelForm):
    
#     form_classes = {
#         'form1': EditCompanyForm,
#         'form2': EditCompanySettingsForm,
#     }



# class AdminUserAddForm(UserCreationForm):
#     class Meta:
#         model= User
#         fields=['username','password1', 'password2',]
#         exclude=['is_staff','first_name', 'last_name', 'email']

    


# class AdminUserProfileAddform(forms.ModelForm):
#     emailaddress = forms.CharField(required = True,label='Email ')
#     pattern_code = forms.CharField(initial='',widget=forms.widgets.HiddenInput(),required=True)
#     def clean_emailaddress(self):
#         emailaddress = self.cleaned_data.get('emailaddress') 
#         encrypt_username=encrypt_with_common_cipher(emailaddress)
#         if AdminUser_Profile.objects.filter(emailaddress=encrypt_username).count() > 0:

#             raise forms.ValidationError(u'This email address is already registered.')
#         return emailaddress
#     class Meta:
#         model= AdminUser_Profile
#         fields='__all__'
#         exclude=['created_on','modified_on','user','state','role','address1',
#         'address2','date_of_birth','referal_status','referal_code','refer_by_id','referal_user_by','status',
#         'gender','phone1','photo','city','emailaddress','country','postcode','country_code','google_id','pattern_status'
#         ]



# class AdminUserAddMultiForm(MultiModelForm):
#     form_classes = {
#         'form1': AdminUserAddForm,
#         'form2': AdminUserProfileAddform,
        
#         }

# class AdminUserEditsubForm(UserCreationForm):
#     email = forms.CharField(required = True)
    
    

#     class Meta:
#         model= User
#         fields=['username', 'email','password1', 'password2',]
#         exclude=['is_staff','first_name', 'last_name', ]
# class AdminSubadmineditform(forms.ModelForm):
  
    
#     class Meta:
#         model= AdminUser_Profile
#         fields='__all__'
#         exclude=['created_on','modified_on','user','state','role','address1',
#         'address2','date_of_birth','referal_status','referal_code','refer_by_id','referal_user_by','status',
#         'gender','phone1','photo','city','country','postcode','country_code','google_id'
#         ]

# class AdminUserEditSubadminMultiForm(MultiModelForm):
#     form_classes = {
#         'form1': AdminUserEditsubForm,
#         'form2': AdminSubadmineditform,
        
#         }

# class AdminUserProfileeditform(forms.ModelForm):
  
    
#     class Meta:
#         model= AdminUser_Profile
#         fields=['emailaddress','phone1','photo']
#         exclude=['user_id','created_on','modified_on','user','state','role',
#         'address2','date_of_birth','pattern_code'
#         ,'gender','address1','city','country','postcode','list_country','country_code','authy_id','google_id'
#         ]


# class AdminUserEditForm(forms.ModelForm):
#     email = forms.CharField(required = True)
    
#     class Meta:
#         model= User
#         fields=['email','username']
#         exclude=['is_staff','first_name', 'last_name','password1', 'password2',]

# class AdminUserEditMultiForm(MultiModelForm):
#     form_classes = {
#         'form1': AdminUserEditForm,
#         'form2':AdminUserProfileeditform
#         }


# class SubAdminUserProfileeditform(forms.ModelForm):
  
#     class Meta:
#         model= AdminUser_Profile
#         fields=['emailaddress','user']
#         exclude=['photo','created_on','modified_on','user','state','role',
#         'address2','date_of_birth','pattern_code'
#         ,'gender','address1','city','country','postcode','list_country','country_code','authy_id','google_id'
#         ]

# class ChangePatternForm(forms.ModelForm):

#     pattern_code = forms.CharField(initial=0,widget=forms.widgets.HiddenInput())
#     class Meta:
#         model= AdminUser_Profile
#         fields='__all__'
#         exclude=['created_on','modified_on','user','state','role',
#         'address2','date_of_birth','refer_id','refer_user_id','refer_by_id','activation_date',
#         'address1','city','country','postcode','phone1','gender','photo','country_code','authy_id','google_id'
#         ]

# class GoogleTokenVerificationForm(forms.Form):
#     token = forms.CharField(required=True,label='TwoFA Code')

# class BlockipForm(forms.ModelForm):
    
#     class Meta:
#         model = Blockip
#         fields = ['ip_address','ip_option','ip_level','status']
#         exclude = ['created_on','modified_on']

# class Delete_aAccount_Reason_Form(forms.ModelForm):
    
#     class Meta:
#         model = Delete_Account_Reason_Management
#         fields = ['Delete_reason','status']
#         exclude = ['created_on','modified_on']

# class Steps_Management_Form(forms.ModelForm):
    
#     class Meta:
#         model = Steps_Management
#         fields = ['step_value','free_plan_days','Step_discount','Step_counter_Discount']
#         exclude = ['created_on','modified_on']

# class Two_x_boost_Form(forms.ModelForm):
    
#     class Meta:
#         model = Two_x_boost
#         fields = ['daily_min','status']
#         exclude = ['created_on','modified_on']

# class User_Management_Form(forms.ModelForm):
    
#     class Meta:
#         model = User_Management
#         fields = ['user_name','Email','Name','user_profile_pic','user_phone_number','status','device_unique_id','notes']
#         exclude = ['created_on','modified_on']

# class Referral_Reward_Form(forms.ModelForm):
    
#     class Meta:
#         model = Referral_reward
#         fields = ['Reward','status']
#         exclude = ['created_on','modified_on']

# class Plan_Form(forms.ModelForm):
    
#     class Meta:
#         model = plan
#         fields = ['plan_type','plan_name','plan_purchase_amount_monthly','plan_purchase_amount_quarterly','plan_purchase_amount_annual','Min_step_count','Max_step_count','reward_amount','Reward_step_value','referral_status','level','referral_level_eligible','withdraw_status','health_withdraw_minimum_limit','health_withdraw_maximum_limit','plan_reward_amount','referral_withdraw_minimum_limit','referral_withdraw_maximum_limit','Total_maximum_limit','stake_wallet_monthly_percentage','withdraw_wallet_monthly_percentage','status','stake_wallet_monthly_percentage','withdraw_wallet_monthly_percentage','plan_purchase_type','user_stake_credit','activate_plan','health_wallet_status','referral_wallet_status','trust_wallet_status','support_status',"monthly_support_status",'quarterly_support_status','halfyearly_support_status','annual_support_status','monthly_support_amount','quarterly_support_amount','halfyearly_support_amount','annual_support_amount']
#         exclude = ['created_on','modified_on']


# class Referral_Level_Form(forms.ModelForm):
    
#     class Meta:
#         model = referral_level
#         fields = ['referral_level_id','commission_amount','second_level_commission_amount','status']


# class User_Referral_Level_Form(forms.ModelForm):
    
#     class Meta:
#         model = referral_table
#         fields = ['user_id','Referral_id','Referral_Level','Direct_referral_id','Direct_referral_user_level']


# class Market_Internal_Form(forms.ModelForm):
    
#     class Meta:
#         model = Market_place
#         fields = ['Google_status','internal_transfer']

# class withdraw_values_Form(forms.ModelForm):
    
#     class Meta:
#         model = withdraw_values
#         fields = ['first_withdraw_value','Health_wallet_minimum_withdraw_limit','Health_wallet_maximum_withdraw_limit','Referral_wallet_minimum_withdraw_limit','Referral_wallet_maximum_withdraw_limit','Minimum_BNB_Balance']


# class List_Wallet_Form(forms.ModelForm):
    
#     class Meta:
#         model = Plan_purchase_wallet
#         fields = ['Health_wallet_plan','Health_wallet_Withdraw','Referral_wallet_plan','Referral_wallet_Withdraw','Trust_wallet_plan']


# class admin_notification_message_Form(forms.ModelForm):
    
#     class Meta:
#         model = admin_notification_message
#         fields = ['Notification_message','Google_fit_message','Step_counter_message','Notification_status']


# class front_page_management_Form(forms.ModelForm):
    
#     class Meta:
#         model = front_page_management
#         fields = ['Front_user_count','status']
#         exclude = ['created_on','modified_on']
        

# from API.models import Admin_Block_Main_Withdraw

# class EmailForm(forms.ModelForm):
#     class Meta:
#         model = Admin_Block_Main_Withdraw
#         fields = ['Email', 'status']


from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm

# from django.forms import ModelChoiceField

from django.forms import widgets
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from API.models import Plan_purchase_wallet, Referral_reward,Delete_Account_Reason_Management, admin_notification_message, plan, referral_level, referral_table, withdraw_values
from company.models import Company,Company_Settings
from trade_auth.models import Market_place
from trade_admin_auth.models import AdminUser_Profile, Steps_Management, Two_x_boost, User_Management, front_page_management

from betterforms.multiform import MultiModelForm
from django.core.validators import MinValueValidator
from collections import OrderedDict
from django.contrib.auth.forms import UserCreationForm

from trade_master.models import Blockip
from API.views import encrypt_with_common_cipher


class Passwordreset(PasswordResetForm):
    class Meta:
        model = User
        fields = ['email']

class SetPasswordForm1(forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput),
    new_password2 = forms.CharField(widget=forms.PasswordInput)
    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        passowrd2 = self.cleaned_data.get('new_password2')
        if password1 and passowrd2:
            if len(passowrd2) < 8:
                raise forms.ValidationError(
                    self.error_messages['password_length'],
                    code='password_length',
                )
            if password1 != password2:
                raise forms.ValidationError(
                        self.error_messages['password_mismatch'],
                        code='password_mismatch'
                    )
        return passowrd2
    error_messages = {
    'password_length' : ("Password Must Have 8 Characters"),
    'password_mismatch' : ("Two Password Fieslds Does not match")
    }



class SetPasswordForm(forms.Form):
    
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=("New password * "),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation * "),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2


class EditCompanyForm(forms.ModelForm):
    class Meta:
        model= Company
        
        fields=['name','email','phone1','company_logo','company_fav','copy_right','telegram','fb','twitter','instagram','linkedin','session_timeout','Device_id_status','support_address','withdraw_type','Android_version','IOS_version','privatekey','securitykey','withaddress','facebookpromo','instapromo','twitterpromo','cmcpromo']

        exclude=['created_on','modified_on','state','admin_redirect','address1','city','country','postcode']



class EditCompanySettingsForm(forms.ModelForm):
    
    site_maintenance = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 30}),required = False)
    class Meta:
        model= Company_Settings
        
        fields=['site_maintenance_status','IOS_site_maintenance_status','adminipaddress']

        exclude=['company_settings_name','site_maintenance']


class EditCompanyMultiForm(MultiModelForm):
    
    form_classes = {
        'form1': EditCompanyForm,
        'form2': EditCompanySettingsForm,
    }



class AdminUserAddForm(UserCreationForm):
    class Meta:
        model= User
        fields=['username','password1', 'password2',]
        exclude=['is_staff','first_name', 'last_name', 'email']

    


class AdminUserProfileAddform(forms.ModelForm):
    emailaddress = forms.CharField(required = True,label='Email ')
    pattern_code = forms.CharField(initial='',widget=forms.widgets.HiddenInput(),required=True)
    def clean_emailaddress(self):
        emailaddress = self.cleaned_data.get('emailaddress')
        encrypt_username=encrypt_with_common_cipher(emailaddress)
        if AdminUser_Profile.objects.filter(emailaddress=encrypt_username).count() > 0:

            raise forms.ValidationError(u'This email address is already registered.')
        return emailaddress
    class Meta:
        model= AdminUser_Profile
        fields='__all__'
        exclude=['created_on','modified_on','user','state','role','address1',
        'address2','date_of_birth','referal_status','referal_code','refer_by_id','referal_user_by','status',
        'gender','phone1','photo','city','emailaddress','country','postcode','country_code','google_id','pattern_status'
        ]



class AdminUserAddMultiForm(MultiModelForm):
    form_classes = {
        'form1': AdminUserAddForm,
        'form2': AdminUserProfileAddform,
        
        }

class AdminUserEditsubForm(UserCreationForm):
    email = forms.CharField(required = True)
    
    

    class Meta:
        model= User
        fields=['username', 'email','password1', 'password2',]
        exclude=['is_staff','first_name', 'last_name', ]
class AdminSubadmineditform(forms.ModelForm):
  
    
    class Meta:
        model= AdminUser_Profile
        fields='__all__'
        exclude=['created_on','modified_on','user','state','role','address1',
        'address2','date_of_birth','referal_status','referal_code','refer_by_id','referal_user_by','status',
        'gender','phone1','photo','city','country','postcode','country_code','google_id'
        ]

class AdminUserEditSubadminMultiForm(MultiModelForm):
    form_classes = {
        'form1': AdminUserEditsubForm,
        'form2': AdminSubadmineditform,
        
        }

class AdminUserProfileeditform(forms.ModelForm):
  
    
    class Meta:
        model= AdminUser_Profile
        fields=['emailaddress','phone1','photo']
        exclude=['user_id','created_on','modified_on','user','state','role',
        'address2','date_of_birth','pattern_code'
        ,'gender','address1','city','country','postcode','list_country','country_code','authy_id','google_id'
        ]


class AdminUserEditForm(forms.ModelForm):
    email = forms.CharField(required = True)
    
    class Meta:
        model= User
        fields=['email','username']
        exclude=['is_staff','first_name', 'last_name','password1', 'password2',]

class AdminUserEditMultiForm(MultiModelForm):
    form_classes = {
        'form1': AdminUserEditForm,
        'form2':AdminUserProfileeditform
        }


class SubAdminUserProfileeditform(forms.ModelForm):
  
    class Meta:
        model= AdminUser_Profile
        fields=['emailaddress','user']
        exclude=['photo','created_on','modified_on','user','state','role',
        'address2','date_of_birth','pattern_code'
        ,'gender','address1','city','country','postcode','list_country','country_code','authy_id','google_id'
        ]

class ChangePatternForm(forms.ModelForm):

    pattern_code = forms.CharField(initial=0,widget=forms.widgets.HiddenInput())
    class Meta:
        model= AdminUser_Profile
        fields='__all__'
        exclude=['created_on','modified_on','user','state','role',
        'address2','date_of_birth','refer_id','refer_user_id','refer_by_id','activation_date',
        'address1','city','country','postcode','phone1','gender','photo','country_code','authy_id','google_id'
        ]

class GoogleTokenVerificationForm(forms.Form):
    token = forms.CharField(required=True,label='TwoFA Code')

class BlockipForm(forms.ModelForm):
    
    class Meta:
        model = Blockip
        fields = ['ip_address','ip_option','ip_level','status']
        exclude = ['created_on','modified_on']

class Delete_aAccount_Reason_Form(forms.ModelForm):
    
    class Meta:
        model = Delete_Account_Reason_Management
        fields = ['Delete_reason','status']
        exclude = ['created_on','modified_on']

class Steps_Management_Form(forms.ModelForm):
    
    class Meta:
        model = Steps_Management
        fields = ['step_value','free_plan_days','Step_discount','Step_counter_Discount']
        exclude = ['created_on','modified_on']

class Two_x_boost_Form(forms.ModelForm):
    
    class Meta:
        model = Two_x_boost
        fields = ['daily_min','status']
        exclude = ['created_on','modified_on']

class User_Management_Form(forms.ModelForm):
    
    class Meta:
        model = User_Management
        fields = ['user_name','Email','Name','user_profile_pic','user_phone_number','status','device_unique_id','notes','USER_INRID']
        exclude = ['created_on','modified_on']

class Referral_Reward_Form(forms.ModelForm):
    
    class Meta:
        model = Referral_reward
        fields = ['Reward','status']
        exclude = ['created_on','modified_on']

class Plan_Form(forms.ModelForm):
    
    class Meta:
        model = plan
        fields = ['plan_type','plan_name','plan_purchase_amount_monthly','plan_purchase_amount_quarterly','plan_purchase_amount_annual','Min_step_count','Max_step_count','reward_amount','Reward_step_value','referral_status','level','referral_level_eligible','withdraw_status','health_withdraw_minimum_limit','health_withdraw_maximum_limit','plan_reward_amount','referral_withdraw_minimum_limit','referral_withdraw_maximum_limit','Total_maximum_limit','stake_wallet_monthly_percentage','withdraw_wallet_monthly_percentage','status','stake_wallet_monthly_percentage','withdraw_wallet_monthly_percentage','plan_purchase_type','user_stake_credit','activate_plan','health_wallet_status','referral_wallet_status','trust_wallet_status','support_status',"monthly_support_status",'quarterly_support_status','halfyearly_support_status','annual_support_status','monthly_support_amount','quarterly_support_amount','halfyearly_support_amount','annual_support_amount','premium_wallet_status']
        exclude = ['created_on','modified_on']


class Referral_Level_Form(forms.ModelForm):
    
    class Meta:
        model = referral_level
        fields = ['referral_level_id','commission_amount','second_level_commission_amount','status']


class User_Referral_Level_Form(forms.ModelForm):
    
    class Meta:
        model = referral_table
        fields = ['user_id','Referral_id','Referral_Level','Direct_referral_id','Direct_referral_user_level']


class Market_Internal_Form(forms.ModelForm):
    
    class Meta:
        model = Market_place
        fields = ['Google_status','internal_transfer']

class withdraw_values_Form(forms.ModelForm):
    
    class Meta:
        model = withdraw_values
        fields = ['first_withdraw_value','Health_wallet_minimum_withdraw_limit','Health_wallet_maximum_withdraw_limit','Referral_wallet_minimum_withdraw_limit','Referral_wallet_maximum_withdraw_limit','Minimum_BNB_Balance']


class List_Wallet_Form(forms.ModelForm):
    
    class Meta:
        model = Plan_purchase_wallet
        fields = ['Health_wallet_plan','Health_wallet_Withdraw','Referral_wallet_plan','Referral_wallet_Withdraw','Trust_wallet_plan']


class admin_notification_message_Form(forms.ModelForm):
    
    class Meta:
        model = admin_notification_message
        fields = ['Notification_message','Google_fit_message','Step_counter_message','Notification_status']


class front_page_management_Form(forms.ModelForm):
    
    class Meta:
        model = front_page_management
        fields = ['Front_user_count','status']
        exclude = ['created_on','modified_on']
        
        
from API.models import Admin_Block_Main_Withdraw

class EmailForm(forms.ModelForm):
    class Meta:
        model = Admin_Block_Main_Withdraw
        fields = ['Email', 'status']



