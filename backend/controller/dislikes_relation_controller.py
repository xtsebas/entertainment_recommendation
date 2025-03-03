from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import sys
import random
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from view.relations.dislikes import DislikesRelation

load_dotenv()

class DislikesRelationController:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        """Cierra la conexión con Neo4j."""
        self.driver.close()

    # Crear relación DISLIKE
    def create_dislikes_relation(self, relation: DislikesRelation):
        with self.driver.session() as session:
            session.execute_write(self._create_dislikes_tx, relation)

    @staticmethod
    def _create_dislikes_tx(tx, relation: DislikesRelation):
        query = """
        MATCH (u:User {node_id: $user_id}), (g:Genre {node_id: $genre_id})
        MERGE (u)-[r:DISLIKES]->(g)
        SET r.rejection_level = $rejection_level,
            r.aggregation_date = date($aggregation_date),
            r.last_engagement = date($last_engagement)
        RETURN r
        """
        tx.run(
            query,
            user_id=relation.start_node.node_id,
            genre_id=relation.end_node.node_id,
            rejection_level=relation.properties['rejection_level'],
            aggregation_date=relation.properties['aggregation_date'],
            last_engagement=relation.properties['last_engagement']
        )

    # Obtener todas las relaciones DISLIKE de un usuario
    def get_dislikes_by_user(self, user_id: str):
        with self.driver.session() as session:
            return session.execute_read(self._get_dislikes_by_user_tx, user_id)

    @staticmethod
    def _get_dislikes_by_user_tx(tx, user_id: str):
        query = """
        MATCH (u:User {user_id: $user_id})-[r:DISLIKES]->(g:Genre)
        RETURN g.genre_id AS genre_id, g.name AS genre_name, r.rejection_level AS rejection_level, 
               r.aggregation_date AS aggregation_date, r.last_engagement AS last_engagement
        """
        result = tx.run(query, user_id=user_id)
        return [record.data() for record in result]

    # Eliminar una relación DISLIKE
    def delete_dislikes_relation(self, user_id: str, genre_id: str):
        with self.driver.session() as session:
            session.execute_write(self._delete_dislikes_tx, user_id, genre_id)

    @staticmethod
    def _delete_dislikes_tx(tx, user_id: str, genre_id: str):
        query = """
        MATCH (u:User {node_id: $user_id})-[r:DISLIKES]->(g:Genre {node_id: $genre_id})
        DELETE r
        """
        tx.run(query, user_id=user_id, genre_id=genre_id)
    
    def dislike_genre_by_user(self, user_id: str, genre_id: str):
        """
        Removes the LIKES relationship (if it exists) and creates a DISLIKES relationship with random properties.
        """
        # Generate random properties
        rejection_level = random.randint(1, 10)
        aggregation_date = self._generate_random_date(730)  # Last 2 years
        last_engagement = self._generate_random_date(180)  # Last 6 months

        with self.driver.session() as session:
            session.execute_write(
                self._dislike_genre_tx, user_id, genre_id, rejection_level, aggregation_date, last_engagement
            )

    @staticmethod
    def _dislike_genre_tx(tx, user_id: str, genre_id: str, rejection_level: int, aggregation_date: str, last_engagement: str):
        query = """
        MATCH (u:User {user_id: $user_id})
        MATCH (g:Genre {genre_id: $genre_id})
        
        OPTIONAL MATCH (u)-[r:LIKES]->(g)
        DELETE r

        MERGE (u)-[d:DISLIKES]->(g)
        SET d.rejection_level = $rejection_level,
            d.aggregation_date = $aggregation_date,
            d.last_engagement = $last_engagement
        RETURN d
        """
        tx.run(
            query,
            user_id=user_id,
            genre_id=genre_id,
            rejection_level=rejection_level,
            aggregation_date=aggregation_date,
            last_engagement=last_engagement
        )

    @staticmethod
    def _generate_random_date(days_back: int) -> str:
        """Generates a random date within the last 'days_back' days."""
        random_days = random.randint(0, days_back)
        random_date = datetime.now() - timedelta(days=random_days)
        return random_date.strftime("%Y-%m-%d")  # Format YYYY-MM-DD