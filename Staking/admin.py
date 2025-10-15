from django.contrib import admin
from Staking.models import stake_wallet_management,staking_admin_management,internal_transfer_admin_management,internal_transfer_history,stake_deposit_management,Stake_history_management,Stake_referral_management,Stake_referral_reward_table,stake_claim_table


admin.site.register(stake_wallet_management)
admin.site.register(staking_admin_management)
admin.site.register(internal_transfer_admin_management)
admin.site.register(internal_transfer_history)
admin.site.register(stake_deposit_management)
admin.site.register(Stake_history_management)
admin.site.register(Stake_referral_management)
admin.site.register(Stake_referral_reward_table)
admin.site.register(stake_claim_table)




# Register your models here.
