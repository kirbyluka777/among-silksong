import struct
import os
from team import Game
from team import Team
#from team import Country
#from team import Country

FILE_TEAM = 'equipos.bin'
FILE_COUNTRY = 'paises.bin'
FORMAT_TEAM = '20s50s8s'
FORMAT_COUNTRY = '3s20s'
SIZE_TEAM = struct.calcsize(FORMAT_TEAM)
SIZE_COUNTRY = struct.calcsize(FORMAT_COUNTRY)

NULL = '\x00'

def save_team(data:Team):
    with open(FILE_TEAM, 'ab') as file:
        name = data.name.encode('utf-8')
        email = data.email.encode('utf-8')
        password = data.password.encode('utf-8')

        packed_data = struct.pack(FORMAT_TEAM, name, email, password)

        file.write(packed_data)

def load_team(game):
    if not os.path.isfile(FILE_TEAM):
        return
    with open(FILE_TEAM, 'rb') as file:
        while True:
            bytes = file.read(SIZE_TEAM)
            if not bytes:
                return
            name, email, password = struct.unpack(FORMAT_TEAM, bytes)
            name = name.decode('utf-8').strip(NULL)
            email = email.decode('utf-8').strip(NULL)
            password = password.decode('utf-8').strip(NULL)

            game.teams.append(Team(name, email, password))