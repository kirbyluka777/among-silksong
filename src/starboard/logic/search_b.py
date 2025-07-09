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


    report_file = open('reports/Reporte_b.txt', 'w', encoding="utf-8")
    report_file.write(f"REPORTE: EQUIPO {team.name} Y EXPEDICIONES EN LAS QUE HA PARTICIPADO\n"
               f"----------------------------------------------\n"
               f"DATOS DE EQUIPO\nID:\t{team.id}\nNOMBRE:\t{team.name}\nCORREO:\t{team.email}\n"
               f"----------------------------------------------\n"
               f"EXPEDICIONES\n"
               f"----------------------------------------------\n")

    km_total = 0
    file = open(expeditions.EXPEDITION_FILE,'rb')
    file.seek(4)
    while True:
        bytes = file.read(expeditions.EXPEDITION_SIZE)
        if not bytes:
            file.close()
            report_file.write("KM TOTAL RECORIDOS\t{0}\n".format(km_total*1000))
            report_file.close()
            return True
        else:
            id, name1, name2, en_unit, difficulty, direction, date = struct.unpack(expeditions.EXPEDITION_FORMAT,bytes)
            name1 = name1.decode('utf-8').strip().strip('\x00')
            name2 = name2.decode('utf-8').strip().strip('\x00')
            date = date.decode('utf-8').strip().strip('\x00')

            player_turn = None
            rival_name = None
            if team.name == name1:
                player_turn = 0
                rival_name = name2
            elif team.name == name2:
                player_turn = 1
                rival_name = name1

            if player_turn is not None:
                km = details.get_total_km_from_expedition(id, player_turn)
                km_total += km
                report_file.write(f"FECHA\t{date}\n"
                        f"ID:\t{id}\n"
                        f"KM RECORRIDOS:\t{km*1000}\n"
                        f"RIVAL:\t{rival_name}\n"
                        f"ENERGÍA INICIAL:\t{en_unit}\n"
                        f"DIFICULTAD:\t{'BASICO' if difficulty == 0 else 'INTERMEDIO' if difficulty == 1 else 'AVANZADO'}\n"
                        f"DIRECCION:\t{'HORARIO' if direction == 0 else 'ANTIHORARIO'}\n")
                report_file.write("----------------------------------------------\n")