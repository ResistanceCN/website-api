import graphene

from lib.mongo import db
from lib.schemas.types.article import Article, ArticleStatus


class AdminQuery(graphene.ObjectType):
    list_articles = graphene.Field(
        type=graphene.List(Article),
        count=graphene.Int(default_value=30),
        offset=graphene.Int(default_value=0),
        status=graphene.Argument(ArticleStatus)
    )

    def resolve_list_articles(self, info, count, offset, status=None):
        cond = {}
        if status is not None:
            cond['status'] = status

        articles = []
        results = db().articles.find(cond).skip(offset).limit(count)

        for result in results:
            articles.append(Article.from_dict(result))

        return articles
