from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Member, Award, Wicket, Role, Club, \
    Batting, Bowling, Team, Type, Cup, MatchFormat, Match, Venue, \
    CoinToss, Extras, OppositionNames, BattingOpponents, BowlingOpponents,\
    Profile


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
admin.site.register(Extras)
admin.site.register(OppositionNames)
admin.site.register(BattingOpponents)
admin.site.register(BowlingOpponents)
admin.site.register(Profile)
