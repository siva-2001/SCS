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
from SCSapp.views.competitionView import competitionView
# from SCSapp.views.createOlympicsView import CreateOlympicsView
from SCSapp.views.eventListsViews import pastEventsView
from django.conf.urls.static import static

from django.urls import include, path, re_path
from django.conf import settings
from SCSapp.views.api_views import CurrentCompetitionAPIView, JudgeCompetitionsAPIView
from SCSapp.views.api_views import JudgeMatchesAPIView, MatchManagmentView

from rest_framework.authtoken import views as drf_views

from authorizationApp.views import JudgeObtainAuthToken
from authorizationApp.urls import auth_urlpatterns
from translationApp.urls import translation_urlpatterns
from SCSapp.urls import scs_urlpatterns

urlpatterns = [
    path('auth/', include(auth_urlpatterns)),
    path('liveStream/', include(translation_urlpatterns)),
    path('', include(scs_urlpatterns)),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)