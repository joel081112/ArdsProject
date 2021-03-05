from django.db.models import Max, Min, Count, Sum, Avg, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Member, Match, Batting, Bowling, Team, Extras, BattingOpponents, BowlingOpponents
from .forms import MemberForm, MatchForm


def member_view(request):
    member_list = Member.objects.order_by('teamsPlayedFor').annotate(
        max_runs=Max('batting__runs'),
        min_runs=Min('batting__runs'),
        count_runs=Count('batting__runs'),
        count_runs_past_2019=Count(
            'batting__runs',
            filter=Q(batting__match__date__year__range=[2019, 2020])
        ),
        sum_runs=Sum('batting__runs'),
        average_runs=Avg('batting__runs'),
        average_runs_pt2=Sum('batting__runs') / Count('batting__runs')
    )
    match_list = Match.objects.order_by('-date')
    batting_list_bn = Batting.objects.order_by('batter_number')
    bowling_list_bn = Bowling.objects.order_by('bowler_number')
    batting_list = Batting.objects.order_by('-match__date')
    bowling_list = Bowling.objects.order_by('-match__date')
    date_list = Member.objects.order_by('batting__match__date__year').values('batting__match__date__year').distinct()
    extras_list = Extras.objects.order_by('match_id')

    context = {'member_list': member_list,
               'match_list': match_list,
               'batting_list_bn': batting_list_bn,
               'bowling_list_bn': bowling_list_bn,
               'batting_list': batting_list,
               'bowling_list': bowling_list,
               'date_list': date_list,
               'extras_list': extras_list
               }
    return render(request, 'club/overview.html', context)


def view_selected_member(request, member_id):
    obj = Member.objects.get(pk=member_id)

    context = {
        'object': obj
    }
    return render(request, 'club/member_selected.html', context)


def view_selected_match(request, match_id):
    obj = Match.objects.get(pk=match_id)
    extras_list_t = Extras.objects.order_by('match_id').filter(match_id=match_id, ards=True)
    extras_list_f = Extras.objects.order_by('match_id').filter(match_id=match_id, ards=False)
    batting_list_bn_t = Batting.objects.order_by('batter_number').filter(match_id=match_id)
    bowling_list_bn_t = Bowling.objects.order_by('bowler_number').filter(match_id=match_id)
    batting_list_bn_f = BattingOpponents.objects.order_by('batter_number').filter(match_id=match_id)
    bowling_list_bn_f = BowlingOpponents.objects.order_by('bowler_number').filter(match_id=match_id)

    context = {
        'object': obj,
        'extras_list_t': extras_list_t,
        'extras_list_f': extras_list_f,
        'batting_list_bn_t': batting_list_bn_t,
        'bowling_list_bn_t': bowling_list_bn_t,
        'batting_list_bn_f': batting_list_bn_f,
        'bowling_list_bn_f': bowling_list_bn_f
    }
    return render(request, 'club/match_selected.html', context)


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
