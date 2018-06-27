from datetime import date

from django.test import Client, TestCase
from django.urls import reverse

from user_extensions.factories import UserFactory

from ..models import Star


class TestStarForm(TestCase):
    '''Stars can be saved via form.'''

    star_arguments = {'spirit': 1, 'exercise': 2, 'play': 3,
                      'work': 4, 'friends': 5, 'adventure': 1}

    def setUp(self):
        '''Prepare a logged in client'''
        self.user = UserFactory()
        self.user.set_password('secret')
        self.user.save()

        self.authorized_client = Client()
        self.logged_in = self.authorized_client.login(
            username=self.user.username, password='secret')

        if not self.logged_in:
            raise RuntimeError(
                'Failed to prepare logged in client for testing')

    def tearDown(self):
        self.authorized_client.logout()

    def test_login_required_to_save(self):
        '''Stars can't be saved without login'''

        client = Client()
        result = client.post(reverse('happiness_star:star_form'),
                             self.star_arguments)
        self.assertEqual(result.status_code, 302)

    def test_400_for_bad_data(self):

        result = self.authorized_client.post(
            reverse('happiness_star:star_form'),
            {'nothing': 2})

        self.assertEqual(result.status_code, 400)
        self.assertTrue('errorlist' in result.content.decode('utf-8'))

    def test_create_works_with_login(self):
        '''Stars can be created via form'''

        result = self.authorized_client.post(
            reverse('happiness_star:star_form'),
            self.star_arguments)

        self.assertEqual(result.status_code, 200)

        star = Star.objects.get(user=self.user, date=date.today())

        for point in self.star_arguments:
            self.assertEqual(getattr(star, point), self.star_arguments[point])
