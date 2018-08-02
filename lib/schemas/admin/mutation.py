import graphene

from .mutations.update_article import UpdateArticle
from .mutations.delete_article import DeleteArticle
from .mutations.empty_join_info import EmptyJoinInfo


class AdminMutation(graphene.ObjectType):
    update_article = UpdateArticle.Field()
    delete_article = DeleteArticle.Field()
    empty_join_info = EmptyJoinInfo.Field()