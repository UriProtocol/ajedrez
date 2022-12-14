class mov:

    def __init__(self, inicial, final):
        #Inicial y final son cuadrados
        self.inicial = inicial
        self.final = final
    
    def __eq__(self, other):
        return self.inicial == other.inicial and self.final == other.final