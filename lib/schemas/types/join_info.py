import graphene

from .object import ObjectType


class JoinStatus(graphene.Enum):
    NOINVITED = 0
    INVITED = 1
    BANNED = 2

    @property
    def description(self):
        if self == JoinStatus.INVITED:
            return "This agent has been invited to our telegram groups."
        if self == JoinStatus.BANNED:
            return "This agent has been banned."
        return "This agent hasn't been invited to our telegram groups."


class JoinInfo(ObjectType):
    agent_name = graphene.String(required=True)
    telegram = graphene.String(required=True)
    regions = graphene.List(graphene.String, required=True)
    other = graphene.String(required=True)
    updated_at = graphene.String(required=True)

    @classmethod
    def from_dict(cls, data: dict):
        try:
            status = JoinStatus.get(data.get('status'))
        except ValueError:
            status = JoinStatus.NOINVITED

        return cls(
            agent_name=data['agent_name'],
            telegram=data['telegram'],
            regions=data['regions'],
            other=data['other'],
            updated_at=data['updated_at']
        )
