import graphene

from .mutations.update_article import UpdateArticle
from .mutations.delete_article import DeleteArticle
from .mutations.update_join_info import UpdateJoinInfo


class AdminMutation(graphene.ObjectType):
    update_article = UpdateArticle.Field()
    delete_article = DeleteArticle.Field()
    # update_join_info = UpdateJoinInfo.Field()
