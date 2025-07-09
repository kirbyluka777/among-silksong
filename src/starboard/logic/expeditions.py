from . import records
import struct
import datetime
import os

EXPEDITION_FILE = 'data\\EXPEDICIONES_ESPACIALES.bin'
EXPEDITION_FORMAT = "i20s20siii8s"
EXPEDITION_SIZE = struct.calcsize(EXPEDITION_FORMAT)

class Expedition:
    def __init__(self, id, team_name_1, team_name_2, board_size, difficulty, board_dir, date):
        self.id = id
        self.team_name_1 = team_name_1
        self.team_name_2 = team_name_2
        self.board_size = board_size
        self.difficulty = difficulty
        self.board_dir = board_dir
        self.date = date

def save_expedition(name1,name2,en_unit,difficulty,direction):
    exp_id = records.increment_records_len(EXPEDITION_FILE)
    date = datetime.datetime.now().strftime(f"%Y/%m/%d")

    file = open(EXPEDITION_FILE,'ab')
    name1 = name1.ljust(20).strip().encode('utf-8')
    name2 = name2.ljust(20).strip().encode('utf-8')
    date = date.ljust(10).strip().encode('utf-8')
    file.write(struct.pack(EXPEDITION_FORMAT,exp_id,name1,name2,en_unit,difficulty,direction,date))
    file.close()

    return exp_id

def read_expeditions() -> list[Expedition]:
    if not os.path.isfile(EXPEDITION_FILE):
        return []
    exp_len = records.get_records_len(EXPEDITION_FILE)
    exp = [None for _ in range(exp_len)]
    i = 0
    file = open(EXPEDITION_FILE,'rb')
    file.seek(4)
    while True:
        bytes = file.read(EXPEDITION_SIZE)
        if not bytes:
            file.close()
            return exp
        else:
            id, name1, name2, en_unit, difficulty, direction, date = struct.unpack(EXPEDITION_FORMAT,bytes)
            name1 = name1.decode('utf-8').strip()
            name2 = name2.decode('utf-8').strip()
            date = date.decode('utf-8').strip()
            exp[i] = Expedition(id, name1, name2, en_unit, difficulty, direction, date)
            i += 1