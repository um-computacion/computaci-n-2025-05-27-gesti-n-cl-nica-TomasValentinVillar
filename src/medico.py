from src.especialidad import Especialidad

class Medico:
    def __init__(self, matricula:str, nombre:str, especialidades:list[Especialidad]):
        self.__matricula = matricula
        self.__nombre = nombre
        self.__especialidades = especialidades 

    def agrgar_especialidad(self, especialidad : Especialidad):
        self.__especialidades.append(especialidad)

    def obtener_matricula(self) -> str:
        return self.__matricula
    def obtener_especialdades(self):
        return self.__especialidades
    def obtener_especialidad_para_dia(self, dia:str) -> str:
        for especialidad in self.__especialidades:
            if dia in especialidad.obtener_dias():
                return especialidad.obtener_especialidad()
        return None
    def __str__(self) -> str:
        especialidades_str = ", ".join(str(e) for e in self.__especialidades)
        return f"Medico: Matricula: {self.__matricula} Nombre: {self.__nombre} Especialidades: [{especialidades_str}]"
