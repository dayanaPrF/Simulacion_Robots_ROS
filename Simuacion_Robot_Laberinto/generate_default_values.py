import os
import networkx as nx
import math as mt
import matplotlib.pyplot as plt

class SpawnOrigin:
    def __init__(self, archivo_original, celdas, grafo, nodo_inicio):
        self.archivo_original = archivo_original
        self.x, self.y = grafo.buscar_posicion_en_grid(nodo_inicio)

    def guardarValores(self):
        num_rows = len(celdas)
        num_cols = len(celdas[0])
        proceso1 = proceso2 = proceso3 = proceso4 = proceso5 = proceso6 = proceso7 = False
        cx = (self.x - num_rows / 2) * 0.4
        cy = (self.y - num_cols / 2) * 0.4 
        with open(self.archivo_original, 'r') as archivo:
            lineas = archivo.readlines()

        for i, linea in enumerate(lineas):
            if 'spawn = Node(' in linea:
                proceso1 = True
            elif proceso1 and 'package=\'gazebo_ros\',' in linea:
                proceso2 = True
            elif proceso2 and 'executable=\'spawn_entity.py\',' in linea:
                proceso3 = True
            elif proceso3 and 'arguments=["-topic", "/robot_description", ' in linea:
                proceso4 = True
            elif proceso4 and '"-entity", robot_name_in_model,' in linea:
                proceso5 = True
            elif proceso5 and '"-x", ' in linea:
                lineas[i] = f'                    "-x", \'{cx}\',\n'
                proceso6 = True
            elif proceso6 and '"-y", ' in linea:
                lineas[i] = f'                    "-y", \'{cy}\',\n'
                proceso7 = True
            elif proceso7 and '"-z",' in linea:
                proceso1 = proceso2 = proceso3 = proceso4 = proceso5 = proceso6 = proceso7 = False

        with open(self.archivo_original, 'w') as archivo:
            archivo.writelines(lineas)




class GeneracionMundo:
    def __init__(self,filename,celdas):
        self.filename = filename
        self.celdas = celdas


    def generate_world_file(self):
        with open(self.filename, 'w') as file:
            file.write("""<?xml version="1.0" ?>
    <sdf version="1.6">
    <world name="default">
        <include>
        <uri>model://ground_plane</uri>
        </include>
        <include>
        <uri>model://sun</uri>
        </include>
    """)

            num_rows = len(self.celdas)
            num_cols = len(self.celdas[0])
            cube_count = 0  # Variable para contar los cubos y generar nombres únicos
            count = 0
            for i in range(num_rows):
                for j in range(num_cols):
                    if count > 4:
                    	count = 0
                    if self.celdas[i][j]:  # Si el estado es False
                        x = (i - num_rows / 2) * 0.4
                        y = (j - num_cols / 2) * 0.4
                        cube_name = f"cube_{cube_count}"  # Nombre único para cada cubo
                        file.write(f"""
        <include>
        <uri>model://cube_traslucid_{count}</uri>
        <name>{cube_name}</name>
        <pose>{x} {y} 0 0 0 0</pose>
        </include>
    """)
                        cube_count += 1  # Incrementar el contador de cubos
                        count += 1
                        
            # Generación de paredes alrededor del perímetro
            # Ancho del perímetro (pared) de un cubo
            wall_width = 0.4
            
            # Definir las dimensiones de la matriz ampliada para incluir las paredes
            expanded_num_rows = num_rows + 2
            expanded_num_cols = num_cols + 2
            
            # Iterar para generar las paredes
            for i in range(expanded_num_rows):
                for j in range(expanded_num_cols):
                    if i == 0 or j == 0 or i == expanded_num_rows - 1 or j == expanded_num_cols - 1:
                        if not (0 < i < expanded_num_rows - 1 and 0 < j < expanded_num_cols - 1 and not self.celdas[i-1][j-1][0]):
                            x = (i - expanded_num_rows / 2) * 0.4
                            y = (j - expanded_num_cols / 2) * 0.4
                            cube_name = f"cube_wall_{cube_count}"  # Nombre único para cada cubo de pared
                            file.write(f"""
        <include>
        <uri>model://cube</uri>
        <name>{cube_name}</name>
        <pose>{x} {y} 0 0 0 0</pose>
        </include>
    """)
                            cube_count += 1  # Incrementar el contador de cubos
            
            file.write("""
    </world>
    </sdf>
    """)
    
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

                   
if __name__ == "__main__":
    celdas = [
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
    grafop =graph(celdas)
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
    
    inicio = SpawnOrigin('/home/user/robotPrueba/src/modelo_robot/launch/gazebo.launch.py', celdas,grafop, 'B')
    inicio.guardarValores()

    mundo = GeneracionMundo('/home/user/robotPrueba/install/modelo_robot/share/modelo_robot/worlds/mundoNodos.world', celdas)
    mundo.generate_world_file()


