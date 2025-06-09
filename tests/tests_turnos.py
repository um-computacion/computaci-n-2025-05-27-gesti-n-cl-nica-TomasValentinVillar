import unittest
from unittest.mock import patch
from src.cli import CLI
from datetime import datetime

class TestTurnos(unittest.TestCase):

    def setUp(self):
        self.__cli__ = CLI()
    
    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Perez', '11/11/2005', 
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin', 'fin',
                     '3', '46866812', '123', '2025-06-09 16:30','Cirujano',
                     '0'])
    def test_turno_exitoso(self, patch_input):
        self.__cli__.ejecutar()

        turnos = self.__cli__.clinica.obtener_turnos()
        self.assertIsNotNone(turnos[0])
        self.assertEqual(turnos[0].obtener_medico(), '123')
        self.assertEqual(turnos[0]._Turno__paciente, '46866812') #como turno no tiene un metodo para obtenr paciente lo llamo de esa manera
        self.assertEqual(turnos[0].obtener_fecha_hora(), datetime(2025,6,9,16,30))
        self.assertEqual(turnos[0].obtener_especialidad_turno(), 'Cirujano')
    
    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Perez', '11/11/2005', 
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin','Pediatra','Lunes','fin', 'fin',
                     '3', '46866812', '123', '2025-06-09 16:30','Cirujano',
                     '3', '46866812', '123', '2025-06-09 16:30', 'Pediatra',
                     '0'])
    @patch('builtins.print')
    def test_duplicado(self, mock_print, mock_input):
        self.__cli__.ejecutar()

        mock_print.assert_any_call('Error: No se puede agendar un turno con el medico y la fecha_hora por que ya existe')

    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin','Pediatra','Lunes','fin', 'fin',
                     '3', '46866812', '123', '2025-06-09 16:30','Cirujano',
                     '0'])
    @patch('builtins.print')
    def test_paciente_no_existe(self, mock_print, mock_input):
        self.__cli__.ejecutar()

        mock_print.assert_any_call('Error: Paciente con DNI 46866812 no existe')

    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Perez', '11/11/2005', 
                     '3', '46866812', '123', '2025-06-09 16:30','Cirujano',
                     '0'])
    @patch('builtins.print')
    def test_medico_no_existe(self, mock_print, mock_input):
        self.__cli__.ejecutar()

        mock_print.assert_any_call('Error: Médico con matrícula 123 no existe')
    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Perez', '11/11/2005', 
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin', 'fin',
                     
                     '3', '46866812', '123', '2025-06-09 16:30', 'Pediatra',
                     '0'])
    @patch('builtins.print')
    def test_medico_no_anteinde_especialidad(self, mock_print, mock_input):
        self.__cli__.ejecutar()

        mock_print.assert_any_call('Error: El medico no tiene la especialidad Pediatra')
    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Perez', '11/11/2005', 
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'fin', 'fin',
                     
                     '3', '46866812', '123', '2025-06-10 16:30', 'Cirujano',
                     '0'])
    @patch('builtins.print')
    def test_medico_no_anteinde_especialidad(self, mock_print, mock_input):
        self.__cli__.ejecutar()

        mock_print.assert_any_call('Error: El medico no atiende la especialidad Cirujano los dias martes')
if __name__ == '__main__':
    unittest.main()