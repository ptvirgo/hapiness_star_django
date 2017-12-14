from django import forms
from .widgets import StarSelect
from .models import Star

one_to_five = tuple([(i, i) for i in range(1, 6)])


class StarForm(forms.ModelForm):

    class Meta:
        model = Star
        fields = ['spirit', 'exercise', 'play', 'work', 'friends', 'adventure']

    spirit = forms.IntegerField(
        label="Energy / spirit",
        widget=StarSelect(choices=one_to_five, attrs={'class': 'star_radio'}))
    exercise = forms.IntegerField(widget=StarSelect(
        choices=one_to_five, attrs={'class': 'star_radio'}))
    play = forms.IntegerField(widget=StarSelect(
        choices=one_to_five, attrs={'class': 'star_radio'}))
    work = forms.IntegerField(widget=StarSelect(
        choices=one_to_five, attrs={'class': 'star_radio'}))
    friends = forms.IntegerField(widget=StarSelect(
        choices=one_to_five, attrs={'class': 'star_radio'}))
    adventure = forms.IntegerField(
        label="Romance / adventure",
        widget=StarSelect(choices=one_to_five, attrs={'class': 'star_radio'}))
