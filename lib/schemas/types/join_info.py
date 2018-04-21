import graphene

from .object import ObjectType


class JoinInfo(ObjectType):
    name = graphene.String(required=True)
    telegram = graphene.String(required=True)
    regions = graphene.List(graphene.String, required=True)
    other = graphene.String(required=True)
    updated_at = graphene.String(required=True)
