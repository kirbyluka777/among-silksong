import pygame as pg
from engine import *
from .. import resources
from ..inputs import PlayerInput

class GameConfig(Scene):
    def load(self, context):
        self.bg = pg.image.load(resources.images.MENU_BG)
        self.font = pygame.font.Font(resources.fonts.BEACH_BALL, 40)

    def start(self, context):
        self.input = PlayerInput(context)

        self.option_selected = 0
        self.difficulty = 0
        self.board_size = 9 # default
    
    def update(self, context):
        if self.input.is_up_button_down():
            self.option_selected = (self.option_selected - 1) % 2
        elif self.input.is_down_button_down():
            self.option_selected = (self.option_selected + 1) % 2

        if  self.input.is_left_button_down():
            if self.option_selected == 0:
                self.difficulty = (self.difficulty - 1) % 3
            elif self.option_selected == 1:
                min_size = 5
                self.board_size = (self.board_size - 1) % 20
                if self.board_size < 5: 
                    self.board_size = 19
        
        if self.input.is_right_button_down():
            if self.option_selected == 0:
                self.difficulty = (self.difficulty + 1) % 3
            elif self.option_selected == 1:
                self.board_size = (self.board_size + 1) % 20
                if self.board_size == 0:
                    self.board_size = 5
        
        if self.input.is_confirm_button_down():
            pass
            # empezar juego con los datos :v

    def draw(self, context):
        screen = context.get_screen()

        self.text_difficulty = self.font.render(f"Dificultad: {'facil' if self.difficulty == 0 else 'intermedio' if self.difficulty == 1 else 'avanzado'}", True, '#ffffff')
        self.text_size = self.font.render(f'Tamaño del mapa: {self.board_size}', True, '#ffffff')
        pg.draw.circle(screen, 'white', (screen.get_width() // 2 - self.text_difficulty.get_width() // 2 - 35 if self.option_selected == 0 else screen.get_width() // 2 - self.text_size.get_width() // 2 - 35, screen.get_height() // 3 + 60 * self.option_selected + 15), 10)
        screen.blit(self.text_difficulty, (screen.get_width() // 2 - self.text_difficulty.get_width() // 2, screen.get_height() // 3))
        screen.blit(self.text_size, (screen.get_width() // 2 - self.text_size.get_width() // 2, screen.get_height() // 3 + 50))

    def exit(self, context):
        pass
