from engine import *
from ..constants import *
from .. import globals
from .. import resources
from ..inputs import PlayerInput
from ..menu.box import DropDown
from ..logic.teams import Team

class GameConfig(Scene):
    def load(self, context):
        self.bg = pygame.image.load(resources.images.MENU_BG)
        self.font = pygame.font.Font(resources.fonts.BEACH_BALL, 40)
        self.teams1 = DropDown(["#696969", "#ffffff"],["#696969","#ffffff"], 100, 100, 150, 40,pygame.font.SysFont(None,32),
                              "Equipo 1",
                              list(t.name for t in globals.teams))
        self.teams2 = DropDown(["#696969", "#ffffff"],["#696969","#ffffff"], 300, 100, 150, 40,pygame.font.SysFont(None,32),
                              "Equipo 2",
                              list(t.name for t in globals.teams))

    def start(self, context):
        self.input = PlayerInput(context)
        
        self.selected_team1 = 0
        self.selected_team2 = 0
        self.option_selected = 0
        self.difficulty = BOARD_DIFFICULTY_EASY
        self.board_dir = BOARD_DIR_OCLOCK
        self.board_size = 0
    
    def update(self, context):
        events = context.get_events()
        self.selected_team1 = self.teams1.update(events)
        self.selected_team2 = self.teams2.update(events)
        
        if self.selected_team1 >=0:
            new_team = globals.teams[self.selected_team1]
            if new_team == globals.team2:
                print("not selected")
                globals.team2 = None
                self.teams1.main = "Equipo 1"
            else:
                print("valid")
                globals.team1 = new_team
                self.teams1.main = self.teams1.options[self.selected_team1]
                print(self.selected_team1)
        
        if self.selected_team2 >=0:
            new_team = globals.teams[self.selected_team2]
            if new_team == globals.team1:
                print("not selected")
                globals.team2 = None
                self.teams2.main = "Equipo 2"
                ...
            else:
                print("valid")
                globals.team2 = new_team
                self.teams2.main = self.teams2.options[self.selected_team2]
                print(self.selected_team2)

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
            if globals.team1 and globals.team2:
                context.scene.change(SCENE_EXPEDITION)
            else:
                print("Not team")

    def draw(self, context):
        screen = context.get_screen()

        self.teams1.draw(screen)
        self.teams2.draw(screen)
        self.text_difficulty = self.font.render(f"Dificultad: {'facil' if self.difficulty == 0 else 'intermedio' if self.difficulty == 1 else 'avanzado'}", True, '#ffffff')
        self.text_size = self.font.render(f'Tamaño del mapa: {5 + self.board_size * 2}', True, '#ffffff')
        self.text_dir = self.font.render(f'Sentido: {"Horario" if self.board_dir == BOARD_DIR_OCLOCK else "Antihorario"}', True, '#ffffff')
        pygame.draw.circle(screen, 'white', (screen.get_width() // 2 - self.text_difficulty.get_width() // 2 - 35 if self.option_selected == 0 else screen.get_width() // 2 - self.text_size.get_width() // 2 - 35, screen.get_height() // 3 + 60 * self.option_selected + 15), 10)
        screen.blit(self.text_difficulty, (screen.get_width() // 2 - self.text_difficulty.get_width() // 2, screen.get_height() // 3))
        screen.blit(self.text_size, (screen.get_width() // 2 - self.text_size.get_width() // 2, screen.get_height() // 3 + 50))
        screen.blit(self.text_dir, (screen.get_width() // 2 - self.text_dir.get_width() // 2, screen.get_height() // 3 + 100))

    def exit(self, context):
        pass
