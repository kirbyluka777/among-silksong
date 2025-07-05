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