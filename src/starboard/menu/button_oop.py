import pygame as pg
from box import InputBox,Button,Text
import sys
import os
import saveload
from team import Team,Game,Country
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

class BestStatsScreen():
    def __init__(self,game:Game):
        self.game = game
        self.text = Text("Ingrese el codigo de un pais para ver su mejor recorrido",(400,100),(140,32))
        self.input_id = InputBox((100, 200), (BOX_WIDTH, BOX_HEIGHT), 'Codigo de Pais')
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

class StatsScreen():
    def __init__(self,game:Game):
        self.game = game
        self.text = Text("Seleccione la opcion que desee ver",(400,100),(140,32))
        self.button_best_exp = Button((200,SCREEN_HEIGHT - 500), (140,70), WHITE, RED, 'Mejor expedicion de un pais', lambda: game.change_screen("mejor expedicion de pais"))
        self.button_team_exp = Button((200,SCREEN_HEIGHT - 400), (140,70), WHITE, RED, 'Expediciones de un equipo', lambda: game.change_screen("expediciones de equipo"))
        self.button_top10_exp = Button((160,SCREEN_HEIGHT - 300), (140,60), WHITE, RED, 'Top 10 expediciones', lambda: game.change_screen("top 10"))
        self.button_back = Button((100,SCREEN_HEIGHT - 100), (140,32), WHITE, RED, 'Back', lambda: game.change_screen("title"))

    def handle_event(self, event):
        self.button_back.handle_event(event)
        self.button_best_exp.handle_event(event)
        self.button_team_exp.handle_event(event)
        self.button_top10_exp.handle_event(event)


    def draw(self, screen):
        screen.fill(WHITE)
        screen.blit(BG,(0,0))
        self.button_best_exp.draw(screen)
        self.button_team_exp.draw(screen)
        self.button_top10_exp.draw(screen)
        self.button_back.draw(screen)
        self.text.draw(screen)

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


class RegistroScreen():
    def __init__(self,game:Game):
        self.game = game
        self.button_back = Button((100,SCREEN_HEIGHT - 100), (140,32), WHITE, RED, 'Back', lambda: game.change_screen("title"))
        self.button_registrar = Button((SCREEN_WIDTH//2,SCREEN_HEIGHT - 100), (140,32), WHITE, RED, 'Registrar', self.register_team)
        self.input_name = InputBox((100, 100), (BOX_WIDTH, BOX_HEIGHT), 'Nombre del equipo')
        self.input_email = InputBox((100,200), (BOX_WIDTH, BOX_HEIGHT), 'Correo electronico')
        self.input_password = InputBox((100, 300), (BOX_WIDTH, BOX_HEIGHT), 'Clave de acceso')

        self.input_boxes = [self.input_name,
                            self.input_email,
                            self.input_password]

    def handle_event(self, event):
        for box in self.input_boxes:
            box.handle_event(event)
        self.button_back.handle_event(event)
        self.button_registrar.handle_event(event)
    
    def draw(self, screen):
        screen.fill(WHITE)
        screen.blit(BG,(0,0))
        for box in self.input_boxes:
            box.draw(screen)
        self.button_back.draw(screen)
        self.button_registrar.draw(screen)


    def register_team(self):
        name = self.input_name.text
        email  = self.input_email.text
        password = self.input_password.text

        if name and email and password:
            password=team.verification(password)
            new_team = Team(name,email,password)
            self.game.teams.append(new_team)
            saveload.save_team(new_team)
            print(f'registrado: {new_team.name}\n'
                  f'correo: {new_team.email}\n'
                  f'contrasena: {new_team.password}')
            self.input_name.text = self.input_email.text = self.input_password.text = ''
            for box in self.input_boxes:
                box.txt_surface = pg.font.SysFont(None, 32).render(box.text, True, box.color)
        else:
            print("No registrado")

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True

        self.teams = []
        self.countries = []

        saveload.load_team(self)
        saveload.load_country(self)

        print(*(team.name for team in self.teams)) # amo la programacion orientada a objetos

        self.screens = {
            "title": TitleScreen(self),
            "registr": RegistroScreen(self),
            "options": OptionScreen(self),
            "estadisticas":StatsScreen(self),
            "mejor expedicion de pais":BestStatsScreen(self),
            "expediciones de equipo":TeamStatsScreen(self),
            "top 10":Top10Screen(self)
            #, Volumen, opcion de agregar un pais
            #"play": La pantalla en la que se van a elegir la configuracion de la partida
            #"tablero": La pantalla del propio juego
        }
        self.current_screen = self.screens["title"]

    def change_screen(self, screen_name):
        self.current_screen = self.screens[screen_name]

    def quit_game(self):
        self.running = False
    
    def save_game(self):
        pass

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit_game()
                self.current_screen.handle_event(event)

        
            self.current_screen.draw(self.screen)

            pg.display.flip()
            self.clock.tick(60)

        self.save_game()
        pg.quit()
        sys.exit()

if __name__ == '__main__':
    ga = Game()
    ga.run()
    pg.quit()