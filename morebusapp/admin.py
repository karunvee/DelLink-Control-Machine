from django.apps import apps
from django.contrib import admin
from .models import *
# Register your models here.


# admin.site.register(Indicator)
# admin.site.register(LineInfo)

# class ListAdminMixin(object):
#     def __init__(self, model, admin_site):
#         self.list_display = [field.name for field in model._meta.fields]
#         super(ListAdminMixin, self).__init__(model, admin_site)


# models = apps.get_models()
# for model in models:
#     admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
#     try:
#         admin.site.register(model, admin_class)
#     except admin.sites.AlreadyRegistered:
#         pass
class LineInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'ip', 'port')
admin.site.register(LineInfo, LineInfoAdmin)

class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'lineID', 'machineID', 'tag_id', 'register', 'data_type', 'display', 'asg')
admin.site.register(Indicator, IndicatorAdmin)