import random
from datetime import datetime, timedelta
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

class UserWatchedController:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        """Cierra la conexión con Neo4j."""
        self.driver.close()

    def create_user_watched_movie(self, user_id: str, media_id: str):
        """Crea una relación WATCHED entre un usuario y una película con propiedades aleatorias."""
        view_date = self._generate_random_date()
        device = self._get_random_device()
        rewatch_count = random.randint(1, 5)

        with self.driver.session() as session:
            session.execute_write(
                self._create_user_watched_movie_tx, user_id, media_id, view_date, device, rewatch_count
            )

    @staticmethod
    def _create_user_watched_movie_tx(tx, user_id: str, media_id: str, view_date: str, device: str, rewatch_count: int):
        query = """
        MATCH (u:User), (m:Media)-[i:IS_A]->(mov:Movie)
        WHERE u.user_id = $user_id AND m.media_id = $media_id
        CREATE (u)-[r:WATCHED {
            view_date: $view_date,
            device: $device,
            rewatch_count: $rewatch_count
        }]->(mov)
        RETURN u, r, mov
        """
        tx.run(query, user_id=user_id, media_id=media_id, view_date=view_date, device=device, rewatch_count=rewatch_count)

    def create_user_watched_serie(self, user_id: str, media_id: str):
        """Crea una relación WATCHED entre un usuario y una serie con propiedades aleatorias."""
        view_date = self._generate_random_date()
        device = self._get_random_device()
        played_episodes = random.randint(1, 20)

        with self.driver.session() as session:
            session.execute_write(
                self._create_user_watched_serie_tx, user_id, media_id, view_date, device, played_episodes
            )

    @staticmethod
    def _create_user_watched_serie_tx(tx, user_id: str, media_id: str, view_date: str, device: str, played_episodes: int):
        query = """
        MATCH (u:User), (m:Media)-[i:IS_A]->(se:Serie)
        WHERE u.user_id = $user_id AND m.media_id = $media_id
        CREATE (u)-[r:WATCHED {
            view_date: $view_date,
            device: $device,
            played_episodes: $played_episodes
        }]->(se)
        RETURN u, r, se
        """
        tx.run(query, user_id=user_id, media_id=media_id, view_date=view_date, device=device, played_episodes=played_episodes)

    def get_watched_movies_by_user(self, user_id: str):
        """
        Retrieves all movies watched by a user, returning movie title, age classification, and view date.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._get_watched_movies_by_user_tx, user_id)
        return result

    @staticmethod
    def _get_watched_movies_by_user_tx(tx, user_id: str):
        query = """
        MATCH (u:User {user_id: $user_id})-[w:WATCHED]->(m:Movie), 
              (med:Media)-[:IS_A]->(m:Movie) 
        RETURN med.title AS movie, m.age_classification AS age_classification, w.view_date AS view_date
        """
        result = tx.run(query, user_id=user_id)
        return [record.data() for record in result]
        

    @staticmethod
    def _generate_random_date():
        """Genera una fecha aleatoria dentro de los últimos 2 años."""
        days_ago = random.randint(0, 730)  # Número de días entre 0 y 730 (últimos 2 años)
        random_date = datetime.now() - timedelta(days=days_ago)
        return random_date.strftime("%Y-%m-%d")  # Formato YYYY-MM-DD

    @staticmethod
    def _get_random_device():
        """Selecciona aleatoriamente un dispositivo de una lista predefinida."""
        devices = ["mobile", "tablet", "laptop", "smart_tv"]
        return random.choice(devices)

    def get_watched_series_by_user(self, user_id: str):
        """
        Retrieves all series watched by a user, returning series title, age classification, and view date.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._get_watched_series_by_user_tx, user_id)
        return result

    @staticmethod
    def _get_watched_series_by_user_tx(tx, user_id: str):
        query = """
        MATCH (u:User {user_id: $user_id})-[w:WATCHED]->(s:Serie), 
              (med:Media)-[:IS_A]->(s:Serie) 
        RETURN med.title as serie, w.played_episodes as played_episodes, w.view_date as view_date, s.total_episodes as total_episodes, s.status as status
        """
        result = tx.run(query, user_id=user_id)
        return [record.data() for record in result]

    def delete_watched_serie_by_user(self, user_id: str, title: str):
        """
        Deletes the WATCHED relationship between a User and a Serie based on the series title.
        """
        with self.driver.session() as session:
            session.execute_write(self._delete_watched_serie_by_user_tx, user_id, title)

    @staticmethod
    def _delete_watched_serie_by_user_tx(tx, user_id: str, title: str):
        query = """
        MATCH (u:User {user_id: $user_id})-[w:WATCHED]->(s:Serie),
              (med:Media)-[:IS_A]->(s:Serie)
        WHERE med.title = $title
        DELETE w
        """
        tx.run(query, user_id=user_id, title=title)

    def delete_watched_movie_by_user(self, user_id: str, title: str):
        """
        Deletes the WATCHED relationship between a User and a Movie based on the movie title.
        """
        with self.driver.session() as session:
            session.execute_write(self._delete_watched_movie_by_user_tx, user_id, title)

    @staticmethod
    def _delete_watched_movie_by_user_tx(tx, user_id: str, title: str):
        query = """
        MATCH (u:User {user_id: $user_id})-[w:WATCHED]->(m:Movie),
              (med:Media)-[:IS_A]->(m:Movie)
        WHERE med.title = $title
        DELETE w
        """
        tx.run(query, user_id=user_id, title=title)