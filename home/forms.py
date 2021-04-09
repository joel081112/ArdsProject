from django import forms
from .models import Member, Match, Batting, Bowling


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'


class MatchForm(forms.ModelForm):

    class Meta:
        model = Match
        fields = '__all__'


class BattingForm(forms.ModelForm):
    match = forms.ModelChoiceField(
        queryset=Match.objects.all(),
        widget=forms.HiddenInput(),
        disabled=True
    )

    class Meta:
        model = Batting
        fields = '__all__'


class BattingFormAdd(forms.ModelForm):

    class Meta:
        model = Batting
        fields = '__all__'


class BowlingForm(forms.ModelForm):
    match = forms.ModelChoiceField(
        queryset=Match.objects.all(),
        widget=forms.HiddenInput(),
        disabled=True
    )

    class Meta:
        model = Bowling
        fields = '__all__'


class BowlingFormAdd(forms.ModelForm):

    class Meta:
        model = Bowling
        fields = '__all__'
