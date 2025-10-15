from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required,user_passes_test

from django.http.response import HttpResponseRedirect
from django.http import HttpResponse,Http404
from django.urls import reverse
from django.contrib import auth

from functools import wraps
from django.db.models import Q,F,Func,Value
from trade_master.models import Blockip
from trade_admin_auth.models import AccessAttempt

from django.contrib.auth.models import User,Group
from company.models import Company,Company_Settings

from trade_master.models import MenuModule,MenuPermission,SubMenuModule, SubMenuPermission, IconMenuModule, IconMenuPermission

from requests import get

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip

def get_browser_type(request):
    browser_with_version = request.user_agent.browser.family+' '+request.user_agent.browser.version_string
    return browser_with_version

def get_browser_os_type(request):
    browser_os_type = request.user_agent.os.family
    return browser_os_type
def get_browser_device_type(request):
    return request.user_agent.device.family


def allow_by_ip(view_func):
    def authorize(request, *args, **kwargs):
        user_ip = get_client_ip(request)
        allowedIps = Blockip.objects.filter(Q(status=0) & Q(ip_level="Admin"))
        for ip in allowedIps:
            if ip.ip_address == user_ip:
                return HttpResponseRedirect("/tradeadmin/adminblockip404/")
        return view_func(request, *args, **kwargs)
    return authorize


# def allow_by_ip(view_func):
#     # Define the list of allowed IP addresses
#     allowed_ips = [
#         '2.50.0.0/16',
#         '5.32.0.0/12',
#         # '203.0.113.1',
#         # Add more IPs as needed
#     ]

#     def authorize(request, *args, **kwargs):
#         user_ip = get_client_ip(request)
#         if user_ip not in allowed_ips:
#             return HttpResponseRedirect("/tradeadmin/adminblockip404/")
#         return view_func(request, *args, **kwargs)

#     return authorize



def check_adminip(group_name):
    def _check_adminip(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try:
                companyqs = Company.objects.get(id=1)
                companyname= companyqs.name
                companyipaddress = companyqs.company_settings.adminipaddress
            except Company.DoesNotExist:
                companyqs = 'HotBitDeal Auction'
                companyname = 'HotBitDeal Auction'
                companyipaddress = ''
            user_ip = get_client_ip(request)
            if companyipaddress is not None and companyipaddress != '':
                if companyipaddress != user_ip:
                    auth.logout(request)
                    return HttpResponseRedirect('/tradeadmin/ipblock404/')
            return view_func(request, *args, **kwargs)
        return wrapper
    return _check_adminip


class BlockIpaddressAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        user_ip = get_client_ip(request)
        allowedIps = Blockip.objects.filter(Q(status=0) & Q(ip_level="Admin"))
        for ip in allowedIps:
            if ip.ip_address == user_ip:
                return HttpResponseRedirect("/tradeadmin/adminblockip404/")
        return super().dispatch(request, *args, **kwargs)


class CheckIpaddressAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        try:
            companyqs = Company.objects.get(id=1)
            companyname= companyqs.name
            companyipaddress = companyqs.company_settings.adminipaddress
            
        except Company.DoesNotExist:
            companyqs = 'Criptomonedas-chile'
            companyname = 'Criptomonedas-chile'
            companyipaddress = ''
        user_ip = get_client_ip(request)

        if companyipaddress is not None and companyipaddress != '':
            if companyipaddress != user_ip:
                auth.logout(request)
                return HttpResponseRedirect('/tradeadmin/ipblock404/')
            else:
                return super().dispatch(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


def check_group(group_name):
    def _check_group(view_func):
        @wraps(view_func)
        def wrapper(request,*args, **kwargs):
            try:
                user_id = request.user.id
                if request.user.admin_user_profile.role == 0:
                    pass
                else:
                    get_groupname = MenuModule.objects.get(module_name=group_name)
                    checkpermission = MenuPermission.objects.get(Q(access_modules=get_groupname.id) & Q(user_permissions=user_id))
                    if checkpermission.access_status == 0:
                        pass
                    else:
                        return HttpResponseRedirect('/tradeadmin/page_403/')
            except:
                pass
            
            return view_func(request,*args, **kwargs)    
        return wrapper
    return _check_group


def check_group_sub_menu(group_name):
    def _check_group_sub_menu(view_func):
        @wraps(view_func)
        def wrapper(request,*args, **kwargs):
            try:
                user_id = request.user.id
                if request.user.admin_user_profile.role == 0:
                    pass
                else:
                    get_groupname = SubMenuModule.objects.get(sub_module_name=group_name)
                    checkpermission = SubMenuPermission.objects.get(Q(sub_menu_name_id=get_groupname.id) & Q(user_permissions=user_id))
                    if checkpermission.access_status == 0:
                        pass
                    else:
                        return HttpResponseRedirect('/tradeadmin/page_403/')
            except:
                pass
            
            return view_func(request,*args, **kwargs)    
        return wrapper
    return _check_group_sub_menu



def check_group_icon_menu(group_name):
    def _check_group_icon_menu(view_func):
        @wraps(view_func)
        def wrapper(request,*args, **kwargs):
            try:
                user_id = request.user.id
                if request.user.admin_user_profile.role == 0:
                    pass
                else:
                    get_groupname = IconMenuModule.objects.get(icon_module_name=group_name)
                    checkpermission = IconMenuPermission.objects.get(Q(icon_menu_name_id=get_groupname.id) & Q(user_permissions=user_id))
                    if checkpermission.access_status == 0:
                        pass
                    else:
                        return HttpResponseRedirect('/tradeadmin/page_403/')
            except:
                pass
            
            return view_func(request,*args, **kwargs)    
        return wrapper
    return _check_group_icon_menu


def check_session(group_name):
    username = ''
    def _check_session(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            username = request.user.username
            if username != None or username !='':
                return HttpResponseRedirect('/')
            return view_func(request, *args, **kwargs)
            
        return wrapper
    return _check_session


def check_attempt(group_name):
    def _check_attempt(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            attempt = AccessAttempt.objects.filter(ip_address=ip)
            access_count = len(attempt)
            if access_count <= 4 :
                return HttpResponseRedirect("/HotBitDeal Auction/login/")
            return view_func(request, *args, **kwargs)
            
        return wrapper
    return _check_attempt

    
class SubAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        user_id =request.user.id
        if ((request.user.admin_user_menupermissions.filter(Q(user_permissions=user_id) & Q(access_modules=15) & (Q(access_permissions=1) | Q (access_permissions=2))).exists())):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/tradeadmin/page_403/')



class CmsAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        user_id =request.user.id
        return super().dispatch(request, *args, **kwargs)

class FaqAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        user_id =request.user.id
        return super().dispatch(request, *args, **kwargs)


class RoadmapAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        user_id =request.user.id
        return super().dispatch(request, *args, **kwargs)

class CurrencyAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        user_id =request.user.id
        return super().dispatch(request, *args, **kwargs)


class ContactusAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        user_id =request.user.id
        return super().dispatch(request, *args, **kwargs)


class EmailTemplateAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        user_id =request.user.id
        return super().dispatch(request, *args, **kwargs)


class ManageUserAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        user_id =request.user.id
        return super().dispatch(request, *args, **kwargs)



class ManageCurrencyAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        user_id =request.user.id
        if ((request.user.admin_user_menupermissions.filter(Q(user_permissions=user_id) & Q(access_modules=13) & (Q(access_permissions=1) | Q (access_permissions=2))).exists())):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/tradeadmin/page_403/')

class ManageReferalAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        user_id =request.user.id
        if ((request.user.admin_user_menupermissions.filter(Q(user_permissions=user_id) & Q(access_modules=16) & (Q(access_permissions=1) | Q (access_permissions=2))).exists())):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/tradeadmin/page_403/')

class ManageTicketSupportAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        user_id =request.user.id
        if ((request.user.admin_user_menupermissions.filter(Q(user_permissions=user_id) & Q(access_modules=7) & (Q(access_permissions=1) | Q (access_permissions=2))).exists())):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/tradeadmin/page_403/')
class ManageTradeAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        user_id =request.user.id
        if ((request.user.admin_user_menupermissions.filter(Q(user_permissions=user_id) & Q(access_modules=10) & (Q(access_permissions=1) | Q (access_permissions=2))).exists())):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/tradeadmin/page_403/')

class ManagePaymentAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        user_id =request.user.id
        if ((request.user.admin_user_menupermissions.filter(Q(user_permissions=user_id) & Q(access_modules=11) & (Q(access_permissions=1) | Q (access_permissions=2))).exists())):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/tradeadmin/page_403/')


class ManagePlanAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        user_id =request.user.id
        if ((request.user.admin_user_menupermissions.filter(Q(user_permissions=user_id) & Q(access_modules=17) & (Q(access_permissions=1) | Q (access_permissions=2))).exists())):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/tradeadmin/page_403/')

class ManageGenerationAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        user_id =request.user.id
        if ((request.user.admin_user_menupermissions.filter(Q(user_permissions=user_id) & Q(access_modules=18) & (Q(access_permissions=1) | Q (access_permissions=2))).exists())):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/tradeadmin/page_403/')


class ManageNewsletterAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        user_id =request.user.id
        return super().dispatch(request, *args, **kwargs)
        

class ManageBlockipAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        user_id =request.user.id
        if ((request.user.admin_user_menupermissions.filter(Q(user_permissions=user_id) & Q(access_modules=8) & (Q(access_permissions=1) | Q (access_permissions=2))).exists())):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/tradeadmin/page_403/')


class ManageBankDetailsAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):        
        user_id =request.user.id
        if ((request.user.admin_user_menupermissions.filter(Q(user_permissions=user_id) & Q(access_modules=19) & (Q(access_permissions=1) | Q (access_permissions=2))).exists())):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/tradeadmin/page_403/')