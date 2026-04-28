from django.contrib import admin
from django.contrib.auth.models import Group
from .models import UserProfile, LoginHistory

admin.site.unregister(Group)
admin.site.site_header = "Omni Platform Admin"
admin.site.index_title = "Omni Platform Management"
admin.site.site_title = "Omni Admin"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')

@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'ip_address', 'user_agent')
    list_filter = ('login_time', 'user')
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('user', 'login_time', 'ip_address', 'user_agent')

