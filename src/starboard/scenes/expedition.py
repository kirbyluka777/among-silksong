import random
from engine import *
from ..constants import *
from .. import resources
from ..inputs import PlayerInput
from ..logic import board
from ..menu.team import Team
from .. import globals
from..logic.items import Item
from ..logic import expeditions
from ..logic import details

STATE_DRAFT = 0
STATE_STRATEGY = 1
STATE_THROW_DICE = 2
STATE_USE_ITEM = 3
STATE_SHOW_BOARD = 4
STATE_ACTION = 5
STATE_STATION = 6
STATE_OBSTACLE = 7
STATE_END_OF_TURN = 8
STATE_MINIGAME = 9

TURN_PLAYER_ONE = 0
TURN_PLAYER_TWO = 1

STRATEGY_OPTION_THROW_DICE = 0
STRATEGY_OPTION_USE_ITEM = 1
STRATEGY_OPTION_SHOW_MAP = 2
STRATEGY_OPTIONS = 3

PLAYER_COUNT = 2

TILE_SIZE = 128

class Expedition(Scene):
    def load(self, context: GameContext):
        # get from context
        screen_rect = context.get_screen_rect()

        self.team_spaceship_img = [pygame.image.load(resources.images.SPACESHIP) for i in range(PLAYER_COUNT)]
        self.team_spaceship_img[TURN_PLAYER_ONE].fill("red", special_flags=pygame.BLEND_ADD)
        self.team_spaceship_img[TURN_PLAYER_TWO].fill("blue", special_flags=pygame.BLEND_ADD)
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
        
        self.disabled_icon_img = pygame.image.load(resources.images.ICON_DISABLED)
        self.disabled_icon_img = pygame.transform.scale(self.disabled_icon_img, (32, 32))

        self.home_img = pygame.image.load(resources.images.CELL_HOME)
        self.home_img = pygame.transform.scale(self.home_img, (TILE_SIZE, TILE_SIZE))
        self.end_img = pygame.image.load(resources.images.CELL_END)
        self.end_img = pygame.transform.scale(self.end_img, (TILE_SIZE, TILE_SIZE))
        self.station_imgs = [
            pygame.image.load(resources.images.CELL_STATION_TITAN),
            pygame.image.load(resources.images.CELL_STATION_SAKAAR),
            pygame.image.load(resources.images.CELL_STATION_EGO),
            pygame.image.load(resources.images.CELL_STATION_ASGARD),
            pygame.image.load(resources.images.CELL_STATION_XANDAR),
        ]
        for i in range(0, len(self.station_imgs), +1):
            self.station_imgs[i] = pygame.transform.scale(self.station_imgs[i], (TILE_SIZE, TILE_SIZE))
        self.obstacle_imgs = [
            pygame.image.load(resources.images.CELL_OBSTACLE_DEBRIS),
            pygame.image.load(resources.images.CELL_OBSTACLE_METEORITE),
            pygame.image.load(resources.images.CELL_OBSTACLE_ASTEROID),
            pygame.image.load(resources.images.CELL_OBSTACLE_COSMIC_RAD),
            pygame.image.load(resources.images.CELL_OBSTACLE_SOLAR_RAD),
        ]
        for i in range(0, len(self.obstacle_imgs), +1):
            self.obstacle_imgs[i] = pygame.transform.scale(self.obstacle_imgs[i], (TILE_SIZE, TILE_SIZE))

        self.img_key_icon_z = pygame.image.load(resources.images.KEY_ICON_Z)
        self.img_key_icon_z = pygame.transform.scale(self.img_key_icon_z, (32, 32))
        self.img_key_icon_m = pygame.image.load(resources.images.KEY_ICON_M)
        self.img_key_icon_m = pygame.transform.scale(self.img_key_icon_m, (32, 32))

        self.menu_font = pygame.font.Font(resources.fonts.BEACH_BALL, 24)

        self.text_press = self.menu_font.render(resources.locale.PRESS, True, resources.colors.ui_text_primary)

        self.text_throw_dice = self.menu_font.render(resources.locale.THROW_DICE, True, "white")
        self.text_throw_dice_sel = self.menu_font.render(resources.locale.THROW_DICE, True, resources.colors.ui_text_primary)

        self.text_use_item = self.menu_font.render(resources.locale.USE_ITEM, True, "white")
        self.text_use_item_sel = self.menu_font.render(resources.locale.USE_ITEM, True, resources.colors.ui_text_primary)

        self.text_show_board = self.menu_font.render(resources.locale.SHOW_BOARD, True, "white")
        self.text_show_board_sel = self.menu_font.render(resources.locale.SHOW_BOARD, True, resources.colors.ui_text_primary)

        self.text_skipped_turn = self.menu_font.render(resources.locale.SKIPPED_TURN, True, resources.colors.ui_text_primary)
        self.text_not_enough_energy = self.menu_font.render(resources.locale.NOT_ENOUGH_ENERGY, True, resources.colors.ui_text_primary)
        self.text_repeat_draft = self.menu_font.render(resources.locale.REPEAT_DRAFT, True, resources.colors.ui_text_primary)

        self.text_player_turn = [
            self.menu_font.render(resources.locale.TURN_OF_PLAYER_FMT.format(self.teams[i].name), True, resources.colors.ui_text_primary) for i in range(0, PLAYER_COUNT)
        ]
        self.text_team_name = [
            self.menu_font.render(self.teams[i].name, True, "white") for i in range(0, PLAYER_COUNT)
        ]
        self.text_team_name_primary = [
            self.menu_font.render(self.teams[i].name, True, resources.colors.ui_text_primary) for i in range(0, PLAYER_COUNT)
        ]
        self.text_draft_to_team = [
            self.menu_font.render(resources.locale.DRAFT_TO_PLAYER_FMT.format(self.teams[i].name), True, resources.colors.ui_text_primary) for i in range(0, PLAYER_COUNT)
        ]

        self.text_state = [
            self.menu_font.render(resources.locale.STATE_DRAFT_MSG, True, resources.colors.ui_text_primary),
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

        self.text_indices = [self.menu_font.render(str(i + 1), True, "white") for i in range(globals.board_size**2)]

        self.text_station_name = [
            self.menu_font.render(resources.locale.CELL_STATION_TITAN_NAME, True, "white"),
            self.menu_font.render(resources.locale.CELL_STATION_SAKAAR_NAME, True, "white"),
            self.menu_font.render(resources.locale.CELL_STATION_EGO_NAME, True, "white"),
            self.menu_font.render(resources.locale.CELL_STATION_ASGARD_NAME, True, "white"),
            self.menu_font.render(resources.locale.CELL_STATION_XANDAR_NAME, True, "white"),
        ]
        self.text_station_description = [
            self.menu_font.render(resources.locale.CELL_STATION_TITAN_DESCRIPTION, True, resources.colors.ui_text_primary),
            self.menu_font.render(resources.locale.CELL_STATION_SAKAAR_DESCRIPTION, True, resources.colors.ui_text_primary),
            self.menu_font.render(resources.locale.CELL_STATION_EGO_DESCRIPTION, True, resources.colors.ui_text_primary),
            self.menu_font.render(resources.locale.CELL_STATION_ASGARD_DESCRIPTION, True, resources.colors.ui_text_primary),
            self.menu_font.render(resources.locale.CELL_STATION_XANDAR_DESCRIPTION, True, resources.colors.ui_text_primary),
        ]

        self.text_obstacle = [
            self.menu_font.render(resources.locale.CELL_OBSTACLE_DEBRIS_NAME, True, "white"),
            self.menu_font.render(resources.locale.CELL_OBSTACLE_METEORITE_NAME, True, "white"),
            self.menu_font.render(resources.locale.CELL_OBSTACLE_ASTEROID_NAME, True, "white"),
            self.menu_font.render(resources.locale.CELL_OBSTACLE_COSMIC_RAD_NAME, True, "white"),
            self.menu_font.render(resources.locale.CELL_OBSTACLE_SOLAR_RAD_NAME, True, "white"),
        ]
        self.text_obstacle_description = [
            self.menu_font.render(resources.locale.CELL_OBSTACLE_DEBRIS_DESCRIPTION, True, resources.colors.ui_text_primary),
            self.menu_font.render(resources.locale.CELL_OBSTACLE_METEORITE_DESCRIPTION, True, resources.colors.ui_text_primary),
            self.menu_font.render(resources.locale.CELL_OBSTACLE_ASTEROID_DESCRIPTION, True, resources.colors.ui_text_primary),
            self.menu_font.render(resources.locale.CELL_OBSTACLE_COSMIC_RAD_DESCRIPTION, True, resources.colors.ui_text_primary),
            self.menu_font.render(resources.locale.CELL_OBSTACLE_SOLAR_RAD_DESCRIPTION, True, resources.colors.ui_text_primary),
        ]

    def start(self, context: GameContext):
        # Crear controladores de lógica
        self.input = PlayerInput(context)

        self.state = StateMachineController(context, STATE_DRAFT)

        self.dice_rolling_timer = TimerController(context)
        self.draft_completed_timer = TimerController(context)
        self.dice_thrown_timer = TimerController(context)
        self.action_anim_timer = TimerController(context)
        self.station_anim_timer = TimerController(context)
        self.obstacle_anim_timer = TimerController(context)
        self.end_of_turn_timer = TimerController(context)

        # Inicializar estado
        self.board = board.generate_random_board(globals.board_size, globals.board_difficulty, globals.board_dir)
        self.option_selected = 0
        self.turn = None
        self.minigames = False
        self.insufficient = False
        self.disabled_now = False
        self.free_dice = False
        self.dice_result = [0 for _ in range(PLAYER_COUNT)]
        self.position = [board.initial_pos(self.board) for _ in range(PLAYER_COUNT)]
        self.items = [[Item('More energy', 'Fills up  your energy') for _ in range(10)] for _ in range(PLAYER_COUNT)]
        self.max_energy = 15
        self.initial_energy = random.randint(5, self.max_energy)
        self.energy = [self.initial_energy for i in range(PLAYER_COUNT)]
        self.immunity = [False for _ in range(PLAYER_COUNT)]
        self.disabled = [False for _ in range(PLAYER_COUNT)]
        self.draft_ready = [False for _ in range(PLAYER_COUNT)]
        self.camera_pos = (0, 0)

        # Crear archivo de expedicion
        self.expedition_id = expeditions.save_expedition(self.teams[TURN_PLAYER_ONE].name,
                                    self.teams[TURN_PLAYER_TWO].name,
                                    self.board.size,
                                    self.board.difficulty,
                                    self.board.dir)

        # Reproducir música
        pygame.mixer.music.load(resources.music.EXPEDITION_THEME)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def update(self, context: GameContext):
        keys_down = context.get_keys_down()
        self.state.init_update()

        # Estado de selección de primer turno
        if self.state.is_current(STATE_DRAFT):
            # Inicializar estado
            if self.state.is_entering:
                self.draft_completed_timer.reset()

            player_key = [pygame.K_z, pygame.K_m] # teclas de cada jugador para capturar dado

            # Mientras no esté completado el draft
            if not self.draft_completed_timer.has_started:
                # Intentar capturar el dado del jugador si no ha presionado aún
                for i in range(0, PLAYER_COUNT, +1):
                    if not self.draft_ready[i]:
                        self.dice_result[i] = random.randint(1, 5)
                        if keys_down[player_key[i]]:
                            self.draft_ready[i] = True
                # Si ya todos presionaron completar el draft
                if self.draft_ready[TURN_PLAYER_ONE] and self.draft_ready[TURN_PLAYER_TWO]:
                    self.draft_completed_timer.start(2000)

            # Después de un tiempo de completar el draft
            elif self.draft_completed_timer.has_finished:
                # En caso que ambos tenga el mismo dado, se repite el draft
                if self.dice_result[TURN_PLAYER_ONE] == self.dice_result[TURN_PLAYER_TWO]:
                    self.draft_ready = [False for _ in range(PLAYER_COUNT)]
                    self.draft_completed_timer.reset()
                else:
                    # Escoger el primer turno según quien tenga el dado más grande
                    if self.dice_result[TURN_PLAYER_ONE] > self.dice_result[TURN_PLAYER_TWO]:
                        self.turn = TURN_PLAYER_ONE
                    elif self.dice_result[TURN_PLAYER_TWO] > self.dice_result[TURN_PLAYER_ONE]:
                        self.turn = TURN_PLAYER_TWO
                    # Comenzar con el flujo del juego
                    self.state.transition_to(STATE_STRATEGY)

        # Estado de menú de estrategia
        if self.state.is_current(STATE_STRATEGY):
            # Inicializar estado
            if self.state.is_entering:
                # Si está inhabilitado, finalizar turno prematuramente
                if self.disabled[self.turn]:
                    self.state.transition_to(STATE_END_OF_TURN)
                # Si no tiene suficiente energia, finalizar turno prematuramente
                elif self.energy[self.turn] <= 0:
                    self.insufficient = True
                    self.state.transition_to(STATE_END_OF_TURN)

            # Si puede realizar una acción
            if not self.disabled[self.turn] or self.energy[self.turn] > 0:
                # Cambiar entre las opciones disponibles en el menú
                if self.input.is_up_button_down():
                    self.option_selected = (self.option_selected - 1) % STRATEGY_OPTIONS
                elif self.input.is_down_button_down():
                    self.option_selected = (self.option_selected + 1) % STRATEGY_OPTIONS

                # Pasar al siguiente estado según la opción escogida
                if self.input.is_confirm_button_down():
                    if self.option_selected == STRATEGY_OPTION_THROW_DICE:
                        self.state.transition_to(STATE_THROW_DICE)
                    elif self.option_selected == STRATEGY_OPTION_USE_ITEM:
                        self.state.transition_to(STATE_USE_ITEM)
                    elif self.option_selected == STRATEGY_OPTION_SHOW_MAP:
                        self.state.transition_to(STATE_SHOW_BOARD)

                # Aciones especiales de depurraión
                if keys_down[pygame.K_F1]:
                    self.dice_result[self.turn] = self.board.size**2 - 2
                    self.state.transition_to(STATE_ACTION)
        
        # Estado de lanzar dado
        elif self.state.is_current(STATE_THROW_DICE):
            # Inicializar estado
            if self.state.is_entering:
                self.dice_result[self.turn] = 0
                self.dice_thrown_timer.reset()
                self.dice_rolling_timer.start(50)

            # Si el dado aún no ha sido lanzado
            if not self.dice_thrown_timer.has_started:
                # Remover aleatoriamente el dado
                if self.dice_rolling_timer.has_finished:
                    self.dice_result[self.turn] = random.randint(1, 5)
                    self.dice_rolling_timer.start(50)
                # Si cancela, regresar al menú de estrategia (no permitido para dado gratis)
                if self.input.is_cancel_button_down() and not self.free_dice:
                    self.state.transition_to(STATE_STRATEGY)
                # Si confirma, lanzar dado
                elif self.input.is_confirm_button_down():
                    self.dice_thrown_timer.start(2000)
                # Acciones especiales para depuración del programa (seleccionar valor de dado)
                elif context.get_keys_down()[pygame.K_1]:
                    self.dice_result[self.turn] = 1
                    self.dice_thrown_timer.start(2000)
                elif context.get_keys_down()[pygame.K_2]:
                    self.dice_result[self.turn] = 2
                    self.dice_thrown_timer.start(2000)
                elif context.get_keys_down()[pygame.K_3]:
                    self.dice_result[self.turn] = 3
                    self.dice_thrown_timer.start(2000)
                elif context.get_keys_down()[pygame.K_4]:
                    self.dice_result[self.turn] = 4
                    self.dice_thrown_timer.start(2000)
                elif context.get_keys_down()[pygame.K_5]:
                    self.dice_result[self.turn] = 5
                    self.dice_thrown_timer.start(2000)

            # Después del tiempo a esperar al lanzar el dado
            elif self.dice_thrown_timer.has_finished:
                # Si hay suficiente energia o es dado gratutio
                if self.energy[self.turn] > 0 or self.free_dice:
                    # Realizar la acción de moverse
                    # Gastar un punto de nergia si no es dado gratutio
                    if not self.free_dice:
                        self.energy[self.turn] -= 1
                    self.free_dice = False
                    details.save_details(
                        id=self.expedition_id,
                        event_type=details.EVENT_MOVE,
                        player_id=self.turn,
                        steps=self.dice_result[self.turn],
                        index=board.cell_at(self.board, self.position[self.turn])[0]
                    )
                    self.state.transition_to(STATE_ACTION)
                else:
                    # De otra forma, terminar turno avisando que no tiene energía
                    self.insufficient = True
                    self.state.transition_to(STATE_END_OF_TURN)

        # Estado de menú de items
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
                    self.option_selected -= 1 if self.option_selected > 0 else 0
            elif self.input.is_cancel_button_down():
                self.option_selected = 1
                self.state.transition_to(STATE_STRATEGY)
        
        # Estado de mostrar tablero
        elif self.state.is_current(STATE_SHOW_BOARD):
            # De cualquier tecla de confirmación/cancelación, regresar al menú de estrategia
            if self.input.is_confirm_button_down() or self.input.is_cancel_button_down():
                self.option_selected = 2
                self.state.transition_to(STATE_STRATEGY)
        
        # Estado de acción
        elif self.state.is_current(STATE_ACTION):
            # Inicializar estado y temporizador
            if self.state.is_entering:
                self.action_anim_timer.start(500)
            
            # Si hay pasos por realizar y el temporizador terminó
            if self.dice_result[self.turn] != 0 and self.action_anim_timer.has_finished:
                # Según la dirección de pasos:
                # Dar un paso adelante
                if self.dice_result[self.turn] > 0:
                    board.spiral_traversal(self.board, self.position[self.turn], +1)
                    self.dice_result[self.turn] -= 1
                # O dar un paso hacia atras
                else:
                    board.spiral_traversal(self.board, self.position[self.turn], -1)
                    self.dice_result[self.turn] += 1
                # Si la posición actual es la casilla de destino
                if board.is_cell_at(self.board, self.position[self.turn], CELL_END):
                    if self.dice_result[self.turn] > 0:
                        # Rebotar, si no fue exacta la cantidad de posiciones a moverse
                        self.dice_result[self.turn] = self.dice_result[self.turn] * -1
                    else:
                        # Definir como ganador de la partida
                        print("GANADOR!")
                self.action_anim_timer.start(500)

            if self.dice_result[self.turn] == 0  and self.action_anim_timer.has_finished:
                if board.is_cell_station_at(self.board, self.position[self.turn]):
                    self.state.transition_to(STATE_STATION)
                elif board.is_cell_obstacle_at(self.board, self.position[self.turn]):
                    self.state.transition_to(STATE_OBSTACLE)
                else:
                    self.state.transition_to(STATE_END_OF_TURN)

        # Estado de manipulación de estación
        elif self.state.is_current(STATE_STATION):
            # Al inicio, esperar 3 segundos
            if self.state.is_entering:
                self.station_anim_timer.start(3000)
            
            if self.station_anim_timer.has_finished:
                # Consecuencia para Titan
                if board.is_cell_at(self.board, self.position[self.turn], CELL_STATION_TITAN):
                    self.energy[self.turn] = min(self.energy[self.turn] + 10, self.max_energy)
                    self.state.transition_to(STATE_END_OF_TURN)
                # Consecuencia para Sakaar
                elif board.is_cell_at(self.board, self.position[self.turn], CELL_STATION_SAKAAR):
                    self.dice_result[self.turn] = board.calc_steps_to_next_space(self.board, self.position[self.turn])
                    if self.dice_result[self.turn] > 0:
                        self.state.transition_to(STATE_ACTION)
                    else:
                        self.state.transition_to(STATE_END_OF_TURN)
                # Consecuencia para Ego
                elif board.is_cell_at(self.board, self.position[self.turn], CELL_STATION_EGO):
                    self.free_dice = True
                    self.state.transition_to(STATE_THROW_DICE)
                # Consecuencia para Asgard
                elif board.is_cell_at(self.board, self.position[self.turn], CELL_STATION_ASGARD):
                    self.immunity[self.turn] = True
                    self.state.transition_to(STATE_END_OF_TURN)
                # Consecuencia para Xandar
                elif board.is_cell_at(self.board, self.position[self.turn], CELL_STATION_XANDAR):
                    self.dice_result[self.turn] = board.calc_steps_to_next_main_diagonal(self.board, self.position[self.turn])
                    if self.dice_result[self.turn] > 0:
                        self.state.transition_to(STATE_ACTION)
                    else:
                        self.state.transition_to(STATE_END_OF_TURN)
                # Guardar detalles de la consecuencia
                cell_type = board.cell_at(self.board, self.position[self.turn])[1]
                details.save_details(
                    id=self.expedition_id,
                    event_type=details.EVENT_CELL_VISIT,
                    player_id=self.turn,
                    cell_type=cell_type,
                    consequence=resources.locale.CELL_STATION_DESC[cell_type-CELL_STATION_TITAN])

        # Estado de manipulación de obstáculo
        elif self.state.is_current(STATE_OBSTACLE):
            # Al inicio, esperar 3 segundos u omitir lógica si el jugador tiene inmunidad
            if self.state.is_entering:
                if self.immunity[self.turn]:
                    # Gastar la inmunidad para futuros turnos
                    self.immunity[self.turn] = False
                    self.state.transition_to(STATE_END_OF_TURN)
                else:
                    self.obstacle_anim_timer.start(3000)

            if self.obstacle_anim_timer.has_finished:
                # Consecuencia para escombros espaciales
                if board.is_cell_at(self.board, self.position[self.turn], CELL_OBSTACLE_DEBRIS):
                    self.dice_result[self.turn] = board.calc_steps_to_last_space(self.board, self.position[self.turn])
                    if self.dice_result[self.turn] < 0:
                        self.state.transition_to(STATE_ACTION)
                    else:
                        self.state.transition_to(STATE_END_OF_TURN)
                # Consecuencia para impacto de meteorito
                elif board.is_cell_at(self.board, self.position[self.turn], CELL_OBSTACLE_METEORITE):
                    self.disabled[self.turn] = True
                    self.disabled_now = True
                    self.state.transition_to(STATE_END_OF_TURN)
                # Consecuencia para asteroide
                elif board.is_cell_at(self.board, self.position[self.turn], CELL_OBSTACLE_ASTEROID):
                    self.energy[self.turn] = max(self.energy[self.turn] - 3, 0)
                    self.state.transition_to(STATE_END_OF_TURN)
                # Consecuencia para radiación cósmica
                elif board.is_cell_at(self.board, self.position[self.turn], CELL_OBSTACLE_COSMIC_RAD):
                    self.energy[self.turn] = max(self.energy[self.turn] - 2, 0)
                    self.state.transition_to(STATE_END_OF_TURN)
                # Consecuencia para radiación solar
                elif board.is_cell_at(self.board, self.position[self.turn], CELL_OBSTACLE_SOLAR_RAD):
                    self.dice_result[self.turn] = board.calc_steps_to_last_secondary_diagonal(self.board, self.position[self.turn])
                    if self.dice_result[self.turn] < 0:
                        self.state.transition_to(STATE_ACTION)
                    else:
                        self.state.transition_to(STATE_END_OF_TURN)
                # Guardar detalles de la consecuencia
                cell_type = board.cell_at(self.board, self.position[self.turn])[1]
                details.save_details(
                    id=self.expedition_id,
                    event_type=details.EVENT_CELL_VISIT,
                    player_id=self.turn,
                    cell_type=cell_type,
                    consequence=resources.locale.CELL_OBSTACLE_DESC[cell_type-CELL_OBSTACLE_DEBRIS])

        elif self.state.is_current(STATE_END_OF_TURN):
            if self.state.is_entering:
                self.end_of_turn_timer.start(3000)
            
            if self.end_of_turn_timer.has_finished:
                if not self.disabled_now:
                    self.disabled[self.turn] = False
                self.turn = (self.turn + 1) % PLAYER_COUNT
                self.insufficient = False
                self.disabled_now = False
                self.option_selected = 0
                if self.turn == TURN_PLAYER_ONE and self.minigames:
                    self.state.transition_to(STATE_MINIGAME)
                else:
                    self.state.transition_to(STATE_STRATEGY)

        elif self.state.is_current(STATE_MINIGAME):
            if self.state.is_entering:
                self.state.transition_to(STATE_STRATEGY)

        if self.turn is not None:
            self.current_player_pos = self.position[self.turn]
            self.camera_pos = (self.current_player_pos.col * TILE_SIZE + TILE_SIZE // 2, self.current_player_pos.row * TILE_SIZE + TILE_SIZE // 2)
        else:
            self.camera_pos = (TILE_SIZE * self.board.size // 2, TILE_SIZE * self.board.size // 2)

        self.state.finish_update()

    def draw(self, context: GameContext):
        screen = context.get_screen()

        # Dibujar fondo espacial
        for i in range(0, 3, +1):
            for j in range(0, 3, +1):
                screen.blit(self.blue_bg_img, (i * 512, j * 512))

        # Dibujar tablero
        for i in range(0, self.board.size, +1):
            for j in range(0, self.board.size, +1):
                cell = board.cell_at(self.board, (i, j))
                coords = self.coords_by_camera(screen, (j * TILE_SIZE, i * TILE_SIZE))
                # Dibujar inicio
                if board.is_cell_at(self.board, (i, j), CELL_HOME):
                    screen.blit(self.home_img, coords)
                # Dibujar destino
                elif board.is_cell_at(self.board, (i, j), CELL_END):
                    screen.blit(self.end_img, coords)
                # Dibujar estación
                elif board.is_cell_station_at(self.board, (i, j)):
                    station_img = self.station_imgs[cell[1] - CELL_STATION_TITAN]
                    screen.blit(station_img, coords)
                    # Dibujar el nombre de la estación si el jugador del turno actual está encima:
                    if self.turn is not None and cell[0] == board.cell_at(self.board, self.position[self.turn])[0]:
                        station_text = self.text_station_name[cell[1] - CELL_STATION_TITAN]
                        screen.blit(station_text, (coords[0] + TILE_SIZE // 2 - station_text.get_width() // 2, coords[1] - 40))
                # Dibujar obstaculo
                elif board.is_cell_obstacle_at(self.board, (i, j)):
                    obstacle_img = self.obstacle_imgs[cell[1] - CELL_OBSTACLE_DEBRIS]
                    screen.blit(obstacle_img, coords)
                    # Dibujar el nombre del obstáculo si el jugador del turno actual está encima:
                    if self.turn is not None and cell[0] == board.cell_at(self.board, self.position[self.turn])[0]:
                        obstacle_text = self.text_obstacle[cell[1] - CELL_OBSTACLE_DEBRIS]
                        screen.blit(obstacle_text, (coords[0] + TILE_SIZE // 2 - obstacle_text.get_width() // 2, coords[1] - 40))
                # Dibujar puntito
                dot_size = self.cell_dot_blue_img.get_width()
                coords = self.coords_by_camera(screen, (j * TILE_SIZE + TILE_SIZE // 2 - dot_size // 2, i * TILE_SIZE + TILE_SIZE // 2 - dot_size // 2))
                screen.blit(self.cell_dot_blue_img, coords)
                # Dibujar indice de secuencia
                text = self.text_indices[cell[0] - 1]
                coords = self.coords_by_camera(screen, (j * TILE_SIZE + TILE_SIZE // 2 - text.get_width() // 2, i * TILE_SIZE + TILE_SIZE // 2 - text.get_height() // 2))
                screen.blit(text, coords)

        # Dibujar jugadores
        for i in range(0, PLAYER_COUNT, +1):
            pos = self.position[i]
            offset_abs = TILE_SIZE // 4
            offset_x = offset_abs if i == TURN_PLAYER_ONE else -offset_abs
            offset_y = -offset_abs if i == TURN_PLAYER_ONE else offset_abs
            coords = self.coords_by_camera(screen, (pos.col * TILE_SIZE + offset_x, pos.row * TILE_SIZE + offset_y))
            screen.blit(self.team_spaceship_img[i], coords)
        
        # Dibujar dado
        if self.state.is_current(STATE_THROW_DICE):
            dice = self.dice[self.dice_result[self.turn] - 1]
            if not self.dice_thrown_timer.has_started or self.dice_thrown_timer.ticks_elapsed // 250 % 2 == 0 and self.dice_thrown_timer.ticks_elapsed < 2000:
                screen.blit(dice, (screen.get_width() // 2 - dice.get_width() // 2, screen.get_height() * 3/4 - dice.get_height() // 2))

        # Dibujar draft
        if self.state.is_current(STATE_DRAFT):
            player_key_img = [self.img_key_icon_z, self.img_key_icon_m]
            for i in range(0, PLAYER_COUNT, +1):
                dice = self.dice[self.dice_result[i] - 1]
                center_x = screen.get_width() * (1+i*2)/4
                center_y = screen.get_height() // 2
                # Dibujar dado
                if not self.draft_completed_timer.has_started or self.draft_completed_timer.ticks_elapsed // 250 % 2 == 0 and self.draft_completed_timer.ticks_elapsed < 2000:
                    screen.blit(dice, (center_x - dice.get_width() // 2, center_y - dice.get_height() // 2))
                # Dibujar indicador de presionar boton
                if not self.draft_ready[i]:
                    indicator_offset = dice.get_height() // 2 + 50
                    indicator_width = (10 + self.text_press.get_width() + 20 + player_key_img[i].get_width() + 10)
                    indicator_left = center_x - indicator_width // 2
                    indicator_top = center_y + indicator_offset
                    pygame.draw.rect(screen, "white", (indicator_left, indicator_top, indicator_width, 40), border_radius=10)
                    screen.blit(self.text_press, (indicator_left + 10, indicator_top + 10))
                    screen.blit(player_key_img[i], (indicator_left + 10 + self.text_press.get_width() + 20, indicator_top + 4))
                # Dibujar nombre de equipo arriba del dado
                team_text = self.text_team_name[i]
                screen.blit(self.text_team_name[i], (center_x - team_text.get_width() // 2, center_y - dice.get_height() // 2 - 60))
            # Dibujar mensaje de quien le tocará primero
            if self.draft_ready[TURN_PLAYER_ONE] and self.draft_ready[TURN_PLAYER_TWO]:
                if self.dice_result[TURN_PLAYER_ONE] > self.dice_result[TURN_PLAYER_TWO]:
                    draft_result_text = self.text_draft_to_team[TURN_PLAYER_ONE]
                elif self.dice_result[TURN_PLAYER_TWO] > self.dice_result[TURN_PLAYER_ONE]:
                    draft_result_text = self.text_draft_to_team[TURN_PLAYER_TWO]
                else:
                    draft_result_text = self.text_repeat_draft
                coords = (screen.get_width() // 2 - draft_result_text.get_width() // 2, screen.get_height() * 3/4 - draft_result_text.get_height() // 2)
                pygame.draw.rect(screen, "white", (coords[0] - 10, coords[1] - 10, draft_result_text.get_width() + 20, draft_result_text.get_height() + 20), border_radius=10)
                screen.blit(draft_result_text, coords)

        # Dibujar descripción de consecuencia
        # Para obstáculos:
        if self.state.is_current(STATE_OBSTACLE) and board.is_cell_obstacle_at(self.board, self.position[self.turn]):
            cell = board.cell_at(self.board, self.position[self.turn])
            description_text = self.text_obstacle_description[cell[1] - CELL_OBSTACLE_DEBRIS]
            coords = (screen.get_width() // 2 - description_text.get_width() // 2, screen.get_height() * 3/4 - description_text.get_height() // 2)
            pygame.draw.rect(screen, "white", (coords[0] - 10, coords[1] - 10, description_text.get_width() + 20, description_text.get_height() + 20), border_radius=10)
            screen.blit(description_text, coords)
        # Para estaciones:
        if self.state.is_current(STATE_STATION) and board.is_cell_station_at(self.board, self.position[self.turn]):
            cell = board.cell_at(self.board, self.position[self.turn])
            description_text = self.text_station_description[cell[1] - CELL_STATION_TITAN]
            coords = (screen.get_width() // 2 - description_text.get_width() // 2, screen.get_height() * 3/4 - description_text.get_height() // 2)
            pygame.draw.rect(screen, "white", (coords[0] - 10, coords[1] - 10, description_text.get_width() + 20, description_text.get_height() + 20), border_radius=10)
            screen.blit(description_text, coords)

        # Dibujar mensaje de fin de turno
        if self.state.is_current(STATE_END_OF_TURN):
            text = None
            if self.disabled[self.turn] and not self.disabled_now:
                text = self.text_skipped_turn
            elif self.insufficient:
                text = self.text_not_enough_energy
            if text:
                coords = (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() * 3/4 - text.get_height() // 2)
                pygame.draw.rect(screen, "white", (coords[0] - 10, coords[1] - 10, text.get_width() + 20, text.get_height() + 20), border_radius=10)
                screen.blit(text, coords)

        # Dibujar indicador de turno
        if self.turn is not None:
            turn_text = self.text_player_turn[self.turn]
            turn_text_box_width = turn_text.get_width() + 50 * 2
            pygame.draw.rect(screen, "white", (screen.get_width() // 2 - turn_text_box_width // 2, 0, turn_text_box_width, 32), border_bottom_left_radius=10, border_bottom_right_radius=10)
            screen.blit(turn_text, (screen.get_width() // 2 - turn_text.get_width() // 2, 4))

        # Dibujar indicador de estado
        state_text = self.text_state[self.state.current_state]
        state_text_box_width = state_text.get_width() + 50 * 2
        pygame.draw.rect(screen, "white", (screen.get_width() // 2 - state_text_box_width // 2, screen.get_height() - 32, state_text_box_width, 32), border_top_left_radius=10, border_top_right_radius=10)
        screen.blit(state_text, (screen.get_width() // 2 - state_text.get_width() // 2, screen.get_height() - state_text.get_height()))

        # Dibujar detalles de equipos
        player_top_left = [
            (50, 50),  # top left corner
            (50, screen.get_width() - 300),  # top right corner
        ]
        for i in range(0, PLAYER_COUNT, +1):
            (top, left) = player_top_left[i]
            player_name_text = self.text_team_name[i]
            player_energy = self.energy[i]
            player_immunity = self.immunity[i]
            player_disabled = self.disabled[i]
            player_pfp = self.team_pfp[i]
            screen.blit(player_pfp, (left, top))
            screen.blit(player_name_text, (left + 64 + 8, top + 4))
            screen.blit(self.energy_icon_img, (left + 64 + 8, top + 32))
            energy_text = self.menu_font.render(f"{player_energy} / {self.max_energy}", True, "white")
            screen.blit(energy_text, (left + 64 + 8 + 32 + 8, top + 32))
            energy_bar_width = player_energy * 64 / self.max_energy
            pygame.draw.rect(screen, "red", (left + 64 + 8 + 32 + 8, top + 56, 64, 8))
            pygame.draw.rect(screen, "green", (left + 64 + 8 + 32 + 8, top + 56, energy_bar_width, 8))
            if player_immunity:
                screen.blit(self.shield_icon_img, (left + 40, top + 40))
            if player_disabled:
                screen.blit(self.disabled_icon_img, (left + 56, top + 40))

        # Dibujar menú de estrategia
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

        # Dibujar menú de items
        if self.state.is_current(STATE_USE_ITEM):
            item_cols = self.option_selected % 5
            item_rows = self.option_selected // 5
            pygame.draw.rect(screen, "#b9b9b9", (200 + 30 * item_cols - 16, 400 + 30 * item_rows - 16,32,32))
            for i, _ in enumerate(self.items[self.turn]):
                item_cols = i % 5
                item_rows = i // 5
                pygame.draw.circle(screen, '#ffffff', (200 + 30 * item_cols, 400 + 30 * item_rows), 10)

        # Dibujar mapa de tablero
        if self.state.is_current(STATE_SHOW_BOARD):
            for i in range(0, self.board.size, +1):
                for j in range(0, self.board.size, +1):
                    cell = self.board.matrix[i][j][1]
                    if cell > 0:
                        color = "red" if cell > 5 else "blue" if cell > 0 else "black"
                        pygame.draw.rect(screen, color, (j * 32 +50, i * 32+400, 32, 32))

    def exit(self, context: GameContext):
        # Detener música
        pygame.mixer.music.stop()

    def coords_by_camera(self, screen: pygame.Surface, coords: tuple[int, int]) -> tuple[int, int]:
        x = self.camera_pos[0] - screen.get_width() // 2
        y = self.camera_pos[1] - screen.get_height() // 2
        new_coords = (coords[0] - x, coords[1] - y)
        return new_coords
