from django.contrib import admin
from .models import Member, Award, Wicket, Role, Opponent, Batting, Bowling, Team, Type, Cup
# Register your models here.

admin.site.register(Member)
admin.site.register(Award)
admin.site.register(Wicket)
admin.site.register(Role)
admin.site.register(Opponent)
admin.site.register(Batting)
admin.site.register(Bowling)
admin.site.register(Team)
admin.site.register(Type)
admin.site.register(Cup)
