from django.shortcuts import render
import datetime
from django.contrib import admin


class AuditableMixin(object,):
    def form_valid(self, form, ):
        try:
            if not form.instance.created_by_id :
                form.instance.created_by_id  = self.request.user.id
                form.instance.created_on   = datetime.datetime.now()
                
        except:
            form.instance.created_by_id  = self.request.user.id
            form.instance.created_on   = datetime.datetime.now()
            
        form.instance.modified_by = self.request.user
        return super(AuditableMixin, self).form_valid(form)

class AuditableAdminMixin(admin.ModelAdmin,object,):
    def save_model(self, request, obj, form, change):
        
        if not obj.created_by_id:
                obj.created_by_id = request.user.id

        obj.modified_by_id = request.user.id

        obj.save()
    def save_formset(self, request, form, formset, change):
        
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.created_by_id:
                instance.created_by_id = request.user.id
            instance.modified_by_id = request.user.id
            instance.save()
        formset.save_m2m()