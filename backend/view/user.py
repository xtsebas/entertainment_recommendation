from typing import List
from model.node import Node

class User(Node):
    def __init__(self, user_id: str, name: str, age: int, favorite_genres: List[str], favorite_duration: int):
        super().__init__(user_id, "User", name=name, age=age, favorite_genres=favorite_genres, favorite_duration=favorite_duration)

    @property
    def name(self):
        return self.properties['name']
    
    @name.setter
    def name(self, value: str):
        self.properties['name'] = value
    
    @property
    def age(self):
        return self.properties['age']
    
    @age.setter
    def age(self, value: int):
        self.properties['age'] = value
    
    @property
    def favorite_genres(self):
        return self.properties['favorite_genres']
    
    @favorite_genres.setter
    def favorite_genres(self, value: List[str]):
        self.properties['favorite_genres'] = value
    
    @property
    def favorite_duration(self):
        return self.properties['favorite_duration']
    
    @favorite_duration.setter
    def favorite_duration(self, value: int):
        self.properties['favorite_duration'] = value