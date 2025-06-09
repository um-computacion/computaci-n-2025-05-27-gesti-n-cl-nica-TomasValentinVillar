
class Paciente:
    def __init__(self, dni:str, nombre:str, fecha_nacimiento:str):
        self.__dni = dni
        self.__nombre = nombre
        self.__fecha_nacimiento = fecha_nacimiento
    def obtener_dni(self) -> str:
        return self.__dni
    def __str__(self) -> str:
        return f"Paciente: DNI: {self.__dni} Nombre: {self.__nombre} Fecha de Nacimiento: {self.__fecha_nacimiento}"
