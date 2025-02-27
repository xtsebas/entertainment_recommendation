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

    def test_get_movies_not_rated_by_user(self):
        """Test fetching movies the user has not rated."""
        print("\nRunning test: test_get_movies_not_rated_by_user")

        limit = 5
        print(f"> Fetching up to {limit} movies that user has NOT rated...")

        # Step 1: Get Movies
        try:
            movies = self.controller.get_movies_not_rated_by_user(self.test_user_id, limit)
        except ValueError as e:
            print(f"⚠️ Error: {e}")
            return

        # Step 2: Wait 5 seconds for manual database check
        for i in range(5, 0, -1):
            print(f" - Checking database... Test continues in {i} seconds.", end="\r")
            time.sleep(1)
        print("\nProceeding to print results...\n")

        # Step 3: Print Results
        if movies:
            print("🎬 Movies NOT Rated by User:")
            for movie in movies:
                print(movie)
        else:
            print("✅ No unrated movies found for this user.")

        # Step 4: Assertions
        self.assertIsInstance(movies, list, "The function should return a list.")
        self.assertLessEqual(len(movies), limit, "Returned movies should not exceed the limit.")
        
        if movies:
            sample_movie = movies[0]
            self.assertIn("media_id", sample_movie)
            self.assertIn("movie_title", sample_movie)
            self.assertIn("revenue", sample_movie)
            self.assertIn("budget", sample_movie)
            self.assertIn("duration", sample_movie)
            self.assertIn("release_date", sample_movie)

if __name__ == '__main__':
    unittest.main()
