import pygame as pg
from pygame import Surface
from pygame import font
import sys

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

class Button:
    def __init__(self, pos:tuple, dim:tuple, inactive_color:str, active_color:str, action=None, text:str='', image:Surface=None):
        """
        pos 0 = x
        pos 1 = y

        dim 0 = width
        dim 1 = height
        """
        self.image = image
        self.text = text
        self.rect = pg.Rect(pos[0],pos[1],dim[0],dim[1])
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.current_color = inactive_color
        self.action = action
        self.font = pg.font.SysFont('Arial', 40)

    def draw(self, surface):
        if self.image is not None:
            screen.blit(self.image, self.rect)
            
        text_surf = self.font.render(self.text, True, self.current_color)
        text_rect = text_surf.get_rect(center=self.rect.center)

        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        mouse_pos = pg.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.active_color
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.action:
                    self.action()
        else:
            self.current_color = self.inactive_color


def testtt():
    print("TEST")

def quit_game():
    pg.quit()
    sys.exit()


def title_screen():
    global_x = SCREEN_WIDTH // 4
    global_y = SCREEN_HEIGHT // 2
    title_text = 'Among Silksong'
    title = pg.font.SysFont('Arial', 60).render(title_text,True,'#ffffff')
    button_play = Button((global_x,global_y), (200,50), GREEN, BRIGHT_GREEN, testtt,'Hola')
    button_registro = Button((global_x,global_y+80), (200,50), WHITE, GREEN, registro_screen, 'Registrar equpo')
    button_options = Button((global_x,global_y+160), (200, 70), '#ffffff', '#00fdfd', testtt,'OPCIONES')
    button_quit = Button((global_x,global_y+240), (200, 70), RED, BRIGHT_RED, quit_game, "QUIT")

    buttons = [button_play,
            button_registro,
            button_options,
            button_quit]
    
    while True:
        screen.fill(WHITE)
        screen.blit(BG,(0,0))
        screen.blit(title,(SCREEN_WIDTH//2,SCREEN_HEIGHT//4))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_game()

            for button in buttons:
                button.handle_event(event)


        for button in buttons:
            button.draw(screen)

        pg.display.flip()

def registro_screen():
    
    # Variables &
    # Buttons
    button_back = Button((100,SCREEN_HEIGHT - 100), (140,32), WHITE, RED, title_screen, 'Back')

    buttons = [button_back] # List of buttons

    # Loop
    while True:
        screen.fill(WHITE)
        screen.blit(BG,(0,0))
        # screen.blit(object,(SCREEN_WIDTH//2,SCREEN_HEIGHT//4))
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_game()

            for button in buttons:
                button.handle_event(event)


        for button in buttons:
            button.draw(screen)

        pg.display.flip()


def blueprint():
    
    # Variables &
    # Buttons

    buttons = [] # List of buttons

    # Loop
    while True:
        screen.fill(WHITE)
        screen.blit(BG,(0,0))
        # screen.blit(object,(SCREEN_WIDTH//2,SCREEN_HEIGHT//4))
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_game()

            for button in buttons:
                button.handle_event(event)


        for button in buttons:
            button.draw(screen)

        pg.display.flip()

if __name__ == '__main__':
    title_screen()
    pg.quit()