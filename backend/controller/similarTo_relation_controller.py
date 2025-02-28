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

    # Crear relación SIMILAR_TO basada en Jaccard
    def create_similar_to_jaccard(self, user_id: str):
        with self.driver.session() as session:
            session.execute_write(self._create_similar_to_jaccard_tx, user_id)

    @staticmethod
    def _create_similar_to_jaccard_tx(tx, user_id: str):
        query = """
        MATCH (u1:User {user_id: $user_id})-[:LIKES]->(g:Genre)<-[:LIKES]-(u2:User)
        WHERE u1 <> u2  
        WITH u1, u2, collect(g.name) AS shared_genres, count(g) AS intersection

        MATCH (u1)-[:LIKES]->(g1:Genre)
        MATCH (u2)-[:LIKES]->(g2:Genre)
        WITH u1, u2, shared_genres, intersection,
             collect(DISTINCT g1.name) + collect(DISTINCT g2.name) AS union_genres

        WITH u1, u2, shared_genres, intersection, size(apoc.coll.toSet(union_genres)) AS union_size

        WITH u1, u2, shared_genres, intersection, union_size,
             (toFloat(intersection) / union_size) AS similarity_score

        MERGE (u1)-[s:SIMILAR_TO]->(u2)
        ON CREATE SET 
            s.score = similarity_score,
            s.date = datetime(),
            s.preferences = shared_genres
        RETURN u1.name AS user1, u2.name AS user2, s.score AS similarity, s.preferences AS shared_genres
        """
        tx.run(query, user_id=user_id)

    # Obtener usuarios similares con puntajes cercanos a 1
    def get_similar_users(self, user_id: str):
        with self.driver.session() as session:
            return session.execute_read(self._get_similar_users_tx, user_id)

    @staticmethod
    def _get_similar_users_tx(tx, user_id: str):
        query = """
        MATCH (u:User {user_id: $user_id})-[r:SIMILAR_TO]->(u2:User)
        WHERE r.score >= 0.8  
        RETURN u2.user_id AS similar_user_id, u2.name AS similar_user_name, 
               r.score AS score, r.date AS score_date, r.preferences AS shared_genres
        ORDER BY r.score DESC
        """
        result = tx.run(query, user_id=user_id)
        return [record.data() for record in result]