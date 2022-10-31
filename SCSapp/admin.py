from django.contrib import admin
#from SCSapp.models import Player, VolleyballTeam, Competition, Match, MatchActions
from SCSapp.models.Match import AbstractMatch
from SCSapp.models.MatchTeamResult import AbstractMatchTeamResult, VolleyballMatchTeamResult
from SCSapp.models.Competition import Competition
from SCSapp.models.Olympics import Olympics
from SCSapp.models.Team import Team
from SCSapp.models.Participant import AbstractParticipant



admin.site.register(Competition)
admin.site.register(Olympics)
admin.site.register(AbstractMatch)
admin.site.register(Team)
admin.site.register(VolleyballMatchTeamResult)
admin.site.register(AbstractParticipant)

