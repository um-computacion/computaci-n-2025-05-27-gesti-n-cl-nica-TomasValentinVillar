import unittest
from unittest.mock import patch
from datetime import datetime
from src.cli import CLI

class TestHistoriaClinica(unittest.TestCase):
    
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

    @patch(
    'builtins.input',
    side_effect=[
                 '1', '46866812','Juan Perez', '11/11/2005',
                 '6', '47668128',
                '0'])
    @patch('builtins.print')
    def test_paciente_no_existe_historia_clinica(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: Paciente con DNI 47668128 no existe')
if __name__ == '__main__':
    unittest.main()