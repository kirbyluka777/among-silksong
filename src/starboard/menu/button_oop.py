import pygame as pg
from box import InputBox,Button,Text
import sys
import os
import saveload
from team import Team,Game#,Country
import team
import re

# Initialize Pygame
pg.init()

BG = pg.image.load("assets\\images\\sussy baka.png")
BG= pg.transform.scale(BG, (1280,720))
#play_button = pg.image.load("play_button.png")
#play_button = pg.transform.scale(play_button, (200,50))
# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("AMONG US")

# Colors
WHITE = "#ffffff"
BLACK = "#000000"
GREEN = "#00ffff"
BRIGHT_GREEN = "#ff00ff"
RED = "#fdaf11"
BRIGHT_RED = "#213555"

BOX_WIDTH = 140
BOX_HEIGHT = 32



class TeamStatsScreen():
    def __init__(self,game:Game):
        self.game = game
        self.text = Text("Ingrese el codigo de un equipo para ver sus expediciones",(400,100),(140,32))
        self.input_id = InputBox((100, 200), (BOX_WIDTH, BOX_HEIGHT), 'Codigo de Equipo')
        self.button_back = Button((100,SCREEN_HEIGHT - 100), (140,32), WHITE, RED, 'Back', lambda: game.change_screen("estadisticas"))
        self.button_search = Button((250,200), (100,32), WHITE, RED, 'Buscar', self.id_input())
        self.input_boxes = [self.input_id]

    def handle_event(self, event):
        for box in self.input_boxes:
            box.handle_event(event)
        self.button_back.handle_event(event)
        self.button_search.handle_event(event)
    
    def draw(self, screen):
        screen.fill(WHITE)
        screen.blit(BG,(0,0))
        for box in self.input_boxes:
            box.draw(screen)
        self.button_back.draw(screen)
        self.button_search.draw(screen)
        self.text.draw(screen)

    def id_input(self):
        pass

class Top10Screen():
    def __init__(self,game:Game):
        self.game = game
        self.text = Text("Top 10 de las mejores expediciones",(400,100),(140,32))
        self.button_back = Button((100,SCREEN_HEIGHT - 100), (140,32), WHITE, RED, 'Back', lambda: game.change_screen("estadisticas"))

    def handle_event(self, event):
        self.button_back.handle_event(event)
    
    def draw(self, screen):
        screen.fill(WHITE)
        screen.blit(BG,(0,0))
        self.button_back.draw(screen)
        self.text.draw(screen)

    def id_input(self):
        pass
