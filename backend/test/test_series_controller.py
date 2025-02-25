import unittest
import os
import sys
import time
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.serie_controller import SerieController
from view.serie import Serie

load_dotenv()

class TestSeriesController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize connection to Neo4j."""
        cls.controller = SerieController()
        cls.test_series = Serie(
            series_id="test-serie-1",
            total_episodes=62,
            total_seasons=5,
            status="Ended",
            release_format="TV Show",
            show_runner="Vince Gilligan"
        )

    @classmethod
    def tearDownClass(cls):
        """Close Neo4j connection."""
        cls.controller.close()

    def test_create_and_delete_series(self):
        """Test creating a Media:Series node and deleting it after a 10-second pause."""
        print("\nRunning test: test_create_and_delete_series")

        # ✅ Step 1: Create Series
        self.controller.create_series(self.test_series)
        print("✅ Series created! Check the database now.")

        # ⏳ Step 2: Wait 10 seconds before deletion
        for i in range(10, 0, -1):
            print(f" - Checking database... Test continues in {i} seconds.", end="\r")
            time.sleep(1)
        print("\nProceeding with deletion...")

        # ❌ Step 3: Manually Delete the Series Node
        with self.controller.driver.session() as session:
            query = """
            MATCH (s:Media:Serie)
            WHERE s.total_episodes = $total_episodes AND s.total_seasons = $total_seasons AND s.status = $status
            DETACH DELETE s
            """
            session.run(query, total_episodes=self.test_series.total_episodes, 
                        total_seasons=self.test_series.total_seasons, status=self.test_series.status)
        
        print("❌ Series deleted! Check the database to confirm.")

if __name__ == '__main__':
    unittest.main()
