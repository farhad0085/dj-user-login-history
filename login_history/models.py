from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.db import models
from django.contrib.auth import get_user_model
from . import settings
import datetime


class LoginHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='login_histories')
    ip = models.CharField(max_length=39, blank=True, null=True) # save only ip, later we can get user's details from this ip address.
    user_agent = models.TextField(blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    is_login = models.BooleanField(default=True, null=True, blank=True) # login or logout
    is_logged_in = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} - {self.user} - {self.ip}"

    class Meta:
        ordering = ['-date_time']
        verbose_name = 'Login History'
        verbose_name_plural = 'Login Histories'

    
    def __eq__(self, other):
        return self.ip==other.ip and self.user_agent==other.user_agent

    def __hash__(self):
        return hash(('ip', self.ip, 'user_agent', self.user_agent))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def delete_old_login_histories(user):
   if settings.LOGIN_HISTORY_DELETE_OLD:
        today = datetime.date.today()

        if settings.LOGIN_HISTORY_KEEP_DAYS:
            days_x_ago = today - datetime.timedelta(days=settings.LOGIN_HISTORY_KEEP_DAYS)
            objs = LoginHistory.objects.filter(date_time__lte=days_x_ago, user=user).order_by('-date_time')
            objs.delete()
        elif settings.LOGIN_HISTORY_KEEP_LAST:
            objs = LoginHistory.objects.filter(user=user)\
                    .order_by('-date_time')[:settings.LOGIN_HISTORY_KEEP_LAST]\
                    .values_list("id", flat=True)
            objs = LoginHistory.objects.exclude(pk__in=list(objs))
            objs.delete()


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    ip = get_client_ip(request)
    LoginHistory.objects.create(
        user=user,
        ip=ip,
        user_agent=request.META['HTTP_USER_AGENT'],
        is_login=True
    )
    delete_old_login_histories(user)

@receiver(user_logged_out)
def post_logout(sender, user, request, **kwargs):
    if user:
        ip = get_client_ip(request)
        LoginHistory.objects.create(
            user=user,
            ip=ip,
            user_agent=request.META['HTTP_USER_AGENT'],
            is_logged_in=False,
            is_login=False
        )

        LoginHistory.objects.filter(
            user=user, ip=ip, user_agent=request.META['HTTP_USER_AGENT'])\
            .update(is_logged_in=False)
    delete_old_login_histories(user)
    


# adding custom methods to default User model
@property
def active_logins(self):
    """Check user's active logins"""
    
    active_logins = self.login_histories.filter(is_logged_in=True)
    
    active_logins = list(set(active_logins))
    return sorted(active_logins, key=lambda item: item.date_time)[::-1]


UserModel = get_user_model()
UserModel.add_to_class("active_logins", active_logins)
