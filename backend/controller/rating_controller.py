from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from view.rating import Rating
load_dotenv()

class RatingController:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        self.driver.close()

    # Create Rating
    def create_rating(self, rating: Rating):
        #Crea un nuevo Rating en la base de datos.
        with self.driver.session() as session:
            session.execute_write(self._create_rating_tx, rating)
            self.update_rating_stats(rating.node_id)

    @staticmethod
    def _create_rating_tx(tx, rating: Rating):
        #MERGE de un nodo Rating.
        query = """
        MERGE (r:Rating {node_id: $node_id})
        SET r.rating = $rating,
            r.comment = $comment,
            r.final_feeling = $final_feeling,
            r.recommend = $recommend,
            r.is_good = false  // Propiedad auxiliar que luego recalculamos
        """
        tx.run(
            query,
            node_id=rating.node_id,
            rating=rating.rating,
            comment=rating.comment,
            final_feeling=rating.final_feeling,
            recommend=rating.recommend
        )

    def get_rating(self, rating_id: str):
        #Obtiene un Rating por su ID
        #Retorna un registro con las propiedades o None si no existe.
        with self.driver.session() as session:
            result = session.execute_read(self._get_rating_tx, rating_id)
            return result

    @staticmethod
    def _get_rating_tx(tx, rating_id: str):
        query = """
        MATCH (r:Rating {node_id: $rating_id})
        RETURN r.node_id AS id,
               r.rating AS rating,
               r.comment AS comment,
               r.final_feeling AS final_feeling,
               r.recommend AS recommend,
               r.is_good AS is_good
        """
        result = tx.run(query, rating_id=rating_id)
        return result.single()

    def get_all_ratings(self):
        #Obtiene todos los Ratings en la base de datos.
        #Retorna una lista de registros.
        with self.driver.session() as session:
            results = session.execute_read(self._get_all_ratings_tx)
            return list(results)

    @staticmethod
    def _get_all_ratings_tx(tx):
        query = """
        MATCH (r:Rating)
        RETURN r.node_id AS id,
               r.rating AS rating,
               r.comment AS comment,
               r.final_feeling AS final_feeling,
               r.recommend AS recommend,
               r.is_good AS is_good
        ORDER BY r.node_id
        """
        return tx.run(query)

    def update_rating(self, rating: Rating):
        #Actualiza la información de un Rating existente.
        #Después de actualizarlo, recalcula las estadísticas.
        with self.driver.session() as session:
            session.execute_write(self._update_rating_tx, rating)
            self.update_rating_stats(rating.node_id)

    @staticmethod
    def _update_rating_tx(tx, rating: Rating):
        query = """
        MATCH (r:Rating {node_id: $node_id})
        SET r.rating = $rating,
            r.comment = $comment,
            r.final_feeling = $final_feeling,
            r.recommend = $recommend
        """
        tx.run(
            query,
            node_id=rating.node_id,
            rating=rating.rating,
            comment=rating.comment,
            final_feeling=rating.final_feeling,
            recommend=rating.recommend
        )

    def delete_rating(self, rating_id: str):
        #Elimina un nodo Rating de la base de datos por su id.
        with self.driver.session() as session:
            session.execute_write(self._delete_rating_tx, rating_id)

    @staticmethod
    def _delete_rating_tx(tx, rating_id: str):
        query = """
        MATCH (r:Rating {node_id: $rating_id})
        DETACH DELETE r
        """
        tx.run(query, rating_id=rating_id)

    def update_rating_stats(self, rating_id: str):
        with self.driver.session() as session:
            rating_data = session.execute_read(self._get_rating_value, rating_id)
            if rating_data is None:
                # Si el nodo no existe, no hacemos nada
                return

            rating_val = rating_data["rating"]
            is_good = rating_val >= 4

            session.execute_write(self._set_is_good, rating_id, is_good)

    @staticmethod
    def _get_rating_value(tx, rating_id: str):
        query = """
        MATCH (r:Rating {node_id: $rating_id})
        RETURN r.rating AS rating
        """
        result = tx.run(query, rating_id=rating_id)
        return result.single()

    @staticmethod
    def _set_is_good(tx, rating_id: str, is_good: bool):
        query = """
        MATCH (r:Rating {node_id: $rating_id})
        SET r.is_good = $is_good
        """
        tx.run(query, rating_id=rating_id, is_good=is_good)
