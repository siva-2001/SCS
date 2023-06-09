
from SCSapp.views.createCompetitionView import CreateCompetitionView
from SCSapp.views.createTestDataView import CreateTestDataView
from SCSapp.views.eventListsViews import homePageView
from SCSapp.views.competitionView import competitionView
# from SCSapp.views.createOlympicsView import CreateOlympicsView
from SCSapp.views.eventListsViews import pastEventsView
from django.urls import path, re_path
from SCSapp.views.api_views import CurrentCompetitionAPIView, JudgeCompetitionsAPIView, CertainVolleyballCompetitionAPIView, CertainVolleyballMatch
from SCSapp.views.api_views import JudgeMatchesAPIView, MatchManagmentView, VolleyballCompetitionAPIView, VolleyballMatchesOfCompetitionAPIView
from SCSapp.views.api_views import VolleyballTeamAPIView, PlayerAPIView
from authorizationApp.views import JudgeObtainAuthToken


scs_urlpatterns = [
    path('createTestDataset/', CreateTestDataView, name='createTestDataView'),
    path('createCompetition/', CreateCompetitionView.as_view(), name='createCompetition'),
    path('', homePageView.as_view(), name='homePage'),
    path('competition/<pk>/', competitionView.as_view(), name='competition'),
    path('past/', pastEventsView, name='history'),

    # __________________________________________    API views    _______________________________________________________
    path('api/v1/competitions/', VolleyballCompetitionAPIView.as_view(), name='competitionsAPI'),
    path('api/v1/currentCompetitions/', CurrentCompetitionAPIView.as_view(), name='currentCompetitions'),


    # __________________________________________________________________________________________________________________

    path('api/v1/competition/<pk>/', CertainVolleyballCompetitionAPIView.as_view(), name = 'competitionAPI'),
    path('api/v1/matchesOfCompetition/<pk>/', VolleyballMatchesOfCompetitionAPIView.as_view(), name = 'matchesOfCompetitionAPI'),
    path('api/v1/match/<pk>/', CertainVolleyballMatch.as_view(), name = 'matchAPI'),
    path('api/v1/teamsOfCompetition/<pk>/', VolleyballTeamAPIView.as_view(), name="teamsOfCompetitionAPI"),
    path('api/v1/playersOfTeam/', PlayerAPIView.as_view(), name="playersOfTeamAPI"),

    # ______________________________________    mobile API views    ____________________________________________
    # path('mobile-api-token-auth/', JudgeObtainAuthToken.as_view(), name="judgeAuthToken"),
    path('api/v1/judgeCompetitions/', JudgeCompetitionsAPIView.as_view(), name='judgeCompetitions'),
    path('api/v1/judgeMatches/', JudgeMatchesAPIView.as_view(), name='judgeMatches'),
    path('api/v1/matchManagment/', MatchManagmentView.as_view(), name='matchManagment'),




    # path('api/v1/currentOlympics/', CurrentOlympicsAPIView.as_view(), name='currentOlympics'),
    # path('api/v1/olympicsList/', OlympicsAPIView.as_view(), name='APIOlympics'),
    # path('api/v1/announcedEvents', AnnouncedEventsAPIView.as_view(), name='announcedEvents'),
    # path('createOlympics/', CreateOlympicsView.as_view(), name='createOlympics'),
]