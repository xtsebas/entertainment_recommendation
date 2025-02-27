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

    #Create user
    def create_user(self, user: User):
        """
        Inserta un usuario en Neo4j.
        """
        with self.driver.session() as session:
            result = session.execute_write(
                self._create_user_tx, 
                user.name, user.age, user.favorite_genres, user.favorite_duration
            )
        return result
    
    @staticmethod
    def _create_user_tx(tx, name: str, age: int, favorite_genres: str, favorite_duration: int):
        query = """
        CREATE (u:User {name: $name, age: $age, favorite_genres: $favorite_genres, favorite_duration: $favorite_duration})
        RETURN u.node_id AS id, u.name AS name, u.age AS age, u.favorite_genres AS favorite_genres, u.favorite_duration AS favorite_duration
        """
        result = tx.run(
            query,
            name=name,
            age=age,
            favorite_genres=favorite_genres,
            favorite_duration=favorite_duration
        )
        return result.single()

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
    def get_user_by_credentials(self, name: str):
        """
        Busca un usuario por nombre y verifica su contraseña.
        """
        with self.driver.session() as session:
            user_data = session.execute_read(self._get_user_by_name_tx, name)
        
        if user_data:
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
    
    # Reimplementing the function `get_movies_not_rated_by_user` after execution state reset

    def get_movies_not_rated_by_user(self, user_id: str, limit: int):
        """
        Retrieves movies that the user has not rated.
        Enforces a maximum limit of 30 movies.
        """
        
        """
        output sample with limit 5 for user_id = cbd92f90-6e2d-4441-b2b9-d9ba9942edd5
        see backen/test/test_get_not_rated_movies.py
        
        {
        "media_id": "06c03bbe-ff2d-46a4-b606-8bd185e35270",
        "movie_title": "Forget despite",
        "revenue": 1012876502.65,
        "budget": 96502898.65,
        "duration": 143,
        "release_date": datetime(1986, 10, 21).isoformat()
        }, ....
        """
        if limit > 30:
            raise ValueError("Limit exceeded: The maximum allowed is 30.")

        with self.driver.session() as session:
            result = session.execute_read(self._get_movies_not_rated_by_user_tx, user_id, limit)
        
        return result  # Returns the movie/series objects

    @staticmethod
    def _get_movies_not_rated_by_user_tx(tx, user_id: str, limit: int):
        query = """
        MATCH (med:Media)-[:IS_A]->(m:Media:Movie)
        WHERE NOT EXISTS {
            MATCH (:User {user_id: $user_id})-[:RATED]->(:Rating)-[:BELONGS_TO]->(m)
        }
        RETURN 
            med.media_id AS media_id, 
            med.title AS movie_title,
            m.revenue AS revenue,
            m.budget AS budget,
            m.duration AS duration,
            med.release_date AS release_date
        ORDER BY rand()
        LIMIT $limit
        """
        result = tx.run(query, user_id=user_id, limit=limit)
        
        
        
        return [record.data() for record in result]

    def get_series_not_rated_by_user(self, user_id: str, limit: int):
        """
        Retrievesseries that the user has not rated.
        Enforces a maximum limit of 30 series.
        """
        
        """
        output sample with limit 5 for user_id = cbd92f90-6e2d-4441-b2b9-d9ba9942edd5
        see backen/test/test_get_not_rated_series.py
        
        {
            "media_id": "41c12c32-e13f-40d1-9540-33596a25325c",
            "serie_title": "Professor my south",
            "total_episodes": 166,
            "total_seasons": 2,
            "show_runner": "Corey Gillespie",
            "status": "Ended",
            "release_date": "2020-04-23T00:00:00"
        },...
        """
        if limit > 30:
            raise ValueError("Limit exceeded: The maximum allowed is 30.")

        with self.driver.session() as session:
            result = session.execute_read(self._get_series_not_rated_by_user_tx, user_id, limit)
        
        return result  # Returns the movie/series objects

    @staticmethod
    def _get_series_not_rated_by_user_tx(tx, user_id: str, limit: int):
        query = """
        MATCH (med:Media)-[:IS_A]->(m:Media:Serie)
        WHERE NOT EXISTS {
            MATCH (:User {user_id: $user_id})-[:RATED]->(:Rating)-[:BELONGS_TO]->(m)
        }
        RETURN 
            med.media_id AS media_id, 
            med.title AS serie_title,
            m.total_episodes AS total_episodes,
            m.total_seasons AS total_seasons,
            m.show_runner AS show_runner,
            m.status AS status,
            med.release_date AS release_date
        ORDER BY rand()
        LIMIT $limit
        """
        result = tx.run(query, user_id=user_id, limit=limit)
        
        
        
        return [record.data() for record in result]

