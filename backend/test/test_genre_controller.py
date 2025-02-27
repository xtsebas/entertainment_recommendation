import unittest
from dotenv import load_dotenv
import os
from neo4j import GraphDatabase
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controller.genre_controller import GenreController
from view.genre import Genre

load_dotenv()

class TestGenreController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configura la conexión con Neo4j antes de ejecutar las pruebas."""
        cls.controller = GenreController()
        cls.test_genre_id = "test-genre-1"

    @classmethod
    def tearDownClass(cls):
        """Cierra la conexión después de todas las pruebas."""
        cls.controller.close()

    def setUp(self):
        """Prepara datos para las pruebas."""
        self.test_genre = Genre(
            self.test_genre_id, "Test Genre", 0, "This is a test genre", False
        )
        self.controller.create_genre(self.test_genre)

    def tearDown(self):
        """Limpia los datos después de cada prueba."""
        self.controller.delete_genre(self.test_genre_id)

    # Prueba de Creación
    def test_create_genre(self):
        """Verifica que se pueda crear un género en Neo4j."""
        genre = self.controller.create_genre(self.test_genre)
        self.assertIsNotNone(genre, "El género no fue creado correctamente.")
        self.assertEqual(genre["name"], "Test Genre")
        self.assertEqual(genre["description"], "This is a test genre")
        self.assertEqual(genre["avg"], 0)
        self.assertFalse(genre["popular"])

    # Prueba de Obtener un Género
    def test_get_genre(self):
        """Verifica que se pueda obtener un género por su ID."""
        genre = self.controller.get_genre(self.test_genre_id)
        self.assertIsNotNone(genre)
        self.assertEqual(genre["id"], self.test_genre_id)

    # Prueba de Obtener Todos los Géneros
    def test_get_all_genres(self):
        """Verifica que se puedan obtener todos los géneros."""
        genres = self.controller.get_all_genres()
        self.assertGreater(len(genres), 0, "No se encontraron géneros en la BD.")

    # Prueba de Actualización
    def test_update_genre(self):
        """Verifica que se pueda actualizar un género."""
        updated_genre = Genre(self.test_genre_id, "Updated Genre", 0, "Updated description", False)
        self.controller.update_genre(updated_genre)
        
        genre = self.controller.get_genre(self.test_genre_id)
        self.assertEqual(genre["name"], "Updated Genre")
        self.assertEqual(genre["description"], "Updated description")

    # Prueba de Eliminación
    def test_delete_genre(self):
        """Verifica que se pueda eliminar un género."""
        self.controller.delete_genre(self.test_genre_id)
        genre = self.controller.get_genre(self.test_genre_id)
        self.assertIsNone(genre, "El género no fue eliminado correctamente.")

    # Prueba de Actualización de Estadísticas
    @unittest.skip("Depende de la relación HAS_GENRE y nodos Movie, aún no creados")
    def test_update_genre_stats(self):
        """Verifica que se actualicen las estadísticas de un género."""
        # Simula relaciones de películas con el género
        with self.controller.driver.session() as session:
            session.execute_write(self._create_mock_movies, self.test_genre_id)

        # Actualiza estadísticas
        self.controller.update_genre_stats(self.test_genre_id)
        genre = self.controller.get_genre(self.test_genre_id)
        
        self.assertGreaterEqual(genre["avg"], 5, "El `avg` no se actualizó correctamente.")
        self.assertTrue(genre["popular"], "El género no fue marcado como `popular` correctamente.")

    @staticmethod
    def _create_mock_movies(tx, genre_id):
        """Crea relaciones de prueba entre películas y un género."""
        query = """
        UNWIND range(1, 15) AS i
        MERGE (m:Movie {node_id: "test-movie-" + toString(i)})
        MERGE (g:Genre {node_id: $genre_id})
        MERGE (m)-[:HAS_GENRE]->(g)
        """
        tx.run(query, genre_id=genre_id)


if __name__ == '__main__':
    unittest.main()
