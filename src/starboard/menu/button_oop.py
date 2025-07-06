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

class TitleScreen:
    def __init__(self, game:Game):
        self.game = game
        self.global_x = SCREEN_WIDTH // 4
        self.global_y = SCREEN_HEIGHT // 2
        self.title_text = 'Among Silksong'

        self.title = pg.font.SysFont('Arial', 60).render(self.title_text,True,'#ffffff')

        self.button_play = Button((self.global_x,self.global_y-80), (200,50), GREEN, BRIGHT_GREEN,'Hola')
        self.button_registro = Button((self.global_x,self.global_y), (200,50), WHITE, GREEN, 'Registrar equipo', lambda: game.change_screen('registr')) #No se como cambiar pantalla
        self.button_estadisticas = Button((self.global_x,self.global_y+80), (200,50), WHITE, GREEN,'Estadisticas', lambda: game.change_screen('estadisticas'))
        self.button_options = Button((self.global_x,self.global_y+160), (200, 70), '#ffffff', '#00fdfd','OPCIONES', lambda: game.change_screen('options'))
        self.button_quit = Button((self.global_x,self.global_y+240), (200, 70), RED, BRIGHT_RED,"QUIT", lambda: game.quit_game())

        self.buttons = [self.button_play,
                        self.button_registro,
                        self.button_estadisticas,
                        self.button_options,
                        self.button_quit]
    
    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def draw(self, screen):
        screen.fill(WHITE)
        screen.blit(BG,(0,0))
        screen.blit(self.title,(SCREEN_WIDTH//2,SCREEN_HEIGHT//4))
        for button in self.buttons:
            button.draw(screen)

class OptionScreen():
    def __init__(self,game:Game):
        self.pais = False
        self.game = game
        self.button_volume = Button((SCREEN_WIDTH//2,200), (140,32), WHITE, RED, 'Volumen')
        self.button_registrar = Button((SCREEN_WIDTH//2,250), (140,32), WHITE, RED, 'Registrar pais', self.toggle_countries)
        self.button_done = Button((SCREEN_WIDTH // 2 + 200,350), (140,32), WHITE, RED, 'Listo', self.register_country)
        self.button_back = Button((100,SCREEN_HEIGHT - 100), (140,32), WHITE, RED, 'Back', lambda: game.change_screen("title"))
        
        self.input_code = InputBox((SCREEN_WIDTH // 2 - 200,350), (BOX_WIDTH, BOX_HEIGHT), 'Codigo')
        self.input_name = InputBox((SCREEN_WIDTH // 2, 350), (BOX_WIDTH, BOX_HEIGHT), 'Nombre')

        self.buttons =[self.button_volume,
                       self.button_registrar,
                       self.button_back]

        self.input_boxes = [self.input_code,
                            self.input_name]

    def handle_event(self, event):
        for box in self.input_boxes:
            box.handle_event(event)
        for button in self.buttons:
            button.handle_event(event)
        if self.pais:
            self.button_done.handle_event(event)
    
    def draw(self, screen):
        screen.fill(WHITE)
        screen.blit(BG,(0,0))
        for button in self.buttons:
            button.draw(screen)
        if self.pais:
            for box in self.input_boxes:
                box.draw(screen)
            self.button_done.draw(screen)
    
    def toggle_countries(self):
        self.pais = False if self.pais else True
    
    def register_country(self):
        code  = self.input_code.text
        name = self.input_name.text

        if code and name:
            # countries=country.read_countries()
            # if (code in countries) or (name in countries):
            #     print("Pais ya existente")
            # else:
                new_country = Country(code,name)
                self.game.countries.append(new_country)
                saveload.save_country(new_country)
                print(f'registrado: {new_country.name}\n'
                    f'codigo: {new_country.code}')
        else:
            print("No registrado")
        self.toggle_countries()

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