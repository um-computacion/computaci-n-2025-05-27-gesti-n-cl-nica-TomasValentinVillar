from src.paciente import Paciente
from src.medico import Medico
from datetime import datetime

class Receta:
    def __init__(self,paciente:Paciente,medico:Medico,medicamentos:list[str]): #en cosigna dice dice datetime.now()
        self.__paciente = paciente.obtener_dni()
        self.__medico = medico.obtener_matricula()
        self.__medicamentos = medicamentos
        self.__fecha = datetime.now()

    def obtener_medicamentos(self):
        return self.__medicamentos

    def __str__(self) -> str:
       return f"Receta: Paciente: {self.__paciente} Medico: {self.__medico} Medicamentos:{self.__medicamentos} Fecha: {self.__fecha}"

