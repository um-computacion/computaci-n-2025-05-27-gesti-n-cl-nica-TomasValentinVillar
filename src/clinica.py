from src.historia_clinica import HistoriaClinica
from src.receta import Receta
from src.medico import Medico
from src.turno import Turno
from datetime import datetime
from src.excepciones import (PacienteNoExisteError, PacienteDatosVaciosError,PacienteYaExisteError,MedicoDatosVaciosError, MedicoNoAtiendeEspecialidadError,MedicoNoExisteError, 
TurnoDuplicadoError, EspecialidadNoExisteError,MedicoNoTieneEsaEspecialdad,EspecielidadDuplicadaError, EspecialidadDiaInvalido, NoSeIngresaronMedicamentosError, MedicoYaExisteError)

class Clinica:
    def __init__(self):
    
        self.__pacientes__ = {}
        self.__medicos__ = {}
        self.__turnos__ = []
        self.__historias_clinicas__ = {}

    def agregar_paciente(self, paciente):

        dni = paciente.obtener_dni()
        self.__pacientes__[dni] = paciente
        self.__historias_clinicas__[dni] = HistoriaClinica(dni)
    

    def agregar_medico(self, medico):

        matricula = medico.obtener_matricula()
        self.__medicos__[matricula] = medico     

    def agendar_turno(self,paciente,medico,fecha_hora:datetime,especialidad):
        dni = paciente.obtener_dni()
        matricula = medico.obtener_matricula()
        self.revisar_turno(matricula,fecha_hora,especialidad)
        turno = Turno(paciente,medico,fecha_hora,especialidad)
        self.__turnos__.append(turno)
        historia = self.__historias_clinicas__[dni]
        historia.agregar_turno(turno)
    def obtener_turnos(self):
        return self.__turnos__
    
    def obtener_pacientes(self): #Hago este metodo para que el CLI pueda mostrar todos los pacientes
        return self.__pacientes__
    
    def obtener_medicos(self): #Hago este metodo para que el CLI pueda mostrar todos los medicos
        return self.__medicos__

    def agregar_especilidad_medico(self,medico,especialidad):
        
        medico.agregar_especialidad(especialidad)
        
    def emitir_recetas(self,paciente,medico,medicamentos):
        dni = paciente.obtener_dni()
        matricula = medico.obtener_matricula()

        
        if medicamentos == ['']:
            raise NoSeIngresaronMedicamentosError("No se ingresaron medicamentos")
        receta = Receta(paciente,medico,medicamentos)
        
        historia = self.__historias_clinicas__[dni]
        historia.agregar_receta(receta)
        return f'Receta emitida: Paciente: {dni} Medico: {matricula} Medicamentos:{medicamentos} Fecha {receta.__fecha__}'
    
    def validar_paciente(self,dni,nombre,fecha_nac):
        if dni in self.__pacientes__:
            raise PacienteYaExisteError(f"Paciente con DNI {dni} ya existe")
        if not dni or not nombre or not fecha_nac:
            raise PacienteDatosVaciosError("No se pueden ingresar datos vacios")
            
        
    def validar_medico(self,matricula,nombre,especialidades):
        if matricula in self.__medicos__:
            raise MedicoYaExisteError(f"Médico con matrícula {matricula} ya existe")
        if not matricula or not nombre or not especialidades:
            raise MedicoDatosVaciosError('No se pueden ingresar datos vacios')

        for esp in especialidades:
            if not esp.obtener_especialidad().strip() or not esp.obtener_dias():
                raise MedicoDatosVaciosError('Cada especialidad debe tener un tipo y al menos un día')
    def validar_especialidad(self,medico,especialidad):
        for esp in medico.obtener_especialidades():
            if esp.obtener_especialidad() == especialidad.obtener_especialidad():
                raise EspecielidadDuplicadaError('No se puede agregar especialidad por que ya existe')



    def obtener_dia_semana_en_espanol(self,fecha_hora: datetime) -> str:
        dias_semana = {0: "lunes",1: "martes",2: "miercoles",3: "jueves",4: "viernes",5: "sabado",6: "domingo"}
        return dias_semana[fecha_hora.weekday()]
    
      
    
    def validar_especialdiad_en_dia(self,medico : Medico,especialidad_solicitada, dia_semana): #si no puede ser entrada matricula y get_medico
        especialidades = []
        for especialidad in medico.obtener_especialidades():
            especialidades.append(especialidad.obtener_especialidad())
        if especialidad_solicitada not in especialidades:
            raise MedicoNoTieneEsaEspecialdad(f"El medico no tiene la especialidad {especialidad_solicitada}")
        if especialidad_solicitada not in medico.obtener_especialidad_para_dia(dia_semana):
            raise MedicoNoAtiendeEspecialidadError(f"El medico no atiende la especialidad {especialidad_solicitada} los dias {dia_semana}")
        
        

        
    def validar_dias(self,especialidad):

        for dia in especialidad.obtener_dias():
            if dia not in ['lunes','martes','miercoles','jueves','viernes','sabado','domingo']:
                raise EspecialidadDiaInvalido("Los dias ingresados deben ser válidos")
        
    def get_paciente(self,dni):
        if dni in self.__pacientes__:
            return self.__pacientes__[dni]
        else:
            raise PacienteNoExisteError(f"Paciente con DNI {dni} no existe")
        
    def get_medico(self, matricula): #equivale a obtener_medico_por_matricula
        if matricula in self.__medicos__:
            return self.__medicos__[matricula]
        else:
            raise MedicoNoExisteError(f"Médico con matrícula {matricula} no existe")
    
    
    def revisar_turno(self, matricula, fecha_hora, especialidad):
        medico = self.get_medico(matricula)
        for turno in self.__turnos__:  
            if matricula == turno.obtener_medico().obtener_matricula() and fecha_hora == turno.obtener_fecha_hora(): 
                raise TurnoDuplicadoError("No se puede agendar un turno con el medico y la fecha_hora por que ya existe")
        dia = self.obtener_dia_semana_en_espanol(fecha_hora)
        self.validar_especialdiad_en_dia(medico,especialidad,dia)
        
    def obtener_historia_clinica(self,dni): 

        historia = self.__historias_clinicas__[dni]
        return historia
