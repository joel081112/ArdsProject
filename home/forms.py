from django import forms
from wagtail.users.forms import User, UserProfile

from .models import Member, Match, Batting, Bowling, Profile, Extras, OppositionNames, BattingOpponents, \
    BowlingOpponents


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'


class MatchForm(forms.ModelForm):

    class Meta:
        model = Match
        fields = '__all__'


class ProfileForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=Profile.objects.all(),
        widget=forms.HiddenInput(),
        disabled=True
    )

    class Meta:
        model = Profile
        fields = '__all__'


class ProfileFormAdd(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ('user',)


class WagtailForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('avatar',)


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


class BattingOppForm(forms.ModelForm):
    match = forms.ModelChoiceField(
        queryset=Match.objects.all(),
        widget=forms.HiddenInput(),
        disabled=True
    )

    class Meta:
        model = BattingOpponents
        fields = '__all__'


class BattingOppFormAdd(forms.ModelForm):

    class Meta:
        model = BattingOpponents
        fields = '__all__'


class BowlingOppForm(forms.ModelForm):
    match = forms.ModelChoiceField(
        queryset=Match.objects.all(),
        widget=forms.HiddenInput(),
        disabled=True
    )

    class Meta:
        model = BowlingOpponents
        fields = '__all__'


class BowlingOppFormAdd(forms.ModelForm):

    class Meta:
        model = BowlingOpponents
        fields = '__all__'


class ExtrasForm(forms.ModelForm):
    match = forms.ModelChoiceField(
        queryset=Match.objects.all(),
        widget=forms.HiddenInput(),
        disabled=True
    )

    class Meta:
        model = Extras
        fields = '__all__'


class ExtrasFormAdd(forms.ModelForm):

    class Meta:
        model = Extras
        fields = '__all__'


class OppositionNamesForm(forms.ModelForm):

    class Meta:
        model = OppositionNames
        fields = '__all__'

