from typing import List
from model.node import Node

class User(Node):
    def __init__(self, name: str, age: int, favorite_genres: str, favorite_duration: int):
        self.name = name
        self.age = age
        self.favorite_genres = favorite_genres
        self.favorite_duration = favorite_duration