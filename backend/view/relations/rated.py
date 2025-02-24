from model.node import Node
from model.relation import Relation
from datetime import datetime

class RatedRelation(Relation):
    def __init__(self, user: Node, rating: Node, recommendation_level: int, rating_date: str = None, rating_change_count: int = 0):
        # Si no se especifica, se asigna la fecha actual
        rating_date = rating_date or datetime.now().strftime('%Y-%m-%d')
        
        super().__init__(
            user,       
            "RATED",      
            rating,       
            rating_date=rating_date,
            recommendation_level=recommendation_level,
            rating_change_count=rating_change_count
        )
