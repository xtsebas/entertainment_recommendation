import unittest
import os
import sys
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controller.rated_relation_controller import RatedRelationController
from view.user import User
from view.rating import Rating
from view.relations.rated import RatedRelation

class TestRatedRelationController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.controller = RatedRelationController()

        #Crear nodos User y Rating 
        cls.user = User(node_id="user_rated_001", name="Alice", age=30, preferences=[], total_ratings=10)
        cls.rating = Rating(node_id="rating_001", rating=5, comment="Excellent", final_feeling="Happy", recommend=True)

        with cls.controller.driver.session() as session:
            #Merge User
            session.run("""
                MERGE (u:User {node_id: $node_id})
                SET u.name = $name, u.age = $age
            """, node_id=cls.user.node_id, name=cls.user.name, age=cls.user.age)

            #Merge Rating
            session.run("""
                MERGE (r:Rating {node_id: $node_id})
                SET r.rating = $rating,
                    r.comment = $comment,
                    r.final_feeling = $final_feeling,
                    r.recommend = $recommend
            """, 
            node_id=cls.rating.node_id,
            rating=cls.rating.rating,
            comment=cls.rating.comment,
            final_feeling=cls.rating.final_feeling,
            recommend=cls.rating.recommend
            )

    def test_create_and_get_rated_relation(self):
        #Crear la relación RATED
        relation = RatedRelation(
            start_node=self.user,
            end_node=self.rating,
            rating_date=str(date.today()),
            recommendation_level=10,
            rating_change_count=2
        )
        self.controller.create_rated_relation(relation)

        #Verificar que exista
        results = self.controller.get_rated_by_user(self.user.node_id)
        self.assertTrue(any(r["rating_id"] == self.rating.node_id for r in results))

    def test_update_rated_relation(self):
        #Actualizar la relación RATED 
        self.controller.update_rated_relation(
            user_id=self.user.node_id,
            rating_id=self.rating.node_id,
            recommendation_level=8,
            rating_change_count=3
        )

        #Verificar cambios
        results = self.controller.get_rated_by_user(self.user.node_id)
        updated_rel = next((r for r in results if r["rating_id"] == self.rating.node_id), None)
        self.assertIsNotNone(updated_rel)
        self.assertEqual(updated_rel["recommendation_level"], 8)
        self.assertEqual(updated_rel["rating_change_count"], 3)

    def test_delete_rated_relation(self):
        #Eliminar la relación RATED
        self.controller.delete_rated_relation(self.user.node_id, self.rating.node_id)
        results = self.controller.get_rated_by_user(self.user.node_id)
        self.assertFalse(any(r["rating_id"] == self.rating.node_id for r in results))

    @classmethod
    def tearDownClass(cls):
        #Limpia nodos creados
        with cls.controller.driver.session() as session:
            session.run("MATCH (u:User {node_id: $uid}) DETACH DELETE u", uid=cls.user.node_id)
            session.run("MATCH (r:Rating {node_id: $rid}) DETACH DELETE r", rid=cls.rating.node_id)
        cls.controller.close()

if __name__ == "__main__":
    unittest.main()
