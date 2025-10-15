

from django.urls import path
from django.contrib.auth.decorators import login_required
from django.urls import include, path,re_path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
app_name = 'trade_admin_auth'

from . import views
from .views import Add_referral_level, AddDeleteReason, Addplan, Delete_Plan, Delete_Referral, Delete_Request, Delete_inactive, Detail_Delete_Request, DetailWithdraw, EditCompanySetting, List2X_Boost, List_Admin_profit_Request, List_Delete_Account_Reason, List_Delete_Account_Request, List_Referral_reward, List_Send_Withdraw_History, List_Steps_history, List_User_Management, List_Withdraw_Request, List_Withdraw_values_internal, List_admin_notification_message, List_front_page_management, List_market_internal, List_plan, List_referral_level, List_user_referral, List_wallet, ListSteps_Management, User_Wallet_Address_Detail,editprofilesetting,ChangePasswordView,BurnList_Withdraw_Request
from .views import ListSubAdmin,CreateSubadminUser,DeleteSubAdmin,ListAdminactivity
from .views import DetailTradeUser
from .views import ChangePatternView,ListTradeDeactiveUserAdmin,ListUseractivity
from .views import DeleteTwoFAAdmin,ListTradeUserAdmin,DeleteTradeuserAdmin,ListTwoFAUserAdmin
from .views import ListAttemptIPBlock,DeleteAttemptIPBlock,ListBlockIp,AddBlockIp,EditBlockIp
from .views import Admin_passwordresetconfirm
from .views import manage_emails, delete_email
from django.views.decorators.csrf import csrf_exempt
from .views import Admin_approve_withdraw,get_promobonus_details, PROMOBONUS,update_promobonus_status,encrypt_private_key_api,get_Swap_details,SWAP,Approve_swap,BURNWITHDRAW,get_Burn_details


app_name = 'trade_admin_auth'

loginurl='/RZqYkZRuiBaffkx/'

urlpatterns = [

	 re_path('admin_auth', views.adminlogin_auth, name='admin_auth'),
	 re_path('logout',    login_required(views.log_out,login_url=loginurl), name='logout'),
	 re_path('dashboard',    login_required(views.dashboard,login_url=loginurl), name='dashboard'),
	 re_path('adminforgotpassword', views.adminforgotpassword, name='adminforgotpassword'),
	 re_path(r'^admin_confirm_reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.Admin_passwordresetconfirm,name='admin_confirm_reset'),
	 re_path('adminforgotpattern', views.adminforgotpattern, name='adminforgotpattern'),
	 re_path(r'^adminpatternupdate/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.Adminpatternupdate, name='adminpatternupdate'),
	 re_path(r'^general_settings/(?P<pk>[-\w]+)/$', login_required(views.EditCompanySetting.as_view(),login_url=loginurl), name='general_settings'),
	 re_path(r'^profile_settings/(?P<user_id>[-\w]+)/$', login_required(views.editprofilesetting,login_url=loginurl), name='profile_settings'),
	 re_path(r'^change_password/$', login_required(ChangePasswordView.as_view(),login_url=loginurl), name='change_password'),
	 re_path(r'^patternchange/(?P<user_id>[-\w]+)/$', login_required(views.change_pattern_view,login_url=loginurl), name='patternchange'),
	 re_path(r'^subadminactivity/$', login_required(ListAdminactivity.as_view(),login_url=loginurl), name='subadminactivity'),

	 
	 re_path(r'^sub_admin_profile_settings/(?P<user_id>[-\w]+)/$', login_required(views.edit_subadmin_profilesetting,login_url=loginurl), name='sub_admin_profile_settings'),
	 re_path('subadminlist',    login_required(ListSubAdmin.as_view(),login_url=loginurl), name='subadminlist'),
	 re_path(r'^updatepermissions/(?P<user_id>[-\w]+)/$',  login_required(views.SubAdmin_FormView,login_url=loginurl), name='updatepermissions'),
	 re_path('subadmin_add',    login_required(CreateSubadminUser.as_view(),login_url=loginurl), name='subadmin_add'),
     path('subadmin_sub_menu_add/<int:id>/',views.CreateSubAdmin_SubMenu_User,name = "subadmin_sub_menu_add"),
	 path('subadmin_iconmenu_add/<int:id>/',views.CreateSubAdmin_IconMenu_User,name = "subadmin_iconmenu_add"),
	 re_path(r'^delete_subadmin/(?P<pk>[-\w]+)/$', login_required(DeleteSubAdmin.as_view(),login_url=loginurl), name='delete_subadmin'),
     re_path(r'^subadmin_change_password/(?P<user_id>[-\w]+)/$', login_required(views.SubAdminChangePasswordView), name='subadmin_change_password'),
     re_path(r'^subadmin_patternchange/(?P<user_id>[-\w]+)/$', login_required(views.sub_adminchange_pattern_view,login_url=loginurl), name='subadmin_patternchange'),
	 re_path(r'^subadmin_edit_permission/(?P<user_id>[-\w]+)/$', login_required(views.SubadminEditPermission,login_url=loginurl), name='subadmin_edit_permission'),
     re_path(r'^subadmin_submenu_edit_permission/(?P<user_id>[-\w]+)/$', login_required(views.Subadmin_SubMenu_EditPermission,login_url=loginurl), name='subadmin_submenu_edit_permission'),
     re_path(r'^subadmin_iconmenu_edit_permission/(?P<user_id>[-\w]+)/$', login_required(views.Subadmin_IconMenu_EditPermission,login_url=loginurl), name='subadmin_iconmenu_edit_permission'),
	 
	 re_path(r'^2fauserdelete/(?P<pk>[-\w]+)/$', login_required(DeleteTwoFAAdmin.as_view(),login_url=loginurl), name='2fauserdelete'),
	 re_path('tradeuserlist', login_required(ListTradeUserAdmin.as_view(),login_url=loginurl), name='tradeuserlist'),
	 re_path('deactivateuserlist', login_required(ListTradeDeactiveUserAdmin.as_view(),login_url=loginurl), name='deactivateuserlist'),
	 re_path(r'^delete_tradeuser/(?P<pk>[-\w]+)/$', login_required(DeleteTradeuserAdmin.as_view(),login_url=loginurl), name='delete_tradeuser'),
	 re_path('twofalist', login_required(ListTwoFAUserAdmin.as_view(),login_url=loginurl), name='twofalist'),
	 re_path(r'^detail_tradeuser/(?P<pk>[-\w]+)/$', login_required(DetailTradeUser.as_view(),login_url=loginurl), name='detail_tradeuser'),
	 re_path('activityuserlist', login_required(ListUseractivity.as_view(),login_url=loginurl), name='activityuserlist'),
	 re_path('admin2fa', login_required(views.admintwofaupdate,login_url=loginurl), name='admin2fa'),
	 re_path(r'^twofaadmin/(?P<uid>[-\w]+)', views.admintwofa, name='twofaadmin'),
	 re_path('attemptiplist', login_required(ListAttemptIPBlock.as_view(),login_url=loginurl), name='attemptiplist'),
	 re_path(r'^attempt_deleteblockip/(?P<pk>[-\w]+)/$', login_required(DeleteAttemptIPBlock.as_view(),login_url=loginurl), name='attempt_deleteblockip'),
	
	 re_path('blockiplist', login_required(ListBlockIp.as_view(),login_url=loginurl), name='blockiplist'),
	 re_path('addblockip', login_required(AddBlockIp.as_view(),login_url=loginurl), name='addblockip'),
	 re_path(r'^editblockip/(?P<pk>[-\w]+)/$', login_required(views.EditBlockIp.as_view(),login_url=loginurl), name='editblokip'),


	 re_path('ListSteps_Management', login_required(ListSteps_Management.as_view(),login_url=loginurl), name='ListSteps_Management'),
	 re_path(r'^edit_Step_Management/(?P<pk>[-\w]+)/$', login_required(views.Edit_Step_Management.as_view(),login_url=loginurl), name='Edit_Step_Management'),

	 re_path('List2X_Boost', login_required(List2X_Boost.as_view(),login_url=loginurl), name='List2X_Boost'),
	 re_path(r'^Edit_2X_Management/(?P<pk>[-\w]+)/$', login_required(views.Edit_2X_Management.as_view(),login_url=loginurl), name='Edit_2X_Management'),
	 
	 re_path('List_User_Management/', login_required(List_User_Management.as_view(),login_url=loginurl), name='List_User_Management'),
	 re_path(r'^Edit_User_Management/(?P<pk>[-\w]+)/$', login_required(views.Edit_User_Management.as_view(),login_url=loginurl), name='Edit_User_Management'),

	 re_path(r'^List_Steps_history/(?P<pk>[-\w]+)/$', login_required(List_Steps_history.as_view(),login_url=loginurl), name='List_Steps_history'),
	 
	 re_path('List_Withdraw_Request/', login_required(List_Withdraw_Request.as_view(),login_url=loginurl), name='List_Withdraw_Request'),
	 re_path('BurnList_Withdraw_Request/', login_required(BurnList_Withdraw_Request.as_view(),login_url=loginurl), name='BurnList_Withdraw_Request'),
	 re_path(r'^DetailWithdraw/(?P<pk>[-\w]+)/$', login_required(DetailWithdraw.as_view(),login_url=loginurl), name='DetailWithdraw'),


	 re_path('List_Referral_reward', login_required(List_Referral_reward.as_view(),login_url=loginurl), name='List_Referral_reward'),
	 re_path(r'^Edit_Referral_Reward_Management/(?P<pk>[-\w]+)/$', login_required(views.Edit_Referral_Reward_Management.as_view(),login_url=loginurl), name='Edit_Referral_Reward_Management'),

	 re_path('List_Delete_Account_Reason', login_required(List_Delete_Account_Reason.as_view(),login_url=loginurl), name='List_Delete_Account_Reason'),
	 re_path('AddDeleteReason', login_required(AddDeleteReason.as_view(),login_url=loginurl), name='AddDeleteReason'),
	 re_path(r'^Edit_Delete_Reason_Management/(?P<pk>[-\w]+)/$', login_required(views.Edit_Delete_Reason_Management.as_view(),login_url=loginurl), name='Edit_Delete_Reason_Management'),

	 re_path('List_Delete_Account_Request', login_required(List_Delete_Account_Request.as_view(),login_url=loginurl), name='List_Delete_Account_Request'),
	 re_path(r'^Detail_Delete_Request/(?P<pk>[-\w]+)/$', login_required(Detail_Delete_Request.as_view(),login_url=loginurl), name='Detail_Delete_Request'),
     re_path(r'^Delete_Request/(?P<pk>[-\w]+)/$', login_required(Delete_Request.as_view(),login_url=loginurl), name='Delete_Request'),
     re_path(r'^Delete_inactive/(?P<pk>[-\w]+)/$', login_required(Delete_inactive.as_view(),login_url=loginurl), name='Delete_inactive'),

	 re_path('List_Admin_profit_Request/', login_required(List_Admin_profit_Request.as_view(),login_url=loginurl), name='List_Admin_profit_Request'),

	 re_path('List_plan', login_required(List_plan.as_view(),login_url=loginurl), name='List_plan'),
	 re_path('Addplan', login_required(Addplan.as_view(),login_url=loginurl), name='Addplan'),
	 re_path(r'^Edit_Plan_Management/(?P<pk>[-\w]+)/$', login_required(views.Edit_Plan_Management.as_view(),login_url=loginurl), name='Edit_Plan_Management'),
     re_path(r'^Delete_Plan/(?P<pk>[-\w]+)/$', login_required(Delete_Plan.as_view(),login_url=loginurl), name='Delete_Plan'),


	 re_path('List_referral_level', login_required(List_referral_level.as_view(),login_url=loginurl), name='List_referral_level'),
	 re_path('Add_referral_level', login_required(Add_referral_level.as_view(),login_url=loginurl), name='Add_referral_level'),
	 re_path(r'^Edit_Referral_level_Management/(?P<pk>[-\w]+)/$', login_required(views.Edit_Referral_level_Management.as_view(),login_url=loginurl), name='Edit_Referral_level_Management'),
     re_path(r'^Delete_Referral/(?P<pk>[-\w]+)/$', login_required(Delete_Referral.as_view(),login_url=loginurl), name='Delete_Referral'),

	 re_path('List_user_referral', login_required(List_user_referral.as_view(),login_url=loginurl), name='List_user_referral'),
	 re_path('List_market_internal', login_required(List_market_internal.as_view(),login_url=loginurl), name='List_market_internal'),
	 re_path(r'^Edit_market_internal_Management/(?P<pk>[-\w]+)/$', login_required(views.Edit_market_internal_Management.as_view(),login_url=loginurl), name='Edit_Referral_level_Management'),

	 re_path('List_Withdraw_values_internal', login_required(List_Withdraw_values_internal.as_view(),login_url=loginurl), name='List_Withdraw_values_internal'),
	 re_path(r'^Edit_Withdraw_value_Management/(?P<pk>[-\w]+)/$', login_required(views.Edit_Withdraw_value_Management.as_view(),login_url=loginurl), name='Edit_Withdraw_value_Management'),

	 path('user_list_management/<str:data>/',login_required(views.user_list_management),name = "user_list_management"),
	 path('user_list_for_update/',login_required(views.user_list_for_update),name = "user_list_for_update"),
	 path('user_list_update/<int:id>/',login_required(views.user_list_update),name = "user_list_update"),

	#  re_path(r'^user_list_management/(?P<relation>[-\w]+)/$', views.UsersHistoryManagement.as_view(), {'relation': 'relation'}, name='user_list_management'),
	 path('disable_withdraw/',login_required(views.disable_withdraw),name = "disable_withdraw"),
	path('disable_pay_later/',login_required(views.disable_pay_later),name = "disable_pay_later"),
	path('isStakeEnable/',login_required(views.isStakeEnable),name = "isStakeEnable"),
	path('isPremiumEnable/',login_required(views.isPremiumEnable),name = "isPremiumEnable"),
 	path('isAdminEnableRrWithdraw/',login_required(views.isAdminEnableRrWithdraw),name = "isAdminEnableRrWithdraw"),
	path('isAdminEnableHrWithdraw/',login_required(views.isAdminEnableHrWithdraw),name = "isAdminEnableHrWithdraw"),
	path('add_purchase_manual/',login_required(views.add_purchase_manual),name = "add_purchase_manual"),
	path('add_purchase_manual_100/',login_required(views.add_purchase_manual_100),name = "add_purchase_manual_100"),
	path('add_purchase_manual_200/',login_required(views.add_purchase_manual_200),name = "add_purchase_manual_200"),

	path('manage_emails/',login_required(views.manage_emails), name='manage_emails'),
    # path('edit_email/<int:id>/', edit_email, name='edit_email'),
    path('delete_email/<int:id>/', login_required(views.delete_email), name='delete_email'),
	 path('disable_buy_plan/',login_required(views.disable_buy_plan),name = "disable_buy_plan"),

	 path('List_wallet', login_required(List_wallet.as_view(),login_url=loginurl), name='List_wallet'),
	 re_path(r'^Edit_List_wallet/(?P<pk>[-\w]+)/$', login_required(views.Edit_wallet.as_view(),login_url=loginurl), name='Edit_List_wallet'),


	 re_path(r'^page_403', views.Page403View, name='page_403'),
	 re_path(r'^page_404', views.Page404View, name='page_404'),
	 re_path(r'^page_500', views.Page500View, name='page_500'),
	 re_path(r'^ipblock404', views.IPBlock404View, name='ipblock404'),
	 re_path(r'^ipblockadmin', views.blockipadmin, name='ipblockadmin'),
	 re_path(r'^adminblockip404', views.adminblockip404, name='adminblockip404'),

	re_path(r'^user_history_table/(?P<pk>[-\w]+)/$', login_required(views.HistoryManagementTable.as_view(),login_url=loginurl), name='user_history_table'),
	 path('step_history_management/<str:data>/',login_required(views.StepHistoryManagement),name = "step_history_management"),
	 re_path(r'^user_referal_history_table/(?P<pk>[-\w]+)/$', login_required(views.ReferalHistoryTable.as_view(),login_url=loginurl), name='user_referal_history_table'),
	 path('Add_User_Plan/<str:id>/',login_required(views.Add_User_Plan),name = "Add_User_Plan"),
	 path('step_update_user/<int:id>/',login_required(views.StepUpdate),name = "step_update_user"),
	 path('step_update_access_token/<int:id>/<str:Date>/<int:val>/',login_required(views.step_update_access_token),name = "step_update_access_token"),
	 path('check_valid/<int:id>/<str:Date>/<int:val>/',login_required(views.check_valid),name = "check_valid"),
	 path('admin_user_shift_plan/<int:id>/',login_required(views.admin_user_shift_plan),name = "admin_user_shift_plan"),
	


	 path('plan_date_edit/<str:id>/',login_required(views.PlanDateEdit),name = "plan_date_edit"),

	 path('plan_expired_users_list/',login_required(views.Plan_Expired_Date_Users_List),name = "plan_expired_users_list"),

	 #  missing reward update url

	path('missing_reward_update_admin/<int:id>/',login_required(views.missing_reward_update_admin),name = "missing_reward_update_admin"),


	# Download CSV url
	
	path('download_csv/', csrf_exempt(views.download_CSV),name = "download_csv"),
	path('download_csv_single_user/<int:id>/', csrf_exempt(views.download_CSV_single_user),name = "download_csv_single_user"),
	path('download_csv_user_management_report/', csrf_exempt(views.download_CSV_user_report),name = "download_csv_user_management_report"),
	path('download_csv_send_withdraw_report/', csrf_exempt(views.download_CSV_sendwithdraw_report),name = "download_csv_send_withdraw_report"),
    path('download_csv_stake_history/', csrf_exempt(views.download_csv_stake_history),name = "download_csv_stake_history"),
	path('download_csv_deposit_history/', csrf_exempt(views.download_csv_deposit_history),name = "download_csv_deposit_history"),
	path('download_csv_claim_history/', csrf_exempt(views.download_csv_claim_history),name = "download_csv_claim_history"),
	path('download_CSV_device_id/', csrf_exempt(views.download_CSV_device_id),name = "download_CSV_device_id"),
	path('download_CSV_full_device_id/', csrf_exempt(views.download_CSV_full_device_id),name = "download_CSV_full_device_id"),

    


	# # Withdraw send url

	re_path('List_Send_Withdraw_History/', login_required(List_Send_Withdraw_History.as_view(),login_url=loginurl), name='List_Send_Withdraw_History'),

	# Notification Management

	re_path('List_admin_notification_message/', login_required(List_admin_notification_message.as_view(),login_url=loginurl), name='List_admin_notification_message'),
	re_path(r'^Edit_admin_notification_message/(?P<pk>[-\w]+)/$', login_required(views.Edit_admin_notification_message.as_view(),login_url=loginurl), name='Edit_admin_notification_message'),


	# Add_User_register url

	path("Add_Register_User/",login_required(views.Add_Register_User),name = "Add_Register_User"),
	 
	re_path('User_Wallet_Address_Detail/(?P<pk>[-\w]+)/$', login_required(User_Wallet_Address_Detail.as_view(),login_url=loginurl), name='User_Wallet_Address_Detail'),
    
	# Marketprice API url

	path('marketprice_api/', login_required(views.MarketPrice_API),name = "marketprice_api"),

	# Front page content
	re_path('List_front_page_management/', login_required(List_front_page_management.as_view(),login_url=loginurl), name='List_front_page_management'),
	re_path(r'^Edit_front_page_management/(?P<pk>[-\w]+)/$', login_required(views.Edit_front_page_management.as_view(),login_url=loginurl), name='Edit_front_page_management'),
    

	path('Edit_RPC/1/', login_required(views.Edit_RPC), name='Edit_RPC'),

    path('wallet_edit_address/<int:id>/',csrf_exempt(views.wallet_edit_address),name='wallet_edit_address'),
    
	path('wallet_address_users_listing/',login_required(views.Wallet_Address_Users_List),name='wallet_address_users_listing'),

	re_path(r'^uplineuser_referal_history_table/(?P<pk>[-\w]+)/$', login_required(views.UplineReferalHistoryTable.as_view(),login_url=loginurl), name='upline_user_referal_history_table'),
	re_path(r'^mpuplineuser_referal_history_table/(?P<pk>[-\w]+)/$', login_required(views.mpUplineReferalHistoryTable.as_view(),login_url=loginurl), name='mpupline_user_referal_history_table'),
	re_path(r'^burnuplineuser_referal_history_table/(?P<pk>[-\w]+)/$', login_required(views.burnUplineReferalHistoryTable.as_view(),login_url=loginurl), name='burnuplineuser_referal_history_table'),
	path('hash_users_listing/',login_required(views.transcation_hash_List),name='hash_users_listing'),
    path('wallet_address_block_list/',login_required(views.wallet_address_block_list),name='wallet_address_block_list'),
    path('unblock_address/<int:id>/',csrf_exempt(views.unblock_address),name='unblock_address'),
	path('wallet_address_block/',login_required(views.wallet_address_block),name='wallet_address_block'),
	path('getUsers/', csrf_exempt(views.getUsers),name = "getUsers"),
	path('getwithdrawUsers/', csrf_exempt(views.getwithdrawUsers),name = "getwithdrawUsers"),
	path('bgetwithdrawUsers/', csrf_exempt(views.bgetwithdrawUsers),name = "bgetwithdrawUsers"),
    path('device_unique/', login_required(views.device_unique),name = "device_unique"),
	path('user_device_id/', csrf_exempt(views.user_device_id),name = "user_device_id"),
    path('device_empty_unique/', login_required(views.device_empty_unique),name = "device_empty_unique"),
	path('user_empty_device_id/', csrf_exempt(views.user_empty_device_id),name = "user_empty_device_id"),
	path('Edit_User_Plan/<str:id>/',login_required(views.Edit_User_Plan),name = "Edit_User_Plan"),
	path('user_add_usdt/<int:id>/', login_required(views.user_add_usdt),name = "user_add_usdt"),
	path('download_CSV_deposit_user/<int:id>/', csrf_exempt(views.download_CSV_deposit_user),name = "download_CSV_deposit_user"),
	path('add_user_deposit/<int:id>/', login_required(views.add_user_deposit),name = "add_user_deposit"), 
	path('delete_withdraw_history/<int:id>/', login_required(views.delete_withdraw_history),name = "delete_withdraw_history"), 
	path('delete_all_withdraw_history/<int:id>/', login_required(views.delete_all_withdraw_history),name = "delete_all_withdraw_history"), 
	path('Edit_withdraw_history/<int:id>/', login_required(views.Edit_withdraw_history),name = "Edit_withdraw_history"), 
	path('reward_update_api/<int:id>/', login_required(views.reward_update_api),name = "reward_update_api"), 
	path('delete_referral/<int:id>/', login_required(views.delete_referral),name = "delete_referral"),
	path('settings_price/', login_required(views.settings_price),name = "settings_price"),
    path('user_plan_edit/<int:id>/', login_required(views.user_plan_edit),name = "user_plan_edit"),
    path('Admin_approve_withdraw/<int:id>/', login_required(views.Admin_approve_withdraw),name = "Admin_approve_withdraw"), 
    path('Admin_approve_withdrawusdt/<int:id>/', login_required(views.Admin_approve_withdrawusdt),name = "Admin_approve_withdrawusdt"), 
    path('Admin_approve_withdraw1/<int:id>/', login_required(views.Admin_approve_withdraw123),name = "Admin_approve_withdraw1"), 
	path('manual_Withdraw_Request/<int:id>/', login_required(views.manual_Withdraw_Request),name = "manual_Withdraw_Request"),
    path('getmultiplewithdrawUsers/', csrf_exempt(views.getmultiplewithdrawUsers),name = "getmultiplewithdrawUsers"),
	path('manual_Withdraw/', login_required(views.manual_Withdraw),name = "manual_Withdraw"),
	path('manual_withdraw_USDT/', login_required(views.manual_withdraw_USDT),name = "manual_withdraw_USDT"),
	path('getmultiplewithdrawUsersusdt/', csrf_exempt(views.getmultiplewithdrawUsersusdt),name = "getmultiplewithdrawUsersusdt"),
 
	path('manual_withdraw_INR/', login_required(views.manual_withdraw_INR),name = "manual_withdraw_INR"),
	path('getmultiplewithdrawUsersinr/', csrf_exempt(views.getmultiplewithdrawUsersinr),name = "getmultiplewithdrawUsersinr"),
	path('Admin_approve_withdrawinr/<int:id>/', login_required(views.Admin_approve_withdrawinr),name = "Admin_approve_withdrawinr"), 

    path('user_hold_payment/<int:id>/', login_required(views.user_hold_payment),name = "user_hold_payment"),
	path('hold_manual_withdraw/', login_required(views.hold_manual_withdraw),name = "hold_manual_withdraw"),
	path('getmultiplewithdrawholdUsers/', csrf_exempt(views.getmultiplewithdrawholdUsers),name = "getmultiplewithdrawholdUsers"),
 
	path('getmultiplewithdrawUsersburntoearn/', csrf_exempt(views.getmultiplewithdrawUsersburntoearn),name = "getmultiplewithdrawUsersburntoearn"),
	path('manual_withdrawburntoearn/', login_required(views.manual_withdrawburntoearn),name = "manual_withdrawburntoearn"),
	path('Admin_approve_withdraw1234/<int:id>/', login_required(views.Admin_approve_withdraw1234),name = "Admin_approve_withdraw1234"), 
	path('burnmanual_Withdraw_Request/<int:id>/', login_required(views.burnmanual_Withdraw_Request),name = "burnmanual_Withdraw_Request"),
 
	path('get_user_pwdetails/', views.get_user_pwdetails, name='get_user_pwdetails'),
    path('USERPW/', views.USERPW, name='USERPW'),
    
    
    
    
    path('stake_admin_approve/<int:id>/', login_required(views.stake_admin_approve),name = "stake_admin_approve"),
	path('stake_manual_withdraw/', login_required(views.stake_manual_withdraw),name = "stake_manual_withdraw"),
	path('getstakemultiplewithdrawUsers/', csrf_exempt(views.getstakemultiplewithdrawUsers),name = "getstakemultiplewithdrawUsers"),
	path('stake_manual_Withdraw_Request/<int:id>/', login_required(views.stake_manual_Withdraw_Request),name = "stake_manual_Withdraw_Request"),
    path('Admin_stake_approve_withdraw/<int:id>/', login_required(views.Admin_stake_approve_withdraw),name = "Admin_stake_approve_withdraw"), 
    path('user_stake_hold_payment/<int:id>/', login_required(views.user_stake_hold_payment),name = "user_stake_hold_payment"),
	path('hold_stake_manual_withdraw/', login_required(views.hold_stake_manual_withdraw),name = "hold_stake_manual_withdraw"),
	path('getstakemultiplewithdrawholdUsers/', csrf_exempt(views.getstakemultiplewithdrawholdUsers),name = "getstakemultiplewithdrawholdUsers"),
	path('premium_wallet_manage/1/', login_required(views.premium_wallet_manage),name = "premium_wallet_manage"),
	path('user_premium_deposit/<int:id>/', login_required(views.user_premium_deposit),name = "user_premium_deposit"),
	path('user_trade_deposit/<int:id>/', login_required(views.user_trade_deposit),name = "user_trade_deposit"),
 
	path('user_burn_deposit/<int:id>/', login_required(views.user_burn_deposit),name = "user_burn_deposit"),
	path('classicuser_burn_deposit/<int:id>/', login_required(views.classicuser_burn_deposit),name = "classicuser_burn_deposit"),
	path('user_monthly_deposit/<int:id>/', login_required(views.user_monthly_deposit),name = "user_monthly_deposit"),
	path('user_monthlyfee_deposit/<int:id>/', login_required(views.user_monthlyfee_deposit),name = "user_monthlyfee_deposit"),

 
	path('user_stake_deposit/<int:id>/', login_required(views.user_stake_deposit),name = "user_stake_deposit"),
	path('botdelete_referral/<int:id>/', login_required(views.botdelete_referral),name = "botdelete_referral"),
	path('mpdelete_referral/<int:id>/', login_required(views.mpdelete_referral),name = "mpdelete_referral"),
	re_path(r'^trade_history_table/(?P<pk>[-\w]+)/$', login_required(views.TradeHistoryManagementTable.as_view(),login_url=loginurl), name='trade_history_table'),
	re_path(r'^stake_history_table/(?P<pk>[-\w]+)/$', login_required(views.StakeHistoryManagementTable.as_view(),login_url=loginurl), name='stake_history_table'),	
	re_path(r'^mp_history_table/(?P<pk>[-\w]+)/$', login_required(views.MPlanHistoryManagementTable.as_view(),login_url=loginurl), name='mp_history_table'),
	re_path(r'^burn_history_table/(?P<pk>[-\w]+)/$', login_required(views.BurnHistoryManagementTable.as_view(),login_url=loginurl), name='burn_history_table'),
	re_path(r'^burnjwc_history_table/(?P<pk>[-\w]+)/$', login_required(views.BurnjwcHistoryManagementTable.as_view(),login_url=loginurl), name='burnjwc_history_table'),
	path('burndelete_referral/<int:id>/', login_required(views.burndelete_referral),name = "burndelete_referral"),
 	path('purchase_bot/<int:id>/', login_required(views.purchase_bot),name = "purchase_bot"),
  
  
	path('get_promobonus_details/', get_promobonus_details, name="get_promobonus_details"),
	path("update_promobonus_status/", update_promobonus_status, name="update_promobonus_status"),
    path('promobonus/', PROMOBONUS, name="PROMOBONUS"),
    path("encrypt-private-key/", encrypt_private_key_api, name="encrypt-private-key"),
    
    path('get_Swap_details/', get_Swap_details, name="get_Swap_details"),
	path("Approve_swap/", Approve_swap, name="Approve_swap"),
    path('SWAP/', SWAP, name="SWAP"),
    
    path('get_Burn_details/', get_Burn_details, name="get_Burn_details"),
    path('BURNWITHDRAW/', BURNWITHDRAW, name="BURNWITHDRAW"),
    path('delete_wallet_address/<int:id>/', login_required(views.delete_wallet_address),name = "delete_wallet_address"),

    
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





