from datetime import datetime
import graphene

from lib.mongo import db
from lib.definition import Faction
from lib.schemas.types.join_info import JoinInfo


class Join(graphene.Mutation):
    class Meta:
        output = JoinInfo

    class Arguments:
        agent_name = graphene.String(required=True)
        telegram = graphene.String(required=True)
        regions = graphene.List(graphene.String, required=True)
        other = graphene.String()

    async def mutate(self, info, agent_name, telegram, regions, other=None):
        if not info.context.logged_in:
            raise Exception('Please log in first.')

        me = info.context.user
        if me.faction != Faction.Resistance:
            raise Exception('Access denied.')

        if agent_name == '' or telegram == '' or len(regions) == 0:
            raise Exception('Agent name, telegram username and regions must not be empty.')

        join_info = {
            'agent_name': agent_name,
            'telegram': telegram,
            'regions': regions,
            'other': '' if other is None else other,
            'updated_at': datetime.now(),
        }

        db().users.update_one({'_id': me.id}, {
            '$set': {
                'join_info': join_info
            }
        })

        return JoinInfo(
            agent_name=join_info['agent_name'],
            telegram=join_info['telegram'],
            regions=join_info['regions'],
            other=join_info['other'],
            updated_at=str(join_info['updated_at'])
        )
