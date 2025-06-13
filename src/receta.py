from src.paciente import Paciente
from src.medico import Medico
from datetime import datetime

class Receta:
    def __init__(self,paciente:Paciente,medico:Medico,medicamentos:list[str]):
        self.__paciente__ = paciente
        self.__medico__ = medico
        self.__medicamentos__ = medicamentos
        self.__fecha__ = datetime.now()

    def obtener_medicamentos(self):
        return self.__medicamentos__

    def __str__(self) -> str:
       return f"Receta: Paciente: {self.__paciente__.obtener_dni()} Medico: {self.__medico__.obtener_matricula()} Medicamentos:{self.__medicamentos__} Fecha: {self.__fecha__}"

