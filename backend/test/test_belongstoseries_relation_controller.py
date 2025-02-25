# test/test_belongs_to_series_relation_controller.py

import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controller.belongstoseries_relation_controller import BelongsToSeriesRelationController
from view.rating import Rating
from backend.view.serie import Series
from view.relations.belongstoseries import BelongsToSeriesRelation

class TestBelongsToSeriesRelationController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.controller = BelongsToSeriesRelationController()

        #Crear nodos Rating y Series
        cls.rating = Rating("rating_series_001", 3, "Decent show", "Neutral", False)
        cls.series = Series("series_001", "Stranger Things", 8.5, "Sci-fi drama", True)

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

            #Merge Series
            session.run("""
                MERGE (s:Series {node_id: $sid})
                SET s.title = $title,
                    s.score = $score,
                    s.description = $description,
                    s.on_air = $on_air
            """,
            sid=cls.series.node_id,
            title=cls.series.title,
            score=cls.series.score,
            description=cls.series.description,
            on_air=cls.series.on_air
            )

    def test_create_and_get_belongs_to_series(self):
        relation = BelongsToSeriesRelation(
            start_node=self.rating,
            end_node=self.series,
            relevance=0.75,
            rating_context="Watched season 1",
            seasons_watched=1
        )
        self.controller.create_belongs_to_series(relation)

        #Verificar que exista
        results = self.controller.get_belongs_to_series_by_rating(self.rating.node_id)
        self.assertTrue(any(r["series_id"] == self.series.node_id for r in results))

    def test_update_belongs_to_series(self):
        #Actualizar la relación
        self.controller.update_belongs_to_series(
            rating_id=self.rating.node_id,
            series_id=self.series.node_id,
            relevance=0.9,
            seasons_watched=2
        )

        #Verificar cambios
        results = self.controller.get_belongs_to_series_by_rating(self.rating.node_id)
        rel = next((r for r in results if r["series_id"] == self.series.node_id), None)
        self.assertIsNotNone(rel)
        self.assertEqual(rel["relevance"], 0.9)
        self.assertEqual(rel["seasons_watched"], 2)

    def test_delete_belongs_to_series(self):
        #Eliminar la relación
        self.controller.delete_belongs_to_series(self.rating.node_id, self.series.node_id)
        results = self.controller.get_belongs_to_series_by_rating(self.rating.node_id)
        self.assertFalse(any(r["series_id"] == self.series.node_id for r in results))

    @classmethod
    def tearDownClass(cls):
        with cls.controller.driver.session() as session:
            session.run("MATCH (r:Rating {node_id: $rid}) DETACH DELETE r", rid=cls.rating.node_id)
            session.run("MATCH (s:Series {node_id: $sid}) DETACH DELETE s", sid=cls.series.node_id)
        cls.controller.close()

if __name__ == "__main__":
    unittest.main()
