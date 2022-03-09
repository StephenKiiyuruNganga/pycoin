class Game:
    def __init__(self):
        self.__name = None
        self.__cost = None

    def add_data(self, name, cost):
        self.__name = name
        self.__cost = cost

    def __repr__(self):
        print("\nLoading game info...\n")
        return f"[+] Name {self.__name:.>20}\n[+] Cost {self.__cost:.>20}\n"


# game1 = Game()
# game1.add_data(cost="50$", name="COD")
# print(game1)
