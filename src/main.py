from engine import *
from starboard.scenes import *
import os

if not os.path.exists("data"):
    os.mkdir("data")

if not os.path.exists("reports"):
    os.mkdir("reports")

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
    Top10Stats(),
    Credits(),
    Wip(),
    Coconut()])

Game(setup).run()
