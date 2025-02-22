from model.node import Node
from model.relation import Relation
from datetime import datetime

class LikesRelation(Relation):
    def __init__(self, user: Node, genre: Node, preference_level: int, aggregation_date=None, last_engagement=None):
        aggregation_date = aggregation_date or datetime.now().strftime('%Y-%m-%d')
        last_engagement = last_engagement or datetime.now().strftime('%Y-%m-%d')

        super().__init__(
            user, "LIKES", genre,
            preference_level=preference_level,
            aggregation_date=aggregation_date,
            last_engagement=last_engagement
        )
