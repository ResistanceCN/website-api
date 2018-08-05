from datetime import datetime
import graphene

from lib.mongo import db
from lib.definition import Faction
from lib.schemas.types.join_info import JoinInfo, JoinStatus


class Join(graphene.Mutation):
    class Meta:
        output = JoinInfo

    class Arguments:
        agent_name = graphene.String(required=True)
        telegram = graphene.String(required=True)
        regions = graphene.List(graphene.String, required=True)
        other = graphene.String()

    async def mutate(self, info, agent_name, telegram, regions, other=''):
        if not info.context.logged_in:
            raise Exception('Please log in first.')

        me = info.context.user
        if me.faction != Faction.Resistance:
            raise Exception('Access denied.')

        if agent_name == '' or telegram == '' or len(regions) == 0:
            raise Exception('Agent name, telegram username and regions must not be empty.')

        user = db().users.find_one({'_id': me.id})
        now = datetime.now()

        try:
            join_info = user['join_info']
        except Exception:
            join_info = {
                'created_at': now,
                'status': JoinStatus.PENDING.value
            }

        if join_info.get('status') == JoinStatus.REJECTED:
            raise Exception('Access denied.')

        join_info = {
            **join_info,
            'agent_name': agent_name,
            'telegram': telegram,
            'regions': regions,
            'other': other,
            'updated_at': now,
        }

        db().users.update_one({'_id': me.id}, {
            '$set': {
                'join_info': join_info
            }
        })

        info.context.loaders.user.clear(me.id)

        return JoinInfo.from_dict({
            **join_info,
            'user_id': me.id,
        })
