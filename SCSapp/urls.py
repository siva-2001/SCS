from SCSapp.views.createTestDataView import CreateTestDataView
from django.urls import path, re_path
from SCSapp.views.api_views import CurrentCompetitionAPIView, JudgeCompetitionsAPIView, CertainVolleyballCompetitionAPIView, CertainVolleyballMatch
from SCSapp.views.api_views import JudgeMatchesAPIView, MatchManagmentView, VolleyballCompetitionAPIView, VolleyballMatchesOfCompetitionAPIView
from SCSapp.views.api_views import VolleyballTeamAPIView, PlayerAPIView, JudgeAPIView, CompetitionDraw
from authorizationApp.views import JudgeObtainAuthToken
from SCSapp.views.templates_views import pastEventsView, homePageView, TemplateView
from SCSapp.views.templates_views import CompetitionView, CreateCompetitionView, TeamRegistrView

scs_urlpatterns = [
    path('createTestDataset/', CreateTestDataView, name='createTestDataView'),
    path('createCompetition/', CreateCompetitionView.as_view(), name='createCompetition'),
    path('', homePageView, name='homePage'),
    path('competition/<pk>/', CompetitionView.as_view(), name='competition'),
    path('past/', pastEventsView, name='history'),
    path('newTeam/', TeamRegistrView.as_view(), name='newCommand'),

    # __________________________________________    API views    _______________________________________________________
    path('api/v1/competitions/', VolleyballCompetitionAPIView.as_view(), name='competitionsAPI'),
    path('api/v1/currentCompetitions/', CurrentCompetitionAPIView.as_view(), name='currentCompetitions'),
    path('api/v1/competition_draw/', CompetitionDraw.as_view(), name="draw"),

    # __________________________________________________________________________________________________________________

    path('api/v1/competition/<pk>/', CertainVolleyballCompetitionAPIView.as_view(), name = 'competitionAPI'),
    path('api/v1/matchesOfCompetition/<pk>/', VolleyballMatchesOfCompetitionAPIView.as_view(), name = 'matchesOfCompetitionAPI'),
    path('api/v1/match/<pk>/', CertainVolleyballMatch.as_view(), name = 'matchAPI'),
    path('api/v1/teamsOfCompetition/<pk>/', VolleyballTeamAPIView.as_view(), name="teamsOfCompetitionAPI"),
    path('api/v1/playersOfTeam/', PlayerAPIView.as_view(), name="playersOfTeamAPI"),
    path('api/v1/judges/', JudgeAPIView.as_view(), name="judges"),

    # ______________________________________    mobile API views    ____________________________________________
    # path('mobile-api-token-auth/', JudgeObtainAuthToken.as_view(), name="judgeAuthToken"),
    path('api/v1/judgeCompetitions/', JudgeCompetitionsAPIView.as_view(), name='judgeCompetitions'),
    path('api/v1/judgeMatches/', JudgeMatchesAPIView.as_view(), name='judgeMatches'),
    path('api/v1/matchManagment/', MatchManagmentView.as_view(), name='matchManagment'),
]