import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controller.belongstomovie_relation_controller import BelongsToMovieRelationController
from view.rating import Rating
from view.movie import Movie
from view.relations.belongstomovie import BelongsToMovieRelation

class TestBelongsToMovieRelationController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.controller = BelongsToMovieRelationController()

        #Crear nodos Rating y Movie
        cls.rating = Rating("rating_movie_001", 4, "Good movie", "Satisfied", True)
        cls.movie = Movie("movie_001", "Inception", 9.0, "Sci-fi thriller", True)

        with cls.controller.driver.session() as session:
            #Merge Rating
            session.run("""
                MERGE (r:Rating {node_id: $rid})
                SET r.rating = $rating,
                    r.comment = $comment,
                    r.final_feeling = $final_feeling,
                    r.recommend = $recommend
            """, 
            rid=cls.rating.node_id,
            rating=cls.rating.rating,
            comment=cls.rating.comment,
            final_feeling=cls.rating.final_feeling,
            recommend=cls.rating.recommend
            )

            #Merge Movie
            session.run("""
                MERGE (m:Movie {node_id: $mid})
                SET m.title = $title,
                    m.score = $score,
                    m.description = $description,
                    m.released = $released
            """,
            mid=cls.movie.node_id,
            title=cls.movie.title,
            score=cls.movie.score,
            description=cls.movie.description,
            released=cls.movie.released
            )

    def test_create_and_get_belongs_to_movie(self):
        relation = BelongsToMovieRelation(
            start_node=self.rating,
            end_node=self.movie,
            relevance=0.85,
            rating_context="Watched in theater",
            first_impression=True
        )
        self.controller.create_belongs_to_movie(relation)

        #Verificar que exista
        results = self.controller.get_belongs_to_movie_by_rating(self.rating.node_id)
        self.assertTrue(any(r["movie_id"] == self.movie.node_id for r in results))

    def test_update_belongs_to_movie(self):
        #Actualizar la relación
        self.controller.update_belongs_to_movie(
            rating_id=self.rating.node_id,
            movie_id=self.movie.node_id,
            relevance=0.95,
            rating_context="Rewatched at home"
        )

        #Verificar cambios
        results = self.controller.get_belongs_to_movie_by_rating(self.rating.node_id)
        rel = next((r for r in results if r["movie_id"] == self.movie.node_id), None)
        self.assertIsNotNone(rel)
        self.assertEqual(rel["relevance"], 0.95)
        self.assertEqual(rel["rating_context"], "Rewatched at home")

    def test_delete_belongs_to_movie(self):
        #Eliminar la relación
        self.controller.delete_belongs_to_movie(self.rating.node_id, self.movie.node_id)
        results = self.controller.get_belongs_to_movie_by_rating(self.rating.node_id)
        self.assertFalse(any(r["movie_id"] == self.movie.node_id for r in results))

    @classmethod
    def tearDownClass(cls):
        with cls.controller.driver.session() as session:
            session.run("MATCH (r:Rating {node_id: $rid}) DETACH DELETE r", rid=cls.rating.node_id)
            session.run("MATCH (m:Movie {node_id: $mid}) DETACH DELETE m", mid=cls.movie.node_id)
        cls.controller.close()

if __name__ == "__main__":
    unittest.main()
