import graphene

from .object import ObjectType


class JoinStatus(graphene.Enum):
    CREATED = 0
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
    agent_name = graphene.String(required=True)
    telegram = graphene.String(required=True)
    regions = graphene.List(graphene.String, required=True)
    other = graphene.String(required=True)
    status = JoinStatus(required=True)
    created_at = graphene.String(required=True)
    updated_at = graphene.String(required=True)

    @classmethod
    def from_dict(cls, data: dict):
        try:
            status = JoinStatus.get(data.get('status'))
        except ValueError:
            status = JoinStatus.CREATED

        return cls(
            agent_name=data['agent_name'],
            telegram=data['telegram'],
            regions=data['regions'],
            other=data['other'],
            status=status,
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )
