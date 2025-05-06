import os

from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.views import View

import auth_usage.settings

# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        remembered = request.POST.get('remembered')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            with open(os.path.join(BASE_DIR, r'templates\index.html'),
                      'r', encoding='utf-8')as f:
                template_string = f.read()
            t = Template(template_string)
            c = RequestContext(request)
            if remembered != 'on':
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(None)
            return redirect(reverse('auth_app:index'), t.render(c))
        else:
            return render(request, 'login.html', {'account_errmsg': '用户名或密码错误'})
@login_required()
def user_center(request):
    return render(request, 'userinfo.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('auth_app:login'))