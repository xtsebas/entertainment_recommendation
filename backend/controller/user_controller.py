from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from view.user import User

load_dotenv()

# Configuración de conexión a Neo4j Aura
NEO4J_URI = os.getenv("NEO4J_URI") 
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

class UserController:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    #Create user
    def create_user(self, user: User):
        """
        Inserta un usuario en Neo4j.
        """
        with self.driver.session() as session:
            session.execute_write(self._create_user_tx, user)
        return {"message": "Usuario creado correctamente"}

    @staticmethod
    def _create_user_tx(tx, user: User):
        query = """
        CREATE (u:User {user_id: $user_id, name: $name, age: $age, favorite_genres: $favorite_genres, favorite_duration: $favorite_duration})
        """
        tx.run(query, user_id=user.node_id, name=user.name, age=user.age, favorite_genres=user.favorite_genres, favorite_duration=user.favorite_duration)

    #Get user
    def get_users(self):
        """
        Obtiene todos los usuarios almacenados en Neo4j.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._get_users_tx)
        return result

    @staticmethod
    def _get_users_tx(tx):
        query = "MATCH (u:User) RETURN u"
        result = tx.run(query)
        return [record["u"] for record in result]

    #Delete user
    def delete_user(self, user_id: str):
        """
        Elimina un usuario de Neo4j.
        """
        with self.driver.session() as session:
            session.execute_write(self._delete_user_tx, user_id)
        return {"message": f"Usuario {user_id} eliminado correctamente"}

    @staticmethod
    def _delete_user_tx(tx, user_id: str):
        query = "MATCH (u:User {user_id: $user_id}) DETACH DELETE u"
        tx.run(query, user_id=user_id)
