from datetime import date

from django.test import TestCase
from django.core.exceptions import ValidationError

from factory.fuzzy import FuzzyInteger
from ..factories import StarFactory, UserFactory


class TestStar(TestCase):

    def test_sanity(self):
        '''This test has run.'''
        self.assertTrue(True)

    def test_star_range_validation(self):
        '''Star point attributes are restricted to 1 - 5'''

        for point in ['spirit', 'exercise', 'work', 'play',
                      'friends', 'adventure']:

            low = {point: FuzzyInteger(-10, 0)}
            high = {point: FuzzyInteger(6, 10)}

            star = StarFactory(**low)
            self.assertRaises(ValidationError, star.clean_fields)
            star = StarFactory(**high)
            self.assertRaises(ValidationError, star.clean_fields)

    def test_star_daily_limitation(self):
        '''One star per person per day.'''

        user = UserFactory()

        first = StarFactory(user=user, date=date(2017, 11, 20))
        first.validate_unique()

        same_user_same_day = StarFactory(user=user, date=date(2017, 11, 20))
        self.assertRaises(ValidationError, same_user_same_day.validate_unique)

        # different day should be fine
        new_day = StarFactory(user=user, date=date.today())
        new_day.validate_unique()

        # different user should be fine
        new_user = StarFactory(user=UserFactory(), date=date(2017, 11, 20))
        new_user.validate_unique()

    def test_overall(self):
        '''Star overall rating appears valid'''
        star = StarFactory(spirit=2, exercise=2, play=4, work=4, friends=3,
                           adventure=3)
        self.assertEqual(star.overall(), 3)
