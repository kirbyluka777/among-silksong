import os
import struct

def get_records_len(filename):
    if not os.path.isfile(filename):
        return 0
    file = open(filename, 'rb')
    records_len_bytes = file.read(4)
    records_len, = struct.unpack("i", records_len_bytes)
    return records_len

def increment_records_len(filename) -> int:
    # Si el archivo no existe, inicializarlo con una cantidad de 1
    if not os.path.isfile(filename):
        file = open(filename, 'wb')
        initial_size = struct.pack("i", 1)
        file.write(initial_size)
        file.close()
        return 1
    else:
        # Abrir archivo en modo tanto escritura y lectura binaria
        file = open(filename, 'r+b')

        # Leer la cantidad de registro actuales
        file.seek(0)
        records_len_bytes = file.read(4)
        records_len, = struct.unpack("i", records_len_bytes)
        
        # Incrementar la cantidad
        new_records_len = records_len + 1

        # Guardar nueva cantidad
        file.seek(0)
        records_len_bytes = struct.pack("i", new_records_len)
        file.write(records_len_bytes)

        # cerramos archivo
        file.close()
        return new_records_len