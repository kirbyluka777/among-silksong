from engine import *
from starboard.scenes import *

setup = GameSetup("Coconut", [MainMenu(), GameConfig(), Expedition(), Options(), Wip(), Coconut()])

Game(setup).run()
