import unittest
import bcrypt
from dotenv import load_dotenv
import os
from neo4j import GraphDatabase
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.user_controller import UserController
from view.user import User

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

class TestUserController(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Se ejecuta antes de cualquier test: Conecta a la BD"""
        cls.controller = UserController()
        cls.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    @classmethod
    def tearDownClass(cls):
        """Se ejecuta después de todos los tests: Cierra la conexión"""
        cls.controller.close()
        cls.driver.close()
    
    def tearDown(self):
        """Se ejecuta después de cada test: Borra los datos insertados"""
        with self.driver.session() as session:
            session.run("MATCH (u:User) DETACH DELETE u")

    def test_create_user(self):
        """ Prueba la creación de un usuario en Neo4j con contraseña hasheada """
        password = "MiContraseñaSegura"
        user = User("123", "Test User", password, 25, ["Acción", "Drama"], 120)
        response = self.controller.create_user(user, password)

        # Verifica que la respuesta sea exitosa
        self.assertEqual(response["message"], "Usuario creado correctamente")

        # Verifica que el usuario existe en la BD y que la contraseña está hasheada
        with self.driver.session() as session:
            result = session.run("MATCH (u:User {user_id: $user_id}) RETURN u.password AS password", user_id="123")
            user_node = result.single()
            self.assertIsNotNone(user_node)
            stored_password = user_node["password"]

            # Verifica que la contraseña almacenada no es la original (debe estar hasheada)
            self.assertNotEqual(stored_password, password)
            self.assertTrue(bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")))

    def test_get_users(self):
        """ Prueba la obtención de usuarios desde Neo4j sin contraseña """
        user = User("456", "Otro Usuario", "UserPass456", 30, ["Comedia"], 90)
        self.controller.create_user(user, "password123")

        users = self.controller.get_users()

        # Verifica que la lista de usuarios no esté vacía
        self.assertTrue(len(users) > 0)

        # Verifica que los usuarios no tengan la contraseña en la respuesta
        for user in users:
            self.assertNotIn("password", user)

    def test_get_user_by_credentials(self):
        """Prueba la autenticación de usuario con nombre y contraseña"""
        password = "SecurePass789"
        user = User("789", "UsuarioAuth", password, 40, ["Thriller"], 100)
        self.controller.create_user(user, password)

        # Prueba autenticación correcta
        authenticated_user = self.controller.get_user_by_credentials("UsuarioAuth", password)
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user["name"], "UsuarioAuth")

        # Prueba autenticación con contraseña incorrecta
        wrong_auth = self.controller.get_user_by_credentials("UsuarioAuth", "ClaveIncorrecta")
        self.assertIsNone(wrong_auth)

    def test_delete_user(self):
        """Prueba la eliminación de un usuario en Neo4j"""
        password = "DeletePass999"
        user = User("789", "Eliminar Usuario", password, 40, ["Terror"], 100)
        self.controller.create_user(user, password)
        
        # Verifica que el usuario existe antes de eliminarlo
        with self.driver.session() as session:
            result = session.run("MATCH (u:User {user_id: $user_id}) RETURN u", user_id="789")
            self.assertIsNotNone(result.single())

        # Elimina el usuario
        self.controller.delete_user("789")
        
        # Verifica que el usuario ya no existe en la BD
        with self.driver.session() as session:
            result = session.run("MATCH (u:User {user_id: $user_id}) RETURN u", user_id="789")
            self.assertIsNone(result.single())

if __name__ == "__main__":
    unittest.main()
