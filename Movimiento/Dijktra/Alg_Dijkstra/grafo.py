import networkx as nx
import math as mt
import matplotlib.pyplot as plt

class graph_Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y


class graph:
    def __init__(self,grid_cells) :
        self.grid_cells = grid_cells
        self.edges = []
        self.nodos = []
        self.adjacencyMatrix = []
        self.grafo = nx.DiGraph()
    
    def define_graph(self): #Toma en cuenta aquellas celdas que marcan en verdadero para la representacion de nodos
        letra = ord('A')
        for i in range(len(self.grid_cells)):
            for j in range(len(self.grid_cells[i])):
                if self.grid_cells[i][j]:
                    self.nodos.append(graph_Node(chr(letra), i, j))
                    letra += 1
    
    def add_edge(self, origen, destino): #Agrega a la lista una tupla (origen, destino,distancia)
        self.edges.append([origen, destino, self.calcular_distancia(origen.x, origen.y, destino.x, destino.y)])
        
    def calcular_distancia(self, x1, y1, x2, y2): #Calculo de distancia euclidiana dependiendo de dos puntos
        distancia = mt.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return round(distancia, 2)
    
    def buscar_posicion(self, nodo_buscado): #Busca la posicion de un nodo segun su id
        for i, nodo in enumerate(self.nodos):
            if nodo.id == nodo_buscado:
                return i
        return -1
    def define_adjacencyMatrix(self): #Definicion de la matriz de adyacencia
        self.adjacencyMatrix = [[float('inf') for _ in range(len(self.nodos))] for _ in range(len(self.nodos))]
        
        for i in range (len(self.edges)):
            pOrigen = self.buscar_posicion(self.edges[i][0].id)
            pDestino = self.buscar_posicion(self.edges[i][1].id)
            self.adjacencyMatrix[pOrigen][pDestino] = self.edges[i][2]
    
    def buscar_posicion_en_grid(self, nodo_id):
        for nodo in self.nodos:
            if nodo.id == nodo_id:
                return (nodo.x, nodo.y)
        return None
    
    def visualizar_grafo(self):
        G = nx.DiGraph() 
        for nodo in self.nodos:
            G.add_node(nodo.id, pos=(nodo.x, nodo.y))
        
        """for origen, destino, peso in self.edges:
            G.add_edge(origen.id, destino.id, weight=peso)"""
        for i in range(len(self.nodos)):
            for j in range(len(self.nodos)):
                if self.adjacencyMatrix[i][j] != float('inf'):
                    G.add_edge(self.nodos[i].id, self.nodos[j].id, weight=self.adjacencyMatrix[i][j])

        pos = nx.get_node_attributes(G, 'pos')
        nx.draw(G, pos, with_labels=True, node_color='teal', node_size=700, font_size=10, font_color='white', arrows=True, arrowstyle='->', arrowsize=15)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='salmon')

        plt.show()
        
    def generar_grafo(self): 
        for nodo in self.nodos:
            self.grafo.add_node(nodo.id, pos=(nodo.x, nodo.y))
        
        """for origen, destino, peso in self.edges:
            self.grafo.add_edge(origen.id, destino.id, weight=peso)"""
        for i in range(len(self.nodos)):
            for j in range(len(self.nodos)):
                if self.adjacencyMatrix[i][j] != float('inf'):
                    self.grafo.add_edge(self.nodos[i].id, self.nodos[j].id, weight=self.adjacencyMatrix[i][j])    
def imprimir_matriz(matriz):
    for fila in matriz:
        print(fila)
        
def imprimir_nodos(lista):
    for nodo in lista:
        print(f"{nodo.id}, ({nodo.x + 1}, {nodo.y + 1})")
        
def imprimir_aristas(lista):
    for arista in lista:
        print(f"({arista[0].id}, {arista[1].id}), PESO: {arista[2]}")

if __name__ == "__main__":
    grid_cells = [
        [False, False, False, False, True, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False],
        [True, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, True, False, False],
        [False, False, False, False, False, False, False, False, False, False],
        [False, False, True, False, False, False, False, False, False, True],
        [False, False, False, False, False, True, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, True]
        ]
    grafop =graph(grid_cells)
    grafop.define_graph()
    grafop.add_edge(grafop.nodos[0], grafop.nodos[3])
    grafop.add_edge(grafop.nodos[0], grafop.nodos[6])
    grafop.add_edge(grafop.nodos[1], grafop.nodos[2])
    grafop.add_edge(grafop.nodos[1], grafop.nodos[6])
    grafop.add_edge(grafop.nodos[2], grafop.nodos[1])
    grafop.add_edge(grafop.nodos[3], grafop.nodos[2])
    grafop.add_edge(grafop.nodos[3], grafop.nodos[5])
    grafop.add_edge(grafop.nodos[3], grafop.nodos[6])
    grafop.add_edge(grafop.nodos[4], grafop.nodos[0])
    grafop.add_edge(grafop.nodos[5], grafop.nodos[2])
    grafop.add_edge(grafop.nodos[5], grafop.nodos[4])
    grafop.add_edge(grafop.nodos[5], grafop.nodos[6])
    grafop.add_edge(grafop.nodos[6], grafop.nodos[5])
    grafop.add_edge(grafop.nodos[6], grafop.nodos[0])
    
    grafop.define_adjacencyMatrix()
    imprimir_matriz(grid_cells)
    imprimir_nodos(grafop.nodos)
    imprimir_aristas(grafop.edges)
    imprimir_matriz(grafop.adjacencyMatrix)
    grafop.generar_grafo()
    grafop.visualizar_grafo()