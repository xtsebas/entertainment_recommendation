from neo4j import GraphDatabase
import bcrypt
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

    @staticmethod
    def _hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    # Método para verificar contraseñas
    @staticmethod
    def _verify_password(hashed_password: str, password: str) -> bool:
        """Verifica una contraseña con su hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    #Create user
    def create_user(self, user: User, password: str):
        """
        Inserta un usuario en Neo4j.
        """
        hashed_password = self._hash_password(password)
        with self.driver.session() as session:
            session.execute_write(self._create_user_tx, user, hashed_password)
        return {"message": "Usuario creado correctamente"}

    @staticmethod
    def _create_user_tx(tx, user: User, hashed_password=str):
        query = """
        CREATE (u:User {user_id: $user_id, name: $name, password: $password, age: $age, favorite_genres: $favorite_genres, favorite_duration: $favorite_duration})
        """
        tx.run(query, user_id=user.node_id, name=user.name, password=hashed_password, age=user.age, favorite_genres=user.favorite_genres, favorite_duration=user.favorite_duration)

    #Get users
    def get_users(self):
        """
        Obtiene todos los usuarios almacenados en Neo4j.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._get_users_tx)
        return result

    @staticmethod
    def _get_users_tx(tx):
        """
        Consulta para obtener todos los usuarios sin la contraseña.
        """
        query = """
        MATCH (u:User)
        RETURN u.user_id AS user_id, u.name AS name, u.age AS age, 
               u.favorite_genres AS favorite_genres, 
               u.favorite_duration AS favorite_duration
        """
        result = tx.run(query)
        return [record.data() for record in result]

    #Get user
    def get_user_by_credentials(self, name: str, password: str):
        """
        Busca un usuario por nombre y verifica su contraseña.
        """
        with self.driver.session() as session:
            user_data = session.execute_read(self._get_user_by_name_tx, name)
        
        if user_data and user_data['password']:
            if self._verify_password(user_data["password"], password):
                # Si la contraseña es correcta, devolver los datos sin incluirla
                return {
                    "user_id": user_data["user_id"],
                    "name": user_data["name"],
                    "age": user_data["age"],
                    "favorite_genres": user_data["favorite_genres"],
                    "favorite_duration": user_data["favorite_duration"]
                }
        return None  # Si no coincide la contraseña o no se encuentra el usuario

    @staticmethod
    def _get_user_by_name_tx(tx, name: str):
        """
        Busca un usuario por su nombre y obtiene su contraseña hasheada.
        """
        query = """
        MATCH (u:User {name: $name})
        RETURN u.user_id AS user_id, u.name AS name, u.age AS age, 
               u.favorite_genres AS favorite_genres, 
               u.favorite_duration AS favorite_duration,
               u.password AS password
        """
        result = tx.run(query, name=name)
        return result.single() 
    

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
