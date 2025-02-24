from model.node import Node
from model.relation import Relation

class BelongsToSeriesRelation(Relation):
    def __init__(self, rating: Node, series: Node, relevance: float, rating_context: str, seasons_watched: int):
        super().__init__(
            rating,          
            "BELONGS_TO",     
            series,           
            relevance=relevance,
            rating_context=rating_context,
            seasons_watched=seasons_watched
        )
