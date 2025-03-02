from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from view.movie import Movie

load_dotenv()

class MovieController:
    def __init__(self):
        """Initialize connection to Neo4j."""
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        """Close the database connection."""
        self.driver.close()

    # ✅ Create Movie:Media Node
    def create_movie(self, movie: Movie):
        """Creates a Movie:Media node in the database."""
        with self.driver.session() as session:
            session.execute_write(self._create_movie_tx, movie)

    @staticmethod
    def _create_movie_tx(tx, movie: Movie):
        query = """
        CREATE (m:Media:Movie {  
            duration: $duration,
            budget: $budget,
            revenue: $revenue,
            nominations: $nominations,
            age_classification: $age_classification
        })
        RETURN m
        """
        tx.run(
            query,
            duration=movie.duration,
            budget=movie.budget,
            revenue=movie.revenue,
            nominations=movie.nominations,
            age_classification=movie.age_classification
        )

    def get_all_movies_sorted_by_creation(self, limit: int = 1979):
        """
        Retrieves all movies sorted by creation date (most recent first), with an optional limit.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._get_all_movies_sorted_by_creation_tx, limit)
        return result

    @staticmethod
    def _get_all_movies_sorted_by_creation_tx(tx, limit: int):
        query = """
        MATCH (m:Media)-[:IS_A]->(mov:Movie)
        RETURN 
            m.title AS movie, 
            m.avg_rating AS rating,
            mov.age_classification AS classification,
            id(mov) AS node_id
        ORDER BY id(mov) DESC       
        LIMIT $limit
        """
        result = tx.run(query, limit=limit)
        return [record.data() for record in result]