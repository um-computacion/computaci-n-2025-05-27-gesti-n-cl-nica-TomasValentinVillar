from datetime import datetime
import unittest
from unittest.mock import patch
from src.excepciones import PacienteYaExisteError
from interfaz.cli import CLI
from src.clinica import Clinica


class TestPacientesYMedicosCLI(unittest.TestCase):

    def setUp(self):
        self.__cli__ = CLI()

    @patch(
        'builtins.input',
        side_effect=['1', '12345678', 'Juan Pérez', '15/03/1990','0']
    )
    def test_registro_exitoso_cli(self, ptach_input):
        self.__cli__.ejecutar()
        
        paciente = self.__cli__.__clinica__.get_paciente('12345678')
        self.assertIsNotNone(paciente)
        self.assertEqual(paciente.__nombre__, 'Juan Pérez')
        self.assertEqual(paciente.obtener_dni(), '12345678')
        self.assertEqual(paciente.__fecha_nacimiento__, '15/03/1990')
    @patch(
        'builtins.input',
        side_effect=['1', '12345678', 'Juan Pérez', '15/03/1990', 
                     '1', '87654321', 'Tomas Villar','11/11/2005', 
                     '1', '13572468', 'pepe', '15/03/1990', '0'])
    def test_registro_exitoso_complejo_cli(self, patch_input):
        
        self.__cli__.ejecutar() 
        
        
        paciente = self.__cli__.__clinica__.get_paciente('12345678')
        self.assertIsNotNone(paciente)
        self.assertEqual(paciente.__nombre__, 'Juan Pérez')
        paciente = self.__cli__.__clinica__.get_paciente('87654321')
        self.assertIsNotNone(paciente)
        self.assertEqual(paciente.__nombre__, 'Tomas Villar')
        paciente = self.__cli__.__clinica__.get_paciente('13572468')
        self.assertIsNotNone(paciente)
        self.assertEqual(paciente.__nombre__, 'pepe')
    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Pérez', '15/03/1990', 
                     '1', '46866812', 'Tomas Villar','11/11/2005', 
                     '0'])
    
    @patch('builtins.print')
    @patch('src.clinica.Clinica.validar_existencia_paciente', side_effect=[PacienteYaExisteError("Paciente con DNI 46866812 ya existe")]) 
    def test_registro_duplicado_cli(self, mock_validar_existencia_paciente, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call("Error: Paciente con DNI 46866812 ya existe")
    
    @patch(
        'builtins.input',
        side_effect=['1', '46866812', '', '','0'])
    @patch('builtins.print')
    def test_registro_vacio_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: No se pueden ingresar datos vacios')
    
    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Perez', '11-11-2005','0'])
    @patch('builtins.print')
    def test_registro_fecha_formato_invalida_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error en formato de fecha: La fecha de nacimiento debe estar en formato dd/mm/aaaa y debe ser valida')

    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Perez', '11/20/2005','0'])
    @patch('builtins.print')
    def test_registro_fecha_invalida_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error en formato de fecha: La fecha de nacimiento debe estar en formato dd/mm/aaaa y debe ser valida')


    @patch(
        'builtins.input',
        side_effect=['1', '468', 'Juan Perez', '11/11/2005','0'])
    @patch('builtins.print')
    def test_registro_dni_invalido_digitos_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: El DNI debe tener exactamente 8 dígitos')

    @patch(
        'builtins.input',
        side_effect=['1', 'aaaaaaaa', 'Juan Perez', '11/11/2005','0'])
    @patch('builtins.print')
    def test_registro_dni_invalido_digitos_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: El DNI solo puede contener números')
    
    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin', 'fin',
                     '0'])
    def test_registro_medico_especialidad_cli(self, patch_input):
        self.__cli__.ejecutar()

        medico = self.__cli__.__clinica__.obtener_medico_por_matricula('123')
        self.assertIsNotNone(medico)
        self.assertEqual(medico.__nombre__, 'Tomas Villar')
        self.assertEqual(medico.__matricula__, '123')
        self.assertEqual(medico.__especialidades__[0].obtener_especialidad(), 'Cirujano')

    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin', 'Cirujano', 'jueves','fin','fin',
                     '0'])
    @patch('builtins.print')

    def test_registro_medico_especialidad_duplicada_cli(self, mock_print,mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: No se puede agregar especialidad por que ya existe')
        
    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin','Pediatra', 'Viernes', 'fin','fin',
                     '2', '456', 'Juan Perez', 'Dermatologo', 'Martes','Jueves','fin','fin',
                     '0'])
    
    def test_registro_medico_especialidad_complejo_cli(self, patch_input):
        self.__cli__.ejecutar()

        medico = self.__cli__.__clinica__.obtener_medico_por_matricula('123')
        self.assertIsNotNone(medico)
        self.assertEqual(medico.__nombre__, 'Tomas Villar')
        self.assertEqual(medico.__especialidades__[0].obtener_especialidad(), 'Cirujano')
        self.assertEqual(medico.__especialidades__[1].obtener_especialidad(), 'Pediatra')
        medico = self.__cli__.__clinica__.obtener_medico_por_matricula('456')
        self.assertIsNotNone(medico)
        self.assertEqual(medico.__nombre__, 'Juan Perez')
        self.assertEqual(medico.__especialidades__[0].obtener_especialidad(), 'Dermatologo')

    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano', 'Lunes', 'fin','fin',
                     '2', '123', 'Juan Perez', 'Dermatologo', 'Miercoles', 'fin', 'fin',
                     '0'])
    @patch('builtins.print')
    def test_registro_medico_especialidad_duplicado_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: Médico con matrícula 123 ya existe')
    @patch(
        'builtins.input',
        side_effect=[
                     '2','' ,'Tomas Villar', 'Cirujano', 'Lunes', 'fin','fin','0'])
    @patch('builtins.print')
    def test_registro_medico_vacio_matricula_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: No se pueden ingresar datos vacios')
    @patch(
        'builtins.input',
        side_effect=[
                     '2','123' ,'Tomas Villar', '', 'Lunes', 'fin','fin','0'])
    @patch('builtins.print')
    def test_registro_medico_vacio_espcialidad_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: Cada especialidad debe tener un tipo y al menos un día')
    @patch(
        'builtins.input',
        side_effect=[
                     '2','123' ,'Tomas Villar', 'Cirujano', 'fin','fin','0'])
    @patch('builtins.print')
    def test_registro_medico_vacio_dias_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: Cada especialidad debe tener un tipo y al menos un día')

class TestRecetasCLI(unittest.TestCase):
    def setUp(self):
        self.__cli__ = CLI()
        self.__clinica = Clinica()
    
   
        
    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Perez', '11/11/2005', 
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin', 'fin',
                     '5', '46866812', '123', 'Ibuprofeno','fin', 
                     '0'])
    def test_receta_exitoso_cli(self, patch_input):
        self.__cli__.ejecutar()

        historia = self.__cli__.__clinica__.obtener_historia_clinica('46866812')
        receta = historia.obtener_recetas()[0]
        self.assertIsNotNone(receta)
        self.assertEqual(receta.__medico__.obtener_matricula(), '123')
        self.assertEqual(receta.__paciente__.obtener_dni(), '46866812')
        self.assertEqual(receta.__medicamentos__, ['Ibuprofeno'])
        
    @patch(
        'builtins.input',
        side_effect=['2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin', 'fin',
                     '5', '46866812', '123', 'Ibuprofeno','fin', 
                     '0'])
    @patch('builtins.print')
    def test_receta_paciente_no_existe__cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()

        mock_print.assert_any_call('Error: Paciente con DNI 46866812 no existe')
    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Perez', '11/11/2005', 
                     '5', '46866812', '123', 'Ibuprofeno','fin', 
                     '0'])
    @patch('builtins.print')
    def test_receta_medico_no_existe_cli(self, mock_print,mock_input):
        self.__cli__.ejecutar()

        mock_print.assert_any_call('Error: Médico con matrícula 123 no existe')
    

    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Perez', '11/11/2005', 
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin', 'fin',
                     '5', '46866812', '123', '','fin', 
                     '0'])
    @patch('builtins.print')
    def test_medicina_vacia_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()

        mock_print.assert_any_call('Error: No se ingresaron medicamentos')    

class TestEspecialidadesCLI(unittest.TestCase):

    def setUp(self):
        self.__cli__ = CLI()
    
    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin', 'fin',
                     '4', '123', 'Pediatra', 'Viernes','fin','0'])
    def test_especialidad_exitoso_cli(self, patch_input):

        self.__cli__.ejecutar()

        medico = self.__cli__.__clinica__.obtener_medico_por_matricula('123')
        self.assertIsNotNone(medico)
        self.assertEqual(medico.__especialidades__[0].obtener_especialidad(), 'Cirujano')
        self.assertEqual(medico.__especialidades__[1].obtener_especialidad(), 'Pediatra')
        self.assertEqual(medico.__especialidades__[0].obtener_dias(), ['lunes','miercoles'])
        self.assertEqual(medico.__especialidades__[1].obtener_dias(), ['viernes'])
    
    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin', 'fin',
                     '4', '123', 'Cirujano', 'Viernes','fin','0'])
    @patch('builtins.print')
    def test_registro_medico_especialidad_duplicado_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: No se puede agregar especialidad por que ya existe')
    
    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin', 'fin',
                     '4', '123', '', 'Viernes','fin','0'])
    @patch('builtins.print')
    def test_registro_medico_especialidad_vacio_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: No se puede ingresar datos vacios')
    
    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano','Lune', 'dia','fin', 'fin',
                     '0'])
    @patch('builtins.print')
    def test_registro_medico_especialidad_invalido_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: Los dias ingresados deben ser válidos')
    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'miercoles','fin', 'fin',
                     '4', '123', 'Pediatra', 'dia','fin','0'])
    @patch('builtins.print')
    def test_registro_especialidad_invalido_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: Los dias ingresados deben ser válidos')
    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'miercoles','fin', 'fin',
                     '4', '456', 'Pediatra', 'dia','fin','0'])
    @patch('builtins.print')
    def test_registro_especialidad_medico_no_existe_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: Médico con matrícula 456 no existe')

class TestHistoriaClinicaCLI(unittest.TestCase):
    
    def setUp(self):
        self.__cli__ = CLI()
    
    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Pérez', '15/03/1990',
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin','fin',
                     '3', '46866812', '123', '2025-06-09 16:30','Cirujano',
                     '5', '46866812', '123', 'Ibuprofeno','fin', '0'])
    def test_historia_clinica_exitosa_cli(self, patch_input):
        self.__cli__.ejecutar()

        historia = self.__cli__.__clinica__.obtener_historia_clinica('46866812')
        receta = historia.obtener_recetas()[0]
        turno = historia.obtener_turnos()[0]
        self.assertIsNotNone(receta)
        self.assertEqual(receta.__medico__.obtener_matricula(), '123')
        self.assertEqual(receta.__paciente__.obtener_dni(), '46866812')
        self.assertEqual(receta.__medicamentos__, ['Ibuprofeno'])
        self.assertIsNotNone(turno)
        self.assertEqual(turno.obtener_medico().obtener_matricula(), '123')
        self.assertEqual(turno.obtener_paciente().obtener_dni(), '46866812')
        self.assertEqual(turno.obtener_fecha_hora(), datetime(2025,6,9,16,30))
        self.assertEqual(turno.obtener_especialidad_turno(), 'Cirujano')

    @patch(
    'builtins.input',
    side_effect=[
                 '1', '46866812','Juan Perez', '11/11/2005',
                 '6', '47668128',
                '0'])
    @patch('builtins.print')
    def test_paciente_no_existe_historia_clinica_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()
        mock_print.assert_any_call('Error: Paciente con DNI 47668128 no existe')

class TestTurnosCLI(unittest.TestCase):

    def setUp(self):
        self.__cli__ = CLI()
    
    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Perez', '11/11/2005', 
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin', 'fin',
                     '3', '46866812', '123', '2025-06-09 16:30','Cirujano',
                     '0'])
    def test_turno_exitoso_cli(self, patch_input):
        self.__cli__.ejecutar()

        turnos = self.__cli__.__clinica__.obtener_turnos()
        self.assertIsNotNone(turnos[0])
        self.assertEqual(turnos[0].obtener_medico().obtener_matricula(), '123')
        self.assertEqual(turnos[0].obtener_paciente().obtener_dni(),'46866812')
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
    def test_duplicado_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()

        mock_print.assert_any_call('Error: No se puede agendar un turno con el medico y la fecha_hora por que ya existe')

    @patch(
        'builtins.input',
        side_effect=[
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin','Pediatra','Lunes','fin', 'fin',
                     '3', '46866812', '123', '2025-06-09 16:30','Cirujano',
                     '0'])
    @patch('builtins.print')
    def test_paciente_no_existe_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()

        mock_print.assert_any_call('Error: Paciente con DNI 46866812 no existe')

    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Perez', '11/11/2005', 
                     '3', '46866812', '123', '2025-06-09 16:30','Cirujano',
                     '0'])
    @patch('builtins.print')
    def test_medico_no_existe_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()

        mock_print.assert_any_call('Error: Médico con matrícula 123 no existe')
    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Perez', '11/11/2005', 
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin', 'fin',
                     
                     '3', '46866812', '123', '2025-06-09 16:30', 'Pediatra',
                     '0'])
    @patch('builtins.print')
    def test_medico_no_anteinde_especialidad_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()

        mock_print.assert_any_call('Error: El medico no tiene la especialidad Pediatra')
    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Perez', '11/11/2005', 
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'fin', 'fin',
                     
                     '3', '46866812', '123', '2025-06-10 16:30', 'Cirujano',
                     '0'])
    @patch('builtins.print')
    def test_medico_no_anteinde_especialidad_dia_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()

        mock_print.assert_any_call('Error: El medico no atiende la especialidad Cirujano los dias martes')

    @patch(
        'builtins.input',
        side_effect=['1', '46866812', 'Juan Perez', '11/11/2005', 
                     '2', '123','Tomas Villar', 'Cirujano','Lunes', 'Miercoles','fin', 'fin',
                     '3', '46866812', '123', '2025/06/09 16:30','Cirujano',
                     '0'])
    @patch('builtins.print')
    def test_tuno_fecha_ivalida_cli(self, mock_print, mock_input):
        self.__cli__.ejecutar()

        mock_print.assert_any_call('Error en formato de fecha: La fecha del turno debe estar en el formato AAAA-MM-DD HH:MM y debe ser valida')

if __name__ == '__main__':
    unittest.main() 