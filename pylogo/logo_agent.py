from colorama import Fore, Back, Style


class LogoAgent:
    colours_fore = {
        "red": Fore.RED,
        "blue": Fore.BLUE,
        "cyan": Fore.CYAN
    }

    colours_back = {
        "red": Back.RED,
        "blue": Back.BLUE,
        "cyan": Back.CYAN
    }

    def __init__(self, colour="cyan", highlight=False) -> None:
        self.colour = colour
        self.highlight = highlight

    def get_styled_repr(self, padding=5):
        padded = self.__class__.__name__.ljust(padding, ' ')
        return f"{self.get_styled()}{padded}{Style.RESET_ALL}"

    def get_styled(self):
        if self.highlight:
            colouring = LogoAgent.colours_back[self.colour] + Fore.WHITE
        else:
            colouring = LogoAgent.colours_fore[self.colour]
        return Style.BRIGHT + colouring

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
