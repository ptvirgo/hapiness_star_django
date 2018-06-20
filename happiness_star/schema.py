from jose import jwt
from datetime import datetime
from dateutil.parser import parse
from warnings import warn

from django.conf import settings
from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType

from .models import Star, Tag


User = get_user_model()


def context_to_user(context):
    """Given the context (expecting a JWT), return the appropriate user"""

    authorization = context.META.get("Authorization", None)

    if authorization is None:

        if settings.DEBUG and context.user.is_authenticated:
            warn("DEBUG MODE: providing user from request context")
            return context.user
        else:
            return

    token = authorization[7:]
    return token_to_user(token)


def token_to_user(token):
    """Given a JWT, return the appropriate user"""

    claims = jwt.decode(
        token, settings.SECRET_KEY,
        [getattr(settings, "JWT_ALGORITHM", "HS256")])

    try:
        user = User.objects.get(pk=int(claims["sub"]))
    except:
        raise ValueError("invalid token")

    return user


class StarNode(DjangoObjectType):
    class Meta:
        model = Star


class StarQuery(graphene.ObjectType):
    all_stars = graphene.List(StarNode, token=graphene.String())
    star = graphene.Field(
        StarNode, date=graphene.String(), token=graphene.String(required=True))

    def resolve_all_stars(self, info, token, **kwargs):
        """Produce all stars owned by the provided user."""
        user = token_to_user(token)

        if user is None:
            return

        return Star.objects.filter(user=user)

    def resolve_star(self, info, date, token, **kwargs):
        """Produce a specific star for a given date."""
        user = token_to_user(token)

        if user is None:
            return

        d = parse(date)
        star = Star.objects.get(date=d, user=user)
        return star


class SaveStar(graphene.Mutation):
    date = graphene.Date(required=True)
    spirit = graphene.Int(required=True)
    exercise = graphene.Int(required=True)
    play = graphene.Int(required=True)
    work = graphene.Int(required=True)
    friends = graphene.Int(required=True)
    adventure = graphene.Int(required=True)

    class Arguments:
        spirit = graphene.Int()
        exercise = graphene.Int()
        play = graphene.Int()
        work = graphene.Int()
        friends = graphene.Int()
        adventure = graphene.Int()
        token = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        today = datetime.today()

        try:
            user = token_to_user(kwargs["token"])
        except:
            user = None

        if user is None:
            raise ValueError("not authorized")

        try:
            star = Star.objects.get(user=user, date=today)
        except Star.DoesNotExist:
            star = Star(user=user, date=today)

        for field in ["spirit", "exercise", "play", "work", "friends"
                     ,"adventure"]:
            new_val = kwargs.get(field, getattr(star, field))

            if new_val is None:
                new_val = 3

            setattr(star, field, new_val)

        star.save()
        return SaveStar(
            date=today, spirit=star.spirit, exercise=star.exercise,
play=star.play, work=star.work,
            friends=star.friends, adventure=star.adventure)


class StarMutation(graphene.ObjectType):
    save_star = SaveStar.Field()
