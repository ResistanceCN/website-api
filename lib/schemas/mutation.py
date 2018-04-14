import graphene

from .mutations.create_profile import CreateProfile
from .mutations.update_article import UpdateArticle


class Mutation(graphene.ObjectType):
    create_profile = CreateProfile.Field()
    update_article = UpdateArticle.Field()
