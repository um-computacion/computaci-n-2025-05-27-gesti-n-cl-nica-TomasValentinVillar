class PacienteNoExisteError(Exception):
    pass

class MedicoNoExisteError(Exception):
    pass

class TurnoDuplicadoError(Exception):
    pass

class PacienteYaExisteError(Exception):
    pass

class PacienteDatosVaciosError(Exception):
    pass

class MedicoYaExisteError(Exception):
    pass

class MedicoDatosVaciosError(Exception):
    pass

class MedicoNoAtiendeEspecialidadError(Exception):
    pass
class MedicoNoTieneEsaEspecialdad(Exception):
    pass

class EspecielidadDuplicadaError(Exception):
    pass

class EspecialidadDiaInvalido(Exception):
    pass

class NoSeIngresaronMedicamentosError(Exception):
    pass

class DNIInvalidoError(Exception):
    pass

class EspecialidadTipoVacioError(Exception):
    pass