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
        dias_str = ", ".join(self.__dias)
        return f'{self.__tipo} (Días: {dias_str})'
        