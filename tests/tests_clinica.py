import unittest
from datetime import datetime
from src.clinica import Clinica
from src.especialidad import Especialidad
from src.medico import Medico
from src.paciente import Paciente
from src.excepciones import (PacienteNoExisteError, PacienteDatosVaciosError,PacienteYaExisteError,MedicoDatosVaciosError, MedicoNoAtiendeEspecialidadError,MedicoNoExisteError, 
TurnoDuplicadoError,MedicoNoTieneEsaEspecialdad,EspecielidadDuplicadaError, EspecialidadDiaInvalido, NoSeIngresaronMedicamentosError, MedicoYaExisteError,DNIInvalidoError)


class TestClinica(unittest.TestCase):
    
    def setUp(self):
        self.__clinica__ = Clinica()
        self.__paciente__ = Paciente("46866812", "Juan","11/11/2005")
        self.__especialidad__ = Especialidad("Cirujano",["lunes","miercoles"])
        self.__medico__ = Medico("123","Tomas",[self.__especialidad__])
        self.__medicamentos__ = ['Ibuprofeno']

    def test_agregar_paciente(self):
        self.__clinica__.agregar_paciente(self.__paciente__)
        self.assertEqual(self.__clinica__.__pacientes__['46866812'].obtener_dni(),'46866812')
        self.assertIsNotNone(self.__clinica__.__historias_clinicas__['46866812'])
    
    def test_agregar_medico(self):
        self.__clinica__.agregar_medico(self.__medico__)
        self.assertEqual(self.__clinica__.__medicos__['123'].obtener_matricula(),'123')
    
    def test_agregar_especialidad_medico(self):

        especialidad2 = Especialidad('Pediatra',['martes','jueves'])
        self.__clinica__.agregar_medico(self.__medico__)
        self.__clinica__.agregar_especilidad_medico(self.__medico__,especialidad2)

        self.assertEqual(self.__clinica__.__medicos__['123'].obtener_especialidades()[1].obtener_especialidad(),'Pediatra')
        self.assertEqual(self.__clinica__.__medicos__['123'].obtener_especialidades()[1].obtener_dias(),['martes','jueves'])

    def test_agendar_turno(self): #los posibles errores de agemdar turno se testean mas adelante

        self.__clinica__.agregar_medico(self.__medico__)
        self.__clinica__.agregar_paciente(self.__paciente__)
        self.__clinica__.agendar_turno(self.__paciente__,self.__medico__,datetime(2025,6,9,16,30),'Cirujano')
        self.assertEqual(self.__clinica__.obtener_turnos()[0].obtener_paciente().obtener_dni(),'46866812')
        self.assertEqual(self.__clinica__.obtener_turnos()[0].obtener_medico().obtener_matricula(),'123')
        self.assertEqual(self.__clinica__.obtener_turnos()[0].obtener_fecha_hora(),datetime(2025,6,9,16,30))
        self.assertEqual(self.__clinica__.obtener_turnos()[0].obtener_especialidad_turno(),'Cirujano')    
    def test_emitir_receta(self):
        

        self.__clinica__.agregar_paciente(self.__paciente__)
        self.__clinica__.emitir_recetas(self.__paciente__,self.__medico__,self.__medicamentos__)
        

        historia = self.__clinica__.obtener_historia_clinica('46866812')
        receta = historia.obtener_recetas()[0]
        self.assertIsNotNone(receta)
        self.assertEqual(receta.__medico__.obtener_matricula(), '123')
        self.assertEqual(receta.__paciente__.obtener_dni(), '46866812')
        self.assertEqual(receta.__medicamentos__, ['Ibuprofeno'])
    
    def test_emitir_receta_sin_medicamentos(self):
        
        medicamentos = ['']
        self.__clinica__.agregar_paciente(self.__paciente__)
        self.__clinica__.agregar_medico(self.__medico__)
        with self.assertRaises(NoSeIngresaronMedicamentosError):
            self.__clinica__.emitir_recetas(self.__paciente__,self.__medico__,medicamentos)
    
    def test_validar_paciente_ya_existe(self):

        self.__clinica__.agregar_paciente(self.__paciente__)

        with self.assertRaises(PacienteYaExisteError):
            self.__clinica__.validar_existencia_paciente("46866812", "Juan","11/11/2005")
    
    def test_validar_paciente_datos_vacios(self):

        with self.assertRaises(PacienteDatosVaciosError):
            Paciente('46866812','Juan','')
            self.__clinica__.validar_existencia_paciente('46866812','Juan','')
        with self.assertRaises(PacienteDatosVaciosError):
            Paciente('46866812','','11/11/2005')
            self.__clinica__.validar_existencia_paciente('46866812','','11/11/2005')
        with self.assertRaises(PacienteDatosVaciosError):
            Paciente('','Juan','11/11/2005')
            self.__clinica__.validar_existencia_paciente('','Juan','11/11/2005')
    
    def test_validar_medico_ya_existe(self):

        self.__clinica__.agregar_medico(self.__medico__)

        with self.assertRaises(MedicoYaExisteError):
            self.__clinica__.validar_existencia_medico("123", "Tomas",[self.__especialidad__])
    
    def test_validar_medico_datos_vacios(self):

        with self.assertRaises(MedicoDatosVaciosError):
            Medico('123','Tomas',[])
            self.__clinica__.validar_existencia_medico('123','Tomas',[])
        with self.assertRaises(MedicoDatosVaciosError):
            Medico('123','',[self.__especialidad__])
            self.__clinica__.validar_existencia_medico('123','',[self.__especialidad__])
        with self.assertRaises(MedicoDatosVaciosError):
            Medico('','Tomas',[self.__especialidad__])
            self.__clinica__.validar_existencia_medico('','Tomas',[self.__especialidad__])
    
    def test_validar_medico_especialidad(self):
        
        with self.assertRaises(MedicoDatosVaciosError):
            especialidad = Especialidad('',['lunes','miercoles'])
            Medico('123','Tomas',especialidad)
            self.__clinica__.validar_existencia_medico('123','Tomas',[especialidad])

        with self.assertRaises(MedicoDatosVaciosError):
            especialidad = Especialidad('Dermatologo',[])
            Medico('123','Tomas',especialidad)
            self.__clinica__.validar_existencia_medico('123','Tomas',[especialidad])
    
    def test_valiadar_fecha_nacimiento(self):

        self.assertTrue(self.__clinica__.validar_fecha_nacimiento('11/11/2005'))

        with self.assertRaises(ValueError):
            self.__clinica__.validar_fecha_nacimiento('11-11-2005')#o cualquier formato distinto a dd/mm/aaaa
    
    def test_validar_dni(self):

        self.assertTrue(self.__clinica__.validar_dni('46866812'))
        
        with self.assertRaises(DNIInvalidoError):
            self.__clinica__.validar_dni('468')
        
        with self.assertRaises(DNIInvalidoError):
            self.__clinica__.validar_dni('aaaaaaaa')

    def test_validar_especialidad(self):
        with self.assertRaises(EspecielidadDuplicadaError):
            especialidad = Especialidad('Cirujano',['lunes','martes'])
            self.__clinica__.validar_especialidad(self.__medico__,especialidad)

    def test_validar_especialidad_duplicada(self):
        with self.assertRaises(EspecielidadDuplicadaError):
            especialidad1 = Especialidad('Cirujano',['lunes','martes'])
            especialidad2 = Especialidad('Pediatra',['miercoles'])
            especialidades = [especialidad1,especialidad2]
            especialidad3 = Especialidad('Cirujano',['lunes'])

            self.__clinica__.validar_especialidad_no_duplicada(especialidades, especialidad3)

    def test_obtener_dia_de_la_semana(self):
        self.assertEqual(self.__clinica__.obtener_dia_semana_en_espanol(datetime(2025,6,9,16,30)),'lunes')
        self.assertEqual(self.__clinica__.obtener_dia_semana_en_espanol(datetime(2025,6,10,16,30)),'martes')
        self.assertEqual(self.__clinica__.obtener_dia_semana_en_espanol(datetime(2025,6,11,16,30)),'miercoles')
        self.assertEqual(self.__clinica__.obtener_dia_semana_en_espanol(datetime(2025,6,12,16,30)),'jueves')
        self.assertEqual(self.__clinica__.obtener_dia_semana_en_espanol(datetime(2025,6,13,16,30)),'viernes')
        self.assertEqual(self.__clinica__.obtener_dia_semana_en_espanol(datetime(2025,6,14,16,30)),'sabado')
        self.assertEqual(self.__clinica__.obtener_dia_semana_en_espanol(datetime(2025,6,15,16,30)),'domingo')
    def test_medico_no_tiene_esa_especialidad(self):
            
        with self.assertRaises(MedicoNoTieneEsaEspecialdad):    
            self.__clinica__.validar_especialdiad_en_dia(self.__medico__,'Pediatra','lunes')
    
    def test_medico_no_atiende_ese_dia(self):
            
        with self.assertRaises(MedicoNoAtiendeEspecialidadError):    
            self.__clinica__.validar_especialdiad_en_dia(self.__medico__,'Cirujano','viernes')
    def test_valdidar_dias(self):

        with self.assertRaises(EspecialidadDiaInvalido):
            especialidad = Especialidad('Cirujano',['dias'])#los dias deben ser palabras distintas a los dias de la semana para pasar el test
            self.__clinica__.validar_dias(especialidad)
    
    def test_get_paciente_exitoso(self):
        self.__clinica__.agregar_paciente(self.__paciente__)
        self.assertEqual(self.__clinica__.get_paciente('46866812'),self.__clinica__.__pacientes__['46866812'])
    
    def test_get_paciente_no_existe(self):
        self.__clinica__.agregar_paciente(self.__paciente__)
        with self.assertRaises(PacienteNoExisteError):
                self.__clinica__.get_paciente('47866812')

    def test_obtener_medico_por_matricula_exitoso(self):
        self.__clinica__.agregar_medico(self.__medico__)
        self.assertEqual(self.__clinica__.obtener_medico_por_matricula('123'),self.__clinica__.__medicos__['123'])
    
    def test_obtener_medico_por_matricula_no_existe(self):
        self.__clinica__.agregar_medico(self.__medico__)
        with self.assertRaises(MedicoNoExisteError):
                self.__clinica__.obtener_medico_por_matricula('456')
    
    def test_revisar_turno_duplicado(self): #los otros posibles problemas con los los turnos son testeados en test_medico_no_tiene_esa_especialidad y test_medico_no_atiende_ese_dia
        self.__clinica__.agregar_medico(self.__medico__)
        self.__clinica__.agregar_paciente(self.__paciente__)
        self.__clinica__.agendar_turno(self.__paciente__,self.__medico__,datetime(2025,6,9,16,30),'Cirujano')
        paciente = Paciente('123','Sebastian', '02/06/1972')
        with self.assertRaises(TurnoDuplicadoError):
            self.__clinica__.validar_turno_no_duplicado(self.__medico__.obtener_matricula(),datetime(2025,6,9,16,30),'Cirujano')

    
    def test_obtener_historia_clinica(self):
        self.__clinica__.agregar_paciente(self.__paciente__)
        self.assertEqual(self.__clinica__.obtener_historia_clinica('46866812'),self.__clinica__.__historias_clinicas__['46866812'])



