from dateutil.parser import parse

import graphene
from graphene_django import DjangoObjectType

from user_extensions.utils import jwt_user, user_time

from .models import Star, Tag


class TagNode(DjangoObjectType):
    class Meta:
        model = Tag


class StarNode(DjangoObjectType):
    class Meta:
        model = Star

    tags = graphene.List(TagNode)

    def resolve_tags(root, info):
        return Tag.objects.filter(star=root)


class StarQuery(graphene.ObjectType):
    all_stars = graphene.List(StarNode, token=graphene.String())
    star = graphene.Field(
        StarNode, date=graphene.String(), token=graphene.String(required=True))

    def resolve_all_stars(self, info, token, **kwargs):
        """Produce all stars owned by the provided user."""
        user = jwt_user(token)

        if user is None:
            return

        return Star.objects.filter(user=user)

    def resolve_star(self, info, date, token, **kwargs):
        """Produce a specific star for a given date."""
        user = jwt_user(token)

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
    tags = graphene.List(TagNode, required=True)

    class Arguments:
        spirit = graphene.Int()
        exercise = graphene.Int()
        play = graphene.Int()
        work = graphene.Int()
        friends = graphene.Int()
        adventure = graphene.Int()
        token = graphene.String(required=True)
        tags = graphene.List(graphene.String)

    def mutate(self, info, **kwargs):
        try:
            user = jwt_user(kwargs["token"])
        except:
            raise ValueError("not authorized")

        today = user_time(user)

        try:
            star = Star.objects.get(user=user, date=today)
        except Star.DoesNotExist:
            star = Star(user=user, date=today)

        for field in ["spirit", "exercise", "play", "work", "friends",
                      "adventure"]:
            new_val = kwargs.get(field, getattr(star, field))

            if new_val is None:
                new_val = 3

            setattr(star, field, new_val)

        star.save()

        tag_names = kwargs.get("tags", None)

        if tag_names is not None:

            for name in tag_names:
                lc = name.lower()

                try:
                    tag = Tag.objects.get(name=lc)
                except Tag.DoesNotExist:
                    tag = Tag(name=lc)

                tag.save()
                star.tag_set.add(tag)

        star.save()

        return SaveStar(
            date=today, spirit=star.spirit, exercise=star.exercise,
            play=star.play, work=star.work,
            friends=star.friends, adventure=star.adventure,
            tags=star.tag_set.all())


class StarMutation(graphene.ObjectType):
    save_star = SaveStar.Field()
