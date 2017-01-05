from nestedworld_api.app import ma
from nestedworld_api.login import login_required, current_session
from . import users


class Stats(users.Resource):

    # - Nombre de victoires (portails, pve, pvp)
    # - Nombre de défaites (same as before)
    # - Stats sur les types de montres (le plus possédé)
    def _get(self, user):
        import random
        from nestedworld_api.db.monster import TYPES

        victories = {
            'portals': random.randint(0, 10),
            'pve': random.randint(0, 10),
            'pvp': random.randint(0, 10),
        }
        victories['total'] = sum(value for (key, value) in victories.items())
        defeats = {
            'portals': random.randint(0, 10),
            'pve': random.randint(0, 10),
            'pvp': random.randint(0, 10),
        }
        defeats['total'] = sum(value for (key, value) in defeats.items())

        monster_types = {ty: 0 for ty in TYPES}
        for entry in user.user_monsters:
            monster_types[entry.monster.type] += 1

        return {
            'combats': {
                'victories': victories,
                'defeats': defeats,
            },
            'monsters': {
                'types': monster_types,
            },
        }


@users.route('/me/stats')
class SelfStats(Stats):

    @login_required
    def get(self):
        return self._get(current_session.user)


@users.route('/<user_id>/stats')
class UserStats(Stats):

    @login_required
    def get(self, user_id):
        from nestedworld_api.db import User
        from sqlalchemy.orm import joinedload

        user = User.query\
            .options(joinedload('user_monsters', 'monster'))\
            .get_or_404(user_id)
        return self._get(user)
