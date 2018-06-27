from datetime import date
import factory
import factory.fuzzy

from user_extensions.factories import ProfileFactory

from . import models


class StarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Star

    date = date.today()

    spirit = factory.fuzzy.FuzzyInteger(1, 5)
    exercise = factory.fuzzy.FuzzyInteger(1, 5)
    work = factory.fuzzy.FuzzyInteger(1, 5)
    play = factory.fuzzy.FuzzyInteger(1, 5)
    friends = factory.fuzzy.FuzzyInteger(1, 5)
    adventure = factory.fuzzy.FuzzyInteger(1, 5)

    @factory.lazy_attribute
    def user(self):
        profile = ProfileFactory()
        return profile.user


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tag

    name = factory.fuzzy.FuzzyText()
