from django.contrib import admin
from .models import CommonUser
from my_group.admin import (GroupMemberInLine,
                            GroupGroupAdministratorInLine)
# Register your models here.

# default:
# admin.site.register(CommonUser)


class CommonUserAdmin(admin.ModelAdmin):
    inlines = (GroupMemberInLine,
               GroupGroupAdministratorInLine)


admin.site.register(CommonUser, CommonUserAdmin)
