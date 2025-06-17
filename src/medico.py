from src.especialidad import Especialidad

class Medico:
    def __init__(self, matricula:str, nombre:str, especialidades:list[Especialidad]):
        self.__matricula__ = matricula
        self.__nombre__ = nombre
        self.__especialidades__ = especialidades 

    def agregar_especialidad(self, especialidad : Especialidad):
        self.__especialidades__.append(especialidad)

    def obtener_matricula(self) -> str:
        return self.__matricula__
    
    def obtener_especialidades(self):
        return self.__especialidades__
    
    def obtener_especialidad_para_dia(self, dia:str) -> str:
        especialidades = []
       
        for especialidad in self.__especialidades__:
            if especialidad.verificar_dia(dia) == True:
                especialidades.append(especialidad.obtener_especialidad())
        
        if especialidades == []:
            return None
        else:
            return especialidades
    
    def __str__(self) -> str:
        especialidades_str = ", ".join(str(e) for e in self.__especialidades__)
        return f"Medico: Matricula: {self.__matricula__} Nombre: {self.__nombre__} Especialidades: [{especialidades_str}]"
