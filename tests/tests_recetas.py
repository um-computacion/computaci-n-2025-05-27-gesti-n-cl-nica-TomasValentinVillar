import unittest
from unittest.mock import patch
from datetime import datetime
from src.especialidad import Especialidad
from src.medico import Medico
from src.paciente import Paciente
from src.receta import Receta


class TestRecetas(unittest.TestCase):
    
    def setUp(self):
        self.__especialidad__ = Especialidad("Cirujano",["lunes","miercoles"])
        self.__medicamentos__ = ['Ibuprofeno']
        self.__receta__ = Receta(Paciente("46866812", "Juan","11/11/2005"),Medico("123","Tomas",[self.__especialidad__]),self.__medicamentos__)

    
    def test_receta_exitoso(self):

        self.assertEqual(self.__receta__.__paciente__.obtener_dni(), '46866812')
        self.assertEqual(self.__receta__.__medico__.obtener_matricula(), '123')
        self.assertEqual(self.__receta__.__medicamentos__, ['Ibuprofeno'])

    def test_str_receta(self):
        representacion = f"Receta: Paciente: 46866812 Medico: 123 Medicamentos:['Ibuprofeno'] Fecha: {self.__receta__.__fecha__}"
        self.assertEqual(str(self.__receta__),representacion)