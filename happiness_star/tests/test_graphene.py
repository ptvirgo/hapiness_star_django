from datetime import datetime
import json
import re

from django.urls import reverse
from django.test import Client, TestCase

from user_extensions.factories import UserFactory

from ..models import Star, Tag
from ..factories import StarFactory


class GrapheneTestCase(TestCase):
    """Provide some standard test configuration for Graphql Queries"""

    star_fields = [
        "spirit", "exercise", "play", "work", "friends", "adventure"]
    bad_jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1Mjc4ODkyMzcuMDk4NDUsIm5iZiI6MTUyNzg4ODYzNy4wOTg0NSwic3ViIjoiNCJ9.DDhCfcBtD0l89oAo3otUaiOZa0IktSvRoN_m5Rp8iWw"

    @classmethod
    def setUpClass(cls, *args, **kwargs):
        """Prepare a JWT for a valid test user"""

        super().setUpClass(*args, **kwargs)

        user = UserFactory()
        user.set_password("logmein")
        user.save()

        client = Client()
        logged_in = client.login(username=user.username, password="logmein")

        if not logged_in:
            raise RuntimeError("unable to log in test user")

        response = client.get(reverse("home"))
        match = re.search('name="jwt" content="([^"]+)"',
                          response.content.decode("utf-8"))

        if match is None:
            print(response.content.decode("utf-8"))
            raise RuntimeError("jwt unavailable for test user")

        jwt = match.groups()[0]
        header = {"Authorization": "Bearer %s" % (jwt,)}
        cls.owner = {"user": user, "header": header, "jwt": jwt}

    @staticmethod
    def execute(query, headers=None, raise_errors=False):
        """Post a GQL query.
        Parameters
            headers -- a dict of HTTP headers to include with query
                       (As expected for JWT, for example)
            raise_errors -- if True, response errors will be raised as
                            AssertionError
        """
        # At last check, the standard Graphene test client does not appear to
        # simulate HTTP headers.  Need this for permission checking.

        client = Client()

        if headers is None:
            response = client.post("/graphql/", {"query": query})
        else:
            response = client.post("/graphql/", {"query": query}, **headers)

        text = response.content.decode("utf-8")

        try:
            result = json.loads(text)
        except Exception as err:
            print(text)
            raise err

        if raise_errors and "errors" in result:
            message = "Query Errors:\n    " + "\n   ".join(
                [error.get("message", "missing error message")
                 for error in result["errors"]])

            raise AssertionError(message)

        return result


class TestReadStars(GrapheneTestCase):
    """Stars can be read via graphql"""

    def test_nobody_gets_nothing(self):
        """Invalid users have no stars, see no stars"""
        star = StarFactory(user=self.owner["user"])

        # allStars
        query = """{allStars(token: "%s") {date spirit work}}""" % \
            (self.bad_jwt,)
        result = self.execute(query)
        self.assertIs(result["data"]["allStars"], None)

        # star
        query = """{star(date: "%s", token: "%s")
                   {date spirit work}}""" % (star.date, self.bad_jwt)
        result = self.execute(query)
        self.assertEqual(result["data"]["star"], None)

    def test_owner_gets_stars(self):
        """Owners can see their stars"""
        star = StarFactory(user=self.owner["user"])

        # allStars
        query = """{allStars(token: "%s"){date spirit work}}""" % \
            (self.owner["jwt"])
        result = self.execute(query, raise_errors=True)
        self.assertEqual(len(result["data"]["allStars"]), 1)

        # star
        query = """{star(date: "%s", token: "%s"){%s}}
                """ % (star.date, self.owner["jwt"],
                       " ".join(self.star_fields))

        result = self.execute(query, raise_errors=True)

        for field in self.star_fields:
            self.assertEqual(
                getattr(star, field, None),
                result["data"]["star"][field],
                msg="mismatch on %s" % (field,))


class TestCreateStar(GrapheneTestCase):
    """Stars can be created via graphql"""

    def test_create_requires_jwt(self):
        query = """mutation{
                    saveStar(
                        spirit: 1,
                        exercise: 2,
                        play: 3,
                        work: 4,
                        friends: 5,
                        adventure: 6,
                        token: "%s"
                    )
                    {date spirit exercise play work friends adventure}}
                """ % (self.bad_jwt,)

        result = self.execute(query)

        self.assertTrue("errors" in result)
        self.assertEqual(result["errors"][0]["message"], "not authorized")

    def test_create_produces_star(self):
        query = """mutation{
                    saveStar(
                        spirit: 1,
                        exercise: 2,
                        play: 3,
                        work: 4,
                        friends: 5,
                        adventure: 6,
                        token: "%s"
                    )
                    {date spirit exercise play work friends adventure}}
                """ % (self.owner["jwt"])

        result = self.execute(query, raise_errors=True)

        lookup = Star.objects.get(
            user=self.owner["user"], date=datetime.today())

        self.assertEqual(lookup.spirit, 1)
        self.assertEqual(lookup.exercise, 2)
        self.assertEqual(lookup.play, 3)
        self.assertEqual(lookup.work, 4)
        self.assertEqual(lookup.friends, 5)
        self.assertEqual(lookup.adventure, 6)

    def test_create_leaves_uspecified_values_alone(self):
        """
        Calling saveStar with some unspecified values should leave those values
        unchanged.
        """
        star = StarFactory(user=self.owner["user"])
        expect = dict(star)
        expect["friends"] = (star.friends + 1) if star.friends < 5 else 1

        query = """mutation{ saveStar( friends: %d, token: "%s" ) {
            date spirit exercise play work friends adventure }}
            """ % (expect["friends"], self.owner["jwt"])

        result = self.execute(query, raise_errors=True)
        star.refresh_from_db()

        for field in self.star_fields:
            self.assertEqual(getattr(star, field),
                             expect[field], msg=f"mismatch on {field}")
