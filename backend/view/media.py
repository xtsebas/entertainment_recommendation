from datetime import date
from model.node import Node

class Media(Node):
    def __init__(self, media_id: str, title: str, genres: list, release_date: date, avg_rating: float):
        super().__init__(media_id, "Media",
                         title=title,
                         genres=genres,
                         release_date=release_date,
                         avg_rating=avg_rating)

    @property
    def title(self) -> str:
        return self.properties.get("title")

    @title.setter
    def title(self, value: str):
        self.properties["title"] = value

    @property
    def genres(self) -> list:
        return self.properties.get("genres")

    @genres.setter
    def genres(self, value: list):
        self.properties["genres"] = value

    @property
    def release_date(self) -> date:
        return self.properties.get("release_date")

    @release_date.setter
    def release_date(self, value: date):
        self.properties["release_date"] = value

    @property
    def avg_rating(self) -> float:
        return self.properties.get("avg_rating")

    @avg_rating.setter
    def avg_rating(self, value: float):
        self.properties["avg_rating"] = value
