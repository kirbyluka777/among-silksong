import random
from engine import *
from .. import resources
from ..inputs import PlayerInput
from ..logic.board import Board, generate_random_board, spiral_traversal, initial_pos_oclock
from ..menu.team import Team
from ..constants import *
from..logic.items import Item

STATE_STRATEGY = 0
STATE_THROW_DICE = 1
STATE_USE_ITEM = 2
STATE_SHOW_MAP = 3
STATE_ACTION = 4
STATE_STATION = 5
STATE_OBSTACLE = 6
STATE_END_OF_TURN = 7
STATE_MINIGAME = 8

TURN_PLAYER_ONE = 0
TURN_PLAYER_TWO = 1

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
        self.dice = [
            pygame.image.load(resources.images.DICE_1),
            pygame.image.load(resources.images.DICE_2),
            pygame.image.load(resources.images.DICE_3),
            pygame.image.load(resources.images.DICE_4),
            pygame.image.load(resources.images.DICE_5),
            pygame.image.load(resources.images.DICE_6)
        ]
        self.team_pfp = [
            pygame.image.load(resources.images.SUS_1),
            pygame.image.load(resources.images.SUS_2)
        ]
        self.teams = [
            Team("Estados Unidos", "administration@gov.us", "XXX"),
            Team("Rusia", "administration@gov.ru", "XXX")
        ]
        for i in range(0, len(self.team_pfp)):
            self.team_pfp[i] = pygame.transform.scale(self.team_pfp[i], (64, 64))
        
        self.energy_icon_img = pygame.image.load(resources.images.ICON_ENERGY)
        self.energy_icon_img = pygame.transform.scale(self.energy_icon_img, (32, 32))
        
        self.shield_icon_img = pygame.image.load(resources.images.ICON_SHIELD)
        self.shield_icon_img = pygame.transform.scale(self.shield_icon_img, (32, 32))

        self.menu_font = pygame.font.Font(resources.fonts.BEACH_BALL, 24)

        self.text_throw_dice = self.menu_font.render(resources.locale.THROW_DICE, True, "white")
        self.text_throw_dice_sel = self.menu_font.render(resources.locale.THROW_DICE, True, resources.colors.ui_text_primary)

        self.text_use_item = self.menu_font.render(resources.locale.USE_ITEM, True, "white")
        self.text_use_item_sel = self.menu_font.render(resources.locale.USE_ITEM, True, resources.colors.ui_text_primary)

        self.text_show_board = self.menu_font.render(resources.locale.SHOW_BOARD, True, "white")
        self.text_show_board_sel = self.menu_font.render(resources.locale.SHOW_BOARD, True, resources.colors.ui_text_primary)

        self.text_player_turn = [
            self.menu_font.render(resources.locale.PLAYER_TURN_FMT.format(i + 1), True, resources.colors.ui_text_primary) for i in range(0, PLAYER_COUNT)
        ]
        self.text_state = [
            self.menu_font.render(resources.locale.STATE_STRATEGY_MSG, True, resources.colors.ui_text_primary),
            self.menu_font.render(resources.locale.STATE_THROW_DICE_MSG, True, resources.colors.ui_text_primary),
            self.menu_font.render(resources.locale.STATE_USE_ITEM_MSG, True, resources.colors.ui_text_primary),
            self.menu_font.render(resources.locale.STATE_SHOW_MAP_MSG, True, resources.colors.ui_text_primary),
            self.menu_font.render(resources.locale.STATE_ACTION_MSG, True, resources.colors.ui_text_primary),
            self.menu_font.render(resources.locale.STATE_STATION_MSG, True, resources.colors.ui_text_primary),
            self.menu_font.render(resources.locale.STATE_OBSTACLE_MSG, True, resources.colors.ui_text_primary),
            self.menu_font.render(resources.locale.STATE_END_OF_TURN_MSG, True, resources.colors.ui_text_primary),
            self.menu_font.render(resources.locale.STATE_MINIGAME_MSG, True, resources.colors.ui_text_primary),
        ]

    def start(self, context: GameContext) -> None:
        # create controllers
        self.input = PlayerInput(context)

        self.state = StateMachineController(context, STATE_STRATEGY)
        
        self.dice_rolling_timer = TimerController(context)
        self.dice_thrown_timer = TimerController(context)
        self.action_anim_timer = TimerController(context)
        self.station_anim_timer = TimerController(context)
        self.obstacle_anim_timer = TimerController(context)
        self.end_of_turn_timer = TimerController(context)

        # init state
        self.option_selected = 0
        self.turn = TURN_PLAYER_ONE
        self.minigames = False
        self.insufficient = False
        self.dice_result = 0
        self.position = [initial_pos_oclock() for i in range(PLAYER_COUNT)]
        self.items = [[Item('More energy', 'fills up  yiur energy') for i in range(10)] for p in range(PLAYER_COUNT)]
        self.max_energy = 15
        self.energy = [self.max_energy for i in range(PLAYER_COUNT)]
        self.immunity = [False for i in range(PLAYER_COUNT)]
        self.disabled = [False for i in range(PLAYER_COUNT)]
        self.board = generate_random_board(9, 1, 0) #TODO: usar valores del formulario
        self.camera_pos = (0, 0)

        # play music
        pygame.mixer.music.load(resources.music.EXPEDITION_THEME)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def update(self, context: GameContext) -> None:
        self.state.init_update()

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
            if self.state.is_entering:
                self.dice_result = 0
                self.dice_thrown_timer.reset()
                self.dice_rolling_timer.start(50)

            if not self.dice_thrown_timer.has_started:
                if self.dice_rolling_timer.has_finished:
                    self.dice_result = random.randint(1, 5)
                    self.dice_rolling_timer.start(50)
                if self.input.is_cancel_button_down():
                    self.state.transition_to(STATE_STRATEGY)
                elif self.input.is_confirm_button_down():
                    self.dice_thrown_timer.start(2000)
            elif self.dice_thrown_timer.has_finished:
                if self.energy[self.turn] - self.dice_result >= 0:
                    self.energy[self.turn] -= self.dice_result
                    self.state.transition_to(STATE_ACTION)
                else:
                    self.insufficient = True
                    self.state.transition_to(STATE_END_OF_TURN)

        elif self.state.is_current(STATE_USE_ITEM):
            if self.state.is_entering:
                self.option_selected = 0

            if self.input.is_left_button_down():
                self.option_selected = (self.option_selected - 1) % len(self.items[self.turn]) if self.items[self.turn] else 0
            elif self.input.is_right_button_down():
                self.option_selected = (self.option_selected + 1) % len(self.items[self.turn]) if self.items[self.turn] else 0
                
            if self.input.is_confirm_button_down():
                if self.items[self.turn]:
                    print(self.items[self.turn][self.option_selected].print_item_data())
                    self.items[self.turn].pop(self.option_selected)
                    self.option_selected -= 1 if self.option_selected > 1 else 0
            elif self.input.is_cancel_button_down():
                self.option_selected = 1
                self.state.transition_to(STATE_STRATEGY)
        
        elif self.state.is_current(STATE_SHOW_MAP):
            if self.input.is_confirm_button_down() or self.input.is_cancel_button_down():
                self.option_selected = 2
                self.state.transition_to(STATE_STRATEGY)
        
        elif self.state.is_current(STATE_ACTION):
            if self.state.is_entering:
                self.action_anim_timer.start(500)
            
            if self.dice_result != 0 and self.action_anim_timer.has_finished:
                if self.dice_result > 0:
                    spiral_traversal(self.board, self.position[self.turn], +1)
                    self.dice_result -= 1
                else:
                    spiral_traversal(self.board, self.position[self.turn], -1)
                    self.dice_result += 1
                self.action_anim_timer.start(500)

            if self.dice_result == 0  and self.action_anim_timer.has_finished:
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
                    while not self.board.is_cell_at(self.position[self.turn], CELL_SPACE):
                        spiral_traversal(self.board, self.position[self.turn], 1)
                    self.state.transition_to(STATE_END_OF_TURN) #TODO: calcular pasos para el siguiente sector desocupado
                elif self.board.is_cell_at(self.position[self.turn], CELL_STATION_EGO):
                    self.state.transition_to(STATE_THROW_DICE)
                elif self.board.is_cell_at(self.position[self.turn], CELL_STATION_ASGARD):
                    self.immunity[self.turn] = True
                    self.state.transition_to(STATE_END_OF_TURN)
                elif self.board.is_cell_at(self.position[self.turn], CELL_STATION_XANDAR):
                    self.dice_result = 1 #TODO: calcular pasos para la siguiente estación espacial
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
                    print("debris")
                    while not self.board.is_cell_at(self.position[self.turn], CELL_SPACE):
                        spiral_traversal(self.board, self.position[self.turn], -1) #TODO: calcular pasos hacia atras para retroceder un sector
                    self.state.transition_to(STATE_END_OF_TURN)
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
                    self.dice_result = -1 #TODO: calcular pasos hacia atras para retroceder al sector anterior en la diagonal secundaria
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

        self.current_player_pos = self.position[self.turn]
        self.camera_pos = (self.current_player_pos.col * 108 + 54, self.current_player_pos.row * 108 + 54)

        self.state.finish_update()

    def draw(self, context: GameContext) -> None:
        screen = context.get_screen()

        # draw board
        for i in range(0, 3, +1):
            for j in range(0, 3, +1):
                screen.blit(self.blue_bg_img, (i * 512, j * 512))
        for i in range(0, self.board.size, +1):
            for j in range(0, self.board.size, +1):
                cell = self.board.matrix[i][j]
                if cell > 0:
                    color = "red" if cell > 5 else "blue" if cell > 0 else "black"
                    coords = self.coords_by_camera(screen, (j * 108, i * 108))
                    pygame.draw.rect(screen, color, (coords[0], coords[1], 108, 108))
                coords = self.coords_by_camera(screen, (j * 108 + 108 // 2 - 16, i * 108 + 108 // 2 - 16))
                screen.blit(self.cell_dot_blue_img, coords)

        # draw players
        for i in range(0, PLAYER_COUNT, +1):
            pos = self.position[i]
            offset_x = 27 if i == TURN_PLAYER_ONE else -27
            offset_y = -27 if i == TURN_PLAYER_ONE else 27
            coords = self.coords_by_camera(screen, (pos.col * 108 + offset_x, pos.row * 108 + offset_y))
            screen.blit(self.spaceship_img, coords)
        
        # draw dice
        if self.state.is_current(STATE_THROW_DICE):
            dice = self.dice[self.dice_result - 1]
            dice_width = dice.get_width()
            if not self.dice_thrown_timer.has_started or self.dice_thrown_timer.ticks_elapsed // 250 % 2 == 0 and self.dice_thrown_timer.ticks_elapsed < 2000:
                screen.blit(dice, (screen.get_width() // 2 - dice_width // 2, screen.get_height() * 3/4 - dice.get_height() // 2))

        # draw turn indicator
        turn_text = self.text_player_turn[self.turn]
        turn_text_box_width = turn_text.get_width() + 50 * 2
        pygame.draw.rect(screen, "white", (screen.get_width() // 2 - turn_text_box_width // 2, 0, turn_text_box_width, 32), border_bottom_left_radius=10, border_bottom_right_radius=10)
        screen.blit(turn_text, (screen.get_width() // 2 - turn_text.get_width() // 2, 4))

        # draw state indicator
        state_text = self.text_state[self.state.current_state]
        state_text_box_width = state_text.get_width() + 50 * 2
        pygame.draw.rect(screen, "white", (screen.get_width() // 2 - state_text_box_width // 2, screen.get_height() - 32, state_text_box_width, 32), border_top_left_radius=10, border_top_right_radius=10)
        screen.blit(state_text, (screen.get_width() // 2 - state_text.get_width() // 2, screen.get_height() - state_text.get_height()))

        # draw players hud
        player_top_left = [
            (50, 50),  # top left corner
            (50, screen.get_width() - 300),  # top right corner
        ]
        for i in range(0, PLAYER_COUNT, +1):
            (top, left) = player_top_left[i]
            player_name = self.teams[i].name
            player_energy = self.energy[i]
            player_immunity = self.immunity[i]
            player_disabled = self.disabled[i]
            player_pfp = self.team_pfp[i]
            screen.blit(player_pfp, (left, top))
            player_name_text = self.menu_font.render(player_name, True, "white")
            screen.blit(player_name_text, (left + 64 + 8, top + 4))
            screen.blit(self.energy_icon_img, (left + 64 + 8, top + 32))
            energy_text = self.menu_font.render(f"{player_energy} / {self.max_energy}", True, "white")
            screen.blit(energy_text, (left + 64 + 8 + 32 + 8, top + 32))
            energy_bar_width = player_energy * 64 / self.max_energy
            pygame.draw.rect(screen, "red", (left + 64 + 8 + 32 + 8, top + 56, 64, 8))
            pygame.draw.rect(screen, "green", (left + 64 + 8 + 32 + 8, top + 56, energy_bar_width, 8))
            if player_immunity:
                screen.blit(self.shield_icon_img, (left + 40, top + 40))

        # draw menu
        if self.state.is_current(STATE_STRATEGY):
            left = 300
            top = 400
            row = 40
            row_margin_top = 4
            row_margin_left = 10
            pygame.draw.rect(screen, resources.colors.ui_bg_primary, (left - 4, top - 4, 200 + 8, row * 3), border_radius=10)
            pygame.draw.rect(screen, "white", (left, top + row * self.option_selected, 200, 32), border_radius=10)
            screen.blit(self.text_throw_dice_sel if self.option_selected == 0 else self.text_throw_dice, (left + row_margin_left, top + row_margin_top))
            screen.blit(self.text_use_item_sel if self.option_selected == 1 else self.text_use_item, (left + row_margin_left, top + row + row_margin_top))
            screen.blit(self.text_show_board_sel if self.option_selected == 2 else self.text_show_board, (left + row_margin_left, top + row * 2 + row_margin_top))

        if self.state.is_current(STATE_THROW_DICE):
            pass

        if self.state.is_current(STATE_USE_ITEM):
            item_cols = self.option_selected % 5
            item_rows = self.option_selected // 5
            pygame.draw.rect(screen, "#b9b9b9", (200 + 30 * item_cols - 16, 400 + 30 * item_rows - 16,32,32))
            for i, _ in enumerate(self.items[self.turn]):
                item_cols = i % 5
                item_rows = i // 5
                pygame.draw.circle(screen, '#ffffff', (200 + 30 * item_cols, 400 + 30 * item_rows), 10)

        if self.state.is_current(STATE_SHOW_MAP):
            for i in range(0, self.board.size, +1):
                for j in range(0, self.board.size, +1):
                    cell = self.board.matrix[i][j]
                    if cell > 0:
                        color = "red" if cell > 5 else "blue" if cell > 0 else "black"
                        pygame.draw.rect(screen, color, (j * 32 +50, i * 32+400, 32, 32))

    def exit(self, context: GameContext):
        # stop music
        pygame.mixer.music.stop()

    def coords_by_camera(self, screen: pygame.Surface, coords: tuple[int, int]) -> tuple[int, int]:
        x = self.camera_pos[0] - screen.get_width() // 2
        y = self.camera_pos[1] - screen.get_height() // 2
        new_coords = (coords[0] - x, coords[1] - y)
        return new_coords
