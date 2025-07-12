from .constants import *
from .logic import teams as t
from .logic import countries as c

teams = t.load_records()
team1 = None
team2 = None
countries =  c.load_records()
ods = ['Fin de la pobreza',
    'Hambre cero',
    'Salud y bienestar',
    'Educación de calidad',
    'Igualdad de género',
    'Agua limpia y saneamiento',
    'Energía asequible y no contaminante',
    'Trabajo decente y crecimiento económico',
    'Industria, innovación e infraestructura',
    'Reducción de las desigualdades',
    'Ciudades y comunidades sostenibles',
    'Producción y consumo responsables',
    'Acción por el clima',
    'Vida submarina',
    'Vida de ecosistemas terrestres',
    'Paz, justicia e instituciones sólidas',
    'Alianzas para lograr los objetivos']

board_size = 9 #BOARD_SIZE_MIN
board_dir = BOARD_DIR_OCLOCK
board_difficulty = BOARD_DIFFICULTY_EASY
