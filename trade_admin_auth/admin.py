from django.contrib import admin

from trade_admin_auth.models import AdminUser_Profile,AdminUser_Activity,AccessAttempt,Steps_Management,Two_x_boost,User_Management,Steps_history,Registration_otp,PlanDateUpdateHistory,WithdrawSendHistory,front_page_management


admin.site.register(AdminUser_Profile)
admin.site.register(AdminUser_Activity)
admin.site.register(AccessAttempt)
admin.site.register(Steps_Management)
admin.site.register(Two_x_boost)
admin.site.register(User_Management)
admin.site.register(Steps_history)
admin.site.register(Registration_otp)
admin.site.register(PlanDateUpdateHistory)
admin.site.register(WithdrawSendHistory)
admin.site.register(front_page_management)

