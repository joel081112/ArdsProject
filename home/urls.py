from django.contrib import admin
from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.member_view, name='members'),
    path('view_member/<member_id>', views.view_selected_member, name='viewmember'),
    path('member/<member_id>', views.member_form, name='memberform'),
    path('role/<role>', views.view_selected_member_role, name='viewmemberrole'),
    path('team/<team>', views.view_selected_member_team, name='viewmemberteam'),
    path('create/member', views.create_member, name='create'),
    path('member/add', views.add_new_member, name='createadd'),

]
