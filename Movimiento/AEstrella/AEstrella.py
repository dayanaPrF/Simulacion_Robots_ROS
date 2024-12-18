from area import Area
from area import Celda
class Nodo: #Clase para agregar caracteristicas de celdas para la ejecucion del algoritmo A*
    def __init__(self, distancia, heuristica, puntaje, padre, celda):
        self.distancia = distancia
        self.heuristica = heuristica
        self.puntaje = puntaje
        self.padre = padre
        self.celda = celda



"""---------ALGORITMO A*--------------------"""
class  AEstrella:
    def __init__(self, area):
        self.area = area    #Cuadricula de trabajo
        self.inicio = area.inicio #Ubicacion del inicio (posicion inicial de robot)
        self.fin = area.fin #Ubicacion del fin (posicion final de robot)
        self.openList = []
        self.closeList = []
        self.caminoFinal = []
    
    def isEmptyList(self, lista):
        return not lista
    
    def isCeldaInList(self, lista, objeto):
        return any(o.celda == objeto for o in lista)
        
    def distancia_manhattan(self, celda, x, y): #Para calcular distancia y heuristica
        return abs(celda.x+1 - x) + abs(celda.y+1 - y)
    
    def agregarLista(self, celdas_colindantes, celda_actual):
        #Revisa las celdas colindantes de la celda actual cumpliendo las siguientes condiciones
        # * La celda no sea un obstaculo
        # * La celda no se encuentre en la lista cerrada (aun no sea considerada)
        # * La celda no este en la lista abierta (ya sea colindante de otra celda)
        for c in celdas_colindantes:
            if c != None:
                if c.estado and not self.isCeldaInList(self.openList, c) and not self.isCeldaInList(self.closeList, c):
                    distancia = self.distancia_manhattan(c,(self.inicio[0]+1),(self.inicio[1]+1))
                    heuristica = self.distancia_manhattan(c,(self.fin[0]+1),(self.fin[1]+1))
                    self.openList.append(Nodo(distancia, heuristica, (distancia+heuristica), celda_actual, c))
                    print(f"Nodo añadido: ({c.x+1} , {c.y+1}), Padre: ({celda_actual.x+1} , {celda_actual.y+1}) ,Distancia: {distancia}, Heuristica: {heuristica}, Puntaje: {distancia+heuristica}")
    
    def obtenerMenorPuntaje(self):
        return min(self.openList, key=lambda nodo: nodo.puntaje)
    
    def eliminarNodo(self, nodo):
        self.openList.remove(nodo)

    def iteraciones(self, celda_actual):
        #A partir de la celda actual, se añaden los colindantes en contra de las manecillas del reloj y 
        #se obtiene el nodo menor
        celdas_colindantes = [celda_actual.norte, celda_actual.noroeste, celda_actual.oeste, celda_actual.suroeste,
                              celda_actual.sur, celda_actual.sureste, celda_actual.este, celda_actual.noreste]
        self.agregarLista(celdas_colindantes,celda_actual)
        menor_nodo = self.obtenerMenorPuntaje()
        return menor_nodo
        
    def algoritmo(self):
        #Ejecucion del algoritmo
        celda_actual = self.area.tabla[self.inicio[0]][self.inicio[1]]
        menor_nodo = self.iteraciones(celda_actual)
        self.closeList.append(menor_nodo)
        celda_actual = menor_nodo.celda
        self.eliminarNodo(menor_nodo)
        while(not self.isEmptyList(self.openList) and self.area.tabla[self.fin[0]][self.fin[1]] != celda_actual):
            menor_nodo = self.iteraciones(celda_actual)
            self.closeList.append(menor_nodo)
            celda_actual = menor_nodo.celda
            self.eliminarNodo(menor_nodo)
        self.obtenerRuta(menor_nodo)
        print("\n\nCONTENIDO DE LISTA CERRADA")
        for n in self.closeList:
            print(f"({n.celda.x+1} , {n.celda.y+1})")

    def buscarNodoPorCelda(self, celda):
        return next((nodo for nodo in self.closeList if nodo.celda == celda), None)
    
    def obtenerRuta(self, nodo):
        aux = nodo
        while aux.padre != self.area.tabla[self.inicio[0]][self.inicio[1]]:
            self.caminoFinal.append(aux.celda)
            aux = self.buscarNodoPorCelda(aux.padre)
        self.caminoFinal.append(aux.celda)  # Añadir la celda de inicio
        self.caminoFinal.append(self.area.tabla[self.inicio[0]][self.inicio[1]])
        self.caminoFinal.reverse()  # Invertir la lista para que el camino esté en el orden correcto

if __name__ == "__main__":

    celdas_ejemplo = [
        [(False, False, False), (False, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (False, False, False), (True, False, False)],
        [(False, False, False), (False, False, False), (True, False, False), (True, False, False), (True, False, True), (True, False, False), (True, False, False), (True, False, False), (False, False, False), (True, False, False)],
        [(True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False)],
        [(False, False, False), (True, False, False), (True, False, False), (False, False, False), (False, False, False), (False, False, False), (False, False, False), (False, False, False), (False, False, False), (True, False, False)],
        [(True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (False, False, False), (True, False, False), (False, False, False), (True, False, False), (True, False, False)],
        [(True, False, False), (True, False, False), (True, False, False), (True, False, False), (True,True, False), (True, False, False), (True, False, False), (False, False, False), (True, False, False), (True, False, False)],
        [(True, False, False), (True, False, False), (False, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (False, False, False), (True, False, False), (True, False, False)],
        [(True, False, False), (False, False, False), (False, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False)],
        [(True, False, False), (True, False, False), (False, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (False, False, False), (False, False, False), (False, False, False)],
        [(True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False), (True, False, False)]
    ]


    area = Area(celdas_ejemplo)
    a = AEstrella(area)
    a.algoritmo()
    print("\n\nRUTA")
    for n in a.caminoFinal:
        print(f"({n.x+1} , {n.y+1})")
    print ((1 - 10 / 2) * 0.4)
    print ((4 - 10 / 2) * 0.4)
