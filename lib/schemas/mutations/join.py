from datetime import datetime
import graphene

from lib.mongo import db
from lib.definition import Faction
from lib.schemas.types.join_info import JoinInfo, JoinStatus

allowed_char = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_'


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

        if len(agent_name) > 16:
            raise Exception('Agent name must not more than 16 characters.')
        if len(telegram) > 40:
            raise Exception('Telegram username must not more than 40 characters.')
        if len(other) > 512:
            raise Exception('Descriptions must not more than 512 characters.')

        for ch in agent_name:
            if ch not in allowed_char:
                raise Exception('Agent name must match the pattern [0-9A-Za-z_]+')
        for ch in telegram:
            if ch not in allowed_char:
                raise Exception('Telegram username must match the pattern [0-9A-Za-z_]+')

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
