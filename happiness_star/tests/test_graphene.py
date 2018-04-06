import json
import re

from django.urls import reverse
from django.test import Client, TestCase

from ..factories import UserFactory, StarFactory


class GrapheneTestCase(TestCase):
    """Provide some standard test configuration for Graphql Queries"""

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
        cls.owner = {"user": user, "header": header}

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
    """Stars can be read via graphene"""

    def test_nobody_gets_nothing(self):
        """Anonymous users have no stars, see no stars"""
        star = StarFactory(user=self.owner["user"])

        # allStars
        query = """{allStars {date spirit work}}"""
        result = self.execute(query, raise_errors=True)
        self.assertIs(result["data"]["allStars"], None)

        # star
        query = """{star(date: "%s"){date spirit work}}""" % \
                (star.date,)
        result = self.execute(query, raise_errors=True)
        self.assertEqual(result["data"]["star"], None)

    def test_owner_gets_stars(self):
        star = StarFactory(user=self.owner["user"])

        # allStars
        query = """{allStars {date spirit work}}"""
        result = self.execute(query, self.owner["header"], True)
        self.assertEqual(len(result["data"]["allStars"]), 1)

        # star
        fields = ["spirit", "exercise", "work", "play", "friends", "adventure"]

        query = """{star(date: "%s"){%s}}
                """ % (star.date, " ".join(fields))

        result = self.execute(query, self.owner["header"], True)

        for field in fields:
            self.assertEqual(
                getattr(star, field, None),
                result["data"]["star"][field],
                msg="mismatch on %s" % (field,))
