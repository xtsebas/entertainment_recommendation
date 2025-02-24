from model.node import Node

class Movie(Node):
    def __init__(self, movie_id: str, title: str, score: float, description: str, released: bool):
        super().__init__(movie_id, "Movie", title=title, score=score, description=description, released=released)

    @property
    def title(self) -> str:
        return self.properties.get("title")
    
    @title.setter
    def title(self, value: str):
        self.properties["title"] = value

    @property
    def score(self) -> float:
        return self.properties.get("score")
    
    @score.setter
    def score(self, value: float):
        self.properties["score"] = value

    @property
    def description(self) -> str:
        return self.properties.get("description")
    
    @description.setter
    def description(self, value: str):
        self.properties["description"] = value

    @property
    def released(self) -> bool:
        return self.properties.get("released")
    
    @released.setter
    def released(self, value: bool):
        self.properties["released"] = value
