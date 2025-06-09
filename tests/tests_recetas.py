import unittest
from unittest.mock import patch
from src.cli import CLI

class TestRecetas(unittest.TestCase):
    
    def setUp(self):
        self.__cli__ = CLI()

    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Perez', '11/11/2005', 
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin', 'fin',
                     '5', '46866812', '123', 'Ibuprofeno','fin', 
                     '0'])
    def test_receta_exitoso(self, patch_input):
        self.__cli__.ejecutar()

        historia = self.__cli__.clinica.obtener_historia_clinica('46866812')
        receta = historia.obtener_recetas()[0]
        self.assertIsNotNone(receta)
        self.assertEqual(receta._Receta__medico, '123')
        self.assertEqual(receta._Receta__paciente, '46866812')
        self.assertEqual(receta._Receta__medicamentos, ['Ibuprofeno'])
        
    @patch(
        'builtins.input',
        side_effect=['2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin', 'fin',
                     '5', '46866812', '123', 'Ibuprofeno','fin', 
                     '0'])
    @patch('builtins.print')
    def test_receta_paciente_no_existe(self, mock_print, mock_input):
        self.__cli__.ejecutar()

        mock_print.assert_any_call('Error: Paciente con DNI 46866812 no existe')
    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Perez', '11/11/2005', 
                     '5', '46866812', '123', 'Ibuprofeno','fin', 
                     '0'])
    @patch('builtins.print')
    def test_receta_medico_no_existe(self, mock_print,mock_input):
        self.__cli__.ejecutar()

        mock_print.assert_any_call('Error: Médico con matrícula 123 no existe')
    
   

    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Perez', '11/11/2005', 
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin', 'fin',
                     '5', '46866812', '123', '','fin', 
                     '0'])
    @patch('builtins.print')
    def test_medicina_vacia(self, mock_print, mock_input):
        self.__cli__.ejecutar()

        mock_print.assert_any_call('Error: No se ingresaron medicamentos')
    

if __name__ == '__main__':
    unittest.main()