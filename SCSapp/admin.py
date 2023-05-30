from django.contrib import admin
from SCSapp.models.Match import AbstractMatch, VolleyballMatch
from SCSapp.models.MatchTeamResult import MatchTeamResult, VolleyballMatchTeamResult
from SCSapp.models.Competition import VolleyballCompetition, CacheScore
from SCSapp.models.VolleyballTeam import VolleyballTeam
from SCSapp.models.Faculty import Faculty
from SCSapp.models.Player import VolleyballPlayer
# from SCSapp.models.Olympics import Olympics

admin.site.register(VolleyballCompetition)
admin.site.register(VolleyballMatch)
admin.site.register(VolleyballTeam)
admin.site.register(VolleyballPlayer)
admin.site.register(VolleyballMatchTeamResult)
admin.site.register(Faculty)
admin.site.register(CacheScore)
# admin.site.register(Olympics)