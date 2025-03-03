from neo4j import GraphDatabase
from dotenv import load_dotenv
from datetime import date
import os
import random
from datetime import datetime, timedelta
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

        
    # Obtener todas las relaciones LIKE de un usuario
    def get_likes_by_user(self, user_id: str):
        with self.driver.session() as session:
            return session.execute_read(self._get_likes_by_user_tx, user_id)

    @staticmethod
    def _get_likes_by_user_tx(tx, user_id: str):
        query = """
        MATCH (u:User {user_id: $user_id})-[r:LIKES]->(g:Genre)
        RETURN g.name AS genre_name, r.preference_level AS preference_level, 
               r.aggregation_date AS aggregation_date, r.last_engagement AS last_engagement, g.genre_id as genre_id
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
        MATCH (u:User {user_id: $user_id})-[r:LIKES]->(g:Genre {genre_id: $genre_id})
        DELETE r
        """
        tx.run(query, user_id=user_id, genre_id=genre_id)

    def get_unrated_genres(self, user_id: str):
        """
        Retrieves genres that the user has NOT liked or disliked.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._get_unrated_genres_tx, user_id)
        return result

    @staticmethod
    def _get_unrated_genres_tx(tx, user_id: str):
        query = """
        MATCH (g:Genre) 
        WHERE NOT EXISTS {
            MATCH (u:User {user_id: $user_id})-[r:LIKES|DISLIKES]->(g)
        }
        RETURN g.name AS genre
        """
        result = tx.run(query, user_id=user_id)
        return [record["genre"] for record in result]

    def create_likes_relation_2(self, user_id: str, genre_name: str):
        """
        Creates a LIKES relationship between a User and a Genre with random properties.
        """
        # Generate random properties
        preference_level = random.randint(1, 10)
        aggregation_date = self._generate_random_date(730)  # Last 2 years
        last_engagement = self._generate_random_date(180)  # Last 6 months

        with self.driver.session() as session:
            session.execute_write(
                self._create_likes_tx_2, user_id, genre_name, preference_level, aggregation_date, last_engagement
            )

    @staticmethod
    def _create_likes_tx_2(tx, user_id: str, genre_name: str, preference_level: int, aggregation_date: str, last_engagement: str):
        query = """
        MATCH (u:User {user_id: $user_id})
        MATCH (g:Genre {name: $genre_name}) 

        // Delete existing DISLIKES relationship (if it exists)
        OPTIONAL MATCH (u)-[d:DISLIKES]->(g)
        DELETE d

        // Create or update the LIKES relationship
        MERGE (u)-[r:LIKES]->(g)
        SET r.preference_level = $preference_level,
            r.aggregation_date = $aggregation_date,
            r.last_engagement = $last_engagement
        RETURN r

        """
        tx.run(
            query,
            user_id=user_id,
            genre_name=genre_name,
            preference_level=preference_level,
            aggregation_date=aggregation_date,
            last_engagement=last_engagement
        )
    
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

    @staticmethod
    def _generate_random_date(days_back: int) -> str:
        """Generates a random date within the last 'days_back' days."""
        random_days = random.randint(0, days_back)
        random_date = datetime.now() - timedelta(days=random_days)
        return random_date.strftime("%Y-%m-%d")  # Format YYYY-MM-DD