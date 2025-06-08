from engine import *
from starboard.scenes import Coconut, Wip

setup = GameSetup("Coconut", [Wip(), Coconut()])

Game(setup).run()
