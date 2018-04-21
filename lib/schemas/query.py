import graphene

from lib.mongo import db
from lib.loaders.user import filter_user_fields
from lib.loaders.article import filter_article_fields
from lib.schemas.types.user import User
from lib.schemas.types.join_info import JoinInfo
from lib.schemas.types.article import Article, ArticleStatus


class Query(graphene.ObjectType):
    hello = graphene.String(
        name=graphene.String(default_value="world"),
    )
    me = graphene.Field(User)
    join_info = graphene.Field(JoinInfo)
    user_by_id = graphene.Field(
        type=User,
        id=graphene.ID(required=True),
    )
    article_by_id = graphene.Field(
        type=Article,
        id=graphene.ID(required=True),
    )
    article_count = graphene.Int()
    latest_articles = graphene.Field(
        type=graphene.List(of_type=Article),
        count=graphene.Int(default_value=15),
        offset=graphene.Int(default_value=0),
    )

    def resolve_hello(self, info, name):
        print(info.context)
        return 'Hello ' + name

    async def resolve_me(self, info):
        if not info.context.logged_in:
            raise Exception('You have not been logged in.')

        user_id = info.context.user.id
        user = await info.context.loaders.user.load(user_id)
        if user is None:
            raise Exception('You have not been logged in.')

        filter_user_fields(user, info.context)
        return user

    async def resolve_join_info(self, info):
        if not info.context.logged_in:
            raise Exception('You have not been logged in.')

        user_id = info.context.user.id
        result = db().users.find_one(user_id).get('join_info')

        return None if result is None else JoinInfo(
            name=result['name'],
            telegram=result['telegram'],
            regions=result['regions'],
            other=result['other'],
            updated_at=str(result['updated_at'])
        )

    async def resolve_user_by_id(self, info, id):
        user = await info.context.loaders.user.load(id)
        filter_user_fields(user, info.context)
        return user

    async def resolve_article_by_id(self, info, id):
        article = await info.context.loaders.article.load(id)
        filter_article_fields(article, info.context)
        return article

    def resolve_article_count(self, info):
        return db().articles.count()

    def resolve_latest_articles(self, info, count, offset):
        articles = []

        results = db().articles\
            .find({'status': ArticleStatus.PUBLISHED.value})\
            .sort('_id', -1)\
            .skip(offset)\
            .limit(count)

        for result in results:
            article = Article.from_dict(result)
            filter_article_fields(article, info.context)
            articles.append(article)

        return articles
