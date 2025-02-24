from model.node import Node
from model.relation import Relation

class BelongsToMovieRelation(Relation):
    def __init__(self, rating: Node, movie: Node, relevance: float, rating_context: str, first_impression: bool):
        super().__init__(
            rating,          
            "BELONGS_TO",     
            movie,       
            relevance=relevance,
            rating_context=rating_context,
            first_impression=first_impression
        )
