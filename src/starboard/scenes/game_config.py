from engine import *
from ..constants import *
from .. import globals
from .. import resources
from ..inputs import PlayerInput

class GameConfig(Scene):
    def load(self, context):
        self.bg = pygame.image.load(resources.images.DIFFICULTY_BG)
        self.font = pygame.font.Font(resources.fonts.BEACH_BALL, 40)
        self.button_sound_sel = pygame.mixer.Sound(resources.sounds.BUTTON_SEL)
        self.button_sound_pressed = pygame.mixer.Sound(resources.sounds.BUTTON_PRESSED)

    def start(self, context):
        pygame.mixer.music.load(resources.music.SETTING_DIFFICULTY)
        pygame.mixer.music.play(-1)
        self.input = PlayerInput(context)
        self.option_selected = 0
        self.difficulty = BOARD_DIFFICULTY_EASY
        self.board_dir = BOARD_DIR_OCLOCK
        self.board_size = 0
    
    def update(self, context):
        if self.input.is_up_button_down():
            self.option_selected = (self.option_selected - 1) % 3
        elif self.input.is_down_button_down():
            self.option_selected = (self.option_selected + 1) % 3

        if  self.input.is_left_button_down():
            if self.option_selected == 0:
                self.difficulty = (self.difficulty - 1) % 3
            elif self.option_selected == 1:
                self.board_size = (self.board_size - 1) % 8
            elif self.option_selected == 2:
                self.board_dir = (self.board_dir - 1) % 2
        
        if self.input.is_right_button_down():
            if self.option_selected == 0:
                self.difficulty = (self.difficulty + 1) % 3
            elif self.option_selected == 1:
                self.board_size = (self.board_size + 1) % 8
            elif self.option_selected == 2:
                self.board_dir = (self.board_dir + 1) % 2
        
        if self.input.is_confirm_button_down():
            globals.board_size = 5 + self.board_size * 2
            globals.board_difficulty = self.difficulty
            globals.board_dir = self.board_dir
            context.scene.change(SCENE_EXPEDITION)

    def draw(self, context):
        screen = context.get_screen()

        self.text_difficulty = self.font.render(f"Dificultad: {'facil' if self.difficulty == 0 else 'intermedio' if self.difficulty == 1 else 'avanzado'}", True, '#ffffff')
        self.text_size = self.font.render(f'Tamaño del mapa: {5 + self.board_size * 2}', True, '#ffffff')
        self.text_dir = self.font.render(f'Sentido: {"Horario" if self.board_dir == BOARD_DIR_OCLOCK else "Antihorario"}', True, '#ffffff')
        pygame.draw.circle(screen, 'white', (screen.get_width() // 2 - self.text_difficulty.get_width() // 2 - 35 if self.option_selected == 0 else screen.get_width() // 2 - self.text_size.get_width() // 2 - 35, screen.get_height() // 3 + 60 * self.option_selected + 15), 10)
        screen.blit(self.text_difficulty, (screen.get_width() // 2 - self.text_difficulty.get_width() // 2, screen.get_height() // 3))
        screen.blit(self.text_size, (screen.get_width() // 2 - self.text_size.get_width() // 2, screen.get_height() // 3 + 50))
        screen.blit(self.text_dir, (screen.get_width() // 2 - self.text_dir.get_width() // 2, screen.get_height() // 3 + 100))

    def exit(self, context):
        pygame.mixer.music.stop()
        pass
