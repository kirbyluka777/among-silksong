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

def allowed_chars(password, allow_chars):   # Verificar caracteres invalidos en la contrasena
    for caracter in password:
        if not (caracter.isalnum() or caracter in allow_chars): #esto tambien
            return False
    return True

def verification(password):     #Verificar la contrasena
    error = True
    while error:
        error = False

        # Longitud
        while len(password) < 6 or len(password) > 10:
            print("Su contraseña debe tener entre 6 y 10 caracteres")
            password = input("Ingrese una nueva contraseña: ")
            error = True

        # Caracteres vqlidos
        while not allowed_chars(password, "*=_#"):
            print("Su contraseña posee caracteres invalidos.")
            password = input("Ingrese una nueva contraseña: ")
            error = True

        # Numeros
        if not re.search(r"\d", password):
            print("A su contraseña le faltan numeros")
            password = input("Ingrese una nueva contraseña: ")
            error = True

        # Letras minusculas
        if not re.search(r"[a-z]", password):
            print("A su contraseña le faltan letras minusculas")
            password = input("Ingrese una nueva contraseña: ")
            error = True
        
        # Letras mayusculas
        if not re.search(r"[A-Z]", password):
            print("A su contraseña le faltan letras mayusculas")
            password = input("Ingrese una nueva contraseña: ")
            error = True
#paulo, no seas imbecil, arregla lo del re no puedes usarlo
        # Repeticion de 3 caracteres
        i = 0
        while i <= len(password) - 3:
            if password[i] == password[i+1] == password[i+2]:
                print("La contraseña posee 3 caracteres repetidos de manera secuencial")
                password = input("Ingrese una nueva contraseña: ")
                error = True
                i=len(password)
            i += 1

    print("Contrasena valida")
    return password

def XOR_Encrypt(text, key):
    return ' '.join(str(ord(c) ^ int(key)) for c in text)

def XOR_Decrypt(encrypted_text, key):
    return ''.join(chr(int(num) ^ int(key)) for num in encrypted_text.split())

#por cada caracter lo convierte a su codigo ascii, aplica la operacion XoR (comparar sus binarios para generar otro numero en binario) con el "^" con la clave,convierte ese numero en un caracter y lo va pegando
# ord conviente un caracter a su codigo ascii y chr convierte un numero ascii a caracter, son opuestos
