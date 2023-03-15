"""SCSapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from SCSapp.views.eventListsViews import homePageView
from SCSapp.views.authViews import signUpUserView, logoutUser, loginView, loginPageView, JudgeObtainAuthToken
from SCSapp.views.competitionView import competitionView
from SCSapp.views.createOlympicsView import CreateOlympicsView
from SCSapp.views.eventListsViews import pastEventsView
from SCSapp.views.matchView import matchView
from SCSapp.views.createCompetitionView import CreateCompetitionView
from django.conf.urls.static import static

from django.urls import include, path, re_path
from django.conf import settings
from SCSapp.views.api_views import OlympicsAPIView, CurrentCompetitionAPIView, CurrentOlympicsAPIView, JudgeCompetitionsAPIView
from SCSapp.views.api_views import JudgeMatchesAPIView, SignUpAPIView, PermissionsAPIView, TestAPIView#, AnnouncedEventsAPIView
from SCSapp.views.createTestDataView import CreateTestDataView
from rest_framework.authtoken import views

urlpatterns = [
    #   admin url's
    path('admin/', admin.site.urls),

    #   auth url's
    path('loginPage/', loginPageView.as_view(), name='loginPage'),
    path('login/', loginView, name='login'),
    path('api-token-auth/', views.obtain_auth_token, name="authToken"),
    
    #   register url's
    path('signupPage/', signUpUserView.as_view(), name='signupPage'),
    path('api/v1/auth/users', SignUpAPIView.as_view(), name='signup'),

    path('logout/', logoutUser, name="logout"),

    #   permission url
    path('permission/', PermissionsAPIView.as_view(), name="permission"),

    # ---------------------------------------------------------------------------------------------
    #   mobile API
    #   нужно отдельное логирование для мобилки, только для судей
    # ---------------------------------------------------------------------------------------------

    # path('api-token-auth/', JudgeObtainAuthToken.as_view(), name="authToken"),
    path('api/v1/judgeCompetitions', JudgeCompetitionsAPIView.as_view(), name='judgeCompetitions'),
    path('api/v1/judgeMatches/', JudgeMatchesAPIView.as_view(), name='judgeMatches'),


    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------






    path('api/v1/currentCompetitions', CurrentCompetitionAPIView.as_view(), name='currentCompetitions'),
    path('api/v1/currentOlympics', CurrentOlympicsAPIView.as_view(), name='currentOlympics'),
    
    # path('api/v1/announcedEvents', AnnouncedEventsAPIView.as_view(), name='announcedEvents'),
    path('api/v1/test', TestAPIView.as_view(), name='test'),
    path('createTestDataset', CreateTestDataView, name='createTestDataView'),
    
    path('past/', pastEventsView, name='history'),
    path('', homePageView, name='homePage'),
    path('api/v1/olympicsList', OlympicsAPIView.as_view(), name='APIOlympics'),
    path('createCompetition/', CreateCompetitionView.as_view(), name='createCompetition'),
    path('competition/<comp_id>/', competitionView, name='competition'),
    path('createOlympics/', CreateOlympicsView.as_view(), name='createOlympics'),
    path('match/<match_id>/', matchView, name='match')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)