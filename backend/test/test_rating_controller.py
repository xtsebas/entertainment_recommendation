import unittest
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.rating_controller import RatingController
from view.rating import Rating

load_dotenv()

class TestRatingController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #Inicializa la conexión a Neo4j y define un ID de prueba.
        cls.controller = RatingController()
        cls.test_rating_id = "test-rating-1"

    @classmethod
    def tearDownClass(cls):        
        #Cierra la conexión al terminar.
        cls.controller.close()

    def setUp(self):
        #Crea un Rating de prueba en la base de datos.
        self.test_rating = Rating(
            rating_id=self.test_rating_id,
            rating=5,
            comment="Excellent",
            final_feeling="Happy",
            recommend=True
        )
        self.controller.create_rating(self.test_rating)

    def tearDown(self):
        #Elimina el Rating de prueba de la base de datos.
        self.controller.delete_rating(self.test_rating_id)

    def test_create_rating(self):
        #Verifica que se pueda crear un rating en Neo4j y que las propiedades sean correctas.
        rating_data = self.controller.get_rating(self.test_rating_id)
        self.assertIsNotNone(rating_data, "El rating no fue creado correctamente.")
        self.assertEqual(rating_data["id"], self.test_rating_id)
        self.assertEqual(rating_data["rating"], 5)
        self.assertEqual(rating_data["comment"], "Excellent")
        self.assertEqual(rating_data["final_feeling"], "Happy")
        self.assertTrue(rating_data["recommend"])
        self.assertTrue(rating_data["is_good"])

    def test_get_rating(self):
        #Verifica que se pueda obtener un rating por su ID.
        rating_data = self.controller.get_rating(self.test_rating_id)
        self.assertIsNotNone(rating_data, "No se pudo obtener el rating.")
        self.assertEqual(rating_data["id"], self.test_rating_id)

    @unittest.skip("Descomenta cuando tengas múltiples Ratings en la BD.")
    def test_get_all_ratings(self):
        #Verifica que se puedan obtener todos los ratings.
        all_ratings = self.controller.get_all_ratings()
        self.assertGreater(len(all_ratings), 0, "No se encontraron Ratings en la BD.")

    def test_update_rating(self):
        #Verifica que se pueda actualizar un rating.
        # Creamos un nuevo objeto Rating con las propiedades actualizadas
        updated_rating = Rating(
            rating_id=self.test_rating_id,
            rating=4,
            comment="Improved",
            final_feeling="Neutral",
            recommend=True
        )
        self.controller.update_rating(updated_rating)

        # Verificamos que se hayan aplicado los cambios
        rating_data = self.controller.get_rating(self.test_rating_id)
        self.assertEqual(rating_data["rating"], 4)
        self.assertEqual(rating_data["comment"], "Improved")
        self.assertEqual(rating_data["final_feeling"], "Neutral")
        self.assertTrue(rating_data["recommend"])
        self.assertTrue(rating_data["is_good"])

    def test_delete_rating(self):
        #Verifica que se pueda eliminar un rating.
        self.controller.delete_rating(self.test_rating_id)
        rating_data = self.controller.get_rating(self.test_rating_id)
        self.assertIsNone(rating_data, "El rating no fue eliminado correctamente.")

if __name__ == '__main__':
    unittest.main()
