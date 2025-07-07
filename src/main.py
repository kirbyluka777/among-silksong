from engine import *
from starboard.scenes import Coconut, Wip, Expedition, GameConfig

setup = GameSetup("Coconut", [GameConfig(), Expedition(), Wip(), Coconut()])

Game(setup).run()
