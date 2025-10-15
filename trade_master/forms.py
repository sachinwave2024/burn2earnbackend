from django.forms import ModelForm
from django import forms


# from django.forms import ModelChoiceField

# from django.forms import widgets
# from betterforms.multiform import MultiModelForm,MultiForm
# from django.core.validators import MinValueValidator, MaxValueValidator
# from collections import OrderedDict

# from django.contrib.auth.models import User,Group
# from company.models import Company,Company_Settings

from trade_master.models import Cms_StaticContent,Faq,Contactus,EmailTemplate,SupportCategory
from trade_master.models import Roadmap,Currencylist



class ContentPageForm(forms.ModelForm):
    
    class Meta:
        model= Cms_StaticContent
        fields=['title', 'content']
        exclude=['name','contenttype','created_on','modified_on','status' ]



class FaqForm(forms.ModelForm):
    
    class Meta:
        model= Faq
        fields=['title', 'content','status']
        exclude=['created_on','modified_on', ]


class RoadmapForm(forms.ModelForm):
    
    class Meta:
        model= Roadmap
        fields=['title','year', 'content','status']
        exclude=['created_on','modified_on']


class CurrencyForm(forms.ModelForm):
    
    class Meta:
        model= Currencylist
        fields=['name','softcap', 'hardcap','timer_date','attachement']
        exclude=['created_on','modified_on','buytoken_url' ]


class ContactForm(forms.ModelForm):
    reply = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":40}),required=True)
    class Meta:
        model= Contactus
        fields=['reply',]
        exclude=['created_on','modified_on' ,'phone1','name','email','subject','message','read_status']

class EmailContentForm(forms.ModelForm):
    
    class Meta:
        model= EmailTemplate
        fields=['Subject','content']
        exclude=['created_on','modified_on','name']


# Support category form

class SupportCategoryForm(forms.ModelForm):
    class Meta:
        model= SupportCategory
        fields=['category','status']


