from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone

from dateutil.parser import parse

from user_extensions import utils

from .models import Star
from .forms import StarForm


class StarView(LoginRequiredMixin, DetailView):
    '''View the star for a given date.'''

    contect_object_name = 'star'
    login_url = 'login'
    template_name = 'happiness_star/star.html'

    def get_object(self):
        user = self.request.user
        star_date = parse(self.args[0])
        star = get_object_or_404(Star, date=star_date, user=user)
        return star


class StarListView(LoginRequiredMixin, ListView):
    '''List the stars for a given user.'''

    context_object_name = 'star_list'
    login_url = 'login'
    template_name = 'happiness_star/star_list.html'

    def get_queryset(self):
        return Star.objects.filter(user=self.request.user)


class StarFormView(LoginRequiredMixin, View):
    '''Allow the user to create a star.'''

    form_class = StarForm
    template_name = 'happiness_star/star_form.html'
    star_date = timezone.localdate(timezone.now())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():

            try:
                star = Star.objects.get(user=request.user, date=self.star_date)
            except Star.DoesNotExist:
                star = Star(user=request.user, date=self.star_date)

            for f in form.cleaned_data:
                setattr(star, f, form.cleaned_data[f])

            star.save()
            status = 200

        else:
            status = 400

        return render(request, self.template_name,
                      {'form': form, 'date': self.star_date}, status=status)

    def get(self, request, *args, **kwargs):

        try:
            star = Star.objects.get(user=request.user, date=self.star_date)
        except Star.DoesNotExist:
            star = None

        if star is not None:
            initial = dict(star)
        else:
            initial = {}

        form = self.form_class(initial=initial)

        return render(request, self.template_name,
                      {'form': form, 'date': self.star_date})


class StarElmView(LoginRequiredMixin, View):
    '''Display the Elm + GQL interface'''

    template_name = 'happiness_star/elm-star.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        token = utils.user_jwt(user)
        return render(
            request, self.template_name, {'token': token}, status=200)
