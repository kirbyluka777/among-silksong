from engine import *
from starboard.scenes import Coconut, Wip, Expedition, GameConfig

setup = GameSetup("Coconut", [GameConfig(), Wip(), Coconut()])

Game(setup).run()
