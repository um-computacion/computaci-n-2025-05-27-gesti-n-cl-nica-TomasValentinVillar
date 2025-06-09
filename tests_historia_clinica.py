import unittest
from main import Paciente, Medico, Turno, Receta, HistoriaClinica, Clinica, CLI, PacienteYaExisteError
from datetime import datetime
from unittest.mock import patch

class TestRecetas(unittest.TestCase):
    
    def setUp(self):
        self.__cli__ = CLI()
    
    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Pérez', '15/03/1990',
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin','fin',
                     '3', '46866812', '123', '2025-06-09 16:30','Cirujano',
                     '5', '46866812', '123', 'Ibuprofeno','fin', '0'])
    def test_historia_clinica_exitosa(self, patch_input):
        self.__cli__.ejecutar()

        historia = self.__cli__.clinica.obtener_historia_clinica('46866812')
        receta = historia.obtener_recetas()[0]
        turno = historia.obtener_turnos()[0]
        self.assertIsNotNone(receta)
        self.assertEqual(receta._Receta__medico, '123')
        self.assertEqual(receta._Receta__paciente, '46866812')
        self.assertEqual(receta._Receta__medicamentos, ['Ibuprofeno'])
        self.assertIsNotNone(turno)
        self.assertEqual(turno.obtener_medico(), '123')
        self.assertEqual(turno._Turno__paciente, '46866812')
        self.assertEqual(turno.obtener_fecha_hora(), datetime(2025,6,9,16,30))
        self.assertEqual(turno.obtener_especialidad_turno(), 'Cirujano')
if __name__ == '__main__':
    unittest.main()