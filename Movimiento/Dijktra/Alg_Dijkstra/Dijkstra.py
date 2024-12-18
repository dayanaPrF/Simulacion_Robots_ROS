import networkx as nx
import matplotlib.pyplot as plt
import sys
import math
from grafo import graph
from grafo import graph_Node

class Dijkstra:
    def __init__(self, nodo_raiz, grafo):
        self.vertices = list(grafo.nodes())
        self.conocido = [False] * len(self.vertices)
        self.distancia = [sys.maxsize] * len(self.vertices)
        self.padre = [''] * len(self.vertices)
        self.nodo_raiz = nodo_raiz
        self.arbolRes = [[False] * len(self.vertices) for _ in range(len(self.vertices))]
        self.matriz_adyacencia = [[sys.maxsize] * len(self.vertices) for _ in range(len(self.vertices))]
        self.llenar_matriz_adyacencia(grafo)
    
    def llenar_matriz_adyacencia(self, grafo):
        for u, v, data in grafo.edges(data=True):
            peso = data.get('weight', sys.maxsize) 
            self.matriz_adyacencia[self.indiceNodo(u)][self.indiceNodo(v)] = peso
        for i in range(len(self.vertices)):
            for j in range(len(self.vertices)):
                if i == j or self.matriz_adyacencia[i][j] == sys.maxsize:
                    self.matriz_adyacencia[i][j] = sys.maxsize

    
    def indiceNodo(self, caracter):
        try:
            return self.vertices.index(caracter)
        except ValueError:
            return None  
    
    def todos_verdaderos(self,lista):
        return all(lista)

        
    def menor_posicion(self, lista):
        min_valor = sys.maxsize
        min_pos = -1
        for i in range(len(lista)):
            if not self.conocido[i] and lista[i] < min_valor:
                min_valor = lista[i]
                min_pos = i
        return min_pos

    
    def obtenerDescendientes(self, index_nodo):
        index_descendientes = []
        for i in range (len(self.vertices)):
            if (self.matriz_adyacencia[index_nodo][i] != sys.maxsize):
                index_descendientes.append(i)
        return index_descendientes
    
    def obtenerDistancia(self, index_padre, peso):
        if (self.distancia[index_padre] == sys.maxsize):
            return peso
        else:
            return self.distancia[index_padre] + peso
    
    def algoritmo(self):
        index_descendientes = []
        nodo_referencia = self.nodo_raiz
        self.conocido[self.indiceNodo(self.nodo_raiz)] = True
        self.distancia[self.indiceNodo(self.nodo_raiz)] = sys.maxsize #marcamos los indices del nodo raiz
        while (not self.todos_verdaderos(self.conocido)):
            print(nodo_referencia)
            index_descendientes = self.obtenerDescendientes(self.indiceNodo(nodo_referencia)) #obtenemos los decendientes para analizarlos
            for index in index_descendientes: #Colocamos valores correspondientes a adyacentes
                distancia = self.obtenerDistancia(self.indiceNodo(nodo_referencia), self.matriz_adyacencia[self.indiceNodo(nodo_referencia)][index])
                if (distancia <= self.distancia[index]): #Relajacion de arista
                    if (index == self.indiceNodo(self.nodo_raiz)):
                        self.padre[index] = ''
                        self.distancia[index] = 0
                    else:
                        self.padre[index] = nodo_referencia
                        self.distancia[index] = distancia
            menor = self.menor_posicion(self.distancia) #Obtenemos valor menor
            nodo_referencia = self.vertices[menor]
            self.conocido[menor] = True #Marcamos como conocido
        print(nodo_referencia)
        print(f"<<<<<<{self.padre}")
        print(f"<<<<<<{self.distancia}")
        
        for i in range(len(self.vertices)):
            for j in range(len(self.vertices)):
                if (self.padre[j] == self.vertices[i]):
                    self.arbolRes[i][j] = True
                else:
                    self.arbolRes[i][j] = False
    
    def grafos(self):
        Grafo = nx.DiGraph()
        Grafo.add_nodes_from(['A','B','C','D','E','F','G'])
        for i in range(len(self.vertices)):
            for j in range(len(self.vertices)):
                if self.arbolRes[i][j]:
                    Grafo.add_edge(self.vertices[i],self.vertices[j])
        return Grafo


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
    grafop.generar_grafo()

    a = Dijkstra('B',grafop.grafo)
    a.algoritmo()
    num_nodos = len(a.vertices)
    grafo = nx.DiGraph()
    grafo = a.grafos()
    pos = nx.spring_layout(grafo)
    nx.draw(grafo, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1000, font_size=15)
    plt.title("Grafo dirigido desde matriz de adyacencia")
    plt.show()
