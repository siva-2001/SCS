from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework.authtoken.views import ObtainAuthToken

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from SCSapp.models.Faculty import Faculty

from rest_framework import generics
from rest_framework.views import APIView
from authorizationApp.func import getTokenFromASGIScope
from authorizationApp.models import User
from authorizationApp.serializers import UserSerializer
from django.contrib.auth.models import AnonymousUser

class loginPageView(TemplateView):
    template_name = 'logInUser.html'


class JudgeObtainAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        response = super().post(request, args, *kwargs)
        token = [token for token in Token.objects.all() if response.data["token"] == token.key][0]
        if "judges" in [group.name for group in token.user.groups.all()]:
            return response
        return Response({"ERROR": "User isn't Judge"})


def loginView(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            print("logined")
            return HttpResponse('{"hello":"answer"}')
        else:
            print("login failed")
            return HttpResponse('{"hello":"answer"}')
        redirect("homePage")


class signUpUserView(TemplateView):
    template_name = 'signUpUser.html'


@login_required
def logoutUser(request):
    token = getTokenFromASGIScope(request.scope)
    print(Token.objects.all().get(key=token).user)
    logout(request)
    Token.objects.all().get(key=token).delete()
    return redirect('homePage')

class PermissionsAPIView(APIView):
    def get(self, request):
        data = {}
        user = request.user
        data["isAnonymousUser"] = True if (type(user) == AnonymousUser) else False
        if not data["isAnonymousUser"]:
            data["id"] = user.id
            data["username"] = user.username
            data["FIO"] = (user.last_name + " " + user.first_name) if (user.last_name or user.first_name) else "Безымянный"
            if user.groups.filter(name="organizer").exists(): data["userrole"] = "Организатор"
            elif user.groups.filter(name="judge").exists(): data["userrole"] = "Судья"
            elif user in [faculty.representative for faculty in Faculty.objects.all()]: data["userrole"] = "Представитель факультета"
        return Response(data)


class SignUpAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
