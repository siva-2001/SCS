# from SCSapp.views.authViews import signUpUserView, logoutUser, loginView, loginPageView, JudgeObtainAuthToken
# from django.conf.urls.static import static
# from django.conf import settings

from django.urls import include, path, re_path
from authApp.views import SignUpAPIView, PermissionsAPIView, signUpUserView, logoutUser, loginView, loginPageView, JudgeObtainAuthToken
from rest_framework.authtoken import views as drf_views

urlpatterns = [
    #   auth url's
    path('loginPage/', loginPageView.as_view(), name='loginPage'),
    path('login/', loginView, name='login'),
    path('api-token-auth/', drf_views.obtain_auth_token, name="authToken"),
    
    #   register url's
    path('signupPage/', signUpUserView.as_view(), name='signupPage'),
    path('api/v1/auth/users', SignUpAPIView.as_view(), name='signup'),

    path('logout/', logoutUser, name="logout"),

    #   permission url
    path('permission/', PermissionsAPIView.as_view(), name="permission"),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)