from rest_framework import serializers

from Staking.models import Stake_history_management , newstake_Referral_reward_History


class user_Active_Stake_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Stake_history_management
        fields= ['id','user','Amount_USDT','Amount_JW','status','period','maximum_reward','reward_percent','reward_per_month','reward_earned','reward_balance','referral_status','referral_level','claim_status','start_date','end_date','created_on','modified_on','modified_by'] 
        
        
        
class stake_Referral_History_Serializers(serializers.ModelSerializer):

    class Meta:
        model = newstake_Referral_reward_History
        fields = '__all__'