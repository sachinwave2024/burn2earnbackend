from django.shortcuts import render
from django.shortcuts import render


from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.list import ListView

from django.http.response import HttpResponseRedirect


from django.db import transaction

from django.contrib import messages


from trade_currency.models import TradeCurrency

from trade_currency.forms import TradeCurrencyForm
from trade_currency.tables import TradeCurrencyTable

from django.utils.decorators import method_decorator
from trade_admin_auth.mixins import check_group



class Listtradecurrency(ListView):
    model = TradeCurrency
    template_name = 'trade_master/generic_list_add.html'
    def get_queryset(self, **kwargs):
      return TradeCurrency.objects.all()
    def get_context_data(self,**kwargs):
        context=super(Listtradecurrency, self).get_context_data(**kwargs)
        context['Title'] = 'Currency List'
        content_qs = TradeCurrency.objects.all()
        context['content_qs'] =content_qs
        contenttable = TradeCurrencyTable(content_qs)
        context['table'] = contenttable
        context['activecls']='currencydetailadmin'
        context['add_title'] ='Add Currency'
        context['Btn_url'] = 'trade_currency:addcurrency'
        return context
    
    @method_decorator(check_group("Currency Management"))
    def dispatch(self, *args, **kwargs):
      return super(Listtradecurrency, self).dispatch(*args, **kwargs)


class Add_tradecurrency(CreateView):
    model = TradeCurrency
    form_class = TradeCurrencyForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(Add_tradecurrency, self).get_context_data(**kwargs)
       context['Title'] = 'Add Currency'
       context['Btn_url']='trade_currency:currencylist'
       context['activecls']='currencydetailadmin'
       return context
    
    @method_decorator(check_group("Currency Management"))
    def dispatch(self, *args, **kwargs):
      return super(Add_tradecurrency, self).dispatch(*args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
       form.instance.created_by_id = self.request.user.id
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Currency created successfully.')
       return HttpResponseRedirect('/tradecurrency/currencylist/')


class Update_tradecurrency(UpdateView):
    model = TradeCurrency
    form_class = TradeCurrencyForm
    template_name = 'trade_currency/currencyedit_form.html'  
    def get_context_data(self, **kwargs):
       context = super(Update_tradecurrency, self).get_context_data(**kwargs)
       context['Title'] = 'Edit Currency'
       context['Btn_url']='trade_currency:currencylist'
       context['activecls']='currencydetailadmin'
       return context
    
    @method_decorator(check_group("Currency Management"))
    def dispatch(self, *args, **kwargs):
      return super(Update_tradecurrency, self).dispatch(*args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'currency updated successfully.')
       return HttpResponseRedirect('/tradecurrency/currencylist/')


