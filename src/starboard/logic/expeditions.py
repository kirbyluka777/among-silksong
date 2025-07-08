import struct
import datetime

EXPEDITION_FILE = 'EXPEDICIONES_ESPACIALES.bin'
EXPEDITION_FORMAT = "i20s20siii8s"
EXPEDITION_SIZE = struct.calcsize(EXPEDITION_FORMAT)
EXP_ID = 1

def save_expedition(name1,name2,en_unit,difficulty,direction):
    global EXP_ID
    date = datetime.datetime.now().strftime("%Y/%m/%d")

    with open(EXPEDITION_FILE,'ab') as file:
        name1 = name1.ljust(20).encode('utf-8')
        name2 = name2.ljust(20).encode('utf-8')
        date = date.ljust(8).encode('utf-8')
        file.write(struct.pack(EXPEDITION_FORMAT,EXP_ID,name1,name2,en_unit,difficulty,direction,date))
        EXP_ID = EXP_ID+1
        return EXP_ID
def read_expeditions():
    with open(EXPEDITION_FILE,'rb') as file:
        expeditions=[]
        EOF = False
        while not EOF:
            bytes = file.read(EXPEDITION_SIZE)
            if not bytes:
                EOF = True
            else:
                data = struct.unpack(EXPEDITION_FORMAT,bytes)
                data[1] = data[1].decode('utf-8')
                data[2] = data[2].decode('utf-8')
                data[6] = data[6].decode('utf-8')
                expeditions.append(data)    
    return expeditions
