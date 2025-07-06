# Placeholder
import random
import math
from typing import Literal, Union
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

    def cell_at(self, pos: BoardCoords):
        row, col = (pos.row, pos.col) if isinstance(pos, Positioning) else (pos[0], pos[1])
        return self.matrix[row][col]

    def is_cell_station_at(self, pos: BoardCoords):
        cell = self.cell_at(pos)
        return cell[1] >= CELL_STATION_TITAN and cell[1] <= CELL_STATION_XANDAR

    def is_cell_obstacle_at(self, pos: BoardCoords):
        cell = self.cell_at(pos)
        return cell[1] >= CELL_OBSTACLE_DEBRIS and cell[1] <= CELL_OBSTACLE_SOLAR_RAD
    
    def is_cell_at(self, pos: BoardCoords, cell_type: int):
        return self.cell_at(pos)[1] == cell_type

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
        for i in range(steps):
            if pos.dir == MOVE_DIR_RIGHT and pos.col >= board.size - pos.hturns // 2:
                pos.vturns -= 1
                pos.dir = MOVE_DIR_DOWN if board.dir == BOARD_DIR_OCLOCK else MOVE_DIR_UP
            elif pos.dir == MOVE_DIR_LEFT and pos.col <= pos.hturns // 2 - 1:
                pos.vturns -= 1
                pos.dir = MOVE_DIR_UP if board.dir == BOARD_DIR_OCLOCK else MOVE_DIR_DOWN
            elif pos.dir == MOVE_DIR_DOWN and pos.row >= board.size - pos.vturns // 2:
                pos.hturns -= 1
                pos.dir = MOVE_DIR_LEFT if board.dir == BOARD_DIR_OCLOCK else MOVE_DIR_RIGHT
            elif pos.dir == MOVE_DIR_UP and pos.row <= pos.vturns // 2 - 1:
                pos.hturns -= 1
                pos.dir = MOVE_DIR_RIGHT if board.dir == BOARD_DIR_OCLOCK else MOVE_DIR_LEFT
            
        if pos.dir == MOVE_DIR_RIGHT:
            pos.col += (1 if steps > 0 else -1)
        elif pos.dir == MOVE_DIR_LEFT:
            pos.col -= (1 if steps > 0 else -1)
        elif pos.dir == MOVE_DIR_DOWN:
            pos.row += (1 if steps > 0 else -1)
        elif pos.dir == MOVE_DIR_UP:
            pos.row -= (1 if steps > 0 else -1)

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
    board_place_object(matrix, size, math.floor(size*size*obstacles_factor), board_random_obstacle)
    board_place_object(matrix, size, math.floor(size*size*stations_factor), board_random_station)

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

def board_random_station():
    return random.randint(CELL_STATION_TITAN, CELL_STATION_XANDAR)

def board_random_obstacle():
    return random.randint(CELL_OBSTACLE_DEBRIS, CELL_OBSTACLE_SOLAR_RAD)

def board_place_object(tablero, n, cantidad, obj_generator):
    while cantidad>0:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        if tablero[i][j][1] == 0:
            tablero[i][j][1] = obj_generator()
            cantidad -= 1

def print_board(board: Board):
    print("-----"*board.size)
    for i in range(board.size):
        print("| ", end="")
        for j in range(board.size):
            print(f"{board.matrix[i][j][0]:02}", end=" | ")
        print("\n" + "-----"*board.size)
