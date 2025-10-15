from django.forms import ModelForm
from django import forms

from trade_currency.models import TradeCurrency




class TradeCurrencyForm(forms.ModelForm):
    
    class Meta:
        model= TradeCurrency
        fields=['name','symbol','currency_image','currncytype','status','withdraw_feestype','withdraw_fees']
        exclude=['big_image','created_on','modified_on','created_by','modified_by','deposit_status','withdraw_status',
        'deposit_content','withdraw_content','deposit_maintenance','withdraw_maintenance','deposit_alert','withdraw_alert',
        'alert_deposit','lend_status','lending_min','lend_duration','lend_loanrate','countryname' 
        ,'depositcontent_three','depositcontent_two','withdrawcontent_two','trans_min','balance_minimum','min_deposit','max_deposi','min_withdraw','max_withdraw',]
