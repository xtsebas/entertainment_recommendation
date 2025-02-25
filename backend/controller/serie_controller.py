from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from view.serie import Serie

load_dotenv()

class SerieController:
    def __init__(self):
        """Initialize connection to Neo4j."""
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        """Close the database connection."""
        self.driver.close()

    # ✅ Create Series:Media Node
    def create_series(self, series: Serie):
        """Creates a Series:Media node in the database."""
        with self.driver.session() as session:
            session.execute_write(self._create_series_tx, series)

    @staticmethod
    def _create_series_tx(tx, series: Serie):
        query = """
        CREATE (s:Media:Serie {  
            total_episodes: $total_episodes,
            total_seasons: $total_seasons,
            status: $status,
            release_format: $release_format,
            show_runner: $show_runner
        })
        RETURN s
        """
        tx.run(
            query,
            total_episodes=series.total_episodes,
            total_seasons=series.total_seasons,
            status=series.status,
            release_format=series.release_format,
            show_runner=series.show_runner
        )
