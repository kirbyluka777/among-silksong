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

def load_records():
    if not os.path.isfile(COUNTRY_FILE):
        return
    #result = []
    with open(COUNTRY_FILE, 'rb') as file:
        while True:
            bytes = file.read(COUNTRY_SIZE)
            if not bytes:
                return
            code, name = struct.unpack(COUNTRY_FORMAT, bytes)
            code = code.decode('utf-8').strip("\x00")
            name = name.decode('utf-8').strip("\x00")
            yield Country(code, name)

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr[1:] if x < pivot]
    right = [x for x in arr[1:] if x >= pivot]
    return quicksort(left)+[pivot]+quicksort(right)
#test
def sort_countries():
    p = list(load_records())
    print(*(c.name+' '+c.code+',' for c in p))

    for c in p:
        save_record(c)

    #print(a.name)

if __name__ == "__main__":
    countries = list(load_records())
    sort_countries()