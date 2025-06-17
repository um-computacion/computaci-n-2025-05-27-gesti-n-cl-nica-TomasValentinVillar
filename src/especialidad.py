class Especialidad:
    def __init__(self, tipo:str, dias:list[str]):
        self.__tipo__ = tipo
        self.__dias__ = dias

    def obtener_especialidad(self) -> str:
        return self.__tipo__
    def obtener_dias(self):
        return self.__dias__
    def verificar_dia(self,dia):
        dia = dia.lower()
        if dia in self.__dias__:
            return True
        else:
            return False
    def __str__(self):
        dias_str = ", ".join(self.__dias__)
        return f'{self.__tipo__} (Días: {dias_str})'
        