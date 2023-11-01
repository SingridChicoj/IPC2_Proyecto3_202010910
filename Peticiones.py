from Mensajes import Mensajes
from Sentimientos import Sentimientos

class Peticiones:
    def __init__(self):
        self.fecha = []
        self.texto = []
        self.positivos = []
        self.negativos = []
    
    def ConsulHas(self, fecha):
        cadena="sdfsdf#sisale#dsfdsf"
        buffer=""
        state=0
        for c in cadena:
            if state==0:
                if c=="#":
                    #aqui empieza un hashtag
                    buffer+=c
                    state=1
                    continue
            if state==1:
                if c!="#":
                    buffer+=c
                    continue
                else:
                    buffer+=c
                    print("Llegamos al final del hashtag:", buffer)
                    state=0
                    continue
        print(buffer)