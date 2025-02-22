from model.node import Node
from typing import List
from model.relation import Relation
from datetime import datetime

class SimilarToRelation(Relation):
    def __init__(self, user1: Node, user2: Node, score: float, score_date=None, preference=List[str]):
        score_date = score_date or datetime.now().strftime('%Y-%m-%d')

        super().__init__(
            user1, "SIMILAR_TO", user2,
            score=score,
            score_date=score_date,
            preference=preference
        )
