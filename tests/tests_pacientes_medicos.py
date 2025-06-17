import unittest
from unittest.mock import patch
from src.excepciones import PacienteYaExisteError

from src.especialidad import Especialidad
from src.medico import Medico
from src.paciente import Paciente


class TestPacientesYMedicos(unittest.TestCase):

    def setUp(self):
   
        self.__paciente__ = Paciente('46866812','Juan Perez', '11/11/2005')
        self.__especialidad__ = Especialidad("Cirujano",["lunes","miercoles"])
        self.__especialidad2__ = Especialidad("Pediatra",["lunes"])
        self.__medico__=Medico("123","Tomas Villar",[self.__especialidad__,self.__especialidad2__])
    
    def test_paciente_existoso(self):
        self.assertEqual(self.__paciente__.__nombre__, "Juan Perez")
        self.assertEqual(self.__paciente__.__dni__, "46866812")
        self.assertEqual(self.__paciente__.__fecha_nacimiento__, "11/11/2005")

    def test_str_paciente(self):
        representacion = "Paciente: DNI: 46866812 Nombre: Juan Perez Fecha de Nacimiento: 11/11/2005"
        self.assertEqual(str(self.__paciente__),representacion)

    def test_medico_exitoso(self):
        self.assertEqual(self.__medico__.__nombre__,"Tomas Villar")
        self.assertEqual(self.__medico__.obtener_matricula(),"123")
        self.assertEqual(self.__medico__.obtener_especialidades()[0].obtener_especialidad(),"Cirujano")
        self.assertEqual(self.__medico__.obtener_especialidades()[0].obtener_dias(),['lunes','miercoles'])
    
    def test_obtener_especialidad_para_dia(self):
        especialidad_dia = self.__medico__.obtener_especialidad_para_dia("lunes")
        self.assertEqual(especialidad_dia, ["Cirujano","Pediatra"])
        
    def test_str_medico(self):
        representacion = "Medico: Matricula: 123 Nombre: Tomas Villar Especialidades: [Cirujano (Días: lunes, miercoles), Pediatra (Días: lunes)]"
        self.assertEqual(str(self.__medico__),representacion)





    
    

        
if __name__ == '__main__':
    unittest.main()