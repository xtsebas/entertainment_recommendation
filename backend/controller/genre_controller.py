from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from view.genre import Genre

load_dotenv()

class GenreController:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        """Cierra la conexión con Neo4j."""
        self.driver.close()
    #Create genre
    def create_genre(self, genre: Genre):
        """Crea un nuevo género en la base de datos."""
        with self.driver.session() as session:
            session.execute_write(self._create_genre_tx, genre)
            # Actualizar estadísticas después de crearlo
            result = session.execute_read(self._get_genre_tx, genre.node_id)
            return result 

    @staticmethod
    def _create_genre_tx(tx, genre: Genre):
        query = """
        MERGE (g:Genre {node_id: $genre_id})
        SET g.name = $name, g.avg = 0, g.description = $description, g.popular = false
        """
        tx.run(query, genre_id=genre.node_id, name=genre.name, description=genre.description)

    #get Genre
    def get_genre(self, genre_id: str):
        """Obtiene un género por su ID."""
        with self.driver.session() as session:
            result = session.execute_read(self._get_genre_tx, genre_id)
        return result
        
    @staticmethod
    def _get_genre_tx(tx, genre_id: str):
        query = """
        MATCH (g:Genre {node_id: $genre_id})
        RETURN g.node_id AS id, g.name AS name, g.avg AS avg, g.description AS description, g.popular AS popular
        """
        result = tx.run(query, genre_id=genre_id)
        return result.single()
    
    #gGet all genres
    def get_all_genres(self):
        """Obtiene todos los géneros en la base de datos y devuelve una lista de diccionarios."""
        with self.driver.session() as session:
            result = session.execute_read(self._get_all_genres_tx)
            genres = [record for record in result]  
        return genres


    @staticmethod
    def _get_all_genres_tx(tx):
        query = """
        MATCH (g:Genre)
        RETURN g.genre_id AS id, g.name AS name, g.avg AS avg, g.description AS description, g.popular AS popular
        ORDER BY g.name
        """
        result = tx.run(query)
        return [record.data() for record in result]  

    #Updated genre
    def update_genre(self, genre: Genre):
        """Actualiza la información de un género."""
        with self.driver.session() as session:
            session.execute_write(self._update_genre_tx, genre)
            # Recalcular estadísticas después de la actualización
            self.update_genre_stats(genre.node_id)

    @staticmethod
    def _update_genre_tx(tx, genre: Genre):
        query = """
        MATCH (g:Genre {node_id: $genre_id})
        SET g.name = $name, g.description = $description
        """
        tx.run(query, genre_id=genre.node_id, name=genre.name, description=genre.description)

    #Delete genre
    def delete_genre(self, genre_id: str):
        """Elimina un género de la base de datos."""
        with self.driver.session() as session:
            session.execute_write(self._delete_genre_tx, genre_id)

    @staticmethod
    def _delete_genre_tx(tx, genre_id):
        query = """
        MATCH (g:Genre {node_id: $genre_id})
        DETACH DELETE g
        """
        tx.run(query, genre_id=genre_id)

    #Updated AVG and Popular
    def update_genre_stats(self, genre_id: str):
        """Actualiza las estadísticas de un género (cantidad de películas/series y popularidad)."""
        with self.driver.session() as session:
            result = session.execute_read(self._count_movies_with_genre, genre_id)
            count = result["count"]
            is_popular = count >= 10  # TODO: value has to change when we have a large database
            session.execute_write(self._update_genre_properties, genre_id, count, is_popular)

    @staticmethod
    def _count_movies_with_genre(tx, genre_id):
        """Cuenta cuántas películas/series tienen este género."""
        query = """
        MATCH (:Movie)-[:HAS_GENRE]->(g:Genre {node_id: $genre_id})
        RETURN COUNT(*) AS count
        """
        result = tx.run(query, genre_id=genre_id)
        return result.single()

    @staticmethod
    def _update_genre_properties(tx, genre_id, count, is_popular):
        """Actualiza `avg` con el número de películas/series y `popular` si es >= 10."""
        query = """
        MATCH (g:Genre {node_id: $genre_id})
        SET g.avg = $count, g.popular = $is_popular
        """
        tx.run(query, genre_id=genre_id, count=count, is_popular=is_popular)
    
    def create_new_genre(self, genre: Genre):
        """
        Creates a new Genre node in the database.
        """
        with self.driver.session() as session:
            session.execute_write(self._create_new_genre_tx, genre)

    @staticmethod
    def _create_new_genre_tx(tx, genre: Genre):
        query = """
        CREATE (g:Genre {
            genre_id: $genre_id,
            name: $name,
            avg: $avg,
            description: $description,
            popular: $popular
        })
        RETURN g
        """
        tx.run(
            query,
            genre_id=genre.genre_id,
            name=genre.name,
            avg=genre.avg,
            description=genre.description,
            popular=genre.popular
        )
    
    def get_genre_popularity(self):
        """
        Retrieves genres ordered by the number of likes in descending order.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._get_genre_popularity_tx)
        return result

    @staticmethod
    def _get_genre_popularity_tx(tx):
        query = """
        MATCH (u:User)-[l:LIKES]->(g:Genre)
        RETURN g.name AS genre, COUNT(l) AS like_count
        ORDER BY like_count DESC
        """
        result = tx.run(query)
        return [record.data() for record in result]

    def get_total_genres(self):
        """
        Returns the total number of genres in the database.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._get_total_genres_tx)
        return result

    @staticmethod
    def _get_total_genres_tx(tx):
        query = """
        MATCH (g:Genre)
        RETURN COUNT(g) AS total_genres
        """
        result = tx.run(query).single()
        return result["total_genres"] if result else 0
