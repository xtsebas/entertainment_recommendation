from typing import List
from model.node import Node

class Genre:
    def __init__(self, genre_id: str, name: str, avg: float, description: str, popular: bool):
        self.genre_id = genre_id
        self.name = name
        self.avg = avg
        self.description = description
        self.popular = popular

    @property
    def genre_id(self):
        return self._genre_id
    
    @genre_id.setter
    def genre_id(self, value: str):
        self._genre_id = value

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def avg(self):
        return self._avg
    
    @avg.setter
    def avg(self, value: float):
        self._avg = value

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def popular(self):
        return self._popular
    
    @popular.setter
    def popular(self, value: bool):
        self._popular = value
