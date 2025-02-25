from model.node import Node

class Movie(Node):
    def __init__(self, movie_id: str, duration: int, budget: float, revenue: float,
                 nominations: list, age_classification: str):
        super().__init__(movie_id, "Movie",
                         duration=duration,
                         budget=budget,
                         revenue=revenue,
                         nominations=nominations,
                         age_classification=age_classification)

    @property
    def duration(self) -> int:
        return self.properties.get("duration")

    @duration.setter
    def duration(self, value: int):
        self.properties["duration"] = value

    @property
    def budget(self) -> float:
        return self.properties.get("budget")

    @budget.setter
    def budget(self, value: float):
        self.properties["budget"] = value

    @property
    def revenue(self) -> float:
        return self.properties.get("revenue")

    @revenue.setter
    def revenue(self, value: float):
        self.properties["revenue"] = value

    @property
    def nominations(self) -> list:
        return self.properties.get("nominations")

    @nominations.setter
    def nominations(self, value: list):
        self.properties["nominations"] = value

    @property
    def age_classification(self) -> str:
        return self.properties.get("age_classification")

    @age_classification.setter
    def age_classification(self, value: str):
        self.properties["age_classification"] = value
