from typing import List
from model.node import Node

class Genre(Node):
    def __init__(self, genre_id: str, name: str, avg: float, description: str, popular: bool):
        super().__init__(genre_id, "Genre", name=name, avg=avg, description=description, popular=popular)

    @property
    def name(self):
        return self.properties['name']
    
    @name.setter
    def name(self, value: str):
        self.properties['name'] = value
    
    @property
    def avg(self):
        return self.properties['avg']
    
    @avg.setter
    def avg(self, value: int):
        self.properties['avg'] = value
    
    @property
    def description(self):
        return self.properties['description']
    
    @description.setter
    def description(self, value: str):
        self.properties['description'] = value
    
    @property
    def popular(self):
        return self.properties['popular']
    
    @popular.setter
    def popular(self, value: bool):
        self.properties['popular'] = value
