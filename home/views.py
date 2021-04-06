from django.db.models import Max, Min, Count, Sum, Avg, Q
from django.shortcuts import render, redirect
from django.core import serializers
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Member, Match, Batting, \
    Bowling, Extras, BattingOpponents, BowlingOpponents, BlogPage, HomePage
from .forms import MemberForm
from datetime import date
from django.http import JsonResponse
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
                    .values('ards_runs').filter(ards_runs__gte=1))
        dates = list(Match.objects.order_by('date')
                     .values('date').filter(ards_runs__gte=1))
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
    """View all members."""
    prev_match_list = Match.objects.filter(
        team__name__contains='firstXI',
        date__lte=date.today()
    ).order_by('-date')
    next_match_list = Match.objects.filter(
        team__name__contains='firstXI',
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
        'blog': blog,
        'homepage': homepage,
        'users': users,
        'member_list': member_list,
        'batting_list': batting_list
    }
    return render(request, template, context)


class UserHomeData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, user_id):
        users = list(User.objects.all().values('username'))
        dates = list(Batting.objects.all().values('match__date')
                     .filter(member__player_link__id=user_id).order_by('match__date'))
        runs_o = list(Batting.objects.all().values('runs')
                      .filter(member__player_link__id=user_id).order_by('match__date'))
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
    team_exact_query = request.GET.get('team_exact')
    team_or_year_query = request.GET.get('team_or_year')
    date_search_picker = request.GET.get('date_picker')
    year_query = request.GET.get('year_choice')
    date_list = queryset.order_by('date__year') \
        .values('date__year') \
        .distinct()
    print(date_list)
    print(queryset)

    if team_contains_queryo != '' and team_contains_queryo is not None:
        queryset = queryset.filter(opponent__name__icontains=team_contains_queryo)

    elif team_exact_query != '' and team_exact_query is not None:
        queryset = queryset.filter(id=team_exact_query)

    elif team_or_year_query != '' and team_or_year_query is not None:
        queryset = queryset.filter(Q(date__year__icontains=team_or_year_query)
                                   | Q(ards_runs__icontains=team_or_year_query)) \
            .distinct()

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
        'bowling_list_bn_f': bowling_list_bn_f
    }
    return render(request, 'club/match_selected.html', context)


def view_selected_fixture(request, match_id):
    """View a selected fixture."""
    obj = Match.objects.get(pk=match_id)

    context = {
        'object': obj
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
            return redirect('members')

    context = {'form': form}

    return render(request, 'club/member_update.html', context)
