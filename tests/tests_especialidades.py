import unittest

from src.especialidad import Especialidad


class TestEspecialidades(unittest.TestCase):
    def setUp(self):
        self.__especialidad__ = Especialidad("Cirujano",["lunes","miercoles"])
    
    def test_especialidad_exitoso(self):
        self.assertEqual(self.__especialidad__.obtener_especialidad(),"Cirujano")
        self.assertEqual(self.__especialidad__.obtener_dias(),["lunes","miercoles"])
    
    def test_verificar_dia(self):
        self.assertTrue(self.__especialidad__.verificar_dia("lunes"))
        self.assertFalse(self.__especialidad__.verificar_dia("martes"))
    
    def test_str_especialidad(self):
        representacion = 'Cirujano (Días: lunes, miercoles)'
        self.assertEqual(str(self.__especialidad__),representacion)
       
   
if __name__ == '__main__':
    unittest.main()