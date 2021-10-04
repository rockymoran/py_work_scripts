# rocco's adventure game


class Player:
    def __init__(self):
        self.p_name = input("Name? ")
        self.stamina = 100
        self.inventory = Inventory()


class Inventory:
    def __init__(self):
        self.equipment = "fishing pole"
        self.items = ""


class Level:
    def __init__(self):
        self.level = ""


def welcome():
    print("Welcome to this cool game.")
    print("Let's get started.")
    new_player = Player()
    return new_player


def main():
    continue_playing = True
    new_player = welcome()
    while continue_playing:
        print(new_player.__dict__)
        print(new_player.inventory.__dict__)
        continue_playing = False
    return print("Thanks for playing!")

if __name__ == '__main__':
    main()
