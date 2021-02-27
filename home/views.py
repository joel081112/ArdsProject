from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Member, Match
from .forms import MemberForm, MatchForm


def member_view(request):
    member_list = Member.objects.order_by('teamsPlayedFor')
    match_list = Match.objects.order_by('-date')

    context = {'member_list': member_list, 'match_list': match_list}
    return render(request, 'club/overview.html', context)


def view_selected_member(request, member_id):
    obj = Member.objects.get(pk=member_id)

    context = {
        'object': obj
    }
    return render(request, 'club/member_selected.html', context)


def view_selected_member_role(request, role):
    role_list = Member.objects.filter(role__name__contains=role)

    context = {
        'role_list': role_list
    }
    return render(request, 'club/member_role.html', context)


def view_selected_member_team(request, team):
    team_list = Member.objects.filter(teamsPlayedFor__name__contains=team)

    context = {
        'team_list': team_list
    }
    return render(request, 'club/member_team.html', context)


def create_member(request):
    form = MemberForm()

    context = {'form': form}
    return render(request, 'club/member_create.html', context)


@require_POST
def add_new_member(request):

    if request.method == 'POST':
        print("Printing POST")
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            print("Valid")
            form.save()

    return redirect('members')


def member_form(request, member_id):
    obj = Member.objects.get(pk=member_id)
    form = MemberForm(instance=obj)
    if request.method == 'POST':
        print("Printing POST")
        form = MemberForm(request.POST, request.FILES, instance=obj)
        print(obj)
        if form.is_valid():
            print("Valid")
            form.save()
            return redirect('members')

    context = {'form': form}

    return render(request, 'club/member_update.html', context)


