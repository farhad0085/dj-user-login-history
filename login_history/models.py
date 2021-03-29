from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.db import models
from django.contrib.auth import get_user_model


class LoginHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='login_histories')
    ip = models.CharField(max_length=15, blank=True, null=True) # save only ip, later we can get user's details from this ip address.
    user_agent = models.TextField(blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    is_logged_in = models.BooleanField(default=True)

    def __str__(self):
        return self.ip or self.username

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


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    ip = get_client_ip(request)
    LoginHistory.objects.create(
        user=user,
        ip=ip,
        user_agent=request.META['HTTP_USER_AGENT'],
    )

@receiver(user_logged_out)
def post_logout(sender, user, request, **kwargs):
    if user:
        ip = get_client_ip(request)
        LoginHistory.objects.create(
            user=user,
            ip=ip,
            user_agent=request.META['HTTP_USER_AGENT'],
            is_logged_in=False
        )

        LoginHistory.objects.filter(user=user, ip=ip, user_agent=request.META['HTTP_USER_AGENT']).update(is_logged_in=False)


# adding custom methods to default User model
@property
def active_logins(self):
    """Check user's active logins"""
    
    active_logins = self.login_histories.filter(is_logged_in=True)
    
    active_logins = list(set(active_logins))
    return sorted(active_logins, key=lambda item: item.date_time)[::-1]


UserModel = get_user_model()
UserModel.add_to_class("active_logins", active_logins)
