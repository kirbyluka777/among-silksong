from engine import *
from starboard.scenes import *

setup = GameSetup("Coconut", [
    Intro(),
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
