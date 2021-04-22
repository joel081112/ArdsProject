from django.db.models import Max, Min, Count, Sum, Avg, Q
from django.shortcuts import render, redirect
from django.core import serializers
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from wagtail.users.models import UserProfile

from .models import Member, Match, Batting, \
    Bowling, Extras, BattingOpponents, BowlingOpponents, BlogPage, HomePage, Profile, TheClub, OppositionNames
from .forms import MemberForm, MatchForm, BattingForm, BowlingForm, BattingFormAdd, BowlingFormAdd, \
    ProfileForm, ProfileFormAdd, WagtailForm, ExtrasForm, ExtrasFormAdd, OppositionNamesForm
from datetime import date
from django.http import JsonResponse, response
from rest_framework import routers, serializers, viewsets


def get_data(request, *args, **kwargs):
    runs = list(Match.objects.order_by('-date')
                .values('ards_runs').filter(ards_runs__gte=1))
    dates = list(Match.objects.order_by('-date')
                 .values('date').filter(ards_runs__gte=1))

    context = {
        'runs': runs,
        'dates': dates
    }
    return JsonResponse(context)


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        runs = list(Match.objects.order_by('date')
                    .values('ards_runs').filter(ards_runs__gte=1, date__lte=date.today()))
        dates = list(Match.objects.order_by('date')
                     .values('date').filter(ards_runs__gte=1, date__lte=date.today()))
        default_labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
        default_items = [10, 12, 13, 14, 9, 3]
        runs_array = []
        dates_array = []

        for items in runs.copy():
            runs_array.append(items['ards_runs'])

        for items in dates.copy():
            dates_array.append(items['date'])

        context = {
            'default_items': default_items,
            'default_labels': default_labels,
            'runs_array': runs_array,
            'dates_array': dates_array,
        }
        return Response(context)


def home_view(request):
    """View the homepage."""
    user_sponsor_list = User.objects.filter(groups__name='Sponsor')
    prev_match_list = Match.objects.filter(
        team__name__contains='firstXI',
        date__lte=date.today()
    ).order_by('-date')
    next_match_list = Match.objects.filter(
        team__name__contains='firstXI',
        date__gte=date.today()
    ).order_by('date')
    next_match_seconds = Match.objects.filter(
        team__name__contains='secondXI',
        date__gte=date.today()
    ).order_by('date')
    blog = BlogPage.objects.order_by('-date')
    homepage = HomePage.objects.all()
    users = User.objects.all()

    if request.user.is_authenticated:
        member_list = Member.objects.filter(
            player_link=request.user
        )
        batting_list = Batting.objects.filter(
            member__player_link=request.user
        ).order_by('-match__date')
    else:
        member_list = {}
        batting_list = {}

    template = 'home/home_page.html'

    context = {
        'prev_match_list': prev_match_list,
        'next_match_list': next_match_list,
        'next_match_seconds': next_match_seconds,
        'blog': blog,
        'homepage': homepage,
        'users': users,
        'member_list': member_list,
        'batting_list': batting_list,
        'user_sponsor_list': user_sponsor_list
    }
    return render(request, template, context)


class UserHomeData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, user_id):
        users = list(User.objects.all().values('username'))
        dates = list(Batting.objects.all().values('match__date')
                     .filter(member__player_link__id=user_id, match__date__lte=date.today())
                     .order_by('match__date'))
        runs_o = list(Batting.objects.all().values('runs')
                      .filter(member__player_link__id=user_id, match__date__lte=date.today())
                      .order_by('match__date'))
        runs = list(User.objects.all().values('username').filter(id=user_id))
        runs_array = []
        dates_array = []

        for items in runs_o.copy():
            runs_array.append(items['runs'])

        for items in dates.copy():
            dates_array.append(items['match__date'])

        context = {
            'users': users,
            'runs': runs,
            'dates': dates,
            'runs_o': runs_o,
            'runs_array': runs_array,
            'dates_array': dates_array
        }
        return Response(context)


def club_view(request):
    """View the club page."""
    club_page = TheClub.objects.all()
    captains = Member.objects.filter(
        role__name__in=['Captain']
    ).distinct()
    coaches = Member.objects.filter(
        role__name__in=['Coach']
    ).distinct()
    board_officers = Member.objects.filter(
        role__name__in=['Board officer']
    ).distinct()

    template = 'club/the_club.html'

    context = {
        'club_page': club_page,
        'captains': captains,
        'coaches': coaches,
        'board_officers': board_officers
    }
    return render(request, template, context)


def member_view(request):
    """View all members."""
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
    date_list = Member.objects.order_by('batting__match__date__year') \
        .values('batting__match__date__year') \
        .distinct()
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


def averages_view_firsts(request):
    """View all firsts averages."""
    queryset = Member.objects.filter(teamsPlayedFor__name='firstXI').order_by('id')
    queryset1 = Batting.objects.order_by('-match__date')
    queryset2 = Bowling.objects.order_by('-match__date')

    return render(request, 'club/averages.html',
                  averages_list_view(queryset, queryset1, queryset2, request))


def averages_view_seconds(request):
    """View all seconds averages."""
    queryset = Member.objects.filter(teamsPlayedFor__name='secondXI').order_by('id')
    queryset1 = Batting.objects.order_by('-match__date')
    queryset2 = Bowling.objects.order_by('-match__date')

    return render(request, 'club/averages.html',
                  averages_list_view(queryset, queryset1, queryset2, request))


def averages_list_view(queryset, queryset1, queryset2, request):
    """Context creation for a list of averages."""

    batting_list__ = queryset1
    bowling_list__ = queryset2
    batting_list = queryset.annotate(
        count_runs=Count('batting__runs'),
        max_runs=Max('batting__runs'),
        min_runs=Min('batting__runs'),
        sum_runs=Sum('batting__runs'),
        average_runs=Avg('batting__runs'),
        average_runs_pt2=Sum('batting__runs') / Count('batting__runs'),
    )
    bowling_list = queryset.annotate(
        count_runs=Count('bowling__runs'),
        max_runs=Max('bowling__runs'),
        min_runs=Min('bowling__runs'),
        sum_runs=Sum('bowling__runs'),
        average_runs=Avg('bowling__runs'),
        average_runs_pt2=Sum('bowling__runs') / Count('bowling__runs'),
    )
    player_list = queryset.values('name').distinct()
    player_choice = request.GET.get('player_choice')

    if player_choice != '' and player_choice is not None:
        queryset = queryset.filter(name__iexact=player_choice)

    context = {
        'batting_list': batting_list,
        'bowling_list': bowling_list,
        'player_list': player_list,
        'queryset': queryset,
        'batting_list__': batting_list__,
        'bowling_list__': bowling_list__
    }

    return context


def players_view_firsts(request):
    """View all firsts players."""
    queryset = Member.objects.filter(teamsPlayedFor__name='firstXI')
    return render(request, 'club/players.html', player_list_view(queryset, request))


def players_view_seconds(request):
    """View all seconds players."""
    queryset = Member.objects.filter(teamsPlayedFor__name='secondXI')
    return render(request, 'club/players.html', player_list_view(queryset, request))


def player_list_view(queryset, request):
    """Context creation for a list of members"""
    member_list = queryset.annotate(
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
    batting_list_bn = Batting.objects.order_by('batter_number')
    bowling_list_bn = Bowling.objects.order_by('bowler_number')
    batting_list = Batting.objects.order_by('-match__date')
    bowling_list = Bowling.objects.order_by('-match__date')
    extras_list = Extras.objects.order_by('match_id')

    context = {
        'member_list': member_list,
        'batting_list_bn': batting_list_bn,
        'bowling_list_bn': bowling_list_bn,
        'batting_list': batting_list,
        'bowling_list': bowling_list,
        'extras_list': extras_list
    }

    return context


def fixture_view_firsts(request):
    """View all firsts matches."""
    queryset = Match.objects.filter(
        team__name__contains='firstXI',
        date__gte=date.today()
    ).order_by('date')
    return render(request, 'club/fixture_preview.html', fixture_list_view(queryset, request))


def fixture_view_seconds(request):
    """View all seconds matches."""
    queryset = Match.objects.filter(
        team__name__contains='secondXI',
        date__gte=date.today()
    ).order_by('date')
    return render(request, 'club/fixture_preview.html', fixture_list_view(queryset, request))


def fixture_list_view(queryset, request):
    match_list = Match.objects.order_by('date')

    context = {
        'match_list': match_list,
        'queryset': queryset
    }
    return context


def match_view_firsts(request):
    """View all firsts matches."""
    queryset = Match.objects.filter(
        team__name__contains='firstXI',
        date__range=["2000-01-01", date.today()]
    ).order_by('-date')
    return render(request, 'club/scorecard.html', match_list_view(queryset, request))


def match_view_seconds(request):
    """View all seconds matches."""
    queryset = Match.objects.filter(
        team__name__contains='secondXI',
        date__range=["2000-01-01", date.today()]
    ).order_by('-date')
    return render(request, 'club/scorecard.html', match_list_view(queryset, request))


def match_list_view(queryset, request):
    match_list = Match.objects.order_by('-date')
    team_contains_queryo = request.GET.get('team_contains')
    date_search_picker = request.GET.get('date_picker')
    year_query = request.GET.get('year_choice')
    date_list = queryset.order_by('-date__year') \
        .values('date__year') \
        .distinct()

    if team_contains_queryo != '' and team_contains_queryo is not None:
        queryset = queryset.filter(opponent__name__icontains=team_contains_queryo)

    elif year_query != '' and year_query is not None:
        queryset = queryset.filter(date__year__iexact=year_query)

    elif date_search_picker != '' and date_search_picker is not None:
        queryset = queryset.filter(
            Q(date__range=[date_search_picker, date_search_picker])
        )

    elif team_contains_queryo == '' and date_search_picker == '' \
            and year_query == '':
        queryset = queryset

    context = {
        'match_list': match_list,
        'date_list': date_list,
        'queryset': queryset
    }
    return context


def view_selected_member(request, member_id):
    """View a selected member."""
    obj = Member.objects.get(pk=member_id)

    context = {
        'object': obj
    }
    return render(request, 'club/member_selected.html', context)


def view_selected_match(request, match_id):
    """View a selected match."""
    obj = Match.objects.get(pk=match_id)
    users = User.objects.all()
    extras_list_t = Extras.objects.order_by('match_id') \
        .filter(match_id=match_id, ards=True)
    extras_list_f = Extras.objects.order_by('match_id') \
        .filter(match_id=match_id, ards=False)
    batting_list_bn_t = Batting.objects.order_by('batter_number') \
        .filter(match_id=match_id)
    bowling_list_bn_t = Bowling.objects.order_by('bowler_number') \
        .filter(match_id=match_id)
    batting_list_bn_f = BattingOpponents.objects.order_by('batter_number') \
        .filter(match_id=match_id)
    bowling_list_bn_f = BowlingOpponents.objects.order_by('bowler_number') \
        .filter(match_id=match_id)

    context = {
        'object': obj,
        'extras_list_t': extras_list_t,
        'extras_list_f': extras_list_f,
        'batting_list_bn_t': batting_list_bn_t,
        'bowling_list_bn_t': bowling_list_bn_t,
        'batting_list_bn_f': batting_list_bn_f,
        'bowling_list_bn_f': bowling_list_bn_f,
        'users': users
    }
    return render(request, 'club/match_selected.html', context)


def view_selected_fixture(request, match_id):
    """View a selected fixture."""
    obj = Match.objects.get(pk=match_id)
    users = User.objects.all()

    context = {
        'object': obj,
        'users': users
    }
    return render(request, 'club/match_preview.html', context)


def view_selected_member_role(request, role):
    """View a selected role."""
    role_list = Member.objects.filter(role__name__contains=role)

    context = {
        'role_list': role_list
    }
    return render(request, 'club/member_role.html', context)


def view_selected_member_team(request, team):
    """View a selected team."""
    team_list = Member.objects.filter(teamsPlayedFor__name__contains=team)

    context = {
        'team_list': team_list
    }
    return render(request, 'club/member_team.html', context)


def create_member(request):
    """Create a new member form."""
    form = MemberForm()
    print(form)

    context = {'form': form}
    return render(request, 'club/member_create.html', context)


@require_POST
def add_new_member(request):
    """Add a new member post."""
    if request.method == 'POST':
        print("Printing POST")
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            print("Valid")
            form.save()
        else:
            print(form.errors)

    return redirect('members')


def member_form(request, member_id):
    """Edit existing member form view."""
    obj = Member.objects.get(pk=member_id)
    form = MemberForm(instance=obj)
    if request.method == 'POST':
        print("Printing POST")
        form = MemberForm(request.POST, request.FILES, instance=obj)
        print(obj)
        if form.is_valid():
            print("Valid")
            form.save()
            return redirect('/club/member/' + member_id)
        else:
            print(form.errors)

    context = {
        'form': form,
        'object': obj
    }

    return render(request, 'club/member_update.html', context)


def update_match_form(request, match_id):
    """Edit existing match form view."""

    obj = Match.objects.get(pk=match_id)
    form = MatchForm(instance=obj)
    if request.method == 'POST':
        print("Printing POST")
        form = MatchForm(request.POST, instance=obj)
        print(obj)
        if form.is_valid():
            print("Valid")
            form.save()
            if form.instance.date <= date.today():
                return redirect('/club/view_match/' + match_id)
            else:
                return redirect('/club/view_fixture/' + match_id)
        else:
            print(form.errors)
            return redirect('/club/match/' + match_id)

    context = {'form': form}

    return render(request, 'club/match_update.html', context)


def add_extras(request, match_id):
    """Add a batter."""
    obj = Match.objects.get(pk=match_id)
    form = ExtrasForm()
    extras_list_t = Extras.objects.filter(match_id=match_id, ards=True).order_by()
    extras_list_f = Extras.objects.filter(match_id=match_id, ards=False).order_by()

    context = {
        'obj': obj,
        'form': form,
        'extras_list_t': extras_list_t,
        'extras_list_f': extras_list_f
    }
    return render(request, 'club/add_extras.html', context)


@require_POST
def adding_extras(request, match_id):
    post_values = request.POST.copy()
    if request.method == 'POST':
        print("Printing POST")
        post_values['match'] = match_id
        form = ExtrasFormAdd(post_values)
        if form.is_valid():
            print("Valid")
            form.save()
        else:
            print(form.errors)

    return redirect('/club/match/' + match_id+'/extras')


def update_extras(request, match_id, extras_id):
    """Edit existing batter form view."""

    obj = Extras.objects.get(pk=extras_id)
    form = ExtrasForm(instance=obj)
    extras_list_t = Extras.objects.filter(match_id=match_id, ards=True).order_by()
    extras_list_f = Extras.objects.filter(match_id=match_id, ards=False).order_by()
    match = Match.objects.get(pk=match_id)
    if request.method == 'POST':
        print("Printing POST")
        form = ExtrasForm(request.POST, instance=obj)
        print(obj)
        if form.is_valid():
            print("Valid")
            form.save()
            return redirect('/club/match/' + match_id + '/extras/' + extras_id)
        else:
            print(form.errors)
            return redirect('/club/match/' + match_id + '/extras/' + extras_id)

    context = {
        'form': form,
        'extras_list_t': extras_list_t,
        'extras_list_f': extras_list_f,
        'match': match
    }

    return render(request, 'club/extras_update.html', context)


def delete_extras(request, match_id, extras_id):
    Extras.objects.get(id=extras_id).delete()
    return redirect('/club/match/' + match_id+'/extras')


def add_match(request):
    """Add a match."""
    match_form = MatchForm()

    context = {
        'match_form': match_form
    }
    return render(request, 'club/add_match.html', context)


@require_POST
def add_new_match(request):
    form_id = ''

    if request.method == 'POST':
        print("Printing POST")
        form = MatchForm(request.POST)
        if form.is_valid():
            print("Valid")
            form.save()
            print(form.instance.date)
            form_id = form.instance.id
            if form.instance.date <= date.today():
                return redirect('/club/view_match/' + str(form_id))
            else:
                return redirect('/club/view_fixture/' + str(form_id))
        else:
            print(form.errors)

    return redirect('/club/view_match/' + str(form_id))


def update_batter_form(request, match_id, batting_id):
    """Edit existing batter form view."""

    obj = Batting.objects.get(pk=batting_id)
    form = BattingForm(instance=obj)
    batting_list_bn = Batting.objects.order_by('batter_number') \
        .filter(match_id=match_id)
    match = Match.objects.get(pk=match_id)
    if request.method == 'POST':
        print("Printing POST")
        form = BattingForm(request.POST, instance=obj)
        print(obj)
        if form.is_valid():
            print("Valid")
            form.save()
            return redirect('/club/match/' + match_id + '/batter/' + batting_id)
        else:
            print(form.errors)
            return redirect('/club/match/' + match_id + '/batter/' + batting_id)

    context = {
        'form': form,
        'batting_list_bn': batting_list_bn,
        'match': match
    }

    return render(request, 'club/batter_update.html', context)


def add_batting(request, match_id, *args, **kwargs):
    """Add a batter."""

    obj = Match.objects.get(pk=match_id)
    form = BattingForm(instance=obj)
    batting_list_bn = Batting.objects.order_by('batter_number') \
        .filter(match_id=match_id)
    print()
    print(kwargs)

    context = {
        'form': form,
        'obj': obj,
        'batting_list_bn': batting_list_bn
    }
    print(context)
    return render(request, 'club/add_batter.html', context)


@require_POST
def add_new_batter(request, match_id):
    post_values = request.POST.copy()
    if request.method == 'POST':
        print("Printing POST")
        post_values['match'] = match_id
        form = BattingFormAdd(post_values)
        if form.is_valid():
            print("Valid")
            form.save()
            return redirect('/club/match/batter/add/' + match_id)
        else:
            print(form.errors.as_data())
            return redirect('/club/match/batter/add/' + match_id)


def delete_batter(request, match_id, batter_id):
    Batting.objects.get(id=batter_id).delete()
    return redirect('/club/match/batter/add/' + match_id)


def update_bowler_form(request, match_id, bowling_id):
    """Edit existing bowler form view."""

    obj = Bowling.objects.get(pk=bowling_id)
    form = BowlingForm(instance=obj)
    bowling_list_bn = Bowling.objects.order_by('bowler_number') \
        .filter(match_id=match_id)
    match = Match.objects.get(pk=match_id)
    if request.method == 'POST':
        print("Printing POST")
        form = BowlingForm(request.POST, instance=obj)
        print(obj)
        if form.is_valid():
            print("Valid")
            form.save()
            return redirect('/club/match/' + match_id + '/bowler/' + bowling_id)
        else:
            print(form.errors)
            return redirect('/club/match/' + match_id + '/bowler/' + bowling_id)

    context = {
        'form': form,
        'bowling_list_bn': bowling_list_bn,
        'match': match
    }

    return render(request, 'club/bowler_update.html', context)


def add_bowling(request, match_id):
    """Add a batter."""
    obj = Match.objects.get(pk=match_id)
    form = BowlingForm(instance=obj)
    bowling_list_bn = Bowling.objects.order_by('bowler_number') \
        .filter(match_id=match_id)

    context = {
        'form': form,
        'obj': obj,
        'bowling_list_bn': bowling_list_bn
    }
    return render(request, 'club/add_bowler.html', context)


@require_POST
def add_new_bowler(request, match_id):
    post_values = request.POST.copy()
    if request.method == 'POST':
        print("Printing POST")
        post_values['match'] = match_id
        form = BowlingFormAdd(post_values)
        if form.is_valid():
            print("Valid")
            form.save()
        else:
            print(form.errors)

    return redirect('/club/match/bowler/add/' + match_id)


def delete_bowler(request, match_id, bowler_id):
    Bowling.objects.get(id=bowler_id).delete()
    return redirect('/club/match/bowler/add/' + match_id)


def add_opposition(request):
    """Add a new opponent name."""
    form = OppositionNamesForm()
    opposition_names = OppositionNames.objects.all()

    context = {
        'form': form,
        'opposition_names': opposition_names
    }
    return render(request, 'club/add_opp_names.html', context)


@require_POST
def add_new_name(request):
    form_id = ''
    if request.method == 'POST':
        print("Printing POST")
        form = OppositionNamesForm(request.POST)
        if form.is_valid():
            print("Valid")
            form.save()
            return redirect('/club/opposition-name/add')
        else:
            print(form.errors)
            return redirect('/club/opposition-name/add')


def delete_opponent(request, opponent_id):
    OppositionNames.objects.get(id=opponent_id).delete()
    return redirect('/club/opposition-name/add')


def update_opponent(request, opponent_id):
    """Edit existing batter form view."""

    obj = OppositionNames.objects.get(pk=opponent_id)
    form = OppositionNamesForm(instance=obj)
    opposition_names = OppositionNames.objects.all()
    if request.method == 'POST':
        print("Printing POST")
        form = OppositionNamesForm(request.POST, instance=obj)
        print(obj)
        if form.is_valid():
            print("Valid")
            form.save()
            return redirect('/club/opposition-name/'+opponent_id+'/update')
        else:
            print(form.errors)
            return redirect('/club/opposition-name/'+opponent_id+'/update')

    context = {
        'form': form,
        'opposition_names': opposition_names
    }

    return render(request, 'club/opp_names_update.html', context)


def delete_account(request):
    """Delete an account."""

    context = {
    }
    return render(request, 'account/delete_account.html', context)


def delete_account_confirmed(request):
    """Delete an account."""

    context = {
    }
    return render(request, 'account/user_deleted.html', context)


def delete_confirm(request):
    request.user.delete()
    logout(request)
    return redirect('/user-deleted')


def view_sponsors(request):
    """View sponsors page."""
    users = User.objects.all()
    user_sponsor_list = User.objects.filter(groups__name='Sponsor')

    context = {
        'users': users,
        'user_sponsor_list': user_sponsor_list
    }
    return render(request, 'club/sponsors_home.html', context)


def view_sponsors_home(request, user_id):
    """View sponsors page."""
    users = User.objects.all()
    user_sponsor_list = User.objects.filter(groups__name='Sponsor')
    obj = Profile.objects.get(user_id=user_id)
    form = ProfileForm(instance=obj)
    if request.method == 'POST':
        print("Printing POST")
        print(request.POST)
        print(obj)
        form = ProfileFormAdd(request.POST, instance=obj)
        if form.is_valid():
            print("Valid")
            form.save()
            return redirect('/club/sponsors/' + user_id)
        else:
            print(form.errors)
            return redirect('/club/sponsors/' + user_id)

    context = {
        'users': users,
        'form': form,
        'user_sponsor_list': user_sponsor_list
    }
    return render(request, 'club/sponsors_home.html', context)


def view_sponsors_home_picture(request, user_id):
    """View sponsors page."""
    users = User.objects.all()
    user_sponsor_list = User.objects.filter(groups__name='Sponsor')
    obj = UserProfile.objects.get(user_id=user_id)
    form = WagtailForm(instance=obj)
    if request.method == 'POST':
        print("Printing POST")
        print(request.POST)
        print(obj)
        form = WagtailForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            print("Valid")
            form.save()
            return redirect('/club/sponsors/' + user_id + '/picture')
        else:
            print(form.errors)
            return redirect('/club/sponsors/' + user_id + '/picture')

    context = {
        'users': users,
        'form': form,
        'user_sponsor_list': user_sponsor_list
    }
    return render(request, 'club/sponsors_home.html', context)

