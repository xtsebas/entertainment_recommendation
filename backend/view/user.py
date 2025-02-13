from typing import List
from model.node import Node

class User(Node):
    def __init__(self, user_id: str, nombre: str, edad: int, generos_favoritos: List[str], duracion_favorita: int):
        super().__init__(user_id, "User", nombre=nombre, edad=edad, generos_favoritos=generos_favoritos, duracion_favorita=duracion_favorita)

    @property
    def nombre(self):
        return self.properties['nombre']
    
    @nombre.setter
    def nombre(self, value: str):
        self.properties['nombre'] = value
    
    @property
    def edad(self):
        return self.properties['edad']
    
    @edad.setter
    def edad(self, value: int):
        self.properties['edad'] = value
    
    @property
    def generos_favoritos(self):
        return self.properties['generos_favoritos']
    
    @generos_favoritos.setter
    def generos_favoritos(self, value: List[str]):
        self.properties['generos_favoritos'] = value
    
    @property
    def duracion_favorita(self):
        return self.properties['duracion_favorita']
    
    @duracion_favorita.setter
    def duracion_favorita(self, value: int):
        self.properties['duracion_favorita'] = value