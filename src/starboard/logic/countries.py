import os
import struct
from . import records

COUNTRY_FILE = "data\\Paises.bin"
COUNTRY_FORMAT = "3s20s"
COUNTRY_SIZE = struct.calcsize(COUNTRY_FORMAT)

class Country:
    def __init__(self, code, name):
        self.code = code
        self.name = name

def save_record(data:Country):
    records.increment_records_len(COUNTRY_FILE)

    file = open(COUNTRY_FILE, 'ab')
    
    code = data.code.encode('utf-8')
    name = data.name.encode('utf-8')

    packed_data = struct.pack(COUNTRY_FORMAT, code, name)

    file.write(packed_data)

def load_records():
    if not os.path.isfile(COUNTRY_FILE):
        return
    
    records_len = records.get_records_len(COUNTRY_FILE)
    records = [None for _ in range(records_len)]
    i = 0

    #result = []
    file = open(COUNTRY_FILE, 'rb')
    file.seek(4)
    while True:
        bytes = file.read(COUNTRY_SIZE)
        if not bytes:
            file.close()
            return records
        code, name = struct.unpack(COUNTRY_FORMAT, bytes)
        code = code.decode('utf-8').strip("\x00")
        name = name.decode('utf-8').strip("\x00")
        records[i] = Country(code,name)
        i +=1

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr[1:] if x < pivot]
    right = [x for x in arr[1:] if x >= pivot]
    return quicksort(left)+[pivot]+quicksort(right)

if __name__ == "__main__":
    countries = list(load_records())