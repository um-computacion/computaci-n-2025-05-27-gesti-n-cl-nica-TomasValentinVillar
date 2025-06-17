
class Paciente:
    def __init__(self, dni:str, nombre:str, fecha_nacimiento:str):
        self.__dni__ = dni
        self.__nombre__ = nombre
        self.__fecha_nacimiento__ = fecha_nacimiento
    def obtener_dni(self) -> str:
        return self.__dni__
    def __str__(self) -> str:
        return f"Paciente: DNI: {self.__dni__} Nombre: {self.__nombre__} Fecha de Nacimiento: {self.__fecha_nacimiento__}"
