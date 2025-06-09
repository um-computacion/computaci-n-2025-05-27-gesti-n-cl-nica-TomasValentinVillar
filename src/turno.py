
from src.paciente import Paciente
from src.medico import Medico
from datetime import datetime

class Turno:
    def __init__(self,paciente:Paciente,medico:Medico,fecha_hora:datetime, especialidad : str):
        self.__paciente = paciente.obtener_dni()
        self.__medico = medico.obtener_matricula()
        self.__fecha_hora = fecha_hora
        self.__especialidad = especialidad


    def obtener_medico(self):
        return self.__medico
    
    def obtener_fecha_hora(self) -> datetime:
        return self.__fecha_hora
    
    #nuevo
    def obtener_especialidad_turno(self):
        return self.__especialidad

    def __str__(self) -> str:
        return f"Turno: Paciente: {self.__paciente} Medico: {self.__medico} Fecha y hora: {self.__fecha_hora} Especialidad: {self.__especialidad}"
