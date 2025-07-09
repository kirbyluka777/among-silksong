# given id
# show team data
# show expeditions
# show km
import struct
from . import teams
from . import details
from . import expeditions
from .expeditions import Expedition
from . import records

def search_b(team_id) -> bool:
    team = teams.search_team(team_id)
    if not team:
        print("not team")
        return False

    exp_max = records.get_records_len(expeditions.EXPEDITION_FILE)
    if exp_max < 0: return False

    exp = [None for _ in range(exp_max)]
    i = 0
    file = open(expeditions.EXPEDITION_FILE,'rb')
    file.seek(4)
    while True:
        bytes = file.read(expeditions.EXPEDITION_SIZE)
        if not bytes:
            file.close()
            if i < 0: return False
            break
        else:
            id, name1, name2, en_unit, difficulty, direction, date = struct.unpack(expeditions.EXPEDITION_FORMAT,bytes)
            name1 = name1.decode('utf-8').strip('\x00')
            name2 = name2.decode('utf-8').strip('\x00')
            date = date.decode('utf-8').strip('\x00')

            if team.name.strip() == name1.strip() or team.name.strip() == name2.strip():
                exp[i] = Expedition(id, name1, name2, en_unit, difficulty, direction, date)
                i+=1
    file = open('Reporte_b.txt', 'w')
    file.write(f"REPORTE: EQUIPO {team.name} Y EXPEDICIONES EN LAS QUE HA PARTICIPADO\n"
               f"----------------------------------------------\n"
               f"DATOS DE EQUIPO\nID:\t{team.id}\nNOMBRE:\t{team.name}\nCORREO:\t{team.email}\n"
               f"----------------------------------------------\n"
               f"EXPEDICIONES\n")
    km_total = 0
    for x in range(i):
        km_total += details.get_total_km_from_expedition(exp[x].id)
        print(km_total)
        file.write(f"FECHA\t{exp[x].date}\n"
                   f"ID\t{exp[x].id}\n"
                   f"EQUIPO 1\t{exp[x].team_name_1}\n"
                   f"EQUIPO 2\t{exp[x].team_name_2}\n"
                   f"TAMAÑO DEL TABLERO\t{exp[x].board_size}\n"
                   f"DIFICULTAD\t{'BASICO' if exp[x].difficulty == 0 else 'INTERMEDIO' if exp[x].difficulty == 1 else 'AVANZADO'}\n"
                   f"DIRECCION\t{'HORARIO' if exp[x].board_dir == 0 else 'ANTIHORARIO'}\n\n")
        file.write("KM TOTAL RECORIDOS\t{0}\n".format(km_total*1000)) 
    return True