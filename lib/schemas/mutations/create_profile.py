from datetime import datetime
import graphene

from lib.definition import Faction
from lib.mongo import db
from lib.schemas.types.user import User


class CreateProfile(graphene.Mutation):
    class Meta:
        output = User

    class Arguments:
        name = graphene.String(required=True)
        faction = graphene.Int(required=True)

    def mutate(self, info, name, faction):
        if info.context.logged_in:
            raise Exception('You have been registered.')

        new_user = info.context.new_user
        if new_user is None:
            raise Exception('Please sign in with Google Account first.')

        name_len = len(name)
        if name_len < 3 or name_len > 16:
            raise Exception('Invalid name: 3 <= len(name) <= 16.')

        try:
            _ = Faction(faction)
        except ValueError:
            raise Exception('Invalid faction.')

        now = datetime.now()

        result = db().users.insert_one({
            'google_id': new_user.google_id,
            'email': new_user.email,
            'is_admin': False,
            'name': name,
            'faction': faction,
            'created_at': now
        })

        token = info.context.request.headers.get('Token')
        db().sessions.replace_one({'token': token}, {
            'token': token,
            'user_id': result.inserted_id,
            'expire': now.timestamp() + 604800,
        })

        return User(
            id=result.inserted_id,
            google_id=new_user.google_id,
            email=new_user.email,
            is_admin=False,
            name=name,
            faction=faction,
            created_at=str(now),
        )
