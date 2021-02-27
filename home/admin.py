from django.contrib import admin
from .models import Member, Award, Wicket, Role, Club, Batting, Bowling, Team, Type, Cup, MatchFormat, Match, Venue, \
    CoinToss
# Register your models here.

admin.site.register(Member)
admin.site.register(Award)
admin.site.register(Wicket)
admin.site.register(Role)
admin.site.register(Club)
admin.site.register(Batting)
admin.site.register(Bowling)

admin.site.register(Team)
admin.site.register(Type)
admin.site.register(Cup)
admin.site.register(CoinToss)
admin.site.register(MatchFormat)
admin.site.register(Match)
admin.site.register(Venue)
