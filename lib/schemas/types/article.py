import graphene

from lib.helper import nstr, estr
from .object import ObjectType
import lib.schemas.types.user
import lib.loaders.user


class ArticleStatus(graphene.Enum):
    DRAFT = 0
    PENDING = 1
    PUBLISHED = 2


class Article(ObjectType):
    id = graphene.ID(required=True)
    author_id = graphene.Int(required=True)
    author = graphene.Field(lambda: lib.schemas.types.user.User, required=True)
    tags = graphene.List(graphene.String)
    title = graphene.String(required=True)
    content = graphene.String(required=True)
    status = ArticleStatus(required=True)
    created_at = graphene.String(required=True)
    updated_at = graphene.String(required=True)
    published_at = graphene.String()

    @classmethod
    def from_dict(cls, data: dict):
        try:
            status = ArticleStatus.get(data.get('status'))
        except ValueError:
            status = ArticleStatus.DRAFT

        return cls(
            id=data['_id'],
            author_id=data['author_id'],
            title=estr(data['title']),
            content=estr(data['content']),
            tags=data.get('tags', []),
            status=status.value,
            created_at=str(data['created_at']),
            updated_at=str(data['updated_at']),
            published_at=nstr(data.get('published_at')),
        )

    async def resolve_author(self, info):
        author = await info.context.loaders.user.load(self.author_id)
        lib.loaders.user.filter_user_fields(author, info.context)
        return author
