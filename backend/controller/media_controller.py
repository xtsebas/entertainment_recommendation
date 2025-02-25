from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from view.media import Media

load_dotenv()

class MediaController:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        """Closes the database connection."""
        self.driver.close()

    #Create Media
    def create_media(self, media: Media):
        """Creates a new Media node in the database."""
        with self.driver.session() as session:
            session.execute_write(self._create_media_tx, media)

    @staticmethod
    def _create_media_tx(tx, media: Media):
        query = """
        CREATE (med:Media {
            media_id: $media_id,
            title: $title,
            genres: $genres,
            release_date: $release_date,
            avg_rating: $avg_rating
        })
        """
        tx.run(
            query,
            media_id=media.node_id,
            title=media.title,
            genres=media.genres,
            release_date=media.release_date.isoformat(),
            avg_rating=media.avg_rating
        )

    #Get All Media
    def get_all_media(self):
        """Retrieves all Media nodes."""
        with self.driver.session() as session:
            results = session.execute_read(self._get_all_media_tx)
            return list(results)

    @staticmethod
    def _get_all_media_tx(tx):
        query = """
        MATCH (med:Media)
        RETURN med.media_id AS media_id,
               med.title AS title,
               med.genres AS genres,
               med.release_date AS release_date,
               med.avg_rating AS avg_rating
        ORDER BY med.media_id
        """
        return tx.run(query)

    #Get All Media Labeled as Movie or Series
    def get_all_labeled_media(self):
        """Retrieves all Media nodes that are also labeled as Movie or Series."""
        with self.driver.session() as session:
            results = session.execute_read(self._get_all_labeled_media_tx)
            return list(results)

    @staticmethod
    def _get_all_labeled_media_tx(tx):
        query = """
        MATCH (med:Media)
        WHERE med:Movie OR med:Series
        RETURN med.media_id AS media_id,
               med.title AS title,
               labels(med) AS labels,
               med.genres AS genres,
               med.release_date AS release_date,
               med.avg_rating AS avg_rating
        ORDER BY med.media_id
        """
        return tx.run(query)

    #Get Media by ID
    def get_media_by_id(self, media_id: str):
        """Retrieves a single Media node by its ID."""
        with self.driver.session() as session:
            result = session.execute_read(self._get_media_by_id_tx, media_id)
            return result

    @staticmethod
    def _get_media_by_id_tx(tx, media_id: str):
        query = """
        MATCH (med:Media {media_id: $media_id})
        RETURN med.media_id AS media_id,
               med.title AS title,
               med.genres AS genres,
               med.release_date AS release_date,
               med.avg_rating AS avg_rating
        """
        result = tx.run(query, media_id=media_id)
        return result.single()

    #Update Media by ID
    def update_media(self, media: Media):
        """Updates an existing Media node by its ID."""
        with self.driver.session() as session:
            session.execute_write(self._update_media_tx, media)

    @staticmethod
    def _update_media_tx(tx, media: Media):
        query = """
        MATCH (med:Media {media_id: $media_id})
        SET med.title = $title,
            med.genres = $genres,
            med.release_date = $release_date,
            med.avg_rating = $avg_rating
        """
        tx.run(
            query,
            media_id=media.node_id,
            title=media.title,
            genres=media.genres,
            release_date=media.release_date.isoformat(),
            avg_rating=media.avg_rating
        )

    #Delete Media by ID (Also Deletes Relationships)
    def delete_media(self, media_id: str):
        """Deletes a Media node and all its relationships by ID."""
        with self.driver.session() as session:
            session.execute_write(self._delete_media_tx, media_id)

    @staticmethod
    def _delete_media_tx(tx, media_id: str):
        query = """
        MATCH (med:Media {media_id: $media_id})
        DETACH DELETE med
        """
        tx.run(query, media_id=media_id)
