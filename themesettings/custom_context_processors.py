from company.models import Company
from django.contrib.auth.models import User,Group
from django.db.models import Q

from trade_admin_auth.models import AdminUser_Profile

from trade_master.models import MenuModule, MenuPermission, SubMenuModule, IconMenuModule, SubMenuPermission, IconMenuPermission


def comp_profile(request):
    try:
        
        comp = Company.objects.get(id=1)

        host_url = "{0}://{1}".format(request.scheme, request.get_host())
        return {'comp_profile_name': comp.name,
                'comp_profile_id': comp.id,
                'company_fav' : comp.company_fav,
                'comp_company_logo' : comp.company_logo,
                'host_url':host_url,
                'copy_right':comp.copy_right,
                'comp_email':comp.email,
                'comp_phonenumber':comp.phone1,
                'comp_telegram':comp.telegram,
                'comp_instagram':comp.instagram,
                'comp_fb':comp.fb,
                'comp_twitter':comp.twitter,
                'comp_linkedin':comp.linkedin,
                'comp_address':comp.address1,
                'comp_city':comp.city,
                'comp_state':comp.state,
                'comp_site':comp.website,
            }
    except Company.DoesNotExist:
        return {
                'comp_profile_name': 'foo',
                'company_fav' : 'leaf',
                'comp_company_logo' : None,
                'comp_favicon' : None,
                'host_url':None,
                'copy_right':None,
                'comp_email':None,
                'comp_phonenumber':None,
                'comp_instagram':None,
                'comp_telegram':None,
                'comp_fb':None,
                'comp_twitter':None,
                'comp_linkedin':None,
                }

def user_menupermissions(request):
    
    if (request.user.id):
        try:
            check_user = User.objects.get(Q(id = request.user.id) & (Q(admin_user_profile__role=0) | Q(admin_user_profile__role=1)))
            try:

            # trade admin auth menu's start

                menu_modules_manage_user = MenuModule.objects.get(module_name = 'Manage User')
                menu_perm_manage_user = MenuPermission.objects.get(Q(access_modules_id=menu_modules_manage_user.id) & Q(user_permissions=request.user.id))

                menu_modules_sub_adm = MenuModule.objects.get(module_name = 'Manage Sub Admin')
                menu_perm_sub_adm = MenuPermission.objects.get(Q(access_modules_id=menu_modules_sub_adm.id) & Q(user_permissions=request.user.id))

                menu_module_front_page = MenuModule.objects.get(module_name = 'Front Page Management')
                menu_perm_front_page = MenuPermission.objects.get(Q(access_modules_id=menu_module_front_page.id) & Q(user_permissions=request.user.id))

                menu_module_transaction = MenuModule.objects.get(module_name = 'Transaction')
                menu_perm_transaction = MenuPermission.objects.get(Q(access_modules_id=menu_module_transaction.id) & Q(user_permissions=request.user.id))

                menu_modules_plan = MenuModule.objects.get(module_name = 'Plan Management')
                menu_perm_plan = MenuPermission.objects.get(Q(access_modules_id=menu_modules_plan.id) & Q(user_permissions=request.user.id))

                menu_modules_referral = MenuModule.objects.get(module_name = 'Referral Management')
                menu_perm_referral = MenuPermission.objects.get(Q(access_modules_id=menu_modules_referral.id) & Q(user_permissions=request.user.id))

                menu_modules_withdraw = MenuModule.objects.get(module_name = 'Withdraw Management')
                menu_perm_withdraw = MenuPermission.objects.get(Q(access_modules_id=menu_modules_withdraw.id) & Q(user_permissions=request.user.id))

                menu_modules_wallet = MenuModule.objects.get(module_name = 'Wallet Management')
                menu_perm_wallet = MenuPermission.objects.get(Q(access_modules_id=menu_modules_wallet.id) & Q(user_permissions=request.user.id))

                menu_modules_notify = MenuModule.objects.get(module_name = 'Notification Management')
                menu_perm_notify = MenuPermission.objects.get(Q(access_modules_id=menu_modules_notify.id) & Q(user_permissions=request.user.id))

                menu_modules_transfer = MenuModule.objects.get(module_name = 'Transfer Management')
                menu_perm_transfer = MenuPermission.objects.get(Q(access_modules_id=menu_modules_transfer.id) & Q(user_permissions=request.user.id))

                menu_modules_rpc = MenuModule.objects.get(module_name = 'RPC Management')
                menu_perm_rpc = MenuPermission.objects.get(Q(access_modules_id=menu_modules_rpc.id) & Q(user_permissions=request.user.id))

                menu_modules_admin_login_attempt = MenuModule.objects.get(module_name = 'Admin Login Attempt')
                menu_perm_admin_login_attempt = MenuPermission.objects.get(Q(access_modules_id=menu_modules_admin_login_attempt.id) & Q(user_permissions=request.user.id))


            # trade admin auth menu's end

            # trade master menu's start
                
                menu_modules_cms = MenuModule.objects.get(module_name = 'CMS Management')
                menu_perm_cms = MenuPermission.objects.get(Q(access_modules_id=menu_modules_cms.id) & Q(user_permissions=request.user.id))

                menu_modules_faq = MenuModule.objects.get(module_name = 'Manage FAQ')
                menu_perm_faq = MenuPermission.objects.get(Q(access_modules_id=menu_modules_faq.id) & Q(user_permissions=request.user.id))

                menu_modules_email_template = MenuModule.objects.get(module_name = 'Manage Email Template')
                menu_perm_email_template = MenuPermission.objects.get(Q(access_modules_id=menu_modules_email_template.id) & Q(user_permissions=request.user.id))

                menu_modules_del_acc_reason = MenuModule.objects.get(module_name = 'Delete Account reason')
                menu_perm_del_acc_reason = MenuPermission.objects.get(Q(access_modules_id=menu_modules_del_acc_reason.id) & Q(user_permissions=request.user.id))

                menu_modules_del_acc_request = MenuModule.objects.get(module_name = 'Delete Account Requests')
                menu_perm_del_acc_request = MenuPermission.objects.get(Q(access_modules_id=menu_modules_del_acc_request.id) & Q(user_permissions=request.user.id))

                menu_modules_support = MenuModule.objects.get(module_name = 'Support Management')
                menu_perm_support = MenuPermission.objects.get(Q(access_modules_id=menu_modules_support.id) & Q(user_permissions=request.user.id))

            # trade master menu's end

            # trade currency menu's start

                menu_modules_currency = MenuModule.objects.get(module_name = 'Currency Management')
                menu_perm_currency = MenuPermission.objects.get(Q(access_modules_id=menu_modules_currency.id) & Q(user_permissions=request.user.id))

                menu_modules_marketprice = MenuModule.objects.get(module_name = 'Marketprice')
                menu_perm_marketprice = MenuPermission.objects.get(Q(access_modules_id=menu_modules_marketprice.id) & Q(user_permissions=request.user.id))

                menu_modules_admin_profit = MenuModule.objects.get(module_name = 'Admin profit')
                menu_perm_admin_profit = MenuPermission.objects.get(Q(access_modules_id=menu_modules_admin_profit.id) & Q(user_permissions=request.user.id))

                menu_modules_step = MenuModule.objects.get(module_name = 'Step Management')
                menu_perm_step = MenuPermission.objects.get(Q(access_modules_id=menu_modules_step.id) & Q(user_permissions=request.user.id))

                menu_modules_ref_reward = MenuModule.objects.get(module_name = 'Referral Reward Management')
                menu_perm_ref_reward = MenuPermission.objects.get(Q(access_modules_id=menu_modules_ref_reward.id) & Q(user_permissions=request.user.id))

            # trade currency menu's end

            # Staking menu's start

                menu_modules_stake = MenuModule.objects.get(module_name = 'Staking Management')
                menu_perm_stake = MenuPermission.objects.get(Q(access_modules_id=menu_modules_stake.id) & Q(user_permissions=request.user.id))

                menu_modules_internal = MenuModule.objects.get(module_name = 'Internal Transfer')
                menu_perm_internal = MenuPermission.objects.get(Q(access_modules_id=menu_modules_internal.id) & Q(user_permissions=request.user.id))

            # Staking menu's end

                return {
                    'menu_permissions_context_manage_user':menu_perm_manage_user.access_status,
                    'menu_permissions_context_manage_sub_adm':menu_perm_sub_adm.access_status,
                    'menu_permissions_context_frontpage':menu_perm_front_page.access_status,
                    'menu_permissions_context_transaction':menu_perm_transaction.access_status,
                    'menu_permissions_context_plan':menu_perm_plan.access_status,
                    'menu_permissions_context_referral':menu_perm_referral.access_status,
                    'menu_permissions_context_withdraw':menu_perm_withdraw.access_status,
                    'menu_permissions_context_wallet':menu_perm_wallet.access_status,
                    'menu_permissions_context_notify':menu_perm_notify.access_status,
                    'menu_permissions_context_transfer':menu_perm_transfer.access_status,
                    'menu_permissions_context_rpc':menu_perm_rpc.access_status,
                    'menu_permissions_context_admin_login_attempt':menu_perm_admin_login_attempt.access_status,


                    'menu_permissions_context_cms':menu_perm_cms.access_status,
                    'menu_permissions_context_faq':menu_perm_faq.access_status,
                    'menu_permissions_context_email_template':menu_perm_email_template.access_status,
                    'menu_permissions_context_del_acc_reason':menu_perm_del_acc_reason.access_status,
                    'menu_permissions_context_del_acc_request':menu_perm_del_acc_request.access_status,
                    'menu_permissions_context_support':menu_perm_support.access_status,

                    'menu_permissions_context_currency':menu_perm_currency.access_status,
                    'menu_permissions_context_marketprice':menu_perm_marketprice.access_status,
                    'menu_permissions_context_admin_profit':menu_perm_admin_profit.access_status,
                    'menu_permissions_context_step':menu_perm_step.access_status,
                    'menu_permissions_context_ref_reward':menu_perm_ref_reward.access_status,

                    'menu_permissions_context_stake':menu_perm_stake.access_status,
                    'menu_permissions_context_internal':menu_perm_internal.access_status,
                   
                }
            except MenuPermission.DoesNotExist:
                return{
                    "menu_modules_manage_user" : None,
                    "menu_perm_manage_user" : None,
                    "menu_modules_sub_adm" : None,
                    "menu_perm_sub_adm" : None,
                    "menu_module_front_page" : None,
                    "menu_perm_front_page" : None,
                    "menu_module_transaction" : None,
                    "menu_perm_transaction" : None,
                    "menu_modules_plan" : None,
                    "menu_perm_plan" : None,
                    "menu_modules_referral" : None,
                    "menu_perm_referral" : None,
                    "menu_modules_withdraw" : None,
                    "menu_perm_withdraw" : None,
                    "menu_modules_wallet" : None,
                    "menu_perm_wallet" : None,
                    "menu_modules_notify" : None,
                    "menu_perm_notify" : None,
                    "menu_modules_transfer" : None,
                    "menu_perm_transfer" : None,
                    "menu_modules_rpc" : None,
                    "menu_perm_rpc" : None,
                    "menu_modules_cms" : None,
                    "menu_perm_cms" : None,
                    "menu_modules_faq" : None,
                    "menu_perm_faq" : None,
                    "menu_modules_email_template" : None,
                    "menu_perm_email_template" : None,
                    "menu_modules_del_acc_reason" : None,
                    "menu_perm_del_acc_reason" : None,
                    "menu_modules_del_acc_request" : None,
                    "menu_perm_del_acc_request" : None,
                    "menu_modules_support" : None,
                    "menu_perm_support" : None,
                    "menu_modules_currency" : None,
                    "menu_perm_currency" : None,
                    "menu_modules_marketprice" : None,
                    "menu_perm_marketprice" : None,
                    "menu_modules_admin_profit" : None,
                    "menu_perm_admin_profit" : None,
                    "menu_modules_step" : None,
                    "menu_perm_step" : None,
                    "menu_modules_ref_reward" : None,
                    "menu_perm_ref_reward" : None,
                    "menu_modules_stake" : None,
                    "menu_perm_stake" : None,
                    "menu_modules_internal" : None,
                    "menu_perm_internal" : None

                }

        except User.DoesNotExist:
            return{
                "check_user" : None
            }
    else:

        return{}
    


def user_submenu_permissions(request):
    if (request.user.id):
        try:
            check_user = User.objects.get(Q(id = request.user.id) & (Q(admin_user_profile__role=0) | Q(admin_user_profile__role=1)))
            try:
                sub_module_userlist = SubMenuModule.objects.get(sub_module_name = 'User List')
                sub_menu_perm_user_list = SubMenuPermission.objects.get(Q(sub_menu_name_id = sub_module_userlist.id) & Q(user_permissions=request.user.id))

                sub_module_adduser = SubMenuModule.objects.get(sub_module_name = 'Add User')
                sub_menu_perm_adduser = SubMenuPermission.objects.get(Q(sub_menu_name_id = sub_module_adduser.id) & Q(user_permissions=request.user.id))

                sub_module_walletaddress = SubMenuModule.objects.get(sub_module_name = 'Wallet Address List')
                sub_menu_perm_walletaddress = SubMenuPermission.objects.get(Q(sub_menu_name_id = sub_module_walletaddress.id) & Q(user_permissions=request.user.id))

                sub_module_ticket_category = SubMenuModule.objects.get(sub_module_name = 'Support Ticket Category')
                sub_menu_perm_ticket_category = SubMenuPermission.objects.get(Q(sub_menu_name_id = sub_module_ticket_category.id) & Q(user_permissions=request.user.id))

                sub_module_ticket_request = SubMenuModule.objects.get(sub_module_name = 'Support Ticket User Request')
                sub_menu_perm_ticket_request = SubMenuPermission.objects.get(Q(sub_menu_name_id = sub_module_ticket_request.id) & Q(user_permissions=request.user.id))

                # sub_module_withdraw_request = SubMenuModule.objects.get(sub_module_name = 'Withdraw History')
                # sub_menu_perm_withdraw_request = SubMenuPermission.objects.get(Q(sub_menu_name_id = sub_module_withdraw_request.id) & Q(user_permissions=request.user.id))

                # sub_module_pending_request = SubMenuModule.objects.get(sub_module_name = '  ')
                # sub_menu_perm_pending_request = SubMenuPermission.objects.get(Q(sub_menu_name_id = sub_module_pending_request.id) & Q(user_permissions=request.user.id))

                # sub_module_payout_request = SubMenuModule.objects.get(sub_module_name = 'Hold Payout Withdraw History')
                # sub_menu_perm_payout_request = SubMenuPermission.objects.get(Q(sub_menu_name_id = sub_module_payout_request.id) & Q(user_permissions=request.user.id))

                return{
                    "sub_menu_permissions_context_userlist" : sub_menu_perm_user_list.access_status,
                    "sub_menu_permissions_context_adduser" : sub_menu_perm_adduser.access_status,
                    "sub_menu_permissions_context_walletaddress" : sub_menu_perm_walletaddress.access_status,
                    "sub_menu_permissions_context_ticket_category" : sub_menu_perm_ticket_category.access_status,
                    "sub_menu_permissions_context_ticket_request" : sub_menu_perm_ticket_request.access_status,
                    # "sub_menu_permissions_context_withdraw_request" : sub_menu_perm_withdraw_request.access_status,
                    # "sub_menu_permissions_context_pending_request" : sub_menu_perm_pending_request.access_status,
                    # "sub_menu_permissions_context_payout_request" : sub_menu_perm_payout_request.access_status,

                                                                    

                }
            except:
                return{
                    "sub_module_userlist" : 0,
                    "sub_menu_perm_user_list" : 0,
                    "sub_module_adduser" : 0,
                    "sub_menu_perm_adduser" : 0,
                    "sub_module_walletaddress" :0,
                    "sub_menu_perm_walletaddress" :0,
                    "sub_module_ticket_category" : 0,
                    "sub_menu_perm_ticket_category" : 0,
                    "sub_module_ticket_request" : 0,
                    "sub_menu_perm_ticket_request" : 0,
                    # "sub_module_withdraw_request":0,
                    # "sub_menu_perm_withdraw_request":0,
                    # "sub_module_pending_request":0,
                    # "sub_menu_perm_pending_request":0,
                    # "sub_module_payout_request":0,
                    # "sub_menu_perm_payout_request":0,


                }
        except User.DoesNotExist:
            return{}
    else:

        return{}


def user_iconmenu_permissions(request):
    if (request.user.id):
        try:
            check_user = User.objects.get(Q(id = request.user.id) & (Q(admin_user_profile__role=0) | Q(admin_user_profile__role=1)))
            try:
                icon_module_userlist_action = IconMenuModule.objects.get(icon_module_name = 'Actions')
                icon_menu_perm_userlist_action = IconMenuPermission.objects.get(Q(icon_menu_name_id = icon_module_userlist_action.id) & Q(user_permissions=request.user.id))

                icon_module_userlist_wall_address = IconMenuModule.objects.get(icon_module_name = 'Wallet address')
                icon_menu_perm_userlist_wall_address = IconMenuPermission.objects.get(Q(icon_menu_name_id = icon_module_userlist_wall_address.id) & Q(user_permissions=request.user.id))

                icon_module_userlist_history = IconMenuModule.objects.get(icon_module_name = 'History')
                icon_menu_perm_userlist_history = IconMenuPermission.objects.get(Q(icon_menu_name_id = icon_module_userlist_history.id) & Q(user_permissions=request.user.id))

                icon_module_userlist_ref_hist = IconMenuModule.objects.get(icon_module_name = 'Referal History')
                icon_menu_perm_userlist_ref_hist = IconMenuPermission.objects.get(Q(icon_menu_name_id = icon_module_userlist_ref_hist.id) & Q(user_permissions=request.user.id))

                icon_module_userlist_add_plan = IconMenuModule.objects.get(icon_module_name = 'Add Plan')
                icon_menu_perm_userlist_add_plan = IconMenuPermission.objects.get(Q(icon_menu_name_id = icon_module_userlist_add_plan.id) & Q(user_permissions=request.user.id))

                icon_module_userlist_step_update = IconMenuModule.objects.get(icon_module_name = 'Step Update')
                icon_menu_perm_userlist_step_update = IconMenuPermission.objects.get(Q(icon_menu_name_id = icon_module_userlist_step_update.id) & Q(user_permissions=request.user.id))

                icon_module_userlist_miss_rew = IconMenuModule.objects.get(icon_module_name = 'Missing reward update')
                icon_menu_perm_userlist_miss_rew = IconMenuPermission.objects.get(Q(icon_menu_name_id = icon_module_userlist_miss_rew.id) & Q(user_permissions=request.user.id))

                icon_module_userlist_stake_hist = IconMenuModule.objects.get(icon_module_name = 'Staking history')
                icon_menu_perm_userlist_stake_hist = IconMenuPermission.objects.get(Q(icon_menu_name_id = icon_module_userlist_stake_hist.id) & Q(user_permissions=request.user.id))


                return{
                    "sub_menu_permissions_context_userlist_action" : icon_menu_perm_userlist_action.access_status,
                    "sub_menu_permissions_context_userlist_wall_address" : icon_menu_perm_userlist_wall_address.access_status,
                    "sub_menu_permissions_context_userlist_history" : icon_menu_perm_userlist_history.access_status,
                    "sub_menu_permissions_context_userlist_ref_hist" : icon_menu_perm_userlist_ref_hist.access_status,
                    "sub_menu_permissions_context_userlist_add_plan" : icon_menu_perm_userlist_add_plan.access_status,
                    "sub_menu_permissions_context_userlist_step_update" : icon_menu_perm_userlist_step_update.access_status,
                    "sub_menu_permissions_context_userlist_miss_rew" : icon_menu_perm_userlist_miss_rew.access_status,
                    "sub_menu_permissions_context_userlist_stake_hist" : icon_menu_perm_userlist_stake_hist.access_status,
                    

                }
            except:
                return{
                    "icon_module_userlist_action" : 0,
                    "icon_menu_perm_userlist_action" : 0,
                    "icon_module_userlist_wall_address" : 0,
                    "icon_menu_perm_userlist_wall_address" : 0,
                    "icon_module_userlist_history" : 0,
                    "icon_menu_perm_userlist_history" : 0,
                    "icon_module_userlist_ref_hist" : 0,
                    "icon_menu_perm_userlist_ref_hist" : 0,
                    "icon_module_userlist_add_plan" : 0,
                    "icon_menu_perm_userlist_add_plan" : 0,
                    "icon_module_userlist_step_update" : 0,
                    "icon_menu_perm_userlist_step_update" : 0,
                    "icon_module_userlist_miss_rew" : 0,
                    "icon_menu_perm_userlist_miss_rew" : 0,
                    "icon_module_userlist_stake_hist" : 0,
                    "icon_menu_perm_userlist_stake_hist" : 0
                }
        except User.DoesNotExist:
            return{}
    else:

        return{}
