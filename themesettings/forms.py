'''
from django import forms

from trade_master.models import Contactus


class Contactform(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),required = True)
    class Meta:
        model= Contactus
        fields='__all__'
        exclude=['created_on','modified_on','reply','status','read_status',]
'''