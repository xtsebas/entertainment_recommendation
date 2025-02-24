from model.node import Node

class Series(Node):
    def __init__(self, series_id: str, title: str, score: float, description: str, on_air: bool):
        super().__init__(series_id, "Series", title=title, score=score, description=description, on_air=on_air)

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
    def on_air(self) -> bool:
        return self.properties.get("on_air")
    
    @on_air.setter
    def on_air(self, value: bool):
        self.properties["on_air"] = value
