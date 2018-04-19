import graphene

from .mutations.create_profile import CreateProfile
from .mutations.create_article import CreateArticle
from .mutations.update_article import UpdateArticle


class Mutation(graphene.ObjectType):
    create_profile = CreateProfile.Field()
    create_article = CreateArticle.Field()
    update_article = UpdateArticle.Field()
