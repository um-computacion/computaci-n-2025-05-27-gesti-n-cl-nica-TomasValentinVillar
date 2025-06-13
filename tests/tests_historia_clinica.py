import unittest
from unittest.mock import patch
from datetime import datetime
from src.especialidad import Especialidad
from src.medico import Medico
from src.paciente import Paciente
from src.receta import Receta
from src.turno import Turno
from src.historia_clinica import HistoriaClinica
class TestHistoriaClinica(unittest.TestCase):
    
    def setUp(self):
        self.__paciente__ = Paciente('46866812','Juan Perez', '11/11/2005')
        self.__especialidad__ = Especialidad("Cirujano",["lunes","miercoles"])
        self.__especialidad2__ = Especialidad("Pediatra",["lunes"])
        self.__medico__= Medico("123","Tomas Villar",[self.__especialidad__,self.__especialidad2__])
        self.__medicamentos__ = ['Ibuprofeno']
        self.__receta__ = Receta(self.__paciente__,self.__medico__,self.__medicamentos__)
        self.__turno__ = Turno(self.__paciente__, self.__medico__,datetime(2025,6,9,16,30),'Cirujano')
        self.__historia_clinca__ = HistoriaClinica(self.__paciente__.obtener_dni())

    def test_historia_clica_turno(self):
        self.__historia_clinca__.agregar_turno(self.__turno__)
        self.assertEqual(self.__historia_clinca__.obtener_turnos()[0].obtener_paciente().obtener_dni(),'46866812')
        self.assertEqual(self.__historia_clinca__.obtener_turnos()[0].obtener_medico().obtener_matricula(),'123')
        self.assertEqual(self.__historia_clinca__.obtener_turnos()[0].obtener_fecha_hora(),datetime(2025,6,9,16,30))
        self.assertEqual(self.__historia_clinca__.obtener_turnos()[0].obtener_especialidad_turno(),'Cirujano')

    def test_historia_clica_receta(self):
        self.__historia_clinca__.agregar_receta(self.__receta__)
        self.assertEqual(self.__historia_clinca__.obtener_recetas()[0].__paciente__.obtener_dni(),'46866812')
        self.assertEqual(self.__historia_clinca__.obtener_recetas()[0].__medico__.obtener_matricula(),'123')
        self.assertEqual(self.__historia_clinca__.obtener_recetas()[0].obtener_medicamentos(),['Ibuprofeno'])
    def test_str_historia_clinica(self):
        turnos_str = "\n  ".join(str(turno) for turno in self.__historia_clinca__.obtener_turnos())
        recetas_str = "\n  ".join(str(receta) for receta in self.__historia_clinca__.obtener_recetas())
        representacion = f"Historia Clinica:\nPaciente: 46866812\nTurnos:\n  {turnos_str}\nRecetas:\n  {recetas_str}"
        self.assertEqual(str(self.__historia_clinca__),representacion)

if __name__ == '__main__':
    unittest.main()