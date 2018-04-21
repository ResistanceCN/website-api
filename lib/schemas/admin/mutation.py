import graphene

from .mutations.update_article import UpdateArticle
from .mutations.delete_article import DeleteArticle


class AdminMutation(graphene.ObjectType):
    update_article = UpdateArticle.Field()
    delete_article = DeleteArticle.Field()
