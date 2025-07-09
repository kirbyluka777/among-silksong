from engine import *
from starboard.scenes import *
import os

if not os.path.exists("data"):
    os.mkdir("data")

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
