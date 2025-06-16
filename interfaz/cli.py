from src.clinica import Clinica
from src.paciente import Paciente
from src.medico import Medico
from src.especialidad import Especialidad

from datetime import datetime
from src.excepciones import (PacienteNoExisteError, PacienteDatosVaciosError,PacienteYaExisteError,MedicoDatosVaciosError, MedicoNoAtiendeEspecialidadError,MedicoNoExisteError, 
TurnoDuplicadoError,MedicoNoTieneEsaEspecialdad,EspecielidadDuplicadaError, EspecialidadDiaInvalido, NoSeIngresaronMedicamentosError, MedicoYaExisteError,DNIInvalidoError,EspecialidadTipoVacio)

class CLI:
    def __init__(self):
        self.__clinica__ = Clinica()
    def mostrar_menu(self):
        print("\nMenu Clinica:")
        print("1. Agregar paciente")
        print("2. Agregar médico")
        print("3. Agendar turno")
        print("4. Agrgar Especialidad")
        print("5. Emitir receta")
        print("6. Ver historia clínica")
        print("7. Ver todos los turnos")
        print("8. Ver todos los pacientes")
        print("9. Ver todos los médicos")
        print("0. Salir")
    
    def ejecutar(self):
        print("=== SISTEMA DE CLÍNICA ===")
        
        while True:
            self.mostrar_menu()
            opcion = input("\nSeleccione una opción: ")
            try:
                if opcion == "1":
                    dni = input("DNI del paciente: ")
                    nombre = input("Nombre del paciente: ")
                    fecha_nac = input("Fecha de nacimiento: ")
                    self.__clinica__.validar_dni(dni)
                    self.__clinica__.validar_existencia_paciente(dni,nombre,fecha_nac)
                    self.__clinica__.validar_fecha_nacimiento(fecha_nac)
                    paciente = Paciente(dni, nombre, fecha_nac)
                    self.__clinica__.agregar_paciente(paciente)
                    
                
                elif opcion == "2":
                    matricula = input("Matrícula del médico: ")
                    nombre = input("Nombre del médico: ")
                    especialidades = []
                    
                    print("Ingrese las especialidades (fin para terminar): ")
                    while True:
                        
                        tipo = input('Especialidad: ')
                        if tipo == 'fin':
                            break
                        else:
                            print(f"Ingrese días de Atención de la especialidad {tipo}(escriba 'fin' para terminar):")
                            dias = []
                            while True:
                                dia = input("Día: ").lower().strip()
                                if dia == 'fin':
                                    break
                                dias.append(dia)
                            
                            especialidad = Especialidad(tipo,dias)
                            
                            self.__clinica__.validar_dias(especialidad)
                            self.__clinica__.validar_especialidad_no_duplicada(especialidades,especialidad)
                        especialidades.append(especialidad)
                        
                    
                    self.__clinica__.validar_existencia_medico(matricula,nombre,especialidades)
                    
                    medico = Medico(matricula, nombre, especialidades)
                    self.__clinica__.agregar_medico(medico)
                
                elif opcion == "3":
                    dni = input("DNI del paciente: ")
                    matricula = input("Matrícula del médico: ")
                    fecha_str = input("Fecha y hora (AAAA-MM-DD HH:MM): ")
                    especialidad = input("Especialidad del turno: ")
                    
                    paciente = self.__clinica__.get_paciente(dni)
                    medico = self.__clinica__.obtener_medico_por_matricula(matricula)

                    self.__clinica__.validar_fecha_turno(fecha_str)
                    
                    fecha_hora = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
                    
                    
                    self.__clinica__.agendar_turno(paciente, medico, fecha_hora,especialidad)
                elif opcion == "4":
                    matricula = input("Matricula del Medico: ")
                    tipo = input("Nombre de Especialidad: ")
                    print(f"Ingrese días de Atención de la especialidad {tipo}(escriba 'fin' para terminar):")
                    dias = []
                    medico = self.__clinica__.obtener_medico_por_matricula(matricula)
                    while True:
                        dia = input("Día: ").lower().strip()
                        if dia == 'fin':
                            break
                        dias.append(dia)   
                    especialidad = Especialidad(tipo,dias)

                    self.__clinica__.validar_especialidad(medico,especialidad)
                    self.__clinica__.validar_dias(especialidad)
                    self.__clinica__.agregar_especilidad_medico(medico,especialidad)
                elif opcion == "5":
                    dni = input("DNI del paciente: ")
                    matricula = input("Matrícula del médico: ")
                    
       
                    paciente = self.__clinica__.get_paciente(dni)
                    medico = self.__clinica__.obtener_medico_por_matricula(matricula)
                    
                    medicamentos = []

                    print(f"Ingrese los Medicamentos de la receta (escriba 'fin' para terminar):")
                    while True:
                        med = input("Medicamento: ")
                        if med.lower() == 'fin':
                            break
                        medicamentos.append(med)
                    
                    
                    if medicamentos:
                        resultado = self.__clinica__.emitir_recetas(paciente, medico, medicamentos)
                        print(resultado)
                    else:
                        print("No se ingresaron medicamentos")
                
                elif opcion == "6":
                    dni = input("DNI del paciente: ")
                    paciente = self.__clinica__.get_paciente(dni)
                    resultado = self.__clinica__.obtener_historia_clinica(dni)
                    print(resultado)
                
                elif opcion == "7":
                    if not self.__clinica__.obtener_turnos():
                        print("No hay turnos agendados")
                    else:
                        print("\n=== TODOS LOS TURNOS ===")
                    for turno in self.__clinica__.obtener_turnos():
                        print(turno)
                
                elif opcion == "8":
                    if not self.__clinica__.obtener_pacientes().values():
                        print("No hay pacientes registrados")
            
                    else:
                        print("\n=== TODOS LOS PACIENTES ===")
                    for paciente in self.__clinica__.obtener_pacientes().values():
                        print(paciente)
                
                elif opcion == "9":
                    if not self.__clinica__.obtener_medicos().values():
                        print("No hay medicos registrados")
                    else:
                        print("\n=== TODOS LOS MEDICOS ===")
                    for medico in self.__clinica__.obtener_medicos().values():
                        print(medico)
                
                elif opcion == "0":
                    print("¡Hasta luego!")
                    break
                
                else:
                    print("Opción inválida")
            
            except PacienteNoExisteError as e:
                print(f"Error: {e}")
            except PacienteYaExisteError as e:
                print(f"Error: {e}")
            except MedicoNoExisteError as e:
                print(f"Error: {e}")
            except MedicoYaExisteError as e:
                print(f'Error: {e}')
            except MedicoDatosVaciosError as e:
                print(f'Error: {e}')
            except TurnoDuplicadoError as e:
                print(f"Error: {e}")
            except PacienteDatosVaciosError as e:
                print(f'Error: {e}')
            except EspecielidadDuplicadaError as e:
                print(f'Error: {e}')    
            except EspecialidadDiaInvalido as e:
                print(f'Error: {e}')
            except MedicoNoAtiendeEspecialidadError as e:
                print(f'Error: {e}')
            except MedicoNoTieneEsaEspecialdad as e:
                print(f'Error: {e}')
            except NoSeIngresaronMedicamentosError as e:
                print(f'Error: {e}')
            except DNIInvalidoError as e:
                print(f'Error: {e}')
            except EspecialidadTipoVacio as e:
                print(f'Error: {e}')
            except ValueError as e:
                print(f"Error en formato de fecha: {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")
            

# Para ejecutar el programa
if __name__ == "__main__":
    cli = CLI()
    cli.ejecutar()