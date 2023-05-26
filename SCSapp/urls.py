
from SCSapp.views.createCompetitionView import CreateCompetitionView
from SCSapp.views.createTestDataView import CreateTestDataView
from SCSapp.views.eventListsViews import homePageView
from SCSapp.views.competitionView import competitionView
# from SCSapp.views.createOlympicsView import CreateOlympicsView
from SCSapp.views.eventListsViews import pastEventsView
from django.urls import path
from SCSapp.views.api_views import CurrentCompetitionAPIView, JudgeCompetitionsAPIView
from SCSapp.views.api_views import JudgeMatchesAPIView, MatchManagmentView, CompetitionAPIView, VolleyballCompetitionAPIView
from authorizationApp.views import JudgeObtainAuthToken


scs_urlpatterns = [
    path('createTestDataset/', CreateTestDataView, name='createTestDataView'),
    path('createCompetition/', CreateCompetitionView.as_view(), name='createCompetition'),
    path('', homePageView, name='homePage'),
    path('competition/<comp_id>/', competitionView, name='competition'),
    path('past/', pastEventsView, name='history'),

    # __________________________________________    API views    ____________________________________________
    path('api/v1/competitions/', VolleyballCompetitionAPIView.as_view(), name='competitionAPI'),
    path('api/v1/currentCompetitions/', CurrentCompetitionAPIView.as_view(), name='currentCompetitions'),

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