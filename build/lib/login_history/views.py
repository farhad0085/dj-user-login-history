from django.http.response import HttpResponse

def home(request):

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