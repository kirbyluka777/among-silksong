import random
from engine import *
from .. import resources
from ..inputs import PlayerInput
from ..logic.board import Board, generate_random_board, spiral_traversal_oclock
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

        self.input = PlayerInput(context)

        self.state = StateMachineController(context, STATE_STRATEGY)

        self.action_anim_timer = TimerController(context)
        self.station_anim_timer = TimerController(context)
        self.obstacle_anim_timer = TimerController(context)

        self.option_selected = 0
        self.turn = TURN_PLAYER_ONE
        self.position = [(0, 0) for i in range(PLAYER_COUNT)]
        self.items = [[f"Item {i}" for i in range(3)] for p in range(PLAYER_COUNT)]
        self.energy = [10 for i in range(PLAYER_COUNT)]
        self.immunity = [False for i in range(PLAYER_COUNT)]
        self.max_energy = 10
        self.board = generate_random_board(9, 1, 0) #TODO: usar valores del formulario

    def start(self, context: GameContext) -> None:
        # init state
        self.paused_time_elapsed = 0
        self.time_elapsed = 0

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
        
        if self.state.is_current(STATE_THROW_DICE):
            pass
        
        if self.state.is_current(STATE_USE_ITEM):
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
        
        if self.state.is_current(STATE_SHOW_MAP):
            if self.input.is_confirm_button_down() or self.input.is_cancel_button_down():
                self.state.transition_to(STATE_STRATEGY)
        
        if self.state.is_current(STATE_ACTION):
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
        
        if self.state.is_current(STATE_STATION):
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

        if self.state.is_current(STATE_OBSTACLE):
            if self.state.is_entering:
                self.obstacle_anim_timer.start(3000) #TODO: establecer duración real
            
            if self.obstacle_anim_timer.has_finished:
                if self.board.is_cell_at(self.position[self.turn], CELL_OBSTACLE_DEBRIS):
                    self.energy[self.turn] = min(self.energy[self.turn] + 10, self.max_energy)
                    self.state.transition_to(STATE_END_OF_TURN)
                elif self.board.is_cell_at(self.position[self.turn], CELL_OBSTACLE_METEORITE):
                    self.k = 1 #TODO: calcular pasos para el siguiente sector desocupado
                    self.state.transition_to(STATE_ACTION)
                elif self.board.is_cell_at(self.position[self.turn], CELL_OBSTACLE_ASTEROID):
                    self.state.transition_to(STATE_THROW_DICE)
                elif self.board.is_cell_at(self.position[self.turn], CELL_OBSTACLE_COSMIC_RAD):
                    self.immunity[self.turn] = True
                    self.state.transition_to(STATE_END_OF_TURN)
                elif self.board.is_cell_at(self.position[self.turn], CELL_OBSTACLE_SOLAR_RAD):
                    self.k = 1 #TODO: calcular pasos para la siguiente estación espacial
                    self.state.transition_to(STATE_ACTION)

    def draw(self, context: GameContext) -> None:
        # get from context
        screen = context.get_screen()
        screen_rect = context.get_screen_rect()

        # draw wip image
        screen.blit(self.image_wip, (0, screen_rect.centery - self.image_wip.get_height() // 2))
        screen.blit(self.text_press_spacebar_anytime, (screen_rect.centerx - self.text_press_spacebar_anytime.get_width() // 2, screen_rect.bottom - self.text_press_spacebar_anytime.get_height() - 20))
        
        # draw elapsed time counter
        seconds_text = self.font_main.render("You've been in here for {} seconds".format(int(self.time_elapsed)), False, "white")
        screen.blit(seconds_text, (screen_rect.centerx - seconds_text.get_width() // 2, screen_rect.bottom - seconds_text.get_height() - 50))
        
        # draw paused elapsed time counter
        if context.is_paused():
            paused_seconds_text = self.font_main.render("You've been paused for {} seconds".format(int(self.paused_time_elapsed)), False, "white")
            screen.blit(paused_seconds_text, (screen_rect.centerx - seconds_text.get_width() // 2, screen_rect.bottom - seconds_text.get_height() - 80))

    def exit(self, context: GameContext):
        # stop music
        pygame.mixer.music.stop()
