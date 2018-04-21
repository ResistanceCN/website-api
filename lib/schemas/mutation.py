import graphene

from .mutations.join import Join
from .mutations.create_profile import CreateProfile
from .mutations.create_article import CreateArticle
from .mutations.update_article import UpdateArticle


class Mutation(graphene.ObjectType):
    join = Join.Field()
    create_profile = CreateProfile.Field()
    create_article = CreateArticle.Field()
    update_article = UpdateArticle.Field()
