import unittest
from main import Paciente, Medico, Turno, Receta, HistoriaClinica, Clinica, CLI, PacienteYaExisteError
from unittest.mock import patch

class TestPacientesYMedicos(unittest.TestCase):

    def setUp(self):
        self.__cli__ = CLI()

    @patch(
        'builtins.input',
        side_effect=['1', '12345678', 'Juan Pérez', '15/03/1990','0']
    )
    def test_registro_exitoso(self, patch_input):
        self.__cli__.ejecutar()  # o tu método principal
        
        paciente = self.__cli__.clinica.get_paciente('12345678')
        self.assertIsNotNone(paciente)
        self.assertEqual(paciente._Paciente__nombre, 'Juan Pérez')
        self.assertEqual(paciente._Paciente__dni, '12345678')
        self.assertEqual(paciente._Paciente__fecha_nacimiento, '15/03/1990')
    @patch(
        'builtins.input',
        side_effect=['1', '12345678', 'Juan Pérez', '15/03/1990', 
                     '1', '87654321', 'Tomas Villar','11/11/2005', 
                     '1', '13572468', 'pepe', '15/03/1990', '0'])
    def test_registro_exitoso_complejo(self, patch_input):
        # Ejecutar el método que maneja el registro
        self.__cli__.ejecutar()  # o tu método principal
        
        # Verificar que el paciente se registró
        paciente = self.__cli__.clinica.get_paciente('12345678')
        self.assertIsNotNone(paciente)
        self.assertEqual(paciente._Paciente__nombre, 'Juan Pérez')
        paciente = self.__cli__.clinica.get_paciente('87654321')
        self.assertIsNotNone(paciente)
        self.assertEqual(paciente._Paciente__nombre, 'Tomas Villar')
        paciente = self.__cli__.clinica.get_paciente('13572468')
        self.assertIsNotNone(paciente)
        self.assertEqual(paciente._Paciente__nombre, 'pepe')
    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Pérez', '15/03/1990', 
                     '1', '46866812', 'Tomas Villar','11/11/2005', 
                     '0'])
    @patch('builtins.print')
    def test_registro_duplicado(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call("Error: Paciente con DNI 46866812 ya existe")
    
    @patch(
        'builtins.input',
        side_effect=['1', '', '', '','0'])
    @patch('builtins.print')
    def test_registro_vacio(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: No se pueden ingresar datos vacios')
    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin', 'fin',
                     '0'])
    def test_registro_medico_especialidad(self, patch_input):
        self.__cli__.ejecutar()

        medico = self.__cli__.clinica.get_medico('123')
        self.assertIsNotNone(medico)
        self.assertEqual(medico._Medico__nombre, 'Tomas Villar')
        self.assertEqual(medico._Medico__matricula, '123')
        self.assertEqual(medico._Medico__especialidades[0].obtener_especialidad(), 'Cirujano')
    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin','Pediatra', 'Viernes', 'fin','fin',
                     '2', '456', 'Juan Perez', 'Dermatologo', 'Martes','Jueves','fin','fin',
                     '0'])
    
    def test_registro_medico_especialidad_complejo(self, patch_input):
        self.__cli__.ejecutar()

        medico = self.__cli__.clinica.get_medico('123')
        self.assertIsNotNone(medico)
        self.assertEqual(medico._Medico__nombre, 'Tomas Villar')
        self.assertEqual(medico._Medico__especialidades[0].obtener_especialidad(), 'Cirujano')
        self.assertEqual(medico._Medico__especialidades[1].obtener_especialidad(), 'Pediatra')
        medico = self.__cli__.clinica.get_medico('456')
        self.assertIsNotNone(medico)
        self.assertEqual(medico._Medico__nombre, 'Juan Perez')
        self.assertEqual(medico._Medico__especialidades[0].obtener_especialidad(), 'Dermatologo')

    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano', 'Lunes', 'fin','fin',
                     '2', '123', 'Juan Perez', 'Dermatologo', 'Miercoles', 'fin', 'fin',
                     '0'])
    @patch('builtins.print')
    def test_registro_medico_especialidad_duplicado(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: Médico con matrícula 123 ya existe')
    @patch(
        'builtins.input',
        side_effect=[
                     '2','' ,'Tomas Villar', 'Cirujano', 'Lunes', 'fin','fin','0'])
    @patch('builtins.print')
    def test_registro_medico_vacio_matricula(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: No se pueden ingresar datos vacios')
    @patch(
        'builtins.input',
        side_effect=[
                     '2','123' ,'Tomas Villar', '', 'Lunes', 'fin','fin','0'])
    @patch('builtins.print')
    def test_registro_medico_vacio_espcialidad(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: Cada especialidad debe tener un tipo y al menos un día')
    @patch(
        'builtins.input',
        side_effect=[
                     '2','123' ,'Tomas Villar', 'Cirujano', 'fin','fin','0'])
    @patch('builtins.print')
    def test_registro_medico_vacio_dias(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: Cada especialidad debe tener un tipo y al menos un día')

        

        
if __name__ == '__main__':
    unittest.main() 