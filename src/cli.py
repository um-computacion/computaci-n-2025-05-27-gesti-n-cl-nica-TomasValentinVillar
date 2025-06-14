from src.clinica import Clinica
from src.paciente import Paciente
from src.medico import Medico
from src.especialidad import Especialidad

from datetime import datetime
from src.excepciones import (PacienteNoExisteError, PacienteDatosVaciosError,PacienteYaExisteError,MedicoDatosVaciosError, MedicoNoAtiendeEspecialidadError,MedicoNoExisteError, 
TurnoDuplicadoError,MedicoNoTieneEsaEspecialdad,EspecielidadDuplicadaError, EspecialidadDiaInvalido, NoSeIngresaronMedicamentosError, MedicoYaExisteError)

class CLI:
    def __init__(self):
        self.clinica = Clinica()
    #se debe salir con 0
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
            #poner .strip() para eliminar espacios al principio y al final
            try:
                if opcion == "1":
                    dni = input("DNI del paciente: ")
                    nombre = input("Nombre del paciente: ")
                    fecha_nac = input("Fecha de nacimiento: ")
                    self.clinica.validar_paciente(dni,nombre,fecha_nac)
                    paciente = Paciente(dni, nombre, fecha_nac)
                    self.clinica.agregar_paciente(paciente)
                    
                
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
                            self.clinica.validar_especialidad(especialidad)
                            self.clinica.validar_dias(especialidad)
                        especialidades.append(especialidad)
                        
                    
                    self.clinica.validar_medico(matricula,nombre,especialidades)
                    
                    medico = Medico(matricula, nombre, especialidades)
                    self.clinica.agregar_medico(medico)
                
                elif opcion == "3":
                    dni = input("DNI del paciente: ")
                    matricula = input("Matrícula del médico: ")
                    fecha_str = input("Fecha y hora (YYYY-MM-DD HH:MM): ")
                    especialidad = input("Especialidad del turno: ")
                    
                    paciente = self.clinica.get_paciente(dni)
                    medico = self.clinica.get_medico(matricula)
                    
                    
                    fecha_hora = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
                    
                    
                    self.clinica.agendar_turno(paciente, medico, fecha_hora,especialidad)
                elif opcion == "4":
                    matricula = input("Matricula del Medico: ")
                    tipo = input("Nombre de Especialidad: ")
                    print(f"Ingrese días de Atención de la especialidad {tipo}(escriba 'fin' para terminar):")
                    dias = []
                    medico = self.clinica.get_medico(matricula)
                    while True:
                        dia = input("Día: ").lower().strip()
                        if dia == 'fin':
                            break
                        dias.append(dia)   
                    especialidad = Especialidad(tipo,dias)

                    self.clinica.validar_especialidad(medico,especialidad)
                    self.clinica.validar_dias(especialidad)
                    self.clinica.agregar_especilidad_medico(medico,especialidad)
                elif opcion == "5":
                    dni = input("DNI del paciente: ")
                    matricula = input("Matrícula del médico: ")
                    
       
                    paciente = self.clinica.get_paciente(dni)
                    medico = self.clinica.get_medico(matricula)
                    
                    medicamentos = []
                    while True:
                        med = input("Medicamento: ")
                        if med.lower() == 'fin':
                            break
                        medicamentos.append(med)
                    
                    
                    if medicamentos:
                        resultado = self.clinica.emitir_recetas(paciente, medico, medicamentos)
                        print(resultado)
                    else:
                        print("No se ingresaron medicamentos")
                
                elif opcion == "6":
                    dni = input("DNI del paciente: ")
                    paciente = self.clinica.get_paciente(dni)
                    resultado = self.clinica.obtener_historia_clinica(dni)
                    print(resultado)
                
                elif opcion == "7":
                    if not self.clinica.obtener_turnos():
                        print("No hay turnos agendados")
                    else:
                        print("\n=== TODOS LOS TURNOS ===")
                    for turno in self.clinica.obtener_turnos():
                        print(turno)
                
                elif opcion == "8":
                    if not self.clinica.obtener_pacientes().values():
                        print("No hay pacientes registrados")
            
                    else:
                        print("\n=== TODOS LOS PACIENTES ===")
                    for paciente in self.clinica.obtener_pacientes().values():
                        print(paciente)
                
                elif opcion == "9":
                    if not self.clinica.obtener_medicos().values():
                        print("No hay medicos registrados")
                    else:
                        print("\n=== TODOS LOS MEDICOS ===")
                    for medico in self.clinica.obtener_medicos().values():
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
            except ValueError as e:
                print(f"Error en formato de fecha: {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")
            

# Para ejecutar el programa
if __name__ == "__main__":
    cli = CLI()
    cli.ejecutar()