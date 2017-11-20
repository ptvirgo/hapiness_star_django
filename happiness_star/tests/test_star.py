from django.test import TestCase
from django.core.exceptions import ValidationError

from factory.fuzzy import FuzzyInteger
from ..factories import StarFactory, TagFactory

# Create your tests here.

class TestStar(TestCase):

    def test_sanity(self):
        '''This test has run.'''
        self.assertTrue(True)


    def test_star_range_validation(self):
        '''Star point attributes are restricted to 1 - 5'''

        for point in ['spirit', 'exercise', 'work', 'play',
                      'friends', 'adventure']:

            low = { point: FuzzyInteger(-10, 0) }
            high = { point: FuzzyInteger(6, 10) }

            star = StarFactory(**low)
            self.assertRaises(ValidationError, star.clean_fields)
            star = StarFactory(**high)
            self.assertRaises(ValidationError, star.clean_fields)

    def test_overall(self):
        '''Star overall rating appears valid'''
        star = StarFactory(spirit=2, exercise=2, play=4, work=4, friends=3,
                           adventure=3)
        self.assertEqual(star.overall(), 3)
