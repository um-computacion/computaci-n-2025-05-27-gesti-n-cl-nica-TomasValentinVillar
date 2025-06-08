from datetime import datetime

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
class EspecialidadNoExisteError(Exception):
    pass
class MedicoNoAtiendeEspecialidadError(Exception):
    pass
class MedicoNoTieneEsaEspecialdad(Exception):
    pass
class EspecielidadDuplicadaError(Exception):
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


class Especialidad:
    def __init__(self, tipo:str, dias:list[str]):
        self.__tipo = tipo
        self.__dias = dias

    def obtener_especialidad(self) -> str:
        return self.__tipo
    def obtener_dias(self):
        return self.__dias
    def verificar_dia(self,dia):
        dia = dia.lower()
        if dia in self.__dias:
            return True
        else:
            return False
    def __str__(self):
        return f'{self.__tipo}(Dias {self.__dias}'

class Medico:
    def __init__(self, matricula:str, nombre:str, especialidades:list[Especialidad]):
        self.__matricula = matricula
        self.__nombre = nombre
        self.__especialidades = especialidades 

    def agrgar_especialidad(self, especialidad : Especialidad):
        self.__especialidades.append(especialidad)

    def obtener_matricula(self) -> str:
        return self.__matricula
    def obtener_especialdades(self):
        return self.__especialidades
    def obtener_especialidad_para_dia(self, dia:str) -> str:
        for especialidad in self.__especialidades:
            if dia in especialidad.obtener_dias():
                return especialidad.obtener_especialidad()
        return None
    def __str__(self) -> str:
        return f"Medico: Matricula: {self.__matricula} Nombre: {self.__nombre} Especialidades: {self.__especialidades}"


class Turno:
    def __init__(self,paciente:Paciente,medico:Medico,fecha_hora:datetime, especialidad : str):
        self.__paciente = paciente.obtener_dni()
        self.__medico = medico.obtener_matricula()
        self.__fecha_hora = fecha_hora
        self.__especialidad = especialidad.obtener_especialidad()


    def obtener_medico(self):
        return self.__medico
    
    def obtener_fecha_hora(self) -> datetime:
        return self.__fecha_hora

    def __str__(self) -> str:
        return f"Turno: Paciente: {self.__paciente} Medico: {self.__medico} Fecha y hora: {self.__fecha_hora} Especialidad: {self.__especialidad}"

class Receta:
    def __init__(self,paciente:Paciente,medico:Medico,medicamentos:list[str],fecha:datetime): #en cosigna dice dice datetime.now()
        self.__paciente = paciente.obtener_dni()
        self.__medico = medico.obtener_matricula()
        self.__medicamentos = medicamentos
        self.__fecha = fecha

    def obtener_medicamentos(self):
        return self.__medicamentos

    def __str__(self) -> str:
       return f"Receta: Paciente: {self.__paciente} Medico: {self.__medico} Medicamentos:{self.__medicamentos} Fecha: {self.__fecha}"
#revisar historia clinica el tema de que casi no se usa el dni
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
        #self.__especialidades = {} # preguntar si esta bien agregar esto que no estaba en la consigna
        self.__turnos = []

        self.__historias_clinicas = {}
    def agregar_paciente(self, paciente):

        dni = paciente.obtener_dni()
        self.__pacientes[dni] = paciente
        self.__historias_clinicas[dni] = HistoriaClinica(dni)
    
    def agregar_especialidades(self, especialidad): #creo que no se usa quitar 

        tipo = especialidad.obtener_especialidad()
        self.__especialidades[tipo] = especialidad

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
    def agregar_especilidad_medico(self,medico,especialidad):
        
        medico.agrgar_especialidad(especialidad)
        
    def emitir_recetas(self,paciente,medico,medicamentos,fecha_hora:datetime):
        dni = paciente.obtener_dni()
        matricula = medico.obtener_matricula()
        medicamentos_ = medicamentos
        
        receta = Receta(paciente,medico,medicamentos,fecha_hora)
        historia = self.__historias_clinicas[dni]
        historia.agregar_receta(receta)
        return f'Receta emitida: Paciente: {dni} Medico: {matricula} Medicamentos:{medicamentos_} Fecha {fecha_hora}'
    
    def validar_paciente(self,dni,nombre,fecha_nac):
        if dni in self.__pacientes:
            raise PacienteYaExisteError(f"Paciente con DNI {dni} ya existe")
        if not dni or not nombre or not fecha_nac:
            raise PacienteDatosVaciosError("No se pueden ingresar datos vacios")
            
        
    def validar_medico(self,matricula,nombre,especialidades):
        if matricula in self.__medicos:
            raise MedicoYaExisteError(f"Médico con matrícula {matricula} ya existe")
        if not matricula or not nombre or not especialidades:
            raise MedicoDatosVaciosError('No se pueden ingresar datos vacios')

        for esp in especialidades:
            if not esp.obtener_especialidad().strip() or not esp.obtener_dias():
                raise MedicoDatosVaciosError('Cada especialidad debe tener un tipo y al menos un día')
    def validar_especialidad(self,medico,especialidad):
        for esp in medico.obtener_especialdades():
            if esp.obtener_especialidad() == especialidad.obtener_especialidad():
                raise EspecielidadDuplicadaError('No se puede agregar especialidad por que ya existe')



    def obtener_dia_semana_en_espanol(fecha_hora: datetime) -> str:
        dias_semana = {0: "Lunes",1: "Martes",2: "Miércoles",3: "Jueves",4: "Viernes",5: "Sábado",6: "Domingo"}
        return dias_semana[fecha_hora.weekday()]
    def obtener_especialidad_disponible(self,medico : Medico, dia_semana): #si no puede ser entrada matricula y get_medico
        for especialidad in medico.obtener_especialdades():
            if dia_semana.lower().strip() in especialidad.obtener_dias():
                return especialidad.obtener_especialidad()
        return None   
    
    def validar_especialdiad_en_dia(self,medico : Medico,especialidad_solicitada, dia_semana): #si no puede ser entrada matricula y get_medico
        for especialidad in medico.obtener_especialdades:
            if especialidad.obtener_especialidad() == especialidad_solicitada:
                if dia_semana in especialidad.obtener_dias:
                    return True
                
                else:
                    raise MedicoNoAtiendeEspecialidadError(f"El medico no atiende la especialidad {especialidad_solicitada} los dias {dia_semana}")

        raise MedicoNoTieneEsaEspecialdad(f"El medico no tiene la especialidad {especialidad_solicitada}")
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
    def get_especialidad(self,tipo):
        if tipo in self.__especialidades:
            return self.__especialidades[tipo]
        else:
            raise EspecialidadNoExisteError(f"Especialidad de tipo {tipo} no existe")
    
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
                    #estos bucles deberian estar en Clinica
                    print("Ingrese las especialidades (fin para terminar): ")
                    while True:
                        
                        tipo = input('Espacialidad: ')
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
                        especialidades.append(especialidad)
                        #especialidad = self.clinica.get_especialidad(tipo)
                        
                    
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
                    
                    
                    fecha_hora = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M") #fijarse que significa esto o cambiar por algo facil
                    self.clinica.revisar_turno(matricula, fecha_hora)
                    self.clinica.agendar_turno(paciente, medico, fecha_hora)
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
                    self.clinica.agregar_especilidad_medico(medico,especialidad)
                elif opcion == "5":
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
                
                elif opcion == "6":
                    dni = input("DNI del paciente: ")
                    resultado = self.clinica.obtener_historia_clinica(dni)
                    print(resultado)
                
                elif opcion == "7":
                    self.clinica.ver_todos_los_turnos()
                
                elif opcion == "8":
                    self.clinica.ver_todos_los_pacientes()
                
                elif opcion == "9":
                    self.clinica.ver_todos_los_medicos()
                
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
