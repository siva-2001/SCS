from django.contrib import admin
from SCSapp.models.Match import AbstractMatch
from SCSapp.models.MatchActions import MatchAction
from SCSapp.models.MatchTeamResult import AbstractMatchTeamResult, VolleyballMatchTeamResult
from SCSapp.models.Competition import Competition, CacheScore
from SCSapp.models.Olympics import Olympics
from SCSapp.models.Team import Team
from SCSapp.models.Participant import AbstractParticipant
from SCSapp.models.User import User

admin.site.register(User)
admin.site.register(Competition)
admin.site.register(Olympics)
admin.site.register(AbstractMatch)
admin.site.register(Team)
admin.site.register(AbstractMatchTeamResult)
admin.site.register(AbstractParticipant)
admin.site.register(CacheScore)
admin.site.register(MatchAction)
