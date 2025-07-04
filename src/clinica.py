from src.historia_clinica import HistoriaClinica
from src.receta import Receta
from src.medico import Medico
from src.turno import Turno
from datetime import datetime
from src.excepciones import (PacienteNoExisteError, PacienteDatosVaciosError,PacienteYaExisteError,MedicoDatosVaciosError, MedicoNoAtiendeEspecialidadError,MedicoNoExisteError, 
TurnoDuplicadoError,MedicoNoTieneEsaEspecialdad,EspecielidadDuplicadaError, EspecialidadDiaInvalido, NoSeIngresaronMedicamentosError, MedicoYaExisteError,DNIInvalidoError, EspecialidadTipoVacioError)

class Clinica:
    def __init__(self):
    
        self.__pacientes__ = {}
        self.__medicos__ = {}
        self.__turnos__ = []
        self.__historias_clinicas__ = {}

    def agregar_paciente(self, paciente):

        dni = paciente.obtener_dni()
        self.__pacientes__[dni] = paciente
        self.__historias_clinicas__[dni] = HistoriaClinica(paciente)
    

    def agregar_medico(self, medico):

        matricula = medico.obtener_matricula()
        self.__medicos__[matricula] = medico     

    def agendar_turno(self,paciente,medico,fecha_hora:datetime,especialidad):
        dni = paciente.obtener_dni()
        matricula = medico.obtener_matricula()
        self.validar_turno_no_duplicado(matricula,fecha_hora,especialidad)
        turno = Turno(paciente,medico,fecha_hora,especialidad)
        self.__turnos__.append(turno)
        historia = self.__historias_clinicas__[dni]
        historia.agregar_turno(turno)
    def obtener_turnos(self):
        return self.__turnos__
    
    def obtener_pacientes(self):
        return self.__pacientes__
    
    def obtener_medicos(self):
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
    
    def validar_existencia_paciente(self,dni,nombre,fecha_nac):
        if dni in self.__pacientes__:
            raise PacienteYaExisteError(f"Paciente con DNI {dni} ya existe")
        if not dni or not nombre or not fecha_nac:
            raise PacienteDatosVaciosError("No se pueden ingresar datos vacios")
            
        
    def validar_existencia_medico(self,matricula,nombre,especialidades):
        if matricula in self.__medicos__:
            raise MedicoYaExisteError(f"Médico con matrícula {matricula} ya existe")
        if not matricula or not nombre or not especialidades:
            raise MedicoDatosVaciosError('No se pueden ingresar datos vacios')

        for esp in especialidades:
            if not esp.obtener_especialidad().strip() or not esp.obtener_dias():
                raise MedicoDatosVaciosError('Cada especialidad debe tener un tipo y al menos un día')
    
    def validar_fecha_nacimiento(self,fecha):
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
            return True
        except ValueError:
            raise ValueError('La fecha de nacimiento debe estar en formato dd/mm/aaaa y debe ser valida')
    
    def validar_fecha_turno(self,fecha):
        try:
            datetime.strptime(fecha, "%Y-%m-%d %H:%M")
            return True
        except ValueError:
            raise ValueError('La fecha del turno debe estar en el formato AAAA-MM-DD HH:MM y debe ser valida')

    def validar_dni(self,dni):

        if len(dni) != 8:
            raise DNIInvalidoError("El DNI debe tener exactamente 8 dígitos")
    
        if not dni.isdigit():
            raise DNIInvalidoError("El DNI solo puede contener números")
    
        return True

    def validar_especialidad(self,medico,especialidad):
        for esp in medico.obtener_especialidades():
            if esp.obtener_especialidad() == especialidad.obtener_especialidad():
                raise EspecielidadDuplicadaError('No se puede agregar especialidad por que ya existe')
        if especialidad.obtener_especialidad() == '':
            raise EspecialidadTipoVacioError('No se puede ingresar datos vacios')
        
        if especialidad.obtener_dias() == []:
            raise EspecialidadTipoVacioError('No se puede ingresar dias vacios')
    
    def validar_especialidad_no_duplicada(self,especialidadades,especialidad): #la diferencia de este con el anteriror es que este sirve para el momento de crear un medico y no para agregar especialidad a medico existente 

        for esp in especialidadades:
            if especialidad.obtener_especialidad() == esp.obtener_especialidad():
                raise EspecielidadDuplicadaError('No se puede agregar especialidad por que ya existe')



    def obtener_dia_semana_en_espanol(self,fecha_hora: datetime) -> str:
        dias_semana = {0: "lunes",1: "martes",2: "miercoles",3: "jueves",4: "viernes",5: "sabado",6: "domingo"}
        return dias_semana[fecha_hora.weekday()]
    
    def obtener_especialidad_disponible(sefl,medico : Medico,dia_semana):
        return medico.obtener_especialidad_para_dia(dia_semana)  
    
    def validar_especialdiad_en_dia(self,medico : Medico,especialidad_solicitada, dia_semana):
        especialidades = []
        for especialidad in medico.obtener_especialidades():
            especialidades.append(especialidad.obtener_especialidad())
        if especialidad_solicitada not in especialidades:
            raise MedicoNoTieneEsaEspecialdad(f"El medico no tiene la especialidad {especialidad_solicitada}")
        if self.obtener_especialidad_disponible(medico,dia_semana) == None:
            raise MedicoNoAtiendeEspecialidadError(f"El medico no atiende la especialidad {especialidad_solicitada} los dias {dia_semana}")
        if especialidad_solicitada not in self.obtener_especialidad_disponible(medico,dia_semana):
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
        
    def obtener_medico_por_matricula(self, matricula):
        if matricula in self.__medicos__:
            return self.__medicos__[matricula]
        else:
            raise MedicoNoExisteError(f"Médico con matrícula {matricula} no existe")
    
    
    def validar_turno_no_duplicado(self, matricula, fecha_hora, especialidad):
        medico = self.obtener_medico_por_matricula(matricula)
        for turno in self.__turnos__:  
            if matricula == turno.obtener_medico().obtener_matricula() and fecha_hora == turno.obtener_fecha_hora(): 
                raise TurnoDuplicadoError("No se puede agendar un turno con el medico y la fecha_hora por que ya existe")
        dia = self.obtener_dia_semana_en_espanol(fecha_hora)
        self.validar_especialdiad_en_dia(medico,especialidad,dia)
        
    def obtener_historia_clinica(self,dni): 

        historia = self.__historias_clinicas__[dni]
        return historia
