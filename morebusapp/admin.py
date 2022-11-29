from django.apps import apps
from django.contrib import admin
from .models import *
from members.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

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

class MachineInfoAdmin(admin.ModelAdmin):
    list_display = ('lineID', 'machineID', 'line_name', 'machine_no', 'machine_name', 'ip_camera')
admin.site.register(MachineInfo, MachineInfoAdmin)



class UserProfileInLine(admin.StackedInline):
    model = UserProfile
    can_delete: False

class AccountsUserAdmin(AuthUserAdmin):
    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(AccountsUserAdmin, self).add_view(*args, **kwargs)
    def change_view(self, *args, **kwargs):
        self.inlines = [UserProfileInLine]
        return super(AccountsUserAdmin, self).change_view(*args, **kwargs)
   

admin.site.unregister(User)
admin.site.register(User, AccountsUserAdmin)