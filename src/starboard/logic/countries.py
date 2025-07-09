from . import records
import os
import struct
from . import records

# Archivo binario de países
COUNTRY_FILE = "data/Paises.bin"
COUNTRY_FORMAT = "3s20s"
COUNTRY_SIZE = struct.calcsize(COUNTRY_FORMAT)

# Archivo binario de indice de países por código
COUNTRY_IDX_FILE = "data/paises_indice.bin"
COUNTRY_IDX_FORMAT = "3si"
COUNTRY_IDX_SIZE = struct.calcsize(COUNTRY_IDX_FORMAT)

# Estructura para representar países
class Country:
    def __init__(self, code, name):
        self.code = code
        self.name = name

# Guarda un país en archivo, generar el archivo indice ordenado con el nuevo registro
def save_record(data:Country):
    index = records.increment_records_len(COUNTRY_FILE)

    file = open(COUNTRY_FILE, 'ab')
    
    code = data.code.encode('utf-8')
    name = data.name.encode('utf-8')

    packed_data = struct.pack(COUNTRY_FORMAT, code, name)

    file.write(packed_data)
    
    file.close()

    add_index_and_sort_by_code(data.code, index - 1)

# Carga los registros de paises (de forma desordenada)
def load_records() -> list[Country]:
    if not os.path.isfile(COUNTRY_FILE):
        return []
    
    records_len = records.get_records_len(COUNTRY_FILE)
    countries = [None for _ in range(records_len)]
    i = 0

    file = open(COUNTRY_FILE, 'rb')
    file.seek(4)
    while True:
        data = file.read(COUNTRY_SIZE)
        if not data:
            file.close()
            return countries
        countries[i] = unpack_country_from_bytes(data)
        i +=1

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr[1:] if x < pivot]
    right = [x for x in arr[1:] if x >= pivot]
    return quicksort(left)+[pivot]+quicksort(right)

# Lee el archivo indice y lo retorna como dos arreglos (codigos e indices)
def load_index() -> list[(str, int)]:
    if not os.path.isfile(COUNTRY_IDX_FILE):
        return []
    
    records_len = records.get_records_len(COUNTRY_IDX_FILE)
    indices = [None for _ in range(records_len)]
    i = 0

    file = open(COUNTRY_IDX_FILE, 'rb')
    file.seek(4)
    while True:
        bytes = file.read(COUNTRY_IDX_SIZE)
        if not bytes:
            file.close()
            return indices
        code, index = struct.unpack(COUNTRY_IDX_FORMAT, bytes)
        code = code.decode('utf-8').strip("\x00")
        indices[i] = code, index
        i +=1

# Crea un archivo indice ordernado alfabeticamente por el código del país
def add_index_and_sort_by_code(code: str, index: int):
    # Construimos arreglo de indices por cada país con desorden original
    # Cargamos el indice actual sin el nuevo registro
    old_indices = load_index()
    # Creamos el nuevo indice con el tamaño adicional
    new_size = len(old_indices) + 1
    new_indices = [0 for _ in range(new_size)]
    for i in range(0, new_size, +1):
        new_indices[i] = i
    # Agregamos el nuevo indice al final
    new_indices[new_size-1] = index

    # Ordenamos los indices en base a su código usando método de inserción
    # Empezamos al final porque ya sabemos que el indice hacía atrás está ordenado
    for i in range(1, new_size):
        current = new_indices[i]
        current_code = code if i == index else old_indices[new_indices[i]][0]
        j = i - 1
        while j >= 0 and old_indices[new_indices[j]][0] > current_code:
            new_indices[j + 1] = new_indices[j]
            j -= 1
        new_indices[j + 1] = current
    
    # Abrimos el archivo indice que guardará los indices de los paises ordenados por código alfabeticamente
    file = open(COUNTRY_IDX_FILE, "wb")
    records_len_bytes = struct.pack("i", new_size)
    file.write(records_len_bytes)

    # Escribimos los indices ordenados en el archivo indice
    for i in range(0, new_size, +1):
        target_code = code if new_indices[i] == index else old_indices[new_indices[i]][0]
        target_index = index if new_indices[i] == index else old_indices[new_indices[i]][1]
        index_record = struct.pack(COUNTRY_IDX_FORMAT, target_code.encode("utf-8"), target_index)
        file.write(index_record)
    
    # Cerramos archivo de indice
    file.close()

# Desempaca de datos binarios un país
def unpack_country_from_bytes(data: bytes):
    code, name = struct.unpack(COUNTRY_FORMAT, data)
    code = code.decode('utf-8').strip("\x00")
    name = name.decode('utf-8').strip("\x00")
    return Country(code, name)

# Obtiene un pais por indice
def get_country_at(index: int):
    file = open(COUNTRY_FILE, "rb")
    file.seek(4 + COUNTRY_SIZE * index)
    data = file.read(COUNTRY_SIZE)
    return unpack_country_from_bytes(data)

# Realiza una búsqueda binaria en el archivo indice de paises por código
def search_country_by_code(code: str):
    indices = load_index()
    left = 0
    right = len(indices) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if indices[mid][0] < code:
            left = mid + 1
        elif indices[mid][0] > code:
            right = mid - 1
        else:
            return get_country_at(indices[mid][1])
    return None
