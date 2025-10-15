from django.contrib import admin
from trade_master.models import Cms_StaticContent,Faq,Contactus,EmailTemplate,SupportCategory
from auditable.views import AuditableAdminMixin

from trade_master.models import Roadmap,Currencylist,Blockip,LoginHistory,MenuModule,MenuPermission,Jw_plan_purchase_history,plan_purchase_history_edited

class Cms_StaticContentAdmin(AuditableAdminMixin):
    model = Cms_StaticContent
    list_display = ['id','name','title','content','status']
    
admin.site.register(Cms_StaticContent,Cms_StaticContentAdmin)
admin.site.register(Faq)
admin.site.register(Contactus)
admin.site.register(EmailTemplate)
admin.site.register(Roadmap)
admin.site.register(Currencylist)
admin.site.register(Blockip)
admin.site.register(LoginHistory)
admin.site.register(SupportCategory)
admin.site.register(MenuModule)
admin.site.register(MenuPermission)
admin.site.register(Jw_plan_purchase_history)
admin.site.register(plan_purchase_history_edited)

