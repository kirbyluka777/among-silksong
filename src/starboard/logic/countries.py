import os
import struct

COUNTRY_FILE = "Paises.bin"
COUNTRY_FORMAT = "3s20s"
COUNTRY_SIZE = struct.calcsize(COUNTRY_FORMAT)

class Country:
    def __init__(self, code, name):
        self.code = code
        self.name = name

def save_record(data:Country):
    with open(COUNTRY_FILE, 'ab') as file:
        code = data.code.encode('utf-8')
        name = data.name.encode('utf-8')

        packed_data = struct.pack(COUNTRY_FORMAT, code, name)

        file.write(packed_data)

def load_records(game):
    if not os.path.isfile(COUNTRY_FILE):
        return []
    result = []
    with open(COUNTRY_FILE, 'rb') as file:
        while True:
            bytes = file.read(COUNTRY_SIZE)
            if not bytes:
                return result
            code, name = struct.unpack(COUNTRY_SIZE, bytes)
            code = code.decode('utf-8').strip("\x00")
            name = name.decode('utf-8').strip("\x00")
            result.append(Country(code, name))
