import unittest
import os
import sys
import time
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.user_controller import UserController

load_dotenv()

class TestUserController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize connection to Neo4j."""
        cls.controller = UserController()
        cls.test_user_id = "cbd92f90-6e2d-4441-b2b9-d9ba9942edd5"  # Provided user_id

    @classmethod
    def tearDownClass(cls):
        """Close Neo4j connection."""
        cls.controller.close()

    def test_get_series_not_rated_by_user(self):
        """Test fetching series the user has not rated."""
        print("\nRunning test: test_get_series_not_rated_by_user")

        limit = 5
        print(f"> Fetching up to {limit} series that user has NOT rated...")

        # Step 1: Get Series
        try:
            series = self.controller.get_series_not_rated_by_user(self.test_user_id, limit)
        except ValueError as e:
            print(f"⚠️ Error: {e}")
            return

        # Step 2: Wait 5 seconds for manual database check
        for i in range(5, 0, -1):
            print(f" - Checking database... Test continues in {i} seconds.", end="\r")
            time.sleep(1)
        print("\nProceeding to print results...\n")

        # Step 3: Print Results
        if series:
            print("🎬 series NOT Rated by User:")
            for serie in series:
                print(serie)
        else:
            print("✅ No unrated series found for this user.")

        # Step 4: Assertions
        self.assertIsInstance(series, list, "The function should return a list.")
        self.assertLessEqual(len(series), limit, "Returned series should not exceed the limit.")
        
        if series:
            sample_serie = series[0]
            self.assertIn("media_id", sample_serie)
            self.assertIn("serie_title", sample_serie)
            self.assertIn("total_episodes", sample_serie)
            self.assertIn("total_seasons", sample_serie)
            self.assertIn("show_runner", sample_serie)
            self.assertIn("status", sample_serie)
            self.assertIn("release_date", sample_serie)

if __name__ == '__main__':
    unittest.main()
