import re

class Game:
    pass

class Team:
    def __init__(self, name, email, password):#, country, ods
        self.name = name # 20 caracteres
        self.email = email # 
        self.password = password
class Country:
    def __init__(self, code, name):
        self.code = code
        self.name = name

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

def verification(password):
    error = True
    while error:
        error = False

        # Longitud
        while len(password) < 6 or len(password) > 10:
            print("Su contraseña debe tener entre 6 y 10 caracteres")
            password = input("Ingrese una nueva contraseña: ")
            error = True

        # Caracteres válidos
        while not allowed_chars(password, "*=_#"):
            print("Su contraseña posee caracteres inválidos.")
            password = input("Ingrese una nueva contraseña: ")
            error = True

        # Números
        if not contain_number(password):
            print("A su contraseña le faltan números")
            password = input("Ingrese una nueva contraseña: ")
            error = True

        # Letras minúsculas
        if not contain_lowercase(password):
            print("A su contraseña le faltan letras minúsculas")
            password = input("Ingrese una nueva contraseña: ")
            error = True

        # Letras mayúsculas
        if not contain_uppercase(password):
            print("A su contraseña le faltan letras mayúsculas")
            password = input("Ingrese una nueva contraseña: ")
            error = True

        # Repetición de 3 caracteres
        if repeat_3(password):
            print("La contraseña posee 3 caracteres repetidos de manera secuencial")
            password = input("Ingrese una nueva contraseña: ")
            error = True

    print("Contraseña válida")
    return password
