from django.contrib import admin
from .models import Group, GroupMember, GroupAdministrator
# Register your models here.


admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(GroupAdministrator)
