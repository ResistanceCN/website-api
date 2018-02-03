import graphene

import lib.schemas.article
import lib.loader.article
from lib.loader.article_ids_of_user import article_ids_of_user_loader


class User(graphene.ObjectType):
    id = graphene.Int()
    google_id = graphene.String()
    email = graphene.String()
    name = graphene.String()
    is_admin = graphene.Boolean()
    faction = graphene.Int()
    created_at = graphene.String()
    articles = graphene.List(lambda: lib.schemas.article.Article)

    async def resolve_articles(self, info):
        article_ids = await article_ids_of_user_loader.load(self.id)
        articles = await lib.loader.article.article_loader.load_many(article_ids)

        if info.context.user.id != self.id:
            articles = [article for article in articles if article.published_at is not None]

        lib.loader.article.filter_article_fields(articles, info.context)
        return articles
