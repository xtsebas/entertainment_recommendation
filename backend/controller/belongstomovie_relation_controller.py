from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from view.relations.belongstomovie import BelongsToMovieRelation

load_dotenv()

class BelongsToMovieRelationController:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        self.driver.close()

    #Create relation belong to movie
    def create_belongs_to_movie(self, relation: BelongsToMovieRelation):
        with self.driver.session() as session:
            session.execute_write(self._create_belongs_to_movie_tx, relation)

    @staticmethod
    def _create_belongs_to_movie_tx(tx, relation: BelongsToMovieRelation):
        query = """
        MATCH (ra:Rating {node_id: $rating_id}), (m:Movie {node_id: $movie_id})
        MERGE (ra)-[r:BELONGS_TO]->(m)
        SET r.relevance = $relevance,
            r.rating_context = $rating_context,
            r.first_impression = $first_impression
        RETURN r
        """
        tx.run(
            query,
            rating_id=relation.start_node.node_id,
            movie_id=relation.end_node.node_id,
            relevance=relation.properties["relevance"],
            rating_context=relation.properties["rating_context"],
            first_impression=relation.properties["first_impression"]
        )

    def get_belongs_to_movie_by_rating(self, rating_id: str):
        #Obtiene las relaciones BELONGS_TO (Rating->Movie) de un Rating específico.
        with self.driver.session() as session:
            return session.execute_read(self._get_belongs_to_movie_tx, rating_id)

    @staticmethod
    def _get_belongs_to_movie_tx(tx, rating_id: str):
        query = """
        MATCH (ra:Rating {node_id: $rating_id})-[r:BELONGS_TO]->(m:Movie)
        RETURN m.node_id AS movie_id,
               r.relevance AS relevance,
               r.rating_context AS rating_context,
               r.first_impression AS first_impression
        """
        result = tx.run(query, rating_id=rating_id)
        return [record.data() for record in result]

    def update_belongs_to_movie(self, rating_id: str, movie_id: str, **new_props):
        #Actualiza las propiedades de la relación BELONGS_TO (Rating->Movie).
        with self.driver.session() as session:
            session.execute_write(self._update_belongs_to_movie_tx, rating_id, movie_id, new_props)

    @staticmethod
    def _update_belongs_to_movie_tx(tx, rating_id, movie_id, new_props):
        set_clauses = []
        params = {"rating_id": rating_id, "movie_id": movie_id}

        for key, value in new_props.items():
            set_clauses.append(f"r.{key} = ${key}")
            params[key] = value

        if not set_clauses:
            return

        query = f"""
        MATCH (ra:Rating {{node_id: $rating_id}})-[r:BELONGS_TO]->(m:Movie {{node_id: $movie_id}})
        SET {", ".join(set_clauses)}
        RETURN r
        """
        tx.run(query, **params)

    def delete_belongs_to_movie(self, rating_id: str, movie_id: str):
        #Elimina la relación BELONGS_TO (Rating->Movie).
        with self.driver.session() as session:
            session.execute_write(self._delete_belongs_to_movie_tx, rating_id, movie_id)

    @staticmethod
    def _delete_belongs_to_movie_tx(tx, rating_id, movie_id):
        query = """
        MATCH (ra:Rating {node_id: $rating_id})-[r:BELONGS_TO]->(m:Movie {node_id: $movie_id})
        DELETE r
        """
        tx.run(query, rating_id=rating_id, movie_id=movie_id)
