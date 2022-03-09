from game import Game


class Fps(Game):
    def __init__(self):
        """
        super().__init__ gets all the attributes from the parent class i.e. Game
        these attributes are now accessible within the child class i.e. Fps
        """
        super().__init__()
        self.wins = 0

    # creating a getter & setter using decorators. They automatically create a private version of the attribute you want to control
    @property
    def wins(self):
        return self.__wins

    @wins.setter
    def wins(self, val):
        self.__wins = val

    def __repr__(self):
        return super().__repr__() + f"[+] Wins {self.wins:.>20}\n"


game1 = Fps()
game1.add_data(name="Battlefield 2042", cost="40$")
game1.wins = 877
print(game1)
