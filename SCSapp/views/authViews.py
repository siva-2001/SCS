from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import TemplateView

from django.http import HttpResponse


class loginPageView(TemplateView):
    template_name = 'logInUser.html'

def loginView(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None: 
            login(request, user)
            print("logined")
            return HttpResponse('{"hello":"answer"}')
        else:
            print("login failed")


class signUpUserView(TemplateView):
    template_name = 'signUpUser.html'

@login_required
def logoutUser(request):
    request.user.auth_token.delete()
    logout(request)
    return redirect('homePage')
