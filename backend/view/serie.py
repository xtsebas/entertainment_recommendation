class Serie:
    def __init__(self, total_episodes: int, total_seasons: int,
                 status: str, release_format: str, show_runner: str):
        self.total_episodes = total_episodes
        self.total_seasons = total_seasons
        self.status = status
        self.release_format = release_format
        self.show_runner = show_runner

    @property
    def total_episodes(self) -> int:
        return self._total_episodes

    @total_episodes.setter
    def total_episodes(self, value: int):
        self._total_episodes = value

    @property
    def total_seasons(self) -> int:
        return self._total_seasons

    @total_seasons.setter
    def total_seasons(self, value: int):
        self._total_seasons = value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = value

    @property
    def release_format(self) -> str:
        return self._release_format

    @release_format.setter
    def release_format(self, value: str):
        self._release_format = value

    @property
    def show_runner(self) -> str:
        return self._show_runner

    @show_runner.setter
    def show_runner(self, value: str):
        self._show_runner = value
