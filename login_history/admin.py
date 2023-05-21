from django.contrib import admin
from .models import LoginHistory


class ReadOnlyLoginHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'date_time', 'ip', 'user_agent', 'is_logged_in', 'get_action_status']
    list_filter = ['user']

    def get_action_status(self, obj):
        if obj.is_login:
            return "Login"
        return "Logout"

    def has_add_permission(self, request):
        return False

    get_action_status.short_description = "Status"


admin.site.register(LoginHistory, ReadOnlyLoginHistoryAdmin)