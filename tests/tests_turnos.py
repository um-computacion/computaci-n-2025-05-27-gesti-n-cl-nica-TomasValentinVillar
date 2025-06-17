import unittest
from datetime import datetime
from unittest.mock import patch
from src.excepciones import PacienteYaExisteError
from src.especialidad import Especialidad
from src.medico import Medico
from src.paciente import Paciente
from src.turno import Turno

class TestTurnos(unittest.TestCase):

    def setUp(self):

        self.__paciente__ = Paciente('46866812','Juan Perez', '11/11/2005')
        self.__especialidad__ = Especialidad("Cirujano",["lunes","miercoles"])
        self.__especialidad2__ = Especialidad("Pediatra",["lunes"])
        self.__medico__=Medico("123","Tomas Villar",[self.__especialidad__,self.__especialidad2__])
        self.__turno__ = Turno(self.__paciente__, self.__medico__,datetime(2025,6,9,16,30),'Cirujano')
    
    def test_turno_exitoso(self):
        self.assertEqual(self.__turno__.obtener_paciente().obtener_dni(),'46866812')
        self.assertEqual(self.__turno__.obtener_medico().obtener_matricula(),'123')
        self.assertEqual(self.__turno__.obtener_fecha_hora(),datetime(2025,6,9,16,30))
        self.assertEqual(self.__turno__.obtener_especialidad_turno(),'Cirujano')
    def test_str_turno(self):
        representacion = 'Turno: Paciente: 46866812 Medico: 123 Fecha y hora: 2025-06-09 16:30:00 Especialidad: Cirujano'
        self.assertEqual(str(self.__turno__), representacion)
    
    
   
if __name__ == '__main__':
    unittest.main()