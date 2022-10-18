from django.contrib import admin
from SCSapp.models import Player, VolleyballTeam, Competition, Match, MatchActions

admin.site.register(Player.Player)
admin.site.register(VolleyballTeam.VolleyballTeam)
admin.site.register(Competition.Competition)
admin.site.register(Match.Match)
admin.site.register(MatchActions.MatchAction)
