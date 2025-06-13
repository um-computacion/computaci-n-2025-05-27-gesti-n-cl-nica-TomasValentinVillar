class HistoriaClinica:
    def __init__(self, dni):
       
        self.__turnos__ = []
        self.__recetas__ = [] 
        self.__dni__ = dni
    def agregar_turno(self, turno):
        self.__turnos__.append(turno)
        return turno
    
    def agregar_receta(self, receta):
        self.__recetas__.append(receta)
        return receta
    
    def obtener_turnos(self):
        return self.__turnos__
    
    def obtener_recetas(self):
        return self.__recetas__
    
    def __str__(self):
        turnos_str = "\n  ".join(str(turno) for turno in self.__turnos__)
        recetas_str = "\n  ".join(str(receta) for receta in self.__recetas__)
        return f"Historia Clinica:\nPaciente: {self.__dni__}\nTurnos:\n  {turnos_str}\nRecetas:\n  {recetas_str}"
