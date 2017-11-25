from django.forms import ModelForm
from .models import Star


class StarForm(ModelForm):

    class Meta:
        model = Star
        fields = ['spirit', 'exercise', 'play', 'work', 'friends', 'adventure']
