import graphene

from lib.mongo import db
from lib.schemas.types.join_info import JoinInfo, JoinStatus
from lib.schemas.types.article import Article, ArticleStatus


class AdminQuery(graphene.ObjectType):
    hello = graphene.String(
        name=graphene.String(default_value="world"),
    )
    total_articles = graphene.Int(
        status=graphene.Argument(ArticleStatus)
    )
    list_articles = graphene.Field(
        type=graphene.List(Article),
        count=graphene.Int(default_value=30),
        offset=graphene.Int(default_value=0),
        status=graphene.Argument(ArticleStatus)
    )
    total_join_info = graphene.Int(
        status=graphene.Argument(JoinStatus)
    )
    # list_join_info = graphene.Field(
    #     type=graphene.List(JoinInfo),
    #     count=graphene.Int(default_value=30),
    #     offset=graphene.Int(default_valu=0),
    #     status=graphene.Argument(JoinStatus)
    # )

    def resolve_hello(self, info, name):
        print(info.context)
        return 'Hello ' + name

    def resolve_total_articles(self, info, status=None):
        cond = {}
        if status is not None:
            cond['status'] = status

        return db().articles.find(cond).count()

    def resolve_list_articles(self, info, count, offset, status=None):
        cond = {}
        if status is not None:
            cond['status'] = status

        articles = []
        results = db().articles.find(cond).skip(offset).limit(count)

        for result in results:
            articles.append(Article.from_dict(result))

        return articles

    def resolve_total_join_info(self, info, status=None):
        cond = {}
        if status is not None:
            cond['status'] = status
        return db().users.join_info.find(cond).count()

    # def resolve_list_join_info(self, info, count, offset, status=None):
    #     cond = {}
    #     if status is not None:
    #         cond['status'] = status
    #
    #     join_info = []
    #     results = db().users.join_info.find(cond).skip(offset).limit(count)
    #
    #     for result in results:
    #         join_info.append(JoinInfo.from_dict(result))
    #
    #     return join_info
