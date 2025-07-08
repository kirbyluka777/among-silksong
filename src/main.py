from engine import *
from starboard.scenes import *

setup = GameSetup("Coconut", [
    MainMenu(),
    GameConfig(),
    Expedition(),
    CreateTeam(),
    Options(),
    Stats(),
    BestStats(),
    TeamStats(),
    Wip(),
    Coconut()])

Game(setup).run()
