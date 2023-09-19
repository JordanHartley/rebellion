from pylogo.turtle import Turtle as PyTurtle


class Turtle(PyTurtle):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.is_cop = False
        self.is_agent = True

    def make_cop(self):
        self.is_cop = True
        self.is_agent = False
