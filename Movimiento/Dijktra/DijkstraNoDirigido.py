import networkx as nx
import matplotlib.pyplot as plt
import sys

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
            self.matriz_adyacencia[self.indiceNodo(v)][self.indiceNodo(u)] = peso 
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
        Grafo = nx.Graph()
        Grafo.add_nodes_from(['A','B','C','D','E','F','G'])
        for i in range(len(self.vertices)):
            for j in range(len(self.vertices)):
                if self.arbolRes[i][j]:
                    Grafo.add_edge(self.vertices[i],self.vertices[j])
        return Grafo


if __name__ == "__main__":
    g = nx.Graph() 
    g.add_nodes_from(['A','B','C','D','E','F','G'])
    g.add_edge('A', 'C', weight=6)
    g.add_edge('A', 'D', weight=4)
    g.add_edge('B', 'A', weight=9)
    g.add_edge('C', 'D', weight=9)
    g.add_edge('D', 'B', weight=5)
    g.add_edge('D', 'E', weight=6)
    g.add_edge('D', 'F', weight=5)
    g.add_edge('D', 'G', weight=7)
    g.add_edge('E', 'B', weight=6)
    g.add_edge('E', 'G', weight=1)
    g.add_edge('F', 'C', weight=1)
    g.add_edge('G', 'F', weight=9)
    """pos = nx.spring_layout(g)  # Posiciones de nodos
    edges = g.edges(data=True) # Lista de aristas
    nx.draw(g, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1000, font_size=15)# Dibuja nodos y aristas
    edge_labels = {(u, v): d['weight'] for u, v, d in edges} # Dibujar los pesos de las aristas
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
    plt.title("Grafo dirigido con pesos en las aristas", fontsize=20)"""
    a = Dijkstra('A',g)
    a.algoritmo()
    num_nodos = len(a.vertices)
    grafo = nx.Graph()
    grafo = a.grafos()
    pos = nx.spring_layout(grafo)
    nx.draw(grafo, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1000, font_size=15)
    plt.title("Grafo dirigido desde matriz de adyacencia")
    plt.show()
