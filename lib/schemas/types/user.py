from hashlib import md5
import graphene

from .object import ObjectType
import lib.schemas.types.article
import lib.loaders.article


class User(ObjectType):
    id = graphene.ID()
    google_id = graphene.String()
    email = graphene.String()
    name = graphene.String()
    is_admin = graphene.Boolean()
    faction = graphene.Int()
    created_at = graphene.String()
    articles = graphene.List(lambda: lib.schemas.types.article.Article)
    email_hash = graphene.String()

    async def resolve_articles(self, info):
        articles = await info.context.loaders.user_articles.load(self.id)

        me = info.context.user
        if not me.is_admin and me.id != self.id:
            articles = [article for article in articles if article.published_at is not None]

        lib.loaders.article.filter_article_fields(articles, info.context)
        return articles

    def resolve_email_hash(self, info):
        if self.email_hash is None:
            self.email_hash = md5(self.get_field('email').encode('utf-8').lower()).hexdigest()

        return self.email_hash
