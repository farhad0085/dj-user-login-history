from django.contrib import admin
from .models import LoginHistory


class ReadOnlyLoginHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_time', 'ip', 'user_agent', 'is_logged_in']
    list_filter = ['user__username']

    def has_add_permission(self, request):
        return False


admin.site.register(LoginHistory, ReadOnlyLoginHistoryAdmin)