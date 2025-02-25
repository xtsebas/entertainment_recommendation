from model.node import Node

class Series(Node):
    def __init__(self, series_id: str, total_episodes: int, total_seasons: int,
                 status: str, release_format: str, show_runner: str):
        super().__init__(series_id, "Series",
                         total_episodes=total_episodes,
                         total_seasons=total_seasons,
                         status=status,
                         release_format=release_format,
                         show_runner=show_runner)

    @property
    def total_episodes(self) -> int:
        return self.properties.get("total_episodes")

    @total_episodes.setter
    def total_episodes(self, value: int):
        self.properties["total_episodes"] = value

    @property
    def total_seasons(self) -> int:
        return self.properties.get("total_seasons")

    @total_seasons.setter
    def total_seasons(self, value: int):
        self.properties["total_seasons"] = value

    @property
    def status(self) -> str:
        return self.properties.get("status")

    @status.setter
    def status(self, value: str):
        self.properties["status"] = value

    @property
    def release_format(self) -> str:
        return self.properties.get("release_format")

    @release_format.setter
    def release_format(self, value: str):
        self.properties["release_format"] = value

    @property
    def show_runner(self) -> str:
        return self.properties.get("show_runner")

    @show_runner.setter
    def show_runner(self, value: str):
        self.properties["show_runner"] = value
