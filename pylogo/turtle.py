from pylogo.logo_agent import LogoAgent


class Turtle(LogoAgent):
    def __init__(self, colour="red", highlight=False, patch=None) -> None:
        super().__init__(colour=colour, highlight=highlight)
        self.patch = patch

    def __repr__(self) -> str:
        return super().__repr__()
