from neo4j import GraphDatabase
from dotenv import load_dotenv
from datetime import date
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

class LikesRelationController:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        """Cierra la conexión con Neo4j."""
        self.driver.close()

    # Crear relación LIKE
    def create_likes_relation(self, user_id: str, genre_id: str, preference_level: int, aggregation_date: date, last_engagement: date):
        """Crea la relación LIKES entre un usuario y un género usando IDs."""
        with self.driver.session() as session:
            session.execute_write(self._create_likes_tx, user_id, genre_id, preference_level, aggregation_date, last_engagement)

    @staticmethod
    def _create_likes_tx(tx, user_id: str, genre_id: str, preference_level: int, aggregation_date: date, last_engagement: date):
        query = """
        MATCH (u:User {user_id: $user_id})
        MATCH (g:Genre {genre_id: $genre_id}) 
        MERGE (u)-[r:LIKES]->(g)
        SET r.preference_level = $preference_level,
            r.aggregation_date = $aggregation_date,
            r.last_engagement = $last_engagement
        RETURN r
        """
        tx.run(
            query,
            user_id=user_id,
            genre_id=genre_id,
            preference_level=preference_level,
            aggregation_date=aggregation_date.isoformat(),
            last_engagement=last_engagement.isoformat()
        )
        
    # Obtener todas las relaciones LIKE de un usuario
    def get_likes_by_user(self, user_id: str):
        with self.driver.session() as session:
            return session.execute_read(self._get_likes_by_user_tx, user_id)

    @staticmethod
    def _get_likes_by_user_tx(tx, user_id: str):
        query = """
        MATCH (u:User {user_id: $user_id})-[r:LIKES]->(g:Genre)
        RETURN g.user_id AS genre_id, g.name AS genre_name, r.preference_level AS preference_level, 
               r.aggregation_date AS aggregation_date, r.last_engagement AS last_engagement
        """
        result = tx.run(query, user_id=user_id)
        return [record.data() for record in result]

    # Eliminar una relación LIKE
    def delete_likes_relation(self, user_id: str, genre_id: str):
        with self.driver.session() as session:
            session.execute_write(self._delete_likes_tx, user_id, genre_id)

    @staticmethod
    def _delete_likes_tx(tx, user_id: str, genre_id: str):
        query = """
        MATCH (u:User {user_id: $user_id})-[r:LIKES]->(g:Genre {genre_id: $genre_id})
        DELETE r
        """
        tx.run(query, user_id=user_id, genre_id=genre_id)