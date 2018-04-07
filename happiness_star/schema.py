from jose import jwt
from datetime import datetime
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
    claims = jwt.decode(
        token, settings.SECRET_KEY,
        [getattr(settings, "JWT_ALGORITHM", "HS256")])
    ts = datetime.now().timestamp()

    if ts < claims["nbf"] or ts > claims["exp"]:
        raise ValueError("invalid token")

    try:
        user = User.objects.get(pk=int(claims["sub"]))
    except:
        raise ValueError("invalid token")

    return user


class StarNode(DjangoObjectType):
    class Meta:
        model = Star


class StarQuery(graphene.ObjectType):
    all_stars = graphene.List(StarNode)
    star = graphene.Field(StarNode, date=graphene.Date())

    def resolve_all_stars(self, info, **kwargs):
        """Produce all stars owned by the provided user."""
        user = context_to_user(info.context)

        if user is None:
            return

        return Star.objects.filter(user=user)

    def resolve_star(self, info, date, **kwargs):
        """Produce a specific star for a given date."""
        user = context_to_user(info.context)

        if user is None:
            return

        star = Star.objects.get(date=date)
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
        spirit = graphene.Int(required=True)
        exercise = graphene.Int(required=True)
        play = graphene.Int(required=True)
        work = graphene.Int(required=True)
        friends = graphene.Int(required=True)
        adventure = graphene.Int(required=True)

    def mutate(self, info, spirit, exercise, play, work, friends, adventure):
        today = datetime.today()
        user = context_to_user(info.context)

        if user is None:
            raise ValueError("not authorized")

        try:
            star = Star.objects.get(user=user, date=today)
        except Star.DoesNotExist:
            star = Star(user=user, date=today)

        star.spirit = spirit
        star.exercise = exercise
        star.play = play
        star.work = work
        star.friends = friends
        star.adventure = adventure
        star.save()

        return SaveStar(
            date=today, spirit=spirit, exercise=exercise, play=play, work=work,
            friends=friends, adventure=adventure)


class StarMutation(graphene.ObjectType):
    save_star = SaveStar.Field()
