# Placeholder
import random
import math
from typing import Callable, Literal, Union
from ..constants import *

class Positioning:
    def __init__(self, row: int, col: int, dir: int, hturns: int = 0, vturns: int = 0):
        self.row = row
        self.col = col
        self.dir = dir
        self.hturns = hturns
        self.vturns = vturns

BoardMatrix = list[list[list[int]]]
BoardCoords = Positioning | tuple[int]

class Board:
    def __init__(self, matrix: BoardMatrix = [], size: int = 0, dir: int = BOARD_DIR_OCLOCK, difficulty: int = BOARD_DIFFICULTY_EASY):
        self.matrix = matrix
        self.size = size
        self.dir = dir
        self.difficulty = difficulty

def spiral_traversal(board: Board, pos: Positioning, steps: int):
    if steps > 0:
        for i in range(steps):
            if pos.dir == MOVE_DIR_RIGHT and pos.col >= board.size - pos.hturns // 2 - 1:
                pos.vturns += 1
                pos.dir = MOVE_DIR_DOWN if board.dir == BOARD_DIR_OCLOCK else MOVE_DIR_UP
            elif pos.dir == MOVE_DIR_LEFT and pos.col <= pos.hturns // 2:
                pos.vturns += 1
                pos.dir = MOVE_DIR_UP if board.dir == BOARD_DIR_OCLOCK else MOVE_DIR_DOWN
            elif pos.dir == MOVE_DIR_DOWN and pos.row >= board.size - pos.vturns // 2 - 1:
                pos.hturns += 1
                pos.dir = MOVE_DIR_LEFT if board.dir == BOARD_DIR_OCLOCK else MOVE_DIR_RIGHT
            elif pos.dir == MOVE_DIR_UP and pos.row <= pos.vturns // 2:
                pos.hturns += 1
                pos.dir = MOVE_DIR_RIGHT if board.dir == BOARD_DIR_OCLOCK else MOVE_DIR_LEFT
                
            if pos.dir == MOVE_DIR_RIGHT:
                pos.col += 1
            elif pos.dir == MOVE_DIR_LEFT:
                pos.col -= 1
            elif pos.dir == MOVE_DIR_DOWN:
                pos.row += 1
            elif pos.dir == MOVE_DIR_UP:
                pos.row -= 1
    elif steps < 0:
        for i in range(abs(steps)):
            if pos.dir == MOVE_DIR_RIGHT and pos.col <= pos.hturns // 2 - (1 if board.dir == BOARD_DIR_OCLOCK else 0):
                pos.hturns -= 1
                pos.dir = MOVE_DIR_UP if board.dir == BOARD_DIR_OCLOCK else MOVE_DIR_DOWN
            elif pos.dir == MOVE_DIR_LEFT and pos.col >= board.size - pos.hturns // 2 - (1 if board.dir == BOARD_DIR_OCLOCK else 0):
                pos.hturns -= 1
                pos.dir = MOVE_DIR_DOWN if board.dir == BOARD_DIR_OCLOCK else MOVE_DIR_UP
            elif pos.dir == MOVE_DIR_DOWN and pos.row <= pos.vturns // 2:
                pos.vturns -= 1
                pos.dir = MOVE_DIR_RIGHT if board.dir == BOARD_DIR_OCLOCK else MOVE_DIR_LEFT
            elif pos.dir == MOVE_DIR_UP and pos.row >= board.size - pos.vturns // 2:
                pos.vturns -= 1
                pos.dir = MOVE_DIR_LEFT if board.dir == BOARD_DIR_OCLOCK else MOVE_DIR_RIGHT
            
            if pos.dir == MOVE_DIR_RIGHT:
                pos.col -= 1
            elif pos.dir == MOVE_DIR_LEFT:
                pos.col += 1
            elif pos.dir == MOVE_DIR_DOWN:
                pos.row -= 1
            elif pos.dir == MOVE_DIR_UP:
                pos.row += 1

def generate_random_board(size: int, difficulty: int, dir: int):
    # Inicializar matriz de tablero
    matrix = [[[0 for _ in range(2)] for _ in range(size)] for _ in range(size)]
    
    # Definir el punto de inicio
    if dir == 0:
        matrix[0][0][1] = CELL_HOME
    else:
        matrix[0][size - 1][1] = CELL_HOME
    
    # Definir el punto de fin
    matrix[size//2][size//2][1] = CELL_END

    # Definir el factor de generacipón aleatoria
    match difficulty:
        case 0:
            obstacles_factor = 0.1
            stations_factor = 0.2
        case 1:
            obstacles_factor = 0.15
            stations_factor = 0.15
        case 2:
            obstacles_factor = 0.2
            stations_factor = 0.1
        case _:       
            obstacles_factor = 0
            stations_factor = 0
            
    # Poner obstaculos y estaciones aleatoriamente
    place_object(matrix, size, math.floor(size*size*obstacles_factor), random_obstacle)
    place_object(matrix, size, math.floor(size*size*stations_factor), random_station)

    # Crear tablero con datos
    board = Board()
    board.matrix = matrix
    board.size = size
    board.dir = dir
    board.difficulty = difficulty

    # Enumerar indices de celdas
    pos = initial_pos(board)
    for i in range(board.size**2):
        board.matrix[pos.row][pos.col][0] = i + 1
        spiral_traversal(board, pos, 1)

    return board

def initial_pos(board: Board):
    if board.dir == BOARD_DIR_OCLOCK:
        return Positioning(0, 0, MOVE_DIR_RIGHT)
    else:
        return Positioning(0, board.size - 1, MOVE_DIR_LEFT)

def copy_pos(pos: Positioning):
    return Positioning(pos.row, pos.col, pos.dir, pos.hturns, pos.vturns)

def random_station():
    return random.randint(CELL_STATION_TITAN, CELL_STATION_XANDAR)

def random_obstacle():
    return random.randint(CELL_OBSTACLE_DEBRIS, CELL_OBSTACLE_SOLAR_RAD)

def place_object(tablero, n, cantidad, obj_generator):
    while cantidad>0:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        if tablero[i][j][1] == 0:
            tablero[i][j][1] = obj_generator()
            cantidad -= 1

def coords_as_tuple(pos: BoardCoords):
    row, col = (pos.row, pos.col) if isinstance(pos, Positioning) else (pos[0], pos[1])
    return row, col

def cell_at(board: Board, pos: BoardCoords):
    row, col = coords_as_tuple(pos)
    return board.matrix[row][col]

def is_cell_station_at(board: Board, pos: BoardCoords):
    cell = cell_at(board, pos)
    return cell[1] >= CELL_STATION_TITAN and cell[1] <= CELL_STATION_XANDAR

def is_cell_obstacle_at(board: Board, pos: BoardCoords):
    cell = cell_at(board, pos)
    return cell[1] >= CELL_OBSTACLE_DEBRIS and cell[1] <= CELL_OBSTACLE_SOLAR_RAD

def is_cell_end_at(board: Board, pos: BoardCoords):
    return cell_at(board, pos)[1] == CELL_END

def is_cell_empty_at(board: Board, pos: BoardCoords):
    return cell_at(board, pos)[1] == CELL_SPACE

def is_cell_at(board: Board, pos: BoardCoords, cell_type: int):
    return cell_at(board, pos)[1] == cell_type

def is_cell_at_main_diagonal(board: Board, pos: BoardCoords):
    row, col = coords_as_tuple(pos)
    return row == col

def is_cell_at_secondary_diagonal(board: Board, pos: BoardCoords):
    row, col = coords_as_tuple(pos)
    return row + col == board.size-1

def calc_steps_to(board: Board, pos_from: Positioning, stop_condition: Callable[[Positioning], bool], step: int = 1, final_condition: Callable[[Positioning], bool] = None):
    temp_pos = copy_pos(pos_from)
    ini_pos = initial_pos(board)
    steps = 0
    while (((step > 0 and steps <= 0) or (step < 0 and steps >= 0)) or not stop_condition(temp_pos) 
            and not (temp_pos.row == ini_pos.row and temp_pos.col == ini_pos.col)
            and not (temp_pos.row == board.size//2 and temp_pos.col == board.size//2)):
        spiral_traversal(board, temp_pos, step)
        steps += step
    if temp_pos.row == board.size//2 and temp_pos.col == board.size//2:
        steps += -step
    if final_condition and not final_condition(temp_pos):
        return 0
    return steps

def calc_steps_to_next_space(board: Board, pos_from: Positioning):
    return calc_steps_to(board, pos_from, lambda p: is_cell_empty_at(board, p), step=+1)

def calc_steps_to_last_space(board: Board, pos_from: Positioning):
    return calc_steps_to(board, pos_from, lambda p: is_cell_empty_at(board, p), step=-1)

def calc_steps_to_next_main_diagonal(board: Board, pos_from: Positioning):
    return calc_steps_to(board, pos_from, lambda p: is_cell_at_main_diagonal(board, p) and is_cell_station_at(board, p), step=+1, final_condition=lambda p: is_cell_station_at(board, p))

def calc_steps_to_last_secondary_diagonal(board: Board, pos_from: Positioning):
    return calc_steps_to(board, pos_from, lambda p: is_cell_at_secondary_diagonal(board, p), step=-1)

def print_board(board: Board):
    print("-----"*board.size)
    for i in range(board.size):
        print("| ", end="")
        for j in range(board.size):
            print(f"{board.matrix[i][j][0]:02}", end=" | ")
        print("\n" + "-----"*board.size)
