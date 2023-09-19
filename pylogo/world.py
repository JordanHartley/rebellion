class WorldError(Exception):
    def __init__(self, message, value):
        super().__init__(message)
        self.value = value


class World:
    def __init__(self, height: int, width: int, max_ticks: int) -> None:
        self.world_height = height
        self.world_width = width
        self.num_patches: int = height * width
        self._max_ticks = max_ticks
        self._ticks = 0
        self._terminated: bool = False
        self.GRID = None

    def __call__(self) -> None:
        self.go()

    def go(self) -> None:
        for _ in self.go_iter():
            pass

    def go_iter(self) -> None:
        assert not (self.GRID is None), WorldError(
            f"cannot go() without a grid - received: {self.GRID}")
        for _ in range(self._max_ticks):
            self.tick()
            yield self.GRID
        self.__terminate()

    def __terminate(self):
        self._terminated = True

    def tick(self) -> None:
        assert not self._terminated, WorldError(
            "cannot tick when world is terminated")
        self._ticks += 1
        self.on_tick()

    def current_tick(self) -> int:
        return self._ticks

    def current_tick(self):
        return self._ticks

    def on_tick(self):
        self.__terminate()
        raise NotImplementedError

    def __repr__(self):
        return f"{self.__class__.__name__}(h={self.world_height}w={self.world_width})"
