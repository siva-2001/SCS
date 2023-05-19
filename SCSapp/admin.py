from django.contrib import admin
from SCSapp.models.Match import AbstractMatch, VolleyballMatch
from SCSapp.models.MatchTeamResult import MatchTeamResult, VolleyballMatchTeamResult
from SCSapp.models.Competition import Competition, CacheScore
from SCSapp.models.Team import Team
from SCSapp.models.Participant import Faculty
# from SCSapp.models.Olympics import Olympics

admin.site.register(Competition)
admin.site.register(AbstractMatch)
admin.site.register(VolleyballMatch)
admin.site.register(Team)
admin.site.register(VolleyballMatchTeamResult)
admin.site.register(Faculty)
admin.site.register(CacheScore)
# admin.site.register(Olympics)