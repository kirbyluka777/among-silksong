import random
from engine import *
from .. import resources
from ..inputs import PlayerInput
from ..logic.board import Board, generate_random_board, spiral_traversal_oclock, initial_pos_oclock
from ..constants import *

STATE_STRATEGY = 1
STATE_THROW_DICE = 2
STATE_USE_ITEM = 3
STATE_SHOW_MAP = 4
STATE_ACTION = 5
STATE_STATION = 6
STATE_OBSTACLE = 7
STATE_END_OF_TURN = 8
STATE_MINIGAME = 9

TURN_PLAYER_ONE = 1
TURN_PLAYER_TWO = 2

STRATEGY_OPTION_THROW_DICE = 0
STRATEGY_OPTION_USE_ITEM = 1
STRATEGY_OPTION_SHOW_MAP = 2
STRATEGY_OPTIONS = 3

PLAYER_COUNT = 2

class Expedition(Scene):
    def load(self, context: GameContext):
        # get from context
        screen_rect = context.get_screen_rect()

        self.spaceship_img = pygame.image.load(resources.images.SPACESHIP)
        self.blue_bg_img = pygame.image.load(resources.images.BLUE_BG)
        self.cell_dot_blue_img = pygame.image.load(resources.images.CELL_DOT_BLUE)

    def start(self, context: GameContext) -> None:
        # create controllers
        self.input = PlayerInput(context)

        self.state = StateMachineController(context, STATE_STRATEGY)

        self.dice_anim_timer = TimerController(context)
        self.action_anim_timer = TimerController(context)
        self.station_anim_timer = TimerController(context)
        self.obstacle_anim_timer = TimerController(context)
        self.end_of_turn_timer = TimerController(context)

        # init state
        self.option_selected = 0
        self.turn = TURN_PLAYER_ONE
        self.minigames = False
        self.insufficient = False
        self.dice_thrown = False
        self.position = [initial_pos_oclock() for i in range(PLAYER_COUNT)]
        self.items = [[f"Item {i}" for i in range(3)] for p in range(PLAYER_COUNT)]
        self.energy = [10 for i in range(PLAYER_COUNT)]
        self.immunity = [False for i in range(PLAYER_COUNT)]
        self.disabled = [False for i in range(PLAYER_COUNT)]
        self.max_energy = 10
        self.board = generate_random_board(9, 1, 0) #TODO: usar valores del formulario

        # play music
        pygame.mixer.music.load(resources.music.EXPEDITION_THEME)
        pygame.mixer.music.play(-1)

    def update(self, context: GameContext) -> None:
        if self.state.is_current(STATE_STRATEGY):
            if self.input.is_up_button_down():
                self.option_selected = (self.option_selected - 1) % STRATEGY_OPTIONS
            elif self.input.is_down_button_down():
                self.option_selected = (self.option_selected + 1) % STRATEGY_OPTIONS

            if self.input.is_confirm_button_down():
                if self.option_selected == STRATEGY_OPTION_THROW_DICE:
                    self.state.transition_to(STATE_THROW_DICE)
                elif self.option_selected == STRATEGY_OPTION_USE_ITEM:
                    self.state.transition_to(STATE_USE_ITEM)
                elif self.option_selected == STRATEGY_OPTION_SHOW_MAP:
                    self.state.transition_to(STATE_SHOW_MAP)
        
        elif self.state.is_current(STATE_THROW_DICE):
            if not self.dice_thrown:
                if self.input.is_cancel_button_down():
                    self.state.transition_to(STATE_STRATEGY)
                elif self.input.is_confirm_button_down():
                    self.dice_thrown = True
                    self.dice_anim_timer.start(3000)
            elif self.dice_anim_timer.has_finished:
                k = random.randint(1, 5)
                if self.energy[self.turn] - k >= 0:
                    self.state.transition_to(STATE_ACTION)
                else:
                    self.insufficient = True

        elif self.state.is_current(STATE_USE_ITEM):
            if self.state.is_entering:
                self.option_selected = 0

            if self.input.is_up_button_down():
                self.option_selected = (self.option_selected - 1) % len(items[self.turn])
            elif self.input.is_down_button_down():
                self.option_selected = (self.option_selected + 1) % len(items[self.turn])
                
            if self.input.is_confirm_button_down():
                pass #TODO: aplicar efectos de las cartas
            elif self.input.is_cancel_button_down():
                self.state.transition_to(STATE_STRATEGY)
        
        elif self.state.is_current(STATE_SHOW_MAP):
            if self.input.is_confirm_button_down() or self.input.is_cancel_button_down():
                self.state.transition_to(STATE_STRATEGY)
        
        elif self.state.is_current(STATE_ACTION):
            if self.state.is_entering:
                self.action_anim_timer.start(3000) #TODO: establecer duración real
            
            if self.action_anim_timer.has_finished:
                self.position[self.turn] = (0, 0) #TODO: implementar recorrido en espiral
                if self.board.is_cell_station_at(self.position[self.turn]):
                    self.state.transition_to(STATE_STATION)
                elif self.board.is_cell_obstacle_at(self.position[self.turn]):
                    self.state.transition_to(STATE_OBSTACLE)
                else:
                    self.state.transition_to(STATE_END_OF_TURN)
        
        elif self.state.is_current(STATE_STATION):
            if self.state.is_entering:
                self.station_anim_timer.start(3000) #TODO: establecer duración real
            
            if self.station_anim_timer.has_finished:
                if self.board.is_cell_at(self.position[self.turn], CELL_STATION_TITAN):
                    self.energy[self.turn] = min(self.energy[self.turn] + 10, self.max_energy)
                    self.state.transition_to(STATE_END_OF_TURN)
                elif self.board.is_cell_at(self.position[self.turn], CELL_STATION_SAKAAR):
                    self.k = 1 #TODO: calcular pasos para el siguiente sector desocupado
                    self.state.transition_to(STATE_ACTION)
                elif self.board.is_cell_at(self.position[self.turn], CELL_STATION_EGO):
                    self.state.transition_to(STATE_THROW_DICE)
                elif self.board.is_cell_at(self.position[self.turn], CELL_STATION_ASGARD):
                    self.immunity[self.turn] = True
                    self.state.transition_to(STATE_END_OF_TURN)
                elif self.board.is_cell_at(self.position[self.turn], CELL_STATION_XANDAR):
                    self.k = 1 #TODO: calcular pasos para la siguiente estación espacial
                    self.state.transition_to(STATE_ACTION)

        elif self.state.is_current(STATE_OBSTACLE):
            if self.state.is_entering:
                if self.immunity[self.turn]:
                    self.immunity[self.turn] = False
                    self.state.transition_to(STATE_END_OF_TURN)
                else:
                    self.obstacle_anim_timer.start(3000) #TODO: establecer duración real
            
            if self.obstacle_anim_timer.has_finished:
                if self.board.is_cell_at(self.position[self.turn], CELL_OBSTACLE_DEBRIS):
                    self.k = -1 #TODO: calcular pasos hacia atras para retroceder un sector
                    self.state.transition_to(STATE_ACTION)
                elif self.board.is_cell_at(self.position[self.turn], CELL_OBSTACLE_METEORITE):
                    self.disabled[self.turn] = True
                    self.state.transition_to(STATE_END_OF_TURN)
                elif self.board.is_cell_at(self.position[self.turn], CELL_OBSTACLE_ASTEROID):
                    self.energy[self.turn] = max(self.energy[self.turn] - 3, 0)
                    self.state.transition_to(STATE_END_OF_TURN)
                elif self.board.is_cell_at(self.position[self.turn], CELL_OBSTACLE_COSMIC_RAD):
                    self.energy[self.turn] = max(self.energy[self.turn] - 2, 0)
                    self.state.transition_to(STATE_END_OF_TURN)
                elif self.board.is_cell_at(self.position[self.turn], CELL_OBSTACLE_SOLAR_RAD):
                    self.k = 1 #TODO: calcular pasos hacia atras para retroceder al sector anterior en la diagonal secundaria
                    self.state.transition_to(STATE_ACTION)
        
        elif self.state.is_current(STATE_END_OF_TURN):
            if self.state.is_entering:
                self.end_of_turn_timer.start(3000)
            
            if self.end_of_turn_timer.has_finished:
                self.turn = (self.turn + 1) % PLAYER_COUNT
                self.insufficient = False
                self.option_selected = 0
                if self.turn == TURN_PLAYER_ONE and self.minigames:
                    self.state.transition_to(STATE_MINIGAME)
                else:
                    self.state.transition_to(STATE_STRATEGY)
        
        elif self.state.is_current(STATE_MINIGAME):
            if self.state.is_entering:
                self.state.transition_to(STATE_STRATEGY)

    def draw(self, context: GameContext) -> None:
        screen = context.get_screen()

        # draw board
        for i in range(0, 3, +1):
            for j in range(0, 3, +1):
                screen.blit(self.blue_bg_img, (i * 512, j * 512))
        for i in range(0, self.board.size, +1):
            for j in range(0, self.board.size, +1):
                cell = self.board.matrix[i][j]

                screen.blit(self.cell_dot_blue_img, (i * 108 + 108 // 2 - 16, j * 108 + 108 // 2 - 16))
                if cell > 0:
                    color = "red" if cell > 5 else "blue" if cell > 0 else "black"
                    pygame.draw.rect(screen, color, (i * 108, j * 108, 108, 108))

        # draw players
        for i in range(0, PLAYER_COUNT, +1):
            pos = self.position[i]
            coords = (pos.col * 108, pos.row * 108)
            screen.blit(self.spaceship_img, coords)

    def exit(self, context: GameContext):
        # stop music
        pygame.mixer.music.stop()
