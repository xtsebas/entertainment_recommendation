import unittest
from datetime import datetime
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importaciones correctas
from controller.similarTo_relation_controller import SimilarToRelationController
from view.user import User
from view.relations.similar_to import SimilarToRelation

class TestSimilarToRelationController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Configuración inicial: Se ejecuta una vez antes de todas las pruebas. """
        cls.controller = SimilarToRelationController()

        # Crear usuarios antes de la prueba
        cls.user1 = User("user123", "John Doe", 25, ["Action", "Comedy"], 120)
        cls.user2 = User("user456", "Jane Doe", 30, ["Action", "Drama"], 130)

        # Insertar los usuarios en la BD
        with cls.controller.driver.session() as session:
            session.run(
                "MERGE (u:User {node_id: $user_id, name: $name, age: $age})",
                user_id=cls.user1.node_id, name=cls.user1.name, age=cls.user1.age
            )
            session.run(
                "MERGE (u:User {node_id: $user_id, name: $name, age: $age})",
                user_id=cls.user2.node_id, name=cls.user2.name, age=cls.user2.age
            )

        # Crear relación SIMILAR_TO antes de probarla
        cls.relation = SimilarToRelation(cls.user1, cls.user2, score=0, preference=[])
        cls.controller.create_similar_to_relation(cls.relation)

    @classmethod
    def tearDownClass(cls):
        """ Cierre de la conexión con Neo4j después de ejecutar todas las pruebas. """
        cls.controller.close()

    def test_create_similar_to_relation(self):
        """ Prueba la creación de la relación SIMILAR_TO """
        relations = self.controller.get_similar_to_by_user("user123")
        self.assertTrue(any(r["similar_user_id"] == "user456" for r in relations))

    def test_get_similar_to_by_user(self):
        """ Prueba la obtención de relaciones SIMILAR_TO de un usuario """
        relations = self.controller.get_similar_to_by_user("user123")
        self.assertGreaterEqual(len(relations), 1)
        self.assertIn("score", relations[0])
        self.assertIn("preference", relations[0])

    @unittest.skip("Depende de que hayan mas de un genero")
    def test_update_similar_to_score(self):
        """ Prueba la actualización del score de similitud """
        self.controller.update_similar_to_score("user123", "user456")
        relations = self.controller.get_similar_to_by_user("user123")
        self.assertGreaterEqual(relations[0]["score"], 0)

    @unittest.skip("Depende de que hayan mas de un genero")
    def test_update_similar_to_preferences(self):
        """ Prueba la actualización de las preferencias compartidas """
        self.controller.update_similar_to_preferences("user123", "user456")
        relations = self.controller.get_similar_to_by_user("user123")
        updated_preferences = relations[0]["preference"]
        self.assertIsInstance(updated_preferences, list)

    def test_delete_similar_to_relation(self):
        """ Prueba la eliminación de una relación SIMILAR_TO """
        self.controller.delete_similar_to_relation("user123", "user456")
        relations = self.controller.get_similar_to_by_user("user123")
        self.assertFalse(any(r["similar_user_id"] == "user456" for r in relations))

    @classmethod
    def tearDownClass(cls):
        """Limpia los datos creados en la base de datos después de las pruebas."""
        with cls.controller.driver.session() as session:
            session.run("MATCH (u) DETACH DELETE u")
        cls.controller.close()

if __name__ == "__main__":
    unittest.main()