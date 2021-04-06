from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.member_view, name='members'),
    path('scorecard/firstXI/', views.match_view_firsts, name='matches'),
    path('scorecard/secondXI/', views.match_view_seconds, name='matches'),
    path('averages/firstXI/', views.averages_view_firsts, name='averages'),
    path('averages/secondXI/', views.averages_view_seconds, name='averages'),
    path('fixtures/firstXI/', views.fixture_view_firsts, name='fixtures'),
    path('fixtures/secondXI/', views.fixture_view_seconds, name='fixtures'),
    path('players/firstXI/', views.players_view_firsts, name='players'),
    path('players/secondXI/', views.players_view_seconds, name='players'),
    path('view_member/<member_id>', views.view_selected_member, name='viewmember'),
    path('member/<member_id>', views.member_form, name='memberform'),
    path('role/<role>', views.view_selected_member_role, name='viewmemberrole'),
    path('team/<team>', views.view_selected_member_team, name='viewmemberteam'),
    path('create/member', views.create_member, name='create'),
    path('member/add', views.add_new_member, name='createadd'),
    path('view_match/<match_id>', views.view_selected_match, name='viewmatch'),
    path('view_fixture/<match_id>', views.view_selected_fixture, name='viewfixture'),
    path('api/data/', views.get_data, name='api-data'),
    path('api/chart/data/', views.ChartData.as_view(), name='api-chart-data'),
    path('api/user/home/data/<user_id>', views.UserHomeData.as_view(), name='api-chart-data')

]
