from . import records
import struct
import datetime

EXPEDITION_FILE = 'data/EXPEDICIONES_ESPACIALES.bin'
EXPEDITION_FORMAT = "i20s20siii8s"
EXPEDITION_SIZE = struct.calcsize(EXPEDITION_FORMAT)
EXP_ID = 1

class Expedition:
    def __init__(self, id, team_name_1, team_name_2, en_unit, difficulty, direction, date):
        self.id = id
        self.team_name_1 = team_name_1
        self.team_name_2 = team_name_2
        self.board_size = en_unit
        self.difficulty = difficulty
        self.board_dir = direction
        self.date = date

def save_expedition(name1,name2,en_unit,difficulty,direction):
    global EXP_ID
    date = datetime.datetime.now().strftime("%Y/%m/%d")

    records.increment_records_len(EXPEDITION_FILE)

    file = open(EXPEDITION_FILE,'ab')
    name1 = name1.ljust(20).encode('utf-8')
    name2 = name2.ljust(20).encode('utf-8')
    date = date.ljust(8).encode('utf-8')
    file.write(struct.pack(EXPEDITION_FORMAT,EXP_ID,name1,name2,en_unit,difficulty,direction,date))
    EXP_ID = EXP_ID+1
    file.close()

    return EXP_ID

def read_expeditions() -> list[Expedition]:
    records_len = records.get_records_len(EXPEDITION_FILE)
    records = [None for _ in range(records_len)]
    i = 0
    file = open(EXPEDITION_FILE,'rb')
    file.seek(4)
    while True:
        bytes = file.read(EXPEDITION_SIZE)
        if not bytes:
            file.close()
            return records
        else:
            id, name1, name2, en_unit, difficulty, direction, date = struct.unpack(EXPEDITION_FORMAT,bytes)
            name1 = name1.decode('utf-8').strip('\x00')
            name2 = name2.decode('utf-8').strip('\x00')
            date = date.decode('utf-8').strip('\x00')
            records[i] = Expedition(id, name1, name2, en_unit, difficulty, direction, date)
            i += 1