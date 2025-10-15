from django.forms import ModelForm
from django import forms

from Staking.models import Stake_referral_management, staking_admin_management






class Stake_Plan_Form(forms.ModelForm):
    
    class Meta:
        model = staking_admin_management
        fields = ['stake_period','reward_percent','minimum_stake','maximum_stake','minimum_withdraw','maximum_withdraw','withdraw_status','minimum_withdraw_referal','maximum_withdraw_referal','status','eligible_plan','stake_wallet_percentage','withdraw_wallet_percentage']
        exclude = ['created_on','modified_on']


class Stake_Referral_Form(forms.ModelForm):
    
    class Meta:
        model = Stake_referral_management
        fields = ['levels','self_stake_Amount','self_stake_Amount_range','first_level_stake','secound_level_stake','status']
        exclude = ['created_on','modified_on']