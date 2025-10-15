from django.contrib import admin
from trade_auth.models import Market_place, UserAddress,UserWallet

admin.site.register(UserAddress)
admin.site.register(UserWallet)
admin.site.register(Market_place)
