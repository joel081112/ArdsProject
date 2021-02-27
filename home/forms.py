from django import forms
from .models import Member, Match


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = '__all__'
