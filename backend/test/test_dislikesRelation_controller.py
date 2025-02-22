import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.dislikes_relation_controller import DislikesRelationController
from view.user import User
from view.genre import Genre
from view.relations.dislikes import DislikesRelation
from datetime import datetime

class TestDislikesRelationController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configura el entorno antes de ejecutar las pruebas."""
        cls.controller = DislikesRelationController()
        cls.user = User("user123", "John Doe", 25, ["Action", "Comedy"], 120)
        cls.genre = Genre("genre123", "Horror", 4.5, "Scary and suspenseful", False)

        # Crear nodos User y Genre en la base de datos (si no existen)
        with cls.controller.driver.session() as session:
            session.run(
                "MERGE (u:User {node_id: $user_id, name: $name, age: $age})",
                user_id=cls.user.node_id, name=cls.user.name, age=cls.user.age
            )
            session.run(
                "MERGE (g:Genre {node_id: $genre_id, name: $name, avg: $avg, description: $description, popular: $popular})",
                genre_id=cls.genre.node_id, name=cls.genre.name, avg=cls.genre.avg, 
                description=cls.genre.description, popular=cls.genre.popular
            )

    def test_create_dislikes_relation(self):
        """Prueba la creación de una relación DISLIKES entre un usuario y un género."""
        relation = DislikesRelation(self.user, self.genre, 5)
        self.controller.create_dislikes_relation(relation)

        # Verificar si la relación se creó correctamente
        results = self.controller.get_dislikes_by_user(self.user.node_id)
        self.assertTrue(any(r["genre_id"] == self.genre.node_id for r in results))

    def test_get_dislikes_by_user(self):
        """Prueba la recuperación de relaciones DISLIKES de un usuario."""
        results = self.controller.get_dislikes_by_user(self.user.node_id)
        self.assertIsInstance(results, list)

        if results:
            first_relation = results[0]
            self.assertIn("genre_id", first_relation)
            self.assertIn("rejection_level", first_relation)
            self.assertIn("aggregation_date", first_relation)
            self.assertIn("last_engagement", first_relation)

    def test_delete_dislikes_relation(self):
        """Prueba la eliminación de una relación DISLIKES."""
        self.controller.delete_dislikes_relation(self.user.node_id, self.genre.node_id)
        results = self.controller.get_dislikes_by_user(self.user.node_id)
        
        self.assertFalse(any(r["genre_id"] == self.genre.node_id for r in results))

    @classmethod
    def tearDownClass(cls):
        """Limpia los datos creados en la base de datos después de las pruebas."""
        with cls.controller.driver.session() as session:
            session.run("MATCH (u:User {node_id: $user_id}) DETACH DELETE u", user_id=cls.user.node_id)
            session.run("MATCH (g:Genre {node_id: $genre_id}) DETACH DELETE g", genre_id=cls.genre.node_id)
        cls.controller.close()

if __name__ == "__main__":
    unittest.main()
