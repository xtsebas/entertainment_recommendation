from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import random
from datetime import datetime, timedelta
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
        MATCH (r:Rating {rating_id: $rating_id})
        RETURN r.rating_id AS rating_id,
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
    
    #Get Rating
    def get_ratings_user(self, user_id: str):
        #Obtiene todos los Ratings en la base de datos.
        #Retorna una lista de registros.
        with self.driver.session() as session:
            results = session.execute_read(self._get_ratings_user_tx, user_id)
            return results

    @staticmethod
    def _get_ratings_user_tx(tx, user_id: str):
        query = """
            MATCH (u:User {user_id: $user_id})-[rr:RATED]->(r:Rating)
            MATCH (r)-[b:BELONGS_TO]->(m:Media)
            MATCH (t)-[:IS_A]->(m)
            RETURN 
            rr.recommendation_level As Recomendation,
            rr.rating_date as Date,
            r.rating_id as rating_id,
            r.rating as Rating,
            r.comment as Comment,
            t.title as Title;

        """
        result =  tx.run(
            query,
            user_id=user_id
        )   
        return [record.data() for record in result]

    def update_rating(self, rating_data: dict):
        """
        Actualiza los datos de un Rating en la base de datos.
        """
        rating_id = rating_data.get("rating_id")
        user_id= rating_data.get("user_id")
        rating = rating_data.get("rating")
        comment = rating_data.get("comment")
        final_feeling = rating_data.get("final_feeling")
        recommend = rating_data.get("recommend")

        if not rating_id:
            return {"message": "Error: Se requiere un ID de rating para actualizar."}

        with self.driver.session() as session:
            result = session.execute_write(
                self._update_rating_tx,
                rating_id,
                user_id,
                rating,
                comment,
                final_feeling,
                recommend
            )
        
        return result

    @staticmethod
    def _update_rating_tx(tx, rating_id: str, user_id: str, rating: int, comment: str, final_feeling: str, recommend: bool):
        query_parts = []
        params = {"rating_id": rating_id}

        if rating_id is not None:
            query_parts.append("r.rating_id = $rating_id")
            params["rating_id"] = rating_id
        if user_id is not None:
            query_parts.append("u.user_id = $user_id")
            params["user_id"] = user_id
        if rating is not None:
            query_parts.append("r.rating = $rating")
            params["rating"] = rating
        if comment is not None:
            query_parts.append("r.comment = $comment")
            params["comment"] = comment
        if final_feeling is not None:
            query_parts.append("r.final_feeling = $final_feeling")
            params["final_feeling"] = final_feeling
        if recommend is not None:
            query_parts.append("r.recommend = $recommend")
            params["recommend"] = recommend

        if not query_parts:
            return {"message": "No se han proporcionado datos para actualizar."}

        query = f"""
        MATCH (r:Rating {{rating_id: $rating_id}})<-[rel:RATED]-(u:User {{user_id: $user_id}})
        SET {", ".join(query_parts)},
            rel.rating_change_count = COALESCE(rel.rating_change_count, 0) + 1
        RETURN r.rating_id AS rating_id, r.rating AS rating, 
            r.comment AS comment, r.final_feeling AS final_feeling, 
            r.recommend AS recommend,
            rel.rating_change_count AS rating_change_count
        """

        result = tx.run(query, **params)
        return result.single()

    def delete_rating(self, rating_id: str):
        #Elimina un nodo Rating de la base de datos por su id.
        with self.driver.session() as session:
            session.execute_write(self._delete_rating_tx, rating_id)

    @staticmethod
    def _delete_rating_tx(tx, rating_id: str):
        query = """
        MATCH (r:Rating {rating_id: $rating_id})
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
    
    # def rate_movie(self, user_id: str, media_id: str, rating: Rating):
    #     pass
    
    # def rate_serie(self, user_id: str, media_id: str, rating: Rating):
    #     pass
    
    def rate_movie(self, user_id: str, media_id: str, rating: Rating):
        """
        Creates a Rating node and links it with a User and Media (Movie) using relations with properties.
        Ensures the Media node is correctly related to Movie via IS_A.
        """
        # Generate random properties
        rating_date = self._generate_random_date()
        recommendation_level = rating.rating  # Same as rating
        rating_change_count = 0

        relevance = round(random.uniform(0.5, 1.0), 2)
        rating_context = random.choice(["Casual Watch", "Cinephile Review", "Critic Opinion", "First Time View", "Rewatch"])
        first_impression = random.choice([True, False])

        with self.driver.session() as session:
            session.execute_write(
                self._rate_movie_tx, user_id, media_id, rating, rating_date, recommendation_level, rating_change_count,
                relevance, rating_context, first_impression
            )

    @staticmethod
    def _rate_movie_tx(tx, user_id, media_id, rating, rating_date, recommendation_level, rating_change_count,
                       relevance, rating_context, first_impression):
        query = """
        MATCH (u:User {user_id: $user_id}), (m:Media {media_id: $media_id})-[:IS_A]->(mov:Movie)
        CREATE (r:Rating {
            rating_id: $rating_id,
            rating: $rating,
            recommend: $recommend,
            final_feeling: $final_feeling,
            comment: $comment
        })
        CREATE (u)-[rated:RATED {
            rating_date: $rating_date,
            recommendation_level: $recommendation_level,
            rating_change_count: $rating_change_count
        }]->(r)
        CREATE (r)-[bt:BELONGS_TO {
            relevance: $relevance,
            rating_context: $rating_context,
            first_impression: $first_impression
        }]->(mov)
        RETURN u, rated, r, bt, mov
        """
        tx.run(query, 
               user_id=user_id, media_id=media_id,
               rating_id=rating.rating_id, rating=rating.rating, recommend=rating.recommend,
               final_feeling=rating.final_feeling, comment=rating.comment,
               rating_date=rating_date, recommendation_level=recommendation_level,
               rating_change_count=rating_change_count,
               relevance=relevance, rating_context=rating_context,
               first_impression=first_impression)

    def rate_serie(self, user_id: str, media_id: str, rating: Rating):
        """
        Creates a Rating node and links it with a User and Media (Serie) using relations with properties.
        Ensures the Media node is correctly related to Serie via IS_A.
        """
        # Generate random properties
        rating_date = self._generate_random_date()
        recommendation_level = rating.rating  # Same as rating
        rating_change_count = random.randint(0, 3)

        relevance = round(random.uniform(0.5, 1.0), 2)
        rating_context = random.choice(["Casual Watch", "Binge Watch", "Critical Review", "First Time Watch", "Rewatch"])
        seasons_watched = random.randint(1, 5)  # Assuming a max of 5 seasons watched

        with self.driver.session() as session:
            session.execute_write(
                self._rate_serie_tx, user_id, media_id, rating, rating_date, recommendation_level, rating_change_count,
                relevance, rating_context, seasons_watched
            )

    @staticmethod
    def _rate_serie_tx(tx, user_id, media_id, rating, rating_date, recommendation_level, rating_change_count,
                       relevance, rating_context, seasons_watched):
        query = """
        MATCH (u:User {user_id: $user_id}), (m:Media {media_id: $media_id})-[:IS_A]->(se:Serie)
        CREATE (r:Rating {
            rating_id: $rating_id,
            rating: $rating,
            recommend: $recommend,
            final_feeling: $final_feeling,
            comment: $comment
        })
        CREATE (u)-[rated:RATED {
            rating_date: $rating_date,
            recommendation_level: $recommendation_level,
            rating_change_count: $rating_change_count
        }]->(r)
        CREATE (r)-[bt:BELONGS_TO {
            relevance: $relevance,
            rating_context: $rating_context,
            seasons_watched: $seasons_watched
        }]->(se)
        RETURN u, rated, r, bt, se
        """
        tx.run(query, 
               user_id=user_id, media_id=media_id,
               rating_id=rating.rating_id, rating=rating.rating, recommend=rating.recommend,
               final_feeling=rating.final_feeling, comment=rating.comment,
               rating_date=rating_date, recommendation_level=recommendation_level,
               rating_change_count=rating_change_count,
               relevance=relevance, rating_context=rating_context,
               seasons_watched=seasons_watched)

    @staticmethod
    def _generate_random_date():
        """Generates a random date within the last 2 years."""
        days_ago = random.randint(0, 730)
        random_date = datetime.now() - timedelta(days=days_ago)
        return random_date.strftime("%Y-%m-%d")