from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import sys
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
        MATCH (u:User {node_id: $user_id})-[r:DISLIKES]->(g:Genre)
        RETURN g.node_id AS genre_id, g.name AS genre_name, r.rejection_level AS rejection_level, 
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