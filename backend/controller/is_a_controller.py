from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from view.movie import Movie
from view.serie import Serie
load_dotenv()

class IS_A_Controller:
    def __init__(self):
        """Initialize connection to Neo4j."""
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        """Close Neo4j connection."""
        self.driver.close()

    # ✅ Create IS_A Relationship for Movie
    def create_movie_relation(self, media_id: str, movie: Movie):
        """Links Media to Movie via IS_A relationship."""
        with self.driver.session() as session:
            session.execute_write(self._create_movie_relation_tx, media_id, movie)

    @staticmethod
    def _create_movie_relation_tx(tx, media_id: str, movie: Movie):
        query = """
        MATCH (med:Media {media_id: $media_id})
        MATCH (m:Media:Movie {
            duration: $duration,
            budget: $budget,
            revenue: $revenue,
            age_classification: $age_classification
        })
        MERGE (med)-[:IS_A {
            type: "Movie",
            created_at: datetime(),
            updated_at: datetime()
        }]->(m)
        """
        tx.run(query, 
            media_id=media_id, 
            duration=movie.duration, 
            budget=movie.budget, 
            revenue=movie.revenue, 
            age_classification=movie.age_classification
            )

    # Create IS_A Relationship for Series
    def create_serie_relation(self, media_id: str, serie : Serie):
        """Links Media to Series via IS_A relationship."""
        with self.driver.session() as session:
            session.execute_write(self._create_serie_relation_tx, media_id, serie)


    @staticmethod
    @staticmethod
    def _create_serie_relation_tx(tx, media_id: str, serie: Serie):
        query = """
        MATCH (med:Media {media_id: $media_id})
        MATCH (s:Media:Serie {
            total_episodes: $total_episodes,
            total_seasons: $total_seasons,
            status: $status,
            release_format: $release_format,
            show_runner: $show_runner
        })
        MERGE (med)-[:IS_A {
            type: "Serie",
            created_at: datetime(),
            updated_at: datetime()
        }]->(s)
        """
        tx.run(query,
            media_id=media_id, 
            total_episodes=serie.total_episodes,
            total_seasons=serie.total_seasons, 
            status=serie.status, 
            release_format=serie.release_format, 
            show_runner=serie.show_runner
            )
