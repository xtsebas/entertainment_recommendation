import unittest
import os
import sys
import time
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.movie_controller import MovieController
from view.movie import Movie

load_dotenv()

class TestMovieController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize connection to Neo4j."""
        cls.controller = MovieController()
        cls.test_movie = Movie(
            movie_id="test-movie-1",
            duration=148,
            budget=160000000,
            revenue=829895144,
            nominations=["Oscar", "BAFTA"],
            age_classification="PG-13"
        )

    @classmethod
    def tearDownClass(cls):
        """Close Neo4j connection."""
        cls.controller.close()

    def test_create_and_delete_movie(self):
        """Test creating a Movie:Media node and deleting it after a 10-second pause."""
        print("\nRunning test: test_create_and_delete_movie")

        # Step 1: Create Movie
        self.controller.create_movie(self.test_movie)
        print("> Movie created! Check the database now.")

        # Step 2: Wait 10 seconds before deletion
        for i in range(10, 0, -1):
            print(f" - Checking database... Test continues in {i} seconds.", end="\r")
            time.sleep(1)
        print("\nProceeding with deletion...")

        # Step 3: Manually Delete the Movie Node
        with self.controller.driver.session() as session:
            query = """
            MATCH (m:Media:Movie)
            WHERE m.duration = $duration AND m.budget = $budget AND m.revenue = $revenue
            DETACH DELETE m
            """
            session.run(query, duration=self.test_movie.duration, budget=self.test_movie.budget, revenue=self.test_movie.revenue)
        
        print("> Movie deleted! Check the database to confirm.")

if __name__ == '__main__':
    unittest.main()
