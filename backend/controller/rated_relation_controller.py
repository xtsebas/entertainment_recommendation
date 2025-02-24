from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from view.relations.rated import RatedRelation
load_dotenv()

class RatedRelationController:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        self.driver.close()

    # Create relacion rated
    def create_rated_relation(self, relation: RatedRelation):
        with self.driver.session() as session:
            session.execute_write(self._create_rated_tx, relation)

    @staticmethod
    def _create_rated_tx(tx, relation: RatedRelation):
        query = """
        MATCH (u:User {node_id: $user_id}), (ra:Rating {node_id: $rating_id})
        MERGE (u)-[r:RATED]->(ra)
        SET r.rating_date = date($rating_date),
            r.recommendation_level = $recommendation_level,
            r.rating_change_count = $rating_change_count
        RETURN r
        """
        tx.run(
            query,
            user_id=relation.start_node.node_id,
            rating_id=relation.end_node.node_id,
            rating_date=relation.properties["rating_date"],
            recommendation_level=relation.properties["recommendation_level"],
            rating_change_count=relation.properties["rating_change_count"]
        )

    
    def get_rated_by_user(self, user_id: str):
        #Retorna una lista de relaciones RATED que parten de un usuario dado.
        with self.driver.session() as session:
            return session.execute_read(self._get_rated_by_user_tx, user_id)

    @staticmethod
    def _get_rated_by_user_tx(tx, user_id: str):
        query = """
        MATCH (u:User {node_id: $user_id})-[r:RATED]->(ra:Rating)
        RETURN ra.node_id AS rating_id,
               r.rating_date AS rating_date,
               r.recommendation_level AS recommendation_level,
               r.rating_change_count AS rating_change_count
        """
        result = tx.run(query, user_id=user_id)
        return [record.data() for record in result]

    def update_rated_relation(self, user_id: str, rating_id: str, **new_props):
        #Actualiza las propiedades de la relación RATED.
        with self.driver.session() as session:
            session.execute_write(self._update_rated_tx, user_id, rating_id, new_props)

    @staticmethod
    def _update_rated_tx(tx, user_id, rating_id, new_props):
        set_clauses = []
        params = {"user_id": user_id, "rating_id": rating_id}
        for key, value in new_props.items():
            set_clauses.append(f"r.{key} = ${key}")
            params[key] = value
        if not set_clauses:
            return  
        query = f"""
        MATCH (u:User {{node_id: $user_id}})-[r:RATED]->(ra:Rating {{node_id: $rating_id}})
        SET {", ".join(set_clauses)}
        RETURN r
        """
        tx.run(query, **params)


    def delete_rated_relation(self, user_id: str, rating_id: str):
        #Elimina la relación RATED (User -> Rating).
        with self.driver.session() as session:
            session.execute_write(self._delete_rated_tx, user_id, rating_id)

    @staticmethod
    def _delete_rated_tx(tx, user_id, rating_id):
        query = """
        MATCH (u:User {node_id: $user_id})-[r:RATED]->(ra:Rating {node_id: $rating_id})
        DELETE r
        """
        tx.run(query, user_id=user_id, rating_id=rating_id)
