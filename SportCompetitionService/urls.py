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
from django.urls import path
from SCSapp.views.competitonListsViews import homePageView
from SCSapp.views.authViews import signUpUserView, logoutUser, logInUserView
from SCSapp.views.competitionView import competitionView
from SCSapp.views.createOlympicsView import CreateOlympicsView
from SCSapp.views.competitonListsViews import pastCompetitionsView
from SCSapp.views.matchView import matchView
from SCSapp.views.createCompetitionView import createCompetitionView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', logInUserView, name='login'),
    path('signup/', signUpUserView, name='signup'),
    path('logout/', logoutUser, name="logout"),
    path('past/', pastCompetitionsView, name='pastCompetition'),
    path('', homePageView, name='homePage'),
    path('createCompetition/', createCompetitionView, name='createCompetition'),
    path('competition/<comp_id>/', competitionView, name='competition'),
    path('createOlympics/', CreateOlympicsView.as_view(), name='createOlympics'),
    path('match/<match_id>/', matchView, name='match')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)