from engine import *
from starboard.scenes import Coconut, Wip, Expedition

setup = GameSetup("Coconut", [Expedition(), Wip(), Coconut()])

Game(setup).run()
