from django.test import TestCase
from .models import Member, Match, Batting, \
    Bowling, Extras, BattingOpponents, BowlingOpponents, BlogPage, HomePage, Profile, TheClub, Type, Team, Venue, \
    MatchFormat, CoinToss, Club, Wicket, OppositionNames
from django.db.models import Max, Min, Count, Sum, Avg, Q


# https://github.com/features/actions
# Create your tests here. https://docs.djangoproject.com/en/3.1/topics/testing/overview/

# Run all the tests in the animals.tests module
# $ ./manage.py test animals.tests

# Run all the tests found within the 'animals' package
# $ ./manage.py test animals

# Run just one test case
# $ ./manage.py test animals.tests.AnimalTestCase

# Run just one test method
# $ ./manage.py test animals.tests.AnimalTestCase.test_animals_can_speak


class BowlingTestCase(TestCase):
    def setUp(self):
        seconds = seconds_create()
        dummy_data1(seconds)

    def test_bowler_extras_joel(self):
        joel = Bowling.objects.get(member__name='Joel Ferguson')
        self.assertEqual(joel.bowler_extras(), '1')

    def test_bowler_economy_joel(self):
        joel = Bowling.objects.get(member__name='Joel Ferguson')
        self.assertEqual(joel.economy(), '5.00')


class BattingTestCase(TestCase):
    def setUp(self):
        seconds = seconds_create()
        dummy_data1(seconds)

    def test_batter_runs(self):
        joel = Batting.objects.get(member__name='Joel Ferguson')
        self.assertEqual(joel.runs, 23)


class BattingOpponentsTestCase(TestCase):
    def setUp(self):
        seconds = seconds_create()
        dummy_data1(seconds)

    def test_opponent_runs(self):
        dano = BattingOpponents.objects.get(batter_name__name='Dani Williams')
        self.assertEqual(dano.runs, 15)


class BowlingOpponentsTestCase(TestCase):
    def setUp(self):
        seconds = seconds_create()
        dummy_data1(seconds)

    def test_bowler_extras(self):
        dano = BowlingOpponents.objects.get(bowler_name__name='Dani Williams')
        self.assertEqual(dano.bowler_extras(), '7')

    def test_bowler_economy(self):
        dano = BowlingOpponents.objects.get(bowler_name__name='Dani Williams')
        self.assertEqual(dano.economy(), '6.00')


class ExtrasTestCase(TestCase):
    def setUp(self):
        seconds = seconds_create()
        dummy_data1(seconds)

    def test_extras_home(self):
        ards = Extras.objects.get(ards=True)
        self.assertEqual(ards.extras_total(), 13)

    def test_extras_away(self):
        ards = Extras.objects.get(ards=False)
        self.assertEqual(ards.extras_total(), 14)


class MatchTestCase(TestCase):
    def setUp(self):
        seconds = seconds_create()
        firsts = firsts_create()
        dummy_data1(seconds)
        dummy_data2(seconds, firsts)

    def test_str(self):
        match = Match.objects.get(date='2020-05-06')
        self.assertEqual(match.__str__(), "secondXI on 06 May 2020 Ards lost by 90 against Dundrum")

    def test_result(self):
        match = Match.objects.get(date='2020-05-06')
        self.assertEqual(match.result(), "Ards lost by 90 runs")

    def test_dif_runs(self):
        match = Match.objects.get(date='2020-05-06')
        self.assertEqual(match.dif_runs(), '-90')

    def test_ards_score(self):
        match = Match.objects.get(date='2020-05-06')
        self.assertEqual(match.ards_score(), '110-5')

    def test_opponents_score(self):
        match = Match.objects.get(date='2020-05-06')
        self.assertEqual(match.opponents_score(), '200-2')

    def test_location(self):
        match = Match.objects.get(date='2020-05-06')
        self.assertEqual(match.location(), 'main Street')

    def test_team_v_team(self):
        match = Match.objects.get(date='2020-05-06')
        self.assertEqual(match.team_v_team(), 'Dundrum v Ards')

    def test_str_1(self):
        match = Match.objects.get(date="2018-04-06")
        self.assertEqual(match.__str__(), "firstXI on 06 April 2018 Ards won by 24 against Bangor")

    def test_result_1(self):
        match = Match.objects.get(date="2018-04-06")
        self.assertEqual(match.result(), "Ards won by 24 runs")

    def test_dif_runs_1(self):
        match = Match.objects.get(date="2018-04-06")
        self.assertEqual(match.dif_runs(), '24')

    def test_ards_score_1(self):
        match = Match.objects.get(date="2018-04-06")
        self.assertEqual(match.ards_score(), '90-8')

    def test_opponents_score_1(self):
        match = Match.objects.get(date="2018-04-06")
        self.assertEqual(match.opponents_score(), '66 All Out')

    def test_location_1(self):
        match = Match.objects.get(date="2018-04-06")
        self.assertEqual(match.location(), 'Londonderry Park, Newtownards')

    def test_team_v_team_1(self):
        match = Match.objects.get(date="2018-04-06")
        self.assertEqual(match.team_v_team(), 'Ards v Bangor')

    def test_str_2(self):
        match = Match.objects.get(date="2019-06-08")
        self.assertEqual(match.__str__(), "secondXI on 08 June 2019 Match drawn against Bangor")

    def test_result_2(self):
        match = Match.objects.get(date="2019-06-08")
        self.assertEqual(match.result(), "Match drawn")

    def test_dif_runs_2(self):
        match = Match.objects.get(date="2019-06-08")
        self.assertEqual(match.dif_runs(), '0')

    def test_ards_score_2(self):
        match = Match.objects.get(date="2019-06-08")
        self.assertEqual(match.ards_score(), '85 All Out')

    def test_opponents_score_2(self):
        match = Match.objects.get(date="2019-06-08")
        self.assertEqual(match.opponents_score(), '85-8')


def dummy_data1(team):
    dano = OppositionNames.objects.create(name='Dani Williams')
    bowled = Wicket.objects.create(name='Bowled')
    game35 = MatchFormat.objects.create(name='35 overs')
    away = Venue.objects.create(name='Away')
    won = CoinToss.objects.create(decision='Won toss and bowl first')
    dundrum = Club.objects.create(name='Dundrum', home_venue='main Street')
    match2 = Match.objects.create(
        team=team, match_format=game35, opponent=dundrum, date="2020-05-06", time="13:00:00", venue=away,
        decision=won, ards_overs_batted=15, ards_runs=110, ards_wickets=5,
        opponent_overs_batted=35, opponent_runs=200, opponent_wickets=2, report="Nothing to report",
    )
    joel = Member.objects.create(
        name='Joel Ferguson', dateOfBirth='1996-08-16', dateJoined='2007-05-05', mobile='07895436125'
    )
    Bowling.objects.create(
        member=joel, bowler_number=1,
        overs=3, runs=15, maidens=1, wickets=2, wides=1, no_balls=0, match=match2
    )
    Batting.objects.create(
        member=joel, batter_number=1, fours=3, sixes=1, runs=23,
        mode_of_dismissal=bowled, out_by=dano, match=match2
    )
    BattingOpponents.objects.create(
        batter_name=dano, batter_number=1, runs=15, mode_of_dismissal=bowled, out_by=joel, match=match2,
    )
    BowlingOpponents.objects.create(
        bowler_name=dano, bowler_number=1, overs=5, runs=30, wickets=1, wides=4, no_balls=3, match=match2,
    )
    Extras.objects.create(
        ards=True,    wides=4,    no_balls=3,    byes=5,    leg_byes=1,    match=match2,
    )
    Extras.objects.create(
        ards=False, wides=6, no_balls=0, byes=2, leg_byes=6, match=match2,
    )


def dummy_data2(team1, team2):
    jackie = OppositionNames.objects.create(name='Jackie Jill')
    runout = Wicket.objects.create(name='Run out')
    t20 = MatchFormat.objects.create(name='T20')
    home = Venue.objects.create(name='Home')
    lost = CoinToss.objects.create(decision='Lost toss and bat first')
    bangor = Club.objects.create(name='Bangor', home_venue='Upritchard Park')
    match1 = Match.objects.create(
        team=team2, match_format=t20, opponent=bangor, date="2018-04-06", time="14:30:00", venue=home,
        decision=lost, ards_overs_batted=20, ards_runs=90, ards_wickets=8,
        opponent_overs_batted=18, opponent_runs=66, opponent_wickets=10, report="A lot to report",
    )
    match2 = Match.objects.create(
        team=team1, match_format=t20, opponent=bangor, date="2019-06-08", time="12:30:00", venue=home,
        decision=lost, ards_overs_batted=14, ards_runs=85, ards_wickets=10,
        opponent_overs_batted=20, opponent_runs=85, opponent_wickets=8, report="A draw happened",
    )
    gareth = Member.objects.create(
        name='gareth Rogers', dateOfBirth='1986-01-16', dateJoined='1997-05-01', mobile='07896512300'
    )
    Bowling.objects.create(
        member=gareth, bowler_number=2,
        overs=5, runs=10, maidens=2, wickets=4, wides=6, no_balls=1, match=match1
    )
    Batting.objects.create(
        member=gareth, batter_number=1, fours=5, sixes=2, runs=45,
        mode_of_dismissal=runout, out_by=jackie, match=match1
    )
    BattingOpponents.objects.create(
        batter_name=jackie, batter_number=1, runs=24, mode_of_dismissal=runout, out_by=gareth, match=match1,
    )
    BowlingOpponents.objects.create(
        bowler_name=jackie, bowler_number=1, overs=2, runs=25, wickets=0, wides=4, no_balls=0, match=match1,
    )
    Extras.objects.create(
        ards=True,    wides=1,    no_balls=3,    byes=1,    leg_byes=3,    match=match1,
    )
    Extras.objects.create(
        ards=False, wides=12, no_balls=2, byes=5, leg_byes=6, match=match1,
    )


def seconds_create():
    return Team.objects.create(
        name='secondXI', abr='2nd XI'
    )


def firsts_create():
    return Team.objects.create(
        name='firstXI', abr='1st XI'
    )
