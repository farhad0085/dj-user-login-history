# dj-user-login-history

A Django app which keep track of user login history.

## How to install
```
pip install dj_user_login_history
```

## Usage

1. Add `login_history` app to INSTALLED_APPS

```
INSTALLED_APPS = [
    ...
    'login_history',
    ...
]
```

2. Migrate database:
```
python manage.py migrate
```

3. Now all your user's login history will be tracked to a model called LoginHistory
4. You can check a user's active logins:
```
user.active_logins
```
5. You can add `login_history.urls` to your project url to see an example page explaining the user login histores.
6. For better understanding, read following code:

```
def login_histories(request):

    if not request.user.is_authenticated:
        return HttpResponse("<h1>Please login to see your login histories</h1>")\
        
    active_logins = request.user.active_logins

    active_logins_html = ""
    for login in active_logins:
        active_logins_html += f'<li>{login.ip} - {login.date_time} - {login.user_agent}</li>'

    return HttpResponse(
    f"""
        <h1>Active Logins</h1>
        <ul>
            {active_logins_html}
        </ul>
    """
    )
```
7. Use the `ip` to grab more information directly from the Frontend instead of backend, it'll optimize performance.
There're huge JS library which do the work, use any one of them.

> NB: When you write your own login view, make sure you log the user in using django login
```
from django.contrib.auth import login as django_login

django_login(request, user)
```