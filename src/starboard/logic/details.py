import os
import struct
from . import records

DETAILS_FILE = 'data\\detalles_{0}.bin'
DETAILS_MOVE_FORMAT = 'iii' # Codigo de jugador, Pasos, Indice
DETAILS_MOVE_SIZE = struct.calcsize(DETAILS_MOVE_FORMAT)
DETAILS_CELL_VISIT_FORMAT = 'ii50s'
DETAILS_CELL_VISIT_SIZE = struct.calcsize(DETAILS_CELL_VISIT_FORMAT)

EVENT_MOVE = 0
EVENT_CELL_VISIT = 1
#save_details(1,1,cel_type=4)

class MoveEvent():
    def __init__(self, player_id, steps, index):
        self.player_id = player_id
        self.steps = steps
        self.index = index

class CellVisitEvent():
    def __init__(self, player_id, cell_type, consequence):
        self.player_id = player_id
        self.cell_type = cell_type
        self.consequence = consequence

def save_details(
        id, event_type,
        player_id:int=None,
        steps:int=None,
        index:int=None,
        cell_type:int=None,
        consequence:str=None):
    filename = DETAILS_FILE.format(id)
    records.increment_records_len(filename)
    file = open(filename, 'ab')
    bytes = struct.pack('i', event_type)
    file.write(bytes)
    if event_type == EVENT_MOVE:
        bytes = struct.pack(DETAILS_MOVE_FORMAT, player_id, steps, index)
        file.write(bytes)
    elif event_type == EVENT_CELL_VISIT:
        bytes = struct.pack(DETAILS_CELL_VISIT_FORMAT, player_id, cell_type, consequence.encode('utf-8'))
        file.write(bytes)
    file.close()

def read_details(id):
    filename = DETAILS_FILE.format(id)
    if not os.path.isfile(filename):
        return []
    details_len = records.get_records_len(filename)
    details = [None for _ in range(details_len)]
    i = 0

    file = open(filename, 'rb')
    while True:
        bytes = file.read(4)
        if not bytes:
            file.close()
            return details
        e, = struct.unpack('i', bytes)
        if e == EVENT_MOVE:
            bytes = file.read(DETAILS_MOVE_SIZE)
            player_id, steps, index = struct.unpack(DETAILS_MOVE_FORMAT, bytes)
            details[i] = MoveEvent(player_id, steps, index)
        elif e == EVENT_CELL_VISIT:
            bytes = file.read(DETAILS_CELL_VISIT_SIZE)
            player_id, cell_type, consequence = struct.unpack(DETAILS_CELL_VISIT_FORMAT, bytes)
            consequence = consequence.decode('utf-8').strip('\x00')
            details[i] = CellVisitEvent(player_id, cell_type, consequence)
        i += 1

def get_total_km_from_expedition(expedition_id, turn):
    km = 0
    for detail in read_details(expedition_id):
        if isinstance(detail, MoveEvent) and detail.player_id == turn:
            km = detail.steps
    return km

if __name__=="__main__":
    sex = read_details(2)
    for x in sex:
        if x.isinstance(MoveEvent):
            print(x)