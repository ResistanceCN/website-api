import graphene

from .object import ObjectType
from lib.helper import estr


class JoinStatus(graphene.Enum):
    PENDING = 0
    APPROVED = 1
    REJECTED = 2

    @property
    def description(self):
        if self == JoinStatus.APPROVED:
            return "The agent has been admitted to our community."
        if self == JoinStatus.REJECTED:
            return "The joining request has been rejected."

        return "The joining request is waiting for review."


class JoinInfo(ObjectType):
    user_id = graphene.ID(required=True)
    agent_name = graphene.String(required=True)
    telegram = graphene.String(required=True)
    regions = graphene.List(graphene.String, required=True)
    other = graphene.String(required=True)
    status = JoinStatus(required=True)
    comment = graphene.String()
    created_at = graphene.String(required=True)
    updated_at = graphene.String(required=True)

    @classmethod
    def from_dict(cls, data: dict):
        try:
            status = JoinStatus.get(data.get('status'))
        except ValueError:
            status = JoinStatus.PENDING

        return cls(
            user_id=data['user_id'],
            agent_name=data['agent_name'],
            telegram=data['telegram'],
            regions=data['regions'],
            other=data['other'],
            status=status,
            comment=estr(data.get('comment')),
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )
