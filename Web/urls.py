"""Api_sample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from API import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt




app_name = 'API'


urlpatterns = [
    path('coin_market_price/', views.coin_market_price, name='coin_market_price'),
    path('adduser/', views.add_User, name='addcategory'),
    path('otp_verification/', views.OTP_Verification, name='otp_verification'),
    path('user_login/', views.User_Login, name='user_login'),
    path('Profile/', views.Profile_data_giving, name='Profile'),
    path('Profile_Update/', views.Profile_Update, name='Profile_Update'),
    path('two_fa/', views.two_fa, name='two_fa'),
    path('google_fitness/', views.Google_fitness, name='google_fitness'),
    path('step_count/', views.step_count, name='step_count'),
    path('step_history_update/', views.step_history, name='step_history_update'),
    path('user_step_history/', views.user_step_history, name='user_step_history'),
    path('user_details_two/', views.reward_footsteps_two, name='user_details_two'),
    path('withdraw_request/', views.withdraw_request, name='withdraw_request'),
    path('two_fa_details/', views.two_fa_details, name='two_fa_details'),
    path('Boost_status/', views.Boost_status, name='Boost_status'),
    path('Maximum_target/', views.Maximum_target, name='Maximum_target'),
    path('two_fa_disable/', views.two_fa_disable, name='two_fa_disable'),
    path('terms_cms/', views.terms_cms, name='terms_cms'),
    path('Privacy_cms/', views.Privacy_cms, name='Privacy_cms'),
    path('FAQ_cms/', views.FAQ_cms, name='FAQ_cms'),
    path('Pin_set/', views.Pin_set, name='Pin_set'),
    path('change_pin/', views.change_pin, name='change_pin'),
    path('Verify_pin/', views.Verify_pin, name='Verify_pin'),
    path('earning_summary/', views.earning_summary, name='earning_summary'),
    path('transaction_history/', views.transaction_history, name='transaction_history'),
    path('Referral_history/', views.Referral_history, name='Referral_history'),
    path('Stake_Credit_History/', views.Stake_Credit, name='Stake_Credit_History'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    path('delete_reason_list/', views.delete_reason_list, name='delete_reason_list'),
    path('delete_account_request/', views.delete_account_request, name='delete_account_request'),
    path('delete_otp_verification/', views.delete_otp_verification, name='delete_otp_verification'),
    path('time_calculation/', views.time_calculation, name='time_calculation'),
    path('referral_details/', views.referral_details, name='referral_details'),
    path('user_target_set/', views.user_target_set, name='user_target_set'),
    path('withdraw_fees/', views.withdraw_fees, name='withdraw_fees'),
    path('front_screen_content/', views.front_screen_content, name='front_screen_content'),
    path('home_page_content/', views.home_page_content, name='home_page_content'),
    path('device_id_update/', views.device_id_update, name='device_id_update'),
    path('provide_TFA/', views.provide_TFA, name='provide_TFA'),
    path('encrypt/<str:input>/', views.encrypt, name='encrypt'),
    path('decrypt/<str:input>/', views.decrypt, name='decrypt'),
    path('privacy/', views.privacy_policy_page, name='privacy'),
    path('terms/', views.terms_condition_page, name='terms'),
    path('', views.landing_page, name='landing_page'),
    path('market_place_status/', views.market_place_status, name='market_place_status'),
    path('country_state/', views.country_state, name='country_state'),
    path('add_address/', views.add_address, name='add_address'),
    path('view_address/', views.view_address, name='view_address'),
    path('verify_google/', views.verify_page, name='verify_google'),
    path('maintanance/', views.maintanance, name='maintanance'),
    path('load_maintanance/', views.load_maintanance, name='load_maintanance'),
    path('select_address/', views.select_address, name='select_address'),
    path('edit_address/', views.edit_address, name='edit_address'),
    path('detail_address/', views.detail_address, name='detail_address'),
    path('delete_address/', views.delete_address, name='delete_address'),
    path('buy_plan/', views.buy_plan, name='buy_plan'),
    path('all_plan/', views.all_plan, name='all_plan'),
    path('referral_system/', views.referral_system, name='referral_system'),
    path('faq_page/', views.faq_page, name='faq_page'),
    path('referral_table/', views.referral__table, name='referral_table'),
    path('User_plan_details/', views.User_plan_details, name='User_plan_details'),
    path('referal_reward/', views.referal_reward, name='referal_reward'),
    path('referalcode/<str:id>/',views.referral_nav,name = "referral_nav"),
    path('plan_static_content/',views.plan_static_content,name = "plan_static_content"),
    path('contract/',views.contract,name = "contract"),
    path('Direct_referral_list/',views.Direct_referral_list,name = "Direct_referral_list"),
    path('current_time/',views.current_time,name = "current_time"),
    path('Current_step_update/',views.Current_step_update,name = "Current_step_update"),
    path('request_notification/<int:start_id>/<int:end_id>/',views.request_notification,name = "request_notification"),
    path('version_code_update/<str:app_type>/<str:android_version>/',views.version_code_update,name = "version_code_update"),
    path('wallet_flush/',views.wallet_flush,name = "wallet_flush"),
    path('Email_send/',views.Email_send,name = "Email_send"),
    path('Pin_reset_Email/',views.Pin_reset_Email,name = "Pin_reset_Email"),
    path('Pin_reset_Email_two/',views.Pin_reset_Email_two,name = "Pin_reset_Email_two"),
    path('pin_set_function_otp_verify/',views.pin_set_function_otp_verify,name = "pin_set_function_otp_verify"),
    path('buy_plan_two/', views.buy_plan_two, name='buy_plan_two'),
    path('direct_referral_tree/',views.direct_referral_tree,name = "direct_referral_tree"),
    path('Direct_referral_list_two/',views.Direct_referral_list_two,name = "Direct_referral_list_two"),
    path('shif_plan/',views.shif_plan,name = "shif_plan"),
    path('shif_plan_details/',views.shif_plan_details,name = "shif_plan_details"),
    path('shift_all_plan/',views.shift_all_plan,name = "shift_all_plan"),
    path('Wallet_details/',views.Wallet_details,name = "Wallet_details"),
    path('missing_reward_update_two/', views.missing_reward_update_two, name='missing_reward_update_two'),
    path('missing_reward_update_two_api/', views.missing_reward_update_two_api, name='missing_reward_update_two_api'),


    path('login_history/', views.login_history, name='login_history'),
    path('login_users_api/<str:Token_header>/', views.login_user_create_api, name='login_users_api'),


    path('purchase_history_api/', views.purchase_history_api, name='purchase_history_api'),
    path('plan_purchase_API/', views.plan_purchase_API, name='plan_purchase_API'),

    
    # Sport module API url
    path('sport_category_list_api/', views.sport_category_api, name='sport_category_list_api'),
    path('user_request_api/', views.user_request_api, name='user_request_api'),
    path('admin_reply_api/<int:id>/', views.admin_reply_api, name='admin_reply_api'),
    path('ticket_list/',views.view_all_ticket,name = 'ticket_list'),
    path('view_ticket_detail/<int:t_id>/',views.View_Ticket_Details_API,name = 'view_ticket_detail'),


    # # Withdraw send function url
    path('send_request_withdraw/', views.withdraw_send_api, name='send_request_withdraw'),
    path('balance_fetch_api/', views.Balance_fetch_API, name='balance_fetch_api'),
    path('withdraw_history_list_api/', views.Withdraw_History_List, name='withdraw_history_list_api'),
    path('Transfer_Function_Email_send/', views.Transfer_Function_Email_send, name='Transfer_Function_Email_send'),
    path('Support_request_withdraw/', views.usdt_send_api, name='Support_request_withdraw'),
    #Step counter status get and update url
    path('step_count_status/', views.step_count_status, name='step_count_status'),
    path('step_count_status_update/', views.step_count_status_update, name='step_count_status_update'),

    path("dynamic_handle/",views.dynamic_handle,name = 'dynamic_handle'),
    path("user_address_trust_live/",views.user_address_trust,name = 'user_address_trust_live'),
    path("user_address_trust_live_edit/",views.user_address_trust_edit,name = 'user_address_trust_live_edit'),
    path('plan_usdt_send_api/', views.plan_usdt_send_api, name='plan_usdt_send_api'),




    path('Active_Currency_List/', views.Active_Currency_List, name='Active_Currency_List'),


    path("current_api/",views.Current_API,name = 'current_api'),

    path("plan_edit_api/<int:id>/",views.Plan_edit_api,name = 'plan_edit_api'),
    path("stack_history_edit_api/<int:id>/",csrf_exempt(views.stack_history_edit_api),name = 'stack_history_edit_api'),
    path("user_add_plan_api/",views.user_add_plan_api,name = 'user_add_plan_api'),
    path("api_status_change/",views.api_status_change,name = 'api_status_change'),
    path("stake_credit_blance/<int:id>/",views.stake_credit_blance,name = 'stake_credit_blance'),
    path("cron_api_market_price/",views.cron_api_market_price,name = 'cron_api_market_price'),
    path("transfer_premium_amount/",views.transfer_premium_amount,name = 'transfer_premium_amount'),
    path("update_plan_end_date/",views.update_plan_end_date,name = 'update_plan_end_date'),
    path("update_plan_end_date_internal/",views.update_plan_end_date_internal,name = 'update_plan_end_date_internal'),
    path("company_raferral/",views.company_raferral,name = 'company_raferral'),
    path("add_purchase/",views.add_purchase,name = 'add_purchase'),
    


    





]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = format_suffix_patterns(urlpatterns)
