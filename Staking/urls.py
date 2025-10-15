from django.urls import include, path,re_path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from Staking import views

from django.views.decorators.csrf import csrf_exempt
from .views import Add_Staking_Referral, Delete_Referral_stake, List_Stake_Claim_History, List_Stake_credit,List_Staking_Referral,List_Stake, StakeHistoryManagementTable
from .views import List_Internal_Transfer_History,List_Stake_Deposit_History

app_name = 'staking'

loginurl='/RZqYkZRuiBaffkx/'

urlpatterns = [

    # re_path('stake_plan_list/', login_required(List_Staking_Plan.as_view(),login_url=loginurl), name='stake_plan_list'),
    # re_path('Add_Staking_Plan/', login_required(Add_Staking_Plan.as_view(),login_url=loginurl), name='Add_Staking_Plan'),
    path('Edit_Staking_Plan/1/', views.Edit_Staking_Plan, name='Edit_Staking_Plan'),
    # re_path(r'^Delete_Staking_Plan/(?P<pk>[-\w]+)/$', login_required(Delete_Staking_Plan.as_view(),login_url=loginurl), name='Delete_Staking_Plan'),


    #Referral MAnagement
    re_path('List_Staking_Referral/', login_required(List_Staking_Referral.as_view(),login_url=loginurl), name='List_Staking_Referral'),
    re_path('Add_Staking_Referral/', login_required(Add_Staking_Referral.as_view(),login_url=loginurl), name='Add_Staking_Referral'),
    path('Edit_Staking_Referral/<int:id>/', views.Edit_Staking_Referral, name='Edit_Staking_Referral'),
    re_path(r'^Delete_Referral_stake/(?P<pk>[-\w]+)/$', login_required(Delete_Referral_stake.as_view(),login_url=loginurl), name='Delete_Referral_stake'),




    # InternalTransferFeesUpdate       
    path('internal_transfer_fees_update/1/', login_required(views.InternalTransferFeesUpdate), name='internal_transfer_fees_update'),
    re_path('List_Internal_Transfer_History/', login_required(List_Internal_Transfer_History.as_view(),login_url=loginurl), name='List_Internal_Transfer_History'),

    # Internal_transfer_API
    path('internal_transfer/',views.Internal_Transfer,name="internal_transfer"),
    path('Internal_Transfer_premium/',views.Internal_Transfer_premium,name="Internal_Transfer_premium"),
    path('internal_transfer_wallet_list/',views.Internal_Transfer_Wallet_List,name="internal_transfer_wallet_list"),
    path('internal_transfer_history_list/',views.Internal_Transfer_History_List,name="internal_transfer_history_list"),    



    #Stake API  
    path('staking_deposit/',views.staking_deposit_api,name="staking_api"),

    # Stake deposit url
    path('stake_history_list/',views.Staking_Deposit_History_List,name="stake_deposit_history_list"), 

    path('stake_deposit_history/',views.stake_deposit_his,name="stake_deposit_history_list"), 


    #Stake API

    path('stake_api/',views.stake_api,name="stake_api"),


    path('stake_api_test/',views.stake_api_test,name="stake_api_test"),



    # Stake reward update

    path('staking_reward_function/',views.staking_reward_function_stake,name = 'staking_reward_function'),

    path('Current_stake/',views.Current_stake,name = 'Current_stake'),

    path('stake_referral_reward_history/',views.stake_referral_reward_history,name = 'stake_referral_reward_history'),

    

    # Staking_management_url
    path('stake_manage_api/',views.Staking_management_API,name="stake_manage_api"), 

    # Active stake api url
    path('active_stake_API/',views.Active_stake_API,name="active_stake_API"), 

    #Stake Claim

    path('claim_reward/',views.claim_reward,name="claim_reward"), 
    


    # Stake claim api url
    path('stake_claim/',views.Stake_Claim_API,name="stake_claim"),    
    path('stake_claim_history/',views.stake_claim_history,name="stake_claim_history"),     


    path('stake_withdraw_values/',views.stake_withdraw_values,name="stake_withdraw_values"),     


    
    # History url
    re_path('List_Stake/', login_required(List_Stake.as_view(),login_url=loginurl), name='List_Stake'),
    re_path('List_Stake_credit/', login_required(List_Stake_credit.as_view(),login_url=loginurl), name='List_Stake_credit'),

    re_path('List_Stake_Deposit_History/', login_required(List_Stake_Deposit_History.as_view(),login_url=loginurl), name='List_Stake_Deposit_History'),
    re_path('List_Stake_Claim_History/', login_required(List_Stake_Claim_History.as_view(),login_url=loginurl), name='List_Stake_Claim_History'),

    # stake individual user history table

    re_path(r'^user_stake_history_table/(?P<pk>[-\w]+)/$', login_required(StakeHistoryManagementTable.as_view(),login_url=loginurl), name='user_stake_history_table'),

    # Stake Withdraw Claim Reward URL

    path('stake_withdraw_wallet_rewards/',views.stake_withdraw_wallet_rewards,name="stake_withdraw_wallet_rewards"),    

    # Stake Monthly Claim history 
    path('stake_monthly_claim_history/',views.stake_monthly_claim,name="stake_monthly_claim_history"),    

    # stake monthly claim reward update 
    path('stke_monthly_claim_update/',views.stke_monthly_claim_update,name="stke_monthly_claim_update"),    
    path('Stake_deposit_edit/<int:id>/',views.Stake_deposit_edit,name="Stake_deposit_edit"),
    path('Stake_claim_edit/<int:id>/',views.Stake_claim_edit,name="Stake_claim_edit"),


    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------


                                    #stake_credit_wallet



    path('Edit_Staking_Monthly_Plan/1/', views.Edit_Staking_Monthly_Plan, name='Edit_Staking_Monthly_Plan'),
	path('Stake_MarketPrice_API/', views.Stake_MarketPrice_API,name = "Stake_MarketPrice_API"),
    path('stake_credit_api/',views.stake_credit_api,name="stake_credit_api"), 
    path('Current_credit_stake/',views.Current_credit_stake,name="Current_credit_stake"),
    path('Stake_deposit_edit/<int:id>/',views.Stake_deposit_edit,name="Stake_deposit_edit"),
    path('Stake_claim_edit/<int:id>/',views.Stake_claim_edit,name="Stake_claim_edit"),
    path('Active_stake_credit_API/',views.Active_stake_credit_API,name="Active_stake_credit_API"),
    path('Staking_management_credit_API/',views.Staking_management_credit_API,name="Staking_management_credit_API"),
    path('staking_credit_reward_function/',views.staking_credit_reward_function,name="staking_credit_reward_function"),
    path('staking_referral_two_update/<int:id>/',views.staking_referral_two_update,name="staking_referral_two_update"),






# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------


                                    #New stake__wallet
    path('new_staking_deposit/',views.new_staking_deposit_api,name="staking_api"),
    path('buy_Newstake/',views.buy_Newstake,name="buy_Newstake"),
    path('Stake_detail/',views.Stake_detail,name="Stake_detail"),
    path('stake_process_rewards/',views.stake_process_rewards,name="stake_process_rewards"),
    path('Stake_Referral_history/',views.Stake_Referral_history,name="Stake_Referral_history"),
    path('NewstakeBuyHistory/',views.NewstakeBuyHistory,name="NewstakeBuyHistory"),
    path('Stake_Transfer_History_List/',views.Stake_Transfer_History_List,name="Stake_Transfer_History_List"),
    path('Stake_expire/',views.Stake_expire,name="Stake_expire"),
    path('NewStakeInternalTransfer/',views.NewStakeInternalTransfer,name="NewStakeInternalTransfer"),
    path('uplinerefferals/',views.uplinerefferals,name="uplinerefferals"),
    path('Stake_Claim_APIorg/',views.Stake_Claim_APIorg,name="Stake_Claim_APIorg"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)











