import unittest
import os
import sys
import time
from datetime import date
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.media_controller import MediaController
from view.media import Media

load_dotenv()

class TestMediaController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize connection to Neo4j and define a test media ID."""
        cls.controller = MediaController()
        cls.test_media_id = "test-media-1"

    @classmethod
    def tearDownClass(cls):
        """Close Neo4j connection after tests."""
        cls.controller.close()

    def setUp(self):
        """Create a test Media node in the database."""
        self.test_media = Media(
            media_id=self.test_media_id,
            title="Test Media",
            genres=["Test Genre"],
            release_date=date(2022, 1, 1),
            avg_rating=5.0
        )
        self.controller.create_media(self.test_media)

    def tearDown(self):
        """Delete the test Media node after each test."""
        self.controller.delete_media(self.test_media_id)

    def wait_and_log(self, test_name):
        """Helper function to log test name and wait 10 seconds."""
        print(f"\nRunning test: {test_name}")
        start_time = time.time()
        for i in range(10, 0, -1):
            print(f" - Checking database... Test continues in {i} seconds.", end="\r")
            time.sleep(1)
        print(f"\n[Test {test_name} completed in {round(time.time() - start_time, 2)} sec]")

    def test_create_media(self):
        """Verify media creation in Neo4j and check its properties."""
        self.wait_and_log("test_create_media")

        media_data = self.controller.get_media_by_id(self.test_media_id)
        self.assertIsNotNone(media_data, "Media was not created successfully.")
        self.assertEqual(media_data["media_id"], self.test_media_id)
        self.assertEqual(media_data["title"], "Test Media")
        self.assertEqual(media_data["genres"], ["Test Genre"])
        self.assertEqual(media_data["avg_rating"], 5.0)

    def test_get_media_by_id(self):
        """Verify that media can be retrieved by ID."""
        self.wait_and_log("test_get_media_by_id")

        media_data = self.controller.get_media_by_id(self.test_media_id)
        self.assertIsNotNone(media_data, "Failed to retrieve media.")
        self.assertEqual(media_data["media_id"], self.test_media_id)

    @unittest.skip("Uncomment when there are multiple media nodes in the database.")
    def test_get_all_media(self):
        """Verify retrieval of all Media nodes."""
        self.wait_and_log("test_get_all_media")

        all_media = self.controller.get_all_media()
        self.assertGreater(len(all_media), 0, "No Media nodes found in the database.")

    @unittest.skip("Uncomment when there are multiple media nodes labeled as Movie or Series.")
    def test_get_all_labeled_media(self):
        """Verify retrieval of Media nodes labeled as Movie or Series."""
        self.wait_and_log("test_get_all_labeled_media")

        labeled_media = self.controller.get_all_labeled_media()
        self.assertGreater(len(labeled_media), 0, "No labeled Media (Movie/Series) found.")

    def test_update_media(self):
        """Verify that a Media node can be updated."""
        self.wait_and_log("test_update_media")

        updated_media = Media(
            media_id=self.test_media_id,
            title="Updated Test Media",
            genres=["Updated Genre"],
            release_date=date(2022, 1, 1),
            avg_rating=4.5
        )
        self.controller.update_media(updated_media)

        media_data = self.controller.get_media_by_id(self.test_media_id)
        self.assertEqual(media_data["title"], "Updated Test Media")
        self.assertEqual(media_data["genres"], ["Updated Genre"])
        self.assertEqual(media_data["avg_rating"], 4.5)

    def test_delete_media(self):
        """Verify that a Media node can be deleted."""
        self.wait_and_log("test_delete_media")

        self.controller.delete_media(self.test_media_id)
        media_data = self.controller.get_media_by_id(self.test_media_id)
        self.assertIsNone(media_data, "Media was not deleted successfully.")

if __name__ == '__main__':
    unittest.main()
