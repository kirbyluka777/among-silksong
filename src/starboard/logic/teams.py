from . import records
import os
import struct
        
TEAM_FILE = 'data\\equipos.bin'
TEAM_FORMAT = 'i20s50s8s3s'
TEAM_SIZE = struct.calcsize(TEAM_FORMAT)

class Team:
    def __init__(self, id, name, email, password, country_code, ods = 1):#, country, ods
        self.id = id
        self.name = name # 20 caracteres
        self.email = email # 
        self.password = password
        self.country_code = country_code
        self.ods = ods

def save_record(data:Team):
    file = open(TEAM_FILE, 'ab')

    id = data.id
    name = data.name.encode('utf-8')
    email = data.email.encode('utf-8')
    password = data.password.encode('utf-8')
    country_code = data.country_code.encode('utf-8')

    packed_data = struct.pack(TEAM_FORMAT, id, name, email, password, country_code)

    file.write(packed_data)

    file.close()

def load_records() -> list[Team]:
    if not os.path.isfile(TEAM_FILE):
        return []
    teams_len = records.get_records_len(TEAM_FILE)
    equipos = [None for _ in range(teams_len)]
    i = 0
    file = open(TEAM_FILE, 'rb')
    file.seek(4)
    while True:
        bytes = file.read(TEAM_SIZE)
        if not bytes:
            file.close()
            return equipos
        id, name, email, password, country_code = struct.unpack(TEAM_FORMAT, bytes)
        name = name.decode('utf-8').strip('\x00')
        email = email.decode('utf-8').strip('\x00')
        password = password.decode('utf-8').strip('\x00')
        country_code = country_code.decode('utf-8').strip('\x00')

        equipos[i] = Team(id, name, email, password, country_code)
        i += 1

def XOR_Encrypt(text, key):
    return ' '.join(str(ord(c) ^ int(key)) for c in text)

def XOR_Decrypt(encrypted_text, key):
    return ''.join(chr(int(num) ^ int(key)) for num in encrypted_text.split())

#por cada caracter lo convierte a su codigo ascii, aplica la operacion XoR (comparar sus binarios para generar otro numero en binario) con el "^" con la clave,convierte ese numero en un caracter y lo va pegando
# ord conviente un caracter a su codigo ascii y chr convierte un numero ascii a caracter, son opuestos

def is_lowercase_letter(c):
    return 'a' <= c <= 'z'

def is_uppercase_case_letter(c):
    return 'A' <= c <= 'Z'

def is_number(c):
    return '0' <= c <= '9'

def is_valid_char(c, allow_chars):
    return is_lowercase_letter(c) or is_uppercase_case_letter(c) or is_number(c) or c in allow_chars

def allowed_chars(password, allow_chars):
    for caracter in password:
        if not is_valid_char(caracter, allow_chars):
            return False
    return True

def contain_number(password):
    for c in password:
        if is_number(c):
            return True
    return False

def contain_lowercase(password):
    for c in password:
        if is_lowercase_letter(c):
            return True
    return False

def contain_uppercase(password):
    for c in password:
        if is_uppercase_case_letter(c):
            return True
    return False

def repeat_3(password):
    for i in range(len(password) - 2):
        if password[i] == password[i+1] == password[i+2]:
            return True
    return False

def search_team(id):
    if not os.path.isfile(TEAM_FILE):
        return None
    teams_len = records.get_records_len(TEAM_FILE)
    if id < 0 or id > teams_len:
        print("id < 0 or id > max len")
        return None
    
    file = open(TEAM_FILE, 'rb')

    file.seek(4 + TEAM_SIZE*(id-1))

    bytes = file.read(TEAM_SIZE)

    id, name, email, password, country = struct.unpack(TEAM_FORMAT, bytes)

    name = name.decode('utf-8').strip('\x00')
    email = email.decode('utf-8').strip('\x00')
    password = password.decode('utf-8').strip('\x00')
    country = country.decode('utf-8').strip('\x00')

    file.close()
    return Team(id,name,email,password,country)

def team_name_exists(team_name):
    if not os.path.isfile(TEAM_FILE):
        return False
    
    file = open(TEAM_FILE, 'rb')

    file.seek(4)
    while True:
        bytes = file.read(TEAM_SIZE)
        if not bytes: return False
        id, name, email, password = struct.unpack(TEAM_FORMAT, bytes)
        name = name.decode('utf-8').strip('\x00')
        if team_name == name:
            return True