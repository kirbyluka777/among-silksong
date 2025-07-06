import struct

COUNTRY_FILE = "Paises.bin"
COUNTRY_FORMAT = "3s20s"
COUNTRY_SIZE = struct.calcsize(COUNTRY_FORMAT)

class Country:
	def init(self,id,name):
		self.id = id
		self.name = name

def save_country(country):
	with open (COUNTRY_FILE,'ab') as file:
		country_name = country.name.ljust(20).encode('utf-8')
		file.write(struct.pack(COUNTRY_FORMAT,country.id,country_name))

def read_countries():
	countries=[]
	with open(COUNTRY_FILE,'rb') as file:
		EOF=False
		while not EOF:
			data_bytes=file.read(COUNTRY_SIZE)
			if not data_bytes:
				EOF=True
			else:
				data=struct.unpack(COUNTRY_FORMAT,data_bytes)
                #esta es una nota para paulo del futuro, acuerdate de no hacerlo tan horrible, bobo
				country=Country(data[0].decode('utf-8'),data[1].decode('utf-8').strip())
				countries.append(country)
	return countries
