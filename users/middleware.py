from django.shortcuts import redirect, render
from django.urls import reverse

class SessionExpiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_urls = [reverse('dealer-login'), reverse('employee-login'), reverse('owner-login')]
        if not request.user.is_authenticated and 'session_expired' in request.session and request.path not in login_urls + [reverse('home')]:
            return render(request, 'users/base/session_expired.html')

        response = self.get_response(request)
        request.session['session_expired'] = True
        return response
    
