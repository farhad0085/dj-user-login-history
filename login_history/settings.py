from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured

LOGIN_HISTORY_DELETE_OLD = getattr(django_settings, 'LOGIN_HISTORY_DELETE_OLD', False)
LOGIN_HISTORY_KEEP_DAYS = getattr(django_settings, 'LOGIN_HISTORY_KEEP_DAYS', 0) # will track last 30 days login
LOGIN_HISTORY_KEEP_LAST = getattr(django_settings, 'LOGIN_HISTORY_KEEP_LAST', 0) # how many login record to keep

if type(LOGIN_HISTORY_DELETE_OLD) != bool:
    raise ImproperlyConfigured("LOGIN_HISTORY_DELETE_OLD must be boolean type (default: False)")
if type(LOGIN_HISTORY_KEEP_DAYS) != int:
    raise ImproperlyConfigured("LOGIN_HISTORY_KEEP_DAYS must be a integer (default: 0)")
if type(LOGIN_HISTORY_KEEP_LAST) != int:
    raise ImproperlyConfigured("LOGIN_HISTORY_KEEP_LAST must be a integer (default: 0)")

# prevent user from selecting both days and last entries number
_keep_days = getattr(django_settings, 'LOGIN_HISTORY_KEEP_DAYS', 0)
_keep_last = getattr(django_settings, 'LOGIN_HISTORY_KEEP_LAST', 0)
if _keep_days and _keep_last:
    raise ImproperlyConfigured("""
    Please set either LOGIN_HISTORY_KEEP_DAYS or LOGIN_HISTORY_KEEP_LAST,
    you don't need to setup both.
    """)
