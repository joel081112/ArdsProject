from django import forms
from .models import Member, Match, Batting


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'


class MatchForm(forms.ModelForm):

    class Meta:
        model = Match
        fields = '__all__'


class BattingForm(forms.ModelForm):

    class Meta:
        model = Batting
        fields = '__all__'
