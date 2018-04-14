import graphene

import lib.schemas.types.article
import lib.loaders.article


class User(graphene.ObjectType):
    id = graphene.ID()
    google_id = graphene.String()
    email = graphene.String()
    name = graphene.String()
    is_admin = graphene.Boolean()
    faction = graphene.Int()
    created_at = graphene.String()
    articles = graphene.List(lambda: lib.schemas.types.article.Article)

    async def resolve_articles(self, info):
        articles = await info.context.loaders.user_articles.load(self.id)

        me = info.context.user
        if not me.is_admin and me.id != self.id:
            articles = [article for article in articles if article.published_at is not None]

        lib.loaders.article.filter_article_fields(articles, info.context)
        return articles
