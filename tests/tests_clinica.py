import unittest
from unittest.mock import patch
from src.clinica import Clinica
from src.especialidad import Especialidad
from src.medico import Medico
from src.paciente import Paciente


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
    

    
    def test_emitir_receta(self):
        

        self.__clinica__.agregar_paciente(self.__paciente__)
        self.__clinica__.emitir_recetas(self.__paciente__,self.__medico__,self.__medicamentos__)
        

        historia = self.__clinica__.obtener_historia_clinica('46866812')
        receta = historia.obtener_recetas()[0]
        self.assertIsNotNone(receta)
        self.assertEqual(receta.__medico__.obtener_matricula(), '123')
        self.assertEqual(receta.__paciente__.obtener_dni(), '46866812')
        self.assertEqual(receta.__medicamentos__, ['Ibuprofeno'])