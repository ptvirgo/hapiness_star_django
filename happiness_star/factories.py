from datetime import date
from django.contrib.auth import get_user_model
import factory
import factory.fuzzy

from . import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.fuzzy.FuzzyText()
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')


class StarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Star

    user = factory.SubFactory(UserFactory)
    date = date.today()

    spirit = factory.fuzzy.FuzzyInteger(1, 5)
    exercise = factory.fuzzy.FuzzyInteger(1, 5)
    work = factory.fuzzy.FuzzyInteger(1, 5)
    play = factory.fuzzy.FuzzyInteger(1, 5)
    friends = factory.fuzzy.FuzzyInteger(1, 5)
    adventure = factory.fuzzy.FuzzyInteger(1, 5)


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tag

    name = factory.fuzzy.FuzzyText()
