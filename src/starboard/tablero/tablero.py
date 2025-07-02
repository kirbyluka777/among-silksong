# Placeholder
import random
import math
import pygame as pg
BOARD_DIFFICULTY_EASY = 0
BOARD_DIFFICULTY_MEDIUM = 1
BOARD_DIFFICULTY_HARD = 2

BOARD_DIR_OCLOCK = 0
BOARD_DIR_COUNTEROCLOCK = 1

DIR_RIGHT = 0
DIR_DOWN = 1
DIR_LEFT = 2
DIR_UP = 3

class Board:
	def init(self):
		self.matrix = list[int](list[int]())
		self.size = 0
		self.dir = BOARD_DIR_OCLOCK
		self.difficulty = BOARD_DIFFICULTY_EASY

class Positioning:
	def init(self):
		self.row = 0
		self.col = 0
		self.hturns = 0
		self.vturns = 0
		self.dir = DIR_RIGHT

def initial_pos_oclock():
	pos = Positioning()
	pos.row = 0
	pos.col = 0
	pos.hturns = 0
	pos.vturns = 0
	pos.dir = DIR_RIGHT
	return pos

def initial_pos_counteroclock(board: Board):
	pos = Positioning()
	pos.row = board.size - 1
	pos.col = board.size - 1
	pos.hturns = 0
	pos.vturns = 0
	pos.dir = DIR_LEFT
	return pos

def spiral_traversal_oclock(board: Board, pos: Positioning, steps: int):
	for i in range(steps):
		if pos.dir == DIR_RIGHT and pos.col >= board.size - pos.hturns // 2 - 1:
			pos.vturns += 1
			pos.dir = DIR_DOWN
		elif pos.dir == DIR_LEFT and pos.col <= pos.hturns // 2:
			pos.vturns += 1
			pos.dir = DIR_UP
		elif pos.dir == DIR_DOWN and pos.row >= board.size - pos.vturns // 2 - 1:
			pos.hturns += 1
			pos.dir = DIR_LEFT
		elif pos.dir == DIR_UP and pos.row <= pos.vturns // 2:
			pos.hturns += 1
			pos.dir = DIR_RIGHT
			
		if pos.dir == DIR_RIGHT:
			pos.col += 1
		elif pos.dir == DIR_LEFT:
			pos.col -= 1
		elif pos.dir == DIR_DOWN:
			pos.row += 1
		elif pos.dir == DIR_UP:
			pos.row -= 1

def place_object(tablero, n, cantidad, obj):
	while cantidad>0:
		i = random.randint(0, n - 1)
		j = random.randint(0, n - 1)
		if tablero[i][j] == 0:
			tablero[i][j] = obj
			cantidad-=1

def generate_random_board(size: int, difficulty: int, dir: int):
	matrix = [[0 for _ in range(size)] for _ in range(size)]
	if dir == 0:
		matrix[1][1] = 1
	else:
		matrix[1][size] = 1
	matrix[size//2][size//2] = 4
	obstacles_factor = 0
	stations_factor = 0
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
			
	place_object(matrix, size, math.floor(size*size*obstacles_factor), 4)
	place_object(matrix, size, math.floor(size*size*stations_factor), 3)

	board = Board()
	board.size = size
	board.matrix = matrix
	return board

def print_board(board: Board):
	print(f"{"-----"*board.size}")
	for i in range(board.size):
		print("| ", end="")
		for j in range(board.size):
			print(f"{board.matrix[i][j]:02}", end=" | ")
		print(f"\n{"-----"*board.size}")

def test_spiral_traversal(board: Board, initial_pos = None, jumps = None, steps = 1):
	pos = initial_pos_oclock() if not initial_pos else initial_pos
	jumps = board.size**2 // steps if not jumps else jumps
	for i in range(board.size**2):
		board.matrix[pos.row][pos.col] = i + 1
		spiral_traversal_oclock(board, pos, steps)

if __name__ == "__main__":
	n = 9 #int(input("n: "))
	dificultad = 1 #int(input("dificultad: "))
	direccion = 0 #int(input("direccion: "))
	board = generate_random_board(n, dificultad, direccion)
	print("Tablero generado:")
	print_board(board)
	print("Tablero recorrido:")
	test_spiral_traversal(board, steps=3)
	print_board(board)

def dice():
	return random.randint(1,5)

