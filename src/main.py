from engine import *
from starboard.scenes import *
from starboard.logic import countries
from starboard.logic.countries import Country
from starboard import globals
import os

if not os.path.exists("data"):
    os.mkdir("data")

if not os.path.exists("reports"):
    os.mkdir("reports")

if not os.path.exists(countries.COUNTRY_FILE):
    countries.save_record(Country("USA", "Estados Unidos"))
    countries.save_record(Country("RUS", "Rusia"))
    countries.save_record(Country("VEN", "Venezuela"))
    globals.countries = countries.load_records()

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
