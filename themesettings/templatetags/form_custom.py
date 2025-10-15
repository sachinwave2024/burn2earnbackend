from django import template
register = template.Library()
import re
import datetime
from decimal import Decimal
import json

import os
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
today = datetime.date.today()


@register.filter('fieldtype')
def fieldtype(field):
    return field.field.widget.__class__.__name__

@register.filter('req_label')
def req_label(field):
    return field.field.widget.is_required
    

@register.filter('field_label')
def field_label(field):
    Field_Type = field.field.widget.__class__.__name__
    Field_class = 'input'
    if (Field_Type == 'Select'):
        Field_class = 'select'
    elif( Field_Type == 'SelectMultiple'):
        Field_class = ''
    elif Field_Type == 'Textarea':
        Field_class =    'textarea'
    elif Field_Type == 'TextInput':
        Field_class =    'input'
    elif Field_Type == 'CheckboxInput':
        Field_class = 'select'
        
    elif Field_Type == 'FileInput':
        Field_class = 'input input-file'
    else:
        Field_class = 'input'

    return Field_class


@register.filter('get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter('get_value')
def get_value(dictionary, key):
    return getattr(dictionary,key)

@register.filter
def formset_filter(value):
    arg = value.split("id_form-")
    return arg[1][0] 

@register.filter
def split_file_name(value):
    arg = value.name.split("/")
    return arg[1]

@register.filter
def avg_filter(value,arg):
    try: 
        result = value/arg
    except ZeroDivisionError:
        result = 0
    return round(result,2)

@register.filter
def multiple_filter(value,arg):
    result = Decimal(value) * Decimal(arg)
    return round(result,2)

@register.filter
def total_avg_filter(value,arg):
    try: 
        avg = value/arg
        result = avg/arg
        
    except ZeroDivisionError:
        result = 0
    return round(result,2) 

@register.simple_tag
def get_verbose_field_name(instance, field_name):
    value=''
    if instance:
        return instance._meta.get_field(field_name).verbose_name.title()
    else:
        return value
        
@register.simple_tag
def update_variable(value):
    return value


