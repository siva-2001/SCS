from django.contrib import admin
#from SCSapp.models import Player, VolleyballTeam, Competition, Match, MatchActions
from SCSapp.models.Competition import Competition
from SCSapp.models.Olympics import Olympics

# admin.site.register(Player.Player)
# admin.site.register(VolleyballTeam.VolleyballTeam)
# admin.site.register(Match.Match)
# admin.site.register(MatchActions.MatchAction)
#

admin.site.register(Competition)
admin.site.register(Olympics)