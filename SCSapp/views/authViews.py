from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class loginPageView(TemplateView):
    template_name = 'logInUser.html'

class JudgeObtainAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        response = super().post(request, args, *kwargs)
        token = [token for token in Token.objects.all() if response.data["token"] == token.key][0]
        if "judges" in [group.name for group in token.user.groups.all()]:
            return response
        return Response({"ERROR":"User isn't Judge"})

        

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
            redirect("homePage")

class signUpUserView(TemplateView):
    template_name = 'signUpUser.html'

@login_required
def logoutUser(request):
    request.user.auth_token.delete()
    return redirect('homePage')
