from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import sys
from typing import List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from view.relations.similar_to import SimilarToRelation

load_dotenv()

class SimilarToRelationController:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        """Cierra la conexión con Neo4j."""
        self.driver.close()

    # Crear relación SIMILAR_TO
    def create_similar_to_relation(self, relation: SimilarToRelation):
        with self.driver.session() as session:
            session.execute_write(self._create_similar_to_tx, relation)

    @staticmethod
    def _create_similar_to_tx(tx, relation: SimilarToRelation):
        query = """
        MATCH (u1:User {node_id: $user1_id}), (u2:User {node_id: $user2_id})
        MERGE (u1)-[r:SIMILAR_TO]->(u2)
        SET r.score = $score,
            r.score_date = date($score_date),
            r.preference = $preference
        RETURN r
        """
        tx.run(
            query,
            user1_id=relation.start_node.node_id,
            user2_id=relation.end_node.node_id,
            score=relation.properties['score'],
            score_date=relation.properties['score_date'],
            preference=relation.properties['preference']
        )

    # Obtener todas las relaciones SIMILAR_TO de un usuario
    def get_similar_to_by_user(self, user_id: str):
        with self.driver.session() as session:
            return session.execute_read(self._get_similar_to_by_user_tx, user_id)

    @staticmethod
    def _get_similar_to_by_user_tx(tx, user_id: str):
        query = """
        MATCH (u:User {node_id: $user_id})-[r:SIMILAR_TO]->(u2:User)
        RETURN u2.node_id AS similar_user_id, u2.name AS similar_user_name, 
               r.score AS score, r.score_date AS score_date, r.preference AS preference
        """
        result = tx.run(query, user_id=user_id)
        return [record.data() for record in result]

    # Eliminar una relación SIMILAR_TO entre dos usuarios
    def delete_similar_to_relation(self, user1_id: str, user2_id: str):
        with self.driver.session() as session:
            session.execute_write(self._delete_similar_to_tx, user1_id, user2_id)

    @staticmethod
    def _delete_similar_to_tx(tx, user1_id: str, user2_id: str):
        query = """
        MATCH (u1:User {node_id: $user1_id})-[r:SIMILAR_TO]->(u2:User {node_id: $user2_id})
        DELETE r
        """
        tx.run(query, user1_id=user1_id, user2_id=user2_id)

    # Actualizar SCORE basándose en los géneros similares
    def update_similar_to_score(self, user1_id: str, user2_id: str):
        with self.driver.session() as session:
            session.execute_write(self._update_similar_to_score_tx, user1_id, user2_id)

    @staticmethod
    def _update_similar_to_score_tx(tx, user1_id: str, user2_id: str):
        query = """
        MATCH (u1:User {node_id: $user1_id})-[r1:LIKES|DISLIKES]->(g:Genre)
        MATCH (u2:User {node_id: $user2_id})-[r2:LIKES|DISLIKES]->(g)
        WITH COUNT(g) AS sharedGenres
        MATCH (u1)-[r:SIMILAR_TO]->(u2)
        SET r.score = sharedGenres / 10.0  # Normalizamos en base a 10 géneros comunes
        RETURN r.score
        """
        tx.run(query, user1_id=user1_id, user2_id=user2_id)

    # Actualizar PREFERENCES con los géneros comunes que ambos dieron LIKE
    def update_similar_to_preferences(self, user1_id: str, user2_id: str):
        with self.driver.session() as session:
            session.execute_write(self._update_similar_to_preferences_tx, user1_id, user2_id)

    @staticmethod
    def _update_similar_to_preferences_tx(tx, user1_id: str, user2_id: str):
        query = """
        MATCH (u1:User {node_id: $user1_id})-[r1:LIKES]->(g:Genre)
        MATCH (u2:User {node_id: $user2_id})-[r2:LIKES]->(g)
        WITH COLLECT(g.name) AS commonGenres
        MATCH (u1)-[r:SIMILAR_TO]->(u2)
        SET r.preference = commonGenres
        RETURN r.preference
        """
        tx.run(query, user1_id=user1_id, user2_id=user2_id)
