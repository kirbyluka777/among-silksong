import pygame
import button_oop
from button_oop import Button,InputBox,Game
WHITE = "#ffffff"
BLACK = "#000000"
GREEN = "#00ffff"
BRIGHT_GREEN = "#ff00ff"
RED = "#fdaf11"
BRIGHT_RED = "#213555"

BOX_WIDTH = 140
BOX_HEIGHT = 32

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

BG = pygame.image.load("src\\starboard\\menu\\sussy baka.png")
BG= pygame.transform.scale(BG, (1280,720))
pygame.init()

class StatsScreen():
    def __init__(self,game:Game):
        self.game = game
        self.button_back = Button((100,SCREEN_HEIGHT - 100), (140,32), WHITE, RED, 'Back', lambda: game.change_screen("title"))
        self.button_registrar = Button((SCREEN_WIDTH//2,SCREEN_HEIGHT - 100), (140,32), WHITE, RED, 'Registrar', self.register_team)
        self.input_id = InputBox((100, 100), (BOX_WIDTH, BOX_HEIGHT), 'Codigo de Pais')

        self.input_boxes = [self.input_id]

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


    def id_input(self):
        id = self.input_name.text


if __name__ == '__main__':
    ga = Game()
    ga.run()
    pygame.quit()

