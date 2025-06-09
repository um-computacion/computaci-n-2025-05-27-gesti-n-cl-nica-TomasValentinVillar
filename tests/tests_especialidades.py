import unittest
from unittest.mock import patch
from src.cli import CLI

class TestEspecialidades(unittest.TestCase):

    def setUp(self):
        self.__cli__ = CLI()
    
    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin', 'fin',
                     '4', '123', 'Pediatra', 'Viernes','fin','0'])
    def test_especialidad_exitoso(self, patch_input):
        self.__cli__.ejecutar()

        medico = self.__cli__.clinica.get_medico('123')
        self.assertIsNotNone(medico)
        self.assertEqual(medico._Medico__especialidades[0].obtener_especialidad(), 'Cirujano')
        self.assertEqual(medico._Medico__especialidades[1].obtener_especialidad(), 'Pediatra')
        self.assertEqual(medico._Medico__especialidades[0].obtener_dias(), ['lunes','miercoles'])
        self.assertEqual(medico._Medico__especialidades[1].obtener_dias(), ['viernes'])
    
    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin', 'fin',
                     '4', '123', 'Cirujano', 'Viernes','fin','0'])
    @patch('builtins.print')
    def test_registro_medico_especialidad_duplicado(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: No se puede agregar especialidad por que ya existe')
    
    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano','Lune', 'dia','fin', 'fin',
                     '0'])
    @patch('builtins.print')
    def test_registro_medico_especialidad_invalido(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: Los dias ingresados deben ser válidos')
    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'miercoles','fin', 'fin',
                     '4', '123', 'Pediatra', 'dia','fin','0'])
    @patch('builtins.print')
    def test_registro_especialidad_invalido(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: Los dias ingresados deben ser válidos')
    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'miercoles','fin', 'fin',
                     '4', '456', 'Pediatra', 'dia','fin','0'])
    @patch('builtins.print')
    def test_registro_especialidad_medico_no_existe(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: Médico con matrícula 456 no existe')
if __name__ == '__main__':
    unittest.main() 