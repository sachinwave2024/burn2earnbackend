
from django.shortcuts import render,get_object_or_404
from django.conf import settings
from django.http import HttpResponseRedirect


from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View


from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.http import JsonResponse

import datetime

from Crypto.Cipher import AES
import base64
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from django.db.models import Q


from django.db import transaction

from django.contrib import messages



from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives

from company.models import Company


from django.utils.decorators import method_decorator
from trade_admin_auth.mixins import check_group,check_group_sub_menu
from trade_admin_auth.mixins import CmsAdminRequiredMixin,FaqAdminRequiredMixin,ContactusAdminRequiredMixin
from trade_admin_auth.mixins import EmailTemplateAdminRequiredMixin,RoadmapAdminRequiredMixin,CurrencyAdminRequiredMixin

from django_tables2 import RequestConfig
from crispy_forms.layout import Submit,Reset

from trade_master.models import Cms_StaticContent,Faq,Contactus,EmailTemplate,Roadmap,Currencylist,SupportCategory,SupportTicket
from trade_master.forms import ContentPageForm,FaqForm,ContactForm,EmailContentForm,RoadmapForm,CurrencyForm,SupportCategoryForm

from trade_master.tables import StaticContentTable,CmsContentTable,FaqTable,ContactusTable,SupportCategoryTable,UserRequestManagementFilter,UserRequestManagementSearch_Form,User_Request_Management_Table
from trade_master.tables import EmailTemplateTable,RoadmapTable,CurrencyTable


def get_email_template(request,email_temp_id):
    email_template = EmailTemplate.objects.get(id = email_temp_id)
    if email_template:
        email_template_qs =email_template
    else:
        email_template_qs = ''
    return email_template_qs

def get_common_cipher():
    return AES.new(settings.COMMON_ENCRYPTION_KEY,
                   AES.MODE_CBC,
                   settings.COMMON_16_BYTE_IV_FOR_AES)

def decrypt_with_common_cipher(ciphertext):
    common_cipher = get_common_cipher()
    raw_ciphertext = base64.b64decode(ciphertext)
    decrypted_message_with_padding = common_cipher.decrypt(raw_ciphertext)
    return decrypted_message_with_padding.decode('utf-8').strip()




class Liststaticcontent(CmsAdminRequiredMixin,ListView):
    model = Cms_StaticContent
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return Cms_StaticContent.objects.filter(contenttype=0)
    
    def get_context_data(self,**kwargs):
        context=super(Liststaticcontent, self).get_context_data(**kwargs)
        context['Title'] = 'CMS Page'
        content_qs = Cms_StaticContent.objects.filter(contenttype=0)
        context['content_qs'] =content_qs
        contenttable = StaticContentTable(content_qs)
        context['table'] = contenttable
        context['activecls']='cmsstaticadmin'
        return context



class UpdateCms_StaticContent(CmsAdminRequiredMixin,UpdateView):
    model = Cms_StaticContent
    form_class = ContentPageForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(UpdateCms_StaticContent, self).get_context_data(**kwargs)
       context['Title'] = 'Cms Page'
       context['Btn_url'] = 'trade_master:cmspagelist'
       context['activecls']='cmsstaticadmin'
       return context

    @transaction.atomic
    def form_valid(self, form):
       
       form.instance.modified_by_id = self.request.user.id
       form.instance.contenttype =0
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'cms page updated successfully.')
       return HttpResponseRedirect('/trademaster/cmspagelist/')


class DetailStaticcontent(CmsAdminRequiredMixin,DetailView):
    model = Cms_StaticContent 
    template_name = 'trade_master/cms_detail.html'
    def get_context_data(self, **kwargs):
       context = super(DetailStaticcontent, self).get_context_data(**kwargs)
       p_key = int(self.kwargs['pk'])
       staticcontent_qs = Cms_StaticContent.objects.get(id=p_key)
       context['Title'] = 'Cms Page Detail'
       context['staticcontent_qs']=staticcontent_qs
       context['activecls']='cmsstaticadmin'
       return context

class Listcontent(CmsAdminRequiredMixin,ListView):
    model = Cms_StaticContent
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return Cms_StaticContent.objects.filter(Q(status=0))
    
    def get_context_data(self,**kwargs):
        context=super(Listcontent, self).get_context_data(**kwargs)
        context['Title'] = 'CMS Home Content'
        content_qs = Cms_StaticContent.objects.filter(Q(status=0))
        context['content_qs'] =content_qs
        contenttable = CmsContentTable(content_qs)
        context['table'] = contenttable
        context['activecls']='cmsstaticadmin'
        return context
    
    @method_decorator(check_group("CMS Management"))
    def dispatch(self, *args, **kwargs):
      return super(Liststaticcontent, self).dispatch(*args, **kwargs)



class UpdateCms_Content(CmsAdminRequiredMixin,UpdateView):
    model = Cms_StaticContent
    form_class = ContentPageForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(UpdateCms_Content, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       staticcontent_qs = Cms_StaticContent.objects.get(id=p_key)
       context['Title'] = 'Cms Home Content'
       context['staticcontent_qs']=staticcontent_qs
       context['Btn_url'] = 'trade_master:cmspagecontentlist'
       context['activecls']='cmsstaticadmin'
       return context
    
    @method_decorator(check_group("CMS Management"))
    def dispatch(self, *args, **kwargs):
      return super(UpdateCms_StaticContent, self).dispatch(*args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
       form.instance.modified_by_id = self.request.user.id
       form.instance.contenttype =1
       formsave=form.save()
       messages.add_message(self.request, messages.SUCCESS, 'cms content updated successfully.')
       return HttpResponseRedirect('/trademaster/cmspagecontentlist/')


class Detailcontent(CmsAdminRequiredMixin,DetailView):
    model = Cms_StaticContent 
    template_name = 'trade_master/cms_content_detail.html'
    def get_context_data(self, **kwargs):
       context = super(Detailcontent, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       staticcontent_qs = Cms_StaticContent.objects.get(id=p_key)
       context['Title'] = 'Cms Home Content Detail'
       context['staticcontent_qs']=staticcontent_qs
       context['activecls']='cmsstaticadmin'
       return context
    
    @method_decorator(check_group("CMS Management"))
    def dispatch(self, *args, **kwargs):
      return super(Detailcontent, self).dispatch(*args, **kwargs)


class ListFaq(FaqAdminRequiredMixin,ListView):
    model = Faq
    template_name = 'trade_master/generic_list_add.html'
    def get_queryset(self, **kwargs):
      return Faq.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(ListFaq, self).get_context_data(**kwargs)
        context['Title'] = 'FAQ'
        content_qs = Faq.objects.all()
        context['content_qs'] =content_qs
        contenttable = FaqTable(content_qs)
        context['table'] = contenttable
        context['add_title'] ='Add FAQ'
        context['Btn_url'] = 'trade_master:addfaq'
        return context
    
    @method_decorator(check_group("Manage FAQ"))
    def dispatch(self, *args, **kwargs):
      return super(ListFaq, self).dispatch(*args, **kwargs)

class AddFaq(FaqAdminRequiredMixin,CreateView):
    model = Faq
    form_class = FaqForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(AddFaq, self).get_context_data(**kwargs)
       context['Title'] = 'Add FAQ'
       context['Btn_url'] = 'trade_master:faqlist'
       return context
    
    @method_decorator(check_group("Manage FAQ"))
    def dispatch(self, *args, **kwargs):
      return super(AddFaq, self).dispatch(*args, **kwargs)

   
    @transaction.atomic
    def form_valid(self, form):
       try:
          title = form.instance.title
          faq = Faq.objects.get(title = title)
          if faq:
             messages.add_message(self.request, messages.ERROR, 'Question Already Added')
             return HttpResponseRedirect('/trademaster/faqlist/')
       except:
         form.instance.created_on   = datetime.datetime.now()
         form.instance.created_by_id = self.request.user.id
         form.instance.modified_by_id = self.request.user.id
         formsave=form.save()
         form.instance.name = formsave.title
         form.save()

         messages.add_message(self.request, messages.SUCCESS, 'faq created successfully.')
         return HttpResponseRedirect('/trademaster/faqlist/')

class UpdateFaq(FaqAdminRequiredMixin,UpdateView):
    model = Faq
    form_class = FaqForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(UpdateFaq, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       staticcontent_qs = Faq.objects.get(id=p_key)
       context['Title'] = 'Update FAQ'
       context['Btn_url'] = 'trade_master:faqlist'
       return context
    
    @method_decorator(check_group("Manage FAQ"))
    def dispatch(self, *args, **kwargs):
      return super(UpdateFaq, self).dispatch(*args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()
       form.instance.created_by_id = self.request.user.id
       form.instance.modified_by_id = self.request.user.id
       messages.add_message(self.request, messages.SUCCESS, 'faq updated successfully.')
       return HttpResponseRedirect('/trademaster/faqlist/')




class Detailfaq(FaqAdminRequiredMixin,DetailView):
    model = Faq 
    template_name = 'trade_master/faq_detail.html'
    def get_context_data(self, **kwargs):
       context = super(Detailfaq, self).get_context_data(**kwargs)
       p_key = int(self.kwargs['pk'])
       staticcontent_qs = Faq.objects.get(id=p_key)
       context['Title'] = 'FAQ Detail'
       context['staticcontent_qs']=staticcontent_qs
       return context
    
    @method_decorator(check_group("Manage FAQ"))
    def dispatch(self, *args, **kwargs):
      return super(Detailfaq, self).dispatch(*args, **kwargs)



class ListRoadmap(RoadmapAdminRequiredMixin,ListView):
    model = Roadmap
    template_name = 'trade_master/generic_list_add.html'
    def get_queryset(self, **kwargs):
      return Roadmap.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super(ListRoadmap, self).get_context_data(**kwargs)
        context['Title'] = 'RoadMap'
        content_qs = Roadmap.objects.all()
        context['content_qs'] =content_qs
        contenttable = RoadmapTable(content_qs)
        context['table'] = contenttable
        context['add_title'] ='Add Roadmap'
        context['Btn_url'] = 'trade_master:addroadmap'
        return context

class AddRoadmap(RoadmapAdminRequiredMixin,CreateView):
    model = Roadmap
    form_class = RoadmapForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(AddRoadmap, self).get_context_data(**kwargs)
       context['Title'] = 'Add Roadmap'
       context['Btn_url'] = 'trade_master:roadmaplist'
       return context

    @transaction.atomic
    def form_valid(self, form):
        
       form.instance.created_on   = datetime.datetime.now()
       form.instance.created_by_id = self.request.user.id
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()
       form.instance.name = formsave.title
       form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Roadmap created successfully.')
       return HttpResponseRedirect('/trademaster/roadmaplist/')

class UpdateRoadmap(RoadmapAdminRequiredMixin,UpdateView):
    model = Roadmap
    form_class = RoadmapForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(UpdateRoadmap, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       staticcontent_qs = Roadmap.objects.get(id=p_key)
       context['Title'] = 'Update Roadmap'
       context['Btn_url'] = 'trade_master:roadmaplist'
       return context

    @transaction.atomic
    def form_valid(self, form):
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()
       messages.add_message(self.request, messages.SUCCESS, 'Roadmap updated successfully.')
       return HttpResponseRedirect('/trademaster/roadmaplist/')



class DetailRoadmap(RoadmapAdminRequiredMixin,DetailView):
    model = Roadmap 
    template_name = 'trade_master/roadmap_detail.html'
    def get_context_data(self, **kwargs):
       context = super(DetailRoadmap, self).get_context_data(**kwargs)
       p_key = int(self.kwargs['pk'])
       staticcontent_qs = Roadmap.objects.get(id=p_key)
       context['Title'] = 'Roadmap Detail'
       context['staticcontent_qs']=staticcontent_qs
       return context



class Listcontactus(ContactusAdminRequiredMixin,ListView):
    model = Contactus
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return Contactus.objects.filter(status=0).order_by('-id')
    
    def get_context_data(self,**kwargs):
        context=super(Listcontactus, self).get_context_data(**kwargs)
        context['Title'] = 'Contacted User List'
        content_qs = Contactus.objects.filter(status=0).order_by('-id')
        context['content_qs'] =content_qs
        contenttable = ContactusTable(content_qs)
        context['table'] = contenttable
        return context


class UpdateContactus(ContactusAdminRequiredMixin,UpdateView):
    model = Contactus
    form_class = ContactForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(UpdateContactus, self).get_context_data(**kwargs)
       context['Title'] = 'Update Contact user'
       context['Btn_url'] = 'trade_master:contactlist'
       return context

    @transaction.atomic
    def form_valid(self, form):
       form.instance.read_status = 1
       formsave=form.save()
       try:
        companyqs = Company.objects.get(id=1)
        companyname= companyqs.name
        copyright= companyqs.copy_right
        comp_logo = companyqs.company_logo
       except:
        companyqs = ''
        copyright = ''
        comp_logo=''
       email_template = EmailTemplate.objects.get(name ="contactus_reply")
       if email_template:
          email_template_qs =email_template
       else:
          email_template_qs = ''

       text_file = open("trade_master/templates/emailtemplate/contactus_reply.html", "w")  
       text_file.write(email_template.content)
       text_file.close()
       email_subject = email_template.Subject
       to_email = formsave.email
       from_email_get = settings.EMAIL_USER
       from_email =decrypt_with_common_cipher(from_email_get)
       hostuser = decrypt_with_common_cipher(settings.EMAIL_USER_ENC)
       hostpassword = decrypt_with_common_cipher(settings.EMAIL_PASSWORD_ENC)
       settings.EMAIL_HOST_USER = hostuser
       settings.EMAIL_HOST_PASSWORD = hostpassword
    
       data= {
          'username':formsave.name,
          'email':to_email,
          'company_logo':'comp_company_logo',
          'reply': formsave.reply,
          'company_logo':comp_logo,
          'copyright':copyright,
          'domain':get_current_site(self.request),
          }
       text_content = 'This is an important message.'
       htmly = get_template('emailtemplate/support_reply.html')
       html_content = htmly.render(data)
       msg = EmailMultiAlternatives(email_subject, text_content, from_email, [to_email])
       msg.attach_alternative(html_content, "text/html")
       msg.send()

       messages.add_message(self.request, messages.SUCCESS, 'reply message updated successfully.')
       return HttpResponseRedirect('/trademaster/contactlist/')


class Detailcontactus(ContactusAdminRequiredMixin,DetailView):
    model = Contactus 
    template_name = 'trade_master/contactus_detail.html'
    def get_context_data(self, **kwargs):
       context = super(Detailcontactus, self).get_context_data(**kwargs)
       p_key = int(self.kwargs['pk'])
       staticcontent_qs = Contactus.objects.get(id=p_key)
       context['Title'] = 'Contact Info'
       context['staticcontent_qs']=staticcontent_qs
       return context





class Listemailcontent(EmailTemplateAdminRequiredMixin,ListView):
    model = EmailTemplate
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return EmailTemplate.objects.filter(status=0)
    
    def get_context_data(self,**kwargs):
        context=super(Listemailcontent, self).get_context_data(**kwargs)
        context['Title'] = 'Email Template List'
        content_qs = EmailTemplate.objects.filter(status=0)
        context['content_qs'] =content_qs
        contenttable = EmailTemplateTable(content_qs)
        context['table'] = contenttable
        return context
    
    @method_decorator(check_group("Manage Email Template"))
    def dispatch(self, *args, **kwargs):
      return super(Listemailcontent, self).dispatch(*args, **kwargs)

class Updateemailcontent(EmailTemplateAdminRequiredMixin,UpdateView):
    model = EmailTemplate
    form_class = EmailContentForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(Updateemailcontent, self).get_context_data(**kwargs)
       context['Title'] = 'Update Email Template'
       context['Btn_url'] = 'trade_master:emailcontactlist'
       return context
    
    @method_decorator(check_group("Manage Email Template"))
    def dispatch(self, *args, **kwargs):
      return super(Updateemailcontent, self).dispatch(*args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Email content updated successfully.')
       return HttpResponseRedirect('/trademaster/emailcontactlist/')


class ListCurrencyDetails(CurrencyAdminRequiredMixin,ListView):
    model = Currencylist
    template_name = 'trade_master/generic_list.html'
    def get_queryset(self, **kwargs):
      return Currencylist.objects.filter(status=0)
    
    def get_context_data(self,**kwargs):
        context=super(ListCurrencyDetails, self).get_context_data(**kwargs)
        context['Title'] = 'List of currency'
        content_qs = Currencylist.objects.filter(status=0)
        context['content_qs'] =content_qs
        contenttable = CurrencyTable(content_qs)
        context['table'] = contenttable
        return context
    
    


class Updatecurrency(CurrencyAdminRequiredMixin,UpdateView):
    model = Currencylist
    form_class = CurrencyForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(Updatecurrency, self).get_context_data(**kwargs)
       context['Title'] = 'Edit Currency'
       context['Btn_url'] = 'trade_master:currencylist'
       return context

    @transaction.atomic
    def form_valid(self, form):
       form.instance.modified_by_id = self.request.user.id
       formsave=form.save()

       messages.add_message(self.request, messages.SUCCESS, 'Currency updated successfully.')
       return HttpResponseRedirect('/trademaster/currencylist/')


class Detailcurrency(CurrencyAdminRequiredMixin,DetailView):
    model = Currencylist 
    template_name = 'trade_master/currency_detail.html'
    def get_context_data(self, **kwargs):
       context = super(Detailcurrency, self).get_context_data(**kwargs)
       p_key = int(self.kwargs['pk'])
       staticcontent_qs = Currencylist.objects.get(id=p_key)
       context['Title'] = 'Currency Detail'
       context['staticcontent_qs']=staticcontent_qs
       return context


import glob
import os
from pathlib import Path
import time


def read_dir_log(request):


   dir_name = '/var/www/html/jasonwellnessenv/logs/'
   list_of_files = filter( os.path.isfile,
                           glob.glob(dir_name + '*') )
   list_of_files = sorted( list_of_files,
                           key = os.path.getmtime)
   list_dir = []
   for file_path in list_of_files:
      dict_dir = {}
      timestamp_str = time.strftime(  '%m/%d/%Y :: %H:%M:%S',
                                 time.gmtime(os.path.getmtime(file_path))) 
      dict_dir["time"]=(timestamp_str)
      dict_dir["path"]=(file_path)
      list_dir.append(dict_dir)


  
   

   return JsonResponse({"success":list_dir})



def read_log(request):
  f = open('/var/www/html/jasonwellnessenv/logs/gunicorn_supervisor.log.10', 'r')
  file_content = f.read()
  f.close() 
  return HttpResponse(file_content,content_type="text/plain")

def delete_log(request):
  try:
    f=open("/var/www/html/jasonwellnessenv/logs/gunicorn_supervisor.log","r+")
    f.truncate()
    f.close()
    f=open("/var/www/html/jasonwellnessenv/logs/gunicorn_supervisor.log.1","r+")
    f.truncate()
    f.close()
    f=open("/var/www/html/jasonwellnessenv/logs/gunicorn_supervisor.log.2","r+")
    f.truncate()
    f.close()
    f=open("/var/www/html/jasonwellnessenv/logs/gunicorn_supervisor.log.3","r+")
    f.truncate()
    f.close()
    f=open("/var/www/html/jasonwellnessenv/logs/gunicorn_supervisor.log.4","r+")
    f.truncate()
    f.close()
    f=open("/var/www/html/jasonwellnessenv/logs/gunicorn_supervisor.log.5","r+")
    f.truncate()
    f.close()
    f=open("/var/www/html/jasonwellnessenv/logs/gunicorn_supervisor.log.6","r+")
    f.truncate()
    f.close()
    f=open("/var/www/html/jasonwellnessenv/logs/gunicorn_supervisor.log.7","r+")
    f.truncate()
    f.close()
    f=open("/var/www/html/jasonwellnessenv/logs/gunicorn_supervisor.log.8","r+")
    f.truncate()
    f.close()
    f=open("/var/www/html/jasonwellnessenv/logs/gunicorn_supervisor.log.9","r+")
    f.truncate()
    f.close()
    f=open("/var/www/html/jasonwellnessenv/logs/gunicorn_supervisor.log.10","r+")
    f.truncate()
    f.close()
  except Exception as e:
    pass
  return JsonResponse({'status':'Success','msg':'successss'})



# Support category listing function

class ListSupportCategory(ListView):
    model = SupportCategory
    template_name = 'trade_master/generic_list_add.html'
    def get_queryset(self, **kwargs):
      return SupportCategory.objects.all().order_by('-id')
    
    def get_context_data(self,**kwargs):
        context=super(ListSupportCategory, self).get_context_data(**kwargs)
        context['Title'] = 'Contacted User List'
        content_qs = SupportCategory.objects.all().order_by('-id')
        context['content_qs'] =content_qs
        contenttable = SupportCategoryTable(content_qs)
        context['table'] = contenttable
        context['add_title'] ='Add Category'
        context['Btn_url'] = 'trade_master:addsupportcategory'
        return context
    
    @method_decorator(check_group_sub_menu("Support Ticket Category"))
    def dispatch(self, *args, **kwargs):
      return super(ListSupportCategory, self).dispatch(*args, **kwargs)

# Support category add function

class AddCategoryTicket(CreateView):
    model = SupportCategory
    form_class = SupportCategoryForm
    template_name = 'trade_master/support_category_add.html'   
    def get_context_data(self, **kwargs):
       context = super(AddCategoryTicket, self).get_context_data(**kwargs)
       context['Title'] = 'Add Category'
       context['Btn_url'] = 'trade_master:supportcategorylist'
       return context
    
    @method_decorator(check_group_sub_menu("Support Ticket Category"))
    def dispatch(self, *args, **kwargs):
      return super(AddCategoryTicket, self).dispatch(*args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
        form.instance.status = 0
        formsave=form.save()
        messages.add_message(self.request, messages.SUCCESS, 'SupportCategory Added successfully.')
        return HttpResponseRedirect('/trademaster/supportcategorylist/')


# Support category update function

class UpdateCategoryTicket(UpdateView):
    model = SupportCategory
    form_class = SupportCategoryForm
    template_name = 'trade_master/generic_form.html'   
    def get_context_data(self, **kwargs):
       context = super(UpdateCategoryTicket, self).get_context_data(**kwargs)
       p_key = self.kwargs['pk']
       staticcontent_qs = SupportCategory.objects.get(id=p_key)
       context['Title'] = 'Update Category'
       context['Btn_url'] = 'trade_master:supportcategorylist'
       return context
    
    @method_decorator(check_group_sub_menu("Support Ticket Category"))
    def dispatch(self, *args, **kwargs):
      return super(UpdateCategoryTicket, self).dispatch(*args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
       formsave=form.save()
       messages.add_message(self.request, messages.SUCCESS, 'SupportCategory Updated successfully.')
       return HttpResponseRedirect('/trademaster/supportcategorylist/')


# Support category delete function

class DeleteSupportCategory(View):
    def get(self, request, *args, **kwargs):
        pkey =  (self.kwargs['pk'])
        user_qs = get_object_or_404(SupportCategory, pk=pkey)
        try:
            get_user_id = SupportCategory.objects.get(id=pkey)
           
            user_qs.delete()
        except:
            user_qs.delete()

        messages.add_message(request, messages.SUCCESS, 'Support Category deleted successfully.') 
        return HttpResponseRedirect(reverse('trade_master:supportcategorylist'))


# User request API listing function 

class UserRequestManagement(ListView):
  model = Contactus
  template_name = 'trade_master/user_request_management_list.html'
  def get_queryset(self, **kwargs):
    return Contactus.objects.all().order_by('-modified_on')
  
  def get_context_data(self,**kwargs):
      context=super(UserRequestManagement, self).get_context_data(**kwargs)
      context['Title'] = 'User Request Management'
      adminactivity_qs = Contactus.objects.all().order_by('-modified_on')
      context['adminactivity_qs'] =adminactivity_qs
      user_count = Contactus.objects.all().count()
      context['user_count'] = user_count
      category_obj = SupportCategory.objects.all()
      context['category_obj'] = category_obj
      filter = UserRequestManagementFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
      filter.form.helper = UserRequestManagementSearch_Form()
      filter.form.helper.add_input(Submit('submit', 'Search',css_class="btn btn-default"))
      
      filter.form.helper.add_input(Reset('Reset Search','Reset Search',css_class="btn btn-default",css_id='reset-search'))
      Adminactivitytable = User_Request_Management_Table(filter.qs)
      RequestConfig(self.request, paginate={'per_page': 10}).configure(Adminactivitytable)
      context['table'] = Adminactivitytable
      context['filter'] = filter
      context['add_title'] ='Add BlockIp'
      context['Btn_url'] = 'trade_master:User_request_list'
      return context
  
  @method_decorator(check_group_sub_menu("Support Ticket User Request"))
  def dispatch(self, *args, **kwargs):
   return super(UserRequestManagement, self).dispatch(*args, **kwargs)


# Admin reply function

import boto3
@check_group_sub_menu("Support Ticket User Request")
def UpdateUserRequest(request,id):
   context = {}
   try:
      staticcontent_qs = Contactus.objects.get(id = id)
   except:
      staticcontent_qs = ""
   try:
      support_ticket_obj = SupportTicket.objects.filter(ticket_id = staticcontent_qs.id).order_by('id')
   except:
      support_ticket_obj = ""
   
   img_dict = {}
   try:
      a = 0
      for img in support_ticket_obj:
         str1 = img.attachment
         y = str1.replace("'","")
         res = y.strip('][').split(', ')
         for i in res:
            a = a + 1
            img_dict_1 = {}
            # res_1 = i[:i.rfind('?')]
            split_type = i.split(".")[-1]
            split_name = i.split("/")[-1]
            img_dict_1["file_type"] = split_type
            img_dict_1["file_name"] = split_name
            img_dict_1["comment"] = img.comment
            img_dict_1["date"] = img.created_on
            img_dict_1["user_type"] = img.created_by
            if i != "":
               img_dict[i] = img_dict_1
            else:
               x = "No image"+str(a)
               img_dict[x] = img_dict_1
   except:
      pass
   context['img_dict'] = img_dict
   img_dict_list = {}
   try:
      obj_contactus = Contactus.objects.filter(id = id)
      for img in obj_contactus:
         str1 = img.attachment
         y = str1.replace("'","")
         res = y.strip('][').split(', ')
         for i in res:
            img_dict_list_1 = {}
            # res_1 = i[:i.rfind('?')]
            split_type = i.split(".")[-1]
            split_name = i.split("/")[-1]
            img_dict_list_1["file_type"] = split_type
            img_dict_list_1["file_name"] = split_name
            img_dict_list[i] = img_dict_list_1
   except:
      pass

   context['img_dict_list'] = img_dict_list
   if request.method == "POST":
      reply = request.POST["reply"]
      status = request.POST["read_status"]
      try:
         file = request.FILES.getlist("attachment_file")
      except:
         file = 1
      img_list_1 = []
  
      
      if reply != "":
         if file != 1:
            for i in file:
               filename = i.name
               s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
               
               s3.upload_fileobj(i, settings.AWS_STORAGE_BUCKET_NAME, filename)
               response = s3.generate_presigned_url('get_object',
                                                Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                      'Key': filename})
               img_list_1.append(response)

            if status == "0":
               sts = 1
            elif status == "1":
               sts = 1
            elif status == "2":
               sts = 2
            elif status == "4":
               sts = 4

            SupportTicket.objects.create(ticket_id = staticcontent_qs.id,comment = reply,created_by = request.user.username,user_type = 1,attachment = img_list_1,created_on = datetime.datetime.now())
            obj_update_ticket = Contactus.objects.filter(ticket_id = staticcontent_qs.ticket_id).update(read_status = sts)
         else:
            SupportTicket.objects.create(ticket_id = staticcontent_qs.id,comment = reply,created_by = request.user.username,user_type = 1,created_on = datetime.datetime.now())
            obj_update_ticket = Contactus.objects.filter(ticket_id = staticcontent_qs.ticket_id).update(read_status = sts)
      
      
         messages.add_message(request, messages.SUCCESS, 'User Request Ticket updated successfully.')
         return HttpResponseRedirect('/trademaster/User_request_list/')
      else:
         messages.add_message(request, messages.ERROR, 'Reply field required.')
   context['support_ticket_obj'] = support_ticket_obj
   context['staticcontent_qs'] = staticcontent_qs
   context['Title'] = 'Update User Request'
   return render(request,'trade_master/user_request_update.html',context)
