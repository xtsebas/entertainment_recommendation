from neo4j import GraphDatabase
import os
from view.user import User

# Configuración de conexión a Neo4j Aura
NEO4J_URI = os.getenv("NEO4J_URI") 
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

class UserController:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def create_user(self, user: User):
        """
        Inserta un usuario en Neo4j.
        """
        with self.driver.session() as session:
            session.write_transaction(self._create_user_tx, user)
        return {"message": "Usuario creado correctamente"}

    @staticmethod
    def _create_user_tx(tx, user: User):
        query = """
        CREATE (u:User {user_id: $user_id, nombre: $nombre, edad: $edad, generos_favoritos: $generos_favoritos, duracion_favorita: $duracion_favorita})
        """
        tx.run(query, user_id=user.node_id, nombre=user.nombre, edad=user.edad, generos_favoritos=user.generos_favoritos, duracion_favorita=user.duracion_favorita)

    def get_users(self):
        """
        Obtiene todos los usuarios almacenados en Neo4j.
        """
        with self.driver.session() as session:
            result = session.read_transaction(self._get_users_tx)
        return result

    @staticmethod
    def _get_users_tx(tx):
        query = "MATCH (u:User) RETURN u"
        result = tx.run(query)
        return [record["u"] for record in result]

    def delete_user(self, user_id: str):
        """
        Elimina un usuario de Neo4j.
        """
        with self.driver.session() as session:
            session.write_transaction(self._delete_user_tx, user_id)
        return {"message": f"Usuario {user_id} eliminado correctamente"}

    @staticmethod
    def _delete_user_tx(tx, user_id: str):
        query = "MATCH (u:User {user_id: $user_id}) DETACH DELETE u"
        tx.run(query, user_id=user_id)
