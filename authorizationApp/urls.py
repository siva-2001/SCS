from authorizationApp.views import signUpUserView, logoutUser, loginView, loginPageView, JudgeObtainAuthToken, SignUpAPIView, PermissionsAPIView
from django.urls import include, path, re_path
from rest_framework.authtoken import views as drf_views

auth_urlpatterns = [
    path('loginPage/', loginPageView.as_view(), name='loginPage'),
    path('login/', loginView, name='login'),
    path('api-token-auth/', drf_views.obtain_auth_token, name="authToken"),
    path('mobile-api-token-auth/', JudgeObtainAuthToken.as_view(), name="judgeAuthToken"),
    path('signupPage/', signUpUserView.as_view(), name='signupPage'),
    path('api/v1/auth/users', SignUpAPIView.as_view(), name='signup'),
    path('logout/', logoutUser, name="logout"),
    path('permission/', PermissionsAPIView.as_view(), name="permission")
]