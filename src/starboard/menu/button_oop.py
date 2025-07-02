import pygame as pg
from box import InputBox
from box import Button
import sys
import struct

# Initialize Pygame
pg.init()

BG = pg.image.load("src\\starboard\\menu\\sussy baka.png")
BG= pg.transform.scale(BG, (1600,900))
#play_button = pg.image.load("play_button.png")
#play_button = pg.transform.scale(play_button, (200,50))
# Screen dimensions
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
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

class Game:
    pass

class Team:
    def __init__(self, name, email, password):#, country, ods
        self.name = name # 20 caracteres
        self.email = email # 
        self.password = password


class TitleScreen:
    def __init__(self, game:Game):
        self.game = game
        self.global_x = SCREEN_WIDTH // 4
        self.global_y = SCREEN_HEIGHT // 2
        self.title_text = 'Among Silksong'

        self.title = pg.font.SysFont('Arial', 60).render(self.title_text,True,'#ffffff')

        self.button_play = Button((self.global_x,self.global_y), (200,50), GREEN, BRIGHT_GREEN,'Hola')
        self.button_registro = Button((self.global_x,self.global_y+80), (200,50), WHITE, GREEN, 'Registrar equpo', lambda: game.change_screen('registr')) #No se como cambiar pantalla
        self.button_options = Button((self.global_x,self.global_y+160), (200, 70), '#ffffff', '#00fdfd','OPCIONES')
        self.button_quit = Button((self.global_x,self.global_y+240), (200, 70), RED, BRIGHT_RED,"QUIT", lambda: game.quit_game())

        self.buttons = [self.button_play,
                        self.button_registro,
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
            new_team = Team(name,email,password)
            self.game.teams.append(new_team)
            save_binary('equipos.bin', new_team,'20s50s8s')
            print(f'registrado: {new_team.name}\n'
                  f'correo: {new_team.email}\n'
                  f'contrasena: {new_team.password}')
        else:
            print("No registrado")

def save_binary(file_name, data, format): # solo funciona para team claramente
    file = open(file_name,"ab")

    name = data.name.encode('utf-8')
    email = data.email.encode('utf-8')
    password = data.password.encode('utf-8')
    packed_data = struct.pack(format, name, email, password)
    
    file.write(packed_data)

    file.close()

def load_binary(file_name, game, format):
    size = struct.calcsize(format)
    NULL = '\x00'
    file = open(file_name, 'rb')
    while True:
        bytes = file.read(size)
        if not bytes:
            break
        
        name, email, password = struct.unpack(format, bytes)
        name = name.decode('utf-8').strip(NULL)
        email= email.decode('utf-8').strip(NULL)
        password.decode('utf-8').strip(NULL)
        game.teams.append(Team(name,email,password))

    file.close()

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True

        self.teams = []

        load_binary('equipos.bin',self,'20s50s8s')

        print(*(team.name for team in self.teams)) # amo la programacion orientada a objetos

        self.screens = {
            "title": TitleScreen(self),
            "registr": RegistroScreen(self)
            #"options": OptionsScreen(self), Volumen, opcion de agregar un pais
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