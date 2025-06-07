from datetime import datetime

class PacienteNoExisteError(Exception):
    pass

class MedicoNoExisteError(Exception):
    pass

class TurnoDuplicadoError(Exception):
    pass

class Paciente:
    def __init__(self, dni:str, nombre:str, fecha_nacimiento:str):
        self.__dni = dni
        self.__nombre = nombre
        self.__fecha_nacimiento = fecha_nacimiento
    def obtener_dni(self) -> str:
        return self.__dni
    def __str__(self) -> str:
        return f"Paciente: DNI: {self.__dni} Nombre: {self.__nombre} Fechad de Nacimiento: {self.__fecha_nacimiento}"

class Medico:
    def __init__(self, matricula:str, nombre:str, especialidad:str):
        self.__matricula = matricula
        self.__nombre = nombre
        self.__especialidad = especialidad
    def obtener_matricula(self) -> str:
        return self.__matricula
    def __str__(self) -> str:
        return f"Medico: Matricula: {self.__matricula} Nombre: {self.__nombre} Especialidad: {self.__especialidad}"


class Turno:
    def __init__(self,paciente:Paciente,medico:Medico,fecha_hora:datetime):
        self.__paciente = paciente.obtener_dni()
        self.__medico = medico.obtener_matricula()
        self.__fecha_hora = fecha_hora
    
    def obtener_fecha_hora(self) -> datetime:
        return self.__fecha_hora
    def __str__(self) -> str:
        return f"Turno: Paciente: {self.__paciente} Medico: {self.__medico} Fecha y hora: {self.__fecha_hora}"

class Receta:
    def __init__(self,paciente:Paciente,medico:Medico,medicamentos:list[str],fecha:datetime):
        self.__paciente = paciente.obtener_dni()
        self.__medico = medico.obtener_matricula()
        self.__medicamentos = medicamentos
        self.__fecha = fecha

    def obtener_medicamentos(self):
        return self.__medicamentos

    def __str__(self) -> str:
       return f"Receta: Paciente: {self.__paciente} Medico: {self.__medico} Medicamentos:{self.__medicamentos} Fecha: {self.__fecha}"
    
class HistoriaClinica:
    def __init__(self, dni):
       
        self.__turnos = []
        self.__recetas = [] 
        self.__dni = dni
    def agregar_turno(self, turno):
        self.__turnos.append(str(turno))
        return turno
    
    def agregar_receta(self, receta):
        self.__recetas.append(str(receta))
        return receta
    
    def obtener_turnos(self):
        return self.__turnos
    
    def obtener_recetas(self):
        return self.__recetas
    
    def __str__(self):
        return f"Historia Clinica: Paciente: {self.__paciente} Turnos: {self.__turnos} Recetas:{self.__recetas}"

class Clinica:
    def __init__(self):
    
        self.__pacientes = {}
        self.__medicos = {}
        self.__turnos = []

        self.__historias_clinicas = {}
    def agregar_paciente(self, paciente):

        dni = paciente.obtener_dni()
        self.__pacientes[dni] = paciente
        self.__historias_clinicas[dni] = HistoriaClinica(dni)

    def agregar_medico(self, medico):

        matricula = medico.obtener_matricula()
        self.__medicos[matricula] = medico     

    def agendar_turno(self,paciente,medico,fecha_hora:datetime):
        dni = paciente.obtener_dni()
        matricula = medico.obtener_matricula()
        turno = Turno(paciente,medico,fecha_hora)
        self.__turnos.append(turno)
        historia = self.__historias_clinicas[dni]
        historia.agregar_turno(turno)
    def emitir_recetas(self,paciente,medico,medicamentos,fecha_hora:datetime):
        dni = paciente.obtener_dni()
        matricula = medico.obtener_matricula()
        medicamentos_ = medicamentos
        
        receta = Receta(paciente,medico,medicamentos,fecha_hora)
        historia = self.__historias_clinicas[dni]
        historia.agregar_receta(receta)
        return f'Receta emitida: Paciente: {dni} Medico: {matricula} Medicamentos:{medicamentos_} Fecha {fecha_hora}'
    def validar_paciente(self,dni):
        if dni not in self.__pacientes:
            raise PacienteNoExisteError(f"Paciente con DNI {dni} no existe")
    def validar_medico(self,matricula):
        if matricula not in self.__medicos:
            raise MedicoNoExisteError(f"Médico con matrícula {matricula} no existe")
    
    def get_paciente(self,dni):
        if dni in self.__pacientes:
            return self.__pacientes[dni]
        else:
            raise PacienteNoExisteError(f"Paciente con DNI {dni} no existe")
    def get_medico(self, matricula):
        if matricula in self.__medicos:
            return self.__medicos[matricula]
        else:
            raise MedicoNoExisteError(f"Médico con matrícula {matricula} no existe")
    def revisar_turno(self, matricula, fecha_hora):
        for turno in self.__turnos:  
            if matricula == turno.medico and fecha_hora == turno.fecha_hora: 
                raise TurnoDuplicadoError("No se puede agendar un turno con el medico y la fecha_hora por que ya existe")

        

    def obtener_historia_clinica(self,dni): 

        
        historia = self.__historias_clinicas[dni]
        paciente = self.__pacientes[dni]
        turnos = historia.obtener_turnos()
        recetas = historia.obtener_recetas()
        return f"Historia Clinica: DNI: {dni} Turnos: {turnos} Recetas:{recetas}"
# no pueden haber prints aca, tiene que estar en CLI
    def ver_todos_los_turnos(self):
            if not self.__turnos:
                print("No hay turnos agendados")
                return
            
            print("\n=== TODOS LOS TURNOS ===")
            for turno in self.__turnos:
                print(turno)
        
    def ver_todos_los_pacientes(self):
        if not self.__pacientes:
            print("No hay pacientes registrados")
            return
            
        print("\n=== TODOS LOS PACIENTES ===")
        for paciente in self.__pacientes.values():
            print(paciente)
        
    def ver_todos_los_medicos(self):
        if not self.__medicos:
            print("No hay médicos registrados")
            return
        
        print("\n=== TODOS LOS MÉDICOS ===")
        for medico in self.__medicos.values():
            print(medico)

class CLI:
    def __init__(self):
        self.clinica = Clinica()
    
    def mostrar_menu(self):
        print("\nMenu Clinica:")
        print("1. Agregar paciente")
        print("2. Agregar médico")
        print("3. Agendar turno")
        print("4. Emitir receta")
        print("5. Ver historia clínica")
        print("6. Ver todos los turnos")
        print("7. Ver todos los pacientes")
        print("8. Ver todos los médicos")
        print("9. Salir")
    
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
                    paciente = Paciente(dni, nombre, fecha_nac)
                    self.clinica.agregar_paciente(paciente)
                
                elif opcion == "2":
                    matricula = input("Matrícula del médico: ")
                    nombre = input("Nombre del médico: ")
                    especialidad = input("Especialidad: ")
                    medico = Medico(matricula, nombre, especialidad)
                    self.clinica.agregar_medico(medico)
                
                elif opcion == "3":
                    dni = input("DNI del paciente: ")
                    matricula = input("Matrícula del médico: ")
                    fecha_str = input("Fecha y hora (YYYY-MM-DD HH:MM): ")
                    
                    
                    paciente = self.clinica.get_paciente(dni)
                    medico = self.clinica.get_medico(matricula)
                    
                    
                    fecha_hora = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M") #fijarse que significa esto o cambiar por algo facil
                    self.clinica.revisar_turno(matricula, fecha_hora)
                    self.clinica.agendar_turno(paciente, medico, fecha_hora)
                
                elif opcion == "4":
                    dni = input("DNI del paciente: ")
                    matricula = input("Matrícula del médico: ")
                    
                    # Buscar paciente y médico
                    if dni in self.clinica._Clinica__pacientes:
                        paciente = self.clinica._Clinica__pacientes[dni]
                    else:
                        raise PacienteNoExisteError(f"Paciente con DNI {dni} no existe")
                    
                    if matricula in self.clinica._Clinica__medicos:
                        medico = self.clinica._Clinica__medicos[matricula]
                    else:
                        raise MedicoNoExisteError(f"Médico con matrícula {matricula} no existe")
                    
                    print("Ingrese medicamentos (escriba 'fin' para terminar):")
                    medicamentos = []
                    while True:
                        med = input("Medicamento: ")
                        if med.lower() == 'fin':
                            break
                        medicamentos.append(med)
                    fecha_str = input("Fecha y hora (YYYY-MM-DD HH:MM): ")
                    fecha_hora = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
                    
                    if medicamentos:
                        resultado = self.clinica.emitir_recetas(paciente, medico, medicamentos,fecha_hora)
                        print(resultado)
                    else:
                        print("No se ingresaron medicamentos")
                
                elif opcion == "5":
                    dni = input("DNI del paciente: ")
                    resultado = self.clinica.obtener_historia_clinica(dni)
                    print(resultado)
                
                elif opcion == "6":
                    self.clinica.ver_todos_los_turnos()
                
                elif opcion == "7":
                    self.clinica.ver_todos_los_pacientes()
                
                elif opcion == "8":
                    self.clinica.ver_todos_los_medicos()
                
                elif opcion == "9":
                    print("¡Hasta luego!")
                    break
                
                else:
                    print("Opción inválida")
            
            except PacienteNoExisteError as e:
                print(f"Error: {e}")
            except MedicoNoExisteError as e:
                print(f"Error: {e}")
            except TurnoDuplicadoError as e:
                print(f"Error: {e}")
            except ValueError as e:
                print(f"Error en formato de fecha: {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")

# Para ejecutar el programa
if __name__ == "__main__":
    cli = CLI()
    cli.ejecutar()

    

"""   
paciente = Paciente("46320390", "juan", "11/11/2005")
medico = Medico("123","Juan Villar","cirujano")
turno = Turno(paciente, medico, datetime(2025, 6, 15, 14, 30))
receta = Receta(paciente, medico, ["ibuprofeno", "tafirol"],datetime(2025, 6, 15, 14, 30))
paciente1 = Paciente("46866812", "juan perez", "01/01/2008")
turno1 = Turno(paciente1, medico, datetime(2025, 11, 11, 16, 40))
receta1 = Receta(paciente1, medico, ["ibuprofeno", "actron"],datetime(2025, 11, 11, 16, 40))
turno12 = Turno(paciente1, medico, datetime(2025, 6, 15, 14, 30))

clinica = Clinica()

#historia_p = HistoriaClinica("46320390")
#historia_p1 = HistoriaClinica("46866812")



#historia_p.agregar_turno(turno)
#historia_p.agregar_receta(receta)
#historia_p1.agregar_turno(turno1)
#historia_p1.agregar_receta(receta1)
#historia_p1.agregar_turno(turno12)

#clinica.agregar_paciente(paciente)
#clinica.agregar_medico("123")
#clinica.agendar_turno(paciente,medico,datetime(2025, 6, 15, 14, 30))
#clinica.emitir_recetas(paciente,medico,["ibuprofeno", "actron"],datetime(2025, 6, 15, 14, 30))


#print(clinica.emitir_recetas(paciente,medico,["ibuprofeno", "actron"],datetime(2025, 6, 15, 14, 30)))
#print(clinica.obtener_historia_clinica("46320390"))
#print(str(paciente))
#print(str(turno))
#print(str(turno))
#print(str(receta))
#print(str(historia_p))
#print(str(historia_p1))
"""
