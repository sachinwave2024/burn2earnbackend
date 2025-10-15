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
from .views import delete_account  # Import the view
from .views import DownloadImageView





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
    path('withdrawUSDT_request/', views.withdrawUSDT_request, name='withdrawUSDT_request'),
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
    path('resend_otp_org/', views.resend_otp_org, name='resend_otp_org'),
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
    path('disclaimer/', views.disclaimer_page, name='disclaimer'),
    path('', views.landing_page, name='landing_page'),
    path('api/landing/', views.landing_page1, name='landing_page1'),
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
    path('buy_plan_test/', views.buy_plan_test, name='buy_plan_test'),
    path('buy_plan_premium/', views.buy_plan_premium, name='buy_plan_premium'),
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
    path('plan_JW_send_api/', views.plan_JW_send_api, name='plan_JW_send_api'),




    path('Active_Currency_List/', views.Active_Currency_List, name='Active_Currency_List'),


    path("current_api/",views.Current_API,name = 'current_api'),

    path("plan_edit_api/<int:id>/",views.Plan_edit_api,name = 'plan_edit_api'),
    path("stack_history_edit_api/<int:id>/",csrf_exempt(views.stack_history_edit_api),name = 'stack_history_edit_api'),
    path("user_add_plan_api/",views.user_add_plan_api,name = 'user_add_plan_api'),
    path("api_status_change/",views.api_status_change,name = 'api_status_change'),
    path("stake_credit_blance/<int:id>/",views.stake_credit_blance,name = 'stake_credit_blance'),
    path("cron_api_market_price/",views.cron_api_market_price,name = 'cron_api_market_price'),
    path("premium_deposit_api/",views.premium_deposit_api,name = 'premium_deposit_api'),
    path("premium_Transfer_History_List/",views.premium_Transfer_History_List,name = 'premium_Transfer_History_List'),
    path("Premium_wallet_blance/<int:id>/",views.Premium_wallet_blance,name = 'Premium_wallet_blance'),
    path("transfer_premium_amount/",views.transfer_premium_amount,name = 'transfer_premium_amount'),
    path("update_plan_end_date/",views.update_plan_end_date,name = 'update_plan_end_date'),
    path("update_plan_end_date_internal/",views.update_plan_end_date_internal,name = 'update_plan_end_date_internal'),
    path("add_purchase/",views.add_purchase,name = 'add_purchase'),
    path("add_dummy_purchase/",views.add_dummy_purchase,name = 'add_dummy_purchase'),
    path("company_raferral/",views.company_raferral,name = 'company_raferral'),
    path("add_leg_business/",views.add_leg_business,name = 'add_leg_business'),
    path("process_rewards/",views.process_rewards,name = 'process_rewards'),
    path('withdraw_LB/', views.withdraw_LB, name='withdraw_LB'),
    path('LB_transaction_history/', views.LB_transaction_history, name='LB_transaction_history'),
    path("LB_Transfer_History_List/",views.LB_Transfer_History_List,name = 'LB_Transfer_History_List'),
    path("auto_update_missing_rewards/",views.auto_update_missing_rewards,name = 'auto_update_missing_rewards'),
    path("update_market_price/",views.update_market_price,name = 'update_market_price'),
    path("AddDirectUSDTstatus/",views.AddDirectUSDTstatus,name = 'AddDirectUSDTstatus'),
    path("Deduct_pw/",views.Deduct_pw,name = 'Deduct_pw'),
    path("roll_process_rewards/",views.roll_process_rewards,name = 'roll_process_rewards'),
    path("clone_LBbusinessapi/",views.clone_LBbusinessapi,name = 'clone_LBbusinessapi'),
    path('generate_details/', views.generate_details, name='generate_details'),
    path('generate_details_from_private_key/', views.generate_details_from_private_key, name='generate_details_from_private_key'),
    path('generate_wallet_with_mnemonic/', views.generate_wallet_with_mnemonic, name='generate_wallet_with_mnemonic'),
    path('token_conversion/', views.token_conversion, name='token_conversion'),
    
    path('decrypt_private_key_api/', views.decrypt_private_key_api, name='decrypt_private_key_api'),
    path('encrypt_private_key_api/', views.encrypt_private_key_api, name='encrypt_private_key_api'),
    
    
    
    path('Health_ROI/', views.Health_ROI, name='Health_ROI'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('delete_account/', delete_account, name='delete_account'),
    path('plan_expire/', views.plan_expire, name='plan_expire'),
    path('Trade_expire/', views.Trade_expire, name='Trade_expire'),
    
    
    path('find_email_template/', views.find_email_template, name='find_email_template'),
    
    
    
    
    
    
    
    
    
    ##for trading boat
    path('Boat_JW_send_api/', views.Boat_JW_send_api, name='Boat_JW_send_api'),
    path('Boat_USDT_send_api/', views.Boat_USDT_send_api, name='Boat_USDT_send_api'),
    path('Support_JW_TradeBot/', views.Support_JW_TradeBot, name='Support_JW_TradeBot'),
    path('buy_boat_plan/', views.buy_boat_plan, name='buy_boat_plan'),
    path('buy_boat_trade/', views.buy_boat_trade, name='buy_boat_trade'),
    path('auto_roi_reward/', views.auto_roi_reward, name='auto_roi_reward'),
    path('Boat_plan_detail/', views.Boat_plan_detail, name='Boat_plan_detail'),
    path('Boat_plan_purchase_API/', views.Boat_plan_purchase_API, name='Boat_plan_purchase_API'),
    path('Boat_purchase_API/', views.Boat_purchase_API, name='Boat_purchase_API'),
    path('Boat_Transfer_History_List/', views.Boat_Transfer_History_List, name='Boat_Transfer_History_List'),
    path('roi_reward_data/', views.roi_reward_data, name='roi_reward_data'),
    path('Trade_earning_summary/', views.Trade_earning_summary, name='Trade_earning_summary'),
    path('Trade_Referral_history/', views.Trade_Referral_history, name='Trade_Referral_history'),
    path('Bot_Direct_referral_list/',views.Bot_Direct_referral_list,name = "Bot_Direct_referral_list"),
    path('Trade_Claim/',views.Trade_Claim,name = "Trade_Claim"),
    path('ClaiAamount/',views.ClaiAamount,name = "ClaiAamount"),
    path('Monthly_matching_bonus/',views.Monthly_matching_bonus,name = "Monthly_matching_bonus"),
    path('Bot_Referral_history/', views.Bot_Referral_history, name='Bot_Referral_history'),
    path('transfer_stake_amount/', views.transfer_stake_amount, name='transfer_stake_amount'),
    
    
    
    
    ### for mp plan
    
    path('MPPlanlist_API/', views.MPPlanlistGroupedAPIView, name='MPPlanlist_API'),
    path('MP_USDT_send_api/', views.MP_USDT_send_api, name='MP_USDT_send_api'),
    path('Support_JW_MP/', views.Support_JW_MP, name='Support_JW_MP'),
    path('Support_JWC_MP/', views.Support_JWC_MP, name='Support_JWC_MP'),
    path('JWMPPlan/', views.JWMPPlan, name='JWMPPlan'),
    path('release_upline_referral/', views.release_upline_referral, name='release_upline_referral'),
    path('MP_plan_detail/', views.MP_plan_detail, name='MP_plan_detail'),
    path('JWMPPlan_classic/', views.JWMPPlan_classic, name='JWMPPlan_classic'),
    path('Performance_bonus/', views.Performance_bonus, name='Performance_bonus'),
    path('MPHealthReward/', views.MPHealthReward, name='MPHealthReward'),
    path('MP_Fee_History_List/', views.MP_Fee_History_List, name='MP_Fee_History_List'),
    path('MP_Plan_History_List/', views.MP_Plan_History_List, name='MP_Plan_History_List'),
    
    path('MP_earning_summary/', views.MP_earning_summary, name='MP_earning_summary'),
    path('MP_Referral_history/', views.MP_Referral_history, name='MP_Referral_history'),
    path('User_Login_api/', views.User_Login_api, name='User_Login_api'),
    path('add_User_new/', views.add_User_new, name='add_User_new'),
    path('BNBStaus_update/', views.BNBStaus_update, name='BNBStaus_update'),
    path('MPlan_auto_expire/', views.MPlan_auto_expire, name='MPlan_auto_expire'),
    path('MPlan_userexpire/', views.MPlan_userexpire, name='MPlan_userexpire'),
    path('user_wallet_balance/', views.user_wallet_balance, name='user_wallet_balance'),
    
    
    
    
    path('swap_tokens/', views.swap_tokens, name='swap_tokens'),
    path('Swapusdt_jwc/', views.Swapusdt_jwc, name='Swapusdt_jwc'),
    path('Swapjwc_usdt/', views.Swapjwc_usdt, name='Swapjwc_usdt'),
    path('swapsend_history/', views.swapsend_history, name='swapsend_history'),
    path('swaprecieve_history/', views.swaprecieve_history, name='swaprecieve_history'),
    
    
    
    path('promobonus/', views.promobonus, name='promobonus'),
    path('promobonus_detail/', views.promobonus_detail, name='promobonus_detail'),
    path('PROMOHISTORY_List/', views.PROMOHISTORY_List, name='PROMOHISTORY_List'),
    
    
    
    ### for burn to earn 
    path('BurntoEarn/', views.BurntoEarn, name='BurntoEarn'),
    path('BurntoEarn_detail/', views.BurntoEarn_detail, name='BurntoEarn_detail'),
    path('burn_upline_referral/', views.burn_upline_referral, name='burn_upline_referral'),
    path('burn_process_rewards/', views.burn_process_rewards, name='burn_process_rewards'),
    path('burnjw_history/', views.burnjw_history, name='burnjw_history'),
    
    path('burn_earning_history/', views.burn_earning_history, name='burn_earning_history'),
    path('burn_Referral_history/', views.burn_Referral_history, name='burn_Referral_history'),
    path('burnwithdraw_request/', views.burnwithdraw_request, name='burnwithdraw_request'),
    path('burntransaction_history/', views.burntransaction_history, name='burntransaction_history'),
    path('burnperformance/', views.burnperformance, name='burnperformance'),
    
    
    
    path('classicBurntoEarn/', views.classicBurntoEarn, name='classicBurntoEarn'),
    path('classicBurntoEarn_detail/', views.classicBurntoEarn_detail, name='classicBurntoEarn_detail'),
    path('classicburn_upline_referral/', views.classicburn_upline_referral, name='classicburn_upline_referral'),
    path('classicburn_process_rewards/', views.classicburn_process_rewards, name='classicburn_process_rewards'),
    path('classicburnjw_history/', views.classicburnjw_history, name='classicburnjw_history'),
    
    path('classicburn_earning_history/', views.classicburn_earning_history, name='classicburn_earning_history'),
    path('classicburn_Referral_history/', views.classicburn_Referral_history, name='classicburn_Referral_history'),
    path('classicburnperformance/', views.classicburnperformance, name='classicburnperformance'),
    
    
    
    path('JWMPPlan_classic_hash/', views.JWMPPlan_classic_hash, name='JWMPPlan_classic_hash'),
    path('JWMPPlan_hash/', views.JWMPPlan_hash, name='JWMPPlan_hash'),
    path('EarntoBurn_hash/', views.EarntoBurn_hash, name='EarntoBurn_hash'),
    
    
    path('download-image/', DownloadImageView.as_view(), name='download_image'),
    
    
    path('burnperformanceaftermay20/', views.burnperformanceaftermay20, name='burnperformanceaftermay20'),
    
    path('create-wallet/', views.create_wallet, name='create_wallet'),
    path('check-usdt-balances/', views.check_usdt_balances, name='check_usdt_balances'),
    path("create_child_wallet/", views.create_child_wallet, name="create_child_wallet"),
    path("generate_wallets_range/", views.generate_wallets_range, name="generate_wallets_range"),
    path("check_usdt_balances_range/", views.check_usdt_balances_range, name="check_usdt_balances_range"),
    path('send_fund/', views.send_fund, name='send_fund'),
    





    





]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = format_suffix_patterns(urlpatterns)
