class HistoriaClinica:
    def __init__(self, dni):
       
        self.__turnos = []
        self.__recetas = [] 
        self.__dni = dni
    def agregar_turno(self, turno):
        self.__turnos.append(turno)
        return turno
    
    def agregar_receta(self, receta):
        self.__recetas.append(receta)
        return receta
    
    def obtener_turnos(self):
        return self.__turnos
    
    def obtener_recetas(self):
        return self.__recetas
    
    def __str__(self):
        turnos_str = "\n  ".join(str(turno) for turno in self.__turnos)
        recetas_str = "\n  ".join(str(receta) for receta in self.__recetas)
        return f"Historia Clinica:\nPaciente: {self.__dni}\nTurnos:\n  {turnos_str}\nRecetas:\n  {recetas_str}"
